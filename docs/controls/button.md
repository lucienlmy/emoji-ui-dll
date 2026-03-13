# 按钮控件 (Button)

[← 返回主文档](../../README.md)

## 创建 Emoji 按钮

创建支持彩色 Emoji 的按钮控件。

```c++
int create_emoji_button_bytes(
    HWND parent,
    const unsigned char* emoji_bytes,
    int emoji_len,
    const unsigned char* text_bytes,
    int text_len,
    int x, int y, int width, int height,
    unsigned int bg_color
);
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `parent` | 父窗口句柄 |
| `emoji_bytes` | UTF-8 编码的 Emoji 字节集指针 |
| `emoji_len` | Emoji 字节集长度 |
| `text_bytes` | UTF-8 编码的文本字节集指针 |
| `text_len` | 文本字节集长度 |
| `x, y` | 按钮位置 |
| `width, height` | 按钮尺寸 |
| `bg_color` | 背景色（ARGB格式） |

### 返回值

按钮 ID，失败返回 -1

## 设置按钮点击回调

```c++
typedef void (__stdcall *ButtonClickCallback)(int button_id);
void __stdcall set_button_click_callback(ButtonClickCallback callback);
```

## 易语言声明

```
.DLL命令 创建Emoji按钮_字节集, 整数型, "emoji_window.dll", "create_emoji_button_bytes"
    .参数 父窗口句柄, 整数型
    .参数 Emoji字节集指针, 整数型
    .参数 Emoji长度, 整数型
    .参数 文本字节集指针, 整数型
    .参数 文本长度, 整数型
    .参数 X坐标, 整数型
    .参数 Y坐标, 整数型
    .参数 宽度, 整数型
    .参数 高度, 整数型
    .参数 背景色, 整数型

.DLL命令 设置按钮点击回调, , "emoji_window.dll", "set_button_click_callback"
    .参数 回调函数指针, 子程序指针
```

## 易语言使用示例

```
.程序集变量 按钮ID, 整数型

.子程序 _启动窗口_创建完毕
.局部变量 emoji字节集, 字节集
.局部变量 文本字节集, 字节集

emoji字节集 = { 240, 159, 152, 128 }  ' 😀
文本字节集 = 到UTF8 ("点击我")

按钮ID = 创建Emoji按钮_字节集 (窗口句柄, 取字节集数据地址 (emoji字节集), 取字节集长度 (emoji字节集), 取字节集数据地址 (文本字节集), 取字节集长度 (文本字节集), 10, 10, 100, 40, #409EFF)

设置按钮点击回调 (&按钮点击处理)


.子程序 按钮点击处理, , 公开, stdcall
.参数 按钮ID_, 整数型

.如果真 (按钮ID_ = 按钮ID)
    信息框 ("按钮被点击了！", 0, "提示")
.如果真结束
```

## 注意事项

⚠️ **重要提示**：在易语言 IDE 中，Unicode 特殊符号（如 emoji）不支持直接输入，因为易语言使用 ANSI 编码。必须使用以下两种方法之一：

1. **使用预先转换好的 UTF-8 字节集**（推荐）
2. **从外部文件读取 emoji 文本**

详见 [常见问题](../faq.md#emoji-显示问题)。
