using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.InteropServices;
using EmojiWindowDemo;

namespace EmojiWindowEcommerceMultiAccountDemo
{
    internal sealed class EcommerceFixedLayoutApp
    {
        private const int TitleBarHeight = 32;

        private sealed class MetricCard
        {
            public IntPtr Panel { get; set; }
            public IntPtr Accent { get; set; }
            public IntPtr Value { get; set; }
            public IntPtr Title { get; set; }
            public IntPtr Hint { get; set; }
            public IntPtr Badge { get; set; }
            public uint AccentColor { get; set; }
        }

        private readonly byte[] _fontYaHei = EmojiWindowNative.ToUtf8("Microsoft YaHei UI");
        private readonly byte[] _fontSegoe = EmojiWindowNative.ToUtf8("Segoe UI");
        private readonly Dictionary<int, Action> _buttonActions = new Dictionary<int, Action>();
        private readonly MetricCard[] _cards = new MetricCard[6];
        private readonly string[] _channelItems = { "🌐 全部渠道", "🛒 Amazon", "🛍️ Shopify" };
        private readonly string[] _storeItems = { "全部店铺", "美国站A店", "美国站B店" };
        private readonly string[] _statusItems = { "🎯 全部状态", "🟢 运行中", "🔵 空闲", "🔴 异常" };

        private readonly EmojiWindowNative.ButtonClickCallback _buttonClickCallback;
        private readonly EmojiWindowNative.WindowResizeCallback _windowResizeCallback;
        private readonly EmojiWindowNative.EditBoxKeyCallback _urlEditKeyCallback;

        private IntPtr _window;
        private int _width = 1440;
        private int _height = 900;
        private bool _darkMode;

        private IntPtr _sidebarPanel;
        private IntPtr _workspacePanel;
        private IntPtr _browserPanel;
        private IntPtr _statusBar;

        private IntPtr _cmbChannel;
        private IntPtr _cmbStore;
        private IntPtr _cmbStatus;
        private IntPtr _txtSearch;
        private IntPtr _txtUrl;
        private IntPtr _grid;

        private int _btnTheme;
        private int _btnQuery;
        private int _btnReset;
        private int _btnAdd;
        private int _btnImport;
        private int _btnExport;
        private int _btnRefresh;
        private int _btnBatchStart;
        private int _btnBatchStop;
        private int _btnBatchDelete;
        private int _btnSelectAll;
        private int _btnLaunch;
        private int _btnStop;
        private int _btnRefreshPage;
        private int _btnClearCache;
        private int _btnRelogin;
        private int _btnOpenProduct;

        private IntPtr _lblSidebarTitle;
        private IntPtr _lblWorkspaceTitle;
        private IntPtr _lblBrowserEmpty;
        private IntPtr _lblBrowserSub;

        public EcommerceFixedLayoutApp()
        {
            _buttonClickCallback = OnButtonClick;
            _windowResizeCallback = OnResize;
            _urlEditKeyCallback = OnUrlEditKey;
        }

        public void Run()
        {
            CreateWindow();
            using (new RedrawScope(_window))
            {
                CreateControls();
                SeedGrid();
                ApplyTheme();
                Layout();
            }

            EmojiWindowNative.SetEditBoxKeyCallback(_txtUrl, _urlEditKeyCallback);
            EmojiWindowNative.set_button_click_callback(_buttonClickCallback);
            EmojiWindowNative.SetWindowResizeCallback(_windowResizeCallback);
            EmojiWindowNative.ShowEmojiWindow(_window, 1);
            RefreshComboVisualsAfterTheme();
            EmojiWindowNative.set_message_loop_main_window(_window);
            EmojiWindowNative.run_message_loop();
        }

        private void CreateWindow()
        {
            byte[] title = EmojiWindowNative.ToUtf8("电商多账号浏览器管理器");
            _window = EmojiWindowNative.create_window_bytes_ex(title, title.Length, -1, -1, _width, _height, Argb(255, 38, 70, 124), Argb(255, 241, 245, 250));
            EmojiWindowNative.SetTitleBarTextColor(_window, Argb(255, 255, 255, 255));

            string iconPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "favicon.ico");
            if (!File.Exists(iconPath))
            {
                iconPath = @"T:\易语言源码\API创建窗口\emoji_window_cpp\examples\Csharp\EmojiWindowEcommerceMultiAccountDemo\favicon.ico";
            }

            if (File.Exists(iconPath))
            {
                byte[] icon = File.ReadAllBytes(iconPath);
                EmojiWindowNative.set_window_icon_bytes(_window, icon, icon.Length);
            }
        }

