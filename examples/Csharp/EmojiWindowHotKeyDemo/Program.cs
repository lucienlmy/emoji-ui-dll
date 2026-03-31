using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowHotKeyDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new HotKeyDemoApp().Run();
        }
    }

    internal sealed class HotKeyDemoApp : DemoApp
    {
        private IntPtr _hotKey;
        private EmojiWindowNative.HotKeyCallback _hotKeyCallback;

        public HotKeyDemoApp()
            : base("EmojiWindow HotKey Demo - C# .NET 4.0", 860, 460)
        {
        }

        protected override void Build()
        {
            CreateHeader("HotKey Demo", "HotKey read, set and callback sample.");

            CreateGroupBox(WindowHandle, "HotKey Stage", 18, 84, 820, 140, ColorPrimary);
            _hotKey = EmojiWindowNative.CreateHotKeyControl(WindowHandle, 52, 165, 280, 34, ColorText, ColorWhite);
            EmojiWindowNative.SetHotKey(_hotKey, 83, EmojiWindowNative.HotKeyCtrl | EmojiWindowNative.HotKeyShift);

            _hotKeyCallback = new EmojiWindowNative.HotKeyCallback(OnHotKeyChanged);
            EmojiWindowNative.SetHotKeyCallback(_hotKey, _hotKeyCallback);

            IntPtr ops = CreateGroupBox(WindowHandle, "HotKey Actions", 18, 244, 820, 140, ColorSuccess);
            AddButton(ops, "R", "Read", 24, 44, 110, 34, ColorPrimary, ReadHotKey);
            AddButton(ops, "S", "Set Ctrl+K", 148, 44, 120, 34, ColorSuccess, delegate
            {
                EmojiWindowNative.SetHotKey(_hotKey, 75, EmojiWindowNative.HotKeyCtrl);
                SetStatus("Set to Ctrl+K.");
            });
            AddButton(ops, "C", "Clear", 282, 44, 110, 34, ColorWarning, delegate
            {
                EmojiWindowNative.ClearHotKey(_hotKey);
                SetStatus("HotKey cleared.");
            });
            AddButton(ops, "P", "Palette", 406, 44, 110, 34, ColorDanger, delegate
            {
                EmojiWindowNative.SetHotKeyColors(_hotKey, ColorPrimary, ColorCard, ColorPrimary);
                SetStatus("HotKey colors updated.");
            });
        }

        private void ReadHotKey()
        {
            int vkCode;
            int modifiers;
            EmojiWindowNative.GetHotKey(_hotKey, out vkCode, out modifiers);
            SetStatus("vk=" + vkCode + ", modifiers=" + modifiers);
        }

        private void OnHotKeyChanged(IntPtr hHotKey, int vkCode, int modifiers)
        {
            SetStatus("HotKey callback: vk=" + vkCode + ", modifiers=" + modifiers);
        }
    }
}
