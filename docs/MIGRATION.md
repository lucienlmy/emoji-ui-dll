# 文档迁移说明

## 📝 文档重构说明

为了提高文档的可读性和可维护性，我们将原来的单一 README 文档（3500+ 行）拆分为多个子文档。

## 🗂️ 新文档结构

```
emoji_window_cpp/
├── README.md                     # 主文档（简洁版，约 300 行）
└── docs/                         # 文档目录
    ├── README.md                 # 文档中心导航
    ├── controls/                 # 控件文档
    │   ├── button.md             # 按钮控件
    │   ├── checkbox.md           # 复选框控件
    │   ├── progressbar.md        # 进度条控件
    │   ├── datagridview.md       # 表格控件
    │   ├── picturebox.md         # 图片框控件
    │   └── ...                   # 其他控件（待完善）
    ├── theme.md                  # 主题系统
    ├── layout.md                 # 布局管理器
    ├── faq.md                    # 常见问题
    └── performance.md            # 性能优化
```

## 📚 文档对照表

### 主 README

| 旧版内容 | 新版位置 |
|---------|---------|
| 项目介绍、特性 | README.md（保留） |
| 快速开始 | README.md（保留） |
| 项目结构 | README.md（保留） |
| 编译步骤 | README.md（保留） |
| 控件列表 | README.md（保留） |
| 详细 API 文档 | 拆分到 docs/controls/ |

### 控件文档

| 控件 | 旧版位置 | 新版位置 |
|------|---------|---------|
| 按钮 | README.md 第 100-200 行 | docs/controls/button.md |
| 复选框 | README.md 第 300-500 行 | docs/controls/checkbox.md |
| 进度条 | README.md 第 500-800 行 | docs/controls/progressbar.md |
| 表格 | README.md 第 1500-2000 行 | docs/controls/datagridview.md |
| 图片框 | README.md 第 800-1200 行 | docs/controls/picturebox.md |
| 其他控件 | README.md | 待完善 |

### 核心功能文档

| 功能 | 旧版位置 | 新版位置 |
|------|---------|---------|
| 主题系统 | README.md 第 2500-2800 行 | docs/theme.md |
| 布局管理器 | README.md 第 2200-2500 行 | docs/layout.md |
| 扩展事件系统 | README.md 第 2000-2200 行 | 待完善 |

### 使用指南

| 内容 | 旧版位置 | 新版位置 |
|------|---------|---------|
| 常见问题 | README.md 第 3000-3200 行 | docs/faq.md |
| 性能优化 | README.md 第 3200-3300 行 | docs/performance.md |

## 🎯 文档改进

### 主 README 改进

- ✅ 从 3500+ 行精简到约 300 行
- ✅ 添加清晰的目录导航
- ✅ 添加 Emoji 图标提升可读性
- ✅ 添加快速开始指南
- ✅ 添加文档链接，方便跳转

### 子文档改进

- ✅ 每个控件独立文档，便于查找
- ✅ 统一的文档格式和结构
- ✅ 添加返回主文档的导航链接
- ✅ 添加相关文档的交叉引用
- ✅ 添加易语言完整示例

### 新增内容

- ✅ 文档中心导航页（docs/README.md）
- ✅ 性能优化专题文档
- ✅ 常见问题专题文档
- ✅ 文档贡献指南

## 📖 如何使用新文档

### 1. 从主 README 开始

访问 [README.md](../README.md)，查看项目概览和快速开始。

### 2. 查找特定控件

- 方法 1：在主 README 的"控件文档"表格中点击链接
- 方法 2：访问 [docs/README.md](README.md) 查看完整文档导航
- 方法 3：直接访问 `docs/controls/控件名.md`

### 3. 查找功能文档

- 主题系统：[docs/theme.md](theme.md)
- 布局管理器：[docs/layout.md](layout.md)
- 常见问题：[docs/faq.md](faq.md)
- 性能优化：[docs/performance.md](performance.md)

### 4. 快速查找问题

访问 [docs/faq.md](faq.md)，使用目录快速定位常见问题。

## 🚧 待完善的文档

以下控件文档正在完善中，目前可参考原 README 或易语言示例代码：

- [ ] 标签控件 (Label)
- [ ] 编辑框控件 (EditBox)
- [ ] 单选按钮 (RadioButton)
- [ ] 列表框 (ListBox)
- [ ] 组合框 (ComboBox)
- [ ] 分组框 (GroupBox)
- [ ] 热键控件 (HotKey)
- [ ] 选项卡 (TabControl)
- [ ] 扩展事件系统

## 💡 贡献文档

欢迎贡献文档！参考已有文档的格式，在 `docs/controls/` 目录下创建对应的 Markdown 文件。

详见 [docs/README.md](README.md#文档贡献)

---

## 📧 反馈

如果你对新文档结构有任何建议，欢迎：

- 提交 [Issue](../../issues)
- 联系作者：QQ 1098901025 / 微信 zhx_ms
