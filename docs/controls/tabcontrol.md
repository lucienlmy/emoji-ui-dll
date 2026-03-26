# 选项卡控件 (TabControl)

[← 返回主文档](../../README.md)

## 概述

多标签页容器控件,支持动态添加/删除标签页、自动创建内容窗口和标签页切换回调。v3.0 新增外观定制、单页控制、内容区域、交互增强、布局位置、批量操作和状态查询共 25 个函数。

## API 文档

### 创建选项卡控件

```c++
HWND __stdcall CreateTabControl(
    HWND hParent,
    int x, int y, int width, int height
);
```

**参数说明:**

| 参数 | 说明 |
|------|------|
| `hParent` | 父窗口句柄 |
| `x, y` | 控件位置 |
| `width, height` | 控件尺寸 |

**返回值:** 选项卡控件句柄

### 添加/删除标签页

```c++
int __stdcall AddTabPage(HWND hTabControl, const unsigned char* title_bytes, int title_len, int icon_index);
void __stdcall RemoveTabPage(HWND hTabControl, int index);
```

**参数说明:**
- `title_bytes`: UTF-8 编码的标签页标题(支持 Emoji)
- `title_len`: 标题长度
- `icon_index`: 图标索引(暂未实现,传 0)
- `index`: 标签页索引(从 0 开始)

### 获取/设置当前标签页

```c++
int __stdcall GetCurrentTabIndex(HWND hTabControl);
void __stdcall SetCurrentTabIndex(HWND hTabControl, int index);
```

### 获取标签页内容窗口

```c++
HWND __stdcall GetTabContentWindow(HWND hTabControl, int index);
```

每个标签页都有一个独立的内容窗口,可以在其中创建子控件。

### 设置标签页标题

```c++
void __stdcall SetTabPageTitle(HWND hTabControl, int index, const unsigned char* title_bytes, int title_len);
```

### 设置切换回调

```c++
typedef void (__stdcall *TabSwitchCallback)(HWND hTabControl, int current_index);
void __stdcall SetTabSwitchCallback(HWND hTabControl, TabSwitchCallback callback);
```

**回调参数:**
- `hTabControl`: 选项卡控件句柄
- `current_index`: 当前选中的标签页索引

### 销毁选项卡

```c++
void __stdcall DestroyTabControl(HWND hTabControl);
```

### 其他操作

```c++
void __stdcall EnableTabControl(HWND hTabControl, BOOL enable);
void __stdcall ShowTabControl(HWND hTabControl, BOOL show);
```

---

## 属性获取/设置 API（v2.1 新增）

### 获取 Tab 页标题

```c++
int __stdcall GetTabTitle(
    HWND hTabControl,
    int index,
    unsigned char* buffer,
    int bufferSize
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTabControl` | TabControl 窗口句柄 |
| `index` | Tab 页索引（从 0 开始） |
| `buffer` | 接收标题的缓冲区指针（传 NULL 获取所需大小） |
| `bufferSize` | 缓冲区大小（字节） |

**返回值：** 成功返回 UTF-8 字节数，失败返回 -1

**两次调用模式：**
- 第一次：`buffer=NULL, bufferSize=0`，返回所需字节数
- 第二次：传入足够大的缓冲区，返回实际写入字节数

**易语言示例：**
```
.局部变量 标题长度, 整数型
.局部变量 标题缓冲区, 字节集
.局部变量 结果字节集, 字节集

' 第一次调用获取所需长度
标题长度 ＝ 获取Tab页标题 (TabControl句柄, 0, 0, 0)
.如果 (标题长度 ＞ 0)
    ' 第二次调用获取实际内容
    标题缓冲区 ＝ 取空白字节集 (标题长度)
    获取Tab页标题 (TabControl句柄, 0, 取变量数据地址 (标题缓冲区), 标题长度)
    ' 标题缓冲区 即为 UTF-8 字节集，可直接拼接显示
    结果字节集 ＝ 编码_Ansi到Utf8 ("Tab[0]标题：") ＋ 标题缓冲区
.如果结束
```

---

### 设置 Tab 页标题

```c++
int __stdcall SetTabTitle(
    HWND hTabControl,
    int index,
    const unsigned char* title_bytes,
    int title_len
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTabControl` | TabControl 窗口句柄 |
| `index` | Tab 页索引（从 0 开始） |
| `title_bytes` | UTF-8 编码的新标题字节集指针 |
| `title_len` | 标题字节集长度 |

**返回值：** 成功返回 0，失败返回 -1

**易语言示例：**
```
.局部变量 新标题字节集, 字节集

' 设置 Tab[0] 的标题（支持 Emoji）
' "✅ 已完成"  ✅ = { 226, 156, 133 }
新标题字节集 ＝ { 226, 156, 133, 32 } ＋ 编码_Ansi到Utf8 ("已完成")
设置Tab页标题 (TabControl句柄, 0, 取变量数据地址 (新标题字节集), 取字节集长度 (新标题字节集))
```

---

### 获取 TabControl 位置和大小

```c++
int __stdcall GetTabControlBounds(
    HWND hTabControl,
    int* x,
    int* y,
    int* width,
    int* height
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTabControl` | TabControl 窗口句柄 |
| `x` | 输出：X 坐标（相对父窗口客户区） |
| `y` | 输出：Y 坐标（相对父窗口客户区） |
| `width` | 输出：宽度 |
| `height` | 输出：高度 |

**返回值：** 成功返回 0，失败返回 -1

**易语言示例：**
```
.局部变量 X, 整数型
.局部变量 Y, 整数型
.局部变量 宽度, 整数型
.局部变量 高度, 整数型

.如果真 (获取TabControl位置 (TabControl句柄, X, Y, 宽度, 高度) ＝ 0)
    ' 使用 X, Y, 宽度, 高度
.如果真结束
```

---

### 设置 TabControl 位置和大小

```c++
int __stdcall SetTabControlBounds(
    HWND hTabControl,
    int x,
    int y,
    int width,
    int height
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTabControl` | TabControl 窗口句柄 |
| `x` | 新 X 坐标（相对父窗口客户区） |
| `y` | 新 Y 坐标（相对父窗口客户区） |
| `width` | 新宽度 |
| `height` | 新高度 |

**返回值：** 成功返回 0，失败返回 -1

**易语言示例：**
```
' 将 TabControl 移动到新位置并调整大小
设置TabControl位置 (TabControl句柄, 20, 100, 760, 400)
```

---

### 获取 TabControl 可视状态

```c++
int __stdcall GetTabControlVisible(HWND hTabControl);
```

**返回值：** 1（可见），0（不可见），-1（无效句柄）

**易语言示例：**
```
.局部变量 可视状态, 整数型

可视状态 ＝ 获取TabControl可视状态 (TabControl句柄)
.判断开始 (可视状态 ＝ 1)
    ' TabControl 可见
.判断 (可视状态 ＝ 0)
    ' TabControl 不可见
.默认
    ' 获取失败（无效句柄）
.判断结束
```

---

### 显示或隐藏 TabControl

```c++
int __stdcall ShowTabControl(HWND hTabControl, int visible);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTabControl` | TabControl 窗口句柄 |
| `visible` | 1=显示，0=隐藏 |

**返回值：** 成功返回 0，失败返回 -1

