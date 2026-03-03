# Emoji Window DLL - C++ 版本

使用 C++ 和 Direct2D 实现彩色 Emoji 显示的 DLL。

## 项目结构

```
emoji_window_cpp/
├── emoji_window.sln          # Visual Studio 解决方案
├── emoji_window/
│   ├── emoji_window.vcxproj  # 项目文件
│   ├── dllmain.cpp           # DLL 入口
│   ├── emoji_window.h        # 头文件
│   ├── emoji_window.cpp      # 主实现
│   ├── renderer.h            # 渲染器头文件
│   ├── renderer.cpp          # 渲染器实现
│   └── exports.def           # 导出定义
└── output/
    └── emoji_window.dll      # 编译输出

```

## 编译步骤

### 1. 使用 Visual Studio（推荐）

1. 安装 Visual Studio 2019 或更高版本
2. 打开 `emoji_window.sln`
3. 选择 Release | x64 配置
4. 生成解决方案（Ctrl+Shift+B）
5. DLL 输出到 `x64\Release\emoji_window.dll`

### 2. 使用命令行（MSBuild）

```cmd
"C:\Program Files\Microsoft Visual Studio\2022\Community\MSBuild\Current\Bin\MSBuild.exe" emoji_window.sln /p:Configuration=Release /p:Platform=x64
```

## API 文档

### 创建窗口

```c++
HWND create_window(const char* title, int width, int height);
```

### 创建 Emoji 按钮（字节集）

```c++
int create_emoji_button_bytes(
    HWND parent,
    const unsigned char* emoji_bytes,
    int emoji_len,
    const unsigned char* text_bytes,
    int text_len,
    int x, int y, int width, int height,
    unsigned int bg_color
);
```

### 设置按钮点击回调

```c++
typedef void (*ButtonClickCallback)(int button_id);
void set_button_click_callback(ButtonClickCallback callback);
```

### 运行消息循环

```c++
int run_message_loop();
```

## 易语言调用示例

参见 `examples/test.txt`

## 技术细节

- **渲染引擎**: Direct2D
- **文字渲染**: DirectWrite
- **彩色 Emoji**: `D2D1_DRAW_TEXT_OPTIONS_ENABLE_COLOR_FONT`
- **字体**: Segoe UI Emoji
- **编译器**: MSVC 2019+
- **平台**: Windows 10+

## 依赖项

- Windows SDK 10.0 或更高
- Direct2D
- DirectWrite
- 无需额外运行时（静态链接）

## 许可证

MIT License
