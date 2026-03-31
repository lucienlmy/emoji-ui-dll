using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowLabelDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new LabelDemoApp().Run();
        }
    }

    internal sealed class LabelDemoApp : DemoApp
    {
        private IntPtr _label;
        private bool _visible;
        private int _fontSize;

        public LabelDemoApp()
            : base("EmojiWindow Label Demo - C# .NET 4.0", 900, 520)
        {
            _visible = true;
            _fontSize = 14;
        }

        protected override void Build()
        {
            CreateHeader("Label 控件示例", "演示文本、颜色、对齐、边界和可见状态。");

            CreateGroupBox(WindowHandle, "Label 舞台", 18, 84, 850, 180, ColorPrimary);
            _label = CreateLabel(WindowHandle, "这是一个可被动态修改的 Label。\r\n你可以切换颜色、对齐方式和显示状态。", 52, 155, 770, 70, ColorText, ColorWhite, 14, false, true, EmojiWindowNative.AlignLeft);

            IntPtr ops = CreateGroupBox(WindowHandle, "Label 操作", 18, 284, 850, 190, ColorSuccess);
            AddButton(ops, "✏️", "改文案", 24, 54, 110, 34, ColorPrimary, ChangeText);
            AddButton(ops, "🎨", "改颜色", 148, 54, 110, 34, ColorSuccess, ChangeColor);
            AddButton(ops, "A+", "改字号", 272, 54, 110, 34, ColorWarning, ChangeFontSize);
            AddButton(ops, "👁️", "显隐", 396, 54, 110, 34, ColorDanger, ToggleVisible);
            AddButton(ops, "📐", "放大区域", 520, 54, 120, 34, ColorPrimary, ResizeLabel);
            AddButton(ops, "📖", "读对齐", 654, 54, 110, 34, ColorSuccess, ReadAlign);
        }

        private void ChangeText()
        {
            byte[] text = U("Label 文案已更新。\r\n现在这一段文字更长，用于观察换行和布局效果。");
            EmojiWindowNative.SetLabelText(_label, text, text.Length);
            SetStatus("Label 文案已更新。");
        }

        private void ChangeColor()
        {
            uint color = ColorPrimary;
            long mode = DateTime.Now.Ticks % 3;
            if (mode == 1)
            {
                color = ColorSuccess;
            }
            else if (mode == 2)
            {
                color = ColorDanger;
            }

            EmojiWindowNative.SetLabelColor(_label, color, ColorCard);
            SetStatus("Label 前景色已切换。");
        }

        private void ChangeFontSize()
        {
            _fontSize = _fontSize == 14 ? 18 : 14;
            EmojiWindowNative.SetLabelFont(_label, FontYaHei, FontYaHei.Length, _fontSize, false, false, false);
            SetStatus("Label 字号已切换到 " + _fontSize);
        }

        private void ToggleVisible()
        {
            _visible = !_visible;
            EmojiWindowNative.ShowLabel(_label, _visible);
            SetStatus("Label 已" + (_visible ? "显示" : "隐藏"));
        }

        private void ResizeLabel()
        {
            EmojiWindowNative.SetLabelBounds(_label, 52, 155, 500, 92);
            SetStatus("Label 区域已缩窄，用于观察自动换行。");
        }

        private void ReadAlign()
        {
            SetStatus("GetLabelAlignment 返回: " + EmojiWindowNative.GetLabelAlignment(_label));
        }
    }
}
