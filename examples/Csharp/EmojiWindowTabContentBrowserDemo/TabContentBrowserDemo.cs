using System;
using System.IO;
using EmojiWindowDemo;

namespace EmojiWindowTabContentBrowserDemo
{
    internal static class TabContentBrowserDemo
    {
        private const int MaxTabs = 32;
        private const string HomeUrl = "https://www.google.com/";

        private static IntPtr _window;
        private static IntPtr _tabControl;
        private static IntPtr _statusLabel;
        private static readonly byte[] FontBytes = EmojiWindowNative.ToUtf8("Microsoft YaHei UI");
        private static int _width = 1200;
        private static int _height = 780;
        private static int _activeSlot;

        private static readonly bool[] TabUsed = new bool[MaxTabs + 1];
        private static readonly string[] TabUrls = new string[MaxTabs + 1];
        private static readonly string[] TabTitles = new string[MaxTabs + 1];
        private static readonly IntPtr[] TabContentWindows = new IntPtr[MaxTabs + 1];
        private static readonly int[] TabBackButtons = new int[MaxTabs + 1];
        private static readonly int[] TabForwardButtons = new int[MaxTabs + 1];
        private static readonly int[] TabRefreshButtons = new int[MaxTabs + 1];
        private static readonly int[] TabHomeButtons = new int[MaxTabs + 1];
        private static readonly IntPtr[] TabAddressEdits = new IntPtr[MaxTabs + 1];
        private static readonly IntPtr[] TabTitleLabels = new IntPtr[MaxTabs + 1];
        private static readonly IntPtr[] TabSubtitleLabels = new IntPtr[MaxTabs + 1];
        private static readonly IntPtr[] TabStatusLabels = new IntPtr[MaxTabs + 1];
        private static readonly IntPtr[] TabInfo1Labels = new IntPtr[MaxTabs + 1];
        private static readonly IntPtr[] TabInfo2Labels = new IntPtr[MaxTabs + 1];
        private static readonly IntPtr[] TabInfo3Labels = new IntPtr[MaxTabs + 1];

        private static EmojiWindowNative.WindowCloseCallback _windowCloseCallback;
        private static EmojiWindowNative.WindowResizeCallback _windowResizeCallback;
        private static EmojiWindowNative.ButtonClickCallback _buttonClickCallback;
        private static EmojiWindowNative.TabCallback _tabCallback;
        private static EmojiWindowNative.TabCloseCallback _tabCloseCallback;
        private static EmojiWindowNative.TabNewButtonCallback _tabNewButtonCallback;
        private static EmojiWindowNative.EditBoxKeyCallback _editKeyCallback;

        public static void Run()
        {
            CreateWindow();
            RegisterCallbacks();
            CreateTabControl();
            CreateStatusBar();

            OnTabControlCreated(_tabControl);
            AddNewTab(HomeUrl, true, true);
            LayoutTabControl();
            LayoutAllTabContents();
            SyncActiveTabContent();
            SetStatus("C# 普通地址栏版：TabControl 内容窗口浏览器 Demo");

            EmojiWindowNative.set_message_loop_main_window(_window);
            EmojiWindowNative.run_message_loop();
        }

        private static void CreateWindow()
        {
            byte[] titleBytes = EmojiWindowNative.ToUtf8("C# Tab 内容窗口浏览器 Demo");
            _window = EmojiWindowNative.create_window_bytes_ex(
                titleBytes,
                titleBytes.Length,
                -1,
                -1,
                _width,
                _height,
                EmojiWindowNative.ARGB(255, 223, 226, 230),
                EmojiWindowNative.ARGB(255, 246, 248, 252));

            if (_window == IntPtr.Zero)
            {
                throw new InvalidOperationException("Failed to create main window.");
            }

            EmojiWindowNative.set_window_titlebar_color(_window, EmojiWindowNative.ARGB(255, 223, 226, 230));
            EmojiWindowNative.SetTitleBarTextColor(_window, EmojiWindowNative.ARGB(255, 32, 33, 36));
            EmojiWindowNative.SetWindowBackgroundColor(_window, EmojiWindowNative.ARGB(255, 246, 248, 252));

            string iconPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "谷歌.ico");
            if (File.Exists(iconPath))
            {
                byte[] iconBytes = File.ReadAllBytes(iconPath);
                EmojiWindowNative.set_window_icon_bytes(_window, iconBytes, iconBytes.Length);
            }
        }

