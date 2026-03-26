# 标题栏样式自定义 (Titlebar Style)

[← 返回主文档](../README.md)

## 概述

标题栏样式自定义功能允许开发者动态调整窗口标题栏的文字颜色、字体、字号和对齐方式。当使用深色标题栏背景时，默认的深色文字在深色背景上不可见，通过本功能可以设置白色或其他浅色文字，确保标题清晰可读。

所有样式修改即时生效（自动触发标题栏重绘），无需手动刷新。

## API 参考

### SetTitleBarTextColor

设置窗口标题栏的文字颜色。

```c++
extern "C" __declspec(dllexport) int __stdcall SetTitleBarTextColor(HWND hwnd, UINT32 color);
```

**参数说明:**

| 参数 | 类型 | 说明 |
|------|------|------|
| `hwnd` | HWND | 目标窗口句柄 |
| `color` | UINT32 | ARGB 颜色值，0 表示恢复跟随主题 |

**返回值:** 1=成功，0=失败（hwnd 无效）

> **提示**：传入 `0` 可恢复为跟随主题模式，此时标题文字颜色由 `ThemeColor_TextPrimary()` 决定（亮色主题为深色文字，暗色主题为浅色文字）。

---

### GetTitleBarTextColor

获取窗口标题栏当前的文字颜色。

```c++
extern "C" __declspec(dllexport) UINT32 __stdcall GetTitleBarTextColor(HWND hwnd);
```

**参数说明:**

| 参数 | 类型 | 说明 |
|------|------|------|
| `hwnd` | HWND | 目标窗口句柄 |

**返回值:** 当前 `titlebar_text_color` 值（UINT32 ARGB），hwnd 无效时返回 0

> **提示**：返回值为 0 时，表示当前处于跟随主题模式。调用方可据此判断是否已设置自定义颜色。

---

### SetTitleBarFont

设置窗口标题栏的字体名称和字号。

```c++
extern "C" __declspec(dllexport) int __stdcall SetTitleBarFont(
    HWND hwnd,
    const unsigned char* fontName, int fontNameLen,
    float fontSize
);
```

**参数说明:**

| 参数 | 类型 | 说明 |
|------|------|------|
| `hwnd` | HWND | 目标窗口句柄 |
| `fontName` | const unsigned char* | 字体名称 UTF-8 字节集指针 |
| `fontNameLen` | int | 字体名称字节长度 |
| `fontSize` | float | 字号（像素），必须 > 0 |

**返回值:** 1=成功，0=失败（hwnd 无效、fontName 为 NULL、fontNameLen ≤ 0 或 fontSize ≤ 0）

---

### SetTitleBarAlignment

设置窗口标题栏文字的水平对齐方式。

```c++
extern "C" __declspec(dllexport) int __stdcall SetTitleBarAlignment(HWND hwnd, int alignment);
```

**参数说明:**

| 参数 | 类型 | 说明 |
|------|------|------|
| `hwnd` | HWND | 目标窗口句柄 |
| `alignment` | int | 0=左对齐，1=居中，2=右对齐 |

**返回值:** 1=成功，0=失败（hwnd 无效或 alignment 不在 0-2 范围内）

**对齐方式映射:**

| alignment 值 | DirectWrite 枚举 | 含义 |
|-------------|-------------------|------|
| 0 | DWRITE_TEXT_ALIGNMENT_LEADING | 左对齐（默认） |
| 1 | DWRITE_TEXT_ALIGNMENT_CENTER | 居中 |
| 2 | DWRITE_TEXT_ALIGNMENT_TRAILING | 右对齐 |

## 默认值与向后兼容性

所有新增属性的默认值与修改前的硬编码行为完全一致，确保现有程序无需任何改动即可正常运行：

| 属性 | 默认值 | 说明 |
|------|--------|------|
| `titlebar_text_color` | 0 | 跟随主题，使用 `ThemeColor_TextPrimary()` 返回的颜色 |
| `titlebar_font_name` | `"Segoe UI Emoji"` | 与原硬编码字体一致 |
| `titlebar_font_size` | 13.0 | 与原硬编码字号一致 |
| `titlebar_alignment` | 0（左对齐） | 与原硬编码对齐方式一致 |

