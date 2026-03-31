using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowColorEmojiEditBoxDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new ColorEmojiEditBoxDemoApp().Run();
        }
    }

    internal sealed class ColorEmojiEditBoxDemoApp : DemoApp
    {
        private IntPtr _emojiEdit;

        public ColorEmojiEditBoxDemoApp()
            : base("EmojiWindow ColorEmojiEditBox Demo - C# .NET 4.0", 940, 540)
        {
        }

        protected override void Build()
        {
            CreateHeader("ColorEmojiEditBox Demo", "RichEdit-based color emoji input sample.");

            CreateGroupBox(WindowHandle, "ColorEmojiEditBox Stage", 18, 84, 890, 220, ColorPrimary);
            _emojiEdit = CreateColorEmojiEdit(WindowHandle);
            CreateLabel(WindowHandle, "This edit box is created on the main window instead of the GroupBox.", 52, 263, 760, 22, ColorMuted, ColorWhite, 11, false, false, EmojiWindowNative.AlignLeft);

            IntPtr ops = CreateGroupBox(WindowHandle, "Actions", 18, 324, 890, 160, ColorSuccess);
            AddButton(ops, "E", "Emoji Text", 24, 50, 140, 34, ColorPrimary, FillEmojiText);
            AddButton(ops, "R", "Read Text", 178, 50, 120, 34, ColorSuccess, ReadText);
            AddButton(ops, "L", "Light Theme", 312, 50, 120, 34, ColorWarning, ApplyLightPalette);
            AddButton(ops, "D", "Dark Theme", 446, 50, 120, 34, ColorDanger, ApplyDarkPalette);
            AddButton(ops, "P", "Plain Text", 580, 50, 120, 34, ColorPrimary, FillPlainText);
        }

        private IntPtr CreateColorEmojiEdit(IntPtr parent)
        {
            byte[] text = U("Emoji Window\r\nColor emoji input\r\nC# / .NET 4.0");
            return EmojiWindowNative.CreateColorEmojiEditBox(parent, 52, 151, 520, 92, text, text.Length, ColorText, ColorWhite, FontYaHei, FontYaHei.Length, 12, false, false, false, EmojiWindowNative.AlignLeft, true, false, false, true, false);
        }

        private void FillEmojiText()
        {
            byte[] text = U("Emoji test ok\r\nSupports multiple lines\r\nMixed text is also supported");
            EmojiWindowNative.SetEditBoxText(_emojiEdit, text, text.Length);
            SetStatus("Updated with emoji sample text.");
        }

        private void FillPlainText()
        {
            byte[] text = U("ColorEmojiEditBox can also show plain text.\r\nThis paragraph is used for comparison.");
            EmojiWindowNative.SetEditBoxText(_emojiEdit, text, text.Length);
            SetStatus("Switched back to plain text.");
        }

        private void ReadText()
        {
            SetStatus("Current text: " + EmojiWindowNative.ReadText(_emojiEdit, EmojiWindowNative.GetEditBoxText));
        }

        private void ApplyLightPalette()
        {
            EmojiWindowNative.SetD2DEditBoxColor(_emojiEdit, ColorPrimary, ColorCard);
            SetStatus("Applied light palette.");
        }

        private void ApplyDarkPalette()
        {
            EmojiWindowNative.SetD2DEditBoxColor(_emojiEdit, ColorWhite, EmojiWindowNative.ARGB(255, 43, 47, 54));
            SetStatus("Applied dark palette.");
        }
    }
}
