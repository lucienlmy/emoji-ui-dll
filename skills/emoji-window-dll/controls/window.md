# Window - 窗口管理控件

## 概述

窗口是 emoji_window.dll 的顶层容器，所有控件必须创建在窗口之上。支持 Emoji 标题、自定义标题栏颜色、窗口图标等特性。通过字节集版本的 API 传入 UTF-8 编码标题可完美显示 Emoji 字符。

## 导出函数

### 创建与销毁

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `create_window_bytes` | `int title_bytes_ptr, int title_len, int width, int height` | `int` (窗口句柄) | 创建窗口，标题为 UTF-8 字节集 |
| `create_window_bytes_ex` | `int title_bytes_ptr, int title_len, int width, int height, int titlebar_color` | `int` (窗口句柄) | 扩展版，额外支持标题栏颜色 |
| `destroy_window` | `int hwnd` | `void` | 销毁窗口 |

### 消息循环

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `set_message_loop_main_window` | `int hwnd` | `void` | 设置消息循环主窗口 |
| `run_message_loop` | 无 | `int` | 运行消息循环（阻塞当前线程） |

### 标题

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `set_window_title` | `int hwnd, int title_bytes_ptr, int title_len` | `void` | 设置窗口标题 |
| `GetWindowTitle` | `int hwnd, int buf_ptr, int buf_size` | `int` (UTF-8 字节数) | 获取标题；buf_ptr=0 时返回所需大小 |

### 图标与外观

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `set_window_icon` | `int hwnd, string icon_path` | `void` | 设置窗口图标（文件路径） |
| `set_window_icon_bytes` | `int hwnd, int icon_data_ptr, int data_len` | `void` | 从字节集设置窗口图标（易语言插入图片资源后传入 `取变量数据地址(图标字节集)` 和 `取字节集长度(图标字节集)`） |
| `set_window_titlebar_color` | `int hwnd, int color` | `void` | 设置标题栏颜色（RGB，0=跟随主题） |
| `GetWindowTitlebarColor` | `int hwnd` | `int` (RGB，-1=错误) | 获取标题栏颜色 |

### 位置与可视

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `GetWindowBounds` | `int hwnd, int* x, int* y, int* w, int* h` | `void` | 获取位置和大小（传址输出） |
| `SetWindowBounds` | `int hwnd, int x, int y, int w, int h` | `void` | 设置位置和大小 |
| `GetWindowVisible` | `int hwnd` | `int` (1=可见，0=不可见，-1=错误) | 获取可视状态 |
| `ShowEmojiWindow` | `int hwnd, bool visible` | `void` | 显示/隐藏窗口 |

### 回调

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetWindowResizeCallback` | `callback` | `void` | 设置窗口大小改变回调 |
| `SetWindowCloseCallback` | `callback` | `void` | 设置窗口关闭回调 |

## 回调签名

```c
// 窗口大小改变回调
void __stdcall OnWindowResize(int hwnd, int width, int height);

// 窗口关闭回调
void __stdcall OnWindowClose(int hwnd);
```

## 注意事项

- 标题使用字节集版本（`create_window_bytes` / `create_window_bytes_ex`）才能正确显示 Emoji
- `run_message_loop()` 会阻塞调用线程，直到主窗口关闭才返回
- `titlebar_color` 使用十进制 RGB 颜色（不是 ARGB），传 0 表示跟随系统主题
- `GetWindowTitle` 需两次调用：第一次 buf_ptr=0 获取所需大小，第二次传入缓冲区读取内容
- `GetWindowBounds` 的 x/y/w/h 参数需要传址（指针），易语言中使用 `传址 变量`
- 窗口关闭回调在用户点击关闭按钮或代码调用 `destroy_window` 时均会触发
- 使用 `set_window_icon_bytes` 时，易语言可插入 .ico 图片资源，先赋值 `图标字节集 ＝ #图标1`，再传入 `取变量数据地址(图标字节集)` 和 `取字节集长度(图标字节集)`，无需依赖外部文件路径
