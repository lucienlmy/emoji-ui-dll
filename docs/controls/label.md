# 标签控件 (Label)

[← 返回主文档](../../README.md)

## 概述

文本标签控件,支持自动换行、多种对齐方式和字体样式。

## API 文档

### 创建标签

```c++
HWND __stdcall CreateLabel(
    HWND hParent,
    int x, int y, int width, int height,
    const unsigned char* text_bytes, int text_len,
    UINT32 fg_color,
    UINT32 bg_color,
    const unsigned char* font_name_bytes, int font_name_len,
    int font_size,
    BOOL bold,
    BOOL italic,
    BOOL underline,
    int alignment,
    BOOL word_wrap
);
```

**参数说明:**

| 参数 | 说明 |
|------|------|
| `hParent` | 父窗口句柄 |
| `x, y` | 控件位置 |
| `width, height` | 控件尺寸 |
| `text_bytes` | UTF-8 编码的文本字节集指针 |
| `text_len` | 文本字节集长度 |
| `fg_color` | 前景色/文本颜色(ARGB格式) |
| `bg_color` | 背景色(ARGB格式) |
| `font_name_bytes` | UTF-8 编码的字体名称指针 |
| `font_name_len` | 字体名称长度 |
| `font_size` | 字体大小(像素) |
| `bold` | 是否粗体 |
| `italic` | 是否斜体 |
| `underline` | 是否下划线 |
| `alignment` | 对齐方式(0=左对齐, 1=居中, 2=右对齐) |
| `word_wrap` | 是否自动换行 |

**返回值:** 标签控件句柄

### 设置/获取文本

```c++
void __stdcall SetLabelText(HWND hLabel, const unsigned char* text_bytes, int text_len);
int __stdcall GetLabelText(HWND hLabel, unsigned char* buffer, int buffer_size);
```

### 设置样式

```c++
void __stdcall SetLabelColor(HWND hLabel, UINT32 fg_color, UINT32 bg_color);
void __stdcall SetLabelFont(HWND hLabel, const unsigned char* font_name_bytes, int font_name_len, int font_size, BOOL bold, BOOL italic, BOOL underline);
void __stdcall SetLabelAlignment(HWND hLabel, int alignment);
void __stdcall SetLabelWordWrap(HWND hLabel, BOOL word_wrap);
```

### 其他操作

```c++
void __stdcall EnableLabel(HWND hLabel, BOOL enable);
void __stdcall ShowLabel(HWND hLabel, BOOL show);
void __stdcall SetLabelBounds(HWND hLabel, int x, int y, int width, int height);
```

## 样式说明

- 默认字体: Microsoft YaHei UI
- 默认字体大小: 14px
- 支持对齐方式: 左对齐、居中、右对齐
- 自动换行: 根据控件宽度自动换行
- 支持手动换行符: `\n`

## 易语言示例

```
.版本 2

.程序集变量 窗口句柄, 整数型
.程序集变量 标签1, 整数型
.程序集变量 标签2, 整数型
.程序集变量 标签3, 整数型

.子程序 _启动窗口_创建完毕

窗口句柄 = 创建Emoji窗口 ("标签示例", 600, 400)

' 创建普通标签(左对齐)
标签1 = 创建标签_辅助 (窗口句柄, 20, 20, 560, 30, "这是一个普通标签", #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE, "Microsoft YaHei UI", 14, 假, 假, 假, 0, 假)

' 创建居中标签(粗体)
标签2 = 创建标签_辅助 (窗口句柄, 20, 70, 560, 40, "标题文本", #COLOR_PRIMARY, #COLOR_BG_LIGHT, "Microsoft YaHei UI", 18, 真, 假, 假, 1, 假)

' 创建自动换行标签
标签3 = 创建标签_辅助 (窗口句柄, 20, 130, 560, 80, "这是一个很长的文本，启用换行后会自动根据宽度换行显示。这样就可以完整显示所有内容了。", #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE, "Microsoft YaHei UI", 14, 假, 假, 假, 0, 真)

运行消息循环 ()
```

## 注意事项

⚠️ **重要提示**:

1. 文本必须使用 UTF-8 编码的字节集
2. 自动换行需要设置 `word_wrap` 参数为 TRUE
3. 手动换行使用 `\n` 字符
4. 背景色设置为透明可使用 `#COLOR_TRANSPARENT`

## 相关文档

- [按钮控件](button.md)
- [编辑框](editbox.md)
