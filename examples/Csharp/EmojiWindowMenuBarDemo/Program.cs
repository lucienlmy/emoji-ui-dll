using System;
using System.Collections.Generic;

namespace EmojiWindowDemo
{
    internal static class Program
    {
        private static readonly byte[] FontName = EmojiWindowNative.ToUtf8("Microsoft YaHei UI");
        private static readonly Dictionary<int, Action> ButtonActions = new Dictionary<int, Action>();
        private static readonly EmojiWindowNative.ButtonClickCallback ButtonCallback = OnButtonClick;
        private static readonly EmojiWindowNative.MenuItemClickCallback MenuCallback = OnMenuItemClick;

        private static IntPtr _window;
        private static IntPtr _menuBar;
        private static IntPtr _selectedLabel;
        private static IntPtr _summaryLabel;
        private static IntPtr _statusLabel;

        [STAThread]
        private static void Main()
        {
            CreateWindow();
            BuildMenuBar();
            BuildContent();

            EmojiWindowNative.set_button_click_callback(ButtonCallback);
            EmojiWindowNative.SetMenuBarCallback(_menuBar, MenuCallback);
            EmojiWindowNative.set_message_loop_main_window(_window);
            EmojiWindowNative.run_message_loop();
        }

        private static void CreateWindow()
        {
            byte[] title = EmojiWindowNative.ToUtf8("EmojiWindowMenuBarDemo - C# x64");
            _window = EmojiWindowNative.create_window_bytes_ex(
                title,
                title.Length,
                120,
                80,
                920,
                430,
                Color(255, 64, 158, 255),
                Color(255, 245, 247, 250));

            if (_window == IntPtr.Zero)
            {
                throw new InvalidOperationException("Failed to create emoji window.");
            }
        }

        private static void BuildMenuBar()
        {
            _menuBar = EmojiWindowNative.CreateMenuBar(_window);
            EmojiWindowNative.SetMenuBarPlacement(_menuBar, 0, 32, 920, 34);

            AddTopMenu("文件", 100);
            AddTopMenu("编辑", 200);
            AddTopMenu("视图", 300);
            AddTopMenu("帮助", 400);

            AddSubMenu(100, "新建工作区", 101);
            AddSubMenu(100, "打开项目", 102);
            AddSubMenu(100, "导出当前页", 103);
            AddSubMenu(100, "退出", 104);

            AddSubMenu(200, "撤销", 201);
            AddSubMenu(200, "重做", 202);
            AddSubMenu(200, "全选", 203);

            AddSubMenu(300, "显示侧边栏", 301);
            AddSubMenu(300, "切换深色模式", 302);

            AddSubMenu(400, "快捷键说明", 401);
            AddSubMenu(400, "关于 Demo", 402);
        }

        private static void BuildContent()
        {
            CreateLabel(24, 18, 760, 28, "MenuBar 组件示例", Color(255, 48, 49, 51), Transparent(), 18, false);
            CreateLabel(24, 92, 860, 26, "请直接点击窗口顶部的“文件 / 编辑 / 视图 / 帮助”菜单，这里验证的是 menubar 组件，不是组合框。", Color(255, 96, 98, 102), Transparent(), 12, true);

            _selectedLabel = CreateLabel(24, 128, 860, 28, "等待点击顶部菜单项...", Color(255, 48, 49, 51), Transparent(), 13, false);
            _summaryLabel = CreateLabel(24, 162, 860, 44, "当前菜单包含 4 个一级菜单和 11 个子菜单。下方按钮会动态修改其中两个子菜单的文字。", Color(255, 96, 98, 102), Transparent(), 12, true);

            CreateLabel(24, 224, 320, 22, "运行时修改子菜单文字", Color(255, 48, 49, 51), Transparent(), 14, false);
            CreateButton(24, 258, 170, 38, "改“导出当前页”", string.Empty, Color(255, 230, 162, 60), () =>
            {
                UpdateSubItemText(100, 103, "导出为 ZIP 包");
                SetStatus("已将“文件 -> 导出当前页”改为“导出为 ZIP 包”。");
            });

            CreateButton(212, 258, 190, 38, "改“切换深色模式”", string.Empty, Color(255, 103, 194, 58), () =>
            {
                UpdateSubItemText(300, 302, "切换浅色模式");
                SetStatus("已将“视图 -> 切换深色模式”改为“切换浅色模式”。");
            });

            CreateLabel(470, 224, 360, 22, "验证步骤", Color(255, 48, 49, 51), Transparent(), 14, false);
            CreateLabel(470, 258, 380, 74,
                "1. 点击顶部菜单，确认状态栏与“最后一次点击”文本更新。\r\n" +
                "2. 点击左侧两个按钮，再展开对应菜单，确认子项文字已变化。\r\n" +
                "3. 这就是 C# 对 MenuBar 组件的直接运行验证。",
                Color(255, 96, 98, 102),
                Transparent(),
                12,
                true);

            _statusLabel = CreateLabel(24, 374, 860, 24, "状态：等待用户操作。", Color(255, 96, 98, 102), Transparent(), 12, false);
        }

