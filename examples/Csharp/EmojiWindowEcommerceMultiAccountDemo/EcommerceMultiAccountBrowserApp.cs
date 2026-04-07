using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using EmojiWindowDemo;

namespace EmojiWindowEcommerceMultiAccountDemo
{
    internal sealed class EcommerceMultiAccountBrowserApp
    {
        private const int WindowWidth = 1440;
        private const int WindowHeight = 900;
        private const int CardCount = 6;
        private const int TitleBarHeight = 32;

        private static class Palette
        {
            public static readonly uint TitleBar = EmojiWindowNative.ARGB(255, 28, 58, 102);
            public static readonly uint PageBackground = EmojiWindowNative.ARGB(255, 240, 244, 250);
            public static readonly uint Surface = EmojiWindowNative.ARGB(255, 255, 255, 255);
            public static readonly uint SurfaceSoft = EmojiWindowNative.ARGB(255, 247, 249, 252);
            public static readonly uint SurfaceMuted = EmojiWindowNative.ARGB(255, 232, 238, 247);
            public static readonly uint Border = EmojiWindowNative.ARGB(255, 214, 224, 237);
            public static readonly uint BorderStrong = EmojiWindowNative.ARGB(255, 190, 205, 226);
            public static readonly uint Text = EmojiWindowNative.ARGB(255, 31, 41, 55);
            public static readonly uint Muted = EmojiWindowNative.ARGB(255, 107, 114, 128);
            public static readonly uint MutedSoft = EmojiWindowNative.ARGB(255, 137, 149, 170);
            public static readonly uint Primary = EmojiWindowNative.ARGB(255, 37, 99, 235);
            public static readonly uint PrimarySoft = EmojiWindowNative.ARGB(255, 235, 244, 255);
            public static readonly uint Success = EmojiWindowNative.ARGB(255, 22, 163, 74);
            public static readonly uint SuccessSoft = EmojiWindowNative.ARGB(255, 235, 250, 239);
            public static readonly uint Warning = EmojiWindowNative.ARGB(255, 217, 119, 6);
            public static readonly uint WarningSoft = EmojiWindowNative.ARGB(255, 255, 247, 237);
            public static readonly uint Danger = EmojiWindowNative.ARGB(255, 220, 38, 38);
            public static readonly uint DangerSoft = EmojiWindowNative.ARGB(255, 254, 242, 242);
            public static readonly uint Info = EmojiWindowNative.ARGB(255, 8, 145, 178);
            public static readonly uint InfoSoft = EmojiWindowNative.ARGB(255, 236, 251, 255);
            public static readonly uint Hover = EmojiWindowNative.ARGB(255, 242, 246, 252);
            public static readonly uint GridLine = EmojiWindowNative.ARGB(255, 230, 236, 242);
            public static readonly uint BrowserPlaceholder = EmojiWindowNative.ARGB(255, 11, 21, 38);
            public static readonly uint BrowserHeader = EmojiWindowNative.ARGB(255, 17, 32, 58);
            public static readonly uint BrowserCanvas = EmojiWindowNative.ARGB(255, 222, 228, 238);
            public static readonly uint BrowserCanvasBorder = EmojiWindowNative.ARGB(255, 78, 108, 152);
            public static readonly uint Cyan = EmojiWindowNative.ARGB(255, 34, 211, 238);
        }

        private sealed class AccountRecord
        {
            public int Id { get; set; }
            public bool Checked { get; set; }
            public string Account { get; set; } = string.Empty;
            public string Channel { get; set; } = string.Empty;
            public string Store { get; set; } = string.Empty;
            public string Note { get; set; } = string.Empty;
            public string Status { get; set; } = string.Empty;
            public string Url { get; set; } = string.Empty;
            public DateTime LastLogin { get; set; }
        }

        private sealed class MetricCard
        {
            public IntPtr Panel { get; set; }
            public IntPtr AccentBar { get; set; }
            public IntPtr BadgeLabel { get; set; }
            public IntPtr ValueLabel { get; set; }
            public IntPtr CaptionLabel { get; set; }
            public IntPtr HintLabel { get; set; }
            public IntPtr TrendLabel { get; set; }
            public uint AccentColor { get; set; }
        }

        private readonly List<AccountRecord> _accounts = new List<AccountRecord>();
        private readonly List<AccountRecord> _visibleAccounts = new List<AccountRecord>();
        private readonly Dictionary<int, Action> _buttonActions = new Dictionary<int, Action>();

        private readonly byte[] _fontYaHei = EmojiWindowNative.ToUtf8("Microsoft YaHei UI");
        private readonly byte[] _fontSegoe = EmojiWindowNative.ToUtf8("Segoe UI");

        private readonly EmojiWindowNative.ButtonClickCallback _buttonClickCallback;
        private readonly EmojiWindowNative.WindowResizeCallback _windowResizeCallback;
        private readonly EmojiWindowNative.WindowCloseCallback _windowCloseCallback;
        private readonly EmojiWindowNative.DataGridCellCallback _gridCellClickCallback;
        private readonly EmojiWindowNative.DataGridCellCallback _gridValueChangedCallback;
        private readonly EmojiWindowNative.DataGridCellCallback _gridSelectionChangedCallback;
        private readonly EmojiWindowNative.DataGridColumnHeaderCallback _gridHeaderClickCallback;
        private readonly EmojiWindowNative.EditBoxKeyCallback _urlEditKeyCallback;

        private readonly MetricCard[] _cards = new MetricCard[CardCount];

        private IntPtr _window;
        private int _windowWidth = WindowWidth;
        private int _windowHeight = WindowHeight;
        private int _nextId = 1;
        private int _selectedAccountId = -1;
        private int _sortColumn = 1;
        private bool _sortAscending = true;
        private bool _selectAllChecked;
        private bool _darkModeEnabled;

        private IntPtr _accountsGroup;
        private IntPtr _workspaceGroup;
        private IntPtr _accountsGroupFillPanel;
        private IntPtr _workspaceGroupFillPanel;
        private IntPtr _accountsHeaderMaskPanel;
        private IntPtr _workspaceHeaderMaskPanel;
        private IntPtr _statusBarPanel;
        private IntPtr _currentAccountPanel;
        private IntPtr _toolbarPanel;
        private IntPtr _browserHostPanel;
        private IntPtr _browserHeaderPanel;
        private IntPtr _browserCanvasPanel;
        private IntPtr _accountsStatsPanel;
        private IntPtr _filterTagsPanel;
        private IntPtr _statAllPanel;
        private IntPtr _statRunningPanel;
        private IntPtr _statIssuePanel;
        private IntPtr _sessionStripPanel;

        private IntPtr _cmbChannel;
        private IntPtr _cmbStore;
        private IntPtr _cmbStatus;
        private IntPtr _txtKeyword;
        private IntPtr _txtAccountSearch;
        private IntPtr _txtUrl;
        private IntPtr _gridAccounts;

        /// <summary>账号表列宽比例基准（总和 308）；布局时按左栏 innerWidth 等比缩放。</summary>
        private static readonly int[] AccountGridColumnWidthsBase = { 30, 88, 62, 80, 48 };

        private IntPtr _lblStatusBar;
        private IntPtr _lblAccountsGroupTitle;
        private IntPtr _lblWorkspaceGroupTitle;
        private IntPtr _lblAccountFooter;
        private IntPtr _lblGridEmptyState;
        private IntPtr _lblCurrentAccount;
        private IntPtr _lblCurrentStore;
        private IntPtr _lblCurrentNote;
        private IntPtr _lblCurrentStatus;
        private IntPtr _lblWorkspaceStatus;
        private IntPtr _lblBrowserTitle;
        private IntPtr _lblBrowserSubtitle;
        private IntPtr _lblBrowserChip;
        private IntPtr _lblCanvasTitle;
        private IntPtr _lblCanvasMeta;
        private IntPtr _lblToolbarTitle;
        private IntPtr _lblToolbarMeta;
        private IntPtr _lblStatAllValue;
        private IntPtr _lblStatAllCaption;
        private IntPtr _lblStatRunningValue;
        private IntPtr _lblStatRunningCaption;
        private IntPtr _lblStatIssueValue;
        private IntPtr _lblStatIssueCaption;
        private IntPtr _lblTagChannel;
        private IntPtr _lblTagStore;
        private IntPtr _lblTagStatus;

        private int _btnSessionPrimary;
        private int _btnSessionSecondary;
        private int _btnSessionTertiary;
        private readonly int[] _sessionAccountIds = new int[3];

        private int _btnQuery;
        private int _btnReset;
        private int _btnTheme;
        private int _btnAdd;
        private int _btnImport;
        private int _btnExport;
        private int _btnRefreshList;
        private int _btnBatchStart;
        private int _btnBatchStop;
        private int _btnBatchDelete;
        private int _btnSelectAll;
        private int _btnLaunchBrowser;
        private int _btnStopBrowser;
        private int _btnRefreshPage;
        private int _btnClearCache;
        private int _btnRelogin;
        private int _btnOpenProduct;

        public EcommerceMultiAccountBrowserApp()
        {
            _buttonClickCallback = OnButtonClick;
            _windowResizeCallback = OnWindowResize;
            _windowCloseCallback = OnWindowClose;
            _gridCellClickCallback = OnGridCellClick;
            _gridValueChangedCallback = OnGridValueChanged;
            _gridSelectionChangedCallback = OnGridSelectionChanged;
            _gridHeaderClickCallback = OnGridHeaderClick;
            _urlEditKeyCallback = OnUrlEditKey;
        }

        public void Run()
        {
            SeedAccounts();
            CreateWindow();
            RegisterCallbacks();
            CreateCards();
            CreateFilterBar();
            CreateLeftPanel();
            CreateRightPanel();
            EmojiWindowNative.SetEditBoxKeyCallback(_txtUrl, _urlEditKeyCallback);
            ApplyLayoutFixed();
            LoadCombos();
            ApplyFilters("已加载示例账号数据。");
            ApplyThemeVisuals();
            RefreshComboDisplays();

            EmojiWindowNative.ShowEmojiWindow(_window, 1);
            EmojiWindowNative.set_message_loop_main_window(_window);
            EmojiWindowNative.run_message_loop();
        }

        private void CreateWindow()
        {
            byte[] titleBytes = U("电商多账号浏览器管理器");
            _window = EmojiWindowNative.create_window_bytes_ex(
                titleBytes,
                titleBytes.Length,
                -1,
                -1,
                WindowWidth,
                WindowHeight,
                Palette.TitleBar,
                Palette.PageBackground);

            if (_window == IntPtr.Zero)
            {
                throw new InvalidOperationException("Failed to create main window.");
            }

            EmojiWindowNative.SetTitleBarTextColor(_window, EmojiWindowNative.ARGB(255, 255, 255, 255));
            ApplyWindowIcon();
            EmojiWindowNative.ShowEmojiWindow(_window, 0);
        }

        private void ApplyWindowIcon()
        {
            string iconPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "favicon.ico");
            if (!File.Exists(iconPath))
            {
                iconPath = @"T:\易语言源码\API创建窗口\emoji_window_cpp\examples\Csharp\EmojiWindowEcommerceMultiAccountDemo\favicon.ico";
            }

            if (!File.Exists(iconPath))
            {
                return;
            }

            byte[] iconBytes = File.ReadAllBytes(iconPath);
            if (iconBytes.Length > 0)
            {
                EmojiWindowNative.set_window_icon_bytes(_window, iconBytes, iconBytes.Length);
            }
        }

        private void RegisterCallbacks()
        {
            EmojiWindowNative.set_button_click_callback(_buttonClickCallback);
            EmojiWindowNative.SetWindowResizeCallback(_windowResizeCallback);
            EmojiWindowNative.SetWindowCloseCallback(_windowCloseCallback);
        }