        private static void RegisterCallbacks()
        {
            _windowCloseCallback = OnWindowClose;
            _windowResizeCallback = OnWindowResize;
            _buttonClickCallback = OnButtonClick;
            _tabCallback = OnTabChanged;
            _tabCloseCallback = OnTabClose;
            _tabNewButtonCallback = OnTabNewButton;
            _editKeyCallback = OnEditKey;

            EmojiWindowNative.SetWindowCloseCallback(_windowCloseCallback);
            EmojiWindowNative.set_button_click_callback(_buttonClickCallback);
            EmojiWindowNative.SetWindowResizeCallback(_windowResizeCallback);
        }

        private static void CreateTabControl()
        {
            _tabControl = EmojiWindowNative.CreateTabControl(_window, 0, 0, _width, _height - 62);
            if (_tabControl == IntPtr.Zero)
            {
                throw new InvalidOperationException("Failed to create TabControl.");
            }

            EmojiWindowNative.SetTabItemSize(_tabControl, 188, 34);
            EmojiWindowNative.SetTabHeaderStyle(_tabControl, 2);
            EmojiWindowNative.SetTabPosition(_tabControl, 0);
            EmojiWindowNative.SetTabAlignment(_tabControl, 0);
            EmojiWindowNative.SetTabScrollable(_tabControl, 1);
            EmojiWindowNative.SetTabClosable(_tabControl, 1);
            EmojiWindowNative.SetTabFont(_tabControl, FontBytes, FontBytes.Length, 11.5f);
            EmojiWindowNative.SetTabColors(
                _tabControl,
                EmojiWindowNative.ARGB(255, 255, 255, 255),
                EmojiWindowNative.ARGB(255, 232, 234, 237),
                EmojiWindowNative.ARGB(255, 32, 33, 36),
                EmojiWindowNative.ARGB(255, 95, 99, 104));
            EmojiWindowNative.SetTabIndicatorColor(_tabControl, EmojiWindowNative.ARGB(255, 32, 33, 36));
            EmojiWindowNative.SetTabPadding(_tabControl, 14, 3);
            EmojiWindowNative.SetTabCallback(_tabControl, _tabCallback);
            EmojiWindowNative.SetTabCloseCallback(_tabControl, _tabCloseCallback);
            EmojiWindowNative.SetTabNewButtonCallback(_tabControl, _tabNewButtonCallback);
        }

        private static void CreateStatusBar()
        {
            _statusLabel = CreateLabel(
                _window,
                20,
                _height - 32,
                _width - 40,
                24,
                string.Empty,
                EmojiWindowNative.ARGB(255, 95, 99, 104),
                EmojiWindowNative.ARGB(255, 246, 248, 252),
                12);
            EmojiWindowNative.ShowLabel(_statusLabel, 1);
        }

        private static int AddNewTab(string url, bool switchToNew, bool syncNow)
        {
            int count = EmojiWindowNative.GetTabCount(_tabControl);
            if (count >= MaxTabs)
            {
                SetStatus("标签页已满");
                return 0;
            }

            int slot = count + 1;
            TabUsed[slot] = true;
            TabUrls[slot] = url;
            TabTitles[slot] = GetTabTitle(url);

            byte[] titleBytes = EmojiWindowNative.ToUtf8(TabTitles[slot]);
            int tabIndex = EmojiWindowNative.AddTabItem(_tabControl, titleBytes, titleBytes.Length, IntPtr.Zero);
            if (tabIndex < 0)
            {
                ResetSlot(slot);
                SetStatus("添加 Tab 页失败");
                return 0;
            }

            IntPtr contentWindow = EmojiWindowNative.GetTabContentWindow(_tabControl, tabIndex);
            if (contentWindow == IntPtr.Zero)
            {
                ResetSlot(slot);
                SetStatus("获取 Tab 内容窗口失败");
                return 0;
            }

            TabContentWindows[slot] = contentWindow;
            CreateTabContent(slot, url);
            LayoutSingleTabContent(slot);

            if (switchToNew)
            {
                _activeSlot = slot;
                EmojiWindowNative.SelectTabImmediate(_tabControl, tabIndex);
            }

            if (syncNow)
            {
                SyncActiveTabContent();
            }

            return slot;
        }

