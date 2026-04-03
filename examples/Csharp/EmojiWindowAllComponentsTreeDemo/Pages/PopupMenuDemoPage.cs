using System;
using System.Collections.Generic;

namespace EmojiWindowDemo
{
    internal static class PopupMenuDemoPage
    {
        private const int PopInfo = 5100;
        private const int PopInfoMsg = 5101;
        private const int PopInfoConfirm = 5102;
        private const int PopState = 5110;
        private const int PopStateActive = 5111;
        private const int PopStateReset = 5112;
        private const int PopBindings = 5121;
        private const int BtnMenuHit = 5201;
        private const int BtnMenuReset = 5202;

        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;

            IntPtr stageBox = app.GroupBox(16, 16, 980, 520, "PopupMenu 舞台", DemoTheme.Border, DemoTheme.Background, page);
            IntPtr sideBox = app.GroupBox(1012, 16, 452, 520, "状态 / 绑定", DemoTheme.Border, DemoTheme.Background, page);
            IntPtr apiBox = app.GroupBox(16, 558, 1448, 224, "最近回调 / 接口覆盖", DemoTheme.Border, DemoTheme.Background, page);

            IntPtr intro = app.Label(40, 54, 920, 24, "这一页只保留 PopupMenu 本体：左侧测试控件右键菜单，右侧测试按钮专属菜单和状态回写。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);

            IntPtr stagePanel = app.Panel(40, 92, 932, 382, DemoTheme.Surface, page);
            IntPtr stageTip = app.Label(24, 24, 884, 20, "在下方区域点击鼠标右键，可以直接打开控件绑定 PopupMenu。", DemoTheme.Muted, DemoTheme.Surface, 12, PageCommon.AlignLeft, false, stagePanel);
            IntPtr sceneLabel = app.Label(24, 58, 884, 34, "等待右键动作", DemoTheme.Primary, DemoTheme.Surface, 24, PageCommon.AlignLeft, false, stagePanel);
            IntPtr detailLabel = app.Label(24, 98, 884, 44, "主菜单包含二级子菜单、状态回写和绑定读取；右侧蓝色按钮则绑定了独立的按钮菜单。", DemoTheme.Muted, DemoTheme.Surface, 14, PageCommon.AlignLeft, true, stagePanel);

            IntPtr menuZone = app.Panel(24, 162, 620, 154, DemoTheme.Background, stagePanel);
            IntPtr menuZoneTitle = app.Label(24, 24, 320, 28, "在这里点鼠标右键", DemoTheme.Text, DemoTheme.Background, 20, PageCommon.AlignLeft, false, menuZone);
            IntPtr menuZoneLine1 = app.Label(24, 72, 540, 22, "主菜单包含：查看说明、回写状态、读取当前绑定。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, false, menuZone);
            IntPtr menuZoneLine2 = app.Label(24, 104, 540, 22, "其中“查看说明”和“回写状态”都带二级子菜单。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, false, menuZone);
            IntPtr stageFoot = app.Label(24, 336, 884, 20, "这块右键区只负责控件绑定菜单，按钮菜单在右侧单独测试，不混在一起。", DemoTheme.Muted, DemoTheme.Surface, 12, PageCommon.AlignLeft, false, stagePanel);

            IntPtr statusTitle = app.Label(1040, 54, 220, 22, "当前状态", DemoTheme.Text, DemoTheme.Background, 15, PageCommon.AlignLeft, false, page);
            IntPtr readout = app.Label(1040, 88, 392, 96, "等待读取 PopupMenu 状态。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr callbackTitle = app.Label(1040, 210, 220, 22, "最近回调", DemoTheme.Text, DemoTheme.Background, 15, PageCommon.AlignLeft, false, page);
            IntPtr callbackLabel = app.Label(1040, 244, 392, 72, "尚未触发 PopupMenu 回调。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr stateLabel = app.Label(1040, 326, 392, 22, "PopupMenu 页面状态会显示在这里。", DemoTheme.Primary, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            IntPtr sideTip = app.Label(1040, 356, 392, 40, "蓝色按钮请直接点右键；左侧白色区域则用于测试控件绑定菜单。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);

            IntPtr bottomCallbackTitle = app.Label(40, 594, 220, 22, "最近回调", DemoTheme.Text, DemoTheme.Background, 15, PageCommon.AlignLeft, false, page);
            IntPtr eventFeed = app.Label(40, 628, 900, 96, "等待触发 PopupMenu 回调。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr apiTitle = app.Label(980, 594, 220, 22, "接口覆盖", DemoTheme.Text, DemoTheme.Background, 15, PageCommon.AlignLeft, false, page);
            IntPtr api1 = app.Label(980, 626, 430, 32, "1. CreateEmojiPopupMenu / PopupMenuAddItem / PopupMenuAddSubItem：创建主菜单、按钮菜单和二级子菜单。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr api2 = app.Label(980, 662, 430, 32, "2. BindControlMenu / BindButtonMenu：分别绑定左侧右键区和右侧按钮。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr api3 = app.Label(980, 698, 430, 32, "3. SetPopupMenuCallback：所有菜单项都会把 menu_id / item_id 和最近动作回写到页面。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);

            app.AttachToGroup(stageBox, intro);
            app.AttachToGroup(sideBox, statusTitle, readout, callbackTitle, callbackLabel, stateLabel, sideTip);
            app.AttachToGroup(apiBox, bottomCallbackTitle, eventFeed, apiTitle, api1, api2, api3);

            var events = new List<string>();
            string scene = "等待右键动作";
            string detail = "在左侧区域点右键，或对右侧蓝色按钮点右键。";
            string lastEvent = "尚未触发 PopupMenu 回调。";
            int lastMenuId = 0;
            int lastItemId = 0;

            var confirmCallback = app.Pin(new EmojiWindowNative.MessageBoxCallback(confirmed =>
                shell.SetStatus("PopupMenu ConfirmBox 返回: " + (confirmed != 0 ? "确定" : "取消"))));

            void PushEvent(string text)
            {
                events.Insert(0, text);
                if (events.Count > 6)
                {
                    events.RemoveAt(events.Count - 1);
                }

                shell.SetLabelText(eventFeed, string.Join("\r\n", events));
            }

            void Refresh(string note)
            {
                shell.SetLabelText(sceneLabel, scene);
                shell.SetLabelText(detailLabel, detail);
                shell.SetLabelText(
                    readout,
                    "主菜单绑定: 左侧右键区\r\n" +
                    "按钮菜单绑定: 蓝色按钮\r\n" +
                    $"最近回调: menu_id={lastMenuId}  item_id={lastItemId}\r\n" +
                    $"当前场景: {scene}");
                shell.SetLabelText(callbackLabel, lastEvent);
                shell.SetLabelText(stateLabel, note);
                shell.SetStatus(note);
            }

            void RestoreDefault(string note)
            {
                scene = "等待右键动作";
                detail = "在左侧区域点右键，或对右侧蓝色按钮点右键。";
                lastEvent = "页面状态已恢复默认。";
                PushEvent(lastEvent);
                Refresh(note);
            }

            void ShowBindingSummary()
            {
                scene = "当前绑定已读取";
                detail = "主菜单绑定=左侧右键区；按钮菜单绑定=右侧蓝色按钮。";
                lastEvent = "已读取当前 PopupMenu 绑定。";
                PushEvent(lastEvent);
                Refresh("PopupMenu 已读取当前绑定");
            }

            int buttonMenuId = app.Button(1040, 414, 180, 38, "按钮右键菜单", "右", DemoColors.Blue, () =>
            {
                scene = "等待按钮右键";
                detail = "请直接对这个蓝色按钮点右键，打开按钮专属 PopupMenu。";
                lastEvent = "按钮提示：请对蓝色按钮点右键。";
                PushEvent(lastEvent);
                Refresh("蓝色按钮已点按，请继续点右键。");
            }, page);
            app.Button(1244, 414, 180, 38, "读取绑定", "i", DemoColors.Green, ShowBindingSummary, page);
            app.Button(1040, 462, 180, 38, "恢复默认", "R", DemoColors.Purple, () => RestoreDefault("PopupMenu 已恢复默认状态"), page);
            app.Button(1244, 462, 180, 38, "操作提示", "?", DemoColors.Gray, () =>
            {
                scene = "等待右键动作";
                detail = "左侧区域和蓝色按钮都支持右键菜单。";
                lastEvent = "操作提示：左侧区域和蓝色按钮都支持右键菜单。";
                PushEvent(lastEvent);
                Refresh("请直接用右键触发 PopupMenu。");
            }, page);

            IntPtr popupMenu = EmojiWindowNative.CreateEmojiPopupMenu(page);
            AddMenuItem(app, popupMenu, "查看说明", PopInfo);
            AddSubItem(app, popupMenu, PopInfo, "打开消息框", PopInfoMsg);
            AddSubItem(app, popupMenu, PopInfo, "打开确认框", PopInfoConfirm);
            AddMenuItem(app, popupMenu, "回写状态", PopState);
            AddSubItem(app, popupMenu, PopState, "标记为已触发", PopStateActive);
            AddSubItem(app, popupMenu, PopState, "恢复等待态", PopStateReset);
            AddMenuItem(app, popupMenu, "读取当前绑定", PopBindings);

            IntPtr buttonMenu = EmojiWindowNative.CreateEmojiPopupMenu(page);
            AddMenuItem(app, buttonMenu, "按钮菜单已触发", BtnMenuHit);
            AddMenuItem(app, buttonMenu, "恢复默认状态", BtnMenuReset);

            var menuCallback = app.Pin(new EmojiWindowNative.MenuItemClickCallback((menuId, itemId) =>
            {
                lastMenuId = menuId;
                lastItemId = itemId;

                if (itemId == PopInfoMsg)
                {
                    scene = "右键菜单已打开消息框";
                    detail = "主菜单的二级子菜单和回调回写都已经生效。";
                    lastEvent = "主菜单 -> 查看说明 -> 打开消息框";
                    byte[] title = app.U("PopupMenu 消息框");
                    byte[] message = app.U("这是从右键菜单打开的 MessageBox。");
                    byte[] icon = app.U("菜单");
                    EmojiWindowNative.show_message_box_bytes(page, title, title.Length, message, message.Length, icon, icon.Length);
                    PushEvent(lastEvent);
                    Refresh("PopupMenu 已触发消息框");
                }
                else if (itemId == PopInfoConfirm)
                {
                    scene = "右键菜单已打开确认框";
                    detail = "ConfirmBox 已弹出，当前菜单回调也已经同步回写。";
                    lastEvent = "主菜单 -> 查看说明 -> 打开确认框";
                    byte[] title = app.U("PopupMenu 确认框");
                    byte[] message = app.U("这是从右键菜单打开的 ConfirmBox。");
                    byte[] icon = app.U("菜单");
                    EmojiWindowNative.show_confirm_box_bytes(page, title, title.Length, message, message.Length, icon, icon.Length, confirmCallback);
                    PushEvent(lastEvent);
                    Refresh("PopupMenu 已触发确认框");
                }
                else if (itemId == PopStateActive)
                {
                    scene = "状态已标记为已触发";
                    detail = "这是通过右键菜单直接回写到页面的状态文本。";
                    lastEvent = "主菜单 -> 回写状态 -> 标记为已触发";
                    PushEvent(lastEvent);
                    Refresh("PopupMenu 已回写“已触发”状态");
                }
                else if (itemId == PopStateReset)
                {
                    scene = "等待右键动作";
                    detail = "页面状态已通过右键菜单恢复为初始等待态。";
                    lastEvent = "主菜单 -> 回写状态 -> 恢复等待态";
                    PushEvent(lastEvent);
                    Refresh("PopupMenu 已恢复等待态");
                }
                else if (itemId == PopBindings)
                {
                    ShowBindingSummary();
                }
                else if (itemId == BtnMenuHit)
                {
                    scene = "按钮菜单已触发";
                    detail = "当前命中的是蓝色按钮专属 PopupMenu。";
                    lastEvent = "按钮菜单 -> 按钮菜单已触发";
                    PushEvent(lastEvent);
                    Refresh("按钮右键菜单回调正常");
                }
                else if (itemId == BtnMenuReset)
                {
                    RestoreDefault("按钮菜单已恢复默认状态");
                    lastEvent = "按钮菜单 -> 恢复默认状态";
                    PushEvent(lastEvent);
                    Refresh("按钮菜单已恢复默认状态");
                }
                else
                {
                    scene = "收到 PopupMenu 回调";
                    detail = $"menu_id={menuId}，item_id={itemId} 已写回页面。";
                    lastEvent = $"PopupMenu 收到 item_id={itemId}";
                    PushEvent(lastEvent);
                    Refresh("PopupMenu 已收到回调");
                }
            }));

            EmojiWindowNative.SetPopupMenuCallback(popupMenu, menuCallback);
            EmojiWindowNative.SetPopupMenuCallback(buttonMenu, menuCallback);
            EmojiWindowNative.BindControlMenu(menuZone, popupMenu);
            EmojiWindowNative.BindButtonMenu(page, buttonMenuId, buttonMenu);

            void ApplyTheme()
            {
                DemoThemePalette palette = shell.Palette;
                EmojiWindowNative.SetPanelBackgroundColor(stagePanel, palette.CardBackground);
                EmojiWindowNative.SetPanelBackgroundColor(menuZone, palette.PageBackground);
            }

            shell.RegisterPageThemeHandler(page, ApplyTheme);
            ApplyTheme();
            RestoreDefault("PopupMenu 页面已整理为控件右键菜单和按钮菜单两类绑定。");

            _ = stageTip;
            _ = stageFoot;
            _ = menuZoneTitle;
            _ = menuZoneLine1;
            _ = menuZoneLine2;
        }

        private static void AddMenuItem(DemoApp app, IntPtr menu, string text, int itemId)
        {
            byte[] bytes = app.U(text);
            EmojiWindowNative.PopupMenuAddItem(menu, bytes, bytes.Length, itemId);
        }

        private static void AddSubItem(DemoApp app, IntPtr menu, int parentId, string text, int itemId)
        {
            byte[] bytes = app.U(text);
            EmojiWindowNative.PopupMenuAddSubItem(menu, parentId, bytes, bytes.Length, itemId);
        }
    }
}