        private void CreateCards()
        {
            string[] captions =
            {
                "今日在线",
                "运行中",
                "异常账号",
                "待处理",
                "店铺数",
                "代理正常率"
            };

            string[] hints =
            {
                "已完成环境校验",
                "当前已启动实例",
                "需人工检查",
                "等待运营处理",
                "覆盖店铺总量",
                "最近 24 小时"
            };

            uint[] accents =
            {
                Palette.Primary,
                Palette.Success,
                Palette.Danger,
                Palette.Warning,
                Palette.Info,
                Palette.Primary
            };

            string[] badges =
            {
                "OPS",
                "LIVE",
                "RISK",
                "TODO",
                "SHOP",
                "NET"
            };

            for (int i = 0; i < CardCount; i++)
            {
                IntPtr panel = EmojiWindowNative.CreatePanel(_window, 0, 0, 100, 80, Palette.Surface);
                IntPtr accentBar = EmojiWindowNative.CreatePanel(panel, 0, 0, 100, 6, accents[i]);
                MetricCard card = new MetricCard
                {
                    Panel = panel,
                    AccentBar = accentBar,
                    BadgeLabel = CreateLabel(panel, 0, 0, 10, 10, badges[i], EmojiWindowNative.ARGB(255, 255, 255, 255), accents[i], 9, 1, 0, 1),
                    ValueLabel = CreateLabel(panel, 0, 0, 10, 10, "0", accents[i], Palette.Surface, 24, 1),
                    CaptionLabel = CreateLabel(panel, 0, 0, 10, 10, captions[i], Palette.Muted, Palette.Surface, 11, 0),
                    HintLabel = CreateLabel(panel, 0, 0, 10, 10, hints[i], accents[i], Palette.Surface, 10, 0),
                    TrendLabel = CreateLabel(panel, 0, 0, 10, 10, "--", Palette.MutedSoft, Palette.Surface, 10, 0),
                    AccentColor = accents[i]
                };

                _cards[i] = card;
            }
        }

        private void CreateFilterBar()
        {
            _cmbChannel = CreateCombo(_window, 0, 0, 100, 30);
            _cmbStore = CreateCombo(_window, 0, 0, 100, 30);
            _cmbStatus = CreateCombo(_window, 0, 0, 100, 30);
            _txtKeyword = CreateEditBox(_window, 0, 0, 100, 30, "全局搜索账号/备注/店铺");

            _btnQuery = CreateButton("查询", Palette.Primary, ApplyFiltersFromControls);
            _btnReset = CreateButton("重置", Palette.SurfaceSoft, ResetFilters);
            _btnTheme = CreateButton(string.Empty, Palette.SurfaceSoft, ToggleTheme);
            UpdateThemeButton();
        }

        private void CreateLeftPanel()
        {
            _accountsGroup = CreateGroupBox("账号管理");
            EmojiWindowNative.SetGroupBoxTitle(_accountsGroup, Array.Empty<byte>(), 0);
            _accountsGroupFillPanel = EmojiWindowNative.CreatePanel(_window, 0, 0, 100, 100, Palette.PageBackground);
            _accountsHeaderMaskPanel = EmojiWindowNative.CreatePanel(_window, 0, 0, 100, 24, Palette.PageBackground);
            _lblAccountsGroupTitle = CreateLabel(IntPtr.Zero, 0, 0, 100, 20, "账号管理", Palette.Text, Palette.PageBackground, 12, 1);

            _btnAdd = CreateButton("新增", Palette.Primary, AddAccount);
            _btnImport = CreateButton("导入", Palette.SurfaceSoft, ImportAccounts);
            _btnExport = CreateButton("导出", Palette.SurfaceSoft, ExportAccounts);
            _btnRefreshList = CreateButton("刷新", Palette.SurfaceSoft, ApplyFiltersFromControls);
            _btnBatchStart = CreateButton("批量启动", Palette.Success, BatchStart);
            _btnBatchStop = CreateButton("批量停止", Palette.Warning, BatchStop);
            _btnBatchDelete = CreateButton("批量删除", Palette.Danger, BatchDelete);
            _btnSelectAll = CreateButton("全选", Palette.SurfaceSoft, ToggleSelectAll);

            _txtAccountSearch = CreateEditBox(_window, 0, 0, 100, 30, "🔍 搜索账号/备注");

            _accountsStatsPanel = EmojiWindowNative.CreatePanel(_window, 0, 0, 100, 54, Palette.SurfaceSoft);
            _filterTagsPanel = EmojiWindowNative.CreatePanel(_window, 0, 0, 100, 28, Palette.PageBackground);
            _statAllPanel = EmojiWindowNative.CreatePanel(_accountsStatsPanel, 0, 0, 100, 40, Palette.PrimarySoft);
            _statRunningPanel = EmojiWindowNative.CreatePanel(_accountsStatsPanel, 0, 0, 100, 40, Palette.SuccessSoft);
            _statIssuePanel = EmojiWindowNative.CreatePanel(_accountsStatsPanel, 0, 0, 100, 40, Palette.DangerSoft);
            _lblStatAllValue = CreateLabel(_statAllPanel, 0, 0, 10, 10, "0", Palette.Primary, Palette.PrimarySoft, 16, 1);
            _lblStatAllCaption = CreateLabel(_statAllPanel, 0, 0, 10, 10, "全部账号", Palette.Muted, Palette.PrimarySoft, 10, 0);
            _lblStatRunningValue = CreateLabel(_statRunningPanel, 0, 0, 10, 10, "0", Palette.Success, Palette.SuccessSoft, 16, 1);
            _lblStatRunningCaption = CreateLabel(_statRunningPanel, 0, 0, 10, 10, "运行中", Palette.Muted, Palette.SuccessSoft, 10, 0);
            _lblStatIssueValue = CreateLabel(_statIssuePanel, 0, 0, 10, 10, "0", Palette.Danger, Palette.DangerSoft, 16, 1);
            _lblStatIssueCaption = CreateLabel(_statIssuePanel, 0, 0, 10, 10, "异常", Palette.Muted, Palette.DangerSoft, 10, 0);
            _lblTagChannel = CreateLabel(_filterTagsPanel, 0, 0, 10, 10, "渠道: 全部", EmojiWindowNative.ARGB(255, 255, 255, 255), Palette.Info, 10, 1, 0);
            _lblTagStore = CreateLabel(_filterTagsPanel, 0, 0, 10, 10, "店铺: 全部", EmojiWindowNative.ARGB(255, 255, 255, 255), Palette.Primary, 10, 1, 0);
            _lblTagStatus = CreateLabel(_filterTagsPanel, 0, 0, 10, 10, "状态: 全部", EmojiWindowNative.ARGB(255, 255, 255, 255), Palette.Success, 10, 1, 0);

            _gridAccounts = EmojiWindowNative.CreateDataGridView(_window, 0, 0, 100, 100, 0, 1, Palette.Text, Palette.Surface);
            // 初始列宽与 AccountGridColumnWidthsBase 一致；实际宽度在 ApplyAccountGridColumnWidths 中按左栏 innerWidth 适配，避免总宽大于表格区域出现横向滚动条
            EmojiWindowNative.DataGrid_AddCheckBoxColumn(_gridAccounts, U("选"), U("选").Length, 30);
            EmojiWindowNative.DataGrid_AddTextColumn(_gridAccounts, U("账号"), U("账号").Length, 88);
            EmojiWindowNative.DataGrid_AddTextColumn(_gridAccounts, U("店铺"), U("店铺").Length, 62);
            EmojiWindowNative.DataGrid_AddTextColumn(_gridAccounts, U("备注"), U("备注").Length, 80);
            EmojiWindowNative.DataGrid_AddTextColumn(_gridAccounts, U("状态"), U("状态").Length, 48);
            EmojiWindowNative.DataGrid_SetSelectionMode(_gridAccounts, 1);
            EmojiWindowNative.DataGrid_SetFreezeHeader(_gridAccounts, 1);
            EmojiWindowNative.DataGrid_SetShowGridLines(_gridAccounts, 1);
            EmojiWindowNative.DataGrid_SetDefaultRowHeight(_gridAccounts, 34);
            EmojiWindowNative.DataGrid_SetHeaderHeight(_gridAccounts, 36);
            EmojiWindowNative.DataGrid_SetDoubleClickEnabled(_gridAccounts, 0);
            EmojiWindowNative.DataGrid_SetColors(
                _gridAccounts,
                Palette.Text,
                Palette.Surface,
                Palette.BrowserHeader,
                EmojiWindowNative.ARGB(255, 255, 255, 255),
                EmojiWindowNative.ARGB(255, 216, 232, 255),
                Palette.Hover,
                Palette.GridLine);
            EmojiWindowNative.DataGrid_SetHeaderStyle(_gridAccounts, 1);
            EmojiWindowNative.DataGrid_SetColumnHeaderAlignment(_gridAccounts, 0, 1);
            EmojiWindowNative.DataGrid_SetColumnHeaderAlignment(_gridAccounts, 4, 1);
            EmojiWindowNative.DataGrid_SetColumnCellAlignment(_gridAccounts, 0, 1);
            EmojiWindowNative.DataGrid_SetColumnCellAlignment(_gridAccounts, 4, 1);
            EmojiWindowNative.DataGrid_SetCellClickCallback(_gridAccounts, _gridCellClickCallback);
            EmojiWindowNative.DataGrid_SetCellValueChangedCallback(_gridAccounts, _gridValueChangedCallback);
            EmojiWindowNative.DataGrid_SetSelectionChangedCallback(_gridAccounts, _gridSelectionChangedCallback);
            EmojiWindowNative.DataGrid_SetColumnHeaderClickCallback(_gridAccounts, _gridHeaderClickCallback);

            _lblAccountFooter = CreateLabel(IntPtr.Zero, 0, 0, 100, 20, string.Empty, Palette.Muted, Palette.PageBackground, 11, 0);
            _lblGridEmptyState = CreateLabel(IntPtr.Zero, 0, 0, 100, 44, "暂无账号数据\n点击上方“新增”或“导入”开始", Palette.Muted, Palette.Surface, 12, 0, 1, 1);
        }

