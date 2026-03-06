# 最终修复方案 - Z顺序问题

## 问题确认

根据你的反馈：
1. **按钮有时隐藏有时还在** - 隐藏逻辑有效但不稳定
2. **鼠标变成编辑指针** - 编辑框存在且位置正确
3. **编辑框视觉上不可见** - 被Tab1窗口遮挡

## 根本原因

**Z顺序（窗口层叠顺序）问题**：

所有Tab内容窗口都在同一位置重叠。即使Tab1窗口被隐藏，它仍然在Z顺序的上层，遮挡了Tab2窗口和编辑框。

```
视觉效果：
┌─────────────────┐
│ Tab1窗口（隐藏） │ ← 在上层，遮挡下面的内容
├─────────────────┤
│ Tab2窗口（显示） │ ← 被遮挡
│  └─编辑框       │ ← 被遮挡（但鼠标能检测到）
└─────────────────┘
```

## 解决方案

### 关键修改：UpdateTabLayout函数

**核心思路**：
1. 先将所有非当前Tab移到 `HWND_BOTTOM`（最底层）
2. 清空它们的渲染内容
3. 再将当前Tab移到 `HWND_TOP`（最顶层）
4. 强制刷新所有子窗口

**修改后的代码**：

```cpp
void UpdateTabLayout(TabControlState* state) {
    // ... 获取显示区域 ...

    // 第一步：将所有非当前Tab移到底部并隐藏
    for (size_t i = 0; i < state->pages.size(); i++) {
        if ((int)i != state->currentIndex) {
            TabPageInfo& page = state->pages[i];
            if (page.hContentWindow && IsWindow(page.hContentWindow)) {
                // ✅ 先移到底部（关键！）
                SetWindowPos(
                    page.hContentWindow,
                    HWND_BOTTOM,  // 移到最底层
                    0, 0, 0, 0,
                    SWP_NOMOVE | SWP_NOSIZE | SWP_NOACTIVATE
                );
                
                // ✅ 再隐藏
                ShowWindow(page.hContentWindow, SW_HIDE);
                page.visible = false;
                
                // ✅ 清空渲染内容（防止残留）
                auto win_it = g_windows.find(page.hContentWindow);
                if (win_it != g_windows.end()) {
                    WindowState* win_state = win_it->second;
                    if (win_state && win_state->render_target) {
                        win_state->render_target->BeginDraw();
                        win_state->render_target->Clear(D2D1::ColorF(0.0f, 0.0f, 0.0f, 0.0f));
                        win_state->render_target->EndDraw();
                    }
                }
                InvalidateRect(page.hContentWindow, nullptr, TRUE);
            }
        }
    }

    // 第二步：显示当前Tab并移到顶部
    if (state->currentIndex >= 0 && state->currentIndex < (int)state->pages.size()) {
        TabPageInfo& page = state->pages[state->currentIndex];
        if (page.hContentWindow && IsWindow(page.hContentWindow)) {
            // ✅ 先设置位置、大小并移到顶部（关键！）
            SetWindowPos(
                page.hContentWindow,
                HWND_TOP,  // 移到最顶层
                rcTab.left,
                rcTab.top,
                contentWidth,
                contentHeight,
                SWP_NOACTIVATE
            );
            
            // ✅ 再显示窗口
            ShowWindow(page.hContentWindow, SW_SHOW);
            page.visible = true;

            // ... 更新渲染目标 ...
            
            // ✅ 强制刷新所有子窗口（包括编辑框）
            InvalidateRect(page.hContentWindow, nullptr, TRUE);
            UpdateWindow(page.hContentWindow);
            
            HWND hChild = GetWindow(page.hContentWindow, GW_CHILD);
            while (hChild) {
                InvalidateRect(hChild, nullptr, TRUE);
                UpdateWindow(hChild);
                hChild = GetWindow(hChild, GW_HWNDNEXT);
            }
        }
    }
}
```

### 其他修改

#### 1. WM_PAINT中的可见性检查
```cpp
case WM_PAINT: {
    if (IsWindowVisible(hwnd)) {
        // 绘制按钮
    } else {
        // 清空为透明
        state->render_target->Clear(D2D1::ColorF(0.0f, 0.0f, 0.0f, 0.0f));
    }
}
```

#### 2. WM_SHOWWINDOW消息处理
```cpp
case WM_SHOWWINDOW: {
    if (!wparam) {  // 窗口被隐藏
        // 立即清空内容
        state->render_target->Clear(D2D1::ColorF(0.0f, 0.0f, 0.0f, 0.0f));
    }
    InvalidateRect(hwnd, nullptr, TRUE);
}
```

## 为什么这次应该有效

### 1. Z顺序控制
- `HWND_BOTTOM` 确保隐藏的窗口在最底层
- `HWND_TOP` 确保当前Tab在最顶层
- 即使窗口重叠，也不会互相遮挡

### 2. 渲染内容清空
- 隐藏窗口时清空Direct2D渲染内容
- 防止残留的按钮图像显示

### 3. 子窗口刷新
- 遍历并刷新所有子窗口（编辑框）
- 确保编辑框正确显示

### 4. 多重保障
- WM_PAINT检查可见性
- WM_SHOWWINDOW清空内容
- UpdateTabLayout控制Z顺序
- 三重保障确保问题解决

## 编译和测试

### 1. 重新编译DLL

```cmd
cd /d "T:\易语言源码\API创建窗口\emoji_window_cpp\emoji_window"

cl.exe /LD /O2 /MD /EHsc emoji_window.cpp ^
    /link d2d1.lib dwrite.lib comctl32.lib uxtheme.lib ^
    /OUT:emoji_window.dll
```

### 2. 替换DLL

```cmd
copy emoji_window.dll "..\emoji_window.dll"
```

### 3. 测试

运行程序，切换到Tab2（编辑框），检查：

✅ **预期结果**：
- Tab1的所有按钮完全消失
- 编辑框清晰可见
- 可以在编辑框中输入文字
- 鼠标在编辑框上显示编辑指针
- 操作按钮正常工作

## 如果还有问题

如果这次修改后仍然有问题，可能需要：

1. **检查窗口样式**：
   - 确认Tab内容窗口没有 `WS_EX_TRANSPARENT` 样式
   - 确认没有其他窗口在上层

2. **使用Spy++工具**：
   - 查看窗口的Z顺序
   - 确认窗口的可见性标志
   - 检查窗口的位置和大小

3. **添加调试输出**：
   ```cpp
   OutputDebugStringA("Tab1 moved to BOTTOM\n");
   OutputDebugStringA("Tab2 moved to TOP\n");
   ```

请重新编译测试，告诉我结果！
