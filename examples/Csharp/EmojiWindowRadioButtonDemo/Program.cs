using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowRadioButtonDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new RadioButtonDemoApp().Run();
        }
    }

    internal sealed class RadioButtonDemoApp : DemoApp
    {
        private IntPtr _radioA;
        private IntPtr _radioB;
        private IntPtr _radioC;
        private EmojiWindowNative.RadioButtonCallback _radioCallback;

        public RadioButtonDemoApp()
            : base("EmojiWindow RadioButton Demo - C# .NET 4.0", 900, 540)
        {
        }

        protected override void Build()
        {
            CreateHeader("RadioButton 控件示例", "演示分组单选、样式更新和选择回调。");

            IntPtr stage = CreateGroupBox(WindowHandle, "RadioButton 舞台", 18, 84, 850, 210, ColorPrimary);
            _radioA = CreateRadio(stage, "默认风格", 24, 52, 101, true);
            _radioB = CreateRadio(stage, "边框风格", 24, 100, 101, false);
            _radioC = CreateRadio(stage, "按钮风格", 24, 148, 101, false);
            EmojiWindowNative.SetRadioButtonStyle(_radioB, EmojiWindowNative.RadioStyleBorder);
            EmojiWindowNative.SetRadioButtonStyle(_radioC, EmojiWindowNative.RadioStyleButton);

            _radioCallback = new EmojiWindowNative.RadioButtonCallback(OnRadioChanged);
            EmojiWindowNative.SetRadioButtonCallback(_radioA, _radioCallback);
            EmojiWindowNative.SetRadioButtonCallback(_radioB, _radioCallback);
            EmojiWindowNative.SetRadioButtonCallback(_radioC, _radioCallback);

            IntPtr ops = CreateGroupBox(WindowHandle, "RadioButton 操作", 18, 314, 850, 170, ColorSuccess);
            AddButton(ops, "1️⃣", "选中默认", 24, 48, 110, 34, ColorPrimary, delegate { SelectRadio(_radioA); });
            AddButton(ops, "2️⃣", "选中边框", 148, 48, 110, 34, ColorSuccess, delegate { SelectRadio(_radioB); });
            AddButton(ops, "3️⃣", "选中按钮", 272, 48, 110, 34, ColorWarning, delegate { SelectRadio(_radioC); });
            AddButton(ops, "🎨", "按钮改颜色", 396, 48, 126, 34, ColorDanger, RecolorButtonRadio);
            AddButton(ops, "📖", "读取状态", 536, 48, 110, 34, ColorPrimary, ReadState);
        }

        private IntPtr CreateRadio(IntPtr parent, string text, int x, int y, int groupId, bool isChecked)
        {
            byte[] textBytes = U(text);
            return EmojiWindowNative.CreateRadioButton(parent, x, y, 240, 36, textBytes, textBytes.Length, groupId, isChecked, ColorText, ColorWhite, FontYaHei, FontYaHei.Length, 13, false, false, false);
        }

        private void SelectRadio(IntPtr radio)
        {
            EmojiWindowNative.SetRadioButtonState(radio, true);
            SetStatus("已切换单选项。");
        }

        private void RecolorButtonRadio()
        {
            EmojiWindowNative.SetRadioButtonColor(_radioC, ColorPrimary, ColorCard);
            EmojiWindowNative.SetRadioButtonDotColor(_radioC, ColorDanger);
            SetStatus("按钮风格单选框已更新配色。");
        }

        private void ReadState()
        {
            string text = "默认=" + EmojiWindowNative.GetRadioButtonState(_radioA) +
                          ", 边框=" + EmojiWindowNative.GetRadioButtonState(_radioB) +
                          ", 按钮=" + EmojiWindowNative.GetRadioButtonState(_radioC);
            SetStatus(text);
        }

        private void OnRadioChanged(IntPtr hRadioButton, int groupId, int isChecked)
        {
            SetStatus("RadioButton 回调: group=" + groupId + ", checked=" + isChecked);
        }
    }
}
