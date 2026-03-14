# Emoji Window DLL - C++ 版本

使用 C++ 和 Direct2D/DirectWrite 实现的 Windows UI 控件库，完美支持彩色 Emoji 显示。提供 16 种控件、布局管理器、主题系统和扩展事件系统，专为易语言应用设计。

## ✨ 特性

- 🎨 **16 种控件**：按钮、编辑框、复选框、单选按钮、进度条、列表框、组合框、表格等
- 🌈 **主题系统**：支持亮色/暗色主题切换，可自定义 JSON 主题
- 📐 **布局管理器**：流式布局、网格布局、停靠布局，自动响应窗口大小
- 🚀 **高性能**：表格虚拟模式支持 100000+ 行数据
- 🎯 **Element UI 风格**：统一的视觉设计，现代化界面
- 💾 **易语言友好**：完整的 DLL 声明和示例代码

## 📑 目录

- [快速开始](#-快速开始)
- [项目结构](#-项目结构)
- [编译步骤](#-编译步骤)
- [控件文档](#-控件文档)
- [核心功能](#-核心功能)
- [完整控件列表](#-完整控件列表)
- [查看截图](#-查看截图)
- [常见问题](#-常见问题)
- [性能优化](#-性能优化)
- [技术细节](#-技术细节)
- [打赏支持](#-打赏支持)

---

## 🚀 快速开始

### 1. 下载 DLL

从 [Releases](../../releases) 下载最新版本的 `emoji_window.dll`，或自行编译。

### 2. 在易语言中引入

```
' 复制 DLL 到程序目录
' 导入 易语言代码/DLL命令.e
' 导入 易语言代码/常量表.e
' 导入 易语言代码/辅助程序集.e
```

### 3. 创建第一个窗口

```
.版本 2

.程序集变量 窗口句柄, 整数型
.程序集变量 按钮ID, 整数型

.子程序 _启动窗口_创建完毕

窗口句柄 = 创建Emoji窗口 ("我的第一个窗口", 800, 600)

按钮ID = 创建Emoji按钮_辅助 (窗口句柄, "🎉", "点击我", 50, 50, 120, 40, #COLOR_PRIMARY)

设置按钮点击回调 (&按钮点击处理)

运行消息循环 ()


.子程序 按钮点击处理, , 公开, stdcall
.参数 按钮ID_, 整数型

信息框 ("按钮被点击了！", 0, "提示")
```

---

## 📁 项目结构

```
emoji_window_cpp/
├── emoji_window.sln              # Visual Studio 解决方案
├── emoji_window/
│   ├── emoji_window.vcxproj      # 项目文件
│   ├── dllmain.cpp               # DLL 入口（初始化 COM、D2D、DWrite）
│   ├── emoji_window.h            # 头文件（所有控件状态结构和 API 声明）
│   ├── emoji_window.cpp          # 主实现（所有控件逻辑和渲染）
│   └── emoji_window.def          # DLL 导出定义（210+ 导出函数）
├── themes/
│   ├── light.json                # 亮色主题（Element UI 标准配色）
│   └── dark.json                 # 暗色主题
├── docs/                         # 📚 文档目录
│   ├── controls/                 # 控件文档
│   │   ├── button.md
│   │   ├── checkbox.md
│   │   ├── progressbar.md
│   │   ├── datagridview.md
│   │   └── ...
│   ├── theme.md                  # 主题系统文档
│   ├── layout.md                 # 布局管理器文档
│   ├── events.md                 # 事件系统文档
│   ├── faq.md                    # 常见问题
│   └── performance.md            # 性能优化建议
├── 易语言代码/
│   ├── DLL命令.e                 # DLL API 声明
│   ├── 常量表.e                  # 颜色、布局、键码等常量
│   ├── 辅助程序集.e              # UTF-8 转换辅助函数
│   ├── 编码转换.e                # 编码转换工具
│   └── 窗口程序集_*.e            # 各控件示例程序（20+个）
└── x64/Release/
    └── emoji_window.dll          # 编译输出
```

---

## 🔨 编译步骤

### 方法 1：使用 Visual Studio（推荐）

1. 安装 Visual Studio 2019 或更高版本
2. 打开 `emoji_window.sln`
3. 选择 Release | x64 配置
4. 生成解决方案（Ctrl+Shift+B）
5. DLL 输出到 `x64\Release\emoji_window.dll`

### 方法 2：使用命令行（MSBuild）

```cmd
"C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\MSBuild.exe" emoji_window.sln /p:Configuration=Release /p:Platform=x64
```

---

## 📚 控件文档

### 基础控件

| 控件 | 文档 | 说明 |
|------|------|------|
| 按钮 | [button.md](docs/controls/button.md) | 支持彩色 Emoji 的按钮控件 |
| 标签 | [label.md](docs/controls/label.md) | 文本标签，支持自动换行 |
| 编辑框 | [editbox.md](docs/controls/editbox.md) | 单行/多行编辑框，支持垂直居中 |
| 复选框 | [checkbox.md](docs/controls/checkbox.md) | Element UI 风格复选框 |
| 单选按钮 | [radiobutton.md](docs/controls/radiobutton.md) | 分组互斥的单选按钮 |
| 进度条 | [progressbar.md](docs/controls/progressbar.md) | 支持确定/不确定模式 |

### 高级控件

| 控件 | 文档 | 说明 |
|------|------|------|
| 列表框 | [listbox.md](docs/controls/listbox.md) | 可滚动的项目列表 |
| 组合框 | [combobox.md](docs/controls/combobox.md) | 下拉列表选择器 |
| 图片框 | [picturebox.md](docs/controls/picturebox.md) | 支持多种格式和缩放模式 |
| 分组框 | [groupbox.md](docs/controls/groupbox.md) | 控件分组容器 |
| 热键控件 | [hotkey.md](docs/controls/hotkey.md) | 键盘快捷键捕获 |
| 树形框 | [treeview.md](docs/controls/treeview.md) | 层次结构数据，支持 Emoji 图标和拖放 |
| 表格 | [datagridview.md](docs/controls/datagridview.md) | 高性能数据表格，支持虚拟模式 |
| 选项卡 | [tabcontrol.md](docs/controls/tabcontrol.md) | 多标签页容器 |



---

## 🎯 核心功能

### 主题系统

支持亮色/暗色主题切换，可从 JSON 文件加载自定义主题。

```
' 切换暗色模式
设置暗色模式 (真)

' 从文件加载主题
从文件加载主题_辅助 ("themes/dark.json")
```

📖 [完整文档](docs/theme.md)

### 布局管理器

自动管理控件位置和大小，支持流式布局、网格布局、停靠布局。

```
' 设置水平流式布局
设置布局管理器 (窗口句柄, #LAYOUT_FLOW_H, 0, 0, 10)
添加控件到布局 (窗口句柄, 按钮句柄)
更新布局 (窗口句柄)
```

📖 [完整文档](docs/layout.md)

### 扩展事件系统

统一的事件回调机制，支持鼠标、键盘、焦点事件。

```
' 设置鼠标进入回调
设置鼠标进入回调 (控件句柄, &鼠标进入处理)

' 设置按键回调
设置按键按下回调 (控件句柄, &按键处理)
```

📖 完整文档（待完善）

---

## 📋 完整控件列表

| 控件 | 创建函数 | 关键特性 |
|------|----------|----------|
| 窗口 | `create_window()` | D2D 渲染，自定义回调 |
| 按钮 | `create_emoji_button_bytes()` | Emoji 支持，自定义颜色 |
| 标签 | `CreateLabel()` | 自动换行，对齐方式 |
| 编辑框 | `CreateEditBox()` | 垂直居中，按键回调 |
| 复选框 | `CreateCheckBox()` | Element UI 风格 |
| 单选按钮 | `CreateRadioButton()` | 分组互斥 |
| 进度条 | `CreateProgressBar()` | 动画，不确定模式 |
| 列表框 | `CreateListBox()` | 多选，自定义渲染 |
| 组合框 | `CreateComboBox()` | 下拉列表，Emoji 支持 |
| 热键控件 | `CreateHotKeyControl()` | 键盘捕获 |
| 图片框 | `CreatePictureBox()` | 文件/内存加载，缩放模式 |
| 分组框 | `CreateGroupBox()` | 子控件容器 |
| 树形框 | `CreateTreeView()` | 层次结构，Emoji 图标，拖放 |
| 表格 | `CreateDataGridView()` | 虚拟模式，多列类型 |
| 选项卡 | `CreateTabControl()` | 多标签页容器 |

---

## 📸 查看截图

查看各控件的实际效果截图，请访问 [imgs 目录](imgs/)。

---

## ❓ 常见问题

### Emoji 显示为乱码？

易语言 IDE 使用 ANSI 编码，需要将 Emoji 转换为 UTF-8 字节集。

📖 [查看解决方案](docs/faq.md#emoji-显示问题)

### 如何处理大数据量表格？

使用虚拟模式，仅加载可见行数据。

📖 [查看虚拟模式文档](docs/controls/datagridview.md#虚拟模式)

### 如何实现响应式布局？

使用布局管理器自动调整控件位置。

📖 [查看布局文档](docs/layout.md)

### 图片从内存加载显示黑色？

必须使用程序集变量（全局变量）保存图片数据，不能使用局部变量。

📖 [查看详细说明](docs/faq.md#图片加载问题)

### 更多问题

📖 [完整 FAQ 文档](docs/faq.md)

---

## ⚡ 性能优化

### 关键优化建议

1. **表格大数据**：超过 1000 行使用虚拟模式
2. **批量布局更新**：批量操作后统一调用 `UpdateLayout()`
3. **图片缩放**：大图片使用 `SCALE_FIT` 模式
4. **事件回调**：避免在回调中执行耗时操作
5. **控件数量**：单窗口控件数量建议 < 200

📖 [完整性能优化文档](docs/performance.md)

---

## 🔧 技术细节

### 核心技术

- **渲染引擎**: Direct2D
- **文字渲染**: DirectWrite
- **彩色 Emoji**: `D2D1_DRAW_TEXT_OPTIONS_ENABLE_COLOR_FONT`
- **图片加载**: WIC (Windows Imaging Component)
- **字体**: Segoe UI Emoji, Microsoft YaHei UI
- **编译器**: MSVC 2019+
- **平台**: Windows 10+

### 依赖项

- Windows SDK 10.0 或更高
- Direct2D
- DirectWrite
- 无需额外运行时（静态链接）

### 许可证

MIT License

---

## 💰 打赏支持

如果这个项目对你有帮助，欢迎请我喝一杯 ☕

<div align="center">
  <table>
    <tr>
      <td align="center">
        <strong>支付宝</strong><br/>
        <img src="https://img.msblog.cc/image-20250523012804344.png" alt="支付宝" width="200">
      </td>
      <td align="center">
        <strong>微信</strong><br/>
        <img src="https://img.msblog.cc/image-20250523012814243.png" alt="微信" width="200">
      </td>
    </tr>
  </table>
</div>

## 📧 联系方式

- **QQ**：1098901025
- **微信**：zhx_ms

> 添加请注明来意

---

<div align="center">
  <p>⭐ 如果觉得项目不错，欢迎 Star 支持！</p>
  <p>MIT License © 2025</p>
</div>
