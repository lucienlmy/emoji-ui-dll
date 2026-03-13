# 选项卡控件 (TabControl)

[← 返回主文档](../../README.md)

## 概述

多标签页容器控件,支持动态添加/删除标签页、自动创建内容窗口和标签页切换回调。

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

## 样式说明

- 标签页高度: 40px
- 标签页最小宽度: 80px
- 标签页最大宽度: 200px
- 标签页间距: 2px
- 选中标签页背景: #409EFF
- 选中标签页文本: #FFFFFF
- 未选中标签页背景: #F5F7FA
- 未选中标签页文本: #606266
- 悬停背景: #ECF5FF
- 内容区域背景: #FFFFFF
- 支持彩色 Emoji 标题

## 使用流程

1. 创建 TabControl
2. 添加标签页(自动创建内容窗口)
3. 获取标签页内容窗口
4. 在内容窗口中创建子控件
5. 设置切换回调(可选)

## 易语言示例

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

' 在 Tab3 中创建标签
创建标签_辅助 (Tab3内容窗口, 30, 30, 700, 100, "这是关于页面" + #换行符 + "版本: 1.0.0" + #换行符 + "作者: XXX", #COLOR_TEXT_PRIMARY, #COLOR_BG_LIGHT, , , , , , , 真)

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


.子程序 _启动窗口_将被销毁

' 销毁 TabControl
.如果真 (TabControl句柄 ≠ 0)
    销毁TabControl (TabControl句柄)
    TabControl句柄 = 0
.如果真结束

' 销毁窗口
.如果真 (窗口句柄 ≠ 0)
    销毁窗口 (窗口句柄)
    窗口句柄 = 0
.如果真结束
```

## 动态添加/删除示例

```
.版本 2

.程序集变量 计数器, 整数型

.子程序 添加新标签页

计数器 = 计数器 + 1
添加Tab页_辅助 (TabControl句柄, "新标签页 " + 到文本 (计数器), 0)

' 获取新标签页的内容窗口
.局部变量 新窗口, 整数型
.局部变量 索引, 整数型

索引 = 获取当前Tab索引 (TabControl句柄)
新窗口 = 获取Tab内容窗口 (TabControl句柄, 索引)

' 在新窗口中创建控件
创建标签_辅助 (新窗口, 20, 20, 300, 30, "这是新添加的标签页", #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE)


.子程序 删除当前标签页
.局部变量 索引, 整数型

索引 = 获取当前Tab索引 (TabControl句柄)
.如果真 (索引 ≥ 0)
    移除Tab页 (TabControl句柄, 索引)
.如果真结束
```

## 注意事项

⚠️ **重要提示**:

1. 标签页标题支持 UTF-8 编码和彩色 Emoji
2. 每个标签页都有独立的内容窗口
3. 在内容窗口中创建的控件坐标相对于内容窗口
4. 切换标签页时,其他标签页的内容会自动隐藏
5. 销毁 TabControl 前应先销毁其中的子控件
6. 窗口大小改变时需要手动调整 TabControl 大小

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
- [布局管理器](../layout.md)