        private void CreateControls()
        {
            string[] titles = { "今日在线", "运行中", "异常账号", "待处理", "店铺数", "代理正常率" };
            string[] hints = { "+2 vs yesterday", "+1 active now", "need review", "queue waiting", "5 stores linked", "check proxies" };
            string[] badges = { "OPS", "LIVE", "RISK", "TODO", "SHOP", "NET" };
            uint[] accents = { Argb(255, 59, 130, 246), Argb(255, 34, 197, 94), Argb(255, 239, 68, 68), Argb(255, 245, 158, 11), Argb(255, 6, 182, 212), Argb(255, 59, 130, 246) };
            string[] values = { "3", "2", "2", "3", "5", "75%" };

            for (int i = 0; i < _cards.Length; i++)
            {
                IntPtr panel = EmojiWindowNative.CreatePanel(_window, 0, 0, 100, 80, Argb(255, 255, 255, 255));
                _cards[i] = new MetricCard
                {
                    Panel = panel,
                    Accent = EmojiWindowNative.CreatePanel(panel, 0, 0, 100, 6, accents[i]),
                    Value = Label(panel, values[i], 24, true, accents[i], Argb(255, 255, 255, 255)),
                    Title = Label(panel, titles[i], 11, false, Argb(255, 71, 85, 105), Argb(255, 255, 255, 255)),
                    Hint = Label(panel, hints[i], 10, false, Argb(255, 100, 116, 139), Argb(255, 255, 255, 255)),
                    Badge = Label(panel, badges[i], 9, true, Argb(255, 255, 255, 255), accents[i]),
                    AccentColor = accents[i]
                };
            }

            _sidebarPanel = EmojiWindowNative.CreatePanel(_window, 0, 0, 100, 100, Argb(255, 255, 255, 255));
            _workspacePanel = EmojiWindowNative.CreatePanel(_window, 0, 0, 100, 100, Argb(255, 255, 255, 255));
            _browserPanel = EmojiWindowNative.CreatePanel(_workspacePanel, 0, 0, 100, 100, Argb(255, 222, 228, 238));
            _statusBar = Label(_window, string.Empty, 11, false, Argb(255, 107, 114, 128), Argb(255, 241, 245, 250));

            _lblSidebarTitle = Label(_sidebarPanel, "账号管理", 13, true, Argb(255, 31, 41, 55), Argb(255, 255, 255, 255));
            _lblWorkspaceTitle = Label(_workspacePanel, "工作区", 13, true, Argb(255, 31, 41, 55), Argb(255, 255, 255, 255));
            _lblBrowserEmpty = Label(_browserPanel, "浏览器容器区域", 20, true, Argb(255, 45, 55, 72), Argb(255, 222, 228, 238));
            _lblBrowserSub = Label(_browserPanel, "这里接入浏览器宿主窗口", 12, false, Argb(255, 88, 100, 118), Argb(255, 222, 228, 238));

            _cmbChannel = Combo(_sidebarPanel);
            _cmbStore = Combo(_sidebarPanel);
            _cmbStatus = Combo(_sidebarPanel);
            FillCombo(_cmbChannel, new[] { "🌐 全部渠道", "🛒 Amazon", "🛍️ Shopify" });
            FillCombo(_cmbStore, new[] { "全部店铺", "美国站A店", "美国站B店" });
            FillCombo(_cmbStatus, new[] { "🎯 全部状态", "🟢 运行中", "🔵 空闲", "🔴 异常" });

            _txtSearch = Edit(_sidebarPanel, "🔍 搜索账号/备注/店铺");
            _txtUrl = Edit(_workspacePanel, "https://admin.shopify.com/");

            _btnTheme = Button(_window, "☀️", Argb(255, 156, 163, 175), null);
            _btnQuery = Button(_sidebarPanel, "查询", Argb(255, 59, 130, 246), null);
            _btnReset = Button(_sidebarPanel, "重置", Argb(255, 148, 163, 184), null);
            _btnAdd = Button(_sidebarPanel, "新增", Argb(255, 59, 130, 246), null);
            _btnImport = Button(_sidebarPanel, "导入", Argb(255, 148, 163, 184), null);
            _btnExport = Button(_sidebarPanel, "导出", Argb(255, 148, 163, 184), null);
            _btnRefresh = Button(_sidebarPanel, "刷新", Argb(255, 148, 163, 184), null);
            _btnBatchStart = Button(_sidebarPanel, "批量启动", Argb(255, 34, 197, 94), null);
            _btnBatchStop = Button(_sidebarPanel, "批量停止", Argb(255, 245, 158, 11), null);
            _btnBatchDelete = Button(_sidebarPanel, "批量删除", Argb(255, 239, 68, 68), null);
            _btnSelectAll = Button(_sidebarPanel, "全选", Argb(255, 148, 163, 184), null);

            _btnLaunch = Button(_workspacePanel, "启动浏览器", Argb(255, 59, 130, 246), null);
            _btnStop = Button(_workspacePanel, "停止", Argb(255, 245, 158, 11), null);
            _btnRefreshPage = Button(_workspacePanel, "刷新", Argb(255, 148, 163, 184), null);
            _btnClearCache = Button(_workspacePanel, "清缓存", Argb(255, 148, 163, 184), null);
            _btnRelogin = Button(_workspacePanel, "重登", Argb(255, 148, 163, 184), null);
            _btnOpenProduct = Button(_workspacePanel, "打开商品页", Argb(255, 34, 197, 94), null);

            _grid = EmojiWindowNative.CreateDataGridView(_sidebarPanel, 0, 0, 100, 100, 0, 1, Argb(255, 31, 41, 55), Argb(255, 255, 255, 255));
            // 初始宽度仅作占位；Layout() 中按 innerW 与 ApplyGridColumnWidths 对齐，避免列宽之和大于表格区域出现横向滚动条
            EmojiWindowNative.DataGrid_AddCheckBoxColumn(_grid, U("选"), U("选").Length, 30);
            EmojiWindowNative.DataGrid_AddTextColumn(_grid, U("账号"), U("账号").Length, 88);
            EmojiWindowNative.DataGrid_AddTextColumn(_grid, U("店铺"), U("店铺").Length, 62);
            EmojiWindowNative.DataGrid_AddTextColumn(_grid, U("备注"), U("备注").Length, 80);
            EmojiWindowNative.DataGrid_AddTextColumn(_grid, U("状态"), U("状态").Length, 48);
            EmojiWindowNative.DataGrid_SetHeaderHeight(_grid, 34);
            EmojiWindowNative.DataGrid_SetDefaultRowHeight(_grid, 34);
            EmojiWindowNative.DataGrid_SetColors(_grid, Argb(255, 31, 41, 55), Argb(255, 255, 255, 255), Argb(255, 243, 246, 252), Argb(255, 71, 85, 105), Argb(255, 236, 245, 255), Argb(255, 248, 250, 252), Argb(255, 229, 231, 235));
        }

