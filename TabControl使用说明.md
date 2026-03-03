# TabControl DLL 使用说明

## 概述

这是一个为易语言设计的 TabControl（选项卡控件）DLL，集成在 `emoji_window.dll` 中。它提供了类似 Vue Element UI 风格的现代化选项卡功能，支持动态添加/删除标签页，并且切换时内容会被保留（不销毁）。

## 核心特性

✅ **现代视觉样式** - 使用 Windows XP/Vista+ 的现代主题（Explorer 样式）
✅ **内容保留机制** - 切换 Tab 时隐藏而非销毁内容窗口，数据和状态完整保留
✅ **动态管理** - 支持运行时添加、删除 Tab 页
✅ **回调通知** - Tab 切换时触发回调函数，通知易语言当前选中的索引
✅ **自动焦点管理** - 删除当前 Tab 时自动切换到相邻 Tab
✅ **UTF-8 支持** - 完美支持中文和 Unicode 字符
✅ **32位兼容** - 使用 stdcall 调用约定，完美兼容易语言

## API 函数列表

### 1. CreateTabControl - 创建 TabControl

```c++
HWND CreateTabControl(HWND hParent, int x, int y, int width, int height)
```

**参数：**
- `hParent` - 父窗口句柄
- `x` - X 坐标
- `y` - Y 坐标
- `width` - 宽度
- `height` - 高度

**返回值：** TabControl 窗口句柄

**易语言声明：**
```
.DLL命令 CreateTabControl, 整数型, , "CreateTabControl"
    .参数 父窗口句柄, 整数型
    .参数 X坐标, 整数型
    .参数 Y坐标, 整数型
    .参数 宽度, 整数型
    .参数 高度, 整数型
```

---

### 2. AddTabItem - 添加 Tab 页

```c++
int AddTabItem(HWND hTabControl, const unsigned char* title_bytes, int title_len, HWND hContentWindow)
```

**参数：**
- `hTabControl` - TabControl 句柄
- `title_bytes` - 标题字节集（UTF-8 编码）
- `title_len` - 标题字节长度
- `hContentWindow` - 内容窗口句柄（可选，传 0 则自动创建 STATIC 窗口）

**返回值：** 新 Tab 的索引（从 0 开始），失败返回 -1

**易语言声明：**
```
.DLL命令 AddTabItem, 整数型, , "AddTabItem"
    .参数 TabControl句柄, 整数型
    .参数 标题字节集, 字节集
    .参数 标题长度, 整数型
    .参数 内容窗口句柄, 整数型, , 可选，传0则自动创建
```

**易语言示例：**
```
.变量 标题, 字节集
标题 = 到字节集("首页")
AddTabItem(TabControl句柄, 标题, 取字节集长度(标题), 内容窗口句柄)
```

---

### 3. RemoveTabItem - 移除 Tab 页

```c++
BOOL RemoveTabItem(HWND hTabControl, int index)
```

**参数：**
- `hTabControl` - TabControl 句柄
- `index` - 要删除的 Tab 索引

**返回值：** 成功返回 TRUE，失败返回 FALSE

**易语言声明：**
```
.DLL命令 RemoveTabItem, 逻辑型, , "RemoveTabItem"
    .参数 TabControl句柄, 整数型
    .参数 索引, 整数型
```

**注意事项：**
- 删除 Tab 时会自动销毁其内容窗口
- 如果删除的是当前选中的 Tab，会自动切换到前一个 Tab（如果是第一个则切换到新的第一个）
- 删除后会自动触发回调函数

---

### 4. SetTabCallback - 设置 Tab 切换回调

```c++
void SetTabCallback(HWND hTabControl, TAB_CALLBACK pCallback)
```

**回调函数原型：**
```c++
typedef void (__stdcall *TAB_CALLBACK)(HWND hTabControl, int selectedIndex);
```

**参数：**
- `hTabControl` - TabControl 句柄
- `pCallback` - 回调函数指针

**易语言声明：**
```
.DLL命令 SetTabCallback, , , "SetTabCallback"
    .参数 TabControl句柄, 整数型
    .参数 回调函数指针, 整数型

.子程序 Tab切换回调, , 公开
    .参数 TabControl, 整数型
    .参数 当前索引, 整数型

    调试输出("Tab切换到索引: " + 到文本(当前索引))
```

**易语言使用：**
```
SetTabCallback(TabControl句柄, &Tab切换回调)
```

---

### 5. GetCurrentTabIndex - 获取当前选中的 Tab 索引

```c++
int GetCurrentTabIndex(HWND hTabControl)
```

**参数：**
- `hTabControl` - TabControl 句柄

**返回值：** 当前选中的 Tab 索引，失败返回 -1

