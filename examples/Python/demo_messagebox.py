"""
MessageBox / ConfirmBox visual demo.
Includes in-window titlebar color switching to verify titlebar button visibility.
"""

import ctypes
import os
import sys


SCRIPT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
sys.path.insert(0, SCRIPT_DIR)

DLL_PATH = os.path.join(PROJECT_ROOT, "bin", "x64", "Release", "emoji_window.dll")
if not os.path.exists(DLL_PATH):
    DLL_PATH = os.path.join(SCRIPT_DIR, "emoji_window.dll")

try:
    dll = ctypes.CDLL(DLL_PATH)
except OSError:
    print("错误: 无法加载 emoji_window.dll")
    sys.exit(1)


def u(text: str) -> bytes:
    return text.encode("utf-8")


def ARGB(a: int, r: int, g: int, b: int) -> int:
    return ((a & 0xFF) << 24) | ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)


dll.create_window_bytes.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]
dll.create_window_bytes.restype = ctypes.c_void_p
dll.set_message_loop_main_window.argtypes = [ctypes.c_void_p]
dll.set_message_loop_main_window.restype = None
dll.run_message_loop.argtypes = []
dll.run_message_loop.restype = ctypes.c_int

dll.create_emoji_button_bytes.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_uint,
]
dll.create_emoji_button_bytes.restype = ctypes.c_int

BUTTON_CB = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_void_p)
dll.set_button_click_callback.argtypes = [BUTTON_CB]
dll.set_button_click_callback.restype = None

dll.CreateLabel.argtypes = [
    ctypes.c_void_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_uint,
    ctypes.c_uint,
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
    ctypes.c_int,
]
dll.CreateLabel.restype = ctypes.c_int
dll.SetLabelText.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
dll.SetLabelText.restype = None

dll.show_message_box_bytes.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_char_p,
    ctypes.c_int,
]
dll.show_message_box_bytes.restype = None

CONFIRM_CB = ctypes.CFUNCTYPE(None, ctypes.c_int)
dll.show_confirm_box_bytes.argtypes = [
    ctypes.c_void_p,
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_char_p,
    ctypes.c_int,
    ctypes.c_char_p,
    ctypes.c_int,
    CONFIRM_CB,
]
dll.show_confirm_box_bytes.restype = None

dll.set_window_titlebar_color.argtypes = [ctypes.c_void_p, ctypes.c_uint]
dll.set_window_titlebar_color.restype = None


FONT = u("Microsoft YaHei UI")

COLOR_PRIMARY = ARGB(255, 64, 158, 255)
COLOR_SUCCESS = ARGB(255, 103, 194, 58)
COLOR_WARNING = ARGB(255, 230, 162, 60)
COLOR_DANGER = ARGB(255, 245, 108, 108)
COLOR_DARK_TITLEBAR = ARGB(255, 33, 37, 41)
COLOR_LIGHT_TITLEBAR = ARGB(255, 245, 247, 250)

main_win = None
label_status = 0

btn_dark_titlebar = 0
btn_light_titlebar = 0
btn_info = 0
btn_success = 0
btn_warning = 0
btn_error = 0
btn_confirm = 0
btn_confirm_delete = 0


def set_status(text: str) -> None:
    payload = u(text)
    dll.SetLabelText(label_status, payload, len(payload))


def set_titlebar_dark() -> None:
    dll.set_window_titlebar_color(main_win, COLOR_DARK_TITLEBAR)
    set_status("已切换为深色标题栏，可观察右上角最小化、最大化、关闭按钮是否清晰。")


def set_titlebar_light() -> None:
    dll.set_window_titlebar_color(main_win, COLOR_LIGHT_TITLEBAR)
    set_status("已切换为浅色标题栏，可继续对比标题栏按钮的可见性。")


def on_confirm_result(confirmed: int) -> None:
    if confirmed:
        set_status("确认框回调: 用户点击了“确认”。")
    else:
        set_status("确认框回调: 用户点击了“取消”。")


def on_confirm_delete(confirmed: int) -> None:
    if confirmed:
        set_status("删除确认回调: 用户确认删除。")
    else:
        set_status("删除确认回调: 用户取消删除。")


_confirm_cb = CONFIRM_CB(on_confirm_result)
_confirm_delete_cb = CONFIRM_CB(on_confirm_delete)


def show_message(title: str, message: str, icon: str, status: str) -> None:
    title_bytes = u(title)
    message_bytes = u(message)
    icon_bytes = u(icon)
    dll.show_message_box_bytes(
        main_win,
        title_bytes,
        len(title_bytes),
        message_bytes,
        len(message_bytes),
        icon_bytes,
        len(icon_bytes),
    )
    set_status(status)


def show_confirm(title: str, message: str, icon: str, callback: CONFIRM_CB, status: str) -> None:
    title_bytes = u(title)
    message_bytes = u(message)
    icon_bytes = u(icon)
    dll.show_confirm_box_bytes(
        main_win,
        title_bytes,
        len(title_bytes),
        message_bytes,
        len(message_bytes),
        icon_bytes,
        len(icon_bytes),
        callback,
    )
    set_status(status)


