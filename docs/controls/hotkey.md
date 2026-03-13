# 热键控件 (HotKey)

[← 返回主文档](../../README.md)

## 概述

键盘快捷键捕获控件,支持 Ctrl、Shift、Alt 修饰键组合,用于设置和显示快捷键。

## API 文档

### 创建热键控件

```c++
HWND __stdcall CreateHotKeyControl(
    HWND hParent,
    int x, int y, int width, int height,
    UINT32 fg_color,
    UINT32 bg_color
);
```

**参数说明:**

| 参数 | 说明 |
|------|------|
| `hParent` | 父窗口句柄 |
| `x, y` | 控件位置 |
| `width, height` | 控件尺寸 |
| `fg_color` | 前景色/文本颜色(ARGB格式) |
| `bg_color` | 背景色(ARGB格式) |

**返回值:** 热键控件句柄

### 获取/设置热键值

```c++
void __stdcall GetHotKeyValue(HWND hHotKey, int* vk_code, int* modifiers);
void __stdcall SetHotKeyValue(HWND hHotKey, int vk_code, int modifiers);
```

**修饰键值:**
- `modifiers` 是修饰键的组合值:
  - 1 = Ctrl
  - 2 = Shift
  - 4 = Alt
  - 可以相加组合,如 3 = Ctrl+Shift

**虚拟键码示例:**
- 字母键: VK_A(65) ~ VK_Z(90)
- 数字键: VK_0(48) ~ VK_9(57)
- 功能键: VK_F1(112) ~ VK_F12(123)
- 特殊键: VK_SPACE(32), VK_RETURN(13), VK_ESCAPE(27)

### 清除热键

```c++
void __stdcall ClearHotKey(HWND hHotKey);
```

### 设置回调

```c++
typedef void (__stdcall *HotKeyCallback)(HWND hHotKey, int vk_code, int modifiers);
void __stdcall SetHotKeyCallback(HWND hHotKey, HotKeyCallback callback);
```

**回调参数:**
- `hHotKey`: 热键控件句柄
- `vk_code`: 虚拟键码
- `modifiers`: 修饰键组合值

### 其他操作

```c++
void __stdcall EnableHotKeyControl(HWND hHotKey, BOOL enable);
void __stdcall ShowHotKeyControl(HWND hHotKey, BOOL show);
void __stdcall SetHotKeyBounds(HWND hHotKey, int x, int y, int width, int height);
```

## 样式说明

- 默认高度: 35px
- 边框颜色: #DCDFE6
- 焦点边框: #409EFF
- 文本格式: "Ctrl+Shift+A"
- 占位符文本: "请按下快捷键"
- 字体: Microsoft YaHei UI, 14px

## 支持的按键

### 修饰键
- Ctrl
- Shift
- Alt

### 字母键
- A ~ Z

### 数字键
- 0 ~ 9

### 功能键
- F1 ~ F12

### 特殊键
- Space, Enter, Esc, Tab
- Backspace, Delete
- Insert, Home, End
- PageUp, PageDown
- 方向键: Left, Right, Up, Down

## 易语言示例

