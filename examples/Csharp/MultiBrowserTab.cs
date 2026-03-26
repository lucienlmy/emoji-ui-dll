using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;

/// <summary>
/// 多标签浏览器示例 - C# 版本
/// 使用 emoji_window.dll 创建多标签浏览器框架
/// CEF3 浏览器嵌入部分需自行实现
/// </summary>
public class MultiBrowserTab
{
    // ========== DLL 导入：emoji_window.dll ==========
    [DllImport("emoji_window.dll")] static extern int create_window_bytes_ex(IntPtr titleBytes, int titleLen, int x, int y, int w, int h, int titlebarColor, int clientBgColor);
    [DllImport("emoji_window.dll")] static extern void set_message_loop_main_window(int hwnd);
    [DllImport("emoji_window.dll")] static extern int run_message_loop();
    [DllImport("emoji_window.dll")] static extern int SetTitleBarTextColor(int hwnd, uint color);
    [DllImport("emoji_window.dll")] static extern int SetTitleBarFont(int hwnd, IntPtr fontName, int fontNameLen, float fontSize);
    [DllImport("emoji_window.dll")] static extern int CreateTabControl(int hParent, int x, int y, int w, int h);
    [DllImport("emoji_window.dll")] static extern int AddTabItem(int hTab, IntPtr titleBytes, int titleLen, int iconIndex);
    [DllImport("emoji_window.dll")] static extern bool RemoveTabItem(int hTab, int index);
    [DllImport("emoji_window.dll")] static extern int GetTabCount(int hTab);
    [DllImport("emoji_window.dll")] static extern int GetTabContentWindow(int hTab, int index);
    [DllImport("emoji_window.dll")] static extern bool SelectTab(int hTab, int index);
    [DllImport("emoji_window.dll")] static extern int SetTabControlBounds(int hTab, int x, int y, int w, int h);
    [DllImport("emoji_window.dll")] static extern int SetTabItemSize(int hTab, int w, int h);
    [DllImport("emoji_window.dll")] static extern int SetTabFont(int hTab, IntPtr fontName, int fontNameLen, float fontSize);
    [DllImport("emoji_window.dll")] static extern int SetTabColors(int hTab, uint selBg, uint unselBg, uint selText, uint unselText);
    [DllImport("emoji_window.dll")] static extern int SetTabIndicatorColor(int hTab, uint color);
    [DllImport("emoji_window.dll")] static extern int SetTabPadding(int hTab, int h, int v);
    [DllImport("emoji_window.dll")] static extern int SetTabClosable(int hTab, int closable);
    [DllImport("emoji_window.dll")] static extern int SetTabDraggable(int hTab, int draggable);
    [DllImport("emoji_window.dll")] static extern int SetTabScrollable(int hTab, int scrollable);
    [DllImport("emoji_window.dll")] static extern int SetTabContentBgColor(int hTab, int index, uint color);
    [DllImport("emoji_window.dll")] static extern int create_emoji_button_bytes(int parent, IntPtr emojiBytes, int emojiLen, IntPtr textBytes, int textLen, int x, int y, int w, int h, uint bgColor);
    [DllImport("emoji_window.dll")] static extern void SetButtonBounds(int buttonId, int x, int y, int w, int h);
    [DllImport("emoji_window.dll")] static extern int CreateEditBox(int parent, int x, int y, int w, int h, IntPtr textBytes, int textLen, uint fgColor, uint bgColor, IntPtr fontNameBytes, int fontNameLen, int fontSize, int bold, int italic, int underline, int alignment, int multiline, int readOnly, int password, int hasBorder, int verticalCenter);
    [DllImport("emoji_window.dll")] static extern void SetEditBoxBounds(int hEdit, int x, int y, int w, int h);
    [DllImport("emoji_window.dll")] static extern int CreateLabel(int parent, int x, int y, int w, int h, IntPtr textBytes, int textLen, uint fgColor, uint bgColor, IntPtr fontNameBytes, int fontNameLen, int fontSize, int bold, int italic, int underline, int alignment, int wordWrap);
    [DllImport("emoji_window.dll")] static extern void SetLabelText(int hLabel, IntPtr textBytes, int textLen);
    [DllImport("emoji_window.dll")] static extern void SetLabelBounds(int hLabel, int x, int y, int w, int h);
    [DllImport("emoji_window.dll")] static extern int CreateProgressBar(int parent, int x, int y, int w, int h, int initValue, uint fgColor, uint bgColor, int showText, uint textColor);
    [DllImport("emoji_window.dll")] static extern void SetProgressBarBounds(int hProgress, int x, int y, int w, int h);

