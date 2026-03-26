# 列表框控件 (ListBox)

[← 返回主文档](../../README.md)

## 概述

可滚动的项目列表控件,支持单选/多选、自定义渲染和 Unicode 多语言显示。

## API 文档

### 创建列表框

```c++
HWND __stdcall CreateListBox(
    HWND hParent,
    int x, int y, int width, int height,
    BOOL multi_select,
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
| `multi_select` | 是否支持多选(TRUE=多选, FALSE=单选) |
| `fg_color` | 前景色/文本颜色(ARGB格式) |
| `bg_color` | 背景色(ARGB格式) |

**返回值:** 列表框控件句柄

### 添加/删除项目

```c++
int __stdcall AddListItem(HWND hListBox, const unsigned char* text_bytes, int text_len);
void __stdcall RemoveListItem(HWND hListBox, int index);
void __stdcall ClearListBox(HWND hListBox);
```

### 获取/设置选中项

```c++
int __stdcall GetSelectedItemIndex(HWND hListBox);
void __stdcall SetSelectedItemIndex(HWND hListBox, int index);
```

### 获取项目文本

```c++
int __stdcall GetListItemText(HWND hListBox, int index, unsigned char* buffer, int buffer_size);
```

**返回值:** 实际文本长度(字节数)

### 设置项目文本

```c++
BOOL __stdcall SetListItemText(HWND hListBox, int index, const unsigned char* text_bytes, int text_len);
```

**参数说明:**

| 参数 | 说明 |
|------|------|
| `hListBox` | 列表框句柄 |
| `index` | 项目索引(从0开始) |
| `text_bytes` | 新文本的UTF-8字节指针 |
| `text_len` | 新文本字节长度 |

**返回值:** 成功返回TRUE，失败返回FALSE

### 获取项目数量

```c++
int __stdcall GetListItemCount(HWND hListBox);
```

### 设置回调

```c++
typedef void (__stdcall *ListBoxCallback)(HWND hListBox, int index);
void __stdcall SetListBoxCallback(HWND hListBox, ListBoxCallback callback);
```

**回调参数:**
- `hListBox`: 列表框句柄
- `index`: 选中项索引(-1 表示未选中)

### 其他操作

```c++
void __stdcall EnableListBox(HWND hListBox, BOOL enable);
void __stdcall ShowListBox(HWND hListBox, BOOL show);
void __stdcall SetListBoxBounds(HWND hListBox, int x, int y, int width, int height);
```

## 样式说明

- 项目高度: 32px
- 选中背景色: #409EFF
- 选中文本色: #FFFFFF
- 悬停背景色: #ECF5FF
- 边框颜色: #DCDFE6
- 滚动条宽度: 8px（圆角矩形滑块，内容超出时自动显示）
- 滚动条轨道: 半透明背景，右侧2px间距
- 支持鼠标滚轮滚动
- 支持彩色 Emoji 显示
- 支持多语言 Unicode 字符

## 易语言示例

```
.版本 2

.程序集变量 窗口句柄, 整数型
.程序集变量 列表框句柄, 整数型
.程序集变量 按钮_添加, 整数型
.程序集变量 按钮_删除, 整数型
.程序集变量 状态标签, 整数型

.子程序 _启动窗口_创建完毕

窗口句柄 = 创建Emoji窗口 ("列表框示例", 500, 500)

' 创建列表框
列表框句柄 = 创建列表框 (窗口句柄, 20, 20, 300, 350, 假, #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE)

' 添加初始项目(支持 Emoji 和多语言)
添加列表项_辅助 (列表框句柄, "🇨🇳 北京市 Beijing")
添加列表项_辅助 (列表框句柄, "🇨🇳 上海市 Shanghai")
添加列表项_辅助 (列表框句柄, "🇯🇵 東京 Tokyo")
添加列表项_辅助 (列表框句柄, "🇰🇷 서울 Seoul")
添加列表项_辅助 (列表框句柄, "🇷🇺 Москва Moscow")
添加列表项_辅助 (列表框句柄, "🇫🇷 Paris 巴黎")

' 设置列表框回调
设置列表框回调 (列表框句柄, &列表框选中回调)

' 创建操作按钮
按钮_添加 = 创建Emoji按钮_辅助 (窗口句柄, "➕", "添加项目", 340, 20, 130, 40, #COLOR_PRIMARY)
按钮_删除 = 创建Emoji按钮_辅助 (窗口句柄, "❌", "删除选中", 340, 70, 130, 40, #COLOR_DANGER)

' 创建状态标签
状态标签 = 创建标签_辅助 (窗口句柄, 20, 390, 460, 80, "请选择一个城市", #COLOR_TEXT_PRIMARY, #COLOR_BG_LIGHT, , , , , , , 真)

' 设置按钮回调
设置按钮点击回调 (&按钮点击回调)

运行消息循环 ()


.子程序 按钮点击回调, , 公开, stdcall
.参数 按钮ID, 整数型
.局部变量 选中索引, 整数型

.如果真 (按钮ID = 按钮_添加)
    ' 添加新项目
    添加列表项_辅助 (列表框句柄, "新城市")
    设置标签文本_辅助 (状态标签, "已添加新项目")
.如果真结束

.如果真 (按钮ID = 按钮_删除)
    ' 删除选中项
    选中索引 = 获取选中项索引 (列表框句柄)
    .如果 (选中索引 ≠ -1)
        移除列表项 (列表框句柄, 选中索引)
        设置标签文本_辅助 (状态标签, "已删除项目")
    .否则
        设置标签文本_辅助 (状态标签, "请先选择一个项目")
    .如果结束
.如果真结束


.子程序 列表框选中回调, , 公开, stdcall
.参数 列表框, 整数型
.参数 索引, 整数型
.局部变量 缓冲区, 字节集
.局部变量 长度, 整数型
.局部变量 文本, 文本型

' 获取列表项文本
长度 = 获取列表项文本 (列表框, 索引, 0, 0)
.如果真 (长度 > 0)
    缓冲区 = 取空白字节集 (长度 + 1)
    获取列表项文本 (列表框, 索引, 取变量数据地址 (缓冲区), 长度 + 1)
    文本 = 编码_Utf8到Ansi (缓冲区)
    设置标签文本_辅助 (状态标签, "选中: " + 文本 + " (索引: " + 到文本 (索引) + ")")
.如果真结束
```

## 注意事项

⚠️ **重要提示**:

1. 所有文本必须使用 UTF-8 编码的字节集
2. 支持彩色 Emoji 和多语言 Unicode 字符
3. 索引从 0 开始
4. 获取文本时需要先调用一次获取长度,再分配缓冲区
5. 多选模式下可使用 Ctrl/Shift 键配合鼠标选择
6. 当项目总高度超过列表框高度时，自动显示滚动条
7. `SetListItemText` 可直接修改已有项目的文本，无需删除重建

## 相关文档

- [组合框](combobox.md)
- [表格控件](datagridview.md)
