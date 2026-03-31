using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowMenuBarDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new MenuBarDemoApp().Run();
        }
    }

    internal sealed class MenuBarDemoApp : DemoApp
    {
        private IntPtr _menuBar;
        private EmojiWindowNative.MenuItemClickCallback _menuCallback;

        public MenuBarDemoApp()
            : base("EmojiWindow MenuBar Demo - C# .NET 4.0", 900, 460)
        {
        }

        protected override void Build()
        {
            CreateHeader("MenuBar 控件示例", "演示菜单栏创建、子项回调和子项文案更新。");

            _menuBar = EmojiWindowNative.CreateMenuBar(WindowHandle);
            EmojiWindowNative.SetMenuBarPlacement(_menuBar, 18, 86, 620, 36);
            AddMenus();

            _menuCallback = new EmojiWindowNative.MenuItemClickCallback(OnMenuClick);
            EmojiWindowNative.SetMenuBarCallback(_menuBar, _menuCallback);

            IntPtr ops = CreateGroupBox(WindowHandle, "MenuBar 操作", 18, 154, 860, 200, ColorPrimary);
            AddButton(ops, "✏️", "改“刷新”文案", 24, 52, 140, 34, ColorPrimary, UpdateRefreshText);
            AddButton(ops, "💬", "弹消息框", 178, 52, 120, 34, ColorSuccess, delegate { ShowInfo("MenuBar", "这是菜单栏 demo 触发的消息框。", "📋"); SetStatus("已弹出消息框。"); });
        }

        private void AddMenus()
        {
            byte[] file = U("文件");
            byte[] view = U("视图");
            EmojiWindowNative.MenuBarAddItem(_menuBar, file, file.Length, 100);
            EmojiWindowNative.MenuBarAddItem(_menuBar, view, view.Length, 200);

            byte[] open = U("打开");
            byte[] refresh = U("刷新");
            byte[] sidebar = U("侧栏");
            EmojiWindowNative.MenuBarAddSubItem(_menuBar, 100, open, open.Length, 101);
            EmojiWindowNative.MenuBarAddSubItem(_menuBar, 100, refresh, refresh.Length, 102);
            EmojiWindowNative.MenuBarAddSubItem(_menuBar, 200, sidebar, sidebar.Length, 201);
        }

        private void UpdateRefreshText()
        {
            byte[] text = U("立即刷新");
            EmojiWindowNative.MenuBarUpdateSubItemText(_menuBar, 100, 102, text, text.Length);
            SetStatus("菜单子项文案已更新。");
        }

        private void OnMenuClick(int menuId, int itemId)
        {
            SetStatus("MenuBar 回调: menuId=" + menuId + ", itemId=" + itemId);
        }
    }
}
