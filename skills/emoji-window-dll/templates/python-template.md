# Python emoji_window.dll 代码模板

## 模板 1：基础使用模板（使用封装类）

```python
from emoji_window import EmojiWindow, Colors

class MyApp:
    def __init__(self):
        self.ew = EmojiWindow()  # 自动搜索 DLL
        # 或指定路径: self.ew = EmojiWindow("path/to/emoji_window.dll")
        self.main_window = None
        self.label_status = None

    def create_ui(self):
        # 创建主窗口（标题支持 Emoji）
        self.main_window = self.ew.create_window("🎨 我的应用", 800, 600)

        # 创建分组框
        self.ew.create_group_box(
            self.main_window, "📋 控制面板",
            20, 50, 360, 200,
            Colors.BORDER_BASE, Colors.BG_LIGHT
        )

        # 创建标签
        self.label_status = self.ew.create_label(
            self.main_window, "🔐 状态: 就绪",
            40, 90, 300, 30,
            Colors.TEXT_PRIMARY, Colors.TRANSPARENT
        )

        # 创建按钮
        self.btn_generate = self.ew.create_button(
            self.main_window, "🚀", "生成",
            40, 130, 120, 35, Colors.PRIMARY
        )
        self.btn_copy = self.ew.create_button(
            self.main_window, "📋", "复制",
            170, 130, 120, 35, Colors.SUCCESS
        )

        # 创建复选框
        self.checkbox = self.ew.create_checkbox(
            self.main_window, "✅ 启用自动刷新",
            40, 180, 200, 30
        )

        # 设置回调
        self.ew.set_button_callback(self.on_button_click)
        self.ew.set_checkbox_callback(self.checkbox, self.on_checkbox_changed)

    def on_button_click(self, button_id, parent_hwnd):
        print(f"按钮被点击: ID={button_id}")
        if button_id == self.btn_generate:
            self.ew.set_label_text(self.label_status, "🔐 状态: 正在生成...")
            self.ew.show_message_box(self.main_window, "💡 提示", "生成完成！", "✅")
        elif button_id == self.btn_copy:
            self.ew.set_label_text(self.label_status, "📋 已复制到剪贴板")

    def on_checkbox_changed(self, hwnd, checked):
        status = "已启用" if checked else "已禁用"
        self.ew.set_label_text(self.label_status, f"🔄 自动刷新: {status}")

    def run(self):
        self.create_ui()
        self.ew.set_main_window(self.main_window)
        self.ew.run_message_loop()

if __name__ == "__main__":
    app = MyApp()
    app.run()
```

## 模板 2：直接 ctypes 调用模板（不用封装类）