        private void SeedGrid()
        {
            AddRow("brand_site_01", "独立站A", "品牌站/大促页", "运行中");
            AddRow("shop_jp_001", "日本站A", "活动专用", "登录中");
            AddRow("shop_uk_003", "英国站B", "高客单品", "异常");
            AddRow("shop_us_001", "美国站A", "主账号/独享", "运行中");
            AddRow("shop_us_002", "美国站B", "备用账号/广告", "空闲");
        }

        private void AddRow(string account, string store, string note, string status)
        {
            int row = EmojiWindowNative.DataGrid_AddRow(_grid);
            SetGrid(row, 1, account);
            SetGrid(row, 2, store);
            SetGrid(row, 3, note);
            SetGrid(row, 4, status);
        }

        /// <summary>列宽比例与 CreateControls 中设计一致（合计 308）；按侧栏 innerW 缩放使列宽之和等于表格客户区宽度。</summary>
        private static readonly int[] GridColumnWidthsBase = { 30, 88, 62, 80, 48 };

        private void ApplyGridColumnWidths(int innerWidth)
        {
            if (_grid == IntPtr.Zero || innerWidth < 200)
            {
                return;
            }

            int[] @base = GridColumnWidthsBase;
            int sumBase = 0;
            for (int i = 0; i < @base.Length; i++)
            {
                sumBase += @base[i];
            }

            int[] col = new int[5];
            int used = 0;
            for (int i = 0; i < 4; i++)
            {
                int v = (@base[i] * innerWidth + sumBase / 2) / sumBase;
                if (v < 30)
                {
                    v = 30;
                }
                col[i] = v;
                used += v;
            }
            col[4] = innerWidth - used;
            if (col[4] < 30)
            {
                int deficit = 30 - col[4];
                col[3] = Math.Max(30, col[3] - deficit);
                col[4] = innerWidth - col[0] - col[1] - col[2] - col[3];
            }

            for (int i = 0; i < 5; i++)
            {
                EmojiWindowNative.DataGrid_SetColumnWidth(_grid, i, col[i]);
            }
        }