        private static void CreateTabContent(int slot, string url)
        {
            IntPtr content = TabContentWindows[slot];
            TabBackButtons[slot] = CreateToolbarButton(content, "<", 20, 14);
            TabForwardButtons[slot] = CreateToolbarButton(content, ">", 56, 14);
            TabRefreshButtons[slot] = CreateToolbarButton(content, "R", 92, 14);
            TabHomeButtons[slot] = CreateToolbarButton(content, "H", 128, 14);

            byte[] urlBytes = EmojiWindowNative.ToUtf8(url);
            TabAddressEdits[slot] = EmojiWindowNative.CreateEditBox(
                content,
                172,
                12,
                _width - 220,
                34,
                urlBytes,
                urlBytes.Length,
                EmojiWindowNative.ARGB(255, 32, 33, 36),
                EmojiWindowNative.ARGB(255, 255, 255, 255),
                FontBytes,
                FontBytes.Length,
                13,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                1,
                1);

            if (TabAddressEdits[slot] != IntPtr.Zero)
            {
                EmojiWindowNative.SetEditBoxColor(
                    TabAddressEdits[slot],
                    EmojiWindowNative.ARGB(255, 32, 33, 36),
                    EmojiWindowNative.ARGB(255, 255, 255, 255));
                EmojiWindowNative.SetEditBoxKeyCallback(TabAddressEdits[slot], _editKeyCallback);
                EmojiWindowNative.ShowEditBox(TabAddressEdits[slot], 1);
            }

            TabTitleLabels[slot] = CreateLabel(content, 32, 84, 720, 40, "新标签页", EmojiWindowNative.ARGB(255, 32, 33, 36), EmojiWindowNative.ARGB(255, 255, 255, 255), 28);
            TabSubtitleLabels[slot] = CreateLabel(content, 32, 132, 900, 26, string.Empty, EmojiWindowNative.ARGB(255, 95, 99, 104), EmojiWindowNative.ARGB(255, 255, 255, 255), 12);
            TabStatusLabels[slot] = CreateLabel(content, 32, 176, 900, 24, string.Empty, EmojiWindowNative.ARGB(255, 66, 133, 244), EmojiWindowNative.ARGB(255, 255, 255, 255), 12);
            TabInfo1Labels[slot] = CreateLabel(content, 32, 230, 980, 24, string.Empty, EmojiWindowNative.ARGB(255, 95, 99, 104), EmojiWindowNative.ARGB(255, 255, 255, 255), 12);
            TabInfo2Labels[slot] = CreateLabel(content, 32, 260, 980, 24, string.Empty, EmojiWindowNative.ARGB(255, 95, 99, 104), EmojiWindowNative.ARGB(255, 255, 255, 255), 12);
            TabInfo3Labels[slot] = CreateLabel(content, 32, 290, 980, 24, string.Empty, EmojiWindowNative.ARGB(255, 95, 99, 104), EmojiWindowNative.ARGB(255, 255, 255, 255), 12);

            EmojiWindowNative.ShowLabel(TabTitleLabels[slot], 1);
            EmojiWindowNative.ShowLabel(TabSubtitleLabels[slot], 1);
            EmojiWindowNative.ShowLabel(TabStatusLabels[slot], 1);
            EmojiWindowNative.ShowLabel(TabInfo1Labels[slot], 1);
            EmojiWindowNative.ShowLabel(TabInfo2Labels[slot], 1);
            EmojiWindowNative.ShowLabel(TabInfo3Labels[slot], 1);
        }

        private static void LayoutTabControl()
        {
            if (_tabControl != IntPtr.Zero)
            {
                EmojiWindowNative.SetTabControlBounds(_tabControl, 0, 0, _width, _height - 62);
            }
        }

        private static void LayoutAllTabContents()
        {
            for (int i = 1; i <= MaxTabs; i++)
            {
                if (TabUsed[i])
                {
                    LayoutSingleTabContent(i);
                }
            }
        }

