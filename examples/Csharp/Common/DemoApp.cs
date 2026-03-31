using System;
using System.Collections.Generic;

namespace EmojiWindowDemoCommon
{
    internal abstract class DemoApp
    {
        private readonly string _windowTitle;
        private readonly int _windowWidth;
        private readonly int _windowHeight;
        private readonly Dictionary<int, Action> _buttonActions;
        private EmojiWindowNative.ButtonClickCallback _buttonCallback;

        protected DemoApp(string windowTitle, int windowWidth, int windowHeight)
        {
            _windowTitle = windowTitle;
            _windowWidth = windowWidth;
            _windowHeight = windowHeight;
            _buttonActions = new Dictionary<int, Action>();
            FontYaHei = EmojiWindowNative.ToUtf8("Microsoft YaHei UI");
        }

        protected IntPtr WindowHandle;
        protected IntPtr StatusLabel;
        protected readonly byte[] FontYaHei;

        protected uint ColorText = EmojiWindowNative.ARGB(255, 48, 49, 51);
        protected uint ColorMuted = EmojiWindowNative.ARGB(255, 96, 98, 102);
        protected uint ColorBackground = EmojiWindowNative.ARGB(255, 250, 250, 252);
        protected uint ColorCard = EmojiWindowNative.ARGB(255, 245, 247, 250);
        protected uint ColorBorder = EmojiWindowNative.ARGB(255, 220, 223, 230);
        protected uint ColorPrimary = EmojiWindowNative.ARGB(255, 64, 158, 255);
        protected uint ColorSuccess = EmojiWindowNative.ARGB(255, 103, 194, 58);
        protected uint ColorWarning = EmojiWindowNative.ARGB(255, 230, 162, 60);
        protected uint ColorDanger = EmojiWindowNative.ARGB(255, 245, 108, 108);
        protected uint ColorWhite = EmojiWindowNative.ARGB(255, 255, 255, 255);

        public void Run()
        {
            byte[] titleBytes = U(_windowTitle);
            WindowHandle = EmojiWindowNative.create_window_bytes_ex(titleBytes, titleBytes.Length, -1, -1, _windowWidth, _windowHeight, EmojiWindowNative.ARGB(255, 36, 41, 47), ColorBackground);
            if (WindowHandle == IntPtr.Zero)
            {
                Console.WriteLine("创建窗口失败。");
                return;
            }

            _buttonCallback = new EmojiWindowNative.ButtonClickCallback(HandleButtonClick);
            EmojiWindowNative.set_button_click_callback(_buttonCallback);
            Build();
            EmojiWindowNative.set_message_loop_main_window(WindowHandle);
            EmojiWindowNative.run_message_loop();
        }

        protected abstract void Build();

        protected byte[] U(string text)
        {
            return EmojiWindowNative.ToUtf8(text);
        }

        protected void CreateHeader(string title, string subtitle)
        {
            CreateLabel(WindowHandle, title, 18, 12, 1000, 28, ColorText, ColorBackground, 17, true, false, EmojiWindowNative.AlignLeft);
            StatusLabel = CreateLabel(WindowHandle, subtitle, 18, 46, 1160, 24, ColorMuted, ColorBackground, 11, false, false, EmojiWindowNative.AlignLeft);
        }

        protected IntPtr CreateLabel(IntPtr parent, string text, int x, int y, int width, int height, uint fgColor, uint bgColor, int fontSize, bool bold, bool wordWrap, int align)
        {
            byte[] textBytes = U(text);
            return EmojiWindowNative.CreateLabel(parent, x, y, width, height, textBytes, textBytes.Length, fgColor, bgColor, FontYaHei, FontYaHei.Length, fontSize, bold, false, false, align, wordWrap);
        }

        protected IntPtr CreateGroupBox(IntPtr parent, string title, int x, int y, int width, int height, uint borderColor)
        {
            byte[] titleBytes = U(title);
            return EmojiWindowNative.CreateGroupBox(parent, x, y, width, height, titleBytes, titleBytes.Length, borderColor, ColorWhite, FontYaHei, FontYaHei.Length, 13, true, false, false);
        }

        protected IntPtr CreatePanel(IntPtr parent, int x, int y, int width, int height, uint bgColor)
        {
            return EmojiWindowNative.CreatePanel(parent, x, y, width, height, bgColor);
        }

        protected IntPtr CreateEditBox(IntPtr parent, string text, int x, int y, int width, int height, bool multiline, bool readOnly)
        {
            byte[] textBytes = U(text);
            return EmojiWindowNative.CreateEditBox(parent, x, y, width, height, textBytes, textBytes.Length, ColorText, ColorWhite, FontYaHei, FontYaHei.Length, 12, false, false, false, EmojiWindowNative.AlignLeft, multiline, readOnly, false, true, false);
        }

        protected int AddButton(IntPtr parent, string emoji, string text, int x, int y, int width, int height, uint bgColor, Action action)
        {
            byte[] emojiBytes = U(emoji);
            byte[] textBytes = U(text);
            int buttonId = EmojiWindowNative.create_emoji_button_bytes(parent, emojiBytes, emojiBytes.Length, textBytes, textBytes.Length, x, y, width, height, bgColor);
            _buttonActions[buttonId] = action;
            return buttonId;
        }

        protected void SetStatus(string text)
        {
            if (StatusLabel == IntPtr.Zero)
            {
                return;
            }

            byte[] textBytes = U(text);
            EmojiWindowNative.SetLabelText(StatusLabel, textBytes, textBytes.Length);
        }

        protected void ShowInfo(string title, string message, string icon)
        {
            byte[] titleBytes = U(title);
            byte[] messageBytes = U(message);
            byte[] iconBytes = U(icon);
            EmojiWindowNative.show_message_box_bytes(WindowHandle, titleBytes, titleBytes.Length, messageBytes, messageBytes.Length, iconBytes, iconBytes.Length);
        }

        private void HandleButtonClick(int buttonId, IntPtr parentHwnd)
        {
            Action action;
            if (_buttonActions.TryGetValue(buttonId, out action))
            {
                action();
            }
        }
    }
}
