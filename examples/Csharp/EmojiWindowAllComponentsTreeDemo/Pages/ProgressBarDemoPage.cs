using System;

namespace EmojiWindowDemo
{
    internal static class ProgressBarDemoPage
    {
        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;

            app.GroupBox(16, 16, 980, 324, "📊 ProgressBar 样式演示", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(1020, 16, 444, 324, "🧪 数值 / 文本 / 动画", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(16, 538, 1448, 220, "📘 ProgressBar API 说明", DemoTheme.Border, DemoTheme.Background, page);

            app.Label(40, 56, 960, 24, "这一页只保留 ProgressBar，不再混入 CheckBox / RadioButton / Slider / Switch。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);

            IntPtr progressMain = EmojiWindowNative.CreateProgressBar(page, 56, 122, 560, 28, 35, DemoTheme.Primary, DemoTheme.BorderLight, 1, DemoTheme.Text);
            IntPtr progressSuccess = EmojiWindowNative.CreateProgressBar(page, 56, 176, 560, 24, 62, DemoTheme.Success, DemoTheme.Surface, 1, DemoTheme.Text);
            IntPtr progressWarning = EmojiWindowNative.CreateProgressBar(page, 56, 226, 560, 20, 78, DemoTheme.Warning, DemoTheme.SurfaceWarning, 0, DemoTheme.Text);
            IntPtr progressInd = EmojiWindowNative.CreateProgressBar(page, 56, 270, 560, 18, 50, DemoTheme.Info, DemoTheme.SurfaceInfo, 0, DemoTheme.Text);
            EmojiWindowNative.SetProgressIndeterminate(progressInd, 1);

            IntPtr readout = app.Label(40, 366, 1384, 108, "等待读取进度条属性。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr stateLabel = app.Label(40, 490, 1360, 22, "进度条页状态将在这里更新。", DemoTheme.Primary, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            bool mainShowText = true;
            bool warningShowText = false;
            bool indeterminate = true;

            void Refresh(string note)
            {
                shell.SetLabelText(
                    readout,
                    $"main={EmojiWindowNative.GetProgressValue(progressMain)} show_text={mainShowText}\r\n" +
                    $"success={EmojiWindowNative.GetProgressValue(progressSuccess)}  warning={EmojiWindowNative.GetProgressValue(progressWarning)} show_text={warningShowText}\r\n" +
                    $"indeterminate={indeterminate}  ind_value={EmojiWindowNative.GetProgressValue(progressInd)}\r\n" +
                    note);
                shell.SetLabelText(stateLabel, note);
                shell.SetStatus(note);
            }

            var callback = app.Pin(new EmojiWindowNative.ProgressBarCallback((_, value) => Refresh("Progress 回调: value=" + value)));
            EmojiWindowNative.SetProgressBarCallback(progressMain, callback);

            app.Button(1044, 94, 116, 34, "主条=0", "0", DemoColors.Gray, () =>
            {
                EmojiWindowNative.SetProgressValue(progressMain, 0);
                Refresh("主进度条已设为 0");
            }, page);
            app.Button(1172, 94, 116, 34, "主条=35", "35", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetProgressValue(progressMain, 35);
                Refresh("主进度条已设为 35");
            }, page);
            app.Button(1300, 94, 124, 34, "主条=80", "80", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetProgressValue(progressMain, 80);
                Refresh("主进度条已设为 80");
            }, page);

            app.Button(1044, 138, 116, 34, "成功=62", "✅", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetProgressValue(progressSuccess, 62);
                Refresh("成功进度条已设为 62");
            }, page);
            app.Button(1172, 138, 116, 34, "警告=78", "⚠", DemoColors.Orange, () =>
            {
                EmojiWindowNative.SetProgressValue(progressWarning, 78);
                Refresh("警告进度条已设为 78");
            }, page);
            app.Button(1300, 138, 124, 34, "动画切换", "↔", DemoColors.Purple, () =>
            {
                indeterminate = !indeterminate;
                EmojiWindowNative.SetProgressIndeterminate(progressInd, indeterminate ? 1 : 0);
                Refresh(indeterminate ? "不确定进度条已开启动画" : "不确定进度条已关闭动画");
            }, page);

            app.Button(1044, 182, 116, 34, "主条文本", "T", DemoColors.Blue, () =>
            {
                mainShowText = !mainShowText;
                EmojiWindowNative.SetProgressBarShowText(progressMain, mainShowText ? 1 : 0);
                Refresh(mainShowText ? "主进度条文本已显示" : "主进度条文本已隐藏");
            }, page);
            app.Button(1172, 182, 116, 34, "警告文本", "T", DemoColors.Orange, () =>
            {
                warningShowText = !warningShowText;
                EmojiWindowNative.SetProgressBarShowText(progressWarning, warningShowText ? 1 : 0);
                Refresh(warningShowText ? "警告进度条文本已显示" : "警告进度条文本已隐藏");
            }, page);
            app.Button(1300, 182, 124, 34, "重刷主题", "🎨", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetProgressBarTextColor(progressMain, shell.Palette.Text);
                EmojiWindowNative.SetProgressBarTextColor(progressSuccess, shell.Palette.Text);
                EmojiWindowNative.SetProgressBarTextColor(progressWarning, shell.Palette.Text);
                EmojiWindowNative.SetProgressBarTextColor(progressInd, shell.Palette.Text);
                Refresh("进度条文字颜色已按主题刷新");
            }, page);

