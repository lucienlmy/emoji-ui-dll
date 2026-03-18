# C# 调用规则

## DllImport 声明模式

使用常量简化声明，所有导入函数统一使用 `StdCall` 调用约定：

```csharp
private const string DLL = "emoji_window.dll";
private const CallingConvention CC = CallingConvention.StdCall;

[DllImport(DLL, CallingConvention = CC)]
public static extern IntPtr create_window_bytes(byte[] title, int titleLen, int w, int h);
```

不要写成：

```csharp
// ❌ 每个函数重复完整字符串
[DllImport("emoji_window.dll", CallingConvention = CallingConvention.StdCall)]
```

## byte[] 传递 UTF-8 文本

所有文本参数使用 `byte[]` + 长度传递，不使用 `string` 或 `StringBuilder`：

```csharp
byte[] titleBytes = Encoding.UTF8.GetBytes("🎨 窗口标题");
IntPtr hwnd = create_window_bytes(titleBytes, titleBytes.Length, 800, 600);
```

文本参数总是成对出现 `(byte[] data, int length)`：

```csharp
[DllImport(DLL, CallingConvention = CC)]
public static extern int CreateLabel(
    IntPtr parent, int x, int y, int w, int h,
    byte[] text, int textLen,     // 文本 + 长度
    uint fg, uint bg,
    byte[] font, int fontLen,     // 字体名 + 长度
    int fontSize, int bold, int italic, int underline,
    int align, int wordWrap
);
```

## 辅助方法

### ToUtf8 — 字符串转 UTF-8 字节数组

```csharp
public static byte[] ToUtf8(string s)
    => string.IsNullOrEmpty(s) ? Array.Empty<byte>() : Encoding.UTF8.GetBytes(s);
```

### ARGB — 构造颜色值

```csharp
public static uint ARGB(int a, int r, int g, int b)
    => (uint)((a << 24) | (r << 16) | (g << 8) | b);

// RGB 便捷版（Alpha 固定 255）
public static int RGB(int r, int g, int b)
    => (r << 16) | (g << 8) | b;
```

### GetText2Call — 通用两次调用

DLL 中获取文本类函数采用"两次调用"模式：
1. 第一次传 `IntPtr.Zero` 和 `0` 获取所需缓冲区长度
2. 第二次用 `Marshal.AllocHGlobal` 分配缓冲区后再调用获取实际数据

#### 基础版 — int 句柄

```csharp
public delegate int GetTextIntDelegate(int handle, IntPtr buf, int bufSize);

public static (byte[] data, int length) GetText2Call(GetTextIntDelegate func, int handle)
{
    int len = func(handle, IntPtr.Zero, 0);
    if (len <= 0) return (Array.Empty<byte>(), len);

    IntPtr buf = Marshal.AllocHGlobal(len);
    try
    {
        func(handle, buf, len);
        byte[] data = new byte[len];
        Marshal.Copy(buf, data, 0, len);
        return (data, len);
    }
    finally
    {
        Marshal.FreeHGlobal(buf);
    }
}

// 使用示例
var (textBytes, textLen) = GetText2Call(GetButtonText, buttonId);
string text = Encoding.UTF8.GetString(textBytes);
```

#### IntPtr 句柄版

```csharp
public delegate int GetTextPtrDelegate(IntPtr handle, IntPtr buf, int bufSize);

public static (byte[] data, int length) GetText2CallPtr(GetTextPtrDelegate func, IntPtr handle)
{
    int len = func(handle, IntPtr.Zero, 0);
    if (len <= 0) return (Array.Empty<byte>(), len);

    IntPtr buf = Marshal.AllocHGlobal(len);
    try
    {
        func(handle, buf, len);
        byte[] data = new byte[len];
        Marshal.Copy(buf, data, 0, len);
        return (data, len);
    }
    finally
    {
        Marshal.FreeHGlobal(buf);
    }
}

// 使用示例 — 窗口标题使用 IntPtr 句柄
var (titleBytes, _) = GetText2CallPtr(GetWindowTitle, hwnd);
string title = Encoding.UTF8.GetString(titleBytes);
```

#### 带索引版 — 列表框/组合框项目

