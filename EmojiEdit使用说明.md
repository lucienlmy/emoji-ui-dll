# EmojiEdit 编辑框组件使用说明

## 概述

EmojiEdit 是一个集成在 `emoji_window.dll` 中的自绘编辑框组件，支持 Unicode 字符、Emoji 表情符号，并提供丰富的自定义样式选项。

## 核心特性

- **Unicode 和 Emoji 支持** - 完美支持中文、Emoji 及其他 Unicode 特殊符号
- **自绘渲染** - 使用 Direct2D 和 DirectWrite 进行高质量渲染
- **字体自定义** - 支持设置字体名称、大小、粗细
- **颜色自定义** - 支持设置文字、背景、边框、选区、光标颜色
- **对齐方式** - 支持左对齐、居中、右对齐
- **边框样式** - 支持无边框、单线边框、圆角边框
- **滚动条** - 支持无滚动条、垂直、水平、双向滚动条
- **多行模式** - 支持单行和多行编辑
- **自动换行** - 支持启用/禁用自动换行
- **只读模式** - 支持只读状态
- **选择功能** - 支持文本选择、复制、剪切、粘贴
- **光标闪烁** - 支持光标闪烁动画

## API 函数列表

### 1. CreateEmojiEdit - 创建编辑框

```c++
HWND CreateEmojiEdit(HWND hParent, int x, int y, int width, int height)
```

**参数：**
- `hParent` - 父窗口句柄
- `x` - X 坐标
- `y` - Y 坐标
- `width` - 宽度
- `height` - 高度

**返回值：** 编辑框窗口句柄，失败返回 NULL

**易语言声明：**
```
.DLL命令 CreateEmojiEdit, 整数型, "emoji_window.dll", "CreateEmojiEdit"
    .参数 父窗口句柄, 整数型
    .参数 X坐标, 整数型
    .参数 Y坐标, 整数型
    .参数 宽度, 整数型
    .参数 高度, 整数型
```

---

### 2. SetEmojiEditText - 设置编辑框文本

```c++
BOOL SetEmojiEditText(HWND hEdit, const unsigned char* text_bytes, int text_len)
```

**参数：**
- `hEdit` - 编辑框句柄
- `text_bytes` - UTF-8 编码的文本字节集
- `text_len` - 字节集长度

**返回值：** 成功返回 TRUE，失败返回 FALSE

**易语言声明：**
```
.DLL命令 SetEmojiEditText, 逻辑型, "emoji_window.dll", "SetEmojiEditText"
    .参数 编辑框句柄, 整数型
    .参数 文本字节集, 字节集
    .参数 文本长度, 整数型
```

**易语言示例：**
```
.变量 文本, 字节集
文本 = 到字节集("Hello 世界! 🎉")
SetEmojiEditText(编辑框句柄, 文本, 取字节集长度(文本))
```

---

### 3. GetEmojiEditTextLength - 获取文本长度

```c++
int GetEmojiEditTextLength(HWND hEdit)
```

**参数：**
- `hEdit` - 编辑框句柄

**返回值：** UTF-8 编码的字节数（用于分配缓冲区）

**易语言声明：**
```
.DLL命令 GetEmojiEditTextLength, 整数型, "emoji_window.dll", "GetEmojiEditTextLength"
    .参数 编辑框句柄, 整数型
```

---

### 4. GetEmojiEditText - 获取编辑框文本

```c++
int GetEmojiEditText(HWND hEdit, unsigned char* buffer, int buffer_size)
```

**参数：**
- `hEdit` - 编辑框句柄
- `buffer` - 接收文本的缓冲区
- `buffer_size` - 缓冲区大小

**返回值：** 实际复制的字节数

**易语言声明：**
```
.DLL命令 GetEmojiEditText, 整数型, "emoji_window.dll", "GetEmojiEditText"
    .参数 编辑框句柄, 整数型
    .参数 缓冲区, 字节集
    .参数 缓冲区大小, 整数型
```

