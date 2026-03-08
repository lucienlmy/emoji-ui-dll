# UI控件扩展设计文档

## 概述

本设计文档描述了emoji_window DLL库的UI控件扩展方案。我们将添加11个新控件类型和功能模块，所有控件都将使用Direct2D/DirectWrite进行自绘，支持Unicode，并遵循Element UI设计规范。

## 架构设计

### 整体架构

```
emoji_window.dll
├── 核心系统
│   ├── D2D1Factory (全局单例)
│   ├── DirectWrite Factory (全局单例)
│   ├── 窗口管理 (g_windows map)
│   └── 消息循环 (run_message_loop)
├── 现有控件
│   ├── EmojiButton (自绘按钮)
│   ├── EditBox (编辑框)
│   ├── Label (标签)
│   ├── TabControl (选项卡)
│   └── MessageBox (消息框)
└── 新增控件 (本次扩展)
    ├── CheckBox (复选框)
    ├── RadioButton (单选按钮)
    ├── ProgressBar (进度条)
    ├── ListBox (列表框)
    ├── ComboBox (组合框)
    ├── HotKeyControl (热键控件)
    ├── PictureBox (图片框)
    ├── GroupBox (分组框)
    ├── LayoutManager (布局管理器)
    ├── ThemeManager (主题系统)
    └── EventSystem (事件系统扩展)
```

### 设计原则

1. **一致性**: 所有新控件遵循现有代码的设计模式
2. **可扩展性**: 使用State结构和全局map管理控件状态
3. **性能**: 使用硬件加速的D2D1渲染
4. **易用性**: 提供简洁的C API供易语言调用
5. **可维护性**: 代码结构清晰，注释完整

## 组件和接口

### 1. 复选框控件 (CheckBox)

#### 数据结构

```cpp
struct CheckBoxState {
    HWND hwnd;                      // 控件句柄
    HWND parent;                    // 父窗口句柄
    int id;                         // 控件ID
    int x, y, width, height;        // 位置和尺寸
    std::wstring text;              // 显示文本
    bool checked;                   // 选中状态
    bool enabled;                   // 启用状态
    bool hovered;                   // 悬停状态
    bool pressed;                   // 按下状态
    UINT32 fg_color;                // 前景色
    UINT32 bg_color;                // 背景色
    UINT32 check_color;             // 勾选标记颜色
    FontStyle font;                 // 字体样式
};

// 全局管理
extern std::map<HWND, CheckBoxState*> g_checkboxes;
```

#### API接口

```cpp
// 创建复选框
__declspec(dllexport) HWND __stdcall CreateCheckBox(
    HWND hParent,
    int x, int y, int width, int height,
    const unsigned char* text_bytes,
    int text_len,
    BOOL checked,
    UINT32 fg_color,
    UINT32 bg_color
);

// 获取选中状态
__declspec(dllexport) BOOL __stdcall GetCheckBoxState(HWND hCheckBox);

// 设置选中状态
__declspec(dllexport) void __stdcall SetCheckBoxState(HWND hCheckBox, BOOL checked);

// 设置复选框回调
typedef void (__stdcall *CheckBoxCallback)(HWND hCheckBox, BOOL checked);
__declspec(dllexport) void __stdcall SetCheckBoxCallback(CheckBoxCallback callback);
```

#### 绘制逻辑

```cpp
void DrawCheckBox(ID2D1HwndRenderTarget* rt, IDWriteFactory* factory, CheckBoxState* state) {
    // 1. 绘制复选框背景（圆角矩形，4px圆角）
    // 2. 根据状态绘制边框（正常/悬停/按下/禁用）
    // 3. 如果选中，绘制勾选标记（使用路径几何）
    // 4. 绘制文本标签（右侧，垂直居中）
    // 5. 应用Element UI配色方案
}
```

### 2. 单选按钮控件 (RadioButton)

#### 数据结构

