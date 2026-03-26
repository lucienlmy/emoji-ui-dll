"""自动验证resize布局：创建窗口，程序化resize，检查gap值"""
import ctypes
from ctypes import CFUNCTYPE, c_int, c_uint, Structure
import sys, os, time, threading
sys.path.insert(0, os.path.dirname(__file__))

dll = ctypes.CDLL('./emoji_window.dll')
user32 = ctypes.windll.user32

dll.create_window_bytes_ex.restype = c_int
dll.create_window_bytes_ex.argtypes = [ctypes.c_void_p, c_int, c_int, c_int, c_int, c_int, c_int, c_int]
dll.set_message_loop_main_window.argtypes = [c_int]
dll.run_message_loop.restype = c_int
dll.SetWindowResizeCallback.argtypes = [ctypes.c_void_p]
dll.CreateLabel.restype = c_int
dll.SetLabelText.argtypes = [c_int, ctypes.c_void_p, c_int]
dll.SetLabelBounds.argtypes = [c_int, c_int, c_int, c_int, c_int]
dll.CreateTabControl.restype = c_int
dll.SetTabControlBounds.restype = c_int
dll.SetTabControlBounds.argtypes = [c_int, c_int, c_int, c_int, c_int]
dll.CreateProgressBar.restype = c_int
dll.SetProgressBarBounds.argtypes = [c_int, c_int, c_int, c_int, c_int]
dll.destroy_window.argtypes = [c_int]

RESIZE_CB = CFUNCTYPE(None, c_int, c_int, c_int)

class RECT(Structure):
    _fields_ = [("l",c_int),("t",c_int),("r",c_int),("b",c_int)]

hwnd = 0
tab = 0
label = 0
progress = 0
STATUS_H = 28
TITLEBAR_H = 30  # 自绘标题栏高度（SetTabControlBounds内部会加这个偏移）
results = []

def argb(a,r,g,b): return (a<<24)|(r<<16)|(g<<8)|b
def rgb(r,g,b): return (r<<16)|(g<<8)|b
def buf(s):
    b = s if isinstance(s, bytes) else s.encode('utf-8')
    return ctypes.create_string_buffer(b), len(b)

def on_resize(wnd, w, h):
    if wnd != hwnd: return
    
    tab_w = w - 44
    # TabControl: SetTabControlBounds内部加tb_offset到Y，所以实际占用[tb_offset, tb_offset+tab_h]
    # 状态栏: parent_drawn标签用D2D绝对坐标，需要放在TabControl下方
    tab_h = h - STATUS_H - TITLEBAR_H
    status_y = tab_h + TITLEBAR_H  # 状态栏Y = TabControl底部 = tb_offset + tab_h
    
    dll.SetTabControlBounds(tab, 0, 0, tab_w, tab_h)
    dll.SetLabelBounds(label, 0, status_y, w - 160, STATUS_H)
    dll.SetProgressBarBounds(progress, w - 160, status_y, 160, STATUS_H)
    
    tr, lr, wr = RECT(), RECT(), RECT()
    user32.GetWindowRect(tab, ctypes.byref(tr))
    user32.GetWindowRect(label, ctypes.byref(lr))
    user32.GetWindowRect(wnd, ctypes.byref(wr))
    
    tab_bottom = tr.b - wr.t
    label_top = lr.t - wr.t
    gap = label_top - tab_bottom
    
    results.append({
        'cb_w': w, 'cb_h': h,
        'tab_bottom': tab_bottom, 'label_top': label_top,
        'gap': gap
    })

resize_cb = RESIZE_CB(on_resize)

def resize_and_quit():
    """等窗口创建后，程序化改变大小，然后关闭"""
    time.sleep(1)
    
    # 改变窗口大小几次
    for w, h in [(1000, 700), (1400, 900), (800, 600), (1200, 800)]:
        user32.MoveWindow(hwnd, 100, 100, w, h, True)
        time.sleep(0.3)
    
    time.sleep(0.5)
    # 关闭窗口
    user32.PostMessageA(hwnd, 0x0010, 0, 0)  # WM_CLOSE

def main():
    global hwnd, tab, label, progress
    
    tb, tl = buf("验证窗口")
    hwnd = dll.create_window_bytes_ex(tb, tl, -1, -1, 1200, 800, rgb(45,45,48), argb(255,240,240,240))
    
    tab = dll.CreateTabControl(hwnd, 0, 0, 1156, 730)
    
    rb, rl = buf("就绪")
    fb, fl = buf("微软雅黑")
    label = dll.CreateLabel(hwnd, 0, 740, 1000, STATUS_H, rb, rl, argb(255,0,0,0), argb(255,245,245,245), fb, fl, 11, 0,0,0,0,0)
    progress = dll.CreateProgressBar(hwnd, 1000, 740, 160, STATUS_H, 100, argb(255,64,158,255), argb(255,230,230,230), 1, argb(255,255,255,255))
    
    dll.SetWindowResizeCallback(resize_cb)
    dll.set_message_loop_main_window(hwnd)
    
    # 在后台线程中改变窗口大小
    t = threading.Thread(target=resize_and_quit, daemon=True)
    t.start()
    
    dll.run_message_loop()
    
    # 输出结果
    print("=" * 70)
    print(f"共收到 {len(results)} 次resize回调")
    print("=" * 70)
    
    all_ok = True
    for i, r in enumerate(results):
        status = "OK" if r['gap'] >= 0 else "FAIL"
        if r['gap'] < 0:
            all_ok = False
        print(f"  [{status}] cb:w={r['cb_w']},h={r['cb_h']} tab_bot={r['tab_bottom']} label_top={r['label_top']} gap={r['gap']}")
    
    print("=" * 70)
    if all_ok:
        print("PASS: 所有resize事件中状态栏都在TabControl下方（gap >= 0）")
    else:
        print("FAIL: 存在TabControl遮挡状态栏的情况（gap < 0）")
    print("=" * 70)
    
    return all_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