**易语言示例：**
```
.变量 长度, 整数型
.变量 缓冲区, 字节集

长度 = GetEmojiEditTextLength(编辑框句柄)
缓冲区 = 取空白字节集(长度 + 1)
GetEmojiEditText(编辑框句柄, 缓冲区, 长度 + 1)
调试输出(到文本(缓冲区))
```

---

### 5. SetEmojiEditFont - 设置字体

```c++
BOOL SetEmojiEditFont(HWND hEdit, const unsigned char* font_name_bytes, int font_name_len,
                      float font_size, int font_weight)
```

**参数：**
- `hEdit` - 编辑框句柄
- `font_name_bytes` - UTF-8 编码的字体名称
- `font_name_len` - 字体名称长度
- `font_size` - 字体大小（浮点数）
- `font_weight` - 字体粗细（100-900，400=正常，700=粗体）

**返回值：** 成功返回 TRUE，失败返回 FALSE

**易语言声明：**
```
.DLL命令 SetEmojiEditFont, 逻辑型, "emoji_window.dll", "SetEmojiEditFont"
    .参数 编辑框句柄, 整数型
    .参数 字体名称, 字节集
    .参数 字体名称长度, 整数型
    .参数 字体大小, 小数型
    .参数 字体粗细, 整数型
```

**字体粗细常量：**
| 值 | 说明 |
|---|---|
| 100 | Thin |
| 200 | Extra Light |
| 300 | Light |
| 400 | Normal (默认) |
| 500 | Medium |
| 600 | Semi Bold |
| 700 | Bold |
| 800 | Extra Bold |
| 900 | Black |

**易语言示例：**
```
.变量 字体名, 字节集
字体名 = 到字节集("Segoe UI Emoji")
SetEmojiEditFont(编辑框句柄, 字体名, 取字节集长度(字体名), 16.0, 400)
```

---

### 6. SetEmojiEditColors - 设置颜色

```c++
BOOL SetEmojiEditColors(HWND hEdit, UINT32 text_color, UINT32 bg_color,
                        UINT32 border_color, UINT32 selection_color, UINT32 cursor_color)
```

**参数：**
- `hEdit` - 编辑框句柄
- `text_color` - 文字颜色 (ARGB 格式)
- `bg_color` - 背景颜色 (ARGB 格式)
- `border_color` - 边框颜色 (ARGB 格式)
- `selection_color` - 选中背景颜色 (ARGB 格式)
- `cursor_color` - 光标颜色 (ARGB 格式)

**返回值：** 成功返回 TRUE，失败返回 FALSE

**易语言声明：**
```
.DLL命令 SetEmojiEditColors, 逻辑型, "emoji_window.dll", "SetEmojiEditColors"
    .参数 编辑框句柄, 整数型
    .参数 文字颜色, 整数型
    .参数 背景颜色, 整数型
    .参数 边框颜色, 整数型
    .参数 选中颜色, 整数型
    .参数 光标颜色, 整数型
```

**颜色格式：**
- ARGB 格式：`0xAARRGGBB`
- AA = Alpha（透明度，FF=不透明）
- RR = Red（红色）
- GG = Green（绿色）
- BB = Blue（蓝色）

**常用颜色示例：**
| 颜色 | ARGB 值 |
|---|---|
| 黑色 | 0xFF000000 |
| 白色 | 0xFFFFFFFF |
| 红色 | 0xFFFF0000 |
| 绿色 | 0xFF00FF00 |
| 蓝色 | 0xFF0000FF |
| 灰色 | 0xFF808080 |
| 浅灰 | 0xFFCCCCCC |
| 深灰 | 0xFF333333 |

**易语言示例：**
```
SetEmojiEditColors(编辑框句柄,
    0xFF000000,  ' 文字：黑色
    0xFFFFFFFF,  ' 背景：白色
    0xFFCCCCCC,  ' 边框：浅灰
    0x330078D7,  ' 选中：半透明蓝色
    0xFF000000   ' 光标：黑色
)
```

---

### 7. SetEmojiEditStyle - 设置样式

```c++
BOOL SetEmojiEditStyle(HWND hEdit, int text_alignment, int border_style,
                       int scroll_style, BOOL multiline, BOOL word_wrap,
                       BOOL readonly, float corner_radius)
```

