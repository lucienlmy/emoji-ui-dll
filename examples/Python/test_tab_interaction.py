"""
测试交互增强函数
测试 SetTabClosable、SetTabCloseCallback、SetTabRightClickCallback、SetTabDraggable、SetTabDoubleClickCallback
覆盖回调设置、功能开关、无效参数等场景

测试的功能点:
- SetTabClosable: 设置标签页是否显示关闭按钮
- SetTabCloseCallback: 设置标签页关闭回调
- SetTabRightClickCallback: 设置标签页右键点击回调
- SetTabDraggable: 设置标签页是否可拖拽排序
- SetTabDoubleClickCallback: 设置标签页双击回调

预期结果:
- 有效参数调用返回 0
- 无效句柄返回 -1
- 回调函数可正确设置（不崩溃）
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

# ========== 回调函数类型定义 ==========

# TAB_CLOSE_CALLBACK: void (__stdcall *)(HWND hTabControl, int index)
TAB_CLOSE_CALLBACK = ctypes.WINFUNCTYPE(None, wintypes.HWND, ctypes.c_int)

# TAB_RIGHTCLICK_CALLBACK: void (__stdcall *)(HWND hTabControl, int index, int x, int y)
TAB_RIGHTCLICK_CALLBACK = ctypes.WINFUNCTYPE(None, wintypes.HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int)

# TAB_DBLCLICK_CALLBACK: void (__stdcall *)(HWND hTabControl, int index)
TAB_DBLCLICK_CALLBACK = ctypes.WINFUNCTYPE(None, wintypes.HWND, ctypes.c_int)

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

# SetTabClosable
dll.SetTabClosable.argtypes = [wintypes.HWND, ctypes.c_int]
dll.SetTabClosable.restype = ctypes.c_int

# SetTabCloseCallback
dll.SetTabCloseCallback.argtypes = [wintypes.HWND, TAB_CLOSE_CALLBACK]
dll.SetTabCloseCallback.restype = ctypes.c_int

# SetTabRightClickCallback
dll.SetTabRightClickCallback.argtypes = [wintypes.HWND, TAB_RIGHTCLICK_CALLBACK]
dll.SetTabRightClickCallback.restype = ctypes.c_int

# SetTabDraggable
dll.SetTabDraggable.argtypes = [wintypes.HWND, ctypes.c_int]
dll.SetTabDraggable.restype = ctypes.c_int

# SetTabDoubleClickCallback
dll.SetTabDoubleClickCallback.argtypes = [wintypes.HWND, TAB_DBLCLICK_CALLBACK]
dll.SetTabDoubleClickCallback.restype = ctypes.c_int


def make_utf8_bytes(text):
    """将 Python 字符串转换为 UTF-8 字节数组指针和长度"""
    encoded = text.encode('utf-8')
    arr = (ctypes.c_ubyte * len(encoded))(*encoded)
    return arr, len(encoded)


def test_tab_interaction():
    """测试交互增强函数"""
    print("=" * 60)
    print("测试交互增强函数")
    print("=" * 60)

    all_passed = True
    INVALID_HWND = wintypes.HWND(0x12345678)

    # 创建测试窗口和 TabControl
    print("\n[准备] 创建测试窗口和 TabControl...")
    hwnd = dll.create_window(b"Test Interaction", 800, 600)
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

    # ========== 测试 SetTabClosable ==========
    print("\n--- 测试 SetTabClosable ---")

    # 启用关闭按钮
    ret = dll.SetTabClosable(hTab, 1)
    if ret == 0:
        print("  [通过] 启用关闭按钮 返回 0")
    else:
        print(f"  [失败] 启用关闭按钮 返回 {ret}，期望 0")
        all_passed = False

    # 禁用关闭按钮
    ret = dll.SetTabClosable(hTab, 0)
    if ret == 0:
        print("  [通过] 禁用关闭按钮 返回 0")
    else:
        print(f"  [失败] 禁用关闭按钮 返回 {ret}，期望 0")
        all_passed = False

    # 重新启用
    ret = dll.SetTabClosable(hTab, 1)
    if ret == 0:
        print("  [通过] 重新启用关闭按钮 返回 0")
    else:
        print(f"  [失败] 重新启用关闭按钮 返回 {ret}，期望 0")
        all_passed = False

    # 无效句柄
    ret = dll.SetTabClosable(INVALID_HWND, 1)
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
        all_passed = False

    # ========== 测试 SetTabCloseCallback ==========
    print("\n--- 测试 SetTabCloseCallback ---")

    # 定义回调函数（用于验证不崩溃）
    close_called_info = {"called": False, "index": -1}

    @TAB_CLOSE_CALLBACK
    def close_callback(hTabControl, index):
        close_called_info["called"] = True
        close_called_info["index"] = index

    # 设置回调
    ret = dll.SetTabCloseCallback(hTab, close_callback)
    if ret == 0:
        print("  [通过] 设置关闭回调 返回 0")
    else:
        print(f"  [失败] 设置关闭回调 返回 {ret}，期望 0")
        all_passed = False

    # 设置 NULL 回调（清除）
    ret = dll.SetTabCloseCallback(hTab, TAB_CLOSE_CALLBACK(0))
    if ret == 0:
        print("  [通过] 清除关闭回调 返回 0")
    else:
        print(f"  [失败] 清除关闭回调 返回 {ret}，期望 0")
        all_passed = False

    # 重新设置回调
    ret = dll.SetTabCloseCallback(hTab, close_callback)
    if ret == 0:
        print("  [通过] 重新设置关闭回调 返回 0")
    else:
        print(f"  [失败] 重新设置关闭回调 返回 {ret}，期望 0")
        all_passed = False

    # 无效句柄
    ret = dll.SetTabCloseCallback(INVALID_HWND, close_callback)
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
        all_passed = False

    # ========== 测试 SetTabRightClickCallback ==========
    print("\n--- 测试 SetTabRightClickCallback ---")

    rightclick_called_info = {"called": False, "index": -1, "x": 0, "y": 0}

    @TAB_RIGHTCLICK_CALLBACK
    def rightclick_callback(hTabControl, index, x, y):
        rightclick_called_info["called"] = True
        rightclick_called_info["index"] = index
        rightclick_called_info["x"] = x
        rightclick_called_info["y"] = y

    # 设置回调
    ret = dll.SetTabRightClickCallback(hTab, rightclick_callback)
    if ret == 0:
        print("  [通过] 设置右键回调 返回 0")
    else:
        print(f"  [失败] 设置右键回调 返回 {ret}，期望 0")
        all_passed = False

    # 清除回调
    ret = dll.SetTabRightClickCallback(hTab, TAB_RIGHTCLICK_CALLBACK(0))
    if ret == 0:
        print("  [通过] 清除右键回调 返回 0")
    else:
        print(f"  [失败] 清除右键回调 返回 {ret}，期望 0")
        all_passed = False

    # 重新设置
    ret = dll.SetTabRightClickCallback(hTab, rightclick_callback)
    if ret == 0:
        print("  [通过] 重新设置右键回调 返回 0")
    else:
        print(f"  [失败] 重新设置右键回调 返回 {ret}，期望 0")
        all_passed = False

    # 无效句柄
    ret = dll.SetTabRightClickCallback(INVALID_HWND, rightclick_callback)
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
        all_passed = False

    # ========== 测试 SetTabDraggable ==========
    print("\n--- 测试 SetTabDraggable ---")

    # 启用拖拽
    ret = dll.SetTabDraggable(hTab, 1)
    if ret == 0:
        print("  [通过] 启用拖拽 返回 0")
    else:
        print(f"  [失败] 启用拖拽 返回 {ret}，期望 0")
        all_passed = False

    # 禁用拖拽
    ret = dll.SetTabDraggable(hTab, 0)
    if ret == 0:
        print("  [通过] 禁用拖拽 返回 0")
    else:
        print(f"  [失败] 禁用拖拽 返回 {ret}，期望 0")
        all_passed = False

    # 重新启用
    ret = dll.SetTabDraggable(hTab, 1)
    if ret == 0:
        print("  [通过] 重新启用拖拽 返回 0")
    else:
        print(f"  [失败] 重新启用拖拽 返回 {ret}，期望 0")
        all_passed = False

    # 无效句柄
    ret = dll.SetTabDraggable(INVALID_HWND, 1)
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
        all_passed = False

    # ========== 测试 SetTabDoubleClickCallback ==========
    print("\n--- 测试 SetTabDoubleClickCallback ---")

    dblclick_called_info = {"called": False, "index": -1}

    @TAB_DBLCLICK_CALLBACK
    def dblclick_callback(hTabControl, index):
        dblclick_called_info["called"] = True
        dblclick_called_info["index"] = index

    # 设置回调
    ret = dll.SetTabDoubleClickCallback(hTab, dblclick_callback)
    if ret == 0:
        print("  [通过] 设置双击回调 返回 0")
    else:
        print(f"  [失败] 设置双击回调 返回 {ret}，期望 0")
        all_passed = False

    # 清除回调
    ret = dll.SetTabDoubleClickCallback(hTab, TAB_DBLCLICK_CALLBACK(0))
    if ret == 0:
        print("  [通过] 清除双击回调 返回 0")
    else:
        print(f"  [失败] 清除双击回调 返回 {ret}，期望 0")
        all_passed = False

    # 重新设置
    ret = dll.SetTabDoubleClickCallback(hTab, dblclick_callback)
    if ret == 0:
        print("  [通过] 重新设置双击回调 返回 0")
    else:
        print(f"  [失败] 重新设置双击回调 返回 {ret}，期望 0")
        all_passed = False

    # 无效句柄
    ret = dll.SetTabDoubleClickCallback(INVALID_HWND, dblclick_callback)
    if ret == -1:
        print("  [通过] 无效句柄返回 -1")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 -1")
        all_passed = False

    # ========== 测试组合场景 ==========
    print("\n--- 测试组合场景 ---")

    # 同时启用关闭按钮和拖拽
    ret1 = dll.SetTabClosable(hTab, 1)
    ret2 = dll.SetTabDraggable(hTab, 1)
    ret3 = dll.SetTabCloseCallback(hTab, close_callback)
    ret4 = dll.SetTabRightClickCallback(hTab, rightclick_callback)
    ret5 = dll.SetTabDoubleClickCallback(hTab, dblclick_callback)
    if ret1 == 0 and ret2 == 0 and ret3 == 0 and ret4 == 0 and ret5 == 0:
        print("  [通过] 同时设置所有交互功能 全部返回 0")
    else:
        print(f"  [失败] 返回值: closable={ret1}, draggable={ret2}, close_cb={ret3}, rightclick_cb={ret4}, dblclick_cb={ret5}")
        all_passed = False

    # 全部禁用/清除
    ret1 = dll.SetTabClosable(hTab, 0)
    ret2 = dll.SetTabDraggable(hTab, 0)
    ret3 = dll.SetTabCloseCallback(hTab, TAB_CLOSE_CALLBACK(0))
    ret4 = dll.SetTabRightClickCallback(hTab, TAB_RIGHTCLICK_CALLBACK(0))
    ret5 = dll.SetTabDoubleClickCallback(hTab, TAB_DBLCLICK_CALLBACK(0))
    if ret1 == 0 and ret2 == 0 and ret3 == 0 and ret4 == 0 and ret5 == 0:
        print("  [通过] 全部禁用/清除交互功能 全部返回 0")
    else:
        print(f"  [失败] 返回值: closable={ret1}, draggable={ret2}, close_cb={ret3}, rightclick_cb={ret4}, dblclick_cb={ret5}")
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
    success = test_tab_interaction()
    sys.exit(0 if success else 1)
