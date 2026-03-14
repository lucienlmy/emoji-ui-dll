"""
简单测试脚本 - 快速验证 DLL 是否可用
"""

from emoji_window import EmojiWindow, Colors

print("=== 简单测试 ===")
print()

# 1. 初始化
print("1. 初始化 DLL...")
ew = EmojiWindow()
print()

# 2. 创建窗口
print("2. 创建窗口...")
hwnd = ew.create_window("🎨 测试窗口", 600, 400)
if hwnd:
    print("✅ 窗口创建成功！")
else:
    print("❌ 窗口创建失败！")
    exit(1)
print()

# 3. 创建标签
print("3. 创建标签...")
label = ew.create_label(
    hwnd,
    "✅ 测试成功！\n\n这是一个简单的测试窗口。\n支持 Unicode 表情：🎉🚀💡",
    50, 50, 500, 150,
    Colors.TEXT_PRIMARY,
    Colors.TRANSPARENT,
    font_size=16,
    word_wrap=True
)
print("✅ 标签创建成功！")
print()

# 4. 创建按钮
print("4. 创建按钮...")
btn_id = ew.create_button(
    hwnd,
    "👋", "关闭窗口",
    50, 220, 120, 40,
    Colors.PRIMARY
)
print("✅ 按钮创建成功！")
print()

# 5. 设置按钮回调
def on_button_click(button_id, parent_hwnd):
    print(f"按钮被点击: ID = {button_id}")
    ew.show_message_box(
        hwnd,
        "✅ 成功",
        "测试完成！\n\nDLL 工作正常。",
        "✅"
    )

ew.set_button_callback(on_button_click)
print("✅ 回调设置成功！")
print()

# 6. 运行消息循环
print("=" * 50)
print("✅ 所有测试通过！")
print("=" * 50)
print()
print("窗口已显示，点击按钮测试回调功能。")
print("关闭窗口退出程序。")
print()

ew.set_main_window(hwnd)
ew.run_message_loop()

print("程序退出。")