        private void CreateRightPanel()
        {
            _workspaceGroup = CreateGroupBox("工作区");
            EmojiWindowNative.SetGroupBoxTitle(_workspaceGroup, Array.Empty<byte>(), 0);
            _workspaceGroupFillPanel = EmojiWindowNative.CreatePanel(_window, 0, 0, 100, 100, Palette.PageBackground);
            _workspaceHeaderMaskPanel = EmojiWindowNative.CreatePanel(_window, 0, 0, 100, 24, Palette.PageBackground);
            _lblWorkspaceGroupTitle = CreateLabel(IntPtr.Zero, 0, 0, 100, 20, "工作区", Palette.Text, Palette.PageBackground, 12, 1);
            _currentAccountPanel = EmojiWindowNative.CreatePanel(_window, 0, 0, 100, 72, Palette.SurfaceMuted);
            _toolbarPanel = EmojiWindowNative.CreatePanel(_window, 0, 0, 100, 46, Palette.BrowserHeader);

            _lblCurrentAccount = CreateLabel(_currentAccountPanel, 0, 0, 100, 24, "当前账号: -", Palette.Text, Palette.SurfaceMuted, 14, 1);
            _lblCurrentStore = CreateLabel(_currentAccountPanel, 0, 0, 100, 24, "店铺: -", Palette.Muted, Palette.SurfaceMuted, 12, 0);
            _lblCurrentNote = CreateLabel(_currentAccountPanel, 0, 0, 100, 24, "备注: -", Palette.Text, Palette.SurfaceMuted, 12, 0);
            _lblCurrentStatus = CreateLabel(_currentAccountPanel, 0, 0, 100, 24, "状态: -", Palette.Primary, Palette.SurfaceMuted, 12, 1, 0, 1);
            _lblToolbarTitle = CreateLabel(_toolbarPanel, 0, 0, 100, 20, "BROWSER OPS", EmojiWindowNative.ARGB(255, 255, 255, 255), Palette.BrowserHeader, 10, 1);
            _lblToolbarMeta = CreateLabel(_toolbarPanel, 0, 0, 100, 20, "启动、会话维护、商品页跳转", Palette.Cyan, Palette.BrowserHeader, 10, 0);

            _btnLaunchBrowser = CreateButton("启动浏览器", Palette.Primary, LaunchBrowser);
            _btnStopBrowser = CreateButton("停止", Palette.Warning, StopBrowser);
            _btnRefreshPage = CreateButton("刷新", Palette.SurfaceSoft, RefreshPage);
            _btnClearCache = CreateButton("清缓存", Palette.SurfaceSoft, ClearCache);
            _btnRelogin = CreateButton("重登", Palette.SurfaceSoft, Relogin);
            _btnOpenProduct = CreateButton("打开商品页", Palette.Success, OpenProductPage);

            _txtUrl = CreateEditBox(_window, 0, 0, 100, 32, string.Empty);

            _browserHostPanel = EmojiWindowNative.CreatePanel(_window, 0, 0, 100, 100, Palette.BrowserPlaceholder);
            _browserHeaderPanel = EmojiWindowNative.CreatePanel(_browserHostPanel, 0, 0, 100, 64, Palette.BrowserHeader);
            _browserCanvasPanel = EmojiWindowNative.CreatePanel(_browserHostPanel, 0, 0, 100, 100, Palette.BrowserCanvas);
            _sessionStripPanel = EmojiWindowNative.CreatePanel(_browserCanvasPanel, 0, 0, 100, 42, Palette.SurfaceMuted);
            _lblBrowserTitle = CreateLabel(_browserHeaderPanel, 0, 0, 100, 30, "浏览器容器已就绪", EmojiWindowNative.ARGB(255, 255, 255, 255), Palette.BrowserHeader, 18, 1, 1);
            _lblBrowserSubtitle = CreateLabel(_browserHeaderPanel, 0, 0, 100, 22, "这里可以直接拿句柄接入你的浏览器内核。", Palette.Cyan, Palette.BrowserHeader, 11, 0, 1);
            _lblBrowserChip = CreateLabel(_browserHeaderPanel, 0, 0, 100, 20, "LIVE SESSION", EmojiWindowNative.ARGB(255, 255, 255, 255), Palette.Info, 10, 1, 0);
            _lblCanvasTitle = CreateLabel(_browserCanvasPanel, 0, 0, 100, 30, "等待浏览器实例挂载", Palette.Text, Palette.BrowserCanvas, 20, 1, 1);
            _lblCanvasMeta = CreateLabel(_browserCanvasPanel, 0, 0, 100, 22, "这里保留给 WebView / CEF / 你自己的浏览器宿主窗口。", Palette.MutedSoft, Palette.BrowserCanvas, 12, 0, 1);
            _btnSessionPrimary = CreateButton("SESSION A", Palette.Primary, () => SwitchSession(0));
            _btnSessionSecondary = CreateButton("SESSION B", Palette.SurfaceSoft, () => SwitchSession(1));
            _btnSessionTertiary = CreateButton("SESSION C", Palette.SurfaceSoft, () => SwitchSession(2));

            _lblWorkspaceStatus = CreateLabel(IntPtr.Zero, 0, 0, 100, 20, string.Empty, Palette.Muted, Palette.PageBackground, 11, 0);
            _lblStatusBar = CreateLabel(IntPtr.Zero, 0, 0, 100, 24, string.Empty, Palette.Muted, Palette.PageBackground, 11, 0);
            _statusBarPanel = EmojiWindowNative.CreatePanel(_window, 0, 0, 100, 24, Palette.PageBackground);
            EmojiWindowNative.ShowLabel(_lblWorkspaceStatus, 0);
        }

        private void LoadCombos()
        {
            FillCombo(_cmbChannel, "🌐 全部渠道", new[] { "🌐 全部渠道", "🛒 Amazon", "🛍️ Shopify", "🔥 Temu", "🎵 TikTok Shop" });
            FillCombo(_cmbStore, "全部店铺", new[] { "全部店铺", "美国站A店", "美国站B店", "日本站旗舰店", "英国站精选店", "独立站A" });
            FillCombo(_cmbStatus, "🎯 全部状态", new[] { "🎯 全部状态", "🟢 运行中", "🔵 空闲", "🔴 异常", "🟡 登录中" });
            RefreshComboDisplays();
        }

        private void ApplyFiltersFromControls()
        {
            ApplyFilters("已按筛选条件刷新账号列表。");
        }

        private void ApplyFilters(string statusMessage)
        {
            string channel = ExtractComboValue(GetSelectedComboText(_cmbChannel));
            string store = ExtractComboValue(GetSelectedComboText(_cmbStore));
            string status = ExtractComboValue(GetSelectedComboText(_cmbStatus));
            string keyword = NormalizeSearchText(GetEditText(_txtAccountSearch));

            IEnumerable<AccountRecord> query = _accounts;

            if (!string.IsNullOrEmpty(channel) && channel != "全部渠道")
            {
                query = query.Where(item => string.Equals(item.Channel, channel, StringComparison.OrdinalIgnoreCase));
            }

            if (!string.IsNullOrEmpty(store) && store != "全部店铺")
            {
                query = query.Where(item => string.Equals(item.Store, store, StringComparison.OrdinalIgnoreCase));
            }

            if (!string.IsNullOrEmpty(status) && status != "全部状态")
            {
                query = query.Where(item => string.Equals(item.Status, status, StringComparison.OrdinalIgnoreCase));
            }

            if (!string.IsNullOrWhiteSpace(keyword))
            {
                string[] tokens = keyword
                    .Split(new[] { ' ' }, StringSplitOptions.RemoveEmptyEntries)
                    .Select(token => token.Trim())
                    .Where(token => token.Length > 0)
                    .ToArray();

                query = query.Where(item => tokens.All(token =>
                    item.Account.IndexOf(token, StringComparison.OrdinalIgnoreCase) >= 0 ||
                    item.Store.IndexOf(token, StringComparison.OrdinalIgnoreCase) >= 0 ||
                    item.Note.IndexOf(token, StringComparison.OrdinalIgnoreCase) >= 0));
            }

            List<AccountRecord> results = query.ToList();
            SortVisibleAccounts(results);

            _visibleAccounts.Clear();
            _visibleAccounts.AddRange(results);

            if (_visibleAccounts.Count == 0)
            {
                _selectedAccountId = -1;
            }
            else if (_visibleAccounts.All(item => item.Id != _selectedAccountId))
            {
                _selectedAccountId = _visibleAccounts[0].Id;
            }

            PopulateGrid();
            UpdateAll(statusMessage);
        }

        private void PopulateGrid()
        {
            EmojiWindowNative.DataGrid_ClearRows(_gridAccounts);

            for (int i = 0; i < _visibleAccounts.Count; i++)
            {
                AccountRecord account = _visibleAccounts[i];
                int row = EmojiWindowNative.DataGrid_AddRow(_gridAccounts);
                SetGridText(row, 1, account.Account);
                SetGridText(row, 2, account.Store);
                SetGridText(row, 3, account.Note);
                SetGridText(row, 4, BuildStatusBadgeText(account.Status));
                EmojiWindowNative.DataGrid_SetCellChecked(_gridAccounts, row, 0, account.Checked ? 1 : 0);

                uint statusBackground;
                uint statusForeground;
                switch (account.Status)
                {
                    case "运行中":
                        statusBackground = Palette.SuccessSoft;
                        statusForeground = Palette.Success;
                        break;
                    case "异常":
                        statusBackground = Palette.DangerSoft;
                        statusForeground = Palette.Danger;
                        break;
                    case "登录中":
                        statusBackground = Palette.WarningSoft;
                        statusForeground = Palette.Warning;
                        break;
                    default:
                        statusBackground = Palette.PrimarySoft;
                        statusForeground = Palette.Primary;
                        break;
                }

                EmojiWindowNative.DataGrid_SetCellStyle(_gridAccounts, row, 4, statusForeground, statusBackground, 1, 0);
                ApplyStoreStyle(row, account);

                if (account.Id == _selectedAccountId)
                {
                    uint selectedBackground = EmojiWindowNative.ARGB(255, 230, 240, 255);
                    EmojiWindowNative.DataGrid_SetCellStyle(_gridAccounts, row, 1, Palette.Primary, selectedBackground, 1, 0);
                    EmojiWindowNative.DataGrid_SetCellStyle(_gridAccounts, row, 2, Palette.Text, selectedBackground, 0, 0);
                    EmojiWindowNative.DataGrid_SetCellStyle(_gridAccounts, row, 3, Palette.Text, selectedBackground, 0, 0);
                }
            }

            int selectedRow = _visibleAccounts.FindIndex(item => item.Id == _selectedAccountId);
            if (selectedRow >= 0)
            {
                EmojiWindowNative.DataGrid_SetSelectedCell(_gridAccounts, selectedRow, 1);
            }

            EmojiWindowNative.DataGrid_Refresh(_gridAccounts);
            bool showEmpty = _visibleAccounts.Count == 0;
            EmojiWindowNative.DataGrid_Show(_gridAccounts, showEmpty ? 0 : 1);
            EmojiWindowNative.ShowLabel(_lblGridEmptyState, showEmpty ? 1 : 0);
            if (showEmpty)
            {
                string emptyText = string.IsNullOrWhiteSpace(NormalizeSearchText(GetEditText(_txtAccountSearch)))
                    ? "暂无账号数据\n点击上方“新增”或“导入”开始"
                    : "没有匹配的账号\n请调整筛选条件后重试";
                SetLabelText(_lblGridEmptyState, emptyText);
            }
        }

        private void SortVisibleAccounts(List<AccountRecord> items)
        {
            Func<AccountRecord, string> textKey;
            switch (_sortColumn)
            {
                case 2:
                    textKey = item => item.Store;
                    break;
                case 3:
                    textKey = item => item.Note;
                    break;
                case 4:
                    textKey = item => item.Status;
                    break;
                default:
                    textKey = item => item.Account;
                    break;
            }

            items.Sort((left, right) =>
            {
                int result = string.Compare(textKey(left), textKey(right), StringComparison.OrdinalIgnoreCase);
                if (result == 0)
                {
                    result = left.Id.CompareTo(right.Id);
                }

                return _sortAscending ? result : -result;
            });
        }

        private void UpdateAll(string statusMessage)
        {
            UpdateMetricCards();
            UpdateAccountSummary();
            UpdateCurrentAccountPanel();
            UpdateBrowserPanel();
            UpdateStatusBar(statusMessage);
        }

        private void UpdateMetricCards()
        {
            int online = _accounts.Count(item => item.Status == "运行中" || item.Status == "登录中");
            int running = _accounts.Count(item => item.Status == "运行中");
            int errors = _accounts.Count(item => item.Status == "异常");
            int pending = _accounts.Count(item => item.Status == "空闲");
            int stores = _accounts.Select(item => item.Store).Distinct(StringComparer.OrdinalIgnoreCase).Count();
            int proxyHealth = _accounts.Count == 0 ? 0 : (int)Math.Round((_accounts.Count - errors) * 100.0 / _accounts.Count);

            string[] values =
            {
                online.ToString(),
                running.ToString(),
                errors.ToString(),
                pending.ToString(),
                stores.ToString(),
                proxyHealth + "%"
            };

            string[] trends =
            {
                "+2 vs yesterday",
                "+1 active now",
                errors > 0 ? "need review" : "all clear",
                pending > 0 ? "queue waiting" : "queue empty",
                stores + " stores linked",
                proxyHealth >= 90 ? "healthy network" : "check proxies"
            };

            for (int i = 0; i < _cards.Length; i++)
            {
                SetLabelText(_cards[i].ValueLabel, values[i]);
                EmojiWindowNative.SetLabelColor(_cards[i].ValueLabel, _cards[i].AccentColor, Palette.Surface);
                EmojiWindowNative.SetLabelColor(_cards[i].HintLabel, _cards[i].AccentColor, Palette.Surface);
                SetLabelText(_cards[i].TrendLabel, trends[i]);
            }
        }

        private void UpdateAccountSummary()
        {
            int checkedCount = _accounts.Count(item => item.Checked);
            SetLabelText(_lblAccountFooter, $"共 {_visibleAccounts.Count} 条，已选 {checkedCount} 项");
            SetButtonText(_btnSelectAll, _selectAllChecked ? "反选" : "全选");
            SetLabelText(_lblStatAllValue, _accounts.Count.ToString());
            SetLabelText(_lblStatRunningValue, _accounts.Count(item => item.Status == "运行中").ToString());
            SetLabelText(_lblStatIssueValue, _accounts.Count(item => item.Status == "异常").ToString());
            SetFilterTagTexts();
        }