- 未调用任何 Set 函数时，窗口标题栏外观与升级前完全相同
- `titlebar_text_color` 设为 0 即可恢复跟随主题模式
- 所有 Set 函数对无效参数采用防御性处理：返回 0 且不修改任何状态

## 颜色格式

颜色使用 UINT32 ARGB 格式（32位无符号整数）：

```
0xAARRGGBB
  AA = Alpha（透明度，FF=不透明）
  RR = Red（红色分量）
  GG = Green（绿色分量）
  BB = Blue（蓝色分量）
```

常用颜色示例：
- `0xFFFFFFFF` — 不透明白色
- `0xFF000000` — 不透明黑色
- `0xFFFF6600` — 不透明橙色
- `0` — 特殊值，表示跟随主题

## 易语言调用

### DLL 命令声明

```
.DLL命令 设置标题栏文字颜色, 整数型, "emoji_window.dll", "SetTitleBarTextColor", , , 设置标题栏文字颜色（ARGB，0=跟随主题）
    .参数 窗口句柄, 整数型
    .参数 颜色, 整数型, , ARGB颜色

.DLL命令 获取标题栏文字颜色, 整数型, "emoji_window.dll", "GetTitleBarTextColor", , , 获取标题栏文字颜色（0=跟随主题）
    .参数 窗口句柄, 整数型

.DLL命令 设置标题栏字体, 整数型, "emoji_window.dll", "SetTitleBarFont", , , 设置标题栏字体和字号
    .参数 窗口句柄, 整数型
    .参数 字体名字节集指针, 整数型, , UTF-8字体名字节集指针
    .参数 字体名长度, 整数型, , 字体名字节集长度
    .参数 字号, 小数型, , 字号（像素），必须大于0

.DLL命令 设置标题栏对齐方式, 整数型, "emoji_window.dll", "SetTitleBarAlignment", , , 设置标题栏文字对齐方式
    .参数 窗口句柄, 整数型
    .参数 对齐方式, 整数型, , 0=左对齐，1=居中，2=右对齐
```

### 易语言使用示例

```
.程序集变量 主窗口句柄, 整数型

.子程序 _启动窗口_创建完毕
.局部变量 标题字节集, 字节集
.局部变量 字体名字节集, 字节集
.局部变量 返回值, 整数型
.局部变量 当前颜色, 整数型

' 创建深色标题栏窗口
' 标题: "🎨 深色标题栏示例"
' 🎨 = { 240, 159, 142, 168 }
标题字节集 ＝ { 240, 159, 142, 168, 32 } ＋ 编码_Ansi到Utf8 ("深色标题栏示例")
主窗口句柄 ＝ 创建Emoji窗口_字节集_扩展 (取变量数据地址 (标题字节集), 取字节集长度 (标题字节集), －1, －1, 800, 600, 到ARGB (255, 30, 30, 30), 到ARGB (255, 45, 45, 45))

' 设置白色文字（深色背景需要浅色文字）
返回值 ＝ 设置标题栏文字颜色 (主窗口句柄, 到ARGB (255, 255, 255, 255))

' 设置自定义字体 "微软雅黑"，字号 15
字体名字节集 ＝ 编码_Ansi到Utf8 ("微软雅黑")
返回值 ＝ 设置标题栏字体 (主窗口句柄, 取变量数据地址 (字体名字节集), 取字节集长度 (字体名字节集), 15)

' 设置标题居中对齐
返回值 ＝ 设置标题栏对齐方式 (主窗口句柄, 1)

' 查询当前文字颜色
当前颜色 ＝ 获取标题栏文字颜色 (主窗口句柄)
调试输出 ("当前标题栏文字颜色: " ＋ 到文本 (当前颜色))

' 恢复跟随主题
' 设置标题栏文字颜色 (主窗口句柄, 0)

运行消息循环 ()
```

## Python 调用