```csharp
public delegate int GetItemTextDelegate(int handle, int index, IntPtr buf, int bufSize);

public static (byte[] data, int length) GetItemText2Call(GetItemTextDelegate func, int handle, int index)
{
    int len = func(handle, index, IntPtr.Zero, 0);
    if (len <= 0) return (Array.Empty<byte>(), len);

    IntPtr buf = Marshal.AllocHGlobal(len);
    try
    {
        func(handle, index, buf, len);
        byte[] data = new byte[len];
        Marshal.Copy(buf, data, 0, len);
        return (data, len);
    }
    finally
    {
        Marshal.FreeHGlobal(buf);
    }
}

// 使用示例
var (itemBytes, _) = GetItemText2Call(GetListItemText, listBoxId, 0);
var (comboBytes, _) = GetItemText2Call(GetComboItemText, comboId, selectedIndex);
```

#### 组合框当前文本版

```csharp
public delegate int GetComboTextDelegate(int handle, IntPtr buf, int bufSize);

public static (byte[] data, int length) GetComboText2Call(GetComboTextDelegate func, int handle)
{
    int len = func(handle, IntPtr.Zero, 0);
    if (len <= 0) return (Array.Empty<byte>(), len);

    IntPtr buf = Marshal.AllocHGlobal(len);
    try
    {
        func(handle, buf, len);
        byte[] data = new byte[len];
        Marshal.Copy(buf, data, 0, len);
        return (data, len);
    }
    finally
    {
        Marshal.FreeHGlobal(buf);
    }
}
```

#### GetCellText2Call — DataGridView 单元格

```csharp
public delegate int GetCellTextDelegate(int grid, int row, int col, IntPtr buf, int bufSize);

public static (byte[] data, int length) GetCellText2Call(GetCellTextDelegate func, int grid, int row, int col)
{
    int len = func(grid, row, col, IntPtr.Zero, 0);
    if (len <= 0) return (Array.Empty<byte>(), len);

    IntPtr buf = Marshal.AllocHGlobal(len);
    try
    {
        func(grid, row, col, buf, len);
        byte[] data = new byte[len];
        Marshal.Copy(buf, data, 0, len);
        return (data, len);
    }
    finally
    {
        Marshal.FreeHGlobal(buf);
    }
}

// 使用示例
var (cellBytes, _) = GetCellText2Call(DataGrid_GetCellText, gridId, row, col);
string cellText = Encoding.UTF8.GetString(cellBytes);
```

## 回调委托定义

所有回调委托必须标注 `[UnmanagedFunctionPointer]`：

```csharp
[UnmanagedFunctionPointer(CC)]
public delegate void ButtonClickCallback(int buttonId, IntPtr parentHwnd);

[UnmanagedFunctionPointer(CC)]
public delegate void MessageBoxCallback(int confirmed);

[UnmanagedFunctionPointer(CC)]
public delegate void CheckBoxCallback(int checkBoxId, int isChecked);

[UnmanagedFunctionPointer(CC)]
public delegate void ListBoxCallback(int hListBox, int index);

[UnmanagedFunctionPointer(CC)]
public delegate void ComboBoxCallback(int hComboBox, int index);

[UnmanagedFunctionPointer(CC)]
public delegate void DataGridCellCallback(int hGrid, int row, int col);

[UnmanagedFunctionPointer(CC)]
public delegate void DataGridColumnHeaderCallback(int hGrid, int col);
```

### 回调签名表

| 委托类型 | 参数 | 说明 |
|---------|------|------|
| `ButtonClickCallback` | `(int buttonId, IntPtr parentHwnd)` | 按钮点击 |
| `MessageBoxCallback` | `(int confirmed)` | 确认框结果（1=确认, 0=取消） |
| `CheckBoxCallback` | `(int checkBoxId, int isChecked)` | 复选框状态变更 |
| `ListBoxCallback` | `(int hListBox, int index)` | 列表框选中项变更 |
| `ComboBoxCallback` | `(int hComboBox, int index)` | 组合框选中项变更 |
| `DataGridCellCallback` | `(int hGrid, int row, int col)` | 单元格点击/双击/选中/值变更 |
| `DataGridColumnHeaderCallback` | `(int hGrid, int col)` | 列标题点击 |

## 委托防 GC

回调委托实例必须保存到 `static` 字段，防止被垃圾回收：

```csharp
// ✅ 正确 - static 字段保存
private static ButtonClickCallback _btnCallback;
private static DataGridCellCallback _cellClickCallback;

public void Init()
{
    _btnCallback = OnButtonClick;
    set_button_click_callback(_btnCallback);

    _cellClickCallback = OnCellClick;
    DataGrid_SetCellClickCallback(gridId, _cellClickCallback);
}

// ❌ 错误 - 局部变量，方法返回后被GC回收
public void Init()
{
    var cb = new ButtonClickCallback(OnButtonClick);
    set_button_click_callback(cb);  // cb 随时可能被回收！
}
```