        private void Layout()
        {
            int padding = 16;
            int gap = 12;
            int topInset = TitleBarHeight + 8;
            int cardsY = topInset;
            int cardsHeight = 96;
            int contentY = cardsY + cardsHeight + 6;
            int contentBottom = _height - 36;
            int contentHeight = contentBottom - contentY;
            int usable = _width - padding * 2 - gap;
            int leftWidth = Math.Max(440, Math.Min(520, usable * 32 / 100));
            int rightX = padding + leftWidth + gap;
            int rightWidth = _width - rightX - padding;

            int cardWidth = (_width - padding * 2 - gap * 5) / 6;
            for (int i = 0; i < _cards.Length; i++)
            {
                int x = padding + i * (cardWidth + gap);
                MetricCard card = _cards[i];
                MoveWindow(card.Panel, x, cardsY, cardWidth, cardsHeight);
                MoveWindow(card.Accent, 0, 0, cardWidth, 6);
                EmojiWindowNative.SetLabelBounds(card.Badge, cardWidth - 74, 14, 52, 18);
                EmojiWindowNative.SetLabelBounds(card.Value, 14, 18, cardWidth - 28, 28);
                EmojiWindowNative.SetLabelBounds(card.Title, 14, 50, cardWidth - 28, 18);
                EmojiWindowNative.SetLabelBounds(card.Hint, 14, 78, cardWidth - 28, 14);
            }

            MoveWindow(_sidebarPanel, padding, contentY, leftWidth, contentHeight);
            MoveWindow(_workspacePanel, rightX, contentY, rightWidth, contentHeight);

            int sx = 12;
            int innerW = leftWidth - 24;
            int rowGap = 8;
            int comboW = (innerW - rowGap * 2) / 3;
            int comboTop = 10;
            int vGap = 8;
            int searchY = comboTop + 34 + vGap;
            int actionsY1 = searchY + 34 + vGap;
            int actionsY2 = actionsY1 + 34 + vGap;
            int accountTitleY = actionsY2 + 34 + vGap;
            int gridY = accountTitleY + 20 + vGap;
            int gridBottomMargin = 24;
            SetComboBoxBounds(_cmbChannel, sx, comboTop, comboW, 34);
            SetComboBoxBounds(_cmbStore, sx + comboW + rowGap, comboTop, comboW, 34);
            SetComboBoxBounds(_cmbStatus, sx + (comboW + rowGap) * 2, comboTop, comboW, 34);

            int searchBtnW = 58;
            int searchW = innerW - searchBtnW * 2 - rowGap * 2;
            EmojiWindowNative.SetEditBoxBounds(_txtSearch, sx, searchY, searchW, 34);
            EmojiWindowNative.SetButtonBounds(_btnQuery, padding + sx + searchW + rowGap, contentY + searchY, searchBtnW, 34);
            EmojiWindowNative.SetButtonBounds(_btnReset, padding + sx + searchW + rowGap + searchBtnW + rowGap, contentY + searchY, searchBtnW, 34);

            int btnW = (innerW - rowGap * 3) / 4;
            EmojiWindowNative.SetButtonBounds(_btnAdd, padding + sx, contentY + actionsY1, btnW, 34);
            EmojiWindowNative.SetButtonBounds(_btnImport, padding + sx + btnW + rowGap, contentY + actionsY1, btnW, 34);
            EmojiWindowNative.SetButtonBounds(_btnExport, padding + sx + (btnW + rowGap) * 2, contentY + actionsY1, btnW, 34);
            EmojiWindowNative.SetButtonBounds(_btnRefresh, padding + sx + (btnW + rowGap) * 3, contentY + actionsY1, btnW, 34);
            EmojiWindowNative.SetButtonBounds(_btnSelectAll, padding + sx, contentY + actionsY2, btnW, 34);
            EmojiWindowNative.SetButtonBounds(_btnBatchStart, padding + sx + btnW + rowGap, contentY + actionsY2, btnW, 34);
            EmojiWindowNative.SetButtonBounds(_btnBatchStop, padding + sx + (btnW + rowGap) * 2, contentY + actionsY2, btnW, 34);
            EmojiWindowNative.SetButtonBounds(_btnBatchDelete, padding + sx + (btnW + rowGap) * 3, contentY + actionsY2, btnW, 34);

            EmojiWindowNative.SetLabelBounds(_lblSidebarTitle, sx, accountTitleY, innerW, 20);
            EmojiWindowNative.DataGrid_SetBounds(_grid, sx, gridY, innerW, contentHeight - gridY - gridBottomMargin);
            ApplyGridColumnWidths(innerW);

            int wx = 14;
            int workW = rightWidth - 28;
            int themeBtnW = 34;
            int urlGap = 12;
            int urlTop = 10;
            int workRowGap = 8;
            EmojiWindowNative.SetLabelBounds(_lblWorkspaceTitle, -2000, -2000, 1, 1);
            EmojiWindowNative.SetEditBoxBounds(_txtUrl, wx, urlTop, workW - themeBtnW - urlGap, 34);
            EmojiWindowNative.SetButtonBounds(_btnTheme, rightX + wx + workW - themeBtnW, contentY + urlTop, themeBtnW, 34);

            int actionY = urlTop + 34 + workRowGap;
            EmojiWindowNative.SetButtonBounds(_btnLaunch, rightX + wx, contentY + actionY, 92, 34);
            EmojiWindowNative.SetButtonBounds(_btnStop, rightX + wx + 100, contentY + actionY, 70, 34);
            EmojiWindowNative.SetButtonBounds(_btnRefreshPage, rightX + wx + 178, contentY + actionY, 70, 34);
            EmojiWindowNative.SetButtonBounds(_btnClearCache, rightX + wx + 256, contentY + actionY, 82, 34);
            EmojiWindowNative.SetButtonBounds(_btnRelogin, rightX + wx + 346, contentY + actionY, 70, 34);
            EmojiWindowNative.SetButtonBounds(_btnOpenProduct, rightX + wx + 424, contentY + actionY, 102, 34);

            int browserTop = actionY + 34 + workRowGap;
            int browserHeight = contentHeight - 6 - browserTop;
            MoveWindow(_browserPanel, wx, browserTop, workW, browserHeight);
            EmojiWindowNative.SetLabelBounds(_lblBrowserEmpty, 28, 28, workW - 56, 30);
            EmojiWindowNative.SetLabelBounds(_lblBrowserSub, 28, 66, workW - 56, 20);

            EmojiWindowNative.SetLabelBounds(_statusBar, padding, _height - 26, _width - padding * 2, 20);
        }