        private static void LayoutSingleTabContent(int slot)
        {
            if (slot <= 0 || !TabUsed[slot])
            {
                return;
            }

            int toolbarX = 12;
            int toolbarY = 14;
            int leftButtonStartX = toolbarX + 8;
            int addressX = toolbarX + 160;
            int addressWidth = Math.Max(120, _width - addressX - 36);
            int contentWidth = Math.Max(320, _width - 64);

            if (TabBackButtons[slot] != 0) EmojiWindowNative.SetButtonBounds(TabBackButtons[slot], leftButtonStartX, toolbarY, 32, 32);
            if (TabForwardButtons[slot] != 0) EmojiWindowNative.SetButtonBounds(TabForwardButtons[slot], leftButtonStartX + 36, toolbarY, 32, 32);
            if (TabRefreshButtons[slot] != 0) EmojiWindowNative.SetButtonBounds(TabRefreshButtons[slot], leftButtonStartX + 72, toolbarY, 32, 32);
            if (TabHomeButtons[slot] != 0) EmojiWindowNative.SetButtonBounds(TabHomeButtons[slot], leftButtonStartX + 108, toolbarY, 32, 32);

            if (TabAddressEdits[slot] != IntPtr.Zero)
            {
                EmojiWindowNative.SetEditBoxBounds(TabAddressEdits[slot], addressX, 8, addressWidth, 34);
                EmojiWindowNative.ShowEditBox(TabAddressEdits[slot], 1);
            }

            if (TabTitleLabels[slot] != IntPtr.Zero) EmojiWindowNative.SetLabelBounds(TabTitleLabels[slot], 32, 84, contentWidth, 40);
            if (TabSubtitleLabels[slot] != IntPtr.Zero) EmojiWindowNative.SetLabelBounds(TabSubtitleLabels[slot], 32, 132, contentWidth, 26);
            if (TabStatusLabels[slot] != IntPtr.Zero) EmojiWindowNative.SetLabelBounds(TabStatusLabels[slot], 32, 176, contentWidth, 24);
            if (TabInfo1Labels[slot] != IntPtr.Zero) EmojiWindowNative.SetLabelBounds(TabInfo1Labels[slot], 32, 230, contentWidth, 24);
            if (TabInfo2Labels[slot] != IntPtr.Zero) EmojiWindowNative.SetLabelBounds(TabInfo2Labels[slot], 32, 260, contentWidth, 24);
            if (TabInfo3Labels[slot] != IntPtr.Zero) EmojiWindowNative.SetLabelBounds(TabInfo3Labels[slot], 32, 290, contentWidth, 24);
        }

        private static void SyncActiveTabContent()
        {
            if (_activeSlot <= 0 || !TabUsed[_activeSlot])
            {
                return;
            }

            string currentUrl = TabUrls[_activeSlot];
            string currentTitle = TabTitles[_activeSlot];
            string addressText = TabAddressEdits[_activeSlot] != IntPtr.Zero
                ? EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetEditBoxText, TabAddressEdits[_activeSlot])
                : currentUrl;

