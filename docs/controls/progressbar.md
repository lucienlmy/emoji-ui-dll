# 进度条控件 (ProgressBar)

[← 返回主文档](../../README.md)

## 概述

Element UI 风格的进度条控件，支持确定模式和不确定模式（循环动画）。

## API 文档

### 创建进度条

```c++
HWND __stdcall CreateProgressBar(
    HWND hParent,
    int x, int y, int width, int height,
    int initial_value,
    UINT32 fg_color,
    UINT32 bg_color,
    BOOL show_text,
    UINT32 text_color
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hParent` | 父窗口句柄 |
| `x, y` | 控件位置 |
| `width, height` | 控件尺寸 |
| `initial_value` | 初始进度值（0-100） |
| `fg_color` | 前景色/进度条颜色（ARGB格式） |
| `bg_color` | 背景色（ARGB格式） |
| `show_text` | 是否显示百分比文本 |
| `text_color` | 文本颜色（ARGB格式） |

### 设置/获取进度值

```c++
void __stdcall SetProgressValue(HWND hProgressBar, int value);
int __stdcall GetProgressValue(HWND hProgressBar);
```

### 不确定模式

```c++
void __stdcall SetProgressIndeterminate(HWND hProgressBar, BOOL indeterminate);
```

用于无法确定具体进度的场景，显示循环动画。

### 设置颜色

```c++
void __stdcall SetProgressBarColor(HWND hProgressBar, UINT32 fg_color, UINT32 bg_color);
```

**Element UI 状态颜色：**

- 主要/信息：#409EFF
- 成功：#67C23A
- 警告：#E6A23C
- 危险/错误：#F56C6C

### 设置回调

```c++
typedef void (__stdcall *ProgressBarCallback)(HWND hProgressBar, int value);
void __stdcall SetProgressBarCallback(HWND hProgressBar, ProgressBarCallback callback);
```

### 其他操作

```c++
void __stdcall EnableProgressBar(HWND hProgressBar, BOOL enable);
void __stdcall ShowProgressBar(HWND hProgressBar, BOOL show);
void __stdcall SetProgressBarBounds(HWND hProgressBar, int x, int y, int width, int height);
void __stdcall SetProgressBarShowText(HWND hProgressBar, BOOL show_text);
```

## 样式说明

- 圆角半径：4px
- 边框颜色：#DCDFE6
- 默认前景色：#409EFF
- 默认背景色：#EBEEF5
- 渐变效果：垂直线性渐变（顶部较亮）
- 动画帧率：60fps
- 平滑过渡：使用缓动函数
- 不确定模式：30% 宽度的进度条循环移动

## 易语言示例

```
.版本 2

.程序集变量 窗口句柄, 整数型
.程序集变量 进度条1, 整数型
.程序集变量 进度条2, 整数型

.子程序 _启动窗口_创建完毕

窗口句柄 = 创建Emoji窗口 ("进度条示例", 600, 400)

' 创建普通进度条（显示百分比，白色文本）
进度条1 = 创建进度条 (窗口句柄, 50, 80, 500, 30, 0, #409EFF, #EBEEF5, 真, #FFFFFFFF)

' 创建不确定模式进度条
进度条2 = 创建进度条 (窗口句柄, 50, 130, 500, 30, 0, #E6A23C, #EBEEF5, 假, #FFFFFFFF)
设置进度条不确定模式 (进度条2, 真)

设置进度条回调 (进度条1, &进度条回调)


.子程序 进度条回调, , 公开, stdcall
.参数 进度条句柄, 整数型
.参数 值, 整数型

调试输出 ("进度：", 值, "%")

.如果真 (值 = 100)
    ' 完成时改为绿色
    设置进度条颜色 (进度条句柄, #67C23A, #EBEEF5)
.如果真结束
```

## 相关文档

- [复选框](checkbox.md)
- [主题系统](../theme.md)
