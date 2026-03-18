# RadioButton - 单选按钮控件

## 概述

自绘单选按钮控件，通过 `groupId` 实现同组互斥。同一组内选中一个按钮后，其他按钮自动取消选中。支持自定义文本、字体、颜色。

## 导出函数

### 创建

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `CreateRadioButton` | `int parent, int x, int y, int w, int h, int text_ptr, int text_len, int groupId, bool isChecked, int fg, int bg, int font_ptr, int font_len, int fontSize, bool bold, bool italic, bool underline` | `int` (单选按钮句柄) | 创建单选按钮 |

### 状态

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `GetRadioButtonState` | `int hRadio` | `bool` | 获取选中状态 |
| `SetRadioButtonState` | `int hRadio, bool checked` | `void` | 设置选中状态 |

### 回调

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetRadioButtonCallback` | `int hRadio, callback` | `void` | 设置状态改变回调 |

### 文本

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetRadioButtonText` | `int hRadio, int text_ptr, int text_len` | `void` | 设置文本 |
| `GetRadioButtonText` | `int hRadio, int buf_ptr, int buf_size` | `int` (UTF-8 字节数) | 获取文本；buf_ptr=0 返回所需大小 |

### 字体

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetRadioButtonFont` | `int hRadio, int font_ptr, int font_len, int fontSize, int bold, int italic, int underline` | `void` | 设置字体 |
| `GetRadioButtonFont` | `int hRadio, int font_buf_ptr, int font_buf_size, int* fontSize, int* bold, int* italic, int* underline` | `int` (字体名字节数) | 获取字体信息；font_buf_ptr=0 返回所需大小 |

### 颜色

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetRadioButtonColor` | `int hRadio, int fg, int bg` | `void` | 设置前景色和背景色（ARGB） |
| `GetRadioButtonColor` | `int hRadio, int* fg, int* bg` | `int` (0=成功，-1=失败) | 获取颜色（传址输出） |

### 位置

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetRadioButtonBounds` | `int hRadio, int x, int y, int w, int h` | `void` | 设置位置和大小 |

### 状态控制

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `EnableRadioButton` | `int hRadio, bool enabled` | `void` | 启用/禁用 |
| `ShowRadioButton` | `int hRadio, bool visible` | `void` | 显示/隐藏 |

## 回调签名

```c
// 单选按钮状态改变回调
void __stdcall OnRadioButtonChanged(int radioButtonId, int isChecked);
// isChecked: 1=选中, 0=未选中
```

## 注意事项

- `groupId` 用于分组互斥：相同 `groupId` 的单选按钮在同一组内，选中一个会自动取消组内其他按钮
- 不同 `groupId` 的单选按钮互不影响
- `SetRadioButtonFont` 的 bold/italic/underline 参数使用 int 类型（1=是，0=否），不是 bool
- `GetRadioButtonFont` 中 fontSize/bold/italic/underline 为传址输出参数
- `GetRadioButtonText` 需两次调用：第一次 buf_ptr=0 获取大小，第二次传入缓冲区
- 颜色格式为 ARGB（0xAARRGGBB）
