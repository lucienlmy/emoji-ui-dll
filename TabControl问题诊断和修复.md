# TabControl 问题诊断和修复方案

## 问题描述

1. **Tab1的按钮显示在Tab2中** - 切换到Tab2时，Tab1的按钮仍然可见
2. **编辑框没有显示** - 在Tab2中创建的编辑框不可见

## 根本原因分析

### 问题1：按钮重叠显示

**原因**：
- Tab内容窗口使用 `WS_CHILD | WS_VISIBLE` 创建
- 所有Tab内容窗口都是父窗口的子窗口，位置重叠
- `UpdateTabLayout` 函数虽然调用了 `SetWindowPos` 隐藏非当前Tab，但可能存在时序问题
- 按钮是通过Direct2D绘制的，不是真正的子窗口，所以即使父窗口隐藏，绘制可能仍然发生

**关键代码位置**：
```cpp
// UpdateTabLayout 函数中
SetWindowPos(
    page.hContentWindow,
    HWND_BOTTOM,
    0, 0, 0, 0,
    SWP_NOMOVE | SWP_NOSIZE | SWP_HIDEWINDOW  // 隐藏非当前Tab
);
```

### 问题2：编辑框不显示

**原因**：
- 编辑框是Tab2内容窗口的子窗口
- 编辑框使用相对坐标 (30, 30, 760, 200)
- 但Tab2内容窗口可能：
  1. 没有正确显示（被Tab1内容窗口遮挡）
  2. 大小为0（渲染目标创建失败）
  3. Z顺序不正确

## 修复方案

### 方案1：强制刷新和Z顺序管理（推荐）

修改 `UpdateTabLayout` 函数，确保：
1. 先隐藏所有非当前Tab
2. 再显示当前Tab
3. 强制刷新所有窗口

```cpp
void UpdateTabLayout(TabControlState* state) {
    if (!state || !state->hTabControl) return;

    // 获取显示区域
    RECT rcTab;
    GetClientRect(state->hTabControl, &rcTab);
    TabCtrl_AdjustRect(state->hTabControl, FALSE, &rcTab);

    // 转换坐标
    POINT pt = { rcTab.left, rcTab.top };
    MapWindowPoints(state->hTabControl, state->hParent, &pt, 1);
    rcTab.left = pt.x;
    rcTab.top = pt.y;

    POINT pt2 = { rcTab.right, rcTab.bottom };
    MapWindowPoints(state->hTabControl, state->hParent, &pt2, 1);
    rcTab.right = pt2.x;
    rcTab.bottom = pt2.y;

    int contentWidth = rcTab.right - rcTab.left;
    int contentHeight = rcTab.bottom - rcTab.top;

    // ========== 关键修复：分两步处理 ==========
    
    // 第一步：隐藏所有非当前Tab的窗口
    for (size_t i = 0; i < state->pages.size(); i++) {
        if ((int)i != state->currentIndex) {
            TabPageInfo& page = state->pages[i];
            if (page.hContentWindow && IsWindow(page.hContentWindow)) {
                // 使用 ShowWindow 而不是 SetWindowPos
                ShowWindow(page.hContentWindow, SW_HIDE);
                page.visible = false;
            }
        }
    }

    // 第二步：显示并更新当前Tab
    if (state->currentIndex >= 0 && state->currentIndex < (int)state->pages.size()) {
        TabPageInfo& page = state->pages[state->currentIndex];
        if (page.hContentWindow && IsWindow(page.hContentWindow)) {
            // 先设置位置和大小
            SetWindowPos(
                page.hContentWindow,
                HWND_TOP,
                rcTab.left,
                rcTab.top,
                contentWidth,
                contentHeight,
                SWP_NOACTIVATE
            );

            // 再显示窗口
            ShowWindow(page.hContentWindow, SW_SHOW);
            page.visible = true;

            // 更新渲染目标
            auto win_it = g_windows.find(page.hContentWindow);
            if (win_it != g_windows.end()) {
                WindowState* win_state = win_it->second;
                if (win_state) {
                    if (!win_state->render_target && contentWidth > 0 && contentHeight > 0) {
                        g_d2d_factory->CreateHwndRenderTarget(
                            D2D1::RenderTargetProperties(),
                            D2D1::HwndRenderTargetProperties(
                                page.hContentWindow,
                                D2D1::SizeU(contentWidth, contentHeight)
                            ),
                            &win_state->render_target
                        );
                    } else if (win_state->render_target) {
                        win_state->render_target->Resize(D2D1::SizeU(contentWidth, contentHeight));
                    }
                }
            }

            // 强制刷新窗口和所有子窗口
            InvalidateRect(page.hContentWindow, nullptr, TRUE);
            UpdateWindow(page.hContentWindow);
            
            // 刷新所有子窗口（包括编辑框）
            EnumChildWindows(page.hContentWindow, [](HWND hwnd, LPARAM lParam) -> BOOL {
                InvalidateRect(hwnd, nullptr, TRUE);
                UpdateWindow(hwnd);
                return TRUE;
            }, 0);
        }
    }
}
```

### 方案2：修改窗口过程，确保隐藏时不绘制

在 `WindowProc` 的 `WM_PAINT` 处理中添加可见性检查：