```python
import ctypes
from ctypes import c_int, c_uint, c_bool, c_void_p, c_char_p, WINFUNCTYPE
import os

# 加载 DLL
dll_path = os.path.abspath("emoji_window.dll")
dll = ctypes.WinDLL(dll_path)

# ===== 设置函数签名 =====

# 窗口
dll.create_window_bytes.argtypes = [c_char_p, c_int, c_int, c_int]
dll.create_window_bytes.restype = c_void_p

dll.set_message_loop_main_window.argtypes = [c_void_p]
dll.set_message_loop_main_window.restype = None

dll.run_message_loop.argtypes = []
dll.run_message_loop.restype = c_int

dll.destroy_window.argtypes = [c_void_p]
dll.destroy_window.restype = None

# 按钮
dll.create_emoji_button_bytes.argtypes = [
    c_void_p, c_char_p, c_int, c_char_p, c_int,
    c_int, c_int, c_int, c_int, c_uint
]
dll.create_emoji_button_bytes.restype = c_int

# 按钮回调
ButtonClickCallback = WINFUNCTYPE(None, c_int, c_void_p)
dll.set_button_click_callback.argtypes = [ButtonClickCallback]
dll.set_button_click_callback.restype = None

# 标签
dll.CreateLabel.argtypes = [
    c_void_p, c_int, c_int, c_int, c_int,
    c_char_p, c_int, c_uint, c_uint,
    c_char_p, c_int, c_int, c_bool, c_bool, c_bool,
    c_int, c_bool
]
dll.CreateLabel.restype = c_void_p

dll.SetLabelText.argtypes = [c_void_p, c_char_p, c_int]
dll.SetLabelText.restype = None

# 信息框
dll.show_message_box_bytes.argtypes = [
    c_void_p, c_char_p, c_int, c_char_p, c_int, c_char_p, c_int
]
dll.show_message_box_bytes.restype = None

# ===== 辅助函数 =====

def utf8(text):
    """字符串转 UTF-8 字节"""
    return text.encode('utf-8')

def argb(a, r, g, b):
    """创建 ARGB 颜色"""
    return (a << 24) | (r << 16) | (g << 8) | b

# ===== 创建界面 =====

# 创建窗口
title = utf8("🎨 我的应用")
hwnd = dll.create_window_bytes(title, len(title), 800, 600)

# 创建标签
text = utf8("💡 点击按钮查看效果")
font = utf8("Microsoft YaHei UI")
label = dll.CreateLabel(
    hwnd, 20, 20, 400, 30,
    text, len(text),
    argb(255, 48, 49, 51),    # 前景色
    argb(0, 0, 0, 0),          # 透明背景
    font, len(font),
    14, False, False, False,    # 字体属性
    0, False                    # 对齐、换行
)

# 创建按钮
emoji = utf8("🚀")
btn_text = utf8("点击我")
btn_id = dll.create_emoji_button_bytes(
    hwnd, emoji, len(emoji),
    btn_text, len(btn_text),
    20, 60, 150, 50,
    argb(255, 64, 158, 255)  # 主题蓝
)

# ===== 回调函数 =====

def on_button_click(button_id, parent_hwnd):
    print(f"按钮 {button_id} 被点击")
    new_text = utf8("✅ 按钮已点击！")
    dll.SetLabelText(label, new_text, len(new_text))

    title = utf8("💡 提示")
    msg = utf8("操作成功！🎉")
    icon = utf8("ℹ️")
    dll.show_message_box_bytes(hwnd, title, len(title), msg, len(msg), icon, len(icon))

# 必须保存回调引用，防止被 GC 回收
_callback = ButtonClickCallback(on_button_click)
dll.set_button_click_callback(_callback)

# ===== 运行消息循环 =====

dll.set_message_loop_main_window(hwnd)
dll.run_message_loop()
```

## 模板 3：回调设置模板

```python
from emoji_window import EmojiWindow, Colors

ew = EmojiWindow()
hwnd = ew.create_window("🎨 回调示例", 800, 600)

# ===== 按钮点击回调 =====
btn1 = ew.create_button(hwnd, "📢", "按钮1", 20, 20, 120, 40, Colors.PRIMARY)
btn2 = ew.create_button(hwnd, "📋", "按钮2", 150, 20, 120, 40, Colors.SUCCESS)

def on_button_click(button_id, parent_hwnd):
    if button_id == btn1:
        print("按钮1被点击")
    elif button_id == btn2:
        print("按钮2被点击")

ew.set_button_callback(on_button_click)

# ===== 复选框回调 =====
cb1 = ew.create_checkbox(hwnd, "✅ 选项A", 20, 80, 150, 30)
cb2 = ew.create_checkbox(hwnd, "✅ 选项B", 20, 120, 150, 30)

def on_checkbox_a(hwnd_cb, checked):
    print(f"选项A: {'选中' if checked else '未选中'}")

def on_checkbox_b(hwnd_cb, checked):
    print(f"选项B: {'选中' if checked else '未选中'}")

ew.set_checkbox_callback(cb1, on_checkbox_a)
ew.set_checkbox_callback(cb2, on_checkbox_b)

# ===== 运行 =====
ew.set_main_window(hwnd)
ew.run_message_loop()
```

## 模板 4：控件创建和操作模板