**参数：**
- `hEdit` - 编辑框句柄
- `text_alignment` - 文本对齐方式（见下表）
- `border_style` - 边框样式（见下表）
- `scroll_style` - 滚动条样式（见下表）
- `multiline` - 是否多行（TRUE/FALSE）
- `word_wrap` - 是否自动换行（TRUE/FALSE）
- `readonly` - 是否只读（TRUE/FALSE）
- `corner_radius` - 圆角半径（浮点数）

**返回值：** 成功返回 TRUE，失败返回 FALSE

**易语言声明：**
```
.DLL命令 SetEmojiEditStyle, 逻辑型, "emoji_window.dll", "SetEmojiEditStyle"
    .参数 编辑框句柄, 整数型
    .参数 文本对齐, 整数型
    .参数 边框样式, 整数型
    .参数 滚动条样式, 整数型
    .参数 多行, 逻辑型
    .参数 自动换行, 逻辑型
    .参数 只读, 逻辑型
    .参数 圆角半径, 小数型
```

**文本对齐常量：**
| 值 | 常量名 | 说明 |
|---|---|---|
| 0 | EDIT_ALIGN_LEFT | 左对齐（默认）|
| 1 | EDIT_ALIGN_CENTER | 居中对齐 |
| 2 | EDIT_ALIGN_RIGHT | 右对齐 |

**边框样式常量：**
| 值 | 常量名 | 说明 |
|---|---|---|
| 0 | EDIT_BORDER_NONE | 无边框 |
| 1 | EDIT_BORDER_SINGLE | 单线边框（默认）|
| 2 | EDIT_BORDER_ROUNDED | 圆角边框 |

**滚动条样式常量：**
| 值 | 常量名 | 说明 |
|---|---|---|
| 0 | EDIT_SCROLL_NONE | 无滚动条（默认）|
| 1 | EDIT_SCROLL_VERTICAL | 垂直滚动条 |
| 2 | EDIT_SCROLL_HORIZONTAL | 水平滚动条 |
| 3 | EDIT_SCROLL_BOTH | 双向滚动条 |

**易语言示例：**
```
' 设置为多行编辑框，带垂直滚动条，圆角边框
SetEmojiEditStyle(编辑框句柄,
    0,      ' 左对齐
    2,      ' 圆角边框
    1,      ' 垂直滚动条
    真,     ' 多行
    真,     ' 自动换行
    假,     ' 非只读
    8.0     ' 圆角半径 8 像素
)
```

---

### 8. SetEmojiEditScroll - 设置滚动位置

```c++
BOOL SetEmojiEditScroll(HWND hEdit, int scroll_x, int scroll_y)
```

**参数：**
- `hEdit` - 编辑框句柄
- `scroll_x` - 水平滚动位置
- `scroll_y` - 垂直滚动位置

**返回值：** 成功返回 TRUE，失败返回 FALSE

**易语言声明：**
```
.DLL命令 SetEmojiEditScroll, 逻辑型, "emoji_window.dll", "SetEmojiEditScroll"
    .参数 编辑框句柄, 整数型
    .参数 水平滚动, 整数型
    .参数 垂直滚动, 整数型
```

---

### 9. GetEmojiEditScrollInfo - 获取滚动信息

```c++
BOOL GetEmojiEditScrollInfo(HWND hEdit, int* max_scroll_x, int* max_scroll_y,
                            int* current_scroll_x, int* current_scroll_y)
```

**参数：**
- `hEdit` - 编辑框句柄
- `max_scroll_x` - 接收最大水平滚动值
- `max_scroll_y` - 接收最大垂直滚动值
- `current_scroll_x` - 接收当前水平滚动值
- `current_scroll_y` - 接收当前垂直滚动值

**返回值：** 成功返回 TRUE，失败返回 FALSE

