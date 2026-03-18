# Python 调用规则

## DLL 加载方式

使用 `ctypes.WinDLL` 加载，必须传入绝对路径：

```python
import ctypes
from ctypes import c_int, c_uint, c_bool, c_void_p, c_char_p, WINFUNCTYPE
import os

abs_path = os.path.abspath("emoji_window.dll")
dll = ctypes.WinDLL(abs_path)
```

注意事项：
- Python 位数必须与 DLL 位数匹配（32位 DLL 用 32位 Python，64位同理）
- 使用 `WinDLL`（StdCall 调用约定），不要用 `CDLL`
- 检查位数：`python -c "import struct; print(struct.calcsize('P') * 8, 'bit')"`

## 函数签名设置

每个 DLL 函数都必须设置 `argtypes` 和 `restype`：

```python
dll.create_window_bytes.argtypes = [c_char_p, c_int, c_int, c_int]
dll.create_window_bytes.restype = c_void_p
```

### 常用类型映射表

| C/C++ 类型 | ctypes 类型 | 说明 |
|-----------|------------|------|
| `int` | `c_int` | 整数型（按钮ID、尺寸等） |
| `unsigned int` / `UINT` | `c_uint` | 无符号整数（ARGB 颜色值） |
| `bool` / `BOOL` | `c_bool` | 布尔型 |
| `void*` / `HWND` / `HANDLE` | `c_void_p` | 指针/句柄 |
| `const char*` | `c_char_p` | UTF-8 字节指针 |
| `void` | `None` | 无返回值 |
| `int*` (输出参数) | `POINTER(c_int)` | 整数输出指针 |

## 回调防 GC

回调函数对象必须保存到实例变量，否则被 Python 垃圾回收后程序崩溃：

```python
# ✅ 正确 - 保存到实例变量
self._button_callback = self.ButtonClickCallback(callback)
dll.set_button_click_callback(self._button_callback)

# ✅ 正确 - 多个同类型回调用字典保存
if not hasattr(self, '_checkbox_callbacks'):
    self._checkbox_callbacks = {}
self._checkbox_callbacks[checkbox_hwnd] = self.CheckBoxCallback(callback)
dll.SetCheckBoxCallback(checkbox_hwnd, self._checkbox_callbacks[checkbox_hwnd])

# ❌ 错误 - 局部变量，函数返回后被GC回收，触发崩溃
cb = ButtonClickCallback(callback)
dll.set_button_click_callback(cb)
```

命名约定：回调实例变量统一以 `self._xxx_callback` 或 `self._xxx_callbacks` 命名。

## str_to_utf8 辅助函数

所有传给 DLL 的文本必须先转为 UTF-8 bytes：

```python
@staticmethod
def str_to_utf8(text):
    """将字符串转换为 UTF-8 字节"""
    if isinstance(text, str):
        return text.encode('utf-8')
    return text
```

使用示例：

```python
title_bytes = str_to_utf8("🎨 窗口标题")
hwnd = dll.create_window_bytes(title_bytes, len(title_bytes), 800, 600)
```

## ARGB 辅助函数

颜色值格式为 `0xAARRGGBB`，使用位运算构造：

```python
@staticmethod
def argb(a, r, g, b):
    """创建 ARGB 颜色值"""
    return (a << 24) | (r << 16) | (g << 8) | b

# 使用示例
PRIMARY   = argb(255, 64, 158, 255)   # #409EFF 主题蓝
SUCCESS   = argb(255, 103, 194, 58)   # #67C23A 成功绿
TRANSPARENT = argb(0, 0, 0, 0)        # 透明
```

## WINFUNCTYPE 回调定义

使用 `WINFUNCTYPE` 定义 StdCall 回调类型（不要用 `CFUNCTYPE`）：

```python
from ctypes import WINFUNCTYPE, c_int, c_void_p, c_bool

ButtonClickCallback  = WINFUNCTYPE(None, c_int, c_void_p)
MessageBoxCallback   = WINFUNCTYPE(None, c_int)
CheckBoxCallback     = WINFUNCTYPE(None, c_void_p, c_bool)
ListBoxCallback      = WINFUNCTYPE(None, c_int, c_int)
ComboBoxCallback     = WINFUNCTYPE(None, c_int, c_int)
DataGridCellCallback = WINFUNCTYPE(None, c_int, c_int, c_int)
DataGridColumnHeaderCallback = WINFUNCTYPE(None, c_int, c_int)
```

### 常用回调签名表

