using System;

namespace EmojiWindowDemo
{
    internal static class CheckBoxDemoPage
    {
        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;
            byte[] font = app.U("Microsoft YaHei UI");

            app.GroupBox(16, 16, 980, 324, "CheckBox 样式展示", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(1020, 16, 444, 424, "状态 / 样式 / 颜色", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(16, 538, 1448, 220, "CheckBox API 说明", DemoTheme.Border, DemoTheme.Background, page);

            app.Label(40, 56, 940, 24, "这一页只保留 CheckBox，不再混入 RadioButton / Slider / Switch，页面层次和 Python v2 保持一致。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);

            byte[] defaultText = app.U("默认勾选");
            byte[] fillText = app.U("Fill 样式");
            byte[] disabledText = app.U("禁用态展示");
            byte[] cardText = app.U("Card 样式");
            byte[] buttonText = app.U("Button 样式");
            byte[] dynamicText = app.U("动态样式");

            IntPtr cbDefault = EmojiWindowNative.CreateCheckBox(page, 56, 118, 250, 34, defaultText, defaultText.Length, 1, DemoTheme.Text, DemoTheme.Background, font, font.Length, 13, 0, 0, 0);
            IntPtr cbFill = EmojiWindowNative.CreateCheckBox(page, 56, 166, 250, 36, fillText, fillText.Length, 0, DemoTheme.Text, DemoTheme.Background, font, font.Length, 13, 0, 0, 0);
            IntPtr cbDisabled = EmojiWindowNative.CreateCheckBox(page, 56, 214, 250, 34, disabledText, disabledText.Length, 1, DemoTheme.Text, DemoTheme.Background, font, font.Length, 13, 0, 0, 0);
            IntPtr cbCard = EmojiWindowNative.CreateCheckBox(page, 360, 114, 260, 42, cardText, cardText.Length, 0, DemoTheme.Text, DemoTheme.Surface, font, font.Length, 13, 0, 0, 0);
            IntPtr cbButton = EmojiWindowNative.CreateCheckBox(page, 360, 168, 260, 40, buttonText, buttonText.Length, 1, DemoTheme.Text, DemoTheme.Surface, font, font.Length, 13, 0, 0, 0);
            IntPtr cbDynamic = EmojiWindowNative.CreateCheckBox(page, 360, 222, 260, 40, dynamicText, dynamicText.Length, 1, DemoTheme.Text, DemoTheme.Background, font, font.Length, 13, 0, 0, 0);

            EmojiWindowNative.SetCheckBoxStyle(cbFill, 1);
            EmojiWindowNative.SetCheckBoxStyle(cbCard, PageCommon.CheckBoxStyleCard);
            EmojiWindowNative.SetCheckBoxStyle(cbButton, PageCommon.CheckBoxStyleButton);
            EmojiWindowNative.SetCheckBoxCheckColor(cbDefault, DemoTheme.Primary);
            EmojiWindowNative.SetCheckBoxCheckColor(cbFill, DemoTheme.Warning);
            EmojiWindowNative.SetCheckBoxCheckColor(cbCard, DemoTheme.Success);
            EmojiWindowNative.SetCheckBoxCheckColor(cbButton, DemoTheme.Primary);
            EmojiWindowNative.SetCheckBoxCheckColor(cbDynamic, DemoColors.Purple);
            EmojiWindowNative.EnableCheckBox(cbDisabled, 0);

            IntPtr readout = app.Label(40, 366, 920, 108, "等待读取复选框属性。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr state = app.Label(40, 490, 920, 22, "复选框页面状态会显示在这里。", DemoTheme.Primary, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            IntPtr[] boxes = { cbDefault, cbFill, cbDisabled, cbCard, cbButton, cbDynamic };
            string[] names = { "default", "fill", "disabled", "card", "button", "dynamic" };
            int cardX = 360;
            bool dynamicAltText = false;

            string StyleName(int style)
            {
                switch (style)
                {
                    case 0: return "default";
                    case 1: return "fill";
                    case PageCommon.CheckBoxStyleButton: return "button";
                    case PageCommon.CheckBoxStyleCard: return "card";
                    default: return "unknown(" + style + ")";
                }
            }

            void ApplyTheme()
            {
                EmojiWindowNative.SetCheckBoxColor(cbDefault, DemoTheme.Text, DemoTheme.Background);
                EmojiWindowNative.SetCheckBoxColor(cbFill, DemoTheme.Text, DemoTheme.Background);
                EmojiWindowNative.SetCheckBoxColor(cbDisabled, DemoTheme.Text, DemoTheme.Background);
                EmojiWindowNative.SetCheckBoxColor(cbCard, DemoTheme.Text, DemoTheme.Surface);
                EmojiWindowNative.SetCheckBoxColor(cbButton, DemoTheme.Text, DemoTheme.Surface);
                EmojiWindowNative.SetCheckBoxColor(cbDynamic, DemoTheme.Text, DemoTheme.Background);
            }

            void Refresh(string note)
            {
                string text = note + "\r\n";
                for (int i = 0; i < boxes.Length; i++)
                {
                    EmojiWindowNative.GetCheckBoxColor(boxes[i], out uint fg, out uint bg);
                    EmojiWindowNative.GetCheckBoxCheckColor(boxes[i], out uint checkColor);
                    string visible = Win32Native.IsWindowVisible(boxes[i]) ? "显示" : "隐藏";
                    string enabled = Win32Native.IsWindowEnabled(boxes[i]) ? "启用" : "禁用";
                    text += $"{names[i]}: checked={EmojiWindowNative.GetCheckBoxState(boxes[i])} style={StyleName(EmojiWindowNative.GetCheckBoxStyle(boxes[i]))} {visible}/{enabled} text={EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetCheckBoxText, boxes[i])} fg={PageCommon.FormatColor(fg)} bg={PageCommon.FormatColor(bg)} check={PageCommon.FormatColor(checkColor)}";
                    if (i < boxes.Length - 1)
                    {
                        text += "\r\n";
                    }
                }

                shell.SetLabelText(readout, text);
                shell.SetLabelText(state, note);
                shell.SetStatus(note);
            }

            void Toggle(IntPtr box, string note)
            {
                EmojiWindowNative.SetCheckBoxState(box, EmojiWindowNative.GetCheckBoxState(box) == 0 ? 1 : 0);
                Refresh(note);
            }

            void SetScheme(uint a, uint b, uint c, uint d, uint e, string note)
            {
                EmojiWindowNative.SetCheckBoxCheckColor(cbDefault, a);
                EmojiWindowNative.SetCheckBoxCheckColor(cbFill, b);
                EmojiWindowNative.SetCheckBoxCheckColor(cbCard, c);
                EmojiWindowNative.SetCheckBoxCheckColor(cbButton, d);
                EmojiWindowNative.SetCheckBoxCheckColor(cbDynamic, e);
                Refresh(note);
            }

            void Restore()
            {
                EmojiWindowNative.SetCheckBoxText(cbDefault, defaultText, defaultText.Length);
                EmojiWindowNative.SetCheckBoxText(cbFill, fillText, fillText.Length);
                EmojiWindowNative.SetCheckBoxText(cbDisabled, disabledText, disabledText.Length);
                EmojiWindowNative.SetCheckBoxText(cbCard, cardText, cardText.Length);
                EmojiWindowNative.SetCheckBoxText(cbButton, buttonText, buttonText.Length);
                EmojiWindowNative.SetCheckBoxText(cbDynamic, dynamicText, dynamicText.Length);
                EmojiWindowNative.SetCheckBoxState(cbDefault, 1);
                EmojiWindowNative.SetCheckBoxState(cbFill, 0);
                EmojiWindowNative.SetCheckBoxState(cbDisabled, 1);
                EmojiWindowNative.SetCheckBoxState(cbCard, 0);
                EmojiWindowNative.SetCheckBoxState(cbButton, 1);
                EmojiWindowNative.SetCheckBoxState(cbDynamic, 1);
                EmojiWindowNative.SetCheckBoxStyle(cbFill, 1);
                EmojiWindowNative.SetCheckBoxStyle(cbCard, PageCommon.CheckBoxStyleCard);
                EmojiWindowNative.SetCheckBoxStyle(cbButton, PageCommon.CheckBoxStyleButton);
                EmojiWindowNative.SetCheckBoxStyle(cbDynamic, 0);
                EmojiWindowNative.EnableCheckBox(cbDisabled, 0);
                EmojiWindowNative.ShowCheckBox(cbCard, 1);
                cardX = 360;
                EmojiWindowNative.SetCheckBoxBounds(cbCard, cardX, 114, 260, 42);
                dynamicAltText = false;
                ApplyTheme();
                SetScheme(DemoTheme.Primary, DemoTheme.Warning, DemoTheme.Success, DemoTheme.Primary, DemoColors.Purple, "复选框页面已恢复默认");
            }

            var callback = app.Pin(new EmojiWindowNative.CheckBoxCallback((handle, checkedState) =>
            {
                string label = EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetCheckBoxText, handle);
                Refresh($"CheckBox 回调: {label} -> {checkedState}");
            }));
            foreach (IntPtr box in boxes)
            {
                EmojiWindowNative.SetCheckBoxCallback(box, callback);
            }

            app.Label(1044, 56, 220, 22, "状态动作", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Button(1044, 94, 116, 34, "读取状态", "i", DemoColors.Blue, () => Refresh("已读取全部 CheckBox 状态"), page);
            app.Button(1172, 94, 116, 34, "切换默认", "D", DemoColors.Green, () => Toggle(cbDefault, "默认复选框状态已切换"), page);
            app.Button(1300, 94, 124, 34, "切换 Fill", "F", DemoColors.Orange, () => Toggle(cbFill, "Fill 复选框状态已切换"), page);

            app.Label(1044, 148, 220, 22, "样式与文案", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Button(1044, 182, 116, 34, "动态-Card", "C", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetCheckBoxStyle(cbDynamic, PageCommon.CheckBoxStyleCard);
                Refresh("动态复选框已切到 card");
            }, page);
            app.Button(1172, 182, 116, 34, "动态-Button", "B", DemoColors.Purple, () =>
            {
                EmojiWindowNative.SetCheckBoxStyle(cbDynamic, PageCommon.CheckBoxStyleButton);
                Refresh("动态复选框已切到 button");
            }, page);
            app.Button(1300, 182, 124, 34, "切换文案", "T", DemoColors.Gray, () =>
            {
                dynamicAltText = !dynamicAltText;
                byte[] text = app.U(dynamicAltText ? "动态样式 / 文本已切换" : "动态样式");
                EmojiWindowNative.SetCheckBoxText(cbDynamic, text, text.Length);
                Refresh("动态复选框文本已切换");
            }, page);

            app.Label(1044, 236, 220, 22, "颜色与位置", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Button(1044, 270, 116, 34, "蓝色方案", "B", DemoColors.Blue, () => SetScheme(DemoTheme.Primary, DemoTheme.Primary, DemoTheme.Primary, DemoTheme.Primary, DemoTheme.Primary, "复选框勾选色已统一切到蓝色方案"), page);
            app.Button(1172, 270, 116, 34, "暖色方案", "W", DemoColors.Orange, () => SetScheme(DemoTheme.Warning, DemoTheme.Warning, DemoTheme.Warning, DemoTheme.Warning, DemoTheme.Warning, "复选框勾选色已统一切到暖色方案"), page);
            app.Button(1300, 270, 124, 34, "Card 右移", ">", DemoColors.Green, () =>
            {
                cardX += 48;
                EmojiWindowNative.SetCheckBoxBounds(cbCard, cardX, 114, 260, 42);
                Refresh("Card 样式复选框已向右移动 48");
            }, page);

            app.Label(1044, 324, 220, 22, "显示与启用", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Button(1044, 358, 116, 34, "禁用态切换", "E", DemoColors.Gray, () =>
            {
                EmojiWindowNative.EnableCheckBox(cbDisabled, Win32Native.IsWindowEnabled(cbDisabled) ? 0 : 1);
                Refresh("禁用态复选框已切换启用状态");
            }, page);
            app.Button(1172, 358, 116, 34, "Card 显隐", "V", DemoColors.Green, () =>
            {
                EmojiWindowNative.ShowCheckBox(cbCard, Win32Native.IsWindowVisible(cbCard) ? 0 : 1);
                Refresh("Card 样式复选框已切换显示状态");
            }, page);
            app.Button(1300, 358, 124, 34, "恢复默认", "R", DemoColors.Blue, Restore, page);

            app.Label(40, 582, 1280, 24, "1. GetCheckBoxState / SetCheckBoxState / SetCheckBoxCallback：读取、写入并监听勾选状态。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 616, 1280, 24, "2. GetCheckBoxStyle / SetCheckBoxStyle：直接切换 default / fill / card / button。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 650, 1280, 24, "3. GetCheckBoxColor / SetCheckBoxColor / SetCheckBoxCheckColor：读取文本色、背景色和勾选色。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 684, 1280, 24, "4. SetCheckBoxText / GetCheckBoxText：动态切换复选框文案。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 718, 1280, 24, "5. EnableCheckBox / ShowCheckBox / SetCheckBoxBounds：演示启用态、显示态和位置更新。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            shell.RegisterPageThemeHandler(page, ApplyTheme);
            ApplyTheme();
            Refresh("CheckBox 页面已重排，可直接测试样式、状态、颜色和文本。");
        }
    }
}