        private void UpdateCurrentAccountPanel()
        {
            AccountRecord current = GetSelectedAccount();
            if (current == null)
            {
                SetLabelText(_lblCurrentAccount, "当前账号: -");
                SetLabelText(_lblCurrentStore, "店铺: -");
                SetLabelText(_lblCurrentNote, "备注: -");
                SetLabelText(_lblCurrentStatus, "状态: -");
                SetLabelText(_lblWorkspaceStatus, "工作区: 当前没有选中的账号。");
                SetEditText(_txtUrl, string.Empty);
                EmojiWindowNative.SetLabelColor(_lblCurrentStatus, Palette.Primary, Palette.SurfaceMuted);
                return;
            }

            SetLabelText(_lblCurrentAccount, $"当前账号: {current.Account}");
            SetLabelText(_lblCurrentStore, $"店铺: {current.Store} / 渠道: {current.Channel}");
            SetLabelText(_lblCurrentNote, $"备注: {current.Note} / 最近登录: {current.LastLogin:MM-dd HH:mm}");
            SetLabelText(_lblCurrentStatus, $"状态: {current.Status}");
            EmojiWindowNative.SetLabelColor(_lblCurrentStatus, GetStatusColor(current.Status), Palette.SurfaceMuted);
            SetLabelText(_lblWorkspaceStatus, $"工作区: 已绑定 {current.Account}，浏览器宿主句柄可直接复用。");
            SetEditText(_txtUrl, current.Url);
        }

        private void UpdateBrowserPanel()
        {
            AccountRecord current = GetSelectedAccount();
            if (current == null)
            {
                SetLabelText(_lblBrowserTitle, "浏览器容器已就绪");
                SetLabelText(_lblBrowserSubtitle, "左侧选中账号后，这里可以直接作为浏览器宿主窗口。");
                SetLabelText(_lblCanvasTitle, "等待浏览器实例挂载");
                SetLabelText(_lblCanvasMeta, "这里保留给 WebView / CEF / 你自己的浏览器宿主窗口。");
                EmojiWindowNative.SetLabelColor(_lblBrowserChip, EmojiWindowNative.ARGB(255, 255, 255, 255), Palette.Info);
                UpdateSessionTabs(Array.Empty<AccountRecord>());
                return;
            }

            SetLabelText(_lblBrowserTitle, $"{current.Account} / {current.Store}");
            SetLabelText(_lblBrowserSubtitle, $"宿主容器句柄: 0x{_browserHostPanel.ToInt64():X}    URL: {current.Url}");
            SetLabelText(_lblCanvasTitle, $"{current.Account} / {current.Store}");
            SetLabelText(_lblCanvasMeta, $"渠道 {current.Channel}    备注 {current.Note}    最近登录 {current.LastLogin:MM-dd HH:mm}");
            EmojiWindowNative.SetLabelColor(_lblBrowserChip, EmojiWindowNative.ARGB(255, 255, 255, 255), GetStatusBadgeColor(current.Status));
            UpdateSessionTabs(BuildSessionCandidates(current));
        }

        private void UpdateStatusBar(string message)
        {
            int selectedCount = _accounts.Count(item => item.Checked);
            int runningCount = _accounts.Count(item => item.Status == "运行中");
            long privateMb = Process.GetCurrentProcess().PrivateMemorySize64 / (1024 * 1024);
            SetLabelText(_lblStatusBar, $"{message}  |  已选 {selectedCount} 个账号  |  浏览器实例 {runningCount}  |  内存 {privateMb}MB  |  时间 {DateTime.Now:yyyy-MM-dd HH:mm}");
        }

        private void AddAccount()
        {
            AccountRecord account = new AccountRecord
            {
                Id = _nextId++,
                Account = $"shop_new_{_nextId:000}",
                Channel = "Amazon",
                Store = "美国站A店",
                Note = "新建账号，待养号",
                Status = "空闲",
                Url = "https://sellercentral.amazon.com/",
                LastLogin = DateTime.Now
            };

            _accounts.Insert(0, account);
            _selectedAccountId = account.Id;
            ApplyFilters("已新增账号。");
        }

        private void ImportAccounts()
        {
            AddImportedAccount("shop_bulk_201", "Amazon", "美国站B店", "Excel导入批次 A", "空闲");
            AddImportedAccount("shop_bulk_202", "Temu", "英国站精选店", "Excel导入批次 A", "登录中");
            AddImportedAccount("shop_bulk_203", "Shopify", "独立站A", "Excel导入批次 A", "异常");
            ApplyFilters("已模拟导入 3 个账号。");
        }

