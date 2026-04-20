# -*- coding: utf-8 -*-
"""
单选框样式测试示例
测试所有单选框样式和功能
"""
import ctypes
import sys
import os
import io

# 设置控制台UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

sys.path.insert(0, os.path.dirname(__file__))

# 加载DLL
dll_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'emoji_window.dll')
try:
    dll = ctypes.CDLL(dll_path)
except OSError as e:
    print(f"错误: 无法加载 emoji_window.dll: {e}")
    sys.exit(1)

# 定义函数原型
dll.create_window_bytes_ex.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint]
dll.create_window_bytes_ex.restype = ctypes.c_void_p
dll.set_message_loop_main_window.argtypes = [ctypes.c_void_p]
dll.run_message_loop.restype = ctypes.c_int

dll.CreateLabel.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
    ctypes.c_char_p, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_char_p, ctypes.c_int,
    ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
dll.CreateLabel.restype = ctypes.c_int

dll.CreateRadioButton.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int,
    ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint,
    ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
dll.CreateRadioButton.restype = ctypes.c_int

dll.SetRadioButtonState.argtypes = [ctypes.c_int, ctypes.c_int]
dll.GetRadioButtonState.argtypes = [ctypes.c_int]
dll.GetRadioButtonState.restype = ctypes.c_int

dll.SetRadioButtonStyle.argtypes = [ctypes.c_int, ctypes.c_int]
dll.SetRadioButtonDotColor.argtypes = [ctypes.c_int, ctypes.c_uint]

RADIO_CB = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int)
dll.SetRadioButtonCallback.argtypes = [ctypes.c_int, RADIO_CB]

dll.SetLabelText.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]

# 单选框样式常量
RADIO_STYLE_DEFAULT = 0  # 默认圆形样式
RADIO_STYLE_BORDER = 1   # 边框样式
RADIO_STYLE_BUTTON = 2   # 按钮样式

def ARGB(a, r, g, b):
    return ((a & 0xFF) << 24) | ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)

def u(s):
    return s.encode('utf-8')

# 全局变量
label_status = 0
radio_groups = {}

def on_radio_changed(radio_id, checked):
    """单选框状态改变回调"""
    global label_status, radio_groups

    if checked:
        # 找到这个单选框属于哪个组
        group_name = None
        for gname, radios in radio_groups.items():
            if radio_id in radios:
                group_name = gname
                break

        if group_name:
            # 获取选中的索引
            idx = radio_groups[group_name].index(radio_id)
            msg = u(f"✓ {group_name} 选中了第 {idx + 1} 项")
            dll.SetLabelText(label_status, msg, len(msg))
            print(f"✓ {group_name} 选中了第 {idx + 1} 项 (ID={radio_id})")

_radio_cb = RADIO_CB(on_radio_changed)