| 回调类型 | 签名 | 参数说明 |
|---------|------|---------|
| `ButtonClickCallback` | `(None, c_int, c_void_p)` | (按钮ID, 父窗口句柄) |
| `MessageBoxCallback` | `(None, c_int)` | (是否确认: 1=确认, 0=取消) |
| `CheckBoxCallback` | `(None, c_void_p, c_bool)` | (复选框句柄, 是否选中) |
| `ListBoxCallback` | `(None, c_int, c_int)` | (列表框句柄, 选中索引) |
| `ComboBoxCallback` | `(None, c_int, c_int)` | (组合框句柄, 选中索引) |
| `DataGridCellCallback` | `(None, c_int, c_int, c_int)` | (表格句柄, 行, 列) |
| `DataGridColumnHeaderCallback` | `(None, c_int, c_int)` | (表格句柄, 列) |

## 文本传递规则

所有文本先 `.encode('utf-8')` 转为 bytes，传入 bytes 和 `len(bytes)`：

```python
# ✅ 正确
text_bytes = "🎯 点击我".encode('utf-8')
dll.SetLabelText(label_handle, text_bytes, len(text_bytes))

# ❌ 错误 - 直接传字符串
dll.SetLabelText(label_handle, "🎯 点击我", len("🎯 点击我"))
```

函数调用模式：

```python
# 文本参数总是成对出现：(bytes, len)
emoji_bytes = str_to_utf8(emoji)
text_bytes  = str_to_utf8(text)
dll.create_emoji_button_bytes(
    parent,
    emoji_bytes, len(emoji_bytes),   # emoji + 长度
    text_bytes, len(text_bytes),     # 文本 + 长度
    x, y, width, height, bg_color
)
```

## 两次调用模式

DLL 中获取文本类函数采用"两次调用"模式：
1. 第一次传 `None` 和 `0` 获取所需缓冲区长度
2. 第二次分配缓冲区后再调用获取实际数据

```python
import ctypes

def get_text_2call(func, handle):
    """通用两次调用辅助函数"""
    # 第一次调用：获取长度
    length = func(handle, None, 0)
    if length <= 0:
        return b"", 0

    # 第二次调用：获取数据
    buf = ctypes.create_string_buffer(length)
    func(handle, buf, length)
    return buf.raw[:length], length

# 使用示例
text_bytes, text_len = get_text_2call(dll.GetButtonText, button_id)
text = text_bytes.decode('utf-8')
```

### 带索引的两次调用变体

列表框/组合框项目文本需要额外的索引参数：

```python
def get_item_text_2call(func, handle, index):
    """带索引的两次调用"""
    length = func(handle, index, None, 0)
    if length <= 0:
        return b"", 0
    buf = ctypes.create_string_buffer(length)
    func(handle, index, buf, length)
    return buf.raw[:length], length

# 使用示例
text_bytes, _ = get_item_text_2call(dll.GetListItemText, listbox, 0)
text_bytes, _ = get_item_text_2call(dll.GetComboItemText, combo, 2)
```

### DataGrid 单元格的两次调用

```python
def get_cell_text_2call(func, grid, row, col):
    """DataGrid 单元格两次调用"""
    length = func(grid, row, col, None, 0)
    if length <= 0:
        return b"", 0
    buf = ctypes.create_string_buffer(length)
    func(grid, row, col, buf, length)
    return buf.raw[:length], length

# 使用示例
text_bytes, _ = get_cell_text_2call(dll.DataGrid_GetCellText, grid, 0, 1)
```

## 完整示例

```python
import ctypes
from ctypes import c_int, c_uint, c_void_p, c_char_p, WINFUNCTYPE
import os

class EmojiWindow:
    def __init__(self, dll_path):
        self.dll = ctypes.WinDLL(os.path.abspath(dll_path))
        self._setup_functions()
        self._checkbox_callbacks = {}

    @staticmethod
    def str_to_utf8(text):
        if isinstance(text, str):
            return text.encode('utf-8')
        return text

    @staticmethod
    def argb(a, r, g, b):
        return (a << 24) | (r << 16) | (g << 8) | b

    def _setup_functions(self):
        self.dll.create_window_bytes.argtypes = [c_char_p, c_int, c_int, c_int]
        self.dll.create_window_bytes.restype = c_void_p

        self.dll.set_message_loop_main_window.argtypes = [c_void_p]
        self.dll.set_message_loop_main_window.restype = None

        self.dll.run_message_loop.argtypes = []
        self.dll.run_message_loop.restype = c_int

        self.ButtonClickCallback = WINFUNCTYPE(None, c_int, c_void_p)
        self.dll.set_button_click_callback.argtypes = [self.ButtonClickCallback]
        self.dll.set_button_click_callback.restype = None

    def create_window(self, title, width, height):
        t = self.str_to_utf8(title)
        return self.dll.create_window_bytes(t, len(t), width, height)

    def set_button_callback(self, callback):
        self._button_callback = self.ButtonClickCallback(callback)
        self.dll.set_button_click_callback(self._button_callback)

    def run(self, hwnd):
        self.dll.set_message_loop_main_window(hwnd)
        return self.dll.run_message_loop()
```
