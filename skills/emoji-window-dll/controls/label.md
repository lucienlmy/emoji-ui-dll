# Label - 标签控件

## 概述

自绘文本标签控件，支持自定义字体、颜色、对齐方式和自动换行。所有文本通过 UTF-8 字节集传入，支持 Emoji 显示。

## 导出函数

### 创建

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `CreateLabel` | `int parent, int x, int y, int w, int h, int text_bytes_ptr, int text_len, int fg_color, int bg_color, int font_bytes_ptr, int font_len, int fontSize, bool bold, bool italic, bool underline, int align, bool wordWrap` | `int` (标签句柄) | 创建标签 |

### 文本

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetLabelText` | `int hLabel, int text_bytes_ptr, int text_len` | `void` | 设置标签文本 |
| `GetLabelText` | `int hLabel, int buf_ptr, int buf_size` | `int` (UTF-8 字节数) | 获取标签文本；buf_ptr=0 返回所需大小 |

### 字体

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetLabelFont` | `int hLabel, int font_bytes_ptr, int font_len, int fontSize, bool bold, bool italic, bool underline` | `void` | 设置字体 |
| `GetLabelFont` | `int hLabel, int font_buf_ptr, int font_buf_size, int* fontSize, int* bold, int* italic, int* underline` | `int` (字体名 UTF-8 字节数) | 获取字体信息；font_buf_ptr=0 返回所需大小 |

### 颜色

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetLabelColor` | `int hLabel, int fg_color, int bg_color` | `void` | 设置前景色和背景色（ARGB） |
| `GetLabelColor` | `int hLabel, int* fg_color, int* bg_color` | `int` (0=成功，-1=失败) | 获取颜色（传址输出） |

### 位置

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetLabelBounds` | `int hLabel, int x, int y, int w, int h` | `void` | 设置位置和大小 |
| `GetLabelBounds` | `int hLabel, int* x, int* y, int* w, int* h` | `int` (0=成功，-1=失败) | 获取位置和大小（传址输出） |

### 状态控制

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `EnableLabel` | `int hLabel, bool enabled` | `void` | 启用/禁用 |
| `ShowLabel` | `int hLabel, bool visible` | `void` | 显示/隐藏 |
| `GetLabelAlignment` | `int hLabel` | `int` (0=左，1=中，2=右，-1=错误) | 获取对齐方式 |
| `GetLabelEnabled` | `int hLabel` | `int` (1=启用，0=禁用，-1=错误) | 获取启用状态 |
| `GetLabelVisible` | `int hLabel` | `int` (1=可见，0=不可见，-1=错误) | 获取可视状态 |

## 回调签名

标签控件无专属回调。可通过扩展事件系统（`SetMouseEnterCallback` 等）为标签绑定通用事件。

## 注意事项

- `align` 对齐方式：0=左对齐，1=居中，2=右对齐
- `GetLabelFont` 中 fontSize/bold/italic/underline 为传址输出参数
- `GetLabelText` 需两次调用模式：第一次 buf_ptr=0 获取大小，第二次传入缓冲区
- 颜色格式为 ARGB（0xAARRGGBB）
- `wordWrap` 参数控制是否自动换行显示
