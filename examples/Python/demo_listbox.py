"""
📋 ListBox 列表框控件综合示例
演示：创建列表框、添加/删除项、选中回调、读写属性
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
dll.destroy_window.argtypes = [ctypes.c_void_p]

dll.create_emoji_button_bytes.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
dll.create_emoji_button_bytes.restype = ctypes.c_int
BUTTON_CB = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_void_p)
dll.set_button_click_callback.argtypes = [BUTTON_CB]

dll.CreateLabel.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
dll.CreateLabel.restype = ctypes.c_int
dll.SetLabelText.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]

# ListBox
dll.CreateListBox.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint]
dll.CreateListBox.restype = ctypes.c_int
dll.AddListItem.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
dll.AddListItem.restype = ctypes.c_int
dll.RemoveListItem.argtypes = [ctypes.c_int, ctypes.c_int]
dll.ClearListBox.argtypes = [ctypes.c_int]
dll.GetSelectedIndex.argtypes = [ctypes.c_int]
dll.GetSelectedIndex.restype = ctypes.c_int
dll.SetSelectedIndex.argtypes = [ctypes.c_int, ctypes.c_int]
dll.GetListItemCount.argtypes = [ctypes.c_int]
dll.GetListItemCount.restype = ctypes.c_int
dll.GetListItemText.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
dll.GetListItemText.restype = ctypes.c_int
LISTBOX_CB = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int)
dll.SetListBoxCallback.argtypes = [ctypes.c_int, LISTBOX_CB]
dll.EnableListBox.argtypes = [ctypes.c_int, ctypes.c_int]
dll.ShowListBox.argtypes = [ctypes.c_int, ctypes.c_int]
dll.SetListBoxBounds.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]

dll.show_message_box_bytes.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]

def ARGB(a, r, g, b):
    return ((a & 0xFF) << 24) | ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)

def u(s):
    return s.encode('utf-8')

# ========== 全局变量 ==========
listbox = 0
label_status = 0
main_win = None
btn_add = 0
btn_del = 0
btn_read = 0
btn_clear = 0
btn_count = 0
add_counter = [0]

# ========== 回调函数 ==========
def on_listbox_select(hListBox, index):
    print(f"📋 列表框选中: 索引={index}")
    if index >= 0:
        size = dll.GetListItemText(hListBox, index, None, 0)
        if size > 0:
            buf = ctypes.create_string_buffer(size)
            dll.GetListItemText(hListBox, index, buf, size)
            text = buf.raw[:size].decode('utf-8', errors='replace')
            msg = u(f"📍 选中第 {index} 项: {text}")
        else:
            msg = u(f"📍 选中第 {index} 项: (空)")
    else:
        msg = u("📍 取消选中")
    dll.SetLabelText(label_status, msg, len(msg))

_listbox_cb = LISTBOX_CB(on_listbox_select)

def on_button_click(button_id, parent_hwnd):
    global listbox, add_counter
    if button_id == btn_add:
        add_counter[0] += 1
        emojis = ["🎵", "🎶", "🎸", "🎹", "🎺", "🎻", "🥁", "🎷"]
        emoji = emojis[add_counter[0] % len(emojis)]
        text = u(f"{emoji} 新项目 #{add_counter[0]}")
        item_id = dll.AddListItem(listbox, text, len(text))
        msg = u(f"✅ 添加成功 (ID={item_id}), 总数: {dll.GetListItemCount(listbox)}")
        dll.SetLabelText(label_status, msg, len(msg))

    elif button_id == btn_del:
        sel = dll.GetSelectedIndex(listbox)
        if sel >= 0:
            dll.RemoveListItem(listbox, sel)
            msg = u(f"🗑️ 已删除第 {sel} 项, 剩余: {dll.GetListItemCount(listbox)}")
        else:
            msg = u("⚠️ 请先选中一项再删除")
        dll.SetLabelText(label_status, msg, len(msg))

    elif button_id == btn_read:
        sel = dll.GetSelectedIndex(listbox)
        count = dll.GetListItemCount(listbox)
        if sel >= 0:
            size = dll.GetListItemText(listbox, sel, None, 0)
            if size > 0:
                buf = ctypes.create_string_buffer(size)
                dll.GetListItemText(listbox, sel, buf, size)
                text = buf.raw[:size].decode('utf-8', errors='replace')
                msg = u(f"📖 第{sel}项: {text} (共{count}项)")
            else:
                msg = u(f"📖 第{sel}项: (空)")
        else:
            msg = u(f"📖 总项数: {count}, 未选中任何项")
        dll.SetLabelText(label_status, msg, len(msg))

    elif button_id == btn_clear:
        dll.ClearListBox(listbox)
        msg = u("🧹 已清空列表框")
        dll.SetLabelText(label_status, msg, len(msg))

    elif button_id == btn_count:
        count = dll.GetListItemCount(listbox)
        sel = dll.GetSelectedIndex(listbox)
        msg = u(f"📊 项目总数: {count}, 当前选中: {sel}")
        dll.SetLabelText(label_status, msg, len(msg))

_btn_cb = BUTTON_CB(on_button_click)

def main():
    global listbox, label_status, main_win
    global btn_add, btn_del, btn_read, btn_clear, btn_count

    print("=" * 60)
    print("📋 ListBox 列表框控件综合示例")
    print("=" * 60)

    title = u("📋 ListBox 列表框示例 - emoji_window")
    main_win = dll.create_window_bytes(title, len(title), 700, 550)
    if not main_win:
        print("❌ 创建窗口失败")
        return

    font = u("Microsoft YaHei UI")

    # 状态标签
    status_text = u("💡 提示：点击列表项查看内容，使用按钮操作列表")
    label_status = dll.CreateLabel(main_win, 20, 10, 660, 30, status_text, len(status_text),
        ARGB(255,50,50,50), ARGB(255,245,247,250), font, len(font), 13, 0, 0, 0, 0, 0)

    # 创建列表框 (多选=0)
    listbox = dll.CreateListBox(main_win, 20, 50, 400, 380, 0,
        ARGB(255,48,49,51), ARGB(255,255,255,255))

    # 添加带emoji的初始项
    items = [
        "🌍 地球 - Earth",
        "🌙 月亮 - Moon",
        "⭐ 星星 - Star",
        "☀️ 太阳 - Sun",
        "🌈 彩虹 - Rainbow",
        "🌊 海浪 - Wave",
        "🌸 樱花 - Sakura",
        "🍀 四叶草 - Clover",
        "🌻 向日葵 - Sunflower",
        "🌺 芙蓉花 - Hibiscus",
        "🎄 圣诞树 - Christmas Tree",
        "🌴 棕榈树 - Palm Tree",
    ]
    for item in items:
        t = u(item)
        dll.AddListItem(listbox, t, len(t))

    # 设置选中回调
    dll.SetListBoxCallback(listbox, _listbox_cb)

    # 默认选中第一项
    dll.SetSelectedIndex(listbox, 0)

    # 按钮组
    btns = [
        ("➕", "添加项", 440, 50, ARGB(255,64,158,255)),
        ("🗑️", "删除选中", 440, 100, ARGB(255,245,108,108)),
        ("📖", "读取属性", 440, 150, ARGB(255,103,194,58)),
        ("🧹", "清空列表", 440, 200, ARGB(255,230,162,60)),
        ("📊", "统计信息", 440, 250, ARGB(255,144,147,153)),
    ]
    btn_ids = []
    for emoji, text, x, y, color in btns:
        e = u(emoji)
        t = u(text)
        bid = dll.create_emoji_button_bytes(main_win, e, len(e), t, len(t), x, y, 230, 35, color)
        btn_ids.append(bid)

    btn_add, btn_del, btn_read, btn_clear, btn_count = btn_ids
    dll.set_button_click_callback(_btn_cb)

    # 读取属性并打印
    print(f"\n--- 📋 列表框属性 ---")
    print(f"项目数: {dll.GetListItemCount(listbox)}")
    print(f"选中索引: {dll.GetSelectedIndex(listbox)}")
    for i in range(min(3, dll.GetListItemCount(listbox))):
        size = dll.GetListItemText(listbox, i, None, 0)
        if size > 0:
            buf = ctypes.create_string_buffer(size)
            dll.GetListItemText(listbox, i, buf, size)
            print(f"  项[{i}]: {buf.raw[:size].decode('utf-8', errors='replace')}")

    # 信息标签
    info = u("📋 列表框支持：添加/删除项、选中回调、读取文本 | 🖱️ 点击选中项目")
    dll.CreateLabel(main_win, 20, 450, 660, 50, info, len(info),
        ARGB(255,144,147,153), ARGB(0,0,0,0), font, len(font), 12, 0, 0, 0, 0, 1)

    dll.set_message_loop_main_window(main_win)
    print("\n✅ 进入消息循环...")
    dll.run_message_loop()
    print("程序退出。")

if __name__ == "__main__":
    main()
