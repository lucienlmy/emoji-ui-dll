using System;

namespace EmojiWindowDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            DemoRunner.Run(DemoKind.ProgressBar);
        }
    }
}
