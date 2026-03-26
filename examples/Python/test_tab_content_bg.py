"""
测试内容区域背景色函数
测试 SetTabContentBgColor、SetTabContentBgColorAll
覆盖单页设置、全部设置、无效参数等场景

测试的功能点:
- SetTabContentBgColor: 设置指定标签页的内容区域背景色
- SetTabContentBgColorAll: 设置所有标签页的内容区域背景色

预期结果:
- 有效参数调用返回 0
- 无效句柄或越界索引返回 -1
"""
import ctypes
from ctypes import wintypes
import sys
import os

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

# 获取 Tab 数量
dll.GetTabCount.argtypes = [wintypes.HWND]
dll.GetTabCount.restype = ctypes.c_int

# 销毁 TabControl
dll.DestroyTabControl.argtypes = [wintypes.HWND]
dll.DestroyTabControl.restype = None

# SetTabContentBgColor
dll.SetTabContentBgColor.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_uint32]
dll.SetTabContentBgColor.restype = ctypes.c_int

# SetTabContentBgColorAll
dll.SetTabContentBgColorAll.argtypes = [wintypes.HWND, ctypes.c_uint32]
dll.SetTabContentBgColorAll.restype = ctypes.c_int


def make_utf8_bytes(text):
    """将 Python 字符串转换为 UTF-8 字节数组指针和长度"""
    encoded = text.encode('utf-8')
    arr = (ctypes.c_ubyte * len(encoded))(*encoded)
    return arr, len(encoded)


def test_tab_content_bg():
    """测试内容区域背景色函数"""
    print("=" * 60)
    print("测试内容区域背景色函数")
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

    # 添加三个标签页
    for title in ["页面1", "页面2", "页面3"]:
        title_bytes, title_len = make_utf8_bytes(title)
        dll.AddTabItem(hTab, title_bytes, title_len, None)
    print("  创建成功，已添加 3 个标签页")

    # ========== 测试 SetTabContentBgColor ==========
    print("\n--- 测试 SetTabContentBgColor ---")

    # 正常设置单页背景色（红色）
    ret = dll.SetTabContentBgColor(hTab, 0, 0xFFFF0000)
    if ret == 0:
        print("  [通过] 设置 index=0 背景色为红色 返回 0")
    else:
        print(f"  [失败] 设置 index=0 背景色为红色 返回 {ret}，期望 0")
        all_passed = False

    # 设置另一页背景色（蓝色）
    ret = dll.SetTabContentBgColor(hTab, 1, 0xFF0000FF)
    if ret == 0:
        print("  [通过] 设置 index=1 背景色为蓝色 返回 0")
    else:
        print(f"  [失败] 设置 index=1 背景色为蓝色 返回 {ret}，期望 0")
        all_passed = False

    # 设置最后一页背景色（绿色）
    ret = dll.SetTabContentBgColor(hTab, 2, 0xFF00FF00)
    if ret == 0:
        print("  [通过] 设置 index=2 背景色为绿色 返回 0")
    else:
        print(f"  [失败] 设置 index=2 背景色为绿色 返回 {ret}，期望 0")
        all_passed = False

    # 重复设置同一页（白色）
    ret = dll.SetTabContentBgColor(hTab, 0, 0xFFFFFFFF)
    if ret == 0:
        print("  [通过] 重新设置 index=0 背景色为白色 返回 0")
    else:
        print(f"  [失败] 重新设置 index=0 背景色为白色 返回 {ret}，期望 0")
        all_passed = False

    # 无效句柄
    ret = dll.SetTabContentBgColor(INVALID_HWND, 0, 0xFFFF0000)
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
        all_passed = False

    # 越界索引（负数）
    ret = dll.SetTabContentBgColor(hTab, -1, 0xFFFF0000)
    if ret == -1:
        print("  [通过] index=-1 返回 -1")
    else:
        print(f"  [失败] index=-1 返回 {ret}，期望 -1")
        all_passed = False

    # 越界索引（超出范围）
    ret = dll.SetTabContentBgColor(hTab, 100, 0xFFFF0000)
    if ret == -1:
        print("  [通过] index=100 返回 -1")
    else:
        print(f"  [失败] index=100 返回 {ret}，期望 -1")
        all_passed = False

    # ========== 测试 SetTabContentBgColorAll ==========
    print("\n--- 测试 SetTabContentBgColorAll ---")

    # 正常设置所有页背景色（浅灰色）
    ret = dll.SetTabContentBgColorAll(hTab, 0xFFF0F0F0)
    if ret == 0:
        print("  [通过] 设置所有页背景色为浅灰色 返回 0")
    else:
        print(f"  [失败] 设置所有页背景色为浅灰色 返回 {ret}，期望 0")
        all_passed = False

    # 设置所有页为白色（恢复默认）
    ret = dll.SetTabContentBgColorAll(hTab, 0xFFFFFFFF)
    if ret == 0:
        print("  [通过] 设置所有页背景色为白色 返回 0")
    else:
        print(f"  [失败] 设置所有页背景色为白色 返回 {ret}，期望 0")
        all_passed = False

    # 无效句柄
    ret = dll.SetTabContentBgColorAll(INVALID_HWND, 0xFFFF0000)
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
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
    success = test_tab_content_bg()
    sys.exit(0 if success else 1)
