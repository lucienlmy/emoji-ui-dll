# 图片框控件 (PictureBox)

## 概述

图片框控件用于显示图片，支持从文件和内存加载，支持 PNG、JPG、BMP、GIF 格式，提供多种缩放模式和透明度控制。

## C++ 导出函数列表

### 创建

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `CreatePictureBox` | `HWND parent, int x, int y, int w, int h, int scaleMode, UINT32 bgColor` | `int` 图片框句柄 |

### 图片加载

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `LoadImageFromFile` | `int hPB, const uint8_t* path_bytes, int path_len` | `BOOL` 成功=TRUE |
| `LoadImageFromMemory` | `int hPB, const uint8_t* data_ptr, int data_len` | `BOOL` 成功=TRUE |
| `ClearImage` | `int hPB` | `void` |

### 显示控制

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `SetImageOpacity` | `int hPB, float opacity` | `void` |
| `SetPictureBoxScaleMode` | `int hPB, int scaleMode` | `void` |
| `SetPictureBoxBackgroundColor` | `int hPB, UINT32 bgColor` | `void` |

### 回调

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `SetPictureBoxCallback` | `int hPB, void* callback` | `void` |

### 通用操作

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `EnablePictureBox` | `int hPB, BOOL enable` | `void` |
| `ShowPictureBox` | `int hPB, BOOL show` | `void` |
| `SetPictureBoxBounds` | `int hPB, int x, int y, int w, int h` | `void` |

## 回调签名

```c++
void __stdcall PictureBoxCallback(int hPictureBox);
```

- `hPictureBox` — 图片框句柄（点击时触发）

## 缩放模式

| 值 | 模式 | 说明 |
|----|------|------|
| 0 | 不缩放 | 原始尺寸显示，超出部分裁剪 |
| 1 | 拉伸 | 拉伸填满整个图片框，可能变形 |
| 2 | 等比缩放 | 保持宽高比缩放，适应图片框 |
| 3 | 居中 | 原始尺寸居中显示 |

## 注意事项

- 支持格式：PNG、JPG、BMP、GIF
- `LoadImageFromFile` 的文件路径为 UTF-8 编码字节集
- `LoadImageFromMemory` 可从内存中的图片数据直接加载，适用于网络下载或资源嵌入场景
- `SetImageOpacity` 的透明度范围为 0.0（完全透明）到 1.0（完全不透明）
- 加载新图片前无需手动调用 `ClearImage`，会自动替换
- 背景色使用 ARGB 格式
