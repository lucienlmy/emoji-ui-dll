using System;

namespace EmojiWindowDemo
{
    internal static class WindowDemoPage
    {
        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;

            app.GroupBox(16, 16, 984, 246, "🪟 EmojiWindow 实时属性读取", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(16, 282, 984, 258, "✏️ 标题 / 尺寸 / 位置快捷设置", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(1024, 16, 440, 524, "🎨 主题 / 标题栏 / 背景色", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(16, 558, 1448, 230, "📘 Window API 说明", DemoTheme.Border, DemoTheme.Background, page);

            IntPtr introA = app.Label(40, 56, 860, 24, "窗口页直接读取主窗口实时属性，不再只放一个按钮演示。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            IntPtr introB = app.Label(40, 90, 930, 24, "这里覆盖标题、句柄、位置尺寸、可见态、标题栏背景、标题栏文字和客户区背景。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            IntPtr readout = app.Label(40, 132, 920, 110, "等待读取窗口属性。", DemoTheme.Text, DemoTheme.Background, 13, PageCommon.AlignLeft, true, page);
            IntPtr state = app.Label(40, 760, 1360, 22, "窗口页状态将在这里更新。", DemoTheme.Primary, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            app.Label(40, 324, 180, 22, "📝 标题预设", DemoTheme.Text, DemoTheme.Background, 15, PageCommon.AlignLeft, false, page);
            app.Label(40, 414, 180, 22, "📐 尺寸预设", DemoTheme.Text, DemoTheme.Background, 15, PageCommon.AlignLeft, false, page);
            app.Label(640, 324, 180, 22, "📍 位置调整", DemoTheme.Text, DemoTheme.Background, 15, PageCommon.AlignLeft, false, page);

            app.Label(1048, 56, 180, 22, "☀️ / 🌙 主题切换", DemoTheme.Text, DemoTheme.Background, 15, PageCommon.AlignLeft, false, page);
            app.Label(1048, 144, 180, 22, "🎨 标题栏背景色", DemoTheme.Text, DemoTheme.Background, 15, PageCommon.AlignLeft, false, page);
            app.Label(1048, 232, 220, 22, "🔠 标题栏文字色", DemoTheme.Text, DemoTheme.Background, 15, PageCommon.AlignLeft, false, page);
            IntPtr titlebarHint = app.Label(1048, 312, 300, 20, "0 = 跟随当前主题自动对比。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(1048, 348, 180, 22, "🧱 客户区背景", DemoTheme.Text, DemoTheme.Background, 15, PageCommon.AlignLeft, false, page);

            bool followThemeBackground = true;
            uint clientBg = shell.Palette.PageBackground;
            string clientBgName = "主题默认背景";

            void Refresh(string note)
            {
                EmojiWindowNative.GetWindowBounds(app.Window, out int x, out int y, out int width, out int height);
                string title = EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetWindowTitle, app.Window);
                string visible = EmojiWindowNative.GetWindowVisible(app.Window) == 1 ? "显示" : "隐藏";
                uint titlebar = EmojiWindowNative.GetWindowTitlebarColor(app.Window);
                uint titlebarText = EmojiWindowNative.GetTitleBarTextColor(app.Window);

                shell.SetLabelText(
                    readout,
                    $"标题: {title}\r\n" +
                    $"句柄: 0x{app.Window.ToInt64():X}  可见状态: {visible}\r\n" +
                    $"位置尺寸: x={x}, y={y}, w={width}, h={height}\r\n" +
                    $"标题栏背景: {PageCommon.FormatColor(titlebar)}  标题栏文字: {PageCommon.FormatColor(titlebarText)}\r\n" +
                    $"最近一次客户区背景: {clientBgName} / {PageCommon.FormatColor(clientBg)}");
                shell.SetLabelText(state, note);
                shell.SetStatus(note);
            }

            void SyncThemeBackground()
            {
                if (!followThemeBackground)
                {
                    return;
                }

                clientBg = shell.Palette.PageBackground;
                clientBgName = "主题默认背景";
                EmojiWindowNative.SetWindowBackgroundColor(app.Window, clientBg);
            }

            void SetWindowBounds(int x, int y, int width, int height, string note)
            {
                EmojiWindowNative.SetWindowBounds(app.Window, x, y, width, height);
                shell.ResizeShell(width, height);
                Refresh(note);
            }

            void SetClientBackground(uint color, string name, string note, bool followTheme = false)
            {
                followThemeBackground = followTheme;
                clientBg = color;
                clientBgName = name;
                EmojiWindowNative.SetWindowBackgroundColor(app.Window, color);
                Refresh(note);
            }

            void ApplyWindowTheme()
            {
                SyncThemeBackground();
                shell.SetLabelText(titlebarHint, shell.Palette.Dark
                    ? "深色主题下，0 会自动切回更易读的标题栏文字对比。"
                    : "浅色主题下，0 会让标题栏文字颜色跟随当前主题自动对比。");
                if (followThemeBackground)
                {
                    Refresh("窗口页已同步当前主题");
                }
            }

            app.Button(40, 360, 146, 36, "产品标题", "🪟", DemoColors.Blue, () =>
            {
                byte[] title = app.U("🪟 Tree AllDemo Enhanced / 产品演示窗口");
                EmojiWindowNative.set_window_title(app.Window, title, title.Length);
                Refresh("窗口标题已切到产品演示风格");
            }, page);
            app.Button(202, 360, 146, 36, "调试标题", "🧪", DemoColors.Green, () =>
            {
                byte[] title = app.U("🧪 EmojiWindow Debug Surface / 属性回归中");
                EmojiWindowNative.set_window_title(app.Window, title, title.Length);
                Refresh("窗口标题已切到调试风格");
            }, page);
            app.Button(364, 360, 146, 36, "彩色标题", "✅", DemoColors.Purple, () =>
            {
                byte[] title = app.U("✅ EmojiWindow 属性页 / 🎨 Unicode 彩色标题");
                EmojiWindowNative.set_window_title(app.Window, title, title.Length);
                Refresh("窗口标题已切到彩色 Unicode 方案");
            }, page);

            app.Button(40, 450, 176, 36, "紧凑 1600x900", "📏", DemoColors.Orange, () =>
            {
                EmojiWindowNative.GetWindowBounds(app.Window, out int x, out int y, out _, out _);
                SetWindowBounds(x, y, 1600, 900, "窗口尺寸已切到紧凑演示 1600x900");
            }, page);
            app.Button(232, 450, 176, 36, "标准 1820x980", "🪄", DemoColors.Blue, () =>
            {
                EmojiWindowNative.GetWindowBounds(app.Window, out int x, out int y, out _, out _);
                SetWindowBounds(x, y, 1820, 980, "窗口尺寸已恢复到标准 1820x980");
            }, page);
            app.Button(424, 450, 176, 36, "加宽 1920x1040", "🧱", DemoColors.Green, () =>
            {
                EmojiWindowNative.GetWindowBounds(app.Window, out int x, out int y, out _, out _);
                SetWindowBounds(x, y, 1920, 1040, "窗口尺寸已切到加宽展示 1920x1040");
            }, page);

            app.Button(640, 360, 156, 36, "恢复到 40,40", "↖️", DemoColors.Gray, () =>
            {
                EmojiWindowNative.GetWindowBounds(app.Window, out _, out _, out int width, out int height);
                SetWindowBounds(40, 40, width, height, "窗口位置已恢复到 (40, 40)");
            }, page);
            app.Button(812, 360, 156, 36, "向右移动 80", "➡️", DemoColors.Blue, () =>
            {
                EmojiWindowNative.GetWindowBounds(app.Window, out int x, out int y, out int width, out int height);
                SetWindowBounds(x + 80, y, width, height, "窗口已向右移动 80 像素");
            }, page);
            app.Button(640, 406, 156, 36, "向下移动 60", "⬇️", DemoColors.Green, () =>
            {
                EmojiWindowNative.GetWindowBounds(app.Window, out int x, out int y, out int width, out int height);
                SetWindowBounds(x, y + 60, width, height, "窗口已向下移动 60 像素");
            }, page);
            app.Button(812, 406, 156, 36, "立即读取", "📋", DemoColors.Purple, () => Refresh("已重新读取窗口当前属性"), page);

            app.Button(1048, 90, 176, 36, "浅色主题", "☀️", DemoColors.Blue, () =>
            {
                shell.SetDarkTheme(false);
                SyncThemeBackground();
                Refresh("主窗口主题已切到浅色");
            }, page);
            app.Button(1240, 90, 176, 36, "深色主题", "🌙", DemoColors.Black, () =>
            {
                shell.SetDarkTheme(true);
                SyncThemeBackground();
                Refresh("主窗口主题已切到深色");
            }, page);

            app.Button(1048, 178, 112, 36, "科技蓝", "🧊", DemoColors.Blue, () =>
            {
                EmojiWindowNative.set_window_titlebar_color(app.Window, DemoColors.Blue);
                Refresh("标题栏背景已切到科技蓝");
            }, page);
            app.Button(1174, 178, 112, 36, "深空黑", "🌑", DemoColors.Black, () =>
            {
                EmojiWindowNative.set_window_titlebar_color(app.Window, EmojiWindowNative.ARGB(255, 43, 47, 54));
                Refresh("标题栏背景已切到深空黑");
            }, page);
            app.Button(1300, 178, 112, 36, "青绿色", "🟢", DemoColors.Green, () =>
            {
                EmojiWindowNative.set_window_titlebar_color(app.Window, EmojiWindowNative.ARGB(255, 39, 174, 96));
                Refresh("标题栏背景已切到青绿色");
            }, page);

            app.Button(1048, 266, 86, 36, "亮字", "🔆", DemoColors.Gray, () =>
            {
                EmojiWindowNative.SetTitleBarTextColor(app.Window, DemoColors.White);
                Refresh("标题栏文字已切到亮色");
            }, page);
            app.Button(1142, 266, 86, 36, "暗字", "🌑", DemoColors.Black, () =>
            {
                EmojiWindowNative.SetTitleBarTextColor(app.Window, EmojiWindowNative.ARGB(255, 29, 30, 31));
                Refresh("标题栏文字已切到暗色");
            }, page);
            app.Button(1236, 266, 86, 36, "蓝字", "🔵", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetTitleBarTextColor(app.Window, EmojiWindowNative.ARGB(255, 140, 197, 255));
                Refresh("标题栏文字已切到蓝色");
            }, page);
            app.Button(1330, 266, 86, 36, "跟随", "↺", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetTitleBarTextColor(app.Window, 0);
                Refresh("标题栏文字已恢复跟随主题");
            }, page);

            app.Button(1048, 382, 112, 36, "纯白背景", "🤍", DemoColors.Green, () => SetClientBackground(DemoColors.White, "纯白", "客户区背景已切到纯白"), page);
            app.Button(1174, 382, 112, 36, "主题背景", "🪟", DemoColors.Gray, () => SetClientBackground(shell.Palette.PageBackground, "主题默认背景", "客户区背景已切回主题背景", true), page);
            app.Button(1300, 382, 112, 36, "深色背景", "🌚", DemoColors.Black, () => SetClientBackground(EmojiWindowNative.ARGB(255, 31, 35, 41), "深色", "客户区背景已切到深色演示底色"), page);

            app.Label(40, 598, 640, 24, "1. GetWindowTitle / set_window_title：读取和修改主窗口标题。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 632, 700, 24, "2. GetWindowBounds / SetWindowBounds：直接读取和修改窗口位置与尺寸。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 666, 660, 24, "3. GetWindowVisible：读取当前可见状态，这里用实时面板展示。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 700, 720, 24, "4. set_window_titlebar_color / GetWindowTitlebarColor：标题栏背景色读写。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(760, 632, 660, 24, "5. SetTitleBarTextColor / GetTitleBarTextColor：标题栏文字颜色读取与设置。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(760, 666, 660, 24, "6. SetWindowBackgroundColor / SetDarkMode：客户区底色和主题切换联动演示。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(760, 700, 620, 48, "7. 这一页保留 Unicode 彩色按钮和标题，用来验证窗口级主题切换不会影响 emoji 显示。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);

            shell.RegisterPageThemeHandler(page, ApplyWindowTheme);
            ApplyWindowTheme();
            Refresh("窗口页已加载，可直接测试窗口属性读取与设置");
        }
    }
}
