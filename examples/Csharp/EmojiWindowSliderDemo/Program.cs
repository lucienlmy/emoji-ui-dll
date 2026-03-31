using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowSliderDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new SliderDemoApp().Run();
        }
    }

    internal sealed class SliderDemoApp : DemoApp
    {
        private IntPtr _mainSlider;
        private IntPtr _wideSlider;
        private EmojiWindowNative.SliderCallback _sliderCallback;
        private bool _wideVisible;

        public SliderDemoApp()
            : base("EmojiWindow Slider Demo - C# .NET 4.0", 960, 560)
        {
            _wideVisible = true;
        }

        protected override void Build()
        {
            const int stageX = 18;
            const int stageY = 84;

            CreateHeader("Slider 控件示例", "演示数值、范围、颜色、可见性和回调。");

            IntPtr stage = CreateGroupBox(WindowHandle, "Slider 舞台", stageX, stageY, 910, 220, ColorPrimary);
            _mainSlider = CreateStageSlider(stage, stageX, stageY, 24, 70, 520, 40, 0, 100, 36, 10, ColorPrimary, ColorBorder);
            _wideSlider = CreateStageSlider(stage, stageX, stageY, 24, 142, 520, 40, 0, 200, 120, 20, ColorWarning, ColorCard);
            EmojiWindowNative.SetSliderShowStops(_mainSlider, true);
            EmojiWindowNative.SetSliderShowStops(_wideSlider, true);

            _sliderCallback = new EmojiWindowNative.SliderCallback(OnSliderChanged);
            EmojiWindowNative.SetSliderCallback(_mainSlider, _sliderCallback);
            EmojiWindowNative.SetSliderCallback(_wideSlider, _sliderCallback);

            IntPtr ops = CreateGroupBox(WindowHandle, "Slider 操作", 18, 324, 910, 190, ColorSuccess);
            AddButton(ops, "➕", "主滑块加 5", 24, 50, 126, 34, ColorPrimary, Increase);
            AddButton(ops, "➖", "主滑块减 5", 164, 50, 126, 34, ColorSuccess, Decrease);
            AddButton(ops, "📹", "改范围 0-300", 304, 50, 140, 34, ColorWarning, ChangeRange);
            AddButton(ops, "🎨", "切颜色", 458, 50, 110, 34, ColorDanger, Recolor);
            AddButton(ops, "👁️", "显隐大范围", 582, 50, 126, 34, ColorPrimary, ToggleWideVisible);
            AddButton(ops, "📉", "读取数值", 722, 50, 110, 34, ColorSuccess, ReadValue);
        }

        private IntPtr CreateStageSlider(IntPtr stage, int stageX, int stageY, int x, int y, int width, int height, int minValue, int maxValue, int value, int step, uint activeColor, uint bgColor)
        {
            const int groupContentLeft = 10;
            const int groupContentTop = 25;

            IntPtr handle = EmojiWindowNative.CreateSlider(
                WindowHandle,
                stageX + groupContentLeft + x,
                stageY + groupContentTop + y,
                width,
                height,
                minValue,
                maxValue,
                value,
                step,
                activeColor,
                bgColor);
            EmojiWindowNative.AddChildToGroup(stage, handle);
            return handle;
        }

        private void Increase()
        {
            EmojiWindowNative.SetSliderValue(_mainSlider, EmojiWindowNative.GetSliderValue(_mainSlider) + 5);
            SetStatus("主滑块已增加。");
        }

        private void Decrease()
        {
            EmojiWindowNative.SetSliderValue(_mainSlider, EmojiWindowNative.GetSliderValue(_mainSlider) - 5);
            SetStatus("主滑块已减少。");
        }

        private void ChangeRange()
        {
            EmojiWindowNative.SetSliderRange(_mainSlider, 0, 300);
            EmojiWindowNative.SetSliderStep(_mainSlider, 15);
            SetStatus("主滑块范围已改成 0-300。");
        }

        private void Recolor()
        {
            EmojiWindowNative.SetSliderColors(_mainSlider, ColorSuccess, ColorCard, ColorDanger);
            SetStatus("主滑块配色已更新。");
        }

        private void ToggleWideVisible()
        {
            _wideVisible = !_wideVisible;
            EmojiWindowNative.ShowSlider(_wideSlider, _wideVisible);
            SetStatus("大范围滑块已" + (_wideVisible ? "显示" : "隐藏"));
        }

        private void ReadValue()
        {
            SetStatus("主滑块值 = " + EmojiWindowNative.GetSliderValue(_mainSlider) + ", 大范围值 = " + EmojiWindowNative.GetSliderValue(_wideSlider));
        }

        private void OnSliderChanged(IntPtr hSlider, int value)
        {
            SetStatus("Slider 回调: value=" + value);
        }
    }
}
