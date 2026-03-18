# Emoji Window DLL — 项目概述

## 简介

Emoji Window DLL 是一个使用 C++ 和 Direct2D/DirectWrite 实现的 Windows UI 控件库。完美支持彩色 Emoji 显示，提供 16 种控件、布局管理器、主题系统和扩展事件系统。

支持 3 种调用语言：
- **易语言 (EPL)**：主要目标语言，通过 DLL 命令声明调用
- **Python**：通过 `ctypes.WinDLL` 加载调用
- **C#**：通过 `DllImport` 声明调用

## ARGB 颜色格式

所有颜色参数使用 32 位 ARGB 格式：

```
颜色值 = (A << 24) | (R << 16) | (G << 8) | B
```

- A = Alpha 透明度（0-255，255=不透明）
- R = 红色（0-255）
- G = 绿色（0-255）
- B = 蓝色（0-255）

易语言辅助函数：
```
.子程序 到ARGB, 整数型
.参数 A, 整数型
.参数 R, 整数型
.参数 G, 整数型
.参数 B, 整数型

返回 (左移 (A, 24) ＋ 左移 (R, 16) ＋ 左移 (G, 8) ＋ B)
```

> 注意：易语言用 `左移` 而非 `位左移`（后者不存在）。

## 两次调用模式

获取文本类 API（如 `GetButtonText`、`GetLabelText`、`GetWindowTitle`）统一使用两次调用模式：

1. **第一次调用**：传入 `buffer=0, buffer_size=0`，返回所需字节数
2. **第二次调用**：分配缓冲区，传入实际 buffer 和 size，获取内容

```
' 易语言示例
' 第一次：获取长度
文本长度 ＝ 获取按钮文本 (按钮ID, 0, 0)

' 第二次：获取内容
文本缓冲区 ＝ 取空白字节集 (文本长度)
获取按钮文本 (按钮ID, 取变量数据地址 (文本缓冲区), 文本长度)
```

获取字体信息的 API（如 `GetLabelFont`）也使用类似模式，第一次传 `buffer=0` 获取字体名长度，同时通过传址参数返回字体大小、粗体、斜体等信息。

## 消息循环

每个使用 Emoji Window DLL 的程序必须运行消息循环：

```c++
// C++ 导出函数
void __stdcall set_message_loop_main_window(HWND hWnd);
void __stdcall run_message_loop();
```

易语言调用：
```
设置消息循环主窗口 (窗口句柄)
运行消息循环 ()
```

Python 调用：
```python
dll.set_message_loop_main_window(hwnd)
dll.run_message_loop()
```

> `run_message_loop()` 会阻塞当前线程直到主窗口关闭。

## Element UI 标准配色

DLL 内置 Element UI 风格配色，以下为常用颜色常量（ARGB 格式）：

| 名称 | 十六进制 | ARGB 值 | 用途 |
|------|---------|---------|------|
| Primary | #409EFF | `到ARGB(255, 64, 158, 255)` | 主色/默认按钮 |
| Success | #67C23A | `到ARGB(255, 103, 194, 58)` | 成功状态 |
| Warning | #E6A23C | `到ARGB(255, 230, 162, 60)` | 警告状态 |
| Danger | #F56C6C | `到ARGB(255, 245, 108, 108)` | 危险/错误 |
| Info | #909399 | `到ARGB(255, 144, 147, 153)` | 信息/次要 |
| Text Primary | #303133 | `到ARGB(255, 48, 49, 51)` | 主要文本 |
| Text Regular | #606266 | `到ARGB(255, 96, 98, 102)` | 常规文本 |
| Text Secondary | #909399 | `到ARGB(255, 144, 147, 153)` | 次要文本 |
| Border Base | #DCDFE6 | `到ARGB(255, 220, 223, 230)` | 边框 |
| Background | #FFFFFF | `到ARGB(255, 255, 255, 255)` | 背景 |

