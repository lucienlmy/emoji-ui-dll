"""
完整验证多标签浏览器布局
模拟非DPI-aware行为，验证所有控件位置
"""
import ctypes
from ctypes import CFUNCTYPE, c_int, Structure
import sys, os, time, threading
sys.path.insert(0, os.path.dirname(__file__))

# 模拟非DPI-aware：在加载DLL前取消DPI感知
# ctypes.windll.user32.SetProcessDpiAwarenessContext(-1)  # DPI_AWARENESS_CONTEXT_UNAWARE

dll = ctypes.CDLL('./emoji_window.dll')
user32 = ctypes.windll.user32

# 函数原型
for name, res, args in [
    ('create_window_bytes_ex', c_int, [ctypes.c_void_p, c_int, c_int, c_int, c_int, c_int, c_int, c_int]),
    ('set_message_loop_main_window', None, [c_int]),
    ('run_message_loop', c_int, []),
    ('SetWindowResizeCallback', None, [ctypes.c_void_p]),
    ('CreateTabControl', c_int, [c_int, c_int, c_int, c_int, c_int]),
    ('SetTabControlBounds', c_int, [c_int, c_int, c_int, c_int, c_int]),
    ('SetTabItemSize', c_int, [c_int, c_int, c_int]),
    ('SetTabClosable', c_int, [c_int, c_int]),
    ('SetTabDraggable', c_int, [c_int, c_int]),
    ('SetTabScrollable', c_int, [c_int, c_int]),
    ('AddTabItem', c_int, [c_int, ctypes.c_void_p, c_int, c_int]),
    ('GetTabContentWindow', c_int, [c_int, c_int]),
    ('SelectTab', c_int, [c_int, c_int]),
    ('GetTabCount', c_int, [c_int]),
    ('CreateLabel', c_int, [c_int,c_int,c_int,c_int,c_int,ctypes.c_void_p,c_int,c_int,c_int,ctypes.c_void_p,c_int,c_int,c_int,c_int,c_int,c_int,c_int]),
    ('SetLabelText', None, [c_int, ctypes.c_void_p, c_int]),
    ('SetLabelBounds', None, [c_int, c_int, c_int, c_int, c_int]),
    ('CreateProgressBar', c_int, [c_int,c_int,c_int,c_int,c_int,c_int,c_int,c_int,c_int,c_int]),
    ('SetProgressBarBounds', None, [c_int, c_int, c_int, c_int, c_int]),
    ('create_emoji_button_bytes', c_int, [c_int,ctypes.c_void_p,c_int,ctypes.c_void_p,c_int,c_int,c_int,c_int,c_int,c_int]),
    ('SetButtonBounds', None, [c_int, c_int, c_int, c_int, c_int]),
    ('CreateEditBox', c_int, [c_int,c_int,c_int,c_int,c_int,ctypes.c_void_p,c_int,c_int,c_int,ctypes.c_void_p,c_int,c_int,c_int,c_int,c_int,c_int,c_int,c_int,c_int,c_int,c_int]),
    ('SetEditBoxBounds', None, [c_int, c_int, c_int, c_int, c_int]),
    ('SetTabContentBgColor', c_int, [c_int, c_int, c_int]),
    ('destroy_window', None, [c_int]),
    ('set_button_click_callback', None, [ctypes.c_void_p]),
    ('SetTitleBarTextColor', c_int, [c_int, c_int]),
]:
    fn = getattr(dll, name)
    if res: fn.restype = res
    if args: fn.argtypes = args

RESIZE_CB = CFUNCTYPE(None, c_int, c_int, c_int)
BTN_CB = CFUNCTYPE(None, c_int, c_int)

class RECT(Structure):
    _fields_ = [("l",c_int),("t",c_int),("r",c_int),("b",c_int)]

# 常量
STATUS_H = 28
TITLEBAR_H = 30
NAV_H = 44

# 全局
hwnd = tab_ctrl = status_label = progress_bar = btn_new_tab = 0
tab_editboxes = []
tab_fav_btns = []
tab_cef_containers = []