```cpp
struct RadioButtonState {
    HWND hwnd;
    HWND parent;
    int id;
    int group_id;                   // 分组ID，同组互斥
    int x, y, width, height;
    std::wstring text;
    bool checked;
    bool enabled;
    bool hovered;
    bool pressed;
    UINT32 fg_color;
    UINT32 bg_color;
    UINT32 dot_color;               // 圆点颜色
    FontStyle font;
};

extern std::map<HWND, RadioButtonState*> g_radiobuttons;
extern std::map<int, std::vector<HWND>> g_radio_groups;  // 分组管理
```

#### API接口

```cpp
__declspec(dllexport) HWND __stdcall CreateRadioButton(
    HWND hParent,
    int x, int y, int width, int height,
    const unsigned char* text_bytes,
    int text_len,
    int group_id,
    BOOL checked,
    UINT32 fg_color,
    UINT32 bg_color
);

__declspec(dllexport) BOOL __stdcall GetRadioButtonState(HWND hRadioButton);
__declspec(dllexport) void __stdcall SetRadioButtonState(HWND hRadioButton, BOOL checked);

typedef void (__stdcall *RadioButtonCallback)(HWND hRadioButton, int group_id, BOOL checked);
__declspec(dllexport) void __stdcall SetRadioButtonCallback(RadioButtonCallback callback);
```

### 3. 进度条控件 (ProgressBar)

#### 数据结构

```cpp
struct ProgressBarState {
    HWND hwnd;
    HWND parent;
    int id;
    int x, y, width, height;
    float value;                    // 当前值 (0.0 - 100.0)
    float target_value;             // 目标值（用于动画）
    bool indeterminate;             // 不确定模式
    float animation_offset;         // 动画偏移量
    UINT32 fg_color;                // 进度条颜色
    UINT32 bg_color;                // 背景色
    bool show_text;                 // 是否显示百分比文本
};

extern std::map<HWND, ProgressBarState*> g_progressbars;
```

#### API接口

```cpp
__declspec(dllexport) HWND __stdcall CreateProgressBar(
    HWND hParent,
    int x, int y, int width, int height,
    UINT32 fg_color,
    UINT32 bg_color
);

__declspec(dllexport) void __stdcall SetProgressValue(HWND hProgressBar, float value);
__declspec(dllexport) float __stdcall GetProgressValue(HWND hProgressBar);
__declspec(dllexport) void __stdcall SetProgressIndeterminate(HWND hProgressBar, BOOL indeterminate);
```

### 4. 列表框控件 (ListBox)

#### 数据结构

```cpp
struct ListBoxItem {
    std::wstring text;
    int id;
    void* user_data;                // 用户自定义数据
};

struct ListBoxState {
    HWND hwnd;
    HWND parent;
    int id;
    int x, y, width, height;
    std::vector<ListBoxItem> items;
    int selected_index;             // 当前选中项
    int hovered_index;              // 悬停项
    int scroll_offset;              // 滚动偏移量
    int item_height;                // 项目高度
    bool multi_select;              // 多选模式
    std::vector<int> selected_indices;  // 多选时的选中项
    UINT32 fg_color;
    UINT32 bg_color;
    UINT32 select_color;            // 选中背景色
    UINT32 hover_color;             // 悬停背景色
    FontStyle font;
};

extern std::map<HWND, ListBoxState*> g_listboxes;
```

#### API接口

```cpp
__declspec(dllexport) HWND __stdcall CreateListBox(
    HWND hParent,
    int x, int y, int width, int height,
    BOOL multi_select,
    UINT32 fg_color,
    UINT32 bg_color
);

__declspec(dllexport) int __stdcall AddListItem(
    HWND hListBox,
    const unsigned char* text_bytes,
    int text_len
);

__declspec(dllexport) void __stdcall RemoveListItem(HWND hListBox, int index);
__declspec(dllexport) void __stdcall ClearListBox(HWND hListBox);
__declspec(dllexport) int __stdcall GetSelectedIndex(HWND hListBox);
__declspec(dllexport) void __stdcall SetSelectedIndex(HWND hListBox, int index);

typedef void (__stdcall *ListBoxCallback)(HWND hListBox, int index);
__declspec(dllexport) void __stdcall SetListBoxCallback(ListBoxCallback callback);
```

