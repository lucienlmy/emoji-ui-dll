using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowTreeViewDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new TreeViewDemoApp().Run();
        }
    }

    internal sealed class TreeViewDemoApp : DemoApp
    {
        private IntPtr _tree;
        private int _rootA;
        private int _rootB;
        private int _childA1;
        private EmojiWindowNative.TreeViewCallback _treeCallback;

        public TreeViewDemoApp()
            : base("EmojiWindow TreeView Demo - C# .NET 4.0", 940, 580)
        {
        }

        protected override void Build()
        {
            const int stageX = 18;
            const int stageY = 84;
            const int treeOffsetX = 18;
            const int treeOffsetY = 44;
            const int groupContentLeft = 10;
            const int groupContentTop = 25;

            CreateHeader("TreeView 控件示例", "演示树节点添加、展开折叠、选中以及侧栏样式。");

            IntPtr stage = CreateGroupBox(WindowHandle, "TreeView 舞台", stageX, stageY, 420, 440, ColorPrimary);
            IntPtr host = CreatePanel(
                WindowHandle,
                stageX + groupContentLeft + treeOffsetX,
                stageY + groupContentTop + treeOffsetY,
                360,
                340,
                ColorWhite);
            EmojiWindowNative.AddChildToGroup(stage, host);
            _tree = EmojiWindowNative.CreateTreeView(host, 0, 0, 360, 340, ColorWhite, ColorText, IntPtr.Zero);
            ConfigureTreeView();
            SeedTree();

            _treeCallback = new EmojiWindowNative.TreeViewCallback(OnTreeSelected);
            EmojiWindowNative.SetTreeViewCallback(_tree, EmojiWindowNative.TreeCallbackNodeSelected, _treeCallback);

            IntPtr ops = CreateGroupBox(WindowHandle, "TreeView 操作", 458, 84, 450, 440, ColorSuccess);
            AddButton(ops, "📨", "展开全部", 24, 48, 110, 34, ColorPrimary, delegate
            {
                EmojiWindowNative.ExpandAll(_tree);
                SetStatus("已展开全部节点。");
            });
            AddButton(ops, "📧", "折叠全部", 148, 48, 110, 34, ColorSuccess, delegate
            {
                EmojiWindowNative.CollapseAll(_tree);
                SetStatus("已折叠全部节点。");
            });
            AddButton(ops, "🎯", "选中子节点", 272, 48, 126, 34, ColorWarning, delegate
            {
                EmojiWindowNative.SetSelectedNode(_tree, _childA1);
                SetStatus("已选中子节点。");
            });
            AddButton(ops, "✏️", "修改子节点文案", 24, 96, 126, 34, ColorDanger, RenameNode);
            AddButton(ops, "🧭", "切换侧栏模式", 164, 96, 126, 34, ColorPrimary, ToggleSidebarMode);
            AddButton(ops, "✅", "切换复选状态", 304, 96, 126, 34, ColorSuccess, ToggleNodeCheck);
        }

        private void ConfigureTreeView()
        {
            EmojiWindowNative.SetTreeViewSidebarMode(_tree, true);
            EmojiWindowNative.SetTreeViewRowHeight(_tree, 38.0f);
            EmojiWindowNative.SetTreeViewItemSpacing(_tree, 6.0f);
            EmojiWindowNative.SetTreeViewTextColor(_tree, ColorText);
            EmojiWindowNative.SetTreeViewSelectedBgColor(_tree, ColorPrimary);
            EmojiWindowNative.SetTreeViewSelectedForeColor(_tree, ColorWhite);
            EmojiWindowNative.SetTreeViewHoverBgColor(_tree, EmojiWindowNative.ARGB(255, 234, 243, 255));
            EmojiWindowNative.SetTreeViewFont(_tree, FontYaHei, FontYaHei.Length, 13.0f, 500, false);
            EmojiWindowNative.EnableTreeViewDragDrop(_tree, false);
        }

        private void SeedTree()
        {
            _rootA = AddNode(_tree, "基础控件", "📚");
            _childA1 = AddChild(_tree, _rootA, "按钮示例", "🔇");
            AddChild(_tree, _rootA, "输入框示例", "⌨️");

            _rootB = AddNode(_tree, "高级控件", "🧩");
            AddChild(_tree, _rootB, "菜单示例", "📵");
            AddChild(_tree, _rootB, "表格示例", "📳");

            EmojiWindowNative.SetSelectedNode(_tree, _childA1);
            EmojiWindowNative.ExpandAll(_tree);
        }

        private int AddNode(IntPtr tree, string text, string icon)
        {
            byte[] textBytes = U(text);
            byte[] iconBytes = U(icon);
            return EmojiWindowNative.AddRootNode(tree, textBytes, textBytes.Length, iconBytes, iconBytes.Length);
        }

        private int AddChild(IntPtr tree, int parentId, string text, string icon)
        {
            byte[] textBytes = U(text);
            byte[] iconBytes = U(icon);
            return EmojiWindowNative.AddChildNode(tree, parentId, textBytes, textBytes.Length, iconBytes, iconBytes.Length);
        }

        private void RenameNode()
        {
            byte[] text = U("按钮示例（已改名）");
            EmojiWindowNative.SetNodeText(_tree, _childA1, text, text.Length);
            SetStatus("子节点文案已更新。");
        }

        private void ToggleSidebarMode()
        {
            bool enabled = EmojiWindowNative.GetTreeViewSidebarMode(_tree);
            EmojiWindowNative.SetTreeViewSidebarMode(_tree, !enabled);
            SetStatus("TreeView 侧栏模式 = " + (!enabled));
        }

        private void ToggleNodeCheck()
        {
            bool checkedState = EmojiWindowNative.GetNodeChecked(_tree, _childA1);
            EmojiWindowNative.SetNodeChecked(_tree, _childA1, !checkedState);
            SetStatus("子节点复选状态 = " + (!checkedState));
        }

        private void OnTreeSelected(int nodeId, IntPtr context)
        {
            SetStatus("TreeView 回调: nodeId=" + nodeId);
        }
    }
}
