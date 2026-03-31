using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowPopupMenuDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new PopupMenuDemoApp().Run();
        }
    }

    internal sealed class PopupMenuDemoApp : DemoApp
    {
        private const int OpsGroupX = 18;
        private const int OpsGroupY = 84;
        private const int ButtonInsetX = 10;
        private const int ButtonInsetY = 25;
        private const int ShowMenuButtonX = 24;
        private const int ShowMenuButtonY = 64;
        private const int ShowMenuButtonHeight = 34;
        private const int PopupGap = 4;

        private IntPtr _popupMenu;
        private EmojiWindowNative.MenuItemClickCallback _popupCallback;

        public PopupMenuDemoApp()
            : base("EmojiWindow PopupMenu Demo - C# .NET 4.0", 860, 460)
        {
        }

        protected override void Build()
        {
            CreateHeader("PopupMenu 控件示例", "演示弹出菜单、子菜单和菜单点击回调。");

            _popupMenu = EmojiWindowNative.CreateEmojiPopupMenu(WindowHandle);
            BuildMenu();
            _popupCallback = new EmojiWindowNative.MenuItemClickCallback(OnPopupClick);
            EmojiWindowNative.SetPopupMenuCallback(_popupMenu, _popupCallback);

            IntPtr ops = CreateGroupBox(WindowHandle, "PopupMenu 操作", 18, 84, 820, 220, ColorPrimary);
            AddButton(ops, "📋", "显示菜单", 24, 64, 120, 34, ColorPrimary, ShowPopupMenu);
            AddButton(ops, "✏️", "弹消息框", 158, 64, 120, 34, ColorSuccess, delegate { ShowInfo("PopupMenu", "也可以配合回调再做二次操作。", "🧩"); SetStatus("已弹出消息框。"); });
        }

        private void ShowPopupMenu()
        {
            int popupX = OpsGroupX + ShowMenuButtonX + ButtonInsetX;
            int popupY = OpsGroupY + ShowMenuButtonY + ButtonInsetY + ShowMenuButtonHeight + PopupGap;
            EmojiWindowNative.Point point = EmojiWindowNative.ClientToScreenPoint(WindowHandle, popupX, popupY);
            EmojiWindowNative.ShowContextMenu(_popupMenu, point.X, point.Y);
            SetStatus("已请求显示弹出菜单。");
        }

        private void BuildMenu()
        {
            byte[] refresh = U("刷新");
            byte[] tools = U("工具");
            byte[] export = U("导出");
            byte[] reset = U("重置");
            EmojiWindowNative.PopupMenuAddItem(_popupMenu, refresh, refresh.Length, 101);
            EmojiWindowNative.PopupMenuAddItem(_popupMenu, tools, tools.Length, 200);
            EmojiWindowNative.PopupMenuAddSubItem(_popupMenu, 200, export, export.Length, 201);
            EmojiWindowNative.PopupMenuAddSubItem(_popupMenu, 200, reset, reset.Length, 202);
        }

        private void OnPopupClick(int menuId, int itemId)
        {
            SetStatus("PopupMenu 回调: menuId=" + menuId + ", itemId=" + itemId);
        }
    }
}
