using System;

namespace EmojiWindowDemo
{
    internal static class TooltipDemoPage
    {
        private const int PopupTop = 0;
        private const int PopupBottom = 1;
        private const int PopupLeft = 2;
        private const int PopupRight = 3;
        private const int ThemeDark = 1;
        private const int ThemeLight = 2;
        private const int ThemeCustom = 3;
        private const int TriggerHover = 0;
        private const int TriggerClick = 1;

        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;

            app.GroupBox(16, 16, 980, 520, "💬 Tooltip 目标舞台", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(1020, 16, 444, 252, "🪄 手动触发 / 隐藏", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(1020, 284, 444, 252, "📋 Tooltip 读数区", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(16, 558, 1448, 220, "📘 Tooltip API 说明", DemoTheme.Border, DemoTheme.Background, page);

            app.Label(
                40,
                56,
                920,
                42,
                "Tooltip 支持上 / 下 / 左 / 右四个方向，dark / light / custom 主题，以及 hover / click 两种触发方式。",
                DemoTheme.Muted,
                DemoTheme.Background,
                12,
                PageCommon.AlignLeft,
                true,
                page);
            IntPtr stageHint = app.Label(
                40,
                98,
                920,
                38,
                "四个目标现在都做成了带语义色的轻卡片，点击右侧按钮时也会同步写回当前操作。",
                DemoTheme.Muted,
                DemoTheme.Background,
                12,
                PageCommon.AlignLeft,
                true,
                page);

            IntPtr topTarget = app.Label(56, 166, 392, 72, "🟦 Top / Dark / Hover", DemoTheme.Primary, DemoTheme.SurfacePrimary, 14, PageCommon.AlignCenter, false, page);
            IntPtr bottomTarget = app.Label(516, 166, 392, 72, "🟩 Bottom / Light / Hover", DemoTheme.Success, DemoTheme.SurfaceSuccess, 14, PageCommon.AlignCenter, false, page);
            IntPtr leftTarget = app.Label(56, 274, 392, 72, "🟨 Left / Custom / Hover", DemoTheme.Warning, DemoTheme.SurfaceWarning, 14, PageCommon.AlignCenter, false, page);
            IntPtr rightTarget = app.Label(516, 274, 392, 72, "🟪 Right / Dark / Click", DemoTheme.Text, DemoTheme.Surface, 14, PageCommon.AlignCenter, false, page);
            app.Label(56, 386, 240, 22, "🧭 使用建议", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            IntPtr stageTip = app.Label(
                56,
                418,
                860,
                68,
                "Top / Bottom / Left 默认走 hover；Right 走 click。右侧按钮用于手动验证显示与隐藏，而不是替代实际交互。",
                DemoTheme.Muted,
                DemoTheme.Background,
                12,
                PageCommon.AlignLeft,
                true,
                page);

            IntPtr stateLabel = app.Label(1044, 324, 396, 24, "Tooltip 页状态将在这里更新。", DemoTheme.Primary, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            IntPtr detailLabel = app.Label(
                1044,
                360,
                396,
                112,
                "读数区会记录当前展示的是哪个目标、用了什么方向和触发方式。",
                DemoTheme.Text,
                DemoTheme.Background,
                12,
                PageCommon.AlignLeft,
                true,
                page);
            IntPtr readoutHint = app.Label(
                1044,
                484,
                396,
                28,
                "可直接悬停目标，也可用右侧按钮手动触发。",
                DemoTheme.Muted,
                DemoTheme.Background,
                12,
                PageCommon.AlignLeft,
                true,
                page);

            byte[] font = app.U("Microsoft YaHei UI");
            IntPtr topTooltip = CreateTooltip(app, page, "🖱️ Hover Top\ndark 主题 / 上方", PopupTop, ThemeDark, TriggerHover, DemoColors.Black, DemoColors.White, DemoColors.Border, font);
            IntPtr bottomTooltip = CreateTooltip(app, page, "🖱️ Hover Bottom\nlight 主题 / 下方", PopupBottom, ThemeLight, TriggerHover, DemoColors.White, DemoColors.Black, DemoColors.Border, font);
            IntPtr leftTooltip = CreateTooltip(app, page, "🖱️ Hover Left\ncustom 主题 / 左侧", PopupLeft, ThemeCustom, TriggerHover, DemoColors.Yellow, EmojiWindowNative.ARGB(255, 140, 74, 0), DemoColors.Orange, font);
            IntPtr rightTooltip = CreateTooltip(app, page, "🖱️ Click / Right / Dark\n点击目标显示，再点一次收起。", PopupRight, ThemeDark, TriggerClick, DemoColors.Black, DemoColors.White, DemoColors.Border, font);

            EmojiWindowNative.BindTooltipToControl(topTooltip, topTarget);
            EmojiWindowNative.BindTooltipToControl(bottomTooltip, bottomTarget);
            EmojiWindowNative.BindTooltipToControl(leftTooltip, leftTarget);
            EmojiWindowNative.BindTooltipToControl(rightTooltip, rightTarget);

            string currentTarget = "等待操作";
            string currentMode = "Hover / Click 尚未触发";

            void Refresh(string note)
            {
                shell.SetLabelText(stateLabel, note);
                shell.SetLabelText(
                    detailLabel,
                    $"当前目标：{currentTarget}\r\n" +
                    $"触发方式：{currentMode}\r\n" +
                    "这里强调的是 Tooltip 与目标控件的绑定关系，而不是单独展示几个 API。");
                shell.SetStatus(note);
            }

            void ShowTip(IntPtr tooltip, IntPtr target, string targetName, string mode, string note)
            {
                currentTarget = targetName;
                currentMode = mode;
                EmojiWindowNative.ShowTooltipForControl(tooltip, target);
                Refresh(note);
            }

            app.Label(1044, 56, 380, 42, "右侧保留手动操作按钮，用来补充 hover / click 的自动交互验证。切主题时，目标卡片也会一起换成更合适的层次。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            app.Button(1044, 122, 116, 38, "显示 Top", "⬆️", DemoColors.Blue, () =>
            {
                ShowTip(topTooltip, topTarget, "Top / Dark", "Hover / Top", "Tooltip -> 手动显示 Top");
            }, page);
            app.Button(1172, 122, 116, 38, "显示 Left", "⬅️", DemoColors.Green, () =>
            {
                ShowTip(leftTooltip, leftTarget, "Left / Custom", "Hover / Left", "Tooltip -> 手动显示 Left");
            }, page);
            app.Button(1300, 122, 124, 38, "隐藏 Left", "🙈", DemoColors.Orange, () =>
            {
                currentTarget = "Left / Custom";
                currentMode = "手动隐藏";
                EmojiWindowNative.HideTooltip(leftTooltip);
                Refresh("Tooltip -> 隐藏 Left");
            }, page);
            app.Button(1044, 176, 116, 38, "显示 Right", "🟪", DemoColors.Purple, () =>
            {
                ShowTip(rightTooltip, rightTarget, "Right / Dark", "Click / Right", "Tooltip -> 手动显示 Right");
            }, page);
            app.Button(1172, 176, 252, 38, "隐藏全部手动提示", "🧹", DemoColors.Gray, () =>
            {
                currentTarget = "全部目标";
                currentMode = "手动隐藏";
                EmojiWindowNative.HideTooltip(topTooltip);
                EmojiWindowNative.HideTooltip(bottomTooltip);
                EmojiWindowNative.HideTooltip(leftTooltip);
                EmojiWindowNative.HideTooltip(rightTooltip);
                Refresh("Tooltip -> 已隐藏全部手动提示");
            }, page);

            app.Label(40, 598, 1360, 24, "1. `CreateTooltip` + `BindTooltipToControl`：创建 Tooltip 并绑定到目标控件。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 632, 1360, 24, "2. `SetTooltipTheme` / `SetTooltipPlacement` / `SetTooltipTrigger`：分别控制主题、方向和触发方式。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 666, 1360, 24, "3. `SetTooltipColors` / `SetTooltipFont`：用于 custom 主题与字体设置，左侧目标就是这个场景。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 700, 1360, 24, "4. `ShowTooltipForControl` / `HideTooltip`：右侧手动按钮直接验证显示与隐藏逻辑。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            void ApplyTheme()
            {
                uint infoBg = shell.Palette.Dark ? EmojiWindowNative.ARGB(255, 35, 56, 82) : DemoColors.LightBlue;
                uint infoFg = shell.Palette.Dark ? EmojiWindowNative.ARGB(255, 205, 228, 255) : EmojiWindowNative.ARGB(255, 31, 94, 153);
                uint successBg = shell.Palette.Dark ? EmojiWindowNative.ARGB(255, 36, 67, 46) : DemoColors.LightGreen;
                uint successFg = shell.Palette.Dark ? EmojiWindowNative.ARGB(255, 204, 242, 191) : EmojiWindowNative.ARGB(255, 58, 122, 45);
                uint warmBg = shell.Palette.Dark ? EmojiWindowNative.ARGB(255, 59, 48, 35) : EmojiWindowNative.ARGB(255, 255, 247, 230);
                uint warmFg = shell.Palette.Dark ? EmojiWindowNative.ARGB(255, 255, 221, 170) : EmojiWindowNative.ARGB(255, 140, 74, 0);
                uint violetBg = shell.Palette.Dark ? EmojiWindowNative.ARGB(255, 57, 44, 84) : EmojiWindowNative.ARGB(255, 244, 240, 255);
                uint violetFg = shell.Palette.Dark ? EmojiWindowNative.ARGB(255, 227, 214, 255) : EmojiWindowNative.ARGB(255, 124, 58, 237);

                EmojiWindowNative.SetLabelColor(topTarget, infoFg, infoBg);
                EmojiWindowNative.SetLabelColor(bottomTarget, successFg, successBg);
                EmojiWindowNative.SetLabelColor(leftTarget, warmFg, warmBg);
                EmojiWindowNative.SetLabelColor(rightTarget, violetFg, violetBg);
                EmojiWindowNative.SetTooltipColors(leftTooltip, warmBg, warmFg, shell.Palette.Dark ? EmojiWindowNative.ARGB(255, 175, 125, 70) : DemoColors.Orange);

                shell.SetLabelText(stageHint, shell.Palette.Dark
                    ? "深色主题下四个目标都会切成更柔和的彩色卡片，避免 Tooltip 区域变成硬切块。"
                    : "浅色主题下四个目标保持轻卡片层次，更接近 Python 版的 Tooltip 观感。");
                shell.SetLabelText(stageTip, shell.Palette.Dark
                    ? "深色主题里 hover / click 的触发差异更需要借助分区说明来承接。"
                    : "浅色主题里保留目标舞台、手动触发区和读数区，Tooltip 页不会显得松散。");
                shell.SetLabelText(readoutHint, shell.Palette.Dark
                    ? "目标可直接悬停，右侧按钮只是补充验证路径。"
                    : "手动触发区用于辅助验证，不替代目标本身的 hover / click 行为。");
                Refresh(currentTarget == "等待操作" ? "Tooltip 页面已加载，可直接悬停或点击目标验证。" : $"Tooltip -> {currentTarget} / {currentMode}");
            }

            shell.RegisterPageThemeHandler(page, ApplyTheme);
            ApplyTheme();
        }

        private static IntPtr CreateTooltip(DemoApp app, IntPtr page, string text, int placement, int theme, int trigger, uint bg, uint fg, uint border, byte[] font)
        {
            byte[] bytes = app.U(text);
            IntPtr tooltip = EmojiWindowNative.CreateTooltip(page, bytes, bytes.Length, placement, bg, fg);
            EmojiWindowNative.SetTooltipTheme(tooltip, theme);
            EmojiWindowNative.SetTooltipPlacement(tooltip, placement);
            EmojiWindowNative.SetTooltipTrigger(tooltip, trigger);
            EmojiWindowNative.SetTooltipColors(tooltip, bg, fg, border);
            EmojiWindowNative.SetTooltipFont(tooltip, font, font.Length, 14f);
            return tooltip;
        }
    }
}