**易语言声明：**
```
.DLL命令 GetEmojiEditScrollInfo, 逻辑型, "emoji_window.dll", "GetEmojiEditScrollInfo"
    .参数 编辑框句柄, 整数型
    .参数 最大水平滚动, 整数型, 传址
    .参数 最大垂直滚动, 整数型, 传址
    .参数 当前水平滚动, 整数型, 传址
    .参数 当前垂直滚动, 整数型, 传址
```

---

### 10. SetEmojiEditSelection - 设置选择范围

```c++
BOOL SetEmojiEditSelection(HWND hEdit, int start_pos, int end_pos)
```

**参数：**
- `hEdit` - 编辑框句柄
- `start_pos` - 选择起始位置（字符索引）
- `end_pos` - 选择结束位置（字符索引）

**返回值：** 成功返回 TRUE，失败返回 FALSE

**易语言声明：**
```
.DLL命令 SetEmojiEditSelection, 逻辑型, "emoji_window.dll", "SetEmojiEditSelection"
    .参数 编辑框句柄, 整数型
    .参数 起始位置, 整数型
    .参数 结束位置, 整数型
```

**易语言示例：**
```
' 选中全部文本（假设文本长度为 10）
SetEmojiEditSelection(编辑框句柄, 0, 10)
```

---

### 11. GetEmojiEditSelection - 获取选择范围

```c++
BOOL GetEmojiEditSelection(HWND hEdit, int* start_pos, int* end_pos)
```

**参数：**
- `hEdit` - 编辑框句柄
- `start_pos` - 接收选择起始位置
- `end_pos` - 接收选择结束位置

**返回值：** 成功返回 TRUE，失败返回 FALSE

**易语言声明：**
```
.DLL命令 GetEmojiEditSelection, 逻辑型, "emoji_window.dll", "GetEmojiEditSelection"
    .参数 编辑框句柄, 整数型
    .参数 起始位置, 整数型, 传址
    .参数 结束位置, 整数型, 传址
```

---

### 12. SetEmojiEditCursorPos - 设置光标位置

```c++
BOOL SetEmojiEditCursorPos(HWND hEdit, int pos)
```

**参数：**
- `hEdit` - 编辑框句柄
- `pos` - 光标位置（字符索引，从 0 开始）

**返回值：** 成功返回 TRUE，失败返回 FALSE

**易语言声明：**
```
.DLL命令 SetEmojiEditCursorPos, 逻辑型, "emoji_window.dll", "SetEmojiEditCursorPos"
    .参数 编辑框句柄, 整数型
    .参数 光标位置, 整数型
```

---

### 13. GetEmojiEditCursorPos - 获取光标位置

```c++
int GetEmojiEditCursorPos(HWND hEdit)
```

**参数：**
- `hEdit` - 编辑框句柄

**返回值：** 当前光标位置（字符索引）

**易语言声明：**
```
.DLL命令 GetEmojiEditCursorPos, 整数型, "emoji_window.dll", "GetEmojiEditCursorPos"
    .参数 编辑框句柄, 整数型
```

---

### 14. SetEmojiEditFocus - 设置焦点

```c++
void SetEmojiEditFocus(HWND hEdit, BOOL focused)
```

**参数：**
- `hEdit` - 编辑框句柄
- `focused` - TRUE 获取焦点，FALSE 取消焦点

**易语言声明：**
```
.DLL命令 SetEmojiEditFocus, , "emoji_window.dll", "SetEmojiEditFocus"
    .参数 编辑框句柄, 整数型
    .参数 是否聚焦, 逻辑型
```

---

### 15. ClearEmojiEdit - 清空编辑框

```c++
void ClearEmojiEdit(HWND hEdit)
```

**参数：**
- `hEdit` - 编辑框句柄

**易语言声明：**
```
.DLL命令 ClearEmojiEdit, , "emoji_window.dll", "ClearEmojiEdit"
    .参数 编辑框句柄, 整数型
```

---

### 16. DestroyEmojiEdit - 销毁编辑框

```c++
void DestroyEmojiEdit(HWND hEdit)
```

**参数：**
- `hEdit` - 编辑框句柄

**易语言声明：**
```
.DLL命令 DestroyEmojiEdit, , "emoji_window.dll", "DestroyEmojiEdit"
    .参数 编辑框句柄, 整数型
```

