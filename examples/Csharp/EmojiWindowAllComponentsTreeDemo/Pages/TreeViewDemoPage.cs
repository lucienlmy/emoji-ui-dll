using System;

namespace EmojiWindowDemo
{
    internal static class TreeViewDemoPage
    {
        private const int CallbackNodeSelected = 1;

        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;
            byte[] font = app.U("Microsoft YaHei UI");

            app.GroupBox(16, 16, 420, 136, "TreeView 页面说明", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(460, 16, 1004, 136, "当前页能力", DemoTheme.Border, DemoTheme.Background, page);
            IntPtr content = app.Panel(16, 170, 1448, 650, DemoTheme.Surface, page);

            app.Label(34, 58, 382, 56, "TreeView 页不再只是一个孤立的树控件，而是带上状态读取、节点操作、样式切换和回调回写。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            app.Label(484, 58, 940, 42, "左侧是树舞台，右侧是状态、最近回调和快捷动作。可以直接验证展开折叠、侧边栏模式、多级节点和节点文本更新。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);

            IntPtr treePanel = app.Panel(24, 24, 560, 586, DemoTheme.Surface, content);
            IntPtr sidePanel = app.Panel(608, 24, 816, 586, DemoTheme.Surface, content);
            IntPtr tree = EmojiWindowNative.CreateTreeView(treePanel, 18, 56, 524, 512, shell.Palette.TreeBackground, shell.Palette.Text, IntPtr.Zero);

            bool sidebarMode = true;
            float rowHeight = 32f;
            float spacing = 6f;
            bool warmHover = false;
            string lastEvent = "尚未触发节点回调。";
            IntPtr detailLabel = IntPtr.Zero;

            int AddRoot(string title, string icon)
            {
                byte[] titleBytes = app.U(title);
                byte[] iconBytes = app.U(icon);
                return EmojiWindowNative.AddRootNode(tree, titleBytes, titleBytes.Length, iconBytes, iconBytes.Length);
            }

            int AddChild(int parentId, string title, string icon)
            {
                byte[] titleBytes = app.U(title);
                byte[] iconBytes = app.U(icon);
                return EmojiWindowNative.AddChildNode(tree, parentId, titleBytes, titleBytes.Length, iconBytes, iconBytes.Length);
            }

            void ApplyTreeTheme()
            {
                DemoThemePalette palette = shell.Palette;
                EmojiWindowNative.SetPanelBackgroundColor(content, palette.CardBackground);
                EmojiWindowNative.SetPanelBackgroundColor(treePanel, palette.CardBackground);
                EmojiWindowNative.SetPanelBackgroundColor(sidePanel, palette.CardBackground);
                EmojiWindowNative.SetTreeViewBackgroundColor(tree, palette.TreeBackground);
                EmojiWindowNative.SetTreeViewTextColor(tree, palette.Text);
                EmojiWindowNative.SetTreeViewSelectedBgColor(tree, DemoColors.Blue);
                EmojiWindowNative.SetTreeViewSelectedForeColor(tree, DemoColors.White);
                EmojiWindowNative.SetTreeViewHoverBgColor(tree, warmHover ? DemoColors.Yellow : palette.TreeHoverBackground);
                if (detailLabel != IntPtr.Zero)
                {
                    shell.SetLabelText(detailLabel, palette.Dark
                        ? "深色主题下重点验证多级节点、回调、运行时改文本以及侧边栏样式是否仍然清晰。"
                        : "浅色主题下重点验证多级节点、回调、运行时改文本以及侧边栏样式是否仍然清晰。");
                }
            }

            EmojiWindowNative.SetTreeViewSidebarMode(tree, 1);
            EmojiWindowNative.SetTreeViewRowHeight(tree, rowHeight);
            EmojiWindowNative.SetTreeViewItemSpacing(tree, spacing);
            EmojiWindowNative.SetTreeViewFont(tree, font, font.Length, 13f, 500, 0);
            EmojiWindowNative.EnableTreeViewDragDrop(tree, 0);

            int rootWorkspace = AddRoot("工作区", "📁");
            int rootBookmarks = AddRoot("书签", "⭐");
            int rootSystem = AddRoot("系统", "⚙");

            int nodeBrowser = AddChild(rootWorkspace, "多标签浏览器", "🌐");
            int nodeControls = AddChild(rootWorkspace, "控件示例", "🧩");
            int nodeTasks = AddChild(rootWorkspace, "测试任务", "📋");
            int nodeOpenAi = AddChild(rootBookmarks, "OpenAI", "🤖");
            AddChild(rootBookmarks, "接口文档", "📘");
            AddChild(rootSystem, "主题设置", "🎨");
            AddChild(rootSystem, "调试日志", "📝");
            AddChild(nodeControls, "Button / Label / EditBox", "🔘");
            AddChild(nodeControls, "DataGrid / ListBox / ComboBox", "🧾");
            AddChild(nodeTasks, "验证冻结首列 / 首行", "✅");
            EmojiWindowNative.SetNodeChecked(tree, nodeControls, 1);
            EmojiWindowNative.SetNodeChecked(tree, nodeTasks, 1);
            EmojiWindowNative.ExpandAll(tree);
            EmojiWindowNative.SetSelectedNode(tree, nodeControls);

            app.Label(18, 16, 500, 24, "Tree 舞台", DemoTheme.Text, DemoTheme.Surface, 14, PageCommon.AlignLeft, false, treePanel);
            IntPtr statusLabel = app.Label(18, 16, 760, 24, "等待 TreeView 动作。", DemoTheme.Primary, DemoTheme.Surface, 13, PageCommon.AlignLeft, false, sidePanel);
            IntPtr readoutLabel = app.Label(18, 56, 760, 120, "等待读取 TreeView 状态。", DemoTheme.Text, DemoTheme.Surface, 12, PageCommon.AlignLeft, true, sidePanel);
            IntPtr callbackLabel = app.Label(18, 202, 760, 84, "等待触发 TreeView 回调。", DemoTheme.Muted, DemoTheme.Surface, 12, PageCommon.AlignLeft, true, sidePanel);
            detailLabel = app.Label(18, 520, 760, 44, "TreeView 这一页重点是验证多级节点、回调、运行时改文本以及侧边栏样式是否一起正常。", DemoTheme.Muted, DemoTheme.Surface, 12, PageCommon.AlignLeft, true, sidePanel);

            void Refresh(string note)
            {
                int current = EmojiWindowNative.GetSelectedNode(tree);
                string currentText = current > 0 ? shell.ReadTreeNodeText(tree, current) : "(无选中)";
                shell.SetLabelText(
                    readoutLabel,
                    $"当前节点={currentText}\r\n" +
                    $"sidebar_mode={(sidebarMode ? "ON" : "OFF")}  row_height={rowHeight:0}  spacing={spacing:0}\r\n" +
                    "右侧按钮会直接改树状态、选中项和节点文本。");
                shell.SetLabelText(callbackLabel, lastEvent);
                shell.SetLabelText(statusLabel, note);
                shell.SetStatus(note);
            }

            var callback = app.Pin(new EmojiWindowNative.TreeNodeCallback((nodeId, _) =>
            {
                string text = shell.ReadTreeNodeText(tree, nodeId);
                lastEvent = "节点回调 -> " + text;
                Refresh("TreeView -> 已选中 " + text);
            }));
            EmojiWindowNative.SetTreeViewCallback(tree, CallbackNodeSelected, callback);

            app.Button(18, 314, 150, 38, "全部展开", "E", DemoColors.Blue, () =>
            {
                EmojiWindowNative.ExpandAll(tree);
                Refresh("TreeView -> 已展开全部节点");
            }, sidePanel);
            app.Button(184, 314, 150, 38, "全部折叠", "C", DemoColors.Orange, () =>
            {
                EmojiWindowNative.CollapseAll(tree);
                Refresh("TreeView -> 已折叠全部节点");
            }, sidePanel);
            app.Button(350, 314, 182, 38, "选中控件示例", "S", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetSelectedNode(tree, nodeControls);
                EmojiWindowNative.ScrollToNode(tree, nodeControls);
                lastEvent = "按钮动作 -> 已跳转到 控件示例";
                Refresh("TreeView -> 已选中“控件示例”");
            }, sidePanel);
            app.Button(548, 314, 214, 38, "改浏览器节点文本", "T", DemoColors.Red, () =>
            {
                byte[] text = app.U("多标签浏览器 Demo");
                EmojiWindowNative.SetNodeText(tree, nodeBrowser, text, text.Length);
                lastEvent = "按钮动作 -> 浏览器节点已重命名";
                Refresh("TreeView -> 树节点文本已修改");
            }, sidePanel);

