# 布局管理器

[← 返回主文档](../README.md)

## 概述

自动管理子控件的位置和大小，支持流式布局、网格布局和停靠布局。窗口大小改变时自动重新排列控件。

## API 文档

### 设置布局管理器

```c++
void __stdcall SetLayoutManager(
    HWND hParent,
    int layout_type,    // 布局类型
    int rows,           // 网格行数（仅网格布局有效）
    int columns,        // 网格列数（仅网格布局有效）
    int spacing         // 控件间距（像素）
);
```

### 设置布局内边距

```c++
void __stdcall SetLayoutPadding(
    HWND hParent,
    int left, int top, int right, int bottom
);
```

### 设置控件布局属性

```c++
void __stdcall SetControlLayoutProps(
    HWND hControl,
    int margin_left, int margin_top, int margin_right, int margin_bottom,
    int dock_position,          // 停靠位置（仅停靠布局有效）
    BOOL stretch_horizontal,    // 水平拉伸
    BOOL stretch_vertical       // 垂直拉伸
);
```

### 添加/移除控件

```c++
void __stdcall AddControlToLayout(HWND hParent, HWND hControl);
void __stdcall RemoveControlFromLayout(HWND hParent, HWND hControl);
```

### 更新布局

```c++
void __stdcall UpdateLayout(HWND hParent);
```

### 移除布局管理器

```c++
void __stdcall RemoveLayoutManager(HWND hParent);
```

## 布局类型

### 1. 水平流式布局 (LAYOUT_FLOW_H = 1)

控件从左到右排列，超出宽度自动换行。

```
设置布局管理器 (窗口句柄, #LAYOUT_FLOW_H, 0, 0, 10)
设置布局内边距 (窗口句柄, 20, 20, 20, 20)
添加控件到布局 (窗口句柄, 按钮1)
添加控件到布局 (窗口句柄, 按钮2)
更新布局 (窗口句柄)
```

### 2. 垂直流式布局 (LAYOUT_FLOW_V = 2)

控件从上到下排列。

```
设置布局管理器 (窗口句柄, #LAYOUT_FLOW_V, 0, 0, 10)
```

### 3. 网格布局 (LAYOUT_GRID = 3)

控件按行列网格排列，自动计算单元格大小。

```
' 3行4列网格，间距8像素
设置布局管理器 (窗口句柄, #LAYOUT_GRID, 3, 4, 8)
```

### 4. 停靠布局 (LAYOUT_DOCK = 4)

控件停靠到父窗口的边缘或填充剩余空间。

```
设置布局管理器 (窗口句柄, #LAYOUT_DOCK, 0, 0, 0)

' 顶部工具栏
设置控件布局属性 (工具栏, 0, 0, 0, 0, #DOCK_TOP, 假, 假)

' 左侧面板
设置控件布局属性 (侧边栏, 0, 0, 0, 0, #DOCK_LEFT, 假, 假)

' 填充剩余空间
设置控件布局属性 (内容区, 0, 0, 0, 0, #DOCK_FILL, 假, 假)
```

## 布局常量

| 常量 | 值 | 说明 |
|------|-----|------|
| `LAYOUT_NONE` | 0 | 无布局 |
| `LAYOUT_FLOW_H` | 1 | 水平流式布局 |
| `LAYOUT_FLOW_V` | 2 | 垂直流式布局 |
| `LAYOUT_GRID` | 3 | 网格布局 |
| `LAYOUT_DOCK` | 4 | 停靠布局 |

## 停靠位置常量

| 常量 | 值 | 说明 |
|------|-----|------|
| `DOCK_NONE` | 0 | 不停靠 |
| `DOCK_TOP` | 1 | 停靠到顶部 |
| `DOCK_BOTTOM` | 2 | 停靠到底部 |
| `DOCK_LEFT` | 3 | 停靠到左侧 |
| `DOCK_RIGHT` | 4 | 停靠到右侧 |
| `DOCK_FILL` | 5 | 填充剩余空间 |

## 布局管理器特性

- ✅ 自动排列：窗口大小改变时自动重新计算控件位置
- ✅ 多种布局：流式、网格、停靠三种布局模式
- ✅ 内边距：支持设置布局区域的内边距
- ✅ 控件间距：统一的控件间距设置
- ✅ 拉伸模式：控件可设置水平/垂直拉伸
- ✅ 动态增减：运行时可添加/移除布局中的控件

## 易语言示例

```
.版本 2

.程序集变量 窗口句柄, 整数型
.程序集变量 按钮1, 整数型
.程序集变量 按钮2, 整数型
.程序集变量 按钮3, 整数型

.子程序 _启动窗口_创建完毕

窗口句柄 = 创建Emoji窗口 ("布局示例", 600, 400)

' 设置水平流式布局
设置布局管理器 (窗口句柄, #LAYOUT_FLOW_H, 0, 0, 10)
设置布局内边距 (窗口句柄, 20, 20, 20, 20)

' 创建按钮
按钮1 = 创建Emoji按钮_辅助 (窗口句柄, "🎉", "按钮1", 0, 0, 100, 40, #409EFF)
按钮2 = 创建Emoji按钮_辅助 (窗口句柄, "🚀", "按钮2", 0, 0, 100, 40, #67C23A)
按钮3 = 创建Emoji按钮_辅助 (窗口句柄, "⭐", "按钮3", 0, 0, 100, 40, #E6A23C)

' 添加到布局
添加控件到布局 (窗口句柄, 按钮1)
添加控件到布局 (窗口句柄, 按钮2)
添加控件到布局 (窗口句柄, 按钮3)

' 更新布局
更新布局 (窗口句柄)
```

## 相关文档

- [窗口回调](../README.md#设置窗口大小改变回调)
- [控件列表](../README.md#完整控件列表)
