using System;

namespace EmojiWindowDemo
{
    internal static class TabControlDemoPage
    {
        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;

            IntPtr stageBox = app.GroupBox(16, 16, 1000, 520, "🗂️ TabControl 舞台", DemoTheme.Border, DemoTheme.Background, page);
            IntPtr sideBox = app.GroupBox(1032, 16, 432, 520, "📍 状态 / 快捷操作", DemoTheme.Border, DemoTheme.Background, page);
            IntPtr apiBox = app.GroupBox(16, 558, 1448, 172, "📘 TabControl API 说明", DemoTheme.Border, DemoTheme.Background, page);

            IntPtr intro = app.Label(40, 54, 940, 24, "这一页只保留 TabControl 本体：左侧是标签页舞台，右侧集中做状态读取与快捷操作。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr tab = EmojiWindowNative.CreateTabControl(page, 40, 96, 940, 420);
            EmojiWindowNative.SetTabItemSize(tab, 140, 38);
            EmojiWindowNative.SetTabPadding(tab, 18, 10);
            EmojiWindowNative.SetTabClosable(tab, 1);
            EmojiWindowNative.SetTabScrollable(tab, 1);
            EmojiWindowNative.SetTabAlignment(tab, 0);
            EmojiWindowNative.SetTabHeaderStyle(tab, 1);

            IntPtr readout = app.Label(1056, 84, 360, 96, string.Empty, DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr stateLabel = app.Label(1056, 196, 360, 24, "TabControl 页状态会显示在这里。", DemoTheme.Primary, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            IntPtr sideTip = app.Label(1056, 232, 360, 44, "手动按钮和标签头关闭按钮现在共用同一套删除逻辑，避免状态刷新和实际删除不同步。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);

            IntPtr api1 = app.Label(40, 592, 1320, 22, "1. CreateTabControl / AddTabItem / GetTabContentWindow：创建标签页并挂载独立内容区。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            IntPtr api2 = app.Label(40, 624, 1320, 22, "2. SetTabCallback / SetTabCloseCallback / SelectTab / RemoveTabItem：切换和关闭标签并回写状态。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            IntPtr api3 = app.Label(40, 656, 1320, 22, "3. SetTabClosable / SetTabScrollable / SetTabAlignment / SetTabHeaderStyle：切换关闭按钮、滚动、对齐和头部样式。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            app.AttachToGroup(stageBox, intro);
            app.AttachToGroup(sideBox, readout, stateLabel, sideTip);
            app.AttachToGroup(apiBox, api1, api2, api3);

            int tabCounter = 0;
            bool closable = true;
            bool scrollable = true;
            int alignment = 0;
            bool suppressCloseCallback = false;

            void ApplyTabTheme()
            {
                DemoThemePalette palette = shell.Palette;
                uint selectedBg = palette.Dark ? EmojiWindowNative.ARGB(255, 36, 44, 58) : palette.CardBackground;
                uint unselectedBg = palette.Dark ? EmojiWindowNative.ARGB(255, 245, 247, 250) : EmojiWindowNative.ARGB(255, 245, 247, 250);
                uint selectedText = palette.Dark ? DemoColors.White : palette.Text;
                uint unselectedText = palette.Dark ? palette.Muted : DemoColors.Gray;
                EmojiWindowNative.SetTabColors(tab, selectedBg, unselectedBg, selectedText, unselectedText);
                EmojiWindowNative.SetTabIndicatorColor(tab, palette.Accent);
            }

            int AddTab(string title, string body)
            {
                byte[] titleBytes = app.U(title);
                int index = EmojiWindowNative.AddTabItem(tab, titleBytes, titleBytes.Length, IntPtr.Zero);
                IntPtr content = EmojiWindowNative.GetTabContentWindow(tab, index);
                app.Label(24, 24, 560, 30, title + " 内容区", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, content);
                app.Label(24, 64, 720, 60, body, DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, content);
                tabCounter = Math.Max(tabCounter, index + 1);
                return index;
            }

            void Refresh(string note)
            {
                int count = EmojiWindowNative.GetTabCount(tab);
                int current = EmojiWindowNative.GetCurrentTabIndex(tab);
                shell.SetLabelText(readout, $"count={count}  current={current}\r\nclosable={closable}  scrollable={scrollable}  alignment={alignment}\r\n{note}");
                shell.SetLabelText(stateLabel, note);
                shell.SetStatus(note);
            }

            bool TryRemoveTab(int index, string note)
            {
                int count = EmojiWindowNative.GetTabCount(tab);
                if (count <= 1 || index < 0 || index >= count)
                {
                    Refresh("至少保留一个标签页");
                    return false;
                }

                suppressCloseCallback = true;
                try
                {
                    EmojiWindowNative.RemoveTabItem(tab, index);
                }
                finally
                {
                    suppressCloseCallback = false;
                }

                Refresh(note + ": index=" + index);
                return true;
            }

            AddTab("首页", "这里验证 TabControl 可以正常创建内容窗口、添加标签和切换标签。");
            AddTab("设置", "这一页用于测试标签切换、头部样式切换和关闭按钮。");
            AddTab("收藏", "这里保留独立标签页内容，方便做多页切换回归。");

            var callback = app.Pin(new EmojiWindowNative.TabCallback((_, selectedIndex) => Refresh("Tab 切换回调: index=" + selectedIndex)));
            var closeCallback = app.Pin(new EmojiWindowNative.TabCloseCallback((_, index) =>
            {
                if (suppressCloseCallback)
                {
                    return;
                }

                TryRemoveTab(index, "已点击关闭按钮移除标签");
            }));
            EmojiWindowNative.SetTabCallback(tab, callback);
            EmojiWindowNative.SetTabCloseCallback(tab, closeCallback);
            EmojiWindowNative.SelectTab(tab, 0);

            app.Button(1056, 300, 160, 34, "新增标签", "➕", DemoColors.Green, () =>
            {
                int index = AddTab("新标签 " + (++tabCounter), "运行时动态创建的新标签内容区。");
                EmojiWindowNative.SelectTab(tab, index);
                Refresh("已新增并切换到新标签");
            }, page);
            app.Button(1232, 300, 160, 34, "关闭当前", "🗌", DemoColors.Red, () =>
            {
                int index = EmojiWindowNative.GetCurrentTabIndex(tab);
                TryRemoveTab(index, "已关闭当前标签");
            }, page);
            app.Button(1056, 344, 160, 34, "切到下一页", "➡️", DemoColors.Blue, () =>
            {
                int count = EmojiWindowNative.GetTabCount(tab);
                int current = EmojiWindowNative.GetCurrentTabIndex(tab);
                if (count > 0)
                {
                    EmojiWindowNative.SelectTab(tab, (current + 1) % count);
                }

                Refresh("已切换到下一页");
            }, page);
            app.Button(1232, 344, 160, 34, "切到第 1 页", "1", DemoColors.Orange, () =>
            {
                EmojiWindowNative.SelectTab(tab, 0);
                Refresh("已切换到第 1 页");
            }, page);

            app.Button(1056, 388, 160, 34, "关闭按钮开关", "✅", DemoColors.Purple, () =>
            {
                closable = !closable;
                EmojiWindowNative.SetTabClosable(tab, closable ? 1 : 0);
                Refresh(closable ? "已开启标签关闭按钮" : "已关闭标签关闭按钮");
            }, page);
            app.Button(1232, 388, 160, 34, "滚动开关", "↔️", DemoColors.Gray, () =>
            {
                scrollable = !scrollable;
                EmojiWindowNative.SetTabScrollable(tab, scrollable ? 1 : 0);
                Refresh(scrollable ? "已开启标签滚动" : "已关闭标签滚动");
            }, page);
            app.Button(1056, 432, 160, 34, "左对齐", "L", DemoColors.Blue, () =>
            {
                alignment = 0;
                EmojiWindowNative.SetTabAlignment(tab, alignment);
                Refresh("标签头已切到左对齐");
            }, page);
            app.Button(1232, 432, 160, 34, "居中对齐", "C", DemoColors.Green, () =>
            {
                alignment = 1;
                EmojiWindowNative.SetTabAlignment(tab, alignment);
                Refresh("标签头已切到居中对齐");
            }, page);

            app.Button(1056, 476, 108, 34, "Line", "━", DemoColors.Gray, () =>
            {
                EmojiWindowNative.SetTabHeaderStyle(tab, 0);
                Refresh("Tab 头部样式已切到 Line");
            }, page);
            app.Button(1172, 476, 108, 34, "Card", "▣", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetTabHeaderStyle(tab, 1);
                Refresh("Tab 头部样式已切到 Card");
            }, page);
            app.Button(1288, 476, 108, 34, "刷新主题", "🎨", DemoColors.Orange, () =>
            {
                ApplyTabTheme();
                Refresh("Tab 头部配色已按当前主题刷新");
            }, page);

            shell.RegisterPageThemeHandler(page, ApplyTabTheme);
            ApplyTabTheme();
            Refresh("TabControl 页面已统一到 Python 版的操作反馈逻辑。");
        }
    }
}
