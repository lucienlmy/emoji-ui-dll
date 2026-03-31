using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;
using System.Runtime.InteropServices;
using System.Text;

namespace EmojiWindowTabControlDemo
{
    internal sealed class TabPageModel
    {
        public string Title;
        public IntPtr ContentWindow;
        public int TitleLabel;
        public int DescLabel;
        public int ButtonId;
        public bool HasIcon;
        public int ColorIndex;
    }

    internal static class Program
    {
        private const int TabHeaderStyleLine = 0;
        private const int TabHeaderStyleCard = 1;
        private const int TabHeaderStyleCardPlain = 2;
        private const int TabHeaderStyleSegmented = 3;
        private const int AlignLeft = 0;
        private const int AlignCenter = 1;
        private const int AlignRight = 2;
        private const int PositionTop = 0;
        private const int PositionBottom = 1;
        private const int PositionLeft = 2;
        private const int PositionRight = 3;
        private const int WindowWidth = 1600;
        private const int WindowHeight = 980;

        private static readonly byte[] FontYaHei = EmojiWindowNative.ToUtf8("Microsoft YaHei UI");
        private static readonly byte[] FontSegoe = EmojiWindowNative.ToUtf8("Segoe UI");
        private static readonly List<string> LogLines = new List<string>();
        private static readonly Dictionary<int, Action> ButtonActions = new Dictionary<int, Action>();
        private static readonly List<TabPageModel> MainPages = new List<TabPageModel>();
        private static readonly List<TabPageModel> StylePages = new List<TabPageModel>();
        private static readonly List<TabPageModel> StatePages = new List<TabPageModel>();
        private static readonly uint[] ContentColors = new uint[]
        {
            EmojiWindowNative.ARGB(255, 248, 250, 252),
            EmojiWindowNative.ARGB(255, 240, 249, 235),
            EmojiWindowNative.ARGB(255, 255, 247, 237),
            EmojiWindowNative.ARGB(255, 243, 244, 246),
            EmojiWindowNative.ARGB(255, 239, 246, 255),
            EmojiWindowNative.ARGB(255, 254, 242, 242)
        };

        private static IntPtr _mainWindow = IntPtr.Zero;
        private static IntPtr _mainTab = IntPtr.Zero;
        private static IntPtr _styleTab = IntPtr.Zero;
        private static IntPtr _stateTab = IntPtr.Zero;
        private static IntPtr _popupMenu = IntPtr.Zero;
        private static int _statusLabel;
        private static int _logEdit;

        private static int _stylePreviewLeft = 980;
        private static int _stylePreviewTop = 506;
        private static int _stylePreviewWidth = 580;
        private static int _stylePreviewHeight = 160;
        private static int _statePreviewLeft = 980;
        private static int _statePreviewTop = 732;
        private static int _statePreviewWidth = 580;
        private static int _statePreviewHeight = 150;
        private static int _stateOriginalLeft;
        private static int _stateOriginalTop;
        private static int _stateOriginalWidth;
        private static int _stateOriginalHeight;

        private static bool _mainClosable = true;
        private static bool _mainDraggable = true;
        private static bool _styleScrollable = false;
        private static bool _styleRoomy = true;
        private static bool _stylePaletteAlt = false;
        private static bool _mainPaletteAlt = false;
        private static bool _stateVisible = true;
        private static bool _stateEnabled = true;
        private static bool _stateMoved = false;
        private static bool _thirdPageVisible = true;
        private static int _styleFontSize = 14;
        private static int _pageSeed = 0;
        private static int _renameSeed = 0;
        private static byte[][] _tabIcons;

        private static EmojiWindowNative.ButtonClickCallback _buttonClickCallback;
        private static EmojiWindowNative.TabCallback _tabCallback;
        private static EmojiWindowNative.TabCloseCallback _tabCloseCallback;
        private static EmojiWindowNative.TabRightClickCallback _tabRightClickCallback;
        private static EmojiWindowNative.TabDoubleClickCallback _tabDoubleClickCallback;
        private static EmojiWindowNative.WindowResizeCallback _windowResizeCallback;

