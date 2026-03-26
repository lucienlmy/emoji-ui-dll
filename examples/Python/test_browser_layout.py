"""
测试多标签浏览器布局
验证窗口resize时所有控件位置是否正确
"""
import ctypes
from ctypes import wintypes, CFUNCTYPE, c_int, c_uint, c_float
import sys, os

sys.path.insert(0, os.path.dirname(__file__))

dll = ctypes.CDLL('./emoji_window.dll')
user32 = ctypes.windll.user32

# 函数原型
dll.create_window_bytes_ex.restype = c_int
dll.create_window_bytes_ex.argtypes = [ctypes.c_void_p, c_int, c_int, c_int, c_int, c_int, c_int, c_int]
dll.set_message_loop_main_window.argtypes = [c_int]
dll.run_message_loop.restype = c_int
dll.SetWindowResizeCallback.argtypes = [ctypes.c_void_p]
dll.CreateTabControl.restype = c_int
dll.CreateTabControl.argtypes = [c_int, c_int, c_int, c_int, c_int]
dll.AddTabItem.restype = c_int
dll.AddTabItem.argtypes = [c_int, ctypes.c_void_p, c_int, c_int]
dll.GetTabContentWindow.restype = c_int
dll.GetTabContentWindow.argtypes = [c_int, c_int]
dll.SetTabControlBounds.restype = c_int
dll.SetTabControlBounds.argtypes = [c_int, c_int, c_int, c_int, c_int]
dll.SetTabItemSize.argtypes = [c_int, c_int, c_int]
dll.SetTabClosable.argtypes = [c_int, c_int]
dll.SetTabDraggable.argtypes = [c_int, c_int]
dll.SetTabScrollable.argtypes = [c_int, c_int]
dll.SetTabCallback.argtypes = [c_int, ctypes.c_void_p]
dll.CreateLabel.restype = c_int
dll.SetLabelText.argtypes = [c_int, ctypes.c_void_p, c_int]
dll.SetLabelBounds.argtypes = [c_int, c_int, c_int, c_int, c_int]
dll.CreateProgressBar.restype = c_int
dll.SetProgressBarBounds.argtypes = [c_int, c_int, c_int, c_int, c_int]
dll.CreateEditBox.restype = c_int
dll.SetEditBoxBounds.argtypes = [c_int, c_int, c_int, c_int, c_int]
dll.create_emoji_button_bytes.restype = c_int
dll.SetButtonBounds.argtypes = [c_int, c_int, c_int, c_int, c_int]

RESIZE_CB = CFUNCTYPE(None, c_int, c_int, c_int)
BTN_CB = CFUNCTYPE(None, c_int, c_int)
TAB_CB = CFUNCTYPE(None, c_int, c_int)

STATUS_H = 28
NAV_H = 44

hwnd = 0
tab_ctrl = 0
status_label = 0
progress_bar = 0
btn_new_tab = 0
tab_editboxes = []
tab_fav_btns = []
tab_cef_containers = []

def to_argb(a, r, g, b):
    return (a << 24) | (r << 16) | (g << 8) | b

def to_rgb(r, g, b):
    return (r << 16) | (g << 8) | b

def make_buf(data):
    return ctypes.create_string_buffer(bytes(data))

def add_tab(url="https://www.baidu.com"):
    global tab_ctrl
    title = b'\xf0\x9f\x8c\x90 ' + "新标签页".encode('utf-8')
    buf = make_buf(title)
    idx = dll.GetTabCount(tab_ctrl)
    dll.AddTabItem(tab_ctrl, buf, len(title), 0)
    content = dll.GetTabContentWindow(tab_ctrl, idx)
    dll.SetTabContentBgColor(tab_ctrl, idx, to_argb(255,255,255,255))

    # 导航按钮
    empty = make_buf(b'')
    for emoji_bytes, x in [(b'\xe2\x97\x80', 4), (b'\xe2\x96\xb6', 44),
                            (b'\xf0\x9f\x94\x84', 84), (b'\xf0\x9f\x8f\xa0', 124)]:
        eb = make_buf(emoji_bytes)
        dll.create_emoji_button_bytes(content, eb, len(emoji_bytes), empty, 0, x, 4, 36, 36, to_argb(255,241,243,244))

    # 地址栏
    url_bytes = url.encode('utf-8')
    url_buf = make_buf(url_bytes)
    font = make_buf("Segoe UI".encode('utf-8'))
    editbox = dll.CreateEditBox(content, 168, 6, 900, 32, url_buf, len(url_bytes),
        to_argb(255,32,33,36), to_argb(255,241,243,244), font, 8, 13, 0,0,0,0, 0,0,0,1,1)

    # 收藏按钮
    star = make_buf(b'\xe2\xad\x90')
    fav_btn = dll.create_emoji_button_bytes(content, star, 3, empty, 0, 1076, 4, 36, 36, to_argb(255,241,243,244))

    # CEF容器
    cef = user32.CreateWindowExA(0, b"Static", b"", 0x52000000, 0, NAV_H, 1160, 680, content, 0, 0, 0)

    tab_editboxes.append(editbox)
    tab_fav_btns.append(fav_btn)
    tab_cef_containers.append(cef)
    dll.SelectTab(tab_ctrl, idx)

