"""
💬 MessageBox / ConfirmBox 信息框控件综合示例
演示：信息提示框、确认框、emoji图标、确认回调
"""
import ctypes
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

try:
    dll = ctypes.CDLL('./emoji_window.dll')
except OSError:
    print("错误: 无法加载 emoji_window.dll")
    sys.exit(1)

# ========== 函数原型 ==========
dll.create_window_bytes.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]
dll.create_window_bytes.restype = ctypes.c_void_p
dll.set_message_loop_main_window.argtypes = [ctypes.c_void_p]
dll.run_message_loop.restype = ctypes.c_int

dll.create_emoji_button_bytes.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
dll.create_emoji_button_bytes.restype = ctypes.c_int
BUTTON_CB = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_void_p)
dll.set_button_click_callback.argtypes = [BUTTON_CB]

dll.CreateLabel.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
dll.CreateLabel.restype = ctypes.c_int
dll.SetLabelText.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]

# MessageBox / ConfirmBox
dll.show_message_box_bytes.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
CONFIRM_CB = ctypes.CFUNCTYPE(None, ctypes.c_int)
dll.show_confirm_box_bytes.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, CONFIRM_CB]

def ARGB(a, r, g, b):
    return ((a & 0xFF) << 24) | ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)

def u(s):
    return s.encode('utf-8')

# ========== 全局变量 ==========
label_status = 0
main_win = None
btn_info = 0
btn_success = 0
btn_warning = 0
btn_error = 0
btn_confirm = 0
btn_confirm_del = 0

# ========== 回调函数 ==========
def on_confirm_result(confirmed):
    result = "✅ 确认" if confirmed else "❌ 取消"
    print(f"💬 确认框结果: {result}")
    msg = u(f"💬 用户选择了: {result}")
    dll.SetLabelText(label_status, msg, len(msg))

def on_confirm_delete(confirmed):
    if confirmed:
        print("🗑️ 用户确认删除")
        msg = u("🗑️ 已确认删除操作")
    else:
        print("🛡️ 用户取消删除")
        msg = u("🛡️ 已取消删除操作")
    dll.SetLabelText(label_status, msg, len(msg))

_confirm_cb = CONFIRM_CB(on_confirm_result)
_confirm_del_cb = CONFIRM_CB(on_confirm_delete)

def on_button_click(button_id, parent_hwnd):
    if button_id == btn_info:
        title = u("ℹ️ 信息提示")
        msg = u("📢 这是一条普通信息提示框\n支持多行文本和emoji表情 🎉")
        icon = u("ℹ️")
        dll.show_message_box_bytes(main_win, title, len(title), msg, len(msg), icon, len(icon))
        status = u("📢 已显示信息提示框")
        dll.SetLabelText(label_status, status, len(status))

    elif button_id == btn_success:
        title = u("✅ 操作成功")
        msg = u("🎊 恭喜！操作已成功完成！\n\n📊 处理了 42 条数据\n⏱️ 耗时 1.5 秒")
        icon = u("✅")
        dll.show_message_box_bytes(main_win, title, len(title), msg, len(msg), icon, len(icon))
        status = u("✅ 已显示成功提示框")
        dll.SetLabelText(label_status, status, len(status))

    elif button_id == btn_warning:
        title = u("⚠️ 警告")
        msg = u("🔔 注意！磁盘空间不足\n\n💾 剩余空间: 512 MB\n📁 建议清理临时文件")
        icon = u("⚠️")
        dll.show_message_box_bytes(main_win, title, len(title), msg, len(msg), icon, len(icon))
        status = u("⚠️ 已显示警告提示框")
        dll.SetLabelText(label_status, status, len(status))

    elif button_id == btn_error:
        title = u("❌ 错误")
        msg = u("💥 发生了一个错误！\n\n🔍 错误代码: 0x80070005\n📝 权限不足，请以管理员身份运行")
        icon = u("❌")
        dll.show_message_box_bytes(main_win, title, len(title), msg, len(msg), icon, len(icon))
        status = u("❌ 已显示错误提示框")
        dll.SetLabelText(label_status, status, len(status))

    elif button_id == btn_confirm:
        title = u("🤔 确认操作")
        msg = u("📋 确定要保存当前更改吗？\n\n💡 点击确认保存，取消放弃更改")
        icon = u("🤔")
        dll.show_confirm_box_bytes(main_win, title, len(title), msg, len(msg), icon, len(icon), _confirm_cb)

    elif button_id == btn_confirm_del:
        title = u("🗑️ 确认删除")
        msg = u("⚠️ 此操作不可撤销！\n\n📁 将删除选中的 5 个文件\n🔒 包含 2 个受保护文件")
        icon = u("🗑️")
        dll.show_confirm_box_bytes(main_win, title, len(title), msg, len(msg), icon, len(icon), _confirm_del_cb)

