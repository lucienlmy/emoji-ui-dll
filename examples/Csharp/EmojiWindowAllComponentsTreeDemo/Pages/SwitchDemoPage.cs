using System;

namespace EmojiWindowDemo
{
    internal static class SwitchDemoPage
    {
        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;

            app.GroupBox(16, 16, 980, 324, "🧭 Switch 样式演示", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(1020, 16, 444, 324, "🧪 状态 / 文案 / 配色", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(16, 538, 1448, 220, "📘 Switch API 说明", DemoTheme.Border, DemoTheme.Background, page);

            app.Label(40, 56, 930, 24, "左侧展示四种 Switch 组合，用于直接验证状态、文案、配色和层次分区。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);

            byte[] on = app.U("开");
            byte[] off = app.U("关");
            byte[] online = app.U("在线");
            byte[] offline = app.U("离线");
            byte[] yes = app.U("是");
            byte[] no = app.U("否");
            byte[] blank = app.U(string.Empty);

            IntPtr switchMain = EmojiWindowNative.CreateSwitch(page, 56, 128, 112, 34, 1, DemoTheme.Primary, DemoTheme.BorderLight, on, on.Length, off, off.Length);
            IntPtr switchCompact = EmojiWindowNative.CreateSwitch(page, 56, 214, 82, 30, 0, DemoTheme.Warning, DemoTheme.BorderLight, blank, blank.Length, blank, blank.Length);
            IntPtr switchStatus = EmojiWindowNative.CreateSwitch(page, 320, 128, 148, 36, 1, DemoTheme.Success, DemoTheme.BorderLight, online, online.Length, offline, offline.Length);
            IntPtr switchConfirm = EmojiWindowNative.CreateSwitch(page, 320, 214, 112, 34, 0, DemoTheme.Muted, DemoTheme.BorderLight, yes, yes.Length, no, no.Length);

            app.Label(56, 96, 180, 20, "主开关", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Label(56, 182, 180, 20, "紧凑样式", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Label(320, 96, 180, 20, "状态文案", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Label(320, 182, 180, 20, "确认文案", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);

            IntPtr readout = app.Label(40, 366, 1384, 108, "等待读取 Switch 状态。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr stateLabel = app.Label(40, 490, 1360, 22, "Switch 页状态将在这里更新。", DemoTheme.Primary, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            string mainOnText = "开";
            string mainOffText = "关";

            void Refresh(string note)
            {
                shell.SetLabelText(
                    readout,
                    $"main={EmojiWindowNative.GetSwitchState(switchMain)} text=({mainOnText}/{mainOffText})\r\n" +
                    $"compact={EmojiWindowNative.GetSwitchState(switchCompact)}  status={EmojiWindowNative.GetSwitchState(switchStatus)}  confirm={EmojiWindowNative.GetSwitchState(switchConfirm)}\r\n" +
                    note);
                shell.SetLabelText(stateLabel, note);
                shell.SetStatus(note);
            }

            var callback = app.Pin(new EmojiWindowNative.SwitchCallback((_, checkedState) => Refresh("Switch 回调: checked=" + checkedState)));
            EmojiWindowNative.SetSwitchCallback(switchMain, callback);
            EmojiWindowNative.SetSwitchCallback(switchCompact, callback);
            EmojiWindowNative.SetSwitchCallback(switchStatus, callback);
            EmojiWindowNative.SetSwitchCallback(switchConfirm, callback);

            app.Button(1044, 94, 116, 34, "主开=开", "ON", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetSwitchState(switchMain, 1);
                Refresh("主开关已设为开启");
            }, page);
            app.Button(1172, 94, 116, 34, "主开=关", "OFF", DemoColors.Gray, () =>
            {
                EmojiWindowNative.SetSwitchState(switchMain, 0);
                Refresh("主开关已设为关闭");
            }, page);
            app.Button(1300, 94, 124, 34, "切换文案", "📝", DemoColors.Blue, () =>
            {
                if (mainOnText == "开")
                {
                    mainOnText = "启用";
                    mainOffText = "停用";
                }
                else
                {
                    mainOnText = "开";
                    mainOffText = "关";
                }

                byte[] active = app.U(mainOnText);
                byte[] inactive = app.U(mainOffText);
                EmojiWindowNative.SetSwitchText(switchMain, active, active.Length, inactive, inactive.Length);
                Refresh("主开关文案已切换");
            }, page);

            app.Button(1044, 138, 116, 34, "紧凑切换", "↔", DemoColors.Purple, () =>
            {
                EmojiWindowNative.SetSwitchState(switchCompact, EmojiWindowNative.GetSwitchState(switchCompact) == 0 ? 1 : 0);
                Refresh("紧凑样式开关已切换");
            }, page);
            app.Button(1172, 138, 116, 34, "状态=在线", "🟢", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetSwitchState(switchStatus, 1);
                Refresh("状态开关已切到在线");
            }, page);
            app.Button(1300, 138, 124, 34, "状态=离线", "🔴", DemoColors.Orange, () =>
            {
                EmojiWindowNative.SetSwitchState(switchStatus, 0);
                Refresh("状态开关已切到离线");
            }, page);

            app.Button(1044, 182, 116, 34, "确认=是", "✓", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetSwitchState(switchConfirm, 1);
                Refresh("确认开关已切到是");
            }, page);
            app.Button(1172, 182, 116, 34, "确认=否", "✕", DemoColors.Gray, () =>
            {
                EmojiWindowNative.SetSwitchState(switchConfirm, 0);
                Refresh("确认开关已切到否");
            }, page);
            app.Button(1300, 182, 124, 34, "恢复默认", "↩", DemoColors.Green, () =>
            {
                mainOnText = "开";
                mainOffText = "关";
                byte[] active = app.U(mainOnText);
                byte[] inactive = app.U(mainOffText);
                EmojiWindowNative.SetSwitchText(switchMain, active, active.Length, inactive, inactive.Length);
                EmojiWindowNative.SetSwitchState(switchMain, 1);
                EmojiWindowNative.SetSwitchState(switchCompact, 0);
                EmojiWindowNative.SetSwitchState(switchStatus, 1);
                EmojiWindowNative.SetSwitchState(switchConfirm, 0);
                Refresh("Switch 页已恢复默认状态");
            }, page);

            app.Label(40, 582, 760, 24, "1. GetSwitchState / SetSwitchState / SetSwitchCallback：读取、设置并监听当前开关状态。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 616, 760, 24, "2. SetSwitchText：动态切换开启 / 关闭两套文案。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            Refresh("Switch 页面已重排，可直接测试状态和文案切换。");
        }
    }
}
