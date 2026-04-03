using System;
using System.Runtime.InteropServices;

namespace EmojiWindowDemo
{
    internal static class LabelDemoPage
    {
        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;

            app.GroupBox(16, 16, 980, 520, "🏷️ Label 舞台区 / 实时读数", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(1020, 16, 444, 520, "🛠️ 文本 / 颜色 / 布局 / 状态", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(16, 558, 1448, 230, "📘 Label API 说明", DemoTheme.Border, DemoTheme.Background, page);

            app.Label(40, 56, 920, 24, "这一页直接展示 Label 的文本、颜色、位置、字体、对齐、可见性和启用态读取，结构改成 Python 风格的舞台区。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            app.Label(56, 98, 240, 22, "标签舞台", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            IntPtr demoLabel = app.Label(56, 124, 560, 36, "🏷️ 这是主演示标签：支持 Unicode 彩色文案和属性读取。", DemoTheme.Text, DemoTheme.SurfacePrimary, 15, PageCommon.AlignLeft, false, page);
            IntPtr readout = app.Label(40, 184, 920, 96, "等待读取标签属性。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr stageTip = app.Label(40, 300, 920, 52, "左侧保留一个主演示标签和读数区，右侧按钮全部作用在这一个对象上，阅读路径会比旧版更清晰。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr stateLabel = app.Label(40, 474, 920, 22, "标签页状态将在这里更新。", DemoTheme.Primary, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            string initialText = EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetLabelText, demoLabel);
            EmojiWindowNative.GetLabelBounds(demoLabel, out int initialX, out int initialY, out int initialWidth, out int initialHeight);
            EmojiWindowNative.GetLabelColor(demoLabel, out uint initialFg, out uint initialBg);
            string initialFontName = ReadFontName(demoLabel, out int initialFontSize, out int initialBold, out _, out _);
            string colorMode = "theme";

            void Refresh(string note)
            {
                EmojiWindowNative.GetLabelColor(demoLabel, out uint fg, out uint bg);
                EmojiWindowNative.GetLabelBounds(demoLabel, out int x, out int y, out int width, out int height);
                string fontName = ReadFontName(demoLabel, out int fontSize, out int bold, out _, out _);
                shell.SetLabelText(
                    readout,
                    $"text={EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetLabelText, demoLabel)}  {(EmojiWindowNative.GetLabelVisible(demoLabel) == 1 ? "显示" : "隐藏")}/{(EmojiWindowNative.GetLabelEnabled(demoLabel) == 1 ? "启用" : "禁用")}\r\n" +
                    $"bounds=({x}, {y}, {width}, {height})  align={PageCommon.AlignmentName(EmojiWindowNative.GetLabelAlignment(demoLabel))}  font={(string.IsNullOrEmpty(fontName) ? "default" : fontName)} {fontSize}px bold={bold}\r\n" +
                    $"fg={PageCommon.FormatColor(fg)}  bg={PageCommon.FormatColor(bg)}");
                shell.SetLabelText(stateLabel, note);
                shell.SetStatus(note);
            }

            void SetTextValue(string text, string note)
            {
                byte[] bytes = app.U(text);
                EmojiWindowNative.SetLabelText(demoLabel, bytes, bytes.Length);
                Refresh(note);
            }

            void ApplyLabelColors()
            {
                switch (colorMode)
                {
                    case "cool":
                        EmojiWindowNative.SetLabelColor(demoLabel, DemoTheme.Primary, DemoTheme.SurfacePrimary);
                        break;
                    case "warm":
                        EmojiWindowNative.SetLabelColor(demoLabel, DemoTheme.Warning, DemoTheme.SurfaceWarning);
                        break;
                    default:
                        EmojiWindowNative.SetLabelColor(demoLabel, DemoTheme.Text, DemoTheme.SurfacePrimary);
                        break;
                }
            }

            void SetFont(string fontName, int fontSize, bool bold, string note)
            {
                byte[] bytes = app.U(fontName);
                EmojiWindowNative.SetLabelFont(demoLabel, bytes, bytes.Length, fontSize, bold ? 1 : 0, 0, 0);
                Refresh(note);
            }

            void MoveLabel(int dx = 0, int dy = 0, int dw = 0)
            {
                EmojiWindowNative.GetLabelBounds(demoLabel, out int x, out int y, out int width, out int height);
                EmojiWindowNative.SetLabelBounds(demoLabel, x + dx, y + dy, width + dw, height);
                Refresh($"标签位置/尺寸已更新: dx={dx}, dy={dy}, dw={dw}");
            }

            void Restore()
            {
                byte[] textBytes = app.U(initialText);
                byte[] fontBytes = app.U(initialFontName);
                EmojiWindowNative.SetLabelText(demoLabel, textBytes, textBytes.Length);
                EmojiWindowNative.SetLabelColor(demoLabel, initialFg, initialBg);
                EmojiWindowNative.SetLabelBounds(demoLabel, initialX, initialY, initialWidth, initialHeight);
                EmojiWindowNative.SetLabelFont(demoLabel, fontBytes, fontBytes.Length, initialFontSize, initialBold, 0, 0);
                EmojiWindowNative.EnableLabel(demoLabel, 1);
                EmojiWindowNative.ShowLabel(demoLabel, 1);
                colorMode = "theme";
                Refresh("标签属性已恢复默认");
            }

            app.Label(1044, 56, 220, 22, "文本预设", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Button(1044, 94, 116, 34, "说明标签", "💬", DemoColors.Blue, () => SetTextValue("💬 当前标签已切到说明文案模式。", "标签文本已切到说明模式"), page);
            app.Button(1172, 94, 116, 34, "强调标签", "📣", DemoColors.Green, () => SetTextValue("📣 当前标签是强调提示，用于展示高关注状态。", "标签文本已切到强调模式"), page);
            app.Button(1300, 94, 124, 34, "彩色标签", "🌈", DemoColors.Purple, () => SetTextValue("🌈 Unicode 标签：🚀 ✅ 📘 🧩", "标签文本已切到 Unicode 彩色模式"), page);

            app.Label(1044, 148, 220, 22, "颜色与字体", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Button(1044, 182, 116, 34, "冷色", "💙", DemoColors.Blue, () =>
            {
                colorMode = "cool";
                ApplyLabelColors();
                Refresh("标签已切到冷色方案");
            }, page);
            app.Button(1172, 182, 116, 34, "暖色", "🧡", DemoColors.Orange, () =>
            {
                colorMode = "warm";
                ApplyLabelColors();
                Refresh("标签已切到暖色方案");
            }, page);
            app.Button(1300, 182, 124, 34, "18px Bold", "🔤", DemoColors.Green, () => SetFont("Segoe UI Emoji", 18, true, "标签字体已切到 18px Bold"), page);
            app.Button(1044, 226, 116, 34, "14px", "🔡", DemoColors.Gray, () => SetFont("Segoe UI Emoji", 14, false, "标签字体已切到 14px"), page);

            app.Label(1044, 280, 220, 22, "布局与状态", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Button(1044, 314, 116, 34, "右移 80", "➡", DemoColors.Blue, () => MoveLabel(dx: 80), page);
            app.Button(1172, 314, 116, 34, "下移 20", "⬇", DemoColors.Green, () => MoveLabel(dy: 20), page);
            app.Button(1300, 314, 124, 34, "加宽 120", "↔", DemoColors.Orange, () => MoveLabel(dw: 120), page);
            app.Button(1044, 358, 116, 34, "禁用/启用", "🚫", DemoColors.Purple, () =>
            {
                EmojiWindowNative.EnableLabel(demoLabel, EmojiWindowNative.GetLabelEnabled(demoLabel) == 1 ? 0 : 1);
                Refresh("标签启用状态已切换");
            }, page);
            app.Button(1172, 358, 116, 34, "显示/隐藏", "👁", DemoColors.Gray, () =>
            {
                EmojiWindowNative.ShowLabel(demoLabel, EmojiWindowNative.GetLabelVisible(demoLabel) == 1 ? 0 : 1);
                Refresh("标签可见状态已切换");
            }, page);
            app.Button(1300, 358, 124, 34, "恢复默认", "↺", DemoColors.Blue, Restore, page);
            app.Label(1044, 410, 382, 56, "当前 DLL 对 Label 提供了对齐方式读取接口 GetLabelAlignment，但没有 SetLabelAlignment 真接口，所以这里只做“可读不伪造可写”。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);

            app.Label(40, 598, 1320, 24, "1. GetLabelText / SetLabelText：读取和修改标签文本。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 632, 1320, 24, "2. GetLabelColor / SetLabelColor：读取和切换前景色 / 背景色。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 666, 1320, 24, "3. GetLabelBounds / SetLabelBounds：直接修改标签位置和宽度。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 700, 1320, 24, "4. GetLabelFont / SetLabelFont：这里用真实字体读写展示字体名、字号和粗体。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 734, 1320, 24, "5. EnableLabel / ShowLabel：演示启用态和可见态切换。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            void ApplyTheme()
            {
                if (colorMode == "theme")
                {
                    ApplyLabelColors();
                }

                shell.SetLabelText(stageTip, shell.Palette.Dark
                    ? "深色主题下也保留舞台区与读数区，不再只是浅底标签直接堆在页面上。"
                    : "浅色主题下舞台区和读数区的分层会更接近 Python 版的观感。");
            }

            shell.RegisterPageThemeHandler(page, ApplyTheme);
            ApplyTheme();
            Refresh("标签页已重排，可直接测试标签属性读取与设置。");
        }

        private static string ReadFontName(IntPtr hLabel, out int fontSize, out int bold, out int italic, out int underline)
        {
            int nameLength = EmojiWindowNative.GetLabelFont(hLabel, IntPtr.Zero, 0, out fontSize, out bold, out italic, out underline);
            if (nameLength <= 0)
            {
                return string.Empty;
            }

            IntPtr buffer = Marshal.AllocHGlobal(nameLength);
            try
            {
                EmojiWindowNative.GetLabelFont(hLabel, buffer, nameLength, out fontSize, out bold, out italic, out underline);
                byte[] bytes = new byte[nameLength];
                Marshal.Copy(buffer, bytes, 0, nameLength);
                return EmojiWindowNative.FromUtf8(bytes);
            }
            finally
            {
                Marshal.FreeHGlobal(buffer);
            }
        }
    }
}