_btn_cb = BUTTON_CB(on_button_click)

def main():
    global label_status, main_win
    global btn_info, btn_success, btn_warning, btn_error, btn_confirm, btn_confirm_del

    print("=" * 60)
    print("💬 MessageBox / ConfirmBox 信息框综合示例")
    print("=" * 60)

    title = u("💬 信息框示例 - emoji_window")
    main_win = dll.create_window_bytes(title, len(title), 650, 480)
    if not main_win:
        print("❌ 创建窗口失败")
        return

    font = u("Microsoft YaHei UI")

    # 状态标签
    status_text = u("💡 点击按钮弹出不同类型的信息框")
    label_status = dll.CreateLabel(main_win, 20, 10, 610, 30, status_text, len(status_text),
        ARGB(255,50,50,50), ARGB(255,245,247,250), font, len(font), 13, 0, 0, 0, 0, 0)

    # 分类标签
    lbl1 = u("📢 信息提示框 (MessageBox):")
    dll.CreateLabel(main_win, 20, 55, 300, 25, lbl1, len(lbl1),
        ARGB(255,50,50,50), ARGB(0,0,0,0), font, len(font), 14, 1, 0, 0, 0, 0)

    # 信息框按钮
    btns_msg = [
        ("ℹ️", "信息提示", 20, 90, ARGB(255,64,158,255)),
        ("✅", "成功提示", 170, 90, ARGB(255,103,194,58)),
        ("⚠️", "警告提示", 320, 90, ARGB(255,230,162,60)),
        ("❌", "错误提示", 470, 90, ARGB(255,245,108,108)),
    ]

    lbl2 = u("🤔 确认框 (ConfirmBox) - 带回调:")
    dll.CreateLabel(main_win, 20, 155, 350, 25, lbl2, len(lbl2),
        ARGB(255,50,50,50), ARGB(0,0,0,0), font, len(font), 14, 1, 0, 0, 0, 0)

    btns_confirm = [
        ("🤔", "确认保存", 20, 190, ARGB(255,64,158,255)),
        ("🗑️", "确认删除", 220, 190, ARGB(255,245,108,108)),
    ]

    all_btns = btns_msg + btns_confirm
    btn_ids = []
    for emoji, text, x, y, color in all_btns:
        e = u(emoji)
        t = u(text)
        bid = dll.create_emoji_button_bytes(main_win, e, len(e), t, len(t), x, y, 140, 40, color)
        btn_ids.append(bid)

    btn_info, btn_success, btn_warning, btn_error, btn_confirm, btn_confirm_del = btn_ids
    dll.set_button_click_callback(_btn_cb)

    # 说明标签
    info_lines = [
        "💬 信息框功能说明:",
        "  📢 MessageBox: 纯提示，只有确定按钮",
        "  🤔 ConfirmBox: 确认/取消，带回调函数返回用户选择",
        "  🎨 支持emoji图标、多行文本、UTF-8编码",
    ]
    for i, line in enumerate(info_lines):
        t = u(line)
        dll.CreateLabel(main_win, 20, 270 + i * 30, 610, 28, t, len(t),
            ARGB(255,100,100,100), ARGB(0,0,0,0), font, len(font), 12, 0, 0, 0, 0, 0)

    dll.set_message_loop_main_window(main_win)
    print("\n✅ 进入消息循环...")
    dll.run_message_loop()
    print("程序退出。")

if __name__ == "__main__":
    main()
