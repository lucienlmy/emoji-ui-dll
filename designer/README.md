# Emoji Window 可视化设计器

emoji_window.dll 的可视化 UI 设计工具，基于 Tauri 2 + React + TypeScript + Vite 构建。支持拖拽控件到画布、实时属性编辑、多语言代码生成（易语言 / Python / C#），以及 AI 辅助设计。

## 技术栈

- 前端：React 19 + TypeScript + Vite 8 + Zustand（状态管理）
- 桌面端：Tauri 2（Rust 后端）
- 拖拽：@dnd-kit
- 代码高亮：prism-react-renderer
- 测试：Vitest + Testing Library

## 项目结构

```
designer/
├── src/                    # 前端源码
│   ├── ai/                 # AI 辅助设计模块（提示词、解析、Provider 路由）
│   ├── codegen/            # 代码生成器（epl.ts / python.ts / csharp.ts）
│   ├── components/         # React 组件（Canvas、Toolbox、PropertyPanel 等）
│   ├── config/             # 运行时配置
│   ├── data/               # 控件定义、Emoji 分类数据
│   ├── services/           # 广告、统计上报服务
│   ├── store/              # Zustand 状态管理
│   ├── types/              # TypeScript 类型定义
│   └── utils/              # 工具函数（颜色、布局、快捷键等）
├── src-tauri/              # Tauri Rust 后端
│   ├── src/                # Rust 源码
│   ├── icons/              # 应用图标
│   ├── Cargo.toml          # Rust 依赖
│   └── tauri.conf.json     # Tauri 配置
├── public/                 # 静态资源
├── dist/                   # 前端构建产物
├── .env.example            # 环境变量模板
├── package.json
├── vite.config.ts
└── tsconfig.json
```

## 环境要求

- Node.js >= 18
- Rust >= 1.77.2（Tauri 后端编译需要）
- npm

Tauri 2 还需要系统级依赖，Windows 上需要：
- Microsoft Visual Studio C++ Build Tools
- WebView2（Windows 10/11 通常已预装）

详见 [Tauri 环境准备文档](https://v2.tauri.app/start/prerequisites/)

## 安装依赖

```bash
cd designer
npm install
```

## 环境变量配置

复制 `.env.example` 为 `.env`，按需填写：

```bash
cp .env.example .env
```

主要配置项：

| 变量 | 说明 |
|------|------|
| `VITE_AI_BASE_URL` | AI API 地址（OpenAI 兼容格式） |
| `VITE_AI_API_KEY` | AI API 密钥 |
| `VITE_AI_MODEL` | AI 模型名称（默认 gpt-4.1-mini） |
| `VITE_AD_API_URL` | 广告接口地址（可选） |
| `VITE_STATS_API_URL` | 统计上报地址（可选） |
| `VITE_EMOJI_HOTKEY` | Emoji 选择器快捷键（默认 Ctrl+Shift+E） |
| `VITE_QUICK_INSERT_HOTKEY` | 快速插入控件快捷键（默认 Ctrl+Shift+I） |

## 开发

### 纯前端开发（浏览器预览）

```bash
npm run dev
```

访问 http://localhost:5173，适合快速调试 UI 和代码生成逻辑。

### Tauri 桌面端开发

```bash
npx tauri dev
```

会同时启动 Vite 开发服务器和 Tauri 窗口，支持文件读写等原生能力。

## 测试

```bash
npm test
```

使用 Vitest + jsdom 环境运行单元测试。

## 打包

### 仅打包前端（Web 版）

```bash
npm run build
```

产物输出到 `dist/` 目录，可直接部署为静态网站。

### 打包桌面安装包

```bash
npx tauri build
```

产物位于 `src-tauri/target/release/bundle/`，包含：

| 格式 | 路径 | 说明 |
|------|------|------|
| NSIS 安装包 | `bundle/nsis/EmojiWindowDesigner_1.0.0_x64-setup.exe` | Windows 安装向导，支持中英文语言选择 |
| MSI 安装包 | `bundle/msi/EmojiWindowDesigner_1.0.0_x64_en-US.msi` | Windows Installer 格式 |

打包配置在 `src-tauri/tauri.conf.json` 的 `bundle` 字段中，当前启用了 `nsis` 和 `msi` 两种目标格式。

### 打包注意事项

1. 首次打包需要下载 Rust 依赖，耗时较长
2. 确保 `npm run build` 能正常完成（Tauri 打包前会自动执行）
3. 如需修改安装包名称或版本号，编辑 `src-tauri/tauri.conf.json` 中的 `productName` 和 `version`
4. 图标文件在 `src-tauri/icons/` 目录下，替换后重新打包即可生效

## 预览构建产物

```bash
npm run preview
```

在本地预览 `dist/` 目录的构建结果。
