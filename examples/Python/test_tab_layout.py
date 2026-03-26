"""
测试布局与位置函数
测试 SetTabPosition、SetTabAlignment、SetTabScrollable
覆盖各位置/对齐方式切换、滚动开关、无效参数等场景

测试的功能点:
- SetTabPosition: 设置标签栏位置（上/下/左/右）
- SetTabAlignment: 设置标签对齐方式（左/居中/右）
- SetTabScrollable: 设置标签栏是否可滚动

预期结果:
- 有效参数调用返回 0
- 无效句柄返回 -1
- 无效参数值返回 -1
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

# 销毁 TabControl
dll.DestroyTabControl.argtypes = [wintypes.HWND]
dll.DestroyTabControl.restype = None

# SetTabPosition
dll.SetTabPosition.argtypes = [wintypes.HWND, ctypes.c_int]
dll.SetTabPosition.restype = ctypes.c_int

# SetTabAlignment
dll.SetTabAlignment.argtypes = [wintypes.HWND, ctypes.c_int]
dll.SetTabAlignment.restype = ctypes.c_int

# SetTabScrollable
dll.SetTabScrollable.argtypes = [wintypes.HWND, ctypes.c_int]
dll.SetTabScrollable.restype = ctypes.c_int


def make_utf8_bytes(text):
    """将 Python 字符串转换为 UTF-8 字节数组指针和长度"""
    encoded = text.encode('utf-8')
    arr = (ctypes.c_ubyte * len(encoded))(*encoded)
    return arr, len(encoded)


def test_tab_layout():
    """测试布局与位置函数"""
    print("=" * 60)
    print("测试布局与位置函数")
    print("=" * 60)

    all_passed = True
    INVALID_HWND = wintypes.HWND(0x12345678)

    # 创建测试窗口和 TabControl
    print("\n[准备] 创建测试窗口和 TabControl...")
    hwnd = dll.create_window(b"Test Layout", 800, 600)
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

    # ========== 测试 SetTabPosition ==========
    print("\n--- 测试 SetTabPosition ---")

    # 位置 0: 上（默认）
    ret = dll.SetTabPosition(hTab, 0)
    if ret == 0:
        print("  [通过] 设置位置=上(0) 返回 0")
    else:
        print(f"  [失败] 设置位置=上(0) 返回 {ret}，期望 0")
        all_passed = False

    # 位置 1: 下
    ret = dll.SetTabPosition(hTab, 1)
    if ret == 0:
        print("  [通过] 设置位置=下(1) 返回 0")
    else:
        print(f"  [失败] 设置位置=下(1) 返回 {ret}，期望 0")
        all_passed = False

    # 位置 2: 左
    ret = dll.SetTabPosition(hTab, 2)
    if ret == 0:
        print("  [通过] 设置位置=左(2) 返回 0")
    else:
        print(f"  [失败] 设置位置=左(2) 返回 {ret}，期望 0")
        all_passed = False

    # 位置 3: 右
    ret = dll.SetTabPosition(hTab, 3)
    if ret == 0:
        print("  [通过] 设置位置=右(3) 返回 0")
    else:
        print(f"  [失败] 设置位置=右(3) 返回 {ret}，期望 0")
        all_passed = False

    # 恢复默认位置
    ret = dll.SetTabPosition(hTab, 0)
    if ret == 0:
        print("  [通过] 恢复位置=上(0) 返回 0")
    else:
        print(f"  [失败] 恢复位置=上(0) 返回 {ret}，期望 0")
        all_passed = False

    # 无效位置: -1
    ret = dll.SetTabPosition(hTab, -1)
    if ret == -1:
        print("  [通过] 无效位置(-1) 返回 -1")
    else:
        print(f"  [失败] 无效位置(-1) 返回 {ret}，期望 -1")
        all_passed = False

    # 无效位置: 4
    ret = dll.SetTabPosition(hTab, 4)
    if ret == -1:
        print("  [通过] 无效位置(4) 返回 -1")
    else:
        print(f"  [失败] 无效位置(4) 返回 {ret}，期望 -1")
        all_passed = False

    # 无效句柄
    ret = dll.SetTabPosition(INVALID_HWND, 0)
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
        all_passed = False

    # ========== 测试 SetTabAlignment ==========
    print("\n--- 测试 SetTabAlignment ---")

    # 对齐 0: 左对齐（默认）
    ret = dll.SetTabAlignment(hTab, 0)
    if ret == 0:
        print("  [通过] 设置对齐=左(0) 返回 0")
    else:
        print(f"  [失败] 设置对齐=左(0) 返回 {ret}，期望 0")
        all_passed = False

    # 对齐 1: 居中
    ret = dll.SetTabAlignment(hTab, 1)
    if ret == 0:
        print("  [通过] 设置对齐=居中(1) 返回 0")
    else:
        print(f"  [失败] 设置对齐=居中(1) 返回 {ret}，期望 0")
        all_passed = False

    # 对齐 2: 右对齐
    ret = dll.SetTabAlignment(hTab, 2)
    if ret == 0:
        print("  [通过] 设置对齐=右(2) 返回 0")
    else:
        print(f"  [失败] 设置对齐=右(2) 返回 {ret}，期望 0")
        all_passed = False

    # 恢复默认
    ret = dll.SetTabAlignment(hTab, 0)
    if ret == 0:
        print("  [通过] 恢复对齐=左(0) 返回 0")
    else:
        print(f"  [失败] 恢复对齐=左(0) 返回 {ret}，期望 0")
        all_passed = False

    # 无效对齐: -1
    ret = dll.SetTabAlignment(hTab, -1)
    if ret == -1:
        print("  [通过] 无效对齐(-1) 返回 -1")
    else:
        print(f"  [失败] 无效对齐(-1) 返回 {ret}，期望 -1")
        all_passed = False

    # 无效对齐: 3
    ret = dll.SetTabAlignment(hTab, 3)
    if ret == -1:
        print("  [通过] 无效对齐(3) 返回 -1")
    else:
        print(f"  [失败] 无效对齐(3) 返回 {ret}，期望 -1")
        all_passed = False

    # 无效句柄
    ret = dll.SetTabAlignment(INVALID_HWND, 0)
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
        all_passed = False

    # ========== 测试 SetTabScrollable ==========
    print("\n--- 测试 SetTabScrollable ---")

    # 启用滚动
    ret = dll.SetTabScrollable(hTab, 1)
    if ret == 0:
        print("  [通过] 启用滚动 返回 0")
    else:
        print(f"  [失败] 启用滚动 返回 {ret}，期望 0")
        all_passed = False

    # 禁用滚动
    ret = dll.SetTabScrollable(hTab, 0)
    if ret == 0:
        print("  [通过] 禁用滚动 返回 0")
    else:
        print(f"  [失败] 禁用滚动 返回 {ret}，期望 0")
        all_passed = False

    # 重新启用
    ret = dll.SetTabScrollable(hTab, 1)
    if ret == 0:
        print("  [通过] 重新启用滚动 返回 0")
    else:
        print(f"  [失败] 重新启用滚动 返回 {ret}，期望 0")
        all_passed = False

    # 无效句柄
    ret = dll.SetTabScrollable(INVALID_HWND, 1)
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
        all_passed = False

    # ========== 测试组合场景 ==========
    print("\n--- 测试组合场景 ---")

    # 位置+对齐+滚动组合
    ret1 = dll.SetTabPosition(hTab, 1)   # 下
    ret2 = dll.SetTabAlignment(hTab, 1)  # 居中
    ret3 = dll.SetTabScrollable(hTab, 1) # 可滚动
    if ret1 == 0 and ret2 == 0 and ret3 == 0:
        print("  [通过] 组合设置(下+居中+滚动) 全部返回 0")
    else:
        print(f"  [失败] 返回值: position={ret1}, alignment={ret2}, scrollable={ret3}")
        all_passed = False

    # 切换位置后再切换回来
    dll.SetTabPosition(hTab, 2)  # 左
    dll.SetTabPosition(hTab, 3)  # 右
    ret = dll.SetTabPosition(hTab, 0)  # 上
    if ret == 0:
        print("  [通过] 连续切换位置后恢复默认 返回 0")
    else:
        print(f"  [失败] 连续切换位置后恢复默认 返回 {ret}，期望 0")
        all_passed = False

    # 全部恢复默认
    ret1 = dll.SetTabPosition(hTab, 0)
    ret2 = dll.SetTabAlignment(hTab, 0)
    ret3 = dll.SetTabScrollable(hTab, 0)
    if ret1 == 0 and ret2 == 0 and ret3 == 0:
        print("  [通过] 全部恢复默认 全部返回 0")
    else:
        print(f"  [失败] 返回值: position={ret1}, alignment={ret2}, scrollable={ret3}")
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
    success = test_tab_layout()
    sys.exit(0 if success else 1)