def on_button_click(button_id: int, parent_hwnd) -> None:
    del parent_hwnd

    if button_id == btn_dark_titlebar:
        set_titlebar_dark()
        return

    if button_id == btn_light_titlebar:
        set_titlebar_light()
        return

    if button_id == btn_info:
        show_message(
            "信息提示",
            "这是一个普通的信息提示框。\n支持多行文本、左侧图标和更接近 Element 的信息框布局。",
            "ℹ️",
            "已弹出信息提示框。",
        )
        return

    if button_id == btn_success:
        show_message(
            "操作成功",
            "保存已经完成。\n\n已处理 42 条数据，用时 1.5 秒。",
            "✅",
            "已弹出成功提示框。",
        )
        return

    if button_id == btn_warning:
        show_message(
            "警告",
            "磁盘空间不足。\n\n剩余空间: 512 MB\n建议清理临时文件。",
            "⚠️",
            "已弹出警告提示框。",
        )
        return

    if button_id == btn_error:
        show_message(
            "错误",
            "发生了一处权限错误。\n\n错误代码: 0x80070005\n请尝试以管理员身份运行。",
            "❌",
            "已弹出错误提示框。",
        )
        return

    if button_id == btn_confirm:
        show_confirm(
            "确认保存",
            "确定要保存当前修改吗？\n\n点击“确认”继续保存，点击“取消”放弃本次修改。",
            "❓",
            _confirm_cb,
            "已弹出保存确认框。",
        )
        return

    if button_id == btn_confirm_delete:
        show_confirm(
            "确认删除",
            "此操作不可撤销。\n\n将删除 5 个文件，其中 2 个为受保护文件。",
            "🗑️",
            _confirm_delete_cb,
            "已弹出删除确认框。",
        )


_button_cb = BUTTON_CB(on_button_click)


def create_label(x: int, y: int, w: int, h: int, text: str, text_color: int, bg_color: int, font_size: int, bold: int = 0) -> int:
    text_bytes = u(text)
    return dll.CreateLabel(
        main_win,
        x,
        y,
        w,
        h,
        text_bytes,
        len(text_bytes),
        text_color,
        bg_color,
        FONT,
        len(FONT),
        font_size,
        bold,
        0,
        0,
        0,
        0,
    )


def create_button(emoji: str, text: str, x: int, y: int, w: int, color: int) -> int:
    emoji_bytes = u(emoji)
    text_bytes = u(text)
    return dll.create_emoji_button_bytes(
        main_win,
        emoji_bytes,
        len(emoji_bytes),
        text_bytes,
        len(text_bytes),
        x,
        y,
        w,
        40,
        color,
    )


def main() -> None:
    global main_win, label_status
    global btn_dark_titlebar, btn_light_titlebar
    global btn_info, btn_success, btn_warning, btn_error, btn_confirm, btn_confirm_delete

    title = u("MessageBox / 标题栏样式测试 - emoji_window")
    main_win = dll.create_window_bytes(title, len(title), 760, 560)
    if not main_win:
        print("错误: 创建窗口失败")
        return

    label_status = create_label(
        20,
        10,
        720,
        34,
        "点击下方按钮测试消息框样式，并切换深浅标题栏检查右上角三个按钮是否可见。",
        ARGB(255, 48, 49, 51),
        ARGB(255, 245, 247, 250),
        13,
        0,
    )

    create_label(20, 60, 360, 26, "标题栏可见性测试", ARGB(255, 48, 49, 51), ARGB(0, 0, 0, 0), 15, 1)
    create_label(
        20,
        88,
        700,
        24,
        "切换为深色标题栏后，重点观察最小化、最大化、关闭按钮是否仍然清晰，hover 是否足够扁平。",
        ARGB(255, 96, 98, 102),
        ARGB(0, 0, 0, 0),
        12,
        0,
    )

    btn_dark_titlebar = create_button("🌙", "深色标题栏", 20, 122, 170, COLOR_PRIMARY)
    btn_light_titlebar = create_button("☀️", "浅色标题栏", 205, 122, 170, ARGB(255, 144, 147, 153))

    create_label(20, 186, 360, 26, "MessageBox 样式测试", ARGB(255, 48, 49, 51), ARGB(0, 0, 0, 0), 15, 1)
    create_label(
        20,
        214,
        700,
        24,
        "用于检查信息框、确认框、图标、按钮区、标题区是否更接近 Element 的视觉结构。",
        ARGB(255, 96, 98, 102),
        ARGB(0, 0, 0, 0),
        12,
        0,
    )

    btn_info = create_button("ℹ️", "信息提示", 20, 250, 160, COLOR_PRIMARY)
    btn_success = create_button("✅", "成功提示", 195, 250, 160, COLOR_SUCCESS)
    btn_warning = create_button("⚠️", "警告提示", 370, 250, 160, COLOR_WARNING)
    btn_error = create_button("❌", "错误提示", 545, 250, 160, COLOR_DANGER)

    btn_confirm = create_button("❓", "确认保存", 20, 310, 200, COLOR_PRIMARY)
    btn_confirm_delete = create_button("🗑️", "确认删除", 235, 310, 200, COLOR_DANGER)

    info_lines = [
        "当前示例窗口不会自动关闭，便于持续观察可视化效果。",
        "标题栏按钮已经改为更扁平的 hover 结构，不再使用圆角悬浮块。",
        "建议先点“深色标题栏”，再观察右上角按钮与关闭按钮 hover 的对比度。",
    ]

    for index, line in enumerate(info_lines):
        create_label(
            20,
            388 + index * 30,
            710,
            24,
            line,
            ARGB(255, 100, 100, 100),
            ARGB(0, 0, 0, 0),
            12,
            0,
        )

    dll.set_button_click_callback(_button_cb)
    dll.set_message_loop_main_window(main_win)
    set_titlebar_light()
    dll.run_message_loop()


if __name__ == "__main__":
    main()
