using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowSwitchDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new SwitchDemoApp().Run();
        }
    }

    internal sealed class SwitchDemoApp : DemoApp
    {
        private IntPtr _mainSwitch;
        private IntPtr _statusSwitch;
        private EmojiWindowNative.SwitchCallback _switchCallback;
        private bool _statusVisible;

        public SwitchDemoApp()
            : base("EmojiWindow Switch Demo - C# .NET 4.0", 920, 540)
        {
            _statusVisible = true;
        }

        protected override void Build()
        {
            const int stageX = 18;
            const int stageY = 84;

            CreateHeader("Switch 控件示例", "演示开关状态、文本、颜色、可见性和回调。");

            IntPtr stage = CreateGroupBox(WindowHandle, "Switch 舞台", stageX, stageY, 870, 220, ColorPrimary);
            _mainSwitch = CreateStageSwitch(stage, stageX, stageY, 24, 64, true, "开", "关", ColorPrimary);
            _statusSwitch = CreateStageSwitch(stage, stageX, stageY, 24, 138, true, "在线", "离线", ColorSuccess);

            _switchCallback = new EmojiWindowNative.SwitchCallback(OnSwitchChanged);
            EmojiWindowNative.SetSwitchCallback(_mainSwitch, _switchCallback);
            EmojiWindowNative.SetSwitchCallback(_statusSwitch, _switchCallback);

            IntPtr ops = CreateGroupBox(WindowHandle, "Switch 操作", 18, 324, 870, 170, ColorSuccess);
            AddButton(ops, "🔧", "切主开关", 24, 48, 110, 34, ColorPrimary, ToggleMain);
            AddButton(ops, "✏️", "改主文案", 148, 48, 110, 34, ColorSuccess, RenameMain);
            AddButton(ops, "🎨", "改主配色", 272, 48, 110, 34, ColorWarning, RecolorMain);
            AddButton(ops, "👁️", "显隐状态开关", 396, 48, 140, 34, ColorDanger, ToggleStatusVisible);
            AddButton(ops, "📉", "读取状态", 550, 48, 110, 34, ColorPrimary, ReadState);
        }

        private IntPtr CreateStageSwitch(IntPtr stage, int stageX, int stageY, int x, int y, bool isChecked, string onText, string offText, uint activeColor)
        {
            const int groupContentLeft = 10;
            const int groupContentTop = 25;

            byte[] onBytes = U(onText);
            byte[] offBytes = U(offText);
            IntPtr handle = EmojiWindowNative.CreateSwitch(
                WindowHandle,
                stageX + groupContentLeft + x,
                stageY + groupContentTop + y,
                128,
                34,
                isChecked,
                activeColor,
                ColorBorder,
                onBytes,
                onBytes.Length,
                offBytes,
                offBytes.Length);
            EmojiWindowNative.AddChildToGroup(stage, handle);
            return handle;
        }

        private void ToggleMain()
        {
            EmojiWindowNative.SetSwitchState(_mainSwitch, !EmojiWindowNative.GetSwitchState(_mainSwitch));
            SetStatus("主开关状态已切换。");
        }

        private void RenameMain()
        {
            byte[] onBytes = U("启用");
            byte[] offBytes = U("停用");
            EmojiWindowNative.SetSwitchText(_mainSwitch, onBytes, onBytes.Length, offBytes, offBytes.Length);
            SetStatus("主开关文案已更新。");
        }

        private void RecolorMain()
        {
            EmojiWindowNative.SetSwitchColors(_mainSwitch, ColorDanger, ColorBorder);
            EmojiWindowNative.SetSwitchTextColors(_mainSwitch, ColorWhite, ColorMuted);
            SetStatus("主开关配色已切换。");
        }

        private void ToggleStatusVisible()
        {
            _statusVisible = !_statusVisible;
            EmojiWindowNative.ShowSwitch(_statusSwitch, _statusVisible);
            SetStatus("状态开关已" + (_statusVisible ? "显示" : "隐藏"));
        }

        private void ReadState()
        {
            SetStatus("主开关=" + EmojiWindowNative.GetSwitchState(_mainSwitch) + ", 状态开关=" + EmojiWindowNative.GetSwitchState(_statusSwitch));
        }

        private void OnSwitchChanged(IntPtr hSwitch, int isChecked)
        {
            SetStatus("Switch 回调: checked=" + isChecked);
        }
    }
}