            app.Button(1044, 226, 116, 34, "主条-10", "−", DemoColors.Gray, () =>
            {
                EmojiWindowNative.SetProgressValue(progressMain, Math.Max(0, EmojiWindowNative.GetProgressValue(progressMain) - 10));
                Refresh("主进度条已减少 10");
            }, page);
            app.Button(1172, 226, 116, 34, "主条+10", "+", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetProgressValue(progressMain, Math.Min(100, EmojiWindowNative.GetProgressValue(progressMain) + 10));
                Refresh("主进度条已增加 10");
            }, page);
            app.Button(1300, 226, 124, 34, "恢复默认", "↩", DemoColors.Green, () =>
            {
                mainShowText = true;
                warningShowText = false;
                indeterminate = true;
                EmojiWindowNative.SetProgressValue(progressMain, 35);
                EmojiWindowNative.SetProgressValue(progressSuccess, 62);
                EmojiWindowNative.SetProgressValue(progressWarning, 78);
                EmojiWindowNative.SetProgressValue(progressInd, 50);
                EmojiWindowNative.SetProgressBarShowText(progressMain, 1);
                EmojiWindowNative.SetProgressBarShowText(progressWarning, 0);
                EmojiWindowNative.SetProgressIndeterminate(progressInd, 1);
                EmojiWindowNative.SetProgressBarTextColor(progressMain, shell.Palette.Text);
                EmojiWindowNative.SetProgressBarTextColor(progressSuccess, shell.Palette.Text);
                EmojiWindowNative.SetProgressBarTextColor(progressWarning, shell.Palette.Text);
                EmojiWindowNative.SetProgressBarTextColor(progressInd, shell.Palette.Text);
                Refresh("ProgressBar 页已恢复默认状态");
            }, page);

            app.Label(40, 582, 760, 24, "1. GetProgressValue / SetProgressValue / SetProgressBarCallback：读取、写入进度值并监听变化。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 616, 760, 24, "2. SetProgressIndeterminate：切换不确定模式。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 650, 980, 24, "3. SetProgressBarShowText / SetProgressBarTextColor：切换文本显示和文字颜色。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            void ApplyTheme()
            {
                EmojiWindowNative.SetProgressBarTextColor(progressMain, shell.Palette.Text);
                EmojiWindowNative.SetProgressBarTextColor(progressSuccess, shell.Palette.Text);
                EmojiWindowNative.SetProgressBarTextColor(progressWarning, shell.Palette.Text);
                EmojiWindowNative.SetProgressBarTextColor(progressInd, shell.Palette.Text);
            }

            shell.RegisterPageThemeHandler(page, ApplyTheme);
            ApplyTheme();
            Refresh("ProgressBar 页面已重排，可直接测试数值、文本和动画。");
        }
    }
}
