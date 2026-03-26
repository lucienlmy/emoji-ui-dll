# 列表框控件 (ListBox)

## 概述

列表框控件用于显示可选择的文本列表，支持单选和多选模式、自定义颜色，适用于列表数据的展示与选择。

## C++ 导出函数列表

### 创建

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `CreateListBox` | `HWND parent, int x, int y, int w, int h, BOOL multiSelect, UINT32 fgColor, UINT32 bgColor` | `int` 列表框句柄 |

### 项目管理

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `AddListItem` | `int hListBox, const uint8_t* text_bytes, int text_len` | `int` 项目ID |
| `RemoveListItem` | `int hListBox, int index` | `void` |
| `ClearListBox` | `int hListBox` | `void` |

### 选择操作

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `GetSelectedIndex` | `int hListBox` | `int` 选中索引，-1=无选中 |
| `SetSelectedIndex` | `int hListBox, int index` | `void` |

### 查询

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `GetListItemCount` | `int hListBox` | `int` 项目数量 |
| `GetListItemText` | `int hListBox, int index, uint8_t* buffer, int bufferSize` | `int` 实际复制字节数 |
| `SetListItemText` | `int hListBox, int index, const uint8_t* text_bytes, int text_len` | `BOOL` 成功TRUE/失败FALSE |

### 回调

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `SetListBoxCallback` | `int hListBox, void* callback` | `void` |

### 通用操作

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `EnableListBox` | `int hListBox, BOOL enable` | `void` |
| `ShowListBox` | `int hListBox, BOOL show` | `void` |
| `SetListBoxBounds` | `int hListBox, int x, int y, int w, int h` | `void` |

## 回调签名

```c++
void __stdcall ListBoxCallback(int hListBox, int index);
```

- `hListBox` — 列表框句柄
- `index` — 被选中的项目索引（从 0 开始）

## 注意事项

- 项目索引从 0 开始
- `SetSelectedIndex` 传入 -1 可取消选中
- `GetListItemText` 采用两次调用模式：第一次 buffer 传 0 获取所需大小，第二次分配缓冲区后再调用获取内容
- `SetListItemText` 可直接修改指定索引项目的文本，无需删除重建
- 文本均为 UTF-8 编码，在易语言中需转换为字节集传递
- 多选模式下 `GetSelectedIndex` 只返回第一个选中项
- 当项目总高度超过列表框可见区域时，自动显示圆角滚动条滑块
- 支持鼠标滚轮滚动