```cpp
case WM_PAINT: {
    if (state) {
        // 检查窗口是否可见
        if (!IsWindowVisible(hwnd)) {
            // 窗口不可见，不绘制
            PAINTSTRUCT ps;
            BeginPaint(hwnd, &ps);
            EndPaint(hwnd, &ps);
            return 0;
        }

        PAINTSTRUCT ps;
        BeginPaint(hwnd, &ps);

        if (state->render_target) {
            state->render_target->BeginDraw();
            state->render_target->Clear(D2D1::ColorF(D2D1::ColorF::White));

            for (const auto& button : state->buttons) {
                DrawButton(state->render_target, state->dwrite_factory, button);
            }

            state->render_target->EndDraw();
        }

        EndPaint(hwnd, &ps);
    }
    return 0;
}
```

### 方案3：调试输出（用于诊断）

在易语言代码中添加调试输出：

```易语言
.子程序 Tab切换回调, , 公开
.参数 TabControl, 整数型
.参数 当前索引, 整数型
.局部变量 Tab1窗口, 整数型
.局部变量 Tab2窗口, 整数型

调试输出 ("Tab切换到索引: " ＋ 到文本 (当前索引))

' 获取各Tab的内容窗口句柄
Tab1窗口 ＝ 获取Tab内容窗口 (TabControl, 0)
Tab2窗口 ＝ 获取Tab内容窗口 (TabControl, 1)

调试输出 ("Tab1窗口句柄: " ＋ 到文本 (Tab1窗口))
调试输出 ("Tab2窗口句柄: " ＋ 到文本 (Tab2窗口))

' 检查窗口可见性
调试输出 ("Tab1可见: " ＋ 到文本 (是否窗口可见 (Tab1窗口)))
调试输出 ("Tab2可见: " ＋ 到文本 (是否窗口可见 (Tab2窗口)))

' 检查编辑框
.如果真 (当前索引 ＝ 1)
    调试输出 ("编辑框句柄: " ＋ 到文本 (编辑框句柄))
    调试输出 ("编辑框可见: " ＋ 到文本 (是否窗口可见 (编辑框句柄)))
.如果真结束
```

## 立即可用的临时解决方案

在易语言代码中，Tab切换回调里手动隐藏/显示窗口：

```易语言
.子程序 Tab切换回调, , 公开
.参数 TabControl, 整数型
.参数 当前索引, 整数型
.局部变量 Tab1窗口, 整数型
.局部变量 Tab2窗口, 整数型

调试输出 ("Tab切换到索引: " ＋ 到文本 (当前索引))

' 获取所有Tab的内容窗口
Tab1窗口 ＝ 获取Tab内容窗口 (TabControl, 0)
Tab2窗口 ＝ 获取Tab内容窗口 (TabControl, 1)

' 手动控制显示/隐藏
.判断开始 (当前索引 ＝ 0)
    ' 显示Tab1，隐藏Tab2
    ShowWindow (Tab1窗口, 5)  ' SW_SHOW = 5
    ShowWindow (Tab2窗口, 0)  ' SW_HIDE = 0
.判断 (当前索引 ＝ 1)
    ' 隐藏Tab1，显示Tab2
    ShowWindow (Tab1窗口, 0)  ' SW_HIDE = 0
    ShowWindow (Tab2窗口, 5)  ' SW_SHOW = 5
    
    ' 强制刷新Tab2及其子窗口
    InvalidateRect (Tab2窗口, 0, 1)
    UpdateWindow (Tab2窗口)
    
    ' 如果编辑框存在，也刷新它
    .如果真 (编辑框句柄 ≠ 0)
        ShowWindow (编辑框句柄, 5)
        InvalidateRect (编辑框句柄, 0, 1)
        UpdateWindow (编辑框句柄)
    .如果真结束
.判断结束
```

需要添加的DLL命令：

```易语言
.DLL命令 ShowWindow, 逻辑型, "user32.dll", "ShowWindow"
    .参数 窗口句柄, 整数型
    .参数 显示命令, 整数型

.DLL命令 InvalidateRect, 逻辑型, "user32.dll", "InvalidateRect"
    .参数 窗口句柄, 整数型
    .参数 矩形指针, 整数型
    .参数 是否擦除背景, 逻辑型

.DLL命令 UpdateWindow, 逻辑型, "user32.dll", "UpdateWindow"
    .参数 窗口句柄, 整数型

.DLL命令 是否窗口可见, 逻辑型, "user32.dll", "IsWindowVisible"
    .参数 窗口句柄, 整数型
```

## 推荐实施步骤

1. **立即测试**：先使用临时解决方案（在易语言回调中手动控制）
2. **验证问题**：添加调试输出，确认窗口句柄和可见性
3. **修改DLL**：如果临时方案有效，则修改DLL的 `UpdateTabLayout` 函数
4. **重新编译**：编译新的 emoji_window.dll
5. **最终测试**：移除临时代码，使用修复后的DLL

## 预期结果

修复后应该实现：
- 切换到Tab1时，只显示Tab1的按钮
- 切换到Tab2时，只显示Tab2的编辑框和按钮
- 没有窗口重叠或内容混乱
