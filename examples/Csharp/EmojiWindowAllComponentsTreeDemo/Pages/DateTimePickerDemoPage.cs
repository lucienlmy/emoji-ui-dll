using System;

namespace EmojiWindowDemo
{
    internal static class DateTimePickerDemoPage
    {
        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;
            byte[] font = app.U("Microsoft YaHei UI");

            IntPtr runtimeBox = app.GroupBox(16, 16, 980, 248, "📮 D2DDateTimePicker 实时属性读取", DemoTheme.Border, DemoTheme.Background, page);
            IntPtr actionBox = app.GroupBox(16, 286, 980, 254, "🛠️ 时间值 / 精度 / 颜色 / 布局", DemoTheme.Border, DemoTheme.Background, page);
            IntPtr stateBox = app.GroupBox(1020, 212, 444, 328, "🗂️ 日期时间状态开关", DemoTheme.Border, DemoTheme.Background, page);
            IntPtr apiBox = app.GroupBox(16, 558, 1448, 230, "📘 D2DDateTimePicker API 说明", DemoTheme.Border, DemoTheme.Background, page);

            IntPtr intro = app.Label(40, 56, 900, 24, "这一页直接读取日期时间值、精度、颜色、位置尺寸、可见态和启用态，不再只是放一个输入控件。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr picker = EmojiWindowNative.CreateD2DDateTimePicker(page, 56, 120, 340, 38, PageCommon.DtpYmdHm, shell.Palette.Text, shell.Palette.PageBackground, app.ThemeColor("border_light"), font, font.Length, 13, 0, 0, 0);
            EmojiWindowNative.SetD2DDateTimePickerDateTime(picker, 2026, 3, 30, 14, 30, 0);

            IntPtr readout = app.Label(40, 184, 920, 56, string.Empty, DemoTheme.Text, DemoTheme.Background, 13, PageCommon.AlignLeft, true, page);
            IntPtr stateLabel = app.Label(40, 760, 1360, 22, "日期时间页状态将在这里更新。", DemoTheme.Primary, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            IntPtr sideNote = app.Label(1044, 344, 382, 56, "这里保留绝对时间值，不用“今天/明天”这类相对词，方便做精确回归。默认值为 2026-03-30 14:30:00。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);

            IntPtr api1 = app.Label(40, 598, 900, 24, "1. GetD2DDateTimePickerDateTime / SetD2DDateTimePickerDateTime：读写具体时间。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            IntPtr api2 = app.Label(40, 632, 980, 24, "2. GetD2DDateTimePickerPrecision / SetD2DDateTimePickerPrecision：切换显示精度。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            IntPtr api3 = app.Label(40, 666, 980, 24, "3. GetD2DDateTimePickerColors / SetD2DDateTimePickerColors：切换颜色方案。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            IntPtr api4 = app.Label(40, 700, 1080, 24, "4. SetD2DDateTimePickerBounds / EnableD2DDateTimePicker / ShowD2DDateTimePicker：切换布局与状态。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            IntPtr api5 = app.Label(40, 734, 900, 24, "5. 这一页用绝对日期做演示，避免相对时间导致的测试歧义。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            app.AttachToGroup(runtimeBox, intro);
            app.AttachToGroup(stateBox, sideNote);
            app.AttachToGroup(apiBox, api1, api2, api3, api4, api5);

            int x = 56;
            int y = 120;
            int width = 340;
            int height = 38;
            bool visible = true;
            bool enabled = true;
            string colorScheme = "theme";

            void ApplyPickerColors()
            {
                if (colorScheme == "cool")
                {
                    EmojiWindowNative.SetD2DDateTimePickerColors(picker, DemoColors.Blue, DemoColors.LightBlue, DemoColors.Blue);
                    return;
                }

                if (colorScheme == "warm")
                {
                    EmojiWindowNative.SetD2DDateTimePickerColors(picker, DemoColors.Orange, DemoColors.Yellow, DemoColors.Orange);
                    return;
                }

                EmojiWindowNative.SetD2DDateTimePickerColors(picker, shell.Palette.Text, shell.Palette.PageBackground, app.ThemeColor("border_light"));
            }

            void Refresh(string note)
            {
                EmojiWindowNative.GetD2DDateTimePickerDateTime(picker, out int year, out int month, out int day, out int hour, out int minute, out int second);
                EmojiWindowNative.GetD2DDateTimePickerColors(picker, out uint fg, out uint bg, out uint border);
                int precision = EmojiWindowNative.GetD2DDateTimePickerPrecision(picker);
                shell.SetLabelText(
                    readout,
                    $"datetime={PageCommon.FormatDateTime(year, month, day, hour, minute, second)}  precision={precision}  {(visible ? "显示" : "隐藏")}/{(enabled ? "启用" : "禁用")}\r\n" +
                    $"bounds=({x}, {y}, {width}, {height})\r\n" +
                    $"fg={PageCommon.FormatColor(fg)}  bg={PageCommon.FormatColor(bg)}  border={PageCommon.FormatColor(border)}");
                shell.SetLabelText(stateLabel, note);
                shell.SetStatus(note);
            }

            var callback = app.Pin(new EmojiWindowNative.ValueChangedCallback(_ => Refresh("日期时间选择器值已变化")));
            EmojiWindowNative.SetD2DDateTimePickerCallback(picker, callback);

            app.Button(40, 360, 156, 36, "设为 2026-03-30", "📮", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetD2DDateTimePickerDateTime(picker, 2026, 3, 30, 14, 30, 0);
                Refresh("日期时间已设为 2026-03-30 14:30:00");
            }, page);
            app.Button(212, 360, 156, 36, "设为 2027-01-01", "🗓️", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetD2DDateTimePickerDateTime(picker, 2027, 1, 1, 9, 0, 0);
                Refresh("日期时间已设为 2027-01-01 09:00:00");
            }, page);
            app.Button(384, 360, 156, 36, "精度 YMD", "🕓", DemoColors.Purple, () =>
            {
                EmojiWindowNative.SetD2DDateTimePickerPrecision(picker, PageCommon.DtpYmd);
                Refresh("日期时间精度已切到 YMD");
            }, page);
            app.Button(556, 360, 156, 36, "精度 YMDHM", "🕘", DemoColors.Orange, () =>
            {
                EmojiWindowNative.SetD2DDateTimePickerPrecision(picker, PageCommon.DtpYmdHm);
                Refresh("日期时间精度已切到 YMDHM");
            }, page);
            app.Button(728, 360, 156, 36, "精度 YMDHMS", "🕛", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetD2DDateTimePickerPrecision(picker, PageCommon.DtpYmdHms);
                Refresh("日期时间精度已切到 YMDHMS");
            }, page);

            app.Button(40, 448, 118, 36, "冷色", "💙", DemoColors.Blue, () =>
            {
                colorScheme = "cool";
                ApplyPickerColors();
                Refresh("日期时间选择框已切到冷色方案");
            }, page);
            app.Button(172, 448, 118, 36, "暖色", "🟠", DemoColors.Orange, () =>
            {
                colorScheme = "warm";
                ApplyPickerColors();
                Refresh("日期时间选择框已切到暖色方案");
            }, page);
            app.Button(304, 448, 118, 36, "右移 80", "➡️", DemoColors.Green, () =>
            {
                x = 136;
                EmojiWindowNative.SetD2DDateTimePickerBounds(picker, x, y, width, height);
                Refresh("日期时间选择框已右移 80");
            }, page);
            app.Button(436, 448, 118, 36, "加宽 100", "↔️", DemoColors.Purple, () =>
            {
                width = 440;
                EmojiWindowNative.SetD2DDateTimePickerBounds(picker, x, y, width, height);
                Refresh("日期时间选择框已加宽到 440");
            }, page);

            app.Button(1044, 286, 118, 36, "禁用/启用", "🚫", DemoColors.Blue, () =>
            {
                enabled = !enabled;
                EmojiWindowNative.EnableD2DDateTimePicker(picker, enabled ? 1 : 0);
                Refresh("日期时间选择框启用状态已切换");
            }, page);
            app.Button(1176, 286, 118, 36, "显示/隐藏", "👁️", DemoColors.Gray, () =>
            {
                visible = !visible;
                EmojiWindowNative.ShowD2DDateTimePicker(picker, visible ? 1 : 0);
                Refresh("日期时间选择框可见状态已切换");
            }, page);
            app.Button(1308, 286, 118, 36, "恢复主题", "↩", DemoColors.Green, () =>
            {
                x = 56;
                y = 120;
                width = 340;
                height = 38;
                visible = true;
                enabled = true;
                colorScheme = "theme";
                EmojiWindowNative.SetD2DDateTimePickerBounds(picker, x, y, width, height);
                EmojiWindowNative.SetD2DDateTimePickerPrecision(picker, PageCommon.DtpYmdHm);
                EmojiWindowNative.SetD2DDateTimePickerDateTime(picker, 2026, 3, 30, 14, 30, 0);
                EmojiWindowNative.EnableD2DDateTimePicker(picker, 1);
                EmojiWindowNative.ShowD2DDateTimePicker(picker, 1);
                ApplyPickerColors();
                Refresh("日期时间页已恢复主题默认状态");
            }, page);

            void ApplyTheme()
            {
                if (colorScheme == "theme")
                {
                    ApplyPickerColors();
                }
            }

            shell.RegisterPageThemeHandler(page, ApplyTheme);
            ApplyTheme();
            Refresh("日期时间页已加载，可直接测试日期时间属性读取与设置");
        }
    }
}
