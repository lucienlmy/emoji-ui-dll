"""
测试标签页外观函数
测试 SetTabItemSize、SetTabFont、SetTabColors、SetTabIndicatorColor、SetTabPadding
覆盖正常调用、无效句柄、无效参数等场景

测试的功能点:
- SetTabItemSize: 设置标签页宽度和高度
- SetTabFont: 设置标签页字体名称和字号
- SetTabColors: 设置选中/未选中的背景色和文字色
- SetTabIndicatorColor: 设置选中指示条颜色
- SetTabPadding: 设置标签页水平和垂直内边距

预期结果:
- 有效参数调用返回 0
- 无效句柄调用返回 -1
- 无效参数调用返回 -1
"""
import ctypes
from ctypes import wintypes
import sys
import os
import time

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

# 加载DLL
try:
    dll = ctypes.CDLL('./emoji_window.dll')
except OSError:
    print("错误: 无法加载 emoji_window.dll")
    sys.exit(1)

# ========== 定义函数原型 ==========

# 创建窗口
dll.create_window.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
dll.create_window.restype = wintypes.HWND

# 销毁窗口
dll.destroy_window.argtypes = [wintypes.HWND]
dll.destroy_window.restype = None

# 创建 TabControl
dll.CreateTabControl.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
dll.CreateTabControl.restype = wintypes.HWND

# 添加 Tab 页
dll.AddTabItem.argtypes = [wintypes.HWND, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int, wintypes.HWND]
dll.AddTabItem.restype = ctypes.c_int

# 销毁 TabControl
dll.DestroyTabControl.argtypes = [wintypes.HWND]
dll.DestroyTabControl.restype = None

# SetTabItemSize
dll.SetTabItemSize.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_int]
dll.SetTabItemSize.restype = ctypes.c_int

# SetTabFont
dll.SetTabFont.argtypes = [wintypes.HWND, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int, ctypes.c_float]
dll.SetTabFont.restype = ctypes.c_int

# SetTabColors
dll.SetTabColors.argtypes = [wintypes.HWND, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32, ctypes.c_uint32]
dll.SetTabColors.restype = ctypes.c_int

# SetTabIndicatorColor
dll.SetTabIndicatorColor.argtypes = [wintypes.HWND, ctypes.c_uint32]
dll.SetTabIndicatorColor.restype = ctypes.c_int

# SetTabPadding
dll.SetTabPadding.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_int]
dll.SetTabPadding.restype = ctypes.c_int


def make_utf8_bytes(text):
    """将 Python 字符串转换为 UTF-8 字节数组指针和长度"""
    encoded = text.encode('utf-8')
    arr = (ctypes.c_ubyte * len(encoded))(*encoded)
    return arr, len(encoded)


