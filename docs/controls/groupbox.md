# 分组框控件 (GroupBox)

[← 返回主文档](../../README.md)

## 概述

控件分组容器,用于将相关控件组织在一起,支持标题显示和子控件管理。

## API 文档

### 创建分组框

```c++
HWND __stdcall CreateGroupBox(
    HWND hParent,
    int x, int y, int width, int height,
    const unsigned char* title_bytes, int title_len,
    UINT32 border_color,
    UINT32 bg_color
);
```

**参数说明:**

| 参数 | 说明 |
|------|------|
| `hParent` | 父窗口句柄 |
| `x, y` | 控件位置 |
| `width, height` | 控件尺寸 |
| `title_bytes` | UTF-8 编码的标题文本指针 |
| `title_len` | 标题文本长度 |
| `border_color` | 边框颜色(ARGB格式) |
| `bg_color` | 背景色(ARGB格式) |

**返回值:** 分组框控件句柄

### 添加子控件

```c++
void __stdcall AddChildToGroupBox(HWND hGroupBox, HWND hChild);
```

将控件添加到分组框中,分组框会管理子控件的启用/禁用和显示/隐藏状态。

### 设置标题

```c++
void __stdcall SetGroupBoxTitle(HWND hGroupBox, const unsigned char* title_bytes, int title_len);
```

### 启用/禁用

```c++
void __stdcall EnableGroupBox(HWND hGroupBox, BOOL enable);
```

启用或禁用分组框及其所有子控件。

### 显示/隐藏

```c++
void __stdcall ShowGroupBox(HWND hGroupBox, BOOL show);
```

显示或隐藏分组框及其所有子控件。

### 其他操作

```c++
void __stdcall SetGroupBoxBounds(HWND hGroupBox, int x, int y, int width, int height);
void __stdcall SetGroupBoxColor(HWND hGroupBox, UINT32 border_color, UINT32 bg_color);
```

## 样式说明

- 边框宽度: 1px
- 边框圆角: 4px
- 标题字体: Microsoft YaHei UI, 14px
- 标题位置: 左上角,距边框 10px
- 标题背景: 与分组框背景色相同
- 默认边框色: #DCDFE6
- 内边距: 建议子控件距边框 10-20px

## 使用场景

1. **单选按钮分组**: 将同一组单选按钮放在一起
2. **复选框分组**: 组织相关的复选框选项
3. **功能区域划分**: 将相关功能的控件组织在一起
4. **表单布局**: 将表单字段按类别分组

## 易语言示例

```
.版本 2

.程序集变量 窗口句柄, 整数型
.程序集变量 分组框1, 整数型
.程序集变量 分组框2, 整数型
.程序集变量 单选按钮1, 整数型
.程序集变量 单选按钮2, 整数型
.程序集变量 单选按钮3, 整数型
.程序集变量 复选框1, 整数型
.程序集变量 复选框2, 整数型
.程序集变量 复选框3, 整数型
.程序集变量 按钮_禁用, 整数型
.程序集变量 按钮_启用, 整数型

.子程序 _启动窗口_创建完毕

窗口句柄 = 创建Emoji窗口 ("分组框示例", 600, 450)

' 创建第一个分组框(性别选择)
分组框1 = 创建分组框_辅助 (窗口句柄, 20, 20, 260, 150, "性别选择", #COLOR_BORDER_BASE, #COLOR_BG_WHITE)

' 在分组框1中创建单选按钮
单选按钮1 = 创建单选按钮_辅助 (窗口句柄, 40, 60, 100, 30, "男", 1, 真, #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE)
单选按钮2 = 创建单选按钮_辅助 (窗口句柄, 40, 100, 100, 30, "女", 1, 假, #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE)
单选按钮3 = 创建单选按钮_辅助 (窗口句柄, 40, 140, 100, 30, "保密", 1, 假, #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE)

' 添加单选按钮到分组框1
添加子控件到分组框 (分组框1, 单选按钮1)
添加子控件到分组框 (分组框1, 单选按钮2)
添加子控件到分组框 (分组框1, 单选按钮3)

' 创建第二个分组框(兴趣爱好)
分组框2 = 创建分组框_辅助 (窗口句柄, 300, 20, 280, 150, "兴趣爱好(多选)", #COLOR_BORDER_BASE, #COLOR_BG_WHITE)

' 在分组框2中创建复选框
复选框1 = 创建复选框_辅助 (窗口句柄, 320, 60, 120, 30, "编程", 假, #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE)
复选框2 = 创建复选框_辅助 (窗口句柄, 320, 100, 120, 30, "音乐", 假, #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE)
复选框3 = 创建复选框_辅助 (窗口句柄, 320, 140, 120, 30, "运动", 假, #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE)

' 添加复选框到分组框2
添加子控件到分组框 (分组框2, 复选框1)
添加子控件到分组框 (分组框2, 复选框2)
添加子控件到分组框 (分组框2, 复选框3)

' 创建控制按钮
按钮_禁用 = 创建Emoji按钮_辅助 (窗口句柄, "🔒", "禁用分组框1", 20, 200, 150, 40, #COLOR_DANGER)
按钮_启用 = 创建Emoji按钮_辅助 (窗口句柄, "🔓", "启用分组框1", 180, 200, 150, 40, #COLOR_SUCCESS)

' 设置按钮回调
设置按钮点击回调 (&按钮点击回调)

运行消息循环 ()


.子程序 按钮点击回调, , 公开, stdcall
.参数 按钮ID, 整数型

.如果真 (按钮ID = 按钮_禁用)
    启用分组框 (分组框1, 假)
    信息框 ("已禁用分组框1及其所有子控件", 0, "提示")
.如果真结束

.如果真 (按钮ID = 按钮_启用)
    启用分组框 (分组框1, 真)
    信息框 ("已启用分组框1及其所有子控件", 0, "提示")
.如果真结束
```

## 注意事项

⚠️ **重要提示**:

1. 子控件的坐标是相对于父窗口,不是相对于分组框
2. 添加到分组框的子控件会受分组框启用/禁用状态影响
3. 分组框隐藏时,所有子控件也会隐藏
4. 标题文本必须使用 UTF-8 编码的字节集
5. 建议子控件距离分组框边框至少 10-20px

## 布局建议

```
分组框布局示例:
┌─ 标题 ──────────────┐
│                      │
│  [子控件1]           │
│  [子控件2]           │
│  [子控件3]           │
│                      │
└──────────────────────┘

推荐间距:
- 标题距顶部: 自动
- 子控件距左边框: 20px
- 子控件距顶部: 40px
- 子控件之间: 10px
- 子控件距底部: 10px
```

## 相关文档

- [单选按钮](radiobutton.md)
- [复选框](checkbox.md)
- [布局管理器](../layout.md)
