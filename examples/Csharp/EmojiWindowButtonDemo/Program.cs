using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowButtonDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new ButtonDemoApp().Run();
        }
    }

    internal sealed class ButtonDemoApp : DemoApp
    {
        private int _primaryButton;
        private int _secondaryButton;
        private int _ghostButton;
        private bool _secondaryEnabled;
        private bool _ghostVisible;
        private int _styleIndex;

        public ButtonDemoApp()
            : base("EmojiWindow Button Demo - C# .NET 4.0", 940, 560)
        {
            _secondaryEnabled = true;
            _ghostVisible = true;
        }

        protected override void Build()
        {
            CreateHeader("Button Demo", "Button text, style and visibility sample.");

            IntPtr stage = CreateGroupBox(WindowHandle, "Button Stage", 18, 84, 886, 200, ColorPrimary);
            _primaryButton = AddButton(stage, "A", "Primary", 24, 70, 150, 40, ColorPrimary, delegate { SetStatus("Clicked primary button."); });
            _secondaryButton = AddButton(stage, "B", "Success", 194, 70, 150, 40, ColorSuccess, delegate { SetStatus("Clicked success button."); });
            _ghostButton = AddButton(stage, "C", "Styled", 364, 70, 150, 40, ColorWarning, delegate { SetStatus("Clicked styled button."); });
            CreateLabel(WindowHandle, "The label below is created on the main window to avoid GroupBox rendering issues.", 52, 241, 760, 22, ColorMuted, ColorWhite, 11, false, false, EmojiWindowNative.AlignLeft);

            IntPtr ops = CreateGroupBox(WindowHandle, "Button Actions", 18, 304, 886, 210, ColorWarning);
            AddButton(ops, "R", "Read Primary", 24, 46, 126, 34, ColorPrimary, ReadPrimaryText);
            AddButton(ops, "W", "Rename", 164, 46, 140, 34, ColorSuccess, RenamePrimary);
            AddButton(ops, "C", "Recolor", 318, 46, 140, 34, ColorWarning, RecolorPrimary);
            AddButton(ops, "E", "Change Mark", 472, 46, 150, 34, ColorDanger, ReEmojiPrimary);
            AddButton(ops, "S", "Toggle Style", 636, 46, 170, 34, ColorPrimary, ToggleGhostStyle);
            AddButton(ops, "T", "Toggle Enabled", 24, 94, 126, 34, ColorDanger, ToggleSecondaryEnabled);
            AddButton(ops, "V", "Toggle Visible", 164, 94, 140, 34, ColorPrimary, ToggleGhostVisible);
            AddButton(ops, "M", "Move Primary", 318, 94, 140, 34, ColorSuccess, MovePrimaryButton);
        }

        private void ReadPrimaryText()
        {
            string text = EmojiWindowNative.ReadText(_primaryButton, EmojiWindowNative.GetButtonText);
            string emoji = EmojiWindowNative.ReadText(_primaryButton, EmojiWindowNative.GetButtonEmoji);
            SetStatus("Primary button: " + emoji + " " + text);
        }

        private void RenamePrimary()
        {
            byte[] text = U("Renamed");
            EmojiWindowNative.SetButtonText(_primaryButton, text, text.Length);
            SetStatus("Primary button text updated.");
        }

        private void RecolorPrimary()
        {
            uint[] colors = new uint[] { ColorPrimary, ColorSuccess, ColorWarning, ColorDanger };
            uint color = colors[(int)(DateTime.Now.Ticks % colors.Length)];
            EmojiWindowNative.SetButtonBackgroundColor(_primaryButton, color);
            SetStatus("Primary button color updated.");
        }

        private void ReEmojiPrimary()
        {
            string[] emojis = new string[] { "A", "B", "C", "D" };
            string value = emojis[(int)(DateTime.Now.Ticks % emojis.Length)];
            byte[] bytes = U(value);
            EmojiWindowNative.SetButtonEmoji(_primaryButton, bytes, bytes.Length);
            SetStatus("Primary button mark changed to " + value);
        }

        private void ToggleGhostStyle()
        {
            _styleIndex = (_styleIndex + 1) % 3;
            EmojiWindowNative.SetButtonStyle(_ghostButton, _styleIndex);
            SetStatus("Styled button style=" + _styleIndex);
        }

        private void ToggleSecondaryEnabled()
        {
            _secondaryEnabled = !_secondaryEnabled;
            EmojiWindowNative.EnableButton(WindowHandle, _secondaryButton, _secondaryEnabled);
            SetStatus("Success button " + (_secondaryEnabled ? "enabled." : "disabled."));
        }

        private void ToggleGhostVisible()
        {
            _ghostVisible = !_ghostVisible;
            EmojiWindowNative.ShowButton(_ghostButton, _ghostVisible);
            SetStatus("Styled button " + (_ghostVisible ? "visible." : "hidden."));
        }

        private void MovePrimaryButton()
        {
            int x;
            int y;
            int width;
            int height;
            EmojiWindowNative.GetButtonBounds(_primaryButton, out x, out y, out width, out height);
            EmojiWindowNative.SetButtonBounds(_primaryButton, x + 10, y, width, height);
            SetStatus("Moved primary button by 10 pixels.");
        }
    }
}
