using System;

namespace EmojiWindowDemo
{
    internal static class ConfirmBoxDemoPage
    {
        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;

            app.GroupBox(16, 16, 980, 520, "❓ ConfirmBox 舞台区", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(1020, 16, 444, 252, "🪄 待确认动作 / 触发入口", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(1020, 284, 444, 252, "📋 回调读数区", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(16, 558, 1448, 220, "📘 ConfirmBox API 说明", DemoTheme.Border, DemoTheme.Background, page);

            app.Label(
                40,
                56,
                920,
                42,
                "ConfirmBox 的重点不是弹窗本身，而是“哪个动作正在等待确认”和“用户最终点了确认还是取消”。",
                DemoTheme.Muted,
                DemoTheme.Background,
                12,
                PageCommon.AlignLeft,
                true,
                page);
            app.Label(56, 118, 240, 22, "🎯 当前待确认动作", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);

            IntPtr actionLabel = app.Label(56, 154, 860, 28, "动作：普通确认框", DemoTheme.Text, DemoTheme.Surface, 14, PageCommon.AlignLeft, false, page);
            IntPtr messageLabel = app.Label(
                56,
                196,
                860,
                70,
                "这是一条常规确认提示，适合在继续执行前请求用户给出明确确认。",
                DemoTheme.Text,
                DemoTheme.Surface,
                12,
                PageCommon.AlignLeft,
                true,
                page);
            IntPtr stageHint = app.Label(
                56,
                288,
                860,
                58,
                "左侧舞台区只描述当前业务动作，右侧负责触发真实弹窗，回调结果统一写回读数区。",
                DemoTheme.Muted,
                DemoTheme.Background,
                12,
                PageCommon.AlignLeft,
                true,
                page);
            app.Label(56, 378, 240, 22, "🧭 为什么这样分层", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            IntPtr stageTip = app.Label(
                56,
                410,
                860,
                70,
                "如果页面只放“确认框”按钮，用户并不知道要验证的是删除确认、继续流程还是关闭标签页这类不同业务语义。现在这些分工都能直接看见。",
                DemoTheme.Muted,
                DemoTheme.Background,
                12,
                PageCommon.AlignLeft,
                true,
                page);

            IntPtr stateLabel = app.Label(1044, 324, 396, 24, "等待触发 ConfirmBox。", DemoTheme.Primary, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            IntPtr detailLabel = app.Label(
                1044,
                360,
                396,
                112,
                "回调读数区会写回最近一次待确认动作，以及用户是确认还是取消。",
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
                "建议分别测试确认和取消两条路径。",
                DemoTheme.Muted,
                DemoTheme.Background,
                12,
                PageCommon.AlignLeft,
                true,
                page);

            string pendingAction = "普通确认框";
            string pendingMessage = "这是一条常规确认提示，适合在继续执行前请求用户给出明确确认。";
            string lastResult = "尚未触发";

            void Refresh(string note)
            {
                shell.SetLabelText(actionLabel, "动作：" + pendingAction);
                shell.SetLabelText(messageLabel, pendingMessage);
                shell.SetLabelText(stateLabel, note);
                shell.SetLabelText(
                    detailLabel,
                    $"最近待确认动作：{pendingAction}\r\n" +
                    $"最近回调结果：{lastResult}\r\n" +
                    "这里验证的是回调有没有真正回写到页面，而不是只看到一个确认框。");
                shell.SetStatus(note);
            }

            var callback = app.Pin(new EmojiWindowNative.MessageBoxCallback(confirmed =>
            {
                lastResult = confirmed != 0 ? "确认" : "取消";
                Refresh($"ConfirmBox 回调 -> {pendingAction} / {lastResult}");
            }));

            void ShowConfirm(string title, string message, string icon, string actionName, string note)
            {
                pendingAction = actionName;
                pendingMessage = message;
                lastResult = "等待用户点击";

                byte[] titleBytes = app.U(title);
                byte[] messageBytes = app.U(message);
                byte[] iconBytes = app.U(icon);
                EmojiWindowNative.show_confirm_box_bytes(app.Window, titleBytes, titleBytes.Length, messageBytes, messageBytes.Length, iconBytes, iconBytes.Length, callback);

                Refresh(note);
            }

            app.Label(1044, 56, 380, 42, "右侧按钮按业务语义拆开，分别对应普通确认、危险操作确认和继续流程确认。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            app.Button(1044, 122, 116, 38, "普通确认", "❓", DemoColors.Orange, () =>
            {
                ShowConfirm(
                    "📣 ConfirmBox",
                    "🧪 这是普通确认框演示。",
                    "❓",
                    "普通确认框",
                    "ConfirmBox -> 普通确认框");
            }, page);
            app.Button(1172, 122, 116, 38, "删除确认", "🧹", DemoColors.Red, () =>
            {
                ShowConfirm(
                    "🗑️ 删除确认",
                    "⚠️ 这是一条删除确认提示。",
                    "🗑️",
                    "删除确认",
                    "ConfirmBox -> 删除确认");
            }, page);
            app.Button(1300, 122, 124, 38, "继续流程", "🚀", DemoColors.Blue, () =>
            {
                ShowConfirm(
                    "🚀 继续流程",
                    "📌 确认继续执行下一步吗？",
                    "🚀",
                    "继续流程",
                    "ConfirmBox -> 继续流程");
            }, page);
            app.Button(1044, 176, 380, 38, "关闭当前标签页", "🗂️", DemoColors.Purple, () =>
            {
                ShowConfirm(
                    "🗂️ 关闭标签页",
                    "当前标签页还有未保存内容，确认关闭吗？",
                    "🗂️",
                    "关闭当前标签页",
                    "ConfirmBox -> 关闭当前标签页");
            }, page);

            app.Label(40, 598, 1360, 24, "1. `show_confirm_box_bytes`：弹出确认框，并在用户点击后通过 `MessageBoxCallback` 回传结果。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 632, 1360, 24, "2. 舞台区提前展示“当前待确认动作”，这样确认框就不是脱离上下文的孤立弹窗。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 666, 1360, 24, "3. 读数区统一回写最近动作和最近结果，方便验证确认 / 取消两条回调链路。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 700, 1360, 24, "4. 删除确认、流程继续、关闭标签页使用不同语义入口，观感与 Python 版的业务分层保持一致。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            void ApplyTheme()
            {
                shell.SetLabelText(stageHint, shell.Palette.Dark
                    ? "深色主题下仍保留“待确认动作 -> 触发入口 -> 回调结果”的阅读顺序。"
                    : "浅色主题下，舞台区和回调区分开后，更容易看清 ConfirmBox 的验证路径。");
                shell.SetLabelText(stageTip, shell.Palette.Dark
                    ? "深色主题里更需要把危险确认、普通确认、流程确认分开，否则页面会显得一团。"
                    : "浅色主题里把业务语义拆开，能直接对齐 Python 版的层次感。");
                shell.SetLabelText(readoutHint, shell.Palette.Dark
                    ? "先触发弹窗，再分别点击确认与取消，读数区会持续回写。"
                    : "读数区承担结果回写，不再让确认框页停留在“只有几个按钮”的层次。");
                Refresh(lastResult == "尚未触发" ? "ConfirmBox 页面已加载，可直接验证确认 / 取消回调。" : $"ConfirmBox 回调 -> {pendingAction} / {lastResult}");
            }

            shell.RegisterPageThemeHandler(page, ApplyTheme);
            ApplyTheme();
        }
    }
}
