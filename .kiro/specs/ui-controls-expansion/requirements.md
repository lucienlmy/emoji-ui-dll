# UI控件扩展需求文档

## 简介

本项目旨在为现有的emoji_window DLL库扩展更多UI控件，以提供完整的Windows窗口控件系统。所有控件必须支持Unicode，使用Direct2D/DirectWrite进行自绘，并保持与现有代码架构的一致性。

## 术语表

- **DLL**: 动态链接库，本项目的emoji_window.dll
- **D2D1**: Direct2D图形API，用于硬件加速的2D图形渲染
- **DirectWrite**: Windows文本渲染API，支持Unicode和复杂文本布局
- **Unicode**: 统一字符编码标准，支持多语言文本
- **UTF-8**: Unicode的8位变长编码方式
- **State结构**: 控件状态管理结构体，存储控件的所有属性和状态
- **Callback**: 回调函数，用于事件通知
- **易语言**: 中文编程语言，本项目的主要调用方
- **HWND**: Windows窗口句柄
- **WM_**: Windows消息前缀
- **Element UI**: 流行的UI设计规范，本项目的视觉风格参考

## 需求

### 需求 1: 复选框控件

**用户故事**: 作为开发者，我希望创建复选框控件，以便用户可以进行多选操作。

#### 验收标准

1. WHEN 开发者调用CreateCheckBox函数 THEN 系统应创建一个复选框控件并返回句柄
2. WHEN 用户点击复选框 THEN 系统应切换选中状态并触发回调函数
3. WHEN 复选框处于选中状态 THEN 系统应显示勾选标记（使用D2D1绘制）
4. WHEN 复选框处于未选中状态 THEN 系统应显示空白框
5. WHEN 复选框处于禁用状态 THEN 系统应显示灰色样式且不响应点击
6. WHEN 鼠标悬停在复选框上 THEN 系统应显示悬停效果（Element UI风格）
7. WHEN 设置复选框文本 THEN 系统应在复选框右侧显示Unicode文本
8. WHEN 调用GetCheckBoxState函数 THEN 系统应返回当前选中状态（0=未选中，1=选中）

### 需求 2: 单选按钮控件

**用户故事**: 作为开发者，我希望创建单选按钮控件，以便用户可以在多个选项中选择一个。

#### 验收标准

1. WHEN 开发者调用CreateRadioButton函数 THEN 系统应创建一个单选按钮控件并返回句柄
2. WHEN 用户点击单选按钮 THEN 系统应选中该按钮并取消同组其他按钮的选中状态
3. WHEN 单选按钮处于选中状态 THEN 系统应在圆形内显示实心圆点
4. WHEN 单选按钮处于未选中状态 THEN 系统应显示空心圆
5. WHEN 设置单选按钮分组ID THEN 系统应确保同组内只有一个按钮被选中
6. WHEN 单选按钮状态改变 THEN 系统应触发回调函数通知状态变化
7. WHEN 设置单选按钮文本 THEN 系统应在按钮右侧显示Unicode文本
8. WHEN 鼠标悬停在单选按钮上 THEN 系统应显示悬停效果

### 需求 3: 进度条控件

**用户故事**: 作为开发者，我希望创建进度条控件，以便向用户显示任务进度。

#### 验收标准

1. WHEN 开发者调用CreateProgressBar函数 THEN 系统应创建一个进度条控件并返回句柄
2. WHEN 调用SetProgressValue函数 THEN 系统应更新进度条的当前值（0-100）
3. WHEN 进度条值改变 THEN 系统应平滑动画过渡到新值
4. WHEN 进度条绘制 THEN 系统应使用Element UI风格（圆角、渐变色）
5. WHEN 设置进度条颜色 THEN 系统应支持自定义前景色和背景色
6. WHEN 进度条达到100% THEN 系统应显示完成状态
7. WHEN 设置进度条为不确定模式 THEN 系统应显示循环动画效果
8. WHEN 获取进度条值 THEN 系统应返回当前进度百分比

### 需求 4: 列表框控件

**用户故事**: 作为开发者，我希望创建列表框控件，以便用户可以从列表中选择项目。

#### 验收标准