        private static void OnButtonClick(int buttonId, IntPtr parentHwnd)
        {
            if (ButtonActions.TryGetValue(buttonId, out Action action))
            {
                action();
            }
        }

        private static void OnMenuItemClick(int menuId, int itemId)
        {
            string name = ResolveMenuName(itemId);
            SetLabelText(_selectedLabel, string.Format("最后一次点击：menuId={0}, itemId={1}, 文本={2}", menuId, itemId, name));
            SetStatus(string.Format("菜单栏回调成功：menuId={0}, itemId={1}, 文本={2}", menuId, itemId, name));
        }

        private static string ResolveMenuName(int itemId)
        {
            switch (itemId)
            {
                case 101: return "新建工作区";
                case 102: return "打开项目";
                case 103: return "导出当前页";
                case 104: return "退出";
                case 201: return "撤销";
                case 202: return "重做";
                case 203: return "全选";
                case 301: return "显示侧边栏";
                case 302: return "切换深色模式";
                case 401: return "快捷键说明";
                case 402: return "关于 Demo";
                default: return "未知菜单项";
            }
        }

        private static void AddTopMenu(string text, int itemId)
        {
            byte[] bytes = EmojiWindowNative.ToUtf8(text);
            EmojiWindowNative.MenuBarAddItem(_menuBar, bytes, bytes.Length, itemId);
        }

        private static void AddSubMenu(int parentId, string text, int itemId)
        {
            byte[] bytes = EmojiWindowNative.ToUtf8(text);
            EmojiWindowNative.MenuBarAddSubItem(_menuBar, parentId, bytes, bytes.Length, itemId);
        }

        private static void UpdateSubItemText(int parentId, int itemId, string text)
        {
            byte[] bytes = EmojiWindowNative.ToUtf8(text);
            EmojiWindowNative.MenuBarUpdateSubItemText(_menuBar, parentId, itemId, bytes, bytes.Length);
        }

        private static IntPtr CreateLabel(int x, int y, int width, int height, string text, uint fgColor, uint bgColor, int fontSize, bool wrap)
        {
            byte[] textBytes = EmojiWindowNative.ToUtf8(text);
            return EmojiWindowNative.CreateLabel(
                _window,
                x,
                y,
                width,
                height,
                textBytes,
                textBytes.Length,
                fgColor,
                bgColor,
                FontName,
                FontName.Length,
                fontSize,
                0,
                0,
                0,
                0,
                wrap ? 1 : 0);
        }

        private static void SetLabelText(IntPtr handle, string text)
        {
            byte[] bytes = EmojiWindowNative.ToUtf8(text);
            EmojiWindowNative.SetLabelText(handle, bytes, bytes.Length);
        }

        private static int CreateButton(int x, int y, int width, int height, string text, string emoji, uint bgColor, Action onClick)
        {
            byte[] textBytes = EmojiWindowNative.ToUtf8(text);
            byte[] emojiBytes = EmojiWindowNative.ToUtf8(emoji);
            int buttonId = EmojiWindowNative.create_emoji_button_bytes(
                _window,
                emojiBytes,
                emojiBytes.Length,
                textBytes,
                textBytes.Length,
                x,
                y,
                width,
                height,
                bgColor);
            ButtonActions[buttonId] = onClick;
            return buttonId;
        }

        private static void SetStatus(string text)
        {
            SetLabelText(_statusLabel, "状态：" + text);
        }

        private static uint Color(int a, int r, int g, int b)
        {
            return EmojiWindowNative.ARGB(a, r, g, b);
        }

        private static uint Transparent()
        {
            return Color(0, 0, 0, 0);
        }
    }
}
