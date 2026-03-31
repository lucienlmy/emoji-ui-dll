using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowMessageBoxDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new MessageBoxDemoApp().Run();
        }
    }

    internal sealed class MessageBoxDemoApp : DemoApp
    {
        public MessageBoxDemoApp()
            : base("EmojiWindow MessageBox Demo - C# .NET 4.0", 820, 420)
        {
        }

        protected override void Build()
        {
            CreateHeader("MessageBox 控件示例", "演示信息、警告、错误三种消息框。");

            IntPtr ops = CreateGroupBox(WindowHandle, "MessageBox 操作", 18, 84, 780, 220, ColorPrimary);
            AddButton(ops, "ℹ️", "信息框", 24, 64, 120, 34, ColorPrimary, delegate { ShowInfo("信息框", "这是来自 C# demo 的信息提示。", "ℹ️"); SetStatus("已打开信息框。"); });
            AddButton(ops, "⚠️", "警告框", 158, 64, 120, 34, ColorWarning, delegate { ShowInfo("警告框", "请注意当前操作的风险。", "⚠️"); SetStatus("已打开警告框。"); });
            AddButton(ops, "❌", "错误框", 292, 64, 120, 34, ColorDanger, delegate { ShowInfo("错误框", "发生了一个可预期的错误。", "❌"); SetStatus("已打开错误框。"); });
        }
    }
}
