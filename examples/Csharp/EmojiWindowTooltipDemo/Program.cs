using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowTooltipDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new TooltipDemoApp().Run();
        }
    }

    internal sealed class TooltipDemoApp : DemoApp
    {
        private IntPtr _targetLabel;
        private IntPtr _tooltip;

        public TooltipDemoApp()
            : base("EmojiWindow Tooltip Demo - C# .NET 4.0", 860, 460)
        {
        }

        protected override void Build()
        {
            const int stageX = 18;
            const int stageY = 84;
            const int groupContentLeft = 10;
            const int groupContentTop = 25;

            CreateHeader("Tooltip 控件示例", "演示绑定控件、主题切换、触发方式和手动显示。");

            IntPtr stage = CreateGroupBox(WindowHandle, "Tooltip 舞台", stageX, stageY, 820, 140, ColorPrimary);
            _targetLabel = CreateLabel(
                WindowHandle,
                "把鼠标移到这段文字上试试 Tooltip。",
                stageX + groupContentLeft + 24,
                stageY + groupContentTop + 54,
                300,
                26,
                ColorText,
                ColorCard,
                12,
                false,
                false,
                EmojiWindowNative.AlignLeft);
            EmojiWindowNative.AddChildToGroup(stage, _targetLabel);

            byte[] text = U("这里是 Tooltip 文案。");
            _tooltip = EmojiWindowNative.CreateTooltip(WindowHandle, text, text.Length, EmojiWindowNative.PopupTop, ColorText, ColorWhite);
            EmojiWindowNative.BindTooltipToControl(_tooltip, _targetLabel);
            EmojiWindowNative.SetTooltipTrigger(_tooltip, EmojiWindowNative.TooltipTriggerHover);

            IntPtr ops = CreateGroupBox(WindowHandle, "Tooltip 操作", 18, 244, 820, 140, ColorSuccess);
            AddButton(ops, "🌙", "深色主题", 24, 44, 120, 34, ColorPrimary, delegate
            {
                EmojiWindowNative.SetTooltipTheme(_tooltip, EmojiWindowNative.TooltipThemeDark);
                SetStatus("Tooltip 已切到深色主题。");
            });
            AddButton(ops, "☀️", "浅色主题", 158, 44, 120, 34, ColorSuccess, delegate
            {
                EmojiWindowNative.SetTooltipTheme(_tooltip, EmojiWindowNative.TooltipThemeLight);
                SetStatus("Tooltip 已切到浅色主题。");
            });
            AddButton(ops, "📍", "切到底部", 292, 44, 120, 34, ColorWarning, delegate
            {
                EmojiWindowNative.SetTooltipPlacement(_tooltip, EmojiWindowNative.PopupBottom);
                SetStatus("Tooltip 已切到底部。");
            });
            AddButton(ops, "✏️", "改文案", 426, 44, 120, 34, ColorDanger, UpdateTooltipText);
            AddButton(ops, "🙈", "隐藏", 560, 44, 120, 34, ColorPrimary, delegate
            {
                EmojiWindowNative.HideTooltip(_tooltip);
                SetStatus("Tooltip 已隐藏。");
            });
        }

        private void UpdateTooltipText()
        {
            byte[] text = U("Tooltip 文案已更新，可以继续悬停查看。");
            EmojiWindowNative.SetTooltipText(_tooltip, text, text.Length);
            SetStatus("Tooltip 文案已更新。");
        }
    }
}