### 5. 组合框控件 (ComboBox)

#### 数据结构

```cpp
struct ComboBoxState {
    HWND hwnd;                      // 主控件句柄
    HWND parent;
    HWND edit_hwnd;                 // 编辑框句柄
    HWND dropdown_hwnd;             // 下拉列表窗口句柄
    int id;
    int x, y, int width, height;
    std::vector<std::wstring> items;
    int selected_index;
    bool dropdown_visible;
    bool readonly;                  // 只读模式
    UINT32 fg_color;
    UINT32 bg_color;
    FontStyle font;
};

extern std::map<HWND, ComboBoxState*> g_comboboxes;
```

#### API接口

```cpp
__declspec(dllexport) HWND __stdcall CreateComboBox(
    HWND hParent,
    int x, int y, int width, int height,
    BOOL readonly,
    UINT32 fg_color,
    UINT32 bg_color
);

__declspec(dllexport) int __stdcall AddComboItem(
    HWND hComboBox,
    const unsigned char* text_bytes,
    int text_len
);

__declspec(dllexport) int __stdcall GetComboSelectedIndex(HWND hComboBox);
__declspec(dllexport) void __stdcall SetComboSelectedIndex(HWND hComboBox, int index);

typedef void (__stdcall *ComboBoxCallback)(HWND hComboBox, int index);
__declspec(dllexport) void __stdcall SetComboBoxCallback(ComboBoxCallback callback);
```

### 6. 热键控件 (HotKeyControl)

#### 数据结构

```cpp
struct HotKeyState {
    HWND hwnd;
    HWND parent;
    int id;
    int x, y, width, height;
    int vk_code;                    // 虚拟键码
    int modifiers;                  // 修饰键 (Ctrl=1, Shift=2, Alt=4)
    std::wstring display_text;      // 显示文本
    bool capturing;                 // 是否正在捕获
    UINT32 fg_color;
    UINT32 bg_color;
    FontStyle font;
};

extern std::map<HWND, HotKeyState*> g_hotkeys;
```

#### API接口

```cpp
__declspec(dllexport) HWND __stdcall CreateHotKeyControl(
    HWND hParent,
    int x, int y, int width, int height,
    UINT32 fg_color,
    UINT32 bg_color
);

__declspec(dllexport) void __stdcall GetHotKey(HWND hHotKey, int* vk_code, int* modifiers);
__declspec(dllexport) void __stdcall SetHotKey(HWND hHotKey, int vk_code, int modifiers);

typedef void (__stdcall *HotKeyCallback)(HWND hHotKey, int vk_code, int modifiers);
__declspec(dllexport) void __stdcall SetHotKeyCallback(HotKeyCallback callback);
```

### 7. 图片框控件 (PictureBox)

#### 数据结构

```cpp
enum ImageScaleMode {
    SCALE_NONE = 0,         // 不缩放
    SCALE_STRETCH = 1,      // 拉伸填充
    SCALE_FIT = 2,          // 等比缩放适应
    SCALE_CENTER = 3        // 居中显示
};

struct PictureBoxState {
    HWND hwnd;
    HWND parent;
    int id;
    int x, y, width, height;
    ID2D1Bitmap* bitmap;            // D2D1位图
    IWICBitmapSource* wic_source;   // WIC位图源
    ImageScaleMode scale_mode;
    float opacity;                  // 透明度 (0.0 - 1.0)
    UINT32 bg_color;
};

extern std::map<HWND, PictureBoxState*> g_pictureboxes;
```

#### API接口

