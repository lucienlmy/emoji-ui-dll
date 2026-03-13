# 编辑框控件 (EditBox)

[← 返回主文档](../../README.md)

## 概述

单行/多行文本编辑框,支持垂直居中、密码模式、只读模式和按键回调。

## API 文档

### 创建编辑框

```c++
HWND __stdcall CreateEditBox(
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
    BOOL multiline,
    BOOL readonly,
    BOOL password,
    BOOL border,
    BOOL vertical_center
);
```

**参数说明:**

| 参数 | 说明 |
|------|------|
| `hParent` | 父窗口句柄 |
| `x, y` | 控件位置 |
| `width, height` | 控件尺寸 |
| `text_bytes` | UTF-8 编码的初始文本指针 |
| `text_len` | 文本长度 |
| `fg_color` | 前景色/文本颜色(ARGB格式) |
| `bg_color` | 背景色(ARGB格式) |
| `font_name_bytes` | UTF-8 编码的字体名称指针 |
| `font_name_len` | 字体名称长度 |
| `font_size` | 字体大小(像素) |
| `bold` | 是否粗体 |
| `italic` | 是否斜体 |
| `underline` | 是否下划线 |
| `alignment` | 对齐方式(0=左对齐, 1=居中, 2=右对齐) |
| `multiline` | 是否多行模式 |
| `readonly` | 是否只读 |
| `password` | 是否密码模式(显示为 *) |
| `border` | 是否显示边框 |
| `vertical_center` | 是否垂直居中(仅单行有效) |

**返回值:** 编辑框控件句柄

### 设置/获取文本

```c++
void __stdcall SetEditBoxText(HWND hEditBox, const unsigned char* text_bytes, int text_len);
int __stdcall GetEditBoxText(HWND hEditBox, unsigned char* buffer, int buffer_size);
```

### 设置按键回调

```c++
typedef void (__stdcall *EditBoxKeyCallback)(
    HWND hEditBox,
    int key_code,
    int key_down,
    int shift,
    int ctrl,
    int alt
);
void __stdcall SetEditBoxKeyCallback(HWND hEditBox, EditBoxKeyCallback callback);
```

**回调参数:**
- `key_code`: Windows 虚拟键码(如 13=回车, 27=Esc, 8=退格)
- `key_down`: 1=键按下, 0=键松开
- `shift`: 1=Shift键按下, 0=未按
- `ctrl`: 1=Ctrl键按下, 0=未按
- `alt`: 1=Alt键按下, 0=未按

### 设置样式

```c++
void __stdcall SetEditBoxColor(HWND hEditBox, UINT32 fg_color, UINT32 bg_color);
void __stdcall SetEditBoxReadOnly(HWND hEditBox, BOOL readonly);
void __stdcall SetEditBoxVerticalCenter(HWND hEditBox, BOOL vertical_center);
```

### 其他操作

```c++
void __stdcall EnableEditBox(HWND hEditBox, BOOL enable);
void __stdcall ShowEditBox(HWND hEditBox, BOOL show);
void __stdcall SetEditBoxBounds(HWND hEditBox, int x, int y, int width, int height);
void __stdcall SetEditBoxFocus(HWND hEditBox);
```

## 样式说明

- 默认字体: Microsoft YaHei UI
- 默认字体大小: 12px
- 边框颜色: #DCDFE6
- 焦点边框: #409EFF
- 单行编辑框支持垂直居中
- 密码模式显示为 `*` 字符

## 易语言示例

```
.版本 2

.程序集变量 窗口句柄, 整数型
.程序集变量 编辑框1, 整数型
.程序集变量 编辑框2, 整数型
.程序集变量 编辑框3, 整数型

.子程序 _启动窗口_创建完毕

窗口句柄 = 创建Emoji窗口 ("编辑框示例", 500, 400)

' 创建单行编辑框(垂直居中)
编辑框1 = 创建编辑框_辅助 (窗口句柄, 20, 30, 280, 30, "请输入用户名", #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE, "Microsoft YaHei UI", 12, 假, 假, 假, 0, 假, 假, 假, 真, 真)

' 设置按键回调
设置编辑框按键回调 (编辑框1, &编辑框按键回调)

' 创建密码框
编辑框2 = 创建编辑框_辅助 (窗口句柄, 20, 80, 280, 30, "", #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE, "Microsoft YaHei UI", 12, 假, 假, 假, 0, 假, 假, 真, 真, 假)

' 创建多行编辑框
编辑框3 = 创建编辑框_辅助 (窗口句柄, 20, 130, 400, 150, "请输入详细内容...", #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE, "Microsoft YaHei UI", 12, 假, 假, 假, 0, 真, 假, 假, 真, 假)

运行消息循环 ()


.子程序 编辑框按键回调, , 公开, stdcall
.参数 编辑框句柄, 整数型
.参数 键码, 整数型
.参数 按下或松开, 整数型
.参数 Shift键, 整数型
.参数 Ctrl键, 整数型
.参数 Alt键, 整数型

.如果真 (按下或松开 = 1)
    .如果真 (键码 = 13)  ' 回车键
        信息框 ("按下了回车键", 0, "提示")
    .如果真结束
.如果真结束
```

## 注意事项

⚠️ **重要提示**:

1. 文本必须使用 UTF-8 编码的字节集
2. 垂直居中仅对单行编辑框有效
3. 密码模式会将输入字符显示为 `*`
4. 多行模式支持 Ctrl+Enter 换行
5. 按键回调可用于实现自定义快捷键

## 相关文档

- [标签控件](label.md)
- [按钮控件](button.md)
