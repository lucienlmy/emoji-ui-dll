using System;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using EmojiWindowDemoCommon;

namespace EmojiWindowPictureBoxDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new PictureBoxDemoApp().Run();
        }
    }

    internal sealed class PictureBoxDemoApp : DemoApp
    {
        private IntPtr _pictureBox;
        private EmojiWindowNative.PictureBoxCallback _pictureCallback;

        public PictureBoxDemoApp()
            : base("EmojiWindow PictureBox Demo - C# .NET 4.0", 920, 560)
        {
        }

        protected override void Build()
        {
            CreateHeader("PictureBox 控件示例", "演示内存图片加载、缩放模式、透明度和点击回调。");

            CreateGroupBox(WindowHandle, "PictureBox 舞台", 18, 84, 880, 260, ColorPrimary);
            _pictureBox = EmojiWindowNative.CreatePictureBox(WindowHandle, 52, 155, 320, 180, EmojiWindowNative.ScaleFit, ColorCard);
            byte[] imageBytes = BuildSampleImage();
            EmojiWindowNative.LoadImageFromMemory(_pictureBox, imageBytes, imageBytes.Length);
            _pictureCallback = new EmojiWindowNative.PictureBoxCallback(OnPictureClicked);
            EmojiWindowNative.SetPictureBoxCallback(_pictureBox, _pictureCallback);

            IntPtr ops = CreateGroupBox(WindowHandle, "PictureBox 操作", 18, 364, 880, 150, ColorSuccess);
            AddButton(ops, "🔄", "重新加载", 24, 46, 120, 34, ColorPrimary, Reload);
            AddButton(ops, "📐", "拉伸模式", 158, 46, 120, 34, ColorSuccess, delegate { EmojiWindowNative.SetPictureBoxScaleMode(_pictureBox, EmojiWindowNative.ScaleStretch); SetStatus("已切到 Stretch 模式。"); });
            AddButton(ops, "🎯", "居中模式", 292, 46, 120, 34, ColorWarning, delegate { EmojiWindowNative.SetPictureBoxScaleMode(_pictureBox, EmojiWindowNative.ScaleCenter); SetStatus("已切到 Center 模式。"); });
            AddButton(ops, "💧", "半透明", 426, 46, 120, 34, ColorDanger, delegate { EmojiWindowNative.SetImageOpacity(_pictureBox, 0.5f); SetStatus("透明度已改成 0.5。"); });
            AddButton(ops, "🧹", "清空图片", 560, 46, 120, 34, ColorPrimary, delegate { EmojiWindowNative.ClearImage(_pictureBox); SetStatus("图片已清空。"); });
        }

        private byte[] BuildSampleImage()
        {
            Bitmap bitmap = new Bitmap(240, 140);
            Graphics g = Graphics.FromImage(bitmap);
            g.Clear(Color.WhiteSmoke);
            g.FillEllipse(new SolidBrush(Color.FromArgb(64, 158, 255)), 18, 18, 72, 72);
            g.FillRectangle(new SolidBrush(Color.FromArgb(103, 194, 58)), 108, 24, 90, 54);
            g.DrawString("emoji_window", new Font("Microsoft YaHei UI", 12), Brushes.Black, 18, 102);
            MemoryStream stream = new MemoryStream();
            bitmap.Save(stream, ImageFormat.Png);
            byte[] bytes = stream.ToArray();
            stream.Dispose();
            g.Dispose();
            bitmap.Dispose();
            return bytes;
        }

        private void Reload()
        {
            byte[] bytes = BuildSampleImage();
            EmojiWindowNative.LoadImageFromMemory(_pictureBox, bytes, bytes.Length);
            SetStatus("图片已重新从内存加载。");
        }

        private void OnPictureClicked(IntPtr hPictureBox)
        {
            SetStatus("PictureBox 点击回调已触发。");
        }
    }
}