```cpp
__declspec(dllexport) HWND __stdcall CreatePictureBox(
    HWND hParent,
    int x, int y, int width, int height,
    int scale_mode,
    UINT32 bg_color
);

__declspec(dllexport) BOOL __stdcall LoadImageFromFile(
    HWND hPictureBox,
    const unsigned char* file_path_bytes,
    int path_len
);

__declspec(dllexport) BOOL __stdcall LoadImageFromMemory(
    HWND hPictureBox,
    const unsigned char* image_data,
    int data_len
);

__declspec(dllexport) void __stdcall ClearImage(HWND hPictureBox);
__declspec(dllexport) void __stdcall SetImageOpacity(HWND hPictureBox, float opacity);
```

### 8. 分组框控件 (GroupBox)

#### 数据结构

```cpp
struct GroupBoxState {
    HWND hwnd;
    HWND parent;
    int id;
    int x, y, width, height;
    std::wstring title;
    std::vector<HWND> children;     // 子控件列表
    UINT32 border_color;
    UINT32 title_color;
    UINT32 bg_color;
    FontStyle font;
};

extern std::map<HWND, GroupBoxState*> g_groupboxes;
```

#### API接口

```cpp
__declspec(dllexport) HWND __stdcall CreateGroupBox(
    HWND hParent,
    int x, int y, int width, int height,
    const unsigned char* title_bytes,
    int title_len,
    UINT32 border_color,
    UINT32 bg_color
);

__declspec(dllexport) void __stdcall AddChildToGroup(HWND hGroupBox, HWND hChild);
__declspec(dllexport) void __stdcall RemoveChildFromGroup(HWND hGroupBox, HWND hChild);
```

### 9. 事件系统扩展

#### 回调类型定义

```cpp
// 鼠标事件
typedef void (__stdcall *MouseEnterCallback)(HWND hwnd);
typedef void (__stdcall *MouseLeaveCallback)(HWND hwnd);
typedef void (__stdcall *DoubleClickCallback)(HWND hwnd, int x, int y);
typedef void (__stdcall *RightClickCallback)(HWND hwnd, int x, int y);

// 焦点事件
typedef void (__stdcall *FocusCallback)(HWND hwnd);
typedef void (__stdcall *BlurCallback)(HWND hwnd);

// 键盘事件
typedef void (__stdcall *KeyDownCallback)(HWND hwnd, int vk_code, int modifiers);
typedef void (__stdcall *KeyUpCallback)(HWND hwnd, int vk_code, int modifiers);
typedef void (__stdcall *CharCallback)(HWND hwnd, wchar_t character);

// 值改变事件
typedef void (__stdcall *ValueChangedCallback)(HWND hwnd);
```

#### API接口

```cpp
__declspec(dllexport) void __stdcall SetMouseEnterCallback(HWND hwnd, MouseEnterCallback callback);
__declspec(dllexport) void __stdcall SetMouseLeaveCallback(HWND hwnd, MouseLeaveCallback callback);
__declspec(dllexport) void __stdcall SetDoubleClickCallback(HWND hwnd, DoubleClickCallback callback);
__declspec(dllexport) void __stdcall SetRightClickCallback(HWND hwnd, RightClickCallback callback);
__declspec(dllexport) void __stdcall SetFocusCallback(HWND hwnd, FocusCallback callback);
__declspec(dllexport) void __stdcall SetBlurCallback(HWND hwnd, BlurCallback callback);
__declspec(dllexport) void __stdcall SetKeyDownCallback(HWND hwnd, KeyDownCallback callback);
__declspec(dllexport) void __stdcall SetKeyUpCallback(HWND hwnd, KeyUpCallback callback);
__declspec(dllexport) void __stdcall SetCharCallback(HWND hwnd, CharCallback callback);
__declspec(dllexport) void __stdcall SetValueChangedCallback(HWND hwnd, ValueChangedCallback callback);
```

### 10. 布局管理器

#### 数据结构