    // 回调
    delegate void TabSwitchCB(int hTab, int index);
    delegate void TabCloseCB(int hTab, int index);
    delegate void TabRightClickCB(int hTab, int index, int x, int y);
    delegate void TabDblClickCB(int hTab, int index);
    delegate void ButtonClickCB(int buttonId, int parentHwnd);
    delegate void WindowResizeCB(int hwnd, int newW, int newH);
    [DllImport("emoji_window.dll")] static extern int SetTabCallback(int hTab, TabSwitchCB cb);
    [DllImport("emoji_window.dll")] static extern int SetTabCloseCallback(int hTab, TabCloseCB cb);
    [DllImport("emoji_window.dll")] static extern int SetTabRightClickCallback(int hTab, TabRightClickCB cb);
    [DllImport("emoji_window.dll")] static extern int SetTabDoubleClickCallback(int hTab, TabDblClickCB cb);
    [DllImport("emoji_window.dll")] static extern void set_button_click_callback(ButtonClickCB cb);
    [DllImport("emoji_window.dll")] static extern void SetWindowResizeCallback(WindowResizeCB cb);

    // ========== DLL 导入：Win32 原生 API ==========
    [DllImport("user32.dll", CharSet = CharSet.Ansi)] static extern int CreateWindowExA(int exStyle, string className, string windowName, int style, int x, int y, int w, int h, int parent, int menu, int hInstance, int param);
    [DllImport("user32.dll")] static extern bool MoveWindow(int hwnd, int x, int y, int w, int h, bool repaint);
    [DllImport("user32.dll")] static extern IntPtr CreatePopupMenu();
    [DllImport("user32.dll", CharSet = CharSet.Ansi)] static extern bool AppendMenuA(IntPtr hMenu, uint flags, uint idNewItem, string newItem);
    [DllImport("user32.dll")] static extern int TrackPopupMenu(IntPtr hMenu, uint flags, int x, int y, int reserved, IntPtr hwnd, IntPtr rect);
    [DllImport("kernel32.dll", CharSet = CharSet.Ansi)] static extern int GetModuleHandleA(string moduleName);

    // ========== 常量 ==========
    const int NAV_BAR_HEIGHT = 44;
    const int STATUS_BAR_HEIGHT = 28;
    const int MAX_TABS = 50;

    // ========== 成员变量 ==========
    static int _mainWindow, _tabControl, _statusLabel, _progressBar, _btnNewTab;
    static IntPtr _contextMenu;
    static int _rightClickTabIndex;

    // 每个Tab的子控件句柄
    static int[] _tabEditBox = new int[MAX_TABS];
    static int[] _tabFavBtnId = new int[MAX_TABS];
    static int[] _tabCefContainer = new int[MAX_TABS];

    // 防止回调被 GC 回收
    static TabSwitchCB _tabSwitchCb;
    static TabCloseCB _tabCloseCb;
    static TabRightClickCB _tabRightClickCb;
    static TabDblClickCB _tabDblClickCb;
    static ButtonClickCB _buttonClickCb;
    static WindowResizeCB _windowResizeCb;

    // ========== 辅助方法 ==========
    static uint ARGB(byte a, byte r, byte g, byte b) => ((uint)a << 24) | ((uint)r << 16) | ((uint)g << 8) | b;
    static int RGB(byte r, byte g, byte b) => (r << 16) | (g << 8) | b;

    static IntPtr Pin(byte[] data, out GCHandle h) { h = GCHandle.Alloc(data, GCHandleType.Pinned); return h.AddrOfPinnedObject(); }

    static int CreateNavButton(int parent, byte[] emoji, int x, int y, int w, int h)
    {
        GCHandle hE, hT;
        var pE = Pin(emoji, out hE);
        var pT = Pin(new byte[0], out hT);
        int id = create_emoji_button_bytes(parent, pE, emoji.Length, pT, 0, x, y, w, h, ARGB(255, 241, 243, 244));
        hE.Free(); hT.Free();
        return id;
    }

    static byte[] Concat(byte[] a, byte[] b)
    {
        var r = new byte[a.Length + b.Length];
        Buffer.BlockCopy(a, 0, r, 0, a.Length);
        Buffer.BlockCopy(b, 0, r, a.Length, b.Length);
        return r;
    }

    static void SetStatus(string text)
    {
        byte[] utf8 = Encoding.UTF8.GetBytes(text);
        GCHandle h; var p = Pin(utf8, out h);
        SetLabelText(_statusLabel, p, utf8.Length);
        h.Free();
    }