        private void ApplyTheme()
        {
            uint page = _darkMode ? Argb(255, 17, 24, 39) : Argb(255, 241, 245, 250);
            uint surface = _darkMode ? Argb(255, 30, 41, 59) : Argb(255, 255, 255, 255);
            uint text = _darkMode ? Argb(255, 226, 232, 240) : Argb(255, 31, 41, 55);
            uint muted = _darkMode ? Argb(255, 148, 163, 184) : Argb(255, 100, 116, 139);
            uint border = _darkMode ? Argb(255, 71, 85, 105) : Argb(255, 226, 232, 240);

            EmojiWindowNative.set_window_titlebar_color(_window, _darkMode ? Argb(255, 30, 41, 59) : Argb(255, 38, 70, 124));
            EmojiWindowNative.SetWindowBackgroundColor(_window, page);
            EmojiWindowNative.SetPanelBackgroundColor(_sidebarPanel, surface);
            EmojiWindowNative.SetPanelBackgroundColor(_workspacePanel, surface);
            uint browserCanvasLight = Argb(255, 222, 228, 238);
            uint browserCanvasDark = Argb(255, 15, 23, 42);
            EmojiWindowNative.SetPanelBackgroundColor(_browserPanel, _darkMode ? browserCanvasDark : browserCanvasLight);
            for (int i = 0; i < _cards.Length; i++)
            {
                uint cardSurfaceBg = _darkMode ? Argb(255, 30, 41, 59) : Argb(255, 255, 255, 255);
                EmojiWindowNative.SetPanelBackgroundColor(_cards[i].Panel, cardSurfaceBg);
                EmojiWindowNative.SetLabelColor(_cards[i].Value, _cards[i].AccentColor, cardSurfaceBg);
                EmojiWindowNative.SetLabelColor(_cards[i].Title, text, cardSurfaceBg);
                EmojiWindowNative.SetLabelColor(_cards[i].Hint, muted, cardSurfaceBg);
                EmojiWindowNative.SetLabelColor(_cards[i].Badge, Argb(255, 255, 255, 255), _cards[i].AccentColor);
            }
            EmojiWindowNative.SetLabelColor(_lblSidebarTitle, text, surface);
            EmojiWindowNative.SetLabelColor(_lblWorkspaceTitle, text, surface);
            EmojiWindowNative.SetLabelColor(_lblBrowserEmpty, text, _darkMode ? browserCanvasDark : browserCanvasLight);
            EmojiWindowNative.SetLabelColor(_lblBrowserSub, muted, _darkMode ? browserCanvasDark : browserCanvasLight);
            EmojiWindowNative.SetLabelColor(_statusBar, muted, page);
            uint fieldBg = _darkMode ? Argb(255, 30, 41, 59) : Argb(255, 255, 255, 255);
            uint fieldHover = _darkMode ? Argb(255, 51, 65, 85) : Argb(255, 255, 255, 255);

            uint gridText = _darkMode ? Argb(255, 226, 232, 240) : Argb(255, 31, 41, 55);
            uint gridBg = _darkMode ? Argb(255, 15, 23, 42) : Argb(255, 255, 255, 255);
            uint gridHeaderBg = _darkMode ? Argb(255, 30, 41, 59) : Argb(255, 243, 246, 252);
            uint gridHeaderText = _darkMode ? Argb(255, 148, 163, 184) : Argb(255, 71, 85, 105);
            uint gridSelect = _darkMode ? Argb(255, 30, 58, 138) : Argb(255, 236, 245, 255);
            uint gridHover = _darkMode ? Argb(255, 30, 41, 59) : Argb(255, 248, 250, 252);
            uint gridBorder = _darkMode ? Argb(255, 71, 85, 105) : Argb(255, 229, 231, 235);

            EmojiWindowNative.SetEditBoxColor(_txtSearch, text, fieldBg);
            EmojiWindowNative.SetEditBoxColor(_txtUrl, text, fieldBg);
            EmojiWindowNative.SetComboBoxColors(_cmbChannel, text, fieldBg, fieldHover, fieldHover);
            EmojiWindowNative.SetComboBoxColors(_cmbStore, text, fieldBg, fieldHover, fieldHover);
            EmojiWindowNative.SetComboBoxColors(_cmbStatus, text, fieldBg, fieldHover, fieldHover);
            EmojiWindowNative.DataGrid_SetColors(_grid, gridText, gridBg, gridHeaderBg, gridHeaderText, gridSelect, gridHover, gridBorder);

            byte[] emoji = U(_darkMode ? "☀️" : "🌙");
            EmojiWindowNative.SetButtonEmoji(_btnTheme, emoji, emoji.Length);
            PaintButton(_btnTheme, Argb(255, 148, 163, 184));
            PaintButton(_btnQuery, Argb(255, 59, 130, 246));
            PaintButton(_btnReset, Argb(255, 148, 163, 184));
            PaintButton(_btnAdd, Argb(255, 59, 130, 246));
            PaintButton(_btnImport, Argb(255, 148, 163, 184));
            PaintButton(_btnExport, Argb(255, 148, 163, 184));
            PaintButton(_btnRefresh, Argb(255, 148, 163, 184));
            PaintButton(_btnBatchStart, Argb(255, 34, 197, 94));
            PaintButton(_btnBatchStop, Argb(255, 245, 158, 11));
            PaintButton(_btnBatchDelete, Argb(255, 239, 68, 68));
            PaintButton(_btnSelectAll, Argb(255, 148, 163, 184));
            PaintButton(_btnLaunch, Argb(255, 59, 130, 246));
            PaintButton(_btnStop, Argb(255, 245, 158, 11));
            PaintButton(_btnRefreshPage, Argb(255, 148, 163, 184));
            PaintButton(_btnClearCache, Argb(255, 148, 163, 184));
            PaintButton(_btnRelogin, Argb(255, 148, 163, 184));
            PaintButton(_btnOpenProduct, Argb(255, 34, 197, 94));
            UpdateThemeEmoji();
        }

