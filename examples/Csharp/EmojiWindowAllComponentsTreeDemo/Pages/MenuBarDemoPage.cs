using System;
using System.Collections.Generic;

namespace EmojiWindowDemo
{
    internal static class MenuBarDemoPage
    {
        private const int MenuFile = 5000;
        private const int MenuDialog = 5100;
        private const int MenuMessage = 5110;
        private const int MenuConfirm = 5111;
        private const int MenuScene = 5200;
        private const int MenuSceneRunning = 5210;
        private const int MenuSceneDone = 5211;
        private const int MenuLayout = 6000;
        private const int MenuLayoutLeft = 6110;
        private const int MenuLayoutStd = 6111;
        private const int MenuLayoutWide = 6112;
        private const int MenuLayoutDown = 6113;
        private const int MenuLayoutReset = 6114;
        private const int MenuTools = 7000;
        private const int MenuToolRename = 7100;
        private const int MenuToolRestore = 7101;
        private const int MenuToolToggle = 7102;
        private const int MenuToolRefresh = 7103;

        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;

            IntPtr stageBox = app.GroupBox(16, 16, 980, 520, "MenuBar 舞台", DemoTheme.Border, DemoTheme.Background, page);
            IntPtr sideBox = app.GroupBox(1012, 16, 452, 520, "状态 / 快捷操作", DemoTheme.Border, DemoTheme.Background, page);
            IntPtr apiBox = app.GroupBox(16, 558, 1448, 224, "最近回调 / 接口覆盖", DemoTheme.Border, DemoTheme.Background, page);

