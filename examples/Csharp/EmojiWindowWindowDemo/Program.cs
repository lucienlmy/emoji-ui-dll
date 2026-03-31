using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowWindowDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new WindowDemoApp().Run();
        }
    }

    internal sealed class WindowDemoApp : DemoApp
    {
        private EmojiWindowNative.WindowResizeCallback _resizeCallback;
        private IntPtr _infoLabel;
        private int _currentWidth;
        private int _currentHeight;

        public WindowDemoApp()
            : base("EmojiWindow Window Demo - C# .NET 4.0", 920, 520)
        {
            _currentWidth = 920;
            _currentHeight = 520;
        }

        protected override void Build()
        {
            CreateHeader("Window 控件示例", "演示窗口标题读取、尺寸更新和 Resize 回调。");

            IntPtr box = CreateGroupBox(WindowHandle, "窗口属性与回调", 18, 84, 870, 380, ColorPrimary);
            CreateLabel(box, "这个 demo 不隐藏主窗口，只演示读取标题、读取 Bounds、调整大小，以及收到窗口尺寸变化回调。", 18, 24, 810, 48, ColorMuted, ColorWhite, 11, false, true, EmojiWindowNative.AlignLeft);
            _infoLabel = CreateLabel(box, "等待读取窗口状态。", 18, 82, 820, 64, ColorText, ColorWhite, 12, false, true, EmojiWindowNative.AlignLeft);

            AddButton(box, "📖", "读取标题", 18, 170, 120, 34, ColorPrimary, ReadTitle);
            AddButton(box, "📐", "读取 Bounds", 150, 170, 120, 34, ColorSuccess, RefreshInfo);
            AddButton(box, "➕", "放大窗口", 282, 170, 120, 34, ColorWarning, EnlargeWindow);
            AddButton(box, "➖", "缩小窗口", 414, 170, 120, 34, ColorDanger, ShrinkWindow);
            AddButton(box, "🎯", "重置尺寸", 546, 170, 120, 34, ColorPrimary, ResetWindow);

            _resizeCallback = new EmojiWindowNative.WindowResizeCallback(OnWindowResized);
            EmojiWindowNative.SetWindowResizeCallback(_resizeCallback);
            RefreshInfo();
        }

        private void ReadTitle()
        {
            string title = EmojiWindowNative.ReadText(WindowHandle, EmojiWindowNative.GetWindowTitle);
            SetStatus("窗口标题: " + title);
        }

        private void EnlargeWindow()
        {
            _currentWidth += 80;
            _currentHeight += 40;
            EmojiWindowNative.SetWindowBounds(WindowHandle, -1, -1, _currentWidth, _currentHeight);
            RefreshInfo();
        }

        private void ShrinkWindow()
        {
            _currentWidth = Math.Max(680, _currentWidth - 80);
            _currentHeight = Math.Max(420, _currentHeight - 40);
            EmojiWindowNative.SetWindowBounds(WindowHandle, -1, -1, _currentWidth, _currentHeight);
            RefreshInfo();
        }

        private void ResetWindow()
        {
            _currentWidth = 920;
            _currentHeight = 520;
            EmojiWindowNative.SetWindowBounds(WindowHandle, -1, -1, _currentWidth, _currentHeight);
            RefreshInfo();
        }

        private void RefreshInfo()
        {
            int x;
            int y;
            int width;
            int height;
            EmojiWindowNative.GetWindowBounds(WindowHandle, out x, out y, out width, out height);
            string text = "当前窗口 Bounds: x=" + x + ", y=" + y + ", width=" + width + ", height=" + height + "\r\n" +
                          "TitleBar Color: 0x" + EmojiWindowNative.GetWindowTitlebarColor(WindowHandle).ToString("X8");
            byte[] bytes = U(text);
            EmojiWindowNative.SetLabelText(_infoLabel, bytes, bytes.Length);
            SetStatus("已读取窗口位置与尺寸。");
        }

        private void OnWindowResized(IntPtr hwnd, int width, int height)
        {
            _currentWidth = width;
            _currentHeight = height;
            SetStatus("Resize 回调: width=" + width + ", height=" + height);
        }
    }
}
