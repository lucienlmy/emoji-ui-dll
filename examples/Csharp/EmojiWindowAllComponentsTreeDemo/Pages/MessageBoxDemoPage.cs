using System;

namespace EmojiWindowDemo
{
    internal static class MessageBoxDemoPage
    {
        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;

            app.GroupBox(16, 16, 980, 520, "💬 MessageBox 舞台区", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(1020, 16, 444, 252, "🪄 消息类型 / 触发入口", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(1020, 284, 444, 252, "📋 最近一次弹窗读数", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(16, 558, 1448, 220, "📘 MessageBox API 说明", DemoTheme.Border, DemoTheme.Background, page);

            app.Label(
                40,
                56,
                920,
                42,
                "这一页不再只是放几个按钮，而是把“将要弹出的内容”“最近一次触发结果”“调用入口”拆开，层次对齐 Python 版。",
                DemoTheme.Muted,
                DemoTheme.Background,
                12,
                PageCommon.AlignLeft,
                true,
                page);
            app.Label(56, 118, 220, 22, "🎯 当前预演消息", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);

            IntPtr previewTitle = app.Label(56, 152, 860, 28, "标题：普通消息", DemoTheme.Text, DemoTheme.Surface, 14, PageCommon.AlignLeft, false, page);
            IntPtr previewIcon = app.Label(56, 190, 180, 68, "💬", DemoTheme.Primary, DemoTheme.SurfacePrimary, 28, PageCommon.AlignCenter, false, page);
            IntPtr previewMessage = app.Label(
                256,
                190,
                660,
                68,
                "这是一个用于说明常规状态、流程提示或结果反馈的消息框示例。",
                DemoTheme.Text,
                DemoTheme.Surface,
                12,
                PageCommon.AlignLeft,
                true,
                page);
            IntPtr stageHint = app.Label(
                56,
                284,
                860,
                54,
                "左侧是“舞台区”，右侧按钮不管点哪一个，这里都会先同步说明弹窗语义，再实际弹出系统消息框。",
                DemoTheme.Muted,
                DemoTheme.Background,
                12,
                PageCommon.AlignLeft,
                true,
                page);
            app.Label(56, 372, 220, 22, "🧭 推荐分工", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            IntPtr stageTip = app.Label(
                56,
                404,
                860,
                76,
                "普通消息用于常规说明，成功消息用于正向反馈，警告消息用于风险提醒，错误消息用于明确失败原因。进入页面时就能看懂按钮各自负责什么。",
                DemoTheme.Muted,
                DemoTheme.Background,
                12,
                PageCommon.AlignLeft,
                true,
                page);

            IntPtr stateLabel = app.Label(1044, 324, 396, 24, "等待触发 MessageBox。", DemoTheme.Primary, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            IntPtr detailLabel = app.Label(
                1044,
                360,
                396,
                112,
                "读数区会记录最近一次弹窗的标题、图标语义和使用场景，避免页面只能看到“按钮被点了”。",
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
                "建议先看舞台区，再点右上按钮验证实际弹窗。",
                DemoTheme.Muted,
                DemoTheme.Background,
                12,
                PageCommon.AlignLeft,
                true,
                page);

            string currentTitle = "普通消息";
            string currentMessage = "这是一个用于说明常规状态、流程提示或结果反馈的消息框示例。";
            string currentIcon = "💬";
            string currentStatus = "MessageBox 页面已加载，可直接测试四种消息框。";
            string currentDetail = "当前消息语义：普通说明\r\n适用场景：展示非风险型提示\r\n当前入口：等待点击右侧按钮";

            void RefreshPreview()
            {
                shell.SetLabelText(previewTitle, "标题：" + currentTitle);
                shell.SetLabelText(previewIcon, currentIcon);
                shell.SetLabelText(previewMessage, currentMessage);
                shell.SetLabelText(stateLabel, currentStatus);
                shell.SetLabelText(detailLabel, currentDetail);
            }

            void ShowMessage(string title, string message, string icon, string status, string detail)
            {
                currentTitle = title;
                currentMessage = message;
                currentIcon = icon;
                currentStatus = status;
                currentDetail = detail;

                byte[] titleBytes = app.U(title);
                byte[] messageBytes = app.U(message);
                byte[] iconBytes = app.U(icon);
                EmojiWindowNative.show_message_box_bytes(app.Window, titleBytes, titleBytes.Length, messageBytes, messageBytes.Length, iconBytes, iconBytes.Length);

                RefreshPreview();
                shell.SetStatus(status);
            }

            app.Label(1044, 56, 380, 42, "按钮按语义色分组，进入页面时就能区分这是普通提示、成功反馈、警告提醒还是错误说明。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            app.Button(1044, 122, 116, 38, "普通消息", "💬", DemoColors.Blue, () =>
            {
                ShowMessage(
                    "📝 普通消息",
                    "🧪 这是普通消息框演示。",
                    "💬",
                    "MessageBox -> 普通消息",
                    "当前消息语义：普通说明\r\n适用场景：帮助信息、流程提示、状态反馈\r\n当前入口：普通消息按钮");
            }, page);
            app.Button(1172, 122, 116, 38, "成功消息", "✅", DemoColors.Green, () =>
            {
                ShowMessage(
                    "✅ 操作成功",
                    "🎉 这是成功消息框演示。",
                    "✅",
                    "MessageBox -> 成功消息",
                    "当前消息语义：成功反馈\r\n适用场景：保存成功、发布完成、任务结束\r\n当前入口：成功消息按钮");
            }, page);
            app.Button(1300, 122, 124, 38, "警告消息", "⚠️", DemoColors.Orange, () =>
            {
                ShowMessage(
                    "⚠️ 注意",
                    "📌 这是警告消息框演示。",
                    "⚠️",
                    "MessageBox -> 警告消息",
                    "当前消息语义：风险提醒\r\n适用场景：继续操作前再次确认上下文\r\n当前入口：警告消息按钮");
            }, page);
            app.Button(1044, 176, 116, 38, "错误消息", "❌", DemoColors.Red, () =>
            {
                ShowMessage(
                    "❌ 错误",
                    "接口调用失败，请检查参数和日志输出。",
                    "❌",
                    "MessageBox -> 错误消息",
                    "当前消息语义：失败反馈\r\n适用场景：明确失败原因并指导下一步处理\r\n当前入口：错误消息按钮");
            }, page);
            app.Button(1172, 176, 252, 38, "再次弹出当前预演消息", "🔁", DemoColors.Purple, () =>
            {
                ShowMessage(currentTitle, currentMessage, currentIcon, "MessageBox -> 再次弹出当前预演消息", currentDetail);
            }, page);

            app.Label(40, 598, 1360, 24, "1. `show_message_box_bytes`：直接调用 DLL 弹出原生消息框，标题、正文和图标都通过 UTF-8 字节传入。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 632, 1360, 24, "2. 页面先更新舞台区与读数区，再触发弹窗，避免界面里只剩一个孤立按钮。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 666, 1360, 24, "3. 语义色对应普通 / 成功 / 警告 / 错误四类消息，和 Python 版的使用路径保持一致。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 700, 1360, 24, "4. 读数区强调“为什么弹这个框”，而不是只记录“点了哪个按钮”。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            void ApplyTheme()
            {
                shell.SetLabelText(stageHint, shell.Palette.Dark
                    ? "深色主题下也保留“预演消息 + 语义说明 + 读数回写”的层次，避免只剩黑底按钮。"
                    : "浅色主题下保持 MessageBox 的舞台区、触发区和读数区分层，阅读顺序更接近 Python 版。");
                shell.SetLabelText(stageTip, shell.Palette.Dark
                    ? "深色主题里语义色仍旧承担分流作用：蓝=普通、绿=成功、橙=警告、红=错误。"
                    : "浅色主题里先看左侧语义说明，再点右侧入口，能更快理解 MessageBox 的分工。");
                shell.SetLabelText(readoutHint, shell.Palette.Dark
                    ? "先看右侧读数，再点按钮，能更清楚地验证消息语义是否写回页面。"
                    : "读数区用于承接最近一次弹窗结果，避免操作完后页面没有上下文。");
                RefreshPreview();
            }

            shell.RegisterPageThemeHandler(page, ApplyTheme);
            ApplyTheme();
            shell.SetStatus(currentStatus);
        }
    }
}
