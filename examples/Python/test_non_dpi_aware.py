"""模拟非DPI-aware程序测试resize布局"""
import ctypes
from ctypes import CFUNCTYPE, c_int, Structure
import sys, os, time, threading
sys.path.insert(0, os.path.dirname(__file__))

# 关键：在加载DLL前设置为非DPI-aware
try:
    ctypes.windll.user32.SetProcessDpiAwarenessContext(c_int(-1))  # DPI_AWARENESS_CONTEXT_UNAWARE
    print("已设置为非DPI-aware模式")
except:
    print("无法设置DPI模式，可能已经设置过")

dll = ctypes.CDLL('./emoji_window.dll')
user32 = ctypes.windll.user32

for name, res, args in [
    ('create_window_bytes_ex', c_int, [ctypes.c_void_p, c_int, c_int, c_int, c_int, c_int, c_int, c_int]),
    ('set_message_loop_main_window', None, [c_int]),
    ('run_message_loop', c_int, []),
    ('SetWindowResizeCallback', None, [ctypes.c_void_p]),
    ('CreateTabControl', c_int, [c_int, c_int, c_int, c_int, c_int]),
    ('SetTabControlBounds', c_int, [c_int, c_int, c_int, c_int, c_int]),
    ('SetTabItemSize', c_int, [c_int, c_int, c_int]),
    ('SetTabClosable', c_int, [c_int, c_int]),
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
    ('SetTabContentBgColor', c_int, [c_int, c_int, c_int]),
    ('SetTitleBarTextColor', c_int, [c_int, c_int]),
    ('destroy_window', None, [c_int]),
]:
    fn = getattr(dll, name)
    if res: fn.restype = res
    if args: fn.argtypes = args

RESIZE_CB = CFUNCTYPE(None, c_int, c_int, c_int)

class RECT(Structure):
    _fields_ = [("l",c_int),("t",c_int),("r",c_int),("b",c_int)]

STATUS_H = 28
TITLEBAR_H = 30
hwnd = tab_ctrl = status_label = progress_bar = btn_new_tab = 0

def argb(a,r,g,b): return (a<<24)|(r<<16)|(g<<8)|b
def rgb(r,g,b): return (r<<16)|(g<<8)|b
def buf(data):
    if isinstance(data, str): data = data.encode('utf-8')
    return ctypes.create_string_buffer(data), len(data)

results = []

def on_resize(wnd, w, h):
    if wnd != hwnd: return
    
    tab_w = w - 44
    tab_h = h - STATUS_H - TITLEBAR_H
    status_y = tab_h + TITLEBAR_H
    
    dll.SetTabControlBounds(tab_ctrl, 0, 0, tab_w, tab_h)
    dll.SetLabelBounds(status_label, 0, status_y, w - 160, STATUS_H)
    dll.SetProgressBarBounds(progress_bar, w - 160, status_y, 160, STATUS_H)
    dll.SetButtonBounds(btn_new_tab, tab_w + 4, 2, 34, 30)
    
    wr, tr, lr, pr = RECT(), RECT(), RECT(), RECT()
    user32.GetWindowRect(wnd, ctypes.byref(wr))
    user32.GetWindowRect(tab_ctrl, ctypes.byref(tr))
    user32.GetWindowRect(status_label, ctypes.byref(lr))
    user32.GetWindowRect(progress_bar, ctypes.byref(pr))
    
    win_w = wr.r - wr.l
    win_h = wr.b - wr.t
    tab_b = tr.b - wr.t
    label_t = lr.t - wr.t
    prog_r = pr.r - wr.l
    prog_b = pr.b - wr.t
    
    gap = label_t - tab_b
    issues = []
    if gap < 0: issues.append(f"TabCtrl遮挡状态栏(gap={gap})")
    if prog_r > win_w: issues.append(f"进度条超右(prog_r={prog_r}>win_w={win_w})")
    if prog_b > win_h: issues.append(f"进度条超底(prog_b={prog_b}>win_h={win_h})")
    if label_t + STATUS_H > win_h: issues.append(f"状态栏超底")
    
    status = "OK" if not issues else "FAIL"
    r = {'w':w,'h':h,'win_w':win_w,'win_h':win_h,'gap':gap,'status':status,'issues':issues}
    results.append(r)
    print(f"[{status}] cb:{w}x{h} win:{win_w}x{win_h} gap={gap} {'; '.join(issues)}")

resize_cb = RESIZE_CB(on_resize)

def resize_and_quit():
    time.sleep(1.5)
    for w, h in [(1000, 700), (1400, 900), (800, 600), (1200, 800)]:
        user32.MoveWindow(hwnd, 100, 100, w, h, True)
        time.sleep(0.5)
    time.sleep(0.5)
    user32.PostMessageA(hwnd, 0x0010, 0, 0)

def main():
    global hwnd, tab_ctrl, status_label, progress_bar, btn_new_tab
    
    tb, tl = buf("测试窗口")
    hwnd = dll.create_window_bytes_ex(tb, tl, -1, -1, 1200, 800, rgb(45,45,48), argb(255,240,240,240))
    
    tab_ctrl = dll.CreateTabControl(hwnd, 0, 0, 1156, 730)
    dll.SetTabItemSize(tab_ctrl, 180, 34)
    dll.SetTabClosable(tab_ctrl, 1)
    
    rb, rl = buf("就绪")
    fb, fl = buf("微软雅黑")
    status_label = dll.CreateLabel(hwnd, 0, 740, 1000, STATUS_H, rb, rl, argb(255,0,0,0), argb(255,245,245,245), fb, fl, 11, 0,0,0,0,0)
    progress_bar = dll.CreateProgressBar(hwnd, 1000, 740, 160, STATUS_H, 100, argb(255,64,158,255), argb(255,230,230,230), 1, argb(255,255,255,255))
    
    eb = ctypes.create_string_buffer(b'\xe2\x9e\x95')
    empty = ctypes.create_string_buffer(b'')
    btn_new_tab = dll.create_emoji_button_bytes(hwnd, eb, 3, empty, 0, 1160, 2, 34, 30, argb(255,222,225,230))
    
    dll.SetWindowResizeCallback(resize_cb)
    dll.set_message_loop_main_window(hwnd)
    
    t = threading.Thread(target=resize_and_quit, daemon=True)
    t.start()
    
    print("非DPI-aware模式测试中...")
    dll.run_message_loop()
    
    print("\n" + "=" * 60)
    ok = all(r['status'] == 'OK' for r in results)
    print(f"结果: {'PASS' if ok else 'FAIL'} ({len(results)} 次resize)")
    print("=" * 60)
    return ok

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
