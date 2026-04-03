using System;

namespace EmojiWindowDemo
{
    internal static class StateDemoPage
    {
        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;

            app.GroupBox(16, 16, 700, 330, "☑️ CheckBox / RadioButton 舞台", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(734, 16, 730, 330, "📊 ProgressBar / Slider / Switch 舞台", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(16, 374, 1448, 120, "📋 联合状态读数", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(16, 516, 1448, 262, "📘 状态组件联调说明", DemoTheme.Border, DemoTheme.Background, page);

            IntPtr leftIntro = app.Label(40, 54, 640, 24, "左侧保留两种 CheckBox 和三种 RadioButton，用来验证布尔选择类组件的联动状态。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr rightIntro = app.Label(758, 54, 660, 24, "右侧集中展示连续值和开关类组件，方便在一页里观察 ProgressBar / Slider / Switch 的变化。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr output = app.Label(40, 414, 1384, 48, "状态读取区。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);

            byte[] font = app.U("Microsoft YaHei UI");

            byte[] cb1Text = app.U("☑️ 启用高级模式");
            IntPtr cb1 = EmojiWindowNative.CreateCheckBox(page, 40, 104, 240, 34, cb1Text, cb1Text.Length, 1, DemoTheme.Text, DemoTheme.Background, font, font.Length, 13, 0, 0, 0);
            byte[] cb2Text = app.U("🧱 卡片样式");
            IntPtr cb2 = EmojiWindowNative.CreateCheckBox(page, 40, 150, 240, 40, cb2Text, cb2Text.Length, 0, DemoTheme.Text, DemoTheme.Background, font, font.Length, 13, 0, 0, 0);
            EmojiWindowNative.SetCheckBoxStyle(cb2, PageCommon.CheckBoxStyleCard);
            EmojiWindowNative.SetCheckBoxCheckColor(cb1, DemoTheme.Primary);
            EmojiWindowNative.SetCheckBoxCheckColor(cb2, DemoTheme.Success);

            byte[] rb1Text = app.U("🅰️ 方案 A");
            byte[] rb2Text = app.U("🅱️ 方案 B");
            byte[] rb3Text = app.U("🅲️ 按钮样式");
            IntPtr rb1 = EmojiWindowNative.CreateRadioButton(page, 340, 104, 130, 34, rb1Text, rb1Text.Length, 99, 1, DemoTheme.Text, DemoTheme.Background, font, font.Length, 13, 0, 0, 0);
            IntPtr rb2 = EmojiWindowNative.CreateRadioButton(page, 480, 104, 130, 34, rb2Text, rb2Text.Length, 99, 0, DemoTheme.Text, DemoTheme.Background, font, font.Length, 13, 0, 0, 0);
            IntPtr rb3 = EmojiWindowNative.CreateRadioButton(page, 340, 150, 150, 36, rb3Text, rb3Text.Length, 99, 0, DemoTheme.Text, DemoTheme.Background, font, font.Length, 13, 0, 0, 0);
            EmojiWindowNative.SetRadioButtonStyle(rb2, PageCommon.RadioStyleBorder);
            EmojiWindowNative.SetRadioButtonStyle(rb3, PageCommon.RadioStyleButton);
            EmojiWindowNative.SetRadioButtonDotColor(rb1, DemoTheme.Primary);
            EmojiWindowNative.SetRadioButtonDotColor(rb2, DemoTheme.Warning);
            EmojiWindowNative.SetRadioButtonDotColor(rb3, DemoTheme.Success);

            IntPtr progress = EmojiWindowNative.CreateProgressBar(page, 758, 104, 420, 28, 35, DemoTheme.Primary, DemoTheme.BorderLight, 1, DemoTheme.Text);
            EmojiWindowNative.SetProgressBarShowText(progress, 1);
            EmojiWindowNative.SetProgressBarTextColor(progress, DemoTheme.Text);

            IntPtr slider = EmojiWindowNative.CreateSlider(page, 758, 160, 260, 40, 0, 100, 36, 10, DemoTheme.Primary, DemoTheme.BorderLight);
            EmojiWindowNative.SetSliderShowStops(slider, 1);

            byte[] onText = app.U("开");
            byte[] offText = app.U("关");
            IntPtr toggle = EmojiWindowNative.CreateSwitch(page, 1048, 156, 88, 34, 1, DemoTheme.Success, DemoTheme.Border, onText, onText.Length, offText, offText.Length);

            app.Button(40, 242, 140, 36, "切换勾选 1", "↺", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetCheckBoxState(cb1, EmojiWindowNative.GetCheckBoxState(cb1) == 0 ? 1 : 0);
                Refresh("程序切换 CheckBox1");
            }, page);
            app.Button(196, 242, 140, 36, "切换勾选 2", "↺", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetCheckBoxState(cb2, EmojiWindowNative.GetCheckBoxState(cb2) == 0 ? 1 : 0);
                Refresh("程序切换 CheckBox2");
            }, page);
            app.Button(758, 242, 120, 36, "进度 -10", "📉", DemoColors.Gray, () =>
            {
                EmojiWindowNative.SetProgressValue(progress, Math.Max(0, EmojiWindowNative.GetProgressValue(progress) - 10));
                Refresh("程序设置 ProgressBar");
            }, page);
            app.Button(894, 242, 120, 36, "进度 +10", "📈", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetProgressValue(progress, Math.Min(100, EmojiWindowNative.GetProgressValue(progress) + 10));
                Refresh("程序设置 ProgressBar");
            }, page);
            app.Button(1030, 242, 120, 36, "Slider=75", "🎚️", DemoColors.Orange, () =>
            {
                EmojiWindowNative.SetSliderValue(slider, 75);
                Refresh("程序设置 Slider=75");
            }, page);
            app.Button(1166, 242, 120, 36, "切换开关", "🔀", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetSwitchState(toggle, EmojiWindowNative.GetSwitchState(toggle) == 0 ? 1 : 0);
                Refresh("程序切换 Switch");
            }, page);

            void Refresh(string prefix)
            {
                string text =
                    $"{prefix}\r\n" +
                    $"CheckBox1={EmojiWindowNative.GetCheckBoxState(cb1)}  CheckBox2={EmojiWindowNative.GetCheckBoxState(cb2)}  " +
                    $"RadioA={EmojiWindowNative.GetRadioButtonState(rb1)}  RadioB={EmojiWindowNative.GetRadioButtonState(rb2)}  RadioC={EmojiWindowNative.GetRadioButtonState(rb3)}\r\n" +
                    $"Progress={EmojiWindowNative.GetProgressValue(progress)}  Slider={EmojiWindowNative.GetSliderValue(slider)}  Switch={EmojiWindowNative.GetSwitchState(toggle)}";
                shell.SetLabelText(output, text);
                shell.SetStatus(prefix);
            }

            var checkCallback = app.Pin(new EmojiWindowNative.CheckBoxCallback((handle, checkedState) =>
            {
                string label = EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetCheckBoxText, handle);
                Refresh($"CheckBox 回调: {label} -> {checkedState}");
            }));
            var radioCallback = app.Pin(new EmojiWindowNative.RadioButtonCallback((handle, groupId, checkedState) =>
            {
                string label = EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetRadioButtonText, handle);
                Refresh($"Radio 回调: {label} group={groupId} checked={checkedState}");
            }));
            var progressCallback = app.Pin(new EmojiWindowNative.ProgressBarCallback((_, value) => Refresh($"Progress 回调: value={value}")));
            var sliderCallback = app.Pin(new EmojiWindowNative.SliderCallback((_, value) => Refresh($"Slider 回调: value={value}")));
            var switchCallback = app.Pin(new EmojiWindowNative.SwitchCallback((_, checkedState) => Refresh($"Switch 回调: checked={checkedState}")));
            EmojiWindowNative.SetCheckBoxCallback(cb1, checkCallback);
            EmojiWindowNative.SetCheckBoxCallback(cb2, checkCallback);
            EmojiWindowNative.SetRadioButtonCallback(rb1, radioCallback);
            EmojiWindowNative.SetRadioButtonCallback(rb2, radioCallback);
            EmojiWindowNative.SetRadioButtonCallback(rb3, radioCallback);
            EmojiWindowNative.SetProgressBarCallback(progress, progressCallback);
            EmojiWindowNative.SetSliderCallback(slider, sliderCallback);
            EmojiWindowNative.SetSwitchCallback(toggle, switchCallback);