def main():
    global label_status, radio_groups

    print("=" * 60)
    print("🔘 单选框样式测试示例")
    print("=" * 60)

    # 创建窗口
    title = u("🔘 RadioButton 单选框样式测试 - emoji_window")
    main_win = dll.create_window_bytes_ex(title, len(title), -1, -1, 1100, 850, ARGB(255, 50, 100, 180), ARGB(255, 240, 240, 240))
    if not main_win:
        print("❌ 创建窗口失败")
        return

    font = u("Microsoft YaHei UI")

    # 状态标签
    status_text = u("💡 点击不同的单选框查看效果")
    label_status = dll.CreateLabel(main_win, 20, 10, 860, 30, status_text, len(status_text),
        ARGB(255,50,50,50), ARGB(255,245,247,250), font, len(font), 14, 0, 0, 0, 0, 0)

    y_pos = 60

    # ========== 组1: 标准圆形单选框 ==========
    title1 = u("📍 组1: 水果选择")
    dll.CreateLabel(main_win, 20, y_pos, 400, 30, title1, len(title1),
        ARGB(255,64,158,255), ARGB(0,0,0,0), font, len(font), 14, 1, 0, 0, 0, 0)
    y_pos += 40

    group1_radios = []
    options1 = ["🍎 苹果", "🍌 香蕉", "🍊 橙子", "🍇 葡萄"]
    for i, opt in enumerate(options1):
        text = u(opt)
        radio_id = dll.CreateRadioButton(main_win, 40, y_pos, 180, 30, text, len(text), 1, 1 if i==0 else 0,
            ARGB(255,64,158,255), ARGB(255,255,255,255), font, len(font), 13, 0, 0, 0)
        dll.SetRadioButtonCallback(radio_id, _radio_cb)
        group1_radios.append(radio_id)
        y_pos += 35

    radio_groups["组1"] = group1_radios

    # ========== 组2: 动物选择 ==========
    y_pos = 60
    x_offset = 250

    title2 = u("📍 组2: 动物选择")
    dll.CreateLabel(main_win, x_offset, y_pos, 400, 30, title2, len(title2),
        ARGB(255,103,194,58), ARGB(0,0,0,0), font, len(font), 14, 1, 0, 0, 0, 0)
    y_pos += 40

    group2_radios = []
    options2 = ["🐶 狗", "🐱 猫", "🐰 兔子", "🐼 熊猫"]
    for i, opt in enumerate(options2):
        text = u(opt)
        radio_id = dll.CreateRadioButton(main_win, x_offset + 20, y_pos, 180, 30, text, len(text), 2, 1 if i==1 else 0,
            ARGB(255,103,194,58), ARGB(255,255,255,255), font, len(font), 13, 0, 0, 0)
        dll.SetRadioButtonCallback(radio_id, _radio_cb)
        group2_radios.append(radio_id)
        y_pos += 35

    radio_groups["组2"] = group2_radios

    # ========== 组3: 样式测试 - 边框样式 ==========
    y_pos = 60
    x_offset = 480

    title3 = u("📍 组3: 边框样式 (BORDER)")
    dll.CreateLabel(main_win, x_offset, y_pos, 400, 30, title3, len(title3),
        ARGB(255,230,162,60), ARGB(0,0,0,0), font, len(font), 14, 1, 0, 0, 0, 0)
    y_pos += 40

    group3_radios = []
    options3 = ["⭐ 优秀", "👍 良好", "👌 一般"]
    for i, opt in enumerate(options3):
        text = u(opt)
        radio_id = dll.CreateRadioButton(main_win, x_offset + 20, y_pos, 200, 40, text, len(text), 3, 1 if i==0 else 0,
            ARGB(255,230,162,60), ARGB(255,255,255,255), font, len(font), 15, 0, 0, 0)
        dll.SetRadioButtonStyle(radio_id, RADIO_STYLE_BORDER)  # 设置边框样式
        dll.SetRadioButtonDotColor(radio_id, ARGB(255,230,162,60))
        dll.SetRadioButtonCallback(radio_id, _radio_cb)
        group3_radios.append(radio_id)
        y_pos += 50

    radio_groups["组3"] = group3_radios

    # ========== 组4: 颜色主题 ==========
    y_pos = 320

    title4 = u("📍 组4: 颜色主题选择")
    dll.CreateLabel(main_win, 20, y_pos, 860, 30, title4, len(title4),
        ARGB(255,245,108,108), ARGB(0,0,0,0), font, len(font), 14, 1, 0, 0, 0, 0)
    y_pos += 40

    colors = [
        ("🔴 红色主题", ARGB(255,245,108,108)),
        ("🟢 绿色主题", ARGB(255,103,194,58)),
        ("🔵 蓝色主题", ARGB(255,64,158,255)),
        ("🟣 紫色主题", ARGB(255,155,89,182)),
        ("🟠 橙色主题", ARGB(255,230,162,60)),
    ]

    group4_radios = []
    x_pos = 40
    for i, (text_str, color) in enumerate(colors):
        text = u(text_str)
        radio_id = dll.CreateRadioButton(main_win, x_pos, y_pos, 160, 30, text, len(text), 4, 1 if i==2 else 0,
            color, ARGB(255,255,255,255), font, len(font), 13, 0, 0, 0)
        dll.SetRadioButtonCallback(radio_id, _radio_cb)
        group4_radios.append(radio_id)
        x_pos += 170

    radio_groups["组4"] = group4_radios

    # ========== 组5: 样式测试 - 按钮样式 ==========
    y_pos = 420

    title5 = u("📍 组5: 按钮样式 (BUTTON)")
    dll.CreateLabel(main_win, 20, y_pos, 400, 30, title5, len(title5),
        ARGB(255,144,147,153), ARGB(0,0,0,0), font, len(font), 14, 1, 0, 0, 0, 0)
    y_pos += 40

    group5_radios = []
    options5 = ["选项 A", "选项 B", "选项 C", "选项 D", "选项 E"]
    for i, opt in enumerate(options5):
        text = u(opt)
        radio_id = dll.CreateRadioButton(main_win, 40, y_pos, 150, 30, text, len(text), 5, 1 if i==2 else 0,
            ARGB(255,255,255,255), ARGB(255,64,158,255), font, len(font), 12, 0, 0, 0)
        dll.SetRadioButtonStyle(radio_id, RADIO_STYLE_BUTTON)  # 设置按钮样式
        dll.SetRadioButtonCallback(radio_id, _radio_cb)
        group5_radios.append(radio_id)
        y_pos += 35

    radio_groups["组5"] = group5_radios

    # ========== 组6: 混合样式展示 ==========
    y_pos = 620
    x_offset = 20

    title6 = u("📍 组6: 混合样式对比")
    dll.CreateLabel(main_win, x_offset, y_pos, 600, 30, title6, len(title6),
        ARGB(255,155,89,182), ARGB(0,0,0,0), font, len(font), 14, 1, 0, 0, 0, 0)
    y_pos += 40

    group6_radios = []
    options6 = [
        ("😀 默认样式", RADIO_STYLE_DEFAULT, ARGB(255,64,158,255)),
        ("😐 边框样式", RADIO_STYLE_BORDER, ARGB(255,230,162,60)),
        ("😢 按钮样式", RADIO_STYLE_BUTTON, ARGB(255,103,194,58))
    ]
    x_pos = x_offset + 20
    for i, (opt, style, color) in enumerate(options6):
        text = u(opt)
        radio_id = dll.CreateRadioButton(main_win, x_pos, y_pos, 180, 35, text, len(text), 6, 1 if i==0 else 0,
            ARGB(255,255,255,255) if style == RADIO_STYLE_BUTTON else color,
            color if style == RADIO_STYLE_BUTTON else ARGB(255,255,255,255),
            font, len(font), 13, 0, 0, 0)
        dll.SetRadioButtonStyle(radio_id, style)
        if style != RADIO_STYLE_BUTTON:
            dll.SetRadioButtonDotColor(radio_id, color)
        dll.SetRadioButtonCallback(radio_id, _radio_cb)
        group6_radios.append(radio_id)
        x_pos += 200

    radio_groups["组6"] = group6_radios

    # 底部说明
    y_pos = 720
    info = u("💡 提示: 演示了3种单选框样式 - DEFAULT(圆形), BORDER(边框), BUTTON(按钮)")
    dll.CreateLabel(main_win, 20, y_pos, 860, 30, info, len(info),
        ARGB(255,144,147,153), ARGB(0,0,0,0), font, len(font), 12, 0, 0, 0, 0, 1)

    # 打印初始状态
    print("\n--- 🔘 单选框初始状态 ---")
    for group_name, radios in radio_groups.items():
        for i, radio_id in enumerate(radios):
            checked = dll.GetRadioButtonState(radio_id)
            status = "✓ 选中" if checked else "○ 未选中"
            print(f"{group_name} 选项{i+1}: {status}")

    dll.set_message_loop_main_window(main_win)
    print("\n✅ 进入消息循环...")
    dll.run_message_loop()
    print("程序退出。")

if __name__ == "__main__":
    main()