```python
from emoji_window import EmojiWindow, Colors

ew = EmojiWindow()
hwnd = ew.create_window("🎨 控件示例", 900, 700)

# ===== 分组框 =====
grp1 = ew.create_group_box(hwnd, "📋 控制面板", 20, 50, 400, 250, Colors.BORDER_BASE, Colors.BG_LIGHT)
grp2 = ew.create_group_box(hwnd, "📊 显示区域", 440, 50, 440, 250, Colors.BORDER_BASE, Colors.BG_LIGHT)

# ===== 标签 =====
lbl_url = ew.create_label(hwnd, "🌐 URL:", 40, 90, 80, 30, Colors.TEXT_PRIMARY, Colors.TRANSPARENT)
lbl_status = ew.create_label(
    hwnd, "🔐 msToken: ✓",
    460, 90, 400, 30,
    Colors.SUCCESS, Colors.TRANSPARENT,
    bold=True
)

# 多行标签（自动换行）
lbl_hint = ew.create_label(
    hwnd,
    "💡 提示：某些参数可能无法生成\n⚠️ 注意：请耐心等待",
    40, 350, 820, 60,
    Colors.TEXT_SECONDARY, Colors.TRANSPARENT,
    font_size=13, word_wrap=True
)

# ===== 按钮组 =====
btn_gen = ew.create_button(hwnd, "🚀", "批量生成", 40, 200, 120, 35, Colors.PRIMARY)
btn_copy = ew.create_button(hwnd, "📋", "复制", 170, 200, 100, 35, Colors.SUCCESS)
btn_verify = ew.create_button(hwnd, "📝", "验证参数", 40, 430, 120, 35, Colors.PRIMARY)
btn_test = ew.create_button(hwnd, "🔄", "测试请求", 170, 430, 120, 35, Colors.WARNING)
btn_clear = ew.create_button(hwnd, "🗑️", "清空", 300, 430, 120, 35, Colors.DANGER)

# ===== 复选框 =====
cb_auto = ew.create_checkbox(hwnd, "✅ 启用自动刷新", 280, 205, 150, 30)

# ===== 信息框 =====
def on_button(button_id, parent_hwnd):
    if button_id == btn_gen:
        ew.set_label_text(lbl_status, "🔐 msToken: ✓ (生成中...)")
    elif button_id == btn_copy:
        ew.show_message_box(hwnd, "📋 复制", "已复制到剪贴板！", "✅")
    elif button_id == btn_verify:
        ew.show_message_box(hwnd, "📝 验证", "参数验证通过！", "✅")
    elif button_id == btn_test:
        ew.show_message_box(hwnd, "⚠️ 警告", "参数生成不完整！\n\nmsToken: ✓ | a_bogus: ✗", "⚠️")
    elif button_id == btn_clear:
        ew.set_label_text(lbl_status, "🔐 msToken: -")

ew.set_button_callback(on_button)

def on_auto_refresh(cb_hwnd, checked):
    if checked:
        ew.set_label_text(lbl_status, "🔐 msToken: ✓ (自动刷新中...)")

ew.set_checkbox_callback(cb_auto, on_auto_refresh)

# ===== 运行 =====
ew.set_main_window(hwnd)
ew.run_message_loop()
```

## 颜色常量参考

```python
from emoji_window import EmojiWindow

argb = EmojiWindow.argb

# Element UI 标准配色
PRIMARY   = argb(255, 64, 158, 255)    # #409EFF 主题蓝
SUCCESS   = argb(255, 103, 194, 58)    # #67C23A 成功绿
WARNING   = argb(255, 230, 162, 60)    # #E6A23C 警告橙
DANGER    = argb(255, 245, 108, 108)   # #F56C6C 危险红
INFO      = argb(255, 144, 147, 153)   # #909399 信息灰

TEXT_PRIMARY   = argb(255, 48, 49, 51)      # #303133 主要文本
TEXT_REGULAR   = argb(255, 96, 98, 102)     # #606266 常规文本
TEXT_SECONDARY = argb(255, 144, 147, 153)   # #909399 次要文本

BORDER_BASE  = argb(255, 220, 223, 230)    # #DCDFE6 基础边框
BORDER_LIGHT = argb(255, 228, 231, 237)    # #E4E7ED 浅色边框

BG_WHITE     = argb(255, 255, 255, 255)    # #FFFFFF 白色
BG_LIGHT     = argb(255, 245, 247, 250)    # #F5F7FA 浅灰
TRANSPARENT  = argb(0, 0, 0, 0)            # 透明
```
