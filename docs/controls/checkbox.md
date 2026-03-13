# 复选框控件 (CheckBox)

[← 返回主文档](../../README.md)

## 概述

Element UI 风格的复选框控件，支持选中/未选中状态切换。

## API 文档

### 创建复选框

```c++
HWND __stdcall CreateCheckBox(
    HWND hParent,
    int x, int y, int width, int height,
    const unsigned char* text_bytes, int text_len,
    BOOL checked,
    UINT32 fg_color,
    UINT32 bg_color
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hParent` | 父窗口句柄 |
| `x, y` | 控件位置 |
| `width, height` | 控件尺寸 |
| `text_bytes` | UTF-8 编码的文本字节集指针 |
| `text_len` | 文本字节集长度 |
| `checked` | 初始选中状态（TRUE=选中，FALSE=未选中） |
| `fg_color` | 前景色（ARGB格式，如 0xFF303133） |
| `bg_color` | 背景色（ARGB格式，如 0xFFFFFFFF） |

**返回值：** 复选框控件句柄

### 获取/设置状态

```c++
BOOL __stdcall GetCheckBoxState(HWND hCheckBox);
void __stdcall SetCheckBoxState(HWND hCheckBox, BOOL checked);
```

### 设置回调

```c++
typedef void (__stdcall *CheckBoxCallback)(HWND hCheckBox, BOOL checked);
void __stdcall SetCheckBoxCallback(HWND hCheckBox, CheckBoxCallback callback);
```

### 其他操作

```c++
void __stdcall EnableCheckBox(HWND hCheckBox, BOOL enable);
void __stdcall ShowCheckBox(HWND hCheckBox, BOOL show);
void __stdcall SetCheckBoxText(HWND hCheckBox, const unsigned char* text_bytes, int text_len);
void __stdcall SetCheckBoxBounds(HWND hCheckBox, int x, int y, int width, int height);
```

## 样式说明

复选框采用 Element UI 设计规范：

- 复选框尺寸：14x14 像素
- 圆角半径：2px
- 选中颜色：#409EFF（Element UI 主色）
- 边框颜色：#DCDFE6（默认）/ #409EFF（悬停/选中）
- 禁用颜色：#C0C4CC
- 文本字体：Microsoft YaHei UI，14px
- 文本间距：复选框右侧 8px

## 易语言示例

```
.版本 2

.程序集变量 窗口句柄, 整数型
.程序集变量 复选框1, 整数型

.子程序 _启动窗口_创建完毕
.局部变量 文本UTF8, 字节集
.局部变量 文本指针, 整数型

窗口句柄 = 创建Emoji窗口 ("复选框示例", 400, 300)

文本UTF8 = 到UTF8 ("接受用户协议")
文本指针 = 取字节集数据地址 (文本UTF8)

复选框1 = 创建复选框 (窗口句柄, 50, 80, 200, 30, 文本指针, 取字节集长度 (文本UTF8), 假, #FF303133, #FFFFFFFF)

设置复选框回调 (复选框1, &复选框回调)


.子程序 复选框回调, , 公开, stdcall
.参数 复选框句柄, 整数型
.参数 选中状态, 逻辑型

调试输出 ("复选框状态：", 选中状态)
```

## 相关文档

- [单选按钮](radiobutton.md)
- [按钮控件](button.md)