            app.Button(18, 368, 150, 38, "跳到 OpenAI", "O", DemoColors.Purple, () =>
            {
                EmojiWindowNative.SetSelectedNode(tree, nodeOpenAi);
                EmojiWindowNative.ScrollToNode(tree, nodeOpenAi);
                lastEvent = "按钮动作 -> 已跳转到 OpenAI";
                Refresh("TreeView -> 已定位到 OpenAI 节点");
            }, sidePanel);
            app.Button(184, 368, 150, 38, "切换 Sidebar", "B", DemoColors.Gray, () =>
            {
                sidebarMode = !sidebarMode;
                EmojiWindowNative.SetTreeViewSidebarMode(tree, sidebarMode ? 1 : 0);
                Refresh("TreeView -> Sidebar 模式已切换");
            }, sidePanel);
            app.Button(350, 368, 182, 38, "加高行高", "H", DemoColors.Green, () =>
            {
                rowHeight = rowHeight >= 40f ? 32f : 40f;
                EmojiWindowNative.SetTreeViewRowHeight(tree, rowHeight);
                Refresh("TreeView -> 行高已切换");
            }, sidePanel);
            app.Button(548, 368, 214, 38, "切换间距", "G", DemoColors.Blue, () =>
            {
                spacing = spacing >= 10f ? 6f : 10f;
                EmojiWindowNative.SetTreeViewItemSpacing(tree, spacing);
                Refresh("TreeView -> 节点间距已切换");
            }, sidePanel);

