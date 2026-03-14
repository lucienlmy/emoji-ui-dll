"""
emoji_window.dll Python 示例程序
展示如何使用 Python 调用 DLL 创建带 Unicode 表情的窗口界面
"""

import os
import sys
from emoji_window import EmojiWindow, Colors


class DemoApp:
    """示例应用程序"""
    
    def __init__(self):
        """初始化应用"""
        print("=== Emoji Window Python 示例 ===")
        print("正在初始化...")
        
        # 初始化 DLL（自动查找可用的 DLL）
        self.ew = EmojiWindow()
        
        # 窗口和控件句柄
        self.main_window = None
        self.checkbox1 = None
        self.label1 = None
    
    def create_ui(self):
        """创建用户界面"""
        print("正在创建窗口...")
        
        # 1. 创建主窗口
        self.main_window = self.ew.create_window(
            "🎨 抖店安全参数生成器 - Python Demo",
            800, 600
        )
        
        if not self.main_window:
            print("❌ 创建窗口失败！")
            sys.exit(1)
        
        print("✅ 窗口创建成功！")
        
        # 2. 创建分组框 - 控制面板
        self.create_group_box1()
        
        # 3. 创建分组框 - 生成结果
        self.create_group_box2()
        
        # 4. 创建分组框 - 验证测试
        self.create_group_box3()
        
        # 5. 设置回调
        self.ew.set_button_callback(self.on_button_click)
        self.ew.set_checkbox_callback(self.checkbox1, self.on_checkbox_changed)
        
        print("✅ 控件创建完成！")
    
    def create_group_box1(self):
        """创建分组框1 - 控制面板"""
        # 分组框
        self.ew.create_group_box(
            self.main_window,
            "📋 控制面板",
            20, 50, 360, 200,
            Colors.BORDER_BASE,
            Colors.BG_LIGHT
        )
        
        # 标签1 - URL
        self.ew.create_label(
            self.main_window,
            "🌐 URL:",
            40, 80, 80, 30,
            Colors.TEXT_PRIMARY,
            Colors.TRANSPARENT
        )
        
        # 标签2 - source
        self.ew.create_label(
            self.main_window,
            "📦 source:",
            40, 120, 80, 30,
            Colors.TEXT_PRIMARY,
            Colors.TRANSPARENT
        )
        
        # 标签3 - appid
        self.ew.create_label(
            self.main_window,
            "🔑 appid:",
            40, 160, 80, 30,
            Colors.TEXT_PRIMARY,
            Colors.TRANSPARENT
        )
        
        # 按钮 - 批量生成
        self.ew.create_button(
            self.main_window,
            "🚀", "批量生成",
            40, 200, 120, 35,
            Colors.PRIMARY
        )
        
        # 复选框
        self.checkbox1 = self.ew.create_checkbox(
            self.main_window,
            "✅ 启用自动刷新",
            180, 205, 150, 30
        )
    
    def create_group_box2(self):
        """创建分组框2 - 生成结果"""
        # 分组框
        self.ew.create_group_box(
            self.main_window,
            "📊 生成结果",
            400, 50, 380, 200,
            Colors.BORDER_BASE,
            Colors.BG_LIGHT
        )
        
        # 标签 - msToken
        self.label1 = self.ew.create_label(
            self.main_window,
            "🔐 msToken: ✓",
            420, 90, 340, 30,
            Colors.SUCCESS,
            Colors.TRANSPARENT,
            bold=True
        )
        
        # 标签 - a_bogus
        self.ew.create_label(
            self.main_window,
            "🔒 a_bogus: ✗",
            420, 130, 340, 30,
            Colors.DANGER,
            Colors.TRANSPARENT,
            bold=True
        )
        
        # 标签 - verifyFp
        self.ew.create_label(
            self.main_window,
            "🛡️ verifyFp: ✓",
            420, 170, 340, 30,
            Colors.SUCCESS,
            Colors.TRANSPARENT,
            bold=True
        )
        
        # 按钮 - 复制
        self.ew.create_button(
            self.main_window,
            "📋", "复制",
            420, 210, 100, 30,
            Colors.SUCCESS
        )
    
    def create_group_box3(self):
        """创建分组框3 - 验证测试"""
        # 分组框
        self.ew.create_group_box(
            self.main_window,
            "🧪 验证测试",
            20, 270, 760, 280,
            Colors.BORDER_BASE,
            Colors.BG_LIGHT
        )
        
        # 标签 - 说明
        self.ew.create_label(
            self.main_window,
            "💡 提示：某些参数可能无法生成，请检查页面是否完全加载。\n"
            "⚠️ 注意：参数生成可能需要一定时间，请耐心等待。",
            40, 310, 720, 60,
            Colors.TEXT_SECONDARY,
            Colors.TRANSPARENT,
            font_size=13,
            word_wrap=True
        )
        
        # 按钮组
        self.ew.create_button(
            self.main_window,
            "📝", "验证参数",
            40, 390, 120, 35,
            Colors.PRIMARY
        )
        
        self.ew.create_button(
            self.main_window,
            "🔄", "测试请求",
            180, 390, 120, 35,
            Colors.WARNING
        )
        
        self.ew.create_button(
            self.main_window,
            "🗑️", "批量生成",
            320, 390, 120, 35,
            Colors.DANGER
        )
        
        # 状态标签
        self.ew.create_label(
            self.main_window,
            "⏱️ 18:15:46 - 生成成功 - msToken: ✓ | a_bogus: ✗ | verifyFp: ✓",
            40, 450, 720, 80,
            Colors.TEXT_PRIMARY,
            Colors.BG_LIGHT,
            font_size=12,
            word_wrap=True
        )
    
    def on_button_click(self, button_id, parent_hwnd):
        """按钮点击回调"""
        print(f"按钮被点击: ID = {button_id}")
        
        # 显示信息框
        self.ew.show_message_box(
            self.main_window,
            "⚠️ 警告",
            "参数生成不完整！\n\n"
            "msToken: ✓ | a_bogus: ✗ | verifyFp: ✓\n\n"
            "某些参数可能无法生成，请检查页面是否完全加载。",
            "⚠️"
        )
    
    def on_checkbox_changed(self, hwnd, checked):
        """复选框状态改变回调"""
        print(f"复选框状态改变: {'选中' if checked else '未选中'}")
        
        if checked:
            # 更新标签文本
            self.ew.set_label_text(
                self.label1,
                "🔐 msToken: ✓ (自动刷新中...)"
            )
    
    def run(self):
        """运行应用"""
        try:
            # 创建界面
            self.create_ui()
            
            # 设置主窗口
            self.ew.set_main_window(self.main_window)
            
            print("✅ 进入消息循环...")
            print("=" * 40)
            
            # 运行消息循环
            self.ew.run_message_loop()
            
            print("程序退出。")
        
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            import traceback
            traceback.print_exc()


def main():
    """主函数"""
    app = DemoApp()
    app.run()


if __name__ == "__main__":
    main()
