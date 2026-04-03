using System;

namespace EmojiWindowDemo
{
    internal static class SliderDemoPage
    {
        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;

            app.GroupBox(16, 16, 980, 324, "🎚️ Slider 样式演示", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(1020, 16, 444, 324, "🧪 数值 / 配色 / 停靠点", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(16, 538, 1448, 220, "📘 Slider API 说明", DemoTheme.Border, DemoTheme.Background, page);

            app.Label(40, 56, 960, 24, "这一页只保留 Slider，本轮重点统一布局层次，不再让滑块和说明散在页面上。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);

            app.Label(56, 108, 120, 20, "主滑块", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            IntPtr sliderMain = EmojiWindowNative.CreateSlider(page, 56, 128, 560, 40, 0, 100, 35, 5, DemoTheme.Primary, DemoTheme.SurfacePrimary);
            EmojiWindowNative.SetSliderShowStops(sliderMain, 1);
            EmojiWindowNative.SetSliderColors(sliderMain, DemoTheme.Primary, DemoTheme.SurfacePrimary, DemoTheme.Warning);

            app.Label(56, 196, 120, 20, "细步长", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            IntPtr sliderFine = EmojiWindowNative.CreateSlider(page, 56, 216, 560, 40, 0, 100, 24, 1, DemoTheme.Success, DemoTheme.SurfaceSuccess);
            EmojiWindowNative.SetSliderShowStops(sliderFine, 0);
            EmojiWindowNative.SetSliderColors(sliderFine, DemoTheme.Success, DemoTheme.SurfaceSuccess, DemoTheme.Success);

            app.Label(56, 272, 120, 20, "大范围", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            IntPtr sliderWide = EmojiWindowNative.CreateSlider(page, 56, 292, 560, 40, 0, 200, 120, 20, DemoTheme.Warning, DemoTheme.SurfaceWarning);
            EmojiWindowNative.SetSliderShowStops(sliderWide, 1);
            EmojiWindowNative.SetSliderColors(sliderWide, DemoTheme.Warning, DemoTheme.SurfaceWarning, DemoTheme.Warning);

            IntPtr readout = app.Label(40, 366, 1384, 108, "等待读取滑块状态。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr stateLabel = app.Label(40, 490, 1360, 22, "滑块页状态会显示在这里。", DemoTheme.Primary, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            bool mainShowStops = true;

            void Refresh(string note)
            {
                shell.SetLabelText(
                    readout,
                    $"main={EmojiWindowNative.GetSliderValue(sliderMain)} range=0..100 step=5 showStops={mainShowStops}\r\n" +
                    $"fine={EmojiWindowNative.GetSliderValue(sliderFine)} range=0..100 step=1\r\n" +
                    $"wide={EmojiWindowNative.GetSliderValue(sliderWide)} range=0..200 step=20\r\n" +
                    note);
                shell.SetLabelText(stateLabel, note);
                shell.SetStatus(note);
            }

            var callback = app.Pin(new EmojiWindowNative.SliderCallback((_, value) => Refresh("Slider 回调: value=" + value)));
            EmojiWindowNative.SetSliderCallback(sliderMain, callback);
            EmojiWindowNative.SetSliderCallback(sliderFine, callback);
            EmojiWindowNative.SetSliderCallback(sliderWide, callback);

            app.Button(1044, 94, 116, 34, "主条=0", "0", DemoColors.Gray, () =>
            {
                EmojiWindowNative.SetSliderValue(sliderMain, 0);
                Refresh("主滑块已设为 0");
            }, page);
            app.Button(1172, 94, 116, 34, "主条=36", "36", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetSliderValue(sliderMain, 36);
                Refresh("主滑块已设为 36");
            }, page);
            app.Button(1300, 94, 124, 34, "主条=75", "75", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetSliderValue(sliderMain, 75);
                Refresh("主滑块已设为 75");
            }, page);

            app.Button(1044, 138, 116, 34, "大范围120", "120", DemoColors.Orange, () =>
            {
                EmojiWindowNative.SetSliderValue(sliderWide, 120);
                Refresh("大范围滑块已设为 120");
            }, page);
            app.Button(1172, 138, 116, 34, "大范围150", "150", DemoColors.Purple, () =>
            {
                EmojiWindowNative.SetSliderValue(sliderWide, 150);
                Refresh("大范围滑块已设为 150");
            }, page);
            app.Button(1300, 138, 124, 34, "停靠点开关", "⋯", DemoColors.Blue, () =>
            {
                mainShowStops = !mainShowStops;
                EmojiWindowNative.SetSliderShowStops(sliderMain, mainShowStops ? 1 : 0);
                Refresh(mainShowStops ? "主滑块已开启停靠点" : "主滑块已关闭停靠点");
            }, page);

            app.Button(1044, 182, 116, 34, "蓝色方案", "🩵", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetSliderColors(sliderMain, DemoTheme.Primary, DemoTheme.SurfacePrimary, DemoTheme.Primary);
                EmojiWindowNative.SetSliderColors(sliderFine, DemoTheme.Success, DemoTheme.SurfaceSuccess, DemoTheme.Success);
                EmojiWindowNative.SetSliderColors(sliderWide, DemoTheme.Info, DemoTheme.SurfaceInfo, DemoTheme.Info);
                Refresh("滑块已切到冷色方案");
            }, page);
            app.Button(1172, 182, 116, 34, "暖色方案", "🟠", DemoColors.Orange, () =>
            {
                EmojiWindowNative.SetSliderColors(sliderMain, DemoTheme.Warning, DemoTheme.SurfaceWarning, DemoTheme.Warning);
                EmojiWindowNative.SetSliderColors(sliderFine, DemoTheme.Danger, DemoTheme.SurfaceDanger, DemoTheme.Danger);
                EmojiWindowNative.SetSliderColors(sliderWide, DemoTheme.Warning, DemoTheme.SurfaceDanger, DemoTheme.Danger);
                Refresh("滑块已切到暖色方案");
            }, page);
            app.Button(1300, 182, 124, 34, "刷新主题", "🎨", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetSliderColors(sliderMain, DemoTheme.Primary, DemoTheme.SurfacePrimary, DemoTheme.Warning);
                EmojiWindowNative.SetSliderColors(sliderFine, DemoTheme.Success, DemoTheme.SurfaceSuccess, DemoTheme.Success);
                EmojiWindowNative.SetSliderColors(sliderWide, DemoTheme.Warning, DemoTheme.SurfaceWarning, DemoTheme.Warning);
                Refresh("滑块配色已按主题刷新");
            }, page);

            app.Button(1044, 226, 116, 34, "读取当前值", "📖", DemoColors.Gray, () => Refresh("已读取当前滑块状态"), page);
            app.Button(1172, 226, 116, 34, "细步长=50", "50", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetSliderValue(sliderFine, 50);
                Refresh("细步长滑块已设为 50");
            }, page);
            app.Button(1300, 226, 124, 34, "恢复默认", "↩", DemoColors.Green, () =>
            {
                mainShowStops = true;
                EmojiWindowNative.SetSliderValue(sliderMain, 35);
                EmojiWindowNative.SetSliderValue(sliderFine, 24);
                EmojiWindowNative.SetSliderValue(sliderWide, 120);
                EmojiWindowNative.SetSliderShowStops(sliderMain, 1);
                EmojiWindowNative.SetSliderShowStops(sliderFine, 0);
                EmojiWindowNative.SetSliderShowStops(sliderWide, 1);
                EmojiWindowNative.SetSliderColors(sliderMain, DemoTheme.Primary, DemoTheme.SurfacePrimary, DemoTheme.Warning);
                EmojiWindowNative.SetSliderColors(sliderFine, DemoTheme.Success, DemoTheme.SurfaceSuccess, DemoTheme.Success);
                EmojiWindowNative.SetSliderColors(sliderWide, DemoTheme.Warning, DemoTheme.SurfaceWarning, DemoTheme.Warning);
                Refresh("Slider 页面已恢复默认状态");
            }, page);

            app.Label(40, 582, 760, 24, "1. GetSliderValue / SetSliderValue / SetSliderCallback：读取、设置并监听滑块数值。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 616, 820, 24, "2. SetSliderShowStops：切换停靠点显示。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 650, 980, 24, "3. SetSliderColors：切换激活轨道、背景轨道和圆点颜色。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            void ApplyTheme()
            {
                EmojiWindowNative.SetSliderColors(sliderMain, DemoTheme.Primary, DemoTheme.SurfacePrimary, DemoTheme.Warning);
                EmojiWindowNative.SetSliderColors(sliderFine, DemoTheme.Success, DemoTheme.SurfaceSuccess, DemoTheme.Success);
                EmojiWindowNative.SetSliderColors(sliderWide, DemoTheme.Warning, DemoTheme.SurfaceWarning, DemoTheme.Warning);
            }

            shell.RegisterPageThemeHandler(page, ApplyTheme);
            ApplyTheme();
            Refresh("Slider 页面已重排，三条滑块都应保持完整可拖拽。");
        }
    }
}
