# 进度条控件 (ProgressBar)

## 概述

进度条控件用于显示任务完成进度，支持 0-100 百分比显示、不确定模式（加载动画）、自定义颜色和百分比文本显示。

## C++ 导出函数列表

### 创建

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `CreateProgressBar` | `HWND parent, int x, int y, int w, int h, int initVal, UINT32 fgColor, UINT32 bgColor, BOOL showText, UINT32 textColor` | `int` 进度条句柄 |

### 值操作

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `SetProgressValue` | `int hPB, int value` | `void` |
| `GetProgressValue` | `int hPB` | `int` 当前值(0-100) |
| `SetProgressIndeterminate` | `int hPB, BOOL indeterminate` | `void` |

### 颜色

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `SetProgressBarColor` | `int hPB, UINT32 fgColor, UINT32 bgColor` | `void` |
| `GetProgressBarColor` | `int hPB, int* outFg, int* outBg` | `int` 0=成功，-1=失败 |

### 回调

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `SetProgressBarCallback` | `int hPB, void* callback` | `void` |

### 通用操作

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `EnableProgressBar` | `int hPB, BOOL enable` | `void` |
| `ShowProgressBar` | `int hPB, BOOL show` | `void` |
| `SetProgressBarBounds` | `int hPB, int x, int y, int w, int h` | `void` |
| `GetProgressBarBounds` | `int hPB, int* x, int* y, int* w, int* h` | `int` 0=成功，-1=失败 |
| `SetProgressBarShowText` | `int hPB, BOOL showText` | `void` |
| `GetProgressBarEnabled` | `int hPB` | `int` 1=启用，0=禁用，-1=错误 |
| `GetProgressBarVisible` | `int hPB` | `int` 1=可见，0=不可见，-1=错误 |
| `GetProgressBarShowText` | `int hPB` | `int` 1=显示，0=不显示，-1=错误 |

## 回调签名

```c++
void __stdcall ProgressBarCallback(int hProgressBar, int value);
```

- `hProgressBar` — 进度条句柄
- `value` — 当前进度值 (0-100)

## 注意事项

- 进度值范围为 0-100，超出范围会被截断
- 不确定模式下进度条显示为循环动画，适用于无法预估进度的任务
- 颜色使用 ARGB 格式（如 `0xFF00FF00` 为绿色）
- `GetProgressBarColor` 的输出参数在易语言中需使用"传址"方式传参
- `showText` 为真时在进度条中央显示百分比文本
