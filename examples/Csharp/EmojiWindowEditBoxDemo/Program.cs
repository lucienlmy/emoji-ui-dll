using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowEditBoxDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new EditBoxDemoApp().Run();
        }
    }

    internal sealed class EditBoxDemoApp : DemoApp
    {
        private IntPtr _singleEdit;
        private IntPtr _multiEdit;
        private bool _singleEnabled;

        public EditBoxDemoApp()
            : base("EmojiWindow EditBox Demo - C# .NET 4.0", 960, 580)
        {
            _singleEnabled = true;
        }

        protected override void Build()
        {
            const int stageX = 18;
            const int stageY = 84;
            const int groupContentLeft = 10;
            const int groupContentTop = 25;

            CreateHeader("EditBox Demo", "Single-line and multi-line EditBox sample.");

            CreateGroupBox(WindowHandle, "EditBox Stage", stageX, stageY, 910, 250, ColorPrimary);
            CreateLabel(WindowHandle, "Single-line EditBox", stageX + groupContentLeft + 24, stageY + groupContentTop + 28, 160, 20, ColorMuted, ColorWhite, 11, false, false, EmojiWindowNative.AlignLeft);
            _singleEdit = CreateEditBox(WindowHandle, "Single-line EditBox", stageX + groupContentLeft + 24, stageY + groupContentTop + 56, 420, 34, false, false);
            CreateLabel(WindowHandle, "Multi-line EditBox", stageX + groupContentLeft + 24, stageY + groupContentTop + 108, 160, 20, ColorMuted, ColorWhite, 11, false, false, EmojiWindowNative.AlignLeft);
            _multiEdit = CreateEditBox(WindowHandle, "Line 1\r\nLine 2\r\nLine 3", stageX + groupContentLeft + 24, stageY + groupContentTop + 136, 520, 84, true, false);

            IntPtr ops = CreateGroupBox(WindowHandle, "EditBox Actions", 18, 354, 910, 180, ColorSuccess);
            AddButton(ops, "R", "Read Single", 24, 50, 120, 34, ColorPrimary, ReadSingle);
            AddButton(ops, "W", "Write Single", 156, 50, 120, 34, ColorSuccess, UpdateSingle);
            AddButton(ops, "M", "Write Multi", 288, 50, 120, 34, ColorWarning, UpdateMulti);
            AddButton(ops, "C", "Recolor", 420, 50, 120, 34, ColorDanger, RecolorSingle);
            AddButton(ops, "A", "Align", 552, 50, 120, 34, ColorPrimary, ChangeAlignment);
            AddButton(ops, "E", "Enable", 684, 50, 120, 34, ColorSuccess, ToggleEnabled);
            AddButton(ops, "P", "Move Multi", 24, 96, 120, 34, ColorWarning, MoveMulti);
        }

        private void ReadSingle()
        {
            SetStatus("Single-line text: " + EmojiWindowNative.ReadText(_singleEdit, EmojiWindowNative.GetEditBoxText));
        }

        private void UpdateSingle()
        {
            byte[] text = U("Updated from C# demo");
            EmojiWindowNative.SetEditBoxText(_singleEdit, text, text.Length);
            SetStatus("Single-line EditBox updated.");
        }

        private void UpdateMulti()
        {
            byte[] text = U("New multi-line content\r\nSupports line breaks\r\nUsed for Get/Set verification");
            EmojiWindowNative.SetEditBoxText(_multiEdit, text, text.Length);
            SetStatus("Multi-line EditBox updated.");
        }

        private void RecolorSingle()
        {
            EmojiWindowNative.SetEditBoxColor(_singleEdit, ColorPrimary, ColorCard);
            SetStatus("Single-line EditBox recolored.");
        }

        private void ChangeAlignment()
        {
            EmojiWindowNative.SetEditBoxAlignment(_singleEdit, EmojiWindowNative.AlignCenter);
            SetStatus("Single-line EditBox aligned center.");
        }

        private void ToggleEnabled()
        {
            _singleEnabled = !_singleEnabled;
            EmojiWindowNative.EnableEditBox(_singleEdit, _singleEnabled);
            SetStatus("Single-line EditBox " + (_singleEnabled ? "enabled." : "disabled."));
        }

        private void MoveMulti()
        {
            EmojiWindowNative.SetEditBoxBounds(_multiEdit, 308, 245, 264, 84);
            SetStatus("Moved multi-line EditBox to the right.");
        }
    }
}
