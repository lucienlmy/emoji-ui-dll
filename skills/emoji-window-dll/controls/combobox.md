# 组合框控件 (ComboBox)

## 概述

组合框控件是下拉列表与编辑框的组合，支持只读（纯下拉选择）和可编辑两种模式。提供标准版和 D2D 版本两种实现，D2D 版本完美支持彩色 Emoji 显示。

## C++ 导出函数列表

### 创建（标准版）

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `CreateComboBox` | `HWND parent, int x, int y, int w, int h, BOOL readOnly, UINT32 fgColor, UINT32 bgColor, int itemHeight, const uint8_t* font_bytes, int font_len, int fontSize, BOOL bold, BOOL italic, BOOL underline` | `int` 组合框句柄 |

### 创建（D2D 版本 — 支持彩色 Emoji）

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `CreateD2DComboBox` | `HWND parent, int x, int y, int w, int h, BOOL readOnly, UINT32 fgColor, UINT32 bgColor, int itemHeight, const uint8_t* font_bytes, int font_len, int fontSize, BOOL bold, BOOL italic, BOOL underline` | `int` 组合框句柄 |

### 项目管理（标准版）

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `AddComboItem` | `int hCB, const uint8_t* text_bytes, int text_len` | `int` 项目ID |
| `RemoveComboItem` | `int hCB, int index` | `void` |
| `ClearComboBox` | `int hCB` | `void` |

### 项目管理（D2D 版本）

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `AddD2DComboItem` | `int hCB, const uint8_t* text_bytes, int text_len` | `int` 项目ID |
| `RemoveD2DComboItem` | `int hCB, int index` | `void` |
| `ClearD2DComboBox` | `int hCB` | `void` |

### 选择操作（标准版）

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `GetComboSelectedIndex` | `int hCB` | `int` 选中索引，-1=无选中 |
| `SetComboSelectedIndex` | `int hCB, int index` | `void` |
| `GetComboItemCount` | `int hCB` | `int` 项目数量 |

### 选择操作（D2D 版本）

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `GetD2DComboSelectedIndex` | `int hCB` | `int` 选中索引，-1=无选中 |
| `SetD2DComboSelectedIndex` | `int hCB, int index` | `void` |
| `GetD2DComboItemCount` | `int hCB` | `int` 项目数量 |

### 文本操作（标准版）

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `GetComboItemText` | `int hCB, int index, uint8_t* buffer, int bufSize` | `int` 实际字节数 |
| `GetComboBoxText` | `int hCB, uint8_t* buffer, int bufSize` | `int` 实际字节数 |
| `SetComboBoxText` | `int hCB, const uint8_t* text_bytes, int text_len` | `void` |

### 文本操作（D2D 版本）

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `GetD2DComboItemText` | `int hCB, int index, uint8_t* buffer, int bufSize` | `int` 实际字节数 |
| `GetD2DComboText` | `int hCB, uint8_t* buffer, int bufSize` | `int` 实际字节数 |
| `SetD2DComboText` | `int hCB, const uint8_t* text_bytes, int text_len` | `void` |
| `GetD2DComboSelectedText` | `int hCB, uint8_t* buffer, int bufSize` | `int` UTF-8字节数(buffer=0时返回所需大小) |

### 回调

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `SetComboBoxCallback` | `int hCB, void* callback` | `void` |
| `SetD2DComboBoxCallback` | `int hCB, void* callback` | `void` |

### 通用操作（标准版）

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `EnableComboBox` | `int hCB, BOOL enable` | `void` |
| `ShowComboBox` | `int hCB, BOOL show` | `void` |
| `SetComboBoxBounds` | `int hCB, int x, int y, int w, int h` | `void` |

### 通用操作（D2D 版本）

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `EnableD2DComboBox` | `int hCB, BOOL enable` | `void` |
| `ShowD2DComboBox` | `int hCB, BOOL show` | `void` |
| `SetD2DComboBoxBounds` | `int hCB, int x, int y, int w, int h` | `void` |

## 回调签名

```c++
void __stdcall ComboBoxCallback(int hComboBox, int index);
```

- `hComboBox` — 组合框句柄
- `index` — 被选中的项目索引（从 0 开始）

## 注意事项

- 标准版和 D2D 版本参数完全相同，D2D 版本使用 Direct2D 渲染，完美支持彩色 Emoji
- `itemHeight` 参数控制下拉列表每项高度，默认 35 像素
- `readOnly` 为真时用户不能手动输入，只能从下拉列表中选择
- `GetComboBoxText` 获取编辑框当前文本（可能与选中项不同）；`GetComboItemText` 获取指定索引项文本
- 文本获取函数采用两次调用模式：第一次 buffer 传 0 获取所需大小
- 字体名、文本均为 UTF-8 编码
- `SetComboSelectedIndex` 传入 -1 可取消选中