    // ========== 主入口 ==========
    static void Main()
    {
        // 创建窗口
        byte[] title = Concat(new byte[] { 240, 159, 140, 144, 32 }, Encoding.UTF8.GetBytes("多标签浏览器"));
        GCHandle h; var p = Pin(title, out h);
        _mainWindow = create_window_bytes_ex(p, title.Length, -1, -1, 1200, 800, RGB(45, 45, 48), (int)ARGB(255, 240, 240, 240));
        h.Free();

        SetTitleBarTextColor(_mainWindow, ARGB(255, 255, 255, 255));
        byte[] fontYH = Encoding.UTF8.GetBytes("微软雅黑");
        p = Pin(fontYH, out h); SetTitleBarFont(_mainWindow, p, fontYH.Length, 13f); h.Free();

        // TabControl（右侧留40px给➕按钮）
        _tabControl = CreateTabControl(_mainWindow, 0, 0, 1120, 730);
        SetTabItemSize(_tabControl, 180, 34);
        byte[] fontSE = Encoding.UTF8.GetBytes("Segoe UI Emoji");
        p = Pin(fontSE, out h); SetTabFont(_tabControl, p, fontSE.Length, 12f); h.Free();
        SetTabColors(_tabControl, ARGB(255,255,255,255), ARGB(255,222,225,230), ARGB(255,32,33,36), ARGB(255,95,99,104));
        SetTabIndicatorColor(_tabControl, ARGB(255, 64, 158, 255));
        SetTabPadding(_tabControl, 8, 2);
        SetTabClosable(_tabControl, 1);
        SetTabDraggable(_tabControl, 1);
        SetTabScrollable(_tabControl, 1);

        // 回调
        _tabSwitchCb = OnTabSwitch; _tabCloseCb = OnTabClose;
        _tabRightClickCb = OnTabRightClick; _tabDblClickCb = OnTabDblClick;
        _buttonClickCb = OnButtonClick; _windowResizeCb = OnWindowResize;
        SetTabCallback(_tabControl, _tabSwitchCb);
        SetTabCloseCallback(_tabControl, _tabCloseCb);
        SetTabRightClickCallback(_tabControl, _tabRightClickCb);
        SetTabDoubleClickCallback(_tabControl, _tabDblClickCb);
        set_button_click_callback(_buttonClickCb);
        SetWindowResizeCallback(_windowResizeCb);

        // Win32 原生右键菜单
        _contextMenu = CreatePopupMenu();
        AppendMenuA(_contextMenu, 0, 101, "新建标签页");
        AppendMenuA(_contextMenu, 0, 102, "关闭当前标签页");
        AppendMenuA(_contextMenu, 0, 103, "关闭其他标签页");

        AddBrowserTab("https://www.baidu.com");

        // ➕ 按钮
        _btnNewTab = CreateNavButton(_mainWindow, new byte[] { 226, 158, 149 }, 1122, 2, 34, 30);

        // 状态栏
        byte[] readyTxt = Encoding.UTF8.GetBytes("就绪");
        GCHandle h1, h2;
        var p1 = Pin(readyTxt, out h1); var p2 = Pin(fontYH, out h2);
        _statusLabel = CreateLabel(_mainWindow, 0, 740, 1000, STATUS_BAR_HEIGHT, p1, readyTxt.Length, ARGB(255,96,98,102), ARGB(255,245,245,245), p2, fontYH.Length, 11, 0,0,0,0,0);
        h1.Free(); h2.Free();
        _progressBar = CreateProgressBar(_mainWindow, 1000, 740, 160, STATUS_BAR_HEIGHT, 100, ARGB(255,64,158,255), ARGB(255,230,230,230), 1, ARGB(255,255,255,255));

        set_message_loop_main_window(_mainWindow);
        run_message_loop();
    }