1. WHEN 开发者调用CreateListBox函数 THEN 系统应创建一个列表框控件并返回句柄
2. WHEN 调用AddListItem函数 THEN 系统应添加新项目到列表末尾
3. WHEN 用户点击列表项 THEN 系统应选中该项并触发回调函数
4. WHEN 列表项超出可见区域 THEN 系统应显示滚动条
5. WHEN 用户滚动列表 THEN 系统应平滑滚动并更新可见项目
6. WHEN 列表项被选中 THEN 系统应显示高亮背景色
7. WHEN 鼠标悬停在列表项上 THEN 系统应显示悬停效果
8. WHEN 调用RemoveListItem函数 THEN 系统应从列表中移除指定项目
9. WHEN 调用GetSelectedIndex函数 THEN 系统应返回当前选中项的索引
10. WHEN 列表项包含Unicode文本 THEN 系统应正确显示多语言文本

### 需求 5: 组合框控件

**用户故事**: 作为开发者，我希望创建组合框控件，以便用户可以从下拉列表中选择或输入文本。

#### 验收标准

1. WHEN 开发者调用CreateComboBox函数 THEN 系统应创建一个组合框控件并返回句柄
2. WHEN 用户点击下拉按钮 THEN 系统应显示下拉列表窗口
3. WHEN 用户选择下拉项 THEN 系统应更新编辑框文本并关闭下拉列表
4. WHEN 用户在编辑框输入文本 THEN 系统应支持自动完成功能（可选）
5. WHEN 下拉列表显示 THEN 系统应在组合框下方创建浮动窗口
6. WHEN 用户点击组合框外部 THEN 系统应关闭下拉列表
7. WHEN 调用AddComboItem函数 THEN 系统应添加新项目到下拉列表
8. WHEN 设置组合框为只读模式 THEN 系统应禁用文本输入功能

### 需求 6: 热键控件

**用户故事**: 作为开发者，我希望创建热键控件，以便用户可以设置键盘快捷键。

#### 验收标准

1. WHEN 开发者调用CreateHotKeyControl函数 THEN 系统应创建一个热键控件并返回句柄
2. WHEN 热键控件获得焦点 THEN 系统应开始捕获键盘输入
3. WHEN 用户按下组合键 THEN 系统应显示组合键文本（如"Ctrl+Shift+A"）
4. WHEN 用户按下无效组合键 THEN 系统应拒绝并保持原有值
5. WHEN 调用GetHotKey函数 THEN 系统应返回虚拟键码和修饰键标志
6. WHEN 调用SetHotKey函数 THEN 系统应设置热键控件的值
7. WHEN 热键控件失去焦点 THEN 系统应停止捕获键盘输入
8. WHEN 显示热键文本 THEN 系统应使用本地化的键名（支持中文）

### 需求 7: 图片框控件

**用户故事**: 作为开发者，我希望创建图片框控件，以便显示图片文件。

#### 验收标准

1. WHEN 开发者调用CreatePictureBox函数 THEN 系统应创建一个图片框控件并返回句柄
2. WHEN 调用LoadImageFromFile函数 THEN 系统应使用WIC加载图片文件（PNG、JPG、BMP、GIF）
3. WHEN 图片加载成功 THEN 系统应使用D2D1绘制图片
4. WHEN 图片尺寸与控件不匹配 THEN 系统应支持缩放模式（拉伸、等比缩放、居中）
5. WHEN 调用LoadImageFromMemory函数 THEN 系统应从内存字节数组加载图片
6. WHEN 图片加载失败 THEN 系统应显示占位符或错误提示
7. WHEN 设置图片透明度 THEN 系统应支持Alpha通道混合
8. WHEN 调用ClearImage函数 THEN 系统应清除当前显示的图片

### 需求 8: 事件回调系统扩展

**用户故事**: 作为开发者，我希望扩展事件回调系统，以便处理更多用户交互事件。

#### 验收标准

