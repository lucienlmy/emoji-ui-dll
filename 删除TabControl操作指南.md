# 删除TabControl代码 - 操作指南

## 方案说明

由于TabControl与Direct2D的冲突问题难以解决，建议删除所有TabControl代码，只保留基本功能。

## 需要删除的代码段

### 1. emoji_window.h

**删除以下行：**

```cpp
// 第23行附近
typedef void (__stdcall *TAB_CALLBACK)(HWND hTabControl, int selectedIndex);

// 第141-148行附近
struct TabPageInfo {
    int index;
    std::wstring title;
    std::vector<EmojiButton> buttons;
    std::vector<HWND> childWindows;
    bool visible;
};

// 第150-159行附近
struct TabControlState {
    HWND hTabControl;
    HWND hParent;
    HWND hContainerWindow;
    ID2D1HwndRenderTarget* render_target;
    IDWriteFactory* dwrite_factory;
    std::vector<TabPageInfo> pages;
    int currentIndex;
    TAB_CALLBACK callback;
};

// 第163行附近
extern std::map<HWND, TabControlState*> g_tab_controls;

// 第195-245行附近 - 所有TabControl函数声明
HWND __stdcall CreateTabControl(...);
int __stdcall AddTabItem(...);
BOOL __stdcall RemoveTabItem(...);
void __stdcall SetTabCallback(...);
int __stdcall GetCurrentTabIndex(...);
BOOL __stdcall SelectTab(...);
int __stdcall GetTabCount(...);
HWND __stdcall GetTabContentWindow(...);
void __stdcall DestroyTabControl(...);
BOOL __stdcall AddChildWindowToCurrentTab(...);

// 第330-332行附近
void UpdateTabLayout(TabControlState* state);
LRESULT CALLBACK TabControlParentSubclassProc(...);
```

### 2. emoji_window.cpp

**删除以下代码段：**

1. **全局变量**（第30行附近）：
```cpp
std::map<HWND, TabControlState*> g_tab_controls;
```

2. **所有TabControl函数实现**（约1100-1600行）：
   - `CreateTabControl`
   - `AddTabItem`
   - `RemoveTabItem`
   - `SetTabCallback`
   - `GetCurrentTabIndex`
   - `SelectTab`
   - `GetTabCount`
   - `GetTabContentWindow`
   - `DestroyTabControl`
   - `AddChildWindowToCurrentTab`
   - `UpdateTabLayout`
   - `TabControlParentSubclassProc`

3. **WM_PAINT中的TabControl检查代码**（第165-230行附近）：
删除检查是否是TabControl容器窗口的代码，只保留普通窗口的绘制逻辑。

4. **WM_LBUTTONDOWN/UP/MOUSEMOVE中的TabControl代码**（第240-350行附近）：
删除TabControl容器窗口的按钮处理代码。

5. **create_emoji_button_bytes中的TabControl代码**（第406-470行附近）：
删除检查是否是TabControl容器窗口的代码。

### 3. emoji_window.def

**删除以下导出：**

```
CreateTabControl
AddTabItem
RemoveTabItem
SetTabCallback
GetCurrentTabIndex
SelectTab
GetTabCount
GetTabContentWindow
DestroyTabControl
AddChildWindowToCurrentTab
```

## 简化后的.def文件

```
LIBRARY emoji_window
EXPORTS
    create_window
    create_emoji_button_bytes
    set_button_click_callback
    run_message_loop
    destroy_window
    set_window_icon
    show_message_box_bytes
    show_confirm_box_bytes
    CreateEmojiEdit
    SetEmojiEditText
    GetEmojiEditTextLength
    GetEmojiEditText
    SetEmojiEditFont
    SetEmojiEditColors
    SetEmojiEditStyle
    SetEmojiEditScroll
    GetEmojiEditScrollInfo
    SetEmojiEditSelection
    GetEmojiEditSelection
    SetEmojiEditCursorPos
    GetEmojiEditCursorPos
    SetEmojiEditFocus
    ClearEmojiEdit
    DestroyEmojiEdit
```

## 编译命令

删除代码后，使用以下命令编译：

```cmd
cd /d "T:\易语言源码\API创建窗口\emoji_window_cpp\emoji_window"
cl.exe /LD /O2 /MD /EHsc emoji_window.cpp /link d2d1.lib dwrite.lib /DEF:emoji_window.def /OUT:emoji_window.dll
copy emoji_window.dll "..\emoji_window.dll"
```

## 替代方案 - 使用易语言Tab控件

如果需要Tab功能，使用易语言自带的超级列表框：

```易语言
.版本 2

.程序集 窗口程序集_窗口1
.程序集变量 窗口句柄, 整数型
.程序集变量 编辑框句柄, 整数型
.程序集变量 按钮区域句柄, 整数型

.子程序 _按钮1_被单击

' 创建主窗口
窗口句柄 ＝ 创建Emoji窗口 ("简化版演示", 900, 650)

' 创建按钮区域（普通窗口）
按钮区域句柄 ＝ CreateWindowExA (0, "STATIC", "", #子窗口 ＋ #可视, 30, 80, 840, 520, 窗口句柄, 0, GetModuleHandleA (0), 0)

' 在按钮区域创建按钮
创建Emoji按钮_字节集 (按钮区域句柄, ...)

' 创建编辑框（初始隐藏）
编辑框句柄 ＝ 创建编辑框_ (窗口句柄, 30, 80, 840, 520)
ShowWindow (编辑框句柄, 0)  ' 隐藏

' 创建Tab切换按钮
' 按钮1：显示按钮区域
' 按钮2：显示编辑框

运行消息循环 ()

.子程序 切换到按钮区域
ShowWindow (编辑框句柄, 0)
ShowWindow (按钮区域句柄, 5)

.子程序 切换到编辑框
ShowWindow (按钮区域句柄, 0)
ShowWindow (编辑框句柄, 5)
```

## 总结

删除TabControl后，DLL将更加稳定和简单。如果需要Tab功能，使用易语言自带的控件或手动管理窗口显示/隐藏。
