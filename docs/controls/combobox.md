# 组合框控件 (ComboBox)

[← 返回主文档](../../README.md)

## 概述

下拉列表选择器,支持可编辑/只读模式、彩色 Emoji 显示和自定义下拉高度。

## API 文档

### 创建组合框

```c++
HWND __stdcall CreateComboBox(
    HWND hParent,
    int x, int y, int width, int height,
    BOOL readonly,
    UINT32 fg_color,
    UINT32 bg_color,
    int dropdown_height,
    const unsigned char* font_name_bytes, int font_name_len,
    int font_size,
    BOOL bold,
    BOOL italic,
    BOOL underline
);
```

**参数说明:**

| 参数 | 说明 |
|------|------|
| `hParent` | 父窗口句柄 |
| `x, y` | 控件位置 |
| `width, height` | 控件尺寸 |
| `readonly` | 是否只读(TRUE=只读, FALSE=可编辑) |
| `fg_color` | 前景色/文本颜色(ARGB格式) |
| `bg_color` | 背景色(ARGB格式) |
| `dropdown_height` | 下拉列表高度(像素) |
| `font_name_bytes` | UTF-8 编码的字体名称指针 |
| `font_name_len` | 字体名称长度 |
| `font_size` | 字体大小(像素) |
| `bold` | 是否粗体 |
| `italic` | 是否斜体 |
| `underline` | 是否下划线 |

**返回值:** 组合框控件句柄

### 添加/删除项目

```c++
int __stdcall AddComboBoxItem(HWND hComboBox, const unsigned char* text_bytes, int text_len);
void __stdcall RemoveComboBoxItem(HWND hComboBox, int index);
void __stdcall ClearComboBox(HWND hComboBox);
```

### 获取/设置选中项

```c++
int __stdcall GetComboBoxSelectedIndex(HWND hComboBox);
void __stdcall SetComboBoxSelectedIndex(HWND hComboBox, int index);
```

### 获取/设置文本

```c++
int __stdcall GetComboBoxText(HWND hComboBox, unsigned char* buffer, int buffer_size);
void __stdcall SetComboBoxText(HWND hComboBox, const unsigned char* text_bytes, int text_len);
```

### 获取项目文本

```c++
int __stdcall GetComboBoxItemText(HWND hComboBox, int index, unsigned char* buffer, int buffer_size);
```

### 设置回调

```c++
typedef void (__stdcall *ComboBoxCallback)(HWND hComboBox, int index);
void __stdcall SetComboBoxCallback(HWND hComboBox, ComboBoxCallback callback);
```

**回调参数:**
- `hComboBox`: 组合框句柄
- `index`: 选中项索引(-1 表示未选中或手动输入)

### 其他操作

```c++
void __stdcall EnableComboBox(HWND hComboBox, BOOL enable);
void __stdcall ShowComboBox(HWND hComboBox, BOOL show);
void __stdcall SetComboBoxBounds(HWND hComboBox, int x, int y, int width, int height);
```

## 样式说明

- 默认高度: 35px
- 下拉按钮宽度: 30px
- 下拉按钮图标: ▼
- 项目高度: 32px
- 选中背景色: #409EFF
- 选中文本色: #FFFFFF
- 悬停背景色: #ECF5FF
- 边框颜色: #DCDFE6
- 焦点边框: #409EFF
- 支持彩色 Emoji 显示

## 模式说明

### 可编辑模式 (readonly=FALSE)
- 用户可以直接输入文本
- 可以从下拉列表选择
- 输入的文本不会自动添加到列表

### 只读模式 (readonly=TRUE)
- 用户只能从下拉列表选择
- 不能手动输入文本
- 更适合固定选项的场景

## 易语言示例

