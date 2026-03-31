using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowPanelDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new PanelDemoApp().Run();
        }
    }

    internal sealed class PanelDemoApp : DemoApp
    {
        private IntPtr _leftPanel;
        private IntPtr _centerPanel;
        private IntPtr _rightPanel;

        public PanelDemoApp()
            : base("EmojiWindow Panel Demo - C# .NET 4.0", 980, 560)
        {
        }

        protected override void Build()
        {
            CreateHeader("Panel 控件示例", "演示 Panel 作为背景容器和分区容器的用法。");

            _leftPanel = CreatePanel(WindowHandle, 24, 92, 220, 280, ColorCard);
            _centerPanel = CreatePanel(WindowHandle, 264, 92, 300, 280, EmojiWindowNative.ARGB(255, 236, 245, 255));
            _rightPanel = CreatePanel(WindowHandle, 584, 92, 340, 280, EmojiWindowNative.ARGB(255, 245, 250, 236));

            CreateLabel(_leftPanel, "左侧 Panel", 16, 18, 180, 22, ColorText, ColorCard, 13, true, false, EmojiWindowNative.AlignLeft);
            CreateLabel(_centerPanel, "中间 Panel", 16, 18, 180, 22, ColorText, EmojiWindowNative.ARGB(255, 236, 245, 255), 13, true, false, EmojiWindowNative.AlignLeft);
            CreateLabel(_rightPanel, "右侧 Panel", 16, 18, 180, 22, ColorText, EmojiWindowNative.ARGB(255, 245, 250, 236), 13, true, false, EmojiWindowNative.AlignLeft);

            AddButton(_leftPanel, "📋", "左侧按钮", 16, 58, 120, 34, ColorPrimary, delegate { SetStatus("点击了左侧 Panel 内按钮。"); });
            AddButton(_centerPanel, "📊", "中间按钮", 16, 58, 120, 34, ColorSuccess, delegate { SetStatus("点击了中间 Panel 内按钮。"); });
            AddButton(_rightPanel, "⚙️", "右侧按钮", 16, 58, 120, 34, ColorWarning, delegate { SetStatus("点击了右侧 Panel 内按钮。"); });

            IntPtr ops = CreateGroupBox(WindowHandle, "Panel 操作", 24, 392, 900, 130, ColorPrimary);
            AddButton(ops, "🎨", "左侧改色", 24, 44, 120, 34, ColorPrimary, delegate { EmojiWindowNative.SetPanelBackgroundColor(_leftPanel, EmojiWindowNative.ARGB(255, 255, 244, 230)); SetStatus("左侧 Panel 已改色。"); });
            AddButton(ops, "🎨", "中间改色", 160, 44, 120, 34, ColorSuccess, delegate { EmojiWindowNative.SetPanelBackgroundColor(_centerPanel, EmojiWindowNative.ARGB(255, 235, 248, 240)); SetStatus("中间 Panel 已改色。"); });
            AddButton(ops, "🎨", "右侧改色", 296, 44, 120, 34, ColorWarning, delegate { EmojiWindowNative.SetPanelBackgroundColor(_rightPanel, EmojiWindowNative.ARGB(255, 255, 240, 240)); SetStatus("右侧 Panel 已改色。"); });
            AddButton(ops, "📖", "读右侧颜色", 432, 44, 120, 34, ColorDanger, ReadRightColor);
        }

        private void ReadRightColor()
        {
            SetStatus("右侧 Panel 背景色 = 0x" + EmojiWindowNative.GetPanelBackgroundColor(_rightPanel).ToString("X8"));
        }
    }
}