    // ========== 添加浏览器标签页 ==========
    static void AddBrowserTab(string defaultUrl)
    {
        byte[] tabTitle = Concat(new byte[] { 240, 159, 140, 144, 32 }, Encoding.UTF8.GetBytes("新标签页"));
        GCHandle h; var p = Pin(tabTitle, out h);
        int idx = GetTabCount(_tabControl);
        AddTabItem(_tabControl, p, tabTitle.Length, 0); h.Free();

        int contentWnd = GetTabContentWindow(_tabControl, idx);
        SetTabContentBgColor(_tabControl, idx, ARGB(255, 255, 255, 255));

        // 导航按钮
        CreateNavButton(contentWnd, new byte[]{226,151,128}, 4, 4, 36, 36);   // ◀
        CreateNavButton(contentWnd, new byte[]{226,150,182}, 44, 4, 36, 36);  // ▶
        CreateNavButton(contentWnd, new byte[]{240,159,148,132}, 84, 4, 36, 36); // 🔄
        CreateNavButton(contentWnd, new byte[]{240,159,143,160}, 124, 4, 36, 36); // 🏠

        // 地址栏
        byte[] url = Encoding.UTF8.GetBytes(defaultUrl);
        byte[] fontSU = Encoding.UTF8.GetBytes("Segoe UI");
        GCHandle h1, h2;
        var p1 = Pin(url, out h1); var p2 = Pin(fontSU, out h2);
        int editBox = CreateEditBox(contentWnd, 168, 6, 900, 32, p1, url.Length, ARGB(255,32,33,36), ARGB(255,241,243,244), p2, fontSU.Length, 13, 0,0,0,0, 0,0,0,1,1);
        h1.Free(); h2.Free();

        // ⭐ 收藏
        int favBtn = CreateNavButton(contentWnd, new byte[]{226,173,144}, 1076, 4, 36, 36);

        // CEF 容器
        int cef = CreateWindowExA(0, "Static", "", 0x52000000, 0, NAV_BAR_HEIGHT, 1160, 680, contentWnd, 0, GetModuleHandleA(null), 0);

        // 保存句柄
        _tabEditBox[idx] = editBox;
        _tabFavBtnId[idx] = favBtn;
        _tabCefContainer[idx] = cef;

        SelectTab(_tabControl, idx);
    }

    // ========== 回调 ==========
    static void OnTabSwitch(int hTab, int index) => SetStatus($"已切换到标签页 {index}");

    static void OnTabClose(int hTab, int index)
    {
        if (GetTabCount(hTab) <= 1) { SetStatus("至少保留一个标签页"); return; }
        RemoveTabItem(hTab, index);
        SetStatus($"已关闭标签页，剩余：{GetTabCount(hTab)}");
    }

    static void OnTabRightClick(int hTab, int index, int x, int y)
    {
        _rightClickTabIndex = index;
        // TPM_RETURNCMD = 0x0100 = 256
        int cmd = TrackPopupMenu(_contextMenu, 256, x, y, 0, (IntPtr)_mainWindow, IntPtr.Zero);
        if (cmd == 101) AddBrowserTab("https://www.baidu.com");
        else if (cmd == 102 && GetTabCount(_tabControl) > 1) RemoveTabItem(_tabControl, _rightClickTabIndex);
        else if (cmd == 103)
        {
            int keep = _rightClickTabIndex;
            for (int i = GetTabCount(_tabControl) - 1; i >= 0; i--)
            {
                if (i != keep) { RemoveTabItem(_tabControl, i); if (i < keep) keep--; }
            }
        }
    }

    static void OnTabDblClick(int hTab, int index) => SetStatus($"双击了标签页 {index}");

    static void OnButtonClick(int buttonId, int parentHwnd)
    {
        if (buttonId == _btnNewTab) AddBrowserTab("https://www.baidu.com");
    }

    static void OnWindowResize(int hwnd, int newW, int newH)
    {
        if (hwnd != _mainWindow) return;

        int tabAreaH = newH - STATUS_BAR_HEIGHT;
        SetTabControlBounds(_tabControl, 0, 0, newW - 40, tabAreaH);
        SetButtonBounds(_btnNewTab, newW - 40, 2, 34, 30);
        SetLabelBounds(_statusLabel, 0, newH - STATUS_BAR_HEIGHT, newW - 160, STATUS_BAR_HEIGHT);
        SetProgressBarBounds(_progressBar, newW - 160, newH - STATUS_BAR_HEIGHT, 160, STATUS_BAR_HEIGHT);

        // 调整每个Tab内容窗口中的子控件
        int contentW = newW - 40;
        int contentH = tabAreaH - 38; // 标签栏高度约38px
        int addrBarW = Math.Max(contentW - 224, 100);

        int count = GetTabCount(_tabControl);
        for (int i = 0; i < count; i++)
        {
            if (_tabEditBox[i] != 0)
                SetEditBoxBounds(_tabEditBox[i], 168, 6, addrBarW, 32);
            if (_tabFavBtnId[i] != 0)
                SetButtonBounds(_tabFavBtnId[i], 168 + addrBarW + 8, 4, 36, 36);
            if (_tabCefContainer[i] != 0)
                MoveWindow(_tabCefContainer[i], 0, NAV_BAR_HEIGHT, contentW, contentH - NAV_BAR_HEIGHT, true);
        }
    }
}
