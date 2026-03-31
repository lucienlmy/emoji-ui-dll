using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowCheckBoxDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new CheckBoxDemoApp().Run();
        }
    }

    internal sealed class CheckBoxDemoApp : DemoApp
    {
        private IntPtr _defaultCheck;
        private IntPtr _fillCheck;
        private IntPtr _buttonCheck;
        private EmojiWindowNative.CheckBoxCallback _checkCallback;

        public CheckBoxDemoApp()
            : base("EmojiWindow CheckBox Demo - C# .NET 4.0", 920, 560)
        {
        }

        protected override void Build()
        {
            CreateHeader("CheckBox 控件示例", "演示状态读取、样式切换、文本更新和回调。");

            IntPtr stage = CreateGroupBox(WindowHandle, "CheckBox 舞台", 18, 84, 870, 220, ColorPrimary);
            _defaultCheck = CreateCheck(stage, "默认风格", 24, 54, true);
            _fillCheck = CreateCheck(stage, "填充风格", 24, 102, false);
            _buttonCheck = CreateCheck(stage, "按钮风格", 24, 150, true);
            EmojiWindowNative.SetCheckBoxStyle(_fillCheck, EmojiWindowNative.CheckBoxStyleFill);
            EmojiWindowNative.SetCheckBoxStyle(_buttonCheck, EmojiWindowNative.CheckBoxStyleButton);

            _checkCallback = new EmojiWindowNative.CheckBoxCallback(OnCheckChanged);
            EmojiWindowNative.SetCheckBoxCallback(_defaultCheck, _checkCallback);
            EmojiWindowNative.SetCheckBoxCallback(_fillCheck, _checkCallback);
            EmojiWindowNative.SetCheckBoxCallback(_buttonCheck, _checkCallback);

            IntPtr ops = CreateGroupBox(WindowHandle, "CheckBox 操作", 18, 324, 870, 180, ColorSuccess);
            AddButton(ops, "🔄", "切默认状态", 24, 50, 126, 34, ColorPrimary, ToggleDefault);
            AddButton(ops, "🎨", "切填充样式", 164, 50, 126, 34, ColorSuccess, ToggleFillStyle);
            AddButton(ops, "✏️", "改按钮文案", 304, 50, 126, 34, ColorWarning, RenameButtonCheck);
            AddButton(ops, "📖", "读取全部状态", 444, 50, 140, 34, ColorDanger, ReadAllState);
            AddButton(ops, "🧱", "按钮改卡片风格", 598, 50, 160, 34, ColorPrimary, ChangeButtonStyle);
        }

        private IntPtr CreateCheck(IntPtr parent, string text, int x, int y, bool isChecked)
        {
            byte[] textBytes = U(text);
            return EmojiWindowNative.CreateCheckBox(parent, x, y, 220, 36, textBytes, textBytes.Length, isChecked, ColorText, ColorWhite, FontYaHei, FontYaHei.Length, 13, false, false, false);
        }

        private void ToggleDefault()
        {
            EmojiWindowNative.SetCheckBoxState(_defaultCheck, !EmojiWindowNative.GetCheckBoxState(_defaultCheck));
            SetStatus("默认 CheckBox 状态已切换。");
        }

        private void ToggleFillStyle()
        {
            int style = EmojiWindowNative.GetCheckBoxStyle(_fillCheck);
            EmojiWindowNative.SetCheckBoxStyle(_fillCheck, style == EmojiWindowNative.CheckBoxStyleFill ? EmojiWindowNative.CheckBoxStyleCard : EmojiWindowNative.CheckBoxStyleFill);
            SetStatus("填充 CheckBox 风格已切换。");
        }

        private void RenameButtonCheck()
        {
            byte[] text = U("已改名按钮复选框");
            EmojiWindowNative.SetCheckBoxText(_buttonCheck, text, text.Length);
            SetStatus("按钮风格复选框文案已更新。");
        }

        private void ReadAllState()
        {
            string text = "默认=" + EmojiWindowNative.GetCheckBoxState(_defaultCheck) +
                          ", 填充=" + EmojiWindowNative.GetCheckBoxState(_fillCheck) +
                          ", 按钮=" + EmojiWindowNative.GetCheckBoxState(_buttonCheck);
            SetStatus(text);
        }

        private void ChangeButtonStyle()
        {
            EmojiWindowNative.SetCheckBoxStyle(_buttonCheck, EmojiWindowNative.CheckBoxStyleCard);
            EmojiWindowNative.SetCheckBoxColor(_buttonCheck, ColorPrimary, ColorCard);
            SetStatus("按钮复选框已切换为卡片风格。");
        }

        private void OnCheckChanged(IntPtr hCheckBox, int isChecked)
        {
            SetStatus("CheckBox 回调: hwnd=0x" + hCheckBox.ToInt64().ToString("X") + ", checked=" + isChecked);
        }
    }
}
