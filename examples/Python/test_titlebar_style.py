"""
测试标题栏样式自定义函数
测试 SetTitleBarTextColor、GetTitleBarTextColor、SetTitleBarFont、SetTitleBarAlignment
覆盖正常调用、无效句柄、无效参数等场景，以及属性测试

测试的功能点:
- SetTitleBarTextColor: 设置标题栏文字颜色（ARGB）
- GetTitleBarTextColor: 获取标题栏文字颜色
- SetTitleBarFont: 设置标题栏字体名称和字号
- SetTitleBarAlignment: 设置标题栏文字对齐方式（0=左，1=中，2=右）

预期结果:
- 有效参数调用返回 1
- 无效句柄调用返回 0
- 无效参数调用返回 0
- GetTitleBarTextColor 默认返回 0（跟随主题）
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

# SetTitleBarTextColor(HWND hwnd, UINT32 color) -> int
dll.SetTitleBarTextColor.argtypes = [wintypes.HWND, ctypes.c_uint32]
dll.SetTitleBarTextColor.restype = ctypes.c_int

# GetTitleBarTextColor(HWND hwnd) -> UINT32
dll.GetTitleBarTextColor.argtypes = [wintypes.HWND]
dll.GetTitleBarTextColor.restype = ctypes.c_uint32

# SetTitleBarFont(HWND hwnd, const unsigned char* fontName, int fontNameLen, float fontSize) -> int
dll.SetTitleBarFont.argtypes = [wintypes.HWND, ctypes.POINTER(ctypes.c_ubyte), ctypes.c_int, ctypes.c_float]
dll.SetTitleBarFont.restype = ctypes.c_int

# SetTitleBarAlignment(HWND hwnd, int alignment) -> int
dll.SetTitleBarAlignment.argtypes = [wintypes.HWND, ctypes.c_int]
dll.SetTitleBarAlignment.restype = ctypes.c_int


def make_utf8_bytes(text):
    """将 Python 字符串转换为 UTF-8 字节数组指针和长度"""
    encoded = text.encode('utf-8')
    arr = (ctypes.c_ubyte * len(encoded))(*encoded)
    return arr, len(encoded)


# ========================================================================
# 任务 7.1: 单元测试
# ========================================================================

def test_titlebar_style():
    """测试标题栏样式自定义函数"""
    print("=" * 60)
    print("测试标题栏样式自定义函数")
    print("=" * 60)

    all_passed = True
    INVALID_HWND = wintypes.HWND(0x12345678)

    # 创建测试窗口
    print("\n[准备] 创建测试窗口...")
    hwnd = dll.create_window(b"test", 400, 300)
    if not hwnd:
        print("  错误: 无法创建窗口")
        return False
    print("  创建成功")

    # ========== 测试默认值 ==========
    print("\n--- 测试默认值 ---")

    ret = dll.GetTitleBarTextColor(hwnd)
    if ret == 0:
        print("  [通过] 新建窗口 GetTitleBarTextColor 返回 0（跟随主题）")
    else:
        print(f"  [失败] 新建窗口 GetTitleBarTextColor 返回 {ret}，期望 0")
        all_passed = False

    # ========== 测试 SetTitleBarTextColor ==========
    print("\n--- 测试 SetTitleBarTextColor ---")

    # 正常调用
    ret = dll.SetTitleBarTextColor(hwnd, 0xFFFF0000)
    if ret == 1:
        print("  [通过] 正常调用 (0xFFFF0000) 返回 1")
    else:
        print(f"  [失败] 正常调用返回 {ret}，期望 1")
        all_passed = False

    # 无效句柄
    ret = dll.SetTitleBarTextColor(INVALID_HWND, 0xFFFF0000)
    if ret == 0:
        print("  [通过] 无效句柄返回 0")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 0")
        all_passed = False

    # ========== 测试 SetTitleBarFont ==========
    print("\n--- 测试 SetTitleBarFont ---")

    # 正常调用
    font_bytes, font_len = make_utf8_bytes("Microsoft YaHei")
    ret = dll.SetTitleBarFont(hwnd, font_bytes, font_len, ctypes.c_float(16.0))
    if ret == 1:
        print("  [通过] 正常调用 ('Microsoft YaHei', 16.0) 返回 1")
    else:
        print(f"  [失败] 正常调用返回 {ret}，期望 1")
        all_passed = False

    # 无效句柄
    ret = dll.SetTitleBarFont(INVALID_HWND, font_bytes, font_len, ctypes.c_float(16.0))
    if ret == 0:
        print("  [通过] 无效句柄返回 0")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 0")
        all_passed = False

    # fontName 为 NULL
    ret = dll.SetTitleBarFont(hwnd, None, 0, ctypes.c_float(16.0))
    if ret == 0:
        print("  [通过] fontName=NULL 返回 0")
    else:
        print(f"  [失败] fontName=NULL 返回 {ret}，期望 0")
        all_passed = False

    # fontNameLen 为负数
    ret = dll.SetTitleBarFont(hwnd, font_bytes, -1, ctypes.c_float(16.0))
    if ret == 0:
        print("  [通过] fontNameLen=-1 返回 0")
    else:
        print(f"  [失败] fontNameLen=-1 返回 {ret}，期望 0")
        all_passed = False

    # fontSize 为负数
    ret = dll.SetTitleBarFont(hwnd, font_bytes, font_len, ctypes.c_float(-5.0))
    if ret == 0:
        print("  [通过] fontSize=-5 返回 0")
    else:
        print(f"  [失败] fontSize=-5 返回 {ret}，期望 0")
        all_passed = False

    # ========== 测试 SetTitleBarAlignment ==========
    print("\n--- 测试 SetTitleBarAlignment ---")

    # alignment=0 (左对齐)
    ret = dll.SetTitleBarAlignment(hwnd, 0)
    if ret == 1:
        print("  [通过] alignment=0 (左对齐) 返回 1")
    else:
        print(f"  [失败] alignment=0 返回 {ret}，期望 1")
        all_passed = False

    # alignment=1 (居中)
    ret = dll.SetTitleBarAlignment(hwnd, 1)
    if ret == 1:
        print("  [通过] alignment=1 (居中) 返回 1")
    else:
        print(f"  [失败] alignment=1 返回 {ret}，期望 1")
        all_passed = False

    # alignment=2 (右对齐)
    ret = dll.SetTitleBarAlignment(hwnd, 2)
    if ret == 1:
        print("  [通过] alignment=2 (右对齐) 返回 1")
    else:
        print(f"  [失败] alignment=2 返回 {ret}，期望 1")
        all_passed = False

    # 边界值: alignment=0 和 alignment=2 均成功
    print("\n--- 测试 SetTitleBarAlignment 边界值 ---")

    ret0 = dll.SetTitleBarAlignment(hwnd, 0)
    ret2 = dll.SetTitleBarAlignment(hwnd, 2)
    if ret0 == 1 and ret2 == 1:
        print("  [通过] 边界值 alignment=0 和 alignment=2 均返回 1")
    else:
        print(f"  [失败] alignment=0 返回 {ret0}，alignment=2 返回 {ret2}，期望均为 1")
        all_passed = False

    # 无效句柄
    ret = dll.SetTitleBarAlignment(INVALID_HWND, 1)
    if ret == 0:
        print("  [通过] 无效句柄返回 0")
    else:
        print(f"  [失败] 无效句柄返回 {ret}，期望 0")
        all_passed = False

    # 无效 alignment: -1
    ret = dll.SetTitleBarAlignment(hwnd, -1)
    if ret == 0:
        print("  [通过] alignment=-1 返回 0")
    else:
        print(f"  [失败] alignment=-1 返回 {ret}，期望 0")
        all_passed = False

    # 无效 alignment: 3
    ret = dll.SetTitleBarAlignment(hwnd, 3)
    if ret == 0:
        print("  [通过] alignment=3 返回 0")
    else:
        print(f"  [失败] alignment=3 返回 {ret}，期望 0")
        all_passed = False

    # ========== 完整场景测试 ==========
    print("\n--- 完整场景测试 ---")

    # 创建新窗口用于完整场景
    hwnd2 = dll.create_window(b"test_full", 400, 300)
    if not hwnd2:
        print("  错误: 无法创建第二个窗口")
        all_passed = False
    else:
        # 设置白色文字 (0xFFFFFFFF)
        ret = dll.SetTitleBarTextColor(hwnd2, 0xFFFFFFFF)
        if ret == 1:
            print("  [通过] 设置白色文字 (0xFFFFFFFF) 返回 1")
        else:
            print(f"  [失败] 设置白色文字返回 {ret}，期望 1")
            all_passed = False

        # 设置自定义字体
        font_bytes2, font_len2 = make_utf8_bytes("Arial")
        ret = dll.SetTitleBarFont(hwnd2, font_bytes2, font_len2, ctypes.c_float(18.0))
        if ret == 1:
            print("  [通过] 设置自定义字体 ('Arial', 18.0) 返回 1")
        else:
            print(f"  [失败] 设置自定义字体返回 {ret}，期望 1")
            all_passed = False

        # 设置居中对齐
        ret = dll.SetTitleBarAlignment(hwnd2, 1)
        if ret == 1:
            print("  [通过] 设置居中对齐 返回 1")
        else:
            print(f"  [失败] 设置居中对齐返回 {ret}，期望 1")
            all_passed = False

        # 验证 GetTitleBarTextColor 返回 0xFFFFFFFF
        color = dll.GetTitleBarTextColor(hwnd2)
        if color == 0xFFFFFFFF:
            print("  [通过] GetTitleBarTextColor 返回 0xFFFFFFFF")
        else:
            print(f"  [失败] GetTitleBarTextColor 返回 {color:#010x}，期望 0xFFFFFFFF")
            all_passed = False

        dll.destroy_window(hwnd2)

    # ========== 清理 ==========
    print("\n[清理] 销毁窗口...")
    dll.destroy_window(hwnd)
    print("  清理完成")

    # ========== 结果 ==========
    print("\n" + "=" * 60)
    if all_passed:
        print("所有单元测试通过!")
    else:
        print("部分单元测试失败!")
    print("=" * 60)

    return all_passed


# ========================================================================
# 属性测试 (Property-Based Tests)
# 使用 Hypothesis 框架
# Feature: titlebar-style-customization
# ========================================================================

from hypothesis import given, settings, strategies as st

# 属性测试共享窗口（避免每次迭代创建/销毁窗口导致超时）
_pbt_hwnd = None

def _get_pbt_hwnd():
    """获取属性测试共享窗口句柄，首次调用时创建"""
    global _pbt_hwnd
    if _pbt_hwnd is None:
        _pbt_hwnd = dll.create_window(b"pbt_test", 400, 300)
    return _pbt_hwnd

def _cleanup_pbt_hwnd():
    """清理属性测试共享窗口"""
    global _pbt_hwnd
    if _pbt_hwnd is not None:
        dll.destroy_window(_pbt_hwnd)
        _pbt_hwnd = None


# ========================================================================
# 任务 7.2: Property 1 - 文字颜色设置-获取往返一致
# **Validates: Requirements 1.1, 2.1**
# Feature: titlebar-style-customization, Property 1: 文字颜色设置-获取往返一致
# ========================================================================

@settings(max_examples=100, deadline=None)
@given(color=st.integers(min_value=0, max_value=0xFFFFFFFF))
def test_property1_text_color_roundtrip(color):
    """Property 1: 文字颜色设置-获取往返一致
    
    对任意 UINT32 颜色值，SetTitleBarTextColor 后 GetTitleBarTextColor 应返回相同值。
    
    **Validates: Requirements 1.1, 2.1**
    Feature: titlebar-style-customization, Property 1: 文字颜色设置-获取往返一致
    """
    hwnd = _get_pbt_hwnd()
    assert hwnd, "无法创建窗口"
    ret = dll.SetTitleBarTextColor(hwnd, ctypes.c_uint32(color))
    assert ret == 1, f"SetTitleBarTextColor 返回 {ret}，期望 1"
    got = dll.GetTitleBarTextColor(hwnd)
    assert got == color, f"GetTitleBarTextColor 返回 {got:#010x}，期望 {color:#010x}"


# ========================================================================
# 任务 7.3: Property 2 - 无效窗口句柄统一返回错误值
# **Validates: Requirements 1.2, 2.2, 4.3**
# Feature: titlebar-style-customization, Property 2: 无效窗口句柄统一返回错误值
# ========================================================================

@settings(max_examples=100, deadline=None)
@given(hwnd_val=st.integers(min_value=0, max_value=0xFFFFFFFF))
def test_property2_invalid_hwnd_returns_zero(hwnd_val):
    """Property 2: 无效窗口句柄统一返回错误值
    
    对任意不在 g_windows 映射表中的 hwnd 值，所有函数应返回 0。
    
    **Validates: Requirements 1.2, 2.2, 4.3**
    Feature: titlebar-style-customization, Property 2: 无效窗口句柄统一返回错误值
    """
    invalid_hwnd = ctypes.cast(hwnd_val, wintypes.HWND)

    # SetTitleBarTextColor 应返回 0
    ret = dll.SetTitleBarTextColor(invalid_hwnd, ctypes.c_uint32(0xFFFF0000))
    assert ret == 0, f"SetTitleBarTextColor(invalid_hwnd={hwnd_val:#x}) 返回 {ret}，期望 0"

    # GetTitleBarTextColor 应返回 0
    ret = dll.GetTitleBarTextColor(invalid_hwnd)
    assert ret == 0, f"GetTitleBarTextColor(invalid_hwnd={hwnd_val:#x}) 返回 {ret}，期望 0"

    # SetTitleBarFont 应返回 0
    font_bytes, font_len = make_utf8_bytes("Arial")
    ret = dll.SetTitleBarFont(invalid_hwnd, font_bytes, font_len, ctypes.c_float(16.0))
    assert ret == 0, f"SetTitleBarFont(invalid_hwnd={hwnd_val:#x}) 返回 {ret}，期望 0"

    # SetTitleBarAlignment 应返回 0
    ret = dll.SetTitleBarAlignment(invalid_hwnd, 1)
    assert ret == 0, f"SetTitleBarAlignment(invalid_hwnd={hwnd_val:#x}) 返回 {ret}，期望 0"


# ========================================================================
# 任务 7.4: Property 3 - SetTitleBarFont 无效参数拒绝
# **Validates: Requirements 3.2, 3.3**
# Feature: titlebar-style-customization, Property 3: SetTitleBarFont 无效参数拒绝
# ========================================================================

@settings(max_examples=100, deadline=None)
@given(
    scenario=st.sampled_from(["null_name", "negative_len", "negative_size"]),
    neg_len=st.integers(min_value=-10000, max_value=-1),
    neg_size=st.floats(min_value=-10000.0, max_value=-0.001),
)
def test_property3_set_font_invalid_params(scenario, neg_len, neg_size):
    """Property 3: SetTitleBarFont 无效参数拒绝
    
    对有效窗口句柄，当 fontName 为 NULL、fontNameLen <= 0、fontSize <= 0 时，
    SetTitleBarFont 应返回 0。
    
    **Validates: Requirements 3.2, 3.3**
    Feature: titlebar-style-customization, Property 3: SetTitleBarFont 无效参数拒绝
    """
    hwnd = _get_pbt_hwnd()
    assert hwnd, "无法创建窗口"
    font_bytes, font_len = make_utf8_bytes("Arial")

    if scenario == "null_name":
        # fontName 为 NULL，len 为 0
        ret = dll.SetTitleBarFont(hwnd, None, 0, ctypes.c_float(16.0))
    elif scenario == "negative_len":
        # 有效 fontName 但负数 len
        ret = dll.SetTitleBarFont(hwnd, font_bytes, neg_len, ctypes.c_float(16.0))
    else:  # negative_size
        # 有效 fontName 和 len 但负数 fontSize
        ret = dll.SetTitleBarFont(hwnd, font_bytes, font_len, ctypes.c_float(neg_size))

    assert ret == 0, f"SetTitleBarFont({scenario}, neg_len={neg_len}, neg_size={neg_size}) 返回 {ret}，期望 0"


# ========================================================================
# 任务 7.5: Property 4 - SetTitleBarAlignment 无效范围拒绝
# **Validates: Requirements 4.2**
# Feature: titlebar-style-customization, Property 4: SetTitleBarAlignment 无效范围拒绝
# ========================================================================

@settings(max_examples=100, deadline=None)
@given(
    alignment=st.one_of(
        st.integers(min_value=-1000000, max_value=-1),
        st.integers(min_value=3, max_value=1000000),
    )
)
def test_property4_set_alignment_invalid_range(alignment):
    """Property 4: SetTitleBarAlignment 无效范围拒绝
    
    对有效窗口句柄，当 alignment 不在 [0, 2] 范围内时，
    SetTitleBarAlignment 应返回 0。
    
    **Validates: Requirements 4.2**
    Feature: titlebar-style-customization, Property 4: SetTitleBarAlignment 无效范围拒绝
    """
    hwnd = _get_pbt_hwnd()
    assert hwnd, "无法创建窗口"
    ret = dll.SetTitleBarAlignment(hwnd, alignment)
    assert ret == 0, f"SetTitleBarAlignment(alignment={alignment}) 返回 {ret}，期望 0"


# ========================================================================
# 主入口
# ========================================================================

if __name__ == "__main__":
    # 运行单元测试
    unit_success = test_titlebar_style()

    # 运行属性测试
    print("\n" + "=" * 60)
    print("运行属性测试 (Hypothesis)")
    print("=" * 60)

    pbt_success = True

    print("\n--- Property 1: 文字颜色设置-获取往返一致 ---")
    try:
        test_property1_text_color_roundtrip()
        print("  [通过] Property 1 通过")
    except Exception as e:
        print(f"  [失败] Property 1 失败: {e}")
        pbt_success = False

    print("\n--- Property 2: 无效窗口句柄统一返回错误值 ---")
    try:
        test_property2_invalid_hwnd_returns_zero()
        print("  [通过] Property 2 通过")
    except Exception as e:
        print(f"  [失败] Property 2 失败: {e}")
        pbt_success = False

    print("\n--- Property 3: SetTitleBarFont 无效参数拒绝 ---")
    try:
        test_property3_set_font_invalid_params()
        print("  [通过] Property 3 通过")
    except Exception as e:
        print(f"  [失败] Property 3 失败: {e}")
        pbt_success = False

    print("\n--- Property 4: SetTitleBarAlignment 无效范围拒绝 ---")
    try:
        test_property4_set_alignment_invalid_range()
        print("  [通过] Property 4 通过")
    except Exception as e:
        print(f"  [失败] Property 4 失败: {e}")
        pbt_success = False

    # 清理属性测试共享窗口
    _cleanup_pbt_hwnd()

    print("\n" + "=" * 60)
    if unit_success and pbt_success:
        print("所有测试通过!")
    else:
        if not unit_success:
            print("单元测试失败!")
        if not pbt_success:
            print("属性测试失败!")
    print("=" * 60)

    sys.exit(0 if (unit_success and pbt_success) else 1)
