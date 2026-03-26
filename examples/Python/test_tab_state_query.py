"""
测试状态查询函数
测试 GetTabEnabled、IsTabItemSelected
覆盖正常查询、无效句柄、越界索引等场景

测试的功能点:
- GetTabEnabled: 获取整个 TabControl 的启用状态
- IsTabItemSelected: 判断指定标签页是否为当前选中

预期结果:
- GetTabEnabled: 启用返回 1，禁用返回 0，无效句柄返回 -1
- IsTabItemSelected: 选中返回 1，未选中返回 0，无效参数返回 -1
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

dll.create_window.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
dll.create_window.restype = wintypes.HWND

dll.destroy_window.argtypes = [wintypes.HWND]
dll.destroy_window.restype = None

dll.CreateTabControl.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
dll.CreateTabControl.restype = wintypes.HWND

dll.AddTabItem.argtypes = [wintypes.HWND, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int, wintypes.HWND]
dll.AddTabItem.restype = ctypes.c_int

dll.SelectTab.argtypes = [wintypes.HWND, ctypes.c_int]
dll.SelectTab.restype = wintypes.BOOL

dll.DestroyTabControl.argtypes = [wintypes.HWND]
dll.DestroyTabControl.restype = None

dll.GetTabCount.argtypes = [wintypes.HWND]
dll.GetTabCount.restype = ctypes.c_int

# GetTabEnabled
dll.GetTabEnabled.argtypes = [wintypes.HWND]
dll.GetTabEnabled.restype = ctypes.c_int

# IsTabItemSelected
dll.IsTabItemSelected.argtypes = [wintypes.HWND, ctypes.c_int]
dll.IsTabItemSelected.restype = ctypes.c_int


# Win32 API for EnableWindow
user32 = ctypes.windll.user32
user32.EnableWindow.argtypes = [wintypes.HWND, wintypes.BOOL]
user32.EnableWindow.restype = wintypes.BOOL


def make_utf8_bytes(text):
    """将 Python 字符串转换为 UTF-8 字节数组指针和长度"""
    encoded = text.encode('utf-8')
    arr = (ctypes.c_ubyte * len(encoded))(*encoded)
    return arr, len(encoded)


def add_tabs(hTab, titles):
    """批量添加标签页，返回索引列表"""
    indices = []
    for t in titles:
        b, l = make_utf8_bytes(t)
        idx = dll.AddTabItem(hTab, b, l, None)
        indices.append(idx)
    return indices


def test_tab_state_query():
    """测试状态查询函数"""
    print("=" * 60)
    print("测试状态查询函数")
    print("=" * 60)

    all_passed = True
    INVALID_HWND = wintypes.HWND(0x12345678)

    # 创建测试窗口和 TabControl
    print("\n[准备] 创建测试窗口和 TabControl...")
    hwnd = dll.create_window(b"Test State Query", 800, 600)
    if not hwnd:
        print("  错误: 无法创建窗口")
        return False

    hTab = dll.CreateTabControl(hwnd, 10, 10, 780, 560)
    if not hTab:
        print("  错误: 无法创建 TabControl")
        dll.destroy_window(hwnd)
        return False

    add_tabs(hTab, ["页面A", "页面B", "页面C"])
    print("  创建成功，已添加 3 个标签页")

    # ========== 测试 GetTabEnabled ==========
    print("\n--- 测试 GetTabEnabled ---")

    # 默认启用状态
    ret = dll.GetTabEnabled(hTab)
    if ret == 1:
        print("  [通过] 默认状态返回 1（启用）")
    else:
        print(f"  [失败] 默认状态返回 {ret}，期望 1")
        all_passed = False

    # 禁用 TabControl 后查询
    user32.EnableWindow(hTab, False)
    ret = dll.GetTabEnabled(hTab)
    if ret == 0:
        print("  [通过] 禁用后返回 0")
    else:
        print(f"  [失败] 禁用后返回 {ret}，期望 0")
        all_passed = False

    # 重新启用后查询
    user32.EnableWindow(hTab, True)
    ret = dll.GetTabEnabled(hTab)
    if ret == 1:
        print("  [通过] 重新启用后返回 1")
    else:
        print(f"  [失败] 重新启用后返回 {ret}，期望 1")
        all_passed = False

    # 无效句柄
    ret = dll.GetTabEnabled(INVALID_HWND)
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
        all_passed = False

    # ========== 测试 IsTabItemSelected ==========
    print("\n--- 测试 IsTabItemSelected ---")

    # 默认选中第 0 页
    dll.SelectTab(hTab, 0)
    ret = dll.IsTabItemSelected(hTab, 0)
    if ret == 1:
        print("  [通过] index=0 选中，返回 1")
    else:
        print(f"  [失败] index=0 选中，返回 {ret}，期望 1")
        all_passed = False

    # 未选中的页面
    ret = dll.IsTabItemSelected(hTab, 1)
    if ret == 0:
        print("  [通过] index=1 未选中，返回 0")
    else:
        print(f"  [失败] index=1 未选中，返回 {ret}，期望 0")
        all_passed = False

    ret = dll.IsTabItemSelected(hTab, 2)
    if ret == 0:
        print("  [通过] index=2 未选中，返回 0")
    else:
        print(f"  [失败] index=2 未选中，返回 {ret}，期望 0")
        all_passed = False

    # 切换选中页后再查询
    dll.SelectTab(hTab, 2)
    ret = dll.IsTabItemSelected(hTab, 2)
    if ret == 1:
        print("  [通过] 切换到 index=2 后，返回 1")
    else:
        print(f"  [失败] 切换到 index=2 后，返回 {ret}，期望 1")
        all_passed = False

    ret = dll.IsTabItemSelected(hTab, 0)
    if ret == 0:
        print("  [通过] 切换后 index=0 未选中，返回 0")
    else:
        print(f"  [失败] 切换后 index=0 未选中，返回 {ret}，期望 0")
        all_passed = False

    # 越界索引
    ret = dll.IsTabItemSelected(hTab, -1)
    if ret == -1:
        print("  [通过] index=-1 越界，返回 -1")
    else:
        print(f"  [失败] index=-1 越界，返回 {ret}，期望 -1")
        all_passed = False

    ret = dll.IsTabItemSelected(hTab, 100)
    if ret == -1:
        print("  [通过] index=100 越界，返回 -1")
    else:
        print(f"  [失败] index=100 越界，返回 {ret}，期望 -1")
        all_passed = False

    # 无效句柄
    ret = dll.IsTabItemSelected(INVALID_HWND, 0)
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
    success = test_tab_state_query()
    sys.exit(0 if success else 1)
