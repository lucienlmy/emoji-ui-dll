# 选项卡控件 (TabControl)

## 概述

选项卡控件用于在同一区域切换显示不同的内容页面。每个 Tab 页可关联一个内容窗口句柄，支持标题设置、动态添加/移除页面和切换回调。

## C++ 导出函数列表

### 创建和销毁

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `CreateTabControl` | `HWND parent, int x, int y, int w, int h` | `int` TabControl 句柄 |
| `DestroyTabControl` | `int hTab` | `void` |

### 页面管理

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `AddTabItem` | `int hTab, const uint8_t* title_bytes, int title_len, HWND contentHwnd` | `int` Tab 页索引 |
| `RemoveTabItem` | `int hTab, int index` | `BOOL` |

### 选择操作

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `GetCurrentTabIndex` | `int hTab` | `int` 当前选中索引 |
| `SelectTab` | `int hTab, int index` | `BOOL` |
| `GetTabCount` | `int hTab` | `int` Tab 页数量 |
| `GetTabContentWindow` | `int hTab, int index` | `int` 内容窗口句柄 |

### 标题操作

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `GetTabTitle` | `int hTab, int index, uint8_t* buffer, int bufSize` | `int` UTF-8字节数(buffer=0时返回所需大小) |
| `SetTabTitle` | `int hTab, int index, const uint8_t* title_bytes, int title_len` | `int` 0=成功，-1=失败 |

### 位置和大小

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `GetTabControlBounds` | `int hTab, int* x, int* y, int* w, int* h` | `int` 0=成功，-1=失败 |
| `SetTabControlBounds` | `int hTab, int x, int y, int w, int h` | `int` 0=成功，-1=失败 |

### 回调

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `SetTabCallback` | `int hTab, void* callback` | `void` |

### 通用操作

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `ShowTabControl` | `int hTab, int visible` | `int` 0=成功，-1=失败 |
| `EnableTabControl` | `int hTab, int enable` | `int` 0=成功，-1=失败 |
| `UpdateTabControlLayout` | `int hTab` | `void` |

### 属性查询

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `GetTabControlVisible` | `int hTab` | `int` 1=可见，0=不可见，-1=错误 |

## 回调签名

```c++
void __stdcall TabCallback(int hTabControl, int newIndex);
```

- `hTabControl` — TabControl 句柄
- `newIndex` — 新选中的 Tab 页索引

## 注意事项

- `AddTabItem` 的 `contentHwnd` 参数可传 0，此时自动创建一个空白内容窗口
- 标题使用 UTF-8 编码字节集，支持 Emoji
- `GetTabTitle` 采用两次调用模式：第一次 buffer 传 0 获取所需大小，第二次传实际缓冲区
- `ShowTabControl` 和 `EnableTabControl` 的参数为 int 类型（1=显示/启用，0=隐藏/禁用），不是 BOOL
- 窗口大小改变后应调用 `UpdateTabControlLayout` 更新布局
- `GetTabControlBounds` 输出参数在易语言中需使用"传址"方式传参
- 移除 Tab 页会销毁对应的内容窗口（如果是自动创建的）
- 不再使用时应调用 `DestroyTabControl` 释放资源