1. WHEN 用户鼠标移动到控件上 THEN 系统应触发OnMouseEnter回调
2. WHEN 用户鼠标离开控件 THEN 系统应触发OnMouseLeave回调
3. WHEN 用户双击控件 THEN 系统应触发OnDoubleClick回调
4. WHEN 用户右键点击控件 THEN 系统应触发OnRightClick回调
5. WHEN 控件获得焦点 THEN 系统应触发OnFocus回调
6. WHEN 控件失去焦点 THEN 系统应触发OnBlur回调
7. WHEN 用户按下键盘按键 THEN 系统应触发OnKeyDown回调（包含虚拟键码和修饰键）
8. WHEN 用户松开键盘按键 THEN 系统应触发OnKeyUp回调
9. WHEN 用户输入字符 THEN 系统应触发OnChar回调（Unicode字符）
10. WHEN 控件值改变 THEN 系统应触发OnValueChanged回调

### 需求 9: 控件分组功能

**用户故事**: 作为开发者，我希望创建分组框控件，以便组织和管理相关控件。

#### 验收标准

1. WHEN 开发者调用CreateGroupBox函数 THEN 系统应创建一个分组框控件并返回句柄
2. WHEN 设置分组框标题 THEN 系统应在边框顶部显示Unicode标题文本
3. WHEN 添加子控件到分组框 THEN 系统应将子控件的父窗口设置为分组框
4. WHEN 分组框移动 THEN 系统应同时移动所有子控件
5. WHEN 分组框禁用 THEN 系统应同时禁用所有子控件
6. WHEN 分组框隐藏 THEN 系统应同时隐藏所有子控件
7. WHEN 绘制分组框 THEN 系统应使用Element UI风格的边框和标题
8. WHEN 单选按钮添加到分组框 THEN 系统应自动设置分组ID实现互斥

### 需求 10: 布局管理器

**用户故事**: 作为开发者，我希望使用布局管理器，以便自动管理控件的位置和大小。

#### 验收标准

1. WHEN 开发者调用SetLayoutManager函数 THEN 系统应为窗口设置布局管理器类型
2. WHEN 布局类型为流式布局 THEN 系统应按添加顺序水平或垂直排列控件
3. WHEN 布局类型为网格布局 THEN 系统应按行列网格排列控件
4. WHEN 布局类型为停靠布局 THEN 系统应支持控件停靠到边缘（上下左右）
5. WHEN 窗口大小改变 THEN 系统应自动重新计算并调整控件布局
6. WHEN 设置控件布局属性 THEN 系统应支持边距、对齐方式、拉伸模式
7. WHEN 添加或移除控件 THEN 系统应自动更新布局
8. WHEN 调用UpdateLayout函数 THEN 系统应立即重新计算布局

### 需求 11: 主题系统

**用户故事**: 作为开发者，我希望使用主题系统，以便统一管理应用程序的视觉风格。

#### 验收标准

1. WHEN 开发者调用LoadTheme函数 THEN 系统应加载主题配置文件
2. WHEN 主题加载成功 THEN 系统应应用主题的颜色、字体、圆角等样式到所有控件
3. WHEN 主题包含颜色定义 THEN 系统应支持主色、成功色、警告色、危险色、信息色
4. WHEN 主题包含字体定义 THEN 系统应支持标题字体、正文字体、等宽字体
5. WHEN 主题包含尺寸定义 THEN 系统应支持圆角半径、边框宽度、间距
6. WHEN 调用SetTheme函数 THEN 系统应切换到指定主题并刷新所有控件
7. WHEN 主题支持暗色模式 THEN 系统应提供亮色和暗色两套配色方案
8. WHEN 控件创建时 THEN 系统应自动应用当前主题样式
9. WHEN 主题文件格式为JSON THEN 系统应解析JSON配置并应用样式
10. WHEN 未加载主题 THEN 系统应使用默认Element UI风格

## 技术约束

1. 所有控件必须支持Unicode文本（UTF-8编码）
2. 所有控件必须使用Direct2D/DirectWrite进行自绘
3. 所有控件必须遵循Element UI设计规范
4. 所有API必须使用stdcall调用约定
5. 所有文本参数必须使用字节数组（unsigned char*）和长度参数
6. 所有控件必须支持DPI缩放
7. 所有控件必须正确处理资源释放（避免内存泄漏）
8. 所有控件必须支持禁用和隐藏状态
9. 所有回调函数必须在主线程中调用
10. 所有控件必须与现有代码架构保持一致（State结构 + 全局map管理）
