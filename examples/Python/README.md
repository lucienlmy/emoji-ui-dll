# Python 示例代码

这是 emoji_window.dll 的 Python 调用示例，使用 `ctypes` 库实现 DLL 调用。

## 📁 项目结构

```
Python/
├── emoji_window.py          # DLL 封装类
├── demo.py                  # 示例程序
├── run.bat                  # 运行脚本（Windows）
├── run.sh                   # 运行脚本（Linux/Mac）
├── requirements.txt         # 依赖列表
└── README.md               # 本文件
```

## ✨ 功能展示

本示例参考截图实现了以下功能：

- ✅ 创建主窗口（带 Unicode 表情标题）
- ✅ 3个分组框（控制面板、生成结果、验证测试）
- ✅ 多个标签（带 Emoji 图标）
- ✅ 多个按钮（带 Emoji 图标）
- ✅ 复选框（带回调）
- ✅ 信息框（带 Unicode 表情）

## 🚀 快速开始

### 前置要求

- Python 3.6 或更高版本
- Windows 操作系统
- emoji_window.dll（32位或64位，需与 Python 版本匹配）

### 安装步骤

1. **检查 Python 版本**

```cmd
python --version
```

2. **检查 Python 位数**

```cmd
python -c "import struct; print(struct.calcsize('P') * 8, 'bit')"
```

输出 `32 bit` 或 `64 bit`，需要与 DLL 版本匹配。

3. **安装依赖**（可选，本示例只使用标准库）

```cmd
pip install -r requirements.txt
```

### 运行程序

#### 方法 1：使用运行脚本（推荐）

```cmd
# Windows
run.bat

# Linux/Mac
chmod +x run.sh
./run.sh
```

#### 方法 2：直接运行

```cmd
python demo.py
```

## 📝 代码说明

### 1. DLL 封装类（emoji_window.py）

`EmojiWindow` 类封装了所有 DLL 函数：

```python
from emoji_window import EmojiWindow, Colors

# 初始化
ew = EmojiWindow("emoji_window.dll")

# 创建窗口
hwnd = ew.create_window("🎨 我的窗口", 800, 600)

# 创建按钮
btn_id = ew.create_button(
    hwnd, "🚀", "点击我",
    50, 50, 120, 40,
    Colors.PRIMARY
)
```

### 2. ctypes 函数声明

使用 `ctypes` 声明 DLL 函数：

```python
import ctypes
from ctypes import c_int, c_uint, c_bool, c_void_p, c_char_p

# 加载 DLL
dll = ctypes.WinDLL("emoji_window.dll")

# 设置函数签名
dll.create_window_bytes.argtypes = [c_char_p, c_int, c_int, c_int]
dll.create_window_bytes.restype = c_void_p
```

### 3. UTF-8 编码转换

Python 字符串需要转换为 UTF-8 字节：

```python
def str_to_utf8(text):
    """将字符串转换为 UTF-8 字节"""
    if isinstance(text, str):
        return text.encode('utf-8')
    return text

# 使用
title = "🎨 我的窗口"
title_bytes = str_to_utf8(title)
hwnd = dll.create_window_bytes(title_bytes, len(title_bytes), 800, 600)
```

### 4. 回调函数

使用 `WINFUNCTYPE` 定义回调：

```python
from ctypes import WINFUNCTYPE

# 定义回调类型
ButtonClickCallback = WINFUNCTYPE(None, c_int, c_void_p)

# 创建回调函数
def on_button_click(button_id, parent_hwnd):
    print(f"按钮被点击: {button_id}")

# 设置回调（保持引用防止被回收）
callback = ButtonClickCallback(on_button_click)
dll.set_button_click_callback(callback)
```

### 5. 颜色常量

使用 `Colors` 类提供的预定义颜色：

```python
from emoji_window import Colors

# Element UI 标准配色
Colors.PRIMARY    # 主题蓝 #409EFF
Colors.SUCCESS    # 成功绿 #67C23A
Colors.WARNING    # 警告橙 #E6A23C
Colors.DANGER     # 危险红 #F56C6C
Colors.INFO       # 信息灰 #909399

# 文本颜色
Colors.TEXT_PRIMARY    # 主要文本 #303133
Colors.TEXT_REGULAR    # 常规文本 #606266
Colors.TEXT_SECONDARY  # 次要文本 #909399

# 边框颜色
Colors.BORDER_BASE     # 基础边框 #DCDFE6
Colors.BORDER_LIGHT    # 浅色边框 #E4E7ED

# 背景颜色
Colors.BG_WHITE        # 白色背景 #FFFFFF
Colors.BG_LIGHT        # 浅色背景 #F5F7FA
Colors.TRANSPARENT     # 透明
```

## 🎨 完整示例

```python
from emoji_window import EmojiWindow, Colors

# 初始化
ew = EmojiWindow("emoji_window.dll")

# 创建窗口
hwnd = ew.create_window("🎨 我的应用", 800, 600)

# 创建分组框
group = ew.create_group_box(
    hwnd, "📋 控制面板",
    20, 50, 360, 200,
    Colors.BORDER_BASE,
    Colors.BG_LIGHT
)

# 创建标签
label = ew.create_label(
    hwnd, "🌐 URL:",
    40, 80, 80, 30,
    Colors.TEXT_PRIMARY,
    Colors.TRANSPARENT
)

# 创建按钮
btn_id = ew.create_button(
    hwnd, "🚀", "批量生成",
    40, 200, 120, 35,
    Colors.PRIMARY
)

# 创建复选框
checkbox = ew.create_checkbox(
    hwnd, "✅ 启用自动刷新",
    180, 205, 150, 30
)

# 设置按钮回调
def on_button_click(button_id, parent_hwnd):
    ew.show_message_box(
        hwnd, "✅ 成功", "操作完成！", "✅"
    )

ew.set_button_callback(on_button_click)

# 设置复选框回调
def on_checkbox_changed(hwnd, checked):
    print(f"复选框: {'选中' if checked else '未选中'}")

ew.set_checkbox_callback(checkbox, on_checkbox_changed)

# 运行消息循环
ew.set_main_window(hwnd)
ew.run_message_loop()
```