多个同类型回调使用 `Dictionary` 或 `List` 保存：

```csharp
private static readonly Dictionary<int, CheckBoxCallback> _checkBoxCallbacks = new();

public void SetCheckBoxCallback(int checkBoxId, Action<int, int> handler)
{
    var cb = new CheckBoxCallback((id, state) => handler(id, state));
    _checkBoxCallbacks[checkBoxId] = cb;
    SetCheckBoxCallback(checkBoxId, cb);
}
```

## DllImport 函数分类速查

### 窗口

```csharp
[DllImport(DLL, CallingConvention = CC)] public static extern IntPtr create_window_bytes(byte[] title, int titleLen, int w, int h);
[DllImport(DLL, CallingConvention = CC)] public static extern IntPtr create_window_bytes_ex(byte[] title, int titleLen, int w, int h, int titlebarColor);
[DllImport(DLL, CallingConvention = CC)] public static extern void set_message_loop_main_window(IntPtr hwnd);
[DllImport(DLL, CallingConvention = CC)] public static extern int run_message_loop();
[DllImport(DLL, CallingConvention = CC)] public static extern void destroy_window(IntPtr hwnd);
[DllImport(DLL, CallingConvention = CC)] public static extern int GetWindowTitle(IntPtr hwnd, IntPtr buf, int bufSize);
[DllImport(DLL, CallingConvention = CC)] public static extern void GetWindowBounds(IntPtr hwnd, out int x, out int y, out int w, out int h);
```

### 按钮

```csharp
[DllImport(DLL, CallingConvention = CC)] public static extern int create_emoji_button_bytes(IntPtr parent, byte[] emoji, int emojiLen, byte[] text, int textLen, int x, int y, int w, int h, uint bgColor);
[DllImport(DLL, CallingConvention = CC)] public static extern void set_button_click_callback(ButtonClickCallback cb);
[DllImport(DLL, CallingConvention = CC)] public static extern int GetButtonText(int btnId, IntPtr buf, int bufSize);
[DllImport(DLL, CallingConvention = CC)] public static extern void SetButtonText(int btnId, byte[] text, int textLen);
```

### 标签

```csharp
[DllImport(DLL, CallingConvention = CC)] public static extern int CreateLabel(IntPtr parent, int x, int y, int w, int h, byte[] text, int textLen, uint fg, uint bg, byte[] font, int fontLen, int fontSize, int bold, int italic, int underline, int align, int wordWrap);
[DllImport(DLL, CallingConvention = CC)] public static extern void SetLabelText(int label, byte[] text, int textLen);
[DllImport(DLL, CallingConvention = CC)] public static extern int GetLabelText(int label, IntPtr buf, int bufSize);
```

### 复选框

```csharp
[DllImport(DLL, CallingConvention = CC)] public static extern int CreateCheckBox(IntPtr parent, int x, int y, int w, int h, byte[] text, int textLen, int isChecked, uint fg, uint bg, byte[] font, int fontLen, int fontSize, int bold, int italic, int underline);
[DllImport(DLL, CallingConvention = CC)] public static extern void SetCheckBoxCallback(int checkBoxId, CheckBoxCallback cb);
```

### 列表框

```csharp
[DllImport(DLL, CallingConvention = CC)] public static extern int CreateListBox(IntPtr parent, int x, int y, int w, int h, int multiSelect, uint fg, uint bg);
[DllImport(DLL, CallingConvention = CC)] public static extern int AddListItem(int listbox, byte[] text, int textLen);
[DllImport(DLL, CallingConvention = CC)] public static extern int GetListItemText(int listbox, int index, IntPtr buf, int bufSize);
[DllImport(DLL, CallingConvention = CC)] public static extern void SetListBoxCallback(int listbox, ListBoxCallback cb);
```

### 组合框

```csharp
[DllImport(DLL, CallingConvention = CC)] public static extern int CreateComboBox(IntPtr parent, int x, int y, int w, int h, int readOnly, uint fg, uint bg, int itemHeight, byte[] font, int fontLen, int fontSize, int bold, int italic, int underline);
[DllImport(DLL, CallingConvention = CC)] public static extern int AddComboItem(int combo, byte[] text, int textLen);
[DllImport(DLL, CallingConvention = CC)] public static extern int GetComboItemText(int combo, int index, IntPtr buf, int bufSize);
[DllImport(DLL, CallingConvention = CC)] public static extern int GetComboBoxText(int combo, IntPtr buf, int bufSize);
[DllImport(DLL, CallingConvention = CC)] public static extern void SetComboBoxCallback(int combo, ComboBoxCallback cb);
```

