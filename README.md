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
typedef void (__stdcall *ButtonClickCallback)(int button_id);
void __stdcall set_button_click_callback(ButtonClickCallback callback);
```

### 设置窗口大小改变回调

当自绘窗口大小被用户或代码改变时触发。

```c++
typedef void (__stdcall *WindowResizeCallback)(HWND hwnd, int width, int height);
void __stdcall SetWindowResizeCallback(WindowResizeCallback callback);
```

| 参数 | 说明 |
|------|------|
| `hwnd` | 发生大小改变的窗口句柄 |
| `width` | 窗口新的客户区宽度（像素） |
| `height` | 窗口新的客户区高度（像素） |

**易语言声明：**
```
.DLL命令 设置窗口大小改变回调, , "emoji_window.dll", "SetWindowResizeCallback"
    .参数 回调函数指针, 子程序指针
```

**易语言使用示例：**
```
.子程序 窗口大小改变回调, , 公开
.参数 窗口句柄_, 整数型
.参数 新宽度, 整数型
.参数 新高度, 整数型

' 窗口大小改变时更新布局
调试输出 ("窗口大小改变: " + 到文本 (新宽度) + " x " + 到文本 (新高度))

' 注册（程序初始化时调用一次）
设置窗口大小改变回调 (&窗口大小改变回调)
```

> **注意**：回调必须在创建窗口后、运行消息循环前完成注册。

---

### 设置窗口被关闭回调

当自绘窗口被关闭时触发（用户点击关闭按钮 ×，或代码调用 `destroy_window`，均会触发 `WM_DESTROY`）。

```c++
typedef void (__stdcall *WindowCloseCallback)(HWND hwnd);
void __stdcall SetWindowCloseCallback(WindowCloseCallback callback);
```

| 参数 | 说明 |
|------|------|
| `hwnd` | 被关闭的窗口句柄（触发时 HWND 已失效，仅用于识别是哪个窗口） |

**易语言声明：**
```
.DLL命令 设置窗口关闭回调, , "emoji_window.dll", "SetWindowCloseCallback"
    .参数 回调函数指针, 子程序指针
```

**易语言使用示例：**
```
.子程序 自绘窗口关闭回调, , 公开
.参数 已关闭的窗口句柄, 整数型

' 重置句柄变量，防止后续误用失效的 HWND
调试输出 ("自绘窗口已关闭, HWND=" + 到文本 (已关闭的窗口句柄))
.如果真 (窗口句柄 = 已关闭的窗口句柄)
    窗口句柄 = 0
.如果真结束
TabControl句柄 = 0

' 注册（程序初始化时调用一次）
设置窗口关闭回调 (&自绘窗口关闭回调)
```

> **注意**：
> - 回调触发时窗口已销毁，不要在回调内对该 `hwnd` 执行任何窗口操作。
> - 只有顶层窗口（非子窗口）关闭时才会触发此回调。
> - 若程序同时运行了 `run_message_loop`，关闭窗口后消息循环会自动退出；若由易语言消息循环驱动，则不会影响易语言进程。

---

### 编辑框

#### 创建编辑框（含文本垂直居中）

单行编辑框支持**文本垂直居中**：创建时最后一个参数传 `TRUE` 即可；仅对单行有效，多行编辑框忽略该选项。

```c++
HWND __stdcall CreateEditBox(
    HWND hParent,
    int x, int y, int width, int height,
    const unsigned char* text_bytes, int text_len,
    UINT32 fg_color, UINT32 bg_color,
    const unsigned char* font_name_bytes, int font_name_len,
    int font_size, BOOL bold, BOOL italic, BOOL underline,
    int alignment,    // 0=左 1=中 2=右
    BOOL multiline, BOOL readonly, BOOL password, BOOL has_border,
    BOOL vertical_center   // 文本垂直居中（仅单行有效）
);
```

**说明**：系统单行 EDIT 不支持垂直居中，DLL 在“单行 + 垂直居中”时内部使用多行样式（`EM_SETRECTNP`）实现垂直居中，并拦截回车以保持单行行为；左右边距设为 0 以减少白边。

**易语言声明：** 在 `创建编辑框` 的 DLL 命令中，最后一个参数为 `文本垂直居中`（逻辑型）。

**易语言示例：**
```
编辑框1 ＝ 创建编辑框 (父句柄, 140, 30, 280, 60, 文本指针, 文本长, 前景色, 背景色, 字体名指针, 字体名长, 12, 假, 假, 假, 1, 假, 假, 假, 真, 真)
' 最后一参 真 = 启用文本垂直居中
```

#### 设置编辑框垂直居中（创建后修改）

创建后也可随时开关垂直居中：

```c++
void __stdcall SetEditBoxVerticalCenter(HWND hEdit, BOOL vertical_center);
```

#### 设置编辑框按键回调

可接收编辑框的按键按下/松开通知（不拦截按键）：

```c++
typedef void (__stdcall *EditBoxKeyCallback)(HWND hEdit, int key_code, int key_down, int shift, int ctrl, int alt);
void __stdcall SetEditBoxKeyCallback(HWND hEdit, EditBoxKeyCallback callback);
```

| 参数 | 说明 |
|------|------|
| `key_code` | Windows 虚拟键码（如 13=回车 27=Esc） |
| `key_down` | 1=按下 0=松开 |
| `shift` / `ctrl` / `alt` | 1=按下 0=未按 |

**易语言**：子程序需 stdcall，参数为（编辑框句柄, 键码, 按下或松开, Shift, Ctrl, Alt）整数型；注册时传 `设置编辑框按键回调(编辑框句柄, 到整数(&子程序))`。

---

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
