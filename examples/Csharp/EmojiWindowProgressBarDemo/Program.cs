using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowProgressBarDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new ProgressBarDemoApp().Run();
        }
    }

    internal sealed class ProgressBarDemoApp : DemoApp
    {
        private IntPtr _mainBar;
        private IntPtr _thinBar;
        private EmojiWindowNative.ProgressBarCallback _progressCallback;
        private bool _showText;
        private int _value;

        public ProgressBarDemoApp()
            : base("EmojiWindow ProgressBar Demo - C# .NET 4.0", 900, 520)
        {
            _showText = true;
            _value = 30;
        }

        protected override void Build()
        {
            CreateHeader("ProgressBar 控件示例", "演示数值更新、颜色切换、不确定模式和显示文本。");

            CreateGroupBox(WindowHandle, "ProgressBar 舞台", 18, 84, 850, 180, ColorPrimary);
            _mainBar = EmojiWindowNative.CreateProgressBar(WindowHandle, 52, 167, 520, 28, _value, ColorPrimary, ColorBorder, true, ColorText);
            _thinBar = EmojiWindowNative.CreateProgressBar(WindowHandle, 52, 221, 520, 18, 62, ColorSuccess, ColorCard, false, ColorText);

            _progressCallback = new EmojiWindowNative.ProgressBarCallback(OnProgressChanged);
            EmojiWindowNative.SetProgressBarCallback(_mainBar, _progressCallback);

            IntPtr ops = CreateGroupBox(WindowHandle, "ProgressBar 操作", 18, 284, 850, 170, ColorSuccess);
            AddButton(ops, "➕", "加 10", 24, 48, 110, 34, ColorPrimary, Increase);
            AddButton(ops, "➖", "减 10", 148, 48, 110, 34, ColorSuccess, Decrease);
            AddButton(ops, "🎨", "切颜色", 272, 48, 110, 34, ColorWarning, Recolor);
            AddButton(ops, "🌀", "不确定模式", 396, 48, 126, 34, ColorDanger, ToggleIndeterminate);
            AddButton(ops, "🔤", "切文字显示", 536, 48, 126, 34, ColorPrimary, ToggleText);
            AddButton(ops, "📐", "改尺寸", 676, 48, 110, 34, ColorSuccess, ResizeMainBar);
        }

        private void Increase()
        {
            _value = Math.Min(100, _value + 10);
            EmojiWindowNative.SetProgressValue(_mainBar, _value);
            SetStatus("当前进度 = " + _value);
        }

        private void Decrease()
        {
            _value = Math.Max(0, _value - 10);
            EmojiWindowNative.SetProgressValue(_mainBar, _value);
            SetStatus("当前进度 = " + _value);
        }

        private void Recolor()
        {
            EmojiWindowNative.SetProgressBarColor(_mainBar, ColorDanger, ColorCard);
            EmojiWindowNative.SetProgressBarTextColor(_mainBar, ColorDanger);
            SetStatus("主进度条已切到红色方案。");
        }

        private void ToggleIndeterminate()
        {
            EmojiWindowNative.SetProgressIndeterminate(_thinBar, true);
            SetStatus("细进度条已切到不确定模式。");
        }

        private void ToggleText()
        {
            _showText = !_showText;
            EmojiWindowNative.SetProgressBarShowText(_mainBar, _showText);
            SetStatus("主进度条文本显示 = " + _showText);
        }

        private void ResizeMainBar()
        {
            EmojiWindowNative.SetProgressBarBounds(_mainBar, 52, 167, 680, 28);
            SetStatus("主进度条宽度已放大。");
        }

        private void OnProgressChanged(IntPtr hProgressBar, int value)
        {
            SetStatus("ProgressBar 回调: value=" + value);
        }
    }
}
