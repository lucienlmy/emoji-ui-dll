using System;

namespace EmojiWindowDemo
{
    internal static class HotKeyDemoPage
    {
        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;

            app.GroupBox(16, 16, 980, 408, "⌨️ HotKeyControl 舞台区", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(1020, 16, 444, 408, "🧪 热键 / 配色 / 布局 / 状态", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(16, 450, 1448, 328, "📘 HotKeyControl API 说明", DemoTheme.Border, DemoTheme.Background, page);

            app.Label(40, 56, 900, 24, "热键页改成“控件舞台 + 实时读数 + 操作区”结构，避免只剩下一行热键框和一排按钮。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);

            int x = 48;
            int y = 110;
            int width = 320;
            int height = 38;
            bool visible = true;
            bool enabled = true;
            string colorMode = "theme";

            IntPtr hotKey = EmojiWindowNative.CreateHotKeyControl(page, x, y, width, height, DemoTheme.Text, DemoTheme.Background);
            IntPtr readout = app.Label(40, 176, 860, 76, "等待读取热键。", DemoTheme.Text, DemoTheme.Background, 13, PageCommon.AlignLeft, true, page);
            IntPtr stageNote = app.Label(40, 270, 900, 56, "建议把热键框放在左侧单独舞台区，右侧再集中放预设和状态切换，这样操作对象更清晰。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr state = app.Label(40, 388, 920, 22, "热键页状态将在这里更新。", DemoTheme.Primary, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            void ApplyHotKeyColors()
            {
                switch (colorMode)
                {
                    case "cool":
                        EmojiWindowNative.SetHotKeyColors(hotKey, DemoTheme.Text, DemoTheme.SurfacePrimary, DemoTheme.Primary);
                        break;
                    case "warm":
                        EmojiWindowNative.SetHotKeyColors(hotKey, DemoTheme.Text, DemoTheme.SurfaceWarning, DemoTheme.Warning);
                        break;
                    default:
                        EmojiWindowNative.SetHotKeyColors(hotKey, DemoTheme.Text, DemoTheme.Background, DemoTheme.BorderLight);
                        break;
                }
            }

            void Refresh(string note)
            {
                EmojiWindowNative.GetHotKey(hotKey, out int vkCode, out int modifiers);
                EmojiWindowNative.GetHotKeyColors(hotKey, out uint fg, out uint bg, out uint border);
                shell.SetLabelText(
                    readout,
                    $"hotkey={PageCommon.FormatHotKey(vkCode, modifiers)}  {(visible ? "显示" : "隐藏")}/{(enabled ? "启用" : "禁用")}\r\n" +
                    $"bounds=({x}, {y}, {width}, {height})\r\n" +
                    $"fg={PageCommon.FormatColor(fg)}  bg={PageCommon.FormatColor(bg)}  border={PageCommon.FormatColor(border)}");
                shell.SetLabelText(state, note);
                shell.SetStatus(note);
            }

            var callback = app.Pin(new EmojiWindowNative.HotKeyCallback((_, vkCode, modifiers) =>
                Refresh("热键回调: " + PageCommon.FormatHotKey(vkCode, modifiers))));
            EmojiWindowNative.SetHotKeyCallback(hotKey, callback);

            app.Label(1044, 56, 220, 22, "热键预设", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Button(1044, 94, 116, 34, "Ctrl+S", "💾", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetHotKey(hotKey, 0x53, 2);
                Refresh("热键已设为 Ctrl+S");
            }, page);
            app.Button(1172, 94, 116, 34, "Ctrl+Shift+P", "📦", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetHotKey(hotKey, 0x50, 3);
                Refresh("热键已设为 Ctrl+Shift+P");
            }, page);
            app.Button(1300, 94, 124, 34, "Alt+F4", "⚠", DemoColors.Orange, () =>
            {
                EmojiWindowNative.SetHotKey(hotKey, 0x73, 4);
                Refresh("热键已设为 Alt+F4");
            }, page);
            app.Button(1044, 138, 116, 34, "清空热键", "🧹", DemoColors.Red, () =>
            {
                EmojiWindowNative.ClearHotKey(hotKey);
                Refresh("热键已清空");
            }, page);
            app.Button(1172, 138, 252, 34, "立即读取", "📡", DemoColors.Gray, () => Refresh("已重新读取当前热键"), page);

            app.Label(1044, 200, 220, 22, "配色与布局", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Button(1044, 236, 116, 34, "冷色方案", "💙", DemoColors.Blue, () =>
            {
                colorMode = "cool";
                ApplyHotKeyColors();
                Refresh("热键控件已切到冷色方案");
            }, page);
            app.Button(1172, 236, 116, 34, "暖色方案", "🧡", DemoColors.Orange, () =>
            {
                colorMode = "warm";
                ApplyHotKeyColors();
                Refresh("热键控件已切到暖色方案");
            }, page);
            app.Button(1300, 236, 124, 34, "恢复主题色", "🎨", DemoColors.Green, () =>
            {
                colorMode = "theme";
                ApplyHotKeyColors();
                Refresh("热键控件已恢复主题配色");
            }, page);
            app.Button(1044, 280, 116, 34, "右移 80", "➡", DemoColors.Green, () =>
            {
                x = 128;
                EmojiWindowNative.SetHotKeyControlBounds(hotKey, x, y, width, height);
                Refresh("热键控件已右移 80");
            }, page);
            app.Button(1172, 280, 116, 34, "加宽 100", "↔", DemoColors.Purple, () =>
            {
                width = 420;
                EmojiWindowNative.SetHotKeyControlBounds(hotKey, x, y, width, height);
                Refresh("热键控件已加宽到 420");
            }, page);

            app.Label(1044, 324, 220, 22, "显示与启用", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Button(1044, 358, 116, 34, "禁用/启用", "🚫", DemoColors.Blue, () =>
            {
                enabled = !enabled;
                EmojiWindowNative.EnableHotKeyControl(hotKey, enabled ? 1 : 0);
                Refresh("热键控件启用状态已切换");
            }, page);
            app.Button(1172, 358, 116, 34, "显示/隐藏", "👁", DemoColors.Gray, () =>
            {
                visible = !visible;
                EmojiWindowNative.ShowHotKeyControl(hotKey, visible ? 1 : 0);
                Refresh("热键控件可见状态已切换");
            }, page);
            app.Button(1300, 358, 124, 34, "恢复默认", "↺", DemoColors.Green, () =>
            {
                x = 48;
                y = 110;
                width = 320;
                height = 38;
                visible = true;
                enabled = true;
                colorMode = "theme";
                EmojiWindowNative.SetHotKeyControlBounds(hotKey, x, y, width, height);
                ApplyHotKeyColors();
                EmojiWindowNative.EnableHotKeyControl(hotKey, 1);
                EmojiWindowNative.ShowHotKeyControl(hotKey, 1);
                EmojiWindowNative.ClearHotKey(hotKey);
                Refresh("热键页已恢复默认状态");
            }, page);

            app.Label(40, 490, 1320, 22, "1. GetHotKey / SetHotKey / ClearHotKey：读取、预设和清空热键。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 524, 1320, 22, "2. SetHotKeyCallback：热键变化会把格式化后的组合键写回页面状态。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 558, 1320, 22, "3. GetHotKeyColors / SetHotKeyColors：读取和切换前景、背景与边框色。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 592, 1320, 22, "4. SetHotKeyControlBounds / EnableHotKeyControl / ShowHotKeyControl：切换布局与状态。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            void ApplyTheme()
            {
                if (colorMode == "theme")
                {
                    ApplyHotKeyColors();
                }

                shell.SetLabelText(stageNote, shell.Palette.Dark
                    ? "深色主题下热键舞台区和操作区仍保持分层，而不是只剩一排按钮。"
                    : "浅色主题下保留“舞台区 + 操作区”的阅读顺序，观感更接近 Python 版。");
            }

            shell.RegisterPageThemeHandler(page, ApplyTheme);
            ApplyTheme();
            Refresh("热键页已整理：舞台区、预设区和状态区已分开。");
        }
    }
}
