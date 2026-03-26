# 选项卡控件 (TabControl)

## 概述

选项卡控件用于在同一区域切换显示不同的内容页面。每个 Tab 页可关联一个内容窗口句柄，支持标题设置、动态添加/移除页面和切换回调。v3.0 新增外观定制、单页控制、内容区域、交互增强、布局位置、批量操作和状态查询共 25 个函数。

## C++ 导出函数列表

### 创建和销毁

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `CreateTabControl` | `HWND parent, int x, int y, int w, int h` | `HWND` TabControl 句柄 | 创建选项卡控件 |
| `DestroyTabControl` | `HWND hTab` | `void` | 销毁选项卡控件 |

### 页面管理

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `AddTabItem` | `HWND hTab, const uint8_t* title_bytes, int title_len, HWND contentHwnd` | `int` Tab 页索引 | contentHwnd 传 0 自动创建内容窗口 |
| `RemoveTabItem` | `HWND hTab, int index` | `BOOL` | 移除指定 Tab 页 |

### 选择操作

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `GetCurrentTabIndex` | `HWND hTab` | `int` 当前选中索引 | |
| `SelectTab` | `HWND hTab, int index` | `BOOL` | |
| `GetTabCount` | `HWND hTab` | `int` Tab 页数量 | |
| `GetTabContentWindow` | `HWND hTab, int index` | `HWND` 内容窗口句柄 | |

### 标题操作

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `GetTabTitle` | `HWND hTab, int index, uint8_t* buffer, int* bufSize` | `int` UTF-8字节数 | buffer=NULL 时返回所需大小（两次调用模式） |
| `SetTabTitle` | `HWND hTab, int index, const uint8_t* title_bytes, int title_len` | `int` 0=成功，-1=失败 | |

### 位置和大小

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `GetTabControlBounds` | `HWND hTab, int* x, int* y, int* w, int* h` | `int` 0=成功，-1=失败 | 传址输出 |
| `SetTabControlBounds` | `HWND hTab, int x, int y, int w, int h` | `int` 0=成功，-1=失败 | |

### 回调

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetTabCallback` | `HWND hTab, TAB_CALLBACK callback` | `void` | 切换回调 |

### 通用操作

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `ShowTabControl` | `HWND hTab, int visible` | `int` 0=成功，-1=失败 | 1=显示，0=隐藏 |
| `EnableTabControl` | `HWND hTab, int enable` | `int` 0=成功，-1=失败 | 1=启用，0=禁用 |
| `GetTabControlVisible` | `HWND hTab` | `int` 1=可见，0=不可见，-1=错误 | |
| `UpdateTabControlLayout` | `HWND hTab` | `void` | 窗口大小改变后调用 |

---

## v3.0 新增函数

### 外观定制（5 个）

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetTabItemSize` | `HWND hTab, int width, int height` | `int` 0=成功，-1=失败 | 设置标签页固定宽度和高度（默认 120×34），width/height 必须 > 0 |
| `SetTabFont` | `HWND hTab, const uint8_t* fontName, int fontNameLen, float fontSize` | `int` 0=成功，-1=失败 | fontName 为 UTF-8 编码，fontSize 必须 > 0（默认 Segoe UI Emoji 13.0） |
| `SetTabColors` | `HWND hTab, uint32_t selectedBg, uint32_t unselectedBg, uint32_t selectedText, uint32_t unselectedText` | `int` 0=成功，-1=失败 | 四个颜色均为 ARGB 格式（默认：白/浅灰/#409EFF/#606266） |
| `SetTabIndicatorColor` | `HWND hTab, uint32_t color` | `int` 0=成功，-1=失败 | 选中标签页底部 2px 指示条颜色（默认 0xFF409EFF） |
| `SetTabPadding` | `HWND hTab, int horizontal, int vertical` | `int` 0=成功，-1=失败 | 标签文字内边距（默认 2, 0），必须 >= 0 |

### 单个标签页控制（4 个）

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `EnableTabItem` | `HWND hTab, int index, int enabled` | `int` 0=成功，-1=失败 | 1=启用，0=禁用；禁用页以 50% 透明度渲染，不响应点击 |
| `GetTabItemEnabled` | `HWND hTab, int index` | `int` 1=启用，0=禁用，-1=错误 | |
| `ShowTabItem` | `HWND hTab, int index, int visible` | `int` 0=成功，-1=失败 | 隐藏页从标签栏消失，其他页自动填补；隐藏当前选中页自动切换 |
| `SetTabItemIcon` | `HWND hTab, int index, const uint8_t* iconBytes, int iconLen` | `int` 0=成功，-1=失败 | PNG 字节数据，显示在标题左侧（间距 4px）；传 NULL/0 清除图标 |

### 内容区域（2 个）

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetTabContentBgColor` | `HWND hTab, int index, uint32_t color` | `int` 0=成功，-1=失败 | 设置指定标签页内容窗口背景色（ARGB） |
| `SetTabContentBgColorAll` | `HWND hTab, uint32_t color` | `int` 0=成功，-1=失败 | 设置所有标签页内容窗口背景色（ARGB） |

### 交互增强（5 个）

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetTabClosable` | `HWND hTab, int closable` | `int` 0=成功，-1=失败 | 1=显示 × 关闭按钮，0=隐藏；悬停时 × 变红色背景 |
| `SetTabCloseCallback` | `HWND hTab, TAB_CLOSE_CALLBACK callback` | `int` 0=成功，-1=失败 | 点击 × 按钮时触发回调 |
| `SetTabRightClickCallback` | `HWND hTab, TAB_RIGHTCLICK_CALLBACK callback` | `int` 0=成功，-1=失败 | 右键点击标签页时触发，传入屏幕坐标 |
| `SetTabDraggable` | `HWND hTab, int draggable` | `int` 0=成功，-1=失败 | 1=可拖拽排序，拖拽时显示插入指示线 |
| `SetTabDoubleClickCallback` | `HWND hTab, TAB_DBLCLICK_CALLBACK callback` | `int` 0=成功，-1=失败 | 双击标签页时触发 |

