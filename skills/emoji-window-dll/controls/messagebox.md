# 信息框控件 (MessageBox)

## 概述

信息框用于向用户显示提示信息或请求确认操作。提供两种形式：纯信息提示框（只有确定按钮）和确认框（确定 + 取消按钮）。标题和图标支持 Emoji，采用自绘窗口实现。

## C++ 导出函数列表

### 信息提示框

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `show_message_box_bytes` | `HWND parent, const uint8_t* title_bytes, int title_len, const uint8_t* msg_bytes, int msg_len, const uint8_t* icon_bytes, int icon_len` | `void` |

### 确认框

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `show_confirm_box_bytes` | `HWND parent, const uint8_t* title_bytes, int title_len, const uint8_t* msg_bytes, int msg_len, const uint8_t* icon_bytes, int icon_len, void* callback` | `void` |

## 回调签名

### 确认框回调

```c++
void __stdcall ConfirmCallback(int confirmed);
```

- `confirmed` — 1 = 用户点击了确认，0 = 用户点击了取消

## 参数说明

| 参数 | 说明 |
|------|------|
| `parent` | 父窗口句柄（信息框居中于此窗口） |
| `title_bytes` | 标题 UTF-8 字节集指针 |
| `title_len` | 标题字节集长度 |
| `msg_bytes` | 消息内容 UTF-8 字节集指针 |
| `msg_len` | 消息字节集长度 |
| `icon_bytes` | 图标 UTF-8 字节集指针（支持 Emoji） |
| `icon_len` | 图标字节集长度 |
| `callback` | 确认框回调函数指针（仅 `show_confirm_box_bytes`） |

## 注意事项

- 所有文本参数（标题、消息、图标）均为 UTF-8 编码字节集
- `icon_bytes` 可传入 Emoji 的 UTF-8 编码作为图标显示，如 `⚠️`、`✅`、`❌`、`ℹ️` 等
- 信息提示框是模态的，关闭后才能操作父窗口
- 确认框通过回调返回结果，不阻塞调用线程
- 信息提示框无回调，用户点击确定后自动关闭
- 在易语言中，字节集指针通过 `取变量数据地址()` 获取，长度通过 `取字节集长度()` 获取