**行为说明：**
- 隐藏 TabControl 时，当前激活的内容窗口也会同步隐藏
- 显示 TabControl 时，当前激活的内容窗口也会同步显示

**易语言示例：**
```
' 隐藏 TabControl
显示隐藏TabControl (TabControl句柄, 0)

' 显示 TabControl
显示隐藏TabControl (TabControl句柄, 1)
```

---

### 启用或禁用 TabControl

```c++
int __stdcall EnableTabControl(HWND hTabControl, int enabled);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTabControl` | TabControl 窗口句柄 |
| `enabled` | 1=启用，0=禁用 |

**返回值：** 成功返回 0，失败返回 -1

**行为说明：**
- 禁用 TabControl 后，所有 Tab 页不可切换
- 禁用状态下 TabControl 仍然可见，但不响应鼠标点击

**易语言示例：**
```
' 禁用 TabControl（Tab 页不可切换）
启用禁用TabControl (TabControl句柄, 0)

' 重新启用 TabControl
启用禁用TabControl (TabControl句柄, 1)
```

---

## 回调函数类型定义（v3.0 新增）

### TAB_CLOSE_CALLBACK - 标签页关闭回调

```c++
typedef void (__stdcall *TAB_CLOSE_CALLBACK)(HWND hTabControl, int index);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTabControl` | TabControl 窗口句柄 |
| `index` | 被关闭的标签页索引 |

**说明：** 当用户点击标签页上的 × 关闭按钮时触发。需先通过 `SetTabClosable` 启用关闭按钮，再通过 `SetTabCloseCallback` 注册回调。

---

### TAB_RIGHTCLICK_CALLBACK - 标签页右键点击回调

```c++
typedef void (__stdcall *TAB_RIGHTCLICK_CALLBACK)(HWND hTabControl, int index, int x, int y);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTabControl` | TabControl 窗口句柄 |
| `index` | 被右键点击的标签页索引 |
| `x` | 鼠标屏幕坐标 X |
| `y` | 鼠标屏幕坐标 Y |

**说明：** 当用户在标签页上右键点击时触发，可用于弹出自定义右键菜单。右键点击位置不在任何标签页上时不触发。

---

### TAB_DBLCLICK_CALLBACK - 标签页双击回调

```c++
typedef void (__stdcall *TAB_DBLCLICK_CALLBACK)(HWND hTabControl, int index);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTabControl` | TabControl 窗口句柄 |
| `index` | 被双击的标签页索引 |

**说明：** 当用户双击标签页时触发，可用于实现双击重命名等交互功能。

---

## 外观定制 API（v3.0 新增）

### SetTabItemSize - 设置标签页尺寸

```c++
int __stdcall SetTabItemSize(
    HWND hTab,
    int width,
    int height
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `width` | 标签页宽度（必须 > 0） |
| `height` | 标签页高度（必须 > 0） |

**返回值：** 成功返回 0，无效参数或无效句柄返回 -1

**易语言 DLL 命令声明：**
```
.DLL命令 设置标签页尺寸, 整数型, "emoji_window.dll", "SetTabItemSize", , , 设置标签页固定宽度和高度（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 宽度, 整数型, , 标签页宽度（必须大于0）
    .参数 高度, 整数型, , 标签页高度（必须大于0）