```python
import ctypes
from ctypes import wintypes

# 加载 DLL
dll = ctypes.CDLL('./emoji_window.dll')

# 定义函数原型
dll.SetTitleBarTextColor.argtypes = [wintypes.HWND, ctypes.c_uint32]
dll.SetTitleBarTextColor.restype = ctypes.c_int

dll.GetTitleBarTextColor.argtypes = [wintypes.HWND]
dll.GetTitleBarTextColor.restype = ctypes.c_uint32

dll.SetTitleBarFont.argtypes = [
    wintypes.HWND,
    ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int,
    ctypes.c_float
]
dll.SetTitleBarFont.restype = ctypes.c_int

dll.SetTitleBarAlignment.argtypes = [wintypes.HWND, ctypes.c_int]
dll.SetTitleBarAlignment.restype = ctypes.c_int

# 创建窗口（使用已有的窗口创建函数）
hwnd = dll.create_window_bytes_ex(
    title_ptr, title_len,
    -1, -1, 800, 600,
    0xFF1E1E1E,  # 深色标题栏
    0xFF2D2D2D   # 深色客户区
)

# 设置白色文字
result = dll.SetTitleBarTextColor(hwnd, 0xFFFFFFFF)
print(f"设置文字颜色: {'成功' if result == 1 else '失败'}")

# 获取当前文字颜色
color = dll.GetTitleBarTextColor(hwnd)
print(f"当前文字颜色: 0x{color:08X}")

# 设置字体为 "Microsoft YaHei"，字号 15
font_name = "Microsoft YaHei".encode('utf-8')
font_buf = (ctypes.c_ubyte * len(font_name))(*font_name)
result = dll.SetTitleBarFont(hwnd, font_buf, len(font_name), ctypes.c_float(15.0))
print(f"设置字体: {'成功' if result == 1 else '失败'}")

# 设置居中对齐
result = dll.SetTitleBarAlignment(hwnd, 1)
print(f"设置对齐: {'成功' if result == 1 else '失败'}")

# 恢复跟随主题
# dll.SetTitleBarTextColor(hwnd, 0)
```

## C# 调用

```csharp
using System;
using System.Runtime.InteropServices;
using System.Text;

public class EmojiWindow
{
    private const string DllName = "emoji_window.dll";

    [DllImport(DllName, CallingConvention = CallingConvention.StdCall)]
    public static extern int SetTitleBarTextColor(IntPtr hwnd, uint color);

    [DllImport(DllName, CallingConvention = CallingConvention.StdCall)]
    public static extern uint GetTitleBarTextColor(IntPtr hwnd);

    [DllImport(DllName, CallingConvention = CallingConvention.StdCall)]
    public static extern int SetTitleBarFont(
        IntPtr hwnd,
        byte[] fontName, int fontNameLen,
        float fontSize
    );

    [DllImport(DllName, CallingConvention = CallingConvention.StdCall)]
    public static extern int SetTitleBarAlignment(IntPtr hwnd, int alignment);
}

// 使用示例
class Program
{
    static void Main()
    {
        IntPtr hwnd = /* 已创建的窗口句柄 */;

        // 设置白色文字
        int result = EmojiWindow.SetTitleBarTextColor(hwnd, 0xFFFFFFFF);
        Console.WriteLine($"设置文字颜色: {(result == 1 ? "成功" : "失败")}");

        // 获取当前文字颜色
        uint color = EmojiWindow.GetTitleBarTextColor(hwnd);
        Console.WriteLine($"当前文字颜色: 0x{color:X8}");

        // 设置字体为 "Microsoft YaHei"，字号 15
        byte[] fontName = Encoding.UTF8.GetBytes("Microsoft YaHei");
        result = EmojiWindow.SetTitleBarFont(hwnd, fontName, fontName.Length, 15.0f);
        Console.WriteLine($"设置字体: {(result == 1 ? "成功" : "失败")}");

        // 设置居中对齐
        result = EmojiWindow.SetTitleBarAlignment(hwnd, 1);
        Console.WriteLine($"设置对齐: {(result == 1 ? "成功" : "失败")}");

        // 恢复跟随主题
        // EmojiWindow.SetTitleBarTextColor(hwnd, 0);
    }
}
```

## 完整使用场景

以下示例演示创建一个深色标题栏窗口，并依次设置白色文字、自定义字体和居中对齐：

### 场景描述