```
.版本 2

.程序集变量 窗口句柄, 整数型
.程序集变量 组合框1, 整数型
.程序集变量 组合框2, 整数型
.程序集变量 按钮_获取, 整数型
.程序集变量 标签_状态, 整数型

.子程序 _启动窗口_创建完毕

窗口句柄 = 创建Emoji窗口 ("组合框示例", 600, 400)

' 创建可编辑组合框
创建标签_辅助 (窗口句柄, 20, 20, 200, 30, "可编辑组合框:", #COLOR_PRIMARY, #COLOR_TRANSPARENT)
组合框1 = 创建组合框_辅助 (窗口句柄, 20, 50, 300, 35, 假, #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE, 150, "Microsoft YaHei UI", 14, 假, 假, 假)

' 添加项目(支持 Emoji)
添加组合框项_辅助 (组合框1, "🍎 苹果")
添加组合框项_辅助 (组合框1, "🍌 香蕉")
添加组合框项_辅助 (组合框1, "🍇 葡萄")
添加组合框项_辅助 (组合框1, "🍓 草莓")

设置组合框回调 (组合框1, &组合框1_回调)

' 创建只读组合框
创建标签_辅助 (窗口句柄, 20, 110, 200, 30, "只读组合框:", #COLOR_PRIMARY, #COLOR_TRANSPARENT)
组合框2 = 创建组合框_辅助 (窗口句柄, 20, 140, 300, 35, 真, #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE, 150, "Microsoft YaHei UI", 14, 假, 假, 假)

' 添加项目
添加组合框项_辅助 (组合框2, "选项一")
添加组合框项_辅助 (组合框2, "选项二")
添加组合框项_辅助 (组合框2, "选项三")

' 设置默认选中
设置组合框选中索引 (组合框2, 0)
设置组合框回调 (组合框2, &组合框2_回调)

' 创建操作按钮
按钮_获取 = 创建Emoji按钮_辅助 (窗口句柄, "✅", "获取选中", 20, 200, 150, 40, #COLOR_PRIMARY)
设置按钮点击回调 (&按钮点击回调)

' 创建状态标签
标签_状态 = 创建标签_辅助 (窗口句柄, 20, 260, 560, 100, "当前选中: 无", #COLOR_TEXT_PRIMARY, #COLOR_BG_LIGHT, , , , , , , 真)

运行消息循环 ()


.子程序 组合框1_回调, , 公开, stdcall
.参数 组合框句柄, 整数型
.参数 索引, 整数型
.局部变量 文本, 文本型

.如果 (索引 ≥ 0)
    文本 = 获取组合框项文本_辅助 (组合框句柄, 索引)
    设置标签文本_辅助 (标签_状态, "组合框1选中: 索引 " + 到文本 (索引) + " - " + 文本)
.否则
    文本 = 获取组合框文本_辅助 (组合框句柄)
    设置标签文本_辅助 (标签_状态, "组合框1编辑框文本: " + 文本)
.如果结束


.子程序 组合框2_回调, , 公开, stdcall
.参数 组合框句柄, 整数型
.参数 索引, 整数型
.局部变量 文本, 文本型

.如果 (索引 ≥ 0)
    文本 = 获取组合框项文本_辅助 (组合框句柄, 索引)
    设置标签文本_辅助 (标签_状态, "组合框2选中: 索引 " + 到文本 (索引) + " - " + 文本)
.如果结束


.子程序 按钮点击回调, , 公开, stdcall
.参数 按钮ID, 整数型
.局部变量 索引, 整数型
.局部变量 文本, 文本型

.如果真 (按钮ID = 按钮_获取)
    索引 = 获取组合框选中索引 (组合框1)
    .如果 (索引 ≥ 0)
        文本 = 获取组合框项文本_辅助 (组合框1, 索引)
        信息框 ("选中项索引: " + 到文本 (索引) + #换行符 + "选中项文本: " + 文本, 0, "获取选中项")
    .否则
        文本 = 获取组合框文本_辅助 (组合框1)
        信息框 ("未选中任何项" + #换行符 + "编辑框文本: " + 文本, 0, "获取选中项")
    .如果结束
.如果真结束
```

## 注意事项

⚠️ **重要提示**:

1. 所有文本必须使用 UTF-8 编码的字节集
2. 支持彩色 Emoji 显示
3. 可编辑模式下,用户输入不会自动添加到列表
4. 索引从 0 开始,-1 表示未选中
5. 下拉高度建议设置为项目高度(32px)的倍数

## 相关文档

- [列表框](listbox.md)
- [编辑框](editbox.md)