            app.Label(40, 556, 1360, 24, "1. 这一页把二值组件和连续值组件放到同一页联调，方便验证多个 callback 是否都能稳定回写。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 590, 1360, 24, "2. CheckBox / RadioButton 使用不同样式与语义色，避免状态页沦为一堆控件的平铺。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 624, 1360, 24, "3. ProgressBar / Slider / Switch 负责展示连续值、步进值和布尔开关三类不同状态模型。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 658, 1360, 24, "4. 下方读数区统一承接程序设置与用户回调，不再让状态页面只有零散按钮。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            void ApplyTheme()
            {
                EmojiWindowNative.SetCheckBoxColor(cb1, DemoTheme.Text, DemoTheme.Background);
                EmojiWindowNative.SetCheckBoxColor(cb2, DemoTheme.Text, DemoTheme.Background);
                EmojiWindowNative.SetRadioButtonColor(rb1, DemoTheme.Text, DemoTheme.Background);
                EmojiWindowNative.SetRadioButtonColor(rb2, DemoTheme.Text, DemoTheme.Background);
                EmojiWindowNative.SetRadioButtonColor(rb3, DemoTheme.Text, DemoTheme.Background);
                shell.SetLabelText(leftIntro, shell.Palette.Dark
                    ? "深色主题下左侧仍保持布尔选择类组件的分层，而不是直接堆控件。"
                    : "浅色主题下左侧保持 CheckBox / RadioButton 的舞台区分层，更接近 Python 版阅读顺序。");
                shell.SetLabelText(rightIntro, shell.Palette.Dark
                    ? "深色主题下右侧继续把连续值和开关类组件集中成一个舞台区。"
                    : "浅色主题下右侧集中展示 ProgressBar / Slider / Switch，更适合做联合状态验证。");
                Refresh("状态联调页已整理：选择类与连续值类组件分区展示。");
            }

            shell.RegisterPageThemeHandler(page, ApplyTheme);
            ApplyTheme();
        }
    }
}