        private void ExportAccounts()
        {
            string exportPath = System.IO.Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "accounts_export.csv");
            byte[] pathBytes = U(exportPath);
            int ok = EmojiWindowNative.DataGrid_ExportCSV(_gridAccounts, pathBytes, pathBytes.Length);
            UpdateStatusBar(ok != 0 ? $"已导出到 {exportPath}" : "导出失败，请确认输出目录可写。");
        }

        private void BatchStart()
        {
            int changed = UpdateCheckedAccounts("运行中", record =>
            {
                record.LastLogin = DateTime.Now;
                if (string.IsNullOrWhiteSpace(record.Url))
                {
                    record.Url = "https://sellercentral.amazon.com/";
                }
            });

            ApplyFilters(changed > 0 ? $"已批量启动 {changed} 个账号。" : "没有勾选可启动的账号。");
        }

        private void BatchStop()
        {
            int changed = UpdateCheckedAccounts("空闲", null);
            ApplyFilters(changed > 0 ? $"已批量停止 {changed} 个账号。" : "没有勾选可停止的账号。");
        }

        private void BatchDelete()
        {
            List<int> ids = _accounts.Where(item => item.Checked).Select(item => item.Id).ToList();
            if (ids.Count == 0)
            {
                UpdateStatusBar("没有勾选可删除的账号。");
                return;
            }

            _accounts.RemoveAll(item => ids.Contains(item.Id));
            _selectedAccountId = _accounts.Count > 0 ? _accounts[0].Id : -1;
            _selectAllChecked = false;
            ApplyFilters($"已删除 {ids.Count} 个账号。");
        }

        private void ToggleSelectAll()
        {
            _selectAllChecked = !_selectAllChecked;
            foreach (AccountRecord account in _visibleAccounts)
            {
                account.Checked = _selectAllChecked;
            }

            PopulateGrid();
            UpdateAll(_selectAllChecked ? "当前筛选结果已全选。" : "当前筛选结果已取消全选。");
        }

        private void ResetFilters()
        {
            EmojiWindowNative.SetComboSelectedIndex(_cmbChannel, 0);
            EmojiWindowNative.SetComboSelectedIndex(_cmbStore, 0);
            EmojiWindowNative.SetComboSelectedIndex(_cmbStatus, 0);
            SetEditText(_txtKeyword, string.Empty);
            SetEditText(_txtAccountSearch, "🔍 搜索账号/备注/店铺");
            RefreshComboDisplays();
            ApplyFilters("已重置筛选条件。");
        }

        private void LaunchBrowser()
        {
            AccountRecord account = GetSelectedAccount();
            if (account == null)
            {
                UpdateStatusBar("请先在左侧选中一个账号。");
                return;
            }

            account.Status = "运行中";
            account.LastLogin = DateTime.Now;
            if (string.IsNullOrWhiteSpace(account.Url))
            {
                account.Url = "https://sellercentral.amazon.com/";
            }

            ApplyFilters($"已为 {account.Account} 启动浏览器容器。");
        }

        private void StopBrowser()
        {
            AccountRecord account = GetSelectedAccount();
            if (account == null)
            {
                UpdateStatusBar("请先在左侧选中一个账号。");
                return;
            }

            account.Status = "空闲";
            ApplyFilters($"已停止 {account.Account} 的浏览器实例。");
        }

        private void RefreshPage()
        {
            AccountRecord account = GetSelectedAccount();
            UpdateStatusBar(account == null ? "没有可刷新的账号。" : $"已刷新 {account.Account} 的当前页面。");
        }

        private void ClearCache()
        {
            AccountRecord account = GetSelectedAccount();
            UpdateStatusBar(account == null ? "没有可清理缓存的账号。" : $"已清理 {account.Account} 的缓存占位逻辑。");
        }

        private void Relogin()
        {
            AccountRecord account = GetSelectedAccount();
            if (account == null)
            {
                UpdateStatusBar("请先在左侧选中一个账号。");
                return;
            }

            account.Status = "登录中";
            account.LastLogin = DateTime.Now;
            ApplyFilters($"已触发 {account.Account} 的重登流程。");
        }

        private void OpenProductPage()
        {
            AccountRecord account = GetSelectedAccount();
            if (account == null)
            {
                UpdateStatusBar("请先在左侧选中一个账号。");
                return;
            }

            account.Url = "https://sellercentral.amazon.com/inventory";
            ApplyFilters($"已切换 {account.Account} 到商品页。");
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
            AccountRecord account = GetSelectedAccount();
            if (account == null)
            {
                UpdateStatusBar("请先在左侧选中一个账号。");
                return;
            }

            string url = GetEditText(_txtUrl).Trim();
            if (string.IsNullOrEmpty(url))
            {
                UpdateStatusBar("地址栏为空，未执行跳转。");
                return;
            }

            account.Url = url;
            ApplyFilters($"已更新 {account.Account} 的目标地址。");
        }

        private void ToggleTheme()
        {
            _darkModeEnabled = !_darkModeEnabled;
            EmojiWindowNative.SetDarkMode(_darkModeEnabled ? 1 : 0);
            ApplyThemeVisuals();
            UpdateAll(_darkModeEnabled ? "已切换到深色模式。" : "已切换到浅色模式。");
            RefreshComboDisplays();
        }

        private void UpdateThemeButton()
        {
            byte[] emojiBytes = U(_darkModeEnabled ? "☀️" : "🌙");
            EmojiWindowNative.SetButtonEmoji(_btnTheme, emojiBytes, emojiBytes.Length);
            SetButtonText(_btnTheme, string.Empty);
        }

        private void ApplyThemeVisuals()
        {
            uint page = GetPageBackgroundColor();
            uint surface = GetSurfaceColor();
            uint surfaceSoft = GetSurfaceSoftColor();
            uint surfaceMuted = GetSurfaceMutedColor();
            uint primarySoft = GetPrimarySoftColor();
            uint successSoft = GetSuccessSoftColor();
            uint dangerSoft = GetDangerSoftColor();
            uint text = GetTextColor();
            uint muted = GetMutedColor();
            uint border = GetBorderColor();

            EmojiWindowNative.set_window_titlebar_color(_window, GetTitleBarColor());
            EmojiWindowNative.SetWindowBackgroundColor(_window, page);
            EmojiWindowNative.SetTitleBarTextColor(_window, EmojiWindowNative.ARGB(255, 255, 255, 255));

            for (int i = 0; i < _cards.Length; i++)
            {
                MetricCard card = _cards[i];
                EmojiWindowNative.SetPanelBackgroundColor(card.Panel, surface);
                EmojiWindowNative.SetLabelColor(card.ValueLabel, card.AccentColor, surface);
                EmojiWindowNative.SetLabelColor(card.CaptionLabel, muted, surface);
                EmojiWindowNative.SetLabelColor(card.HintLabel, card.AccentColor, surface);
                EmojiWindowNative.SetLabelColor(card.TrendLabel, muted, surface);
            }

            EmojiWindowNative.SetPanelBackgroundColor(_statusBarPanel, page);
            EmojiWindowNative.SetPanelBackgroundColor(_accountsGroupFillPanel, surface);
            EmojiWindowNative.SetPanelBackgroundColor(_workspaceGroupFillPanel, surface);
            EmojiWindowNative.SetPanelBackgroundColor(_accountsHeaderMaskPanel, surface);
            EmojiWindowNative.SetPanelBackgroundColor(_workspaceHeaderMaskPanel, surface);
            EmojiWindowNative.SetPanelBackgroundColor(_accountsStatsPanel, surfaceSoft);
            EmojiWindowNative.SetPanelBackgroundColor(_filterTagsPanel, page);
            EmojiWindowNative.SetPanelBackgroundColor(_statAllPanel, primarySoft);
            EmojiWindowNative.SetPanelBackgroundColor(_statRunningPanel, successSoft);
            EmojiWindowNative.SetPanelBackgroundColor(_statIssuePanel, dangerSoft);
            EmojiWindowNative.SetPanelBackgroundColor(_currentAccountPanel, surfaceMuted);
            EmojiWindowNative.SetPanelBackgroundColor(_toolbarPanel, GetToolbarColor());
            EmojiWindowNative.SetPanelBackgroundColor(_browserHostPanel, GetBrowserHostColor());
            EmojiWindowNative.SetPanelBackgroundColor(_browserHeaderPanel, GetBrowserHeaderColor());
            EmojiWindowNative.SetPanelBackgroundColor(_browserCanvasPanel, GetBrowserCanvasColor());
            EmojiWindowNative.SetPanelBackgroundColor(_sessionStripPanel, surfaceMuted);

            EmojiWindowNative.SetLabelColor(_lblStatAllValue, Palette.Primary, primarySoft);
            EmojiWindowNative.SetLabelColor(_lblStatAllCaption, muted, primarySoft);
            EmojiWindowNative.SetLabelColor(_lblStatRunningValue, Palette.Success, successSoft);
            EmojiWindowNative.SetLabelColor(_lblStatRunningCaption, muted, successSoft);
            EmojiWindowNative.SetLabelColor(_lblStatIssueValue, Palette.Danger, dangerSoft);
            EmojiWindowNative.SetLabelColor(_lblStatIssueCaption, muted, dangerSoft);
            EmojiWindowNative.SetLabelColor(_lblAccountsGroupTitle, text, surface);
            EmojiWindowNative.SetLabelColor(_lblWorkspaceGroupTitle, text, surface);
            EmojiWindowNative.SetLabelColor(_lblCurrentAccount, text, surfaceMuted);
            EmojiWindowNative.SetLabelColor(_lblCurrentStore, muted, surfaceMuted);
            EmojiWindowNative.SetLabelColor(_lblCurrentNote, text, surfaceMuted);
            EmojiWindowNative.SetLabelColor(_lblGridEmptyState, muted, surface);
            EmojiWindowNative.SetLabelColor(_lblToolbarTitle, EmojiWindowNative.ARGB(255, 255, 255, 255), GetToolbarColor());
            EmojiWindowNative.SetLabelColor(_lblToolbarMeta, Palette.Cyan, GetToolbarColor());
            EmojiWindowNative.SetLabelColor(_lblBrowserTitle, EmojiWindowNative.ARGB(255, 255, 255, 255), GetBrowserHeaderColor());
            EmojiWindowNative.SetLabelColor(_lblBrowserSubtitle, Palette.Cyan, GetBrowserHeaderColor());
            EmojiWindowNative.SetLabelColor(_lblCanvasTitle, text, GetBrowserCanvasColor());
            EmojiWindowNative.SetLabelColor(_lblCanvasMeta, muted, GetBrowserCanvasColor());
            EmojiWindowNative.SetLabelColor(_lblAccountFooter, muted, page);
            EmojiWindowNative.SetLabelColor(_lblStatusBar, muted, page);

            EmojiWindowNative.SetEditBoxColor(_txtKeyword, text, surface);
            EmojiWindowNative.SetEditBoxColor(_txtAccountSearch, text, surface);
            EmojiWindowNative.SetEditBoxColor(_txtUrl, text, surface);
            uint comboSelect = _darkModeEnabled ? surfaceSoft : surface;
            uint comboHover = _darkModeEnabled ? surfaceMuted : surface;
            EmojiWindowNative.SetComboBoxColors(_cmbChannel, text, surface, comboSelect, comboHover);
            EmojiWindowNative.SetComboBoxColors(_cmbStore, text, surface, comboSelect, comboHover);
            EmojiWindowNative.SetComboBoxColors(_cmbStatus, text, surface, comboSelect, comboHover);
            EmojiWindowNative.DataGrid_SetColors(
                _gridAccounts,
                text,
                surface,
                GetBrowserHeaderColor(),
                EmojiWindowNative.ARGB(255, 255, 255, 255),
                _darkModeEnabled ? EmojiWindowNative.ARGB(255, 48, 72, 118) : EmojiWindowNative.ARGB(255, 216, 232, 255),
                _darkModeEnabled ? EmojiWindowNative.ARGB(255, 39, 52, 76) : Palette.Hover,
                border);

            ApplyButtonTheme(_btnReset, false);
            ApplyButtonTheme(_btnTheme, false);
            ApplyFlatSurfaceButtonTheme(_btnImport);
            ApplyFlatSurfaceButtonTheme(_btnExport);
            ApplyFlatSurfaceButtonTheme(_btnRefreshList);
            ApplyFlatSurfaceButtonTheme(_btnSelectAll);
            ApplyButtonTheme(_btnRefreshPage, false);
            ApplyButtonTheme(_btnClearCache, false);
            ApplyButtonTheme(_btnRelogin, false);
            ApplyButtonTheme(_btnSessionSecondary, false);
            ApplyButtonTheme(_btnSessionTertiary, false);

            UpdateThemeButton();
            PopulateGrid();
            RefreshComboDisplays();
        }

        private void ApplyButtonTheme(int buttonId, bool solid)
        {
            uint bg = solid ? Palette.Primary : GetNeutralButtonColor();
            uint text = EmojiWindowNative.ARGB(255, 255, 255, 255);
            uint border = solid ? Palette.Primary : GetNeutralButtonColor();
            EmojiWindowNative.SetButtonBackgroundColor(buttonId, bg);
            EmojiWindowNative.SetButtonTextColor(buttonId, text);
            EmojiWindowNative.SetButtonBorderColor(buttonId, border);
            uint hoverBg = solid ? Palette.Primary : GetNeutralButtonHoverColor();
            EmojiWindowNative.SetButtonHoverColors(buttonId, hoverBg, border, text);
        }

        private void ApplyFlatSurfaceButtonTheme(int buttonId)
        {
            uint bg = GetNeutralButtonColor();
            uint text = EmojiWindowNative.ARGB(255, 255, 255, 255);
            uint border = bg;
            EmojiWindowNative.SetButtonBackgroundColor(buttonId, bg);
            EmojiWindowNative.SetButtonTextColor(buttonId, text);
            EmojiWindowNative.SetButtonBorderColor(buttonId, border);
            uint hoverBg = GetNeutralButtonHoverColor();
            EmojiWindowNative.SetButtonHoverColors(buttonId, hoverBg, border, text);
        }

        private int UpdateCheckedAccounts(string newStatus, Action<AccountRecord> mutate)
        {
            int changed = 0;
            foreach (AccountRecord account in _accounts.Where(item => item.Checked))
            {
                account.Status = newStatus;
                mutate?.Invoke(account);
                changed++;
            }

            return changed;
        }

        private void AddImportedAccount(string accountName, string channel, string store, string note, string status)
        {
            _accounts.Add(new AccountRecord
            {
                Id = _nextId++,
                Account = accountName,
                Channel = channel,
                Store = store,
                Note = note,
                Status = status,
                Url = "https://sellercentral.amazon.com/",
                LastLogin = DateTime.Now.AddMinutes(-_nextId * 3)
            });
        }

        private void OnButtonClick(int buttonId, IntPtr parentHwnd)
        {
            if (_buttonActions.TryGetValue(buttonId, out Action action))
            {
                action();
            }
        }

        private void OnWindowResize(IntPtr hwnd, int width, int height)
        {
            if (hwnd != _window || width <= 0 || height <= 0)
            {
                return;
            }

            if (_windowWidth == width && _windowHeight == height)
            {
                return;
            }

            _windowWidth = width;
            _windowHeight = height;
            ApplyLayoutFixed();
        }

        private void OnWindowClose(IntPtr hwnd)
        {
        }

        private void OnGridCellClick(IntPtr hGrid, int row, int col)
        {
            if (hGrid != _gridAccounts || row < 0 || row >= _visibleAccounts.Count)
            {
                return;
            }

            if (col == 0)
            {
                SyncCheckedState(row);
                UpdateAll($"已切换 {_visibleAccounts[row].Account} 的勾选状态。");
                return;
            }

            _selectedAccountId = _visibleAccounts[row].Id;
            UpdateAll($"已切换当前账号到 {_visibleAccounts[row].Account}。");
        }

        private void OnGridValueChanged(IntPtr hGrid, int row, int col)
        {
            if (hGrid != _gridAccounts || row < 0 || row >= _visibleAccounts.Count)
            {
                return;
            }

            if (col == 0)
            {
                SyncCheckedState(row);
                UpdateAll("批量选择状态已更新。");
            }
        }

        private void OnGridSelectionChanged(IntPtr hGrid, int row, int col)
        {
            if (hGrid != _gridAccounts || row < 0 || row >= _visibleAccounts.Count)
            {
                return;
            }

            _selectedAccountId = _visibleAccounts[row].Id;
            UpdateAll($"当前聚焦账号: {_visibleAccounts[row].Account}");
        }

        private void OnGridHeaderClick(IntPtr hGrid, int col)
        {
            if (hGrid != _gridAccounts || col <= 0)
            {
                return;
            }

            if (_sortColumn == col)
            {
                _sortAscending = !_sortAscending;
            }
            else
            {
                _sortColumn = col;
                _sortAscending = true;
            }

            ApplyFilters($"已按“{GetColumnName(col)}”{(_sortAscending ? "升序" : "降序")}排序。");
        }

        private void SyncCheckedState(int row)
        {
            bool isChecked = EmojiWindowNative.DataGrid_GetCellChecked(_gridAccounts, row, 0) != 0;
            _visibleAccounts[row].Checked = isChecked;
            _selectAllChecked = _visibleAccounts.Count > 0 && _visibleAccounts.All(item => item.Checked);
        }

        private void ApplyAccountGridColumnWidths(int innerWidth)
        {
            if (_gridAccounts == IntPtr.Zero || innerWidth < 200)
            {
                return;
            }

            int[] @base = AccountGridColumnWidthsBase;
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
                EmojiWindowNative.DataGrid_SetColumnWidth(_gridAccounts, i, col[i]);
            }
        }

        private void ApplyLayout()
        {
            int padding = 16;
            int gap = 12;
            int topInset = TitleBarHeight + 8;
            int cardsY = topInset;
            int cardsHeight = 96;
            int utilityY = cardsY + cardsHeight + 10;
            int contentY = utilityY + 6;
            int statusHeight = 32;
            int contentBottom = _windowHeight - padding - statusHeight - 2;
            int contentHeight = Math.Max(420, contentBottom - contentY);
            int leftWidth = Math.Max(420, Math.Min(520, (_windowWidth - padding * 2 - gap) * 34 / 100));
            int rightX = padding + leftWidth + gap;
            int rightWidth = Math.Max(620, _windowWidth - rightX - padding);

            int cardWidth = (_windowWidth - padding * 2 - gap * (CardCount - 1)) / CardCount;
            for (int i = 0; i < _cards.Length; i++)
            {
                int x = padding + i * (cardWidth + gap);
                MetricCard card = _cards[i];
                MoveWindow(card.Panel, x, cardsY, cardWidth, cardsHeight);
                MoveWindow(card.AccentBar, 0, 0, cardWidth, 6);
                EmojiWindowNative.SetLabelBounds(card.BadgeLabel, cardWidth - 78, 14, 58, 18);
                EmojiWindowNative.SetLabelBounds(card.ValueLabel, 16, 18, cardWidth - 32, 30);
                EmojiWindowNative.SetLabelBounds(card.CaptionLabel, 16, 50, cardWidth - 32, 18);
                EmojiWindowNative.SetLabelBounds(card.HintLabel, 16, 66, cardWidth - 32, 14);
                EmojiWindowNative.SetLabelBounds(card.TrendLabel, 16, 80, cardWidth - 32, 14);
            }

            int themeWidth = 42;
            EmojiWindowNative.SetEditBoxBounds(_txtKeyword, -2000, -2000, 1, 1);

            MoveWindow(_accountsGroup, -2000, -2000, 1, 1);
            MoveWindow(_workspaceGroup, -2000, -2000, 1, 1);
            MoveWindow(_accountsGroupFillPanel, padding, contentY, leftWidth, contentHeight);
            MoveWindow(_workspaceGroupFillPanel, rightX, contentY, rightWidth, contentHeight);
            MoveWindow(_accountsHeaderMaskPanel, -2000, -2000, 1, 1);
            MoveWindow(_workspaceHeaderMaskPanel, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblAccountsGroupTitle, padding + 16, contentY + 10, 96, 20);
            EmojiWindowNative.SetLabelBounds(_lblWorkspaceGroupTitle, -2000, -2000, 1, 1);

            int accountsInnerX = padding + 12;
            int leftInnerWidth = leftWidth - 24;
            int rowGap = 8;
            int filtersY = contentY + 18;
            int searchY = contentY + 62;
            int actionsY1 = contentY + 108;
            int actionsY2 = contentY + 150;
            int gridY = contentY + 198;
            int footerY = contentY + contentHeight - 34;
            int gridHeight = Math.Max(220, footerY - gridY - 8);
            int comboWidth = (leftInnerWidth - rowGap * 2) / 3;
            int searchButtonWidth = 68;
            int searchWidth = leftInnerWidth - searchButtonWidth * 2 - rowGap * 2;
            int row1ButtonWidth = (leftInnerWidth - rowGap * 3) / 4;
            int row2ButtonWidth = (leftInnerWidth - rowGap * 3) / 4;

            SetComboBoxBounds(_cmbChannel, accountsInnerX, filtersY, comboWidth, 34);
            SetComboBoxBounds(_cmbStore, accountsInnerX + comboWidth + rowGap, filtersY, comboWidth, 34);
            SetComboBoxBounds(_cmbStatus, accountsInnerX + (comboWidth + rowGap) * 2, filtersY, comboWidth, 34);
            EmojiWindowNative.SetEditBoxBounds(_txtAccountSearch, accountsInnerX, searchY, searchWidth, 34);
            EmojiWindowNative.SetButtonBounds(_btnQuery, accountsInnerX + searchWidth + rowGap, searchY, searchButtonWidth, 34);
            EmojiWindowNative.SetButtonBounds(_btnReset, accountsInnerX + searchWidth + rowGap + searchButtonWidth + rowGap, searchY, searchButtonWidth, 34);

            EmojiWindowNative.SetButtonBounds(_btnAdd, accountsInnerX, actionsY1, row1ButtonWidth, 34);
            EmojiWindowNative.SetButtonBounds(_btnImport, accountsInnerX + row1ButtonWidth + rowGap, actionsY1, row1ButtonWidth, 34);
            EmojiWindowNative.SetButtonBounds(_btnExport, accountsInnerX + (row1ButtonWidth + rowGap) * 2, actionsY1, row1ButtonWidth, 34);
            EmojiWindowNative.SetButtonBounds(_btnRefreshList, accountsInnerX + (row1ButtonWidth + rowGap) * 3, actionsY1, row1ButtonWidth, 34);
            EmojiWindowNative.SetButtonBounds(_btnSelectAll, accountsInnerX, actionsY2, row2ButtonWidth, 34);
            EmojiWindowNative.SetButtonBounds(_btnBatchStart, accountsInnerX + row2ButtonWidth + rowGap, actionsY2, row2ButtonWidth, 34);
            EmojiWindowNative.SetButtonBounds(_btnBatchStop, accountsInnerX + (row2ButtonWidth + rowGap) * 2, actionsY2, row2ButtonWidth, 34);
            EmojiWindowNative.SetButtonBounds(_btnBatchDelete, accountsInnerX + (row2ButtonWidth + rowGap) * 3, actionsY2, row2ButtonWidth, 34);

            MoveWindow(_accountsStatsPanel, -2000, -2000, 1, 1);
            MoveWindow(_statAllPanel, -2000, -2000, 1, 1);
            MoveWindow(_statRunningPanel, -2000, -2000, 1, 1);
            MoveWindow(_statIssuePanel, -2000, -2000, 1, 1);
            MoveWindow(_filterTagsPanel, -2000, -2000, 1, 1);

            EmojiWindowNative.DataGrid_SetBounds(_gridAccounts, accountsInnerX, gridY, leftInnerWidth, gridHeight);
            ApplyAccountGridColumnWidths(leftInnerWidth);
            EmojiWindowNative.SetLabelBounds(_lblGridEmptyState, accountsInnerX + 24, gridY + 88, leftInnerWidth - 48, 72);
            EmojiWindowNative.SetLabelBounds(_lblAccountFooter, accountsInnerX, footerY, leftInnerWidth, 20);

            int rightInnerX = rightX + 12;
            int rightInnerWidth = rightWidth - 24;
            int addressY = contentY + 12;
            int actionsY = addressY + 34 + 10;
            int browserY = actionsY + 34 + 10;
            int footerWorkY = contentY + contentHeight - 34;
            int browserHeight = Math.Max(260, footerWorkY - browserY - 4);

            MoveWindow(_currentAccountPanel, -2000, -2000, 1, 1);
            MoveWindow(_toolbarPanel, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblCurrentAccount, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblCurrentStore, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblCurrentNote, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblCurrentStatus, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblToolbarTitle, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblToolbarMeta, -2000, -2000, 1, 1);

            int urlGap = 10;
            EmojiWindowNative.SetEditBoxBounds(_txtUrl, rightInnerX, addressY, rightInnerWidth - themeWidth - urlGap, 34);
            EmojiWindowNative.SetButtonBounds(_btnTheme, rightInnerX + rightInnerWidth - themeWidth, addressY, themeWidth, 34);

            int actionGap = 10;
            int b1 = 94;
            int b2 = 72;
            int b3 = 72;
            int b4 = 84;
            int b5 = 72;
            int b6 = 104;
            EmojiWindowNative.SetButtonBounds(_btnLaunchBrowser, rightInnerX, actionsY, b1, 34);
            EmojiWindowNative.SetButtonBounds(_btnStopBrowser, rightInnerX + b1 + actionGap, actionsY, b2, 34);
            EmojiWindowNative.SetButtonBounds(_btnRefreshPage, rightInnerX + b1 + actionGap + b2 + actionGap, actionsY, b3, 34);
            EmojiWindowNative.SetButtonBounds(_btnClearCache, rightInnerX + b1 + actionGap + b2 + actionGap + b3 + actionGap, actionsY, b4, 34);
            EmojiWindowNative.SetButtonBounds(_btnRelogin, rightInnerX + b1 + actionGap + b2 + actionGap + b3 + actionGap + b4 + actionGap, actionsY, b5, 34);
            EmojiWindowNative.SetButtonBounds(_btnOpenProduct, rightInnerX + b1 + actionGap + b2 + actionGap + b3 + actionGap + b4 + actionGap + b5 + actionGap, actionsY, b6, 34);

            MoveWindow(_browserHostPanel, rightInnerX, browserY, rightInnerWidth, browserHeight);
            MoveWindow(_browserHeaderPanel, 0, 0, rightInnerWidth, 58);
            MoveWindow(_browserCanvasPanel, 1, 59, rightInnerWidth - 2, browserHeight - 60);
            MoveWindow(_sessionStripPanel, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblBrowserTitle, 20, 14, rightInnerWidth - 180, 24);
            EmojiWindowNative.SetLabelBounds(_lblBrowserSubtitle, 20, 34, rightInnerWidth - 220, 18);
            EmojiWindowNative.SetLabelBounds(_lblBrowserChip, rightInnerWidth - 138, 18, 110, 24);
            EmojiWindowNative.SetButtonBounds(_btnSessionPrimary, -2000, -2000, 1, 1);
            EmojiWindowNative.SetButtonBounds(_btnSessionSecondary, -2000, -2000, 1, 1);
            EmojiWindowNative.SetButtonBounds(_btnSessionTertiary, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblCanvasTitle, 28, 24, rightInnerWidth - 56, 30);
            EmojiWindowNative.SetLabelBounds(_lblCanvasMeta, 28, 62, rightInnerWidth - 56, 22);
            EmojiWindowNative.SetLabelBounds(_lblWorkspaceStatus, rightInnerX, footerWorkY, rightInnerWidth, 20);

            MoveWindow(_statusBarPanel, padding, _windowHeight - padding - 24, _windowWidth - padding * 2, 24);
            EmojiWindowNative.SetLabelBounds(_lblStatusBar, padding + 8, _windowHeight - padding - 22, _windowWidth - padding * 2 - 16, 20);
        }

        private void ApplyLayoutFixed()
        {
            int padding = 16;
            int gap = 12;
            int topInset = TitleBarHeight + 8;
            int cardsY = topInset;
            int cardsHeight = 96;
            int utilityY = cardsY + cardsHeight + 10;
            int contentY = utilityY + 6;
            int statusHeight = 32;
            int contentBottom = _windowHeight - padding - statusHeight - 2;
            int contentHeight = Math.Max(420, contentBottom - contentY);
            int leftWidth = 440;
            int rightX = padding + leftWidth + gap;
            int rightWidth = _windowWidth - rightX - padding;

            int cardWidth = (_windowWidth - padding * 2 - gap * (CardCount - 1)) / CardCount;
            for (int i = 0; i < _cards.Length; i++)
            {
                int x = padding + i * (cardWidth + gap);
                MetricCard card = _cards[i];
                MoveWindow(card.Panel, x, cardsY, cardWidth, cardsHeight);
                MoveWindow(card.AccentBar, 0, 0, cardWidth, 6);
                EmojiWindowNative.SetLabelBounds(card.BadgeLabel, cardWidth - 78, 14, 58, 18);
                EmojiWindowNative.SetLabelBounds(card.ValueLabel, 16, 18, cardWidth - 32, 30);
                EmojiWindowNative.SetLabelBounds(card.CaptionLabel, 16, 50, cardWidth - 32, 18);
                EmojiWindowNative.SetLabelBounds(card.HintLabel, 16, 66, cardWidth - 32, 14);
                EmojiWindowNative.SetLabelBounds(card.TrendLabel, 16, 80, cardWidth - 32, 14);
            }

            int themeWidth = 42;
            EmojiWindowNative.SetEditBoxBounds(_txtKeyword, -2000, -2000, 1, 1);

            MoveWindow(_accountsGroup, -2000, -2000, 1, 1);
            MoveWindow(_workspaceGroup, -2000, -2000, 1, 1);
            MoveWindow(_accountsGroupFillPanel, padding, contentY, leftWidth, contentHeight);
            MoveWindow(_workspaceGroupFillPanel, rightX, contentY, rightWidth, contentHeight);
            MoveWindow(_accountsHeaderMaskPanel, -2000, -2000, 1, 1);
            MoveWindow(_workspaceHeaderMaskPanel, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblAccountsGroupTitle, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblWorkspaceGroupTitle, -2000, -2000, 1, 1);

            int accountsInnerX = padding + 12;
            int leftInnerWidth = leftWidth - 24;
            int rowGap = 8;
            int filtersY = contentY + 18;
            int searchY = contentY + 60;
            int actionsY1 = contentY + 106;
            int actionsY2 = contentY + 148;
            int gridY = contentY + 196;
            int footerY = contentY + contentHeight - 34;
            int gridHeight = Math.Max(220, footerY - gridY - 8);
            int comboWidth = (leftInnerWidth - rowGap * 2) / 3;
            int searchButtonWidth = 58;
            int searchWidth = leftInnerWidth - searchButtonWidth * 2 - rowGap * 2;
            int actionWidth = (leftInnerWidth - rowGap * 3) / 4;

            SetComboBoxBounds(_cmbChannel, accountsInnerX, filtersY, comboWidth, 34);
            SetComboBoxBounds(_cmbStore, accountsInnerX + comboWidth + rowGap, filtersY, comboWidth, 34);
            SetComboBoxBounds(_cmbStatus, accountsInnerX + (comboWidth + rowGap) * 2, filtersY, comboWidth, 34);

            EmojiWindowNative.SetEditBoxBounds(_txtAccountSearch, accountsInnerX, searchY, searchWidth, 34);
            EmojiWindowNative.SetButtonBounds(_btnQuery, accountsInnerX + searchWidth + rowGap, searchY, searchButtonWidth, 34);
            EmojiWindowNative.SetButtonBounds(_btnReset, accountsInnerX + searchWidth + rowGap + searchButtonWidth + rowGap, searchY, searchButtonWidth, 34);

            EmojiWindowNative.SetButtonBounds(_btnAdd, accountsInnerX, actionsY1, actionWidth, 34);
            EmojiWindowNative.SetButtonBounds(_btnImport, accountsInnerX + actionWidth + rowGap, actionsY1, actionWidth, 34);
            EmojiWindowNative.SetButtonBounds(_btnExport, accountsInnerX + (actionWidth + rowGap) * 2, actionsY1, actionWidth, 34);
            EmojiWindowNative.SetButtonBounds(_btnRefreshList, accountsInnerX + (actionWidth + rowGap) * 3, actionsY1, actionWidth, 34);
            EmojiWindowNative.SetButtonBounds(_btnSelectAll, accountsInnerX, actionsY2, actionWidth, 34);
            EmojiWindowNative.SetButtonBounds(_btnBatchStart, accountsInnerX + actionWidth + rowGap, actionsY2, actionWidth, 34);
            EmojiWindowNative.SetButtonBounds(_btnBatchStop, accountsInnerX + (actionWidth + rowGap) * 2, actionsY2, actionWidth, 34);
            EmojiWindowNative.SetButtonBounds(_btnBatchDelete, accountsInnerX + (actionWidth + rowGap) * 3, actionsY2, actionWidth, 34);

            MoveWindow(_accountsStatsPanel, -2000, -2000, 1, 1);
            MoveWindow(_statAllPanel, -2000, -2000, 1, 1);
            MoveWindow(_statRunningPanel, -2000, -2000, 1, 1);
            MoveWindow(_statIssuePanel, -2000, -2000, 1, 1);
            MoveWindow(_filterTagsPanel, -2000, -2000, 1, 1);

            EmojiWindowNative.DataGrid_SetBounds(_gridAccounts, accountsInnerX, gridY, leftInnerWidth, gridHeight);
            ApplyAccountGridColumnWidths(leftInnerWidth);
            EmojiWindowNative.SetLabelBounds(_lblGridEmptyState, accountsInnerX + 24, gridY + 88, leftInnerWidth - 48, 72);
            EmojiWindowNative.SetLabelBounds(_lblAccountFooter, accountsInnerX, footerY, leftInnerWidth, 20);

            int rightInnerX = rightX + 12;
            int rightInnerWidth = rightWidth - 24;
            int addressY = contentY + 12;
            int actionsY = addressY + 34 + 10;
            int browserY = actionsY + 34 + 10;
            int footerWorkY = contentY + contentHeight - 34;
            int browserHeight = Math.Max(300, footerWorkY - browserY - 2);

            MoveWindow(_currentAccountPanel, -2000, -2000, 1, 1);
            MoveWindow(_toolbarPanel, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblCurrentAccount, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblCurrentStore, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblCurrentNote, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblCurrentStatus, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblToolbarTitle, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblToolbarMeta, -2000, -2000, 1, 1);

            int urlGap = 10;
            EmojiWindowNative.SetEditBoxBounds(_txtUrl, rightInnerX, addressY, rightInnerWidth - themeWidth - urlGap, 34);
            EmojiWindowNative.SetButtonBounds(_btnTheme, rightInnerX + rightInnerWidth - themeWidth, addressY, themeWidth, 34);

            int actionGap = 10;
            int b1 = 92;
            int b2 = 70;
            int b3 = 70;
            int b4 = 82;
            int b5 = 70;
            int b6 = 102;
            EmojiWindowNative.SetButtonBounds(_btnLaunchBrowser, rightInnerX, actionsY, b1, 34);
            EmojiWindowNative.SetButtonBounds(_btnStopBrowser, rightInnerX + b1 + actionGap, actionsY, b2, 34);
            EmojiWindowNative.SetButtonBounds(_btnRefreshPage, rightInnerX + b1 + actionGap + b2 + actionGap, actionsY, b3, 34);
            EmojiWindowNative.SetButtonBounds(_btnClearCache, rightInnerX + b1 + actionGap + b2 + actionGap + b3 + actionGap, actionsY, b4, 34);
            EmojiWindowNative.SetButtonBounds(_btnRelogin, rightInnerX + b1 + actionGap + b2 + actionGap + b3 + actionGap + b4 + actionGap, actionsY, b5, 34);
            EmojiWindowNative.SetButtonBounds(_btnOpenProduct, rightInnerX + b1 + actionGap + b2 + actionGap + b3 + actionGap + b4 + actionGap + b5 + actionGap, actionsY, b6, 34);

            MoveWindow(_browserHostPanel, rightInnerX, browserY, rightInnerWidth, browserHeight);
            MoveWindow(_browserHeaderPanel, -2000, -2000, 1, 1);
            MoveWindow(_browserCanvasPanel, 0, 0, rightInnerWidth, browserHeight);
            MoveWindow(_sessionStripPanel, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblBrowserTitle, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblBrowserSubtitle, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblBrowserChip, -2000, -2000, 1, 1);
            EmojiWindowNative.SetButtonBounds(_btnSessionPrimary, -2000, -2000, 1, 1);
            EmojiWindowNative.SetButtonBounds(_btnSessionSecondary, -2000, -2000, 1, 1);
            EmojiWindowNative.SetButtonBounds(_btnSessionTertiary, -2000, -2000, 1, 1);
            EmojiWindowNative.SetLabelBounds(_lblCanvasTitle, 28, 28, rightInnerWidth - 56, 30);
            EmojiWindowNative.SetLabelBounds(_lblCanvasMeta, 28, 66, rightInnerWidth - 56, 22);
            EmojiWindowNative.SetLabelBounds(_lblWorkspaceStatus, rightInnerX, footerWorkY, rightInnerWidth, 20);

            MoveWindow(_statusBarPanel, padding, _windowHeight - padding - 24, _windowWidth - padding * 2, 24);
            EmojiWindowNative.SetLabelBounds(_lblStatusBar, padding + 8, _windowHeight - padding - 22, _windowWidth - padding * 2 - 16, 20);
        }

        private void SeedAccounts()
        {
            AddSeedAccount("shop_us_001", "Amazon", "美国站A店", "主账号 / 独享代理", "运行中", "https://sellercentral.amazon.com/");
            AddSeedAccount("shop_us_002", "Amazon", "美国站B店", "备用账号 / 广告组", "空闲", "https://sellercentral.amazon.com/");
            AddSeedAccount("shop_jp_001", "Amazon", "日本站旗舰店", "活动专用", "登录中", "https://sellercentral-japan.amazon.com/");
            AddSeedAccount("shop_uk_003", "Temu", "英国站精选店", "高客单品店铺", "异常", "https://seller.temu.com/");
            AddSeedAccount("brand_site_01", "Shopify", "独立站A", "品牌站 / 大促页", "运行中", "https://admin.shopify.com/");
            AddSeedAccount("tiktok_store_7", "TikTok Shop", "美国站A店", "直播店铺", "空闲", "https://seller-us.tiktok.com/");
            AddSeedAccount("shop_us_008", "Amazon", "美国站A店", "FBA 补货账号", "空闲", "https://sellercentral.amazon.com/inventory");
            AddSeedAccount("shop_jp_008", "Amazon", "日本站旗舰店", "品牌备案跟进", "异常", "https://sellercentral-japan.amazon.com/brand");
        }

        private void AddSeedAccount(string account, string channel, string store, string note, string status, string url)
        {
            _accounts.Add(new AccountRecord
            {
                Id = _nextId++,
                Account = account,
                Channel = channel,
                Store = store,
                Note = note,
                Status = status,
                Url = url,
                LastLogin = DateTime.Now.AddMinutes(-_nextId * 11)
            });
        }

        private IntPtr CreateGroupBox(string title)
        {
            byte[] titleBytes = U(title);
            IntPtr group = EmojiWindowNative.CreateGroupBox(
                _window,
                0,
                0,
                100,
                100,
                titleBytes,
                titleBytes.Length,
                Palette.BorderStrong,
                Palette.PageBackground,
                _fontYaHei,
                _fontYaHei.Length,
                14,
                1,
                0,
                0);
            EmojiWindowNative.SetGroupBoxStyle(group, 1);
            EmojiWindowNative.SetGroupBoxTitleColor(group, Palette.Text);
            return group;
        }

        private IntPtr CreateLabel(IntPtr parent, int x, int y, int width, int height, string text, uint fg, uint bg, int fontSize, int bold, int wrap = 0, int alignment = 0)
        {
            byte[] textBytes = U(text);
            return EmojiWindowNative.CreateLabel(
                parent == IntPtr.Zero ? _window : parent,
                x,
                y,
                width,
                height,
                textBytes,
                textBytes.Length,
                fg,
                bg,
                _fontYaHei,
                _fontYaHei.Length,
                fontSize,
                bold,
                0,
                0,
                alignment,
                wrap);
        }

        private IntPtr CreateEditBox(IntPtr parent, int x, int y, int width, int height, string text)
        {
            byte[] textBytes = U(text);
            return EmojiWindowNative.CreateEditBox(
                parent,
                x,
                y,
                width,
                height,
                textBytes,
                textBytes.Length,
                Palette.Text,
                Palette.Surface,
                _fontSegoe,
                _fontSegoe.Length,
                12,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                1,
                1);
        }

        private IntPtr CreateCombo(IntPtr parent, int x, int y, int width, int height)
        {
            return EmojiWindowNative.CreateComboBox(
                parent,
                x,
                y,
                width,
                height,
                1,
                Palette.Text,
                Palette.Surface,
                32,
                _fontSegoe,
                _fontSegoe.Length,
                13,
                0,
                0,
                0);
        }

        private int CreateButton(string text, uint bgColor, Action onClick)
        {
            byte[] textBytes = U(text);
            int buttonId = EmojiWindowNative.create_emoji_button_bytes(_window, Array.Empty<byte>(), 0, textBytes, textBytes.Length, 0, 0, 90, 32, bgColor);
            _buttonActions[buttonId] = onClick;
            EmojiWindowNative.SetButtonStyle(buttonId, 0);
            EmojiWindowNative.SetButtonSize(buttonId, 1);
            EmojiWindowNative.SetButtonRound(buttonId, 0);
            EmojiWindowNative.SetButtonCircle(buttonId, 0);
            return buttonId;
        }

        private void FillCombo(IntPtr combo, string fallback, IEnumerable<string> items)
        {
            EmojiWindowNative.ClearComboBox(combo);
            int count = 0;
            foreach (string item in items)
            {
                byte[] textBytes = U(item);
                EmojiWindowNative.AddComboItem(combo, textBytes, textBytes.Length);
                count++;
            }

            if (count == 0)
            {
                byte[] fallbackBytes = U(fallback);
                EmojiWindowNative.AddComboItem(combo, fallbackBytes, fallbackBytes.Length);
            }

            EmojiWindowNative.SetComboSelectedIndex(combo, 0);
        }

        private string GetSelectedComboText(IntPtr combo)
        {
            int index = EmojiWindowNative.GetComboSelectedIndex(combo);
            return index < 0 ? string.Empty : EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetComboItemText, combo, index);
        }

        private string GetEditText(IntPtr edit)
        {
            return EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetEditBoxText, edit);
        }

        private void SetEditText(IntPtr edit, string text)
        {
            byte[] textBytes = U(text);
            EmojiWindowNative.SetEditBoxText(edit, textBytes, textBytes.Length);
        }

        private void SetLabelText(IntPtr label, string text)
        {
            byte[] textBytes = U(text);
            EmojiWindowNative.SetLabelText(label, textBytes, textBytes.Length);
        }

        private void SetButtonText(int buttonId, string text)
        {
            byte[] textBytes = U(text);
            EmojiWindowNative.SetButtonText(buttonId, textBytes, textBytes.Length);
        }

        private void SetGridText(int row, int col, string text)
        {
            byte[] textBytes = U(text);
            EmojiWindowNative.DataGrid_SetCellText(_gridAccounts, row, col, textBytes, textBytes.Length);
        }

        private AccountRecord GetSelectedAccount()
        {
            return _accounts.FirstOrDefault(item => item.Id == _selectedAccountId);
        }

        private string GetColumnName(int col)
        {
            switch (col)
            {
                case 1: return "账号";
                case 2: return "店铺";
                case 3: return "备注";
                case 4: return "状态";
                default: return "列表";
            }
        }

        private string BuildStatusBadgeText(string status)
        {
            switch (status)
            {
                case "运行中":
                    return "● 运行中";
                case "异常":
                    return "● 异常";
                case "登录中":
                    return "● 登录中";
                default:
                    return "● 空闲";
            }
        }

        private void ApplyStoreStyle(int row, AccountRecord account)
        {
            uint bg;
            uint fg;

            switch (account.Channel)
            {
                case "Amazon":
                    bg = EmojiWindowNative.ARGB(255, 255, 245, 229);
                    fg = EmojiWindowNative.ARGB(255, 180, 95, 0);
                    break;
                case "Shopify":
                    bg = EmojiWindowNative.ARGB(255, 237, 250, 241);
                    fg = EmojiWindowNative.ARGB(255, 17, 120, 60);
                    break;
                case "Temu":
                    bg = EmojiWindowNative.ARGB(255, 255, 239, 236);
                    fg = EmojiWindowNative.ARGB(255, 215, 73, 36);
                    break;
                case "TikTok Shop":
                    bg = EmojiWindowNative.ARGB(255, 238, 246, 255);
                    fg = EmojiWindowNative.ARGB(255, 20, 86, 180);
                    break;
                default:
                    bg = Palette.SurfaceSoft;
                    fg = Palette.Text;
                    break;
            }

            EmojiWindowNative.DataGrid_SetCellStyle(_gridAccounts, row, 2, fg, bg, 1, 0);
        }

        private void SetFilterTagTexts()
        {
            string channelText = GetSelectedComboText(_cmbChannel);
            string storeText = GetSelectedComboText(_cmbStore);
            string statusText = GetSelectedComboText(_cmbStatus);
            string channel = ExtractComboValue(channelText);
            string store = ExtractComboValue(storeText);
            string status = ExtractComboValue(statusText);

            SetLabelText(_lblTagChannel, "渠道: " + NormalizeFilterValue(channelText, "🌐 全部渠道"));
            SetLabelText(_lblTagStore, "店铺: " + NormalizeFilterValue(storeText, "全部店铺"));
            SetLabelText(_lblTagStatus, "状态: " + NormalizeFilterValue(statusText, "🎯 全部状态"));

            EmojiWindowNative.SetLabelColor(_lblTagChannel, EmojiWindowNative.ARGB(255, 255, 255, 255), channel == "全部渠道" || string.IsNullOrEmpty(channel) ? Palette.Info : Palette.Primary);
            EmojiWindowNative.SetLabelColor(_lblTagStore, EmojiWindowNative.ARGB(255, 255, 255, 255), store == "全部店铺" || string.IsNullOrEmpty(store) ? Palette.Primary : Palette.Warning);
            EmojiWindowNative.SetLabelColor(_lblTagStatus, EmojiWindowNative.ARGB(255, 255, 255, 255), status == "全部状态" || string.IsNullOrEmpty(status) ? Palette.Success : GetStatusBadgeColor(status));
        }

        private string NormalizeFilterValue(string value, string fallback)
        {
            return string.IsNullOrEmpty(value) ? fallback : value;
        }

        private string NormalizeSearchText(string value)
        {
            if (string.IsNullOrWhiteSpace(value))
            {
                return string.Empty;
            }

            string trimmed = value.Trim();
            return trimmed.IndexOf("搜索账号/备注", StringComparison.Ordinal) >= 0
                ? string.Empty
                : trimmed;
        }

        private string NormalizeGlobalSearchText(string value)
        {
            if (string.IsNullOrWhiteSpace(value))
            {
                return string.Empty;
            }

            string trimmed = value.Trim();
            return string.Equals(trimmed, "全局搜索账号/备注/店铺", StringComparison.Ordinal)
                ? string.Empty
                : trimmed;
        }

        private string ExtractComboValue(string text)
        {
            if (string.IsNullOrWhiteSpace(text))
            {
                return string.Empty;
            }

            int separator = text.IndexOf(' ');
            if (separator >= 0 && separator + 1 < text.Length)
            {
                return text.Substring(separator + 1).Trim();
            }

            return text.Trim();
        }

        private void RefreshComboDisplays()
        {
            SyncComboDisplay(_cmbChannel);
            SyncComboDisplay(_cmbStore);
            SyncComboDisplay(_cmbStatus);
        }

        private void SyncComboDisplay(IntPtr combo)
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

            string itemText = EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetComboItemText, combo, index);
            if (string.IsNullOrEmpty(itemText))
            {
                return;
            }

            byte[] bytes = U(itemText);
            EmojiWindowNative.SetComboSelectedIndex(combo, index);
            EmojiWindowNative.SetComboBoxText(combo, bytes, bytes.Length);
        }

        private List<AccountRecord> BuildSessionCandidates(AccountRecord current)
        {
            List<AccountRecord> sessions = new List<AccountRecord> { current };
            foreach (AccountRecord account in _accounts)
            {
                if (account.Id == current.Id || account.Status == "异常")
                {
                    continue;
                }

                sessions.Add(account);
                if (sessions.Count == 3)
                {
                    break;
                }
            }

            return sessions;
        }

        private void UpdateSessionTabs(IReadOnlyList<AccountRecord> sessions)
        {
            UpdateSessionButton(_btnSessionPrimary, 0, sessions.Count > 0 ? sessions[0] : null, true);
            UpdateSessionButton(_btnSessionSecondary, 1, sessions.Count > 1 ? sessions[1] : null, false);
            UpdateSessionButton(_btnSessionTertiary, 2, sessions.Count > 2 ? sessions[2] : null, false);
        }

        private void UpdateSessionButton(int buttonId, int slot, AccountRecord account, bool primarySlot)
        {
            _sessionAccountIds[slot] = account?.Id ?? -1;
            if (account == null)
            {
                SetButtonText(buttonId, slot == 0 ? "当前会话  空" : slot == 1 ? "待切换  空" : "代理槽位  空");
                ApplySessionButtonStyle(buttonId, Palette.SurfaceSoft, false);
                return;
            }

            string prefix = slot == 0 ? "当前会话" : slot == 1 ? "待切换" : "代理槽位";
            SetButtonText(buttonId, $"{prefix}  {account.Account}");
            ApplySessionButtonStyle(buttonId, GetSessionButtonColor(account, primarySlot), account.Id == _selectedAccountId);
        }

        private uint GetSessionButtonColor(AccountRecord account, bool primarySlot)
        {
            if (account.Id == _selectedAccountId)
            {
                return Palette.Primary;
            }

            switch (account.Status)
            {
                case "运行中":
                    return Palette.Success;
                case "登录中":
                    return Palette.Warning;
                case "空闲":
                    return primarySlot ? Palette.Primary : GetNeutralButtonColor();
                default:
                    return GetNeutralButtonColor();
            }
        }

        private void ApplySessionButtonStyle(int buttonId, uint bgColor, bool selected)
        {
            uint textColor = EmojiWindowNative.ARGB(255, 255, 255, 255);
            uint borderColor = selected ? Palette.Primary : bgColor;
            if (!_darkModeEnabled && bgColor != Palette.Primary && bgColor != Palette.Success && bgColor != Palette.Warning && bgColor != Palette.Danger)
            {
                textColor = Palette.Text;
                borderColor = GetBorderStrongColor();
            }
            EmojiWindowNative.SetButtonBackgroundColor(buttonId, bgColor);
            EmojiWindowNative.SetButtonTextColor(buttonId, textColor);
            EmojiWindowNative.SetButtonBorderColor(buttonId, borderColor);
            uint hoverBg = bgColor == Palette.Primary ? Palette.Primary : GetNeutralButtonHoverColor();
            EmojiWindowNative.SetButtonHoverColors(buttonId, hoverBg, borderColor, textColor);
        }

        private void SwitchSession(int slot)
        {
            if (slot < 0 || slot >= _sessionAccountIds.Length)
            {
                return;
            }

            int accountId = _sessionAccountIds[slot];
            if (accountId <= 0)
            {
                return;
            }

            _selectedAccountId = accountId;
            PopulateGrid();
            UpdateAll("已切换会话标签。");
        }

        private uint GetStatusColor(string status)
        {
            switch (status)
            {
                case "运行中":
                    return Palette.Success;
                case "异常":
                    return Palette.Danger;
                case "登录中":
                    return Palette.Warning;
                default:
                    return Palette.Primary;
            }
        }

        private uint GetStatusBadgeColor(string status)
        {
            switch (status)
            {
                case "运行中":
                    return Palette.Success;
                case "异常":
                    return Palette.Danger;
                case "登录中":
                    return Palette.Warning;
                default:
                    return Palette.Info;
            }
        }

        private uint GetTitleBarColor() => _darkModeEnabled ? EmojiWindowNative.ARGB(255, 17, 24, 39) : Palette.TitleBar;

        private uint GetPageBackgroundColor() => _darkModeEnabled ? EmojiWindowNative.ARGB(255, 18, 24, 36) : Palette.PageBackground;

        private uint GetSurfaceColor() => _darkModeEnabled ? EmojiWindowNative.ARGB(255, 28, 36, 52) : Palette.Surface;

        private uint GetSurfaceSoftColor() => _darkModeEnabled ? EmojiWindowNative.ARGB(255, 35, 45, 66) : Palette.SurfaceSoft;

        private uint GetSurfaceMutedColor() => _darkModeEnabled ? EmojiWindowNative.ARGB(255, 31, 43, 64) : Palette.SurfaceMuted;

        private uint GetPrimarySoftColor() => _darkModeEnabled ? EmojiWindowNative.ARGB(255, 32, 51, 86) : Palette.PrimarySoft;

        private uint GetSuccessSoftColor() => _darkModeEnabled ? EmojiWindowNative.ARGB(255, 28, 61, 47) : Palette.SuccessSoft;

        private uint GetDangerSoftColor() => _darkModeEnabled ? EmojiWindowNative.ARGB(255, 72, 39, 46) : Palette.DangerSoft;

        private uint GetTextColor() => _darkModeEnabled ? EmojiWindowNative.ARGB(255, 233, 240, 250) : Palette.Text;

        private uint GetMutedColor() => _darkModeEnabled ? EmojiWindowNative.ARGB(255, 154, 169, 190) : Palette.Muted;

        private uint GetBorderColor() => _darkModeEnabled ? EmojiWindowNative.ARGB(255, 61, 80, 112) : EmojiWindowNative.ARGB(255, 232, 238, 246);

        private uint GetBorderStrongColor() => _darkModeEnabled ? EmojiWindowNative.ARGB(255, 87, 110, 148) : EmojiWindowNative.ARGB(255, 223, 231, 242);

        private uint GetNeutralButtonColor() => _darkModeEnabled ? EmojiWindowNative.ARGB(255, 76, 89, 113) : EmojiWindowNative.ARGB(255, 144, 147, 153);

        private uint GetNeutralButtonHoverColor() => _darkModeEnabled ? EmojiWindowNative.ARGB(255, 92, 106, 132) : EmojiWindowNative.ARGB(255, 123, 126, 133);

        private uint GetToolbarColor() => _darkModeEnabled ? EmojiWindowNative.ARGB(255, 12, 26, 48) : Palette.BrowserHeader;

        private uint GetBrowserHostColor() => _darkModeEnabled ? EmojiWindowNative.ARGB(255, 8, 18, 34) : Palette.BrowserPlaceholder;

        private uint GetBrowserHeaderColor() => _darkModeEnabled ? EmojiWindowNative.ARGB(255, 12, 26, 48) : Palette.BrowserHeader;

        private uint GetBrowserCanvasColor() => _darkModeEnabled ? EmojiWindowNative.ARGB(255, 25, 36, 54) : Palette.BrowserCanvas;

        private void MoveWindow(IntPtr hwnd, int x, int y, int width, int height)
        {
            NativeMethods.MoveWindow(hwnd, x, y, width, height, true);
        }

        private void SetComboBoxBounds(IntPtr combo, int x, int y, int width, int height)
        {
            EmojiWindowNative.SetComboBoxBounds(combo, x, y, width, height);
        }

        private byte[] U(string text)
        {
            return EmojiWindowNative.ToUtf8(text);
        }

        private static class NativeMethods
        {
            [DllImport("user32.dll", SetLastError = true)]
            [return: MarshalAs(UnmanagedType.Bool)]
            public static extern bool MoveWindow(IntPtr hWnd, int x, int y, int nWidth, int nHeight, [MarshalAs(UnmanagedType.Bool)] bool bRepaint);
        }
    }
}