            app.Button(18, 422, 150, 38, "主题悬停", "T", DemoColors.Blue, () =>
            {
                warmHover = false;
                ApplyTreeTheme();
                Refresh("TreeView -> Hover 背景已切回主题方案");
            }, sidePanel);
            app.Button(184, 422, 150, 38, "暖色悬停", "W", DemoColors.Orange, () =>
            {
                warmHover = true;
                ApplyTreeTheme();
                Refresh("TreeView -> Hover 背景已切到暖色");
            }, sidePanel);
            app.Button(350, 422, 182, 38, "恢复默认选中", "R", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetTreeViewSelectedBgColor(tree, DemoColors.Blue);
                EmojiWindowNative.SetTreeViewSelectedForeColor(tree, DemoColors.White);
                Refresh("TreeView -> 选中颜色已恢复默认");
            }, sidePanel);
            app.Button(548, 422, 214, 38, "系统节点改名", "N", DemoColors.Purple, () =>
            {
                byte[] text = app.U("系统 / 偏好设置");
                EmojiWindowNative.SetNodeText(tree, rootSystem, text, text.Length);
                lastEvent = "按钮动作 -> 系统根节点已改名";
                Refresh("TreeView -> 根节点文本已修改");
            }, sidePanel);

            shell.RegisterPageThemeHandler(page, ApplyTreeTheme);
            ApplyTreeTheme();
            Refresh("TreeView 页面已加载，可直接测试展开 / 折叠 / 侧边栏与节点回调。");
        }
    }
}