### 布局与位置（3 个）

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `SetTabPosition` | `HWND hTab, int position` | `int` 0=成功，-1=失败 | 0=上，1=下，2=左，3=右（默认 0） |
| `SetTabAlignment` | `HWND hTab, int align` | `int` 0=成功，-1=失败 | 0=左对齐，1=居中，2=右对齐（默认 0） |
| `SetTabScrollable` | `HWND hTab, int scrollable` | `int` 0=成功，-1=失败 | 1=单行滚动模式，0=多行模式（默认 0） |

### 批量操作（4 个）

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `RemoveAllTabs` | `HWND hTab` | `int` 0=成功，-1=失败 | 清空所有标签页，销毁内容窗口，currentIndex 设为 -1 |
| `InsertTabItem` | `HWND hTab, int index, const uint8_t* title, int titleLen, HWND hContent` | `int` 实际索引，-1=失败 | index < 0 返回 -1，超出范围追加到末尾；hContent 传 0 自动创建 |
| `MoveTabItem` | `HWND hTab, int fromIndex, int toIndex` | `int` 0=成功，-1=失败 | fromIndex == toIndex 返回 0 不操作；移动选中页时 currentIndex 自动更新 |
| `GetTabIndexByTitle` | `HWND hTab, const uint8_t* titleBytes, int titleLen` | `int` 索引，-1=未找到 | 精确匹配，区分大小写，返回第一个匹配的索引 |

### 状态查询（2 个）

| 函数名 | 参数 | 返回值 | 说明 |
|--------|------|--------|------|
| `GetTabEnabled` | `HWND hTab` | `int` 1=启用，0=禁用，-1=错误 | 获取整个 TabControl 的启用状态（通过 IsWindowEnabled） |
| `IsTabItemSelected` | `HWND hTab, int index` | `int` 1=选中，0=未选中，-1=错误 | 比较 index 与 currentIndex |

---

## 回调签名

### TAB_CALLBACK - 切换回调

```c++
void __stdcall TabCallback(HWND hTabControl, int newIndex);
```

### TAB_CLOSE_CALLBACK - 关闭回调（v3.0 新增）

```c++
void __stdcall TabCloseCallback(HWND hTabControl, int index);
```

点击 × 关闭按钮时触发。需先调用 `SetTabClosable(hTab, 1)` 启用关闭按钮。

### TAB_RIGHTCLICK_CALLBACK - 右键回调（v3.0 新增）

```c++
void __stdcall TabRightClickCallback(HWND hTabControl, int index, int screenX, int screenY);
```

右键点击标签页时触发，传入鼠标屏幕坐标，可直接用于弹出菜单定位。点击位置不在任何标签页上时不触发。

### TAB_DBLCLICK_CALLBACK - 双击回调（v3.0 新增）

```c++
void __stdcall TabDblClickCallback(HWND hTabControl, int index);
```

双击标签页时触发，可用于实现双击重命名等交互。

---

## 默认值参考

| 属性 | 默认值 | 说明 |
|------|--------|------|
| tabWidth | 120 | 标签页宽度 |
| tabHeight | 34 | 标签页高度 |
| fontName | Segoe UI Emoji | 字体名称 |
| fontSize | 13.0 | 字号 |
| selectedBgColor | 0xFFFFFFFF | 选中背景色（白色） |
| unselectedBgColor | 0xFFF5F7FA | 未选中背景色（浅灰） |
| selectedTextColor | 0xFF409EFF | 选中文字色（蓝色） |
| unselectedTextColor | 0xFF606266 | 未选中文字色（深灰） |
| indicatorColor | 0xFF409EFF | 指示条颜色 |
| paddingH | 2 | 水平内边距 |
| paddingV | 0 | 垂直内边距 |
| closable | false | 关闭按钮 |
| draggable | false | 拖拽排序 |
| scrollable | false | 滚动模式 |
| tabPosition | 0 | 标签栏位置（上） |
| tabAlignment | 0 | 标签对齐（左） |

---

## 注意事项

- `AddTabItem` / `InsertTabItem` 的 `contentHwnd` 参数可传 0，自动创建空白内容窗口
- 标题使用 UTF-8 编码字节集，支持 Emoji
- `GetTabTitle` 采用两次调用模式：第一次 buffer 传 NULL 获取所需大小，第二次传实际缓冲区
- `ShowTabControl` 和 `EnableTabControl` 的参数为 int 类型（1=显示/启用，0=隐藏/禁用）
- 窗口大小改变后应调用 `UpdateTabControlLayout` 更新布局
- `GetTabControlBounds` 输出参数在易语言中需使用"传址"方式传参
- 移除 Tab 页会销毁对应的内容窗口（如果是自动创建的）
- 不再使用时应调用 `DestroyTabControl` 释放资源
- 禁用的标签页（`EnableTabItem`）以 50% 透明度渲染，点击不响应
- 隐藏的标签页（`ShowTabItem`）从标签栏消失但数据保留，可随时恢复显示
- 关闭按钮需先 `SetTabClosable` 启用，再 `SetTabCloseCallback` 设置回调
- 拖拽完成后被拖拽的标签页保持选中状态
- `InsertTabItem` 在当前选中页之前插入时，currentIndex 自动 +1
- `MoveTabItem` 移动选中页时，currentIndex 自动更新为新位置
- 所有新增字段的默认值保证向后兼容，现有 TabControl 行为不变