**易语言声明：**
```
.DLL命令 GetCurrentTabIndex, 整数型, , "GetCurrentTabIndex"
    .参数 TabControl句柄, 整数型
```

---

### 6. SelectTab - 切换到指定 Tab

```c++
BOOL SelectTab(HWND hTabControl, int index)
```

**参数：**
- `hTabControl` - TabControl 句柄
- `index` - 目标 Tab 索引

**返回值：** 成功返回 TRUE，失败返回 FALSE

**易语言声明：**
```
.DLL命令 SelectTab, 逻辑型, , "SelectTab"
    .参数 TabControl句柄, 整数型
    .参数 索引, 整数型
```

---

### 7. GetTabCount - 获取 Tab 数量

```c++
int GetTabCount(HWND hTabControl)
```

**参数：**
- `hTabControl` - TabControl 句柄

**返回值：** Tab 总数

**易语言声明：**
```
.DLL命令 GetTabCount, 整数型, , "GetTabCount"
    .参数 TabControl句柄, 整数型
```

---

### 8. GetTabContentWindow - 获取指定 Tab 的内容窗口句柄

```c++
HWND GetTabContentWindow(HWND hTabControl, int index)
```

**参数：**
- `hTabControl` - TabControl 句柄
- `index` - Tab 索引

**返回值：** 内容窗口句柄，失败返回 NULL

**易语言声明：**
```
.DLL命令 GetTabContentWindow, 整数型, , "GetTabContentWindow"
    .参数 TabControl句柄, 整数型
    .参数 索引, 整数型
```

---

### 9. DestroyTabControl - 销毁 TabControl

```c++
void DestroyTabControl(HWND hTabControl)
```

**参数：**
- `hTabControl` - TabControl 句柄

**易语言声明：**
```
.DLL命令 DestroyTabControl, , , "DestroyTabControl"
    .参数 TabControl句柄, 整数型
```

**注意事项：**
- 会自动销毁所有内容窗口
- 会清理所有内部资源
- 建议在窗口关闭时调用

---

## 完整易语言示例

```
.版本 2

.程序集 窗口程序集_启动窗口

.程序集变量 TabControl句柄, 整数型
.程序集变量 编辑框1, 整数型
.程序集变量 编辑框2, 整数型
.程序集变量 编辑框3, 整数型

.子程序 _启动窗口_创建完毕

' 创建 TabControl
TabControl句柄 = CreateTabControl(取窗口句柄(), 10, 10, 600, 400)

' 创建内容窗口（使用编辑框）
编辑框1 = 创建窗口(#编辑框, "第一个Tab的内容", #子窗口 + #可视 + #多行编辑, 0, 0, 0, 0, 取窗口句柄(), 0)
编辑框2 = 创建窗口(#编辑框, "第二个Tab的内容", #子窗口 + #可视 + #多行编辑, 0, 0, 0, 0, 取窗口句柄(), 0)
编辑框3 = 创建窗口(#编辑框, "第三个Tab的内容", #子窗口 + #可视 + #多行编辑, 0, 0, 0, 0, 取窗口句柄(), 0)

' 添加 Tab 页
.变量 标题1, 字节集
.变量 标题2, 字节集
.变量 标题3, 字节集

标题1 = 到字节集("首页")
标题2 = 到字节集("设置")
标题3 = 到字节集("关于")

AddTabItem(TabControl句柄, 标题1, 取字节集长度(标题1), 编辑框1)
AddTabItem(TabControl句柄, 标题2, 取字节集长度(标题2), 编辑框2)
AddTabItem(TabControl句柄, 标题3, 取字节集长度(标题3), 编辑框3)

' 设置回调
SetTabCallback(TabControl句柄, &Tab切换回调)

.子程序 Tab切换回调, , 公开
    .参数 TabControl, 整数型
    .参数 当前索引, 整数型

    调试输出("当前Tab索引: " + 到文本(当前索引))

.子程序 _启动窗口_将被销毁

' 清理资源
DestroyTabControl(TabControl句柄)
```

---

## 技术实现细节

### 1. 内容保留机制

TabControl 使用 **显示/隐藏** 而非 **创建/销毁** 的方式管理内容窗口：

```c++
if ((int)i == state->currentIndex) {
    // 显示当前选中的页面
    SetWindowPos(page.hContentWindow, HWND_TOP, ...);
    ShowWindow(page.hContentWindow, SW_SHOW);
} else {
    // 隐藏其他页面（但不销毁）
    ShowWindow(page.hContentWindow, SW_HIDE);
}
```

这确保了：
- ✅ 切换 Tab 时，隐藏的页面内容完整保留
- ✅ 用户输入的数据不会丢失
- ✅ 控件状态（滚动位置、选中项等）保持不变

### 2. 消息处理机制

