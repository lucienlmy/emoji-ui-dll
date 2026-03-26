"""
测试单个标签页控制函数
测试 EnableTabItem、GetTabItemEnabled、ShowTabItem、SetTabItemIcon
覆盖启用/禁用切换、隐藏/显示、图标设置/清除、越界索引等场景

测试的功能点:
- EnableTabItem: 启用/禁用单个标签页
- GetTabItemEnabled: 获取单个标签页的启用状态
- ShowTabItem: 显示/隐藏单个标签页
- SetTabItemIcon: 设置/清除标签页图标

预期结果:
- 有效参数调用返回 0
- 无效句柄或越界索引返回 -1
- GetTabItemEnabled 返回 1(启用)/0(禁用)/-1(错误)
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

# 获取当前选中索引
dll.GetCurrentTabIndex.argtypes = [wintypes.HWND]
dll.GetCurrentTabIndex.restype = ctypes.c_int

# 销毁 TabControl
dll.DestroyTabControl.argtypes = [wintypes.HWND]
dll.DestroyTabControl.restype = None

# EnableTabItem
dll.EnableTabItem.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_int]
dll.EnableTabItem.restype = ctypes.c_int

# GetTabItemEnabled
dll.GetTabItemEnabled.argtypes = [wintypes.HWND, ctypes.c_int]
dll.GetTabItemEnabled.restype = ctypes.c_int

# ShowTabItem
dll.ShowTabItem.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.c_int]
dll.ShowTabItem.restype = ctypes.c_int

# SetTabItemIcon
dll.SetTabItemIcon.argtypes = [wintypes.HWND, ctypes.c_int, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int]
dll.SetTabItemIcon.restype = ctypes.c_int


def make_utf8_bytes(text):
    """将 Python 字符串转换为 UTF-8 字节数组指针和长度"""
    encoded = text.encode('utf-8')
    arr = (ctypes.c_ubyte * len(encoded))(*encoded)
    return arr, len(encoded)


def create_minimal_png():
    """创建一个最小的有效 1x1 PNG 图片字节数据"""
    # 最小的 1x1 红色像素 PNG
    png_data = bytes([
        0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A,  # PNG signature
        0x00, 0x00, 0x00, 0x0D, 0x49, 0x48, 0x44, 0x52,  # IHDR chunk
        0x00, 0x00, 0x00, 0x01, 0x00, 0x00, 0x00, 0x01,  # 1x1
        0x08, 0x02, 0x00, 0x00, 0x00, 0x90, 0x77, 0x53,  # 8-bit RGB
        0xDE, 0x00, 0x00, 0x00, 0x0C, 0x49, 0x44, 0x41,  # IDAT chunk
        0x54, 0x08, 0xD7, 0x63, 0xF8, 0xCF, 0xC0, 0x00,
        0x00, 0x00, 0x02, 0x00, 0x01, 0xE2, 0x21, 0xBC,
        0x33, 0x00, 0x00, 0x00, 0x00, 0x49, 0x45, 0x4E,  # IEND chunk
        0x44, 0xAE, 0x42, 0x60, 0x82
    ])
    arr = (ctypes.c_ubyte * len(png_data))(*png_data)
    return arr, len(png_data)


def test_tab_item_control():
    """测试单个标签页控制函数"""
    print("=" * 60)
    print("测试单个标签页控制函数")
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

    # ========== 测试 EnableTabItem ==========
    print("\n--- 测试 EnableTabItem ---")

    # 正常禁用
    ret = dll.EnableTabItem(hTab, 1, 0)
    if ret == 0:
        print("  [通过] 禁用 index=1 返回 0")
    else:
        print(f"  [失败] 禁用 index=1 返回 {ret}，期望 0")
        all_passed = False

    # 正常启用
    ret = dll.EnableTabItem(hTab, 1, 1)
    if ret == 0:
        print("  [通过] 启用 index=1 返回 0")
    else:
        print(f"  [失败] 启用 index=1 返回 {ret}，期望 0")
        all_passed = False

    # 无效句柄
    ret = dll.EnableTabItem(INVALID_HWND, 0, 1)
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
        all_passed = False

    # 越界索引（负数）
    ret = dll.EnableTabItem(hTab, -1, 1)
    if ret == -1:
        print("  [通过] index=-1 返回 -1")
    else:
        print(f"  [失败] index=-1 返回 {ret}，期望 -1")
        all_passed = False

    # 越界索引（超出范围）
    ret = dll.EnableTabItem(hTab, 100, 1)
    if ret == -1:
        print("  [通过] index=100 返回 -1")
    else:
        print(f"  [失败] index=100 返回 {ret}，期望 -1")
        all_passed = False

    # ========== 测试 GetTabItemEnabled ==========
    print("\n--- 测试 GetTabItemEnabled ---")

    # 默认启用状态
    ret = dll.GetTabItemEnabled(hTab, 0)
    if ret == 1:
        print("  [通过] 默认状态 index=0 返回 1（启用）")
    else:
        print(f"  [失败] 默认状态 index=0 返回 {ret}，期望 1")
        all_passed = False

    # 禁用后查询
    dll.EnableTabItem(hTab, 2, 0)
    ret = dll.GetTabItemEnabled(hTab, 2)
    if ret == 0:
        print("  [通过] 禁用后 index=2 返回 0（禁用）")
    else:
        print(f"  [失败] 禁用后 index=2 返回 {ret}，期望 0")
        all_passed = False

    # 重新启用后查询
    dll.EnableTabItem(hTab, 2, 1)
    ret = dll.GetTabItemEnabled(hTab, 2)
    if ret == 1:
        print("  [通过] 重新启用后 index=2 返回 1（启用）")
    else:
        print(f"  [失败] 重新启用后 index=2 返回 {ret}，期望 1")
        all_passed = False

    # 无效句柄
    ret = dll.GetTabItemEnabled(INVALID_HWND, 0)
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
        all_passed = False

    # 越界索引
    ret = dll.GetTabItemEnabled(hTab, 50)
    if ret == -1:
        print("  [通过] index=50 返回 -1")
    else:
        print(f"  [失败] index=50 返回 {ret}，期望 -1")
        all_passed = False

    # ========== 测试 ShowTabItem ==========
    print("\n--- 测试 ShowTabItem ---")

    # 隐藏标签页
    ret = dll.ShowTabItem(hTab, 1, 0)
    if ret == 0:
        print("  [通过] 隐藏 index=1 返回 0")
    else:
        print(f"  [失败] 隐藏 index=1 返回 {ret}，期望 0")
        all_passed = False

    # 重复隐藏（状态未变）
    ret = dll.ShowTabItem(hTab, 1, 0)
    if ret == 0:
        print("  [通过] 重复隐藏 index=1 返回 0（状态未变）")
    else:
        print(f"  [失败] 重复隐藏 index=1 返回 {ret}，期望 0")
        all_passed = False

    # 显示标签页
    ret = dll.ShowTabItem(hTab, 1, 1)
    if ret == 0:
        print("  [通过] 显示 index=1 返回 0")
    else:
        print(f"  [失败] 显示 index=1 返回 {ret}，期望 0")
        all_passed = False

    # 隐藏当前选中页（应自动切换）
    current = dll.GetCurrentTabIndex(hTab)
    print(f"  当前选中索引: {current}")
    ret = dll.ShowTabItem(hTab, current, 0)
    if ret == 0:
        new_current = dll.GetCurrentTabIndex(hTab)
        if new_current != current:
            print(f"  [通过] 隐藏当前选中页后自动切换到 index={new_current}")
        else:
            print(f"  [失败] 隐藏当前选中页后未自动切换，仍为 index={new_current}")
            all_passed = False
    else:
        print(f"  [失败] 隐藏当前选中页返回 {ret}，期望 0")
        all_passed = False

    # 恢复显示
    dll.ShowTabItem(hTab, current, 1)

    # 无效句柄
    ret = dll.ShowTabItem(INVALID_HWND, 0, 1)
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
        all_passed = False

    # 越界索引
    ret = dll.ShowTabItem(hTab, -1, 1)
    if ret == -1:
        print("  [通过] index=-1 返回 -1")
    else:
        print(f"  [失败] index=-1 返回 {ret}，期望 -1")
        all_passed = False

    ret = dll.ShowTabItem(hTab, 100, 0)
    if ret == -1:
        print("  [通过] index=100 返回 -1")
    else:
        print(f"  [失败] index=100 返回 {ret}，期望 -1")
        all_passed = False

    # ========== 测试 SetTabItemIcon ==========
    print("\n--- 测试 SetTabItemIcon ---")

    # 设置图标（使用最小 PNG）
    png_bytes, png_len = create_minimal_png()
    ret = dll.SetTabItemIcon(hTab, 0, png_bytes, png_len)
    if ret == 0:
        print("  [通过] 设置图标 index=0 返回 0")
    else:
        print(f"  [失败] 设置图标 index=0 返回 {ret}，期望 0")
        all_passed = False

    # 清除图标（iconBytes=NULL）
    ret = dll.SetTabItemIcon(hTab, 0, None, 0)
    if ret == 0:
        print("  [通过] 清除图标 (NULL, 0) 返回 0")
    else:
        print(f"  [失败] 清除图标 (NULL, 0) 返回 {ret}，期望 0")
        all_passed = False

    # 清除图标（iconLen=0）
    ret = dll.SetTabItemIcon(hTab, 0, png_bytes, 0)
    if ret == 0:
        print("  [通过] 清除图标 (data, 0) 返回 0")
    else:
        print(f"  [失败] 清除图标 (data, 0) 返回 {ret}，期望 0")
        all_passed = False

    # 无效句柄
    ret = dll.SetTabItemIcon(INVALID_HWND, 0, png_bytes, png_len)
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
        all_passed = False

    # 越界索引
    ret = dll.SetTabItemIcon(hTab, -1, png_bytes, png_len)
    if ret == -1:
        print("  [通过] index=-1 返回 -1")
    else:
        print(f"  [失败] index=-1 返回 {ret}，期望 -1")
        all_passed = False

    ret = dll.SetTabItemIcon(hTab, 100, png_bytes, png_len)
    if ret == -1:
        print("  [通过] index=100 返回 -1")
    else:
        print(f"  [失败] index=100 返回 {ret}，期望 -1")
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
    success = test_tab_item_control()
    sys.exit(0 if success else 1)
