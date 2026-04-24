using System;
using System.IO;

namespace EmojiWindowDemo
{
    internal static class Program
    {
        private const int ScaleFit = 2;
        private const string FontName = "Microsoft YaHei UI";
        private const string ExpectedImagePath = @"T:\易语言源码\API创建窗口\emoji_window_cpp\examples\Csharp\qrcode_523446917.jpg";

        private static readonly byte[] FontBytes = EmojiWindowNative.ToUtf8(FontName);
        private static readonly EmojiWindowNative.ButtonClickCallback ButtonClickHandler = OnButtonClick;
        private static readonly EmojiWindowNative.PictureBoxCallback PictureClickHandler = OnPictureBoxClick;

        private static IntPtr _window;
        private static IntPtr _statusLabel;
        private static IntPtr _pictureBox;
        private static int _reloadButtonId;
        private static int _fitButtonId;
        private static int _backgroundButtonId;
        private static int _clearButtonId;

        [STAThread]
        private static void Main()
        {
            CreateDemoWindow();
            EmojiWindowNative.set_button_click_callback(ButtonClickHandler);
            EmojiWindowNative.SetPictureBoxCallback(_pictureBox, PictureClickHandler);
            LoadQrImage();
            EmojiWindowNative.set_message_loop_main_window(_window);
            EmojiWindowNative.run_message_loop();
        }

        private static void CreateDemoWindow()
        {
            byte[] title = EmojiWindowNative.ToUtf8("EmojiWindowPictureBoxDemo - QR Code x64");
            _window = EmojiWindowNative.create_window_bytes_ex(
                title,
                title.Length,
                160,
                100,
                820,
                760,
                DemoColors.Blue,
                DemoColors.WindowBg);

            if (_window == IntPtr.Zero)
            {
                throw new InvalidOperationException("Failed to create demo window.");
            }

            CreateLabel(24, 24, 760, 28, "Target image: examples/Csharp/qrcode_523446917.jpg", DemoColors.Black, DemoColors.Transparent, 12);
            CreateLabel(24, 54, 760, 24, "Scale mode uses FIT so the whole image stays visible in the picture box.", DemoColors.Gray, DemoColors.Transparent, 11);

            _pictureBox = EmojiWindowNative.CreatePictureBox(_window, 24, 96, 420, 600, ScaleFit, DemoColors.White);
            if (_pictureBox == IntPtr.Zero)
            {
                throw new InvalidOperationException("Failed to create picture box.");
            }

            _reloadButtonId = CreateButton(484, 112, 240, 40, "Reload QR image", DemoColors.Blue);
            _fitButtonId = CreateButton(484, 168, 240, 40, "Keep full image visible", DemoColors.Green);
            _backgroundButtonId = CreateButton(484, 224, 240, 40, "Set white background", DemoColors.Cyan);
            _clearButtonId = CreateButton(484, 280, 240, 40, "Clear image", DemoColors.Red);

            _statusLabel = CreateLabel(24, 708, 760, 24, "Ready.", DemoColors.Black, DemoColors.Transparent, 12);
        }

        private static int CreateButton(int x, int y, int width, int height, string text, uint color)
        {
            byte[] textBytes = EmojiWindowNative.ToUtf8(text);
            return EmojiWindowNative.create_emoji_button_bytes(
                _window,
                Array.Empty<byte>(),
                0,
                textBytes,
                textBytes.Length,
                x,
                y,
                width,
                height,
                color);
        }

        private static IntPtr CreateLabel(int x, int y, int width, int height, string text, uint fgColor, uint bgColor, int fontSize)
        {
            byte[] textBytes = EmojiWindowNative.ToUtf8(text);
            return EmojiWindowNative.CreateLabel(
                _window,
                x,
                y,
                width,
                height,
                textBytes,
                textBytes.Length,
                fgColor,
                bgColor,
                FontBytes,
                FontBytes.Length,
                fontSize,
                0,
                0,
                0,
                0,
                0);
        }

        private static void SetStatus(string text)
        {
            if (_statusLabel == IntPtr.Zero)
            {
                return;
            }

            byte[] textBytes = EmojiWindowNative.ToUtf8(text);
            EmojiWindowNative.SetLabelText(_statusLabel, textBytes, textBytes.Length);
        }

        private static void OnButtonClick(int buttonId, IntPtr parentHwnd)
        {
            if (buttonId == _reloadButtonId)
            {
                LoadQrImage();
                return;
            }

            if (buttonId == _fitButtonId)
            {
                EmojiWindowNative.SetPictureBoxScaleMode(_pictureBox, ScaleFit);
                EmojiWindowNative.SetImageOpacity(_pictureBox, 1.0f);
                SetStatus("Scale mode set to FIT. The whole QR image stays visible.");
                return;
            }

            if (buttonId == _backgroundButtonId)
            {
                EmojiWindowNative.SetPictureBoxBackgroundColor(_pictureBox, DemoColors.White);
                SetStatus("Picture box background changed to white.");
                return;
            }

            if (buttonId == _clearButtonId)
            {
                EmojiWindowNative.ClearImage(_pictureBox);
                SetStatus("Image cleared.");
            }
        }

        private static void OnPictureBoxClick(IntPtr handle)
        {
            SetStatus("PictureBox clicked.");
        }

        private static void LoadQrImage()
        {
            string imagePath = ResolveImagePath();
            if (string.IsNullOrEmpty(imagePath))
            {
                SetStatus("Image not found: qrcode_523446917.jpg");
                return;
            }

            byte[] pathBytes = EmojiWindowNative.ToUtf8(imagePath);
            EmojiWindowNative.SetPictureBoxScaleMode(_pictureBox, ScaleFit);
            EmojiWindowNative.SetImageOpacity(_pictureBox, 1.0f);
            int result = EmojiWindowNative.LoadImageFromFile(_pictureBox, pathBytes, pathBytes.Length);

            if (result == 0)
            {
                SetStatus("Failed to load image.");
                return;
            }

            SetStatus("Loaded in FIT mode: " + Path.GetFileName(imagePath));
        }

        private static string ResolveImagePath()
        {
            if (File.Exists(ExpectedImagePath))
            {
                return ExpectedImagePath;
            }

            string current = AppDomain.CurrentDomain.BaseDirectory;
            while (!string.IsNullOrEmpty(current))
            {
                string candidate = Path.Combine(current, "qrcode_523446917.jpg");
                if (File.Exists(candidate))
                {
                    return candidate;
                }

                DirectoryInfo parent = Directory.GetParent(current);
                if (parent == null)
                {
                    break;
                }

                current = parent.FullName;
            }

            return string.Empty;
        }
    }
}