        private void PaintButton(int id, uint bg)
        {
            EmojiWindowNative.SetButtonStyle(id, 0);
            EmojiWindowNative.SetButtonSize(id, 1);
            EmojiWindowNative.SetButtonRound(id, 0);
            EmojiWindowNative.SetButtonBackgroundColor(id, bg);
            EmojiWindowNative.SetButtonBorderColor(id, bg);
            EmojiWindowNative.SetButtonTextColor(id, Argb(255, 255, 255, 255));

            uint hoverBg = ShiftColor(bg, 18);
            uint hoverBorder = ShiftColor(bg, 8);
            EmojiWindowNative.SetButtonHoverColors(id, hoverBg, hoverBorder, Argb(255, 255, 255, 255));
        }

        private void UpdateThemeEmoji()
        {
            string symbol = _darkMode ? "\u2600\uFE0F" : "\uD83C\uDF19";
            byte[] emoji = U(symbol);
            byte[] empty = U(string.Empty);
            EmojiWindowNative.SetButtonEmoji(_btnTheme, emoji, emoji.Length);
            EmojiWindowNative.SetButtonText(_btnTheme, empty, 0);
        }

        private void OnUrlEditKey(IntPtr hEdit, int keyCode, int keyDown, int shift, int ctrl, int alt)
        {
            if (hEdit != _txtUrl || keyCode != 0x0D || keyDown == 0)
            {
                return;
            }

            NavigateToUrl();
        }

