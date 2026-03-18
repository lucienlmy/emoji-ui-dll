# 树形框控件 (TreeView)

## 概述

树形框控件用于显示层次结构数据，支持 Emoji 图标、复选框、拖放排序、键盘导航等功能。采用 Direct2D 渲染引擎和 Element UI 设计风格，完美支持彩色 Emoji。

## C++ 导出函数列表

### 创建

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `CreateTreeView` | `HWND hParent, int x, int y, int width, int height, UINT32 bg_color, UINT32 text_color, int context` | `HWND` 树形框句柄，失败返回 0 |

### 节点管理

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `AddRootNode` | `HWND hTV, const uint8_t* text_bytes, int text_len, const uint8_t* icon_bytes, int icon_len` | `int` 节点ID |
| `AddChildNode` | `HWND hTV, int parent_node_id, const uint8_t* text_bytes, int text_len, const uint8_t* icon_bytes, int icon_len` | `int` 节点ID |
| `RemoveNode` | `HWND hTV, int node_id` | `BOOL` |
| `ClearTree` | `HWND hTV` | `BOOL` |

### 展开/折叠

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `ExpandNode` | `HWND hTV, int node_id` | `BOOL` |
| `CollapseNode` | `HWND hTV, int node_id` | `BOOL` |
| `ExpandAll` | `HWND hTV` | `BOOL` |
| `CollapseAll` | `HWND hTV` | `BOOL` |
| `IsNodeExpanded` | `HWND hTV, int node_id` | `BOOL` |

### 节点选择

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `SetSelectedNode` | `HWND hTV, int node_id` | `BOOL` |
| `GetSelectedNode` | `HWND hTV` | `int` 选中节点ID |

### 节点文本和图标

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `SetNodeText` | `HWND hTV, int node_id, const uint8_t* text_bytes, int text_len` | `BOOL` |
| `GetNodeText` | `HWND hTV, int node_id, uint8_t* buffer, int buffer_size` | `int` UTF-8字节数 |
| `SetNodeIcon` | `HWND hTV, int node_id, const uint8_t* icon_bytes, int icon_len` | `BOOL` |
| `GetNodeIcon` | `HWND hTV, int node_id, uint8_t* buffer, int buffer_size` | `int` UTF-8字节数 |

### 节点颜色和状态

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `SetNodeForeColor` | `HWND hTV, int node_id, UINT32 color` | `BOOL` |
| `SetNodeBackColor` | `HWND hTV, int node_id, UINT32 color` | `BOOL` |
| `SetNodeEnabled` | `HWND hTV, int node_id, BOOL enabled` | `BOOL` |
| `IsNodeEnabled` | `HWND hTV, int node_id` | `BOOL` |

### 复选框

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `SetNodeCheckBox` | `HWND hTV, int node_id, BOOL show` | `BOOL` |
| `SetNodeChecked` | `HWND hTV, int node_id, BOOL checked` | `BOOL` |
| `GetNodeChecked` | `HWND hTV, int node_id` | `BOOL` |

### 节点查找和关系

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `FindNodeByText` | `HWND hTV, const uint8_t* text_bytes, int text_len` | `int` 节点ID，未找到返回 0 |
| `GetNodeParent` | `HWND hTV, int node_id` | `int` 父节点ID |
| `GetNodeChildCount` | `HWND hTV, int node_id` | `int` 子节点数 |
| `GetNodeChildren` | `HWND hTV, int node_id, uint8_t* buffer, int buffer_size` | `int` 数据长度 |
| `GetNodeLevel` | `HWND hTV, int node_id` | `int` 层级深度 |

### 滚动控制

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `ScrollToNode` | `HWND hTV, int node_id` | `BOOL` |
| `SetTreeViewScrollPos` | `HWND hTV, int position` | `BOOL` |
| `GetTreeViewScrollPos` | `HWND hTV` | `int` 滚动位置 |

### 拖放

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `EnableTreeViewDragDrop` | `HWND hTV, BOOL enable` | `BOOL` |

### 回调

| 函数名 | 参数 | 返回值 |
|--------|------|--------|
| `SetTreeViewCallback` | `HWND hTV, int callback_type, void* callback_function` | `BOOL` |

## 回调类型及签名

通过 `SetTreeViewCallback` 的 `callback_type` 参数指定回调类型：

| callback_type | 说明 | 回调签名 |
|---------------|------|---------|
| 1 | 节点被选中 | `void(int node_id, int context)` |
| 2 | 节点被展开 | `void(int node_id, int context)` |
| 3 | 节点被折叠 | `void(int node_id, int context)` |
| 4 | 节点被双击 | `void(int node_id, int context)` |
| 5 | 节点被右键点击 | `void(int node_id, int x, int y, int context)` |
| 6 | 节点文本改变 | `void(int node_id, const char* text, int text_len, int context)` |
| 7 | 节点复选框改变 | `void(int node_id, BOOL checked, int context)` |
| 8 | 节点被移动(拖放) | `void(int node_id, int new_parent_id, int new_index, int context)` |

## 键盘快捷键

| 按键 | 功能 |
|------|------|
| ↑/↓ | 上下移动选中节点 |
| ←/→ | 折叠/展开节点 |
| Home | 跳到第一个节点 |
| End | 跳到最后一个节点 |
| PageUp/PageDown | 翻页 |
| Space | 切换复选框状态 |
| Enter | 展开/折叠节点 |

## 注意事项

- 创建时 `context` 参数可传 0，会在所有回调中原样传回，用于区分多个树形框实例
- 节点图标支持 Emoji（UTF-8 编码），如 `📁`、`📄` 等
- `GetNodeText`/`GetNodeIcon` 采用两次调用模式：第一次 buffer 传 0 获取所需大小
- 大量节点时建议使用动态加载（展开时才加载子节点）
- 拖放功能会增加内存占用，不需要时应通过 `EnableTreeViewDragDrop(hTV, FALSE)` 禁用
- 颜色使用 ARGB 格式
- 渲染引擎为 Direct2D + DirectWrite