        [DllImport("user32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        private static extern IntPtr CreatePopupMenu();

        [DllImport("user32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern bool AppendMenuW(IntPtr hMenu, uint uFlags, UIntPtr uIDNewItem, string lpNewItem);

        [DllImport("user32.dll", SetLastError = true)]
        private static extern int TrackPopupMenu(IntPtr hMenu, uint uFlags, int x, int y, int nReserved, IntPtr hWnd, IntPtr prcRect);

        [DllImport("user32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern bool SetForegroundWindow(IntPtr hWnd);

        private static uint White { get { return EmojiWindowNative.ARGB(255, 255, 255, 255); } }
        private static uint Black { get { return EmojiWindowNative.ARGB(255, 32, 33, 36); } }
        private static uint Gray { get { return EmojiWindowNative.ARGB(255, 96, 98, 102); } }
        private static uint LightGray { get { return EmojiWindowNative.ARGB(255, 245, 247, 250); } }
        private static uint BorderBlue { get { return EmojiWindowNative.ARGB(255, 64, 158, 255); } }
        private static uint BorderGreen { get { return EmojiWindowNative.ARGB(255, 103, 194, 58); } }
        private static uint BorderOrange { get { return EmojiWindowNative.ARGB(255, 230, 162, 60); } }
        private static uint BorderRed { get { return EmojiWindowNative.ARGB(255, 245, 108, 108); } }
        private static uint BorderPurple { get { return EmojiWindowNative.ARGB(255, 142, 68, 173); } }

        [STAThread]
        private static void Main()
        {
            InitializeIcons();
            CreateWindow();
            CreateStaticLayout();
            CreateMainDemoTab();
            CreateStylePreviewTab();
            CreateStatePreviewTab();
            InstallCallbacks();
            CreatePopup();
            SetStatus("TabControl .NET 4.0 示例已启动：右键主页签可弹菜单，双击页签可重命名。");
            AppendLog("已创建 3 个 TabControl：主页、样式预览、状态预览。");
            EmojiWindowNative.set_message_loop_main_window(_mainWindow);
            EmojiWindowNative.run_message_loop();
        }

        private static void InitializeIcons()
        {
            _tabIcons = new byte[][]
            {
                CreateIconBytes(Color.FromArgb(64, 158, 255)),
                CreateIconBytes(Color.FromArgb(103, 194, 58)),
                CreateIconBytes(Color.FromArgb(230, 162, 60)),
                CreateIconBytes(Color.FromArgb(245, 108, 108))
            };
        }

        private static void CreateWindow()
        {
            byte[] title = EmojiWindowNative.ToUtf8("🗂️ TabControl 全功能示例 - C# / .NET Framework 4.0");
            _mainWindow = EmojiWindowNative.create_window_bytes_ex(
                title,
                title.Length,
                -1,
                -1,
                WindowWidth,
                WindowHeight,
                EmojiWindowNative.ARGB(255, 36, 41, 47),
                EmojiWindowNative.ARGB(255, 250, 250, 252));

            if (_mainWindow == IntPtr.Zero)
            {
                Console.WriteLine("创建窗口失败。");
                Environment.Exit(1);
            }
        }

        private static void CreateStaticLayout()
        {
            CreateLabel(_mainWindow, "🧭 这个 demo 覆盖 TabControl 的样式、布局、单页控制、批量操作、增强交互和状态查询。", 16, 10, 1550, 28, Black, LightGray, 14, true, false);
            _statusLabel = CreateLabel(_mainWindow, "初始化中...", 16, 42, 1550, 28, Gray, White, 12, false, false);
            CreateGroupBox(_mainWindow, "🗂️ 主 TabControl（关闭 / 右键 / 双击 / 拖拽 / 批量操作）", 16, 80, 930, 552, BorderBlue);
            CreateGroupBox(_mainWindow, "🛠️ 样式 / 布局 / 状态操作按钮", 966, 80, 610, 408, BorderOrange);
            CreateGroupBox(_mainWindow, "🎨 样式预览 TabControl", 966, 506, 610, 190, BorderGreen);
            CreateGroupBox(_mainWindow, "📐 状态预览 TabControl", 966, 714, 610, 190, BorderPurple);
            CreateGroupBox(_mainWindow, "📝 事件日志", 16, 650, 930, 254, BorderRed);
            CreateLabel(_mainWindow, "样式预览用于切换 header 风格、位置、对齐、滚动、字体、尺寸和配色。", 982, 536, 560, 20, Gray, White, 11, false, false);
            CreateLabel(_mainWindow, "状态预览用于演示 Show/Enable/Bounds/Destroy/重建。", 982, 744, 560, 20, Gray, White, 11, false, false);

            _logEdit = EmojiWindowNative.CreateEditBox(
                _mainWindow,
                28,
                684,
                906,
                196,
                EmojiWindowNative.ToUtf8(""),
                0,
                Black,
                White,
                FontYaHei,
                FontYaHei.Length,
                11,
                0,
                0,
                0,
                AlignLeft,
                1,
                1,
                0,
                1,
                0);

            CreateOperationButtons();
        }

        private static void CreateOperationButtons()
        {
            int[] cols = new int[] { 982, 1096, 1210, 1324, 1438 };
            int rowTop = 148;
            int rowStep = 36;
            int width = 104;
            int height = 28;

            AddButton(_mainWindow, "━", "线条", cols[0], rowTop + rowStep * 0, width, height, BorderBlue, delegate { ApplyHeaderStyle(TabHeaderStyleLine, "Line"); });
            AddButton(_mainWindow, "▣", "卡片", cols[1], rowTop + rowStep * 0, width, height, BorderBlue, delegate { ApplyHeaderStyle(TabHeaderStyleCard, "Card"); });
            AddButton(_mainWindow, "▤", "纯卡", cols[2], rowTop + rowStep * 0, width, height, BorderBlue, delegate { ApplyHeaderStyle(TabHeaderStyleCardPlain, "Card Plain"); });
            AddButton(_mainWindow, "◫", "分段", cols[3], rowTop + rowStep * 0, width, height, BorderBlue, delegate { ApplyHeaderStyle(TabHeaderStyleSegmented, "Segmented"); });
            AddButton(_mainWindow, "↔", "滚动", cols[4], rowTop + rowStep * 0, width, height, BorderGreen, ToggleScrollable);

            AddButton(_mainWindow, "⬆", "上部", cols[0], rowTop + rowStep * 1, width, height, BorderOrange, delegate { ApplyTabPosition(PositionTop, "上部"); });
            AddButton(_mainWindow, "⬇", "下部", cols[1], rowTop + rowStep * 1, width, height, BorderOrange, delegate { ApplyTabPosition(PositionBottom, "下部"); });
            AddButton(_mainWindow, "⬅", "左侧", cols[2], rowTop + rowStep * 1, width, height, BorderOrange, delegate { ApplyTabPosition(PositionLeft, "左侧"); });
            AddButton(_mainWindow, "➡", "右侧", cols[3], rowTop + rowStep * 1, width, height, BorderOrange, delegate { ApplyTabPosition(PositionRight, "右侧"); });
            AddButton(_mainWindow, "≡", "左对齐", cols[4], rowTop + rowStep * 1, width, height, BorderPurple, delegate { ApplyTabAlignment(AlignLeft, "左对齐"); });

            AddButton(_mainWindow, "◎", "居中", cols[0], rowTop + rowStep * 2, width, height, BorderPurple, delegate { ApplyTabAlignment(AlignCenter, "居中"); });
            AddButton(_mainWindow, "≣", "右对齐", cols[1], rowTop + rowStep * 2, width, height, BorderPurple, delegate { ApplyTabAlignment(AlignRight, "右对齐"); });
            AddButton(_mainWindow, "A-", "字体小", cols[2], rowTop + rowStep * 2, width, height, BorderGreen, delegate { ApplyStyleFont(12); });
            AddButton(_mainWindow, "A+", "字体大", cols[3], rowTop + rowStep * 2, width, height, BorderGreen, delegate { ApplyStyleFont(16); });
            AddButton(_mainWindow, "⇳", "舒展", cols[4], rowTop + rowStep * 2, width, height, BorderGreen, ToggleStyleDensity);

            AddButton(_mainWindow, "◼", "紧凑", cols[0], rowTop + rowStep * 3, width, height, BorderGreen, ApplyCompactStylePreset);
            AddButton(_mainWindow, "🔵", "蓝主题", cols[1], rowTop + rowStep * 3, width, height, BorderBlue, delegate { ApplyStylePalette(false); });
            AddButton(_mainWindow, "🟢", "绿主题", cols[2], rowTop + rowStep * 3, width, height, BorderGreen, delegate { ApplyStylePalette(true); });
            AddButton(_mainWindow, "✖", "可关闭", cols[3], rowTop + rowStep * 3, width, height, BorderRed, ToggleMainClosable);
            AddButton(_mainWindow, "⇆", "可拖拽", cols[4], rowTop + rowStep * 3, width, height, BorderPurple, ToggleMainDraggable);

            AddButton(_mainWindow, "＋", "添加页", cols[0], rowTop + rowStep * 4, width, height, BorderBlue, AddMainPage);
            AddButton(_mainWindow, "↧", "插入@1", cols[1], rowTop + rowStep * 4, width, height, BorderBlue, InsertMainPageAtOne);
            AddButton(_mainWindow, "✎", "改标题", cols[2], rowTop + rowStep * 4, width, height, BorderBlue, RenameCurrentMainPage);
            AddButton(_mainWindow, "🔍", "查Style03", cols[3], rowTop + rowStep * 4, width, height, BorderBlue, FindStylePageByTitle);
            AddButton(_mainWindow, "📖", "读标题", cols[4], rowTop + rowStep * 4, width, height, BorderBlue, ReadCurrentMainTitle);

            AddButton(_mainWindow, "←", "左移", cols[0], rowTop + rowStep * 5, width, height, BorderOrange, delegate { MoveCurrentMainPage(-1); });
            AddButton(_mainWindow, "→", "右移", cols[1], rowTop + rowStep * 5, width, height, BorderOrange, delegate { MoveCurrentMainPage(1); });
            AddButton(_mainWindow, "②", "禁用2页", cols[2], rowTop + rowStep * 5, width, height, BorderOrange, ToggleSecondPageEnabled);
            AddButton(_mainWindow, "③", "显示3页", cols[3], rowTop + rowStep * 5, width, height, BorderOrange, ToggleThirdPageVisible);
            AddButton(_mainWindow, "🖼", "图标", cols[4], rowTop + rowStep * 5, width, height, BorderOrange, ToggleCurrentPageIcon);

            AddButton(_mainWindow, "🎨", "当前底色", cols[0], rowTop + rowStep * 6, width, height, BorderGreen, ApplyCurrentPageColor);
            AddButton(_mainWindow, "🪄", "全部底色", cols[1], rowTop + rowStep * 6, width, height, BorderGreen, ApplyAllPageColors);
            AddButton(_mainWindow, "▶", "下一个", cols[2], rowTop + rowStep * 6, width, height, BorderGreen, SelectNextMainPage);
            AddButton(_mainWindow, "📊", "读状态", cols[3], rowTop + rowStep * 6, width, height, BorderGreen, ReadDetailedState);
            AddButton(_mainWindow, "🖌", "重绘", cols[4], rowTop + rowStep * 6, width, height, BorderGreen, RedrawAllTabs);

            AddButton(_mainWindow, "🔄", "刷新布局", cols[0], rowTop + rowStep * 7, width, height, BorderPurple, UpdateAllTabLayouts);
            AddButton(_mainWindow, "👁", "显隐预览", cols[1], rowTop + rowStep * 7, width, height, BorderPurple, ToggleStatePreviewVisible);
            AddButton(_mainWindow, "⛔", "启用预览", cols[2], rowTop + rowStep * 7, width, height, BorderPurple, ToggleStatePreviewEnabled);
            AddButton(_mainWindow, "📦", "移动预览", cols[3], rowTop + rowStep * 7, width, height, BorderPurple, MoveStatePreview);
            AddButton(_mainWindow, "↺", "还原预览", cols[4], rowTop + rowStep * 7, width, height, BorderPurple, RestoreStatePreviewBounds);

            AddButton(_mainWindow, "－", "删当前", cols[0], rowTop + rowStep * 8, width, height, BorderRed, RemoveCurrentMainPage);
            AddButton(_mainWindow, "♻", "重置主页", cols[1], rowTop + rowStep * 8, width, height, BorderRed, ResetMainPages);
            AddButton(_mainWindow, "☒", "重建预览", cols[2], rowTop + rowStep * 8, width, height, BorderRed, RecreateStatePreviewTab);
        }

        private static void CreateMainDemoTab()
        {
            _mainTab = EmojiWindowNative.CreateTabControl(_mainWindow, 28, 114, 906, 490);
            EmojiWindowNative.SetTabHeaderStyle(_mainTab, TabHeaderStyleCardPlain);
            EmojiWindowNative.SetTabItemSize(_mainTab, 144, 36);
            EmojiWindowNative.SetTabPadding(_mainTab, 18, 8);
            EmojiWindowNative.SetTabColors(_mainTab, White, LightGray, BorderBlue, Gray);
            EmojiWindowNative.SetTabIndicatorColor(_mainTab, BorderBlue);
            EmojiWindowNative.SetTabClosable(_mainTab, 1);
            EmojiWindowNative.SetTabDraggable(_mainTab, 1);
            EmojiWindowNative.SetTabScrollable(_mainTab, 1);
            ResetMainPages();
        }

        private static void CreateStylePreviewTab()
        {
            _styleTab = EmojiWindowNative.CreateTabControl(_mainWindow, _stylePreviewLeft, _stylePreviewTop, _stylePreviewWidth, _stylePreviewHeight);
            ApplyStylePalette(false);
            EmojiWindowNative.SetTabHeaderStyle(_styleTab, TabHeaderStyleCardPlain);
            EmojiWindowNative.SetTabPosition(_styleTab, PositionTop);
            EmojiWindowNative.SetTabAlignment(_styleTab, AlignLeft);
            EmojiWindowNative.SetTabScrollable(_styleTab, 0);
            StylePages.Clear();

            int i;
            for (i = 0; i < 8; i++)
            {
                AddTabPage(_styleTab, StylePages, string.Format("Style {0:00}", i + 1), -1, "样式页签", "观察 header 风格、方向、字体、尺寸和滚动变化。");
            }

            EmojiWindowNative.SelectTab(_styleTab, 0);
            EmojiWindowNative.UpdateTabControlLayout(_styleTab);
            EmojiWindowNative.RedrawTabControl(_styleTab);
        }

        private static void CreateStatePreviewTab()
        {
            _stateVisible = true;
            _stateEnabled = true;
            _stateMoved = false;
            _stateTab = EmojiWindowNative.CreateTabControl(_mainWindow, _statePreviewLeft, _statePreviewTop, _statePreviewWidth, _statePreviewHeight);
            EmojiWindowNative.SetTabHeaderStyle(_stateTab, TabHeaderStyleLine);
            EmojiWindowNative.SetTabItemSize(_stateTab, 138, 34);
            EmojiWindowNative.SetTabPadding(_stateTab, 14, 6);
            EmojiWindowNative.SetTabColors(_stateTab, White, LightGray, BorderPurple, Gray);
            EmojiWindowNative.SetTabIndicatorColor(_stateTab, BorderPurple);
            StatePages.Clear();
            AddTabPage(_stateTab, StatePages, "状态一", -1, "状态页 1", "这个预览区专门给 Show/Enable/Bounds/Destroy 使用。");
            AddTabPage(_stateTab, StatePages, "状态二", -1, "状态页 2", "隐藏或禁用后，可通过右侧按钮恢复。");
            AddTabPage(_stateTab, StatePages, "状态三", -1, "状态页 3", "重建预览会先 DestroyTabControl 再重新创建。");
            EmojiWindowNative.SelectTab(_stateTab, 0);
            EmojiWindowNative.UpdateTabControlLayout(_stateTab);
            EmojiWindowNative.RedrawTabControl(_stateTab);
            SaveStatePreviewBounds();
        }

        private static void InstallCallbacks()
        {
            _buttonClickCallback = new EmojiWindowNative.ButtonClickCallback(OnButtonClick);
            _tabCallback = new EmojiWindowNative.TabCallback(OnTabChanged);
            _tabCloseCallback = new EmojiWindowNative.TabCloseCallback(OnTabClose);
            _tabRightClickCallback = new EmojiWindowNative.TabRightClickCallback(OnTabRightClick);
            _tabDoubleClickCallback = new EmojiWindowNative.TabDoubleClickCallback(OnTabDoubleClick);
            _windowResizeCallback = new EmojiWindowNative.WindowResizeCallback(OnWindowResize);
            EmojiWindowNative.set_button_click_callback(_buttonClickCallback);
            EmojiWindowNative.SetWindowResizeCallback(_windowResizeCallback);
            ApplyTabCallbacks(_mainTab, true);
            ApplyTabCallbacks(_styleTab, false);
            ApplyTabCallbacks(_stateTab, false);
        }

        private static void ApplyTabCallbacks(IntPtr tab, bool closable)
        {
            if (tab == IntPtr.Zero) return;
            EmojiWindowNative.SetTabCallback(tab, _tabCallback);
            EmojiWindowNative.SetTabRightClickCallback(tab, _tabRightClickCallback);
            EmojiWindowNative.SetTabDoubleClickCallback(tab, _tabDoubleClickCallback);
            if (closable)
            {
                EmojiWindowNative.SetTabCloseCallback(tab, _tabCloseCallback);
            }
        }

        private static void CreatePopup()
        {
            _popupMenu = CreatePopupMenu();
            AppendMenuW(_popupMenu, 0, new UIntPtr(1001), "关闭当前页");
            AppendMenuW(_popupMenu, 0, new UIntPtr(1002), "重命名当前页");
            AppendMenuW(_popupMenu, 0, new UIntPtr(1003), "切换图标");
            AppendMenuW(_popupMenu, 0, new UIntPtr(1004), "跳到第一页");
        }

        private static int CreateLabel(IntPtr parent, string text, int x, int y, int width, int height, uint fg, uint bg, int size, bool bold, bool wrap)
        {
            byte[] bytes = EmojiWindowNative.ToUtf8(text);
            return EmojiWindowNative.CreateLabel(parent, x, y, width, height, bytes, bytes.Length, fg, bg, FontYaHei, FontYaHei.Length, size, bold ? 1 : 0, 0, 0, AlignLeft, wrap ? 1 : 0);
        }

        private static IntPtr CreateGroupBox(IntPtr parent, string title, int x, int y, int width, int height, uint borderColor)
        {
            byte[] bytes = EmojiWindowNative.ToUtf8(title);
            return EmojiWindowNative.CreateGroupBox(parent, x, y, width, height, bytes, bytes.Length, borderColor, White, FontYaHei, FontYaHei.Length, 12, 1, 0, 0);
        }

        private static int AddButton(IntPtr parent, string emoji, string text, int x, int y, int width, int height, uint bgColor, Action action)
        {
            byte[] emojiBytes = EmojiWindowNative.ToUtf8(emoji);
            byte[] textBytes = EmojiWindowNative.ToUtf8(text);
            int id = EmojiWindowNative.create_emoji_button_bytes(parent, emojiBytes, emojiBytes.Length, textBytes, textBytes.Length, x, y, width, height, bgColor);
            ButtonActions[id] = action;
            return id;
        }

        private static TabPageModel AddTabPage(IntPtr tab, List<TabPageModel> pages, string title, int insertIndex, string caption, string description)
        {
            byte[] titleBytes = EmojiWindowNative.ToUtf8(title);
            int actualIndex = insertIndex < 0
                ? EmojiWindowNative.AddTabItem(tab, titleBytes, titleBytes.Length, IntPtr.Zero)
                : EmojiWindowNative.InsertTabItem(tab, insertIndex, titleBytes, titleBytes.Length, IntPtr.Zero);

            if (actualIndex < 0)
            {
                AppendLog("Add/InsertTabItem 返回 -1，未能创建页签。");
                return null;
            }

            TabPageModel model = new TabPageModel();
            model.Title = title;
            model.ColorIndex = pages.Count % ContentColors.Length;
            model.ContentWindow = EmojiWindowNative.GetTabContentWindow(tab, actualIndex);
            model.TitleLabel = CreateLabel(model.ContentWindow, "📄 " + caption, 20, 18, 420, 28, Black, White, 16, true, false);
            model.DescLabel = CreateLabel(model.ContentWindow, description, 20, 54, 520, 38, Gray, White, 12, false, true);
            model.ButtonId = AddButton(model.ContentWindow, "🧪", "页内按钮", 20, 110, 130, 34, BorderBlue, delegate
            {
                SetStatus(string.Format("{0} -> 点击了页内按钮，Content HWND={1}", title, model.ContentWindow));
                AppendLog(string.Format("{0} 内容区按钮被点击，GetTabContentWindow 句柄={1}", title, model.ContentWindow));
            });
            CreateLabel(model.ContentWindow, "这里的内容窗口由 GetTabContentWindow 获取，切换页签时会跟随显示/隐藏。", 20, 162, 640, 24, Gray, White, 11, false, false);
            CreateLabel(model.ContentWindow, "你可以直接点击上方页签、拖拽主页签顺序，或使用右侧按钮触发各种 Tab API。", 20, 192, 640, 24, Gray, White, 11, false, false);

            if (insertIndex < 0 || actualIndex >= pages.Count)
            {
                pages.Add(model);
            }
            else
            {
                pages.Insert(actualIndex, model);
            }

            EmojiWindowNative.SetTabContentBgColor(tab, actualIndex, ContentColors[model.ColorIndex]);
            return model;
        }

        private static List<TabPageModel> GetPages(IntPtr hTab)
        {
            if (hTab == _mainTab) return MainPages;
            if (hTab == _styleTab) return StylePages;
            if (hTab == _stateTab) return StatePages;
            return null;
        }

        private static string GetTabName(IntPtr hTab)
        {
            if (hTab == _mainTab) return "主页";
            if (hTab == _styleTab) return "样式预览";
            if (hTab == _stateTab) return "状态预览";
            return "未知";
        }

        private static void OnButtonClick(int buttonId, IntPtr parentHwnd)
        {
            Action action;
            if (ButtonActions.TryGetValue(buttonId, out action))
            {
                action();
                return;
            }

            AppendLog(string.Format("收到未注册按钮回调：buttonId={0}, parent={1}", buttonId, parentHwnd));
        }

        private static void OnTabChanged(IntPtr hTabControl, int selectedIndex)
        {
            string title = selectedIndex >= 0 ? EmojiWindowNative.GetTabTitleString(hTabControl, selectedIndex) : string.Empty;
            SetStatus(string.Format("{0} 已切换到索引 {1} [{2}]", GetTabName(hTabControl), selectedIndex, title));
            AppendLog(string.Format("SetTabCallback -> {0}, 当前索引={1}, 标题={2}", GetTabName(hTabControl), selectedIndex, title));
        }

        private static void OnTabClose(IntPtr hTabControl, int index)
        {
            if (hTabControl != _mainTab) return;
            if (EmojiWindowNative.GetTabCount(hTabControl) <= 1)
            {
                SetStatus("主页签至少保留 1 个，已阻止关闭。");
                AppendLog("SetTabCloseCallback 命中，但主页签数量只剩 1 个。");
                return;
            }

            if (EmojiWindowNative.RemoveTabItem(hTabControl, index))
            {
                if (index >= 0 && index < MainPages.Count) MainPages.RemoveAt(index);
                SetStatus(string.Format("关闭主页签成功，移除索引 {0}。", index));
                AppendLog(string.Format("SetTabCloseCallback -> RemoveTabItem(main, {0}) 成功。", index));
            }
        }

        private static void OnTabRightClick(IntPtr hTabControl, int index, int x, int y)
        {
            SetStatus(string.Format("{0} 页签右键：index={1}, screen=({2},{3})", GetTabName(hTabControl), index, x, y));
            AppendLog(string.Format("SetTabRightClickCallback -> {0}, index={1}, screen=({2},{3})", GetTabName(hTabControl), index, x, y));
            if (hTabControl != _mainTab || index < 0) return;

            SetForegroundWindow(_mainWindow);
            int cmd = TrackPopupMenu(_popupMenu, 0x0100, x, y, 0, _mainWindow, IntPtr.Zero);
            if (cmd == 1001) RemoveMainPageAt(index);
            if (cmd == 1002) RenameMainPage(index);
            if (cmd == 1003) TogglePageIcon(index);
            if (cmd == 1004) EmojiWindowNative.SelectTab(_mainTab, 0);
        }

        private static void OnTabDoubleClick(IntPtr hTabControl, int index)
        {
            if (index < 0) return;
            string oldTitle = EmojiWindowNative.GetTabTitleString(hTabControl, index);
            string newTitle = oldTitle + " · 双击";
            SetPageTitle(hTabControl, index, newTitle);
            SetStatus(string.Format("{0} 双击页签 -> {1}", GetTabName(hTabControl), newTitle));
            AppendLog(string.Format("SetTabDoubleClickCallback -> {0}, index={1}, 新标题={2}", GetTabName(hTabControl), index, newTitle));
        }

        private static void OnWindowResize(IntPtr hwnd, int width, int height)
        {
            if (hwnd == _mainWindow)
            {
                SetStatus(string.Format("窗口尺寸变化：{0} x {1}。当前示例使用固定布局。", width, height));
            }
        }

        private static void ApplyHeaderStyle(int style, string name)
        {
            EmojiWindowNative.SetTabHeaderStyle(_styleTab, style);
            EmojiWindowNative.UpdateTabControlLayout(_styleTab);
            EmojiWindowNative.RedrawTabControl(_styleTab);
            SetStatus("样式预览 header 已切换为 " + name);
            AppendLog("SetTabHeaderStyle(stylePreview, " + name + ")");
        }

        private static void ApplyTabPosition(int position, string name)
        {
            EmojiWindowNative.SetTabPosition(_styleTab, position);
            EmojiWindowNative.UpdateTabControlLayout(_styleTab);
            EmojiWindowNative.RedrawTabControl(_styleTab);
            SetStatus("样式预览位置已切换为 " + name);
            AppendLog("SetTabPosition(stylePreview, " + name + ")");
        }

        private static void ApplyTabAlignment(int align, string name)
        {
            EmojiWindowNative.SetTabAlignment(_styleTab, align);
            EmojiWindowNative.RedrawTabControl(_styleTab);
            SetStatus("样式预览对齐已切换为 " + name);
            AppendLog("SetTabAlignment(stylePreview, " + name + ")");
        }

        private static void ToggleScrollable()
        {
            _styleScrollable = !_styleScrollable;
            EmojiWindowNative.SetTabScrollable(_styleTab, _styleScrollable ? 1 : 0);
            EmojiWindowNative.UpdateTabControlLayout(_styleTab);
            EmojiWindowNative.RedrawTabControl(_styleTab);
            SetStatus("样式预览滚动模式 = " + (_styleScrollable ? "单行可滚动" : "多行模式"));
            AppendLog("SetTabScrollable(stylePreview, " + (_styleScrollable ? "1" : "0") + ")");
        }

        private static void ApplyStyleFont(int fontSize)
        {
            _styleFontSize = fontSize;
            EmojiWindowNative.SetTabFont(_styleTab, FontSegoe, FontSegoe.Length, (float)_styleFontSize);
            EmojiWindowNative.UpdateTabControlLayout(_styleTab);
            EmojiWindowNative.RedrawTabControl(_styleTab);
            SetStatus("样式预览字体大小已调整为 " + fontSize);
            AppendLog("SetTabFont(stylePreview, Segoe UI, " + fontSize + ")");
        }

        private static void ToggleStyleDensity()
        {
            _styleRoomy = !_styleRoomy;
            if (_styleRoomy)
            {
                EmojiWindowNative.SetTabItemSize(_styleTab, 138, 36);
                EmojiWindowNative.SetTabPadding(_styleTab, 18, 8);
                SetStatus("样式预览已切换为舒展尺寸。");
                AppendLog("SetTabItemSize(stylePreview, 138, 36) + SetTabPadding(18, 8)");
                EmojiWindowNative.UpdateTabControlLayout(_styleTab);
                EmojiWindowNative.RedrawTabControl(_styleTab);
                return;
            }

            ApplyCompactStylePreset();
        }

        private static void ApplyCompactStylePreset()
        {
            _styleRoomy = false;
            EmojiWindowNative.SetTabItemSize(_styleTab, 116, 30);
            EmojiWindowNative.SetTabPadding(_styleTab, 10, 4);
            EmojiWindowNative.UpdateTabControlLayout(_styleTab);
            EmojiWindowNative.RedrawTabControl(_styleTab);
            SetStatus("样式预览已切换为紧凑尺寸。");
            AppendLog("SetTabItemSize(stylePreview, 116, 30) + SetTabPadding(10, 4)");
        }

        private static void ApplyStylePalette(bool alt)
        {
            _stylePaletteAlt = alt;
            if (_styleTab == IntPtr.Zero) return;
            if (alt)
            {
                EmojiWindowNative.SetTabColors(_styleTab, EmojiWindowNative.ARGB(255, 236, 253, 245), EmojiWindowNative.ARGB(255, 240, 253, 244), BorderGreen, Gray);
                EmojiWindowNative.SetTabIndicatorColor(_styleTab, BorderGreen);
            }
            else
            {
                EmojiWindowNative.SetTabColors(_styleTab, White, LightGray, BorderBlue, Gray);
                EmojiWindowNative.SetTabIndicatorColor(_styleTab, BorderBlue);
            }

            EmojiWindowNative.RedrawTabControl(_styleTab);
            SetStatus("样式预览已切换到 " + (alt ? "绿色主题" : "蓝色主题"));
            AppendLog("SetTabColors/SetTabIndicatorColor(stylePreview)");
        }

        private static void ToggleMainClosable()
        {
            _mainClosable = !_mainClosable;
            EmojiWindowNative.SetTabClosable(_mainTab, _mainClosable ? 1 : 0);
            EmojiWindowNative.RedrawTabControl(_mainTab);
            SetStatus("主页签关闭按钮 = " + (_mainClosable ? "开启" : "关闭"));
            AppendLog("SetTabClosable(main, " + (_mainClosable ? "1" : "0") + ")");
        }

        private static void ToggleMainDraggable()
        {
            _mainDraggable = !_mainDraggable;
            EmojiWindowNative.SetTabDraggable(_mainTab, _mainDraggable ? 1 : 0);
            SetStatus("主页签拖拽排序 = " + (_mainDraggable ? "开启" : "关闭"));
            AppendLog("SetTabDraggable(main, " + (_mainDraggable ? "1" : "0") + ")");
        }

        private static void AddMainPage()
        {
            _pageSeed++;
            string title = string.Format("🧩 新页 {0}", _pageSeed);
            AddTabPage(_mainTab, MainPages, title, -1, "动态添加页签", "这个页签由 AddTabItem 动态加入，content window 由 DLL 自动创建。");
            EmojiWindowNative.SelectTab(_mainTab, EmojiWindowNative.GetTabCount(_mainTab) - 1);
            EmojiWindowNative.UpdateTabControlLayout(_mainTab);
            SetStatus("已添加主页签：" + title);
            AppendLog("AddTabItem(main, " + title + ")");
        }

        private static void InsertMainPageAtOne()
        {
            _pageSeed++;
            string title = string.Format("📌 插入 {0}", _pageSeed);
            AddTabPage(_mainTab, MainPages, title, 1, "插入页签", "这个页签通过 InsertTabItem 插入到索引 1。");
            EmojiWindowNative.SelectTab(_mainTab, 1);
            EmojiWindowNative.UpdateTabControlLayout(_mainTab);
            SetStatus("已在索引 1 插入主页签：" + title);
            AppendLog("InsertTabItem(main, 1, " + title + ")");
        }

        private static void RenameCurrentMainPage()
        {
            int index = EmojiWindowNative.GetCurrentTabIndex(_mainTab);
            if (index >= 0) RenameMainPage(index);
        }

        private static void RenameMainPage(int index)
        {
            _renameSeed++;
            string title = string.Format("✏️ 已改名 {0}", _renameSeed);
            SetPageTitle(_mainTab, index, title);
            SetStatus(string.Format("主页签 {0} 已改名为 {1}", index, title));
            AppendLog(string.Format("SetTabTitle(main, {0}, {1})", index, title));
        }

        private static void FindStylePageByTitle()
        {
            byte[] title = EmojiWindowNative.ToUtf8("Style 03");
            int index = EmojiWindowNative.GetTabIndexByTitle(_styleTab, title, title.Length);
            if (index >= 0)
            {
                EmojiWindowNative.SelectTab(_styleTab, index);
                SetStatus("GetTabIndexByTitle 找到样式页签：Style 03");
                AppendLog("GetTabIndexByTitle(stylePreview, Style 03) -> " + index);
            }
        }

        private static void ReadCurrentMainTitle()
        {
            int index = EmojiWindowNative.GetCurrentTabIndex(_mainTab);
            if (index < 0) return;
            string title = EmojiWindowNative.GetTabTitleString(_mainTab, index);
            SetStatus("当前主页签标题：" + title);
            AppendLog(string.Format("GetTabTitle(main, {0}) -> {1}", index, title));
        }

        private static void MoveCurrentMainPage(int delta)
        {
            int from = EmojiWindowNative.GetCurrentTabIndex(_mainTab);
            if (from < 0) return;
            int to = from + delta;
            if (to < 0 || to >= MainPages.Count)
            {
                SetStatus("已经到边界，无法继续移动。");
                return;
            }

            if (EmojiWindowNative.MoveTabItem(_mainTab, from, to) == 0)
            {
                TabPageModel model = MainPages[from];
                MainPages.RemoveAt(from);
                MainPages.Insert(to, model);
                EmojiWindowNative.SelectTab(_mainTab, to);
                SetStatus(string.Format("主页签从 {0} 移动到 {1}", from, to));
                AppendLog(string.Format("MoveTabItem(main, {0}, {1})", from, to));
            }
        }

        private static void ToggleSecondPageEnabled()
        {
            if (MainPages.Count < 2) return;
            int current = EmojiWindowNative.GetTabItemEnabled(_mainTab, 1);
            int next = current == 1 ? 0 : 1;
            EmojiWindowNative.EnableTabItem(_mainTab, 1, next);
            SetStatus("第 2 个主页签启用状态 = " + (next == 1 ? "启用" : "禁用"));
            AppendLog("EnableTabItem(main, 1, " + next + ")");
        }

        private static void ToggleThirdPageVisible()
        {
            if (MainPages.Count < 3) return;
            _thirdPageVisible = !_thirdPageVisible;
            EmojiWindowNative.ShowTabItem(_mainTab, 2, _thirdPageVisible ? 1 : 0);
            SetStatus("第 3 个主页签可见状态 = " + (_thirdPageVisible ? "显示" : "隐藏"));
            AppendLog("ShowTabItem(main, 2, " + (_thirdPageVisible ? "1" : "0") + ")");
        }

        private static void ToggleCurrentPageIcon()
        {
            int index = EmojiWindowNative.GetCurrentTabIndex(_mainTab);
            if (index >= 0) TogglePageIcon(index);
        }

        private static void TogglePageIcon(int index)
        {
            if (index < 0 || index >= MainPages.Count) return;
            TabPageModel model = MainPages[index];
            if (model.HasIcon)
            {
                EmojiWindowNative.SetTabItemIcon(_mainTab, index, null, 0);
                model.HasIcon = false;
                SetStatus("已清除当前主页签图标。");
                AppendLog("SetTabItemIcon(main, " + index + ", NULL, 0)");
            }
            else
            {
                byte[] icon = _tabIcons[index % _tabIcons.Length];
                EmojiWindowNative.SetTabItemIcon(_mainTab, index, icon, icon.Length);
                model.HasIcon = true;
                SetStatus("已设置当前主页签图标。");
                AppendLog("SetTabItemIcon(main, " + index + ", pngBytes, " + icon.Length + ")");
            }

            EmojiWindowNative.RedrawTabControl(_mainTab);
        }

        private static void ApplyCurrentPageColor()
        {
            int index = EmojiWindowNative.GetCurrentTabIndex(_mainTab);
            if (index < 0 || index >= MainPages.Count) return;
            TabPageModel model = MainPages[index];
            model.ColorIndex = (model.ColorIndex + 1) % ContentColors.Length;
            EmojiWindowNative.SetTabContentBgColor(_mainTab, index, ContentColors[model.ColorIndex]);
            SetStatus("已切换当前主页签内容背景色。");
            AppendLog(string.Format("SetTabContentBgColor(main, {0}, 0x{1:X8})", index, ContentColors[model.ColorIndex]));
        }

        private static void ApplyAllPageColors()
        {
            _mainPaletteAlt = !_mainPaletteAlt;
            uint color = _mainPaletteAlt ? EmojiWindowNative.ARGB(255, 241, 248, 241) : EmojiWindowNative.ARGB(255, 248, 250, 252);
            EmojiWindowNative.SetTabContentBgColorAll(_mainTab, color);
            SetStatus("已批量设置主页签内容背景色。");
            AppendLog(string.Format("SetTabContentBgColorAll(main, 0x{0:X8})", color));
        }

        private static void SelectNextMainPage()
        {
            int count = EmojiWindowNative.GetTabCount(_mainTab);
            if (count <= 0) return;
            int current = EmojiWindowNative.GetCurrentTabIndex(_mainTab);
            int next = current + 1;
            if (next >= count) next = 0;
            EmojiWindowNative.SelectTab(_mainTab, next);
            AppendLog("SelectTab(main, " + next + ")");
        }

        private static void ReadDetailedState()
        {
            int mainCount = EmojiWindowNative.GetTabCount(_mainTab);
            int mainIndex = EmojiWindowNative.GetCurrentTabIndex(_mainTab);
            int styleVisible = _styleTab != IntPtr.Zero ? EmojiWindowNative.GetTabControlVisible(_styleTab) : -1;
            int stateVisible = _stateTab != IntPtr.Zero ? EmojiWindowNative.GetTabControlVisible(_stateTab) : -1;
            int stateEnabled = _stateTab != IntPtr.Zero ? EmojiWindowNative.GetTabEnabled(_stateTab) : -1;
            int stateX = 0;
            int stateY = 0;
            int stateW = 0;
            int stateH = 0;
            if (_stateTab != IntPtr.Zero)
            {
                EmojiWindowNative.GetTabControlBounds(_stateTab, out stateX, out stateY, out stateW, out stateH);
            }

            int secondEnabled = mainCount > 1 ? EmojiWindowNative.GetTabItemEnabled(_mainTab, 1) : -1;
            int currentSelected = mainIndex >= 0 ? EmojiWindowNative.IsTabItemSelected(_mainTab, mainIndex) : -1;
            string summary = string.Format(
                "主页签数={0}, 当前={1}, 样式预览可见={2}, 状态预览可见={3}, 状态预览启用={4}, 状态预览Bounds=({5},{6},{7},{8}), 第2页启用={9}, 当前选中检查={10}",
                mainCount, mainIndex, styleVisible, stateVisible, stateEnabled, stateX, stateY, stateW, stateH, secondEnabled, currentSelected);
            SetStatus(summary);
            AppendLog("状态读取 -> " + summary);
        }

        private static void RedrawAllTabs()
        {
            if (_mainTab != IntPtr.Zero) EmojiWindowNative.RedrawTabControl(_mainTab);
            if (_styleTab != IntPtr.Zero) EmojiWindowNative.RedrawTabControl(_styleTab);
            if (_stateTab != IntPtr.Zero) EmojiWindowNative.RedrawTabControl(_stateTab);
            SetStatus("已调用 RedrawTabControl 重绘全部示例。");
            AppendLog("RedrawTabControl(main/style/state)");
        }

        private static void UpdateAllTabLayouts()
        {
            if (_mainTab != IntPtr.Zero) EmojiWindowNative.UpdateTabControlLayout(_mainTab);
            if (_styleTab != IntPtr.Zero) EmojiWindowNative.UpdateTabControlLayout(_styleTab);
            if (_stateTab != IntPtr.Zero) EmojiWindowNative.UpdateTabControlLayout(_stateTab);
            SetStatus("已调用 UpdateTabControlLayout 更新全部布局。");
            AppendLog("UpdateTabControlLayout(main/style/state)");
        }

        private static void ToggleStatePreviewVisible()
        {
            if (_stateTab == IntPtr.Zero) return;
            _stateVisible = !_stateVisible;
            EmojiWindowNative.ShowTabControl(_stateTab, _stateVisible ? 1 : 0);
            SetStatus("状态预览可见 = " + (_stateVisible ? "显示" : "隐藏"));
            AppendLog("ShowTabControl(statePreview, " + (_stateVisible ? "1" : "0") + ")");
        }

        private static void ToggleStatePreviewEnabled()
        {
            if (_stateTab == IntPtr.Zero) return;
            _stateEnabled = !_stateEnabled;
            EmojiWindowNative.EnableTabControl(_stateTab, _stateEnabled ? 1 : 0);
            SetStatus("状态预览启用 = " + (_stateEnabled ? "启用" : "禁用"));
            AppendLog("EnableTabControl(statePreview, " + (_stateEnabled ? "1" : "0") + ")");
        }

        private static void MoveStatePreview()
        {
            if (_stateTab == IntPtr.Zero) return;
            if (_stateMoved)
            {
                RestoreStatePreviewBounds();
                return;
            }

            EmojiWindowNative.SetTabControlBounds(_stateTab, _statePreviewLeft + 40, _statePreviewTop + 18, _statePreviewWidth - 80, _statePreviewHeight - 16);
            _stateMoved = true;
            SetStatus("状态预览已移动并缩放。");
            AppendLog("SetTabControlBounds(statePreview, moved)");
        }

        private static void RestoreStatePreviewBounds()
        {
            if (_stateTab == IntPtr.Zero) return;
            EmojiWindowNative.SetTabControlBounds(_stateTab, _stateOriginalLeft, _stateOriginalTop, _stateOriginalWidth, _stateOriginalHeight);
            _stateMoved = false;
            SetStatus("状态预览已恢复原始位置。");
            AppendLog("SetTabControlBounds(statePreview, original)");
        }

        private static void RemoveCurrentMainPage()
        {
            int index = EmojiWindowNative.GetCurrentTabIndex(_mainTab);
            RemoveMainPageAt(index);
        }

        private static void RemoveMainPageAt(int index)
        {
            if (index < 0 || EmojiWindowNative.GetTabCount(_mainTab) <= 1)
            {
                SetStatus("至少保留一个主页签。");
                return;
            }

            if (EmojiWindowNative.RemoveTabItem(_mainTab, index))
            {
                if (index < MainPages.Count) MainPages.RemoveAt(index);
                SetStatus("已删除主页签索引 " + index);
                AppendLog("RemoveTabItem(main, " + index + ")");
            }
        }

        private static void ResetMainPages()
        {
            EmojiWindowNative.RemoveAllTabs(_mainTab);
            MainPages.Clear();
            _thirdPageVisible = true;
            AddTabPage(_mainTab, MainPages, "📌 概览", -1, "主页签 1 / 概览", "这里展示最基础的 Tab 切换、内容窗口和状态输出。");
            AddTabPage(_mainTab, MainPages, "📦 API", -1, "主页签 2 / API", "可配合右侧按钮检查 GetTabTitle、SetTabTitle、GetTabCount 等接口。");
            AddTabPage(_mainTab, MainPages, "🧪 交互", -1, "主页签 3 / 交互", "关闭按钮、右键菜单、双击回调、拖拽排序都在这个主控件上验证。");
            AddTabPage(_mainTab, MainPages, "🎨 样式", -1, "主页签 4 / 样式", "当前页背景色可单独设置，也可对所有页批量设置。");
            AddTabPage(_mainTab, MainPages, "📜 日志", -1, "主页签 5 / 日志", "左下角日志会记录各个按钮触发的底层 TabControl API。");
            EmojiWindowNative.SelectTab(_mainTab, 0);
            EmojiWindowNative.UpdateTabControlLayout(_mainTab);
            EmojiWindowNative.RedrawTabControl(_mainTab);
            SetStatus("主页签已通过 RemoveAllTabs + AddTabItem 重置。");
            AppendLog("RemoveAllTabs(main) + rebuild initial pages");
        }

        private static void RecreateStatePreviewTab()
        {
            if (_stateTab != IntPtr.Zero)
            {
                EmojiWindowNative.DestroyTabControl(_stateTab);
                AppendLog("DestroyTabControl(statePreview)");
            }

            _stateTab = IntPtr.Zero;
            StatePages.Clear();
            CreateStatePreviewTab();
            ApplyTabCallbacks(_stateTab, false);
            SetStatus("状态预览已重新创建。");
        }

        private static void SaveStatePreviewBounds()
        {
            if (_stateTab == IntPtr.Zero) return;
            EmojiWindowNative.GetTabControlBounds(_stateTab, out _stateOriginalLeft, out _stateOriginalTop, out _stateOriginalWidth, out _stateOriginalHeight);
        }

        private static void SetPageTitle(IntPtr hTab, int index, string newTitle)
        {
            List<TabPageModel> pages = GetPages(hTab);
            if (pages == null || index < 0 || index >= pages.Count) return;
            byte[] bytes = EmojiWindowNative.ToUtf8(newTitle);
            if (EmojiWindowNative.SetTabTitle(hTab, index, bytes, bytes.Length) == 0)
            {
                pages[index].Title = newTitle;
                byte[] caption = EmojiWindowNative.ToUtf8("📄 " + newTitle);
                EmojiWindowNative.SetLabelText(pages[index].TitleLabel, caption, caption.Length);
            }
        }

        private static void SetStatus(string text)
        {
            byte[] bytes = EmojiWindowNative.ToUtf8(text);
            EmojiWindowNative.SetLabelText(_statusLabel, bytes, bytes.Length);
        }

        private static void AppendLog(string message)
        {
            string line = DateTime.Now.ToString("HH:mm:ss") + "  " + message;
            LogLines.Add(line);
            if (LogLines.Count > 26) LogLines.RemoveAt(0);

            StringBuilder builder = new StringBuilder();
            int i;
            for (i = 0; i < LogLines.Count; i++)
            {
                if (i > 0) builder.Append("\r\n");
                builder.Append(LogLines[i]);
            }

            byte[] bytes = Encoding.UTF8.GetBytes(builder.ToString());
            EmojiWindowNative.SetEditBoxText(_logEdit, bytes, bytes.Length);
        }

        private static byte[] CreateIconBytes(Color fillColor)
        {
            using (Bitmap bitmap = new Bitmap(16, 16))
            using (Graphics graphics = Graphics.FromImage(bitmap))
            using (SolidBrush brush = new SolidBrush(fillColor))
            using (Pen pen = new Pen(Color.FromArgb(255, 255, 255, 255)))
            using (MemoryStream stream = new MemoryStream())
            {
                graphics.Clear(Color.Transparent);
                graphics.FillRectangle(brush, 1, 1, 14, 14);
                graphics.DrawRectangle(pen, 1, 1, 13, 13);
                bitmap.Save(stream, ImageFormat.Png);
                return stream.ToArray();
            }
        }
    }
}
