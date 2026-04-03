using System;

namespace EmojiWindowDemo
{
    internal static class ButtonDemoPage
    {
        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;

            app.GroupBox(16, 16, 980, 520, "🔘 Button 舞台区 / 实时读数", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(1020, 16, 444, 520, "🛠️ 文本 / 配色 / 布局 / 状态", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(16, 558, 1448, 220, "📘 Button API 说明", DemoTheme.Border, DemoTheme.Background, page);

            app.Label(40, 56, 920, 24, "这一页保留一个主演示按钮，把属性读取、布局移动和状态切换集中展示，页面分区对齐 Python 版。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            app.Label(56, 98, 240, 22, "按钮舞台", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            int demoButton = 0;
            IntPtr readout = IntPtr.Zero;
            IntPtr stateLabel = IntPtr.Zero;
            demoButton = app.Button(56, 122, 216, 44, "主操作按钮", "🚀", DemoColors.Blue, () => Refresh("主演示按钮被点击"), page);
            IntPtr stageTip = app.Label(56, 176, 560, 22, "右侧所有操作都会直接作用在这颗按钮上，读数区会同步刷新。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);

            readout = app.Label(40, 238, 920, 136, "等待读取按钮属性。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr summary = app.Label(40, 396, 920, 58, "建议把“舞台按钮”和“读数区”放在同一块区域里，用户能立刻理解右侧按钮操作的对象是谁。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            stateLabel = app.Label(40, 474, 920, 22, "按钮页状态将在这里更新。", DemoTheme.Primary, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            string initialText = EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetButtonText, demoButton);
            string initialEmoji = EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetButtonEmoji, demoButton);
            EmojiWindowNative.GetButtonBounds(demoButton, out int initialX, out int initialY, out int initialWidth, out int initialHeight);
            uint initialBg = EmojiWindowNative.GetButtonBackgroundColor(demoButton);
            int initialType = EmojiWindowNative.GetButtonType(demoButton);
            int initialStyle = EmojiWindowNative.GetButtonStyle(demoButton);
            int initialSize = EmojiWindowNative.GetButtonSize(demoButton);
            int initialRound = EmojiWindowNative.GetButtonRound(demoButton);
            int initialCircle = EmojiWindowNative.GetButtonCircle(demoButton);
            int initialLoading = EmojiWindowNative.GetButtonLoading(demoButton);

            void Refresh(string note)
            {
                string text = EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetButtonText, demoButton);
                string emoji = EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetButtonEmoji, demoButton);
                EmojiWindowNative.GetButtonBounds(demoButton, out int x, out int y, out int width, out int height);
                uint bg = EmojiWindowNative.GetButtonBackgroundColor(demoButton);
                uint fg = EmojiWindowNative.GetButtonTextColor(demoButton);
                uint border = EmojiWindowNative.GetButtonBorderColor(demoButton);
                string visible = EmojiWindowNative.GetButtonVisible(demoButton) != 0 ? "显示" : "隐藏";
                string enabled = EmojiWindowNative.GetButtonEnabled(demoButton) != 0 ? "启用" : "禁用";

                shell.SetLabelText(
                    readout,
                    $"text={text}    emoji={emoji}    {visible}/{enabled}\r\n" +
                    $"bounds=({x}, {y}, {width}, {height})  type={ButtonTypeName(EmojiWindowNative.GetButtonType(demoButton))}  style={ButtonStyleName(EmojiWindowNative.GetButtonStyle(demoButton))}  size={ButtonSizeName(EmojiWindowNative.GetButtonSize(demoButton))}  round={EmojiWindowNative.GetButtonRound(demoButton)}  circle={EmojiWindowNative.GetButtonCircle(demoButton)}  loading={EmojiWindowNative.GetButtonLoading(demoButton)}\r\n" +
                    $"bg={PageCommon.FormatColor(bg)}  fg={PageCommon.FormatColor(fg)}  border={PageCommon.FormatColor(border)}");
                shell.SetLabelText(stateLabel, note);
                shell.SetStatus(note);
            }

            void SetButtonTextValue(string text, string note)
            {
                byte[] bytes = app.U(text);
                EmojiWindowNative.SetButtonText(demoButton, bytes, bytes.Length);
                Refresh(note);
            }

            void SetButtonEmojiValue(string emoji, string note)
            {
                byte[] bytes = app.U(emoji);
                EmojiWindowNative.SetButtonEmoji(demoButton, bytes, bytes.Length);
                Refresh(note);
            }

            void SetButtonColors(uint bg, uint fg, uint border, string note)
            {
                EmojiWindowNative.SetButtonBackgroundColor(demoButton, bg);
                EmojiWindowNative.SetButtonTextColor(demoButton, fg);
                EmojiWindowNative.SetButtonBorderColor(demoButton, border);
                EmojiWindowNative.SetButtonHoverColors(demoButton, bg, border, fg);
                Refresh(note);
            }

            void MoveButton(int dx = 0, int dy = 0, int dw = 0)
            {
                EmojiWindowNative.GetButtonBounds(demoButton, out int x, out int y, out int width, out int height);
                EmojiWindowNative.SetButtonBounds(demoButton, x + dx, y + dy, width + dw, height);
                Refresh($"按钮位置/尺寸已更新: dx={dx}, dy={dy}, dw={dw}");
            }

            void RestoreButton()
            {
                byte[] textBytes = app.U(initialText);
                byte[] emojiBytes = app.U(initialEmoji);
                EmojiWindowNative.SetButtonText(demoButton, textBytes, textBytes.Length);
                EmojiWindowNative.SetButtonEmoji(demoButton, emojiBytes, emojiBytes.Length);
                EmojiWindowNative.SetButtonBounds(demoButton, initialX, initialY, initialWidth, initialHeight);
                EmojiWindowNative.SetButtonBackgroundColor(demoButton, initialBg);
                EmojiWindowNative.ResetButtonColorOverrides(demoButton);
                EmojiWindowNative.SetButtonType(demoButton, initialType);
                EmojiWindowNative.SetButtonStyle(demoButton, initialStyle);
                EmojiWindowNative.SetButtonSize(demoButton, initialSize);
                EmojiWindowNative.SetButtonRound(demoButton, initialRound);
                EmojiWindowNative.SetButtonCircle(demoButton, initialCircle);
                EmojiWindowNative.SetButtonLoading(demoButton, initialLoading);
                EmojiWindowNative.ShowButton(demoButton, 1);
                EmojiWindowNative.EnableButton(page, demoButton, 1);
                Refresh("按钮属性已恢复默认");
            }

            app.Label(1044, 56, 220, 22, "文案与 Emoji", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Label(1044, 80, 360, 36, "先改按钮文案，再看左侧读数区如何同步出文本、emoji 和类型信息。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            app.Button(1044, 126, 116, 34, "保存草稿", "📝", DemoColors.Blue, () => SetButtonTextValue("保存草稿", "按钮文本已改成“保存草稿”"), page);
            app.Button(1172, 126, 116, 34, "立即发布", "✅", DemoColors.Green, () => SetButtonTextValue("立即发布", "按钮文本已改成“立即发布”"), page);
            app.Button(1300, 126, 124, 34, "切换 Emoji", "🎯", DemoColors.Purple, () => SetButtonEmojiValue("🎯", "按钮 emoji 已切到 🎯"), page);

            app.Label(1044, 184, 220, 22, "布局与尺寸", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Button(1044, 214, 116, 34, "右移 80", "➡", DemoColors.Orange, () => MoveButton(dx: 80), page);
            app.Button(1172, 214, 116, 34, "下移 24", "⬇", DemoColors.Blue, () => MoveButton(dy: 24), page);
            app.Button(1300, 214, 124, 34, "加宽 60", "↔", DemoColors.Green, () => MoveButton(dw: 60), page);

            app.Label(1044, 272, 220, 22, "配色与样式", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Button(1044, 302, 116, 34, "冷色", "💙", DemoColors.Blue, () => SetButtonColors(DemoTheme.Primary, DemoTheme.Surface, DemoTheme.Primary, "按钮已切到冷色方案"), page);
            app.Button(1172, 302, 116, 34, "暖色", "🧡", DemoColors.Orange, () => SetButtonColors(DemoTheme.Warning, DemoTheme.Surface, DemoTheme.Warning, "按钮已切到暖色方案"), page);
            app.Button(1300, 302, 124, 34, "浅灰", "🌫", DemoColors.Gray, () => SetButtonColors(DemoTheme.Surface, DemoTheme.Muted, DemoTheme.BorderLight, "按钮已切到浅灰方案"), page);
            app.Button(1044, 346, 116, 34, "Plain", "🫧", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetButtonStyle(demoButton, PageCommon.ButtonStylePlain);
                Refresh("按钮样式已切到 plain");
            }, page);
            app.Button(1172, 346, 116, 34, "Link", "🔗", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetButtonStyle(demoButton, PageCommon.ButtonStyleLink);
                Refresh("按钮样式已切到 link");
            }, page);
            app.Button(1300, 346, 124, 34, "Solid", "🧱", DemoColors.Gray, () =>
            {
                EmojiWindowNative.SetButtonStyle(demoButton, PageCommon.ButtonStyleSolid);
                Refresh("按钮样式已切回 solid");
            }, page);

            app.Label(1044, 404, 220, 22, "状态与行为", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Button(1044, 434, 116, 34, "Round", "⭕", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetButtonRound(demoButton, 1);
                EmojiWindowNative.SetButtonCircle(demoButton, 0);
                Refresh("按钮已切到 round");
            }, page);
            app.Button(1172, 434, 116, 34, "Circle", "⚪", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetButtonCircle(demoButton, 1);
                Refresh("按钮已切到 circle");
            }, page);
            app.Button(1300, 434, 124, 34, "Loading", "⏳", DemoColors.Purple, () =>
            {
                EmojiWindowNative.SetButtonLoading(demoButton, EmojiWindowNative.GetButtonLoading(demoButton) == 0 ? 1 : 0);
                Refresh("按钮 loading 状态已切换");
            }, page);
            app.Button(1044, 478, 116, 34, "禁用/启用", "🚫", DemoColors.Orange, () =>
            {
                EmojiWindowNative.EnableButton(page, demoButton, EmojiWindowNative.GetButtonEnabled(demoButton) == 0 ? 1 : 0);
                Refresh("按钮启用状态已切换");
            }, page);
            app.Button(1172, 478, 116, 34, "显示/隐藏", "👁", DemoColors.Gray, () =>
            {
                EmojiWindowNative.ShowButton(demoButton, EmojiWindowNative.GetButtonVisible(demoButton) == 0 ? 1 : 0);
                Refresh("按钮可见状态已切换");
            }, page);
            app.Button(1300, 478, 124, 34, "恢复默认", "↩", DemoColors.Green, RestoreButton, page);

            app.Label(40, 598, 1320, 24, "1. GetButtonText / GetButtonEmoji / GetButtonBounds：读取文本、emoji 和位置尺寸。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 632, 1320, 24, "2. SetButtonText / SetButtonEmoji / SetButtonBounds：直接修改按钮文案与布局。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 666, 1320, 24, "3. GetButtonBackgroundColor / GetButtonTextColor / GetButtonBorderColor：读取按钮三类颜色。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 700, 1320, 24, "4. SetButtonStyle / SetButtonSize / SetButtonRound / SetButtonCircle / SetButtonLoading：切换样式、尺寸和行为状态。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 734, 1320, 24, "5. ShowButton / EnableButton：这里展示的是真实状态切换，不是静态标签说明。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            void ApplyTheme()
            {
                shell.SetLabelText(stageTip, shell.Palette.Dark
                    ? "深色主题下仍然保留“舞台区 + 读数区 + 操作区”的层次。"
                    : "浅色主题下舞台区和说明区保持清晰分层。");
                shell.SetLabelText(summary, shell.Palette.Dark
                    ? "深色主题不只是换底色，舞台区和操作区的阅读顺序也要稳定。"
                    : "浅色主题下保持舞台区、读数区和操作区的结构，对照 Python 版会更接近。");
            }

            shell.RegisterPageThemeHandler(page, ApplyTheme);
            ApplyTheme();
            Refresh("Button 页面已重排，可直接测试文案、布局、配色和状态切换。");
        }

        private static string ButtonTypeName(int type)
        {
            switch (type)
            {
                case 0: return "default";
                case 1: return "primary";
                case 2: return "success";
                case 3: return "warning";
                case 4: return "danger";
                case 5: return "info";
                default: return "unknown";
            }
        }

        private static string ButtonStyleName(int style)
        {
            switch (style)
            {
                case PageCommon.ButtonStyleSolid: return "solid";
                case PageCommon.ButtonStylePlain: return "plain";
                case PageCommon.ButtonStyleText: return "text";
                case PageCommon.ButtonStyleLink: return "link";
                default: return "unknown";
            }
        }

        private static string ButtonSizeName(int size)
        {
            switch (size)
            {
                case PageCommon.ButtonSizeLarge: return "large";
                case PageCommon.ButtonSizeDefault: return "default";
                case PageCommon.ButtonSizeSmall: return "small";
                default: return "unknown";
            }
        }
    }
}
