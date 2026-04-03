using System;
using System.Collections.Generic;
using System.IO;

namespace EmojiWindowDemo
{
    internal static class PictureBoxDemoPage
    {
        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;

            app.GroupBox(16, 16, 980, 520, "PictureBox 预览与操作", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(1020, 16, 444, 392, "事件 / 状态 / 属性", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(1020, 420, 444, 116, "焦点 / 布局 / 背景", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(16, 558, 1448, 220, "PictureBox API 说明", DemoTheme.Border, DemoTheme.Background, page);

            app.Label(
                40,
                54,
                900,
                38,
                "这一页只保留 PictureBox 本体。上方两排按钮直接操作图片加载、缩放模式和透明度，右侧集中展示事件、焦点与布局状态。",
                DemoTheme.Muted,
                DemoTheme.Background,
                12,
                PageCommon.AlignLeft,
                true,
                page);
            app.Label(1020, 54, 220, 22, "当前状态", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Label(1020, 228, 220, 22, "最近事件", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Label(
                1020,
                84,
                412,
                40,
                "点击图片框或先点“聚焦图片”，再按键盘，可以验证 Click / DoubleClick / RightClick / Focus / Blur / KeyDown / KeyUp / Char / ValueChanged。",
                DemoTheme.Muted,
                DemoTheme.Background,
                12,
                PageCommon.AlignLeft,
                true,
                page);

            IntPtr readout = app.Label(1020, 126, 412, 86, "等待读取 PictureBox 状态。", DemoTheme.Text, DemoTheme.Surface, 12, PageCommon.AlignLeft, true, page);
            IntPtr eventLog = app.Label(1020, 258, 412, 104, "等待触发 PictureBox 事件。", DemoTheme.Muted, DemoTheme.Surface, 12, PageCommon.AlignLeft, true, page);
            IntPtr stateText = app.Label(1020, 370, 412, 22, "PictureBox 页面状态会显示在这里。", DemoTheme.Primary, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            IntPtr stageTip = app.Label(
                40,
                492,
                912,
                24,
                "图片源、缩放模式、透明度和背景色都直接作用在同一个 PictureBox 上，右侧读数区会同步回写。",
                DemoTheme.Muted,
                DemoTheme.Background,
                12,
                PageCommon.AlignLeft,
                true,
                page);

            string pngPath = PageCommon.FindFirstExistingPath(app, @"imgs\图片框示例.png", @"imgs\1.png");
            string altPath = PageCommon.FindFirstExistingPath(app, @"imgs\2.png", @"imgs\3.png");
            var events = new List<string>();

            int x = 40;
            int y = 184;
            int width = 912;
            int height = 290;
            bool visible = true;
            bool enabled = true;
            float opacity = 1.0f;
            string scaleText = "FIT";
            string imageName = "未加载";
            bool loaded = false;
            string backgroundMode = "theme";

            uint ThemeBackground() => shell.Palette.CardBackground;
            uint CoolBackground() => shell.Palette.Dark ? EmojiWindowNative.ARGB(255, 36, 54, 73) : EmojiWindowNative.ARGB(255, 234, 243, 255);
            uint WarmBackground() => shell.Palette.Dark ? EmojiWindowNative.ARGB(255, 59, 48, 35) : EmojiWindowNative.ARGB(255, 255, 244, 232);

            uint CurrentBackground()
            {
                switch (backgroundMode)
                {
                    case "cool":
                        return CoolBackground();
                    case "warm":
                        return WarmBackground();
                    default:
                        return ThemeBackground();
                }
            }

            IntPtr picture = EmojiWindowNative.CreatePictureBox(page, x, y, width, height, PageCommon.ScaleFit, CurrentBackground());

            void PushEvent(string message, bool publishStatus = false)
            {
                events.Insert(0, message);
                if (events.Count > 6)
                {
                    events.RemoveAt(events.Count - 1);
                }

                shell.SetLabelText(eventLog, string.Join("\r\n", events));
                if (publishStatus)
                {
                    shell.SetStatus(message);
                }
            }

            void Refresh(string note)
            {
                bool hasFocus = Win32Native.GetFocus() == picture;
                uint background = CurrentBackground();

                shell.SetLabelText(
                    readout,
                    $"图片={imageName}  已加载={(loaded ? "是" : "否")}  可见={(visible ? "是" : "否")}  启用={(enabled ? "是" : "否")}\r\n" +
                    $"模式={scaleText}  透明度={(int)(opacity * 100)}%  焦点={(hasFocus ? "是" : "否")}\r\n" +
                    $"背景={PageCommon.FormatColor(background)}  位置=({x}, {y})  尺寸={width} x {height}");
                shell.SetLabelText(stateText, note);
                shell.SetStatus(note);
            }

            void LoadFromPath(string path, string label)
            {
                bool ok = false;
                if (!string.IsNullOrEmpty(path) && File.Exists(path))
                {
                    byte[] bytes = app.U(path);
                    ok = EmojiWindowNative.LoadImageFromFile(picture, bytes, bytes.Length) != 0;
                }

                if (!ok)
                {
                    ok = EmojiWindowNative.LoadImageFromMemory(picture, PageCommon.TinyPngBytes, PageCommon.TinyPngBytes.Length) != 0;
                    label = ok ? "内存占位图" : "未加载";
                }

                loaded = ok;
                imageName = label;
                Refresh(ok ? $"PictureBox 已加载 {label}" : "PictureBox 加载失败");
            }

            void SetScale(int mode, string label, string note)
            {
                scaleText = label;
                EmojiWindowNative.SetPictureBoxScaleMode(picture, mode);
                Refresh(note);
            }

            void SetOpacity(float value, string note)
            {
                opacity = value;
                EmojiWindowNative.SetImageOpacity(picture, value);
                Refresh(note);
            }

            void SetBackgroundMode(string mode, string note)
            {
                backgroundMode = mode;
                EmojiWindowNative.SetPictureBoxBackgroundColor(picture, CurrentBackground());
                Refresh(note);
            }

            var clickCallback = app.Pin(new EmojiWindowNative.PictureBoxCallback(_ =>
            {
                PushEvent("Click -> PictureBox 被单击");
                Refresh("PictureBox 点击事件已触发");
            }));
            var mouseEnterCallback = app.Pin(new EmojiWindowNative.ValueChangedCallback(_ => PushEvent("MouseEnter -> 鼠标进入 PictureBox")));
            var mouseLeaveCallback = app.Pin(new EmojiWindowNative.ValueChangedCallback(_ => PushEvent("MouseLeave -> 鼠标离开 PictureBox")));
            var doubleClickCallback = app.Pin(new EmojiWindowNative.ControlPointCallback((_, px, py) =>
            {
                PushEvent($"DoubleClick -> ({px}, {py})");
                Refresh("PictureBox 双击事件已触发");
            }));
            var rightClickCallback = app.Pin(new EmojiWindowNative.ControlPointCallback((_, px, py) =>
            {
                PushEvent($"RightClick -> ({px}, {py})");
                Refresh("PictureBox 右键事件已触发");
            }));
            var focusCallback = app.Pin(new EmojiWindowNative.ValueChangedCallback(_ =>
            {
                PushEvent("Focus -> PictureBox 获得焦点");
                Refresh("PictureBox 已获得焦点");
            }));
            var blurCallback = app.Pin(new EmojiWindowNative.ValueChangedCallback(_ =>
            {
                PushEvent("Blur -> PictureBox 失去焦点");
                Refresh("PictureBox 已失去焦点");
            }));
            var keyDownCallback = app.Pin(new EmojiWindowNative.ControlKeyCallback((_, vk, shift, ctrl, alt) =>
                PushEvent($"KeyDown -> {PageCommon.FormatHotKey(vk, (shift != 0 ? 1 : 0) | (ctrl != 0 ? 2 : 0) | (alt != 0 ? 4 : 0))}")));
            var keyUpCallback = app.Pin(new EmojiWindowNative.ControlKeyCallback((_, vk, shift, ctrl, alt) =>
                PushEvent($"KeyUp -> {PageCommon.FormatHotKey(vk, (shift != 0 ? 1 : 0) | (ctrl != 0 ? 2 : 0) | (alt != 0 ? 4 : 0))}")));
            var charCallback = app.Pin(new EmojiWindowNative.ControlCharCallback((_, charCode) =>
                PushEvent($"Char -> {(charCode >= 32 && charCode <= 126 ? ((char)charCode).ToString() : "U+" + charCode.ToString("X4"))}")));
            var valueChangedCallback = app.Pin(new EmojiWindowNative.ValueChangedCallback(_ => PushEvent("ValueChanged -> 图片内容或属性已变化")));

            EmojiWindowNative.SetPictureBoxCallback(picture, clickCallback);
            EmojiWindowNative.SetMouseEnterCallback(picture, mouseEnterCallback);
            EmojiWindowNative.SetMouseLeaveCallback(picture, mouseLeaveCallback);
            EmojiWindowNative.SetDoubleClickCallback(picture, doubleClickCallback);
            EmojiWindowNative.SetRightClickCallback(picture, rightClickCallback);
            EmojiWindowNative.SetFocusCallback(picture, focusCallback);
            EmojiWindowNative.SetBlurCallback(picture, blurCallback);
            EmojiWindowNative.SetKeyDownCallback(picture, keyDownCallback);
            EmojiWindowNative.SetKeyUpCallback(picture, keyUpCallback);
            EmojiWindowNative.SetCharCallback(picture, charCallback);
            EmojiWindowNative.SetValueChangedCallback(picture, valueChangedCallback);

            app.Button(40, 96, 120, 34, "PNG 示例", "图", DemoColors.Blue, () => LoadFromPath(pngPath, Path.GetFileName(pngPath)), page);
            app.Button(172, 96, 120, 34, "第二张图", "2", DemoColors.Green, () => LoadFromPath(altPath, Path.GetFileName(altPath)), page);
            app.Button(304, 96, 120, 34, "清空图片", "X", DemoColors.Orange, () =>
            {
                EmojiWindowNative.ClearImage(picture);
                loaded = false;
                imageName = "已清空";
                Refresh("PictureBox 图片已清空");
            }, page);
            app.Button(436, 96, 120, 34, "原始大小", "1:1", DemoColors.Red, () => SetScale(PageCommon.ScaleNone, "NONE", "PictureBox 缩放模式已切到 NONE"), page);
            app.Button(568, 96, 120, 34, "拉伸铺满", "拉", DemoColors.Gray, () => SetScale(PageCommon.ScaleStretch, "STRETCH", "PictureBox 缩放模式已切到 STRETCH"), page);

            app.Button(40, 138, 120, 34, "等比适应", "FIT", DemoColors.Purple, () => SetScale(PageCommon.ScaleFit, "FIT", "PictureBox 缩放模式已切到 FIT"), page);
            app.Button(172, 138, 120, 34, "居中显示", "中", DemoColors.Blue, () => SetScale(PageCommon.ScaleCenter, "CENTER", "PictureBox 缩放模式已切到 CENTER"), page);
            app.Button(304, 138, 120, 34, "100%", "100", DemoColors.Green, () => SetOpacity(1.0f, "PictureBox 透明度已设为 100%"), page);
            app.Button(436, 138, 120, 34, "60%", "60", DemoColors.Orange, () => SetOpacity(0.6f, "PictureBox 透明度已设为 60%"), page);
            app.Button(568, 138, 120, 34, "25%", "25", DemoColors.Red, () => SetOpacity(0.25f, "PictureBox 透明度已设为 25%"), page);

            app.Button(1040, 460, 84, 30, "聚焦", "F", DemoColors.Blue, () =>
            {
                Win32Native.SetFocus(picture);
                Refresh("焦点已切到 PictureBox");
            }, page);
            app.Button(1134, 460, 84, 30, "移焦", "B", DemoColors.Gray, () =>
            {
                Win32Native.SetFocus(page);
                Refresh("焦点已从 PictureBox 移开");
            }, page);
            app.Button(1228, 460, 84, 30, "显隐", "V", DemoColors.Green, () =>
            {
                visible = !visible;
                EmojiWindowNative.ShowPictureBox(picture, visible ? 1 : 0);
                Refresh(visible ? "PictureBox 已显示" : "PictureBox 已隐藏");
            }, page);
            app.Button(1322, 460, 84, 30, "启用", "E", DemoColors.Red, () =>
            {
                enabled = !enabled;
                EmojiWindowNative.EnablePictureBox(picture, enabled ? 1 : 0);
                Refresh(enabled ? "PictureBox 已启用" : "PictureBox 已禁用");
            }, page);

            app.Button(1040, 496, 84, 30, "放大", "+", DemoColors.Purple, () =>
            {
                x = 40;
                y = 184;
                width = 960;
                height = 304;
                EmojiWindowNative.SetPictureBoxBounds(picture, x, y, width, height);
                Refresh("PictureBox 预览区域已放大");
            }, page);
            app.Button(1134, 496, 84, 30, "重置", "R", DemoColors.Blue, () =>
            {
                x = 40;
                y = 184;
                width = 912;
                height = 290;
                visible = true;
                enabled = true;
                opacity = 1.0f;
                backgroundMode = "theme";
                EmojiWindowNative.SetPictureBoxBounds(picture, x, y, width, height);
                EmojiWindowNative.ShowPictureBox(picture, 1);
                EmojiWindowNative.EnablePictureBox(picture, 1);
                EmojiWindowNative.SetPictureBoxBackgroundColor(picture, CurrentBackground());
                SetScale(PageCommon.ScaleFit, "FIT", "PictureBox 已恢复默认状态");
                LoadFromPath(pngPath, Path.GetFileName(pngPath));
            }, page);
            app.Button(1228, 496, 84, 30, "冷色", "C", DemoColors.Green, () => SetBackgroundMode("cool", "PictureBox 已切到冷色背景"), page);
            app.Button(1322, 496, 84, 30, "暖色", "W", DemoColors.Orange, () => SetBackgroundMode("warm", "PictureBox 已切到暖色背景"), page);

            app.Label(40, 598, 1360, 24, "1. `CreatePictureBox` / `LoadImageFromFile` / `LoadImageFromMemory` / `ClearImage`：创建图片框并切换图片来源。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 632, 1360, 24, "2. `SetPictureBoxScaleMode`：直接切换 NONE / STRETCH / FIT / CENTER 四种缩放模式。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 666, 1360, 24, "3. `SetImageOpacity` / `SetPictureBoxBackgroundColor`：透明度与背景色可独立调整，并支持跟随主题刷新。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 700, 1360, 24, "4. `SetPictureBoxBounds` / `ShowPictureBox` / `EnablePictureBox`：布局、可见态和启用态都可以实时切换。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 734, 1360, 24, "5. 页面已接入 Click / DoubleClick / RightClick / MouseEnter / MouseLeave / Focus / Blur / KeyDown / KeyUp / Char / ValueChanged。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            void ApplyTheme()
            {
                EmojiWindowNative.SetLabelColor(readout, shell.Palette.Text, shell.Palette.CardBackground);
                EmojiWindowNative.SetLabelColor(eventLog, shell.Palette.Muted, shell.Palette.CardBackground);
                EmojiWindowNative.SetLabelColor(stateText, shell.Palette.Accent, shell.Palette.PageBackground);
                EmojiWindowNative.SetPictureBoxBackgroundColor(picture, CurrentBackground());
                shell.SetLabelText(
                    stageTip,
                    shell.Palette.Dark
                        ? "深色主题下，预览舞台和右侧状态区仍保持清晰分层，不会糊成一整块。"
                        : "浅色主题下，PictureBox 舞台区、按钮区和右侧读数区保持和 Python 版接近的结构。");
                Refresh(events.Count == 0 ? "PictureBox 页面已加载，右侧集中展示状态与事件回写。" : "PictureBox 页面主题已刷新。");
            }

            shell.RegisterPageThemeHandler(page, ApplyTheme);
            LoadFromPath(pngPath, Path.GetFileName(pngPath));
            ApplyTheme();
        }
    }
}