            IntPtr intro = app.Label(40, 54, 920, 24, "这一页只保留 MenuBar 本体：左侧是真实菜单舞台，右侧只放状态和快捷操作，不再混入别的组件演示。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr stagePanel = app.Panel(40, 92, 932, 382, DemoTheme.Surface, page);
            IntPtr sceneLabel = app.Label(24, 126, 884, 34, "等待菜单动作", DemoTheme.Primary, DemoTheme.Surface, 24, PageCommon.AlignLeft, false, stagePanel);
            IntPtr detailLabel = app.Label(24, 172, 884, 44, "点击“文件 / 布局 / 工具”菜单项，右侧状态和底部日志会立刻同步。", DemoTheme.Muted, DemoTheme.Surface, 14, PageCommon.AlignLeft, true, stagePanel);
            IntPtr stageTip = app.Label(24, 72, 884, 20, "直接点击上方菜单，验证三级子菜单、布局调整、文案更新和回调回写。", DemoTheme.Muted, DemoTheme.Surface, 12, PageCommon.AlignLeft, false, stagePanel);
            IntPtr stageFoot = app.Label(24, 330, 884, 20, "右侧按钮只保留常用快捷入口，其余动作直接在 MenuBar 自身菜单里测试。", DemoTheme.Muted, DemoTheme.Surface, 12, PageCommon.AlignLeft, false, stagePanel);

            IntPtr statusTitle = app.Label(1040, 54, 220, 22, "当前状态", DemoTheme.Text, DemoTheme.Background, 15, PageCommon.AlignLeft, false, page);
            IntPtr readout = app.Label(1040, 88, 392, 96, "等待读取 MenuBar 状态。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr stateLabel = app.Label(1040, 194, 392, 22, "MenuBar 页面状态会显示在这里。", DemoTheme.Primary, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            IntPtr sideTip = app.Label(1040, 226, 392, 48, "右侧只保留快捷入口；下移、归位、刷新等动作也都能从菜单本身触发。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr quickTitle = app.Label(1040, 292, 220, 22, "快捷操作", DemoTheme.Text, DemoTheme.Background, 15, PageCommon.AlignLeft, false, page);

            IntPtr callbackTitle = app.Label(40, 594, 220, 22, "最近回调", DemoTheme.Text, DemoTheme.Background, 15, PageCommon.AlignLeft, false, page);
            IntPtr eventFeed = app.Label(40, 628, 900, 96, "等待触发 MenuBar 回调。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr apiTitle = app.Label(980, 594, 220, 22, "接口覆盖", DemoTheme.Text, DemoTheme.Background, 15, PageCommon.AlignLeft, false, page);
            IntPtr api1 = app.Label(980, 626, 430, 32, "1. CreateMenuBar / DestroyMenuBar：重建默认菜单与紧凑菜单。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr api2 = app.Label(980, 662, 430, 32, "2. MenuBarAddItem / MenuBarAddSubItem / SetMenuBarCallback：验证一、二、三级菜单及回调回写。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr api3 = app.Label(980, 698, 430, 32, "3. SetMenuBarPlacement / MenuBarUpdateSubItemText：直接修改菜单宽度、位置和子项文案。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);

            app.AttachToGroup(stageBox, intro);
            app.AttachToGroup(sideBox, statusTitle, readout, stateLabel, sideTip, quickTitle);
            app.AttachToGroup(apiBox, callbackTitle, eventFeed, apiTitle, api1, api2, api3);

            IntPtr bar = IntPtr.Zero;
            int x = 24;
            int y = 24;
            int width = 760;
            int height = 34;
            string mode = "default";
            string messageText = "显示消息框";
            string scene = "等待菜单动作";
            string detail = "点击“文件 / 布局 / 工具”菜单项，右侧状态和底部日志会立刻同步。";
            string lastEvent = "尚未触发菜单回调。";
            int lastMenuId = 0;
            int lastItemId = 0;
            var eventLines = new List<string>();
            EmojiWindowNative.MenuItemClickCallback menuCallback = null;

            var confirmCallback = app.Pin(new EmojiWindowNative.MessageBoxCallback(confirmed =>
                shell.SetStatus("MenuBar ConfirmBox 返回: " + (confirmed != 0 ? "确定" : "取消"))));

            void PushEvent(string text)
            {
                eventLines.Insert(0, text);
                if (eventLines.Count > 6)
                {
                    eventLines.RemoveAt(eventLines.Count - 1);
                }

                shell.SetLabelText(eventFeed, string.Join("\r\n", eventLines));
            }

            void Refresh(string note)
            {
                shell.SetLabelText(sceneLabel, scene);
                shell.SetLabelText(detailLabel, detail);
                shell.SetLabelText(
                    readout,
                    $"方案={(mode == "default" ? "默认三级菜单" : "紧凑菜单")}\r\n" +
                    $"位置=({x}, {y})  尺寸={width} x {height}\r\n" +
                    $"消息子项={messageText}\r\n" +
                    $"最近回调: menu_id={lastMenuId}  item_id={lastItemId}");
                shell.SetLabelText(stateLabel, note);
                shell.SetStatus(note);
            }

            void AddItem(IntPtr menuBar, string text, int itemId)
            {
                byte[] bytes = app.U(text);
                EmojiWindowNative.MenuBarAddItem(menuBar, bytes, bytes.Length, itemId);
            }

            void AddSub(IntPtr menuBar, int parentId, string text, int itemId)
            {
                byte[] bytes = app.U(text);
                EmojiWindowNative.MenuBarAddSubItem(menuBar, parentId, bytes, bytes.Length, itemId);
            }

            void ApplyPlacement(int newX, int newY, int newWidth, int newHeight, string note)
            {
                x = newX;
                y = newY;
                width = newWidth;
                height = newHeight;
                if (bar != IntPtr.Zero)
                {
                    EmojiWindowNative.SetMenuBarPlacement(bar, x, y, width, height);
                }

                Refresh(note);
            }

            void UpdateMessageText(string text, string note)
            {
                if (bar == IntPtr.Zero)
                {
                    Refresh("MenuBar 尚未创建");
                    return;
                }

                byte[] bytes = app.U(text);
                if (EmojiWindowNative.MenuBarUpdateSubItemText(bar, MenuDialog, MenuMessage, bytes, bytes.Length) != 0)
                {
                    messageText = text;
                    lastEvent = "MenuBar 子项文案已更新";
                }
                else
                {
                    lastEvent = "MenuBar 子项文案更新失败";
                }

                PushEvent(lastEvent);
                Refresh(note);
            }

            void RebuildMenu(string nextMode, string note)
            {
                if (bar != IntPtr.Zero)
                {
                    EmojiWindowNative.DestroyMenuBar(bar);
                }

                mode = nextMode;
                bar = EmojiWindowNative.CreateMenuBar(stagePanel);
                EmojiWindowNative.SetMenuBarPlacement(bar, x, y, width, height);

                if (mode == "default")
                {
                    AddItem(bar, "文件", MenuFile);
                    AddSub(bar, MenuFile, "对话框", MenuDialog);
                    AddSub(bar, MenuDialog, messageText, MenuMessage);
                    AddSub(bar, MenuDialog, "显示确认框", MenuConfirm);
                    AddSub(bar, MenuFile, "场景文本", MenuScene);
                    AddSub(bar, MenuScene, "运行中", MenuSceneRunning);
                    AddSub(bar, MenuScene, "已完成", MenuSceneDone);
                    AddItem(bar, "布局", MenuLayout);
                }
                else
                {
                    AddItem(bar, "快捷操作", MenuFile);
                    AddSub(bar, MenuFile, "对话框", MenuDialog);
                    AddSub(bar, MenuDialog, messageText, MenuMessage);
                    AddSub(bar, MenuDialog, "显示确认框", MenuConfirm);
                    AddItem(bar, "布局", MenuLayout);
                }

                AddSub(bar, MenuLayout, "靠左 360", MenuLayoutLeft);
                AddSub(bar, MenuLayout, "标准 560", MenuLayoutStd);
                AddSub(bar, MenuLayout, "满宽 900", MenuLayoutWide);
                AddSub(bar, MenuLayout, "下移 28", MenuLayoutDown);
                AddSub(bar, MenuLayout, "顶部归位", MenuLayoutReset);
                AddItem(bar, "工具", MenuTools);
                AddSub(bar, MenuTools, "更新子项文案", MenuToolRename);
                AddSub(bar, MenuTools, "恢复子项文案", MenuToolRestore);
                AddSub(bar, MenuTools, "切换菜单方案", MenuToolToggle);
                AddSub(bar, MenuTools, "刷新状态", MenuToolRefresh);

                EmojiWindowNative.SetMenuBarCallback(bar, menuCallback);
                lastEvent = "MenuBar 已重建为" + (mode == "default" ? "默认三级菜单" : "紧凑菜单");
                PushEvent(lastEvent);
                Refresh(note);
            }

            void HandleMenu(int menuId, int itemId)
            {
                lastMenuId = menuId;
                lastItemId = itemId;

                if (itemId == MenuMessage)
                {
                    scene = "消息框已通过 MenuBar 打开。";
                    detail = "三级子菜单、菜单回调和页面状态回写都已经同步联动。";
                    lastEvent = "菜单项 -> " + messageText;
                    byte[] title = app.U("MenuBar 消息框");
                    byte[] message = app.U("这是从 MenuBar 子菜单打开的 MessageBox。");
                    byte[] icon = app.U("菜单");
                    EmojiWindowNative.show_message_box_bytes(page, title, title.Length, message, message.Length, icon, icon.Length);
                    PushEvent(lastEvent);
                    Refresh("MenuBar 已触发消息框");
                }
                else if (itemId == MenuConfirm)
                {
                    scene = "确认框已通过 MenuBar 打开。";
                    detail = "ConfirmBox 已弹出，当前菜单回调也已经同步回写。";
                    lastEvent = "菜单项 -> 显示确认框";
                    byte[] title = app.U("MenuBar 确认框");
                    byte[] message = app.U("这是从 MenuBar 子菜单打开的 ConfirmBox。");
                    byte[] icon = app.U("菜单");
                    EmojiWindowNative.show_confirm_box_bytes(page, title, title.Length, message, message.Length, icon, icon.Length, confirmCallback);
                    PushEvent(lastEvent);
                    Refresh("MenuBar 已触发确认框");
                }
                else if (itemId == MenuSceneRunning)
                {
                    scene = "运行中 - 菜单栏已回写场景文本。";
                    detail = "这类状态切换更适合直接通过菜单回写页面主状态。";
                    lastEvent = "菜单项 -> 运行中";
                    PushEvent(lastEvent);
                    Refresh("MenuBar 已切换场景为运行中");
                }
                else if (itemId == MenuSceneDone)
                {
                    scene = "已完成 - 菜单栏已回写场景文本。";
                    detail = "一页里只保留 MenuBar 相关动作后，状态层次会比混合演示更清晰。";
                    lastEvent = "菜单项 -> 已完成";
                    PushEvent(lastEvent);
                    Refresh("MenuBar 已切换场景为已完成");
                }
                else if (itemId == MenuLayoutLeft)
                {
                    lastEvent = "菜单项 -> 靠左 360";
                    PushEvent(lastEvent);
                    ApplyPlacement(24, 24, 360, 34, "MenuBar 已切到靠左 360");
                }
                else if (itemId == MenuLayoutStd)
                {
                    lastEvent = "菜单项 -> 标准 560";
                    PushEvent(lastEvent);
                    ApplyPlacement(24, 24, 560, 34, "MenuBar 已切到标准宽度 560");
                }
                else if (itemId == MenuLayoutWide)
                {
                    lastEvent = "菜单项 -> 满宽 900";
                    PushEvent(lastEvent);
                    ApplyPlacement(24, 24, 900, 34, "MenuBar 已切到满宽 900");
                }
                else if (itemId == MenuLayoutDown)
                {
                    lastEvent = "菜单项 -> 下移 28";
                    PushEvent(lastEvent);
                    ApplyPlacement(x, 52, width, height, "MenuBar 已下移 28 像素");
                }
                else if (itemId == MenuLayoutReset)
                {
                    lastEvent = "菜单项 -> 顶部归位";
                    PushEvent(lastEvent);
                    ApplyPlacement(24, 24, mode == "default" ? 760 : 620, 34, "MenuBar 已恢复默认位置");
                }
                else if (itemId == MenuToolRename)
                {
                    UpdateMessageText("打开消息框", "MenuBar 子项文案已改成“打开消息框”");
                }
                else if (itemId == MenuToolRestore)
                {
                    UpdateMessageText("显示消息框", "MenuBar 子项文案已恢复默认");
                }
                else if (itemId == MenuToolToggle)
                {
                    RebuildMenu(mode == "default" ? "compact" : "default", "MenuBar 已切换菜单方案");
                }
                else if (itemId == MenuToolRefresh)
                {
                    lastEvent = "菜单项 -> 刷新状态";
                    PushEvent(lastEvent);
                    Refresh("MenuBar 状态已刷新");
                }
                else
                {
                    lastEvent = $"MenuBar 收到 item_id={itemId}";
                    PushEvent(lastEvent);
                    Refresh("MenuBar 已收到菜单回调");
                }
            }

            menuCallback = app.Pin(new EmojiWindowNative.MenuItemClickCallback(HandleMenu));

            app.Button(1040, 332, 120, 34, "靠左 360", "L", DemoColors.Blue, () =>
            {
                lastEvent = "快捷按钮 -> 靠左 360";
                PushEvent(lastEvent);
                ApplyPlacement(24, 24, 360, 34, "MenuBar 已切到靠左 360");
            }, page);
            app.Button(1172, 332, 120, 34, "标准 560", "S", DemoColors.Green, () =>
            {
                lastEvent = "快捷按钮 -> 标准 560";
                PushEvent(lastEvent);
                ApplyPlacement(24, 24, 560, 34, "MenuBar 已切到标准宽度 560");
            }, page);
            app.Button(1304, 332, 120, 34, "满宽 900", "W", DemoColors.Orange, () =>
            {
                lastEvent = "快捷按钮 -> 满宽 900";
                PushEvent(lastEvent);
                ApplyPlacement(24, 24, 900, 34, "MenuBar 已切到满宽 900");
            }, page);
            app.Button(1040, 376, 120, 34, "下移 28", "D", DemoColors.Purple, () =>
            {
                lastEvent = "快捷按钮 -> 下移 28";
                PushEvent(lastEvent);
                ApplyPlacement(x, 52, width, height, "MenuBar 已下移 28 像素");
            }, page);
            app.Button(1172, 376, 120, 34, "恢复位置", "R", DemoColors.Gray, () =>
            {
                lastEvent = "快捷按钮 -> 恢复位置";
                PushEvent(lastEvent);
                ApplyPlacement(24, 24, mode == "default" ? 760 : 620, 34, "MenuBar 已恢复默认位置");
            }, page);
            app.Button(1304, 376, 120, 34, "改子项文案", "T", DemoColors.Blue, () => UpdateMessageText("打开消息框", "MenuBar 子项文案已改成“打开消息框”"), page);
            app.Button(1040, 420, 120, 34, "恢复文案", "A", DemoColors.Green, () => UpdateMessageText("显示消息框", "MenuBar 子项文案已恢复默认"), page);
            app.Button(1172, 420, 120, 34, "默认菜单", "1", DemoColors.Orange, () => RebuildMenu("default", "MenuBar 已重建为默认三级菜单"), page);
            app.Button(1304, 420, 120, 34, "紧凑菜单", "2", DemoColors.Purple, () => RebuildMenu("compact", "MenuBar 已重建为紧凑菜单"), page);

            void ApplyTheme()
            {
                EmojiWindowNative.SetPanelBackgroundColor(stagePanel, shell.Palette.CardBackground);
            }

            shell.RegisterPageThemeHandler(page, ApplyTheme);
            ApplyTheme();
            RebuildMenu("default", "MenuBar 页面已重排，只保留菜单栏本身和相关操作。");

            _ = stageTip;
            _ = stageFoot;
        }
    }
}
