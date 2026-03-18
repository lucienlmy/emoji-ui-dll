# Button - Emoji 按钮控件

## 概述

支持 Emoji 图标的自绘按钮控件。按钮上方显示 Emoji，下方显示文字，背景色可自定义。通过全局唯一的点击回调函数，按 buttonId 区分不同按钮的点击事件。

## 导出函数

### 创建

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `create_emoji_button_bytes` | `int parent_hwnd, int emoji_bytes_ptr, int emoji_len, int text_bytes_ptr, int text_len, int x, int y, int w, int h, int bg_color` | `int` (按钮 ID) | 创建 Emoji 按钮，bg_color 为 ARGB |

### 回调

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `set_button_click_callback` | `callback` | `void` | 设置全局按钮点击回调 |

### 文本与 Emoji

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `GetButtonText` | `int btnId, int buf_ptr, int buf_size` | `int` (UTF-8 字节数) | 获取按钮文本；buf_ptr=0 返回所需大小 |
| `SetButtonText` | `int btnId, int text_bytes_ptr, int text_len` | `void` | 设置按钮文本 |
| `GetButtonEmoji` | `int btnId, int buf_ptr, int buf_size` | `int` (UTF-8 字节数) | 获取按钮 Emoji；buf_ptr=0 返回所需大小 |
| `SetButtonEmoji` | `int btnId, int emoji_bytes_ptr, int emoji_len` | `void` | 设置按钮 Emoji |

### 位置与外观

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `GetButtonBounds` | `int btnId, int* x, int* y, int* w, int* h` | `void` | 获取按钮位置（传址输出） |
| `SetButtonBounds` | `int btnId, int x, int y, int w, int h` | `void` | 设置按钮位置 |
| `GetButtonBackgroundColor` | `int btnId` | `int` (ARGB) | 获取按钮背景色 |
| `SetButtonBackgroundColor` | `int btnId, int bg_color` | `void` | 设置按钮背景色（ARGB） |

### 状态控制

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `GetButtonVisible` | `int btnId` | `bool` | 获取可视状态 |
| `ShowButton` | `int btnId, bool visible` | `void` | 显示/隐藏按钮 |
| `GetButtonEnabled` | `int btnId` | `bool` | 获取启用状态 |
| `EnableButton` | `int parent_hwnd, int btnId, bool enabled` | `void` | 启用/禁用按钮 |
| `DisableButton` | `int parent_hwnd, int btnId` | `void` | 禁用按钮（快捷方式） |

## 回调签名

```c
// 全局按钮点击回调
void __stdcall OnButtonClick(int buttonId, int parentHwnd);
```

## 注意事项

- 按钮 ID 由 `create_emoji_button_bytes` 动态分配返回，必须保存到变量中供后续操作使用
- 点击回调是**全局唯一**的，所有按钮共享同一个回调，需在回调中通过 `buttonId` 判断是哪个按钮被点击
- `EnableButton` / `DisableButton` 需要传入父窗口句柄和按钮 ID 两个参数
- `GetButtonText` / `GetButtonEmoji` 需两次调用：第一次 buf_ptr=0 获取大小，第二次传入缓冲区
- 背景色使用 ARGB 格式（0xAARRGGBB）
