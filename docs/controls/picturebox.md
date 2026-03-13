# 图片框控件 (PictureBox)

[← 返回主文档](../../README.md) | [← 返回文档中心](../README.md)

## 概述

图片框控件用于显示图片，支持多种图片格式（PNG、JPG、BMP、GIF）和缩放模式。

## 创建图片框

```c++
HWND __stdcall CreatePictureBox(
    HWND hParent,
    int x, int y, int width, int height,
    int scale_mode,
    UINT32 bg_color
);
```

### 参数说明

| 参数 | 说明 |
|------|------|
| `hParent` | 父窗口句柄 |
| `x, y` | 控件位置 |
| `width, height` | 控件尺寸 |
| `scale_mode` | 缩放模式（见下表） |
| `bg_color` | 背景色（ARGB格式） |

### 缩放模式

| 常量 | 值 | 说明 |
|------|-----|------|
| `SCALE_NONE` | 0 | 不缩放，左上角对齐显示原始尺寸 |
| `SCALE_STRETCH` | 1 | 拉伸填充整个控件区域（可能变形） |
| `SCALE_FIT` | 2 | 等比缩放适应控件（保持宽高比，居中显示）⭐ 推荐 |
| `SCALE_CENTER` | 3 | 居中显示原始尺寸（不缩放） |

## 加载图片

### 从文件加载

```c++
BOOL __stdcall LoadImageFromFile(
    HWND hPictureBox,
    const unsigned char* file_path_bytes,
    int path_len
);
```

**支持的格式：** PNG、JPEG、BMP、GIF（仅第一帧）

### 从内存加载

```c++
BOOL __stdcall LoadImageFromMemory(
    HWND hPictureBox,
    const unsigned char* image_data,
    int data_len
);
```

⚠️ **重要注意事项：**

在易语言中使用 `从内存加载图片` 时，**必须使用程序集变量（全局变量）保存图片数据**，不能使用局部变量！

**原因：** DLL 内部使用 WIC 异步解码图片。如果使用局部变量，当子程序返回后，易语言会释放或移动局部变量的内存，导致 DLL 中保存的数据指针失效，图片显示为黑色。

**✅ 正确示例：**

```
.程序集变量 全局_图片数据, 字节集  ' ✅ 使用程序集变量

.子程序 加载图片按钮_被单击
.局部变量 数据指针, 整数型

全局_图片数据 ＝ HTTP读文件 ("https://example.com/image.png")
数据指针 ＝ 取变量数据地址 (全局_图片数据)
从内存加载图片 (图片框句柄, 数据指针, 取字节集长度 (全局_图片数据))
```

详见 [FAQ - 图片加载问题](../faq.md#图片加载问题)

## 其他操作

### 清除图片

```c++
void __stdcall ClearImage(HWND hPictureBox);
```

### 设置透明度

```c++
void __stdcall SetImageOpacity(HWND hPictureBox, float opacity);
```

透明度范围：0.0（完全透明）~ 1.0（完全不透明）

### 设置回调

```c++
typedef void (__stdcall *PictureBoxCallback)(HWND hPictureBox);
void __stdcall SetPictureBoxCallback(HWND hPictureBox, PictureBoxCallback callback);
```

### 控制显示

```c++
void __stdcall EnablePictureBox(HWND hPictureBox, BOOL enable);
void __stdcall ShowPictureBox(HWND hPictureBox, BOOL show);
void __stdcall SetPictureBoxBounds(HWND hPictureBox, int x, int y, int width, int height);
void __stdcall SetPictureBoxScaleMode(HWND hPictureBox, int scale_mode);
void __stdcall SetPictureBoxBackgroundColor(HWND hPictureBox, UINT32 bg_color);
```

## 技术说明

- **图片加载**：WIC (Windows Imaging Component)
- **图片渲染**：Direct2D
- **透明通道**：完全支持 Alpha 通道混合
- **硬件加速**：使用 GPU 加速渲染
- **插值模式**：线性插值（D2D1_BITMAP_INTERPOLATION_MODE_LINEAR）

## 易语言完整示例

```
.版本 2

.程序集变量 窗口句柄, 整数型
.程序集变量 图片框1, 整数型
.程序集变量 图片框2, 整数型
.程序集变量 全局_图片数据, 字节集  ' 用于内存加载

.子程序 _启动窗口_创建完毕

窗口句柄 = 创建Emoji窗口 ("图片框示例", 800, 600)

' 创建拉伸模式图片框
图片框1 = 创建图片框 (窗口句柄, 50, 80, 300, 200, 1, #FFF5F7FA)

' 创建等比缩放模式图片框
图片框2 = 创建图片框 (窗口句柄, 400, 80, 300, 200, 2, #FFF5F7FA)

' 从文件加载图片
.局部变量 路径UTF8, 字节集
.局部变量 路径指针, 整数型

路径UTF8 = 到UTF8 ("images\\photo.png")
路径指针 = 取字节集数据地址 (路径UTF8)

从文件加载图片 (图片框1, 路径指针, 取字节集长度 (路径UTF8))
从文件加载图片 (图片框2, 路径指针, 取字节集长度 (路径UTF8))

' 设置透明度
设置图片透明度 (图片框1, 0.8)

' 设置回调
设置图片框回调 (图片框1, &图片框回调)


.子程序 图片框回调, , 公开, stdcall
.参数 图片框句柄, 整数型

信息框 ("图片框被点击", 0, "提示")
```

## 性能建议

- 大图片建议使用 `SCALE_FIT` 模式，减少内存占用
- 从内存加载图片时必须使用程序集变量
- 不再使用的图片及时调用 `ClearImage()` 释放资源

详见 [性能优化文档](../performance.md#图片加载优化)

## 相关文档

- [常见问题 - 图片加载问题](../faq.md#图片加载问题)
- [性能优化 - 图片加载优化](../performance.md#图片加载优化)