```

**易语言示例：**
```
' 设置标签页尺寸为 150×40
设置标签页尺寸 (TabControl句柄, 150, 40)
```

---

### SetTabFont - 设置标签字体

```c++
int __stdcall SetTabFont(
    HWND hTab,
    const unsigned char* fontName,
    int fontNameLen,
    float fontSize
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `fontName` | UTF-8 编码的字体名称字节集指针 |
| `fontNameLen` | 字体名称字节集长度（必须 > 0） |
| `fontSize` | 字号大小（必须 > 0） |

**返回值：** 成功返回 0，无效参数或无效句柄返回 -1

**易语言 DLL 命令声明：**
```
.DLL命令 设置标签字体, 整数型, "emoji_window.dll", "SetTabFont", , , 设置标签页字体名称和字号（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 字体名字节集指针, 整数型, , UTF-8编码的字体名称字节集指针
    .参数 字体名长度, 整数型, , 字体名称字节集长度
    .参数 字号, 小数型, , 字号大小（如 14.0）
```

**易语言示例：**
```
.局部变量 字体名字节集, 字节集

' 设置字体为微软雅黑 14号
字体名字节集 ＝ 编码_Ansi到Utf8 ("微软雅黑")
设置标签字体 (TabControl句柄, 取变量数据地址 (字体名字节集), 取字节集长度 (字体名字节集), 14.0)
```

---

### SetTabColors - 设置标签颜色

```c++
int __stdcall SetTabColors(
    HWND hTab,
    UINT32 selectedBg,
    UINT32 unselectedBg,
    UINT32 selectedText,
    UINT32 unselectedText
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `selectedBg` | 选中标签页背景色（ARGB 格式） |
| `unselectedBg` | 未选中标签页背景色（ARGB 格式） |
| `selectedText` | 选中标签页文字色（ARGB 格式） |
| `unselectedText` | 未选中标签页文字色（ARGB 格式） |

**返回值：** 成功返回 0，无效句柄返回 -1

**易语言 DLL 命令声明：**
```
.DLL命令 设置标签颜色, 整数型, "emoji_window.dll", "SetTabColors", , , 设置选中/未选中标签页的背景色和文字色（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 选中背景色, 整数型, , ARGB格式颜色值
    .参数 未选中背景色, 整数型, , ARGB格式颜色值
    .参数 选中文字色, 整数型, , ARGB格式颜色值
    .参数 未选中文字色, 整数型, , ARGB格式颜色值
```

**易语言示例：**
```
' 自定义主题配色：深蓝选中背景、浅灰未选中背景、白色选中文字、深灰未选中文字
设置标签颜色 (TabControl句柄, 到ARGB (255, 64, 158, 255), 到ARGB (255, 245, 247, 250), 到ARGB (255, 255, 255, 255), 到ARGB (255, 96, 98, 102))
```

---

### SetTabIndicatorColor - 设置指示条颜色

```c++
int __stdcall SetTabIndicatorColor(
    HWND hTab,
    UINT32 color
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `color` | 指示条颜色（ARGB 格式） |

**返回值：** 成功返回 0，无效句柄返回 -1

**易语言 DLL 命令声明：**
```
.DLL命令 设置指示条颜色, 整数型, "emoji_window.dll", "SetTabIndicatorColor", , , 设置选中标签页底部指示条颜色（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 颜色, 整数型, , ARGB格式颜色值
```

**易语言示例：**
```
' 设置指示条为绿色
设置指示条颜色 (TabControl句柄, 到ARGB (255, 103, 194, 58))
```

---

### SetTabPadding - 设置标签内边距

```c++
int __stdcall SetTabPadding(
    HWND hTab,
    int horizontal,
    int vertical
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `horizontal` | 水平内边距（必须 >= 0） |
| `vertical` | 垂直内边距（必须 >= 0） |

**返回值：** 成功返回 0，无效参数或无效句柄返回 -1

**易语言 DLL 命令声明：**
```
.DLL命令 设置标签内边距, 整数型, "emoji_window.dll", "SetTabPadding", , , 设置标签页水平和垂直内边距（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 水平内边距, 整数型, , 水平方向内边距（>=0）
    .参数 垂直内边距, 整数型, , 垂直方向内边距（>=0）
```

**易语言示例：**
```
' 设置水平内边距 10，垂直内边距 5
设置标签内边距 (TabControl句柄, 10, 5)
```

---

## 单个标签页控制 API（v3.0 新增）

### EnableTabItem - 启用/禁用单个标签页

```c++
int __stdcall EnableTabItem(
    HWND hTab,
    int index,
    int enabled
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `index` | 标签页索引（从 0 开始） |
| `enabled` | 1=启用，0=禁用 |

**返回值：** 成功返回 0，无效句柄或越界索引返回 -1

**行为说明：**
- 禁用的标签页不响应点击，无法切换到该页
- 禁用的标签页以 50% 透明度渲染，提供视觉反馈

**易语言 DLL 命令声明：**
```
.DLL命令 启用禁用标签页, 整数型, "emoji_window.dll", "EnableTabItem", , , 启用或禁用单个标签页（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 索引, 整数型, , 标签页索引（从0开始）
    .参数 是否启用, 整数型, , 1=启用，0=禁用
```

**易语言示例：**
```
' 禁用第2个标签页（索引1）
启用禁用标签页 (TabControl句柄, 1, 0)

' 重新启用
启用禁用标签页 (TabControl句柄, 1, 1)
```

---

### GetTabItemEnabled - 获取标签页启用状态

```c++
int __stdcall GetTabItemEnabled(
    HWND hTab,
    int index
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `index` | 标签页索引（从 0 开始） |

**返回值：** 1=启用，0=禁用，-1=错误（无效句柄或越界索引）

**易语言 DLL 命令声明：**
```
.DLL命令 获取标签页启用状态, 整数型, "emoji_window.dll", "GetTabItemEnabled", , , 获取单个标签页的启用状态（1=启用，0=禁用，-1=错误）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 索引, 整数型, , 标签页索引（从0开始）
```

**易语言示例：**
```
.局部变量 状态, 整数型

状态 ＝ 获取标签页启用状态 (TabControl句柄, 1)
.如果 (状态 ＝ 1)
    ' 标签页已启用
.否则
    ' 标签页已禁用或查询失败
.如果结束
```

---

### ShowTabItem - 显示/隐藏单个标签页

```c++
int __stdcall ShowTabItem(
    HWND hTab,
    int index,
    int visible
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `index` | 标签页索引（从 0 开始） |
| `visible` | 1=显示，0=隐藏 |

**返回值：** 成功返回 0，无效句柄或越界索引返回 -1

**行为说明：**
- 隐藏的标签页不在标签栏中显示，其他标签页自动填补空位
- 如果隐藏的是当前选中页，自动切换到下一个可见的标签页

**易语言 DLL 命令声明：**
```
.DLL命令 显示隐藏标签页, 整数型, "emoji_window.dll", "ShowTabItem", , , 显示或隐藏单个标签页（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 索引, 整数型, , 标签页索引（从0开始）
    .参数 是否显示, 整数型, , 1=显示，0=隐藏
```

**易语言示例：**
```
' 隐藏第3个标签页（索引2）
显示隐藏标签页 (TabControl句柄, 2, 0)

' 重新显示
显示隐藏标签页 (TabControl句柄, 2, 1)
```

---

### SetTabItemIcon - 设置标签页图标

```c++
int __stdcall SetTabItemIcon(
    HWND hTab,
    int index,
    const unsigned char* iconBytes,
    int iconLen
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `index` | 标签页索引（从 0 开始） |
| `iconBytes` | PNG 图片字节数据指针（传 NULL 清除图标） |
| `iconLen` | 图片字节数据长度（传 0 清除图标） |

**返回值：** 成功返回 0，无效句柄或越界索引返回 -1

**行为说明：**
- 图标显示在标签标题文字左侧，图标与文字间距 4px
- 使用 WIC 解码 PNG 图标数据，通过 D2D 渲染

**易语言 DLL 命令声明：**
```
.DLL命令 设置标签页图标, 整数型, "emoji_window.dll", "SetTabItemIcon", , , 设置标签页图标PNG数据（成功返回0，失败返回-1，传0清除图标）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 索引, 整数型, , 标签页索引（从0开始）
    .参数 图标字节集指针, 整数型, , PNG图片字节数据指针（传0清除图标）
    .参数 图标长度, 整数型, , 图片字节数据长度（传0清除图标）
```

**易语言示例：**
```
.局部变量 图标数据, 字节集

' 从文件读取 PNG 图标
图标数据 ＝ 读入文件 ("icon.png")
.如果真 (取字节集长度 (图标数据) ＞ 0)
    设置标签页图标 (TabControl句柄, 0, 取变量数据地址 (图标数据), 取字节集长度 (图标数据))
.如果真结束

' 清除图标
设置标签页图标 (TabControl句柄, 0, 0, 0)
```

---

## 内容区域 API（v3.0 新增）

### SetTabContentBgColor - 设置单个标签页内容区域背景色

```c++
int __stdcall SetTabContentBgColor(
    HWND hTab,
    int index,
    UINT32 color
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `index` | 标签页索引（从 0 开始） |
| `color` | 背景色（ARGB 格式） |

**返回值：** 成功返回 0，无效句柄或越界索引返回 -1

**易语言 DLL 命令声明：**
```
.DLL命令 设置标签页内容背景色, 整数型, "emoji_window.dll", "SetTabContentBgColor", , , 设置指定标签页的内容区域背景色（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 索引, 整数型, , 标签页索引（从0开始）
    .参数 颜色, 整数型, , ARGB格式颜色值
```

**易语言示例：**
```
' 设置第1个标签页内容区域为浅蓝色背景
设置标签页内容背景色 (TabControl句柄, 0, 到ARGB (255, 236, 245, 255))
```

---

### SetTabContentBgColorAll - 设置所有标签页内容区域背景色

```c++
int __stdcall SetTabContentBgColorAll(
    HWND hTab,
    UINT32 color
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `color` | 背景色（ARGB 格式） |

**返回值：** 成功返回 0，无效句柄返回 -1

**易语言 DLL 命令声明：**
```
.DLL命令 设置所有标签页内容背景色, 整数型, "emoji_window.dll", "SetTabContentBgColorAll", , , 设置所有标签页的内容区域背景色（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 颜色, 整数型, , ARGB格式颜色值
```

**易语言示例：**
```
' 设置所有标签页内容区域为浅灰色背景
设置所有标签页内容背景色 (TabControl句柄, 到ARGB (255, 245, 247, 250))
```

---

## 交互增强 API（v3.0 新增）

### SetTabClosable - 设置标签页关闭按钮

```c++
int __stdcall SetTabClosable(
    HWND hTab,
    int closable
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `closable` | 1=显示关闭按钮，0=隐藏关闭按钮 |

**返回值：** 成功返回 0，无效句柄返回 -1

**行为说明：**
- 启用后，每个标签页标题右侧显示 × 关闭按钮
- 鼠标悬停在 × 按钮上时，按钮变为红色背景提供视觉反馈
- 点击 × 按钮触发通过 `SetTabCloseCallback` 设置的回调

**易语言 DLL 命令声明：**
```
.DLL命令 设置标签页可关闭, 整数型, "emoji_window.dll", "SetTabClosable", , , 设置标签页是否显示关闭按钮（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 是否可关闭, 整数型, , 1=显示关闭按钮，0=隐藏
```

**易语言示例：**
```
' 启用关闭按钮
设置标签页可关闭 (TabControl句柄, 1)
```

---

### SetTabCloseCallback - 设置关闭回调

```c++
int __stdcall SetTabCloseCallback(
    HWND hTab,
    TAB_CLOSE_CALLBACK callback
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `callback` | 关闭回调函数指针（`TAB_CLOSE_CALLBACK` 类型） |

**返回值：** 成功返回 0，无效句柄返回 -1

**易语言 DLL 命令声明：**
```
.DLL命令 设置标签页关闭回调, 整数型, "emoji_window.dll", "SetTabCloseCallback", , , 设置标签页关闭按钮点击回调（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 回调函数, 子程序指针, , 回调函数指针（参数：TabControl句柄, 索引）
```

**易语言示例：**
```
' 设置关闭回调
设置标签页可关闭 (TabControl句柄, 1)
设置标签页关闭回调 (TabControl句柄, &标签页关闭回调)

.子程序 标签页关闭回调, , , stdcall
.参数 TabControl句柄, 整数型
.参数 索引, 整数型

' 用户点击了关闭按钮，执行删除操作
移除Tab页 (TabControl句柄, 索引)
```

---

### SetTabRightClickCallback - 设置右键点击回调

```c++
int __stdcall SetTabRightClickCallback(
    HWND hTab,
    TAB_RIGHTCLICK_CALLBACK callback
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `callback` | 右键回调函数指针（`TAB_RIGHTCLICK_CALLBACK` 类型） |

**返回值：** 成功返回 0，无效句柄返回 -1

**行为说明：**
- 右键点击位置不在任何标签页上时不触发回调
- 回调传入鼠标屏幕坐标，可直接用于弹出菜单定位

**易语言 DLL 命令声明：**
```
.DLL命令 设置标签页右键回调, 整数型, "emoji_window.dll", "SetTabRightClickCallback", , , 设置标签页右键点击回调（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 回调函数, 子程序指针, , 回调函数指针（参数：TabControl句柄, 索引, X, Y）
```

**易语言示例：**
```
设置标签页右键回调 (TabControl句柄, &标签页右键回调)

.子程序 标签页右键回调, , , stdcall
.参数 TabControl句柄, 整数型
.参数 索引, 整数型
.参数 X, 整数型
.参数 Y, 整数型

' 在鼠标位置弹出右键菜单
弹出菜单 (右键菜单句柄, X, Y)
```

---

### SetTabDraggable - 设置标签页可拖拽

```c++
int __stdcall SetTabDraggable(
    HWND hTab,
    int draggable
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `draggable` | 1=可拖拽，0=不可拖拽 |

**返回值：** 成功返回 0，无效句柄返回 -1

**行为说明：**
- 启用后，用户可按住鼠标左键拖动标签页重新排序
- 拖拽时显示插入位置指示线
- 拖拽完成后保持拖拽的标签页为选中状态

**易语言 DLL 命令声明：**
```
.DLL命令 设置标签页可拖拽, 整数型, "emoji_window.dll", "SetTabDraggable", , , 设置标签页是否可拖拽排序（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 是否可拖拽, 整数型, , 1=可拖拽，0=不可拖拽
```

**易语言示例：**
```
' 启用拖拽排序
设置标签页可拖拽 (TabControl句柄, 1)
```

---

### SetTabDoubleClickCallback - 设置双击回调

```c++
int __stdcall SetTabDoubleClickCallback(
    HWND hTab,
    TAB_DBLCLICK_CALLBACK callback
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `callback` | 双击回调函数指针（`TAB_DBLCLICK_CALLBACK` 类型） |

**返回值：** 成功返回 0，无效句柄返回 -1

**易语言 DLL 命令声明：**
```
.DLL命令 设置标签页双击回调, 整数型, "emoji_window.dll", "SetTabDoubleClickCallback", , , 设置标签页双击回调（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 回调函数, 子程序指针, , 回调函数指针（参数：TabControl句柄, 索引）
```

**易语言示例：**
```
设置标签页双击回调 (TabControl句柄, &标签页双击回调)

.子程序 标签页双击回调, , , stdcall
.参数 TabControl句柄, 整数型
.参数 索引, 整数型

' 双击标签页，可实现重命名等功能
调试输出 ("双击了标签页索引：" ＋ 到文本 (索引))
```

---

## 布局与位置 API（v3.0 新增）

### SetTabPosition - 设置标签栏位置

```c++
int __stdcall SetTabPosition(
    HWND hTab,
    int position
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `position` | 标签栏位置：0=上，1=下，2=左，3=右 |

**返回值：** 成功返回 0，无效句柄或无效 position 值返回 -1

**行为说明：**
- 标签栏位置为左或右时，标签页垂直排列，文字保持水平方向
- 位置变更后自动重新计算内容区域的位置和大小

**易语言 DLL 命令声明：**
```
.DLL命令 设置标签栏位置, 整数型, "emoji_window.dll", "SetTabPosition", , , 设置标签栏位置（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 位置, 整数型, , 0=上，1=下，2=左，3=右
```

**易语言示例：**
```
' 将标签栏放到底部
设置标签栏位置 (TabControl句柄, 1)

' 将标签栏放到左侧
设置标签栏位置 (TabControl句柄, 2)
```

---

### SetTabAlignment - 设置标签对齐方式

> ⚠️ **注意：** 此功能在 TCS_OWNERDRAWFIXED 模式下暂未实现视觉效果。Win32 Tab Control 的标签位置由系统控制，自绘模式下无法直接调整标签的对齐方式。值会被存储但不会产生视觉变化。

```c++
int __stdcall SetTabAlignment(
    HWND hTab,
    int align
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `align` | 对齐方式：0=左对齐，1=居中，2=右对齐 |

**返回值：** 成功返回 0，无效句柄或无效 align 值返回 -1

**易语言 DLL 命令声明：**
```
.DLL命令 设置标签对齐方式, 整数型, "emoji_window.dll", "SetTabAlignment", , , 设置标签在标签栏中的对齐方式（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 对齐方式, 整数型, , 0=左对齐，1=居中，2=右对齐
```

**易语言示例：**
```
' 设置标签居中对齐
设置标签对齐方式 (TabControl句柄, 1)
```

---

### SetTabScrollable - 设置标签栏可滚动

```c++
int __stdcall SetTabScrollable(
    HWND hTab,
    int scrollable
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `scrollable` | 1=可滚动，0=不可滚动（多行模式） |

**返回值：** 成功返回 0，无效句柄返回 -1

**行为说明：**
- 启用滚动后，标签页总宽度超过标签栏时显示左右滚动箭头
- 支持鼠标滚轮和箭头点击滚动
- 禁用滚动时使用 Win32 Tab Control 默认的多行标签行为

**易语言 DLL 命令声明：**
```
.DLL命令 设置标签栏可滚动, 整数型, "emoji_window.dll", "SetTabScrollable", , , 设置标签栏是否可滚动（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 是否可滚动, 整数型, , 1=可滚动，0=不可滚动（多行模式）
```

**易语言示例：**
```
' 启用标签栏滚动
设置标签栏可滚动 (TabControl句柄, 1)
```

---

## 批量操作 API（v3.0 新增）

### RemoveAllTabs - 清空所有标签页

```c++
int __stdcall RemoveAllTabs(
    HWND hTab
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |

**返回值：** 成功返回 0，无效句柄返回 -1

**行为说明：**
- 销毁所有标签页的内容窗口，清空 pages 数组
- 正确清理每个内容窗口关联的 WindowState 和 D2D 渲染目标资源
- 清空后 currentIndex 设为 -1

**易语言 DLL 命令声明：**
```
.DLL命令 清空所有标签页, 整数型, "emoji_window.dll", "RemoveAllTabs", , , 清空所有标签页并销毁内容窗口（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
```

**易语言示例：**
```
' 清空所有标签页
清空所有标签页 (TabControl句柄)

' 清空后重新添加
.局部变量 标题字节集, 字节集
标题字节集 ＝ 编码_Ansi到Utf8 ("新标签页")
添加Tab页 (TabControl句柄, 取变量数据地址 (标题字节集), 取字节集长度 (标题字节集), 0)
```

---

### InsertTabItem - 在指定位置插入标签页

```c++
int __stdcall InsertTabItem(
    HWND hTab,
    int index,
    const unsigned char* title,
    int titleLen,
    HWND hContent
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `index` | 插入位置索引（超出范围追加到末尾） |
| `title` | UTF-8 编码的标签页标题字节集指针 |
| `titleLen` | 标题字节集长度 |
| `hContent` | 内容窗口句柄（传 NULL 则自动创建） |

**返回值：** 成功返回新插入标签页的实际索引，index < 0 或无效句柄返回 -1

**行为说明：**
- 插入后自动更新所有后续标签页的索引
- 如果插入位置在当前选中标签页之前或等于当前选中标签页，currentIndex 自动加 1

**易语言 DLL 命令声明：**
```
.DLL命令 插入标签页, 整数型, "emoji_window.dll", "InsertTabItem", , , 在指定位置插入标签页（返回实际索引，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 索引, 整数型, , 插入位置索引（超出范围追加到末尾）
    .参数 标题字节集指针, 整数型, , UTF-8编码的标题字节集指针
    .参数 标题长度, 整数型, , 标题字节集长度
    .参数 内容窗口句柄, 整数型, , 内容窗口句柄（传0自动创建）
```

**易语言示例：**
```
.局部变量 标题字节集, 字节集
.局部变量 新索引, 整数型

' 在第1个位置（索引0）插入新标签页
' "➕ 新页面"  ➕ = { 226, 158, 149 }
标题字节集 ＝ { 226, 158, 149, 32 } ＋ 编码_Ansi到Utf8 ("新页面")
新索引 ＝ 插入标签页 (TabControl句柄, 0, 取变量数据地址 (标题字节集), 取字节集长度 (标题字节集), 0)
```

---

### MoveTabItem - 移动标签页位置

```c++
int __stdcall MoveTabItem(
    HWND hTab,
    int fromIndex,
    int toIndex
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `fromIndex` | 源位置索引 |
| `toIndex` | 目标位置索引 |

**返回值：** 成功返回 0，fromIndex == toIndex 返回 0（不操作），越界索引或无效句柄返回 -1

**行为说明：**
- 移动后自动更新所有受影响标签页的索引
- 如果被移动的标签页是当前选中页，currentIndex 更新为移动后的新位置

**易语言 DLL 命令声明：**
```
.DLL命令 移动标签页, 整数型, "emoji_window.dll", "MoveTabItem", , , 移动标签页位置（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 源索引, 整数型, , 源位置索引
    .参数 目标索引, 整数型, , 目标位置索引
```

**易语言示例：**
```
' 将第1个标签页（索引0）移动到第3个位置（索引2）
移动标签页 (TabControl句柄, 0, 2)
```

---

### GetTabIndexByTitle - 根据标题查找标签页索引

```c++
int __stdcall GetTabIndexByTitle(
    HWND hTab,
    const unsigned char* titleBytes,
    int titleLen
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `titleBytes` | UTF-8 编码的标题字节集指针 |
| `titleLen` | 标题字节集长度 |

**返回值：** 找到返回标签页索引，未找到返回 -1，无效参数返回 -1

**行为说明：**
- 使用精确匹配（区分大小写）
- 返回第一个匹配的标签页索引

**易语言 DLL 命令声明：**
```
.DLL命令 根据标题查找标签页, 整数型, "emoji_window.dll", "GetTabIndexByTitle", , , 根据标题查找标签页索引（未找到返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 标题字节集指针, 整数型, , UTF-8编码的标题字节集指针
    .参数 标题长度, 整数型, , 标题字节集长度
```

**易语言示例：**
```
.局部变量 标题字节集, 字节集
.局部变量 索引, 整数型

' 查找标题为 "设置" 的标签页
标题字节集 ＝ 编码_Ansi到Utf8 ("设置")
索引 ＝ 根据标题查找标签页 (TabControl句柄, 取变量数据地址 (标题字节集), 取字节集长度 (标题字节集))
.如果 (索引 ≥ 0)
    ' 找到了，切换到该标签页
    切换到Tab (TabControl句柄, 索引)
.否则
    ' 未找到
.如果结束
```

---

## 状态查询 API（v3.0 新增）

### GetTabEnabled - 获取 TabControl 启用状态

```c++
int __stdcall GetTabEnabled(
    HWND hTab
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |

**返回值：** 1=启用，0=禁用，-1=无效句柄

**行为说明：**
- 通过 Win32 API `IsWindowEnabled` 获取整个控件的启用状态

**易语言 DLL 命令声明：**
```
.DLL命令 获取TabControl启用状态, 整数型, "emoji_window.dll", "GetTabEnabled", , , 获取整个TabControl的启用状态（1=启用，0=禁用，-1=错误）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
```

**易语言示例：**
```
.局部变量 状态, 整数型

状态 ＝ 获取TabControl启用状态 (TabControl句柄)
.如果 (状态 ＝ 1)
    ' TabControl 已启用
.否则
    ' TabControl 已禁用或查询失败
.如果结束
```

---

### IsTabItemSelected - 判断标签页是否选中

```c++
int __stdcall IsTabItemSelected(
    HWND hTab,
    int index
);
```

**参数说明：**

| 参数 | 说明 |
|------|------|
| `hTab` | TabControl 窗口句柄 |
| `index` | 标签页索引（从 0 开始） |

**返回值：** 1=选中，0=未选中，-1=错误（无效句柄或越界索引）

**易语言 DLL 命令声明：**
```
.DLL命令 标签页是否选中, 整数型, "emoji_window.dll", "IsTabItemSelected", , , 判断指定标签页是否为当前选中（1=选中，0=未选中，-1=错误）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 索引, 整数型, , 标签页索引（从0开始）
```

**易语言示例：**
```
.局部变量 是否选中, 整数型

是否选中 ＝ 标签页是否选中 (TabControl句柄, 0)
.如果 (是否选中 ＝ 1)
    ' 第1个标签页是当前选中页
.否则
    ' 第1个标签页未选中
.如果结束
```

---

## 样式说明

- 标签页高度: 34px（默认，可通过 SetTabItemSize 修改）
- 标签页宽度: 120px（默认，可通过 SetTabItemSize 修改）
- 标签页间距: 2px
- 选中标签页背景: #FFFFFF（默认，可通过 SetTabColors 修改）
- 选中标签页文本: #409EFF（默认，可通过 SetTabColors 修改）
- 未选中标签页背景: #F5F7FA（默认，可通过 SetTabColors 修改）
- 未选中标签页文本: #606266（默认，可通过 SetTabColors 修改）
- 选中指示条: #409EFF（默认，可通过 SetTabIndicatorColor 修改）
- 悬停背景: #ECF5FF
- 内容区域背景: #FFFFFF（默认，可通过 SetTabContentBgColor 修改）
- 字体: Segoe UI Emoji 13px（默认，可通过 SetTabFont 修改）
- 水平内边距: 2px（默认，可通过 SetTabPadding 修改）
- 垂直内边距: 0px（默认，可通过 SetTabPadding 修改）
- 支持彩色 Emoji 标题

## 使用流程

1. 创建 TabControl
2. 添加标签页(自动创建内容窗口)
3. 获取标签页内容窗口
4. 在内容窗口中创建子控件
5. 设置切换回调(可选)
6. 自定义外观（可选）：设置尺寸、字体、颜色、内边距
7. 启用交互增强（可选）：关闭按钮、拖拽排序、右键菜单、双击回调
8. 调整布局（可选）：标签栏位置、对齐方式、滚动支持


## 易语言声明

```
.DLL命令 创建TabControl, 整数型, "emoji_window.dll", "CreateTabControl"
    .参数 父窗口句柄, 整数型
    .参数 X坐标, 整数型
    .参数 Y坐标, 整数型
    .参数 宽度, 整数型
    .参数 高度, 整数型

.DLL命令 添加Tab页, 整数型, "emoji_window.dll", "AddTabItem"
    .参数 TabControl句柄, 整数型
    .参数 标题字节集指针, 整数型
    .参数 标题长度, 整数型
    .参数 图标索引, 整数型

.DLL命令 移除Tab页, 逻辑型, "emoji_window.dll", "RemoveTabItem"
    .参数 TabControl句柄, 整数型
    .参数 索引, 整数型

.DLL命令 设置Tab切换回调, , "emoji_window.dll", "SetTabCallback"
    .参数 TabControl句柄, 整数型
    .参数 回调函数, 子程序指针

.DLL命令 获取当前Tab索引, 整数型, "emoji_window.dll", "GetCurrentTabIndex"
    .参数 TabControl句柄, 整数型

.DLL命令 切换到Tab, 逻辑型, "emoji_window.dll", "SelectTab"
    .参数 TabControl句柄, 整数型
    .参数 索引, 整数型

.DLL命令 获取Tab数量, 整数型, "emoji_window.dll", "GetTabCount"
    .参数 TabControl句柄, 整数型

.DLL命令 获取Tab内容窗口, 整数型, "emoji_window.dll", "GetTabContentWindow"
    .参数 TabControl句柄, 整数型
    .参数 索引, 整数型

.DLL命令 销毁TabControl, , "emoji_window.dll", "DestroyTabControl"
    .参数 TabControl句柄, 整数型

.DLL命令 更新TabControl布局, , "emoji_window.dll", "UpdateTabControlLayout"
    .参数 TabControl句柄, 整数型

' ========== TabControl 属性命令（v2.1 新增）==========

.DLL命令 获取Tab页标题, 整数型, "emoji_window.dll", "GetTabTitle", , , 获取指定Tab页的标题（返回UTF-8字节数，缓冲区指针为0时返回所需大小）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 索引, 整数型, , Tab页索引（从0开始）
    .参数 缓冲区指针, 整数型, , 接收标题的缓冲区指针（传0获取所需大小）
    .参数 缓冲区大小, 整数型, , 缓冲区大小（字节）

.DLL命令 设置Tab页标题, 整数型, "emoji_window.dll", "SetTabTitle", , , 设置指定Tab页的标题（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 索引, 整数型, , Tab页索引（从0开始）
    .参数 标题字节集指针, 整数型, , UTF-8编码的标题字节集指针
    .参数 标题长度, 整数型, , 标题字节集长度

.DLL命令 获取TabControl位置, 整数型, "emoji_window.dll", "GetTabControlBounds", , , 获取TabControl位置和大小（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 X坐标, 整数型, 传址, 输出：X坐标（相对父窗口）
    .参数 Y坐标, 整数型, 传址, 输出：Y坐标（相对父窗口）
    .参数 宽度, 整数型, 传址, 输出：宽度
    .参数 高度, 整数型, 传址, 输出：高度

.DLL命令 设置TabControl位置, 整数型, "emoji_window.dll", "SetTabControlBounds", , , 设置TabControl位置和大小（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 X坐标, 整数型, , 新X坐标（相对父窗口）
    .参数 Y坐标, 整数型, , 新Y坐标（相对父窗口）
    .参数 宽度, 整数型, , 新宽度
    .参数 高度, 整数型, , 新高度

.DLL命令 获取TabControl可视状态, 整数型, "emoji_window.dll", "GetTabControlVisible", , , 获取TabControl可视状态（1=可见，0=不可见，-1=错误）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄

.DLL命令 显示隐藏TabControl, 整数型, "emoji_window.dll", "ShowTabControl", , , 显示或隐藏TabControl（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 是否显示, 整数型, , 1=显示，0=隐藏

.DLL命令 启用禁用TabControl, 整数型, "emoji_window.dll", "EnableTabControl", , , 启用或禁用TabControl（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 是否启用, 整数型, , 1=启用，0=禁用

' ========== TabControl 增强命令（v3.0 新增）==========

' ----- 外观定制 -----
.DLL命令 设置标签页尺寸, 整数型, "emoji_window.dll", "SetTabItemSize", , , 设置标签页固定宽度和高度（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 宽度, 整数型, , 标签页宽度（必须大于0）
    .参数 高度, 整数型, , 标签页高度（必须大于0）

.DLL命令 设置标签字体, 整数型, "emoji_window.dll", "SetTabFont", , , 设置标签页字体名称和字号（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 字体名字节集指针, 整数型, , UTF-8编码的字体名称字节集指针
    .参数 字体名长度, 整数型, , 字体名称字节集长度
    .参数 字号, 小数型, , 字号大小（如 14.0）

.DLL命令 设置标签颜色, 整数型, "emoji_window.dll", "SetTabColors", , , 设置选中/未选中标签页的背景色和文字色（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 选中背景色, 整数型, , ARGB格式颜色值
    .参数 未选中背景色, 整数型, , ARGB格式颜色值
    .参数 选中文字色, 整数型, , ARGB格式颜色值
    .参数 未选中文字色, 整数型, , ARGB格式颜色值

.DLL命令 设置指示条颜色, 整数型, "emoji_window.dll", "SetTabIndicatorColor", , , 设置选中标签页底部指示条颜色（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 颜色, 整数型, , ARGB格式颜色值

.DLL命令 设置标签内边距, 整数型, "emoji_window.dll", "SetTabPadding", , , 设置标签页水平和垂直内边距（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 水平内边距, 整数型, , 水平方向内边距（>=0）
    .参数 垂直内边距, 整数型, , 垂直方向内边距（>=0）

' ----- 单个标签页控制 -----
.DLL命令 启用禁用标签页, 整数型, "emoji_window.dll", "EnableTabItem", , , 启用或禁用单个标签页（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 索引, 整数型, , 标签页索引（从0开始）
    .参数 是否启用, 整数型, , 1=启用，0=禁用

.DLL命令 获取标签页启用状态, 整数型, "emoji_window.dll", "GetTabItemEnabled", , , 获取单个标签页的启用状态（1=启用，0=禁用，-1=错误）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 索引, 整数型, , 标签页索引（从0开始）

.DLL命令 显示隐藏标签页, 整数型, "emoji_window.dll", "ShowTabItem", , , 显示或隐藏单个标签页（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 索引, 整数型, , 标签页索引（从0开始）
    .参数 是否显示, 整数型, , 1=显示，0=隐藏

.DLL命令 设置标签页图标, 整数型, "emoji_window.dll", "SetTabItemIcon", , , 设置标签页图标PNG数据（成功返回0，失败返回-1，传0清除图标）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 索引, 整数型, , 标签页索引（从0开始）
    .参数 图标字节集指针, 整数型, , PNG图片字节数据指针（传0清除图标）
    .参数 图标长度, 整数型, , 图片字节数据长度（传0清除图标）

' ----- 内容区域 -----
.DLL命令 设置标签页内容背景色, 整数型, "emoji_window.dll", "SetTabContentBgColor", , , 设置指定标签页的内容区域背景色（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 索引, 整数型, , 标签页索引（从0开始）
    .参数 颜色, 整数型, , ARGB格式颜色值

.DLL命令 设置所有标签页内容背景色, 整数型, "emoji_window.dll", "SetTabContentBgColorAll", , , 设置所有标签页的内容区域背景色（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 颜色, 整数型, , ARGB格式颜色值

' ----- 交互增强 -----
.DLL命令 设置标签页可关闭, 整数型, "emoji_window.dll", "SetTabClosable", , , 设置标签页是否显示关闭按钮（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 是否可关闭, 整数型, , 1=显示关闭按钮，0=隐藏

.DLL命令 设置标签页关闭回调, 整数型, "emoji_window.dll", "SetTabCloseCallback", , , 设置标签页关闭按钮点击回调（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 回调函数, 子程序指针, , 回调函数指针（参数：TabControl句柄, 索引）

.DLL命令 设置标签页右键回调, 整数型, "emoji_window.dll", "SetTabRightClickCallback", , , 设置标签页右键点击回调（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 回调函数, 子程序指针, , 回调函数指针（参数：TabControl句柄, 索引, X, Y）

.DLL命令 设置标签页可拖拽, 整数型, "emoji_window.dll", "SetTabDraggable", , , 设置标签页是否可拖拽排序（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 是否可拖拽, 整数型, , 1=可拖拽，0=不可拖拽

.DLL命令 设置标签页双击回调, 整数型, "emoji_window.dll", "SetTabDoubleClickCallback", , , 设置标签页双击回调（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 回调函数, 子程序指针, , 回调函数指针（参数：TabControl句柄, 索引）

' ----- 布局与位置 -----
.DLL命令 设置标签栏位置, 整数型, "emoji_window.dll", "SetTabPosition", , , 设置标签栏位置（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 位置, 整数型, , 0=上，1=下，2=左，3=右

.DLL命令 设置标签对齐方式, 整数型, "emoji_window.dll", "SetTabAlignment", , , 设置标签在标签栏中的对齐方式（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 对齐方式, 整数型, , 0=左对齐，1=居中，2=右对齐

.DLL命令 设置标签栏可滚动, 整数型, "emoji_window.dll", "SetTabScrollable", , , 设置标签栏是否可滚动（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 是否可滚动, 整数型, , 1=可滚动，0=不可滚动（多行模式）

' ----- 批量操作 -----
.DLL命令 清空所有标签页, 整数型, "emoji_window.dll", "RemoveAllTabs", , , 清空所有标签页并销毁内容窗口（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄

.DLL命令 插入标签页, 整数型, "emoji_window.dll", "InsertTabItem", , , 在指定位置插入标签页（返回实际索引，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 索引, 整数型, , 插入位置索引（超出范围追加到末尾）
    .参数 标题字节集指针, 整数型, , UTF-8编码的标题字节集指针
    .参数 标题长度, 整数型, , 标题字节集长度
    .参数 内容窗口句柄, 整数型, , 内容窗口句柄（传0自动创建）

.DLL命令 移动标签页, 整数型, "emoji_window.dll", "MoveTabItem", , , 移动标签页位置（成功返回0，失败返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 源索引, 整数型, , 源位置索引
    .参数 目标索引, 整数型, , 目标位置索引

.DLL命令 根据标题查找标签页, 整数型, "emoji_window.dll", "GetTabIndexByTitle", , , 根据标题查找标签页索引（未找到返回-1）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 标题字节集指针, 整数型, , UTF-8编码的标题字节集指针
    .参数 标题长度, 整数型, , 标题字节集长度

' ----- 状态查询 -----
.DLL命令 获取TabControl启用状态, 整数型, "emoji_window.dll", "GetTabEnabled", , , 获取整个TabControl的启用状态（1=启用，0=禁用，-1=错误）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄

.DLL命令 标签页是否选中, 整数型, "emoji_window.dll", "IsTabItemSelected", , , 判断指定标签页是否为当前选中（1=选中，0=未选中，-1=错误）
    .参数 TabControl句柄, 整数型, , TabControl窗口句柄
    .参数 索引, 整数型, , 标签页索引（从0开始）
```


## 易语言示例

### 基础示例（创建 TabControl 并添加 Tab 页）

```
.版本 2

.程序集变量 窗口句柄, 整数型
.程序集变量 TabControl句柄, 整数型
.程序集变量 Tab1内容窗口, 整数型
.程序集变量 Tab2内容窗口, 整数型
.程序集变量 Tab3内容窗口, 整数型
.程序集变量 按钮1, 整数型
.程序集变量 按钮2, 整数型

.子程序 _启动窗口_创建完毕

窗口句柄 = 创建Emoji窗口 ("选项卡示例", 800, 600)

' 创建 TabControl
TabControl句柄 = 创建TabControl (窗口句柄, 20, 20, 760, 560)

' 添加标签页(支持 Emoji)
添加Tab页_辅助 (TabControl句柄, "❤️ 首页", 0)
添加Tab页_辅助 (TabControl句柄, "🔧 设置", 0)
添加Tab页_辅助 (TabControl句柄, "⏰ 关于", 0)

' 设置切换回调
设置Tab切换回调 (TabControl句柄, &Tab切换回调)

' 获取各个标签页的内容窗口
Tab1内容窗口 = 获取Tab内容窗口 (TabControl句柄, 0)
Tab2内容窗口 = 获取Tab内容窗口 (TabControl句柄, 1)
Tab3内容窗口 = 获取Tab内容窗口 (TabControl句柄, 2)

' 在 Tab1 中创建控件
按钮1 = 创建Emoji按钮_辅助 (Tab1内容窗口, "⭐", "收藏", 30, 30, 150, 50, #COLOR_PRIMARY)

' 在 Tab2 中创建控件
按钮2 = 创建Emoji按钮_辅助 (Tab2内容窗口, "⚙️", "设置项", 30, 30, 150, 50, #COLOR_SUCCESS)

设置按钮点击回调 (&按钮点击回调)

运行消息循环 ()


.子程序 Tab切换回调, , 公开, stdcall
.参数 TabControl, 整数型
.参数 当前索引, 整数型

调试输出 ("Tab切换到索引: " + 到文本 (当前索引))


.子程序 按钮点击回调, , 公开, stdcall
.参数 按钮ID, 整数型
.参数 父窗口句柄, 整数型

.判断开始 (父窗口句柄 = Tab1内容窗口)
    .如果真 (按钮ID = 按钮1)
        信息框 ("这是Tab1中的按钮", 0, "提示")
    .如果真结束
    
.判断 (父窗口句柄 = Tab2内容窗口)
    .如果真 (按钮ID = 按钮2)
        信息框 ("这是Tab2中的按钮", 0, "提示")
    .如果真结束
.判断结束
```

### 增强功能示例（v3.0 新增）

```
.版本 2

.程序集变量 主窗口句柄, 整数型
.程序集变量 TabControl句柄, 整数型

.子程序 _启动子程序, 整数型
.局部变量 utf8字节集, 字节集
.局部变量 Tab标题字节集, 字节集
.局部变量 字体名字节集, 字节集

' 创建窗口
utf8字节集 ＝ 编码_Ansi到Utf8 ("TabControl增强功能示例")
主窗口句柄 ＝ 创建Emoji窗口_字节集_扩展 (取变量数据地址 (utf8字节集), 取字节集长度 (utf8字节集), 800, 600, 到RGB (70, 130, 180))

' 创建 TabControl
TabControl句柄 ＝ 创建TabControl (主窗口句柄, 20, 20, 760, 500)

' 添加Tab页
' "📋 基本信息"  📋 = { 240, 159, 147, 139 }
Tab标题字节集 ＝ { 240, 159, 147, 139, 32 } ＋ 编码_Ansi到Utf8 ("基本信息")
添加Tab页 (TabControl句柄, 取变量数据地址 (Tab标题字节集), 取字节集长度 (Tab标题字节集), 0)

' "⚙ 设置选项"  ⚙ = { 226, 154, 153 }
Tab标题字节集 ＝ { 226, 154, 153, 32 } ＋ 编码_Ansi到Utf8 ("设置选项")
添加Tab页 (TabControl句柄, 取变量数据地址 (Tab标题字节集), 取字节集长度 (Tab标题字节集), 0)

' "🔧 高级功能"  🔧 = { 240, 159, 148, 167 }
Tab标题字节集 ＝ { 240, 159, 148, 167, 32 } ＋ 编码_Ansi到Utf8 ("高级功能")
添加Tab页 (TabControl句柄, 取变量数据地址 (Tab标题字节集), 取字节集长度 (Tab标题字节集), 0)

' ===== 自定义外观 =====
' 设置标签页尺寸
设置标签页尺寸 (TabControl句柄, 150, 40)

' 设置字体
字体名字节集 ＝ 编码_Ansi到Utf8 ("微软雅黑")
设置标签字体 (TabControl句柄, 取变量数据地址 (字体名字节集), 取字节集长度 (字体名字节集), 14.0)

' 设置颜色主题
设置标签颜色 (TabControl句柄, 到ARGB (255, 64, 158, 255), 到ARGB (255, 245, 247, 250), 到ARGB (255, 255, 255, 255), 到ARGB (255, 96, 98, 102))

' 设置指示条为绿色
设置指示条颜色 (TabControl句柄, 到ARGB (255, 103, 194, 58))

' 设置内边距
设置标签内边距 (TabControl句柄, 10, 5)

' ===== 启用交互增强 =====
' 启用关闭按钮和回调
设置标签页可关闭 (TabControl句柄, 1)
设置标签页关闭回调 (TabControl句柄, &标签页关闭回调)

' 启用拖拽排序
设置标签页可拖拽 (TabControl句柄, 1)

' 设置右键和双击回调
设置标签页右键回调 (TabControl句柄, &标签页右键回调)
设置标签页双击回调 (TabControl句柄, &标签页双击回调)

' ===== 设置内容区域背景色 =====
设置所有标签页内容背景色 (TabControl句柄, 到ARGB (255, 250, 250, 250))

' ===== 禁用第3个标签页 =====
启用禁用标签页 (TabControl句柄, 2, 0)

设置消息循环主窗口 (主窗口句柄)
运行消息循环 ()
返回 (0)


.子程序 标签页关闭回调, , , stdcall
.参数 TabControl句柄, 整数型
.参数 索引, 整数型

移除Tab页 (TabControl句柄, 索引)


.子程序 标签页右键回调, , , stdcall
.参数 TabControl句柄, 整数型
.参数 索引, 整数型
.参数 X, 整数型
.参数 Y, 整数型

调试输出 ("右键点击标签页索引：" ＋ 到文本 (索引))


.子程序 标签页双击回调, , , stdcall
.参数 TabControl句柄, 整数型
.参数 索引, 整数型

调试输出 ("双击标签页索引：" ＋ 到文本 (索引))


.子程序 到ARGB, 整数型
.参数 A, 整数型
.参数 R, 整数型
.参数 G, 整数型
.参数 B, 整数型

返回 (左移 (A, 24) ＋ 左移 (R, 16) ＋ 左移 (G, 8) ＋ B)

.子程序 到RGB, 整数型
.参数 R, 整数型
.参数 G, 整数型
.参数 B, 整数型

返回 (左移 (R, 16) ＋ 左移 (G, 8) ＋ B)
```

## 注意事项

⚠️ **重要提示：**

1. 标签页标题支持 UTF-8 编码和彩色 Emoji，使用字节集方式传递（参考易语言 Emoji 使用注意事项）
2. 每个标签页都有独立的内容窗口
3. 在内容窗口中创建的控件坐标相对于内容窗口
4. 切换标签页时，其他标签页的内容会自动隐藏
5. 销毁 TabControl 前应先销毁其中的子控件
6. 窗口大小改变时需要手动调整 TabControl 大小
7. **两次调用模式**：`GetTabTitle` 使用两次调用模式，第一次传 0 获取所需缓冲区大小，第二次传入缓冲区获取实际内容
8. **UTF-8 字节集显示**：DLL 返回的标题缓冲区是 UTF-8 字节集，不能用 `到文本()` 转换，必须全程用字节集拼接后传给显示函数
9. **按钮 ID 保存**：创建按钮时必须将返回的 ID 保存到程序集变量，不能用硬编码数字判断
10. **ShowTabControl 行为**：隐藏 TabControl 时，当前激活的内容窗口也会同步隐藏；显示时同步显示
11. **回调函数防 GC**：回调函数必须声明为 stdcall 调用约定，且回调函数指针需保持有效（不要使用局部变量传递）
12. **关闭按钮**：需先调用 `SetTabClosable` 启用关闭按钮，再调用 `SetTabCloseCallback` 设置回调
13. **禁用标签页**：禁用的标签页以 50% 透明度渲染，点击不响应

## 窗口大小改变处理

```
.子程序 窗口大小改变回调, , 公开, stdcall
.参数 窗口句柄, 整数型
.参数 新宽度, 整数型
.参数 新高度, 整数型

' 调整 TabControl 大小
.如果真 (TabControl句柄 ≠ 0)
    MoveWindow (TabControl句柄, 20, 20, 新宽度 - 40, 新高度 - 40, 真)
.如果真结束
```

## 相关文档

- [分组框](groupbox.md)
- [按钮控件](button.md)
- [布局管理器](../layout.md)