def test_tab_appearance():
    """测试标签页外观函数"""
    print("=" * 60)
    print("测试标签页外观函数")
    print("=" * 60)

    all_passed = True
    INVALID_HWND = wintypes.HWND(0x12345678)

    # 创建测试窗口和 TabControl
    print("\n[准备] 创建测试窗口和 TabControl...")
    hwnd = dll.create_window(b"Test Window", 800, 600)
    if not hwnd:
        print("  错误: 无法创建窗口")
        return False

    hTab = dll.CreateTabControl(hwnd, 10, 10, 780, 560)
    if not hTab:
        print("  错误: 无法创建 TabControl")
        dll.destroy_window(hwnd)
        return False

    # 添加一个标签页
    title_bytes, title_len = make_utf8_bytes("测试页")
    dll.AddTabItem(hTab, title_bytes, title_len, None)
    print("  创建成功")

    # ========== 测试 SetTabItemSize ==========
    print("\n--- 测试 SetTabItemSize ---")

    # 正常调用
    ret = dll.SetTabItemSize(hTab, 150, 40)
    if ret == 0:
        print("  [通过] 正常调用 (150, 40) 返回 0")
    else:
        print(f"  [失败] 正常调用 (150, 40) 返回 {ret}，期望 0")
        all_passed = False

    # 无效句柄
    ret = dll.SetTabItemSize(INVALID_HWND, 150, 40)
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
        all_passed = False

    # width <= 0
    ret = dll.SetTabItemSize(hTab, 0, 40)
    if ret == -1:
        print("  [通过] width=0 返回 -1")
    else:
        print(f"  [失败] width=0 返回 {ret}，期望 -1")
        all_passed = False

    # height <= 0
    ret = dll.SetTabItemSize(hTab, 150, -1)
    if ret == -1:
        print("  [通过] height=-1 返回 -1")
    else:
        print(f"  [失败] height=-1 返回 {ret}，期望 -1")
        all_passed = False

    # 负 width
    ret = dll.SetTabItemSize(hTab, -10, 40)
    if ret == -1:
        print("  [通过] width=-10 返回 -1")
    else:
        print(f"  [失败] width=-10 返回 {ret}，期望 -1")
        all_passed = False

    # ========== 测试 SetTabFont ==========
    print("\n--- 测试 SetTabFont ---")

    # 正常调用
    font_bytes, font_len = make_utf8_bytes("Microsoft YaHei")
    ret = dll.SetTabFont(hTab, font_bytes, font_len, ctypes.c_float(16.0))
    if ret == 0:
        print("  [通过] 正常调用 ('Microsoft YaHei', 16.0) 返回 0")
    else:
        print(f"  [失败] 正常调用返回 {ret}，期望 0")
        all_passed = False

    # 中文字体名
    font_bytes2, font_len2 = make_utf8_bytes("微软雅黑")
    ret = dll.SetTabFont(hTab, font_bytes2, font_len2, ctypes.c_float(14.0))
    if ret == 0:
        print("  [通过] 中文字体名 ('微软雅黑', 14.0) 返回 0")
    else:
        print(f"  [失败] 中文字体名返回 {ret}，期望 0")
        all_passed = False

    # 无效句柄
    ret = dll.SetTabFont(INVALID_HWND, font_bytes, font_len, ctypes.c_float(16.0))
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
        all_passed = False

    # fontName 为 NULL
    ret = dll.SetTabFont(hTab, None, 10, ctypes.c_float(16.0))
    if ret == -1:
        print("  [通过] fontName=NULL 返回 -1")
    else:
        print(f"  [失败] fontName=NULL 返回 {ret}，期望 -1")
        all_passed = False

    # fontNameLen <= 0
    ret = dll.SetTabFont(hTab, font_bytes, 0, ctypes.c_float(16.0))
    if ret == -1:
        print("  [通过] fontNameLen=0 返回 -1")
    else:
        print(f"  [失败] fontNameLen=0 返回 {ret}，期望 -1")
        all_passed = False

    # fontSize <= 0
    ret = dll.SetTabFont(hTab, font_bytes, font_len, ctypes.c_float(0.0))
    if ret == -1:
        print("  [通过] fontSize=0 返回 -1")
    else:
        print(f"  [失败] fontSize=0 返回 {ret}，期望 -1")
        all_passed = False

    # fontSize 负数
    ret = dll.SetTabFont(hTab, font_bytes, font_len, ctypes.c_float(-5.0))
    if ret == -1:
        print("  [通过] fontSize=-5 返回 -1")
    else:
        print(f"  [失败] fontSize=-5 返回 {ret}，期望 -1")
        all_passed = False

    # ========== 测试 SetTabColors ==========
    print("\n--- 测试 SetTabColors ---")

    # 正常调用
    ret = dll.SetTabColors(hTab, 0xFFFF0000, 0xFF00FF00, 0xFF0000FF, 0xFF333333)
    if ret == 0:
        print("  [通过] 正常调用返回 0")
    else:
        print(f"  [失败] 正常调用返回 {ret}，期望 0")
        all_passed = False

    # 无效句柄
    ret = dll.SetTabColors(INVALID_HWND, 0xFFFF0000, 0xFF00FF00, 0xFF0000FF, 0xFF333333)
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
        all_passed = False

    # 全零颜色（合法值）
    ret = dll.SetTabColors(hTab, 0x00000000, 0x00000000, 0x00000000, 0x00000000)
    if ret == 0:
        print("  [通过] 全零颜色返回 0（合法值）")
    else:
        print(f"  [失败] 全零颜色返回 {ret}，期望 0")
        all_passed = False

    # ========== 测试 SetTabIndicatorColor ==========
    print("\n--- 测试 SetTabIndicatorColor ---")

    # 正常调用
    ret = dll.SetTabIndicatorColor(hTab, 0xFFFF6600)
    if ret == 0:
        print("  [通过] 正常调用 (0xFFFF6600) 返回 0")
    else:
        print(f"  [失败] 正常调用返回 {ret}，期望 0")
        all_passed = False

    # 无效句柄
    ret = dll.SetTabIndicatorColor(INVALID_HWND, 0xFFFF6600)
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
        all_passed = False

    # ========== 测试 SetTabPadding ==========
    print("\n--- 测试 SetTabPadding ---")

    # 正常调用
    ret = dll.SetTabPadding(hTab, 10, 5)
    if ret == 0:
        print("  [通过] 正常调用 (10, 5) 返回 0")
    else:
        print(f"  [失败] 正常调用返回 {ret}，期望 0")
        all_passed = False

    # 零值（合法）
    ret = dll.SetTabPadding(hTab, 0, 0)
    if ret == 0:
        print("  [通过] 零值 (0, 0) 返回 0")
    else:
        print(f"  [失败] 零值返回 {ret}，期望 0")
        all_passed = False

    # 无效句柄
    ret = dll.SetTabPadding(INVALID_HWND, 10, 5)
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
        all_passed = False

    # horizontal < 0
    ret = dll.SetTabPadding(hTab, -1, 5)
    if ret == -1:
        print("  [通过] horizontal=-1 返回 -1")
    else:
        print(f"  [失败] horizontal=-1 返回 {ret}，期望 -1")
        all_passed = False

    # vertical < 0
    ret = dll.SetTabPadding(hTab, 10, -1)
    if ret == -1:
        print("  [通过] vertical=-1 返回 -1")
    else:
        print(f"  [失败] vertical=-1 返回 {ret}，期望 -1")
        all_passed = False

    # ========== 清理 ==========
    print("\n[清理] 销毁 TabControl 和窗口...")
    dll.DestroyTabControl(hTab)
    dll.destroy_window(hwnd)
    print("  清理完成")

    # ========== 结果 ==========
    print("\n" + "=" * 60)
    if all_passed:
        print("所有测试通过!")
    else:
        print("部分测试失败!")
    print("=" * 60)

    return all_passed


if __name__ == "__main__":
    success = test_tab_appearance()
    sys.exit(0 if success else 1)
