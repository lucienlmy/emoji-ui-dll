using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowConfirmBoxDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new ConfirmBoxDemoApp().Run();
        }
    }

    internal sealed class ConfirmBoxDemoApp : DemoApp
    {
        private EmojiWindowNative.MessageBoxCallback _confirmCallback;

        public ConfirmBoxDemoApp()
            : base("EmojiWindow ConfirmBox Demo - C# .NET 4.0", 820, 420)
        {
        }

        protected override void Build()
        {
            CreateHeader("ConfirmBox 控件示例", "演示确认框弹出和回调结果。");

            IntPtr ops = CreateGroupBox(WindowHandle, "ConfirmBox 操作", 18, 84, 780, 220, ColorPrimary);
            AddButton(ops, "❓", "打开确认框", 24, 64, 140, 34, ColorPrimary, OpenConfirm);
        }

        private void OpenConfirm()
        {
            _confirmCallback = new EmojiWindowNative.MessageBoxCallback(OnConfirm);
            byte[] title = U("确认框");
            byte[] message = U("确定要继续执行这个演示动作吗？");
            byte[] icon = U("❓");
            EmojiWindowNative.show_confirm_box_bytes(WindowHandle, title, title.Length, message, message.Length, icon, icon.Length, _confirmCallback);
            SetStatus("确认框已打开。");
        }

        private void OnConfirm(int confirmed)
        {
            SetStatus(confirmed != 0 ? "用户点击了确认。" : "用户点击了取消。");
        }
    }
}
