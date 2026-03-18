# 热键控件 (HotKey)

## 概述

热键控件用于让用户通过键盘录入自定义快捷键组合。用户点击控件后按下快捷键即可录入，支持 Ctrl、Shift、Alt 修饰键的任意组合。

## C++ 导出函数列表

### 创建

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `CreateHotKeyControl` | `HWND parent, int x, int y, int w, int h, UINT32 fgColor, UINT32 bgColor` | `int` 热键控件句柄 |

### 热键操作

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `GetHotKey` | `int hHK, int* vk_code, int* modifiers` | `void` |
| `SetHotKey` | `int hHK, int vk_code, int modifiers` | `void` |
| `ClearHotKey` | `int hHK` | `void` |

### 回调

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `SetHotKeyCallback` | `int hHK, void* callback` | `void` |

### 通用操作

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `EnableHotKeyControl` | `int hHK, BOOL enable` | `void` |
| `ShowHotKeyControl` | `int hHK, BOOL show` | `void` |
| `SetHotKeyControlBounds` | `int hHK, int x, int y, int w, int h` | `void` |

## 回调签名

```c++
void __stdcall HotKeyCallback(int hHotKey, int vk_code, int modifiers);
```

- `hHotKey` — 热键控件句柄
- `vk_code` — Windows 虚拟键码（VK_* 常量，如 VK_F1=0x70, VK_A=0x41）
- `modifiers` — 修饰键组合（按位标志）

## 修饰键常量

| 常量 | 值 | 说明 |
|------|-----|------|
| Ctrl | 1 | 控制键 |
| Shift | 2 | 上档键 |
| Alt | 4 | 替换键 |

修饰键可按位组合，例如：
- `Ctrl + Shift` = 1 + 2 = **3**
- `Ctrl + Alt` = 1 + 4 = **5**
- `Ctrl + Shift + Alt` = 1 + 2 + 4 = **7**

## 注意事项

- `GetHotKey` 的 `vk_code` 和 `modifiers` 为输出参数，在易语言中需使用"传址"方式传参
- `SetHotKey` 可通过代码预设快捷键
- `ClearHotKey` 清除当前录入的热键，控件恢复为空状态
- 回调在用户每次修改热键时触发
- 颜色使用 ARGB 格式