        private void NavigateToUrl()
        {
            string url = GetEditText(_txtUrl).Trim();
            byte[] msg = U(string.IsNullOrEmpty(url) ? "地址栏为空。" : "已导航: " + url);
            EmojiWindowNative.SetLabelText(_statusBar, msg, msg.Length);
        }

        private static string GetEditText(IntPtr edit)
        {
            return EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetEditBoxText, edit);
        }

        private void OnButtonClick(int buttonId, IntPtr parent)
        {
            if (buttonId == _btnTheme)
            {
                using (new RedrawScope(_window, includeChildren: true))
                {
                    _darkMode = !_darkMode;
                    ApplyTheme();
                }

                RefreshComboVisualsAfterTheme();
                return;
            }

            if (_buttonActions.TryGetValue(buttonId, out Action action))
            {
                action();
            }
        }

        private void OnResize(IntPtr hwnd, int width, int height)
        {
            if (hwnd != _window || width <= 0 || height <= 0)
            {
                return;
            }

            if (_width == width && _height == height)
            {
                return;
            }

            _width = width;
            _height = height;
            using (new RedrawScope(_window, includeChildren: true))
            {
                Layout();
            }
        }

        private IntPtr Combo(IntPtr parent)
        {
            return EmojiWindowNative.CreateComboBox(parent, 0, 0, 100, 34, 1, Argb(255, 31, 41, 55), Argb(255, 255, 255, 255), 32, _fontSegoe, _fontSegoe.Length, 11, 0, 0, 0);
        }

        private void FillCombo(IntPtr combo, IEnumerable<string> items)
        {
            EmojiWindowNative.ClearComboBox(combo);
            foreach (string item in items)
            {
                byte[] bytes = U(item);
                EmojiWindowNative.AddComboItem(combo, bytes, bytes.Length);
            }

            EmojiWindowNative.SetComboSelectedIndex(combo, 0);
        }

        private IntPtr Edit(IntPtr parent, string text)
        {
            byte[] bytes = U(text);
            return EmojiWindowNative.CreateEditBox(parent, 0, 0, 100, 34, bytes, bytes.Length, Argb(255, 31, 41, 55), Argb(255, 255, 255, 255), _fontSegoe, _fontSegoe.Length, 9, 0, 0, 0, 0, 0, 0, 0, 1, 1);
        }

        private IntPtr Label(IntPtr parent, string text, int size, bool bold, uint fg, uint bg)
        {
            byte[] bytes = U(text);
            return EmojiWindowNative.CreateLabel(parent, 0, 0, 100, 20, bytes, bytes.Length, fg, bg, _fontYaHei, _fontYaHei.Length, size, bold ? 1 : 0, 0, 0, 0, 0);
        }

        private int Button(IntPtr parent, string text, uint bg, Action action)
        {
            byte[] bytes = U(text);
            int id = EmojiWindowNative.create_emoji_button_bytes(parent, Array.Empty<byte>(), 0, bytes, bytes.Length, 0, 0, 90, 34, bg);
            if (action != null)
            {
                _buttonActions[id] = action;
            }

            return id;
        }

        private void SetGrid(int row, int col, string text)
        {
            byte[] bytes = U(text);
            EmojiWindowNative.DataGrid_SetCellText(_grid, row, col, bytes, bytes.Length);
        }

        private void RefreshComboDisplays()
        {
            // 预留接口
        }

        private void RefreshComboVisualsAfterTheme()
        {
            RefreshComboVisual(_cmbChannel);
            RefreshComboVisual(_cmbStore);
            RefreshComboVisual(_cmbStatus);
        }

        private void RefreshComboVisual(IntPtr combo)
        {
            if (combo == IntPtr.Zero)
            {
                return;
            }

            int count = EmojiWindowNative.GetComboItemCount(combo);
            if (count <= 0)
            {
                return;
            }

            int index = EmojiWindowNative.GetComboSelectedIndex(combo);
            if (index < 0 || index >= count)
            {
                index = 0;
                EmojiWindowNative.SetComboSelectedIndex(combo, index);
            }

            string text = EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetComboItemText, combo, index);
            if (string.IsNullOrEmpty(text))
            {
                return;
            }

            byte[] bytes = U(text);
            EmojiWindowNative.SetComboSelectedIndex(combo, index);
            EmojiWindowNative.SetComboBoxText(combo, bytes, bytes.Length);
        }

        private void MoveWindow(IntPtr hwnd, int x, int y, int w, int h)
        {
            Native.MoveWindow(hwnd, x, y, w, h, true);
        }

        private void SetComboBoxBounds(IntPtr combo, int x, int y, int w, int h)
        {
            EmojiWindowNative.SetComboBoxBounds(combo, x, y, w, h);
        }

        private static uint Argb(int a, int r, int g, int b) => EmojiWindowNative.ARGB(a, r, g, b);

        private static uint ShiftColor(uint argb, int delta)
        {
            int a = (int)((argb >> 24) & 0xFF);
            int r = ClampColor((int)((argb >> 16) & 0xFF) + delta);
            int g = ClampColor((int)((argb >> 8) & 0xFF) + delta);
            int b = ClampColor((int)(argb & 0xFF) + delta);
            return Argb(a, r, g, b);
        }

        private static int ClampColor(int value)
        {
            if (value < 0) return 0;
            if (value > 255) return 255;
            return value;
        }

        private byte[] U(string text) => EmojiWindowNative.ToUtf8(text);

        private static class Native
        {
            private const uint WmSetRedraw = 0x000B;
            private const uint RdwInvalidate = 0x0001;
            private const uint RdwErase = 0x0004;
            private const uint RdwAllChildren = 0x0080;
            private const uint RdwFrame = 0x0400;
            private const uint RdwUpdateNow = 0x0100;

            private delegate bool EnumChildProc(IntPtr hwnd, IntPtr lParam);

            [DllImport("user32.dll", SetLastError = true)]
            [return: MarshalAs(UnmanagedType.Bool)]
            public static extern bool MoveWindow(IntPtr hWnd, int x, int y, int nWidth, int nHeight, [MarshalAs(UnmanagedType.Bool)] bool bRepaint);

            [DllImport("user32.dll", SetLastError = true)]
            private static extern IntPtr SendMessage(IntPtr hWnd, uint msg, IntPtr wParam, IntPtr lParam);

            [DllImport("user32.dll", SetLastError = true)]
            private static extern bool RedrawWindow(IntPtr hWnd, IntPtr lprcUpdate, IntPtr hrgnUpdate, uint flags);

            [DllImport("user32.dll", SetLastError = true)]
            private static extern bool EnumChildWindows(IntPtr hWndParent, EnumChildProc lpEnumFunc, IntPtr lParam);

            public static List<IntPtr> CollectWindowTree(IntPtr hwnd)
            {
                List<IntPtr> handles = new List<IntPtr>();
                if (hwnd == IntPtr.Zero)
                {
                    return handles;
                }

                handles.Add(hwnd);
                EnumChildWindows(hwnd, (child, _) =>
                {
                    if (!handles.Contains(child))
                    {
                        handles.Add(child);
                    }

                    return true;
                }, IntPtr.Zero);

                return handles;
            }

            public static void SetRedraw(IntPtr hwnd, bool enabled)
            {
                if (hwnd == IntPtr.Zero)
                {
                    return;
                }

                SendMessage(hwnd, WmSetRedraw, enabled ? new IntPtr(1) : IntPtr.Zero, IntPtr.Zero);
            }

            public static void RefreshWindow(IntPtr hwnd)
            {
                if (hwnd == IntPtr.Zero)
                {
                    return;
                }

                RedrawWindow(hwnd, IntPtr.Zero, IntPtr.Zero, RdwInvalidate | RdwErase | RdwFrame | RdwAllChildren | RdwUpdateNow);
            }
        }

        private sealed class RedrawScope : IDisposable
        {
            private readonly List<IntPtr> _handles;

            public RedrawScope(IntPtr hwnd, bool includeChildren = false)
            {
                _handles = includeChildren ? Native.CollectWindowTree(hwnd) : new List<IntPtr> { hwnd };
                for (int i = 0; i < _handles.Count; i++)
                {
                    Native.SetRedraw(_handles[i], false);
                }
            }

            public void Dispose()
            {
                for (int i = _handles.Count - 1; i >= 0; i--)
                {
                    Native.SetRedraw(_handles[i], true);
                }

                if (_handles.Count > 0)
                {
                    Native.RefreshWindow(_handles[0]);
                }
            }
        }
    }
}