```
.版本 2

.程序集变量 窗口句柄, 整数型
.程序集变量 热键控件1, 整数型
.程序集变量 热键控件2, 整数型
.程序集变量 标签_热键1, 整数型
.程序集变量 标签_热键2, 整数型
.程序集变量 按钮_获取, 整数型
.程序集变量 按钮_设置, 整数型
.程序集变量 按钮_清除, 整数型

.子程序 _启动窗口_创建完毕

窗口句柄 = 创建Emoji窗口 ("热键控件示例", 600, 450)

' 创建热键控件1
创建标签_辅助 (窗口句柄, 20, 20, 200, 30, "快捷键1:", #COLOR_TEXT_PRIMARY, #COLOR_TRANSPARENT)
热键控件1 = 创建热键控件_辅助 (窗口句柄, 20, 50, 300, 35, #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE)
设置热键回调 (热键控件1, &热键1_改变回调)
标签_热键1 = 创建标签_辅助 (窗口句柄, 330, 50, 250, 35, "当前热键: 无", #COLOR_TEXT_SECONDARY, #COLOR_BG_BASE)

' 创建热键控件2
创建标签_辅助 (窗口句柄, 20, 110, 200, 30, "快捷键2:", #COLOR_TEXT_PRIMARY, #COLOR_TRANSPARENT)
热键控件2 = 创建热键控件_辅助 (窗口句柄, 20, 140, 300, 35, #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE)
设置热键回调 (热键控件2, &热键2_改变回调)
标签_热键2 = 创建标签_辅助 (窗口句柄, 330, 140, 250, 35, "当前热键: 无", #COLOR_TEXT_SECONDARY, #COLOR_BG_BASE)

' 创建说明标签
创建标签_辅助 (窗口句柄, 20, 200, 560, 80, "使用说明:" + #换行符 + "1. 点击热键控件,然后按下键盘上的任意键组合" + #换行符 + "2. 支持 Ctrl、Shift、Alt 修饰键" + #换行符 + "3. 支持字母键、数字键、功能键等", #COLOR_TEXT_SECONDARY, #COLOR_BG_LIGHT, , , , , , , 真)

' 创建操作按钮
按钮_获取 = 创建Emoji按钮_辅助 (窗口句柄, "📋", "获取热键1", 20, 300, 150, 40, #COLOR_PRIMARY)
按钮_设置 = 创建Emoji按钮_辅助 (窗口句柄, "✏️", "设置Ctrl+S", 180, 300, 150, 40, #COLOR_SUCCESS)
按钮_清除 = 创建Emoji按钮_辅助 (窗口句柄, "🗑️", "清除热键1", 340, 300, 150, 40, #COLOR_WARNING)

设置按钮点击回调 (&按钮点击回调)

运行消息循环 ()


.子程序 热键1_改变回调, , 公开, stdcall
.参数 热键句柄, 整数型
.参数 虚拟键码, 整数型
.参数 修饰键, 整数型
.局部变量 热键文本, 文本型

热键文本 = 获取热键文本 (虚拟键码, 修饰键)
设置标签文本_辅助 (标签_热键1, "当前热键: " + 热键文本)


.子程序 热键2_改变回调, , 公开, stdcall
.参数 热键句柄, 整数型
.参数 虚拟键码, 整数型
.参数 修饰键, 整数型
.局部变量 热键文本, 文本型

热键文本 = 获取热键文本 (虚拟键码, 修饰键)
设置标签文本_辅助 (标签_热键2, "当前热键: " + 热键文本)


.子程序 获取热键文本, 文本型
.参数 虚拟键码, 整数型
.参数 修饰键, 整数型
.局部变量 文本, 文本型
.局部变量 Ctrl, 逻辑型
.局部变量 Shift, 逻辑型
.局部变量 Alt, 逻辑型
.局部变量 剩余, 整数型

.如果真 (虚拟键码 = 0)
    返回 ("无")
.如果真结束

' 解析修饰键
Ctrl = 假
Shift = 假
Alt = 假
剩余 = 修饰键

.如果真 (剩余 ≥ 4)
    Alt = 真
    剩余 = 剩余 - 4
.如果真结束
.如果真 (剩余 ≥ 2)
    Shift = 真
    剩余 = 剩余 - 2
.如果真结束
.如果真 (剩余 ≥ 1)
    Ctrl = 真
.如果真结束

' 构建文本
文本 = ""
.如果真 (Ctrl)
    文本 = 文本 + "Ctrl+"
.如果真结束
.如果真 (Shift)
    文本 = 文本 + "Shift+"
.如果真结束
.如果真 (Alt)
    文本 = 文本 + "Alt+"
.如果真结束

' 添加键名
文本 = 文本 + 获取键名称 (虚拟键码)

返回 (文本)


.子程序 获取键名称, 文本型
.参数 虚拟键码, 整数型

' 字母键
.如果真 (虚拟键码 ≥ VK_A 且 虚拟键码 ≤ VK_Z)
    返回 (字符 (虚拟键码))
.如果真结束

' 数字键
.如果真 (虚拟键码 ≥ VK_0 且 虚拟键码 ≤ VK_9)
    返回 (字符 (虚拟键码))
.如果真结束

' 功能键
.如果真 (虚拟键码 ≥ VK_F1 且 虚拟键码 ≤ VK_F12)
    返回 ("F" + 到文本 (虚拟键码 - VK_F1 + 1))
.如果真结束

' 特殊键
.判断开始 (虚拟键码 = VK_SPACE)
    返回 ("Space")
.判断 (虚拟键码 = VK_RETURN)
    返回 ("Enter")
.判断 (虚拟键码 = VK_ESCAPE)
    返回 ("Esc")
.判断 (虚拟键码 = VK_TAB)
    返回 ("Tab")
.默认
    返回 ("Key" + 到文本 (虚拟键码))
.判断结束


.子程序 按钮点击回调, , 公开, stdcall
.参数 按钮ID, 整数型
.局部变量 虚拟键码, 整数型
.局部变量 修饰键, 整数型
.局部变量 热键文本, 文本型

.判断开始 (按钮ID = 按钮_获取)
    获取热键值 (热键控件1, 虚拟键码, 修饰键)
    热键文本 = 获取热键文本 (虚拟键码, 修饰键)
    信息框 ("热键1当前值:" + #换行符 + 热键文本, 0, "获取热键")
    
.判断 (按钮ID = 按钮_设置)
    ' 设置为 Ctrl+S (VK_S=83, Ctrl=1)
    设置热键值 (热键控件1, VK_S, 1)
    信息框 ("已设置热键1为 Ctrl+S", 0, "设置热键")
    
.判断 (按钮ID = 按钮_清除)
    清除热键 (热键控件1)
    设置标签文本_辅助 (标签_热键1, "当前热键: 无")
    信息框 ("已清除热键1", 0, "清除热键")
.判断结束
```

## 常用快捷键示例

```
Ctrl+S      - 保存
Ctrl+C      - 复制
Ctrl+V      - 粘贴
Ctrl+Z      - 撤销
Ctrl+Shift+P - 命令面板
Alt+F4      - 关闭窗口
F5          - 刷新
F12         - 开发者工具
```

## 注意事项

⚠️ **重要提示**:

1. 修饰键值可以相加组合(Ctrl=1, Shift=2, Alt=4)
2. 虚拟键码参考 Windows VK 常量
3. 不支持单独的修饰键(必须配合其他键)
4. 某些系统快捷键可能无法捕获
5. 建议避免使用系统保留的快捷键

## 相关文档

- [编辑框](editbox.md)
- [按钮控件](button.md)
