using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowD2DComboBoxDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new D2DComboBoxDemoApp().Run();
        }
    }

    internal sealed class D2DComboBoxDemoApp : DemoApp
    {
        private IntPtr _combo;
        private EmojiWindowNative.ComboBoxCallback _comboCallback;

        public D2DComboBoxDemoApp()
            : base("EmojiWindow D2DComboBox Demo - C# .NET 4.0", 880, 500)
        {
        }

        protected override void Build()
        {
            CreateHeader("D2DComboBox Demo", "Direct2D ComboBox sample.");

            CreateGroupBox(WindowHandle, "D2DComboBox Stage", 18, 84, 840, 160, ColorPrimary);
            _combo = EmojiWindowNative.CreateD2DComboBox(WindowHandle, 46, 169, 420, 38, false, ColorText, ColorWhite, 32, FontYaHei, FontYaHei.Length, 12, false, false, false);
            SeedItems();
            _comboCallback = new EmojiWindowNative.ComboBoxCallback(OnComboChanged);
            EmojiWindowNative.SetD2DComboBoxCallback(_combo, _comboCallback);

            IntPtr ops = CreateGroupBox(WindowHandle, "D2DComboBox Actions", 18, 264, 840, 160, ColorSuccess);
            AddButton(ops, "R", "Read Text", 24, 48, 120, 34, ColorPrimary, ReadText);
            AddButton(ops, "W", "Set Text", 158, 48, 120, 34, ColorSuccess, SetText);
            AddButton(ops, "C", "Colors", 292, 48, 120, 34, ColorWarning, ChangeColors);
            AddButton(ops, "2", "Select #2", 426, 48, 120, 34, ColorDanger, delegate
            {
                EmojiWindowNative.SetComboSelectedIndex(_combo, 1);
                SetStatus("Selected item #2.");
            });
        }

        private void SeedItems()
        {
            string[] items = new string[] { "🎨 Design", "📊 Data", "🧭 Navigation" };
            int i;
            for (i = 0; i < items.Length; i++)
            {
                byte[] bytes = U(items[i]);
                EmojiWindowNative.AddD2DComboItem(_combo, bytes, bytes.Length);
            }

            EmojiWindowNative.SetD2DComboSelectedIndex(_combo, 0);
        }

        private void ReadText()
        {
            SetStatus("D2DComboBox text: " + EmojiWindowNative.ReadText(_combo, EmojiWindowNative.GetD2DComboText));
        }

        private void SetText()
        {
            byte[] bytes = U("🧪 Custom D2D text");
            EmojiWindowNative.SetD2DComboText(_combo, bytes, bytes.Length);
            SetStatus("D2DComboBox text updated.");
        }

        private void ChangeColors()
        {
            EmojiWindowNative.SetD2DComboBoxColors(_combo, ColorPrimary, ColorCard, EmojiWindowNative.ARGB(255, 204, 232, 255), EmojiWindowNative.ARGB(255, 232, 244, 253), ColorPrimary, ColorPrimary);
            SetStatus("D2DComboBox colors updated.");
        }

        private void OnComboChanged(IntPtr hComboBox, int index)
        {
            SetStatus("D2DComboBox callback: index=" + index);
        }
    }
}
