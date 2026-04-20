# C# DPI 使用注意事项

本文说明 C# 调用 `emoji_window` DLL 时，控件坐标、尺寸和文本传参需要遵守的 DPI 约定。

## 核心约定

C# 调用方传给 DLL 的控件坐标和尺寸，统一使用 `96 DPI` 逻辑单位。

调用方不要自己按系统缩放比例换算像素。例如按钮宽 `120`、高 `36`，就直接传 `120, 36`。DLL 内部会根据当前窗口或控件 DPI 转成真实物理像素。

## 坐标和尺寸

所有 `Create*`、`Set*Bounds` 的 `x`、`y`、`width`、`height` 参数都按逻辑单位传入。

例如：

```csharp
SetButtonBounds(buttonId, 40, 60, 120, 36);
SetCheckBoxBounds(checkBox, 40, 110, 180, 32);
SetRadioButtonBounds(radioButton, 40, 150, 180, 32);
```

不要在 C# 里执行类似下面的换算：

```csharp
// 不推荐：DLL 内部已经会做 DPI 换算
int pxWidth = (int)(logicalWidth * dpi / 96.0);
```

## 不要直接移动 DLL 控件

不要直接用 Win32 的 `MoveWindow` 或 `SetWindowPos` 移动 DLL 创建的控件。

应使用 DLL 提供的 bounds API：

- `SetButtonBounds`
- `SetCheckBoxBounds`
- `SetRadioButtonBounds`
- `SetProgressBarBounds`
- `SetSliderBounds`
- `SetSwitchBounds`
- `SetD2DDateTimePickerBounds`
- `SetPanelBounds`
- `SetTreeViewBounds`

这样 DLL 才能保存 logical bounds，并在 DPI 变化时重新应用正确的物理尺寸。

## GetBounds 返回值

`Get*Bounds` 返回值也应理解为 `96 DPI` 逻辑单位，而不是物理像素。

例如先调用：

```csharp
SetRadioButtonBounds(radioButton, 40, 60, 200, 36);
```

再调用 `GetRadioButtonBounds`，期望读回的仍是：

```text
x=40, y=60, width=200, height=36
```

不要把返回值再按 DPI 反算一次。

## 窗口尺寸

窗口创建和移动也使用逻辑单位。

例如：

```csharp
CreateWindow(..., 40, 40, 1280, 800);
SetWindowBounds(hwnd, 40, 40, 1280, 800);
```

C# 层不要预先乘 DPI。

## 文本传参

DLL 的文本参数按 UTF-8 字节数组传入。

C# 中建议统一这样处理：

```csharp
byte[] bytes = Encoding.UTF8.GetBytes(text);
```

然后传入 `bytes` 和 `bytes.Length`。

不要直接把 C# `string` 当作 ANSI 或 Unicode 指针传给这些 UTF-8 API。

## 位数匹配

C# 程序位数必须和 DLL 位数一致：

- x64 C# 程序加载 `emoji_window_x64.dll`
- x86 C# 程序加载 `emoji_window_x86.dll`

不建议用 `AnyCPU` 随系统自动切换，除非加载 DLL 的路径也会同步选择 x86/x64。更稳妥的做法是把 C# 项目明确设置为 `x64` 或 `x86`。

## DPI 变化

窗口拖到不同缩放比例的显示器后，C# 层不要自己重算全部控件的物理像素尺寸。

长期约定是：

- C# 层保存和传递 logical bounds。
- DLL 层保存 logical bounds。
- DPI 变化时，DLL 根据新的 DPI 重新计算控件物理位置和尺寸。

如果 C# 层有自己的布局系统，也应该重新输出逻辑单位，而不是输出物理像素。

## GroupBox 子控件

如果控件的 parent 是 `GroupBox`，传入的是相对 GroupBox 内容区的逻辑坐标。

不要手动加上 GroupBox 自己的物理位置，也不要手动加标题栏或内容区偏移。DLL 内部会处理 GroupBox 内容区偏移和 DPI 缩放。

## 总结

C# 调用方只负责传 `96 DPI` 逻辑布局。

DPI 缩放、物理像素转换、控件内部绘制裁剪、DPI 切换后的重新布局，都应交给 DLL 处理。
