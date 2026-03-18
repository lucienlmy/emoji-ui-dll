"""
🔽 ComboBox 组合框控件综合示例
演示：创建组合框、添加/删除项、选中回调、读写属性
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

# ComboBox
dll.CreateComboBox.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
dll.CreateComboBox.restype = ctypes.c_int
dll.AddComboItem.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
dll.AddComboItem.restype = ctypes.c_int
dll.RemoveComboItem.argtypes = [ctypes.c_int, ctypes.c_int]
dll.ClearComboBox.argtypes = [ctypes.c_int]
dll.GetComboSelectedIndex.argtypes = [ctypes.c_int]
dll.GetComboSelectedIndex.restype = ctypes.c_int
dll.SetComboSelectedIndex.argtypes = [ctypes.c_int, ctypes.c_int]
dll.GetComboItemCount.argtypes = [ctypes.c_int]
dll.GetComboItemCount.restype = ctypes.c_int
dll.GetComboItemText.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
dll.GetComboItemText.restype = ctypes.c_int
dll.GetComboBoxText.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
dll.GetComboBoxText.restype = ctypes.c_int
dll.SetComboBoxText.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
COMBO_CB = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int)
dll.SetComboBoxCallback.argtypes = [ctypes.c_int, COMBO_CB]
dll.EnableComboBox.argtypes = [ctypes.c_int, ctypes.c_int]
dll.ShowComboBox.argtypes = [ctypes.c_int, ctypes.c_int]
dll.SetComboBoxBounds.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]

def ARGB(a, r, g, b):
    return ((a & 0xFF) << 24) | ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)

def u(s):
    return s.encode('utf-8')

# ========== 全局变量 ==========
combo_readonly = 0
combo_editable = 0
label_status = 0
main_win = None
btn_add = 0
btn_del = 0
btn_read = 0
btn_set_text = 0
btn_get_text = 0
btn_clear = 0
add_counter = [0]

# ========== 回调函数 ==========
def on_combo_readonly_select(hCombo, index):
    print(f"🔽 只读组合框选中: 索引={index}")
    if index >= 0:
        size = dll.GetComboItemText(hCombo, index, None, 0)
        if size > 0:
            buf = ctypes.create_string_buffer(size)
            dll.GetComboItemText(hCombo, index, buf, size)
            text = buf.raw[:size].decode('utf-8', errors='replace')
            msg = u(f"📍 只读框选中第 {index} 项: {text}")
        else:
            msg = u(f"📍 只读框选中第 {index} 项")
    else:
        msg = u("📍 取消选中")
    dll.SetLabelText(label_status, msg, len(msg))

def on_combo_editable_select(hCombo, index):
    print(f"✏️ 可编辑组合框选中: 索引={index}")
    if index >= 0:
        size = dll.GetComboItemText(hCombo, index, None, 0)
        if size > 0:
            buf = ctypes.create_string_buffer(size)
            dll.GetComboItemText(hCombo, index, buf, size)
            text = buf.raw[:size].decode('utf-8', errors='replace')
            msg = u(f"✏️ 可编辑框选中第 {index} 项: {text}")
        else:
            msg = u(f"✏️ 可编辑框选中第 {index} 项")
    else:
        msg = u("✏️ 取消选中")
    dll.SetLabelText(label_status, msg, len(msg))

_combo_ro_cb = COMBO_CB(on_combo_readonly_select)
_combo_ed_cb = COMBO_CB(on_combo_editable_select)

def on_button_click(button_id, parent_hwnd):
    global combo_readonly, combo_editable, add_counter
    if button_id == btn_add:
        add_counter[0] += 1
        fruits = ["🍎 苹果", "🍊 橙子", "🍋 柠檬", "🍇 葡萄", "🍓 草莓", "🍑 桃子", "🍒 樱桃", "🥝 猕猴桃"]
        text = u(fruits[add_counter[0] % len(fruits)] + f" #{add_counter[0]}")
        dll.AddComboItem(combo_readonly, text, len(text))
        dll.AddComboItem(combo_editable, text, len(text))
        msg = u(f"✅ 两个组合框各添加1项, 总数: {dll.GetComboItemCount(combo_readonly)}")
        dll.SetLabelText(label_status, msg, len(msg))

    elif button_id == btn_del:
        sel = dll.GetComboSelectedIndex(combo_readonly)
        if sel >= 0:
            dll.RemoveComboItem(combo_readonly, sel)
            dll.RemoveComboItem(combo_editable, sel)
            msg = u(f"🗑️ 已删除第 {sel} 项")
        else:
            msg = u("⚠️ 请先在只读框选中一项再删除")
        dll.SetLabelText(label_status, msg, len(msg))

    elif button_id == btn_read:
        sel_ro = dll.GetComboSelectedIndex(combo_readonly)
        sel_ed = dll.GetComboSelectedIndex(combo_editable)
        count = dll.GetComboItemCount(combo_readonly)
        msg = u(f"📖 只读框选中:{sel_ro} | 可编辑框选中:{sel_ed} | 总项数:{count}")
        dll.SetLabelText(label_status, msg, len(msg))

    elif button_id == btn_set_text:
        text = u("🎉 自定义输入文本")
        dll.SetComboBoxText(combo_editable, text, len(text))
        msg = u("✏️ 已设置可编辑框文本")
        dll.SetLabelText(label_status, msg, len(msg))

    elif button_id == btn_get_text:
        size = dll.GetComboBoxText(combo_editable, None, 0)
        if size > 0:
            buf = ctypes.create_string_buffer(size)
            dll.GetComboBoxText(combo_editable, buf, size)
            text = buf.raw[:size].decode('utf-8', errors='replace')
            msg = u(f"📖 可编辑框文本: {text}")
        else:
            msg = u("📖 可编辑框文本: (空)")
        dll.SetLabelText(label_status, msg, len(msg))

    elif button_id == btn_clear:
        dll.ClearComboBox(combo_readonly)
        dll.ClearComboBox(combo_editable)
        msg = u("🧹 已清空两个组合框")
        dll.SetLabelText(label_status, msg, len(msg))

_btn_cb = BUTTON_CB(on_button_click)

def main():
    global combo_readonly, combo_editable, label_status, main_win
    global btn_add, btn_del, btn_read, btn_set_text, btn_get_text, btn_clear

    print("=" * 60)
    print("🔽 ComboBox 组合框控件综合示例")
    print("=" * 60)

    title = u("🔽 ComboBox 组合框示例 - emoji_window")
    main_win = dll.create_window_bytes(title, len(title), 750, 520)
    if not main_win:
        print("❌ 创建窗口失败")
        return

    font = u("Microsoft YaHei UI")

    # 状态标签
    status_text = u("💡 提示：上方为只读组合框，下方为可编辑组合框")
    label_status = dll.CreateLabel(main_win, 20, 10, 710, 30, status_text, len(status_text),
        ARGB(255,50,50,50), ARGB(255,245,247,250), font, len(font), 13, 0, 0, 0, 0, 0)

    # 标签：只读组合框
    lbl1 = u("🔒 只读组合框:")
    dll.CreateLabel(main_win, 20, 55, 200, 25, lbl1, len(lbl1),
        ARGB(255,50,50,50), ARGB(0,0,0,0), font, len(font), 13, 1, 0, 0, 0, 0)

    # 创建只读组合框
    combo_readonly = dll.CreateComboBox(main_win, 20, 85, 420, 40, 1,
        ARGB(255,48,49,51), ARGB(255,255,255,255), 35, font, len(font), 14, 0, 0, 0)

    # 标签：可编辑组合框
    lbl2 = u("✏️ 可编辑组合框:")
    dll.CreateLabel(main_win, 20, 145, 200, 25, lbl2, len(lbl2),
        ARGB(255,50,50,50), ARGB(0,0,0,0), font, len(font), 13, 1, 0, 0, 0, 0)

    # 创建可编辑组合框
    combo_editable = dll.CreateComboBox(main_win, 20, 175, 420, 40, 0,
        ARGB(255,48,49,51), ARGB(255,255,255,255), 35, font, len(font), 14, 0, 0, 0)

    # 添加初始项
    items = [
        "🐶 狗 - Dog",
        "🐱 猫 - Cat",
        "🐰 兔子 - Rabbit",
        "🐼 熊猫 - Panda",
        "🦊 狐狸 - Fox",
        "🐨 考拉 - Koala",
        "🦁 狮子 - Lion",
        "🐯 老虎 - Tiger",
    ]
    for item in items:
        t = u(item)
        dll.AddComboItem(combo_readonly, t, len(t))
        dll.AddComboItem(combo_editable, t, len(t))

    # 设置回调
    dll.SetComboBoxCallback(combo_readonly, _combo_ro_cb)
    dll.SetComboBoxCallback(combo_editable, _combo_ed_cb)

    # 默认选中
    dll.SetComboSelectedIndex(combo_readonly, 0)
    dll.SetComboSelectedIndex(combo_editable, 2)

    # 按钮组
    btns = [
        ("➕", "添加项", 470, 50, ARGB(255,64,158,255)),
        ("🗑️", "删除选中", 470, 100, ARGB(255,245,108,108)),
        ("📖", "读取属性", 470, 150, ARGB(255,103,194,58)),
        ("✏️", "设置文本", 470, 200, ARGB(255,230,162,60)),
        ("📋", "获取文本", 470, 250, ARGB(255,144,147,153)),
        ("🧹", "清空全部", 470, 300, ARGB(255,200,100,100)),
    ]
    btn_ids = []
    for emoji, text, x, y, color in btns:
        e = u(emoji)
        t = u(text)
        bid = dll.create_emoji_button_bytes(main_win, e, len(e), t, len(t), x, y, 240, 35, color)
        btn_ids.append(bid)

    btn_add, btn_del, btn_read, btn_set_text, btn_get_text, btn_clear = btn_ids
    dll.set_button_click_callback(_btn_cb)

    # 读取属性并打印
    print(f"\n--- 🔽 组合框属性 ---")
    print(f"只读框项数: {dll.GetComboItemCount(combo_readonly)}")
    print(f"只读框选中: {dll.GetComboSelectedIndex(combo_readonly)}")
    print(f"可编辑框项数: {dll.GetComboItemCount(combo_editable)}")
    print(f"可编辑框选中: {dll.GetComboSelectedIndex(combo_editable)}")

    # 信息标签
    info = u("🔽 组合框支持：只读/可编辑模式、添加/删除项、选中回调、读写文本")
    dll.CreateLabel(main_win, 20, 420, 710, 50, info, len(info),
        ARGB(255,144,147,153), ARGB(0,0,0,0), font, len(font), 12, 0, 0, 0, 0, 1)

    dll.set_message_loop_main_window(main_win)
    print("\n✅ 进入消息循环...")
    dll.run_message_loop()
    print("程序退出。")

if __name__ == "__main__":
    main()
