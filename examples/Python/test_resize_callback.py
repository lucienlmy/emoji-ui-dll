"""
测试窗口大小改变回调的参数含义
确定回调传入的新宽度/新高度是窗口尺寸还是客户区尺寸
"""
import ctypes
from ctypes import wintypes, CFUNCTYPE, c_int
import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))

try:
    dll = ctypes.CDLL('./emoji_window.dll')
except OSError:
    print("错误: 无法加载emoji_window.dll")
    sys.exit(1)

# Win32 API
user32 = ctypes.windll.user32

class RECT(ctypes.Structure):
    _fields_ = [("left", c_int), ("top", c_int), ("right", c_int), ("bottom", c_int)]

# DLL 函数
dll.create_window_bytes_ex.restype = c_int
dll.create_window_bytes_ex.argtypes = [ctypes.c_void_p, c_int, c_int, c_int, c_int, c_int, c_int, c_int]

dll.set_message_loop_main_window.argtypes = [c_int]
dll.run_message_loop.restype = c_int

dll.SetWindowResizeCallback.argtypes = [ctypes.c_void_p]

dll.CreateLabel.restype = c_int
dll.SetLabelText.argtypes = [c_int, ctypes.c_void_p, c_int]

# 回调类型
RESIZE_CB = CFUNCTYPE(None, c_int, c_int, c_int)

hwnd = 0
label = 0

def on_resize(window_handle, new_w, new_h):
    global hwnd
    if window_handle != hwnd:
        return
    
    # 获取客户区
    rc = RECT()
    user32.GetClientRect(window_handle, ctypes.byref(rc))
    client_w = rc.right
    client_h = rc.bottom
    
    # 获取窗口矩形
    wr = RECT()
    user32.GetWindowRect(window_handle, ctypes.byref(wr))
    win_w = wr.right - wr.left
    win_h = wr.bottom - wr.top
    
    info = f"callback: {new_w}x{new_h} | client: {client_w}x{client_h} | window: {win_w}x{win_h}"
    print(info)
    
    # 显示到标签
    info_bytes = info.encode('utf-8')
    buf = ctypes.create_string_buffer(info_bytes)
    dll.SetLabelText(label, buf, len(info_bytes))

resize_cb = RESIZE_CB(on_resize)

def test_resize():
    global hwnd, label
    
    print("=" * 60)
    print("测试窗口大小改变回调参数")
    print("=" * 60)
    
    title = "测试窗口".encode('utf-8')
    title_buf = ctypes.create_string_buffer(title)
    hwnd = dll.create_window_bytes_ex(title_buf, len(title), -1, -1, 800, 600, 0, 0)
    
    if hwnd == 0:
        print("创建窗口失败")
        return False
    
    print(f"窗口句柄: {hwnd}")
    print(f"创建参数: 800x600")
    
    # 获取初始客户区
    rc = RECT()
    user32.GetClientRect(hwnd, ctypes.byref(rc))
    print(f"初始客户区: {rc.right}x{rc.bottom}")
    
    wr = RECT()
    user32.GetWindowRect(hwnd, ctypes.byref(wr))
    print(f"初始窗口矩形: {wr.right - wr.left}x{wr.bottom - wr.top}")
    
    # 创建标签显示信息
    text = "拖动窗口边缘查看回调参数".encode('utf-8')
    text_buf = ctypes.create_string_buffer(text)
    font = "微软雅黑".encode('utf-8')
    font_buf = ctypes.create_string_buffer(font)
    
    label = dll.CreateLabel(hwnd, 10, 10, 780, 40, text_buf, len(text), 
                           0xFF000000, 0xFFFFFFFF, font_buf, len(font), 14, 0, 0, 0, 0, 1)
    
    dll.SetWindowResizeCallback(resize_cb)
    dll.set_message_loop_main_window(hwnd)
    
    print("\n请拖动窗口边缘改变大小，观察控制台输出...")
    print("关闭窗口退出测试\n")
    
    dll.run_message_loop()
    return True

if __name__ == "__main__":
    success = test_resize()
    sys.exit(0 if success else 1)
