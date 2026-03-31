using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowComboBoxDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new ComboBoxDemoApp().Run();
        }
    }

    internal sealed class ComboBoxDemoApp : DemoApp
    {
        private IntPtr _readOnlyCombo;
        private IntPtr _editableCombo;
        private EmojiWindowNative.ComboBoxCallback _comboCallback;

        public ComboBoxDemoApp()
            : base("EmojiWindow ComboBox Demo - C# .NET 4.0", 920, 540)
        {
        }

        protected override void Build()
        {
            const int stageX = 18;
            const int stageY = 84;
            const int groupContentLeft = 10;
            const int groupContentTop = 25;

            CreateHeader("ComboBox Demo", "Read-only and editable ComboBox examples.");

            CreateGroupBox(WindowHandle, "ComboBox Stage", stageX, stageY, 880, 220, ColorPrimary);
            CreateLabel(WindowHandle, "Read-only ComboBox", stageX + groupContentLeft + 18, stageY + groupContentTop + 34, 180, 20, ColorMuted, ColorWhite, 11, false, false, EmojiWindowNative.AlignLeft);
            _readOnlyCombo = CreateCombo(WindowHandle, stageX + groupContentLeft + 18, stageY + groupContentTop + 60, true);
            CreateLabel(WindowHandle, "Editable ComboBox", stageX + groupContentLeft + 18, stageY + groupContentTop + 116, 180, 20, ColorMuted, ColorWhite, 11, false, false, EmojiWindowNative.AlignLeft);
            _editableCombo = CreateCombo(WindowHandle, stageX + groupContentLeft + 18, stageY + groupContentTop + 142, false);

            _comboCallback = new EmojiWindowNative.ComboBoxCallback(OnComboChanged);
            EmojiWindowNative.SetComboBoxCallback(_readOnlyCombo, _comboCallback);
            EmojiWindowNative.SetComboBoxCallback(_editableCombo, _comboCallback);

            IntPtr ops = CreateGroupBox(WindowHandle, "ComboBox Actions", 18, 324, 880, 170, ColorSuccess);
            AddButton(ops, "R", "Read Selected", 24, 48, 126, 34, ColorPrimary, ReadReadOnly);
            AddButton(ops, "W", "Write Text", 164, 48, 140, 34, ColorSuccess, UpdateEditableText);
            AddButton(ops, "T", "Read Text", 318, 48, 140, 34, ColorWarning, ReadEditableText);
            AddButton(ops, "+", "Add Item", 472, 48, 110, 34, ColorDanger, AddOption);
            AddButton(ops, "2", "Select #2", 596, 48, 126, 34, ColorPrimary, delegate
            {
                EmojiWindowNative.SetComboSelectedIndex(_readOnlyCombo, 1);
                SetStatus("Selected item #2.");
            });
        }

        private IntPtr CreateCombo(IntPtr parent, int x, int y, bool readOnly)
        {
            IntPtr combo = EmojiWindowNative.CreateComboBox(parent, x, y, 360, 36, readOnly, ColorText, ColorWhite, 30, FontYaHei, FontYaHei.Length, 12, false, false, false);
            string[] items = new string[] { "Stable", "Test", "Preview" };
            int i;
            for (i = 0; i < items.Length; i++)
            {
                byte[] bytes = U(items[i]);
                EmojiWindowNative.AddComboItem(combo, bytes, bytes.Length);
            }

            EmojiWindowNative.SetComboSelectedIndex(combo, 0);
            return combo;
        }

        private void ReadReadOnly()
        {
            int index = EmojiWindowNative.GetComboSelectedIndex(_readOnlyCombo);
            SetStatus("Read-only ComboBox: " + EmojiWindowNative.ReadIndexedText(_readOnlyCombo, index, EmojiWindowNative.GetComboItemText));
        }

        private void UpdateEditableText()
        {
            byte[] text = U("Custom text from C#");
            EmojiWindowNative.SetComboBoxText(_editableCombo, text, text.Length);
            SetStatus("Editable ComboBox text updated.");
        }

        private void ReadEditableText()
        {
            SetStatus("Editable text: " + EmojiWindowNative.ReadText(_editableCombo, EmojiWindowNative.GetComboBoxText));
        }

        private void AddOption()
        {
            string text = "Item " + (EmojiWindowNative.GetComboItemCount(_editableCombo) + 1);
            byte[] bytes = U(text);
            EmojiWindowNative.AddComboItem(_editableCombo, bytes, bytes.Length);
            SetStatus("Added a new item.");
        }

        private void OnComboChanged(IntPtr hComboBox, int index)
        {
            SetStatus("ComboBox callback: index=" + index);
        }
    }
}