```cpp
enum LayoutType {
    LAYOUT_NONE = 0,
    LAYOUT_FLOW_HORIZONTAL = 1,     // 水平流式布局
    LAYOUT_FLOW_VERTICAL = 2,       // 垂直流式布局
    LAYOUT_GRID = 3,                // 网格布局
    LAYOUT_DOCK = 4                 // 停靠布局
};

enum DockPosition {
    DOCK_NONE = 0,
    DOCK_TOP = 1,
    DOCK_BOTTOM = 2,
    DOCK_LEFT = 3,
    DOCK_RIGHT = 4,
    DOCK_FILL = 5
};

struct LayoutProperties {
    int margin_left, margin_top, margin_right, margin_bottom;
    int padding;
    DockPosition dock;
    bool stretch_horizontal;
    bool stretch_vertical;
};

struct LayoutManager {
    HWND parent_hwnd;
    LayoutType type;
    int rows, columns;              // 网格布局参数
    int spacing;                    // 控件间距
    std::map<HWND, LayoutProperties> control_props;
};

extern std::map<HWND, LayoutManager*> g_layout_managers;
```

#### API接口

```cpp
__declspec(dllexport) void __stdcall SetLayoutManager(
    HWND hParent,
    int layout_type,
    int rows,
    int columns,
    int spacing
);

__declspec(dllexport) void __stdcall SetControlLayoutProps(
    HWND hControl,
    int margin_left, int margin_top, int margin_right, int margin_bottom,
    int dock_position,
    BOOL stretch_horizontal,
    BOOL stretch_vertical
);

__declspec(dllexport) void __stdcall UpdateLayout(HWND hParent);
```

### 11. 主题系统

#### 数据结构

```cpp
struct ThemeColors {
    UINT32 primary;         // 主色 #409EFF
    UINT32 success;         // 成功 #67C23A
    UINT32 warning;         // 警告 #E6A23C
    UINT32 danger;          // 危险 #F56C6C
    UINT32 info;            // 信息 #909399
    UINT32 text_primary;    // 主要文本 #303133
    UINT32 text_regular;    // 常规文本 #606266
    UINT32 text_secondary;  // 次要文本 #909399
    UINT32 text_placeholder;// 占位文本 #C0C4CC
    UINT32 border_base;     // 基础边框 #DCDFE6
    UINT32 border_light;    // 浅色边框 #E4E7ED
    UINT32 border_lighter;  // 更浅边框 #EBEEF5
    UINT32 border_extra_light; // 极浅边框 #F2F6FC
    UINT32 background;      // 背景色 #FFFFFF
    UINT32 background_light;// 浅色背景 #F5F7FA
};

struct ThemeFonts {
    std::wstring title_font;        // 标题字体
    std::wstring body_font;         // 正文字体
    std::wstring mono_font;         // 等宽字体
    int title_size;
    int body_size;
    int small_size;
};

struct ThemeSizes {
    float border_radius;            // 圆角半径
    float border_width;             // 边框宽度
    int control_height;             // 控件高度
    int spacing_small;              // 小间距
    int spacing_medium;             // 中间距
    int spacing_large;              // 大间距
};

struct Theme {
    std::wstring name;
    bool dark_mode;
    ThemeColors colors;
    ThemeFonts fonts;
    ThemeSizes sizes;
};

extern Theme* g_current_theme;
```

#### API接口

```cpp
__declspec(dllexport) BOOL __stdcall LoadThemeFromFile(
    const unsigned char* file_path_bytes,
    int path_len
);

__declspec(dllexport) BOOL __stdcall LoadThemeFromJSON(
    const unsigned char* json_bytes,
    int json_len
);

__declspec(dllexport) void __stdcall SetTheme(const char* theme_name);
__declspec(dllexport) void __stdcall SetDarkMode(BOOL dark_mode);
__declspec(dllexport) UINT32 __stdcall GetThemeColor(const char* color_name);
```

## 数据模型

### 控件状态管理

所有控件状态都存储在全局map中：

