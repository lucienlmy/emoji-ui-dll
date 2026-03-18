# CheckBox - 复选框控件

## 概述

自绘复选框控件，支持自定义文本、字体、颜色。每个复选框可独立绑定状态改变回调。

## 导出函数

### 创建

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `CreateCheckBox` | `int parent, int x, int y, int w, int h, int text_ptr, int text_len, bool isChecked, int fg, int bg, int font_ptr, int font_len, int fontSize, bool bold, bool italic, bool underline` | `int` (复选框句柄) | 创建复选框 |

### 状态

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `GetCheckBoxState` | `int hCheckBox` | `bool` | 获取选中状态 |
| `SetCheckBoxState` | `int hCheckBox, bool checked` | `void` | 设置选中状态 |

### 回调

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetCheckBoxCallback` | `int hCheckBox, callback` | `void` | 设置状态改变回调（每个复选框独立绑定） |

### 文本

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetCheckBoxText` | `int hCheckBox, int text_ptr, int text_len` | `void` | 设置文本 |
| `GetCheckBoxText` | `int hCheckBox, int buf_ptr, int buf_size` | `int` (UTF-8 字节数) | 获取文本；buf_ptr=0 返回所需大小 |

### 字体

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetCheckBoxFont` | `int hCheckBox, int font_ptr, int font_len, int fontSize, int bold, int italic, int underline` | `void` | 设置字体 |
| `GetCheckBoxFont` | `int hCheckBox, int font_buf_ptr, int font_buf_size, int* fontSize, int* bold, int* italic, int* underline` | `int` (字体名字节数) | 获取字体信息；font_buf_ptr=0 返回所需大小 |

### 颜色

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetCheckBoxColor` | `int hCheckBox, int fg, int bg` | `void` | 设置前景色和背景色（ARGB） |
| `GetCheckBoxColor` | `int hCheckBox, int* fg, int* bg` | `int` (0=成功，-1=失败) | 获取颜色（传址输出） |

### 位置

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetCheckBoxBounds` | `int hCheckBox, int x, int y, int w, int h` | `void` | 设置位置和大小 |

### 状态控制

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `EnableCheckBox` | `int hCheckBox, bool enabled` | `void` | 启用/禁用 |
| `ShowCheckBox` | `int hCheckBox, bool visible` | `void` | 显示/隐藏 |

## 回调签名

```c
// 复选框状态改变回调
void __stdcall OnCheckBoxChanged(int checkBoxId, int isChecked);
// isChecked: 1=选中, 0=未选中
```

## 注意事项

- 回调是**每个复选框独立绑定**的（与按钮的全局回调不同）
- `SetCheckBoxFont` 的 bold/italic/underline 参数使用 int 类型（1=是，0=否），不是 bool
- `GetCheckBoxFont` 中 fontSize/bold/italic/underline 为传址输出参数
- `GetCheckBoxText` 需两次调用：第一次 buf_ptr=0 获取大小，第二次传入缓冲区
- 颜色格式为 ARGB（0xAARRGGBB）