### DataGridView

```csharp
[DllImport(DLL, CallingConvention = CC)] public static extern int CreateDataGridView(IntPtr parent, int x, int y, int w, int h, int virtualMode, int alternateRowColor, uint fg, uint bg);
[DllImport(DLL, CallingConvention = CC)] public static extern int DataGrid_AddTextColumn(int grid, byte[] header, int headerLen, int width);
[DllImport(DLL, CallingConvention = CC)] public static extern int DataGrid_AddCheckBoxColumn(int grid, byte[] header, int headerLen, int width);
[DllImport(DLL, CallingConvention = CC)] public static extern int DataGrid_AddButtonColumn(int grid, byte[] header, int headerLen, int width);
[DllImport(DLL, CallingConvention = CC)] public static extern int DataGrid_AddRow(int grid);
[DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetCellText(int grid, int row, int col, byte[] text, int textLen);
[DllImport(DLL, CallingConvention = CC)] public static extern int DataGrid_GetCellText(int grid, int row, int col, IntPtr buf, int bufSize);
[DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetCellClickCallback(int grid, DataGridCellCallback cb);
[DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetCellDoubleClickCallback(int grid, DataGridCellCallback cb);
[DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetSelectionChangedCallback(int grid, DataGridCellCallback cb);
[DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetColumnHeaderClickCallback(int grid, DataGridColumnHeaderCallback cb);
[DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetCellValueChangedCallback(int grid, DataGridCellCallback cb);
```

### 信息框

```csharp
[DllImport(DLL, CallingConvention = CC)] public static extern void show_message_box_bytes(IntPtr parent, byte[] title, int titleLen, byte[] msg, int msgLen, byte[] icon, int iconLen);
[DllImport(DLL, CallingConvention = CC)] public static extern void show_confirm_box_bytes(IntPtr parent, byte[] title, int titleLen, byte[] msg, int msgLen, byte[] icon, int iconLen, MessageBoxCallback cb);
```

## 32位与64位注意事项

| 项目 | 说明 |
|------|------|
| DLL 版本 | 分 `x86` 和 `x64` 两个版本，分别在 `Release` 和 `x64/Release` 目录 |
| Platform Target | C# 项目的 **Platform Target** 必须与 DLL 位数匹配 |
| AnyCPU | 不建议使用 AnyCPU，应明确选择 x86 或 x64 |
| IntPtr 大小 | x86 下 `IntPtr` 为 4 字节，x64 下为 8 字节 |
| 运行时检查 | `IntPtr.Size == 4` 表示 32 位，`== 8` 表示 64 位 |

项目配置示例（.csproj）：

```xml
<!-- 32位项目 -->
<PropertyGroup>
  <PlatformTarget>x86</PlatformTarget>
</PropertyGroup>

<!-- 64位项目 -->
<PropertyGroup>
  <PlatformTarget>x64</PlatformTarget>
</PropertyGroup>
```

DLL 放置路径：将对应位数的 `emoji_window.dll` 放在项目输出目录（`bin/Debug` 或 `bin/Release`）中。

## 完整声明类模板

```csharp
using System;
using System.Runtime.InteropServices;
using System.Text;

public static class EmojiWindowNative
{
    private const string DLL = "emoji_window.dll";
    private const CallingConvention CC = CallingConvention.StdCall;

    // 辅助方法
    public static byte[] ToUtf8(string s)
        => string.IsNullOrEmpty(s) ? Array.Empty<byte>() : Encoding.UTF8.GetBytes(s);

    public static uint ARGB(int a, int r, int g, int b)
        => (uint)((a << 24) | (r << 16) | (g << 8) | b);

    // 回调委托
    [UnmanagedFunctionPointer(CC)] public delegate void ButtonClickCallback(int buttonId, IntPtr parentHwnd);
    [UnmanagedFunctionPointer(CC)] public delegate void MessageBoxCallback(int confirmed);
    [UnmanagedFunctionPointer(CC)] public delegate void CheckBoxCallback(int checkBoxId, int isChecked);

    // DllImport 声明
    [DllImport(DLL, CallingConvention = CC)]
    public static extern IntPtr create_window_bytes(byte[] title, int titleLen, int w, int h);

    [DllImport(DLL, CallingConvention = CC)]
    public static extern void set_message_loop_main_window(IntPtr hwnd);

    [DllImport(DLL, CallingConvention = CC)]
    public static extern int run_message_loop();
}
```