使用 **子类化（Subclassing）** 技术拦截 TabControl 的消息：

```c++
SetWindowSubclass(hTabControl, TabControlSubclassProc, 0, (DWORD_PTR)state);
```

关键消息处理：
- `WM_NOTIFY` + `TCN_SELCHANGE` - 捕获 Tab 切换事件
- `WM_SIZE` - 窗口大小改变时自动调整内容区域
- `WM_DESTROY` - 清理子类化资源

### 3. 现代视觉样式

```c++
// 启用 Explorer 主题（现代扁平风格）
SetWindowTheme(hTabControl, L"Explorer", nullptr);

// 使用 Segoe UI 字体 + ClearType 抗锯齿
HFONT hFont = CreateFontW(-14, 0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE,
    DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS,
    CLEARTYPE_QUALITY, DEFAULT_PITCH | FF_DONTCARE, L"Segoe UI");
```

### 4. 内存管理

- 使用 `std::map` 管理 TabControl 状态
- 使用 `std::vector` 管理 Tab 页信息
- 销毁时自动清理所有资源

---

## 常见问题 (FAQ)

### Q1: 为什么内容窗口必须是子窗口？

**A:** 内容窗口必须使用 `WS_CHILD` 样式，因为：
- TabControl 需要控制其位置和大小
- 必须作为父窗口的子窗口才能正确显示在 Tab 区域内

### Q2: 如何在 Tab 页中放置多个控件？

**A:** 有两种方法：

**方法1：使用容器窗口**
```
' 创建一个容器窗口
容器窗口 = 创建窗口(#窗口, "", #子窗口 + #可视, 0, 0, 0, 0, 取窗口句柄(), 0)

' 在容器窗口中创建多个控件
按钮1 = 创建窗口(#按钮, "按钮1", #子窗口 + #可视, 10, 10, 100, 30, 容器窗口, 0)
编辑框1 = 创建窗口(#编辑框, "", #子窗口 + #可视, 10, 50, 200, 100, 容器窗口, 0)

' 将容器窗口添加到 Tab
AddTabItem(TabControl句柄, 标题, 长度, 容器窗口)
```

**方法2：传 0 让 DLL 自动创建，然后获取句柄**
```
索引 = AddTabItem(TabControl句柄, 标题, 长度, 0)
内容窗口 = GetTabContentWindow(TabControl句柄, 索引)

' 在内容窗口中创建控件
按钮1 = 创建窗口(#按钮, "按钮1", #子窗口 + #可视, 10, 10, 100, 30, 内容窗口, 0)
```

### Q3: 删除 Tab 时内容窗口会被销毁吗？

**A:** 是的，`RemoveTabItem` 会自动销毁内容窗口。如果需要保留窗口，请在删除前：
1. 使用 `GetTabContentWindow` 获取窗口句柄
2. 使用 `SetParent` 将窗口移到其他父窗口
3. 然后再调用 `RemoveTabItem`

### Q4: 如何动态修改 Tab 标题？

**A:** 目前 DLL 不提供修改标题的接口，但可以使用 Windows API：

```
' 使用 SendMessage 修改 Tab 标题
.DLL命令 SendMessageW, 整数型, "user32.dll", "SendMessageW"
    .参数 窗口句柄, 整数型
    .参数 消息, 整数型
    .参数 wParam, 整数型
    .参数 lParam, 整数型

' TCM_SETITEMW = 0x133D
' TCIF_TEXT = 0x0001
```

### Q5: 回调函数为什么没有被触发？

**A:** 检查以下几点：
1. 确保回调函数声明为 **公开** 子程序
2. 确保使用 `&函数名` 传递函数指针
3. 确保回调函数参数类型正确（两个整数型参数）

---

## 编译说明

### Visual Studio 编译设置

1. **平台配置：** Win32 (x86)
2. **字符集：** Unicode
3. **运行库：** 多线程 DLL (/MD)
4. **调用约定：** __stdcall
5. **链接库：** comctl32.lib, d2d1.lib, dwrite.lib, uxtheme.lib

### 项目文件

- `emoji_window.h` - 头文件（包含 TabControl 声明）
- `emoji_window.cpp` - 实现文件（包含 TabControl 实现）
- `dllmain.cpp` - DLL 入口点

---

## 版本历史

**v1.0 (2026-03-04)**
- ✅ 初始版本
- ✅ 支持创建、添加、删除 Tab
- ✅ 支持 Tab 切换回调
- ✅ 内容保留机制
- ✅ 现代视觉样式
- ✅ UTF-8 中文支持

---

## 许可证

本 DLL 集成在 emoji_window.dll 中，遵循原项目许可证。

---

## 技术支持

如有问题或建议，请联系开发者或提交 Issue。