def argb(a,r,g,b): return (a<<24)|(r<<16)|(g<<8)|b
def rgb(r,g,b): return (r<<16)|(g<<8)|b
def buf(data):
    if isinstance(data, str): data = data.encode('utf-8')
    return ctypes.create_string_buffer(data), len(data)

def create_nav_button(parent, emoji_bytes, x, y, w, h):
    eb = ctypes.create_string_buffer(bytes(emoji_bytes))
    empty = ctypes.create_string_buffer(b'')
    return dll.create_emoji_button_bytes(parent, eb, len(emoji_bytes), empty, 0, x, y, w, h, argb(255,241,243,244))

def add_tab(url="https://www.baidu.com"):
    title = b'\xf0\x9f\x8c\x90 ' + "新标签页".encode('utf-8')
    tb, tl = buf(title)
    idx = dll.GetTabCount(tab_ctrl)
    dll.AddTabItem(tab_ctrl, tb, tl, 0)
    content = dll.GetTabContentWindow(tab_ctrl, idx)
    dll.SetTabContentBgColor(tab_ctrl, idx, argb(255,255,255,255))
    
    create_nav_button(content, [226,151,128], 4, 4, 36, 36)
    create_nav_button(content, [226,150,182], 44, 4, 36, 36)
    create_nav_button(content, [240,159,148,132], 84, 4, 36, 36)
    create_nav_button(content, [240,159,143,160], 124, 4, 36, 36)
    
    ub, ul = buf(url)
    fb, fl = buf("Segoe UI")
    editbox = dll.CreateEditBox(content, 168, 6, 900, 32, ub, ul, argb(255,32,33,36), argb(255,241,243,244), fb, fl, 13, 0,0,0,0, 0,0,0,1,1)
    fav_btn = create_nav_button(content, [226,173,144], 1076, 4, 36, 36)
    cef = user32.CreateWindowExA(0, b"Static", b"", 0x52000000, 0, NAV_H, 1160, 680, content, 0, 0, 0)
    
    tab_editboxes.append(editbox)
    tab_fav_btns.append(fav_btn)
    tab_cef_containers.append(cef)
    dll.SelectTab(tab_ctrl, idx)

def on_resize(wnd, w, h):
    if wnd != hwnd: return
    
    tab_w = w - 44
    tab_h = h - STATUS_H - TITLEBAR_H
    status_y = tab_h + TITLEBAR_H
    
    dll.SetTabControlBounds(tab_ctrl, 0, 0, tab_w, tab_h)
    dll.SetLabelBounds(status_label, 0, status_y, w - 160, STATUS_H)
    dll.SetProgressBarBounds(progress_bar, w - 160, status_y, 160, STATUS_H)
    dll.SetButtonBounds(btn_new_tab, tab_w + 4, 2, 34, 30)
    
    # 调整Tab内容
    content_w = tab_w
    content_h = tab_h - 38
    addr_w = max(content_w - 224, 100)
    
    count = dll.GetTabCount(tab_ctrl)
    for i in range(min(count, len(tab_editboxes))):
        if tab_editboxes[i]: dll.SetEditBoxBounds(tab_editboxes[i], 168, 6, addr_w, 32)
        if tab_fav_btns[i]: dll.SetButtonBounds(tab_fav_btns[i], 168 + addr_w + 8, 4, 36, 36)
        if tab_cef_containers[i]: user32.MoveWindow(tab_cef_containers[i], 0, NAV_H, content_w, max(content_h - NAV_H, 10), True)
    
    # 验证所有控件位置
    wr, tr, lr, pr, br = RECT(), RECT(), RECT(), RECT(), RECT()
    user32.GetWindowRect(wnd, ctypes.byref(wr))
    user32.GetWindowRect(tab_ctrl, ctypes.byref(tr))
    user32.GetWindowRect(status_label, ctypes.byref(lr))
    user32.GetWindowRect(progress_bar, ctypes.byref(pr))
    
    # 获取按钮位置（按钮是D2D绘制的，用GetButtonBounds）
    bx, by, bw, bh = c_int(), c_int(), c_int(), c_int()
    dll.GetButtonBounds(btn_new_tab, ctypes.byref(bx), ctypes.byref(by), ctypes.byref(bw), ctypes.byref(bh))
    
    win_w = wr.r - wr.l
    win_h = wr.b - wr.t
    tab_r = tr.r - wr.l  # TabControl右边缘
    tab_b = tr.b - wr.t  # TabControl底部
    label_t = lr.t - wr.t
    label_vis = 1 if lr.b > lr.t else 0
    prog_t = pr.t - wr.t
    prog_r = pr.r - wr.l
    
    # 检查
    issues = []
    tab_label_gap = label_t - tab_b
    if tab_label_gap < 0: issues.append(f"TabControl遮挡状态栏(gap={tab_label_gap})")
    if prog_r > win_w: issues.append(f"进度条超出右边缘(prog_r={prog_r} > win_w={win_w})")
    if label_t + STATUS_H > win_h: issues.append(f"状态栏超出底部(label_b={label_t+STATUS_H} > win_h={win_h})")
    # 按钮位置检查
    btn_right = bx.value + bw.value
    if btn_right > win_w: issues.append(f"➕按钮超出右边缘(btn_r={btn_right} > win_w={win_w})")
    
    status = "OK" if not issues else "FAIL"
    info = f"[{status}] w={w},h={h} win={win_w}x{win_h} tab_gap={tab_label_gap} btn=({bx.value},{by.value})"
    if issues: info += " " + "; ".join(issues)
    print(info)
    
    ib, il = buf(info)
    dll.SetLabelText(status_label, ib, il)