## 主题系统

支持亮色/暗色主题切换，可从 JSON 文件加载自定义主题。切换主题时所有控件自动刷新。

核心 API：
- `SetDarkMode(BOOL)` — 切换暗色/亮色模式
- `LoadThemeFromFile(path_bytes, path_len)` — 从 JSON 文件加载主题
- `LoadThemeFromJSON(json_bytes, json_len)` — 从 JSON 字符串加载主题
- `SetThemeChangedCallback(callback)` — 设置主题切换回调
- `IsDarkMode()` — 查询当前是否暗色模式

主题 JSON 支持的字段：name、dark_mode、primary、success、warning、danger、info、text_primary、text_regular、text_secondary、text_placeholder、border_base、border_light、border_lighter、background、background_light、border_radius、title_size、body_size。

## 布局管理器

自动管理子控件的位置和大小，支持 4 种布局模式：

| 类型 | 常量值 | 说明 |
|------|--------|------|
| 水平流式 | LAYOUT_FLOW_H = 1 | 从左到右排列，超宽自动换行 |
| 垂直流式 | LAYOUT_FLOW_V = 2 | 从上到下排列 |
| 网格 | LAYOUT_GRID = 3 | 按行列网格排列 |
| 停靠 | LAYOUT_DOCK = 4 | 停靠到父窗口边缘或填充 |

核心 API：
- `SetLayoutManager(hParent, type, rows, cols, spacing)`
- `SetLayoutPadding(hParent, left, top, right, bottom)`
- `AddControlToLayout(hParent, hControl)`
- `UpdateLayout(hParent)`

停靠位置常量：DOCK_TOP=1, DOCK_BOTTOM=2, DOCK_LEFT=3, DOCK_RIGHT=4, DOCK_FILL=5。

## 扩展事件系统

统一的事件回调机制，支持鼠标、键盘、焦点事件：

- `设置鼠标进入回调(控件句柄, 回调地址)`
- `设置鼠标离开回调(控件句柄, 回调地址)`
- `设置鼠标移动回调(控件句柄, 回调地址)`
- `设置按键按下回调(控件句柄, 回调地址)`
- `设置按键释放回调(控件句柄, 回调地址)`
- `设置获得焦点回调(控件句柄, 回调地址)`
- `设置失去焦点回调(控件句柄, 回调地址)`

## 16 种控件一览

| 序号 | 控件 | 创建函数 | 关键特性 |
|------|------|----------|----------|
| 1 | 窗口 | `create_window` | D2D 渲染，自定义标题栏颜色 |
| 2 | 按钮 | `create_emoji_button_bytes` | Emoji 支持，自定义颜色 |
| 3 | 标签 | `CreateLabel` | 自动换行，对齐方式 |
| 4 | 编辑框 | `CreateEditBox` | 垂直居中，按键回调 |
| 5 | 复选框 | `CreateCheckBox` | Element UI 风格 |
| 6 | 单选按钮 | `CreateRadioButton` | 分组互斥 |
| 7 | 进度条 | `CreateProgressBar` | 动画，不确定模式 |
| 8 | 列表框 | `CreateListBox` | 多选，自定义渲染 |
| 9 | 组合框 | `CreateComboBox` | 下拉列表，Emoji 支持 |
| 10 | 图片框 | `CreatePictureBox` | 文件/内存加载，缩放模式 |
| 11 | 分组框 | `CreateGroupBox` | 子控件容器 |
| 12 | 热键控件 | `CreateHotKeyControl` | 键盘快捷键捕获 |
| 13 | 树形框 | `CreateTreeView` | 层次结构，Emoji 图标，拖放 |
| 14 | 表格 | `CreateDataGridView` | 虚拟模式，多列类型 |
| 15 | 选项卡 | `CreateTabControl` | 多标签页容器 |
| 16 | 信息框 | `ShowMessageBox` | 自定义按钮，确认框 |