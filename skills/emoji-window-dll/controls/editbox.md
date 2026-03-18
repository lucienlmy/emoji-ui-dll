# EditBox - 编辑框控件

## 概述

编辑框控件提供三种实现版本：标准编辑框（`CreateEditBox`）、彩色 Emoji 编辑框（`CreateColorEmojiEditBox`，基于 RichEdit）、D2D 彩色 Emoji 编辑框（`CreateD2DColorEmojiEditBox`，完美支持彩色 Emoji）。三者创建参数一致，后续操作 API 标准版和 RichEdit 版共用，D2D 版使用独立的 `*D2D*` 系列 API。

## 导出函数

### 创建

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `CreateEditBox` | `int parent, int x, int y, int w, int h, int text_ptr, int text_len, int fg, int bg, int font_ptr, int font_len, int fontSize, bool bold, bool italic, bool underline, int align, bool multiline, bool readOnly, bool password, bool showBorder, bool vertCenter` | `int` (编辑框句柄) | 标准编辑框 |
| `CreateColorEmojiEditBox` | 同上 | `int` (编辑框句柄) | RichEdit 版彩色 Emoji 编辑框 |
| `CreateD2DColorEmojiEditBox` | 同上 | `int` (编辑框句柄) | D2D 版完美彩色 Emoji 编辑框 |

### 文本（标准版 / RichEdit 版）

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetEditBoxText` | `int hEdit, int text_ptr, int text_len` | `void` | 设置文本 |
| `GetEditBoxText` | `int hEdit, int buf_ptr, int buf_size` | `int` (UTF-8 字节数) | 获取文本 |

### 文本（D2D 版）

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetD2DEditBoxText` | `int hEdit, int text_ptr, int text_len` | `void` | 设置文本 |
| `GetD2DEditBoxText` | `int hEdit, int buf_ptr, int buf_size` | `int` (UTF-8 字节数) | 获取文本；buf_ptr=0 返回所需大小 |

### 字体

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetEditBoxFont` | `int hEdit, int font_ptr, int font_len, int fontSize, bool bold, bool italic, bool underline` | `void` | 设置字体（标准/RichEdit） |
| `GetEditBoxFont` | `int hEdit, int font_buf_ptr, int font_buf_size, int* fontSize, int* bold, int* italic, int* underline` | `int` (字体名字节数) | 获取字体（标准/RichEdit） |
| `SetD2DEditBoxFont` | `int hEdit, int font_ptr, int font_len, int fontSize, bool bold, bool italic, bool underline` | `void` | 设置字体（D2D） |

### 颜色

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetEditBoxColor` | `int hEdit, int fg, int bg` | `void` | 设置颜色（标准/RichEdit，ARGB） |
| `GetEditBoxColor` | `int hEdit, int* fg, int* bg` | `int` (0=成功，-1=失败) | 获取颜色 |
| `SetD2DEditBoxColor` | `int hEdit, int fg, int bg` | `void` | 设置颜色（D2D，ARGB） |

### 位置

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetEditBoxBounds` | `int hEdit, int x, int y, int w, int h` | `void` | 设置位置（标准/RichEdit） |
| `GetEditBoxBounds` | `int hEdit, int* x, int* y, int* w, int* h` | `int` (0=成功，-1=失败) | 获取位置 |
| `SetD2DEditBoxBounds` | `int hEdit, int x, int y, int w, int h` | `void` | 设置位置（D2D） |

### 状态控制

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `EnableEditBox` | `int hEdit, bool enabled` | `void` | 启用/禁用（标准/RichEdit） |
| `ShowEditBox` | `int hEdit, bool visible` | `void` | 显示/隐藏（标准/RichEdit） |
| `EnableD2DEditBox` | `int hEdit, bool enabled` | `void` | 启用/禁用（D2D） |
| `ShowD2DEditBox` | `int hEdit, bool visible` | `void` | 显示/隐藏（D2D） |
| `GetEditBoxAlignment` | `int hEdit` | `int` (0=左，1=中，2=右，-1=错误) | 获取对齐方式 |
| `GetEditBoxEnabled` | `int hEdit` | `int` (1=启用，0=禁用，-1=错误) | 获取启用状态 |
| `GetEditBoxVisible` | `int hEdit` | `int` (1=可见，0=不可见，-1=错误) | 获取可视状态 |

### 特殊功能

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetEditBoxVerticalCenter` | `int hEdit, bool vertCenter` | `void` | 设置垂直居中（仅单行有效） |
| `SetEditBoxKeyCallback` | `int hEdit, int callback_ptr` | `void` | 设置按键回调（标准/RichEdit） |
| `SetD2DEditBoxKeyCallback` | `int hEdit, int callback_ptr` | `void` | 设置按键回调（D2D） |

## 回调签名

```c
// 编辑框按键回调（标准/RichEdit/D2D 通用签名）
void __stdcall OnEditBoxKey(int hEdit, int keyCode, int keyDown, int shift, int ctrl, int alt);
// keyDown: 1=按下, 0=松开
// shift/ctrl/alt: 1=按住, 0=未按住
```

## 注意事项

- 三种编辑框创建参数完全一致，仅函数名不同
- `CreateEditBox` 和 `CreateColorEmojiEditBox` 创建的编辑框共用 `SetEditBoxText` 等 API
- `CreateD2DColorEmojiEditBox` 创建的编辑框必须使用 `SetD2DEditBoxText` 等带 D2D 前缀的 API
- `SetEditBoxVerticalCenter` 仅对单行编辑框有效
- `align` 对齐方式：0=左对齐，1=居中，2=右对齐
- 颜色格式为 ARGB（0xAARRGGBB）
- `GetEditBoxText` 需两次调用：第一次 buf_ptr=0 获取大小，第二次传入缓冲区
