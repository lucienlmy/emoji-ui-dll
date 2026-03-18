# 分组框控件 (GroupBox)

## 概述

分组框控件用于将相关控件组织在一起，提供带标题的边框容器。支持自定义边框颜色、背景色和字体，可添加/移除子控件。

## C++ 导出函数列表

### 创建

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `CreateGroupBox` | `HWND parent, int x, int y, int w, int h, const uint8_t* title_bytes, int title_len, UINT32 borderColor, UINT32 bgColor, const uint8_t* font_bytes, int font_len, int fontSize, BOOL bold, BOOL italic, BOOL underline` | `int` 分组框句柄 |

### 子控件管理

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `AddChildToGroup` | `int hGroup, int hChild` | `void` |
| `RemoveChildFromGroup` | `int hGroup, int hChild` | `void` |

### 标题操作

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `SetGroupBoxTitle` | `int hGroup, const uint8_t* title_bytes, int title_len` | `void` |
| `GetGroupBoxTitle` | `int hGroup, uint8_t* buffer, int bufSize` | `int` UTF-8字节数(buffer=0时返回所需大小) |

### 属性获取

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `GetGroupBoxBounds` | `int hGroup, int* x, int* y, int* w, int* h` | `int` 0=成功，-1=失败 |
| `GetGroupBoxColor` | `int hGroup, int* borderColor, int* bgColor` | `int` 0=成功，-1=失败 |
| `GetGroupBoxVisible` | `int hGroup` | `int` 1=可见，0=不可见，-1=错误 |
| `GetGroupBoxEnabled` | `int hGroup` | `int` 1=启用，0=禁用，-1=错误 |

### 回调

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `SetGroupBoxCallback` | `int hGroup, void* callback` | `void` |

### 通用操作

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `EnableGroupBox` | `int hGroup, BOOL enable` | `void` |
| `ShowGroupBox` | `int hGroup, BOOL show` | `void` |
| `SetGroupBoxBounds` | `int hGroup, int x, int y, int w, int h` | `void` |

## 回调签名

```c++
void __stdcall GroupBoxCallback(int hGroupBox);
```

- `hGroupBox` — 分组框句柄

## 注意事项

- 标题和字体名使用 UTF-8 编码字节集
- `font_bytes` 传 0 时使用默认字体；`fontSize` 传 0 时使用默认大小 14
- 分组框内的子控件坐标是相对于父窗口的，不是相对于分组框
- `AddChildToGroup` 将子控件逻辑关联到分组框，便于统一管理（启用/禁用/显示/隐藏等操作会影响子控件）
- `GetGroupBoxColor` 输出参数在易语言中需使用"传址"方式传参
- 边框颜色和背景色使用 ARGB 格式