def on_resize(wnd, w, h):
    if wnd != hwnd:
        return

    tab_w = w - 44
    tab_h = h - STATUS_H

    # 状态栏和进度条
    dll.SetLabelBounds(status_label, 0, tab_h, w - 160, STATUS_H)
    dll.SetProgressBarBounds(progress_bar, w - 160, tab_h, 160, STATUS_H)

    # TabControl
    dll.SetTabControlBounds(tab_ctrl, 0, 0, tab_w, tab_h)

    # ➕ 按钮
    dll.SetButtonBounds(btn_new_tab, tab_w + 4, 2, 34, 30)

    # Tab内容
    content_w = tab_w
    content_h = tab_h - 38
    addr_w = max(content_w - 224, 100)

    count = dll.GetTabCount(tab_ctrl)
    for i in range(min(count, len(tab_editboxes))):
        if tab_editboxes[i]:
            dll.SetEditBoxBounds(tab_editboxes[i], 168, 6, addr_w, 32)
        if tab_fav_btns[i]:
            dll.SetButtonBounds(tab_fav_btns[i], 168 + addr_w + 8, 4, 36, 36)
        if tab_cef_containers[i]:
            user32.MoveWindow(tab_cef_containers[i], 0, NAV_H, content_w, content_h - NAV_H, True)

    # 调试输出
    info = f"w={w} h={h} tab={tab_w}x{tab_h} status_y={tab_h}".encode('utf-8')
    buf = ctypes.create_string_buffer(info)
    dll.SetLabelText(status_label, buf, len(info))

resize_cb = RESIZE_CB(on_resize)

def on_btn(btn_id, parent):
    if btn_id == btn_new_tab:
        add_tab()

btn_cb = BTN_CB(on_btn)

def main():
    global hwnd, tab_ctrl, status_label, progress_bar, btn_new_tab

    title = b'\xf0\x9f\x8c\x90 ' + "多标签浏览器".encode('utf-8')
    buf = make_buf(title)
    hwnd = dll.create_window_bytes_ex(buf, len(title), -1, -1, 1200, 800, to_rgb(45,45,48), to_argb(255,240,240,240))

    dll.SetTitleBarTextColor(hwnd, to_argb(255,255,255,255))

    # TabControl
    tab_ctrl = dll.CreateTabControl(hwnd, 0, 0, 1156, 730)
    dll.SetTabItemSize(tab_ctrl, 180, 34)
    dll.SetTabClosable(tab_ctrl, 1)
    dll.SetTabDraggable(tab_ctrl, 1)
    dll.SetTabScrollable(tab_ctrl, 1)

    dll.SetWindowResizeCallback(resize_cb)
    dll.set_button_click_callback(btn_cb)

    # 状态栏（在TabControl之后创建）
    ready = "就绪".encode('utf-8')
    font = "微软雅黑".encode('utf-8')
    rb = make_buf(ready)
    fb = make_buf(font)
    status_label = dll.CreateLabel(hwnd, 0, 740, 1000, STATUS_H, rb, len(ready),
        to_argb(255,96,98,102), to_argb(255,245,245,245), fb, len(font), 11, 0,0,0,0,0)
    progress_bar = dll.CreateProgressBar(hwnd, 1000, 740, 160, STATUS_H, 100,
        to_argb(255,64,158,255), to_argb(255,230,230,230), 1, to_argb(255,255,255,255))

    add_tab()

    # ➕ 按钮
    plus = make_buf(b'\xe2\x9e\x95')
    empty = make_buf(b'')
    btn_new_tab = dll.create_emoji_button_bytes(hwnd, plus, 3, empty, 0, 1160, 2, 34, 30, to_argb(255,222,225,230))

    dll.set_message_loop_main_window(hwnd)
    print("窗口已创建，请拖动窗口边缘测试resize...")
    dll.run_message_loop()

if __name__ == "__main__":
    main()