1. 创建窗口，标题栏背景色设为深色 `0xFF1E1E1E`
2. 设置标题文字颜色为白色 `0xFFFFFFFF`，确保深色背景上文字可见
3. 设置标题字体为"微软雅黑"，字号 15px
4. 设置标题文字居中对齐
5. 查询当前文字颜色，确认设置生效

### 易语言完整示例

```
.版本 2

.程序集 窗口程序集_深色标题栏示例
.程序集变量 主窗口句柄, 整数型

.子程序 _启动窗口_创建完毕
.局部变量 标题字节集, 字节集
.局部变量 字体名字节集, 字节集
.局部变量 返回值, 整数型
.局部变量 当前颜色, 整数型

' ===== 第1步：创建深色标题栏窗口 =====
' 标题: "🎨 深色主题窗口"
' 🎨 = { 240, 159, 142, 168 }
标题字节集 ＝ { 240, 159, 142, 168, 32 } ＋ 编码_Ansi到Utf8 ("深色主题窗口")
主窗口句柄 ＝ 创建Emoji窗口_字节集_扩展 (取变量数据地址 (标题字节集), 取字节集长度 (标题字节集), －1, －1, 800, 600, 到ARGB (255, 30, 30, 30), 到ARGB (255, 45, 45, 45))
' 此时标题文字为默认主题色（深色），在深色标题栏上几乎不可见

' ===== 第2步：设置白色文字 =====
返回值 ＝ 设置标题栏文字颜色 (主窗口句柄, 到ARGB (255, 255, 255, 255))
' 返回值 ＝ 1 表示成功，标题文字立即变为白色

' ===== 第3步：设置自定义字体 =====
字体名字节集 ＝ 编码_Ansi到Utf8 ("微软雅黑")
返回值 ＝ 设置标题栏字体 (主窗口句柄, 取变量数据地址 (字体名字节集), 取字节集长度 (字体名字节集), 15)
' 标题字体变为"微软雅黑" 15px

' ===== 第4步：设置居中对齐 =====
返回值 ＝ 设置标题栏对齐方式 (主窗口句柄, 1)
' 标题文字居中显示

' ===== 第5步：查询当前颜色 =====
当前颜色 ＝ 获取标题栏文字颜色 (主窗口句柄)
' 当前颜色应为 0xFFFFFFFF（白色）

.如果真 (当前颜色 ≠ 0)
    调试输出 ("已设置自定义文字颜色")
.如果真结束

运行消息循环 ()
```

## 注意事项

⚠️ **重要提示**：

1. **颜色值 0 的特殊含义**：`titlebar_text_color` 为 0 时表示跟随主题，而非黑色。如需设置黑色文字，请使用 `0xFF000000`。

2. **字体名称编码**：`SetTitleBarFont` 的 `fontName` 参数必须是 UTF-8 编码的字节集。在易语言中使用 `编码_Ansi到Utf8("字体名")` 转换，在 Python 中使用 `"字体名".encode('utf-8')` 转换。

3. **即时生效**：所有 Set 函数修改后立即触发标题栏重绘（通过 `InvalidateRect`），无需手动调用刷新函数。

4. **无效参数保护**：
   - 无效窗口句柄：所有函数返回 0，不修改任何状态
   - `SetTitleBarFont`：fontName 为 NULL、fontNameLen ≤ 0 或 fontSize ≤ 0 时返回 0
   - `SetTitleBarAlignment`：alignment 不在 0-2 范围内时返回 0

5. **线程安全**：所有 API 应在主 UI 线程调用，不支持多线程并发访问。

6. **易语言符号**：易语言代码中必须使用全角符号（`＝` `＋` `＞` `＜` `≠` 等），半角符号会导致语法错误。

7. **易语言 Emoji 处理**：易语言 IDE 使用 ANSI 编码，不支持直接输入 emoji。必须使用 UTF-8 字节集形式（如 `{ 240, 159, 142, 168 }` 表示 🎨），中文部分用 `编码_Ansi到Utf8()` 转换后拼接。

8. **易语言指针传递**：传递字节集指针时使用 `取变量数据地址`（不是 `取字节集指针` 或 `取字节集数据地址`）。

## 相关文档

- [按钮控件](controls/button.md)
- [主题系统](theme.md)
- [常见问题](faq.md)
