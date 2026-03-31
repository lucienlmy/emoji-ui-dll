using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowNotificationDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new NotificationDemoApp().Run();
        }
    }

    internal sealed class NotificationDemoApp : DemoApp
    {
        private EmojiWindowNative.NotificationCallback _notificationCallback;

        public NotificationDemoApp()
            : base("EmojiWindow Notification Demo - C# .NET 4.0", 840, 420)
        {
        }

        protected override void Build()
        {
            CreateHeader("Notification 控件示例", "演示四种通知类型和关闭回调。");

            IntPtr ops = CreateGroupBox(WindowHandle, "通知操作", 18, 84, 800, 220, ColorPrimary);
            AddButton(ops, "ℹ️", "信息通知", 24, 56, 120, 34, ColorPrimary, delegate { ShowNotify("信息通知", "这是一个信息提示。", EmojiWindowNative.NotifyInfo); });
            AddButton(ops, "✅", "成功通知", 158, 56, 120, 34, ColorSuccess, delegate { ShowNotify("成功通知", "操作已经完成。", EmojiWindowNative.NotifySuccess); });
            AddButton(ops, "⚠️", "警告通知", 292, 56, 120, 34, ColorWarning, delegate { ShowNotify("警告通知", "请检查输入内容。", EmojiWindowNative.NotifyWarning); });
            AddButton(ops, "❌", "错误通知", 426, 56, 120, 34, ColorDanger, delegate { ShowNotify("错误通知", "请求执行失败。", EmojiWindowNative.NotifyError); });
        }

        private void ShowNotify(string title, string message, int type)
        {
            byte[] titleBytes = U(title);
            byte[] messageBytes = U(message);
            IntPtr notify = EmojiWindowNative.ShowNotification(WindowHandle, titleBytes, titleBytes.Length, messageBytes, messageBytes.Length, type, EmojiWindowNative.NotifyTopRight, 2600);
            _notificationCallback = new EmojiWindowNative.NotificationCallback(OnNotifyEvent);
            EmojiWindowNative.SetNotificationCallback(notify, _notificationCallback);
            SetStatus("已弹出通知: " + title);
        }

        private void OnNotifyEvent(IntPtr hNotification, int eventType)
        {
            SetStatus("Notification 回调: eventType=" + eventType);
        }
    }
}