            SetLabelText(TabTitleLabels[_activeSlot], currentTitle);
            SetLabelText(TabSubtitleLabels[_activeSlot], "已输入地址：" + addressText);
            SetLabelText(TabStatusLabels[_activeSlot], "页面状态：当前为 C# 演示版内容窗口，可继续接入真实浏览器内核。");
            SetLabelText(TabInfo1Labels[_activeSlot], "Current URL: " + currentUrl);
            SetLabelText(TabInfo2Labels[_activeSlot], "Current Tab: " + _activeSlot);
            SetLabelText(TabInfo3Labels[_activeSlot], "Toolbar Actions: Back / Forward / Refresh / Home");
        }

        private static void RefreshTabTitles()
        {
            for (int i = 1; i <= MaxTabs; i++)
            {
                if (!TabUsed[i])
                {
                    continue;
                }

                byte[] titleBytes = EmojiWindowNative.ToUtf8(TabTitles[i]);
                EmojiWindowNative.SetTabTitle(_tabControl, i - 1, titleBytes, titleBytes.Length);
            }
        }

        private static void OnTabControlCreated(IntPtr hTabControl)
        {
            if (hTabControl == IntPtr.Zero)
            {
                return;
            }

            LayoutTabControl();
            SetStatus("TabControl 已创建并完成初始化");
        }

        private static void OnTabChanged(IntPtr hTabControl, int selectedIndex)
        {
            if (hTabControl != _tabControl || selectedIndex < 0)
            {
                return;
            }

            _activeSlot = selectedIndex + 1;
            SyncActiveTabContent();
            SetStatus("已切换到标签：" + _activeSlot);
        }

        private static void OnTabClose(IntPtr hTabControl, int index)
        {
            if (hTabControl != _tabControl)
            {
                return;
            }

            if (EmojiWindowNative.GetTabCount(hTabControl) <= 1)
            {
                SetStatus("至少保留一个标签页");
                return;
            }

            int slot = index + 1;
            for (int i = slot; i < MaxTabs; i++)
            {
                TabContentWindows[i] = TabContentWindows[i + 1];
                TabBackButtons[i] = TabBackButtons[i + 1];
                TabForwardButtons[i] = TabForwardButtons[i + 1];
                TabRefreshButtons[i] = TabRefreshButtons[i + 1];
                TabHomeButtons[i] = TabHomeButtons[i + 1];
                TabAddressEdits[i] = TabAddressEdits[i + 1];
                TabTitleLabels[i] = TabTitleLabels[i + 1];
                TabSubtitleLabels[i] = TabSubtitleLabels[i + 1];
                TabStatusLabels[i] = TabStatusLabels[i + 1];
                TabInfo1Labels[i] = TabInfo1Labels[i + 1];
                TabInfo2Labels[i] = TabInfo2Labels[i + 1];
                TabInfo3Labels[i] = TabInfo3Labels[i + 1];
                TabUsed[i] = TabUsed[i + 1];
                TabUrls[i] = TabUrls[i + 1];
                TabTitles[i] = TabTitles[i + 1];
            }

            ResetSlot(MaxTabs);

            EmojiWindowNative.RemoveTabItem(hTabControl, index);
            _activeSlot = EmojiWindowNative.GetCurrentTabIndex(hTabControl) + 1;
            if (_activeSlot < 1)
            {
                _activeSlot = 1;
            }

            LayoutAllTabContents();
            SyncActiveTabContent();
            SetStatus("已关闭标签：" + slot);
        }

        private static void OnTabNewButton(IntPtr hTabControl)
        {
            if (hTabControl != _tabControl)
            {
                return;
            }

            AddNewTab(HomeUrl, true, true);
            SetStatus("已新建标签页");
        }

        private static void OnButtonClick(int buttonId, IntPtr parentHwnd)
        {
            int slot = GetSlotByButton(buttonId);
            if (slot == 0)
            {
                return;
            }

            _activeSlot = slot;
            EmojiWindowNative.SelectTabImmediate(_tabControl, slot - 1);

            if (buttonId == TabBackButtons[slot])
            {
                SetStatus("后退按钮已点击，当前为演示版。");
                return;
            }

            if (buttonId == TabForwardButtons[slot])
            {
                SetStatus("前进按钮已点击，当前为演示版。");
                return;
            }

            if (buttonId == TabRefreshButtons[slot])
            {
                SyncActiveTabContent();
                SetStatus("已刷新当前标签信息");
                return;
            }

            if (buttonId == TabHomeButtons[slot])
            {
                TabUrls[slot] = HomeUrl;
                TabTitles[slot] = "google.com/";

                byte[] titleBytes = EmojiWindowNative.ToUtf8(TabTitles[slot]);
                EmojiWindowNative.SetTabTitle(_tabControl, slot - 1, titleBytes, titleBytes.Length);

                if (TabAddressEdits[slot] != IntPtr.Zero)
                {
                    byte[] addressBytes = EmojiWindowNative.ToUtf8(TabUrls[slot]);
                    EmojiWindowNative.SetEditBoxText(TabAddressEdits[slot], addressBytes, addressBytes.Length);
                }

                SyncActiveTabContent();
                SetStatus("已回到主页");
            }
        }

        private static void OnEditKey(IntPtr hEdit, int keyCode, int keyDown, int shift, int ctrl, int alt)
        {
            if (keyDown == 0 || keyCode != 13)
            {
                return;
            }

            int slot = GetSlotByEdit(hEdit);
            if (slot == 0)
            {
                return;
            }

            string text = EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetEditBoxText, hEdit);
            if (string.IsNullOrWhiteSpace(text))
            {
                return;
            }

            _activeSlot = slot;
            TabUrls[slot] = text;
            TabTitles[slot] = GetTabTitle(text);
            RefreshTabTitles();
            SyncActiveTabContent();
            SetStatus("已更新地址：" + text);
        }

        private static void OnWindowResize(IntPtr hwnd, int width, int height)
        {
            if (hwnd != _window || width <= 1 || height <= 1 || _tabControl == IntPtr.Zero)
            {
                return;
            }

            _width = Math.Max(320, width);
            _height = Math.Max(240, height);

            EmojiWindowNative.SetTabControlBounds(_tabControl, 0, 0, _width, _height - 62);
            LayoutAllTabContents();

            if (_activeSlot > 0 && _activeSlot <= EmojiWindowNative.GetTabCount(_tabControl))
            {
                EmojiWindowNative.SelectTabImmediate(_tabControl, _activeSlot - 1);
            }

            EmojiWindowNative.RedrawTabControl(_tabControl);

            if (_statusLabel != IntPtr.Zero)
            {
                EmojiWindowNative.SetLabelBounds(_statusLabel, 20, _height - 32, _width - 40, 24);
            }
        }

        private static void OnWindowClose(IntPtr hwnd)
        {
        }

        private static int CreateToolbarButton(IntPtr parent, string text, int x, int y)
        {
            byte[] textBytes = EmojiWindowNative.ToUtf8(text);
            int buttonId = EmojiWindowNative.create_emoji_button_bytes(
                parent,
                Array.Empty<byte>(),
                0,
                textBytes,
                textBytes.Length,
                x,
                y,
                32,
                32,
                EmojiWindowNative.ARGB(255, 244, 247, 252));

            EmojiWindowNative.SetButtonBackgroundColor(buttonId, EmojiWindowNative.ARGB(255, 244, 247, 252));
            EmojiWindowNative.SetButtonTextColor(buttonId, EmojiWindowNative.ARGB(255, 92, 100, 110));
            EmojiWindowNative.SetButtonBorderColor(buttonId, EmojiWindowNative.ARGB(255, 244, 247, 252));
            EmojiWindowNative.SetButtonHoverColors(
                buttonId,
                EmojiWindowNative.ARGB(255, 232, 238, 246),
                EmojiWindowNative.ARGB(255, 232, 238, 246),
                EmojiWindowNative.ARGB(255, 66, 133, 244));
            EmojiWindowNative.ShowButton(buttonId, 1);
            return buttonId;
        }

        private static IntPtr CreateLabel(IntPtr parent, int x, int y, int width, int height, string text, uint fg, uint bg, int fontSize)
        {
            byte[] textBytes = EmojiWindowNative.ToUtf8(text);
            return EmojiWindowNative.CreateLabel(
                parent,
                x,
                y,
                width,
                height,
                textBytes,
                textBytes.Length,
                fg,
                bg,
                FontBytes,
                FontBytes.Length,
                fontSize,
                0,
                0,
                0,
                0,
                0);
        }

        private static void SetLabelText(IntPtr label, string text)
        {
            if (label == IntPtr.Zero)
            {
                return;
            }

            byte[] textBytes = EmojiWindowNative.ToUtf8(text);
            EmojiWindowNative.SetLabelText(label, textBytes, textBytes.Length);
        }

        private static void SetStatus(string text)
        {
            if (_statusLabel != IntPtr.Zero)
            {
                SetLabelText(_statusLabel, text);
            }
        }

        private static string GetTabTitle(string url)
        {
            if (string.IsNullOrWhiteSpace(url))
            {
                return "New Tab";
            }

            string result = url.Replace("https://", string.Empty).Replace("http://", string.Empty).Replace("www.", string.Empty);
            return result.Length > 18 ? result.Substring(0, 18) : result;
        }

        private static int GetSlotByButton(int buttonId)
        {
            for (int i = 1; i <= MaxTabs; i++)
            {
                if (TabUsed[i] &&
                    (TabBackButtons[i] == buttonId ||
                     TabForwardButtons[i] == buttonId ||
                     TabRefreshButtons[i] == buttonId ||
                     TabHomeButtons[i] == buttonId))
                {
                    return i;
                }
            }

            return 0;
        }

        private static int GetSlotByEdit(IntPtr editHandle)
        {
            for (int i = 1; i <= MaxTabs; i++)
            {
                if (TabUsed[i] && TabAddressEdits[i] == editHandle)
                {
                    return i;
                }
            }

            return 0;
        }

        private static void ResetSlot(int slot)
        {
            TabUsed[slot] = false;
            TabUrls[slot] = string.Empty;
            TabTitles[slot] = string.Empty;
            TabContentWindows[slot] = IntPtr.Zero;
            TabBackButtons[slot] = 0;
            TabForwardButtons[slot] = 0;
            TabRefreshButtons[slot] = 0;
            TabHomeButtons[slot] = 0;
            TabAddressEdits[slot] = IntPtr.Zero;
            TabTitleLabels[slot] = IntPtr.Zero;
            TabSubtitleLabels[slot] = IntPtr.Zero;
            TabStatusLabels[slot] = IntPtr.Zero;
            TabInfo1Labels[slot] = IntPtr.Zero;
            TabInfo2Labels[slot] = IntPtr.Zero;
            TabInfo3Labels[slot] = IntPtr.Zero;
        }
    }
}
