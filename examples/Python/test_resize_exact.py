"""精确测试resize回调参数与控件坐标的关系"""
import ctypes
from ctypes import CFUNCTYPE, c_int, c_uint
import sys, os, time
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

RESIZE_CB = CFUNCTYPE(None, c_int, c_int, c_int)

hwnd = 0
tab = 0
label = 0
progress = 0
STATUS_H = 28

def argb(a,r,g,b): return (a<<24)|(r<<16)|(g<<8)|b
def rgb(r,g,b): return (r<<16)|(g<<8)|b
def buf(s):
    b = s if isinstance(s, bytes) else s.encode('utf-8')
    return ctypes.create_string_buffer(b), len(b)

def on_resize(wnd, w, h):
    if wnd != hwnd: return
    
    # 用回调参数直接布局
    tab_w = w - 44
    tab_h = h - STATUS_H
    
    dll.SetTabControlBounds(tab, 0, 0, tab_w, tab_h)
    dll.SetLabelBounds(label, 0, tab_h, w - 160, STATUS_H)
    dll.SetProgressBarBounds(progress, w - 160, tab_h, 160, STATUS_H)
    
    # 用GetWindowRect验证实际位置
    class RECT(ctypes.Structure):
        _fields_ = [("l",c_int),("t",c_int),("r",c_int),("b",c_int)]
    
    tr, lr, pr, wr = RECT(), RECT(), RECT(), RECT()
    user32.GetWindowRect(tab, ctypes.byref(tr))
    user32.GetWindowRect(label, ctypes.byref(lr))
    user32.GetWindowRect(progress, ctypes.byref(pr))
    user32.GetWindowRect(wnd, ctypes.byref(wr))
    
    win_h = wr.b - wr.t
    tab_bottom = tr.b - wr.t  # TabControl底部相对窗口顶部
    label_top = lr.t - wr.t   # 状态栏顶部相对窗口顶部
    prog_top = pr.t - wr.t
    
    info = (f"cb:w={w},h={h} | win_h={win_h} | "
            f"tab_bot={tab_bottom} label_top={label_top} prog_top={prog_top} | "
            f"gap={label_top - tab_bottom}")
    print(info)
    
    ib, il = buf(info)
    dll.SetLabelText(label, ib, il)

resize_cb = RESIZE_CB(on_resize)

def main():
    global hwnd, tab, label, progress
    
    tb, tl = buf("测试窗口".encode('utf-8'))
    hwnd = dll.create_window_bytes_ex(tb, tl, -1, -1, 1200, 800, rgb(45,45,48), argb(255,240,240,240))
    
    tab = dll.CreateTabControl(hwnd, 0, 0, 1156, 730)
    
    rb, rl = buf("就绪")
    fb, fl = buf("微软雅黑")
    label = dll.CreateLabel(hwnd, 0, 740, 1000, STATUS_H, rb, rl, argb(255,0,0,0), argb(255,245,245,245), fb, fl, 11, 0,0,0,0,0)
    progress = dll.CreateProgressBar(hwnd, 1000, 740, 160, STATUS_H, 100, argb(255,64,158,255), argb(255,230,230,230), 1, argb(255,255,255,255))
    
    dll.SetWindowResizeCallback(resize_cb)
    dll.set_message_loop_main_window(hwnd)
    print("拖动窗口查看输出...")
    dll.run_message_loop()

if __name__ == "__main__":
    main()