**注意事项：**
- 销毁编辑框会自动清理所有资源
- 建议在窗口关闭时调用

---

## 完整易语言示例

```
.版本 2

.程序集 窗口程序集_启动窗口
.程序集变量 编辑框句柄, 整数型

.子程序 _启动窗口_创建完毕

' 创建编辑框
编辑框句柄 = CreateEmojiEdit(取窗口句柄(), 10, 10, 400, 200)

' 设置字体（支持 Emoji 的字体）
.变量 字体名, 字节集
字体名 = 到字节集("Segoe UI Emoji")
SetEmojiEditFont(编辑框句柄, 字体名, 取字节集长度(字体名), 16.0, 400)

' 设置颜色
SetEmojiEditColors(编辑框句柄,
    0xFF333333,  ' 深灰文字
    0xFFFFFFFF,  ' 白色背景
    0xFFCCCCCC,  ' 浅灰边框
    0x330078D7,  ' 半透明蓝色选中
    0xFF333333   ' 深灰光标
)

' 设置样式（多行、垂直滚动条、圆角边框）
SetEmojiEditStyle(编辑框句柄,
    0,      ' 左对齐
    2,      ' 圆角边框
    1,      ' 垂直滚动条
    真,     ' 多行
    真,     ' 自动换行
    假,     ' 非只读
    8.0     ' 圆角半径
)

' 设置初始文本（包含 Emoji）
.变量 初始文本, 字节集
初始文本 = 到字节集("欢迎使用 EmojiEdit 编辑框！🎉" + #换行符 + "支持 Emoji：😀😃😄😁" + #换行符 + "支持 Unicode 特殊符号：★☆●○◆◇■□▲△")
SetEmojiEditText(编辑框句柄, 初始文本, 取字节集长度(初始文本))

' 设置焦点
SetEmojiEditFocus(编辑框句柄, 真)

.子程序 _按钮_获取文本_被单击

' 获取文本长度
.变量 长度, 整数型
.变量 缓冲区, 字节集

长度 = GetEmojiEditTextLength(编辑框句柄)
缓冲区 = 取空白字节集(长度 + 1)
GetEmojiEditText(编辑框句柄, 缓冲区, 长度 + 1)

信息框(到文本(缓冲区), 0, , )

.子程序 _按钮_获取光标位置_被单击

.变量 位置, 整数型
位置 = GetEmojiEditCursorPos(编辑框句柄)
信息框("光标位置：" + 到文本(位置), 0, , )

.子程序 _启动窗口_将被销毁

' 清理资源
DestroyEmojiEdit(编辑框句柄)
```

---

## 键盘快捷键

| 快捷键 | 功能 |
|---|---|
| Ctrl+A | 全选 |
| Ctrl+C | 复制 |
| Ctrl+X | 剪切 |
| Ctrl+V | 粘贴 |
| Home | 移动到开头 |
| End | 移动到结尾 |
| Shift+方向键 | 扩展选择 |
| Backspace | 删除前一个字符 |
| Delete | 删除后一个字符 |
| Enter（多行模式）| 插入换行 |

---

## 技术实现

### 渲染引擎
- **Direct2D** - 硬件加速的 2D 图形渲染
- **DirectWrite** - 高质量文本渲染，支持 Emoji 彩色字体

### 字体支持
默认使用 `Segoe UI Emoji` 字体，支持：
- 彩色 Emoji（Windows 8.1+）
- Unicode 特殊符号
- 中日韩文字
- 任何 Unicode 字符

### 性能优化
- 使用 `IDWriteTextLayout` 缓存文本布局
- 仅在文本改变时重新计算布局
- 硬件加速渲染

---

## 版本历史

**v1.0 (2026-03-04)**
- 初始版本
- 支持 Unicode 和 Emoji
- 支持字体、颜色、样式自定义
- 支持多行、滚动条、选择功能

---

## 许可证

本组件集成在 emoji_window.dll 中，遵循原项目许可证。

---

## 技术支持

如有问题或建议，请联系开发者或提交 Issue。