resize_cb = RESIZE_CB(on_resize)
btn_cb = BTN_CB(lambda bid, phwnd: add_tab() if bid == btn_new_tab else None)

def resize_and_quit():
    time.sleep(1.5)
    for w, h in [(1000, 700), (1400, 900), (800, 600), (1200, 800)]:
        user32.MoveWindow(hwnd, 100, 100, w, h, True)
        time.sleep(0.5)
    time.sleep(0.5)
    user32.PostMessageA(hwnd, 0x0010, 0, 0)

def main():
    global hwnd, tab_ctrl, status_label, progress_bar, btn_new_tab
    
    tb, tl = buf(b'\xf0\x9f\x8c\x90 ' + "多标签浏览器".encode('utf-8'))
    hwnd = dll.create_window_bytes_ex(tb, tl, -1, -1, 1200, 800, rgb(45,45,48), argb(255,240,240,240))
    dll.SetTitleBarTextColor(hwnd, argb(255,255,255,255))
    
    tab_ctrl = dll.CreateTabControl(hwnd, 0, 0, 1156, 730)
    dll.SetTabItemSize(tab_ctrl, 180, 34)
    dll.SetTabClosable(tab_ctrl, 1)
    dll.SetTabDraggable(tab_ctrl, 1)
    dll.SetTabScrollable(tab_ctrl, 1)
    
    rb, rl = buf("就绪")
    fb, fl = buf("微软雅黑")
    status_label = dll.CreateLabel(hwnd, 0, 740, 1000, STATUS_H, rb, rl, argb(255,96,98,102), argb(255,245,245,245), fb, fl, 11, 0,0,0,0,0)
    progress_bar = dll.CreateProgressBar(hwnd, 1000, 740, 160, STATUS_H, 100, argb(255,64,158,255), argb(255,230,230,230), 1, argb(255,255,255,255))
    
    add_tab()
    
    eb = ctypes.create_string_buffer(b'\xe2\x9e\x95')
    empty = ctypes.create_string_buffer(b'')
    btn_new_tab = dll.create_emoji_button_bytes(hwnd, eb, 3, empty, 0, 1160, 2, 34, 30, argb(255,222,225,230))
    
    dll.SetWindowResizeCallback(resize_cb)
    dll.set_button_click_callback(btn_cb)
    dll.set_message_loop_main_window(hwnd)
    
    t = threading.Thread(target=resize_and_quit, daemon=True)
    t.start()
    
    print("自动测试中...")
    dll.run_message_loop()
    print("\n测试完成")

if __name__ == "__main__":
    main()