```cpp
std::map<HWND, CheckBoxState*> g_checkboxes;
std::map<HWND, RadioButtonState*> g_radiobuttons;
std::map<HWND, ProgressBarState*> g_progressbars;
std::map<HWND, ListBoxState*> g_listboxes;
std::map<HWND, ComboBoxState*> g_comboboxes;
std::map<HWND, HotKeyState*> g_hotkeys;
std::map<HWND, PictureBoxState*> g_pictureboxes;
std::map<HWND, GroupBoxState*> g_groupboxes;
```

### 资源管理

- 所有D2D1资源在控件销毁时释放
- 所有WIC资源在图片更换或控件销毁时释放
- 所有HBRUSH在控件销毁时删除
- 所有子类化在WM_NCDESTROY时移除

## 错误处理

1. 所有API函数返回值表示成功/失败
2. 无效句柄检查：`if (!hwnd || !IsWindow(hwnd)) return;`
3. 空指针检查：`if (!state) return;`
4. 资源创建失败检查
5. 文件加载失败返回FALSE

## 测试策略

### 单元测试

- 测试每个控件的创建和销毁
- 测试状态获取和设置函数
- 测试回调函数触发
- 测试Unicode文本显示

### 集成测试

- 测试多个控件同时使用
- 测试布局管理器
- 测试主题切换
- 测试事件系统

### 性能测试

- 测试大量控件的渲染性能
- 测试列表框滚动性能
- 测试进度条动画流畅度

## 正确性属性

*属性是系统应该在所有有效执行中保持为真的特征或行为——本质上是关于系统应该做什么的形式化陈述。属性作为人类可读规范和机器可验证正确性保证之间的桥梁。*

### 属性 1: 控件创建后句柄有效性
*对于任何*控件创建函数，如果创建成功返回非NULL句柄，则该句柄必须是有效的Windows窗口句柄
**验证: 需求 1.1, 2.1, 3.1, 4.1, 5.1, 6.1, 7.1, 9.1**

### 属性 2: 状态设置后立即可获取
*对于任何*控件状态设置函数，设置状态后立即调用获取函数应返回相同的值
**验证: 需求 1.8, 2.1, 3.8, 4.9**

### 属性 3: 回调函数触发时机正确
*对于任何*用户交互事件，当且仅当事件发生时，对应的回调函数应被触发一次
**验证: 需求 1.2, 2.2, 8.1-8.10**

### 属性 4: Unicode文本往返一致性
*对于任何*UTF-8编码的文本输入，经过Utf8ToWide转换后再转换回UTF-8应得到相同的字节序列
**验证: 需求 1.7, 2.7, 4.10, 7.1**

### 属性 5: 单选按钮分组互斥性
*对于任何*单选按钮分组，同一时刻最多只有一个按钮处于选中状态
**验证: 需求 2.2, 2.5**

### 属性 6: 进度条值范围约束
*对于任何*进度条，其值必须始终在0到100之间（包含边界）
**验证: 需求 3.2, 3.8**

### 属性 7: 列表框索引有效性
*对于任何*列表框操作，选中索引必须在-1（无选中）到项目数量-1之间
**验证: 需求 4.9**

### 属性 8: 图片加载失败不崩溃
*对于任何*无效的图片文件或内存数据，LoadImage函数应返回FALSE且不导致程序崩溃
**验证: 需求 7.6**

### 属性 9: 布局更新保持控件可见性
*对于任何*布局更新操作，所有启用且未隐藏的控件应保持在父窗口的可见区域内
**验证: 需求 10.5**

### 属性 10: 主题切换不丢失控件状态
*对于任何*主题切换操作，所有控件的状态（选中、文本、值等）应保持不变
**验证: 需求 11.6**

### 属性 11: 资源释放完整性
*对于任何*控件销毁操作，所有关联的D2D1、WIC、GDI资源必须被正确释放
**验证: 技术约束 7**

### 属性 12: 控件禁用时不响应交互
*对于任何*处于禁用状态的控件，所有用户交互事件（点击、键盘输入等）应被忽略
**验证: 需求 1.5, 技术约束 8**

## 实现计划

详见 tasks.md 文件。