## ⚠️ 注意事项

### 1. Python 位数与 DLL 匹配

**必须确保 Python 和 DLL 位数一致：**

- 32位 Python → 32位 DLL
- 64位 Python → 64位 DLL

**检查 Python 位数：**
```cmd
python -c "import struct; print(struct.calcsize('P') * 8, 'bit')"
```

### 2. 回调函数生命周期

**必须保持回调对象的引用**，否则会被垃圾回收导致崩溃：

```python
# ✅ 正确：保存为实例变量
class App:
    def __init__(self):
        self.ew = EmojiWindow()
        self._button_callback = None
    
    def setup(self):
        def on_click(btn_id, hwnd):
            print("clicked")
        
        # 保存引用
        self._button_callback = self.ew.ButtonClickCallback(on_click)
        self.ew.dll.set_button_click_callback(self._button_callback)

# ❌ 错误：局部变量会被回收
def setup():
    callback = ButtonClickCallback(on_click)
    dll.set_button_click_callback(callback)
    # callback 离开作用域后会被回收！
```

### 3. DLL 路径

DLL 文件需要在以下位置之一：

- 当前目录
- Python 脚本所在目录
- 系统 PATH 环境变量中的目录

`demo.py` 会自动搜索以下路径：
```python
paths = [
    "emoji_window.dll",                      # 当前目录
    "../../x64/Release/emoji_window.dll",    # 64位
    "../../Release/emoji_window.dll",        # 32位
]
```

### 4. 字符编码

所有字符串必须转换为 UTF-8 字节：

```python
# ✅ 正确
text = "🎨 Hello"
text_bytes = text.encode('utf-8')
dll.CreateLabel(..., text_bytes, len(text_bytes), ...)

# ❌ 错误：直接传递字符串
dll.CreateLabel(..., "🎨 Hello", ...)
```

### 5. 句柄管理

窗口和控件句柄是整数指针，需要妥善保存：

```python
# 保存句柄
self.main_window = ew.create_window(...)
self.label1 = ew.create_label(...)

# 后续使用
ew.set_label_text(self.label1, "新文本")
```

## 🔧 常见问题

### Q1: 提示找不到 DLL？

**解决方案：**
1. 检查 DLL 是否存在
2. 检查 Python 位数是否与 DLL 匹配
3. 将 DLL 复制到脚本目录

### Q2: 程序崩溃或无响应？

**可能原因：**
1. 回调函数被垃圾回收（使用实例变量保存）
2. Python 位数与 DLL 不匹配
3. 传递了无效的句柄

### Q3: Emoji 显示为方框？

**解决方案：**
1. 确保使用 UTF-8 编码
2. 使用支持 Emoji 的字体
3. 检查 Windows 版本（建议 Windows 10+）

### Q4: 如何调试 ctypes 调用？

**方法：**
```python
# 1. 打印参数
print(f"创建窗口: title={title}, width={width}, height={height}")

# 2. 检查返回值
hwnd = ew.create_window(...)
print(f"窗口句柄: {hwnd}")
if not hwnd:
    print("创建失败！")

# 3. 捕获异常
try:
    ew.create_window(...)
except Exception as e:
    print(f"错误: {e}")
    import traceback
    traceback.print_exc()
```

## 📚 API 文档

### EmojiWindow 类

#### 窗口管理

```python
create_window(title, width, height) -> hwnd
    创建窗口
    
    参数:
        title: 窗口标题（支持 Unicode 表情）
        width: 窗口宽度
        height: 窗口高度
    
    返回:
        窗口句柄

set_main_window(hwnd)
    设置消息循环主窗口

run_message_loop() -> int
    运行消息循环
```

#### 控件创建

```python
create_button(parent, emoji, text, x, y, width, height, bg_color) -> button_id
    创建按钮

create_label(parent, text, x, y, width, height, fg_color, bg_color, ...) -> hwnd
    创建标签

create_group_box(parent, title, x, y, width, height, border_color, bg_color) -> hwnd
    创建分组框

create_checkbox(parent, text, x, y, width, height, checked, fg_color, bg_color) -> hwnd
    创建复选框
```

#### 回调设置

```python
set_button_callback(callback)
    设置按钮点击回调
    
    回调签名: callback(button_id, parent_hwnd)

set_checkbox_callback(checkbox_hwnd, callback)
    设置复选框回调
    
    回调签名: callback(hwnd, checked)
```

#### 工具方法

```python
show_message_box(parent, title, message, icon)
    显示信息框

set_label_text(label_hwnd, text)
    设置标签文本

@staticmethod
str_to_utf8(text) -> bytes
    将字符串转换为 UTF-8 字节

@staticmethod
argb(a, r, g, b) -> int
    创建 ARGB 颜色值
```

## 💡 扩展建议

1. **封装更多控件**：添加编辑框、进度条、列表框等
2. **异步操作**：使用 `threading` 或 `asyncio` 处理耗时操作
3. **配置文件**：使用 JSON/YAML 保存界面配置
4. **日志记录**：使用 `logging` 模块记录操作日志
5. **单元测试**：使用 `unittest` 编写测试用例

## 📄 许可证

MIT License

---

如有问题，请联系：
- QQ：1098901025
- 微信：zhx_ms
