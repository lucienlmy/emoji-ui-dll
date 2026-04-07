# -*- coding: utf-8 -*-
from __future__ import annotations

import ctypes
import sys
from ctypes import wintypes

import demo_all_components_tabs as base

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except OSError:
        pass
if hasattr(sys.stderr, "reconfigure"):
    try:
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except OSError:
        pass

HWND = wintypes.HWND
BOOL = wintypes.BOOL
UINT32 = wintypes.UINT

DLL = base.DLL
USER32 = base.USER32
STATE = base.STATE
KEEP = base.KEEP

SW_HIDE = 0
SW_SHOW = 5
WM_SETREDRAW = 0x000B
RDW_NOCHILDREN = 0x0040

WINDOW_W = 1820
WINDOW_H = 980
SIDEBAR_W = 292
CONTENT_X = 324
CONTENT_W = 1480
SHELL_TOP = 34
SHELL_BOTTOM_GAP = 64
HEADER_H = 88
STATUS_Y = 924

GROUPBOX_STYLE_OUTLINE = 0
GROUPBOX_STYLE_CARD = 1
GROUPBOX_STYLE_HEADER_BAR = 3

SCALE_NONE = 0
SCALE_STRETCH = 1
SCALE_FIT = 2
SCALE_CENTER = 3

POPUP_TOP = 0
POPUP_BOTTOM = 3
POPUP_LEFT = 6
POPUP_RIGHT = 9
TOOLTIP_THEME_DARK = 0
TOOLTIP_THEME_LIGHT = 1
TOOLTIP_THEME_CUSTOM = 2
TOOLTIP_TRIGGER_HOVER = 0
TOOLTIP_TRIGGER_CLICK = 1
NOTIFY_INFO = 0
NOTIFY_SUCCESS = 1
NOTIFY_WARNING = 2
NOTIFY_ERROR = 3

HOTKEY_CTRL = 1
HOTKEY_SHIFT = 2
HOTKEY_ALT = 4

DTP_YMD = 1
DTP_YMDHM = 3
DTP_YMDHMS = 4

THEME_PRIMARY = 0
THEME_SUCCESS = 1
THEME_WARNING = 2
THEME_DANGER = 3
THEME_INFO = 4
THEME_TEXT = 5
THEME_MUTED = 6
THEME_SUBTLE = 7
THEME_BORDER = 9
THEME_BORDER_LIGHT = 10
THEME_BORDER_SOFT = 11
THEME_BG = 13
THEME_SURFACE = 14
THEME_SURFACE_PRIMARY = 15
THEME_SURFACE_SUCCESS = 16
THEME_SURFACE_WARNING = 17
THEME_SURFACE_DANGER = 18
THEME_SURFACE_INFO = 19


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class RECT(ctypes.Structure):
    _fields_ = [
        ("left", ctypes.c_long),
        ("top", ctypes.c_long),
        ("right", ctypes.c_long),
        ("bottom", ctypes.c_long),
    ]


ENUM_CHILD_PROC = ctypes.WINFUNCTYPE(BOOL, HWND, wintypes.LPARAM)


LOCAL: dict[str, object] = {
    "sidebar": None,
    "nav_tree": None,
    "sidebar_title": None,
    "sidebar_desc": None,
    "header_title": None,
    "header_desc": None,
    "host": None,
    "pages": {},
    "built": set(),
    "current": "",
    "node_info": {},
    "page_nodes": {},
    "selected_nav_node": 0,
    "suppress_nav_once": 0,
    "theme_labels": [],
}


CATEGORY_TREE: list[dict[str, object]] = [
    {
        "title": "基础组件",
        "icon": "🧱",
        "page": "overview_basic",
        "desc": "基础组件包含窗口、按钮、文本输入、状态选择和基础容器。",
        "children": [
            ("窗口 EmojiWindow", "🪟", "page_window", "窗口主题切换、背景颜色和状态读取。"),
            ("按钮 EmojiButton", "🔘", "page_button", "按钮类型、样式、尺寸、圆角、圆形和 Loading 状态。"),
            ("标签 Label", "🏷️", "page_label", "标签文本、前景色、背景色和对齐展示。"),
            ("编辑框 EditBox", "⌨️", "page_editbox", "普通编辑框的输入展示与说明信息。"),
            ("彩色 Emoji 编辑框", "🌈", "page_color_emoji_edit", "ColorEmojiEditBox 的 emoji 文本和展示说明。"),
            ("复选框 CheckBox", "☑️", "page_checkbox", "CheckBox 更多样式、状态读取与属性设置。"),
            ("单选框 RadioButton", "🔘", "page_radiobutton", "RadioButton 更多样式、状态读取与属性设置。"),
            ("进度条 ProgressBar", "📊", "page_progressbar", "ProgressBar 数值读写、颜色、显示和布局控制。"),
            ("滑块 Slider", "🎚️", "page_slider", "Slider 数值、范围、步长、颜色和布局控制。"),
            ("开关 Switch", "🔀", "page_switch", "Switch 更多样式、状态读取与属性设置。"),
            ("分组框 GroupBox", "🗂️", "page_groupbox", "GroupBox 的 Outline、Card、Header Bar 三种样式。"),
            ("面板 Panel", "🧩", "page_panel_demo", "Panel 作为背景容器和布局分区的用法。"),
        ],
    },
    {
        "title": "选择类组件",
        "icon": "🎛️",
        "page": "overview_select",
        "desc": "选择类组件按列表、组合框、日期时间和热键分开展示。",
        "children": [
            ("列表框 ListBox", "📋", "page_listbox", "ListBox 项目列表、程序选择和回调。"),
            ("组合框 ComboBox", "📑", "page_combobox", "普通 ComboBox 的只读/可编辑模式。"),
            ("D2D 组合框", "🫧", "page_d2d_combobox", "D2DComboBox 的样式和选择回调。"),
            ("日期时间选择框", "📅", "page_datetime", "D2DDateTimePicker 日期时间写入和读取。"),
            ("热键框 HotKeyControl", "⌨️", "page_hotkey", "热键录入、预设、清空、读取和颜色设置。"),
        ],
    },
    {
        "title": "显示类组件",
        "icon": "🖼️",
        "page": "overview_display",
        "desc": "显示类组件包括 PictureBox、Tooltip 和 Notification。",
        "children": [
            ("图片框 PictureBox", "🖼️", "page_picturebox", "缩放模式、透明度和背景色。"),
            ("文字提示 Tooltip", "💬", "page_tooltip", "四个方向、三种主题、hover/click 触发。"),
            ("通知 Notification", "🔔", "page_notification", "在软件窗口右上角弹出的通知。"),
        ],
    },
    {
        "title": "弹窗类组件",
        "icon": "🪄",
        "page": "overview_popup",
        "desc": "弹窗类组件单独提供 MessageBox 与 ConfirmBox 触发页。",
        "children": [
            ("消息框 MessageBox", "📝", "page_messagebox", "调用 show_message_box_bytes 的消息提示。"),
            ("确认框 ConfirmBox", "❓", "page_confirmbox", "调用 show_confirm_box_bytes 的确认提示和回调。"),
        ],
    },
    {
        "title": "页签与导航",
        "icon": "🧭",
        "page": "overview_nav",
        "desc": "页签导航保留成熟的综合页，集中展示复杂交互。",
        "children": [
            ("页签控件 TabControl", "🗂️", "page_tabcontrol", "页签样式、关闭按钮、关闭回调与读取示例。"),
            ("树形框 TreeView", "🌲", "page_treeview", "树形框样式、侧栏模式、多级节点和回调。"),
            ("菜单栏 MenuBar", "📁", "page_menubar", "一级/二级菜单和回调。"),
            ("弹出菜单 EmojiPopupMenu", "🧷", "page_popupmenu", "右键菜单、二级菜单和句柄绑定。"),
        ],
    },
    {
        "title": "数据组件",
        "icon": "🧾",
        "page": "overview_data",
        "desc": "数据组件当前重点是 DataGridView 综合演示页。",
        "children": [
            ("表格 DataGridView", "📊", "page_datagrid", "普通模式、虚拟模式、回调和对齐设置。"),
        ],
    },
]


def bind_extra_apis() -> None:
    hotkey_cb = getattr(DLL, "_HotKeyCB", None)
    if hotkey_cb is None:
        hotkey_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int, ctypes.c_int)
        DLL._HotKeyCB = hotkey_cb
    grid_sel_cb = getattr(DLL, "_GridSelCB", None)
    if grid_sel_cb is None:
        grid_sel_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int, ctypes.c_int)
        DLL._GridSelCB = grid_sel_cb
    grid_header_cb = getattr(DLL, "_GridHeaderCB", None)
    if grid_header_cb is None:
        grid_header_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int)
        DLL._GridHeaderCB = grid_header_cb
    value_cb = getattr(DLL, "_ValueCB", None)
    if value_cb is None:
        value_cb = ctypes.WINFUNCTYPE(None, HWND)
        DLL._ValueCB = value_cb
    double_click_cb = getattr(DLL, "_DoubleClickCB", None)
    if double_click_cb is None:
        double_click_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int, ctypes.c_int)
        DLL._DoubleClickCB = double_click_cb
    key_event_cb = getattr(DLL, "_KeyEventCB", None)
    if key_event_cb is None:
        key_event_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
        DLL._KeyEventCB = key_event_cb
    char_cb = getattr(DLL, "_CharCB", None)
    if char_cb is None:
        char_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int)
        DLL._CharCB = char_cb

    USER32.GetFocus.argtypes = []
    USER32.GetFocus.restype = HWND
    USER32.SetFocus.argtypes = [HWND]
    USER32.SetFocus.restype = HWND
    DLL.DestroyMenuBar.argtypes = [HWND]
    DLL.MenuBarUpdateSubItemText.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.MenuBarUpdateSubItemText.restype = BOOL
    DLL.LoadImageFromFile.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.LoadImageFromFile.restype = BOOL
    DLL.ClearImage.argtypes = [HWND]
    DLL.EnablePictureBox.argtypes = [HWND, BOOL]
    DLL.ShowPictureBox.argtypes = [HWND, BOOL]
    DLL.SetPictureBoxBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.SetPictureBoxScaleMode.argtypes = [HWND, ctypes.c_int]
    DLL.SetPictureBoxBackgroundColor.argtypes = [HWND, UINT32]
    DLL.SetImageOpacity.argtypes = [HWND, ctypes.c_float]
    DLL.SetMouseEnterCallback.argtypes = [HWND, value_cb]
    DLL.SetMouseLeaveCallback.argtypes = [HWND, value_cb]
    DLL.SetDoubleClickCallback.argtypes = [HWND, double_click_cb]
    DLL.SetFocusCallback.argtypes = [HWND, value_cb]
    DLL.SetBlurCallback.argtypes = [HWND, value_cb]
    DLL.SetKeyDownCallback.argtypes = [HWND, key_event_cb]
    DLL.SetKeyUpCallback.argtypes = [HWND, key_event_cb]
    DLL.SetCharCallback.argtypes = [HWND, char_cb]
    DLL.SetValueChangedCallback.argtypes = [HWND, value_cb]
    DLL.GetButtonText.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.GetButtonText.restype = ctypes.c_int
    DLL.SetButtonText.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.GetButtonEmoji.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.GetButtonEmoji.restype = ctypes.c_int
    DLL.SetButtonEmoji.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.GetButtonBounds.argtypes = [ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
    DLL.GetButtonBounds.restype = ctypes.c_int
    DLL.SetButtonBounds.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.GetButtonBackgroundColor.argtypes = [ctypes.c_int]
    DLL.GetButtonBackgroundColor.restype = UINT32
    DLL.SetButtonBackgroundColor.argtypes = [ctypes.c_int, UINT32]
    DLL.GetButtonTextColor.argtypes = [ctypes.c_int]
    DLL.GetButtonTextColor.restype = UINT32
    DLL.SetButtonTextColor.argtypes = [ctypes.c_int, UINT32]
    DLL.GetButtonBorderColor.argtypes = [ctypes.c_int]
    DLL.GetButtonBorderColor.restype = UINT32
    DLL.SetButtonBorderColor.argtypes = [ctypes.c_int, UINT32]
    DLL.GetButtonHoverColors.argtypes = [ctypes.c_int, ctypes.POINTER(UINT32), ctypes.POINTER(UINT32), ctypes.POINTER(UINT32)]
    DLL.GetButtonHoverColors.restype = ctypes.c_int
    DLL.ResetButtonColorOverrides.argtypes = [ctypes.c_int]
    DLL.GetButtonType.argtypes = [ctypes.c_int]
    DLL.GetButtonType.restype = ctypes.c_int
    DLL.GetButtonStyle.argtypes = [ctypes.c_int]
    DLL.GetButtonStyle.restype = ctypes.c_int
    DLL.GetButtonSize.argtypes = [ctypes.c_int]
    DLL.GetButtonSize.restype = ctypes.c_int
    DLL.GetButtonRound.argtypes = [ctypes.c_int]
    DLL.GetButtonRound.restype = BOOL
    DLL.GetButtonCircle.argtypes = [ctypes.c_int]
    DLL.GetButtonCircle.restype = BOOL
    DLL.GetButtonLoading.argtypes = [ctypes.c_int]
    DLL.GetButtonLoading.restype = BOOL
    DLL.GetButtonVisible.argtypes = [ctypes.c_int]
    DLL.GetButtonVisible.restype = BOOL
    DLL.ShowButton.argtypes = [ctypes.c_int, BOOL]
    DLL.GetButtonEnabled.argtypes = [ctypes.c_int]
    DLL.GetButtonEnabled.restype = BOOL
    DLL.EnableButton.argtypes = [HWND, ctypes.c_int, BOOL]

    DLL.GetWindowTitle.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.GetWindowTitle.restype = ctypes.c_int
    DLL.GetWindowBounds.argtypes = [HWND, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
    DLL.GetWindowBounds.restype = ctypes.c_int
    DLL.SetWindowBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.GetWindowVisible.argtypes = [HWND]
    DLL.GetWindowVisible.restype = ctypes.c_int
    DLL.GetWindowTitlebarColor.argtypes = [HWND]
    DLL.GetWindowTitlebarColor.restype = UINT32
    DLL.SetTitleBarTextColor.argtypes = [HWND, UINT32]
    DLL.SetTitleBarTextColor.restype = ctypes.c_int
    DLL.GetTitleBarTextColor.argtypes = [HWND]
    DLL.GetTitleBarTextColor.restype = UINT32
    DLL.set_window_title.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.set_window_titlebar_color.argtypes = [HWND, UINT32]
    DLL.SetWindowBackgroundColor.argtypes = [HWND, UINT32]
    DLL.ShowEmojiWindow.argtypes = [HWND, ctypes.c_int]
    DLL.SetPanelBackgroundColor.argtypes = [HWND, UINT32]
    DLL.GetPanelBackgroundColor.argtypes = [HWND, ctypes.POINTER(UINT32)]
    DLL.GetPanelBackgroundColor.restype = ctypes.c_int
    DLL.SetTreeViewBackgroundColor.argtypes = [HWND, UINT32]
    DLL.GetTreeViewBackgroundColor.argtypes = [HWND]
    DLL.GetTreeViewBackgroundColor.restype = UINT32
    DLL.SetLabelFont.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, BOOL, BOOL, BOOL]
    DLL.SetLabelBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.EnableLabel.argtypes = [HWND, BOOL]
    DLL.ShowLabel.argtypes = [HWND, BOOL]
    DLL.GetLabelText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.GetLabelText.restype = ctypes.c_int
    DLL.GetLabelFont.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
    DLL.GetLabelFont.restype = ctypes.c_int
    DLL.GetLabelColor.argtypes = [HWND, ctypes.POINTER(UINT32), ctypes.POINTER(UINT32)]
    DLL.GetLabelColor.restype = ctypes.c_int
    DLL.GetLabelBounds.argtypes = [HWND, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
    DLL.GetLabelBounds.restype = ctypes.c_int
    DLL.GetLabelAlignment.argtypes = [HWND]
    DLL.GetLabelAlignment.restype = ctypes.c_int
    DLL.SetLabelAlignment.argtypes = [HWND, ctypes.c_int]
    DLL.GetLabelEnabled.argtypes = [HWND]
    DLL.GetLabelEnabled.restype = ctypes.c_int
    DLL.GetLabelVisible.argtypes = [HWND]
    DLL.GetLabelVisible.restype = ctypes.c_int

    DLL.GetEditBoxText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.GetEditBoxText.restype = ctypes.c_int
    DLL.SetEditBoxText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.SetEditBoxFont.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, BOOL, BOOL, BOOL]
    DLL.SetEditBoxColor.argtypes = [HWND, UINT32, UINT32]
    DLL.SetEditBoxBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.EnableEditBox.argtypes = [HWND, BOOL]
    DLL.ShowEditBox.argtypes = [HWND, BOOL]
    DLL.GetEditBoxFont.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
    DLL.GetEditBoxFont.restype = ctypes.c_int
    DLL.GetEditBoxColor.argtypes = [HWND, ctypes.POINTER(UINT32), ctypes.POINTER(UINT32)]
    DLL.GetEditBoxColor.restype = ctypes.c_int
    DLL.GetEditBoxBounds.argtypes = [HWND, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
    DLL.GetEditBoxBounds.restype = ctypes.c_int
    DLL.GetEditBoxAlignment.argtypes = [HWND]
    DLL.GetEditBoxAlignment.restype = ctypes.c_int
    DLL.SetEditBoxAlignment.argtypes = [HWND, ctypes.c_int]
    DLL.GetEditBoxEnabled.argtypes = [HWND]
    DLL.GetEditBoxEnabled.restype = ctypes.c_int
    DLL.GetEditBoxVisible.argtypes = [HWND]
    DLL.GetEditBoxVisible.restype = ctypes.c_int
    DLL.GetCheckBoxText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.GetCheckBoxText.restype = ctypes.c_int
    DLL.SetCheckBoxText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.SetCheckBoxBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.EnableCheckBox.argtypes = [HWND, BOOL]
    DLL.ShowCheckBox.argtypes = [HWND, BOOL]
    DLL.SetCheckBoxColor.argtypes = [HWND, UINT32, UINT32]
    DLL.SetCheckBoxCheckColor.argtypes = [HWND, UINT32]
    DLL.GetCheckBoxCheckColor.argtypes = [HWND, ctypes.POINTER(UINT32)]
    DLL.GetCheckBoxCheckColor.restype = ctypes.c_int
    DLL.SetCheckBoxStyle.argtypes = [HWND, ctypes.c_int]
    DLL.GetCheckBoxStyle.argtypes = [HWND]
    DLL.GetCheckBoxStyle.restype = ctypes.c_int
    DLL.GetCheckBoxColor.argtypes = [HWND, ctypes.POINTER(UINT32), ctypes.POINTER(UINT32)]
    DLL.GetCheckBoxColor.restype = ctypes.c_int
    DLL.GetRadioButtonText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.GetRadioButtonText.restype = ctypes.c_int
    DLL.GetRadioButtonState.argtypes = [HWND]
    DLL.GetRadioButtonState.restype = BOOL
    DLL.SetRadioButtonState.argtypes = [HWND, BOOL]
    DLL.SetRadioButtonText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.SetRadioButtonBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.EnableRadioButton.argtypes = [HWND, BOOL]
    DLL.ShowRadioButton.argtypes = [HWND, BOOL]
    DLL.SetRadioButtonColor.argtypes = [HWND, UINT32, UINT32]
    DLL.GetRadioButtonColor.argtypes = [HWND, ctypes.POINTER(UINT32), ctypes.POINTER(UINT32)]
    DLL.GetRadioButtonColor.restype = ctypes.c_int
    DLL.SetRadioButtonDotColor.argtypes = [HWND, UINT32]
    DLL.GetRadioButtonDotColor.argtypes = [HWND, ctypes.POINTER(UINT32)]
    DLL.GetRadioButtonDotColor.restype = ctypes.c_int
    DLL.SetRadioButtonStyle.argtypes = [HWND, ctypes.c_int]
    DLL.GetRadioButtonStyle.argtypes = [HWND]
    DLL.GetRadioButtonStyle.restype = ctypes.c_int
    DLL.SetProgressIndeterminate.argtypes = [HWND, BOOL]
    DLL.SetProgressBarColor.argtypes = [HWND, UINT32, UINT32]
    DLL.EnableProgressBar.argtypes = [HWND, BOOL]
    DLL.ShowProgressBar.argtypes = [HWND, BOOL]
    DLL.SetProgressBarBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.GetProgressBarColor.argtypes = [HWND, ctypes.POINTER(UINT32), ctypes.POINTER(UINT32)]
    DLL.GetProgressBarColor.restype = ctypes.c_int
    DLL.GetProgressBarBounds.argtypes = [HWND, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
    DLL.GetProgressBarBounds.restype = ctypes.c_int
    DLL.GetProgressBarEnabled.argtypes = [HWND]
    DLL.GetProgressBarEnabled.restype = ctypes.c_int
    DLL.GetProgressBarVisible.argtypes = [HWND]
    DLL.GetProgressBarVisible.restype = ctypes.c_int
    DLL.GetProgressBarShowText.argtypes = [HWND]
    DLL.GetProgressBarShowText.restype = ctypes.c_int
    DLL.SetSliderColors.argtypes = [HWND, UINT32, UINT32, UINT32]
    DLL.GetSliderColors.argtypes = [HWND, ctypes.POINTER(UINT32), ctypes.POINTER(UINT32), ctypes.POINTER(UINT32)]
    DLL.GetSliderColors.restype = ctypes.c_int
    DLL.EnableSlider.argtypes = [HWND, BOOL]
    DLL.ShowSlider.argtypes = [HWND, BOOL]
    DLL.SetSliderBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.SetSwitchTextColors.argtypes = [HWND, UINT32, UINT32]
    DLL.GetSwitchColors.argtypes = [HWND, ctypes.POINTER(UINT32), ctypes.POINTER(UINT32), ctypes.POINTER(UINT32), ctypes.POINTER(UINT32)]
    DLL.GetSwitchColors.restype = ctypes.c_int
    DLL.EnableSwitch.argtypes = [HWND, BOOL]
    DLL.ShowSwitch.argtypes = [HWND, BOOL]
    DLL.SetSwitchBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.GetD2DEditBoxText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.GetD2DEditBoxText.restype = ctypes.c_int
    DLL.SetD2DEditBoxText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.SetD2DEditBoxFont.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, BOOL, BOOL, BOOL]
    DLL.SetD2DEditBoxBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.EnableD2DEditBox.argtypes = [HWND, BOOL]
    DLL.ShowD2DEditBox.argtypes = [HWND, BOOL]
    DLL.RemoveListItem.argtypes = [HWND, ctypes.c_int]
    DLL.ClearListBox.argtypes = [HWND]
    DLL.GetSelectedIndex.argtypes = [HWND]
    DLL.GetSelectedIndex.restype = ctypes.c_int
    DLL.GetListItemCount.argtypes = [HWND]
    DLL.GetListItemCount.restype = ctypes.c_int
    DLL.EnableListBox.argtypes = [HWND, BOOL]
    DLL.ShowListBox.argtypes = [HWND, BOOL]
    DLL.SetListBoxBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.SetListBoxColors.argtypes = [HWND, UINT32, UINT32, UINT32, UINT32]
    DLL.GetListBoxColors.argtypes = [HWND, ctypes.POINTER(UINT32), ctypes.POINTER(UINT32), ctypes.POINTER(UINT32), ctypes.POINTER(UINT32)]
    DLL.GetListBoxColors.restype = ctypes.c_int
    DLL.SetListItemText.argtypes = [HWND, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.SetListItemText.restype = BOOL

    DLL.RemoveComboItem.argtypes = [HWND, ctypes.c_int]
    DLL.ClearComboBox.argtypes = [HWND]
    DLL.GetComboSelectedIndex.argtypes = [HWND]
    DLL.GetComboSelectedIndex.restype = ctypes.c_int
    DLL.GetComboItemCount.argtypes = [HWND]
    DLL.GetComboItemCount.restype = ctypes.c_int
    DLL.GetComboItemText.argtypes = [HWND, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.GetComboItemText.restype = ctypes.c_int
    DLL.EnableComboBox.argtypes = [HWND, BOOL]
    DLL.ShowComboBox.argtypes = [HWND, BOOL]
    DLL.SetComboBoxBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.GetComboBoxText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.GetComboBoxText.restype = ctypes.c_int
    DLL.SetComboBoxText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.SetComboBoxColors.argtypes = [HWND, UINT32, UINT32, UINT32, UINT32]
    DLL.GetComboBoxColors.argtypes = [HWND, ctypes.POINTER(UINT32), ctypes.POINTER(UINT32), ctypes.POINTER(UINT32), ctypes.POINTER(UINT32)]
    DLL.GetComboBoxColors.restype = ctypes.c_int

    DLL.RemoveD2DComboItem.argtypes = [HWND, ctypes.c_int]
    DLL.ClearD2DComboBox.argtypes = [HWND]
    DLL.GetD2DComboSelectedIndex.argtypes = [HWND]
    DLL.GetD2DComboSelectedIndex.restype = ctypes.c_int
    DLL.GetD2DComboItemCount.argtypes = [HWND]
    DLL.GetD2DComboItemCount.restype = ctypes.c_int
    DLL.GetD2DComboItemText.argtypes = [HWND, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.GetD2DComboItemText.restype = ctypes.c_int
    DLL.GetD2DComboText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.GetD2DComboText.restype = ctypes.c_int
    DLL.GetD2DComboSelectedText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.GetD2DComboSelectedText.restype = ctypes.c_int
    DLL.SetD2DComboText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.EnableD2DComboBox.argtypes = [HWND, BOOL]
    DLL.ShowD2DComboBox.argtypes = [HWND, BOOL]
    DLL.SetD2DComboBoxBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.SetD2DComboBoxColors.argtypes = [HWND, UINT32, UINT32, UINT32, UINT32, UINT32, UINT32]
    DLL.GetD2DComboBoxColors.argtypes = [HWND, ctypes.POINTER(UINT32), ctypes.POINTER(UINT32), ctypes.POINTER(UINT32), ctypes.POINTER(UINT32), ctypes.POINTER(UINT32), ctypes.POINTER(UINT32)]
    DLL.GetD2DComboBoxColors.restype = ctypes.c_int

    DLL.GetD2DDateTimePickerPrecision.argtypes = [HWND]
    DLL.GetD2DDateTimePickerPrecision.restype = ctypes.c_int
    DLL.SetD2DDateTimePickerPrecision.argtypes = [HWND, ctypes.c_int]
    DLL.EnableD2DDateTimePicker.argtypes = [HWND, BOOL]
    DLL.ShowD2DDateTimePicker.argtypes = [HWND, BOOL]
    DLL.SetD2DDateTimePickerBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.SetD2DDateTimePickerColors.argtypes = [HWND, UINT32, UINT32, UINT32]
    DLL.GetD2DDateTimePickerColors.argtypes = [HWND, ctypes.POINTER(UINT32), ctypes.POINTER(UINT32), ctypes.POINTER(UINT32)]
    DLL.GetD2DDateTimePickerColors.restype = ctypes.c_int

    DLL.CreateHotKeyControl.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, UINT32, UINT32]
    DLL.CreateHotKeyControl.restype = HWND
    DLL.GetHotKey.argtypes = [HWND, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
    DLL.SetHotKey.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
    DLL.ClearHotKey.argtypes = [HWND]
    DLL.SetHotKeyCallback.argtypes = [HWND, hotkey_cb]
    DLL.EnableHotKeyControl.argtypes = [HWND, BOOL]
    DLL.ShowHotKeyControl.argtypes = [HWND, BOOL]
    DLL.SetHotKeyControlBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.SetHotKeyColors.argtypes = [HWND, UINT32, UINT32, UINT32]
    DLL.GetHotKeyColors.argtypes = [HWND, ctypes.POINTER(UINT32), ctypes.POINTER(UINT32), ctypes.POINTER(UINT32)]
    DLL.GetHotKeyColors.restype = ctypes.c_int

    DLL.DataGrid_ClearColumns.argtypes = [HWND]
    DLL.DataGrid_AddButtonColumn.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_AddLinkColumn.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_AddImageColumn.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_GetColumnCount.argtypes = [HWND]
    DLL.DataGrid_GetColumnCount.restype = ctypes.c_int
    DLL.DataGrid_GetRowCount.argtypes = [HWND]
    DLL.DataGrid_GetRowCount.restype = ctypes.c_int
    DLL.DataGrid_SetColumnHeaderText.argtypes = [HWND, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.DataGrid_GetColumnHeaderText.argtypes = [HWND, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.DataGrid_GetColumnHeaderText.restype = ctypes.c_int
    DLL.DataGrid_GetCellText.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.DataGrid_GetCellText.restype = ctypes.c_int
    DLL.DataGrid_SetCellImageFromFile.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.DataGrid_SetCellImageFromFile.restype = BOOL
    DLL.DataGrid_SetCellImageFromMemory.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.DataGrid_SetCellImageFromMemory.restype = BOOL
    DLL.DataGrid_ClearCellImage.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_GetCellChecked.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_GetCellChecked.restype = BOOL
    DLL.DataGrid_GetSelectedRow.argtypes = [HWND]
    DLL.DataGrid_GetSelectedRow.restype = ctypes.c_int
    DLL.DataGrid_GetSelectedCol.argtypes = [HWND]
    DLL.DataGrid_GetSelectedCol.restype = ctypes.c_int
    DLL.DataGrid_SetSelectedCell.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_SetColumnHeaderAlignment.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_SetColumnCellAlignment.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_SortByColumn.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_SetHeaderMultiline.argtypes = [HWND, BOOL]
    DLL.DataGrid_SetColors.argtypes = [HWND, UINT32, UINT32, UINT32, UINT32, UINT32, UINT32, UINT32]
    DLL.DataGrid_GetColors.argtypes = [HWND, ctypes.POINTER(UINT32), ctypes.POINTER(UINT32), ctypes.POINTER(UINT32), ctypes.POINTER(UINT32), ctypes.POINTER(UINT32), ctypes.POINTER(UINT32), ctypes.POINTER(UINT32)]
    DLL.DataGrid_GetColors.restype = ctypes.c_int
    DLL.DataGrid_SetColumnHeaderClickCallback.argtypes = [HWND, grid_header_cb]
    DLL.DataGrid_SetSelectionChangedCallback.argtypes = [HWND, grid_sel_cb]
    DLL.DataGrid_ExportCSV.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.DataGrid_ExportCSV.restype = BOOL

    USER32.ShowWindow.argtypes = [HWND, ctypes.c_int]
    USER32.ShowWindow.restype = BOOL
USER32.MoveWindow.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, BOOL]
USER32.MoveWindow.restype = BOOL
USER32.EnumChildWindows.argtypes = [HWND, ENUM_CHILD_PROC, wintypes.LPARAM]
USER32.EnumChildWindows.restype = BOOL
USER32.IsWindowVisible.argtypes = [HWND]
USER32.IsWindowVisible.restype = BOOL
USER32.SendMessageW.argtypes = [HWND, ctypes.c_uint, wintypes.WPARAM, wintypes.LPARAM]
USER32.SendMessageW.restype = ctypes.c_ssize_t


def s(text: str):
    return base.s(text)


def show_hwnd(hwnd: HWND | None, visible: bool) -> None:
    if hwnd:
        USER32.ShowWindow(hwnd, SW_SHOW if visible else SW_HIDE)


def set_window_redraw(hwnd: HWND | None, enabled: bool) -> None:
    if hwnd:
        USER32.SendMessageW(hwnd, WM_SETREDRAW, wintypes.WPARAM(1 if enabled else 0), 0)


def force_redraw(hwnd: HWND | None, *, sync: bool = False) -> None:
    if hwnd:
        flags = base.RDW_INVALIDATE | base.RDW_FRAME | RDW_NOCHILDREN
        if sync:
            flags |= base.RDW_UPDATENOW
        USER32.RedrawWindow(
            hwnd,
            None,
            None,
            flags,
        )


def invalidate_visible_tree(hwnd: HWND | None, *, sync_root: bool = True) -> None:
    if not hwnd:
        return
    force_redraw(hwnd, sync=sync_root)
    visible_children: list[HWND] = []

    @ENUM_CHILD_PROC
    def collect(child: HWND, _lparam) -> BOOL:
        if USER32.IsWindowVisible(child):
            visible_children.append(child)
        return True

    USER32.EnumChildWindows(hwnd, collect, 0)
    for child in visible_children:
        force_redraw(child)


def set_shell_redraw(enabled: bool) -> None:
    pages: dict[str, HWND] = LOCAL["pages"]  # type: ignore[assignment]
    current = str(LOCAL.get("current") or "")
    targets: list[HWND | None] = [
        STATE.get("hwnd"),
        LOCAL.get("sidebar"),
        LOCAL.get("nav_tree"),
        LOCAL.get("host"),
        STATE.get("status"),
    ]
    if current in pages:
        targets.append(pages[current])

    seen: set[int] = set()
    for hwnd in targets:
        key = base.hwnd_key(hwnd)
        if key == 0 or key in seen:
            continue
        seen.add(key)
        set_window_redraw(hwnd, enabled)


def refresh_visible_shell() -> None:
    invalidate_visible_tree(LOCAL.get("sidebar"))
    invalidate_visible_tree(LOCAL.get("host"))
    force_redraw(STATE.get("status"))
    force_redraw(STATE.get("hwnd"))


def refresh_theme_visuals(*, refresh_now: bool = True) -> None:
    apply_shell_theme()
    apply_registered_theme_labels()
    for key in ("nested_tab", "tab_style_demo", "tab_style_secondary"):
        h_tab = base.STATE.get(key)
        if h_tab and USER32.IsWindowVisible(h_tab):
            DLL.UpdateTabControlLayout(h_tab)
            DLL.RedrawTabControl(h_tab)
    if refresh_now:
        refresh_visible_shell()


def apply_shell_theme() -> None:
    palette = page_palette()
    dark = is_dark_theme()
    sidebar = LOCAL.get("sidebar")
    host = LOCAL.get("host")
    nav_tree = LOCAL.get("nav_tree")
    pages: dict[str, HWND] = LOCAL["pages"]  # type: ignore[assignment]

    sidebar_bg = 0xFF161718 if dark else 0xFFFFFFFF
    host_bg = palette["page_bg"]
    sidebar_text = 0xFFF3F5F7 if dark else 0xFF303133
    sidebar_muted = 0xFF9CA3AF if dark else 0xFF909399

    if sidebar:
        DLL.SetPanelBackgroundColor(sidebar, sidebar_bg)
    if host:
        DLL.SetPanelBackgroundColor(host, host_bg)
    for page in pages.values():
        DLL.SetPanelBackgroundColor(page, host_bg)

    if nav_tree:
        DLL.SetTreeViewBackgroundColor(nav_tree, 0xFF1D1E20 if dark else 0xFFFFFFFF)
        DLL.SetTreeViewTextColor(nav_tree, sidebar_text)
        DLL.SetTreeViewSelectedBgColor(nav_tree, 0xFF409EFF)
        DLL.SetTreeViewSelectedForeColor(nav_tree, 0xFFFFFFFF)
        DLL.SetTreeViewHoverBgColor(nav_tree, 0xFF2B2F36 if dark else 0xFFEAF3FF)

    if LOCAL.get("sidebar_title"):
        DLL.SetLabelColor(LOCAL["sidebar_title"], sidebar_text, sidebar_bg)
    if LOCAL.get("sidebar_desc"):
        DLL.SetLabelColor(LOCAL["sidebar_desc"], sidebar_muted, sidebar_bg)
    if LOCAL.get("header_title"):
        DLL.SetLabelColor(LOCAL["header_title"], palette["text"], host_bg)
    if LOCAL.get("header_desc"):
        DLL.SetLabelColor(LOCAL["header_desc"], palette["muted"], host_bg)
    if STATE.get("status"):
        DLL.SetLabelColor(STATE["status"], palette["muted"], host_bg)


def relayout_shell(width: int, height: int, *, refresh_now: bool = True) -> None:
    sidebar = LOCAL.get("sidebar")
    nav_tree = LOCAL.get("nav_tree")
    host = LOCAL.get("host")
    pages: dict[str, HWND] = LOCAL["pages"]  # type: ignore[assignment]
    status = STATE.get("status")
    hwnd = STATE.get("hwnd")

    content_h = max(760, height - SHELL_TOP - SHELL_BOTTOM_GAP)
    page_h = max(640, content_h - HEADER_H)
    status_y = max(16, height - 56)
    status_w = max(240, width - 40)
    host_w = max(1120, width - CONTENT_X - 16)
    tree_h = max(420, content_h - 80)

    if sidebar:
        USER32.MoveWindow(sidebar, 16, SHELL_TOP, SIDEBAR_W, content_h, False)
    if nav_tree:
        USER32.MoveWindow(nav_tree, 16, 56, SIDEBAR_W - 32, tree_h, False)
    if host:
        USER32.MoveWindow(host, CONTENT_X, SHELL_TOP, host_w, content_h, False)
    if status:
        USER32.MoveWindow(status, 16, status_y, status_w, 28, False)
    for page in pages.values():
        USER32.MoveWindow(page, 0, HEADER_H, host_w, page_h, False)

    if refresh_now:
        refresh_visible_shell()


def page_panel(key: str) -> HWND:
    pages: dict[str, HWND] = LOCAL["pages"]  # type: ignore[assignment]
    if key in pages:
        return pages[key]
    host = LOCAL["host"]
    page = DLL.CreatePanel(host, 0, HEADER_H, CONTENT_W, 900 - HEADER_H, page_palette()["page_bg"])
    pages[key] = page
    show_hwnd(page, False)
    return page


def set_header(title: str, desc: str) -> None:
    base.set_label_text(LOCAL["header_title"], title)
    base.set_label_text(LOCAL["header_desc"], desc)


def is_dark_theme() -> bool:
    return bool(DLL.IsDarkMode())


def page_palette() -> dict[str, int]:
    dark = is_dark_theme()
    card_bg = int(base.theme_color("background_light"))
    text = int(base.theme_color("text_primary"))
    muted = int(base.theme_color("text_regular"))
    accent = int(base.theme_color("primary"))
    if dark:
        return {
            "page_bg": 0xFF1D1E1F,
            "card_bg": card_bg,
            "text": text,
            "muted": muted,
            "accent": accent,
        }
    return {
        "page_bg": 0xFFF5F7FA,
        "card_bg": card_bg,
        "text": text,
        "muted": muted,
        "accent": accent,
    }


def register_theme_label(h_label: HWND, role: str = "text", surface: str = "card") -> HWND:
    labels: list[tuple[HWND, str, str]] = LOCAL["theme_labels"]  # type: ignore[assignment]
    labels.append((h_label, role, surface))
    return h_label


def apply_registered_theme_labels() -> None:
    palette = page_palette()
    labels: list[tuple[HWND, str, str]] = LOCAL["theme_labels"]  # type: ignore[assignment]
    for h_label, role, surface in labels:
        fg = palette["accent"] if role == "accent" else (palette["muted"] if role == "muted" else palette["text"])
        bg = palette["page_bg"] if surface == "page" else palette["card_bg"]
        DLL.SetLabelColor(h_label, fg, bg)


def add_tree_root(h_tree: HWND, text: str, icon: str, page_key: str, desc: str) -> int:
    node_id = base.add_tree_root(h_tree, text, icon)
    LOCAL["node_info"][node_id] = (page_key, text, desc)  # type: ignore[index]
    page_nodes: dict[str, list[tuple[int, str]]] = LOCAL["page_nodes"]  # type: ignore[assignment]
    page_nodes.setdefault(page_key, []).append((node_id, text))
    return node_id


def add_tree_child(h_tree: HWND, parent_id: int, text: str, icon: str, page_key: str, desc: str) -> int:
    node_id = base.add_tree_child(h_tree, parent_id, text, icon)
    LOCAL["node_info"][node_id] = (page_key, text, desc)  # type: ignore[index]
    page_nodes: dict[str, list[tuple[int, str]]] = LOCAL["page_nodes"]  # type: ignore[assignment]
    page_nodes.setdefault(page_key, []).append((node_id, text))
    return node_id


def find_nav_node_for_page(page_key: str, title: str) -> int:
    page_nodes: dict[str, list[tuple[int, str]]] = LOCAL["page_nodes"]  # type: ignore[assignment]
    entries = page_nodes.get(page_key, [])
    for node_id, node_title in entries:
        if node_title == title:
            return node_id
    return entries[0][0] if entries else 0


def sync_nav_selection(page_key: str, title: str) -> None:
    nav_tree = LOCAL.get("nav_tree")
    if not nav_tree:
        return
    target_node = find_nav_node_for_page(page_key, title)
    if not target_node:
        return
    current_node = int(LOCAL.get("selected_nav_node") or 0)
    if current_node == target_node:
        return
    LOCAL["suppress_nav_once"] = target_node
    LOCAL["selected_nav_node"] = target_node
    DLL.SetSelectedNode(nav_tree, target_node)





def hotkey_text(vk_code: int, modifiers: int) -> str:
    if vk_code == 0:
        return "未设置"
    parts: list[str] = []
    if modifiers & HOTKEY_CTRL:
        parts.append("Ctrl")
    if modifiers & HOTKEY_SHIFT:
        parts.append("Shift")
    if modifiers & HOTKEY_ALT:
        parts.append("Alt")
    if 65 <= vk_code <= 90 or 48 <= vk_code <= 57:
        key_name = chr(vk_code)
    elif 112 <= vk_code <= 123:
        key_name = f"F{vk_code - 111}"
    else:
        key_name = {
            13: "Enter",
            27: "Esc",
            32: "Space",
            9: "Tab",
            46: "Delete",
            45: "Insert",
            36: "Home",
            35: "End",
            33: "PageUp",
            34: "PageDown",
            37: "Left",
            38: "Up",
            39: "Right",
            40: "Down",
        }.get(vk_code, str(vk_code))
    parts.append(key_name)
    return "+".join(parts)


def build_overview(page: HWND, title: str, desc: str, items: list[str], api_text: str) -> None:
    base.groupbox(page, f"{title} 组件清单", 16, 16, 620, 420)
    for idx, item in enumerate(items):
        base.label(page, f"• {item}", 40, 58 + idx * 28, 540, 24, fg=0xFF303133, bg=0xFFF5F7FA, size=13)

    base.groupbox(page, "说明", 660, 16, 780, 160)
    base.label(page, desc, 684, 58, 730, 42, fg=0xFF606266, bg=0xFFF5F7FA, wrap=True)
    base.label(page, "左侧二级节点会切到该组件的详情页或成熟综合页。", 684, 114, 700, 24, fg=0xFF909399, bg=0xFFF5F7FA)

    base.groupbox(page, "本页重点", 660, 196, 780, 160)
    base.label(page, api_text, 684, 236, 730, 90, fg=0xFF606266, bg=0xFFF5F7FA, wrap=True)


def build_label_property_demo(page: HWND, title: str, x: int, y: int, w: int = 420, h: int = 176) -> HWND:
    palette = page_palette()
    base.groupbox(page, f"🏷️ {title}", x, y, w, h)
    demo = register_theme_label(
        base.label(page, "🌈 Unicode 彩色标签示例：😀 🚀 🎉 🧩", x + 24, y + 48, w - 48, 28, fg=palette["text"], bg=palette["card_bg"], size=14, bold=True),
        "text",
        "card",
    )
    info = register_theme_label(
        base.label(page, "当前状态：默认", x + 24, y + 128, w - 48, 24, fg=palette["muted"], bg=palette["card_bg"]),
        "muted",
        "card",
    )

    def apply_state(text: str, fg: int, bg: int, note: str) -> None:
        DLL.SetLabelText(demo, *s(text)[:2])
        DLL.SetLabelColor(demo, fg, bg)
        base.set_label_text(info, note)
        base.set_status(note)

    base.button(page, "📝", "改文本", x + 24, y + 82, 100, 34, 0xFF409EFF, lambda: apply_state("🪄 标签文字已改写：🍀 📦 ⭐", palette["text"], palette["card_bg"], f"{title} -> 文本已更新"))
    base.button(page, "🎨", "强调色", x + 136, y + 82, 100, 34, 0xFF67C23A, lambda: apply_state("💎 强调态标签：🔵 🟢 🟠 🔴", THEME_PRIMARY, THEME_SURFACE_PRIMARY, f"{title} -> 切到强调色"))
    base.button(page, "↺", "恢复", x + 248, y + 82, 100, 34, 0xFF909399, lambda: apply_state("🌈 Unicode 彩色标签示例：😀 🚀 🎉 🧩", page_palette()["text"], page_palette()["card_bg"], f"{title} -> 已恢复默认"))
    return demo


def build_state_strip(page: HWND, title: str, x: int, y: int, w: int = 1448) -> HWND:
    base.groupbox(page, title, x, y, w, 86)
    palette = page_palette()
    return register_theme_label(base.label(page, "等待读取状态。", x + 24, y + 42, w - 48, 24, fg=palette["muted"], bg=palette["card_bg"]), "muted", "card")


def create_content_host(page: HWND, top: int = 152) -> HWND:
    return DLL.CreatePanel(page, 16, top, 1448, 636, THEME_SURFACE)


def build_page_overview_basic(page: HWND) -> None:
    build_overview(
        page,
        "基础组件",
        "基础组件树形版已按按钮、文本、状态控件、容器拆开，便于大空间详细展示。",
        ["窗口", "按钮", "标签", "编辑框", "彩色 Emoji 编辑框", "复选框", "单选框", "进度条", "滑块", "开关", "分组框", "面板"],
        "重点接口: SetButtonType / SetButtonStyle / SetButtonLoading / SetLabelText / SetLabelColor / "
        "GetLabelFont / SetLabelFont / GetLabelBounds / SetLabelBounds / GetLabelAlignment / SetLabelAlignment / "
        "GetCheckBoxState / SetCheckBoxState / GetProgressValue / SetProgressValue / GetSliderValue / SetSliderValue / "
        "GetSwitchState / SetSwitchState。",
    )


def build_page_overview_select(page: HWND) -> None:
    build_overview(
        page,
        "选择类组件",
        "选择类组件拆成列表/组合框页与日期时间/热键页，避免所有内容挤在一个综合区。",
        ["列表框", "组合框", "D2D 组合框", "日期时间选择框", "热键框"],
        "重点接口: AddListItem / SetSelectedIndex / AddComboItem / SetComboSelectedIndex / "
        "AddD2DComboItem / SetD2DComboSelectedIndex / SetD2DDateTimePickerDateTime / GetD2DDateTimePickerDateTime / "
        "SetHotKey / GetHotKey / ClearHotKey / SetHotKeyColors。",
    )


def build_page_overview_display(page: HWND) -> None:
    build_overview(
        page,
        "显示类组件",
        "PictureBox、Tooltip、Notification 已拆成可单独验证的页面。",
        ["图片框", "Tooltip", "Notification"],
        "重点接口: SetPictureBoxScaleMode / SetPictureBoxBackgroundColor / SetImageOpacity / "
        "SetTooltipPlacement / SetTooltipTheme / SetTooltipTrigger / SetTooltipColors / SetTooltipFont / "
        "ShowNotification / SetNotificationCallback。",
    )


def build_page_overview_popup(page: HWND) -> None:
    build_overview(
        page,
        "弹窗类组件",
        "弹窗类组件单独保留基础消息框与确认框测试入口，便于快速验证回调。",
        ["MessageBox", "ConfirmBox"],
        "重点接口: show_message_box_bytes / show_confirm_box_bytes / Confirm 回调。",
    )


def build_page_overview_nav(page: HWND) -> None:
    build_overview(
        page,
        "页签与导航",
        "TabControl、TreeView、MenuBar、EmojiPopupMenu 继续复用当前最完整的综合演示页。",
        ["TabControl", "TreeView", "MenuBar", "EmojiPopupMenu"],
        "重点接口: SetTabClosable / SetTabCloseCallback / SetTabHeaderStyle / "
        "SetTreeViewSidebarMode / SetTreeViewRowHeight / SetTreeViewItemSpacing / SetMenuBarCallback / SetPopupMenuCallback。",
    )


def build_page_overview_data(page: HWND) -> None:
    build_overview(
        page,
        "数据组件",
        "数据组件保留成熟的 DataGridView 综合页，继续覆盖普通模式和虚拟模式。",
        ["DataGridView"],
        "重点接口: DataGrid_AddTextColumn / DataGrid_AddCheckBoxColumn / DataGrid_AddComboBoxColumn / "
        "DataGrid_SetCellText / DataGrid_SetVirtualRowCount / DataGrid_SetVirtualDataCallback。",
    )



def build_page_state(page: HWND) -> None:
    base.groupbox(page, "CheckBox / RadioButton", 16, 16, 700, 330)
    base.groupbox(page, "ProgressBar / Slider / Switch", 734, 16, 730, 330)
    out = base.label(page, "状态读取区。", 40, 374, 1320, 40, fg=0xFF606266, bg=0xFFF5F7FA, wrap=True)

    c1p, c1n, _ = s("☑️ 启用高级模式")
    c2p, c2n, _ = s("🧱 卡片样式")
    r1p, r1n, _ = s("🅰️ 方案 A")
    r2p, r2n, _ = s("🅱️ 方案 B")
    r3p, r3n, _ = s("🅲️ 按钮样式")

    cb1 = DLL.CreateCheckBox(page, 40, 90, 240, 34, c1p, c1n, BOOL(True), THEME_TEXT, THEME_BG, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    cb2 = DLL.CreateCheckBox(page, 40, 136, 240, 40, c2p, c2n, BOOL(False), THEME_TEXT, THEME_BG, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    DLL.SetCheckBoxStyle(cb2, 3)
    DLL.SetCheckBoxCheckColor(cb1, 0xFF409EFF)
    DLL.SetCheckBoxCheckColor(cb2, 0xFF67C23A)

    rb1 = DLL.CreateRadioButton(page, 340, 90, 130, 34, r1p, r1n, 99, BOOL(True), THEME_TEXT, THEME_BG, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    rb2 = DLL.CreateRadioButton(page, 480, 90, 130, 34, r2p, r2n, 99, BOOL(False), THEME_TEXT, THEME_BG, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    rb3 = DLL.CreateRadioButton(page, 340, 136, 150, 36, r3p, r3n, 99, BOOL(False), THEME_TEXT, THEME_BG, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    DLL.SetRadioButtonStyle(rb2, base.RADIO_STYLE_BORDER)
    DLL.SetRadioButtonStyle(rb3, base.RADIO_STYLE_BUTTON)
    DLL.SetRadioButtonDotColor(rb1, 0xFF409EFF)
    DLL.SetRadioButtonDotColor(rb2, 0xFFE6A23C)
    DLL.SetRadioButtonDotColor(rb3, 0xFF67C23A)

    prog = DLL.CreateProgressBar(page, 758, 90, 420, 28, 35, 0xFF409EFF, THEME_BORDER_LIGHT, BOOL(True), THEME_TEXT)
    DLL.SetProgressBarShowText(prog, BOOL(True))
    DLL.SetProgressBarTextColor(prog, THEME_TEXT)
    slider = DLL.CreateSlider(page, 758, 146, 260, 40, 0, 100, 36, 10, 0xFF409EFF, THEME_BORDER_LIGHT)
    DLL.SetSliderShowStops(slider, BOOL(True))
    on_p, on_n, _ = s("开")
    off_p, off_n, _ = s("关")
    switcher = DLL.CreateSwitch(page, 1048, 142, 88, 34, BOOL(True), 0xFF13CE66, THEME_BORDER, on_p, on_n, off_p, off_n)

    def refresh_output(extra: str = "") -> None:
        text = (
            f"CheckBox1={int(bool(DLL.GetCheckBoxState(cb1)))}  "
            f"CheckBox2={int(bool(DLL.GetCheckBoxState(cb2)))}  "
            f"Progress={DLL.GetProgressValue(prog)}  "
            f"Slider={DLL.GetSliderValue(slider)}  "
            f"Switch={int(bool(DLL.GetSwitchState(switcher)))}"
        )
        if extra:
            text = f"{extra}\n{text}"
        base.set_label_text(out, text)
        base.set_status(text.splitlines()[0])

    cb = DLL._CheckBoxCB(lambda h, checked: refresh_output(f"CheckBox 回调: hwnd=0x{base.hwnd_key(h):X} checked={int(bool(checked))}"))
    rb = DLL._RadioCB(lambda h, gid, checked: refresh_output(f"Radio 回调: hwnd=0x{base.hwnd_key(h):X} group={gid} checked={int(bool(checked))}"))
    pb = DLL._ProgressCB(lambda h, value: refresh_output(f"Progress 回调: hwnd=0x{base.hwnd_key(h):X} value={value}"))
    sl = DLL._SliderCB(lambda h, value: refresh_output(f"Slider 回调: hwnd=0x{base.hwnd_key(h):X} value={value}"))
    sw = DLL._SwitchCB(lambda h, checked: refresh_output(f"Switch 回调: hwnd=0x{base.hwnd_key(h):X} checked={int(bool(checked))}"))
    KEEP.extend([cb, rb, pb, sl, sw])
    DLL.SetCheckBoxCallback(cb1, cb)
    DLL.SetCheckBoxCallback(cb2, cb)
    DLL.SetRadioButtonCallback(rb1, rb)
    DLL.SetRadioButtonCallback(rb2, rb)
    DLL.SetRadioButtonCallback(rb3, rb)
    DLL.SetProgressBarCallback(prog, pb)
    DLL.SetSliderCallback(slider, sl)
    DLL.SetSwitchCallback(switcher, sw)

    base.button(page, "↺", "切换勾选 1", 40, 228, 140, 36, 0xFF409EFF, lambda: (DLL.SetCheckBoxState(cb1, BOOL(not bool(DLL.GetCheckBoxState(cb1)))), refresh_output("程序切换 CheckBox1")))
    base.button(page, "↺", "切换勾选 2", 196, 228, 140, 36, 0xFF67C23A, lambda: (DLL.SetCheckBoxState(cb2, BOOL(not bool(DLL.GetCheckBoxState(cb2)))), refresh_output("程序切换 CheckBox2")))
    base.button(page, "📉", "进度 -10", 758, 228, 120, 36, 0xFF909399, lambda: (DLL.SetProgressValue(prog, max(0, DLL.GetProgressValue(prog) - 10)), refresh_output("程序设置 ProgressBar")))
    base.button(page, "📈", "进度 +10", 894, 228, 120, 36, 0xFF409EFF, lambda: (DLL.SetProgressValue(prog, min(100, DLL.GetProgressValue(prog) + 10)), refresh_output("程序设置 ProgressBar")))
    base.button(page, "🎚️", "Slider=75", 1030, 228, 120, 36, 0xFFE6A23C, lambda: (DLL.SetSliderValue(slider, 75), refresh_output("程序设置 Slider=75")))
    base.button(page, "🔀", "切换开关", 1166, 228, 120, 36, 0xFF67C23A, lambda: (DLL.SetSwitchState(switcher, BOOL(not bool(DLL.GetSwitchState(switcher)))), refresh_output("程序切换 Switch")))
    refresh_output("初始状态")


def build_page_groupbox(page: HWND) -> None:
    g1 = base.groupbox(page, "Outline 分组框", 24, 24, 360, 180)
    g2 = base.groupbox(page, "Card 分组框", 414, 24, 360, 180)
    g3 = base.groupbox(page, "Header Bar 分组框", 804, 24, 420, 180)
    DLL.SetGroupBoxStyle(g1, GROUPBOX_STYLE_OUTLINE)
    DLL.SetGroupBoxStyle(g2, GROUPBOX_STYLE_CARD)
    DLL.SetGroupBoxStyle(g3, GROUPBOX_STYLE_HEADER_BAR)
    DLL.SetGroupBoxTitleColor(g3, 0xFF409EFF)

    base.label(page, "🪄 Outline 风格更适合做配置分区。", 48, 76, 300, 24, fg=0xFF606266, bg=0xFFF5F7FA)
    base.button(g1, "🔎", "读取样式", 10, 56, 120, 34, 0xFF409EFF, lambda: base.set_status("GroupBox -> Outline"))
    base.button(g1, "🧪", "测试按钮", 140, 56, 120, 34, 0xFF67C23A, lambda: base.set_status("GroupBox -> Outline 按钮点击"))
    base.label(page, "📌 适合配置区 / 侧栏区 / 轻分组。", 48, 132, 260, 24, fg=0xFF909399, bg=0xFFF5F7FA)

    base.label(page, "🧩 Card 风格适合信息卡片和表单块。", 438, 76, 300, 24, fg=0xFF606266, bg=0xFFF5F7FA)
    base.button(g2, "💬", "消息", 10, 56, 100, 34, 0xFFE6A23C, lambda: base.show_msg("🗂️ GroupBox", "这是 Card 分组框里的消息框。", "💬"))
    base.button(g2, "🎨", "变标题色", 122, 56, 120, 34, 0xFF8E44AD, lambda: (DLL.SetGroupBoxTitleColor(g2, 0xFF8E44AD), base.set_status("GroupBox -> Card 标题色已修改")))
    base.label(page, "📋 常用于资料卡、属性面板、摘要信息。", 438, 132, 280, 24, fg=0xFF909399, bg=0xFFF5F7FA)

    base.label(page, "🚀 Header Bar 风格适合做主功能区标题。", 828, 76, 340, 24, fg=0xFF606266, bg=0xFFF5F7FA)
    base.button(g3, "✅", "成功动作", 10, 56, 120, 34, 0xFF67C23A, lambda: base.set_status("GroupBox -> Header Bar 成功动作"))
    base.button(g3, "📌", "状态动作", 140, 56, 120, 34, 0xFF409EFF, lambda: base.set_status("GroupBox -> Header Bar 状态动作"))
    base.label(page, "🧭 更适合大页面里的一级业务模块。", 828, 132, 300, 24, fg=0xFF909399, bg=0xFFF5F7FA)
    build_label_property_demo(page, "分组框页标签演示", 964, 224, 500, 176)


def build_page_groupbox_v2(page: HWND) -> None:
    palette = page_palette()
    page_bg = palette["page_bg"]
    card_bg = palette["card_bg"]
    text_color = palette["text"]
    muted_color = palette["muted"]
    accent_color = palette["accent"]

    g1 = base.groupbox(page, "Outline 分组框", 16, 16, 692, 284)
    g2 = base.groupbox(page, "Card 分组框", 756, 16, 692, 284)
    g3 = base.groupbox(page, "Header Bar 分组框", 16, 336, 692, 284)
    DLL.SetGroupBoxStyle(g1, GROUPBOX_STYLE_OUTLINE)
    DLL.SetGroupBoxStyle(g2, GROUPBOX_STYLE_CARD)
    DLL.SetGroupBoxStyle(g3, GROUPBOX_STYLE_HEADER_BAR)
    DLL.SetGroupBoxTitleColor(g3, accent_color)

    register_theme_label(base.label(g1, "Outline 风格更适合轻量分区。", 18, 42, 628, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(g1, "适合配置区、属性区、筛选栏这类弱层级的布局，重点是把区域分开，而不是制造很强的卡片感。", 18, 74, 628, 44, fg=muted_color, bg=page_bg, wrap=True), "muted", "page")
    base.button(g1, "🔎", "读取样式", 18, 140, 148, 38, 0xFF409EFF, lambda: base.set_status("GroupBox -> Outline"))
    base.button(g1, "🧪", "测试按钮", 180, 140, 148, 38, 0xFF67C23A, lambda: base.set_status("GroupBox -> Outline 按钮点击"))
    register_theme_label(base.label(g1, "适合用在设置面板、筛选栏、轻分组块。", 18, 202, 620, 24, fg=muted_color, bg=page_bg), "muted", "page")

    register_theme_label(base.label(g2, "Card 风格适合信息卡片和表单块。", 18, 42, 628, 24, fg=text_color, bg=card_bg), "text", "card")
    register_theme_label(base.label(g2, "Card 会提供更完整的容器感，适合资料摘要、状态卡片、表单区和需要承载更连续内容的区域。", 18, 74, 628, 44, fg=muted_color, bg=card_bg, wrap=True), "muted", "card")
    base.button(g2, "💬", "消息", 18, 140, 136, 38, 0xFFE6A23C, lambda: base.show_msg("📦 GroupBox", "这是 Card 分组框里的消息框。", "💬"))
    base.button(g2, "🎨", "标题色", 168, 140, 148, 38, 0xFF8E44AD, lambda: (DLL.SetGroupBoxTitleColor(g2, 0xFF8E44AD), base.set_status("GroupBox -> Card 标题色已修改")))
    register_theme_label(base.label(g2, "常用于资料卡、属性面板、摘要信息。", 18, 202, 620, 24, fg=muted_color, bg=card_bg), "muted", "card")

    register_theme_label(base.label(g3, "Header Bar 风格适合主功能区标题。", 18, 54, 628, 24, fg=text_color, bg=card_bg), "text", "card")
    register_theme_label(base.label(g3, "顶部有更明确的抬头区，适合承担一级业务模块、工具区或页面主功能块，比 Outline 和 Card 更有章节感。", 18, 88, 628, 44, fg=muted_color, bg=card_bg, wrap=True), "muted", "card")
    base.button(g3, "✅", "成功动作", 18, 156, 148, 38, 0xFF67C23A, lambda: base.set_status("GroupBox -> Header Bar 成功动作"))
    base.button(g3, "📌", "状态动作", 180, 156, 148, 38, 0xFF409EFF, lambda: base.set_status("GroupBox -> Header Bar 状态动作"))
    register_theme_label(base.label(g3, "更适合大页面里的一级业务模块。", 18, 218, 620, 24, fg=muted_color, bg=card_bg), "muted", "card")

    build_label_property_demo(page, "分组框页标签演示", 756, 336, 692, 284)


def build_page_panel_demo(page: HWND) -> None:
    build_label_property_demo(page, "面板页标签演示", 1010, 16, 454, 176)
    base.groupbox(page, "🧩 Panel 组合布局", 16, 16, 970, 420)
    base.label(page, "Panel 页改成更像实际软件界面的组合布局：摘要卡、状态区、快捷操作区、活动流。", 40, 56, 900, 24, fg=0xFF606266, bg=0xFFF5F7FA)

    sidebar = DLL.CreatePanel(page, 40, 96, 220, 290, THEME_BG)
    stats = DLL.CreatePanel(page, 284, 96, 300, 136, THEME_SURFACE)
    actions = DLL.CreatePanel(page, 608, 96, 354, 136, THEME_SURFACE_PRIMARY)
    feed = DLL.CreatePanel(page, 284, 250, 678, 136, THEME_BG)
    panel_state = base.label(page, "等待 Panel 按钮动作。", 40, 392, 922, 24, fg=0xFF606266, bg=0xFFF5F7FA)

    def set_panel_state(text: str) -> None:
        base.set_label_text(panel_state, text)
        base.set_status(text)

    base.label(sidebar, "🧭 左侧导航 Panel", 16, 14, 180, 24, fg=0xFF303133, bg=0xFFFFFFFF, size=14, bold=True)
    base.label(sidebar, "📁 项目概览", 16, 50, 160, 22, fg=0xFF409EFF, bg=0xFFFFFFFF)
    base.label(sidebar, "📝 表单区域", 16, 78, 160, 22, fg=0xFF606266, bg=0xFFFFFFFF)
    base.label(sidebar, "📊 数据面板", 16, 106, 160, 22, fg=0xFF606266, bg=0xFFFFFFFF)
    base.label(sidebar, "⚙️ 设置中心", 16, 134, 160, 22, fg=0xFF606266, bg=0xFFFFFFFF)
    base.button(sidebar, "🚀", "进入工作区", 6, 178, 176, 36, 0xFF409EFF, lambda: set_panel_state("Panel -> 进入工作区"))
    base.button(sidebar, "💬", "说明消息", 6, 224, 176, 36, 0xFF909399, lambda: (base.show_msg("🧩 Panel", "左侧导航 Panel 常用于后台导航与功能入口。", "💬"), set_panel_state("Panel -> 说明消息已弹出")))

    base.label(stats, "📈 数据摘要 Panel", 16, 14, 180, 24, fg=0xFF303133, bg=0xFFF5F7FA, size=14, bold=True)
    base.label(stats, "🚀 活跃项目", 16, 52, 120, 20, fg=0xFF909399, bg=0xFFF5F7FA)
    base.label(stats, "12", 18, 74, 80, 32, fg=0xFF409EFF, bg=0xFFF5F7FA, size=24, bold=True)
    base.label(stats, "✅ 已完成任务", 148, 52, 120, 20, fg=0xFF909399, bg=0xFFF5F7FA)
    base.label(stats, "86", 150, 74, 80, 32, fg=0xFF67C23A, bg=0xFFF5F7FA, size=24, bold=True)

    base.label(actions, "⚡ 快捷操作 Panel", 16, 14, 180, 24, fg=0xFF303133, bg=0xFFEAF3FF, size=14, bold=True)
    base.label(actions, "适合放高频按钮、状态按钮、筛选器。", 16, 46, 280, 20, fg=0xFF606266, bg=0xFFEAF3FF)
    base.button(actions, "➕", "新建任务", 6, 74, 104, 34, 0xFF409EFF, lambda: set_panel_state("Panel -> 新建任务"))
    base.button(actions, "🧪", "测试接口", 118, 74, 104, 34, 0xFF67C23A, lambda: set_panel_state("Panel -> 测试接口"))
    base.button(actions, "🧹", "清理缓存", 230, 74, 104, 34, 0xFFE6A23C, lambda: set_panel_state("Panel -> 清理缓存"))

    base.label(feed, "📰 活动流 Panel", 16, 14, 180, 24, fg=0xFF303133, bg=0xFFFFFFFF, size=14, bold=True)
    base.label(feed, "🕒 10:20  已完成主题切换兼容修复", 16, 50, 420, 20, fg=0xFF606266, bg=0xFFFFFFFF)
    base.label(feed, "🕒 10:32  已补充 Tooltip 四方向与主题展示", 16, 76, 420, 20, fg=0xFF606266, bg=0xFFFFFFFF)
    base.label(feed, "🕒 10:48  已增加树形版独立组件详情页", 16, 102, 420, 20, fg=0xFF606266, bg=0xFFFFFFFF)
    set_panel_state("🧩 Panel 页 ready，可直接验证 Panel 宿主按钮是否可见、可点、可回写状态。")



def build_page_panel_demo_v2(page: HWND) -> None:
    palette = page_palette()
    page_bg = palette["page_bg"]
    text_color = palette["text"]
    muted_color = palette["muted"]
    accent_color = palette["accent"]

    base.groupbox(page, "🧱 Panel 组合布局", 16, 16, 1448, 500)
    base.groupbox(page, "📘 Panel 使用说明", 16, 540, 1448, 208)

    register_theme_label(
        base.label(
            page,
            "Panel 页面改成更像实际软件界面的组合布局：侧栏、摘要、快捷操作区和活动流都放在同一块主工作区里。",
            40,
            56,
            1368,
            24,
            fg=muted_color,
            bg=page_bg,
        ),
        "muted",
        "page",
    )

    sidebar = DLL.CreatePanel(page, 40, 96, 260, 392, THEME_BG)
    stats = DLL.CreatePanel(page, 324, 96, 360, 184, THEME_SURFACE)
    actions = DLL.CreatePanel(page, 708, 96, 716, 184, THEME_SURFACE_PRIMARY)
    feed = DLL.CreatePanel(page, 324, 304, 1100, 184, THEME_BG)
    panel_state = register_theme_label(
        base.label(page, "等待 Panel 动作。", 40, 586, 1368, 28, fg=accent_color, bg=page_bg),
        "accent",
        "page",
    )
    panel_detail = register_theme_label(
        base.label(page, "Panel 适合把同一业务域的控件组织成一个视觉整体，既能当背景容器，也能承担布局分区。", 40, 626, 1368, 50, fg=text_color, bg=page_bg, wrap=True),
        "text",
        "page",
    )

    def set_panel_state(text: str, detail: str | None = None) -> None:
        base.set_label_text(panel_state, text)
        if detail:
            base.set_label_text(panel_detail, detail)
        base.set_status(text)

    base.label(sidebar, "🧭 左侧导航 Panel", 18, 16, 200, 24, fg=THEME_TEXT, bg=THEME_BG, size=14, bold=True)
    base.label(sidebar, "📋 项目总览", 18, 58, 170, 22, fg=THEME_PRIMARY, bg=THEME_BG)
    base.label(sidebar, "🧾 表单区域", 18, 88, 170, 22, fg=THEME_MUTED, bg=THEME_BG)
    base.label(sidebar, "📊 数据面板", 18, 118, 170, 22, fg=THEME_MUTED, bg=THEME_BG)
    base.label(sidebar, "⚙️ 设置中心", 18, 148, 170, 22, fg=THEME_MUTED, bg=THEME_BG)
    base.label(sidebar, "📨 消息归档", 18, 178, 170, 22, fg=THEME_MUTED, bg=THEME_BG)
    base.button(sidebar, "🚀", "进入工作区", 18, 240, 196, 38, 0xFF409EFF, lambda: set_panel_state("Panel -> 进入工作区", "侧栏型 Panel 适合承载主导航、功能入口和分区切换。"))
    base.button(sidebar, "💬", "说明消息", 18, 288, 196, 38, 0xFF909399, lambda: (base.show_msg("🧱 Panel", "左侧导航 Panel 常用于后台导航与功能入口。", "💬"), set_panel_state("Panel -> 说明消息已弹出", "说明消息和状态反馈也可以集中在容器区域里处理。")))
    base.button(sidebar, "📌", "固定视图", 18, 336, 196, 38, 0xFF67C23A, lambda: set_panel_state("Panel -> 视图已固定", "把一组按钮、标签和状态绑在同一个 Panel 里，后续整体移动和显示隐藏会更轻松。"))

    base.label(stats, "📈 数据摘要 Panel", 18, 16, 200, 24, fg=THEME_TEXT, bg=THEME_SURFACE, size=14, bold=True)
    base.label(stats, "🟦 活跃项目", 18, 58, 120, 20, fg=THEME_MUTED, bg=THEME_SURFACE)
    base.label(stats, "12", 18, 82, 96, 34, fg=THEME_PRIMARY, bg=THEME_SURFACE, size=26, bold=True)
    base.label(stats, "✅ 已完成任务", 190, 58, 140, 20, fg=THEME_MUTED, bg=THEME_SURFACE)
    base.label(stats, "86", 190, 82, 96, 34, fg=THEME_SUCCESS, bg=THEME_SURFACE, size=26, bold=True)
    base.label(stats, "📦 容器内的数字卡片、摘要信息、统计指标很适合放进独立 Panel。", 18, 134, 314, 40, fg=THEME_MUTED, bg=THEME_SURFACE, wrap=True)

    base.label(actions, "⚡ 快捷操作 Panel", 18, 16, 220, 24, fg=THEME_TEXT, bg=THEME_SURFACE_PRIMARY, size=14, bold=True)
    base.label(actions, "适合高频按钮、状态开关、筛选器和即时操作入口。", 18, 48, 420, 22, fg=THEME_MUTED, bg=THEME_SURFACE_PRIMARY)
    base.button(actions, "➕", "新建任务", 18, 88, 136, 38, 0xFF409EFF, lambda: set_panel_state("Panel -> 新建任务", "操作区 Panel 适合放页面里最高频的一组操作。"))
    base.button(actions, "🧪", "测试接口", 168, 88, 136, 38, 0xFF67C23A, lambda: set_panel_state("Panel -> 测试接口", "把同一类动作集中在 Panel 里，能快速建立区域语义。"))
    base.button(actions, "🧹", "清理缓存", 318, 88, 136, 38, 0xFFE6A23C, lambda: set_panel_state("Panel -> 清理缓存", "有背景层的 Panel 很适合承载工具区、命令区和局部工作台。"))
    base.button(actions, "🔁", "刷新视图", 468, 88, 136, 38, 0xFF8E44AD, lambda: set_panel_state("Panel -> 刷新视图", "刷新、过滤、切换这些操作，放在同一个 Panel 里会比散落在页面上更整洁。"))
    base.label(actions, "当前建议：把操作按钮和说明文字放到同一块 Panel 里，用户更容易理解这是一个功能区。", 18, 142, 662, 28, fg=THEME_MUTED, bg=THEME_SURFACE_PRIMARY, wrap=True)

    base.label(feed, "📰 活动流 Panel", 18, 16, 180, 24, fg=THEME_TEXT, bg=THEME_BG, size=14, bold=True)
    base.label(feed, "🕘 10:20  已完成主题切换兼容修复", 18, 56, 440, 20, fg=THEME_MUTED, bg=THEME_BG)
    base.label(feed, "🕘 10:32  已补全 Tooltip 四方向与主题展示", 18, 86, 440, 20, fg=THEME_MUTED, bg=THEME_BG)
    base.label(feed, "🕘 10:48  已增加树形版独立组件详情页", 18, 116, 440, 20, fg=THEME_MUTED, bg=THEME_BG)
    base.label(feed, "🕘 11:06  已完成 Switch / GroupBox 页面重排", 18, 146, 440, 20, fg=THEME_MUTED, bg=THEME_BG)
    base.label(feed, "这一块模拟的是消息流、日志流或最近活动区域。Panel 在这里最重要的作用，是把连续文本和操作上下文打包成一个稳定区块。", 520, 56, 548, 74, fg=THEME_MUTED, bg=THEME_BG, wrap=True)

    register_theme_label(base.label(page, "1. CreatePanel：创建背景容器和布局分区。", 40, 688, 620, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "2. Panel 适合承载导航、摘要卡、工具区、活动流这类强语义区域。", 40, 718, 760, 24, fg=text_color, bg=page_bg), "text", "page")

    set_panel_state("🧱 Panel 页已重排完成", "主工作区已经铺满页面，上方是 4 块组合 Panel，下方是状态和使用说明，不再保留右上角的标签演示分组框。")


def build_page_hotkey(page: HWND) -> None:
    base.groupbox(page, "⌨️ HotKeyControl 热键框", 16, 16, 960, 360)
    build_label_property_demo(page, "热键框页标签演示", 1000, 16, 464, 176)
    hk_out = base.label(page, "等待读取热键。", 40, 316, 860, 40, fg=0xFF606266, bg=0xFFF5F7FA, wrap=True)
    hotkey = DLL.CreateHotKeyControl(page, 758, 90, 300, 38, THEME_TEXT, THEME_BG)
    DLL.SetHotKeyColors(hotkey, THEME_TEXT, THEME_BG, THEME_BORDER_LIGHT)
    DLL.SetHotKey(hotkey, ord("S"), HOTKEY_CTRL)
    DLL.SetHotKeyControlBounds(hotkey, 40, 100, 320, 38)

    def refresh_hotkey(prefix: str = "读取热键") -> None:
        vk_code = ctypes.c_int()
        modifiers = ctypes.c_int()
        fg = UINT32()
        bg = UINT32()
        border = UINT32()
        DLL.GetHotKey(hotkey, ctypes.byref(vk_code), ctypes.byref(modifiers))
        DLL.GetHotKeyColors(hotkey, ctypes.byref(fg), ctypes.byref(bg), ctypes.byref(border))
        text = (
            f"{prefix}: {hotkey_text(vk_code.value, modifiers.value)}  "
            f"(vk={vk_code.value}, mod={modifiers.value})\n"
            f"颜色 fg=0x{fg.value:08X} bg=0x{bg.value:08X} border=0x{border.value:08X}"
        )
        base.set_label_text(hk_out, text)
        base.set_status(text.splitlines()[0])

    hcb = DLL._HotKeyCB(lambda _h, vk_code, modifiers: refresh_hotkey(f"热键回调 -> {hotkey_text(vk_code, modifiers)}"))
    KEEP.append(hcb)
    DLL.SetHotKeyCallback(hotkey, hcb)

    base.button(page, "💾", "Ctrl+S", 40, 156, 110, 36, 0xFF409EFF, lambda: (DLL.SetHotKey(hotkey, ord("S"), HOTKEY_CTRL), refresh_hotkey("程序设置 Ctrl+S")))
    base.button(page, "📦", "Ctrl+Shift+P", 166, 156, 140, 36, 0xFF67C23A, lambda: (DLL.SetHotKey(hotkey, ord("P"), HOTKEY_CTRL | HOTKEY_SHIFT), refresh_hotkey("程序设置 Ctrl+Shift+P")))
    base.button(page, "⚠️", "Alt+F4", 322, 156, 100, 36, 0xFFE6A23C, lambda: (DLL.SetHotKey(hotkey, 115, HOTKEY_ALT), refresh_hotkey("程序设置 Alt+F4")))
    base.button(page, "🧹", "清空", 438, 156, 100, 36, 0xFF909399, lambda: (DLL.ClearHotKey(hotkey), refresh_hotkey("程序清空热键")))
    base.button(page, "🎨", "切暗色边框", 40, 206, 130, 36, 0xFF303133, lambda: (DLL.SetHotKeyColors(hotkey, THEME_TEXT, THEME_SURFACE, THEME_PRIMARY), refresh_hotkey("程序设置热键颜色")))
    base.button(page, "🚫", "禁用", 186, 206, 90, 36, 0xFFF56C6C, lambda: (DLL.EnableHotKeyControl(hotkey, BOOL(False)), refresh_hotkey("已禁用热键控件")))
    base.button(page, "✅", "启用", 292, 206, 90, 36, 0xFF67C23A, lambda: (DLL.EnableHotKeyControl(hotkey, BOOL(True)), refresh_hotkey("已启用热键控件")))
    refresh_hotkey("初始值")


def build_page_picturebox_v2(page: HWND) -> None:
    palette = page_palette()
    card_bg = palette["card_bg"]
    text_color = palette["text"]
    muted_color = palette["muted"]
    accent_color = palette["accent"]

    base.groupbox(page, "🖼️ PictureBox 预览与操作", 16, 16, 960, 520)
    base.groupbox(page, "🎯 事件 / 状态 / 属性", 996, 16, 468, 520)
    base.groupbox(page, "📘 PictureBox API 说明", 16, 558, 1448, 220)

    register_theme_label(
        base.label(
            page,
            "这一页只保留 PictureBox 本体。上方两排按钮直接操作图片加载、缩放模式和透明度，右侧集中展示事件、焦点与布局状态。",
            40,
            54,
            900,
            38,
            fg=muted_color,
            bg=card_bg,
            wrap=True,
        ),
        "muted",
        "card",
    )
    register_theme_label(base.label(page, "📋 当前状态", 1020, 54, 220, 22, fg=text_color, bg=card_bg, size=14, bold=True), "text", "card")
    register_theme_label(base.label(page, "🧪 最近事件", 1020, 250, 220, 22, fg=text_color, bg=card_bg, size=14, bold=True), "text", "card")
    register_theme_label(
        base.label(
            page,
            "点击图片框或先点“聚焦图片”，然后直接按键，可验证 Click / DoubleClick / RightClick / MouseEnter / MouseLeave / Focus / Blur / KeyDown / KeyUp / Char / ValueChanged。",
            1020,
            84,
            412,
            48,
            fg=muted_color,
            bg=card_bg,
            wrap=True,
        ),
        "muted",
        "card",
    )

    readout = register_theme_label(base.label(page, "等待读取 PictureBox 状态。", 1020, 140, 412, 92, fg=text_color, bg=card_bg, wrap=True), "text", "card")
    event_log = register_theme_label(base.label(page, "等待触发 PictureBox 事件。", 1020, 278, 412, 120, fg=muted_color, bg=card_bg, wrap=True), "muted", "card")
    state_text = register_theme_label(base.label(page, "PictureBox 页状态将在这里更新。", 1020, 410, 412, 22, fg=accent_color, bg=card_bg), "accent", "card")

    pic_x = 40
    pic_y = 184
    pic_w = 912
    pic_h = 290
    pic = DLL.CreatePictureBox(page, pic_x, pic_y, pic_w, pic_h, SCALE_FIT, card_bg)

    png_demo = base.repo_root() / "imgs" / "图片框示例.png"
    jpg_demo = base.repo_root() / "examples" / "Python" / "微信图片.jpg"
    fallback_buf = ctypes.create_string_buffer(base.PNG_BYTES)
    KEEP.append(fallback_buf)

    pic_state: dict[str, object] = {
        "image": "未加载",
        "loaded": False,
        "visible": True,
        "enabled": True,
        "scale_mode": "FIT",
        "opacity": 1.0,
        "bg_color": card_bg,
        "bounds": (pic_x, pic_y, pic_w, pic_h),
    }
    event_lines: list[str] = []

    def current_theme_bg() -> int:
        return int(page_palette()["card_bg"])

    def current_cool_bg() -> int:
        return 0xFF243649 if is_dark_theme() else 0xFFEAF3FF

    def current_warm_bg() -> int:
        return 0xFF3B3023 if is_dark_theme() else 0xFFFFF4E8

    def picture_has_focus() -> bool:
        return base.hwnd_key(USER32.GetFocus()) == base.hwnd_key(pic)

    def render_readout(note: str | None = None, *, publish_status: bool = False) -> None:
        x, y, w, h = pic_state["bounds"]  # type: ignore[misc]
        base.set_label_text(
            readout,
            f"图片={pic_state['image']}  已加载={'是' if pic_state['loaded'] else '否'}  可见={'是' if pic_state['visible'] else '否'}  启用={'是' if pic_state['enabled'] else '否'}\n"
            f"模式={pic_state['scale_mode']}  透明度={int(float(pic_state['opacity']) * 100)}%  焦点={'是' if picture_has_focus() else '否'}\n"
            f"背景=0x{int(pic_state['bg_color']):08X}  位置=({x}, {y})  尺寸={w} x {h}",
        )
        if note is not None:
            base.set_label_text(state_text, note)
            if publish_status:
                base.set_status(note)

    def log_event(text: str, *, refresh_detail: bool = True, publish_status: bool = False) -> None:
        event_lines.insert(0, text)
        del event_lines[6:]
        base.set_label_text(event_log, "\n".join(event_lines))
        if refresh_detail:
            render_readout()
        if publish_status:
            base.set_status(text)

    def load_demo_image(path, label: str) -> None:
        ok = False
        if path.is_file():
            path_p, path_n, _ = s(str(path))
            pic_state["image"] = label
            pic_state["loaded"] = True
            ok = bool(DLL.LoadImageFromFile(pic, path_p, path_n))
        if not ok:
            pic_state["image"] = "内存占位图"
            pic_state["loaded"] = True
            ok = bool(DLL.LoadImageFromMemory(pic, ctypes.cast(fallback_buf, ctypes.c_void_p), len(base.PNG_BYTES)))
        if not ok:
            pic_state["image"] = "未加载"
            pic_state["loaded"] = False
            render_readout(f"{label} 加载失败", publish_status=True)
            return
        render_readout(f"PictureBox 已加载 {pic_state['image']}", publish_status=True)

    def clear_image() -> None:
        pic_state["image"] = "已清空"
        pic_state["loaded"] = False
        DLL.ClearImage(pic)
        render_readout("PictureBox 图片已清空", publish_status=True)

    def set_scale(mode: int, label: str) -> None:
        pic_state["scale_mode"] = label
        DLL.SetPictureBoxScaleMode(pic, mode)
        render_readout(f"PictureBox 缩放模式已切到 {label}", publish_status=True)

    def set_opacity(value: float) -> None:
        pic_state["opacity"] = max(0.0, min(1.0, value))
        DLL.SetImageOpacity(pic, ctypes.c_float(pic_state["opacity"]))
        render_readout(f"PictureBox 透明度已设为 {int(pic_state['opacity'] * 100)}%", publish_status=True)

    def set_background(color: int, note: str) -> None:
        pic_state["bg_color"] = color
        DLL.SetPictureBoxBackgroundColor(pic, color)
        render_readout(note, publish_status=True)

    def set_bounds(x: int, y: int, w: int, h: int, note: str) -> None:
        pic_state["bounds"] = (x, y, w, h)
        DLL.SetPictureBoxBounds(pic, x, y, w, h)
        render_readout(note, publish_status=True)

    def toggle_visible() -> None:
        next_visible = not bool(pic_state["visible"])
        pic_state["visible"] = next_visible
        DLL.ShowPictureBox(pic, BOOL(next_visible))
        render_readout(f"PictureBox 已{'显示' if next_visible else '隐藏'}", publish_status=True)

    def toggle_enabled() -> None:
        next_enabled = not bool(pic_state["enabled"])
        pic_state["enabled"] = next_enabled
        DLL.EnablePictureBox(pic, BOOL(next_enabled))
        render_readout(f"PictureBox 已{'启用' if next_enabled else '禁用'}", publish_status=True)

    def restore_default() -> None:
        pic_state["visible"] = True
        pic_state["enabled"] = True
        pic_state["scale_mode"] = "FIT"
        pic_state["opacity"] = 1.0
        pic_state["bg_color"] = current_theme_bg()
        pic_state["bounds"] = (pic_x, pic_y, pic_w, pic_h)
        DLL.ShowPictureBox(pic, BOOL(True))
        DLL.EnablePictureBox(pic, BOOL(True))
        DLL.SetPictureBoxBounds(pic, pic_x, pic_y, pic_w, pic_h)
        DLL.SetPictureBoxScaleMode(pic, SCALE_FIT)
        DLL.SetImageOpacity(pic, ctypes.c_float(1.0))
        DLL.SetPictureBoxBackgroundColor(pic, pic_state["bg_color"])
        load_demo_image(png_demo, "PNG 示例图")
        render_readout("PictureBox 已恢复默认状态", publish_status=True)

    def key_mods(shift: int, ctrl: int, alt: int) -> str:
        parts: list[str] = []
        if ctrl:
            parts.append("Ctrl")
        if shift:
            parts.append("Shift")
        if alt:
            parts.append("Alt")
        return "+".join(parts) if parts else "无修饰键"

    def on_click(_hwnd: HWND) -> None:
        log_event("Click -> PictureBox 被单击")
        render_readout("PictureBox 点击事件已触发", publish_status=True)

    def on_mouse_enter(_hwnd: HWND) -> None:
        log_event("MouseEnter -> 鼠标进入 PictureBox")

    def on_mouse_leave(_hwnd: HWND) -> None:
        log_event("MouseLeave -> 鼠标离开 PictureBox")

    def on_double_click(_hwnd: HWND, x: int, y: int) -> None:
        log_event(f"DoubleClick -> ({x}, {y})")
        render_readout("PictureBox 双击事件已触发", publish_status=True)

    def on_right_click(_hwnd: HWND, x: int, y: int) -> None:
        log_event(f"RightClick -> ({x}, {y})")
        render_readout("PictureBox 右键事件已触发", publish_status=True)

    def on_focus(_hwnd: HWND) -> None:
        log_event("Focus -> PictureBox 获得焦点")
        render_readout("PictureBox 已获得焦点", publish_status=True)

    def on_blur(_hwnd: HWND) -> None:
        log_event("Blur -> PictureBox 失去焦点")
        render_readout("PictureBox 已失去焦点", publish_status=True)

    def on_key_down(_hwnd: HWND, vk_code: int, shift: int, ctrl: int, alt: int) -> None:
        log_event(f"KeyDown -> vk={vk_code} ({key_mods(shift, ctrl, alt)})")

    def on_key_up(_hwnd: HWND, vk_code: int, shift: int, ctrl: int, alt: int) -> None:
        log_event(f"KeyUp -> vk={vk_code} ({key_mods(shift, ctrl, alt)})")

    def on_char(_hwnd: HWND, char_code: int) -> None:
        char_text = chr(char_code) if 32 <= char_code <= 126 else f"U+{char_code:04X}"
        log_event(f"Char -> {char_text} ({char_code})")

    def on_value_changed(_hwnd: HWND) -> None:
        log_event("ValueChanged -> 图片内容或属性已变化")

    pcb = DLL._PictureCB(on_click)
    enter_cb = DLL._ValueCB(on_mouse_enter)
    leave_cb = DLL._ValueCB(on_mouse_leave)
    dbl_cb = DLL._DoubleClickCB(on_double_click)
    right_cb = DLL._RightClickCB(on_right_click)
    focus_cb = DLL._ValueCB(on_focus)
    blur_cb = DLL._ValueCB(on_blur)
    key_down_cb = DLL._KeyEventCB(on_key_down)
    key_up_cb = DLL._KeyEventCB(on_key_up)
    char_cb = DLL._CharCB(on_char)
    value_cb = DLL._ValueCB(on_value_changed)
    KEEP.extend([pcb, enter_cb, leave_cb, dbl_cb, right_cb, focus_cb, blur_cb, key_down_cb, key_up_cb, char_cb, value_cb])
    DLL.SetPictureBoxCallback(pic, pcb)
    DLL.SetMouseEnterCallback(pic, enter_cb)
    DLL.SetMouseLeaveCallback(pic, leave_cb)
    DLL.SetDoubleClickCallback(pic, dbl_cb)
    DLL.SetRightClickCallback(pic, right_cb)
    DLL.SetFocusCallback(pic, focus_cb)
    DLL.SetBlurCallback(pic, blur_cb)
    DLL.SetKeyDownCallback(pic, key_down_cb)
    DLL.SetKeyUpCallback(pic, key_up_cb)
    DLL.SetCharCallback(pic, char_cb)
    DLL.SetValueChangedCallback(pic, value_cb)

    base.button(page, "🖼️", "PNG 示例", 40, 96, 120, 34, 0xFF409EFF, lambda: load_demo_image(png_demo, "PNG 示例图"))
    base.button(page, "📷", "JPG 示例", 172, 96, 120, 34, 0xFF67C23A, lambda: load_demo_image(jpg_demo, "JPG 示例图"))
    base.button(page, "🧹", "清空图片", 304, 96, 120, 34, 0xFFE6A23C, clear_image)
    base.button(page, "1:1", "原始大小", 436, 96, 120, 34, 0xFFF56C6C, lambda: set_scale(SCALE_NONE, "NONE"))
    base.button(page, "↔", "拉伸铺满", 568, 96, 120, 34, 0xFF909399, lambda: set_scale(SCALE_STRETCH, "STRETCH"))

    base.button(page, "FIT", "等比适应", 40, 138, 120, 34, 0xFF8E44AD, lambda: set_scale(SCALE_FIT, "FIT"))
    base.button(page, "◎", "居中显示", 172, 138, 120, 34, 0xFF409EFF, lambda: set_scale(SCALE_CENTER, "CENTER"))
    base.button(page, "100%", "完全显示", 304, 138, 120, 34, 0xFF67C23A, lambda: set_opacity(1.0))
    base.button(page, "60%", "半透明", 436, 138, 120, 34, 0xFFE6A23C, lambda: set_opacity(0.6))
    base.button(page, "25%", "低透明", 568, 138, 120, 34, 0xFFF56C6C, lambda: set_opacity(0.25))

    base.button(page, "🎯", "聚焦图片", 1020, 444, 94, 34, 0xFF409EFF, lambda: (USER32.SetFocus(pic), render_readout("焦点已切到 PictureBox", publish_status=True)))
    base.button(page, "↩", "移开焦点", 1124, 444, 94, 34, 0xFF909399, lambda: (USER32.SetFocus(STATE["hwnd"]), render_readout("焦点已从 PictureBox 移开", publish_status=True)))
    base.button(page, "👁", "显示切换", 1228, 444, 94, 34, 0xFF67C23A, toggle_visible)
    base.button(page, "🚫", "启用切换", 1332, 444, 94, 34, 0xFFF56C6C, toggle_enabled)

    base.button(page, "⬆", "放大预览", 1020, 486, 94, 34, 0xFF8E44AD, lambda: set_bounds(40, 176, 912, 308, "PictureBox 预览区域已放大"))
    base.button(page, "↺", "恢复默认", 1124, 486, 94, 34, 0xFF409EFF, restore_default)
    base.button(page, "💙", "冷色底", 1228, 486, 94, 34, 0xFF67C23A, lambda: set_background(current_cool_bg(), "PictureBox 已切到冷色背景"))
    base.button(page, "🧡", "暖色底", 1332, 486, 94, 34, 0xFFE6A23C, lambda: set_background(current_warm_bg(), "PictureBox 已切到暖色背景"))

    register_theme_label(
        base.label(
            page,
            "提示：点击图片框后直接按字母、数字、方向键或 Tab，可在右侧看到 KeyDown / KeyUp / Char 日志；点击其它按钮会触发 Blur。",
            40,
            492,
            900,
            24,
            fg=muted_color,
            bg=card_bg,
            wrap=True,
        ),
        "muted",
        "card",
    )

    register_theme_label(base.label(page, "1. CreatePictureBox / LoadImageFromFile / LoadImageFromMemory / ClearImage：创建图片框、加载本地图片、回退到内存占位图以及清空内容。", 40, 598, 1320, 24, fg=text_color, bg=card_bg), "text", "card")
    register_theme_label(base.label(page, "2. SetPictureBoxScaleMode：直接切换 NONE / STRETCH / FIT / CENTER 四种缩放模式。", 40, 632, 980, 24, fg=text_color, bg=card_bg), "text", "card")
    register_theme_label(base.label(page, "3. SetImageOpacity / SetPictureBoxBackgroundColor：验证透明度和图片框底色在亮色/暗色主题下都能独立调整。", 40, 666, 1240, 24, fg=text_color, bg=card_bg), "text", "card")
    register_theme_label(base.label(page, "4. SetPictureBoxBounds / ShowPictureBox / EnablePictureBox：演示布局调整、可见性和启用状态切换。", 40, 700, 1180, 24, fg=text_color, bg=card_bg), "text", "card")
    register_theme_label(base.label(page, "5. SetPictureBoxCallback + 通用事件回调：页面已接入 Click、DoubleClick、RightClick、MouseEnter、MouseLeave、Focus、Blur、KeyDown、KeyUp、Char、ValueChanged。", 40, 734, 1380, 24, fg=text_color, bg=card_bg), "text", "card")

    load_demo_image(png_demo, "PNG 示例图")
    render_readout("图片框页已重新排版，按钮不再遮挡，右侧集中展示全部事件回调。", publish_status=True)


def build_page_tooltip(page: HWND) -> None:
    base.groupbox(page, "💬 Tooltip 文字提示", 16, 16, 1448, 360)
    base.label(page, "Tooltip 支持上/下/左/右四个方向，dark/light/custom 主题，自定义字体字号颜色，以及 hover/click 两种触发。", 40, 56, 960, 22, fg=0xFF606266, bg=0xFFF5F7FA)

    hover_top_target = base.label(page, "🟦 Top / Dark / Hover", 40, 110, 210, 42, fg=0xFF1F5E99, bg=0xFFEAF3FF, size=13, bold=True, align=base.ALIGN_CENTER)
    hover_bottom_target = base.label(page, "🟩 Bottom / Light / Hover", 270, 110, 220, 42, fg=0xFF3A7A2D, bg=0xFFF0F9EB, size=13, bold=True, align=base.ALIGN_CENTER)
    hover_left_target = base.label(page, "🟨 Left / Custom / Hover", 510, 110, 220, 42, fg=0xFF8C4A00, bg=0xFFFFF7E6, size=13, bold=True, align=base.ALIGN_CENTER)
    click_right_target = base.label(page, "🟪 Right / Dark / Click", 750, 110, 220, 42, fg=0xFF7C3AED, bg=0xFFF4F0FF, size=13, bold=True, align=base.ALIGN_CENTER)
    base._bind_tooltip_demo_hover(hover_top_target, 0xFF1F5E99, 0xFFEAF3FF, 0xFFFFFFFF, 0xFF409EFF)
    base._bind_tooltip_demo_hover(hover_bottom_target, 0xFF3A7A2D, 0xFFF0F9EB, 0xFFFFFFFF, 0xFF67C23A)
    base._bind_tooltip_demo_hover(hover_left_target, 0xFF8C4A00, 0xFFFFF7E6, 0xFFFFFFFF, 0xFFE6A23C)
    base._bind_tooltip_demo_hover(click_right_target, 0xFF7C3AED, 0xFFF4F0FF, 0xFFFFFFFF, 0xFF8E44AD)

    top_tp, top_tn, _ = s("🖱️ Hover Top\ndark 主题 / 上方")
    top_tooltip = DLL.CreateTooltip(page, top_tp, top_tn, POPUP_TOP, 0, 0)
    DLL.SetTooltipTheme(top_tooltip, TOOLTIP_THEME_DARK)
    DLL.SetTooltipPlacement(top_tooltip, POPUP_TOP)
    DLL.SetTooltipTrigger(top_tooltip, TOOLTIP_TRIGGER_HOVER)
    DLL.BindTooltipToControl(top_tooltip, hover_top_target)

    bottom_tp, bottom_tn, _ = s("🖱️ Hover Bottom\nlight 主题 / 下方")
    bottom_tooltip = DLL.CreateTooltip(page, bottom_tp, bottom_tn, POPUP_BOTTOM, 0, 0)
    DLL.SetTooltipTheme(bottom_tooltip, TOOLTIP_THEME_LIGHT)
    DLL.SetTooltipPlacement(bottom_tooltip, POPUP_BOTTOM)
    DLL.SetTooltipTrigger(bottom_tooltip, TOOLTIP_TRIGGER_HOVER)
    DLL.BindTooltipToControl(bottom_tooltip, hover_bottom_target)

    left_tp, left_tn, _ = s("🖱️ Hover Left\ncustom 主题 / 左侧")
    left_tooltip = DLL.CreateTooltip(page, left_tp, left_tn, POPUP_LEFT, 0, 0)
    DLL.SetTooltipTheme(left_tooltip, TOOLTIP_THEME_CUSTOM)
    DLL.SetTooltipColors(left_tooltip, 0xFFFFF7E6, 0xFF8C4A00, 0xFFE3B261)
    left_font_p, left_font_n, _ = s("Microsoft YaHei UI")
    DLL.SetTooltipFont(left_tooltip, left_font_p, left_font_n, ctypes.c_float(15.0))
    DLL.SetTooltipPlacement(left_tooltip, POPUP_LEFT)
    DLL.SetTooltipTrigger(left_tooltip, TOOLTIP_TRIGGER_HOVER)
    DLL.BindTooltipToControl(left_tooltip, hover_left_target)

    right_tp, right_tn, _ = s("🖱️ Click / Right / Dark\n点击目标显示，再点一次收起。")
    right_tooltip = DLL.CreateTooltip(page, right_tp, right_tn, POPUP_RIGHT, 0, 0)
    DLL.SetTooltipTheme(right_tooltip, TOOLTIP_THEME_DARK)
    DLL.SetTooltipPlacement(right_tooltip, POPUP_RIGHT)
    DLL.SetTooltipTrigger(right_tooltip, TOOLTIP_TRIGGER_CLICK)
    right_font_p, right_font_n, _ = s("Microsoft YaHei UI")
    DLL.SetTooltipFont(right_tooltip, right_font_p, right_font_n, ctypes.c_float(14.0))
    DLL.BindTooltipToControl(right_tooltip, click_right_target)
    KEEP.extend([top_tooltip, bottom_tooltip, left_tooltip, right_tooltip])

    base.label(page, "四个 Tooltip 目标现在都改成了带主题色的轻底卡片，不再是突兀白块。", 40, 188, 860, 24, fg=0xFF606266, bg=0xFFF5F7FA)
    build_label_property_demo(page, "Tooltip 页标签演示", 1000, 16, 464, 176)


def build_page_notification(page: HWND) -> None:
    base.groupbox(page, "🔔 Notification 通知", 16, 16, 1448, 320)
    build_label_property_demo(page, "通知页标签演示", 980, 24, 460, 176)
    note_cb = DLL._NotificationCB(base.on_notification_event)
    KEEP.append(note_cb)
    base.label(page, "通知固定弹在软件窗口右上角，按钮全部使用语义色，避免白底生硬。", 40, 56, 860, 24, fg=0xFF606266, bg=0xFFF5F7FA)
    base.button(page, "🔵", "信息通知", 40, 110, 150, 40, 0xFF409EFF, lambda: base._show_note(STATE["hwnd"], "🔔 信息通知", "📝 这是一条 info 类型通知。", NOTIFY_INFO, note_cb))
    base.button(page, "🟢", "成功通知", 206, 110, 150, 40, 0xFF67C23A, lambda: base._show_note(STATE["hwnd"], "✅ 操作成功", "🎉 这是一条 success 类型通知。", NOTIFY_SUCCESS, note_cb))
    base.button(page, "🟠", "警告通知", 372, 110, 150, 40, 0xFFE6A23C, lambda: base._show_note(STATE["hwnd"], "⚠️ 注意", "📌 这是一条 warning 类型通知。", NOTIFY_WARNING, note_cb))
    base.button(page, "🔴", "错误通知", 538, 110, 150, 40, 0xFFF56C6C, lambda: base._show_note(STATE["hwnd"], "❌ 失败", "🧯 这是一条 error 类型通知。", NOTIFY_ERROR, note_cb))
    base.button(page, "📣", "连续两条", 704, 110, 150, 40, 0xFF8E44AD, lambda: (base._show_note(STATE["hwnd"], "📣 批量通知", "第一条通知。", NOTIFY_INFO, note_cb), base._show_note(STATE["hwnd"], "📣 批量通知", "第二条通知。", NOTIFY_SUCCESS, note_cb)))


def build_page_messagebox(page: HWND) -> None:
    base.groupbox(page, "📝 MessageBox 功能演示", 16, 16, 960, 260)
    build_label_property_demo(page, "消息框页标签演示", 1000, 16, 464, 176)
    base.label(page, "消息框页不只是一个按钮，而是保留多种消息内容、图标和说明组件。", 40, 56, 860, 24, fg=0xFF606266, bg=0xFFF5F7FA)
    base.button(page, "💬", "普通消息框", 40, 110, 150, 38, 0xFF409EFF, lambda: (base.show_msg("📝 普通消息", "🧪 这是普通消息框演示。", "💬"), base.set_status("MessageBox -> 普通消息")))
    base.button(page, "✅", "成功消息", 206, 110, 150, 38, 0xFF67C23A, lambda: (base.show_msg("✅ 操作成功", "🎉 这是成功消息框演示。", "✅"), base.set_status("MessageBox -> 成功消息")))
    base.button(page, "⚠️", "警告消息", 372, 110, 150, 38, 0xFFE6A23C, lambda: (base.show_msg("⚠️ 注意", "📌 这是警告消息框演示。", "⚠️"), base.set_status("MessageBox -> 警告消息")))
    base.label(page, "这里同时保留页面内标签说明和弹窗按钮，避免进入页面后只有一个空按钮。", 40, 178, 860, 24, fg=0xFF909399, bg=0xFFF5F7FA)


def build_page_confirmbox(page: HWND) -> None:
    base.groupbox(page, "❓ ConfirmBox 功能演示", 16, 16, 960, 260)
    build_label_property_demo(page, "确认框页标签演示", 1000, 16, 464, 176)
    base.label(page, "确认框页保留多个触发入口，用来验证确定/取消回调。", 40, 56, 860, 24, fg=0xFF606266, bg=0xFFF5F7FA)
    base.button(page, "❓", "普通确认框", 40, 110, 150, 38, 0xFFE6A23C, lambda: (base.show_confirm("📣 ConfirmBox", "🧪 这是普通确认框演示。", "❓"), base.set_status("ConfirmBox -> 普通确认框")))
    base.button(page, "🧹", "删除确认", 206, 110, 150, 38, 0xFFF56C6C, lambda: (base.show_confirm("🗑️ 删除确认", "⚠️ 这是一条删除确认提示。", "🗑️"), base.set_status("ConfirmBox -> 删除确认")))
    base.button(page, "🚀", "继续流程", 372, 110, 150, 38, 0xFF409EFF, lambda: (base.show_confirm("🚀 继续流程", "📌 确认继续执行下一步吗？", "🚀"), base.set_status("ConfirmBox -> 继续流程")))


def build_page_tabcontrol(page: HWND) -> None:
    build_label_property_demo(page, "页签页标签演示", 16, 16, 420, 136)
    base.groupbox(page, "🗂️ TabControl 属性读取 / 设置", 460, 16, 1004, 184)
    tab_state = base.label(page, "等待页签状态。", 484, 112, 940, 24, fg=0xFF606266, bg=0xFFF5F7FA)
    mini = DLL.CreateTabControl(page, 40, 172, 420, 170)
    mini_titles = ("📘 文档", "🧪 测试", "⚙️ 设置")
    for idx, title in enumerate(mini_titles):
        content = base.add_tab(mini, title)
        base.label(content, f"Mini Tab {idx + 1}", 16, 16, 180, 24, size=14, bold=True)
        base.label(content, "这个小页签区用于直接测试读取、切换、样式同步。", 16, 46, 320, 24, fg=0xFF606266)
    DLL.SetTabItemSize(mini, 122, 34)
    DLL.SetTabPadding(mini, 14, 8)
    DLL.SetTabColors(mini, THEME_BG, THEME_SURFACE, THEME_TEXT, THEME_MUTED)
    DLL.SetTabIndicatorColor(mini, 0xFF409EFF)
    DLL.UpdateTabControlLayout(mini)
    base.enable_closable_tab_control(mini, mini_titles)
    DLL.SelectTab(mini, 0)

    def apply_style(style: int) -> None:
        DLL.SetTabHeaderStyle(mini, style)
        DLL.UpdateTabControlLayout(mini)
        DLL.RedrawTabControl(mini)
        base.apply_demo_tab_style(style)
        read_tab_state()

    def read_tab_state() -> None:
        tab = STATE.get("tab_style_demo")
        main_idx = DLL.GetCurrentTabIndex(tab) if tab else -1
        mini_idx = DLL.GetCurrentTabIndex(mini)
        text = f"Mini 当前索引={mini_idx}  主预览索引={main_idx}  关闭按钮=ON"
        base.set_label_text(tab_state, text)
        base.set_status(f"TabControl -> {text}")

    base.button(page, "━", "Line", 484, 56, 110, 34, 0xFF909399, lambda: apply_style(base.TAB_HEADER_STYLE_LINE))
    base.button(page, "▣", "Card", 608, 56, 110, 34, 0xFF409EFF, lambda: apply_style(base.TAB_HEADER_STYLE_CARD))
    base.button(page, "▤", "Plain", 732, 56, 110, 34, 0xFF67C23A, lambda: apply_style(base.TAB_HEADER_STYLE_CARD_PLAIN))
    base.button(page, "◫", "Segmented", 856, 56, 130, 34, 0xFFE6A23C, lambda: apply_style(base.TAB_HEADER_STYLE_SEGMENTED))
    base.button(page, "1", "Mini 选 1", 1000, 56, 110, 34, 0xFF409EFF, lambda: (DLL.SelectTab(mini, 0), read_tab_state()))
    base.button(page, "2", "Mini 选 2", 1124, 56, 110, 34, 0xFF67C23A, lambda: (DLL.SelectTab(mini, 1), read_tab_state()))
    base.button(page, "🔎", "读取索引", 1248, 56, 120, 34, 0xFF8E44AD, read_tab_state)
    content = create_content_host(page, 356)
    base.tab_styles_page(content)
    read_tab_state()


def build_page_editbox(page: HWND) -> None:
    palette = page_palette()
    page_bg = palette["page_bg"]
    text_color = palette["text"]
    muted_color = palette["muted"]
    accent_color = palette["accent"]

    build_label_property_demo(page, "编辑框页标签演示", 1020, 16, 444, 176)
    base.groupbox(page, "⌨️ EditBox 实时属性读取", 16, 16, 980, 248)
    base.groupbox(page, "🪄 文本 / 颜色 / 尺寸 / 状态", 16, 286, 980, 254)
    base.groupbox(page, "📄 多行 EditBox 演示", 1020, 212, 444, 328)
    base.groupbox(page, "📌 EditBox API 说明", 16, 558, 1448, 230)

    demo_edit = base.edit(page, "📌 单行 EditBox：可直接读取和设置文本。", 56, 120, 420, 38, False)
    memo = DLL.CreateEditBox(
        page,
        1044,
        262,
        380,
        132,
        *s("📄 已从主编辑框同步：\r\n1. 用于展示多行输入\r\n2. 保持统一浅底风格\r\n3. 可作为备注或说明区域")[:2],
        THEME_TEXT,
        THEME_BG,
        base.FONT_PTR,
        base.FONT_LEN,
        13,
        BOOL(False),
        BOOL(False),
        BOOL(False),
        base.ALIGN_LEFT,
        BOOL(True),
        BOOL(False),
        BOOL(False),
        BOOL(True),
        BOOL(False),
    )
    readout = register_theme_label(base.label(page, "等待读取编辑框属性。", 40, 184, 920, 56, fg=text_color, bg=page_bg, wrap=True), "text", "page")
    state_text = register_theme_label(base.label(page, "编辑框页状态将在这里更新。", 40, 760, 1360, 22, fg=accent_color, bg=page_bg), "accent", "page")
    register_theme_label(base.label(page, "这一页直接读取文本、颜色、位置、字体、启用态和可见态，不再只是放一个输入框。", 40, 56, 900, 24, fg=muted_color, bg=page_bg), "muted", "page")

    def read_utf8_edit(h_edit: HWND) -> str:
        size = int(DLL.GetEditBoxText(h_edit, None, 0))
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        DLL.GetEditBoxText(h_edit, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    def read_edit_bounds() -> tuple[int, int, int, int]:
        x = ctypes.c_int()
        y = ctypes.c_int()
        w = ctypes.c_int()
        h = ctypes.c_int()
        if int(DLL.GetEditBoxBounds(demo_edit, ctypes.byref(x), ctypes.byref(y), ctypes.byref(w), ctypes.byref(h))) != 0:
            return 0, 0, 0, 0
        return x.value, y.value, w.value, h.value

    def read_edit_font() -> tuple[str, int, int]:
        buf = ctypes.create_string_buffer(128)
        size = ctypes.c_int()
        bold = ctypes.c_int()
        italic = ctypes.c_int()
        underline = ctypes.c_int()
        result = int(DLL.GetEditBoxFont(demo_edit, buf, 128, ctypes.byref(size), ctypes.byref(bold), ctypes.byref(italic), ctypes.byref(underline)))
        name = buf.raw[:max(result, 0)].decode("utf-8", errors="replace") if result > 0 else ""
        return name, size.value, bold.value

    fg0 = UINT32()
    bg0 = UINT32()
    DLL.GetEditBoxColor(demo_edit, ctypes.byref(fg0), ctypes.byref(bg0))
    initial = {
        "text": read_utf8_edit(demo_edit),
        "bounds": read_edit_bounds(),
        "fg": int(fg0.value),
        "bg": int(bg0.value),
    }

    def refresh(note: str = "已刷新编辑框属性") -> None:
        fg = UINT32()
        bg = UINT32()
        DLL.GetEditBoxColor(demo_edit, ctypes.byref(fg), ctypes.byref(bg))
        x, y, w, h = read_edit_bounds()
        font_name, font_size, bold = read_edit_font()
        align_name = base.alignment_name(int(DLL.GetEditBoxAlignment(demo_edit)))
        enabled = "启用" if int(DLL.GetEditBoxEnabled(demo_edit)) == 1 else "禁用"
        visible = "显示" if int(DLL.GetEditBoxVisible(demo_edit)) == 1 else "隐藏"
        base.set_label_text(
            readout,
            f"text={read_utf8_edit(demo_edit)}  {visible}/{enabled}\n"
            f"bounds=({x}, {y}, {w}, {h})  align={align_name}  font={font_name or 'default'} {font_size}px bold={bold}\n"
            f"fg=0x{int(fg.value):08X}  bg=0x{int(bg.value):08X}"
        )
        base.set_label_text(state_text, note)
        base.set_status(note)

    def set_edit_text_value(text: str, note: str) -> None:
        DLL.SetEditBoxText(demo_edit, *s(text)[:2])
        DLL.SetEditBoxText(memo, *s("📄 已从主编辑框同步：\r\n" + text)[:2])
        refresh(note)

    def set_edit_colors(fg: int, bg: int, note: str) -> None:
        DLL.SetEditBoxColor(demo_edit, fg, bg)
        refresh(note)

    def set_edit_font_value(font_name: str, font_size: int, bold: bool, note: str) -> None:
        x, y, w, _h = read_edit_bounds()
        target_h = 44 if font_size >= 16 else int(initial["bounds"][3])
        DLL.SetEditBoxBounds(demo_edit, x, y, w, target_h)
        DLL.SetEditBoxFont(demo_edit, *s(font_name)[:2], font_size, BOOL(bold), BOOL(False), BOOL(False))
        refresh(note)

    def move_edit(dx: int = 0, dy: int = 0, dw: int = 0) -> None:
        x, y, w, h = read_edit_bounds()
        DLL.SetEditBoxBounds(demo_edit, x + dx, y + dy, w + dw, h)
        refresh(f"编辑框位置/尺寸已更新: dx={dx}, dy={dy}, dw={dw}")

    def restore_edit() -> None:
        x, y, w, h = initial["bounds"]
        DLL.SetEditBoxText(demo_edit, *s(str(initial["text"]))[:2])
        DLL.SetEditBoxColor(demo_edit, int(initial["fg"]), int(initial["bg"]))
        DLL.SetEditBoxBounds(demo_edit, int(x), int(y), int(w), int(h))
        DLL.SetEditBoxFont(demo_edit, *s("Segoe UI Emoji")[:2], 13, BOOL(False), BOOL(False), BOOL(False))
        DLL.EnableEditBox(demo_edit, BOOL(True))
        DLL.ShowEditBox(demo_edit, BOOL(True))
        refresh("编辑框属性已恢复默认")

    register_theme_label(base.label(page, "📝 文本预设", 40, 326, 180, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    base.button(page, "🧾", "写入表单文案", 40, 360, 156, 36, 0xFF409EFF, lambda: set_edit_text_value("请输入项目名称 / 关键词 / 标题", "编辑框文本已切到表单模式"))
    base.button(page, "🌈", "写入混排文案", 212, 360, 156, 36, 0xFF67C23A, lambda: set_edit_text_value("🌈 EmojiWindow 支持 emoji / English / 数字 123", "编辑框文本已切到混排模式"))
    base.button(page, "📄", "同步到多行框", 384, 360, 156, 36, 0xFF8E44AD, lambda: (DLL.SetEditBoxText(memo, *s("📄 已从主编辑框同步：\r\n" + read_utf8_edit(demo_edit))[:2]), refresh("当前单行内容已同步到多行 EditBox")))

    register_theme_label(base.label(page, "🎨 颜色 / 字体", 40, 414, 180, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    base.button(page, "🧊", "冷色", 40, 448, 118, 36, 0xFF409EFF, lambda: set_edit_colors(THEME_PRIMARY, THEME_SURFACE_PRIMARY, "编辑框已切到冷色方案"))
    base.button(page, "🧡", "暖色", 172, 448, 118, 36, 0xFFE6A23C, lambda: set_edit_colors(THEME_WARNING, THEME_SURFACE_WARNING, "编辑框已切到暖色方案"))
    base.button(page, "🔠", "16px Bold", 304, 448, 118, 36, 0xFF67C23A, lambda: set_edit_font_value("Segoe UI Emoji", 16, True, "编辑框字体已切到 16px Bold"))
    base.button(page, "🔡", "13px", 436, 448, 118, 36, 0xFF909399, lambda: set_edit_font_value("Segoe UI Emoji", 13, False, "编辑框字体已切回 13px"))

    register_theme_label(base.label(page, "📻 布局 / 状态", 1044, 404, 180, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    base.button(page, "➡️", "右移 80", 1044, 438, 112, 32, 0xFF409EFF, lambda: move_edit(dx=80))
    base.button(page, "⬇️", "下移 24", 1168, 438, 112, 32, 0xFF67C23A, lambda: move_edit(dy=24))
    base.button(page, "↔️", "加宽 120", 1292, 438, 132, 32, 0xFFE6A23C, lambda: move_edit(dw=120))
    base.button(page, "🚫", "禁用/启用", 1044, 478, 112, 32, 0xFF8E44AD, lambda: (DLL.EnableEditBox(demo_edit, BOOL(not (int(DLL.GetEditBoxEnabled(demo_edit)) == 1))), refresh("编辑框启用状态已切换")))
    base.button(page, "👁️", "显示/隐藏", 1168, 478, 112, 32, 0xFF909399, lambda: (DLL.ShowEditBox(demo_edit, BOOL(not (int(DLL.GetEditBoxVisible(demo_edit)) == 1))), refresh("编辑框可见状态已切换")))
    base.button(page, "↺", "恢复默认", 1292, 478, 132, 32, 0xFF409EFF, restore_edit)

    register_theme_label(base.label(page, "1. GetEditBoxText / SetEditBoxText：读取和修改输入文本。", 40, 598, 700, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "2. GetEditBoxColor / SetEditBoxColor：读取和切换前景色 / 背景色。", 40, 632, 720, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "3. GetEditBoxBounds / SetEditBoxBounds：直接修改编辑框位置与宽度。", 40, 666, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "4. GetEditBoxFont / SetEditBoxFont：读取和切换字体名、字号和粗体。", 40, 700, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "5. EnableEditBox / ShowEditBox：演示启用态和可见态切换。", 40, 734, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    refresh("编辑框页已加载，可直接测试属性读取与设置")


def build_page_datagrid_enhanced_v2(page: HWND) -> None:
    build_label_property_demo(page, "表格页标签演示", 16, 16, 420, 136)
    base.groupbox(page, "🧰 DataGridView 属性读取 / 表格主操作工具栏", 460, 16, 1004, 192)
    mode_label = base.label(page, "当前模式: 普通表格", 484, 48, 220, 24, fg=0xFF409EFF, bg=0xFFF5F7FA, size=13, bold=True)
    grid_state = base.label(page, "等待表格状态。", 484, 78, 940, 40, fg=0xFF606266, bg=0xFFF5F7FA, wrap=True)
    toolbar_panel = DLL.CreatePanel(page, 482, 122, 948, 54, THEME_SURFACE)
    base.label(page, "这一页直接完整展示：普通表格、虚拟表格、按钮列、链接列、真 bitmap 图片列、排序、导出 CSV、表头真接口读写。", 484, 180, 920, 18, fg=0xFF606266, bg=0xFFF5F7FA, wrap=True)

    base.groupbox(page, "🧾 全列型 DataGridView 演示", 16, 232, 1036, 556)
    base.groupbox(page, "🧪 表头 / 单元格 / 排序 / 导出", 1072, 232, 392, 556)
    base.label(page, "左侧是完整表格区，支持普通表格与 100 万行虚拟表格切换，并绑定表格右键菜单。", 40, 264, 940, 24, fg=0xFF606266, bg=0xFFF5F7FA)
    base.label(page, "右侧把表头文本真读写、单元格读取修改、按钮列 / 链接列 / 图片列、排序和导出 CSV 全部单独露出来。", 1096, 264, 340, 42, fg=0xFF606266, bg=0xFFF5F7FA, wrap=True)

    header_readout = base.label(page, "等待读取表头。", 1096, 338, 340, 66, fg=0xFF606266, bg=THEME_SURFACE, wrap=True)
    cell_readout = base.label(page, "等待读取单元格。", 1096, 526, 340, 60, fg=0xFF606266, bg=THEME_SURFACE, wrap=True)
    export_path_label = base.label(page, "CSV 尚未导出。", 1096, 756, 340, 24, fg=0xFF909399, bg=0xFFF5F7FA, wrap=True)

    normal_headers = ["🧾 任务", "☑️ 启用", "🚦 状态", "🏷️ 标签", "🔘 动作", "🔗 链接", "🖼️ 图片", "📝 备注"]
    virtual_headers = ["🧾 序号", "🚦 状态", "🏷️ 优先级", "👤 节点", "🧭 路由", "🖼️ 图片", "📝 虚拟备注"]
    default_normal_headers = list(normal_headers)
    default_virtual_headers = list(virtual_headers)
    rows_seed: list[dict[str, object]] = [
        {"task": "🧾 任务 1", "enabled": True, "status": "🚧 进行中", "tag": "🔵 P1", "action": "执行", "link": "查看详情", "icon": "图片-A", "note": "支持下拉、勾选和标签色块"},
        {"task": "🧾 任务 2", "enabled": False, "status": "🕒 待处理", "tag": "🟢 P2", "action": "审核", "link": "打开文档", "icon": "图片-B", "note": "支持按钮列、链接列和图片列"},
        {"task": "🧾 任务 3", "enabled": True, "status": "✅ 已完成", "tag": "🟠 P3", "action": "归档", "link": "查看报告", "icon": "图片-C", "note": "支持排序、导出 CSV 与表头读写"},
    ]
    image_demo_paths = [
        base.repo_root() / "imgs" / "1.png",
        base.repo_root() / "imgs" / "2.png",
        base.repo_root() / "imgs" / "3.png",
    ]
    normal_column_defs = (
        (normal_headers[0], DLL.DataGrid_AddTextColumn, 168),
        (normal_headers[1], DLL.DataGrid_AddCheckBoxColumn, 68),
        (normal_headers[2], DLL.DataGrid_AddComboBoxColumn, 116),
        (normal_headers[3], DLL.DataGrid_AddTagColumn, 90),
        (normal_headers[4], DLL.DataGrid_AddButtonColumn, 92),
        (normal_headers[5], DLL.DataGrid_AddLinkColumn, 118),
        (normal_headers[6], DLL.DataGrid_AddImageColumn, 88),
        (normal_headers[7], DLL.DataGrid_AddTextColumn, 236),
    )
    virtual_column_widths = (124, 118, 108, 110, 126, 88, 260)
    grid_local: dict[str, object] = {
        "normal": None,
        "virtual": None,
        "virtual_mode": False,
        "header_dark": True,
        "selected_row": 0,
        "selected_col": 0,
        "sort_states": {},
        "row_count": len(rows_seed),
        "dblclick_enabled": True,
        "accent_style": False,
    }

    def set_grid_state(text: str) -> None:
        base.set_label_text(grid_state, text)
        base.set_status(text)

    def active_grid() -> HWND | None:
        return grid_local["virtual"] if bool(grid_local["virtual_mode"]) else grid_local["normal"]  # type: ignore[return-value]

    def update_mode_label() -> None:
        if bool(grid_local["virtual_mode"]):
            base.set_label_text(mode_label, "当前模式: 虚拟表格 1,000,000 行")
        else:
            base.set_label_text(mode_label, f"当前模式: 普通表格 {int(grid_local['row_count'])} 行")

    def utf8_buf_read(fn, *args) -> str:
        size = fn(*args, None, 0)
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        fn(*args, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    def get_header_text(h_grid: HWND, col: int) -> str:
        return utf8_buf_read(DLL.DataGrid_GetColumnHeaderText, h_grid, col)

    def get_cell_text(h_grid: HWND, row: int, col: int) -> str:
        if h_grid == grid_local["virtual"]:
            return base.build_virtual_grid_text(row, col)
        return utf8_buf_read(DLL.DataGrid_GetCellText, h_grid, row, col)

    def refresh_header_readout(prefix: str = "读取表头") -> None:
        normal_grid = grid_local["normal"]
        virtual_grid = grid_local["virtual"]
        normal_text = " | ".join(get_header_text(normal_grid, i) for i in range(DLL.DataGrid_GetColumnCount(normal_grid))) if normal_grid else ""
        virtual_text = " | ".join(get_header_text(virtual_grid, i) for i in range(DLL.DataGrid_GetColumnCount(virtual_grid))) if virtual_grid else ""
        base.set_label_text(header_readout, f"{prefix}\n普通表头: {normal_text}\n虚拟表头: {virtual_text}")

    def refresh_cell_readout(prefix: str = "读取单元格") -> None:
        h_grid = active_grid()
        if not h_grid:
            return
        row = int(DLL.DataGrid_GetSelectedRow(h_grid))
        col = int(DLL.DataGrid_GetSelectedCol(h_grid))
        if row < 0 or col < 0:
            row = int(grid_local["selected_row"])
            col = int(grid_local["selected_col"])
        text = get_cell_text(h_grid, row, col)
        extra = ""
        if h_grid == grid_local["normal"] and col == 1 and row >= 0:
            extra = f"\n勾选状态: {'True' if bool(DLL.DataGrid_GetCellChecked(h_grid, row, col)) else 'False'}"
        base.set_label_text(cell_readout, f"{prefix}\nrow={row}, col={col}\nvalue={text if text else '(空)'}{extra}")

    def apply_demo_cell_styles() -> None:
        for row in range(int(DLL.DataGrid_GetRowCount(normal_grid))):
            tag_bg = THEME_SURFACE_PRIMARY if row % 2 == 0 else THEME_SURFACE_SUCCESS
            image_bg = THEME_SURFACE_PRIMARY if row % 2 == 0 else THEME_SURFACE_SUCCESS
            DLL.DataGrid_SetCellStyle(normal_grid, row, 3, 0xFF409EFF if row % 2 == 0 else 0xFF67C23A, tag_bg, BOOL(False), BOOL(False))
            DLL.DataGrid_SetCellStyle(normal_grid, row, 4, 0xFFFFFFFF, 0xFF409EFF if row % 2 == 0 else 0xFF67C23A, BOOL(False), BOOL(False))
            DLL.DataGrid_SetCellStyle(normal_grid, row, 5, 0xFF409EFF, 0x00000000, BOOL(False), BOOL(False))
            DLL.DataGrid_SetCellStyle(normal_grid, row, 6, 0xFF409EFF if row % 2 == 0 else 0xFF67C23A, image_bg, BOOL(False), BOOL(False))
            if bool(grid_local["accent_style"]):
                DLL.DataGrid_SetCellStyle(normal_grid, row, 0, 0xFF8E44AD, THEME_SURFACE_INFO, BOOL(True), BOOL(False))
                DLL.DataGrid_SetCellStyle(normal_grid, row, 7, THEME_TEXT, THEME_SURFACE_WARNING, BOOL(False), BOOL(False))
            else:
                DLL.DataGrid_SetCellStyle(normal_grid, row, 0, 0x00000000, 0x00000000, BOOL(False), BOOL(False))
                DLL.DataGrid_SetCellStyle(normal_grid, row, 7, 0x00000000, 0x00000000, BOOL(False), BOOL(False))
        DLL.DataGrid_Refresh(normal_grid)

    def set_demo_bitmap(row: int, image_index: int) -> None:
        if row < 0:
            return
        path = image_demo_paths[image_index % len(image_demo_paths)]
        p, n, _ = s(str(path))
        DLL.DataGrid_SetCellImageFromFile(normal_grid, row, 6, p, n)

    def apply_common_styles(h_grid: HWND, header_count: int) -> None:
        DLL.DataGrid_SetSelectionMode(h_grid, 0)
        DLL.DataGrid_SetShowGridLines(h_grid, BOOL(True))
        DLL.DataGrid_SetDefaultRowHeight(h_grid, 40)
        DLL.DataGrid_SetHeaderHeight(h_grid, 48)
        DLL.DataGrid_SetHeaderStyle(h_grid, 2 if bool(grid_local["header_dark"]) else 0)
        DLL.DataGrid_SetHeaderMultiline(h_grid, BOOL(False))
        for col in range(header_count):
            DLL.DataGrid_SetColumnHeaderAlignment(h_grid, col, base.ALIGN_CENTER)
            DLL.DataGrid_SetColumnCellAlignment(h_grid, col, base.ALIGN_LEFT)
        DLL.DataGrid_Refresh(h_grid)

    normal_grid = DLL.CreateDataGridView(page, 36, 300, 996, 448, BOOL(False), BOOL(True), THEME_TEXT, THEME_BG)
    virtual_grid = DLL.CreateDataGridView(page, 36, 300, 996, 448, BOOL(True), BOOL(True), THEME_TEXT, THEME_BG)
    grid_local["normal"] = normal_grid
    grid_local["virtual"] = virtual_grid
    DLL.DataGrid_SetColors(normal_grid, THEME_TEXT, THEME_BG, THEME_SURFACE, THEME_TEXT, THEME_SURFACE_PRIMARY, THEME_SURFACE, THEME_BORDER_LIGHT)
    DLL.DataGrid_SetColors(virtual_grid, THEME_TEXT, THEME_BG, THEME_SURFACE, THEME_TEXT, THEME_SURFACE_PRIMARY, THEME_SURFACE, THEME_BORDER_LIGHT)
    DLL.DataGrid_Show(virtual_grid, BOOL(False))

    for title, fn, width in normal_column_defs:
        p, n, _ = s(title)
        fn(normal_grid, p, n, width)

    for title, width in zip(virtual_headers, virtual_column_widths):
        p, n, _ = s(title)
        DLL.DataGrid_AddTextColumn(virtual_grid, p, n, width)

    cp, cn, _ = s("🕒 待处理\n🚧 进行中\n✅ 已完成\n⏸️ 已暂停")
    DLL.DataGrid_SetColumnComboItems(normal_grid, 2, cp, cn)
    DLL.DataGrid_SetDoubleClickEnabled(normal_grid, BOOL(bool(grid_local["dblclick_enabled"])))
    apply_common_styles(normal_grid, len(normal_headers))
    apply_common_styles(virtual_grid, len(virtual_headers))
    DLL.DataGrid_SetColumnCellAlignment(normal_grid, 1, base.ALIGN_CENTER)
    DLL.DataGrid_SetColumnCellAlignment(normal_grid, 2, base.ALIGN_CENTER)
    DLL.DataGrid_SetColumnCellAlignment(normal_grid, 3, base.ALIGN_CENTER)
    DLL.DataGrid_SetColumnCellAlignment(normal_grid, 4, base.ALIGN_CENTER)
    DLL.DataGrid_SetColumnCellAlignment(normal_grid, 6, base.ALIGN_CENTER)

    for row_data in rows_seed:
        row = DLL.DataGrid_AddRow(normal_grid)
        values = [
            str(row_data["task"]),
            None,
            str(row_data["status"]),
            str(row_data["tag"]),
            str(row_data["action"]),
            str(row_data["link"]),
            str(row_data["icon"]),
            str(row_data["note"]),
        ]
        for col, value in enumerate(values):
            if value is None:
                DLL.DataGrid_SetCellChecked(normal_grid, row, col, BOOL(bool(row_data["enabled"])))
                continue
            p, n, _ = s(value)
            DLL.DataGrid_SetCellText(normal_grid, row, col, p, n)
        tag_fg = 0xFF409EFF if "P1" in str(row_data["tag"]) else (0xFF67C23A if "P2" in str(row_data["tag"]) else 0xFFE6A23C)
        tag_bg = THEME_SURFACE_PRIMARY if "P1" in str(row_data["tag"]) else (THEME_SURFACE_SUCCESS if "P2" in str(row_data["tag"]) else THEME_SURFACE_WARNING)
        DLL.DataGrid_SetCellStyle(normal_grid, row, 3, tag_fg, tag_bg, BOOL(False), BOOL(False))
        DLL.DataGrid_SetCellStyle(normal_grid, row, 4, 0xFFFFFFFF, 0xFF409EFF if row == 0 else (0xFF67C23A if row == 1 else 0xFFE6A23C), BOOL(False), BOOL(False))
        DLL.DataGrid_SetCellStyle(normal_grid, row, 5, 0xFF409EFF, 0x00000000, BOOL(False), BOOL(False))
        DLL.DataGrid_SetCellStyle(normal_grid, row, 6, 0xFF409EFF if row == 0 else (0xFF67C23A if row == 1 else 0xFFE6A23C), THEME_SURFACE_PRIMARY if row == 0 else (THEME_SURFACE_SUCCESS if row == 1 else THEME_SURFACE_WARNING), BOOL(False), BOOL(False))
        set_demo_bitmap(row, row)
    apply_demo_cell_styles()

    vcb = DLL._GridVirtualCB(base.on_virtual_grid_request)
    KEEP.append(vcb)
    DLL.DataGrid_SetVirtualDataCallback(virtual_grid, vcb)
    DLL.DataGrid_SetVirtualRowCount(virtual_grid, 1_000_000)

    def on_grid_click(h_grid: HWND, row: int, col: int) -> None:
        grid_local["selected_row"] = row
        grid_local["selected_col"] = col
        text = get_cell_text(h_grid, row, col)
        if h_grid == normal_grid and col == 4:
            base.show_msg("按钮列点击", f"点击了按钮列: row={row}, value={text}", "🔘")
        elif h_grid == normal_grid and col == 5:
            base.show_msg("链接列点击", f"点击了链接列: row={row}, value={text}", "🔗")
        elif h_grid == normal_grid and col == 6:
            base.show_msg("图片列点击", f"点击了 bitmap 图片列: row={row}, alt={text}", "🖼️")
        set_grid_state(f"🧾 单元格点击: row={row}, col={col}, value={text if text else '(空)'}")
        refresh_cell_readout("点击后读取单元格")

    def on_grid_dblclick(_h_grid: HWND, row: int, col: int) -> None:
        set_grid_state(f"🖱️ 双击编辑: row={row}, col={col}")

    def on_grid_change(h_grid: HWND, row: int, col: int) -> None:
        text = get_cell_text(h_grid, row, col)
        set_grid_state(f"✏️ 单元格值变化: row={row}, col={col}, value={text if text else '(空)'}")
        refresh_cell_readout("值变化后读取单元格")

    def on_grid_selection(h_grid: HWND, row: int, col: int) -> None:
        grid_local["selected_row"] = row
        grid_local["selected_col"] = col
        text = get_cell_text(h_grid, row, col)
        set_grid_state(f"🎯 选中单元格: row={row}, col={col}, value={text if text else '(空)'}")
        refresh_cell_readout("选中后读取单元格")

    def toggle_sort(col: int) -> None:
        if bool(grid_local["virtual_mode"]):
            set_grid_state("虚拟表格不做排序演示，请先切回普通表格。")
            return
        current = int(grid_local["sort_states"].get(col, 2))
        next_order = 1 if current != 1 else 2
        grid_local["sort_states"][col] = next_order
        DLL.DataGrid_SortByColumn(normal_grid, col, next_order)
        DLL.DataGrid_Refresh(normal_grid)
        set_grid_state(f"🔀 已按列 {col} {'升序' if next_order == 1 else '降序'} 排序。")
        refresh_cell_readout("排序后读取单元格")

    def on_header_click(h_grid: HWND, col: int) -> None:
        if h_grid == normal_grid:
            toggle_sort(col)
        else:
            set_grid_state(f"📑 虚拟表格列表头点击: col={col}")

    g1 = DLL._GridCB(on_grid_click)
    g2 = DLL._GridCB(on_grid_dblclick)
    g3 = DLL._GridCB(on_grid_change)
    g4 = DLL._GridSelCB(on_grid_selection)
    g5 = DLL._GridHeaderCB(on_header_click)
    KEEP.extend([g1, g2, g3, g4, g5])
    for h_grid in (normal_grid, virtual_grid):
        DLL.DataGrid_SetCellClickCallback(h_grid, g1)
        DLL.DataGrid_SetCellDoubleClickCallback(h_grid, g2)
        DLL.DataGrid_SetSelectionChangedCallback(h_grid, g4)
        DLL.DataGrid_SetColumnHeaderClickCallback(h_grid, g5)
    DLL.DataGrid_SetCellValueChangedCallback(normal_grid, g3)

    def append_row() -> None:
        row_index = DLL.DataGrid_AddRow(normal_grid)
        idx = int(grid_local["row_count"]) + 1
        grid_local["row_count"] = idx
        values = [f"🧾 任务 {idx}", None, "🚧 进行中" if idx % 2 else "🕒 待处理", "🔵 P1" if idx % 2 else "🟢 P2", "执行", "查看详情", f"图片-{idx}", "新插入行，支持完整列型展示"]
        for col, value in enumerate(values):
            if value is None:
                DLL.DataGrid_SetCellChecked(normal_grid, row_index, col, BOOL(idx % 2 == 1))
                continue
            p, n, _ = s(value)
            DLL.DataGrid_SetCellText(normal_grid, row_index, col, p, n)
        set_demo_bitmap(row_index, idx - 1)
        apply_demo_cell_styles()
        update_mode_label()
        set_grid_state(f"➕ 已新增普通表格第 {idx} 行。")

    def clear_rows() -> None:
        DLL.DataGrid_ClearRows(normal_grid)
        grid_local["row_count"] = 0
        DLL.DataGrid_Refresh(normal_grid)
        update_mode_label()
        set_grid_state("🧹 已清空普通表格。")
        refresh_cell_readout("清空后读取单元格")

    def toggle_virtual_mode() -> None:
        use_virtual = not bool(grid_local["virtual_mode"])
        grid_local["virtual_mode"] = use_virtual
        DLL.DataGrid_Show(normal_grid, BOOL(not use_virtual))
        DLL.DataGrid_Show(virtual_grid, BOOL(use_virtual))
        DLL.DataGrid_Refresh(virtual_grid if use_virtual else normal_grid)
        update_mode_label()
        set_grid_state("🚀 已切换到 1,000,000 行虚拟表格。" if use_virtual else f"🧾 已切回普通表格，共 {int(grid_local['row_count'])} 行。")
        refresh_cell_readout("切换模式后读取单元格")

    def toggle_header_style() -> None:
        grid_local["header_dark"] = not bool(grid_local["header_dark"])
        for h_grid in (normal_grid, virtual_grid):
            DLL.DataGrid_SetHeaderStyle(h_grid, 2 if bool(grid_local["header_dark"]) else 0)
            DLL.DataGrid_Refresh(h_grid)
        set_grid_state(f"🎨 已切换表头样式为 {'Dark' if bool(grid_local['header_dark']) else 'Plain'}。")

    def toggle_double_click_edit() -> None:
        grid_local["dblclick_enabled"] = not bool(grid_local["dblclick_enabled"])
        DLL.DataGrid_SetDoubleClickEnabled(normal_grid, BOOL(bool(grid_local["dblclick_enabled"])))
        set_grid_state(f"🖱️ 普通表格双击编辑已{'开启' if bool(grid_local['dblclick_enabled']) else '关闭'}。")

    def toggle_demo_cell_style() -> None:
        grid_local["accent_style"] = not bool(grid_local["accent_style"])
        apply_demo_cell_styles()
        set_grid_state(f"🪄 单元格演示样式已{'开启' if bool(grid_local['accent_style']) else '恢复默认'}。")

    def rename_header(col: int, text: str, *, virtual: bool = False) -> None:
        target = virtual_grid if virtual else normal_grid
        p, n, _ = s(text)
        DLL.DataGrid_SetColumnHeaderText(target, col, p, n)
        DLL.DataGrid_Refresh(target)
        refresh_header_readout("修改表头后读取")
        set_grid_state(f"🗂️ 已修改{'虚拟' if virtual else '普通'}表格列表头 col={col} -> {text}")

    def restore_headers() -> None:
        for idx, text in enumerate(default_normal_headers):
            p, n, _ = s(text)
            DLL.DataGrid_SetColumnHeaderText(normal_grid, idx, p, n)
        for idx, text in enumerate(default_virtual_headers):
            p, n, _ = s(text)
            DLL.DataGrid_SetColumnHeaderText(virtual_grid, idx, p, n)
        DLL.DataGrid_Refresh(normal_grid)
        DLL.DataGrid_Refresh(virtual_grid)
        refresh_header_readout("已恢复默认表头")
        set_grid_state("↩️ 已恢复普通表格和虚拟表格默认表头。")

    def select_cell(row: int, col: int) -> None:
        h_grid = active_grid()
        if not h_grid:
            return
        DLL.DataGrid_SetSelectedCell(h_grid, row, col)
        grid_local["selected_row"] = row
        grid_local["selected_col"] = col
        refresh_cell_readout(f"已定位到 [{row}, {col}]")

    def focus_image_column() -> None:
        if bool(grid_local["virtual_mode"]):
            select_cell(0, 5)
            set_grid_state("🖼️ 已定位到虚拟表格图片列（col=5）。")
            return
        select_cell(0, 6)
        set_grid_state("🖼️ 已定位到普通表格图片列（col=6）。")

    def write_selected_cell() -> None:
        if bool(grid_local["virtual_mode"]):
            set_grid_state("虚拟表格不支持直接改单元格，请先切回普通表格。")
            return
        row = int(DLL.DataGrid_GetSelectedRow(normal_grid))
        col = int(DLL.DataGrid_GetSelectedCol(normal_grid))
        if row < 0 or col < 0:
            row, col = 0, 7
        text = f"🛠️ 已修改 [{row},{col}]"
        p, n, _ = s(text)
        DLL.DataGrid_SetCellText(normal_grid, row, col, p, n)
        DLL.DataGrid_Refresh(normal_grid)
        grid_local["selected_row"] = row
        grid_local["selected_col"] = col
        set_grid_state(f"✏️ 已修改普通表格单元格 [{row}, {col}]。")
        refresh_cell_readout("修改后读取单元格")

    def toggle_selected_checkbox() -> None:
        if bool(grid_local["virtual_mode"]):
            set_grid_state("虚拟表格没有勾选列，请先切回普通表格。")
            return
        row = int(DLL.DataGrid_GetSelectedRow(normal_grid))
        if row < 0:
            row = 0
        current = bool(DLL.DataGrid_GetCellChecked(normal_grid, row, 1))
        DLL.DataGrid_SetCellChecked(normal_grid, row, 1, BOOL(not current))
        DLL.DataGrid_Refresh(normal_grid)
        grid_local["selected_row"] = row
        grid_local["selected_col"] = 1
        set_grid_state(f"☑️ 已切换第 {row} 行勾选状态为 {not current}。")
        refresh_cell_readout("切换勾选后读取单元格")

    def export_csv() -> None:
        export_path = base.repo_root() / "examples" / "Python" / "_datagrid_export_demo.csv"
        p, n, _ = s(str(export_path))
        ok = bool(DLL.DataGrid_ExportCSV(normal_grid, p, n))
        if ok:
            base.set_label_text(export_path_label, f"CSV 已导出:\n{export_path}")
            set_grid_state(f"📤 已导出 CSV -> {export_path}")
        else:
            base.set_label_text(export_path_label, "CSV 导出失败。")
            set_grid_state("CSV 导出失败。")

    menu_ids = {"add": 9301, "clear": 9302, "toggle_virtual": 9303, "read": 9304, "header": 9305}

    def on_grid_menu(_menu_id: int, item_id: int) -> None:
        if item_id == menu_ids["add"]:
            append_row()
        elif item_id == menu_ids["clear"]:
            clear_rows()
        elif item_id == menu_ids["toggle_virtual"]:
            toggle_virtual_mode()
        elif item_id == menu_ids["read"]:
            refresh_cell_readout("右键菜单读取单元格")
            set_grid_state("📄 已通过表格右键菜单读取当前单元格。")
        elif item_id == menu_ids["header"]:
            toggle_header_style()

    grid_menu = DLL.CreateEmojiPopupMenu(page)
    base.menu_add(grid_menu, "➕ 添加一行", menu_ids["add"])
    base.menu_add(grid_menu, "🧹 清空普通表格", menu_ids["clear"])
    base.menu_add(grid_menu, "🚀 切换虚拟表格", menu_ids["toggle_virtual"])
    base.menu_add(grid_menu, "📄 读取当前单元格", menu_ids["read"])
    base.menu_add(grid_menu, "🎨 切换表头样式", menu_ids["header"])
    menu_cb = DLL._MenuCB(on_grid_menu)
    KEEP.append(menu_cb)
    DLL.SetPopupMenuCallback(grid_menu, menu_cb)
    DLL.BindControlMenu(normal_grid, grid_menu)
    DLL.BindControlMenu(virtual_grid, grid_menu)

    base.button(toolbar_panel, "➕", "加一行", 10, 10, 94, 34, 0xFF409EFF, append_row)
    base.button(toolbar_panel, "🧹", "清空表格", 112, 10, 102, 34, 0xFFF56C6C, clear_rows)
    base.button(toolbar_panel, "🚀", "切换虚拟", 222, 10, 102, 34, 0xFF8E44AD, toggle_virtual_mode)
    base.button(toolbar_panel, "🖼️", "定位图片列", 332, 10, 106, 34, 0xFF409EFF, focus_image_column)
    base.button(toolbar_panel, "🔀", "任务排序", 446, 10, 96, 34, 0xFF409EFF, lambda: toggle_sort(0))
    base.button(toolbar_panel, "🖱️", "双击编辑开关", 550, 10, 118, 34, 0xFF909399, toggle_double_click_edit)
    base.button(toolbar_panel, "📤", "导出 CSV", 676, 10, 100, 34, 0xFF67C23A, export_csv)
    base.button(toolbar_panel, "🎨", "单元格样式", 784, 10, 106, 34, 0xFFE6A23C, toggle_demo_cell_style)

    base.label(page, "🗂️ 表头文本真读写", 1096, 312, 240, 22, fg=0xFF303133, bg=0xFFF5F7FA, size=14, bold=True)
    base.button(page, "📄", "读取表头", 1096, 438, 150, 36, 0xFF409EFF, lambda: refresh_header_readout("手动读取表头"))
    base.button(page, "1", "改普通首列", 1262, 438, 174, 36, 0xFFE6A23C, lambda: rename_header(0, "🧩 工单"))
    base.button(page, "7", "改虚拟末列", 1096, 482, 150, 36, 0xFF67C23A, lambda: rename_header(6, "📝 虚拟说明", virtual=True))
    base.button(page, "↩", "恢复默认表头", 1262, 482, 174, 36, 0xFF909399, restore_headers)

    base.label(page, "📄 单元格读取 / 修改", 1096, 522, 240, 22, fg=0xFF303133, bg=0xFFF5F7FA, size=14, bold=True)
    base.button(page, "🎯", "定位 [0,0]", 1096, 594, 150, 34, 0xFF409EFF, lambda: select_cell(0, 0))
    base.button(page, "📍", "定位 [0,7]", 1262, 594, 174, 34, 0xFFE6A23C, lambda: select_cell(0, 7))
    base.button(page, "📝", "修改当前格", 1096, 636, 150, 34, 0xFF8E44AD, write_selected_cell)
    base.button(page, "☑️", "切换勾选", 1262, 636, 174, 34, 0xFF67C23A, toggle_selected_checkbox)
    base.label(page, "🪄 样式 / 双击 / 导出", 1096, 688, 240, 22, fg=0xFF303133, bg=0xFFF5F7FA, size=14, bold=True)
    base.button(page, "🎨", "切换单元格样式", 1096, 716, 110, 34, 0xFF409EFF, toggle_demo_cell_style)
    base.button(page, "🖱️", "双击编辑开关", 1212, 716, 110, 34, 0xFF909399, toggle_double_click_edit)
    base.button(page, "📤", "导出 CSV", 1328, 716, 108, 34, 0xFF67C23A, export_csv)

    refresh_header_readout("初始表头")
    update_mode_label()
    select_cell(0, 0)
    set_grid_state("🧾 表格页已升级：按钮列、链接列、真 bitmap 图片列、排序、导出 CSV、表头 DLL 真接口都已接入。")


def build_page_window(page: HWND) -> None:
    hwnd = STATE["hwnd"]
    base.groupbox(page, "🪟 EmojiWindow 实时属性读取", 16, 16, 984, 246)
    base.groupbox(page, "✏️ 标题 / 尺寸 / 位置快捷设置", 16, 282, 984, 258)
    base.groupbox(page, "🎨 主题 / 标题栏 / 背景色", 1024, 16, 440, 524)
    base.groupbox(page, "📘 Window API 说明", 16, 558, 1448, 230)
    palette = page_palette()
    themed_labels: list[tuple[HWND, str]] = []

    def themed_label(
        text: str,
        x: int,
        y: int,
        w: int,
        h: int,
        *,
        role: str = "text",
        size: int = 13,
        bold: bool = False,
        wrap: bool = False,
    ) -> HWND:
        color = palette["accent"] if role == "accent" else (palette["muted"] if role == "muted" else palette["text"])
        h_label = base.label(page, text, x, y, w, h, fg=color, bg=palette["card_bg"], size=size, bold=bold, wrap=wrap)
        themed_labels.append((h_label, role))
        return h_label

    themed_label("窗口页现在直接读取主窗口本身的实时属性，不再单独放一个标签演示分组。", 40, 56, 860, 24, role="muted")
    themed_label("这里重点覆盖：标题读取、句柄、位置尺寸、可见性、主题色、标题栏背景色、标题栏文字色和客户区背景色。", 40, 90, 930, 24, role="muted")

    readout = themed_label("等待读取窗口属性…", 40, 132, 920, 118, size=13, wrap=True)
    op_state = themed_label("窗口操作状态将在这里更新。", 40, 760, 1360, 22, role="accent")
    window_local: dict[str, object] = {
        "client_bg": int(base.theme_color("background")),
        "client_bg_name": "主题默认背景",
    }

    def apply_window_theme() -> None:
        nonlocal palette
        palette = page_palette()
        for h_label, role in themed_labels:
            color = palette["accent"] if role == "accent" else (palette["muted"] if role == "muted" else palette["text"])
            DLL.SetLabelColor(h_label, color, palette["card_bg"])

    def read_window_title() -> str:
        size = int(DLL.GetWindowTitle(hwnd, None, 0))
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        DLL.GetWindowTitle(hwnd, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    def read_window_bounds() -> tuple[int, int, int, int]:
        x = ctypes.c_int()
        y = ctypes.c_int()
        w = ctypes.c_int()
        h = ctypes.c_int()
        result = int(DLL.GetWindowBounds(hwnd, ctypes.byref(x), ctypes.byref(y), ctypes.byref(w), ctypes.byref(h)))
        if result != 0:
            return 0, 0, 0, 0
        return x.value, y.value, w.value, h.value

    def refresh(note: str = "已刷新窗口属性") -> None:
        name = base.theme_name() or "unknown"
        primary = base.theme_color("primary")
        background = base.theme_color("background")
        title = read_window_title() or "(空标题)"
        x, y, w, h = read_window_bounds()
        visible = "显示" if int(DLL.GetWindowVisible(hwnd)) == 1 else "隐藏"
        titlebar = int(DLL.GetWindowTitlebarColor(hwnd))
        titlebar_desc = "跟随主题" if titlebar == 0 else f"0xFF{titlebar:06X}"
        titlebar_text = int(DLL.GetTitleBarTextColor(hwnd))
        titlebar_text_desc = "跟随主题" if titlebar_text == 0 else f"0x{titlebar_text:08X}"
        client_bg = int(window_local["client_bg"])
        client_bg_name = str(window_local["client_bg_name"])
        base.set_label_text(
            readout,
            f"标题: {title}\n"
            f"句柄: 0x{base.hwnd_key(hwnd):X}    可见性: {visible}\n"
            f"位置尺寸: x={x}, y={y}, w={w}, h={h}\n"
            f"当前主题: {name}    primary=0x{primary:08X}    theme.background=0x{background:08X}\n"
            f"标题栏背景: {titlebar_desc}    标题栏文字: {titlebar_text_desc}\n"
            f"最近一次客户区背景: {client_bg_name} / 0x{client_bg:08X}"
        )
        base.set_label_text(op_state, note)
        base.set_status(note)

    def set_title(text: str, note: str) -> None:
        p, n, _ = s(text)
        DLL.set_window_title(hwnd, p, n)
        refresh(note)

    def set_bounds(width: int, height: int, note: str, dx: int = 0, dy: int = 0) -> None:
        x, y, _, _ = read_window_bounds()
        DLL.SetWindowBounds(hwnd, x + dx, y + dy, width, height)
        relayout_shell(width, height)
        refresh(note)

    def set_titlebar(color: int, note: str) -> None:
        DLL.set_window_titlebar_color(hwnd, color)
        refresh(note)

    def set_titlebar_text(color: int, note: str) -> None:
        DLL.SetTitleBarTextColor(hwnd, color)
        refresh(note)

    def set_client_bg(color: int, name: str, note: str) -> None:
        window_local["client_bg"] = color
        window_local["client_bg_name"] = name
        DLL.SetWindowBackgroundColor(hwnd, color)
        refresh(note)

    def set_theme(dark: bool, note: str) -> None:
        set_shell_redraw(False)
        try:
            DLL.SetDarkMode(BOOL(dark))
            if str(window_local["client_bg_name"]) == "主题默认背景":
                window_local["client_bg"] = int(base.theme_color("background"))
            apply_window_theme()
            refresh_theme_visuals(refresh_now=False)
        finally:
            set_shell_redraw(True)
        refresh_visible_shell()
        refresh(note)

    def reset_position() -> None:
        _, _, w, h = read_window_bounds()
        DLL.SetWindowBounds(hwnd, 40, 40, w, h)
        relayout_shell(w, h)
        refresh("窗口位置已恢复到 (40, 40)")

    themed_label("📝 标题预设", 40, 324, 180, 22, size=15, bold=True)
    base.button(page, "🪟", "产品标题", 40, 360, 146, 36, 0xFF409EFF, lambda: set_title("🪟 Tree AllDemo Enhanced / 产品演示窗口", "窗口标题已切到产品演示风格"))
    base.button(page, "🛠️", "调试标题", 202, 360, 146, 36, 0xFF67C23A, lambda: set_title("🛠️ EmojiWindow Debug Surface / 属性回归中", "窗口标题已切到调试风格"))
    base.button(page, "✨", "彩色标题", 364, 360, 146, 36, 0xFF8E44AD, lambda: set_title("✨ EmojiWindow 属性页 / 🌈 Unicode 彩色标题", "窗口标题已切到彩色 Unicode 方案"))

    themed_label("📐 尺寸预设", 40, 414, 180, 22, size=15, bold=True)
    base.button(page, "📦", "紧凑 1600x900", 40, 450, 176, 36, 0xFFE6A23C, lambda: set_bounds(1600, 900, "窗口尺寸已切到紧凑演示 1600x900"))
    base.button(page, "🖥️", "标准 1820x980", 232, 450, 176, 36, 0xFF409EFF, lambda: set_bounds(WINDOW_W, WINDOW_H, "窗口尺寸已恢复到标准 1820x980"))
    base.button(page, "🧱", "加宽 1920x1040", 424, 450, 176, 36, 0xFF67C23A, lambda: set_bounds(1920, 1040, "窗口尺寸已切到加宽展示 1920x1040"))

    themed_label("📍 位置调整", 640, 324, 180, 22, size=15, bold=True)
    base.button(page, "↖️", "恢复到 40,40", 640, 360, 156, 36, 0xFF909399, reset_position)
    base.button(page, "➡️", "向右移动 80", 812, 360, 156, 36, 0xFF409EFF, lambda: set_bounds(read_window_bounds()[2], read_window_bounds()[3], "窗口已向右移动 80 像素", dx=80))
    base.button(page, "⬇️", "向下移动 60", 640, 406, 156, 36, 0xFF67C23A, lambda: set_bounds(read_window_bounds()[2], read_window_bounds()[3], "窗口已向下移动 60 像素", dy=60))
    base.button(page, "📡", "立即读取", 812, 406, 156, 36, 0xFF8E44AD, lambda: refresh("已重新读取窗口当前属性"))

    themed_label("☀️ / 🌙 主题切换", 1048, 56, 180, 22, size=15, bold=True)
    base.button(page, "☀️", "浅色主题", 1048, 90, 176, 36, 0xFF409EFF, lambda: set_theme(False, "主窗口主题已切到浅色"))
    base.button(page, "🌙", "深色主题", 1240, 90, 176, 36, 0xFF303133, lambda: set_theme(True, "主窗口主题已切到深色"))

    themed_label("🎨 标题栏背景色", 1048, 144, 180, 22, size=15, bold=True)
    base.button(page, "💙", "科技蓝", 1048, 178, 112, 36, 0xFF409EFF, lambda: set_titlebar(0xFF409EFF, "标题栏背景已切到科技蓝"))
    base.button(page, "🖤", "深空黑", 1174, 178, 112, 36, 0xFF303133, lambda: set_titlebar(0xFF2B2F36, "标题栏背景已切到深空黑"))
    base.button(page, "💚", "青绿色", 1300, 178, 112, 36, 0xFF67C23A, lambda: set_titlebar(0xFF27AE60, "标题栏背景已切到青绿色"))

    themed_label("🅰️ 标题栏文字色", 1048, 232, 220, 22, size=15, bold=True)
    base.button(page, "🤍", "亮字", 1048, 266, 86, 36, 0xFF909399, lambda: set_titlebar_text(0xFFFFFFFF, "标题栏文字已切到亮色"))
    base.button(page, "🖤", "暗字", 1142, 266, 86, 36, 0xFF303133, lambda: set_titlebar_text(0xFF1D1E1F, "标题栏文字已切到暗色"))
    base.button(page, "💙", "蓝字", 1236, 266, 86, 36, 0xFF409EFF, lambda: set_titlebar_text(0xFF8CC5FF, "标题栏文字已切到蓝色"))
    base.button(page, "↺", "跟随", 1330, 266, 86, 36, 0xFF67C23A, lambda: set_titlebar_text(0, "标题栏文字已恢复为跟随主题"))
    themed_label("0 = 跟随当前主题自动对比。", 1048, 312, 260, 20, role="muted")

    themed_label("🧩 客户区背景", 1048, 348, 180, 22, size=15, bold=True)
    base.button(page, "🤍", "纯白背景", 1048, 382, 112, 36, 0xFF67C23A, lambda: set_client_bg(0xFFFFFFFF, "纯白", "客户区背景已切到纯白"))
    base.button(page, "🩶", "灰蓝背景", 1174, 382, 112, 36, 0xFF909399, lambda: set_client_bg(0xFFF5F7FA, "灰蓝", "客户区背景已切到默认灰蓝"))
    base.button(page, "🌘", "深色背景", 1300, 382, 112, 36, 0xFF303133, lambda: set_client_bg(0xFF1F2329, "深色", "客户区背景已切到深色演示底色"))

    themed_label("1. set_window_title / GetWindowTitle：读取和修改主窗口标题。", 40, 598, 640, 24)
    themed_label("2. GetWindowBounds / SetWindowBounds：直接读取和修改窗口位置与尺寸。", 40, 632, 700, 24)
    themed_label("3. GetWindowVisible：读取窗口当前可见状态，这里用实时面板展示。", 40, 666, 660, 24)
    themed_label("4. set_window_titlebar_color / GetWindowTitlebarColor：标题栏背景色读写。", 40, 700, 720, 24)
    themed_label("5. SetTitleBarTextColor / GetTitleBarTextColor：标题栏文字颜色读取与设置。", 40, 734, 760, 24)
    themed_label("6. SetWindowBackgroundColor / SetDarkMode：客户区底色和主题切换联动演示。", 760, 632, 660, 24)
    themed_label("7. 这一页专门保留 Unicode 彩色文案与按钮，用来验证主窗口级改动不会影响彩色 emoji 展示。", 760, 672, 620, 48, role="muted", wrap=True)

    apply_window_theme()
    refresh("窗口页已加载，可直接测试窗口属性读取与设置")


def build_page_button(page: HWND) -> None:
    base.groupbox(page, "🔘 EmojiButton 属性读取", 16, 16, 980, 248)
    base.groupbox(page, "🛠️ 按钮快捷设置", 16, 286, 980, 254)
    base.groupbox(page, "🎨 样式 / 可见性 / 启用态", 1020, 212, 444, 328)
    base.groupbox(page, "📘 Button API 说明", 16, 558, 1448, 230)

    state_text = base.label(page, "按钮页状态将在这里更新。", 40, 760, 1360, 22, fg=0xFF409EFF, bg=0xFFF5F7FA)
    readout = base.label(page, "等待读取按钮属性…", 40, 184, 920, 56, fg=0xFF303133, bg=0xFFF5F7FA, wrap=True)
    base.label(page, "这一页直接读取按钮文本、emoji、位置大小、颜色、类型、样式、尺寸、圆角、可见性和启用状态。", 40, 56, 900, 24, fg=0xFF606266, bg=0xFFF5F7FA)

    def read_utf8(getter, target: int) -> str:
        size = int(getter(target, None, 0))
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        getter(target, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    demo_btn = base.button(page, "🚀", "主操作按钮", 56, 122, 208, 44, 0xFF409EFF, lambda: refresh("主演示按钮被点击"))

    def read_bounds() -> tuple[int, int, int, int]:
        x = ctypes.c_int()
        y = ctypes.c_int()
        w = ctypes.c_int()
        h = ctypes.c_int()
        if int(DLL.GetButtonBounds(int(demo_btn), ctypes.byref(x), ctypes.byref(y), ctypes.byref(w), ctypes.byref(h))) != 0:
            return 0, 0, 0, 0
        return x.value, y.value, w.value, h.value

    hover_bg = UINT32()
    hover_border = UINT32()
    hover_text = UINT32()
    DLL.GetButtonHoverColors(int(demo_btn), ctypes.byref(hover_bg), ctypes.byref(hover_border), ctypes.byref(hover_text))
    initial = {
        "text": read_utf8(DLL.GetButtonText, int(demo_btn)),
        "emoji": read_utf8(DLL.GetButtonEmoji, int(demo_btn)),
        "bounds": read_bounds(),
        "bg": int(DLL.GetButtonBackgroundColor(int(demo_btn))),
        "text_color": int(DLL.GetButtonTextColor(int(demo_btn))),
        "border": int(DLL.GetButtonBorderColor(int(demo_btn))),
        "hover": (int(hover_bg.value), int(hover_border.value), int(hover_text.value)),
        "type": int(DLL.GetButtonType(int(demo_btn))),
        "style": int(DLL.GetButtonStyle(int(demo_btn))),
        "size": int(DLL.GetButtonSize(int(demo_btn))),
        "round": bool(DLL.GetButtonRound(int(demo_btn))),
        "circle": bool(DLL.GetButtonCircle(int(demo_btn))),
        "loading": bool(DLL.GetButtonLoading(int(demo_btn))),
    }

    def refresh(note: str = "已刷新按钮属性") -> None:
        x, y, w, h = read_bounds()
        text = read_utf8(DLL.GetButtonText, int(demo_btn))
        emoji = read_utf8(DLL.GetButtonEmoji, int(demo_btn))
        bg = int(DLL.GetButtonBackgroundColor(int(demo_btn)))
        fg = int(DLL.GetButtonTextColor(int(demo_btn)))
        border = int(DLL.GetButtonBorderColor(int(demo_btn)))
        visible = "显示" if bool(DLL.GetButtonVisible(int(demo_btn))) else "隐藏"
        enabled = "启用" if bool(DLL.GetButtonEnabled(int(demo_btn))) else "禁用"
        type_name = {0: "default", 1: "primary", 2: "success", 3: "warning", 4: "danger", 5: "info"}.get(int(DLL.GetButtonType(int(demo_btn))), "unknown")
        style_name = {0: "solid", 1: "plain", 2: "text", 3: "link"}.get(int(DLL.GetButtonStyle(int(demo_btn))), "unknown")
        size_name = {0: "large", 1: "default", 2: "small"}.get(int(DLL.GetButtonSize(int(demo_btn))), "unknown")
        base.set_label_text(
            readout,
            f"text={text}    emoji={emoji}    {visible}/{enabled}\n"
            f"bounds=({x}, {y}, {w}, {h})  type={type_name}  style={style_name}  size={size_name}  "
            f"round={int(bool(DLL.GetButtonRound(int(demo_btn))))}  circle={int(bool(DLL.GetButtonCircle(int(demo_btn))))}  loading={int(bool(DLL.GetButtonLoading(int(demo_btn))))}\n"
            f"bg=0x{bg:08X}  fg=0x{fg:08X}  border=0x{border:08X}"
        )
        base.set_label_text(state_text, note)
        base.set_status(note)

    def set_btn_text(text: str, note: str) -> None:
        DLL.SetButtonText(int(demo_btn), *s(text)[:2])
        refresh(note)

    def set_btn_emoji(text: str, note: str) -> None:
        DLL.SetButtonEmoji(int(demo_btn), *s(text)[:2])
        refresh(note)

    def set_btn_colors(bg: int, fg: int, border: int, note: str) -> None:
        DLL.SetButtonBackgroundColor(int(demo_btn), bg)
        DLL.SetButtonTextColor(int(demo_btn), fg)
        DLL.SetButtonBorderColor(int(demo_btn), border)
        DLL.SetButtonHoverColors(int(demo_btn), bg, border, fg)
        refresh(note)

    def move_btn(dx: int = 0, dy: int = 0, dw: int = 0) -> None:
        x, y, w, h = read_bounds()
        DLL.SetButtonBounds(int(demo_btn), x + dx, y + dy, w + dw, h)
        refresh(f"按钮位置/尺寸已更新: dx={dx}, dy={dy}, dw={dw}")

    def restore_btn() -> None:
        x, y, w, h = initial["bounds"]
        DLL.SetButtonText(int(demo_btn), *s(str(initial["text"]))[:2])
        DLL.SetButtonEmoji(int(demo_btn), *s(str(initial["emoji"]))[:2])
        DLL.SetButtonBounds(int(demo_btn), int(x), int(y), int(w), int(h))
        DLL.SetButtonBackgroundColor(int(demo_btn), int(initial["bg"]))
        DLL.ResetButtonColorOverrides(int(demo_btn))
        DLL.SetButtonType(int(demo_btn), int(initial["type"]))
        DLL.SetButtonStyle(int(demo_btn), int(initial["style"]))
        DLL.SetButtonSize(int(demo_btn), int(initial["size"]))
        DLL.SetButtonRound(int(demo_btn), BOOL(bool(initial["round"])))
        DLL.SetButtonCircle(int(demo_btn), BOOL(bool(initial["circle"])))
        DLL.SetButtonLoading(int(demo_btn), BOOL(bool(initial["loading"])))
        DLL.ShowButton(int(demo_btn), BOOL(True))
        DLL.EnableButton(page, int(demo_btn), BOOL(True))
        refresh("按钮属性已恢复默认")

    base.label(page, "📝 文本 / Emoji", 40, 326, 180, 22, fg=0xFF303133, bg=0xFFF5F7FA, size=15, bold=True)
    base.button(page, "📝", "改成保存草稿", 40, 360, 156, 36, 0xFF409EFF, lambda: set_btn_text("保存草稿", "按钮文本已改成“保存草稿”"))
    base.button(page, "✨", "改成立即发布", 212, 360, 156, 36, 0xFF67C23A, lambda: set_btn_text("立即发布", "按钮文本已改成“立即发布”"))
    base.button(page, "🎯", "切换 Emoji", 384, 360, 156, 36, 0xFF8E44AD, lambda: set_btn_emoji("🎯", "按钮 emoji 已切到 🎯"))

    base.label(page, "📐 位置 / 尺寸", 40, 414, 180, 22, fg=0xFF303133, bg=0xFFF5F7FA, size=15, bold=True)
    base.button(page, "➡️", "右移 80", 40, 448, 140, 36, 0xFFE6A23C, lambda: move_btn(dx=80))
    base.button(page, "⬇️", "下移 24", 196, 448, 140, 36, 0xFF409EFF, lambda: move_btn(dy=24))
    base.button(page, "↔️", "加宽 60", 352, 448, 140, 36, 0xFF67C23A, lambda: move_btn(dw=60))
    base.button(page, "↺", "恢复默认", 508, 448, 140, 36, 0xFF909399, restore_btn)

    base.label(page, "🎨 颜色 / 样式", 1044, 252, 180, 22, fg=0xFF303133, bg=0xFFF5F7FA, size=15, bold=True)
    base.button(page, "💙", "冷色", 1044, 286, 118, 36, 0xFF409EFF, lambda: set_btn_colors(THEME_PRIMARY, 0xFFFFFFFF, THEME_PRIMARY, "按钮已切到冷色方案"))
    base.button(page, "🧡", "暖色", 1176, 286, 118, 36, 0xFFE6A23C, lambda: set_btn_colors(THEME_WARNING, 0xFFFFFFFF, THEME_WARNING, "按钮已切到暖色方案"))
    base.button(page, "🌫️", "浅灰", 1308, 286, 118, 36, 0xFF909399, lambda: set_btn_colors(THEME_SURFACE, THEME_MUTED, THEME_BORDER_LIGHT, "按钮已切到浅灰方案"))
    base.button(page, "🫧", "Plain", 1044, 336, 118, 36, 0xFF409EFF, lambda: (DLL.SetButtonStyle(int(demo_btn), base.BUTTON_STYLE_PLAIN), refresh("按钮样式已切到 plain")))
    base.button(page, "🔗", "Link", 1176, 336, 118, 36, 0xFF67C23A, lambda: (DLL.SetButtonStyle(int(demo_btn), base.BUTTON_STYLE_LINK), refresh("按钮样式已切到 link")))
    base.button(page, "🧱", "Solid", 1308, 336, 118, 36, 0xFF909399, lambda: (DLL.SetButtonStyle(int(demo_btn), 0), refresh("按钮样式已切回 solid")))

    base.label(page, "⚙️ 行为状态", 1044, 390, 180, 22, fg=0xFF303133, bg=0xFFF5F7FA, size=15, bold=True)
    base.button(page, "⭕", "Round", 1044, 424, 118, 36, 0xFF409EFF, lambda: (DLL.SetButtonRound(int(demo_btn), BOOL(True)), DLL.SetButtonCircle(int(demo_btn), BOOL(False)), refresh("按钮已切到 round")))
    base.button(page, "⚪", "Circle", 1176, 424, 118, 36, 0xFF67C23A, lambda: (DLL.SetButtonCircle(int(demo_btn), BOOL(True)), refresh("按钮已切到 circle")))
    base.button(page, "⏳", "Loading", 1308, 424, 118, 36, 0xFF8E44AD, lambda: (DLL.SetButtonLoading(int(demo_btn), BOOL(not bool(DLL.GetButtonLoading(int(demo_btn))))), refresh("按钮 loading 状态已切换")))
    base.button(page, "🚫", "禁用/启用", 1044, 474, 118, 36, 0xFFE6A23C, lambda: (DLL.EnableButton(page, int(demo_btn), BOOL(not bool(DLL.GetButtonEnabled(int(demo_btn))))), refresh("按钮启用状态已切换")))
    base.button(page, "👁️", "显示/隐藏", 1176, 474, 118, 36, 0xFF909399, lambda: (DLL.ShowButton(int(demo_btn), BOOL(not bool(DLL.GetButtonVisible(int(demo_btn))))), refresh("按钮可见状态已切换")))
    base.button(page, "📏", "Large", 1308, 474, 118, 36, 0xFF409EFF, lambda: (DLL.SetButtonSize(int(demo_btn), base.BUTTON_SIZE_LARGE), refresh("按钮尺寸已切到 large")))

    base.label(page, "1. GetButtonText / GetButtonEmoji / GetButtonBounds：读取文本、emoji 和位置尺寸。", 40, 598, 760, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "2. SetButtonText / SetButtonEmoji / SetButtonBounds：直接修改按钮文案与布局。", 40, 632, 760, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "3. GetButtonBackgroundColor / TextColor / BorderColor：读取按钮三类颜色。", 40, 666, 760, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "4. SetButtonStyle / SetButtonType / SetButtonSize / SetButtonRound / SetButtonCircle / SetButtonLoading：读取和切换样式。", 40, 700, 940, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "5. ShowButton / EnableButton：这里直接做真状态切换，不是静态文案。", 40, 734, 760, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    refresh("按钮页已加载，可直接测试按钮属性读取与设置")


def build_page_label(page: HWND) -> None:
    build_label_property_demo(page, "标签页标签演示", 1020, 16, 444, 176)
    base.groupbox(page, "🏷️ Label 实时属性读取", 16, 16, 980, 248)
    base.groupbox(page, "🛠️ 文本 / 颜色 / 位置 / 字体", 16, 286, 980, 254)
    base.groupbox(page, "📐 Label 状态开关", 1020, 212, 444, 328)
    base.groupbox(page, "📘 Label API 说明", 16, 558, 1448, 230)

    demo_label = base.label(page, "🏷️ 这是主演示标签：支持 Unicode 彩色文案和属性读取。", 56, 124, 560, 36, fg=0xFF303133, bg=0xFFEAF3FF, size=15, bold=True)
    readout = base.label(page, "等待读取标签属性…", 40, 184, 920, 56, fg=0xFF303133, bg=0xFFF5F7FA, wrap=True)
    state_text = base.label(page, "标签页状态将在这里更新。", 40, 760, 1360, 22, fg=0xFF409EFF, bg=0xFFF5F7FA)
    base.label(page, "标签页现在直接展示 Label 的文本、颜色、位置、字体、对齐、可见性和启用态读取。", 40, 56, 900, 24, fg=0xFF606266, bg=0xFFF5F7FA)

    def read_utf8_label() -> str:
        size = int(DLL.GetLabelText(demo_label, None, 0))
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        DLL.GetLabelText(demo_label, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    def read_label_bounds() -> tuple[int, int, int, int]:
        x = ctypes.c_int()
        y = ctypes.c_int()
        w = ctypes.c_int()
        h = ctypes.c_int()
        if int(DLL.GetLabelBounds(demo_label, ctypes.byref(x), ctypes.byref(y), ctypes.byref(w), ctypes.byref(h))) != 0:
            return 0, 0, 0, 0
        return x.value, y.value, w.value, h.value

    def read_label_font() -> tuple[str, int, int, int, int]:
        buf = ctypes.create_string_buffer(128)
        size = ctypes.c_int()
        bold = ctypes.c_int()
        italic = ctypes.c_int()
        underline = ctypes.c_int()
        result = int(DLL.GetLabelFont(demo_label, buf, 128, ctypes.byref(size), ctypes.byref(bold), ctypes.byref(italic), ctypes.byref(underline)))
        name = buf.raw[:max(result, 0)].decode("utf-8", errors="replace") if result > 0 else ""
        return name, size.value, bold.value, italic.value, underline.value

    fg0 = UINT32()
    bg0 = UINT32()
    DLL.GetLabelColor(demo_label, ctypes.byref(fg0), ctypes.byref(bg0))
    initial = {
        "text": read_utf8_label(),
        "bounds": read_label_bounds(),
        "fg": int(fg0.value),
        "bg": int(bg0.value),
        "alignment": max(0, int(DLL.GetLabelAlignment(demo_label))),
    }

    def refresh(note: str = "已刷新标签属性") -> None:
        fg = UINT32()
        bg = UINT32()
        DLL.GetLabelColor(demo_label, ctypes.byref(fg), ctypes.byref(bg))
        x, y, w, h = read_label_bounds()
        font_name, font_size, bold, italic, underline = read_label_font()
        align_name = base.alignment_name(int(DLL.GetLabelAlignment(demo_label)))
        enabled = "启用" if int(DLL.GetLabelEnabled(demo_label)) == 1 else "禁用"
        visible = "显示" if int(DLL.GetLabelVisible(demo_label)) == 1 else "隐藏"
        base.set_label_text(
            readout,
            f"text={read_utf8_label()}  {visible}/{enabled}\n"
            f"bounds=({x}, {y}, {w}, {h})  align={align_name}  font={font_name or 'default'} {font_size}px b/i/u={bold}/{italic}/{underline}\n"
            f"fg=0x{int(fg.value):08X}  bg=0x{int(bg.value):08X}"
        )
        base.set_label_text(state_text, note)
        base.set_status(note)

    def set_label_text_value(text: str, note: str) -> None:
        DLL.SetLabelText(demo_label, *s(text)[:2])
        refresh(note)

    def set_label_colors(fg: int, bg: int, note: str) -> None:
        DLL.SetLabelColor(demo_label, fg, bg)
        refresh(note)

    def set_label_font(font_name: str, font_size: int, bold: bool, note: str) -> None:
        DLL.SetLabelFont(demo_label, *s(font_name)[:2], font_size, BOOL(bold), BOOL(False), BOOL(False))
        refresh(note)

    def move_label(dx: int = 0, dy: int = 0, dw: int = 0) -> None:
        x, y, w, h = read_label_bounds()
        DLL.SetLabelBounds(demo_label, x + dx, y + dy, w + dw, h)
        refresh(f"标签位置/尺寸已更新: dx={dx}, dy={dy}, dw={dw}")

    def set_label_alignment(align: int, note: str) -> None:
        DLL.SetLabelAlignment(demo_label, align)
        refresh(note)

    def restore_label() -> None:
        x, y, w, h = initial["bounds"]
        DLL.SetLabelText(demo_label, *s(str(initial["text"]))[:2])
        DLL.SetLabelColor(demo_label, int(initial["fg"]), int(initial["bg"]))
        DLL.SetLabelBounds(demo_label, int(x), int(y), int(w), int(h))
        DLL.SetLabelAlignment(demo_label, int(initial["alignment"]))
        DLL.SetLabelFont(demo_label, *s("Segoe UI Emoji")[:2], 15, BOOL(True), BOOL(False), BOOL(False))
        DLL.EnableLabel(demo_label, BOOL(True))
        DLL.ShowLabel(demo_label, BOOL(True))
        refresh("标签属性已恢复默认")

    base.label(page, "📝 文本预设", 40, 326, 180, 22, fg=0xFF303133, bg=0xFFF5F7FA, size=15, bold=True)
    base.button(page, "💬", "说明标签", 40, 360, 146, 36, 0xFF409EFF, lambda: set_label_text_value("💬 当前标签已切到说明文案模式。", "标签文本已切到说明模式"))
    base.button(page, "📣", "强调标签", 202, 360, 146, 36, 0xFF67C23A, lambda: set_label_text_value("📣 当前标签是强调提示，用于展示高关注状态。", "标签文本已切到强调模式"))
    base.button(page, "🌈", "彩色标签", 364, 360, 146, 36, 0xFF8E44AD, lambda: set_label_text_value("🌈 Unicode 标签：🚀 ✅ 📘 🧩", "标签文本已切到 Unicode 彩色模式"))

    base.label(page, "🎨 颜色 / 字体", 40, 414, 180, 22, fg=0xFF303133, bg=0xFFF5F7FA, size=15, bold=True)
    base.button(page, "💙", "冷色", 40, 448, 118, 36, 0xFF409EFF, lambda: set_label_colors(THEME_PRIMARY, THEME_SURFACE_PRIMARY, "标签已切到冷色方案"))
    base.button(page, "🧡", "暖色", 172, 448, 118, 36, 0xFFE6A23C, lambda: set_label_colors(THEME_WARNING, THEME_SURFACE_WARNING, "标签已切到暖色方案"))
    base.button(page, "🔤", "18px Bold", 304, 448, 118, 36, 0xFF67C23A, lambda: set_label_font("Segoe UI Emoji", 18, True, "标签字体已切到 18px Bold"))
    base.button(page, "🔡", "14px", 436, 448, 118, 36, 0xFF909399, lambda: set_label_font("Segoe UI Emoji", 14, False, "标签字体已切到 14px"))

    base.label(page, "📐 位置 / 状态", 1044, 252, 180, 22, fg=0xFF303133, bg=0xFFF5F7FA, size=15, bold=True)
    base.button(page, "➡️", "右移 80", 1044, 286, 118, 36, 0xFF409EFF, lambda: move_label(dx=80))
    base.button(page, "⬇️", "下移 20", 1176, 286, 118, 36, 0xFF67C23A, lambda: move_label(dy=20))
    base.button(page, "↔️", "加宽 120", 1308, 286, 118, 36, 0xFFE6A23C, lambda: move_label(dw=120))
    base.label(page, "↔️ 对齐 SetLabelAlignment(0/1/2)", 1044, 318, 380, 22, fg=0xFF303133, bg=0xFFF5F7FA, size=14, bold=True)
    base.button(page, "◀️", "左对齐", 1044, 348, 118, 36, 0xFF409EFF, lambda: set_label_alignment(base.ALIGN_LEFT, "对齐已设为左"))
    base.button(page, "⏺", "居中", 1176, 348, 118, 36, 0xFF67C23A, lambda: set_label_alignment(base.ALIGN_CENTER, "对齐已设为居中"))
    base.button(page, "▶️", "右对齐", 1308, 348, 118, 36, 0xFFE6A23C, lambda: set_label_alignment(base.ALIGN_RIGHT, "对齐已设为右"))
    base.button(page, "🚫", "禁用/启用", 1044, 394, 118, 36, 0xFF8E44AD, lambda: (DLL.EnableLabel(demo_label, BOOL(not (int(DLL.GetLabelEnabled(demo_label)) == 1))), refresh("标签启用状态已切换")))
    base.button(page, "👁️", "显示/隐藏", 1176, 394, 118, 36, 0xFF909399, lambda: (DLL.ShowLabel(demo_label, BOOL(not (int(DLL.GetLabelVisible(demo_label)) == 1))), refresh("标签可见状态已切换")))
    base.button(page, "↺", "恢复默认", 1308, 394, 118, 36, 0xFF409EFF, restore_label)
    base.label(page, "「恢复默认」会连同对齐方式一并还原为进入本页时记录的值。", 1044, 438, 382, 44, fg=0xFF606266, bg=0xFFF5F7FA, wrap=True)

    base.label(
        page,
        "DLL 导出（与本页演示对应）：CreateLabel（创建时指定 alignment、word_wrap）；"
        "GetLabelText / SetLabelText；GetLabelColor / SetLabelColor；GetLabelBounds / SetLabelBounds；"
        "GetLabelFont / SetLabelFont（字体名 UTF-8、字号、粗/斜/下划线）；GetLabelAlignment / SetLabelAlignment（0=左 1=中 2=右）；"
        "GetLabelEnabled / EnableLabel；GetLabelVisible / ShowLabel。",
        40,
        598,
        1360,
        120,
        fg=0xFF303133,
        bg=0xFFF5F7FA,
        wrap=True,
    )
    refresh("标签页已加载，可直接测试标签属性读取与设置")




def build_page_color_emoji_edit(page: HWND) -> None:
    build_label_property_demo(page, "彩色 Emoji 编辑框页标签演示", 1020, 16, 444, 176)
    base.groupbox(page, "🌈 ColorEmojiEditBox 实时属性读取", 16, 16, 980, 248)
    base.groupbox(page, "🛠️ 文本 / 颜色 / 尺寸 / 状态", 16, 286, 980, 254)
    base.groupbox(page, "✨ 彩色 Emoji 能力说明", 1020, 212, 444, 328)
    base.groupbox(page, "📘 ColorEmojiEditBox API 说明", 16, 558, 1448, 230)

    demo_edit = base.edit(page, "🌈 ColorEmojiEditBox：😀🚀📘✅", 56, 120, 460, 40, True)
    preview_edit = base.edit(page, "🧪 第二组彩色内容：🎯🪄🫧🎉", 1044, 262, 380, 40, True)
    readout = base.label(page, "等待读取彩色编辑框属性…", 40, 184, 920, 56, fg=0xFF303133, bg=0xFFF5F7FA, wrap=True)
    state_text = base.label(page, "彩色 Emoji 编辑框页状态将在这里更新。", 40, 760, 1360, 22, fg=0xFF409EFF, bg=0xFFF5F7FA)
    base.label(page, "这一页直接用真接口读取彩色 Emoji 编辑框的文本、颜色、位置、字体、启用态和可见态。", 40, 56, 900, 24, fg=0xFF606266, bg=0xFFF5F7FA)

    def read_text(h_edit: HWND) -> str:
        size = int(DLL.GetEditBoxText(h_edit, None, 0))
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        DLL.GetEditBoxText(h_edit, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    def read_bounds() -> tuple[int, int, int, int]:
        x = ctypes.c_int()
        y = ctypes.c_int()
        w = ctypes.c_int()
        h = ctypes.c_int()
        if int(DLL.GetEditBoxBounds(demo_edit, ctypes.byref(x), ctypes.byref(y), ctypes.byref(w), ctypes.byref(h))) != 0:
            return 0, 0, 0, 0
        return x.value, y.value, w.value, h.value

    def read_font() -> tuple[str, int, int]:
        buf = ctypes.create_string_buffer(128)
        size = ctypes.c_int()
        bold = ctypes.c_int()
        italic = ctypes.c_int()
        underline = ctypes.c_int()
        result = int(DLL.GetEditBoxFont(demo_edit, buf, 128, ctypes.byref(size), ctypes.byref(bold), ctypes.byref(italic), ctypes.byref(underline)))
        name = buf.raw[:max(result, 0)].decode("utf-8", errors="replace") if result > 0 else ""
        return name, size.value, bold.value

    fg0 = UINT32()
    bg0 = UINT32()
    DLL.GetEditBoxColor(demo_edit, ctypes.byref(fg0), ctypes.byref(bg0))
    initial = {"text": read_text(demo_edit), "bounds": read_bounds(), "fg": int(fg0.value), "bg": int(bg0.value)}

    def refresh(note: str = "已刷新彩色 Emoji 编辑框属性") -> None:
        fg = UINT32()
        bg = UINT32()
        DLL.GetEditBoxColor(demo_edit, ctypes.byref(fg), ctypes.byref(bg))
        x, y, w, h = read_bounds()
        font_name, font_size, bold = read_font()
        enabled = "启用" if int(DLL.GetEditBoxEnabled(demo_edit)) == 1 else "禁用"
        visible = "显示" if int(DLL.GetEditBoxVisible(demo_edit)) == 1 else "隐藏"
        base.set_label_text(
            readout,
            f"text={read_text(demo_edit)}  {visible}/{enabled}\n"
            f"bounds=({x}, {y}, {w}, {h})  font={font_name or 'default'} {font_size}px bold={bold}\n"
            f"fg=0x{int(fg.value):08X}  bg=0x{int(bg.value):08X}"
        )
        base.set_label_text(state_text, note)
        base.set_status(note)

    def set_text_value(text: str, note: str) -> None:
        DLL.SetEditBoxText(demo_edit, *s(text)[:2])
        DLL.SetEditBoxText(preview_edit, *s("🔁 预览区同步： " + text)[:2])
        refresh(note)

    def set_colors(fg: int, bg: int, note: str) -> None:
        DLL.SetEditBoxColor(demo_edit, fg, bg)
        refresh(note)

    def set_font_value(size: int, bold: bool, note: str) -> None:
        DLL.SetEditBoxFont(demo_edit, *s("Segoe UI Emoji")[:2], size, BOOL(bold), BOOL(False), BOOL(False))
        refresh(note)

    def move_box(dx: int = 0, dy: int = 0, dw: int = 0) -> None:
        x, y, w, h = read_bounds()
        DLL.SetEditBoxBounds(demo_edit, x + dx, y + dy, w + dw, h)
        refresh(f"彩色编辑框位置/尺寸已更新: dx={dx}, dy={dy}, dw={dw}")

    def restore_box() -> None:
        x, y, w, h = initial["bounds"]
        DLL.SetEditBoxText(demo_edit, *s(str(initial["text"]))[:2])
        DLL.SetEditBoxColor(demo_edit, int(initial["fg"]), int(initial["bg"]))
        DLL.SetEditBoxBounds(demo_edit, int(x), int(y), int(w), int(h))
        DLL.SetEditBoxFont(demo_edit, *s("Segoe UI Emoji")[:2], 13, BOOL(False), BOOL(False), BOOL(False))
        DLL.EnableEditBox(demo_edit, BOOL(True))
        DLL.ShowEditBox(demo_edit, BOOL(True))
        refresh("彩色 Emoji 编辑框属性已恢复默认")

    base.label(page, "📝 文本预设", 40, 326, 180, 22, fg=0xFF303133, bg=0xFFF5F7FA, size=15, bold=True)
    base.button(page, "😀", "表情混排", 40, 360, 156, 36, 0xFF409EFF, lambda: set_text_value("😀 Emoji / English / 数字 123 / ✅", "彩色编辑框文本已切到混排模式"))
    base.button(page, "🚀", "产品文案", 212, 360, 156, 36, 0xFF67C23A, lambda: set_text_value("🚀 EmojiWindow Pro / 支持 Unicode 彩色 emoji", "彩色编辑框文本已切到产品文案"))
    base.button(page, "🎨", "主题文案", 384, 360, 156, 36, 0xFF8E44AD, lambda: set_text_value("🎨 Light / Dark / Custom theme preview", "彩色编辑框文本已切到主题文案"))

    base.label(page, "🎨 颜色 / 字体", 40, 414, 180, 22, fg=0xFF303133, bg=0xFFF5F7FA, size=15, bold=True)
    base.button(page, "💙", "冷色", 40, 448, 118, 36, 0xFF409EFF, lambda: set_colors(THEME_PRIMARY, THEME_SURFACE_PRIMARY, "彩色编辑框已切到冷色方案"))
    base.button(page, "🧡", "暖色", 172, 448, 118, 36, 0xFFE6A23C, lambda: set_colors(THEME_WARNING, THEME_SURFACE_WARNING, "彩色编辑框已切到暖色方案"))
    base.button(page, "🔤", "16px Bold", 304, 448, 118, 36, 0xFF67C23A, lambda: set_font_value(16, True, "彩色编辑框字体已切到 16px Bold"))
    base.button(page, "🔡", "13px", 436, 448, 118, 36, 0xFF909399, lambda: set_font_value(13, False, "彩色编辑框字体已切回 13px"))

    base.label(page, "📐 布局 / 状态", 1044, 322, 180, 22, fg=0xFF303133, bg=0xFFF5F7FA, size=15, bold=True)
    base.button(page, "➡️", "右移 80", 1044, 356, 118, 36, 0xFF409EFF, lambda: move_box(dx=80))
    base.button(page, "⬇️", "下移 20", 1176, 356, 118, 36, 0xFF67C23A, lambda: move_box(dy=20))
    base.button(page, "↔️", "加宽 120", 1308, 356, 118, 36, 0xFFE6A23C, lambda: move_box(dw=120))
    base.button(page, "🚫", "禁用/启用", 1044, 406, 118, 36, 0xFF8E44AD, lambda: (DLL.EnableEditBox(demo_edit, BOOL(not (int(DLL.GetEditBoxEnabled(demo_edit)) == 1))), refresh("彩色编辑框启用状态已切换")))
    base.button(page, "👁️", "显示/隐藏", 1176, 406, 118, 36, 0xFF909399, lambda: (DLL.ShowEditBox(demo_edit, BOOL(not (int(DLL.GetEditBoxVisible(demo_edit)) == 1))), refresh("彩色编辑框可见状态已切换")))
    base.button(page, "↺", "恢复默认", 1308, 406, 118, 36, 0xFF409EFF, restore_box)
    base.label(page, "ColorEmojiEditBox 和普通 EditBox 共享文本/颜色/位置/显示控制接口，但这一页专门强调彩色 emoji 渲染，不会退化成黑白字符。", 1044, 462, 382, 70, fg=0xFF606266, bg=0xFFF5F7FA, wrap=True)

    base.label(page, "1. GetEditBoxText / SetEditBoxText：直接读写彩色 emoji 文本。", 40, 598, 700, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "2. GetEditBoxColor / SetEditBoxColor：读写前景色 / 背景色。", 40, 632, 700, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "3. GetEditBoxBounds / SetEditBoxBounds：直接调整位置与宽度。", 40, 666, 760, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "4. EnableEditBox / ShowEditBox：演示启用态和可见态切换。", 40, 700, 760, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "5. 这一页的重点不是接口差异，而是确认 DLL 的彩色 emoji 文本在真实读写后仍然保持彩色。", 40, 734, 940, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    refresh("彩色 Emoji 编辑框页已加载，可直接测试属性读取与设置")


def build_page_listbox(page: HWND) -> None:
    build_label_property_demo(page, "列表框页标签演示", 1020, 16, 444, 176)
    base.groupbox(page, "📋 ListBox 实时属性读取", 16, 16, 980, 248)
    base.groupbox(page, "🛠️ 项目 / 选中 / 颜色 / 布局", 16, 286, 980, 254)
    base.groupbox(page, "📐 ListBox 状态开关", 1020, 212, 444, 328)
    base.groupbox(page, "📘 ListBox API 说明", 16, 558, 1448, 230)

    listbox = DLL.CreateListBox(page, 56, 116, 320, 112, BOOL(False), THEME_TEXT, THEME_BG)
    for item in ("📘 文档中心", "🚀 发布任务", "🎨 主题切换", "🧪 回归测试"):
        DLL.AddListItem(listbox, *s(item)[:2])
    DLL.SetSelectedIndex(listbox, 1)
    DLL.SetListBoxColors(listbox, THEME_TEXT, THEME_BG, THEME_SURFACE_PRIMARY, THEME_SURFACE)
    readout = base.label(page, "等待读取列表框属性…", 410, 124, 550, 104, fg=0xFF303133, bg=0xFFF5F7FA, wrap=True)
    state_text = base.label(page, "列表框页状态将在这里更新。", 40, 760, 1360, 22, fg=0xFF409EFF, bg=0xFFF5F7FA)
    base.label(page, "这一页直接读取 ListBox 的项目数量、选中项、颜色、位置尺寸、可见态和启用态。", 40, 56, 900, 24, fg=0xFF606266, bg=0xFFF5F7FA)

    def read_list_text(index: int) -> str:
        size = int(DLL.GetListItemText(listbox, index, None, 0))
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        DLL.GetListItemText(listbox, index, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    def read_bounds() -> tuple[int, int, int, int]:
        rc = RECT()
        USER32.GetWindowRect(listbox, ctypes.byref(rc))
        root = LOCAL["host"]
        pt = POINT(rc.left, rc.top)
        USER32.ScreenToClient(root, ctypes.byref(pt))
        return pt.x, pt.y, rc.right - rc.left, rc.bottom - rc.top

    fg0 = UINT32()
    bg0 = UINT32()
    sel0 = UINT32()
    hover0 = UINT32()
    DLL.GetListBoxColors(listbox, ctypes.byref(fg0), ctypes.byref(bg0), ctypes.byref(sel0), ctypes.byref(hover0))

    def refresh(note: str = "已刷新列表框属性") -> None:
        fg = UINT32()
        bg = UINT32()
        sel = UINT32()
        hover = UINT32()
        DLL.GetListBoxColors(listbox, ctypes.byref(fg), ctypes.byref(bg), ctypes.byref(sel), ctypes.byref(hover))
        count = int(DLL.GetListItemCount(listbox))
        index = int(DLL.GetSelectedIndex(listbox))
        text = read_list_text(index) if index >= 0 else "(无选中)"
        x, y, w, h = read_bounds()
        enabled = "启用" if USER32.IsWindowEnabled(listbox) else "禁用"
        visible = "显示" if USER32.IsWindowVisible(listbox) else "隐藏"
        base.set_label_text(
            readout,
            f"count={count}  selected={index}  selected_text={text}\n"
            f"bounds=({x}, {y}, {w}, {h})  {visible}/{enabled}\n"
            f"fg=0x{int(fg.value):08X}  bg=0x{int(bg.value):08X}  select=0x{int(sel.value):08X}  hover=0x{int(hover.value):08X}"
        )
        base.set_label_text(state_text, note)
        base.set_status(note)

    def set_item(index: int, text: str, note: str) -> None:
        DLL.SetListItemText(listbox, index, *s(text)[:2])
        refresh(note)

    def move_box(dx: int = 0, dy: int = 0, dw: int = 0, dh: int = 0) -> None:
        x, y, w, h = read_bounds()
        DLL.SetListBoxBounds(listbox, x + dx, y + dy, w + dw, h + dh)
        refresh(f"列表框位置/尺寸已更新: dx={dx}, dy={dy}, dw={dw}, dh={dh}")

    base.button(page, "➕", "新增项目", 40, 360, 140, 36, 0xFF409EFF, lambda: (DLL.AddListItem(listbox, *s("🆕 新增项目")[:2]), refresh("列表框已新增一项")))
    base.button(page, "✏️", "改写第 1 项", 196, 360, 140, 36, 0xFF67C23A, lambda: set_item(0, "✏️ 第 1 项已改写", "列表框第 1 项文本已改写"))
    base.button(page, "🗑️", "删除最后项", 352, 360, 140, 36, 0xFFE6A23C, lambda: (DLL.RemoveListItem(listbox, max(0, int(DLL.GetListItemCount(listbox)) - 1)), refresh("列表框最后一项已删除")))
    base.button(page, "📍", "选中第 3 项", 508, 360, 140, 36, 0xFF8E44AD, lambda: (DLL.SetSelectedIndex(listbox, 2), refresh("列表框已选中第 3 项")))
    base.button(page, "🧹", "清空并重建", 664, 360, 140, 36, 0xFF909399, lambda: (DLL.ClearListBox(listbox), DLL.AddListItem(listbox, *s("📘 文档中心")[:2]), DLL.AddListItem(listbox, *s("🚀 发布任务")[:2]), DLL.AddListItem(listbox, *s("🎨 主题切换")[:2]), DLL.AddListItem(listbox, *s("🧪 回归测试")[:2]), DLL.SetSelectedIndex(listbox, 1), refresh("列表框已清空并恢复默认项")))

    base.button(page, "💙", "冷色", 40, 448, 118, 36, 0xFF409EFF, lambda: (DLL.SetListBoxColors(listbox, THEME_PRIMARY, THEME_SURFACE_PRIMARY, THEME_PRIMARY, THEME_SURFACE), refresh("列表框已切到冷色方案")))
    base.button(page, "🧡", "暖色", 172, 448, 118, 36, 0xFFE6A23C, lambda: (DLL.SetListBoxColors(listbox, THEME_WARNING, THEME_SURFACE_WARNING, THEME_WARNING, THEME_SURFACE), refresh("列表框已切到暖色方案")))
    base.button(page, "➡️", "右移 80", 304, 448, 118, 36, 0xFF67C23A, lambda: move_box(dx=80))
    base.button(page, "↔️", "加宽 120", 436, 448, 118, 36, 0xFF8E44AD, lambda: move_box(dw=120))
    base.button(page, "🚫", "禁用/启用", 1044, 286, 118, 36, 0xFF409EFF, lambda: (DLL.EnableListBox(listbox, BOOL(not USER32.IsWindowEnabled(listbox))), refresh("列表框启用状态已切换")))
    base.button(page, "👁️", "显示/隐藏", 1176, 286, 118, 36, 0xFF909399, lambda: (DLL.ShowListBox(listbox, BOOL(not USER32.IsWindowVisible(listbox))), refresh("列表框可见状态已切换")))
    base.button(page, "↺", "恢复默认", 1308, 286, 118, 36, 0xFF67C23A, lambda: (DLL.SetListBoxBounds(listbox, 56, 116, 320, 112), DLL.SetListBoxColors(listbox, int(fg0.value), int(bg0.value), int(sel0.value), int(hover0.value)), DLL.ShowListBox(listbox, BOOL(True)), DLL.EnableListBox(listbox, BOOL(True)), refresh("列表框已恢复默认状态")))

    base.label(page, "1. GetListItemCount / GetSelectedIndex / GetListItemText：读取当前列表数据与选中项。", 40, 598, 860, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "2. AddListItem / RemoveListItem / ClearListBox / SetListItemText：直接改项目。", 40, 632, 860, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "3. SetListBoxColors / GetListBoxColors：切换并读取颜色方案。", 40, 666, 820, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "4. SetListBoxBounds / EnableListBox / ShowListBox：切换布局、可见性和启用态。", 40, 700, 900, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "5. 这页同样保留 Unicode 彩色文案项目，用来验证 ListBox 的文本读写。", 40, 734, 860, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    refresh("列表框页已加载，可直接测试列表框属性读取与设置")


def build_page_listbox_v2(page: HWND) -> None:
    palette = page_palette()
    page_bg = palette["page_bg"]
    text_color = palette["text"]
    muted_color = palette["muted"]
    accent_color = palette["accent"]

    base.groupbox(page, "📋 ListBox 主展示区", 16, 16, 1048, 500)
    base.groupbox(page, "🧪 项目 / 选中 / 颜色 / 布局", 1080, 16, 384, 500)
    base.groupbox(page, "📘 ListBox API 说明", 16, 540, 1448, 208)

    register_theme_label(
        base.label(
            page,
            "这一页把 ListBox 本体放大为主展示区，重点演示项目列表、选中反馈、颜色切换、布局调整和状态开关。",
            40,
            56,
            980,
            24,
            fg=muted_color,
            bg=page_bg,
        ),
        "muted",
        "page",
    )

    listbox = DLL.CreateListBox(page, 40, 104, 620, 340, BOOL(False), THEME_TEXT, THEME_BG)
    for item in (
        "📌 文档中心",
        "🚀 发布任务",
        "🧩 主题切换",
        "🧪 回归测试",
        "🗂️ 资源整理",
        "📦 组件打包",
        "📝 变更记录",
        "✅ 发布复核",
    ):
        DLL.AddListItem(listbox, *s(item)[:2])
    DLL.SetSelectedIndex(listbox, 1)
    DLL.SetListBoxColors(listbox, THEME_TEXT, THEME_BG, THEME_SURFACE_PRIMARY, THEME_SURFACE)

    readout = register_theme_label(
        base.label(page, "等待读取列表框属性。", 688, 104, 340, 184, fg=text_color, bg=page_bg, wrap=True),
        "text",
        "page",
    )
    state_text = register_theme_label(
        base.label(page, "ListBox 页面状态将在这里更新。", 40, 470, 980, 24, fg=accent_color, bg=page_bg),
        "accent",
        "page",
    )
    register_theme_label(
        base.label(
            page,
            "左侧直接展示更大的列表区，便于验证滚动、选中高亮、可见项数量和真实组件观感。",
            688,
            304,
            340,
            46,
            fg=muted_color,
            bg=page_bg,
            wrap=True,
        ),
        "muted",
        "page",
    )

    def read_list_text(index: int) -> str:
        size = int(DLL.GetListItemText(listbox, index, None, 0))
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        DLL.GetListItemText(listbox, index, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    def read_bounds() -> tuple[int, int, int, int]:
        rc = RECT()
        USER32.GetWindowRect(listbox, ctypes.byref(rc))
        root = LOCAL["host"]
        pt = POINT(rc.left, rc.top)
        USER32.ScreenToClient(root, ctypes.byref(pt))
        return pt.x, pt.y, rc.right - rc.left, rc.bottom - rc.top

    fg0 = UINT32()
    bg0 = UINT32()
    sel0 = UINT32()
    hover0 = UINT32()
    DLL.GetListBoxColors(listbox, ctypes.byref(fg0), ctypes.byref(bg0), ctypes.byref(sel0), ctypes.byref(hover0))
    initial_bounds = {"x": 40, "y": 104, "w": 620, "h": 340}
    listbox_flags = {"enabled": True}

    def refresh(note: str = "已刷新列表框属性") -> None:
        fg = UINT32()
        bg = UINT32()
        sel = UINT32()
        hover = UINT32()
        DLL.GetListBoxColors(listbox, ctypes.byref(fg), ctypes.byref(bg), ctypes.byref(sel), ctypes.byref(hover))
        count = int(DLL.GetListItemCount(listbox))
        index = int(DLL.GetSelectedIndex(listbox))
        text = read_list_text(index) if index >= 0 else "(无选中)"
        x, y, w, h = read_bounds()
        enabled = "启用" if bool(listbox_flags["enabled"]) else "禁用"
        visible = "显示" if USER32.IsWindowVisible(listbox) else "隐藏"
        base.set_label_text(
            readout,
            f"count={count}  selected={index}  selected_text={text}\n"
            f"bounds=({x}, {y}, {w}, {h})  {visible}/{enabled}\n"
            f"fg=0x{int(fg.value):08X}  bg=0x{int(bg.value):08X}\n"
            f"select=0x{int(sel.value):08X}  hover=0x{int(hover.value):08X}"
        )
        base.set_label_text(state_text, note)
        base.set_status(note)

    def set_item(index: int, text: str, note: str) -> None:
        DLL.SetListItemText(listbox, index, *s(text)[:2])
        refresh(note)

    def move_box(dx: int = 0, dy: int = 0, dw: int = 0, dh: int = 0) -> None:
        x, y, w, h = read_bounds()
        DLL.SetListBoxBounds(listbox, x + dx, y + dy, w + dw, h + dh)
        refresh(f"列表框位置/尺寸已更新 dx={dx}, dy={dy}, dw={dw}, dh={dh}")

    def restore() -> None:
        DLL.SetListBoxBounds(listbox, initial_bounds["x"], initial_bounds["y"], initial_bounds["w"], initial_bounds["h"])
        DLL.SetListBoxColors(listbox, int(fg0.value), int(bg0.value), int(sel0.value), int(hover0.value))
        DLL.ShowListBox(listbox, BOOL(True))
        DLL.EnableListBox(listbox, BOOL(True))
        listbox_flags["enabled"] = True
        DLL.ClearListBox(listbox)
        for item in (
            "📌 文档中心",
            "🚀 发布任务",
            "🧩 主题切换",
            "🧪 回归测试",
            "🗂️ 资源整理",
            "📦 组件打包",
            "📝 变更记录",
            "✅ 发布复核",
        ):
            DLL.AddListItem(listbox, *s(item)[:2])
        DLL.SetSelectedIndex(listbox, 1)
        refresh("列表框已恢复默认")

    def toggle_enabled() -> None:
        next_enabled = not bool(listbox_flags["enabled"])
        listbox_flags["enabled"] = next_enabled
        DLL.EnableListBox(listbox, BOOL(next_enabled))
        refresh("列表框启用状态已切换")

    base.button(page, "➕", "新增项目", 1104, 94, 112, 36, 0xFF409EFF, lambda: (DLL.AddListItem(listbox, *s("🆕 新增项目")[:2]), refresh("列表框已新增一项")))
    base.button(page, "✏️", "改写第 1 项", 1230, 94, 128, 36, 0xFF67C23A, lambda: set_item(0, "✏️ 第 1 项已改写", "列表框第 1 项文本已改写"))
    base.button(page, "🗑️", "删除最后项", 1104, 142, 112, 36, 0xFFE6A23C, lambda: (DLL.RemoveListItem(listbox, max(0, int(DLL.GetListItemCount(listbox)) - 1)), refresh("列表框最后一项已删除")))
    base.button(page, "📍", "选中第 5 项", 1230, 142, 128, 36, 0xFF8E44AD, lambda: (DLL.SetSelectedIndex(listbox, 4), refresh("列表框已选中第 5 项")))
    base.button(page, "💙", "冷色", 1104, 202, 112, 36, 0xFF409EFF, lambda: (DLL.SetListBoxColors(listbox, THEME_PRIMARY, THEME_SURFACE_PRIMARY, THEME_PRIMARY, THEME_SURFACE), refresh("列表框已切到冷色方案")))
    base.button(page, "🧡", "暖色", 1230, 202, 128, 36, 0xFFE6A23C, lambda: (DLL.SetListBoxColors(listbox, THEME_WARNING, THEME_SURFACE_WARNING, THEME_WARNING, THEME_SURFACE), refresh("列表框已切到暖色方案")))
    base.button(page, "↔️", "加宽 160", 1104, 250, 112, 36, 0xFF67C23A, lambda: move_box(dw=160))
    base.button(page, "↕️", "加高 120", 1230, 250, 128, 36, 0xFF8E44AD, lambda: move_box(dh=120))
    base.button(page, "🚫", "禁用/启用", 1104, 310, 112, 36, 0xFF409EFF, toggle_enabled)
    base.button(page, "👁️", "显示/隐藏", 1230, 310, 128, 36, 0xFF909399, lambda: (DLL.ShowListBox(listbox, BOOL(not USER32.IsWindowVisible(listbox))), refresh("列表框可见状态已切换")))
    base.button(page, "↺", "恢复默认", 1104, 370, 254, 36, 0xFF67C23A, restore)

    register_theme_label(base.label(page, "1. GetListItemCount / GetSelectedIndex / GetListItemText：读取当前列表数据与选中项。", 40, 582, 920, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "2. AddListItem / RemoveListItem / ClearListBox / SetListItemText：直接改项目。", 40, 616, 900, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "3. SetListBoxColors / GetListBoxColors：切换并读取颜色方案。", 40, 650, 820, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "4. SetListBoxBounds / EnableListBox / ShowListBox：切换布局、可见性和启用态。", 40, 684, 940, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "5. 页面保留 Unicode 彩色文案项目，用来验证 ListBox 的文本读写。", 40, 718, 860, 24, fg=text_color, bg=page_bg), "text", "page")
    refresh("列表框页面已重排：主展示区放大，优先展示 ListBox 本体")


def build_page_combobox(page: HWND) -> None:
    build_label_property_demo(page, "组合框页标签演示", 1020, 16, 444, 176)
    base.groupbox(page, "📑 ComboBox / D2DComboBox 实时属性读取", 16, 16, 980, 248)
    base.groupbox(page, "🛠️ 文本 / 选中 / 颜色 / 布局", 16, 286, 980, 254)
    base.groupbox(page, "🫧 D2D 组合框状态开关", 1020, 212, 444, 328)
    base.groupbox(page, "📘 ComboBox API 说明", 16, 558, 1448, 230)

    combo = DLL.CreateComboBox(page, 56, 120, 240, 38, BOOL(True), THEME_TEXT, THEME_BG, 32, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    d2d_combo = DLL.CreateD2DComboBox(page, 320, 120, 320, 38, BOOL(False), THEME_TEXT, THEME_BG, 32, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    for item in ("默认", "主题", "紧凑", "高亮"):
        DLL.AddComboItem(combo, *s(item)[:2])
        DLL.AddD2DComboItem(d2d_combo, *s("🫧 " + item)[:2])
    DLL.SetComboSelectedIndex(combo, 1)
    DLL.SetD2DComboSelectedIndex(d2d_combo, 2)
    DLL.SetComboBoxColors(combo, THEME_TEXT, THEME_BG, THEME_SURFACE_PRIMARY, THEME_SURFACE)
    DLL.SetD2DComboBoxColors(d2d_combo, THEME_TEXT, THEME_BG, THEME_SURFACE_PRIMARY, THEME_SURFACE, THEME_BORDER_LIGHT, THEME_SURFACE)
    readout = base.label(page, "等待读取组合框属性…", 40, 184, 920, 56, fg=0xFF303133, bg=0xFFF5F7FA, wrap=True)
    state_text = base.label(page, "组合框页状态将在这里更新。", 40, 760, 1360, 22, fg=0xFF409EFF, bg=0xFFF5F7FA)
    base.label(page, "这一页同时演示普通 ComboBox 和 D2DComboBox，覆盖选中项、文本、颜色、布局和显示状态。", 40, 56, 940, 24, fg=0xFF606266, bg=0xFFF5F7FA)

    def read_utf8(call, *args) -> str:
        size = int(call(*args, None, 0))
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        call(*args, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    c_fg0 = UINT32(); c_bg0 = UINT32(); c_sel0 = UINT32(); c_hover0 = UINT32()
    DLL.GetComboBoxColors(combo, ctypes.byref(c_fg0), ctypes.byref(c_bg0), ctypes.byref(c_sel0), ctypes.byref(c_hover0))
    d_fg0 = UINT32(); d_bg0 = UINT32(); d_sel0 = UINT32(); d_hover0 = UINT32(); d_border0 = UINT32(); d_btn0 = UINT32()
    DLL.GetD2DComboBoxColors(d2d_combo, ctypes.byref(d_fg0), ctypes.byref(d_bg0), ctypes.byref(d_sel0), ctypes.byref(d_hover0), ctypes.byref(d_border0), ctypes.byref(d_btn0))

    def refresh(note: str = "已刷新组合框属性") -> None:
        c_fg = UINT32(); c_bg = UINT32(); c_sel = UINT32(); c_hover = UINT32()
        DLL.GetComboBoxColors(combo, ctypes.byref(c_fg), ctypes.byref(c_bg), ctypes.byref(c_sel), ctypes.byref(c_hover))
        d_fg = UINT32(); d_bg = UINT32(); d_sel = UINT32(); d_hover = UINT32(); d_border = UINT32(); d_btn = UINT32()
        DLL.GetD2DComboBoxColors(d2d_combo, ctypes.byref(d_fg), ctypes.byref(d_bg), ctypes.byref(d_sel), ctypes.byref(d_hover), ctypes.byref(d_border), ctypes.byref(d_btn))
        base.set_label_text(
            readout,
            f"ComboBox: count={int(DLL.GetComboItemCount(combo))}  selected={int(DLL.GetComboSelectedIndex(combo))}  text={read_utf8(DLL.GetComboBoxText, combo)}\n"
            f"D2DComboBox: count={int(DLL.GetD2DComboItemCount(d2d_combo))}  selected={int(DLL.GetD2DComboSelectedIndex(d2d_combo))}  text={read_utf8(DLL.GetD2DComboText, d2d_combo)}  selected_text={read_utf8(DLL.GetD2DComboSelectedText, d2d_combo)}\n"
            f"Combo fg/bg=0x{int(c_fg.value):08X}/0x{int(c_bg.value):08X}    D2D fg/bg/border=0x{int(d_fg.value):08X}/0x{int(d_bg.value):08X}/0x{int(d_border.value):08X}"
        )
        base.set_label_text(state_text, note)
        base.set_status(note)

    base.button(page, "1️⃣", "选中第 1 项", 40, 360, 146, 36, 0xFF409EFF, lambda: (DLL.SetComboSelectedIndex(combo, 0), refresh("普通 ComboBox 已选中第 1 项")))
    base.button(page, "3️⃣", "选中第 3 项", 202, 360, 146, 36, 0xFF67C23A, lambda: (DLL.SetComboSelectedIndex(combo, 2), refresh("普通 ComboBox 已选中第 3 项")))
    base.button(page, "📝", "写入文本", 364, 360, 146, 36, 0xFF8E44AD, lambda: (DLL.SetComboBoxText(combo, *s("手动写入 / Manual input")[:2]), refresh("普通 ComboBox 文本已写入")))
    base.button(page, "🫧", "D2D 写入", 526, 360, 146, 36, 0xFFE6A23C, lambda: (DLL.SetD2DComboText(d2d_combo, *s("🫧 D2D 手动输入 / 可编辑")[:2]), refresh("D2DComboBox 文本已写入")))
    base.button(page, "🎯", "D2D 选第 4 项", 688, 360, 146, 36, 0xFF409EFF, lambda: (DLL.SetD2DComboSelectedIndex(d2d_combo, 3), refresh("D2DComboBox 已选中第 4 项")))

    base.button(page, "💙", "普通冷色", 40, 448, 118, 36, 0xFF409EFF, lambda: (DLL.SetComboBoxColors(combo, THEME_PRIMARY, THEME_SURFACE_PRIMARY, THEME_PRIMARY, THEME_SURFACE), refresh("普通 ComboBox 已切到冷色方案")))
    base.button(page, "🧡", "普通暖色", 172, 448, 118, 36, 0xFFE6A23C, lambda: (DLL.SetComboBoxColors(combo, THEME_WARNING, THEME_SURFACE_WARNING, THEME_WARNING, THEME_SURFACE), refresh("普通 ComboBox 已切到暖色方案")))
    base.button(page, "💜", "D2D 主题色", 304, 448, 118, 36, 0xFF8E44AD, lambda: (DLL.SetD2DComboBoxColors(d2d_combo, THEME_INFO, THEME_SURFACE_INFO, THEME_INFO, THEME_SURFACE, THEME_BORDER_LIGHT, THEME_SURFACE_INFO), refresh("D2DComboBox 已切到主题色方案")))
    base.button(page, "➡️", "右移 80", 436, 448, 118, 36, 0xFF67C23A, lambda: (DLL.SetComboBoxBounds(combo, 136, 120, 240, 38), DLL.SetD2DComboBoxBounds(d2d_combo, 400, 120, 320, 38), refresh("两个组合框已整体右移")))
    base.button(page, "↔️", "D2D 加宽", 568, 448, 118, 36, 0xFF909399, lambda: (DLL.SetD2DComboBoxBounds(d2d_combo, 320, 120, 420, 38), refresh("D2DComboBox 已加宽到 420")))

    base.button(page, "🚫", "普通禁用/启用", 1044, 286, 126, 36, 0xFF409EFF, lambda: (DLL.EnableComboBox(combo, BOOL(not USER32.IsWindowEnabled(combo))), refresh("普通 ComboBox 启用状态已切换")))
    base.button(page, "👁️", "普通显示/隐藏", 1184, 286, 126, 36, 0xFF909399, lambda: (DLL.ShowComboBox(combo, BOOL(not USER32.IsWindowVisible(combo))), refresh("普通 ComboBox 可见状态已切换")))
    base.button(page, "🫧", "D2D 禁用/启用", 1044, 336, 126, 36, 0xFF67C23A, lambda: (DLL.EnableD2DComboBox(d2d_combo, BOOL(not USER32.IsWindowEnabled(d2d_combo))), refresh("D2DComboBox 启用状态已切换")))
    base.button(page, "🌫️", "D2D 显示/隐藏", 1184, 336, 126, 36, 0xFF8E44AD, lambda: (DLL.ShowD2DComboBox(d2d_combo, BOOL(not USER32.IsWindowVisible(d2d_combo))), refresh("D2DComboBox 可见状态已切换")))
    base.button(page, "↺", "恢复默认", 1324, 286, 102, 36, 0xFFE6A23C, lambda: (DLL.SetComboBoxBounds(combo, 56, 120, 240, 38), DLL.SetD2DComboBoxBounds(d2d_combo, 320, 120, 320, 38), DLL.SetComboBoxColors(combo, int(c_fg0.value), int(c_bg0.value), int(c_sel0.value), int(c_hover0.value)), DLL.SetD2DComboBoxColors(d2d_combo, int(d_fg0.value), int(d_bg0.value), int(d_sel0.value), int(d_hover0.value), int(d_border0.value), int(d_btn0.value)), DLL.ShowComboBox(combo, BOOL(True)), DLL.ShowD2DComboBox(d2d_combo, BOOL(True)), DLL.EnableComboBox(combo, BOOL(True)), DLL.EnableD2DComboBox(d2d_combo, BOOL(True)), refresh("组合框页已恢复默认状态")))

    base.label(page, "1. GetComboSelectedIndex / GetComboBoxText / GetComboItemCount：读取普通组合框当前状态。", 40, 598, 900, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "2. SetComboSelectedIndex / SetComboBoxText / SetComboBoxColors：修改普通组合框。", 40, 632, 900, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "3. GetD2DComboSelectedText / SetD2DComboText / SetD2DComboBoxColors：修改 D2D 组合框。", 40, 666, 980, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "4. EnableComboBox / ShowComboBox / EnableD2DComboBox / ShowD2DComboBox：切换状态。", 40, 700, 980, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "5. 这一页同时保留普通 ComboBox 和 D2DComboBox，方便横向对照属性读写。", 40, 734, 940, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    refresh("组合框页已加载，可直接测试组合框属性读取与设置")


def build_page_combobox_v2(page: HWND) -> None:
    palette = page_palette()
    page_bg = palette["page_bg"]
    text_color = palette["text"]
    muted_color = palette["muted"]
    accent_color = palette["accent"]

    base.groupbox(page, "普通 ComboBox 样式展示", 16, 16, 980, 520)
    base.groupbox(page, "项目 / 文本 / 颜色 / 状态", 1020, 16, 444, 520)
    base.groupbox(page, "ComboBox API 说明", 16, 558, 1448, 220)

    register_theme_label(
        base.label(
            page,
            "这一页只保留普通 ComboBox。左侧保留只读和可编辑两种模式，右侧集中演示普通 ComboBox 的属性读取和设置。",
            40,
            56,
            930,
            24,
            fg=muted_color,
            bg=page_bg,
            wrap=True,
        ),
        "muted",
        "page",
    )
    register_theme_label(base.label(page, "只读 ComboBox", 56, 104, 180, 20, fg=text_color, bg=page_bg, size=14, bold=True), "text", "page")
    combo_readonly = DLL.CreateComboBox(page, 56, 128, 560, 38, BOOL(True), THEME_TEXT, THEME_BG, 32, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    register_theme_label(base.label(page, "可编辑 ComboBox", 56, 212, 180, 20, fg=text_color, bg=page_bg, size=14, bold=True), "text", "page")
    combo_edit = DLL.CreateComboBox(page, 56, 236, 560, 38, BOOL(False), THEME_TEXT, THEME_BG, 32, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))

    readonly_items = [
        "北京",
        "上海",
        "深圳",
        "杭州",
    ]
    edit_items = [
        "默认方案",
        "主题模式",
        "紧急文案",
        "高亮标记",
    ]

    def fill_combo(hwnd: HWND, items: list[str]) -> None:
        DLL.ClearComboBox(hwnd)
        for item in items:
            DLL.AddComboItem(hwnd, *s(item)[:2])

    fill_combo(combo_readonly, readonly_items)
    fill_combo(combo_edit, edit_items)
    DLL.SetComboSelectedIndex(combo_readonly, 1)
    DLL.SetComboSelectedIndex(combo_edit, 1)
    DLL.SetComboBoxColors(combo_readonly, THEME_TEXT, THEME_BG, THEME_SURFACE_PRIMARY, THEME_SURFACE)
    DLL.SetComboBoxColors(combo_edit, THEME_TEXT, THEME_BG, THEME_SURFACE_PRIMARY, THEME_SURFACE)

    register_theme_label(
        base.label(
            page,
            "只读框用于对照模式；右侧操作默认作用于下方可编辑 ComboBox。你手动下拉、切换选择或输入文字后，读数区会同步刷新。",
            56,
            292,
            900,
            38,
            fg=muted_color,
            bg=page_bg,
            wrap=True,
        ),
        "muted",
        "page",
    )
    readout = register_theme_label(
        base.label(page, "等待读取 ComboBox 状态。", 40, 348, 920, 96, fg=text_color, bg=page_bg, wrap=True),
        "text",
        "page",
    )
    state_text = register_theme_label(
        base.label(page, "组合框页状态将在这里更新。", 40, 470, 1360, 22, fg=accent_color, bg=page_bg),
        "accent",
        "page",
    )

    register_theme_label(
        base.label(
            page,
            "首行按钮专门切换只读 ComboBox 的选中项。其余按钮只操作普通可编辑 ComboBox，不再混入 D2DComboBox 或其它组件。",
            1044,
            56,
            380,
            44,
            fg=muted_color,
            bg=page_bg,
            wrap=True,
        ),
        "muted",
        "page",
    )

    edit_fg0 = UINT32()
    edit_bg0 = UINT32()
    edit_sel0 = UINT32()
    edit_hover0 = UINT32()
    DLL.GetComboBoxColors(combo_edit, ctypes.byref(edit_fg0), ctypes.byref(edit_bg0), ctypes.byref(edit_sel0), ctypes.byref(edit_hover0))

    edit_bounds = {"x": 56, "y": 236, "w": 560, "h": 38}
    combo_flags = {"edit_enabled": True}
    next_item_id = {"value": 1}

    def read_utf8(call, *args) -> str:
        size = int(call(*args, None, 0))
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        call(*args, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    def read_item_text(hwnd: HWND, index: int) -> str:
        if index < 0:
            return "(无选中)"
        size = int(DLL.GetComboItemText(hwnd, index, None, 0))
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        DLL.GetComboItemText(hwnd, index, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    def read_bounds(hwnd: HWND) -> tuple[int, int, int, int]:
        rc = RECT()
        USER32.GetWindowRect(hwnd, ctypes.byref(rc))
        root = LOCAL["host"]
        pt = POINT(rc.left, rc.top)
        USER32.ScreenToClient(root, ctypes.byref(pt))
        return pt.x, pt.y, rc.right - rc.left, rc.bottom - rc.top

    def refresh(note: str = "已刷新 ComboBox 状态") -> None:
        ro_fg = UINT32()
        ro_bg = UINT32()
        ro_sel = UINT32()
        ro_hover = UINT32()
        DLL.GetComboBoxColors(combo_readonly, ctypes.byref(ro_fg), ctypes.byref(ro_bg), ctypes.byref(ro_sel), ctypes.byref(ro_hover))
        ed_fg = UINT32()
        ed_bg = UINT32()
        ed_sel = UINT32()
        ed_hover = UINT32()
        DLL.GetComboBoxColors(combo_edit, ctypes.byref(ed_fg), ctypes.byref(ed_bg), ctypes.byref(ed_sel), ctypes.byref(ed_hover))

        ro_index = int(DLL.GetComboSelectedIndex(combo_readonly))
        ed_index = int(DLL.GetComboSelectedIndex(combo_edit))
        ro_count = int(DLL.GetComboItemCount(combo_readonly))
        ed_count = int(DLL.GetComboItemCount(combo_edit))
        ro_x, ro_y, ro_w, ro_h = read_bounds(combo_readonly)
        ed_x, ed_y, ed_w, ed_h = read_bounds(combo_edit)
        ed_visible = "显示" if USER32.IsWindowVisible(combo_edit) else "隐藏"
        ed_enabled = "启用" if bool(combo_flags["edit_enabled"]) else "禁用"

        base.set_label_text(
            readout,
            f"只读: count={ro_count}  selected={ro_index}  selected_text={read_item_text(combo_readonly, ro_index)}  text={read_utf8(DLL.GetComboBoxText, combo_readonly)}\n"
            f"只读 bounds=({ro_x}, {ro_y}, {ro_w}, {ro_h})  fg/bg=0x{int(ro_fg.value):08X}/0x{int(ro_bg.value):08X}  select/hover=0x{int(ro_sel.value):08X}/0x{int(ro_hover.value):08X}\n"
            f"编辑: count={ed_count}  selected={ed_index}  selected_text={read_item_text(combo_edit, ed_index)}  text={read_utf8(DLL.GetComboBoxText, combo_edit)}\n"
            f"编辑 bounds=({ed_x}, {ed_y}, {ed_w}, {ed_h})  {ed_visible}/{ed_enabled}  fg/bg=0x{int(ed_fg.value):08X}/0x{int(ed_bg.value):08X}  select/hover=0x{int(ed_sel.value):08X}/0x{int(ed_hover.value):08X}"
        )
        base.set_label_text(state_text, note)
        base.set_status(note)

    def set_readonly_index(index: int, note: str) -> None:
        if int(DLL.GetComboItemCount(combo_readonly)) <= index:
            refresh("只读 ComboBox 项目数量不足，无法选中该项")
            return
        DLL.SetComboSelectedIndex(combo_readonly, index)
        refresh(note)

    def set_edit_index(index: int, note: str) -> None:
        if int(DLL.GetComboItemCount(combo_edit)) <= index:
            refresh("可编辑 ComboBox 项目数量不足，无法选中该项")
            return
        DLL.SetComboSelectedIndex(combo_edit, index)
        refresh(note)

    def add_item() -> None:
        text = f"新增项目 {next_item_id['value']}"
        next_item_id["value"] += 1
        DLL.AddComboItem(combo_edit, *s(text)[:2])
        DLL.SetComboSelectedIndex(combo_edit, int(DLL.GetComboItemCount(combo_edit)) - 1)
        refresh("可编辑 ComboBox 已新增一项并选中末项")

    def remove_last_item() -> None:
        count = int(DLL.GetComboItemCount(combo_edit))
        if count <= 0:
            refresh("可编辑 ComboBox 当前没有可删除的项目")
            return
        DLL.RemoveComboItem(combo_edit, count - 1)
        if int(DLL.GetComboItemCount(combo_edit)) > 0:
            DLL.SetComboSelectedIndex(combo_edit, max(0, int(DLL.GetComboItemCount(combo_edit)) - 1))
        refresh("可编辑 ComboBox 已删除末项")

    def clear_items() -> None:
        DLL.ClearComboBox(combo_edit)
        refresh("可编辑 ComboBox 项目已清空")

    def restore_items() -> None:
        fill_combo(combo_edit, edit_items)
        DLL.SetComboSelectedIndex(combo_edit, 1)
        next_item_id["value"] = 1
        refresh("可编辑 ComboBox 项目已恢复默认列表")

    def fill_text_from_selection() -> None:
        index = int(DLL.GetComboSelectedIndex(combo_edit))
        if index < 0:
            refresh("当前没有选中项，无法回填文本")
            return
        DLL.SetComboBoxText(combo_edit, *s(read_item_text(combo_edit, index))[:2])
        refresh("已将当前选中项回填到可编辑 ComboBox 文本")

    def move_edit(dx: int = 0, dw: int = 0) -> None:
        edit_bounds["x"] += dx
        edit_bounds["w"] += dw
        DLL.SetComboBoxBounds(combo_edit, edit_bounds["x"], edit_bounds["y"], edit_bounds["w"], edit_bounds["h"])
        refresh(f"可编辑 ComboBox 布局已更新: dx={dx}, dw={dw}")

    def toggle_enabled() -> None:
        next_enabled = not bool(combo_flags["edit_enabled"])
        combo_flags["edit_enabled"] = next_enabled
        DLL.EnableComboBox(combo_edit, BOOL(next_enabled))
        refresh("可编辑 ComboBox 启用状态已切换")

    def toggle_visible() -> None:
        DLL.ShowComboBox(combo_edit, BOOL(not USER32.IsWindowVisible(combo_edit)))
        refresh("可编辑 ComboBox 可见状态已切换")

    def restore() -> None:
        fill_combo(combo_readonly, readonly_items)
        fill_combo(combo_edit, edit_items)
        DLL.SetComboSelectedIndex(combo_readonly, 1)
        DLL.SetComboSelectedIndex(combo_edit, 1)
        DLL.SetComboBoxText(combo_edit, *s(edit_items[1])[:2])
        edit_bounds["x"] = 56
        edit_bounds["y"] = 236
        edit_bounds["w"] = 560
        edit_bounds["h"] = 38
        DLL.SetComboBoxBounds(combo_edit, edit_bounds["x"], edit_bounds["y"], edit_bounds["w"], edit_bounds["h"])
        DLL.SetComboBoxColors(combo_edit, int(edit_fg0.value), int(edit_bg0.value), int(edit_sel0.value), int(edit_hover0.value))
        DLL.ShowComboBox(combo_edit, BOOL(True))
        DLL.EnableComboBox(combo_edit, BOOL(True))
        combo_flags["edit_enabled"] = True
        next_item_id["value"] = 1
        refresh("组合框页已恢复默认状态")

    def on_combo_changed(hwnd: HWND, index: int) -> None:
        which = "只读 ComboBox" if base.hwnd_key(hwnd) == base.hwnd_key(combo_readonly) else "可编辑 ComboBox"
        refresh(f"{which} 回调: selected={index}")

    combo_cb = DLL._ComboCB(on_combo_changed)
    KEEP.append(combo_cb)
    DLL.SetComboBoxCallback(combo_readonly, combo_cb)
    DLL.SetComboBoxCallback(combo_edit, combo_cb)

    base.button(page, "RO1", "只读第1项", 1044, 118, 116, 34, 0xFF409EFF, lambda: set_readonly_index(0, "只读 ComboBox 已选中第 1 项"))
    base.button(page, "RO4", "只读第4项", 1172, 118, 116, 34, 0xFF67C23A, lambda: set_readonly_index(3, "只读 ComboBox 已选中第 4 项"))
    base.button(page, "ED2", "编辑第2项", 1300, 118, 124, 34, 0xFF8E44AD, lambda: set_edit_index(1, "可编辑 ComboBox 已选中第 2 项"))

    base.button(page, "ED4", "编辑第4项", 1044, 162, 116, 34, 0xFFE6A23C, lambda: set_edit_index(3, "可编辑 ComboBox 已选中第 4 项"))
    base.button(page, "TXT", "写入文本", 1172, 162, 116, 34, 0xFF409EFF, lambda: (DLL.SetComboBoxText(combo_edit, *s("手动写入 / Manual input")[:2]), refresh("可编辑 ComboBox 文本已写入")))
    base.button(page, "SEL", "回填选中", 1300, 162, 124, 34, 0xFF67C23A, fill_text_from_selection)

    base.button(page, "+", "新增项目", 1044, 206, 116, 34, 0xFF409EFF, add_item)
    base.button(page, "-", "删除末项", 1172, 206, 116, 34, 0xFFE6A23C, remove_last_item)
    base.button(page, "CLR", "清空列表", 1300, 206, 124, 34, 0xFF909399, clear_items)

    base.button(page, "RST", "恢复项目", 1044, 250, 116, 34, 0xFF67C23A, restore_items)
    base.button(page, "BLUE", "蓝色方案", 1172, 250, 116, 34, 0xFF409EFF, lambda: (DLL.SetComboBoxColors(combo_edit, THEME_PRIMARY, THEME_SURFACE_PRIMARY, THEME_PRIMARY, THEME_SURFACE), refresh("可编辑 ComboBox 已切到蓝色方案")))
    base.button(page, "WARM", "暖色方案", 1300, 250, 124, 34, 0xFFE6A23C, lambda: (DLL.SetComboBoxColors(combo_edit, THEME_WARNING, THEME_SURFACE_WARNING, THEME_WARNING, THEME_SURFACE), refresh("可编辑 ComboBox 已切到暖色方案")))

    base.button(page, "MOVE", "右移 80", 1044, 294, 116, 34, 0xFF67C23A, lambda: move_edit(dx=80))
    base.button(page, "WIDE", "加宽 140", 1172, 294, 116, 34, 0xFF8E44AD, lambda: move_edit(dw=140))
    base.button(page, "ENA", "禁用/启用", 1300, 294, 124, 34, 0xFF909399, toggle_enabled)

    base.button(page, "VIS", "显示/隐藏", 1044, 338, 116, 34, 0xFF409EFF, toggle_visible)
    base.button(page, "DEF", "恢复默认", 1172, 338, 252, 34, 0xFF67C23A, restore)

    register_theme_label(
        base.label(
            page,
            "说明：EnableComboBox 在 DLL 内只同步内部状态和编辑子句柄，没有同步最外层 ComboBox 窗口的 EnableWindow，所以这里在 Python 页面侧显式维护启用状态。",
            1044,
            394,
            380,
            72,
            fg=muted_color,
            bg=page_bg,
            wrap=True,
        ),
        "muted",
        "page",
    )

    register_theme_label(base.label(page, "1. GetComboItemCount / GetComboSelectedIndex / GetComboItemText / GetComboBoxText：读取项目数、选中项、选中文本和当前文本。", 40, 598, 1120, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "2. AddComboItem / RemoveComboItem / ClearComboBox：直接操作下拉项目列表。", 40, 632, 900, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "3. SetComboSelectedIndex / SetComboBoxText / SetComboBoxCallback：程序设置当前选中项、输入文本和选择回调。", 40, 666, 1120, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "4. SetComboBoxColors / GetComboBoxColors / SetComboBoxBounds：切换颜色方案和调整布局。", 40, 700, 1040, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "5. EnableComboBox / ShowComboBox：演示启用态和可见态切换；启用状态在页面侧显式维护。", 40, 734, 1220, 24, fg=text_color, bg=page_bg), "text", "page")
    refresh("组合框页已整理：只保留普通 ComboBox，并补齐项目 / 文本 / 颜色 / 状态读写")


def build_page_datetime(page: HWND) -> None:
    build_label_property_demo(page, "日期时间页标签演示", 1020, 16, 444, 176)
    base.groupbox(page, "📅 D2DDateTimePicker 实时属性读取", 16, 16, 980, 248)
    base.groupbox(page, "🛠️ 时间值 / 精度 / 颜色 / 布局", 16, 286, 980, 254)
    base.groupbox(page, "🗓️ 日期时间状态开关", 1020, 212, 444, 328)
    base.groupbox(page, "📘 D2DDateTimePicker API 说明", 16, 558, 1448, 230)

    picker = DLL.CreateD2DDateTimePicker(page, 56, 120, 340, 38, DTP_YMDHM, THEME_TEXT, THEME_BG, THEME_BORDER, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    DLL.SetD2DDateTimePickerDateTime(picker, 2026, 3, 30, 14, 30, 0)
    readout = base.label(page, "等待读取日期时间属性…", 40, 184, 920, 56, fg=0xFF303133, bg=0xFFF5F7FA, wrap=True)
    state_text = base.label(page, "日期时间页状态将在这里更新。", 40, 760, 1360, 22, fg=0xFF409EFF, bg=0xFFF5F7FA)
    base.label(page, "这一页直接读取日期时间值、精度、颜色、位置尺寸、可见态和启用态。", 40, 56, 900, 24, fg=0xFF606266, bg=0xFFF5F7FA)

    c_fg0 = UINT32(); c_bg0 = UINT32(); c_border0 = UINT32()
    DLL.GetD2DDateTimePickerColors(picker, ctypes.byref(c_fg0), ctypes.byref(c_bg0), ctypes.byref(c_border0))

    def read_bounds() -> tuple[int, int, int, int]:
        rc = RECT()
        USER32.GetWindowRect(picker, ctypes.byref(rc))
        root = LOCAL["host"]
        pt = POINT(rc.left, rc.top)
        USER32.ScreenToClient(root, ctypes.byref(pt))
        return pt.x, pt.y, rc.right - rc.left, rc.bottom - rc.top

    def refresh(note: str = "已刷新日期时间属性") -> None:
        fg = UINT32(); bg = UINT32(); border = UINT32()
        DLL.GetD2DDateTimePickerColors(picker, ctypes.byref(fg), ctypes.byref(bg), ctypes.byref(border))
        x, y, w, h = read_bounds()
        precision = int(DLL.GetD2DDateTimePickerPrecision(picker))
        visible = "显示" if USER32.IsWindowVisible(picker) else "隐藏"
        enabled = "启用" if USER32.IsWindowEnabled(picker) else "禁用"
        base.set_label_text(
            readout,
            f"datetime={base.dt_text(picker)}  precision={precision}  {visible}/{enabled}\n"
            f"bounds=({x}, {y}, {w}, {h})\n"
            f"fg=0x{int(fg.value):08X}  bg=0x{int(bg.value):08X}  border=0x{int(border.value):08X}"
        )
        base.set_label_text(state_text, note)
        base.set_status(note)

    base.button(page, "📅", "设为 2026-03-30", 40, 360, 156, 36, 0xFF409EFF, lambda: (DLL.SetD2DDateTimePickerDateTime(picker, 2026, 3, 30, 14, 30, 0), refresh("日期时间已设为 2026-03-30 14:30:00")))
    base.button(page, "⏰", "设为 2027-01-01", 212, 360, 156, 36, 0xFF67C23A, lambda: (DLL.SetD2DDateTimePickerDateTime(picker, 2027, 1, 1, 9, 0, 0), refresh("日期时间已设为 2027-01-01 09:00:00")))
    base.button(page, "🕒", "精度 YMD", 384, 360, 156, 36, 0xFF8E44AD, lambda: (DLL.SetD2DDateTimePickerPrecision(picker, DTP_YMD), refresh("日期时间精度已切到 YMD")))
    base.button(page, "🕓", "精度 YMDHM", 556, 360, 156, 36, 0xFFE6A23C, lambda: (DLL.SetD2DDateTimePickerPrecision(picker, DTP_YMDHM), refresh("日期时间精度已切到 YMDHM")))
    base.button(page, "🕕", "精度 YMDHMS", 728, 360, 156, 36, 0xFF409EFF, lambda: (DLL.SetD2DDateTimePickerPrecision(picker, DTP_YMDHMS), refresh("日期时间精度已切到 YMDHMS")))

    base.button(page, "💙", "冷色", 40, 448, 118, 36, 0xFF409EFF, lambda: (DLL.SetD2DDateTimePickerColors(picker, THEME_PRIMARY, THEME_SURFACE_PRIMARY, THEME_PRIMARY), refresh("日期时间选择框已切到冷色方案")))
    base.button(page, "🧡", "暖色", 172, 448, 118, 36, 0xFFE6A23C, lambda: (DLL.SetD2DDateTimePickerColors(picker, THEME_WARNING, THEME_SURFACE_WARNING, THEME_WARNING), refresh("日期时间选择框已切到暖色方案")))
    base.button(page, "➡️", "右移 80", 304, 448, 118, 36, 0xFF67C23A, lambda: (DLL.SetD2DDateTimePickerBounds(picker, 136, 120, 340, 38), refresh("日期时间选择框已右移 80")))
    base.button(page, "↔️", "加宽 100", 436, 448, 118, 36, 0xFF8E44AD, lambda: (DLL.SetD2DDateTimePickerBounds(picker, 56, 120, 440, 38), refresh("日期时间选择框已加宽到 440")))

    base.button(page, "🚫", "禁用/启用", 1044, 286, 118, 36, 0xFF409EFF, lambda: (DLL.EnableD2DDateTimePicker(picker, BOOL(not USER32.IsWindowEnabled(picker))), refresh("日期时间选择框启用状态已切换")))
    base.button(page, "👁️", "显示/隐藏", 1176, 286, 118, 36, 0xFF909399, lambda: (DLL.ShowD2DDateTimePicker(picker, BOOL(not USER32.IsWindowVisible(picker))), refresh("日期时间选择框可见状态已切换")))
    base.button(page, "↺", "恢复默认", 1308, 286, 118, 36, 0xFF67C23A, lambda: (DLL.SetD2DDateTimePickerBounds(picker, 56, 120, 340, 38), DLL.SetD2DDateTimePickerPrecision(picker, DTP_YMDHM), DLL.SetD2DDateTimePickerDateTime(picker, 2026, 3, 30, 14, 30, 0), DLL.SetD2DDateTimePickerColors(picker, int(c_fg0.value), int(c_bg0.value), int(c_border0.value)), DLL.EnableD2DDateTimePicker(picker, BOOL(True)), DLL.ShowD2DDateTimePicker(picker, BOOL(True)), refresh("日期时间页已恢复默认状态")))
    base.label(page, "这里保留绝对时间值，不用“今天/明天”这类相对词，方便你做精确回归。当前默认值是 2026-03-30 14:30:00。", 1044, 344, 382, 56, fg=0xFF606266, bg=0xFFF5F7FA, wrap=True)

    base.label(page, "1. GetD2DDateTimePickerDateTime / SetD2DDateTimePickerDateTime：读写具体时间。", 40, 598, 900, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "2. GetD2DDateTimePickerPrecision / SetD2DDateTimePickerPrecision：切换显示精度。", 40, 632, 980, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "3. GetD2DDateTimePickerColors / SetD2DDateTimePickerColors：切换颜色方案。", 40, 666, 980, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "4. SetD2DDateTimePickerBounds / EnableD2DDateTimePicker / ShowD2DDateTimePicker：切换布局与状态。", 40, 700, 1080, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "5. 这一页用绝对日期做演示，避免相对时间导致的测试歧义。", 40, 734, 900, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    refresh("日期时间页已加载，可直接测试日期时间属性读取与设置")


def build_page_editbox(page: HWND) -> None:
    build_label_property_demo(page, "编辑框页标签演示", 1020, 16, 444, 176)
    base.groupbox(page, "⌨️ EditBox 实时属性读取", 16, 16, 980, 248)
    base.groupbox(page, "🛠️ 文本 / 颜色 / 尺寸 / 状态", 16, 286, 980, 254)
    base.groupbox(page, "📝 多行 EditBox 演示", 1020, 212, 444, 328)
    base.groupbox(page, "📌 EditBox API 说明", 16, 558, 1448, 230)

    demo_edit = base.edit(page, "📘 单行 EditBox：可直接读取和设置文本。", 56, 120, 420, 38, False)
    memo = DLL.CreateEditBox(
        page,
        1044,
        262,
        380,
        166,
        *s("📝 多行 EditBox 示例：\r\n1. 用于展示多行输入\r\n2. 保持统一浅底风格\r\n3. 可作为备注或说明区域")[:2],
        THEME_TEXT,
        THEME_BG,
        base.FONT_PTR,
        base.FONT_LEN,
        13,
        BOOL(False),
        BOOL(False),
        BOOL(False),
        base.ALIGN_LEFT,
        BOOL(True),
        BOOL(False),
        BOOL(False),
        BOOL(True),
        BOOL(False),
    )
    readout = base.label(page, "等待读取编辑框属性。", 40, 184, 920, 56, fg=0xFF303133, bg=0xFFF5F7FA, wrap=True)
    state_text = base.label(page, "编辑框页状态将在这里更新。", 40, 760, 1360, 22, fg=0xFF409EFF, bg=0xFFF5F7FA)
    base.label(page, "这一页直接读取文本、颜色、位置、字体、启用态和可见态，不再只是放一个输入框。", 40, 56, 900, 24, fg=0xFF606266, bg=0xFFF5F7FA)

    def read_utf8_edit(h_edit: HWND) -> str:
        size = int(DLL.GetEditBoxText(h_edit, None, 0))
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        DLL.GetEditBoxText(h_edit, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    def read_edit_bounds() -> tuple[int, int, int, int]:
        x = ctypes.c_int()
        y = ctypes.c_int()
        w = ctypes.c_int()
        h = ctypes.c_int()
        if int(DLL.GetEditBoxBounds(demo_edit, ctypes.byref(x), ctypes.byref(y), ctypes.byref(w), ctypes.byref(h))) != 0:
            return 0, 0, 0, 0
        return x.value, y.value, w.value, h.value

    def read_edit_font() -> tuple[str, int, int]:
        buf = ctypes.create_string_buffer(128)
        size = ctypes.c_int()
        bold = ctypes.c_int()
        italic = ctypes.c_int()
        underline = ctypes.c_int()
        result = int(DLL.GetEditBoxFont(demo_edit, buf, 128, ctypes.byref(size), ctypes.byref(bold), ctypes.byref(italic), ctypes.byref(underline)))
        name = buf.raw[:max(result, 0)].decode("utf-8", errors="replace") if result > 0 else ""
        return name, size.value, bold.value

    fg0 = UINT32()
    bg0 = UINT32()
    DLL.GetEditBoxColor(demo_edit, ctypes.byref(fg0), ctypes.byref(bg0))
    initial = {
        "text": read_utf8_edit(demo_edit),
        "bounds": read_edit_bounds(),
        "fg": int(fg0.value),
        "bg": int(bg0.value),
    }

    def refresh(note: str = "已刷新编辑框属性") -> None:
        fg = UINT32()
        bg = UINT32()
        DLL.GetEditBoxColor(demo_edit, ctypes.byref(fg), ctypes.byref(bg))
        x, y, w, h = read_edit_bounds()
        font_name, font_size, bold = read_edit_font()
        align_name = base.alignment_name(int(DLL.GetEditBoxAlignment(demo_edit)))
        enabled = "启用" if int(DLL.GetEditBoxEnabled(demo_edit)) == 1 else "禁用"
        visible = "显示" if int(DLL.GetEditBoxVisible(demo_edit)) == 1 else "隐藏"
        base.set_label_text(
            readout,
            f"text={read_utf8_edit(demo_edit)}  {visible}/{enabled}\n"
            f"bounds=({x}, {y}, {w}, {h})  align={align_name}  font={font_name or 'default'} {font_size}px bold={bold}\n"
            f"fg=0x{int(fg.value):08X}  bg=0x{int(bg.value):08X}"
        )
        base.set_label_text(state_text, note)
        base.set_status(note)

    def set_edit_text_value(text: str, note: str) -> None:
        DLL.SetEditBoxText(demo_edit, *s(text)[:2])
        refresh(note)

    def set_edit_colors(fg: int, bg: int, note: str) -> None:
        DLL.SetEditBoxColor(demo_edit, fg, bg)
        refresh(note)

    def set_edit_font_value(font_name: str, font_size: int, bold: bool, note: str) -> None:
        DLL.SetEditBoxFont(demo_edit, *s(font_name)[:2], font_size, BOOL(bold), BOOL(False), BOOL(False))
        refresh(note)

    def move_edit(dx: int = 0, dy: int = 0, dw: int = 0) -> None:
        x, y, w, h = read_edit_bounds()
        DLL.SetEditBoxBounds(demo_edit, x + dx, y + dy, w + dw, h)
        refresh(f"编辑框位置/尺寸已更新: dx={dx}, dy={dy}, dw={dw}")

    def restore_edit() -> None:
        x, y, w, h = initial["bounds"]
        DLL.SetEditBoxText(demo_edit, *s(str(initial["text"]))[:2])
        DLL.SetEditBoxColor(demo_edit, int(initial["fg"]), int(initial["bg"]))
        DLL.SetEditBoxBounds(demo_edit, int(x), int(y), int(w), int(h))
        DLL.SetEditBoxFont(demo_edit, *s("Segoe UI Emoji")[:2], 13, BOOL(False), BOOL(False), BOOL(False))
        DLL.EnableEditBox(demo_edit, BOOL(True))
        DLL.ShowEditBox(demo_edit, BOOL(True))
        refresh("编辑框属性已恢复默认")

    base.label(page, "📘 文本预设", 40, 326, 180, 22, fg=0xFF303133, bg=0xFFF5F7FA, size=15, bold=True)
    base.button(page, "🗂️", "写入表单文案", 40, 360, 156, 36, 0xFF409EFF, lambda: set_edit_text_value("请输入项目名称 / 关键字 / 标题", "编辑框文本已切到表单模式"))
    base.button(page, "🌈", "写入混排文案", 212, 360, 156, 36, 0xFF67C23A, lambda: set_edit_text_value("🌈 EmojiWindow 支持 emoji / English / 数字 123", "编辑框文本已切到混排模式"))
    base.button(page, "📝", "同步到多行框", 384, 360, 156, 36, 0xFF8E44AD, lambda: (DLL.SetEditBoxText(memo, *s("📝 已从主编辑框同步：\r\n" + read_utf8_edit(demo_edit))[:2]), refresh("当前单行内容已同步到多行 EditBox")))

    base.label(page, "🎨 颜色 / 字体", 40, 414, 180, 22, fg=0xFF303133, bg=0xFFF5F7FA, size=15, bold=True)
    base.button(page, "💙", "冷色", 40, 448, 118, 36, 0xFF409EFF, lambda: set_edit_colors(THEME_PRIMARY, THEME_SURFACE_PRIMARY, "编辑框已切到冷色方案"))
    base.button(page, "🧡", "暖色", 172, 448, 118, 36, 0xFFE6A23C, lambda: set_edit_colors(THEME_WARNING, THEME_SURFACE_WARNING, "编辑框已切到暖色方案"))
    base.button(page, "🔠", "16px Bold", 304, 448, 118, 36, 0xFF67C23A, lambda: set_edit_font_value("Segoe UI Emoji", 16, True, "编辑框字体已切到 16px Bold"))
    base.button(page, "🪶", "13px", 436, 448, 118, 36, 0xFF909399, lambda: set_edit_font_value("Segoe UI Emoji", 13, False, "编辑框字体已切回 13px"))

    base.label(page, "📻 布局 / 状态", 1044, 432, 180, 22, fg=0xFF303133, bg=0xFFF5F7FA, size=15, bold=True)
    base.button(page, "➡️", "右移 80", 1044, 466, 118, 36, 0xFF409EFF, lambda: move_edit(dx=80))
    base.button(page, "⬇️", "下移 24", 1176, 466, 118, 36, 0xFF67C23A, lambda: move_edit(dy=24))
    base.button(page, "↔️", "加宽 120", 1308, 466, 118, 36, 0xFFE6A23C, lambda: move_edit(dw=120))
    base.button(page, "🚫", "禁用/启用", 1044, 510, 118, 36, 0xFF8E44AD, lambda: (DLL.EnableEditBox(demo_edit, BOOL(not (int(DLL.GetEditBoxEnabled(demo_edit)) == 1))), refresh("编辑框启用状态已切换")))
    base.button(page, "👁️", "显示/隐藏", 1176, 510, 118, 36, 0xFF909399, lambda: (DLL.ShowEditBox(demo_edit, BOOL(not (int(DLL.GetEditBoxVisible(demo_edit)) == 1))), refresh("编辑框可见状态已切换")))
    base.button(page, "↺", "恢复默认", 1308, 510, 118, 36, 0xFF409EFF, restore_edit)

    base.label(page, "1. GetEditBoxText / SetEditBoxText：读取和修改输入文本。", 40, 598, 640, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "2. GetEditBoxColor / SetEditBoxColor：读取和切换前景色 / 背景色。", 40, 632, 700, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "3. GetEditBoxBounds / SetEditBoxBounds：直接修改编辑框位置与宽度。", 40, 666, 760, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "4. GetEditBoxFont / SetEditBoxFont：读取和切换字体名、字号和粗体。", 40, 700, 760, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    base.label(page, "5. EnableEditBox / ShowEditBox：演示启用态和可见态切换。", 40, 734, 720, 24, fg=0xFF303133, bg=0xFFF5F7FA)
    refresh("编辑框页已加载，可直接测试编辑框属性读取与设置")


def build_page_d2d_combobox_enhanced(page: HWND) -> None:
    build_label_property_demo(page, "D2D 组合框页标签演示", 1000, 16, 464, 176)
    base.groupbox(page, "🫧 D2DComboBox 属性读取 / 设置", 16, 16, 960, 360)
    out = base.label(page, "等待读取 D2DComboBox。", 40, 320, 860, 24, fg=0xFF606266, bg=0xFFF5F7FA)
    combo = DLL.CreateD2DComboBox(page, 40, 110, 320, 40, BOOL(False), THEME_TEXT, THEME_BG, 32, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    for item in ("🌟 D2D 默认", "🎨 D2D 主题", "🚀 D2D 高亮", "🧩 D2D 大空间"):
        p, n, _ = s(item)
        DLL.AddD2DComboItem(combo, p, n)
    DLL.SetD2DComboSelectedIndex(combo, 2)
    DLL.SetD2DComboBoxColors(combo, THEME_TEXT, THEME_BG, THEME_SURFACE_PRIMARY, THEME_SURFACE, THEME_BORDER_LIGHT, THEME_SURFACE)

    def refresh(prefix: str = "D2DComboBox 读取结果") -> None:
        idx = int(DLL.GetD2DComboSelectedIndex(combo))
        base.set_label_text(out, f"{prefix}: index={idx}")
        base.set_status(f"{prefix}: index={idx}")

    cb = DLL._ComboCB(lambda _h, idx: (base.set_label_text(out, f"D2DComboBox 读取结果: index={idx}"), base.set_status(f"D2DComboBox -> {idx}")))
    KEEP.append(cb)
    DLL.SetD2DComboBoxCallback(combo, cb)
    base.button(page, "1", "选第 1 项", 400, 110, 120, 34, 0xFF409EFF, lambda: (DLL.SetD2DComboSelectedIndex(combo, 0), refresh("D2DComboBox 程序设置")))
    base.button(page, "4", "选第 4 项", 536, 110, 120, 34, 0xFF67C23A, lambda: (DLL.SetD2DComboSelectedIndex(combo, 3), refresh("D2DComboBox 程序设置")))
    base.label(page, "D2D 组合框页保留独立页面，用于验证样式、选择变化和回调。", 400, 166, 520, 24, fg=0xFF606266, bg=0xFFF5F7FA)
    refresh()


def build_page_d2d_combobox_v2(page: HWND) -> None:
    palette = page_palette()
    page_bg = palette["page_bg"]
    text_color = palette["text"]
    muted_color = palette["muted"]
    accent_color = palette["accent"]

    base.groupbox(page, "D2DComboBox 模式与事件", 16, 16, 980, 520)
    base.groupbox(page, "文本 / 项目 / 颜色 / 状态", 1020, 16, 444, 520)
    base.groupbox(page, "D2DComboBox API 说明", 16, 558, 1448, 220)

    register_theme_label(
        base.label(
            page,
            "这一页只保留 D2DComboBox。本页同时放置只读和可编辑两种模式，回调、文本读写、项目增删、颜色和布局都集中在这里演示。",
            40,
            56,
            930,
            24,
            fg=muted_color,
            bg=page_bg,
            wrap=True,
        ),
        "muted",
        "page",
    )
    register_theme_label(base.label(page, "只读 D2DComboBox", 56, 104, 220, 20, fg=text_color, bg=page_bg, size=14, bold=True), "text", "page")
    combo_readonly = DLL.CreateD2DComboBox(page, 56, 128, 560, 40, BOOL(True), THEME_TEXT, THEME_BG, 32, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    register_theme_label(base.label(page, "可编辑 D2DComboBox", 56, 216, 220, 20, fg=text_color, bg=page_bg, size=14, bold=True), "text", "page")
    combo_edit = DLL.CreateD2DComboBox(page, 56, 240, 560, 40, BOOL(False), THEME_TEXT, THEME_BG, 32, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))

    readonly_items = [
        "🧭 D2D 默认",
        "🎨 D2D 主题",
        "🚀 D2D 高亮",
        "🧩 D2D 扩展",
    ]
    edit_items = [
        "📝 可编辑默认",
        "🌈 彩色文案",
        "⚠️ 紧急提示",
        "✨ 高亮条目",
    ]

    def fill_combo(hwnd: HWND, items: list[str]) -> None:
        DLL.ClearD2DComboBox(hwnd)
        for item in items:
            DLL.AddD2DComboItem(hwnd, *s(item)[:2])

    fill_combo(combo_readonly, readonly_items)
    fill_combo(combo_edit, edit_items)
    DLL.SetD2DComboSelectedIndex(combo_readonly, 1)
    DLL.SetD2DComboSelectedIndex(combo_edit, 1)
    DLL.SetD2DComboBoxColors(combo_readonly, THEME_TEXT, THEME_BG, THEME_SURFACE_PRIMARY, THEME_SURFACE, THEME_BORDER_LIGHT, THEME_SURFACE)
    DLL.SetD2DComboBoxColors(combo_edit, THEME_TEXT, THEME_BG, THEME_SURFACE_PRIMARY, THEME_SURFACE, THEME_BORDER_LIGHT, THEME_SURFACE)

    register_theme_label(
        base.label(
            page,
            "左侧两只控件都是真实 D2DComboBox。只读款用于验证 readonly 模式和选中回调，右侧操作默认作用于下方可编辑 D2DComboBox。",
            56,
            298,
            900,
            38,
            fg=muted_color,
            bg=page_bg,
            wrap=True,
        ),
        "muted",
        "page",
    )
    readout = register_theme_label(
        base.label(page, "等待读取 D2DComboBox 状态。", 40, 350, 920, 104, fg=text_color, bg=page_bg, wrap=True),
        "text",
        "page",
    )
    state_text = register_theme_label(
        base.label(page, "D2DComboBox 页状态将在这里更新。", 40, 474, 1360, 22, fg=accent_color, bg=page_bg),
        "accent",
        "page",
    )

    register_theme_label(
        base.label(
            page,
            "首行保留只读 D2DComboBox 的程序选中操作。其余按钮覆盖可编辑 D2DComboBox 的回调、文本、项目、颜色、显示和启用状态。",
            1044,
            56,
            380,
            44,
            fg=muted_color,
            bg=page_bg,
            wrap=True,
        ),
        "muted",
        "page",
    )

    edit_fg0 = UINT32()
    edit_bg0 = UINT32()
    edit_sel0 = UINT32()
    edit_hover0 = UINT32()
    edit_border0 = UINT32()
    edit_btn0 = UINT32()
    DLL.GetD2DComboBoxColors(combo_edit, ctypes.byref(edit_fg0), ctypes.byref(edit_bg0), ctypes.byref(edit_sel0), ctypes.byref(edit_hover0), ctypes.byref(edit_border0), ctypes.byref(edit_btn0))

    edit_bounds = {"x": 56, "y": 240, "w": 560, "h": 40}
    combo_flags = {"edit_enabled": True}
    next_item_id = {"value": 1}

    def read_utf8(call, *args) -> str:
        size = int(call(*args, None, 0))
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        call(*args, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    def read_item_text(hwnd: HWND, index: int) -> str:
        if index < 0:
            return "(无选中)"
        size = int(DLL.GetD2DComboItemText(hwnd, index, None, 0))
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        DLL.GetD2DComboItemText(hwnd, index, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    def read_bounds(hwnd: HWND) -> tuple[int, int, int, int]:
        rc = RECT()
        USER32.GetWindowRect(hwnd, ctypes.byref(rc))
        root = LOCAL["host"]
        pt = POINT(rc.left, rc.top)
        USER32.ScreenToClient(root, ctypes.byref(pt))
        return pt.x, pt.y, rc.right - rc.left, rc.bottom - rc.top

    def refresh(note: str = "已刷新 D2DComboBox 状态") -> None:
        ro_fg = UINT32()
        ro_bg = UINT32()
        ro_sel = UINT32()
        ro_hover = UINT32()
        ro_border = UINT32()
        ro_btn = UINT32()
        DLL.GetD2DComboBoxColors(combo_readonly, ctypes.byref(ro_fg), ctypes.byref(ro_bg), ctypes.byref(ro_sel), ctypes.byref(ro_hover), ctypes.byref(ro_border), ctypes.byref(ro_btn))
        ed_fg = UINT32()
        ed_bg = UINT32()
        ed_sel = UINT32()
        ed_hover = UINT32()
        ed_border = UINT32()
        ed_btn = UINT32()
        DLL.GetD2DComboBoxColors(combo_edit, ctypes.byref(ed_fg), ctypes.byref(ed_bg), ctypes.byref(ed_sel), ctypes.byref(ed_hover), ctypes.byref(ed_border), ctypes.byref(ed_btn))

        ro_index = int(DLL.GetD2DComboSelectedIndex(combo_readonly))
        ed_index = int(DLL.GetD2DComboSelectedIndex(combo_edit))
        ro_count = int(DLL.GetD2DComboItemCount(combo_readonly))
        ed_count = int(DLL.GetD2DComboItemCount(combo_edit))
        ro_x, ro_y, ro_w, ro_h = read_bounds(combo_readonly)
        ed_x, ed_y, ed_w, ed_h = read_bounds(combo_edit)
        ed_visible = "显示" if USER32.IsWindowVisible(combo_edit) else "隐藏"
        ed_enabled = "启用" if bool(combo_flags["edit_enabled"]) else "禁用"

        base.set_label_text(
            readout,
            f"只读: count={ro_count}  selected={ro_index}  selected_text={read_utf8(DLL.GetD2DComboSelectedText, combo_readonly)}  text={read_utf8(DLL.GetD2DComboText, combo_readonly)}\n"
            f"只读 bounds=({ro_x}, {ro_y}, {ro_w}, {ro_h})  fg/bg=0x{int(ro_fg.value):08X}/0x{int(ro_bg.value):08X}  border/button=0x{int(ro_border.value):08X}/0x{int(ro_btn.value):08X}\n"
            f"编辑: count={ed_count}  selected={ed_index}  selected_text={read_utf8(DLL.GetD2DComboSelectedText, combo_edit)}  text={read_utf8(DLL.GetD2DComboText, combo_edit)}\n"
            f"编辑 bounds=({ed_x}, {ed_y}, {ed_w}, {ed_h})  {ed_visible}/{ed_enabled}  fg/bg=0x{int(ed_fg.value):08X}/0x{int(ed_bg.value):08X}  select/hover=0x{int(ed_sel.value):08X}/0x{int(ed_hover.value):08X}  border/button=0x{int(ed_border.value):08X}/0x{int(ed_btn.value):08X}"
        )
        base.set_label_text(state_text, note)
        base.set_status(note)

    def set_readonly_index(index: int, note: str) -> None:
        if int(DLL.GetD2DComboItemCount(combo_readonly)) <= index:
            refresh("只读 D2DComboBox 项目数量不足，无法选中该项")
            return
        DLL.SetD2DComboSelectedIndex(combo_readonly, index)
        refresh(note)

    def set_edit_index(index: int, note: str) -> None:
        if int(DLL.GetD2DComboItemCount(combo_edit)) <= index:
            refresh("可编辑 D2DComboBox 项目数量不足，无法选中该项")
            return
        DLL.SetD2DComboSelectedIndex(combo_edit, index)
        refresh(note)

    def add_item() -> None:
        text = f"🆕 D2D 新增 {next_item_id['value']}"
        next_item_id["value"] += 1
        DLL.AddD2DComboItem(combo_edit, *s(text)[:2])
        DLL.SetD2DComboSelectedIndex(combo_edit, int(DLL.GetD2DComboItemCount(combo_edit)) - 1)
        refresh("可编辑 D2DComboBox 已新增一项并选中末项")

    def remove_last_item() -> None:
        count = int(DLL.GetD2DComboItemCount(combo_edit))
        if count <= 0:
            refresh("可编辑 D2DComboBox 当前没有可删除的项目")
            return
        DLL.RemoveD2DComboItem(combo_edit, count - 1)
        if int(DLL.GetD2DComboItemCount(combo_edit)) > 0:
            DLL.SetD2DComboSelectedIndex(combo_edit, max(0, int(DLL.GetD2DComboItemCount(combo_edit)) - 1))
        refresh("可编辑 D2DComboBox 已删除末项")

    def clear_items() -> None:
        DLL.ClearD2DComboBox(combo_edit)
        refresh("可编辑 D2DComboBox 项目已清空")

    def restore_items() -> None:
        fill_combo(combo_edit, edit_items)
        DLL.SetD2DComboSelectedIndex(combo_edit, 1)
        next_item_id["value"] = 1
        refresh("可编辑 D2DComboBox 项目已恢复默认列表")

    def set_text_manual() -> None:
        DLL.SetD2DComboText(combo_edit, *s("🫧 D2D 手动输入 / Manual input")[:2])
        refresh("可编辑 D2DComboBox 文本已写入")

    def fill_text_from_selection() -> None:
        selected_text = read_utf8(DLL.GetD2DComboSelectedText, combo_edit)
        if not selected_text:
            refresh("当前没有选中项，无法回填文本")
            return
        DLL.SetD2DComboText(combo_edit, *s(selected_text)[:2])
        refresh("已将当前选中项回填到可编辑 D2DComboBox 文本")

    def move_edit(dx: int = 0, dw: int = 0) -> None:
        edit_bounds["x"] += dx
        edit_bounds["w"] += dw
        DLL.SetD2DComboBoxBounds(combo_edit, edit_bounds["x"], edit_bounds["y"], edit_bounds["w"], edit_bounds["h"])
        refresh(f"可编辑 D2DComboBox 布局已更新: dx={dx}, dw={dw}")

    def toggle_enabled() -> None:
        next_enabled = not bool(combo_flags["edit_enabled"])
        combo_flags["edit_enabled"] = next_enabled
        DLL.EnableD2DComboBox(combo_edit, BOOL(next_enabled))
        refresh("可编辑 D2DComboBox 启用状态已切换")

    def toggle_visible() -> None:
        DLL.ShowD2DComboBox(combo_edit, BOOL(not USER32.IsWindowVisible(combo_edit)))
        refresh("可编辑 D2DComboBox 可见状态已切换")

    def restore() -> None:
        fill_combo(combo_readonly, readonly_items)
        fill_combo(combo_edit, edit_items)
        DLL.SetD2DComboSelectedIndex(combo_readonly, 1)
        DLL.SetD2DComboSelectedIndex(combo_edit, 1)
        DLL.SetD2DComboText(combo_edit, *s(edit_items[1])[:2])
        edit_bounds["x"] = 56
        edit_bounds["y"] = 240
        edit_bounds["w"] = 560
        edit_bounds["h"] = 40
        DLL.SetD2DComboBoxBounds(combo_edit, edit_bounds["x"], edit_bounds["y"], edit_bounds["w"], edit_bounds["h"])
        DLL.SetD2DComboBoxColors(combo_edit, int(edit_fg0.value), int(edit_bg0.value), int(edit_sel0.value), int(edit_hover0.value), int(edit_border0.value), int(edit_btn0.value))
        DLL.ShowD2DComboBox(combo_edit, BOOL(True))
        DLL.EnableD2DComboBox(combo_edit, BOOL(True))
        combo_flags["edit_enabled"] = True
        next_item_id["value"] = 1
        refresh("D2DComboBox 页已恢复默认状态")

    def on_combo_changed(hwnd: HWND, index: int) -> None:
        which = "只读 D2DComboBox" if base.hwnd_key(hwnd) == base.hwnd_key(combo_readonly) else "可编辑 D2DComboBox"
        selected_text = read_item_text(hwnd, index)
        refresh(f"{which} 回调: selected={index} text={selected_text}")

    combo_cb = DLL._ComboCB(on_combo_changed)
    KEEP.append(combo_cb)
    DLL.SetD2DComboBoxCallback(combo_readonly, combo_cb)
    DLL.SetD2DComboBoxCallback(combo_edit, combo_cb)

    base.button(page, "RO1", "只读第1项", 1044, 118, 116, 34, 0xFF409EFF, lambda: set_readonly_index(0, "只读 D2DComboBox 已选中第 1 项"))
    base.button(page, "RO4", "只读第4项", 1172, 118, 116, 34, 0xFF67C23A, lambda: set_readonly_index(3, "只读 D2DComboBox 已选中第 4 项"))
    base.button(page, "ED2", "编辑第2项", 1300, 118, 124, 34, 0xFF8E44AD, lambda: set_edit_index(1, "可编辑 D2DComboBox 已选中第 2 项"))

    base.button(page, "ED4", "编辑第4项", 1044, 162, 116, 34, 0xFFE6A23C, lambda: set_edit_index(3, "可编辑 D2DComboBox 已选中第 4 项"))
    base.button(page, "TXT", "写入文本", 1172, 162, 116, 34, 0xFF409EFF, set_text_manual)
    base.button(page, "SEL", "回填选中", 1300, 162, 124, 34, 0xFF67C23A, fill_text_from_selection)

    base.button(page, "+", "新增项目", 1044, 206, 116, 34, 0xFF409EFF, add_item)
    base.button(page, "-", "删除末项", 1172, 206, 116, 34, 0xFFE6A23C, remove_last_item)
    base.button(page, "CLR", "清空列表", 1300, 206, 124, 34, 0xFF909399, clear_items)

    base.button(page, "RST", "恢复项目", 1044, 250, 116, 34, 0xFF67C23A, restore_items)
    base.button(page, "BLUE", "蓝色方案", 1172, 250, 116, 34, 0xFF409EFF, lambda: (DLL.SetD2DComboBoxColors(combo_edit, THEME_TEXT, THEME_SURFACE_PRIMARY, THEME_SURFACE_PRIMARY, THEME_SURFACE, THEME_PRIMARY, THEME_SURFACE_PRIMARY), refresh("可编辑 D2DComboBox 已切到蓝色方案")))
    base.button(page, "WARM", "暖色方案", 1300, 250, 124, 34, 0xFFE6A23C, lambda: (DLL.SetD2DComboBoxColors(combo_edit, THEME_TEXT, THEME_SURFACE_WARNING, THEME_WARNING, THEME_SURFACE, THEME_WARNING, THEME_SURFACE_WARNING), refresh("可编辑 D2DComboBox 已切到暖色方案")))

    base.button(page, "MOVE", "右移 80", 1044, 294, 116, 34, 0xFF67C23A, lambda: move_edit(dx=80))
    base.button(page, "WIDE", "加宽 160", 1172, 294, 116, 34, 0xFF8E44AD, lambda: move_edit(dw=160))
    base.button(page, "ENA", "禁用/启用", 1300, 294, 124, 34, 0xFF909399, toggle_enabled)

    base.button(page, "VIS", "显示/隐藏", 1044, 338, 116, 34, 0xFF409EFF, toggle_visible)
    base.button(page, "DEF", "恢复默认", 1172, 338, 252, 34, 0xFF67C23A, restore)

    register_theme_label(
        base.label(
            page,
            "说明：EnableD2DComboBox 在 DLL 内同样只同步内部状态和编辑子句柄，没有同步最外层 D2DComboBox 窗口的 EnableWindow，所以页面侧显式维护启用状态。",
            1044,
            394,
            380,
            72,
            fg=muted_color,
            bg=page_bg,
            wrap=True,
        ),
        "muted",
        "page",
    )

    register_theme_label(base.label(page, "1. GetD2DComboItemCount / GetD2DComboSelectedIndex / GetD2DComboItemText：读取项目数、选中项和项目文本。", 40, 598, 1120, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "2. GetD2DComboText / GetD2DComboSelectedText / SetD2DComboText：读取或修改输入区文本与当前选中文本。", 40, 632, 1120, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "3. AddD2DComboItem / RemoveD2DComboItem / ClearD2DComboBox：直接操作 D2D 下拉项目列表。", 40, 666, 1120, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "4. SetD2DComboSelectedIndex / SetD2DComboBoxCallback / SetD2DComboBoxColors：程序选中、回调读取和颜色切换。", 40, 700, 1200, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "5. SetD2DComboBoxBounds / EnableD2DComboBox / ShowD2DComboBox：演示布局、启用态和可见态切换。", 40, 734, 1160, 24, fg=text_color, bg=page_bg), "text", "page")
    refresh("D2DComboBox 页已整理：移除标签演示分组框，并补齐回调 / 文本 / 项目 / 颜色 / 状态读写")


def build_page_treeview_enhanced(page: HWND) -> None:
    build_label_property_demo(page, "树形框页标签演示", 16, 16, 420, 136)
    base.groupbox(page, "🌲 TreeView 页面说明", 460, 16, 1004, 136)
    base.label(page, "树形框页继续复用成熟的 Tree / Menu 综合演示区，包含展开折叠、侧边栏模式、多级节点和回调。", 484, 56, 940, 42, fg=0xFF606266, bg=0xFFF5F7FA, wrap=True)
    content = DLL.CreatePanel(page, 16, 170, 1448, 650, THEME_SURFACE)
    base.menu_tree_page(content)
    base.set_status("🌲 主树状态: ready，当前可直接测试展开/折叠/侧边栏与节点回调。")


def build_page_menubar_v2(page: HWND) -> None:
    palette = page_palette()
    card_bg = palette["card_bg"]
    text_color = palette["text"]
    muted_color = palette["muted"]
    accent_color = palette["accent"]

    base.groupbox(page, "📁 MenuBar 菜单舞台", 16, 16, 980, 520)
    base.groupbox(page, "🎛️ 状态 / 布局 / 文案", 1012, 16, 452, 520)
    base.groupbox(page, "📘 MenuBar API 说明", 16, 558, 1448, 220)

    stage_panel = DLL.CreatePanel(page, 30, 62, 952, 448, THEME_SURFACE)
    side_panel = DLL.CreatePanel(page, 1026, 62, 424, 448, THEME_SURFACE)
    api_panel = DLL.CreatePanel(page, 30, 602, 1420, 140, THEME_SURFACE)
    preview_panel = DLL.CreatePanel(stage_panel, 16, 104, 920, 248, THEME_BG)

    register_theme_label(
        base.label(
            stage_panel,
            "这一页只保留 MenuBar 控件，左侧是菜单舞台，右侧只放状态读取、布局调整、文案更新和菜单重建。",
            16,
            16,
            900,
            22,
            fg=muted_color,
            bg=card_bg,
            wrap=True,
        ),
        "muted",
        "card",
    )
    register_theme_label(base.label(stage_panel, "📁 菜单舞台", 16, 44, 200, 20, fg=text_color, bg=card_bg, size=14, bold=True), "text", "card")
    scene_label = register_theme_label(base.label(stage_panel, "当前场景: 等待菜单操作。", 16, 72, 920, 24, fg=accent_color, bg=card_bg, size=15, bold=True), "accent", "card")
    register_theme_label(base.label(stage_panel, "直接点击上方菜单，可验证一级菜单、二级菜单、三级子菜单、消息框/确认框回调，以及布局/文案更新是否立即生效。", 16, 364, 920, 42, fg=muted_color, bg=card_bg, wrap=True), "muted", "card")
    register_theme_label(base.label(stage_panel, "提示：这块区域只用于展示 MenuBar 的菜单行为，不再混入树形框、评分或其他组件。", 16, 414, 920, 20, fg=muted_color, bg=card_bg, wrap=True), "muted", "card")

    register_theme_label(base.label(preview_panel, "🧾 舞台说明", 16, 16, 180, 20, fg=text_color, bg=card_bg, size=14, bold=True), "text", "card")
    register_theme_label(base.label(preview_panel, "1. 第一组菜单用于演示对话框、状态写回和三级子菜单。", 16, 52, 420, 22, fg=text_color, bg=card_bg), "text", "card")
    register_theme_label(base.label(preview_panel, "2. 第二组菜单用于演示 SetMenuBarPlacement，直接改菜单栏宽度和纵向位置。", 16, 84, 520, 22, fg=text_color, bg=card_bg), "text", "card")
    register_theme_label(base.label(preview_panel, "3. 第三组菜单用于演示 MenuBarUpdateSubItemText、菜单方案切换和状态刷新。", 16, 116, 520, 22, fg=text_color, bg=card_bg), "text", "card")
    register_theme_label(base.label(preview_panel, "4. 右侧按钮和菜单里的“布局 / 工具”子项做的是同一套真实接口，不是摆设说明。", 16, 148, 560, 22, fg=text_color, bg=card_bg), "text", "card")
    register_theme_label(base.label(preview_panel, "5. 当前页只保留 MenuBar 本身，方便你单独看菜单行为，不再被其他演示内容干扰。", 16, 180, 560, 22, fg=text_color, bg=card_bg), "text", "card")

    register_theme_label(base.label(side_panel, "📡 菜单状态", 16, 16, 220, 20, fg=text_color, bg=card_bg, size=14, bold=True), "text", "card")
    readout = register_theme_label(base.label(side_panel, "等待读取 MenuBar 状态。", 16, 48, 392, 110, fg=text_color, bg=card_bg, wrap=True), "text", "card")
    register_theme_label(base.label(side_panel, "🧪 最近回调", 16, 176, 220, 20, fg=text_color, bg=card_bg, size=14, bold=True), "text", "card")
    callback_label = register_theme_label(base.label(side_panel, "等待触发 MenuBar 回调。", 16, 208, 392, 76, fg=muted_color, bg=card_bg, wrap=True), "muted", "card")
    state_text = register_theme_label(base.label(side_panel, "MenuBar 页状态将在这里更新。", 16, 288, 392, 22, fg=accent_color, bg=card_bg), "accent", "card")
    register_theme_label(base.label(side_panel, "右侧按钮只做改位置、改文案、重建菜单三类操作。", 16, 316, 392, 22, fg=muted_color, bg=card_bg, wrap=True), "muted", "card")

    MENU_FILE = 5000
    MENU_DIALOG = 5100
    MENU_MSG = 5110
    MENU_CONFIRM = 5111
    MENU_SCENE = 5200
    MENU_SCENE_RUNNING = 5210
    MENU_SCENE_DONE = 5211
    MENU_LAYOUT = 6000
    MENU_LAYOUT_LEFT = 6110
    MENU_LAYOUT_STD = 6111
    MENU_LAYOUT_WIDE = 6112
    MENU_LAYOUT_DOWN = 6113
    MENU_LAYOUT_RESET = 6114
    MENU_TOOLS = 7000
    MENU_TOOL_RENAME = 7100
    MENU_TOOL_RESTORE = 7101
    MENU_TOOL_TOGGLE_MODE = 7102
    MENU_TOOL_REFRESH = 7103

    menu_state: dict[str, object] = {
        "host": stage_panel,
        "bar": None,
        "mode": "default",
        "x": 16,
        "y": 46,
        "w": 720,
        "h": 34,
        "message_text": "💬 显示消息框",
        "scene": "等待菜单操作。",
        "last_menu_id": 0,
        "last_item_id": 0,
        "last_event": "尚未触发菜单回调。",
    }

    def mode_name() -> str:
        return "默认三级菜单" if menu_state["mode"] == "default" else "紧凑菜单"

    def add_item(bar: HWND, text: str, item_id: int) -> None:
        text_p, text_n, _ = s(text)
        DLL.MenuBarAddItem(bar, text_p, text_n, item_id)

    def add_sub(bar: HWND, parent_id: int, text: str, item_id: int) -> None:
        text_p, text_n, _ = s(text)
        DLL.MenuBarAddSubItem(bar, parent_id, text_p, text_n, item_id)

    def refresh(note: str | None = None, *, push_status: bool = False) -> None:
        base.set_label_text(scene_label, f"当前场景: {menu_state['scene']}")
        base.set_label_text(
            readout,
            f"菜单方案={mode_name()}\n"
            f"位置=({menu_state['x']}, {menu_state['y']})  尺寸={menu_state['w']} x {menu_state['h']}\n"
            f"消息子项={menu_state['message_text']}\n"
            f"最近回调: menu_id={menu_state['last_menu_id']}  item_id={menu_state['last_item_id']}",
        )
        base.set_label_text(callback_label, str(menu_state["last_event"]))
        if note is not None:
            base.set_label_text(state_text, note)
            if push_status:
                base.set_status(note)

    def rebuild_menu(mode: str, note: str) -> None:
        old_bar = menu_state.get("bar")
        if old_bar:
            DLL.DestroyMenuBar(old_bar)

        bar = DLL.CreateMenuBar(menu_state["host"])
        menu_state["bar"] = bar
        menu_state["mode"] = mode
        DLL.SetMenuBarPlacement(bar, int(menu_state["x"]), int(menu_state["y"]), int(menu_state["w"]), int(menu_state["h"]))

        if mode == "default":
            add_item(bar, "📁 文件", MENU_FILE)
            add_sub(bar, MENU_FILE, "💬 对话框", MENU_DIALOG)
            add_sub(bar, MENU_DIALOG, str(menu_state["message_text"]), MENU_MSG)
            add_sub(bar, MENU_DIALOG, "❓ 显示确认框", MENU_CONFIRM)
            add_sub(bar, MENU_FILE, "🧭 场景文案", MENU_SCENE)
            add_sub(bar, MENU_SCENE, "🟡 运行中", MENU_SCENE_RUNNING)
            add_sub(bar, MENU_SCENE, "🟢 已完成", MENU_SCENE_DONE)
            add_item(bar, "📐 布局", MENU_LAYOUT)
            add_sub(bar, MENU_LAYOUT, "⬅ 靠左 360", MENU_LAYOUT_LEFT)
            add_sub(bar, MENU_LAYOUT, "↔ 标准 560", MENU_LAYOUT_STD)
            add_sub(bar, MENU_LAYOUT, "⟷ 满宽 900", MENU_LAYOUT_WIDE)
            add_sub(bar, MENU_LAYOUT, "⬇ 下移 24", MENU_LAYOUT_DOWN)
            add_sub(bar, MENU_LAYOUT, "⬆ 顶部归位", MENU_LAYOUT_RESET)
            add_item(bar, "🛠️ 工具", MENU_TOOLS)
        else:
            add_item(bar, "⚡ 快捷操作", MENU_FILE)
            add_sub(bar, MENU_FILE, "💬 对话框", MENU_DIALOG)
            add_sub(bar, MENU_DIALOG, str(menu_state["message_text"]), MENU_MSG)
            add_sub(bar, MENU_DIALOG, "❓ 显示确认框", MENU_CONFIRM)
            add_sub(bar, MENU_FILE, "📐 布局", MENU_LAYOUT)
            add_sub(bar, MENU_LAYOUT, "⬅ 靠左 360", MENU_LAYOUT_LEFT)
            add_sub(bar, MENU_LAYOUT, "↔ 标准 560", MENU_LAYOUT_STD)
            add_sub(bar, MENU_LAYOUT, "⟷ 满宽 900", MENU_LAYOUT_WIDE)
            add_sub(bar, MENU_LAYOUT, "⬇ 下移 24", MENU_LAYOUT_DOWN)
            add_sub(bar, MENU_LAYOUT, "⬆ 顶部归位", MENU_LAYOUT_RESET)
            add_item(bar, "🛠️ 工具", MENU_TOOLS)

        add_sub(bar, MENU_TOOLS, "✏️ 更新子项文案", MENU_TOOL_RENAME)
        add_sub(bar, MENU_TOOLS, "↺ 恢复子项文案", MENU_TOOL_RESTORE)
        add_sub(bar, MENU_TOOLS, "🔁 切换菜单方案", MENU_TOOL_TOGGLE_MODE)
        add_sub(bar, MENU_TOOLS, "📡 刷新状态", MENU_TOOL_REFRESH)

        DLL.SetMenuBarCallback(bar, menu_cb)
        menu_state["last_event"] = f"已重建 {mode_name()}。"
        refresh(note, push_status=True)

    def apply_placement(x: int, y: int, w: int, h: int, note: str) -> None:
        menu_state["x"] = x
        menu_state["y"] = y
        menu_state["w"] = w
        menu_state["h"] = h
        bar = menu_state.get("bar")
        if bar:
            DLL.SetMenuBarPlacement(bar, x, y, w, h)
        refresh(note, push_status=True)

    def update_message_text(text: str, note: str) -> None:
        bar = menu_state.get("bar")
        if not bar:
            refresh("MenuBar 尚未创建", push_status=True)
            return
        text_p, text_n, _ = s(text)
        ok = bool(DLL.MenuBarUpdateSubItemText(bar, MENU_DIALOG, MENU_MSG, text_p, text_n))
        if ok:
            menu_state["message_text"] = text
            menu_state["last_event"] = f"MenuBar 子项文案已更新为 {text}"
            refresh(note, push_status=True)
        else:
            refresh("MenuBar 子项文案更新失败", push_status=True)

    def handle_menu(menu_id: int, item_id: int) -> None:
        menu_state["last_menu_id"] = menu_id
        menu_state["last_item_id"] = item_id

        if item_id == MENU_DIALOG:
            menu_state["last_event"] = "文件 -> 对话框：继续选择消息框或确认框。"
            refresh("MenuBar 已展开对话框子菜单", push_status=True)
        elif item_id == MENU_SCENE:
            menu_state["last_event"] = "文件 -> 场景文案：继续选择运行中或已完成。"
            refresh("MenuBar 已展开场景文案子菜单", push_status=True)
        elif item_id == MENU_MSG:
            menu_state["scene"] = "消息框已通过 MenuBar 打开。"
            menu_state["last_event"] = f"触发菜单项 -> {menu_state['message_text']}"
            base.show_msg("MenuBar 消息框", "这是从 MenuBar 子菜单打开的 MessageBox。", "📁")
            refresh("MenuBar 已触发消息框", push_status=True)
        elif item_id == MENU_CONFIRM:
            menu_state["scene"] = "确认框已通过 MenuBar 打开。"
            menu_state["last_event"] = "触发菜单项 -> ❓ 显示确认框"
            base.show_confirm("MenuBar 确认框", "这是从 MenuBar 子菜单打开的 ConfirmBox。", "📁")
            refresh("MenuBar 已触发确认框", push_status=True)
        elif item_id == MENU_SCENE_RUNNING:
            menu_state["scene"] = "运行中 - 菜单栏已写回场景文案。"
            menu_state["last_event"] = "触发菜单项 -> 🟡 运行中"
            refresh("MenuBar 已切换场景为运行中", push_status=True)
        elif item_id == MENU_SCENE_DONE:
            menu_state["scene"] = "已完成 - 菜单栏已写回场景文案。"
            menu_state["last_event"] = "触发菜单项 -> 🟢 已完成"
            refresh("MenuBar 已切换场景为已完成", push_status=True)
        elif item_id == MENU_LAYOUT_LEFT:
            menu_state["last_event"] = "触发菜单项 -> ⬅ 靠左 360"
            apply_placement(16, 46, 360, 34, "MenuBar 已切到靠左 360")
        elif item_id == MENU_LAYOUT_STD:
            menu_state["last_event"] = "触发菜单项 -> ↔ 标准 560"
            apply_placement(16, 46, 560, 34, "MenuBar 已切到标准宽度 560")
        elif item_id == MENU_LAYOUT_WIDE:
            menu_state["last_event"] = "触发菜单项 -> ⟷ 满宽 900"
            apply_placement(16, 46, 900, 34, "MenuBar 已切到满宽 900")
        elif item_id == MENU_LAYOUT_DOWN:
            menu_state["last_event"] = "触发菜单项 -> ⬇ 下移 24"
            apply_placement(int(menu_state["x"]), 74, int(menu_state["w"]), int(menu_state["h"]), "MenuBar 已下移 28 像素")
        elif item_id == MENU_LAYOUT_RESET:
            menu_state["last_event"] = "触发菜单项 -> ⬆ 顶部归位"
            apply_placement(16, 46, 720 if menu_state["mode"] == "default" else 620, 34, "MenuBar 已恢复顶部默认位置")
        elif item_id == MENU_TOOL_RENAME:
            update_message_text("📨 打开消息框", "MenuBar 子项文案已改为“打开消息框”")
        elif item_id == MENU_TOOL_RESTORE:
            update_message_text("💬 显示消息框", "MenuBar 子项文案已恢复")
        elif item_id == MENU_TOOL_TOGGLE_MODE:
            target_mode = "compact" if menu_state["mode"] == "default" else "default"
            rebuild_menu(target_mode, f"MenuBar 已切换到{mode_name()}")
        elif item_id == MENU_TOOL_REFRESH:
            menu_state["last_event"] = "触发菜单项 -> 📡 刷新状态"
            refresh("MenuBar 状态已刷新", push_status=True)
        else:
            menu_state["last_event"] = f"MenuBar 收到 item_id={item_id}"
            refresh("MenuBar 已收到菜单回调", push_status=True)

    menu_cb = DLL._MenuCB(handle_menu)
    KEEP.append(menu_cb)

    base.button(side_panel, "⬅", "靠左 360", 16, 344, 120, 30, 0xFF409EFF, lambda: apply_placement(16, 46, 360, 34, "MenuBar 已切到靠左 360"))
    base.button(side_panel, "↔", "标准 560", 152, 344, 120, 30, 0xFF67C23A, lambda: apply_placement(16, 46, 560, 34, "MenuBar 已切到标准宽度 560"))
    base.button(side_panel, "⟷", "满宽 900", 288, 344, 120, 30, 0xFFE6A23C, lambda: apply_placement(16, 46, 900, 34, "MenuBar 已切到满宽 900"))
    base.button(side_panel, "⬇", "下移 28", 16, 379, 120, 30, 0xFF8E44AD, lambda: apply_placement(int(menu_state["x"]), 74, int(menu_state["w"]), int(menu_state["h"]), "MenuBar 已下移 28 像素"))
    base.button(side_panel, "⬆", "顶部归位", 152, 379, 120, 30, 0xFF909399, lambda: apply_placement(16, 46, 720 if menu_state["mode"] == "default" else 620, 34, "MenuBar 已恢复顶部默认位置"))
    base.button(side_panel, "✏️", "更新文案", 288, 379, 120, 30, 0xFF409EFF, lambda: update_message_text("📨 打开消息框", "MenuBar 子项文案已改为“打开消息框”"))
    base.button(side_panel, "↺", "恢复文案", 16, 414, 120, 30, 0xFF67C23A, lambda: update_message_text("💬 显示消息框", "MenuBar 子项文案已恢复"))
    base.button(side_panel, "📁", "默认菜单", 152, 414, 120, 30, 0xFFE6A23C, lambda: rebuild_menu("default", "MenuBar 已重建为默认三级菜单"))
    base.button(side_panel, "📚", "紧凑菜单", 288, 414, 120, 30, 0xFF8E44AD, lambda: rebuild_menu("compact", "MenuBar 已重建为紧凑菜单"))

    register_theme_label(base.label(api_panel, "1. CreateMenuBar / DestroyMenuBar：创建菜单栏，并通过“默认菜单 / 紧凑菜单”实际演示销毁后重建。", 16, 14, 1220, 22, fg=text_color, bg=card_bg), "text", "card")
    register_theme_label(base.label(api_panel, "2. MenuBarAddItem / MenuBarAddSubItem：页面内保留一级菜单、二级菜单和三级子菜单。", 16, 40, 1040, 22, fg=text_color, bg=card_bg), "text", "card")
    register_theme_label(base.label(api_panel, "3. SetMenuBarPlacement：右侧按钮和“布局”菜单都会直接改写菜单栏位置与宽度。", 16, 66, 1060, 22, fg=text_color, bg=card_bg), "text", "card")
    register_theme_label(base.label(api_panel, "4. SetMenuBarCallback：所有菜单项都会把 menu_id / item_id、最近动作和场景文案写回到页面。", 16, 92, 1160, 22, fg=text_color, bg=card_bg), "text", "card")
    register_theme_label(base.label(api_panel, "5. MenuBarUpdateSubItemText：可直接把“显示消息框”改成“打开消息框”，再恢复默认文案。", 16, 118, 1200, 22, fg=text_color, bg=card_bg), "text", "card")

    rebuild_menu("default", "MenuBar 页已重构：只保留菜单栏能力，不再混入树形框和评分演示。")

def build_page_menubar_v3(page: HWND) -> None:
    palette = page_palette()
    page_bg = palette["page_bg"]
    card_bg = palette["card_bg"]
    text_color = palette["text"]
    muted_color = palette["muted"]
    accent_color = palette["accent"]

    base.groupbox(page, "MenuBar 舞台", 16, 16, 980, 520)
    base.groupbox(page, "状态 / 快捷操作", 1012, 16, 452, 520)
    base.groupbox(page, "最近回调 / 接口覆盖", 16, 558, 1448, 200)

    register_theme_label(
        base.label(
            page,
            "这一页只保留 MenuBar 本体：左侧是真实菜单舞台，右侧只放状态和快捷操作，不再混入别的组件演示。",
            40,
            54,
            920,
            24,
            fg=muted_color,
            bg=page_bg,
            wrap=True,
        ),
        "muted",
        "page",
    )

    stage_panel = DLL.CreatePanel(page, 40, 92, 932, 382, THEME_SURFACE)
    register_theme_label(
        base.label(
            stage_panel,
            "直接点击上方菜单，验证三级子菜单、布局调整、文案更新和回调写回。",
            24,
            72,
            884,
            20,
            fg=muted_color,
            bg=card_bg,
        ),
        "muted",
        "card",
    )
    scene_label = register_theme_label(
        base.label(
            stage_panel,
            "等待菜单操作",
            24,
            126,
            884,
            34,
            fg=accent_color,
            bg=card_bg,
            size=24,
            bold=True,
        ),
        "accent",
        "card",
    )
    detail_label = register_theme_label(
        base.label(
            stage_panel,
            "点击“文件 / 布局 / 工具”菜单项，右侧状态和底部日志会立即同步。",
            24,
            172,
            884,
            44,
            fg=muted_color,
            bg=card_bg,
            size=14,
            wrap=True,
        ),
        "muted",
        "card",
    )
    register_theme_label(
        base.label(
            stage_panel,
            "右侧按钮只保留常用快捷入口，其余动作直接在 MenuBar 自身菜单里测试。",
            24,
            330,
            884,
            20,
            fg=muted_color,
            bg=card_bg,
        ),
        "muted",
        "card",
    )

    register_theme_label(base.label(page, "当前状态", 1040, 54, 220, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    readout = register_theme_label(base.label(page, "等待读取 MenuBar 状态。", 1040, 88, 392, 96, fg=text_color, bg=page_bg, wrap=True), "text", "page")
    state_text = register_theme_label(base.label(page, "MenuBar 页状态将在这里更新。", 1040, 194, 392, 22, fg=accent_color, bg=page_bg), "accent", "page")
    register_theme_label(
        base.label(
            page,
            "右侧只保留快捷入口；下移、归位、刷新等动作也能从菜单本身触发。",
            1040,
            226,
            392,
            48,
            fg=muted_color,
            bg=page_bg,
            wrap=True,
        ),
        "muted",
        "page",
    )
    register_theme_label(base.label(page, "快捷操作", 1040, 292, 220, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")

    register_theme_label(base.label(page, "最近回调", 40, 594, 220, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    event_feed = register_theme_label(base.label(page, "等待触发 MenuBar 回调。", 40, 628, 900, 96, fg=text_color, bg=page_bg, wrap=True), "text", "page")
    register_theme_label(base.label(page, "接口覆盖", 980, 594, 220, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    register_theme_label(base.label(page, "1. CreateMenuBar / DestroyMenuBar：重建默认菜单与紧凑菜单。", 980, 628, 430, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "2. MenuBarAddItem / MenuBarAddSubItem / SetMenuBarCallback：验证一级、二级、三级菜单及回调写回。", 980, 662, 430, 24, fg=text_color, bg=page_bg, wrap=True), "text", "page")
    register_theme_label(base.label(page, "3. SetMenuBarPlacement / MenuBarUpdateSubItemText：直接修改菜单宽度、位置和子项文案。", 980, 696, 430, 24, fg=text_color, bg=page_bg, wrap=True), "text", "page")

    MENU_FILE = 5000
    MENU_DIALOG = 5100
    MENU_MSG = 5110
    MENU_CONFIRM = 5111
    MENU_SCENE = 5200
    MENU_SCENE_RUNNING = 5210
    MENU_SCENE_DONE = 5211
    MENU_LAYOUT = 6000
    MENU_LAYOUT_LEFT = 6110
    MENU_LAYOUT_STD = 6111
    MENU_LAYOUT_WIDE = 6112
    MENU_LAYOUT_DOWN = 6113
    MENU_LAYOUT_RESET = 6114
    MENU_TOOLS = 7000
    MENU_TOOL_RENAME = 7100
    MENU_TOOL_RESTORE = 7101
    MENU_TOOL_TOGGLE_MODE = 7102
    MENU_TOOL_REFRESH = 7103

    event_lines: list[str] = []
    menu_state: dict[str, object] = {
        "host": stage_panel,
        "bar": None,
        "mode": "default",
        "x": 24,
        "y": 24,
        "w": 760,
        "h": 34,
        "message_text": "显示消息框",
        "scene": "等待菜单操作",
        "detail": "点击“文件 / 布局 / 工具”菜单项，右侧状态和底部日志会立即同步。",
        "last_menu_id": 0,
        "last_item_id": 0,
        "last_event": "尚未触发菜单回调。",
    }

    def mode_name() -> str:
        return "默认三级菜单" if menu_state["mode"] == "default" else "紧凑菜单"

    def set_scene(title: str, detail: str) -> None:
        menu_state["scene"] = title
        menu_state["detail"] = detail

    def push_event(text: str) -> None:
        event_lines.insert(0, text)
        del event_lines[6:]
        base.set_label_text(event_feed, "\n".join(event_lines))

    def add_item(bar: HWND, text: str, item_id: int) -> None:
        text_p, text_n, _ = s(text)
        DLL.MenuBarAddItem(bar, text_p, text_n, item_id)

    def add_sub(bar: HWND, parent_id: int, text: str, item_id: int) -> None:
        text_p, text_n, _ = s(text)
        DLL.MenuBarAddSubItem(bar, parent_id, text_p, text_n, item_id)

    def refresh(note: str | None = None, *, push_status: bool = False) -> None:
        base.set_label_text(scene_label, str(menu_state["scene"]))
        base.set_label_text(detail_label, str(menu_state["detail"]))
        base.set_label_text(
            readout,
            f"方案：{mode_name()}\n"
            f"位置：({menu_state['x']}, {menu_state['y']})  尺寸：{menu_state['w']} x {menu_state['h']}\n"
            f"消息子项：{menu_state['message_text']}\n"
            f"最近回调：menu_id={menu_state['last_menu_id']}  item_id={menu_state['last_item_id']}",
        )
        if note is not None:
            base.set_label_text(state_text, note)
            if push_status:
                base.set_status(note)

    def rebuild_menu(mode: str, note: str) -> None:
        old_bar = menu_state.get("bar")
        if old_bar:
            DLL.DestroyMenuBar(old_bar)

        bar = DLL.CreateMenuBar(menu_state["host"])
        menu_state["bar"] = bar
        menu_state["mode"] = mode
        DLL.SetMenuBarPlacement(bar, int(menu_state["x"]), int(menu_state["y"]), int(menu_state["w"]), int(menu_state["h"]))

        if mode == "default":
            add_item(bar, "文件", MENU_FILE)
            add_sub(bar, MENU_FILE, "对话框", MENU_DIALOG)
            add_sub(bar, MENU_DIALOG, str(menu_state["message_text"]), MENU_MSG)
            add_sub(bar, MENU_DIALOG, "显示确认框", MENU_CONFIRM)
            add_sub(bar, MENU_FILE, "场景文本", MENU_SCENE)
            add_sub(bar, MENU_SCENE, "运行中", MENU_SCENE_RUNNING)
            add_sub(bar, MENU_SCENE, "已完成", MENU_SCENE_DONE)
            add_item(bar, "布局", MENU_LAYOUT)
            add_sub(bar, MENU_LAYOUT, "靠左 360", MENU_LAYOUT_LEFT)
            add_sub(bar, MENU_LAYOUT, "标准 560", MENU_LAYOUT_STD)
            add_sub(bar, MENU_LAYOUT, "满宽 900", MENU_LAYOUT_WIDE)
            add_sub(bar, MENU_LAYOUT, "下移 28", MENU_LAYOUT_DOWN)
            add_sub(bar, MENU_LAYOUT, "顶部归位", MENU_LAYOUT_RESET)
            add_item(bar, "工具", MENU_TOOLS)
        else:
            add_item(bar, "快捷操作", MENU_FILE)
            add_sub(bar, MENU_FILE, "对话框", MENU_DIALOG)
            add_sub(bar, MENU_DIALOG, str(menu_state["message_text"]), MENU_MSG)
            add_sub(bar, MENU_DIALOG, "显示确认框", MENU_CONFIRM)
            add_sub(bar, MENU_FILE, "布局", MENU_LAYOUT)
            add_sub(bar, MENU_LAYOUT, "靠左 360", MENU_LAYOUT_LEFT)
            add_sub(bar, MENU_LAYOUT, "标准 560", MENU_LAYOUT_STD)
            add_sub(bar, MENU_LAYOUT, "满宽 900", MENU_LAYOUT_WIDE)
            add_sub(bar, MENU_LAYOUT, "下移 28", MENU_LAYOUT_DOWN)
            add_sub(bar, MENU_LAYOUT, "顶部归位", MENU_LAYOUT_RESET)
            add_item(bar, "工具", MENU_TOOLS)

        add_sub(bar, MENU_TOOLS, "改子项文案", MENU_TOOL_RENAME)
        add_sub(bar, MENU_TOOLS, "恢复默认文案", MENU_TOOL_RESTORE)
        add_sub(bar, MENU_TOOLS, "切换菜单方案", MENU_TOOL_TOGGLE_MODE)
        add_sub(bar, MENU_TOOLS, "刷新状态", MENU_TOOL_REFRESH)

        DLL.SetMenuBarCallback(bar, menu_cb)
        menu_state["last_event"] = note
        set_scene(
            "默认三级菜单已就绪" if mode == "default" else "紧凑菜单已就绪",
            "继续点击菜单项，验证回调写回、位置调整和子项文案更新。",
        )
        refresh(note, push_status=True)
        push_event(str(menu_state["last_event"]))

    def apply_placement(x: int, y: int, w: int, h: int, note: str) -> None:
        menu_state["x"] = x
        menu_state["y"] = y
        menu_state["w"] = w
        menu_state["h"] = h
        bar = menu_state.get("bar")
        if bar:
            DLL.SetMenuBarPlacement(bar, x, y, w, h)
        menu_state["last_event"] = note
        set_scene("菜单布局已调整", f"当前菜单栏位置已更新为 ({x}, {y})，宽度 {w}px。")
        refresh(note, push_status=True)
        push_event(str(menu_state["last_event"]))

    def update_message_text(text: str, note: str) -> None:
        bar = menu_state.get("bar")
        if not bar:
            menu_state["last_event"] = "MenuBar 尚未创建"
            refresh("MenuBar 尚未创建", push_status=True)
            push_event(str(menu_state["last_event"]))
            return
        text_p, text_n, _ = s(text)
        ok = bool(DLL.MenuBarUpdateSubItemText(bar, MENU_DIALOG, MENU_MSG, text_p, text_n))
        if ok:
            menu_state["message_text"] = text
            menu_state["last_event"] = note
            set_scene("子项文案已更新", f"“文件 -> 对话框 -> {text}” 已立即同步到菜单。")
            refresh(note, push_status=True)
            push_event(str(menu_state["last_event"]))
        else:
            menu_state["last_event"] = "MenuBar 子项文案更新失败"
            refresh("MenuBar 子项文案更新失败", push_status=True)
            push_event(str(menu_state["last_event"]))

    def handle_menu(menu_id: int, item_id: int) -> None:
        menu_state["last_menu_id"] = menu_id
        menu_state["last_item_id"] = item_id

        if item_id == MENU_DIALOG:
            menu_state["last_event"] = "已展开“文件 -> 对话框”子菜单"
            set_scene("对话框菜单已展开", "继续点击“显示消息框 / 显示确认框”，验证三级子菜单回调。")
            refresh("MenuBar 已展开对话框子菜单", push_status=True)
            push_event(f"{menu_state['last_event']}  [menu_id={menu_id}, item_id={item_id}]")
        elif item_id == MENU_SCENE:
            menu_state["last_event"] = "已展开“文件 -> 场景文本”子菜单"
            set_scene("场景菜单已展开", "继续点击“运行中 / 已完成”，验证主文案立即切换。")
            refresh("MenuBar 已展开场景文本子菜单", push_status=True)
            push_event(f"{menu_state['last_event']}  [menu_id={menu_id}, item_id={item_id}]")
        elif item_id == MENU_MSG:
            set_scene("消息框已通过菜单打开", "MessageBox 已弹出，回调和状态写回已经生效。")
            menu_state["last_event"] = f"触发子项 -> {menu_state['message_text']}"
            base.show_msg("MenuBar 消息框", "这是从 MenuBar 子菜单打开的 MessageBox。", "Menu")
            refresh("MenuBar 已触发消息框", push_status=True)
            push_event(f"{menu_state['last_event']}  [menu_id={menu_id}, item_id={item_id}]")
        elif item_id == MENU_CONFIRM:
            set_scene("确认框已通过菜单打开", "ConfirmBox 已弹出，当前菜单回调也已同步写回。")
            menu_state["last_event"] = "触发子项 -> 显示确认框"
            base.show_confirm("MenuBar 确认框", "这是从 MenuBar 子菜单打开的 ConfirmBox。", "Menu")
            refresh("MenuBar 已触发确认框", push_status=True)
            push_event(f"{menu_state['last_event']}  [menu_id={menu_id}, item_id={item_id}]")
        elif item_id == MENU_SCENE_RUNNING:
            set_scene("运行中", "场景文案已通过 MenuBar 立即写回到舞台。")
            menu_state["last_event"] = "场景切换 -> 运行中"
            refresh("MenuBar 已切换场景为运行中", push_status=True)
            push_event(f"{menu_state['last_event']}  [menu_id={menu_id}, item_id={item_id}]")
        elif item_id == MENU_SCENE_DONE:
            set_scene("已完成", "场景文案已通过 MenuBar 立即切换为完成态。")
            menu_state["last_event"] = "场景切换 -> 已完成"
            refresh("MenuBar 已切换场景为已完成", push_status=True)
            push_event(f"{menu_state['last_event']}  [menu_id={menu_id}, item_id={item_id}]")
        elif item_id == MENU_LAYOUT_LEFT:
            apply_placement(24, 24, 360, 34, "MenuBar 已切到靠左 360")
        elif item_id == MENU_LAYOUT_STD:
            apply_placement(24, 24, 560, 34, "MenuBar 已切到标准宽度 560")
        elif item_id == MENU_LAYOUT_WIDE:
            apply_placement(24, 24, 900, 34, "MenuBar 已切到满宽 900")
        elif item_id == MENU_LAYOUT_DOWN:
            apply_placement(int(menu_state["x"]), 52, int(menu_state["w"]), int(menu_state["h"]), "MenuBar 已下移 28 像素")
        elif item_id == MENU_LAYOUT_RESET:
            apply_placement(24, 24, 760 if menu_state["mode"] == "default" else 620, 34, "MenuBar 已恢复默认位置")
        elif item_id == MENU_TOOL_RENAME:
            update_message_text("打开消息框", "MenuBar 子项文案已改为“打开消息框”")
        elif item_id == MENU_TOOL_RESTORE:
            update_message_text("显示消息框", "MenuBar 子项文案已恢复")
        elif item_id == MENU_TOOL_TOGGLE_MODE:
            target_mode = "compact" if menu_state["mode"] == "default" else "default"
            rebuild_menu(target_mode, f"MenuBar 已切换到{'紧凑菜单' if target_mode == 'compact' else '默认三级菜单'}")
        elif item_id == MENU_TOOL_REFRESH:
            set_scene("状态已刷新", "当前菜单状态、位置和最近回调已重新写回右侧。")
            menu_state["last_event"] = "已刷新 MenuBar 状态"
            refresh("MenuBar 状态已刷新", push_status=True)
            push_event(f"{menu_state['last_event']}  [menu_id={menu_id}, item_id={item_id}]")
        else:
            set_scene("收到菜单回调", f"menu_id={menu_id}，item_id={item_id} 已写回到底部日志。")
            menu_state["last_event"] = f"MenuBar 收到 item_id={item_id}"
            refresh("MenuBar 已收到菜单回调", push_status=True)
            push_event(f"{menu_state['last_event']}  [menu_id={menu_id}, item_id={item_id}]")

    menu_cb = DLL._MenuCB(handle_menu)
    KEEP.append(menu_cb)

    base.button(page, "<", "靠左 360", 1040, 330, 120, 34, 0xFF409EFF, lambda: apply_placement(24, 24, 360, 34, "MenuBar 已切到靠左 360"))
    base.button(page, "=", "标准 560", 1172, 330, 120, 34, 0xFF67C23A, lambda: apply_placement(24, 24, 560, 34, "MenuBar 已切到标准宽度 560"))
    base.button(page, "[]", "满宽 900", 1304, 330, 120, 34, 0xFFE6A23C, lambda: apply_placement(24, 24, 900, 34, "MenuBar 已切到满宽 900"))
    base.button(page, "v", "下移 28", 1040, 374, 120, 34, 0xFF8E44AD, lambda: apply_placement(int(menu_state["x"]), 52, int(menu_state["w"]), int(menu_state["h"]), "MenuBar 已下移 28 像素"))
    base.button(page, "R", "恢复位置", 1172, 374, 120, 34, 0xFF909399, lambda: apply_placement(24, 24, 760 if menu_state["mode"] == "default" else 620, 34, "MenuBar 已恢复默认位置"))
    base.button(page, "T", "改子项文案", 1304, 374, 120, 34, 0xFF409EFF, lambda: update_message_text("打开消息框", "MenuBar 子项文案已改为“打开消息框”"))
    base.button(page, "<-", "恢复文案", 1040, 418, 120, 34, 0xFF67C23A, lambda: update_message_text("显示消息框", "MenuBar 子项文案已恢复"))
    base.button(page, "A", "默认菜单", 1172, 418, 120, 34, 0xFFE6A23C, lambda: rebuild_menu("default", "MenuBar 已重建为默认三级菜单"))
    base.button(page, "B", "紧凑菜单", 1304, 418, 120, 34, 0xFF8E44AD, lambda: rebuild_menu("compact", "MenuBar 已重建为紧凑菜单"))

    rebuild_menu("default", "MenuBar 页面已精简重排，只保留菜单栏本身和相关操作。")


def build_page_popupmenu_enhanced(page: HWND) -> None:
    palette = page_palette()
    page_bg = palette["page_bg"]
    card_bg = palette["card_bg"]
    text_color = palette["text"]
    muted_color = palette["muted"]
    accent_color = palette["accent"]

    base.groupbox(page, "PopupMenu 舞台", 16, 16, 980, 520)
    base.groupbox(page, "状态 / 绑定", 1012, 16, 452, 520)
    base.groupbox(page, "最近回调 / 接口覆盖", 16, 558, 1448, 200)

    register_theme_label(
        base.label(
            page,
            "这一页只保留 PopupMenu 本体：左侧测试控件右键菜单，右侧测试按钮专属菜单和状态写回。",
            40,
            54,
            920,
            24,
            fg=muted_color,
            bg=page_bg,
            wrap=True,
        ),
        "muted",
        "page",
    )

    stage_panel = DLL.CreatePanel(page, 40, 92, 932, 382, THEME_SURFACE)
    register_theme_label(base.label(stage_panel, "在下方区域点击鼠标右键，可直接打开控件绑定 PopupMenu。", 24, 24, 884, 20, fg=muted_color, bg=card_bg), "muted", "card")
    scene_label = register_theme_label(base.label(stage_panel, "等待右键操作", 24, 58, 884, 34, fg=accent_color, bg=card_bg, size=24, bold=True), "accent", "card")
    detail_label = register_theme_label(
        base.label(
            stage_panel,
            "主菜单包含二级子菜单、状态写回和绑定读取；右侧蓝色按钮则绑定了独立的按钮菜单。",
            24,
            98,
            884,
            44,
            fg=muted_color,
            bg=card_bg,
            size=14,
            wrap=True,
        ),
        "muted",
        "card",
    )

    menu_zone = DLL.CreatePanel(stage_panel, 24, 162, 620, 154, THEME_BG)
    base.label(menu_zone, "在这里点击鼠标右键", 24, 24, 320, 28, fg=THEME_TEXT, bg=THEME_BG, size=20, bold=True)
    base.label(menu_zone, "主菜单包含：查看说明、写回状态、读取当前绑定。", 24, 72, 540, 22, fg=THEME_MUTED, bg=THEME_BG)
    base.label(menu_zone, "其中“查看说明”和“写回状态”都带二级子菜单。", 24, 104, 540, 22, fg=THEME_MUTED, bg=THEME_BG)

    register_theme_label(base.label(stage_panel, "这块右键区只负责控件绑定菜单，按钮菜单在右侧单独测试，不混在一起。", 24, 336, 884, 20, fg=muted_color, bg=card_bg), "muted", "card")

    register_theme_label(base.label(page, "当前状态", 1040, 54, 220, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    readout = register_theme_label(base.label(page, "等待读取 PopupMenu 状态。", 1040, 88, 392, 96, fg=text_color, bg=page_bg, wrap=True), "text", "page")
    register_theme_label(base.label(page, "最近回调", 1040, 210, 220, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    callback_label = register_theme_label(base.label(page, "尚未触发 PopupMenu 回调。", 1040, 244, 392, 72, fg=muted_color, bg=page_bg, wrap=True), "muted", "page")
    state_text = register_theme_label(base.label(page, "PopupMenu 页状态将在这里更新。", 1040, 326, 392, 22, fg=accent_color, bg=page_bg), "accent", "page")
    register_theme_label(base.label(page, "蓝色按钮请直接点右键；左侧白色区域则用于测试控件绑定菜单。", 1040, 356, 392, 40, fg=muted_color, bg=page_bg, wrap=True), "muted", "page")

    register_theme_label(base.label(page, "最近回调", 40, 594, 220, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    event_feed = register_theme_label(base.label(page, "等待触发 PopupMenu 回调。", 40, 628, 900, 96, fg=text_color, bg=page_bg, wrap=True), "text", "page")
    register_theme_label(base.label(page, "接口覆盖", 980, 594, 220, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    register_theme_label(base.label(page, "1. CreateEmojiPopupMenu / PopupMenuAddItem / PopupMenuAddSubItem：创建主菜单、按钮菜单和二级子菜单。", 980, 628, 430, 24, fg=text_color, bg=page_bg, wrap=True), "text", "page")
    register_theme_label(base.label(page, "2. BindControlMenu / BindButtonMenu：分别绑定左侧右键区和右侧按钮。", 980, 662, 430, 24, fg=text_color, bg=page_bg, wrap=True), "text", "page")
    register_theme_label(base.label(page, "3. SetPopupMenuCallback：所有菜单项都会把 menu_id / item_id 和最近动作写回页面。", 980, 696, 430, 24, fg=text_color, bg=page_bg, wrap=True), "text", "page")

    POP_INFO = 5100
    POP_INFO_MSG = 5101
    POP_INFO_CONFIRM = 5102
    POP_STATE = 5110
    POP_STATE_ACTIVE = 5111
    POP_STATE_RESET = 5112
    POP_BINDINGS = 5121
    BTN_MENU_HIT = 5201
    BTN_MENU_RESET = 5202

    event_lines: list[str] = []
    popup_state: dict[str, object] = {
        "scene": "等待右键操作",
        "detail": "在左侧区域点右键，或对右侧蓝色按钮点右键。",
        "last_menu_id": 0,
        "last_item_id": 0,
        "last_event": "尚未触发 PopupMenu 回调。",
    }

    def push_event(text: str) -> None:
        event_lines.insert(0, text)
        del event_lines[6:]
        base.set_label_text(event_feed, "\n".join(event_lines))

    def refresh(note: str | None = None, *, push_status: bool = False) -> None:
        base.set_label_text(scene_label, str(popup_state["scene"]))
        base.set_label_text(detail_label, str(popup_state["detail"]))
        base.set_label_text(
            readout,
            f"主菜单绑定：左侧右键区\n"
            f"按钮菜单绑定：蓝色按钮\n"
            f"最近回调：menu_id={popup_state['last_menu_id']}  item_id={popup_state['last_item_id']}\n"
            f"当前场景：{popup_state['scene']}",
        )
        base.set_label_text(callback_label, str(popup_state["last_event"]))
        if note is not None:
            base.set_label_text(state_text, note)
            if push_status:
                base.set_status(note)

    def set_scene(scene: str, detail: str, note: str, *, push_status: bool = True, log_text: str | None = None) -> None:
        popup_state["scene"] = scene
        popup_state["detail"] = detail
        refresh(note, push_status=push_status)
        if log_text:
            popup_state["last_event"] = log_text
            base.set_label_text(callback_label, str(popup_state["last_event"]))
            push_event(str(log_text))

    def restore_default(note: str = "PopupMenu 已恢复默认状态", *, push_status: bool = True) -> None:
        popup_state["scene"] = "等待右键操作"
        popup_state["detail"] = "在左侧区域点右键，或对右侧蓝色按钮点右键。"
        popup_state["last_event"] = "页面状态已恢复默认。"
        refresh(note, push_status=push_status)
        push_event(str(popup_state["last_event"]))

    def show_binding_summary() -> None:
        popup_state["last_event"] = "已读取当前 PopupMenu 绑定。"
        popup_state["scene"] = "当前绑定已读取"
        popup_state["detail"] = "主菜单绑定=左侧右键区；按钮菜单绑定=右侧蓝色按钮。"
        refresh("PopupMenu 已读取当前绑定", push_status=True)
        push_event(str(popup_state["last_event"]))

    menu_btn = base.button(page, "⋯", "按钮右键菜单", 1040, 414, 180, 38, 0xFF409EFF, lambda: set_scene("等待按钮右键", "请直接对这个蓝色按钮点右键，打开按钮专属 PopupMenu。", "蓝色按钮已点击，请继续点右键。", log_text="按钮提示：请对蓝色按钮点右键。"))
    base.button(page, "i", "读取绑定", 1244, 414, 180, 38, 0xFF67C23A, show_binding_summary)
    base.button(page, "↺", "恢复默认", 1040, 462, 180, 38, 0xFF8E44AD, restore_default)
    base.button(page, "?", "操作提示", 1244, 462, 180, 38, 0xFF909399, lambda: set_scene("等待右键操作", "在左侧区域点右键，或对右侧蓝色按钮点右键。", "请直接用右键触发 PopupMenu。", log_text="操作提示：左侧区域和蓝色按钮都支持右键菜单。"))

    popup_menu = DLL.CreateEmojiPopupMenu(page)
    base.menu_add(popup_menu, "查看说明", POP_INFO)
    base.menu_add_sub(popup_menu, POP_INFO, "打开消息框", POP_INFO_MSG)
    base.menu_add_sub(popup_menu, POP_INFO, "打开确认框", POP_INFO_CONFIRM)
    base.menu_add(popup_menu, "写回状态", POP_STATE)
    base.menu_add_sub(popup_menu, POP_STATE, "标记为已触发", POP_STATE_ACTIVE)
    base.menu_add_sub(popup_menu, POP_STATE, "恢复等待态", POP_STATE_RESET)
    base.menu_add(popup_menu, "读取当前绑定", POP_BINDINGS)

    button_menu = DLL.CreateEmojiPopupMenu(page)
    base.menu_add(button_menu, "按钮菜单已触发", BTN_MENU_HIT)
    base.menu_add(button_menu, "恢复默认状态", BTN_MENU_RESET)

    def on_popup_menu(menu_id: int, item_id: int) -> None:
        popup_state["last_menu_id"] = menu_id
        popup_state["last_item_id"] = item_id

        if item_id == POP_INFO_MSG:
            popup_state["last_event"] = "主菜单 -> 查看说明 -> 打开消息框"
            popup_state["scene"] = "右键菜单已打开消息框"
            popup_state["detail"] = "主菜单的二级子菜单和回调写回都已生效。"
            base.show_msg("PopupMenu 消息框", "这是从右键菜单打开的 MessageBox。", "菜单")
            refresh("PopupMenu 已触发消息框", push_status=True)
        elif item_id == POP_INFO_CONFIRM:
            popup_state["last_event"] = "主菜单 -> 查看说明 -> 打开确认框"
            popup_state["scene"] = "右键菜单已打开确认框"
            popup_state["detail"] = "ConfirmBox 已弹出，当前菜单回调也已同步写回。"
            base.show_confirm("PopupMenu 确认框", "这是从右键菜单打开的 ConfirmBox。", "菜单")
            refresh("PopupMenu 已触发确认框", push_status=True)
        elif item_id == POP_STATE_ACTIVE:
            popup_state["last_event"] = "主菜单 -> 写回状态 -> 标记为已触发"
            popup_state["scene"] = "状态已标记为已触发"
            popup_state["detail"] = "这是通过右键菜单直接写回到页面的状态文本。"
            refresh("PopupMenu 已写回“已触发”状态", push_status=True)
        elif item_id == POP_STATE_RESET:
            popup_state["last_event"] = "主菜单 -> 写回状态 -> 恢复等待态"
            popup_state["scene"] = "等待右键操作"
            popup_state["detail"] = "页面状态已通过右键菜单恢复为初始等待态。"
            refresh("PopupMenu 已恢复等待态", push_status=True)
        elif item_id == POP_BINDINGS:
            popup_state["last_event"] = "主菜单 -> 读取当前绑定"
            popup_state["scene"] = "当前绑定已读取"
            popup_state["detail"] = "主菜单绑定=左侧右键区；按钮菜单绑定=右侧蓝色按钮。"
            refresh("PopupMenu 已读取当前绑定", push_status=True)
        elif item_id == BTN_MENU_HIT:
            popup_state["last_event"] = "按钮菜单 -> 按钮菜单已触发"
            popup_state["scene"] = "按钮菜单已触发"
            popup_state["detail"] = "当前命中的是蓝色按钮专属 PopupMenu。"
            refresh("按钮右键菜单回调正常", push_status=True)
        elif item_id == BTN_MENU_RESET:
            restore_default("按钮菜单已恢复默认状态", push_status=True)
            popup_state["last_event"] = "按钮菜单 -> 恢复默认状态"
            base.set_label_text(callback_label, str(popup_state["last_event"]))
            push_event(f"{popup_state['last_event']}  [menu_id={menu_id}, item_id={item_id}]")
            return
        else:
            popup_state["last_event"] = f"PopupMenu 收到 item_id={item_id}"
            popup_state["scene"] = "收到 PopupMenu 回调"
            popup_state["detail"] = f"menu_id={menu_id}，item_id={item_id} 已写回页面。"
            refresh("PopupMenu 已收到回调", push_status=True)

        base.set_label_text(callback_label, str(popup_state["last_event"]))
        push_event(f"{popup_state['last_event']}  [menu_id={menu_id}, item_id={item_id}]")

    menu_cb = DLL._MenuCB(on_popup_menu)
    KEEP.append(menu_cb)
    DLL.SetPopupMenuCallback(popup_menu, menu_cb)
    DLL.SetPopupMenuCallback(button_menu, menu_cb)
    DLL.BindControlMenu(menu_zone, popup_menu)
    DLL.BindButtonMenu(page, int(menu_btn), button_menu)

    restore_default("PopupMenu 页面已重排，只保留控件右键菜单和按钮菜单两类绑定。", push_status=True)


def build_page_datagrid_enhanced_v2(page: HWND) -> None:
    palette = page_palette()
    top_bg = palette["page_bg"]
    card_bg = palette["card_bg"]
    text_color = palette["text"]
    muted_color = palette["muted"]
    accent_color = palette["accent"]

    base.groupbox(page, "🧰 DataGridView 属性读取 / 主操作工具栏", 16, 16, 1448, 192)
    mode_label = register_theme_label(
        base.label(page, "当前模式: 普通表格", 40, 48, 240, 24, fg=accent_color, bg=card_bg, size=13, bold=True),
        "accent",
        "card",
    )
    grid_state = register_theme_label(
        base.label(page, "等待表格状态。", 296, 48, 760, 58, fg=muted_color, bg=card_bg, wrap=True),
        "muted",
        "card",
    )
    export_path_label = register_theme_label(
        base.label(page, "CSV 尚未导出。", 1096, 48, 328, 58, fg=muted_color, bg=card_bg, wrap=True),
        "muted",
        "card",
    )
    register_theme_label(
        base.label(
            page,
            "这一页只保留表格相关能力：普通/虚拟表格、排序、单元格读写、表头读写、对齐切换和 CSV 导出。",
            40,
            116,
            1180,
            18,
            fg=muted_color,
            bg=top_bg,
            wrap=True,
        ),
        "muted",
        "page",
    )
    toolbar_panel = DLL.CreatePanel(page, 40, 146, 1384, 42, THEME_SURFACE)

    base.groupbox(page, "🧾 全列型 DataGridView 演示", 16, 224, 1048, 564)
    base.groupbox(page, "🧭 表头 / 单元格 / 对齐 / 导出", 1080, 224, 384, 564)
    register_theme_label(
        base.label(
            page,
            "左侧是完整表格区，支持普通表格与 1,000,000 行虚拟表格切换，并绑定右键菜单。",
            40,
            256,
            960,
            24,
            fg=muted_color,
            bg=top_bg,
        ),
        "muted",
        "page",
    )
    register_theme_label(
        base.label(
            page,
            "右侧集中放表头读写、单元格读写、表头/内容对齐按钮和导出操作，避免右下角按钮再被遮住。",
            1104,
            256,
            336,
            40,
            fg=muted_color,
            bg=top_bg,
            wrap=True,
        ),
        "muted",
        "page",
    )

    register_theme_label(base.label(page, "🗂️ 表头读取 / 修改 / 对齐", 1104, 302, 260, 22, fg=text_color, bg=top_bg, size=14, bold=True), "text", "page")
    header_readout = register_theme_label(
        base.label(page, "等待读取表头。", 1104, 328, 336, 54, fg=muted_color, bg=card_bg, wrap=True),
        "muted",
        "card",
    )
    register_theme_label(base.label(page, "🧪 单元格读取 / 修改 / 对齐", 1104, 516, 260, 22, fg=text_color, bg=top_bg, size=14, bold=True), "text", "page")
    cell_readout = register_theme_label(
        base.label(page, "等待读取单元格。", 1104, 542, 336, 48, fg=muted_color, bg=card_bg, wrap=True),
        "muted",
        "card",
    )
    register_theme_label(base.label(page, "🎨 样式 / 编辑 / 导出", 1104, 716, 240, 22, fg=text_color, bg=top_bg, size=14, bold=True), "text", "page")

    normal_headers = ["🧾 任务", "☑️ 启用", "🚦 状态", "🏷️ 标签", "🔘 动作", "🔗 链接", "🖼️ 图片", "📝 备注"]
    virtual_headers = ["🧾 序号", "🚦 状态", "🏷️ 优先级", "👤 节点", "🛠 路由", "🖼️ 图片", "📝 虚拟备注"]
    default_normal_headers = list(normal_headers)
    default_virtual_headers = list(virtual_headers)
    rows_seed: list[dict[str, object]] = [
        {"task": "🧾 任务 1", "enabled": True, "status": "🚧 进行中", "tag": "🔵 P1", "action": "执行", "link": "查看详情", "icon": "图片-A", "note": "支持下拉、勾选和标签色块"},
        {"task": "🧾 任务 2", "enabled": False, "status": "🕒 待处理", "tag": "🟢 P2", "action": "审核", "link": "打开文档", "icon": "图片-B", "note": "支持按钮列、链接列和图片列"},
        {"task": "🧾 任务 3", "enabled": True, "status": "✅ 已完成", "tag": "🟠 P3", "action": "归档", "link": "查看报告", "icon": "图片-C", "note": "支持排序、导出 CSV 与表头读写"},
    ]
    image_demo_paths = [
        base.repo_root() / "imgs" / "1.png",
        base.repo_root() / "imgs" / "2.png",
        base.repo_root() / "imgs" / "3.png",
    ]
    normal_column_defs = (
        (normal_headers[0], DLL.DataGrid_AddTextColumn, 168),
        (normal_headers[1], DLL.DataGrid_AddCheckBoxColumn, 68),
        (normal_headers[2], DLL.DataGrid_AddComboBoxColumn, 116),
        (normal_headers[3], DLL.DataGrid_AddTagColumn, 90),
        (normal_headers[4], DLL.DataGrid_AddButtonColumn, 92),
        (normal_headers[5], DLL.DataGrid_AddLinkColumn, 118),
        (normal_headers[6], DLL.DataGrid_AddImageColumn, 88),
        (normal_headers[7], DLL.DataGrid_AddTextColumn, 246),
    )
    virtual_column_widths = (124, 118, 108, 110, 126, 88, 270)
    grid_local: dict[str, object] = {
        "normal": None,
        "virtual": None,
        "virtual_mode": False,
        "header_dark": True,
        "selected_row": 0,
        "selected_col": 0,
        "sort_states": {},
        "row_count": len(rows_seed),
        "dblclick_enabled": True,
        "accent_style": False,
    }

    def alignment_name(value: int) -> str:
        return {
            base.ALIGN_LEFT: "靠左",
            base.ALIGN_CENTER: "居中",
            base.ALIGN_RIGHT: "靠右",
        }.get(value, f"未知({value})")

    def set_grid_state(text: str) -> None:
        base.set_label_text(grid_state, text)
        base.set_status(text)

    def active_grid() -> HWND | None:
        return grid_local["virtual"] if bool(grid_local["virtual_mode"]) else grid_local["normal"]  # type: ignore[return-value]

    def update_mode_label() -> None:
        if bool(grid_local["virtual_mode"]):
            base.set_label_text(mode_label, "当前模式: 虚拟表格 1,000,000 行")
        else:
            base.set_label_text(mode_label, f"当前模式: 普通表格 {int(grid_local['row_count'])} 行")

    def utf8_buf_read(fn, *args) -> str:
        size = fn(*args, None, 0)
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        fn(*args, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    def get_header_text(h_grid: HWND, col: int) -> str:
        return utf8_buf_read(DLL.DataGrid_GetColumnHeaderText, h_grid, col)

    def get_cell_text(h_grid: HWND, row: int, col: int) -> str:
        if h_grid == grid_local["virtual"]:
            return base.build_virtual_grid_text(row, col)
        return utf8_buf_read(DLL.DataGrid_GetCellText, h_grid, row, col)

    def refresh_header_readout(prefix: str = "读取表头") -> None:
        normal_grid = grid_local["normal"]
        virtual_grid = grid_local["virtual"]
        normal_text = " | ".join(get_header_text(normal_grid, i) for i in range(DLL.DataGrid_GetColumnCount(normal_grid))) if normal_grid else ""
        virtual_text = " | ".join(get_header_text(virtual_grid, i) for i in range(DLL.DataGrid_GetColumnCount(virtual_grid))) if virtual_grid else ""
        base.set_label_text(header_readout, f"{prefix}\n普通表头: {normal_text}\n虚拟表头: {virtual_text}")

    def refresh_cell_readout(prefix: str = "读取单元格") -> None:
        h_grid = active_grid()
        if not h_grid:
            return
        row = int(DLL.DataGrid_GetSelectedRow(h_grid))
        col = int(DLL.DataGrid_GetSelectedCol(h_grid))
        if row < 0 or col < 0:
            row = int(grid_local["selected_row"])
            col = int(grid_local["selected_col"])
        text = get_cell_text(h_grid, row, col)
        extra = ""
        if h_grid == grid_local["normal"] and col == 1 and row >= 0:
            extra = f"\n勾选状态: {'True' if bool(DLL.DataGrid_GetCellChecked(h_grid, row, col)) else 'False'}"
        base.set_label_text(cell_readout, f"{prefix}\nrow={row}, col={col}\nvalue={text if text else '(空)'}{extra}")

    def apply_demo_cell_styles() -> None:
        for row in range(int(DLL.DataGrid_GetRowCount(normal_grid))):
            tag_bg = THEME_SURFACE_PRIMARY if row % 2 == 0 else THEME_SURFACE_SUCCESS
            image_bg = THEME_SURFACE_PRIMARY if row % 2 == 0 else THEME_SURFACE_SUCCESS
            DLL.DataGrid_SetCellStyle(normal_grid, row, 3, 0xFF409EFF if row % 2 == 0 else 0xFF67C23A, tag_bg, BOOL(False), BOOL(False))
            DLL.DataGrid_SetCellStyle(normal_grid, row, 4, 0xFFFFFFFF, 0xFF409EFF if row % 2 == 0 else 0xFF67C23A, BOOL(False), BOOL(False))
            DLL.DataGrid_SetCellStyle(normal_grid, row, 5, 0xFF409EFF, 0x00000000, BOOL(False), BOOL(False))
            DLL.DataGrid_SetCellStyle(normal_grid, row, 6, 0xFF409EFF if row % 2 == 0 else 0xFF67C23A, image_bg, BOOL(False), BOOL(False))
            if bool(grid_local["accent_style"]):
                DLL.DataGrid_SetCellStyle(normal_grid, row, 0, 0xFF8E44AD, THEME_SURFACE_INFO, BOOL(True), BOOL(False))
                DLL.DataGrid_SetCellStyle(normal_grid, row, 7, THEME_TEXT, THEME_SURFACE_WARNING, BOOL(False), BOOL(False))
            else:
                DLL.DataGrid_SetCellStyle(normal_grid, row, 0, 0x00000000, 0x00000000, BOOL(False), BOOL(False))
                DLL.DataGrid_SetCellStyle(normal_grid, row, 7, 0x00000000, 0x00000000, BOOL(False), BOOL(False))
        DLL.DataGrid_Refresh(normal_grid)

    def set_demo_bitmap(row: int, image_index: int) -> None:
        if row < 0:
            return
        path = image_demo_paths[image_index % len(image_demo_paths)]
        p, n, _ = s(str(path))
        DLL.DataGrid_SetCellImageFromFile(normal_grid, row, 6, p, n)

    def apply_common_styles(h_grid: HWND, header_count: int) -> None:
        DLL.DataGrid_SetSelectionMode(h_grid, 0)
        DLL.DataGrid_SetShowGridLines(h_grid, BOOL(True))
        DLL.DataGrid_SetDefaultRowHeight(h_grid, 40)
        DLL.DataGrid_SetHeaderHeight(h_grid, 48)
        DLL.DataGrid_SetHeaderStyle(h_grid, 2 if bool(grid_local["header_dark"]) else 0)
        DLL.DataGrid_SetHeaderMultiline(h_grid, BOOL(False))
        for col in range(header_count):
            DLL.DataGrid_SetColumnHeaderAlignment(h_grid, col, base.ALIGN_CENTER)
            DLL.DataGrid_SetColumnCellAlignment(h_grid, col, base.ALIGN_LEFT)
        DLL.DataGrid_Refresh(h_grid)

    normal_grid = DLL.CreateDataGridView(page, 36, 292, 1008, 468, BOOL(False), BOOL(True), THEME_TEXT, THEME_BG)
    virtual_grid = DLL.CreateDataGridView(page, 36, 292, 1008, 468, BOOL(True), BOOL(True), THEME_TEXT, THEME_BG)
    grid_local["normal"] = normal_grid
    grid_local["virtual"] = virtual_grid
    DLL.DataGrid_SetColors(normal_grid, THEME_TEXT, THEME_BG, THEME_SURFACE, THEME_TEXT, THEME_SURFACE_PRIMARY, THEME_SURFACE, THEME_BORDER_LIGHT)
    DLL.DataGrid_SetColors(virtual_grid, THEME_TEXT, THEME_BG, THEME_SURFACE, THEME_TEXT, THEME_SURFACE_PRIMARY, THEME_SURFACE, THEME_BORDER_LIGHT)
    DLL.DataGrid_Show(virtual_grid, BOOL(False))

    for title, fn, width in normal_column_defs:
        p, n, _ = s(title)
        fn(normal_grid, p, n, width)

    for title, width in zip(virtual_headers, virtual_column_widths):
        p, n, _ = s(title)
        DLL.DataGrid_AddTextColumn(virtual_grid, p, n, width)

    cp, cn, _ = s("🕒 待处理\n🚧 进行中\n✅ 已完成\n⏸️ 已暂停")
    DLL.DataGrid_SetColumnComboItems(normal_grid, 2, cp, cn)
    DLL.DataGrid_SetDoubleClickEnabled(normal_grid, BOOL(bool(grid_local["dblclick_enabled"])))
    apply_common_styles(normal_grid, len(normal_headers))
    apply_common_styles(virtual_grid, len(virtual_headers))
    DLL.DataGrid_SetColumnCellAlignment(normal_grid, 1, base.ALIGN_CENTER)
    DLL.DataGrid_SetColumnCellAlignment(normal_grid, 2, base.ALIGN_CENTER)
    DLL.DataGrid_SetColumnCellAlignment(normal_grid, 3, base.ALIGN_CENTER)
    DLL.DataGrid_SetColumnCellAlignment(normal_grid, 4, base.ALIGN_CENTER)
    DLL.DataGrid_SetColumnCellAlignment(normal_grid, 6, base.ALIGN_CENTER)

    def apply_alignment(*, header_align: int | None = None, cell_align: int | None = None) -> None:
        targets = (
            (normal_grid, len(normal_headers)),
            (virtual_grid, len(virtual_headers)),
        )
        for h_grid, count in targets:
            for col in range(count):
                if header_align is not None:
                    DLL.DataGrid_SetColumnHeaderAlignment(h_grid, col, header_align)
                if cell_align is not None:
                    DLL.DataGrid_SetColumnCellAlignment(h_grid, col, cell_align)
            DLL.DataGrid_Refresh(h_grid)
        if header_align is not None and cell_align is not None:
            set_grid_state(f"已将表头设为{alignment_name(header_align)}，单元格内容设为{alignment_name(cell_align)}。")
        elif header_align is not None:
            set_grid_state(f"已将全部列表头设为{alignment_name(header_align)}。")
        elif cell_align is not None:
            set_grid_state(f"已将全部单元格内容设为{alignment_name(cell_align)}。")

    for row_data in rows_seed:
        row = DLL.DataGrid_AddRow(normal_grid)
        values = [
            str(row_data["task"]),
            None,
            str(row_data["status"]),
            str(row_data["tag"]),
            str(row_data["action"]),
            str(row_data["link"]),
            str(row_data["icon"]),
            str(row_data["note"]),
        ]
        for col, value in enumerate(values):
            if value is None:
                DLL.DataGrid_SetCellChecked(normal_grid, row, col, BOOL(bool(row_data["enabled"])))
                continue
            p, n, _ = s(value)
            DLL.DataGrid_SetCellText(normal_grid, row, col, p, n)
        tag_fg = 0xFF409EFF if "P1" in str(row_data["tag"]) else (0xFF67C23A if "P2" in str(row_data["tag"]) else 0xFFE6A23C)
        tag_bg = THEME_SURFACE_PRIMARY if "P1" in str(row_data["tag"]) else (THEME_SURFACE_SUCCESS if "P2" in str(row_data["tag"]) else THEME_SURFACE_WARNING)
        DLL.DataGrid_SetCellStyle(normal_grid, row, 3, tag_fg, tag_bg, BOOL(False), BOOL(False))
        DLL.DataGrid_SetCellStyle(normal_grid, row, 4, 0xFFFFFFFF, 0xFF409EFF if row == 0 else (0xFF67C23A if row == 1 else 0xFFE6A23C), BOOL(False), BOOL(False))
        DLL.DataGrid_SetCellStyle(normal_grid, row, 5, 0xFF409EFF, 0x00000000, BOOL(False), BOOL(False))
        DLL.DataGrid_SetCellStyle(normal_grid, row, 6, 0xFF409EFF if row == 0 else (0xFF67C23A if row == 1 else 0xFFE6A23C), THEME_SURFACE_PRIMARY if row == 0 else (THEME_SURFACE_SUCCESS if row == 1 else THEME_SURFACE_WARNING), BOOL(False), BOOL(False))
        set_demo_bitmap(row, row)
    apply_demo_cell_styles()

    vcb = DLL._GridVirtualCB(base.on_virtual_grid_request)
    KEEP.append(vcb)
    DLL.DataGrid_SetVirtualDataCallback(virtual_grid, vcb)
    DLL.DataGrid_SetVirtualRowCount(virtual_grid, 1_000_000)

    def on_grid_click(h_grid: HWND, row: int, col: int) -> None:
        grid_local["selected_row"] = row
        grid_local["selected_col"] = col
        text = get_cell_text(h_grid, row, col)
        if h_grid == normal_grid and col == 4:
            base.show_msg("按钮列点击", f"点击了按钮列: row={row}, value={text}", "🔘")
        elif h_grid == normal_grid and col == 5:
            base.show_msg("链接列点击", f"点击了链接列: row={row}, value={text}", "🔗")
        elif h_grid == normal_grid and col == 6:
            base.show_msg("图片列点击", f"点击了 bitmap 图片列: row={row}, alt={text}", "🖼️")
        set_grid_state(f"🧾 单元格点击: row={row}, col={col}, value={text if text else '(空)'}")
        refresh_cell_readout("点击后读取单元格")

    def on_grid_dblclick(_h_grid: HWND, row: int, col: int) -> None:
        set_grid_state(f"🖋️ 双击编辑: row={row}, col={col}")

    def on_grid_change(h_grid: HWND, row: int, col: int) -> None:
        text = get_cell_text(h_grid, row, col)
        set_grid_state(f"✅ 单元格值变化: row={row}, col={col}, value={text if text else '(空)'}")
        refresh_cell_readout("值变化后读取单元格")

    def on_grid_selection(h_grid: HWND, row: int, col: int) -> None:
        grid_local["selected_row"] = row
        grid_local["selected_col"] = col
        text = get_cell_text(h_grid, row, col)
        set_grid_state(f"🎯 选中单元格: row={row}, col={col}, value={text if text else '(空)'}")
        refresh_cell_readout("选中后读取单元格")

    def toggle_sort(col: int) -> None:
        if bool(grid_local["virtual_mode"]):
            set_grid_state("虚拟表格不做排序演示，请先切回普通表格。")
            return
        current = int(grid_local["sort_states"].get(col, 2))
        next_order = 1 if current != 1 else 2
        grid_local["sort_states"][col] = next_order
        DLL.DataGrid_SortByColumn(normal_grid, col, next_order)
        DLL.DataGrid_Refresh(normal_grid)
        set_grid_state(f"📊 已按列 {col} {'升序' if next_order == 1 else '降序'} 排序。")
        refresh_cell_readout("排序后读取单元格")

    def on_header_click(h_grid: HWND, col: int) -> None:
        if h_grid == normal_grid:
            toggle_sort(col)
        else:
            set_grid_state(f"🧭 虚拟表格列表头点击: col={col}")

    g1 = DLL._GridCB(on_grid_click)
    g2 = DLL._GridCB(on_grid_dblclick)
    g3 = DLL._GridCB(on_grid_change)
    g4 = DLL._GridSelCB(on_grid_selection)
    g5 = DLL._GridHeaderCB(on_header_click)
    KEEP.extend([g1, g2, g3, g4, g5])
    for h_grid in (normal_grid, virtual_grid):
        DLL.DataGrid_SetCellClickCallback(h_grid, g1)
        DLL.DataGrid_SetCellDoubleClickCallback(h_grid, g2)
        DLL.DataGrid_SetSelectionChangedCallback(h_grid, g4)
        DLL.DataGrid_SetColumnHeaderClickCallback(h_grid, g5)
    DLL.DataGrid_SetCellValueChangedCallback(normal_grid, g3)

    def append_row() -> None:
        row_index = DLL.DataGrid_AddRow(normal_grid)
        idx = int(grid_local["row_count"]) + 1
        grid_local["row_count"] = idx
        values = [
            f"🧾 任务 {idx}",
            None,
            "🚧 进行中" if idx % 2 else "🕒 待处理",
            "🔵 P1" if idx % 2 else "🟢 P2",
            "执行",
            "查看详情",
            f"图片-{idx}",
            "新插入行，支持完整列型展示",
        ]
        for col, value in enumerate(values):
            if value is None:
                DLL.DataGrid_SetCellChecked(normal_grid, row_index, col, BOOL(idx % 2 == 1))
                continue
            p, n, _ = s(value)
            DLL.DataGrid_SetCellText(normal_grid, row_index, col, p, n)
        set_demo_bitmap(row_index, idx - 1)
        apply_demo_cell_styles()
        update_mode_label()
        set_grid_state(f"➕ 已新增普通表格第 {idx} 行。")

    def clear_rows() -> None:
        DLL.DataGrid_ClearRows(normal_grid)
        grid_local["row_count"] = 0
        DLL.DataGrid_Refresh(normal_grid)
        update_mode_label()
        set_grid_state("🧹 已清空普通表格。")
        refresh_cell_readout("清空后读取单元格")

    def toggle_virtual_mode() -> None:
        use_virtual = not bool(grid_local["virtual_mode"])
        grid_local["virtual_mode"] = use_virtual
        DLL.DataGrid_Show(normal_grid, BOOL(not use_virtual))
        DLL.DataGrid_Show(virtual_grid, BOOL(use_virtual))
        DLL.DataGrid_Refresh(virtual_grid if use_virtual else normal_grid)
        update_mode_label()
        set_grid_state("🚀 已切换到 1,000,000 行虚拟表格。" if use_virtual else f"🧾 已切回普通表格，共 {int(grid_local['row_count'])} 行。")
        refresh_cell_readout("切换模式后读取单元格")

    def toggle_header_style() -> None:
        grid_local["header_dark"] = not bool(grid_local["header_dark"])
        for h_grid in (normal_grid, virtual_grid):
            DLL.DataGrid_SetHeaderStyle(h_grid, 2 if bool(grid_local["header_dark"]) else 0)
            DLL.DataGrid_Refresh(h_grid)
        set_grid_state(f"🎛️ 已切换表头样式为 {'Dark' if bool(grid_local['header_dark']) else 'Plain'}。")

    def toggle_double_click_edit() -> None:
        grid_local["dblclick_enabled"] = not bool(grid_local["dblclick_enabled"])
        DLL.DataGrid_SetDoubleClickEnabled(normal_grid, BOOL(bool(grid_local["dblclick_enabled"])))
        set_grid_state(f"🖋️ 普通表格双击编辑已{'开启' if bool(grid_local['dblclick_enabled']) else '关闭'}。")

    def toggle_demo_cell_style() -> None:
        grid_local["accent_style"] = not bool(grid_local["accent_style"])
        apply_demo_cell_styles()
        set_grid_state(f"🎨 单元格演示样式已{'开启' if bool(grid_local['accent_style']) else '恢复默认'}。")

    def rename_header(col: int, text: str, *, virtual: bool = False) -> None:
        target = virtual_grid if virtual else normal_grid
        p, n, _ = s(text)
        DLL.DataGrid_SetColumnHeaderText(target, col, p, n)
        DLL.DataGrid_Refresh(target)
        refresh_header_readout("修改表头后读取")
        set_grid_state(f"🗂️ 已修改{'虚拟' if virtual else '普通'}表格列表头 col={col} -> {text}")

    def restore_headers() -> None:
        for idx, text in enumerate(default_normal_headers):
            p, n, _ = s(text)
            DLL.DataGrid_SetColumnHeaderText(normal_grid, idx, p, n)
        for idx, text in enumerate(default_virtual_headers):
            p, n, _ = s(text)
            DLL.DataGrid_SetColumnHeaderText(virtual_grid, idx, p, n)
        DLL.DataGrid_Refresh(normal_grid)
        DLL.DataGrid_Refresh(virtual_grid)
        refresh_header_readout("已恢复默认表头")
        set_grid_state("↩️ 已恢复普通表格和虚拟表格默认表头。")

    def select_cell(row: int, col: int) -> None:
        h_grid = active_grid()
        if not h_grid:
            return
        DLL.DataGrid_SetSelectedCell(h_grid, row, col)
        grid_local["selected_row"] = row
        grid_local["selected_col"] = col
        refresh_cell_readout(f"已定位到 [{row}, {col}]")

    def focus_image_column() -> None:
        if bool(grid_local["virtual_mode"]):
            select_cell(0, 5)
            set_grid_state("🖼️ 已定位到虚拟表格图片列（col=5）。")
            return
        select_cell(0, 6)
        set_grid_state("🖼️ 已定位到普通表格图片列（col=6）。")

    def write_selected_cell() -> None:
        if bool(grid_local["virtual_mode"]):
            set_grid_state("虚拟表格不支持直接改单元格，请先切回普通表格。")
            return
        row = int(DLL.DataGrid_GetSelectedRow(normal_grid))
        col = int(DLL.DataGrid_GetSelectedCol(normal_grid))
        if row < 0 or col < 0:
            row, col = 0, 7
        text = f"🪄 已修改[{row},{col}]"
        p, n, _ = s(text)
        DLL.DataGrid_SetCellText(normal_grid, row, col, p, n)
        DLL.DataGrid_Refresh(normal_grid)
        grid_local["selected_row"] = row
        grid_local["selected_col"] = col
        set_grid_state(f"✅ 已修改普通表格单元格 [{row}, {col}]。")
        refresh_cell_readout("修改后读取单元格")

    def toggle_selected_checkbox() -> None:
        if bool(grid_local["virtual_mode"]):
            set_grid_state("虚拟表格没有勾选列，请先切回普通表格。")
            return
        row = int(DLL.DataGrid_GetSelectedRow(normal_grid))
        if row < 0:
            row = 0
        current = bool(DLL.DataGrid_GetCellChecked(normal_grid, row, 1))
        DLL.DataGrid_SetCellChecked(normal_grid, row, 1, BOOL(not current))
        DLL.DataGrid_Refresh(normal_grid)
        grid_local["selected_row"] = row
        grid_local["selected_col"] = 1
        set_grid_state(f"☑️ 已切换第 {row} 行勾选状态为 {not current}。")
        refresh_cell_readout("切换勾选后读取单元格")

    def export_csv() -> None:
        export_path = base.repo_root() / "examples" / "Python" / "_datagrid_export_demo.csv"
        p, n, _ = s(str(export_path))
        ok = bool(DLL.DataGrid_ExportCSV(normal_grid, p, n))
        if ok:
            base.set_label_text(export_path_label, f"CSV 已导出:\n{export_path}")
            set_grid_state(f"📦 已导出 CSV -> {export_path}")
        else:
            base.set_label_text(export_path_label, "CSV 导出失败。")
            set_grid_state("CSV 导出失败。")

    menu_ids = {"add": 9301, "clear": 9302, "toggle_virtual": 9303, "read": 9304, "header": 9305}

    def on_grid_menu(_menu_id: int, item_id: int) -> None:
        if item_id == menu_ids["add"]:
            append_row()
        elif item_id == menu_ids["clear"]:
            clear_rows()
        elif item_id == menu_ids["toggle_virtual"]:
            toggle_virtual_mode()
        elif item_id == menu_ids["read"]:
            refresh_cell_readout("右键菜单读取单元格")
            set_grid_state("📥 已通过表格右键菜单读取当前单元格。")
        elif item_id == menu_ids["header"]:
            toggle_header_style()

    grid_menu = DLL.CreateEmojiPopupMenu(page)
    base.menu_add(grid_menu, "➕ 添加一行", menu_ids["add"])
    base.menu_add(grid_menu, "🧹 清空普通表格", menu_ids["clear"])
    base.menu_add(grid_menu, "🚀 切换虚拟表格", menu_ids["toggle_virtual"])
    base.menu_add(grid_menu, "📥 读取当前单元格", menu_ids["read"])
    base.menu_add(grid_menu, "🎛️ 切换表头样式", menu_ids["header"])
    menu_cb = DLL._MenuCB(on_grid_menu)
    KEEP.append(menu_cb)
    DLL.SetPopupMenuCallback(grid_menu, menu_cb)
    DLL.BindControlMenu(normal_grid, grid_menu)
    DLL.BindControlMenu(virtual_grid, grid_menu)

    base.button(toolbar_panel, "➕", "加一行", 8, 4, 96, 32, 0xFF409EFF, append_row)
    base.button(toolbar_panel, "🧹", "清空表格", 112, 4, 104, 32, 0xFFF56C6C, clear_rows)
    base.button(toolbar_panel, "🚀", "切换虚拟", 224, 4, 104, 32, 0xFF8E44AD, toggle_virtual_mode)
    base.button(toolbar_panel, "🖼️", "定位图片列", 336, 4, 112, 32, 0xFF409EFF, focus_image_column)
    base.button(toolbar_panel, "📊", "任务排序", 456, 4, 96, 32, 0xFF409EFF, lambda: toggle_sort(0))
    base.button(toolbar_panel, "🎛️", "切表头风格", 560, 4, 116, 32, 0xFFE6A23C, toggle_header_style)

    base.button(page, "📥", "读表头", 1104, 390, 160, 34, 0xFF409EFF, lambda: refresh_header_readout("手动读取表头"))
    base.button(page, "↩", "恢复表头", 1280, 390, 160, 34, 0xFF909399, restore_headers)
    base.button(page, "1", "改首列", 1104, 432, 160, 34, 0xFFE6A23C, lambda: rename_header(0, "🧪 工单"))
    base.button(page, "7", "改末列", 1280, 432, 160, 34, 0xFF67C23A, lambda: rename_header(6, "📝 虚拟说明", virtual=True))
    base.button(page, "L", "表头靠左", 1104, 474, 104, 34, 0xFF909399, lambda: apply_alignment(header_align=base.ALIGN_LEFT))
    base.button(page, "C", "表头居中", 1216, 474, 104, 34, 0xFF409EFF, lambda: apply_alignment(header_align=base.ALIGN_CENTER))
    base.button(page, "R", "表头靠右", 1328, 474, 104, 34, 0xFFE6A23C, lambda: apply_alignment(header_align=base.ALIGN_RIGHT))

    base.button(page, "🎯", "定位[0,0]", 1104, 594, 160, 34, 0xFF409EFF, lambda: select_cell(0, 0))
    base.button(page, "📝", "定位备注", 1280, 594, 160, 34, 0xFFE6A23C, lambda: select_cell(0, 7))
    base.button(page, "✏️", "改单元格", 1104, 636, 160, 34, 0xFF8E44AD, write_selected_cell)
    base.button(page, "☑️", "切勾选", 1280, 636, 160, 34, 0xFF67C23A, toggle_selected_checkbox)
    base.button(page, "L", "内容靠左", 1104, 678, 104, 34, 0xFF909399, lambda: apply_alignment(cell_align=base.ALIGN_LEFT))
    base.button(page, "C", "内容居中", 1216, 678, 104, 34, 0xFF409EFF, lambda: apply_alignment(cell_align=base.ALIGN_CENTER))
    base.button(page, "R", "内容靠右", 1328, 678, 104, 34, 0xFFE6A23C, lambda: apply_alignment(cell_align=base.ALIGN_RIGHT))

    base.button(page, "🎨", "切单元格样式", 1104, 742, 104, 34, 0xFF409EFF, toggle_demo_cell_style)
    base.button(page, "🖋️", "双击编辑", 1216, 742, 104, 34, 0xFF909399, toggle_double_click_edit)
    base.button(page, "📦", "导出 CSV", 1328, 742, 104, 34, 0xFF67C23A, export_csv)

    refresh_header_readout("初始表头")
    update_mode_label()
    select_cell(0, 0)
    set_grid_state("🧾 表格页已整理：移除了无关标签演示，补齐了表头/单元格对齐按钮，并重新压紧了右侧操作区布局。")

def build_page_editbox(page: HWND) -> None:
    palette = page_palette()
    page_bg = palette["page_bg"]
    text_color = palette["text"]
    muted_color = palette["muted"]
    accent_color = palette["accent"]

    base.groupbox(page, "⌨️ EditBox 实时属性读取", 16, 16, 980, 248)
    base.groupbox(page, "🪄 文本 / 颜色 / 尺寸 / 状态", 16, 286, 980, 254)
    base.groupbox(page, "📄 多行 EditBox 演示", 1020, 16, 444, 524)
    base.groupbox(page, "📌 EditBox API 说明", 16, 558, 1448, 230)

    demo_edit = base.edit(page, "📌 单行 EditBox：可直接读取和设置文本。", 56, 120, 420, 38, False)
    memo = DLL.CreateEditBox(
        page,
        1044,
        72,
        396,
        244,
        *s("📄 已从主编辑框同步：\r\n1. 用于展示多行输入\r\n2. 保持统一浅底风格\r\n3. 可作为备注或说明区域")[:2],
        THEME_TEXT,
        THEME_BG,
        base.FONT_PTR,
        base.FONT_LEN,
        13,
        BOOL(False),
        BOOL(False),
        BOOL(False),
        base.ALIGN_LEFT,
        BOOL(True),
        BOOL(False),
        BOOL(False),
        BOOL(True),
        BOOL(False),
    )
    readout = register_theme_label(base.label(page, "等待读取编辑框属性。", 40, 184, 920, 56, fg=text_color, bg=page_bg, wrap=True), "text", "page")
    state_text = register_theme_label(base.label(page, "编辑框页状态将在这里更新。", 40, 760, 1360, 22, fg=accent_color, bg=page_bg), "accent", "page")
    register_theme_label(base.label(page, "这一页直接读取文本、颜色、位置、字体、启用态和可见态，不再只是放一个输入框。", 40, 56, 900, 24, fg=muted_color, bg=page_bg), "muted", "page")

    def read_utf8_edit(h_edit: HWND) -> str:
        size = int(DLL.GetEditBoxText(h_edit, None, 0))
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        DLL.GetEditBoxText(h_edit, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    def read_edit_bounds() -> tuple[int, int, int, int]:
        x = ctypes.c_int()
        y = ctypes.c_int()
        w = ctypes.c_int()
        h = ctypes.c_int()
        if int(DLL.GetEditBoxBounds(demo_edit, ctypes.byref(x), ctypes.byref(y), ctypes.byref(w), ctypes.byref(h))) != 0:
            return 0, 0, 0, 0
        return x.value, y.value, w.value, h.value

    def read_edit_font() -> tuple[str, int, int]:
        buf = ctypes.create_string_buffer(128)
        size = ctypes.c_int()
        bold = ctypes.c_int()
        italic = ctypes.c_int()
        underline = ctypes.c_int()
        result = int(DLL.GetEditBoxFont(demo_edit, buf, 128, ctypes.byref(size), ctypes.byref(bold), ctypes.byref(italic), ctypes.byref(underline)))
        name = buf.raw[:max(result, 0)].decode("utf-8", errors="replace") if result > 0 else ""
        return name, size.value, bold.value

    fg0 = UINT32()
    bg0 = UINT32()
    DLL.GetEditBoxColor(demo_edit, ctypes.byref(fg0), ctypes.byref(bg0))
    initial = {
        "text": read_utf8_edit(demo_edit),
        "bounds": read_edit_bounds(),
        "fg": int(fg0.value),
        "bg": int(bg0.value),
    }

    def refresh(note: str = "已刷新编辑框属性") -> None:
        fg = UINT32()
        bg = UINT32()
        DLL.GetEditBoxColor(demo_edit, ctypes.byref(fg), ctypes.byref(bg))
        x, y, w, h = read_edit_bounds()
        font_name, font_size, bold = read_edit_font()
        align_name = base.alignment_name(int(DLL.GetEditBoxAlignment(demo_edit)))
        enabled = "启用" if int(DLL.GetEditBoxEnabled(demo_edit)) == 1 else "禁用"
        visible = "显示" if int(DLL.GetEditBoxVisible(demo_edit)) == 1 else "隐藏"
        base.set_label_text(
            readout,
            f"text={read_utf8_edit(demo_edit)}  {visible}/{enabled}\n"
            f"bounds=({x}, {y}, {w}, {h})  align={align_name}  font={font_name or 'default'} {font_size}px bold={bold}\n"
            f"fg=0x{int(fg.value):08X}  bg=0x{int(bg.value):08X}"
        )
        base.set_label_text(state_text, note)
        base.set_status(note)

    def set_edit_text_value(text: str, note: str) -> None:
        DLL.SetEditBoxText(demo_edit, *s(text)[:2])
        DLL.SetEditBoxText(memo, *s("📄 已从主编辑框同步：\r\n" + text)[:2])
        refresh(note)

    def set_edit_colors(fg: int, bg: int, note: str) -> None:
        DLL.SetEditBoxColor(demo_edit, fg, bg)
        refresh(note)

    def set_edit_font_value(font_name: str, font_size: int, bold: bool, note: str) -> None:
        x, y, w, _h = read_edit_bounds()
        target_h = 44 if font_size >= 16 else int(initial["bounds"][3])
        DLL.SetEditBoxBounds(demo_edit, x, y, w, target_h)
        DLL.SetEditBoxFont(demo_edit, *s(font_name)[:2], font_size, BOOL(bold), BOOL(False), BOOL(False))
        refresh(note)

    def move_edit(dx: int = 0, dy: int = 0, dw: int = 0) -> None:
        x, y, w, h = read_edit_bounds()
        DLL.SetEditBoxBounds(demo_edit, x + dx, y + dy, w + dw, h)
        refresh(f"编辑框位置/尺寸已更新: dx={dx}, dy={dy}, dw={dw}")

    def restore_edit() -> None:
        x, y, w, h = initial["bounds"]
        DLL.SetEditBoxText(demo_edit, *s(str(initial["text"]))[:2])
        DLL.SetEditBoxColor(demo_edit, int(initial["fg"]), int(initial["bg"]))
        DLL.SetEditBoxBounds(demo_edit, int(x), int(y), int(w), int(h))
        DLL.SetEditBoxFont(demo_edit, *s("Segoe UI Emoji")[:2], 13, BOOL(False), BOOL(False), BOOL(False))
        DLL.EnableEditBox(demo_edit, BOOL(True))
        DLL.ShowEditBox(demo_edit, BOOL(True))
        refresh("编辑框属性已恢复默认")

    register_theme_label(base.label(page, "📝 文本预设", 40, 326, 180, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    base.button(page, "🧾", "写入表单文案", 40, 360, 156, 36, 0xFF409EFF, lambda: set_edit_text_value("请输入项目名称 / 关键词 / 标题", "编辑框文本已切到表单模式"))
    base.button(page, "🌈", "写入混排文案", 212, 360, 156, 36, 0xFF67C23A, lambda: set_edit_text_value("🌈 EmojiWindow 支持 emoji / English / 数字 123", "编辑框文本已切到混排模式"))
    base.button(page, "📄", "同步到多行框", 384, 360, 156, 36, 0xFF8E44AD, lambda: (DLL.SetEditBoxText(memo, *s("📄 已从主编辑框同步：\r\n" + read_utf8_edit(demo_edit))[:2]), refresh("当前单行内容已同步到多行 EditBox")))

    register_theme_label(base.label(page, "🎨 颜色 / 字体", 40, 414, 180, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    base.button(page, "🧊", "冷色", 40, 448, 118, 36, 0xFF409EFF, lambda: set_edit_colors(THEME_PRIMARY, THEME_SURFACE_PRIMARY, "编辑框已切到冷色方案"))
    base.button(page, "🧡", "暖色", 172, 448, 118, 36, 0xFFE6A23C, lambda: set_edit_colors(THEME_WARNING, THEME_SURFACE_WARNING, "编辑框已切到暖色方案"))
    base.button(page, "🔠", "16px Bold", 304, 448, 118, 36, 0xFF67C23A, lambda: set_edit_font_value("Segoe UI Emoji", 16, True, "编辑框字体已切到 16px Bold"))
    base.button(page, "🔡", "13px", 436, 448, 118, 36, 0xFF909399, lambda: set_edit_font_value("Segoe UI Emoji", 13, False, "编辑框字体已切回 13px"))

    register_theme_label(base.label(page, "📻 布局 / 状态", 1044, 336, 180, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    base.button(page, "➡️", "右移 80", 1044, 370, 116, 32, 0xFF409EFF, lambda: move_edit(dx=80))
    base.button(page, "⬇️", "下移 24", 1172, 370, 116, 32, 0xFF67C23A, lambda: move_edit(dy=24))
    base.button(page, "↔️", "加宽 120", 1300, 370, 124, 32, 0xFFE6A23C, lambda: move_edit(dw=120))
    base.button(page, "🚫", "禁用/启用", 1044, 410, 116, 32, 0xFF8E44AD, lambda: (DLL.EnableEditBox(demo_edit, BOOL(not (int(DLL.GetEditBoxEnabled(demo_edit)) == 1))), refresh("编辑框启用状态已切换")))
    base.button(page, "👁️", "显示/隐藏", 1172, 410, 116, 32, 0xFF909399, lambda: (DLL.ShowEditBox(demo_edit, BOOL(not (int(DLL.GetEditBoxVisible(demo_edit)) == 1))), refresh("编辑框可见状态已切换")))
    base.button(page, "↺", "恢复默认", 1300, 410, 124, 32, 0xFF409EFF, restore_edit)
    register_theme_label(base.label(page, "右侧只保留多行编辑框和布局/状态控制，不再放无关的标签演示。", 1044, 458, 380, 52, fg=muted_color, bg=page_bg, wrap=True), "muted", "page")

    register_theme_label(base.label(page, "1. GetEditBoxText / SetEditBoxText：读取和修改输入文本。", 40, 598, 700, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "2. GetEditBoxColor / SetEditBoxColor：读取和切换前景色 / 背景色。", 40, 632, 720, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "3. GetEditBoxBounds / SetEditBoxBounds：直接修改编辑框位置与宽度。", 40, 666, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "4. GetEditBoxFont / SetEditBoxFont：读取和切换字体名、字号和粗体。", 40, 700, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "5. EnableEditBox / ShowEditBox：演示启用态和可见态切换。", 40, 734, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    refresh("编辑框页已整理：右侧只保留 EditBox 组件相关内容")


def build_page_color_emoji_edit(page: HWND) -> None:
    palette = page_palette()
    page_bg = palette["page_bg"]
    text_color = palette["text"]
    muted_color = palette["muted"]
    accent_color = palette["accent"]

    base.groupbox(page, "🌈 ColorEmojiEditBox 实时属性读取", 16, 16, 980, 248)
    base.groupbox(page, "🪄 文本 / 颜色 / 尺寸 / 状态", 16, 286, 980, 254)
    base.groupbox(page, "✨ 彩色 Emoji 多行编辑框演示", 1020, 16, 444, 524)
    base.groupbox(page, "📌 ColorEmojiEditBox API 说明", 16, 558, 1448, 230)

    demo_edit = base.edit(page, "🌈 ColorEmojiEditBox: 😀🚀📘✅", 56, 120, 460, 40, True)
    preview_edit = DLL.CreateColorEmojiEditBox(
        page,
        1044,
        72,
        396,
        128,
        *s("📎 第二组彩色内容：😀 Emoji / English / 数字 123 / ✅\r\n📝 这里现在是真正的多行 ColorEmojiEditBox。\r\n🚀 可继续验证彩色 emoji 在多行下的绘制。")[:2],
        THEME_TEXT,
        THEME_BG,
        base.FONT_PTR,
        base.FONT_LEN,
        13,
        BOOL(False),
        BOOL(False),
        BOOL(False),
        base.ALIGN_LEFT,
        BOOL(True),
        BOOL(False),
        BOOL(False),
        BOOL(True),
        BOOL(False),
    )
    readout = register_theme_label(base.label(page, "等待读取彩色 Emoji 编辑框属性。", 40, 184, 920, 56, fg=text_color, bg=page_bg, wrap=True), "text", "page")
    state_text = register_theme_label(base.label(page, "彩色 Emoji 编辑框页状态将在这里更新。", 40, 760, 1360, 22, fg=accent_color, bg=page_bg), "accent", "page")
    register_theme_label(base.label(page, "这一页直接用真实接口读取彩色 Emoji 编辑框的文本、颜色、位置、字体、启用态和可见态。", 40, 56, 920, 24, fg=muted_color, bg=page_bg), "muted", "page")

    def read_text(h_edit: HWND) -> str:
        size = int(DLL.GetEditBoxText(h_edit, None, 0))
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        DLL.GetEditBoxText(h_edit, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    def read_bounds() -> tuple[int, int, int, int]:
        x = ctypes.c_int()
        y = ctypes.c_int()
        w = ctypes.c_int()
        h = ctypes.c_int()
        if int(DLL.GetEditBoxBounds(demo_edit, ctypes.byref(x), ctypes.byref(y), ctypes.byref(w), ctypes.byref(h))) != 0:
            return 0, 0, 0, 0
        return x.value, y.value, w.value, h.value

    def read_font() -> tuple[str, int, int]:
        buf = ctypes.create_string_buffer(128)
        size = ctypes.c_int()
        bold = ctypes.c_int()
        italic = ctypes.c_int()
        underline = ctypes.c_int()
        result = int(DLL.GetEditBoxFont(demo_edit, buf, 128, ctypes.byref(size), ctypes.byref(bold), ctypes.byref(italic), ctypes.byref(underline)))
        name = buf.raw[:max(result, 0)].decode("utf-8", errors="replace") if result > 0 else ""
        return name, size.value, bold.value

    fg0 = UINT32()
    bg0 = UINT32()
    DLL.GetEditBoxColor(demo_edit, ctypes.byref(fg0), ctypes.byref(bg0))
    initial = {"text": read_text(demo_edit), "bounds": read_bounds(), "fg": int(fg0.value), "bg": int(bg0.value)}
    preview_initial = read_text(preview_edit)

    def refresh(note: str = "已刷新彩色 Emoji 编辑框属性") -> None:
        fg = UINT32()
        bg = UINT32()
        DLL.GetEditBoxColor(demo_edit, ctypes.byref(fg), ctypes.byref(bg))
        x, y, w, h = read_bounds()
        font_name, font_size, bold = read_font()
        enabled = "启用" if int(DLL.GetEditBoxEnabled(demo_edit)) == 1 else "禁用"
        visible = "显示" if int(DLL.GetEditBoxVisible(demo_edit)) == 1 else "隐藏"
        base.set_label_text(
            readout,
            f"text={read_text(demo_edit)}  {visible}/{enabled}\n"
            f"bounds=({x}, {y}, {w}, {h})  font={font_name or 'default'} {font_size}px bold={bold}\n"
            f"fg=0x{int(fg.value):08X}  bg=0x{int(bg.value):08X}"
        )
        base.set_label_text(state_text, note)
        base.set_status(note)

    def set_text_value(text: str, note: str) -> None:
        DLL.SetEditBoxText(demo_edit, *s(text)[:2])
        DLL.SetEditBoxText(preview_edit, *s("📎 第二组彩色内容：\r\n" + text + "\r\n✨ 多行彩色 Emoji 渲染中")[:2])
        refresh(note)

    def set_colors(fg: int, bg: int, note: str) -> None:
        DLL.SetEditBoxColor(demo_edit, fg, bg)
        refresh(note)

    def set_font_value(size: int, bold: bool, note: str) -> None:
        x, y, w, _h = read_bounds()
        target_h = 44 if size >= 16 else int(initial["bounds"][3])
        DLL.SetEditBoxBounds(demo_edit, x, y, w, target_h)
        DLL.SetEditBoxFont(demo_edit, *s("Segoe UI Emoji")[:2], size, BOOL(bold), BOOL(False), BOOL(False))
        refresh(note)

    def move_box(dx: int = 0, dy: int = 0, dw: int = 0) -> None:
        x, y, w, h = read_bounds()
        DLL.SetEditBoxBounds(demo_edit, x + dx, y + dy, w + dw, h)
        refresh(f"彩色编辑框位置/尺寸已更新: dx={dx}, dy={dy}, dw={dw}")

    def restore_box() -> None:
        x, y, w, h = initial["bounds"]
        DLL.SetEditBoxText(demo_edit, *s(str(initial["text"]))[:2])
        DLL.SetEditBoxText(preview_edit, *s(preview_initial)[:2])
        DLL.SetEditBoxColor(demo_edit, int(initial["fg"]), int(initial["bg"]))
        DLL.SetEditBoxBounds(demo_edit, int(x), int(y), int(w), int(h))
        DLL.SetEditBoxFont(demo_edit, *s("Segoe UI Emoji")[:2], 13, BOOL(False), BOOL(False), BOOL(False))
        DLL.EnableEditBox(demo_edit, BOOL(True))
        DLL.ShowEditBox(demo_edit, BOOL(True))
        refresh("彩色 Emoji 编辑框属性已恢复默认")

    register_theme_label(base.label(page, "📝 文本预设", 40, 326, 180, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    base.button(page, "😀", "表情混排", 40, 360, 156, 36, 0xFF409EFF, lambda: set_text_value("😀 Emoji / English / 数字 123 / ✅", "彩色编辑框文本已切到混排模式"))
    base.button(page, "🚀", "产品文案", 212, 360, 156, 36, 0xFF67C23A, lambda: set_text_value("🚀 EmojiWindow Pro / 支持 Unicode 彩色 emoji", "彩色编辑框文本已切到产品文案"))
    base.button(page, "🎨", "主题文案", 384, 360, 156, 36, 0xFF8E44AD, lambda: set_text_value("🎨 Light / Dark / Custom theme preview", "彩色编辑框文本已切到主题文案"))

    register_theme_label(base.label(page, "🎨 颜色 / 字体", 40, 414, 180, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    base.button(page, "🧊", "冷色", 40, 448, 118, 36, 0xFF409EFF, lambda: set_colors(THEME_PRIMARY, THEME_SURFACE_PRIMARY, "彩色编辑框已切到冷色方案"))
    base.button(page, "🧡", "暖色", 172, 448, 118, 36, 0xFFE6A23C, lambda: set_colors(THEME_WARNING, THEME_SURFACE_WARNING, "彩色编辑框已切到暖色方案"))
    base.button(page, "🔠", "16px Bold", 304, 448, 118, 36, 0xFF67C23A, lambda: set_font_value(16, True, "彩色编辑框字体已切到 16px Bold"))
    base.button(page, "🔡", "13px", 436, 448, 118, 36, 0xFF909399, lambda: set_font_value(13, False, "彩色编辑框字体已切回 13px"))

    register_theme_label(base.label(page, "📻 布局 / 状态", 1044, 222, 180, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    base.button(page, "➡️", "右移 80", 1044, 256, 116, 32, 0xFF409EFF, lambda: move_box(dx=80))
    base.button(page, "⬇️", "下移 20", 1172, 256, 116, 32, 0xFF67C23A, lambda: move_box(dy=20))
    base.button(page, "↔️", "加宽 120", 1300, 256, 124, 32, 0xFFE6A23C, lambda: move_box(dw=120))
    base.button(page, "🚫", "禁用/启用", 1044, 296, 116, 32, 0xFF8E44AD, lambda: (DLL.EnableEditBox(demo_edit, BOOL(not (int(DLL.GetEditBoxEnabled(demo_edit)) == 1))), refresh("彩色编辑框启用状态已切换")))
    base.button(page, "👁️", "显示/隐藏", 1172, 296, 116, 32, 0xFF909399, lambda: (DLL.ShowEditBox(demo_edit, BOOL(not (int(DLL.GetEditBoxVisible(demo_edit)) == 1))), refresh("彩色编辑框可见状态已切换")))
    base.button(page, "↺", "恢复默认", 1300, 296, 124, 32, 0xFF409EFF, restore_box)
    register_theme_label(base.label(page, "ColorEmojiEditBox 和普通 EditBox 共用文本/颜色/位置/显示控制接口，这里现在直接展示多行彩色 emoji 渲染。", 1044, 352, 382, 88, fg=muted_color, bg=page_bg, wrap=True), "muted", "page")

    register_theme_label(base.label(page, "1. GetEditBoxText / SetEditBoxText：直接读取和写入彩色 emoji 文本。", 40, 598, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "2. GetEditBoxColor / SetEditBoxColor：读取和切换前景色 / 背景色。", 40, 632, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "3. GetEditBoxBounds / SetEditBoxBounds：直接调整位置与宽度。", 40, 666, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "4. EnableEditBox / ShowEditBox：演示启用态和可见态切换。", 40, 700, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "5. 这一页重点不是接口差异，而是确认 DLL 的彩色 emoji 文本在真实读写后仍保持彩色。", 40, 734, 980, 24, fg=text_color, bg=page_bg), "text", "page")
    refresh("彩色 Emoji 编辑框页已整理：移除了无关标签演示，只保留编辑框组件相关内容")


def build_page_color_emoji_edit(page: HWND) -> None:
    palette = page_palette()
    page_bg = palette["page_bg"]
    text_color = palette["text"]
    muted_color = palette["muted"]
    accent_color = palette["accent"]

    base.groupbox(page, "🌈 ColorEmojiEditBox 实时属性读取", 16, 16, 980, 248)
    base.groupbox(page, "🪄 文本 / 颜色 / 尺寸 / 状态", 16, 286, 980, 254)
    base.groupbox(page, "✨ 彩色 Emoji 多行编辑框演示", 1020, 16, 444, 524)
    base.groupbox(page, "📌 ColorEmojiEditBox API 说明", 16, 558, 1448, 230)

    demo_edit = base.edit(page, "🌈 ColorEmojiEditBox: 😀🚀📘✅", 56, 120, 460, 40, True)
    preview_edit = DLL.CreateColorEmojiEditBox(
        page,
        1044,
        72,
        396,
        132,
        *s("📎 第二组彩色内容：\n😀 Emoji / English / 数字 123 / ✅\n📝 这里现在是真正的多行 ColorEmojiEditBox。\n🚀 可继续验证彩色 emoji 在多行下的绘制。")[:2],
        THEME_TEXT,
        THEME_BG,
        base.FONT_PTR,
        base.FONT_LEN,
        13,
        BOOL(False),
        BOOL(False),
        BOOL(False),
        base.ALIGN_LEFT,
        BOOL(True),
        BOOL(False),
        BOOL(False),
        BOOL(True),
        BOOL(False),
    )
    readout = register_theme_label(base.label(page, "等待读取彩色 Emoji 编辑框属性。", 40, 184, 920, 56, fg=text_color, bg=page_bg, wrap=True), "text", "page")
    state_text = register_theme_label(base.label(page, "彩色 Emoji 编辑框页状态将在这里更新。", 40, 760, 1360, 22, fg=accent_color, bg=page_bg), "accent", "page")
    register_theme_label(base.label(page, "这一页直接用真实接口读取彩色 Emoji 编辑框的文本、颜色、位置、字体、启用态和可见态。", 40, 56, 920, 24, fg=muted_color, bg=page_bg), "muted", "page")

    def read_text(h_edit: HWND) -> str:
        size = int(DLL.GetEditBoxText(h_edit, None, 0))
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        DLL.GetEditBoxText(h_edit, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    def read_bounds() -> tuple[int, int, int, int]:
        x = ctypes.c_int()
        y = ctypes.c_int()
        w = ctypes.c_int()
        h = ctypes.c_int()
        if int(DLL.GetEditBoxBounds(demo_edit, ctypes.byref(x), ctypes.byref(y), ctypes.byref(w), ctypes.byref(h))) != 0:
            return 0, 0, 0, 0
        return x.value, y.value, w.value, h.value

    def read_font() -> tuple[str, int, int]:
        buf = ctypes.create_string_buffer(128)
        size = ctypes.c_int()
        bold = ctypes.c_int()
        italic = ctypes.c_int()
        underline = ctypes.c_int()
        result = int(DLL.GetEditBoxFont(demo_edit, buf, 128, ctypes.byref(size), ctypes.byref(bold), ctypes.byref(italic), ctypes.byref(underline)))
        name = buf.raw[:max(result, 0)].decode("utf-8", errors="replace") if result > 0 else ""
        return name, size.value, bold.value

    fg0 = UINT32()
    bg0 = UINT32()
    DLL.GetEditBoxColor(demo_edit, ctypes.byref(fg0), ctypes.byref(bg0))
    initial = {"text": read_text(demo_edit), "bounds": read_bounds(), "fg": int(fg0.value), "bg": int(bg0.value)}
    preview_initial = read_text(preview_edit)

    def refresh(note: str = "已刷新彩色 Emoji 编辑框属性") -> None:
        fg = UINT32()
        bg = UINT32()
        DLL.GetEditBoxColor(demo_edit, ctypes.byref(fg), ctypes.byref(bg))
        x, y, w, h = read_bounds()
        font_name, font_size, bold = read_font()
        align_name = base.alignment_name(int(DLL.GetEditBoxAlignment(demo_edit)))
        enabled = "启用" if int(DLL.GetEditBoxEnabled(demo_edit)) == 1 else "禁用"
        visible = "显示" if int(DLL.GetEditBoxVisible(demo_edit)) == 1 else "隐藏"
        base.set_label_text(
            readout,
            f"text={read_text(demo_edit)}  {visible}/{enabled}\n"
            f"bounds=({x}, {y}, {w}, {h})  align={align_name}  font={font_name or 'default'} {font_size}px bold={bold}\n"
            f"fg=0x{int(fg.value):08X}  bg=0x{int(bg.value):08X}"
        )
        base.set_label_text(state_text, note)
        base.set_status(note)

    def set_text_value(text: str, note: str) -> None:
        DLL.SetEditBoxText(demo_edit, *s(text)[:2])
        DLL.SetEditBoxText(preview_edit, *s("📎 第二组彩色内容：\n" + text + "\n✨ 多行彩色 Emoji 渲染中")[:2])
        refresh(note)

    def set_colors(fg: int, bg: int, note: str) -> None:
        DLL.SetEditBoxColor(demo_edit, fg, bg)
        refresh(note)

    def set_font_value(size: int, bold: bool, note: str) -> None:
        x, y, w, _h = read_bounds()
        target_h = 44 if size >= 16 else int(initial["bounds"][3])
        DLL.SetEditBoxBounds(demo_edit, x, y, w, target_h)
        DLL.SetEditBoxFont(demo_edit, *s("Segoe UI Emoji")[:2], size, BOOL(bold), BOOL(False), BOOL(False))
        refresh(note)

    def set_alignment_value(alignment: int, note: str) -> None:
        DLL.SetEditBoxAlignment(demo_edit, alignment)
        DLL.SetEditBoxAlignment(preview_edit, alignment)
        refresh(note)

    def move_box(dx: int = 0, dy: int = 0, dw: int = 0) -> None:
        x, y, w, h = read_bounds()
        DLL.SetEditBoxBounds(demo_edit, x + dx, y + dy, w + dw, h)
        refresh(f"彩色编辑框位置/尺寸已更新: dx={dx}, dy={dy}, dw={dw}")

    def restore_box() -> None:
        x, y, w, h = initial["bounds"]
        DLL.SetEditBoxText(demo_edit, *s(str(initial["text"]))[:2])
        DLL.SetEditBoxText(preview_edit, *s(preview_initial)[:2])
        DLL.SetEditBoxColor(demo_edit, int(initial["fg"]), int(initial["bg"]))
        DLL.SetEditBoxBounds(demo_edit, int(x), int(y), int(w), int(h))
        DLL.SetEditBoxFont(demo_edit, *s("Segoe UI Emoji")[:2], 13, BOOL(False), BOOL(False), BOOL(False))
        DLL.SetEditBoxAlignment(demo_edit, base.ALIGN_LEFT)
        DLL.SetEditBoxAlignment(preview_edit, base.ALIGN_LEFT)
        DLL.EnableEditBox(demo_edit, BOOL(True))
        DLL.ShowEditBox(demo_edit, BOOL(True))
        refresh("彩色 Emoji 编辑框属性已恢复默认")

    register_theme_label(base.label(page, "📝 文本预设", 40, 326, 180, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    base.button(page, "😀", "表情混排", 40, 360, 156, 36, 0xFF409EFF, lambda: set_text_value("😀 Emoji / English / 数字 123 / ✅", "彩色编辑框文本已切到混排模式"))
    base.button(page, "🚀", "产品文案", 212, 360, 156, 36, 0xFF67C23A, lambda: set_text_value("🚀 EmojiWindow Pro / 支持 Unicode 彩色 emoji", "彩色编辑框文本已切到产品文案"))
    base.button(page, "🎨", "主题文案", 384, 360, 156, 36, 0xFF8E44AD, lambda: set_text_value("🎨 Light / Dark / Custom theme preview", "彩色编辑框文本已切到主题文案"))

    register_theme_label(base.label(page, "🎨 颜色 / 字体", 40, 414, 180, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    base.button(page, "🧊", "冷色", 40, 448, 118, 36, 0xFF409EFF, lambda: set_colors(THEME_PRIMARY, THEME_SURFACE_PRIMARY, "彩色编辑框已切到冷色方案"))
    base.button(page, "🧡", "暖色", 172, 448, 118, 36, 0xFFE6A23C, lambda: set_colors(THEME_WARNING, THEME_SURFACE_WARNING, "彩色编辑框已切到暖色方案"))
    base.button(page, "🔠", "16px Bold", 304, 448, 118, 36, 0xFF67C23A, lambda: set_font_value(16, True, "彩色编辑框字体已切到 16px Bold"))
    base.button(page, "🔡", "13px", 436, 448, 118, 36, 0xFF909399, lambda: set_font_value(13, False, "彩色编辑框字体已切回 13px"))

    register_theme_label(base.label(page, "📻 布局 / 状态", 1044, 222, 180, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    base.button(page, "➡️", "右移 80", 1044, 256, 116, 32, 0xFF409EFF, lambda: move_box(dx=80))
    base.button(page, "⬇️", "下移 20", 1172, 256, 116, 32, 0xFF67C23A, lambda: move_box(dy=20))
    base.button(page, "↔️", "加宽 120", 1300, 256, 124, 32, 0xFFE6A23C, lambda: move_box(dw=120))
    base.button(page, "🚫", "禁用/启用", 1044, 296, 116, 32, 0xFF8E44AD, lambda: (DLL.EnableEditBox(demo_edit, BOOL(not (int(DLL.GetEditBoxEnabled(demo_edit)) == 1))), refresh("彩色编辑框启用状态已切换")))
    base.button(page, "👁️", "显示/隐藏", 1172, 296, 116, 32, 0xFF909399, lambda: (DLL.ShowEditBox(demo_edit, BOOL(not (int(DLL.GetEditBoxVisible(demo_edit)) == 1))), refresh("彩色编辑框可见状态已切换")))
    base.button(page, "↺", "恢复默认", 1300, 296, 124, 32, 0xFF409EFF, restore_box)

    register_theme_label(base.label(page, "📐 对齐", 1044, 342, 180, 22, fg=text_color, bg=page_bg, size=15, bold=True), "text", "page")
    base.button(page, "L", "居左", 1044, 376, 116, 32, 0xFF909399, lambda: set_alignment_value(base.ALIGN_LEFT, "彩色编辑框已切到左对齐"))
    base.button(page, "C", "居中", 1172, 376, 116, 32, 0xFF409EFF, lambda: set_alignment_value(base.ALIGN_CENTER, "彩色编辑框已切到居中对齐"))
    base.button(page, "R", "居右", 1300, 376, 124, 32, 0xFFE6A23C, lambda: set_alignment_value(base.ALIGN_RIGHT, "彩色编辑框已切到右对齐"))
    register_theme_label(base.label(page, "ColorEmojiEditBox 和普通 EditBox 共用文本/颜色/位置/显示控制接口，这里现在直接展示多行彩色 emoji 渲染。", 1044, 424, 382, 86, fg=muted_color, bg=page_bg, wrap=True), "muted", "page")

    register_theme_label(base.label(page, "1. GetEditBoxText / SetEditBoxText：直接读取和写入彩色 emoji 文本。", 40, 598, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "2. GetEditBoxColor / SetEditBoxColor：读取和切换前景色 / 背景色。", 40, 632, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "3. GetEditBoxBounds / SetEditBoxBounds：直接调整位置与宽度。", 40, 666, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "4. GetEditBoxAlignment / SetEditBoxAlignment：切换左对齐 / 居中 / 右对齐。", 40, 700, 820, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "5. EnableEditBox / ShowEditBox：演示启用态和可见态切换。", 40, 734, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    refresh("彩色 Emoji 编辑框页已整理：支持多行彩色 emoji 渲染和对齐切换")


def build_page_checkbox(page: HWND) -> None:
    palette = page_palette()
    page_bg = palette["page_bg"]
    text_color = palette["text"]
    muted_color = palette["muted"]
    accent_color = palette["accent"]

    CHECKBOX_STYLE_DEFAULT = 0
    CHECKBOX_STYLE_FILL = 1
    CHECKBOX_STYLE_BUTTON = 2
    CHECKBOX_STYLE_CARD = 3

    base.groupbox(page, "☑️ CheckBox 样式演示", 16, 16, 980, 324)
    base.groupbox(page, "🧪 状态 / 样式 / 颜色", 1020, 16, 444, 324)
    base.groupbox(page, "📘 CheckBox API 说明", 16, 538, 1448, 220)

    register_theme_label(
        base.label(
            page,
            "这一页只保留 CheckBox，不再夹带 RadioButton / ProgressBar / Slider / Switch。",
            40,
            56,
            960,
            24,
            fg=muted_color,
            bg=page_bg,
        ),
        "muted",
        "page",
    )
    readout = register_theme_label(
        base.label(page, "等待读取复选框属性。", 40, 366, 1384, 108, fg=text_color, bg=page_bg, wrap=True),
        "text",
        "page",
    )
    state_text = register_theme_label(
        base.label(page, "复选框页状态将在这里更新。", 40, 490, 1360, 22, fg=accent_color, bg=page_bg),
        "accent",
        "page",
    )

    default_p, default_n, _ = s("☑️ 默认勾选")
    fill_p, fill_n, _ = s("🟧 Fill 样式")
    disabled_p, disabled_n, _ = s("🔒 禁用态展示")
    card_p, card_n, _ = s("🧱 Card 样式")
    button_p, button_n, _ = s("🔘 Button 样式")
    dynamic_p, dynamic_n, _ = s("🧪 动态样式")

    cb_default = DLL.CreateCheckBox(page, 56, 118, 250, 34, default_p, default_n, BOOL(True), THEME_TEXT, THEME_BG, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    cb_fill = DLL.CreateCheckBox(page, 56, 166, 250, 36, fill_p, fill_n, BOOL(False), THEME_TEXT, THEME_BG, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    cb_disabled = DLL.CreateCheckBox(page, 56, 214, 250, 34, disabled_p, disabled_n, BOOL(True), THEME_TEXT, THEME_BG, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    cb_card = DLL.CreateCheckBox(page, 360, 114, 260, 42, card_p, card_n, BOOL(False), THEME_TEXT, THEME_SURFACE, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    cb_button = DLL.CreateCheckBox(page, 360, 168, 260, 40, button_p, button_n, BOOL(True), THEME_TEXT, THEME_SURFACE, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    cb_dynamic = DLL.CreateCheckBox(page, 360, 222, 260, 40, dynamic_p, dynamic_n, BOOL(True), THEME_TEXT, THEME_BG, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))

    DLL.SetCheckBoxStyle(cb_fill, CHECKBOX_STYLE_FILL)
    DLL.SetCheckBoxStyle(cb_card, CHECKBOX_STYLE_CARD)
    DLL.SetCheckBoxStyle(cb_button, CHECKBOX_STYLE_BUTTON)
    DLL.SetCheckBoxCheckColor(cb_default, 0xFF409EFF)
    DLL.SetCheckBoxCheckColor(cb_fill, 0xFFE6A23C)
    DLL.SetCheckBoxCheckColor(cb_card, 0xFF67C23A)
    DLL.SetCheckBoxCheckColor(cb_button, 0xFF409EFF)
    DLL.SetCheckBoxCheckColor(cb_dynamic, 0xFF8E44AD)
    DLL.EnableCheckBox(cb_disabled, BOOL(False))

    checkbox_items: list[tuple[str, HWND]] = [
        ("default", cb_default),
        ("fill", cb_fill),
        ("disabled", cb_disabled),
        ("card", cb_card),
        ("button", cb_button),
        ("dynamic", cb_dynamic),
    ]
    card_bounds = {"x": 360, "y": 114, "w": 260, "h": 42}
    dynamic_text = {"alt": False}

    def read_utf8(fn, *args) -> str:
        size = int(fn(*args, None, 0))
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        fn(*args, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    def style_name(style: int) -> str:
        return {
            CHECKBOX_STYLE_DEFAULT: "default",
            CHECKBOX_STYLE_FILL: "fill",
            CHECKBOX_STYLE_BUTTON: "button",
            CHECKBOX_STYLE_CARD: "card",
        }.get(style, f"unknown({style})")

    def refresh(note: str = "已读取复选框状态") -> None:
        lines: list[str] = []
        for short_name, hwnd in checkbox_items:
            fg = UINT32()
            bg = UINT32()
            check_color = UINT32()
            DLL.GetCheckBoxColor(hwnd, ctypes.byref(fg), ctypes.byref(bg))
            DLL.GetCheckBoxCheckColor(hwnd, ctypes.byref(check_color))
            checked = int(bool(DLL.GetCheckBoxState(hwnd)))
            enabled = "启用" if bool(USER32.IsWindowEnabled(hwnd)) else "禁用"
            visible = "显示" if bool(USER32.IsWindowVisible(hwnd)) else "隐藏"
            text = read_utf8(DLL.GetCheckBoxText, hwnd)
            lines.append(
                f"{short_name}: checked={checked} style={style_name(int(DLL.GetCheckBoxStyle(hwnd)))} "
                f"{visible}/{enabled} text={text} fg=0x{int(fg.value):08X} bg=0x{int(bg.value):08X} check=0x{int(check_color.value):08X}"
            )
        base.set_label_text(readout, f"{note}\n" + "\n".join(lines))
        base.set_label_text(state_text, note)
        base.set_status(note)

    def toggle_box(hwnd: HWND, note: str) -> None:
        DLL.SetCheckBoxState(hwnd, BOOL(not bool(DLL.GetCheckBoxState(hwnd))))
        refresh(note)

    def toggle_disabled_demo() -> None:
        DLL.EnableCheckBox(cb_disabled, BOOL(not bool(USER32.IsWindowEnabled(cb_disabled))))
        refresh("禁用态复选框已切换启用状态")

    def toggle_card_visible() -> None:
        DLL.ShowCheckBox(cb_card, BOOL(not bool(USER32.IsWindowVisible(cb_card))))
        refresh("Card 样式复选框已切换显示状态")

    def set_dynamic_style(style: int, note: str) -> None:
        DLL.SetCheckBoxStyle(cb_dynamic, style)
        refresh(note)

    def set_dynamic_text() -> None:
        dynamic_text["alt"] = not bool(dynamic_text["alt"])
        text = "🧪 动态样式" if not bool(dynamic_text["alt"]) else "🧪 动态样式 / 文本已切换"
        DLL.SetCheckBoxText(cb_dynamic, *s(text)[:2])
        refresh("动态样式复选框文本已切换")

    def set_scheme(default_color: int, fill_color: int, card_color: int, button_color: int, dynamic_color: int, note: str) -> None:
        DLL.SetCheckBoxCheckColor(cb_default, default_color)
        DLL.SetCheckBoxCheckColor(cb_fill, fill_color)
        DLL.SetCheckBoxCheckColor(cb_card, card_color)
        DLL.SetCheckBoxCheckColor(cb_button, button_color)
        DLL.SetCheckBoxCheckColor(cb_dynamic, dynamic_color)
        refresh(note)

    def shift_card(dx: int) -> None:
        card_bounds["x"] += dx
        DLL.SetCheckBoxBounds(cb_card, card_bounds["x"], card_bounds["y"], card_bounds["w"], card_bounds["h"])
        refresh(f"Card 样式复选框位置已更新 dx={dx}")

    def restore() -> None:
        DLL.SetCheckBoxText(cb_default, *s("☑️ 默认勾选")[:2])
        DLL.SetCheckBoxText(cb_fill, *s("🟧 Fill 样式")[:2])
        DLL.SetCheckBoxText(cb_disabled, *s("🔒 禁用态展示")[:2])
        DLL.SetCheckBoxText(cb_card, *s("🧱 Card 样式")[:2])
        DLL.SetCheckBoxText(cb_button, *s("🔘 Button 样式")[:2])
        DLL.SetCheckBoxText(cb_dynamic, *s("🧪 动态样式")[:2])
        DLL.SetCheckBoxState(cb_default, BOOL(True))
        DLL.SetCheckBoxState(cb_fill, BOOL(False))
        DLL.SetCheckBoxState(cb_disabled, BOOL(True))
        DLL.SetCheckBoxState(cb_card, BOOL(False))
        DLL.SetCheckBoxState(cb_button, BOOL(True))
        DLL.SetCheckBoxState(cb_dynamic, BOOL(True))
        DLL.SetCheckBoxStyle(cb_fill, CHECKBOX_STYLE_FILL)
        DLL.SetCheckBoxStyle(cb_card, CHECKBOX_STYLE_CARD)
        DLL.SetCheckBoxStyle(cb_button, CHECKBOX_STYLE_BUTTON)
        DLL.SetCheckBoxStyle(cb_dynamic, CHECKBOX_STYLE_DEFAULT)
        DLL.SetCheckBoxColor(cb_default, THEME_TEXT, THEME_BG)
        DLL.SetCheckBoxColor(cb_fill, THEME_TEXT, THEME_BG)
        DLL.SetCheckBoxColor(cb_disabled, THEME_TEXT, THEME_BG)
        DLL.SetCheckBoxColor(cb_card, THEME_TEXT, THEME_SURFACE)
        DLL.SetCheckBoxColor(cb_button, THEME_TEXT, THEME_SURFACE)
        DLL.SetCheckBoxColor(cb_dynamic, THEME_TEXT, THEME_BG)
        DLL.ShowCheckBox(cb_card, BOOL(True))
        DLL.EnableCheckBox(cb_disabled, BOOL(False))
        card_bounds["x"] = 360
        DLL.SetCheckBoxBounds(cb_card, card_bounds["x"], card_bounds["y"], card_bounds["w"], card_bounds["h"])
        dynamic_text["alt"] = False
        set_scheme(0xFF409EFF, 0xFFE6A23C, 0xFF67C23A, 0xFF409EFF, 0xFF8E44AD, "复选框页已恢复默认")

    cb_cb = DLL._CheckBoxCB(lambda h, checked: refresh(f"CheckBox 回调: hwnd=0x{base.hwnd_key(h):X} checked={int(bool(checked))}"))
    KEEP.append(cb_cb)
    for _, checkbox_hwnd in checkbox_items:
        DLL.SetCheckBoxCallback(checkbox_hwnd, cb_cb)

    register_theme_label(base.label(page, "左侧展示默认 / Fill / Card / Button / 禁用态，并保留一个可动态切换样式的 CheckBox。", 40, 288, 900, 24, fg=muted_color, bg=page_bg), "muted", "page")

    base.button(page, "↺", "切换默认", 1044, 94, 116, 34, 0xFF409EFF, lambda: toggle_box(cb_default, "默认复选框已切换勾选状态"))
    base.button(page, "↺", "切换 Fill", 1172, 94, 116, 34, 0xFFE6A23C, lambda: toggle_box(cb_fill, "Fill 样式复选框已切换勾选状态"))
    base.button(page, "↺", "切换 Card", 1300, 94, 124, 34, 0xFF67C23A, lambda: toggle_box(cb_card, "Card 样式复选框已切换勾选状态"))
    base.button(page, "↺", "切换 Button", 1044, 138, 116, 34, 0xFF8E44AD, lambda: toggle_box(cb_button, "Button 样式复选框已切换勾选状态"))
    base.button(page, "🔒", "禁用/启用", 1172, 138, 116, 34, 0xFF909399, toggle_disabled_demo)
    base.button(page, "👁", "显示/隐藏", 1300, 138, 124, 34, 0xFF409EFF, toggle_card_visible)
    base.button(page, "A", "默认样式", 1044, 182, 116, 34, 0xFF909399, lambda: set_dynamic_style(CHECKBOX_STYLE_DEFAULT, "动态复选框已切到 default 样式"))
    base.button(page, "F", "Fill 样式", 1172, 182, 116, 34, 0xFFE6A23C, lambda: set_dynamic_style(CHECKBOX_STYLE_FILL, "动态复选框已切到 fill 样式"))
    base.button(page, "C", "Card 样式", 1300, 182, 124, 34, 0xFF67C23A, lambda: set_dynamic_style(CHECKBOX_STYLE_CARD, "动态复选框已切到 card 样式"))
    base.button(page, "B", "Button 样式", 1044, 226, 116, 34, 0xFF409EFF, lambda: set_dynamic_style(CHECKBOX_STYLE_BUTTON, "动态复选框已切到 button 样式"))
    base.button(page, "✏", "切换文本", 1172, 226, 116, 34, 0xFF8E44AD, set_dynamic_text)
    base.button(page, "↔", "右移 Card", 1300, 226, 124, 34, 0xFF909399, lambda: shift_card(60))
    base.button(page, "💙", "蓝色方案", 1044, 270, 116, 34, 0xFF409EFF, lambda: set_scheme(0xFF409EFF, 0xFFE6A23C, 0xFF67C23A, 0xFF409EFF, 0xFF8E44AD, "复选框已切到蓝绿配色方案"))
    base.button(page, "💚", "绿色方案", 1172, 270, 116, 34, 0xFF67C23A, lambda: set_scheme(0xFF67C23A, 0xFF85CE61, 0xFF13CE66, 0xFF67C23A, 0xFF2EC4B6, "复选框已切到绿色配色方案"))
    base.button(page, "↺", "恢复默认", 1300, 270, 124, 34, 0xFF409EFF, restore)

    register_theme_label(base.label(page, "1. GetCheckBoxState / SetCheckBoxState：读取和切换勾选状态。", 40, 582, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "2. GetCheckBoxStyle / SetCheckBoxStyle：直接切换 default / fill / card / button。", 40, 616, 920, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "3. GetCheckBoxColor / SetCheckBoxColor / SetCheckBoxCheckColor：读取文本 / 背景 / 勾选色。", 40, 650, 980, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "4. SetCheckBoxText / GetCheckBoxText：动态切换复选框文案。", 40, 684, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "5. EnableCheckBox / ShowCheckBox / SetCheckBoxBounds：演示启用态、显示态和位置更新。", 40, 718, 1040, 24, fg=text_color, bg=page_bg), "text", "page")
    refresh("复选框页已整理：只保留 CheckBox，并补上样式 / 颜色 / 状态控制")


def build_page_radiobutton(page: HWND) -> None:
    palette = page_palette()
    page_bg = palette["page_bg"]
    text_color = palette["text"]
    muted_color = palette["muted"]
    accent_color = palette["accent"]

    base.groupbox(page, "🔘 RadioButton 样式演示", 16, 16, 980, 324)
    base.groupbox(page, "🧪 状态 / 样式 / 分组", 1020, 16, 444, 324)
    base.groupbox(page, "📘 RadioButton API 说明", 16, 538, 1448, 220)

    register_theme_label(
        base.label(
            page,
            "这一页只保留 RadioButton，不再混入 CheckBox 和右侧的 ProgressBar / Slider / Switch。",
            40,
            56,
            980,
            24,
            fg=muted_color,
            bg=page_bg,
        ),
        "muted",
        "page",
    )
    readout = register_theme_label(
        base.label(page, "等待读取单选框属性。", 40, 366, 1384, 108, fg=text_color, bg=page_bg, wrap=True),
        "text",
        "page",
    )
    state_text = register_theme_label(
        base.label(page, "单选框页状态将在这里更新。", 40, 490, 1360, 22, fg=accent_color, bg=page_bg),
        "accent",
        "page",
    )

    default_p, default_n, _ = s("🔘 默认样式")
    border_p, border_n, _ = s("🧱 Border 样式")
    button_p, button_n, _ = s("🟦 Button 样式")
    disabled_p, disabled_n, _ = s("🔒 禁用态")
    dynamic_p, dynamic_n, _ = s("🧪 动态样式")

    rb_default = DLL.CreateRadioButton(page, 56, 118, 250, 34, default_p, default_n, 301, BOOL(True), THEME_TEXT, THEME_BG, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    rb_border = DLL.CreateRadioButton(page, 56, 166, 250, 36, border_p, border_n, 301, BOOL(False), THEME_TEXT, THEME_BG, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    rb_button = DLL.CreateRadioButton(page, 56, 214, 250, 38, button_p, button_n, 301, BOOL(False), THEME_TEXT, THEME_SURFACE, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    rb_disabled = DLL.CreateRadioButton(page, 360, 118, 260, 34, disabled_p, disabled_n, 302, BOOL(True), THEME_TEXT, THEME_BG, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    rb_dynamic = DLL.CreateRadioButton(page, 360, 170, 260, 38, dynamic_p, dynamic_n, 302, BOOL(False), THEME_TEXT, THEME_BG, base.FONT_PTR, base.FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))

    DLL.SetRadioButtonStyle(rb_border, base.RADIO_STYLE_BORDER)
    DLL.SetRadioButtonStyle(rb_button, base.RADIO_STYLE_BUTTON)
    DLL.SetRadioButtonStyle(rb_dynamic, base.RADIO_STYLE_BORDER)
    DLL.SetRadioButtonDotColor(rb_default, 0xFF409EFF)
    DLL.SetRadioButtonDotColor(rb_border, 0xFFE6A23C)
    DLL.SetRadioButtonDotColor(rb_button, 0xFF67C23A)
    DLL.SetRadioButtonDotColor(rb_disabled, 0xFF909399)
    DLL.SetRadioButtonDotColor(rb_dynamic, 0xFF8E44AD)
    DLL.EnableRadioButton(rb_disabled, BOOL(False))

    radio_items: list[tuple[str, HWND, int]] = [
        ("default", rb_default, 301),
        ("border", rb_border, 301),
        ("button", rb_button, 301),
        ("disabled", rb_disabled, 302),
        ("dynamic", rb_dynamic, 302),
    ]
    dynamic_bounds = {"x": 360, "y": 170, "w": 260, "h": 38}
    dynamic_text = {"alt": False}

    def read_utf8_radio(h_radio: HWND) -> str:
        size = int(DLL.GetRadioButtonText(h_radio, None, 0))
        if size <= 0:
            return ""
        buf = ctypes.create_string_buffer(size)
        DLL.GetRadioButtonText(h_radio, buf, size)
        return buf.raw[:size].decode("utf-8", errors="replace")

    def style_name(style: int) -> str:
        return {
            base.RADIO_STYLE_DEFAULT: "default",
            base.RADIO_STYLE_BORDER: "border",
            base.RADIO_STYLE_BUTTON: "button",
        }.get(style, f"unknown({style})")

    def refresh(note: str = "已读取单选框状态") -> None:
        lines: list[str] = []
        for short_name, hwnd, group_id in radio_items:
            fg = UINT32()
            bg = UINT32()
            dot = UINT32()
            DLL.GetRadioButtonColor(hwnd, ctypes.byref(fg), ctypes.byref(bg))
            DLL.GetRadioButtonDotColor(hwnd, ctypes.byref(dot))
            checked = int(bool(DLL.GetRadioButtonState(hwnd)))
            enabled = "启用" if bool(USER32.IsWindowEnabled(hwnd)) else "禁用"
            visible = "显示" if bool(USER32.IsWindowVisible(hwnd)) else "隐藏"
            lines.append(
                f"{short_name}: checked={checked} group={group_id} style={style_name(int(DLL.GetRadioButtonStyle(hwnd)))} "
                f"{visible}/{enabled} text={read_utf8_radio(hwnd)} fg=0x{int(fg.value):08X} bg=0x{int(bg.value):08X} dot=0x{int(dot.value):08X}"
            )
        base.set_label_text(readout, f"{note}\n" + "\n".join(lines))
        base.set_label_text(state_text, note)
        base.set_status(note)

    def select_radio(hwnd: HWND, note: str) -> None:
        DLL.SetRadioButtonState(hwnd, BOOL(True))
        refresh(note)

    def toggle_disabled_demo() -> None:
        DLL.EnableRadioButton(rb_disabled, BOOL(not bool(USER32.IsWindowEnabled(rb_disabled))))
        refresh("禁用态单选框已切换启用状态")

    def toggle_dynamic_visible() -> None:
        DLL.ShowRadioButton(rb_dynamic, BOOL(not bool(USER32.IsWindowVisible(rb_dynamic))))
        refresh("动态单选框已切换显示状态")

    def set_dynamic_style(style: int, note: str) -> None:
        DLL.SetRadioButtonStyle(rb_dynamic, style)
        refresh(note)

    def set_dynamic_text() -> None:
        dynamic_text["alt"] = not bool(dynamic_text["alt"])
        text = "🧪 动态样式" if not bool(dynamic_text["alt"]) else "🧪 动态样式 / 文本已切换"
        DLL.SetRadioButtonText(rb_dynamic, *s(text)[:2])
        refresh("动态单选框文本已切换")

    def shift_dynamic(dx: int) -> None:
        dynamic_bounds["x"] += dx
        DLL.SetRadioButtonBounds(rb_dynamic, dynamic_bounds["x"], dynamic_bounds["y"], dynamic_bounds["w"], dynamic_bounds["h"])
        refresh(f"动态单选框位置已更新 dx={dx}")

    def set_scheme(default_color: int, border_color: int, button_color: int, disabled_color: int, dynamic_color: int, note: str) -> None:
        DLL.SetRadioButtonDotColor(rb_default, default_color)
        DLL.SetRadioButtonDotColor(rb_border, border_color)
        DLL.SetRadioButtonDotColor(rb_button, button_color)
        DLL.SetRadioButtonDotColor(rb_disabled, disabled_color)
        DLL.SetRadioButtonDotColor(rb_dynamic, dynamic_color)
        refresh(note)

    def restore() -> None:
        DLL.SetRadioButtonText(rb_default, *s("🔘 默认样式")[:2])
        DLL.SetRadioButtonText(rb_border, *s("🧱 Border 样式")[:2])
        DLL.SetRadioButtonText(rb_button, *s("🟦 Button 样式")[:2])
        DLL.SetRadioButtonText(rb_disabled, *s("🔒 禁用态")[:2])
        DLL.SetRadioButtonText(rb_dynamic, *s("🧪 动态样式")[:2])
        DLL.SetRadioButtonState(rb_default, BOOL(True))
        DLL.SetRadioButtonState(rb_disabled, BOOL(True))
        DLL.SetRadioButtonStyle(rb_default, base.RADIO_STYLE_DEFAULT)
        DLL.SetRadioButtonStyle(rb_border, base.RADIO_STYLE_BORDER)
        DLL.SetRadioButtonStyle(rb_button, base.RADIO_STYLE_BUTTON)
        DLL.SetRadioButtonStyle(rb_dynamic, base.RADIO_STYLE_BORDER)
        DLL.SetRadioButtonColor(rb_default, THEME_TEXT, THEME_BG)
        DLL.SetRadioButtonColor(rb_border, THEME_TEXT, THEME_BG)
        DLL.SetRadioButtonColor(rb_button, THEME_TEXT, THEME_SURFACE)
        DLL.SetRadioButtonColor(rb_disabled, THEME_TEXT, THEME_BG)
        DLL.SetRadioButtonColor(rb_dynamic, THEME_TEXT, THEME_BG)
        DLL.EnableRadioButton(rb_disabled, BOOL(False))
        DLL.ShowRadioButton(rb_dynamic, BOOL(True))
        dynamic_bounds["x"] = 360
        DLL.SetRadioButtonBounds(rb_dynamic, dynamic_bounds["x"], dynamic_bounds["y"], dynamic_bounds["w"], dynamic_bounds["h"])
        dynamic_text["alt"] = False
        set_scheme(0xFF409EFF, 0xFFE6A23C, 0xFF67C23A, 0xFF909399, 0xFF8E44AD, "单选框页已恢复默认")

    rb_cb = DLL._RadioCB(lambda h, gid, checked: refresh(f"RadioButton 回调: hwnd=0x{base.hwnd_key(h):X} group={gid} checked={int(bool(checked))}"))
    KEEP.append(rb_cb)
    for _, radio_hwnd, _ in radio_items:
        DLL.SetRadioButtonCallback(radio_hwnd, rb_cb)

    register_theme_label(base.label(page, "左侧展示 default / border / button 三种主样式，并补充禁用态和一个可动态切换样式的单选框。", 40, 288, 960, 24, fg=muted_color, bg=page_bg), "muted", "page")

    base.button(page, "①", "选中默认", 1044, 94, 116, 34, 0xFF409EFF, lambda: select_radio(rb_default, "默认样式单选框已设为选中"))
    base.button(page, "②", "选中 Border", 1172, 94, 116, 34, 0xFFE6A23C, lambda: select_radio(rb_border, "Border 样式单选框已设为选中"))
    base.button(page, "③", "选中 Button", 1300, 94, 124, 34, 0xFF67C23A, lambda: select_radio(rb_button, "Button 样式单选框已设为选中"))
    base.button(page, "④", "选中动态", 1044, 138, 116, 34, 0xFF8E44AD, lambda: select_radio(rb_dynamic, "动态样式单选框已设为选中"))
    base.button(page, "🔒", "禁用/启用", 1172, 138, 116, 34, 0xFF909399, toggle_disabled_demo)
    base.button(page, "👁", "显示/隐藏", 1300, 138, 124, 34, 0xFF409EFF, toggle_dynamic_visible)
    base.button(page, "A", "默认样式", 1044, 182, 116, 34, 0xFF909399, lambda: set_dynamic_style(base.RADIO_STYLE_DEFAULT, "动态单选框已切到 default 样式"))
    base.button(page, "B", "Border 样式", 1172, 182, 116, 34, 0xFFE6A23C, lambda: set_dynamic_style(base.RADIO_STYLE_BORDER, "动态单选框已切到 border 样式"))
    base.button(page, "C", "Button 样式", 1300, 182, 124, 34, 0xFF67C23A, lambda: set_dynamic_style(base.RADIO_STYLE_BUTTON, "动态单选框已切到 button 样式"))
    base.button(page, "✏", "切换文本", 1044, 226, 116, 34, 0xFF8E44AD, set_dynamic_text)
    base.button(page, "↔", "右移 60", 1172, 226, 116, 34, 0xFF909399, lambda: shift_dynamic(60))
    base.button(page, "↺", "恢复默认", 1300, 226, 124, 34, 0xFF409EFF, restore)
    base.button(page, "💙", "蓝绿方案", 1044, 270, 116, 34, 0xFF409EFF, lambda: set_scheme(0xFF409EFF, 0xFFE6A23C, 0xFF67C23A, 0xFF909399, 0xFF8E44AD, "单选框已切到蓝绿配色方案"))
    base.button(page, "🟠", "暖色方案", 1172, 270, 116, 34, 0xFFE6A23C, lambda: set_scheme(0xFFE6A23C, 0xFFF56C6C, 0xFFE6A23C, 0xFF909399, 0xFFF56C6C, "单选框已切到暖色配色方案"))

    register_theme_label(base.label(page, "1. GetRadioButtonState / SetRadioButtonState：读取与切换当前组内选中项。", 40, 582, 840, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "2. GetRadioButtonStyle / SetRadioButtonStyle：直接切换 default / border / button。", 40, 616, 900, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "3. GetRadioButtonColor / SetRadioButtonColor / SetRadioButtonDotColor：读取文本 / 背景 / 圆点色。", 40, 650, 1060, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "4. GetRadioButtonText / SetRadioButtonText：动态切换单选框文案。", 40, 684, 820, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "5. EnableRadioButton / ShowRadioButton / SetRadioButtonBounds：演示启用态、显示态和位置更新。", 40, 718, 1100, 24, fg=text_color, bg=page_bg), "text", "page")
    refresh("单选框页已整理：只保留 RadioButton，并补上样式 / 分组 / 状态控制")


def build_page_progressbar(page: HWND) -> None:
    palette = page_palette()
    page_bg = palette["page_bg"]
    text_color = palette["text"]
    muted_color = palette["muted"]
    accent_color = palette["accent"]

    base.groupbox(page, "📊 ProgressBar 样式演示", 16, 16, 980, 324)
    base.groupbox(page, "🧪 数值 / 颜色 / 布局", 1020, 16, 444, 324)
    base.groupbox(page, "📘 ProgressBar API 说明", 16, 538, 1448, 220)

    register_theme_label(
        base.label(
            page,
            "这一页只保留 ProgressBar，不再混入 CheckBox / RadioButton / Slider / Switch。",
            40,
            56,
            960,
            24,
            fg=muted_color,
            bg=page_bg,
        ),
        "muted",
        "page",
    )
    readout = register_theme_label(
        base.label(page, "等待读取进度条属性。", 40, 366, 1384, 108, fg=text_color, bg=page_bg, wrap=True),
        "text",
        "page",
    )
    state_text = register_theme_label(
        base.label(page, "进度条页状态将在这里更新。", 40, 490, 1360, 22, fg=accent_color, bg=page_bg),
        "accent",
        "page",
    )

    prog_main = DLL.CreateProgressBar(page, 56, 122, 560, 28, 35, THEME_PRIMARY, THEME_BORDER_LIGHT, BOOL(True), THEME_TEXT)
    prog_success = DLL.CreateProgressBar(page, 56, 176, 560, 24, 62, THEME_SUCCESS, THEME_SURFACE, BOOL(True), THEME_TEXT)
    prog_warning = DLL.CreateProgressBar(page, 56, 226, 560, 20, 78, THEME_WARNING, THEME_SURFACE_WARNING, BOOL(False), THEME_TEXT)
    prog_ind = DLL.CreateProgressBar(page, 56, 270, 560, 18, 50, THEME_INFO, THEME_SURFACE_INFO, BOOL(False), THEME_TEXT)
    DLL.SetProgressIndeterminate(prog_ind, BOOL(True))

    progress_items: list[tuple[str, HWND]] = [
        ("main", prog_main),
        ("success", prog_success),
        ("warning", prog_warning),
        ("indeterminate", prog_ind),
    ]
    progress_meta: dict[str, dict[str, object]] = {
        "main": {"show_text": True, "indeterminate": False},
        "success": {"show_text": True, "indeterminate": False},
        "warning": {"show_text": False, "indeterminate": False},
        "indeterminate": {"show_text": False, "indeterminate": True},
    }
    main_bounds = {"x": 56, "y": 122, "w": 560, "h": 28}

    def read_bounds(hwnd: HWND) -> tuple[int, int, int, int]:
        x = ctypes.c_int()
        y = ctypes.c_int()
        w = ctypes.c_int()
        h = ctypes.c_int()
        DLL.GetProgressBarBounds(hwnd, ctypes.byref(x), ctypes.byref(y), ctypes.byref(w), ctypes.byref(h))
        return int(x.value), int(y.value), int(w.value), int(h.value)

    def refresh(note: str = "已读取进度条状态") -> None:
        lines: list[str] = []
        for short_name, hwnd in progress_items:
            fg = UINT32()
            bg = UINT32()
            DLL.GetProgressBarColor(hwnd, ctypes.byref(fg), ctypes.byref(bg))
            x, y, w, h = read_bounds(hwnd)
            value = int(DLL.GetProgressValue(hwnd))
            enabled = "启用" if int(DLL.GetProgressBarEnabled(hwnd)) == 1 else "禁用"
            visible = "显示" if int(DLL.GetProgressBarVisible(hwnd)) == 1 else "隐藏"
            show_text = bool(progress_meta[short_name]["show_text"])
            indeterminate = bool(progress_meta[short_name]["indeterminate"])
            lines.append(
                f"{short_name}: value={value} bounds=({x}, {y}, {w}, {h}) "
                f"{visible}/{enabled} show_text={int(show_text)} indeterminate={int(indeterminate)} "
                f"fg=0x{int(fg.value):08X} bg=0x{int(bg.value):08X}"
            )
        base.set_label_text(readout, f"{note}\n" + "\n".join(lines))
        base.set_label_text(state_text, note)
        base.set_status(note)

    def set_main_value(value: int, note: str) -> None:
        DLL.SetProgressValue(prog_main, value)
        refresh(note)

    def set_palette(note: str, main_fg: int, main_bg: int, success_fg: int, success_bg: int, warning_fg: int, warning_bg: int, ind_fg: int, ind_bg: int) -> None:
        DLL.SetProgressBarColor(prog_main, main_fg, main_bg)
        DLL.SetProgressBarColor(prog_success, success_fg, success_bg)
        DLL.SetProgressBarColor(prog_warning, warning_fg, warning_bg)
        DLL.SetProgressBarColor(prog_ind, ind_fg, ind_bg)
        refresh(note)

    def toggle_show_text(hwnd: HWND, key: str, note: str) -> None:
        next_value = not bool(progress_meta[key]["show_text"])
        progress_meta[key]["show_text"] = next_value
        DLL.SetProgressBarShowText(hwnd, BOOL(next_value))
        refresh(note)

    def toggle_indeterminate() -> None:
        next_value = not bool(progress_meta["indeterminate"]["indeterminate"])
        progress_meta["indeterminate"]["indeterminate"] = next_value
        DLL.SetProgressIndeterminate(prog_ind, BOOL(next_value))
        refresh("不确定进度条已切换动画状态")

    def toggle_main_enabled() -> None:
        DLL.EnableProgressBar(prog_main, BOOL(not (int(DLL.GetProgressBarEnabled(prog_main)) == 1)))
        refresh("主进度条已切换启用状态")

    def toggle_warning_visible() -> None:
        DLL.ShowProgressBar(prog_warning, BOOL(not (int(DLL.GetProgressBarVisible(prog_warning)) == 1)))
        refresh("Warning 进度条已切换显示状态")

    def widen_main(dw: int) -> None:
        main_bounds["w"] += dw
        DLL.SetProgressBarBounds(prog_main, main_bounds["x"], main_bounds["y"], main_bounds["w"], main_bounds["h"])
        refresh(f"主进度条宽度已更新 dw={dw}")

    def restore() -> None:
        main_bounds["x"] = 56
        main_bounds["y"] = 122
        main_bounds["w"] = 560
        main_bounds["h"] = 28
        DLL.SetProgressBarBounds(prog_main, main_bounds["x"], main_bounds["y"], main_bounds["w"], main_bounds["h"])
        DLL.SetProgressValue(prog_main, 35)
        DLL.SetProgressValue(prog_success, 62)
        DLL.SetProgressValue(prog_warning, 78)
        DLL.SetProgressValue(prog_ind, 50)
        DLL.EnableProgressBar(prog_main, BOOL(True))
        DLL.ShowProgressBar(prog_warning, BOOL(True))
        progress_meta["main"]["show_text"] = True
        progress_meta["success"]["show_text"] = True
        progress_meta["warning"]["show_text"] = False
        progress_meta["indeterminate"]["show_text"] = False
        progress_meta["indeterminate"]["indeterminate"] = True
        DLL.SetProgressBarShowText(prog_main, BOOL(True))
        DLL.SetProgressBarShowText(prog_success, BOOL(True))
        DLL.SetProgressBarShowText(prog_warning, BOOL(False))
        DLL.SetProgressBarShowText(prog_ind, BOOL(False))
        DLL.SetProgressIndeterminate(prog_ind, BOOL(True))
        DLL.SetProgressBarTextColor(prog_main, THEME_TEXT)
        DLL.SetProgressBarTextColor(prog_success, THEME_TEXT)
        DLL.SetProgressBarTextColor(prog_warning, THEME_TEXT)
        DLL.SetProgressBarTextColor(prog_ind, THEME_TEXT)
        set_palette(
            "进度条页已恢复默认",
            THEME_PRIMARY,
            THEME_BORDER_LIGHT,
            THEME_SUCCESS,
            THEME_SURFACE,
            THEME_WARNING,
            THEME_SURFACE_WARNING,
            THEME_INFO,
            THEME_SURFACE_INFO,
        )

    pb_cb = DLL._ProgressCB(lambda h, value: refresh(f"ProgressBar 回调: hwnd=0x{base.hwnd_key(h):X} value={value}"))
    KEEP.append(pb_cb)
    for _, progress_hwnd in progress_items:
        DLL.SetProgressBarCallback(progress_hwnd, pb_cb)

    register_theme_label(base.label(page, "左侧展示常规、成功、警告和不确定四种 ProgressBar，用于直接验证数值、文字和颜色切换。", 40, 310, 930, 24, fg=muted_color, bg=page_bg), "muted", "page")

    base.button(page, "0%", "设为 0", 1044, 94, 116, 34, 0xFF909399, lambda: set_main_value(0, "主进度条已设为 0%"))
    base.button(page, "35%", "设为 35", 1172, 94, 116, 34, 0xFF409EFF, lambda: set_main_value(35, "主进度条已设为 35%"))
    base.button(page, "75%", "设为 75", 1300, 94, 124, 34, 0xFF67C23A, lambda: set_main_value(75, "主进度条已设为 75%"))
    base.button(page, "100%", "设为 100", 1044, 138, 116, 34, 0xFFE6A23C, lambda: set_main_value(100, "主进度条已设为 100%"))
    base.button(page, "📝", "主条文字", 1172, 138, 116, 34, 0xFF8E44AD, lambda: toggle_show_text(prog_main, "main", "主进度条已切换百分比文本"))
    base.button(page, "📝", "警告文字", 1300, 138, 124, 34, 0xFF409EFF, lambda: toggle_show_text(prog_warning, "warning", "Warning 进度条已切换百分比文本"))
    base.button(page, "🎬", "切动画", 1044, 182, 116, 34, 0xFF67C23A, toggle_indeterminate)
    base.button(page, "🔒", "禁用/启用", 1172, 182, 116, 34, 0xFF909399, toggle_main_enabled)
    base.button(page, "👁", "显示/隐藏", 1300, 182, 124, 34, 0xFF409EFF, toggle_warning_visible)
    base.button(page, "↔", "加宽 120", 1044, 226, 116, 34, 0xFFE6A23C, lambda: widen_main(120))
    base.button(page, "💙", "蓝色方案", 1172, 226, 116, 34, 0xFF409EFF, lambda: set_palette("进度条已切到蓝色方案", THEME_PRIMARY, THEME_SURFACE, THEME_SUCCESS, THEME_SURFACE_SUCCESS, THEME_WARNING, THEME_SURFACE_WARNING, THEME_INFO, THEME_SURFACE_INFO))
    base.button(page, "🔥", "暖色方案", 1300, 226, 124, 34, 0xFFE6A23C, lambda: set_palette("进度条已切到暖色方案", THEME_WARNING, THEME_SURFACE_WARNING, THEME_DANGER, THEME_SURFACE_DANGER, THEME_WARNING, THEME_SURFACE_WARNING, THEME_DANGER, THEME_SURFACE_DANGER))
    base.button(page, "↺", "恢复默认", 1044, 270, 116, 34, 0xFF409EFF, restore)

    register_theme_label(base.label(page, "1. GetProgressValue / SetProgressValue：读取和设置当前进度值。", 40, 582, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "2. SetProgressBarColor / GetProgressBarColor：切换前景色 / 背景色。", 40, 616, 820, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "3. SetProgressBarShowText / GetProgressBarShowText：控制百分比文本显示。", 40, 650, 930, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "4. SetProgressIndeterminate：切换不确定进度动画。", 40, 684, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "5. EnableProgressBar / ShowProgressBar / SetProgressBarBounds：演示启用态、可见态和尺寸更新。", 40, 718, 1120, 24, fg=text_color, bg=page_bg), "text", "page")
    refresh("进度条页已整理：只保留 ProgressBar，并补上数值 / 颜色 / 显示控制")


def build_page_slider(page: HWND) -> None:
    palette = page_palette()
    page_bg = palette["page_bg"]
    text_color = palette["text"]
    muted_color = palette["muted"]
    accent_color = palette["accent"]
    slider_surface = THEME_SURFACE

    base.groupbox(page, "🎚️ Slider 样式演示", 16, 16, 980, 324)
    base.groupbox(page, "🧪 数值 / 范围 / 颜色", 1020, 16, 444, 324)
    base.groupbox(page, "📘 Slider API 说明", 16, 538, 1448, 220)

    register_theme_label(
        base.label(
            page,
            "这一页只保留 Slider，不再混入 CheckBox / RadioButton / ProgressBar / Switch。",
            40,
            56,
            960,
            24,
            fg=muted_color,
            bg=page_bg,
        ),
        "muted",
        "page",
    )
    readout = register_theme_label(
        base.label(page, "等待读取滑块属性。", 40, 366, 1384, 108, fg=text_color, bg=page_bg, wrap=True),
        "text",
        "page",
    )
    state_text = register_theme_label(
        base.label(page, "滑块页状态将在这里更新。", 40, 490, 1360, 22, fg=accent_color, bg=page_bg),
        "accent",
        "page",
    )

    register_theme_label(base.label(page, "主滑块", 56, 108, 120, 20, fg=text_color, bg=page_bg, size=14, bold=True), "text", "page")
    slider_main = DLL.CreateSlider(page, 56, 128, 560, 40, 0, 100, 36, 10, THEME_PRIMARY, slider_surface)
    DLL.SetSliderShowStops(slider_main, BOOL(True))
    register_theme_label(base.label(page, "细步长", 56, 176, 120, 20, fg=text_color, bg=page_bg, size=14, bold=True), "text", "page")
    slider_fine = DLL.CreateSlider(page, 56, 196, 560, 40, 0, 100, 24, 1, THEME_SUCCESS, slider_surface)
    DLL.SetSliderShowStops(slider_fine, BOOL(False))
    register_theme_label(base.label(page, "大范围", 56, 244, 120, 20, fg=text_color, bg=page_bg, size=14, bold=True), "text", "page")
    slider_wide = DLL.CreateSlider(page, 56, 264, 560, 40, 0, 200, 120, 20, THEME_WARNING, slider_surface)
    DLL.SetSliderShowStops(slider_wide, BOOL(True))
    register_theme_label(base.label(page, "禁用态", 650, 108, 120, 20, fg=text_color, bg=page_bg, size=14, bold=True), "text", "page")
    slider_disabled = DLL.CreateSlider(page, 650, 128, 260, 40, 0, 100, 60, 10, THEME_MUTED, slider_surface)
    DLL.SetSliderShowStops(slider_disabled, BOOL(True))
    DLL.EnableSlider(slider_disabled, BOOL(False))

    slider_items: list[tuple[str, HWND]] = [
        ("main", slider_main),
        ("fine", slider_fine),
        ("wide", slider_wide),
        ("disabled", slider_disabled),
    ]
    slider_meta: dict[str, dict[str, object]] = {
        "main": {"min": 0, "max": 100, "step": 10, "show_stops": True},
        "fine": {"min": 0, "max": 100, "step": 1, "show_stops": False},
        "wide": {"min": 0, "max": 200, "step": 20, "show_stops": True},
        "disabled": {"min": 0, "max": 100, "step": 10, "show_stops": True},
    }
    main_bounds = {"x": 56, "y": 128, "w": 560, "h": 40}

    def refresh(note: str = "已读取滑块状态") -> None:
        lines: list[str] = []
        for short_name, hwnd in slider_items:
            active = UINT32()
            bg = UINT32()
            button = UINT32()
            DLL.GetSliderColors(hwnd, ctypes.byref(active), ctypes.byref(bg), ctypes.byref(button))
            value = int(DLL.GetSliderValue(hwnd))
            enabled = "启用" if bool(USER32.IsWindowEnabled(hwnd)) else "禁用"
            visible = "显示" if bool(USER32.IsWindowVisible(hwnd)) else "隐藏"
            meta = slider_meta[short_name]
            lines.append(
                f"{short_name}: value={value} range=[{meta['min']}, {meta['max']}] step={meta['step']} "
                f"show_stops={int(bool(meta['show_stops']))} {visible}/{enabled} "
                f"active=0x{int(active.value):08X} bg=0x{int(bg.value):08X} thumb=0x{int(button.value):08X}"
            )
        base.set_label_text(readout, f"{note}\n" + "\n".join(lines))
        base.set_label_text(state_text, note)
        base.set_status(note)

    def set_main_value(value: int, note: str) -> None:
        DLL.SetSliderValue(slider_main, value)
        refresh(note)

    def set_wide_value(value: int, note: str) -> None:
        DLL.SetSliderValue(slider_wide, value)
        refresh(note)

    def set_main_range(min_value: int, max_value: int, step: int, note: str) -> None:
        slider_meta["main"]["min"] = min_value
        slider_meta["main"]["max"] = max_value
        slider_meta["main"]["step"] = step
        DLL.SetSliderRange(slider_main, min_value, max_value)
        DLL.SetSliderStep(slider_main, step)
        current = int(DLL.GetSliderValue(slider_main))
        DLL.SetSliderValue(slider_main, max(min_value, min(max_value, current)))
        refresh(note)

    def toggle_main_stops() -> None:
        next_value = not bool(slider_meta["main"]["show_stops"])
        slider_meta["main"]["show_stops"] = next_value
        DLL.SetSliderShowStops(slider_main, BOOL(next_value))
        refresh("主滑块已切换停靠点显示")

    def toggle_disabled_slider() -> None:
        DLL.EnableSlider(slider_disabled, BOOL(not bool(USER32.IsWindowEnabled(slider_disabled))))
        refresh("禁用态滑块已切换启用状态")

    def toggle_wide_visible() -> None:
        DLL.ShowSlider(slider_wide, BOOL(not bool(USER32.IsWindowVisible(slider_wide))))
        refresh("大范围滑块已切换显示状态")

    def set_palette(note: str, main_colors: tuple[int, int, int], fine_colors: tuple[int, int, int], wide_colors: tuple[int, int, int], disabled_colors: tuple[int, int, int]) -> None:
        DLL.SetSliderColors(slider_main, *main_colors)
        DLL.SetSliderColors(slider_fine, *fine_colors)
        DLL.SetSliderColors(slider_wide, *wide_colors)
        DLL.SetSliderColors(slider_disabled, *disabled_colors)
        refresh(note)

    def widen_main(dw: int) -> None:
        main_bounds["w"] += dw
        DLL.SetSliderBounds(slider_main, main_bounds["x"], main_bounds["y"], main_bounds["w"], main_bounds["h"])
        refresh(f"主滑块宽度已更新 dw={dw}")

    def restore() -> None:
        main_bounds["x"] = 56
        main_bounds["y"] = 128
        main_bounds["w"] = 560
        main_bounds["h"] = 40
        DLL.SetSliderBounds(slider_main, main_bounds["x"], main_bounds["y"], main_bounds["w"], main_bounds["h"])
        slider_meta["main"]["min"] = 0
        slider_meta["main"]["max"] = 100
        slider_meta["main"]["step"] = 10
        slider_meta["main"]["show_stops"] = True
        slider_meta["fine"]["min"] = 0
        slider_meta["fine"]["max"] = 100
        slider_meta["fine"]["step"] = 1
        slider_meta["fine"]["show_stops"] = False
        slider_meta["wide"]["min"] = 0
        slider_meta["wide"]["max"] = 200
        slider_meta["wide"]["step"] = 20
        slider_meta["wide"]["show_stops"] = True
        slider_meta["disabled"]["min"] = 0
        slider_meta["disabled"]["max"] = 100
        slider_meta["disabled"]["step"] = 10
        slider_meta["disabled"]["show_stops"] = True
        DLL.SetSliderRange(slider_main, 0, 100)
        DLL.SetSliderStep(slider_main, 10)
        DLL.SetSliderShowStops(slider_main, BOOL(True))
        DLL.SetSliderValue(slider_main, 36)
        DLL.SetSliderRange(slider_fine, 0, 100)
        DLL.SetSliderStep(slider_fine, 1)
        DLL.SetSliderShowStops(slider_fine, BOOL(False))
        DLL.SetSliderValue(slider_fine, 24)
        DLL.SetSliderRange(slider_wide, 0, 200)
        DLL.SetSliderStep(slider_wide, 20)
        DLL.SetSliderShowStops(slider_wide, BOOL(True))
        DLL.SetSliderValue(slider_wide, 120)
        DLL.SetSliderRange(slider_disabled, 0, 100)
        DLL.SetSliderStep(slider_disabled, 10)
        DLL.SetSliderShowStops(slider_disabled, BOOL(True))
        DLL.SetSliderValue(slider_disabled, 60)
        DLL.EnableSlider(slider_disabled, BOOL(False))
        DLL.ShowSlider(slider_wide, BOOL(True))
        set_palette(
            "滑块页已恢复默认",
            (THEME_PRIMARY, slider_surface, THEME_PRIMARY),
            (THEME_SUCCESS, slider_surface, THEME_SUCCESS),
            (THEME_WARNING, slider_surface, THEME_WARNING),
            (THEME_MUTED, slider_surface, THEME_MUTED),
        )

    sl_cb = DLL._SliderCB(lambda h, value: refresh(f"Slider 回调: hwnd=0x{base.hwnd_key(h):X} value={value}"))
    KEEP.append(sl_cb)
    for _, slider_hwnd in slider_items:
        DLL.SetSliderCallback(slider_hwnd, sl_cb)

    register_theme_label(base.label(page, "左侧展示主滑块、细步长、大范围和禁用态四种 Slider，用于直接验证数值、范围和停靠点切换。", 40, 310, 940, 24, fg=muted_color, bg=page_bg), "muted", "page")

    base.button(page, "0", "主条=0", 1044, 94, 116, 34, 0xFF909399, lambda: set_main_value(0, "主滑块已设为 0"))
    base.button(page, "36", "主条=36", 1172, 94, 116, 34, 0xFF409EFF, lambda: set_main_value(36, "主滑块已设为 36"))
    base.button(page, "75", "主条=75", 1300, 94, 124, 34, 0xFF67C23A, lambda: set_main_value(75, "主滑块已设为 75"))
    base.button(page, "120", "大范围=120", 1044, 138, 116, 34, 0xFFE6A23C, lambda: set_wide_value(120, "大范围滑块已设为 120"))
    base.button(page, "150", "大范围=150", 1172, 138, 116, 34, 0xFF8E44AD, lambda: set_wide_value(150, "大范围滑块已设为 150"))
    base.button(page, "•", "停靠点", 1300, 138, 124, 34, 0xFF409EFF, toggle_main_stops)
    base.button(page, "50", "范围 0-50", 1044, 182, 116, 34, 0xFF67C23A, lambda: set_main_range(0, 50, 5, "主滑块已切到范围 0-50 / step=5"))
    base.button(page, "100", "范围 0-100", 1172, 182, 116, 34, 0xFF909399, lambda: set_main_range(0, 100, 10, "主滑块已切回范围 0-100 / step=10"))
    base.button(page, "↔", "加宽 120", 1300, 182, 124, 34, 0xFFE6A23C, lambda: widen_main(120))
    base.button(page, "🔒", "禁用/启用", 1044, 226, 116, 34, 0xFF909399, toggle_disabled_slider)
    base.button(page, "👁", "显示/隐藏", 1172, 226, 116, 34, 0xFF409EFF, toggle_wide_visible)
    base.button(page, "💙", "蓝色方案", 1300, 226, 124, 34, 0xFF409EFF, lambda: set_palette("滑块已切到蓝色方案", (THEME_PRIMARY, slider_surface, THEME_PRIMARY), (THEME_SUCCESS, slider_surface, THEME_SUCCESS), (THEME_INFO, slider_surface, THEME_INFO), (THEME_MUTED, slider_surface, THEME_MUTED)))
    base.button(page, "🔥", "暖色方案", 1044, 270, 116, 34, 0xFFE6A23C, lambda: set_palette("滑块已切到暖色方案", (THEME_WARNING, slider_surface, THEME_WARNING), (THEME_DANGER, slider_surface, THEME_DANGER), (THEME_WARNING, slider_surface, THEME_DANGER), (THEME_MUTED, slider_surface, THEME_MUTED)))
    base.button(page, "↺", "恢复默认", 1172, 270, 116, 34, 0xFF409EFF, restore)

    register_theme_label(base.label(page, "1. GetSliderValue / SetSliderValue：读取和设置当前滑块值。", 40, 582, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "2. SetSliderRange / SetSliderStep：切换最小值、最大值和步长。", 40, 616, 820, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "3. SetSliderShowStops / SetSliderColors / GetSliderColors：切换停靠点和配色。", 40, 650, 980, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "4. EnableSlider / ShowSlider：演示启用态和可见态切换。", 40, 684, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "5. SetSliderBounds：直接调整主滑块宽度。", 40, 718, 700, 24, fg=text_color, bg=page_bg), "text", "page")
    refresh("滑块页已整理：只保留 Slider，并补上数值 / 范围 / 颜色控制")


def build_page_switch(page: HWND) -> None:
    palette = page_palette()
    page_bg = palette["page_bg"]
    card_bg = palette["card_bg"]
    text_color = palette["text"]
    muted_color = palette["muted"]
    accent_color = palette["accent"]

    base.groupbox(page, "🔀 Switch 样式演示", 16, 16, 980, 324)
    base.groupbox(page, "🧪 状态 / 文案 / 配色", 1020, 16, 444, 324)
    base.groupbox(page, "📘 Switch API 说明", 16, 538, 1448, 220)

    register_theme_label(
        base.label(
            page,
            "这一页只保留 Switch，不再混入 CheckBox / RadioButton / ProgressBar / Slider。",
            40,
            56,
            960,
            24,
            fg=muted_color,
            bg=page_bg,
        ),
        "muted",
        "page",
    )
    readout = register_theme_label(
        base.label(page, "等待读取 Switch 状态。", 40, 366, 1384, 108, fg=text_color, bg=page_bg, wrap=True),
        "text",
        "page",
    )
    state_text = register_theme_label(
        base.label(page, "Switch 页面状态将在这里更新。", 40, 490, 1360, 22, fg=accent_color, bg=page_bg),
        "accent",
        "page",
    )

    switch_stage = DLL.CreatePanel(page, 40, 96, 930, 208, THEME_SURFACE)
    register_theme_label(base.label(switch_stage, "主开关", 16, 16, 180, 20, fg=text_color, bg=card_bg, size=14, bold=True), "text", "card")
    register_theme_label(base.label(switch_stage, "紧凑样式", 16, 102, 180, 20, fg=text_color, bg=card_bg, size=14, bold=True), "text", "card")
    register_theme_label(base.label(switch_stage, "状态文案", 320, 16, 180, 20, fg=text_color, bg=card_bg, size=14, bold=True), "text", "card")
    register_theme_label(base.label(switch_stage, "禁用态", 320, 102, 180, 20, fg=text_color, bg=card_bg, size=14, bold=True), "text", "card")

    on_p, on_n, _ = s("开")
    off_p, off_n, _ = s("关")
    online_p, online_n, _ = s("在线")
    offline_p, offline_n, _ = s("离线")
    yes_p, yes_n, _ = s("是")
    no_p, no_n, _ = s("否")
    blank_p, blank_n, _ = s("")

    sw_main = DLL.CreateSwitch(switch_stage, 16, 44, 112, 34, BOOL(True), THEME_PRIMARY, THEME_BORDER_LIGHT, on_p, on_n, off_p, off_n)
    sw_compact = DLL.CreateSwitch(switch_stage, 16, 130, 82, 30, BOOL(False), THEME_WARNING, THEME_BORDER_LIGHT, blank_p, blank_n, blank_p, blank_n)
    sw_status = DLL.CreateSwitch(switch_stage, 320, 44, 148, 36, BOOL(True), THEME_SUCCESS, THEME_BORDER_LIGHT, online_p, online_n, offline_p, offline_n)
    sw_disabled = DLL.CreateSwitch(switch_stage, 320, 130, 112, 34, BOOL(False), THEME_MUTED, THEME_BORDER_LIGHT, yes_p, yes_n, no_p, no_n)
    DLL.EnableSwitch(sw_disabled, BOOL(False))

    register_theme_label(
        base.label(
            switch_stage,
            "左侧展示主开关、紧凑开关、状态开关和禁用态开关，用于直接验证状态、文案、颜色、可见性和尺寸切换。",
            16,
            176,
            880,
            20,
            fg=muted_color,
            bg=card_bg,
        ),
        "muted",
        "card",
    )

    switch_items = [
        ("main", sw_main),
        ("compact", sw_compact),
        ("status", sw_status),
        ("disabled", sw_disabled),
    ]
    switch_meta = {
        "main": {"active_text": "开", "inactive_text": "关", "bounds": {"x": 16, "y": 44, "w": 112, "h": 34}},
        "compact": {"active_text": "", "inactive_text": "", "bounds": {"x": 16, "y": 130, "w": 82, "h": 30}},
        "status": {"active_text": "在线", "inactive_text": "离线", "bounds": {"x": 320, "y": 44, "w": 148, "h": 36}},
        "disabled": {"active_text": "是", "inactive_text": "否", "bounds": {"x": 320, "y": 130, "w": 112, "h": 34}},
    }
    main_bounds = switch_meta["main"]["bounds"]
    ui_flags = {"text_emphasis": False}

    def set_switch_texts(hwnd: HWND, key: str, active_text: str, inactive_text: str) -> None:
        active_p, active_n, _ = s(active_text)
        inactive_p, inactive_n, _ = s(inactive_text)
        DLL.SetSwitchText(hwnd, active_p, active_n, inactive_p, inactive_n)
        switch_meta[key]["active_text"] = active_text
        switch_meta[key]["inactive_text"] = inactive_text

    def apply_text_colors(emphasis: bool) -> None:
        if emphasis:
            DLL.SetSwitchTextColors(sw_main, 0xFFFFFFFF, THEME_PRIMARY)
            DLL.SetSwitchTextColors(sw_compact, 0xFFFFFFFF, THEME_WARNING)
            DLL.SetSwitchTextColors(sw_status, 0xFFFFFFFF, THEME_SUCCESS)
            DLL.SetSwitchTextColors(sw_disabled, 0xFFFFFFFF, THEME_MUTED)
        else:
            for hwnd in (sw_main, sw_compact, sw_status, sw_disabled):
                DLL.SetSwitchTextColors(hwnd, 0xFFFFFFFF, THEME_TEXT)

    def refresh(note: str = "已读取 Switch 状态") -> None:
        lines: list[str] = []
        for key, hwnd in switch_items:
            active = UINT32()
            inactive = UINT32()
            active_text_color = UINT32()
            inactive_text_color = UINT32()
            DLL.GetSwitchColors(hwnd, ctypes.byref(active), ctypes.byref(inactive), ctypes.byref(active_text_color), ctypes.byref(inactive_text_color))
            meta = switch_meta[key]
            bounds = meta["bounds"]
            checked = int(bool(DLL.GetSwitchState(hwnd)))
            enabled = "启用" if bool(USER32.IsWindowEnabled(hwnd)) else "禁用"
            visible = "显示" if bool(USER32.IsWindowVisible(hwnd)) else "隐藏"
            lines.append(
                f"{key}: state={checked} bounds=({bounds['x']}, {bounds['y']}, {bounds['w']}, {bounds['h']}) "
                f"text=({meta['active_text']}/{meta['inactive_text']}) {visible}/{enabled} "
                f"active=0x{int(active.value):08X} inactive=0x{int(inactive.value):08X} "
                f"text_active=0x{int(active_text_color.value):08X} text_inactive=0x{int(inactive_text_color.value):08X}"
            )
        base.set_label_text(readout, f"{note}\n" + "\n".join(lines))
        base.set_label_text(state_text, note)
        base.set_status(note)

    def set_main_state(checked: bool, note: str) -> None:
        DLL.SetSwitchState(sw_main, BOOL(checked))
        refresh(note)

    def toggle_compact() -> None:
        DLL.SetSwitchState(sw_compact, BOOL(not bool(DLL.GetSwitchState(sw_compact))))
        refresh("紧凑开关已切换状态")

    def toggle_main_texts() -> None:
        if str(switch_meta["main"]["active_text"]) == "开":
            set_switch_texts(sw_main, "main", "启用", "停用")
            refresh("主开关文案已切换为 启用 / 停用")
        else:
            set_switch_texts(sw_main, "main", "开", "关")
            refresh("主开关文案已恢复为 开 / 关")

    def toggle_disabled_demo() -> None:
        DLL.EnableSwitch(sw_disabled, BOOL(not bool(USER32.IsWindowEnabled(sw_disabled))))
        refresh("禁用态开关已切换启用状态")

    def toggle_status_visible() -> None:
        DLL.ShowSwitch(sw_status, BOOL(not bool(USER32.IsWindowVisible(sw_status))))
        refresh("状态开关已切换显示状态")

    def widen_main(dw: int) -> None:
        main_bounds["w"] += dw
        DLL.SetSwitchBounds(sw_main, main_bounds["x"], main_bounds["y"], main_bounds["w"], main_bounds["h"])
        refresh(f"主开关宽度已更新 dw={dw}")

    def set_palette(note: str, main_colors: tuple[int, int], compact_colors: tuple[int, int], status_colors: tuple[int, int], disabled_colors: tuple[int, int]) -> None:
        DLL.SetSwitchColors(sw_main, *main_colors)
        DLL.SetSwitchColors(sw_compact, *compact_colors)
        DLL.SetSwitchColors(sw_status, *status_colors)
        DLL.SetSwitchColors(sw_disabled, *disabled_colors)
        refresh(note)

    def toggle_text_emphasis() -> None:
        ui_flags["text_emphasis"] = not bool(ui_flags["text_emphasis"])
        apply_text_colors(bool(ui_flags["text_emphasis"]))
        refresh("Switch 文案颜色已切换")

    def restore() -> None:
        main_bounds["x"] = 16
        main_bounds["y"] = 44
        main_bounds["w"] = 112
        main_bounds["h"] = 34
        DLL.SetSwitchBounds(sw_main, 16, 44, 112, 34)
        switch_meta["compact"]["bounds"] = {"x": 16, "y": 130, "w": 82, "h": 30}
        switch_meta["status"]["bounds"] = {"x": 320, "y": 44, "w": 148, "h": 36}
        switch_meta["disabled"]["bounds"] = {"x": 320, "y": 130, "w": 112, "h": 34}
        DLL.SetSwitchBounds(sw_compact, 16, 130, 82, 30)
        DLL.SetSwitchBounds(sw_status, 320, 44, 148, 36)
        DLL.SetSwitchBounds(sw_disabled, 320, 130, 112, 34)
        set_switch_texts(sw_main, "main", "开", "关")
        set_switch_texts(sw_compact, "compact", "", "")
        set_switch_texts(sw_status, "status", "在线", "离线")
        set_switch_texts(sw_disabled, "disabled", "是", "否")
        DLL.SetSwitchState(sw_main, BOOL(True))
        DLL.SetSwitchState(sw_compact, BOOL(False))
        DLL.SetSwitchState(sw_status, BOOL(True))
        DLL.SetSwitchState(sw_disabled, BOOL(False))
        DLL.EnableSwitch(sw_disabled, BOOL(False))
        DLL.ShowSwitch(sw_status, BOOL(True))
        ui_flags["text_emphasis"] = False
        apply_text_colors(False)
        set_palette(
            "Switch 页面已恢复默认",
            (THEME_PRIMARY, THEME_BORDER_LIGHT),
            (THEME_WARNING, THEME_BORDER_LIGHT),
            (THEME_SUCCESS, THEME_BORDER_LIGHT),
            (THEME_MUTED, THEME_BORDER_LIGHT),
        )

    sw_cb = DLL._SwitchCB(lambda h, checked: refresh(f"Switch 回调: hwnd=0x{base.hwnd_key(h):X} checked={int(bool(checked))}"))
    KEEP.append(sw_cb)
    for _, switch_hwnd in switch_items:
        DLL.SetSwitchCallback(switch_hwnd, sw_cb)

    apply_text_colors(False)
    register_theme_label(base.label(page, "左侧展示四种 Switch 组合，用于直接验证状态、文案、配色、启用态、可见性和尺寸更新。", 40, 310, 930, 24, fg=muted_color, bg=page_bg), "muted", "page")

    base.button(page, "ON", "主开=开", 1044, 94, 116, 34, 0xFF67C23A, lambda: set_main_state(True, "主开关已设为开启"))
    base.button(page, "OFF", "主开=关", 1172, 94, 116, 34, 0xFF909399, lambda: set_main_state(False, "主开关已设为关闭"))
    base.button(page, "📝", "切换文案", 1300, 94, 124, 34, 0xFF409EFF, toggle_main_texts)
    base.button(page, "↺", "紧凑切换", 1044, 138, 116, 34, 0xFF8E44AD, toggle_compact)
    base.button(page, "🔒", "禁用/启用", 1172, 138, 116, 34, 0xFF909399, toggle_disabled_demo)
    base.button(page, "👁️", "显示/隐藏", 1300, 138, 124, 34, 0xFF409EFF, toggle_status_visible)
    base.button(page, "↔", "加宽 48", 1044, 182, 116, 34, 0xFFE6A23C, lambda: widen_main(48))
    base.button(page, "💙", "蓝色方案", 1172, 182, 116, 34, 0xFF409EFF, lambda: set_palette("Switch 已切到蓝色方案", (THEME_PRIMARY, THEME_BORDER_LIGHT), (THEME_INFO, THEME_BORDER_LIGHT), (THEME_SUCCESS, THEME_BORDER_LIGHT), (THEME_MUTED, THEME_BORDER_LIGHT)))
    base.button(page, "🔥", "暖色方案", 1300, 182, 124, 34, 0xFFE6A23C, lambda: set_palette("Switch 已切到暖色方案", (THEME_WARNING, THEME_BORDER_LIGHT), (THEME_DANGER, THEME_BORDER_LIGHT), (THEME_WARNING, THEME_BORDER_LIGHT), (THEME_MUTED, THEME_BORDER_LIGHT)))
    base.button(page, "🎨", "文案高亮", 1044, 226, 116, 34, 0xFF8E44AD, toggle_text_emphasis)
    base.button(page, "↺", "恢复默认", 1172, 226, 116, 34, 0xFF409EFF, restore)

    register_theme_label(base.label(page, "1. GetSwitchState / SetSwitchState：读取和切换当前开关状态。", 40, 582, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "2. SetSwitchText：动态切换开启 / 关闭两套文案。", 40, 616, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "3. SetSwitchColors / SetSwitchTextColors / GetSwitchColors：切换轨道和文字配色。", 40, 650, 980, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "4. EnableSwitch / ShowSwitch：演示启用态和可见态切换。", 40, 684, 760, 24, fg=text_color, bg=page_bg), "text", "page")
    register_theme_label(base.label(page, "5. SetSwitchBounds：直接调整主开关宽度。", 40, 718, 700, 24, fg=text_color, bg=page_bg), "text", "page")
    refresh("Switch 页面已整理：只保留 Switch，并补上状态 / 文案 / 颜色 / 布局控制")


PAGE_BUILDERS = {
    "overview_basic": build_page_overview_basic,
    "overview_select": build_page_overview_select,
    "overview_display": build_page_overview_display,
    "overview_popup": build_page_overview_popup,
    "overview_nav": build_page_overview_nav,
    "overview_data": build_page_overview_data,
    "page_window": build_page_window,
    "page_button": build_page_button,
    "page_label": build_page_label,
    "page_editbox": build_page_editbox,
    "page_color_emoji_edit": build_page_color_emoji_edit,
    "page_checkbox": build_page_checkbox,
    "page_radiobutton": build_page_radiobutton,
    "page_progressbar": build_page_progressbar,
    "page_slider": build_page_slider,
    "page_switch": build_page_switch,
    "page_state": build_page_state,
    "page_groupbox": build_page_groupbox_v2,
    "page_panel_demo": build_page_panel_demo_v2,
    "page_listbox": build_page_listbox_v2,
    "page_combobox": build_page_combobox_v2,
    "page_d2d_combobox": build_page_d2d_combobox_v2,
    "page_datetime": build_page_datetime,
    "page_hotkey": build_page_hotkey,
    "page_picturebox": build_page_picturebox_v2,
    "page_tooltip": build_page_tooltip,
    "page_notification": build_page_notification,
    "page_messagebox": build_page_messagebox,
    "page_confirmbox": build_page_confirmbox,
    "page_tabcontrol": build_page_tabcontrol,
    "page_treeview": build_page_treeview_enhanced,
    "page_menubar": build_page_menubar_v3,
    "page_popupmenu": build_page_popupmenu_enhanced,
    "page_datagrid": build_page_datagrid_enhanced_v2,
}


def activate_page(page_key: str, title: str, desc: str) -> None:
    built: set[str] = LOCAL["built"]  # type: ignore[assignment]
    pages: dict[str, HWND] = LOCAL["pages"]  # type: ignore[assignment]
    if page_key not in built:
        PAGE_BUILDERS[page_key](page_panel(page_key))
        built.add(page_key)
    current = LOCAL.get("current")
    if current and current in pages:
        show_hwnd(pages[current], False)
    show_hwnd(pages[page_key], True)
    LOCAL["current"] = page_key
    sync_nav_selection(page_key, title)
    set_header(title, desc)
    invalidate_visible_tree(LOCAL.get("host"))
    force_redraw(STATE.get("hwnd"))
    base.set_status(f"已切换到: {title}")


def on_nav_selected(node_id: int, _ctx) -> None:
    LOCAL["selected_nav_node"] = node_id
    suppressed = int(LOCAL.get("suppress_nav_once") or 0)
    if suppressed == node_id:
        LOCAL["suppress_nav_once"] = 0
        return
    info = LOCAL["node_info"].get(node_id)  # type: ignore[union-attr]
    if info:
        page_key, title, desc = info
        activate_page(str(page_key), str(title), str(desc))


def build_nav_tree(parent: HWND) -> None:
    palette = page_palette()
    tree_bg = 0xFF161718 if is_dark_theme() else 0xFFFFFFFF
    tree = DLL.CreateTreeView(parent, 16, 56, SIDEBAR_W - 32, 820, tree_bg, palette["text"], ctypes.c_void_p())
    DLL.SetTreeViewSidebarMode(tree, BOOL(True))
    DLL.SetTreeViewRowHeight(tree, ctypes.c_float(38.0))
    DLL.SetTreeViewItemSpacing(tree, ctypes.c_float(6.0))
    DLL.SetTreeViewTextColor(tree, palette["text"])
    DLL.SetTreeViewSelectedBgColor(tree, 0xFF409EFF)
    DLL.SetTreeViewSelectedForeColor(tree, 0xFFFFFFFF)
    DLL.SetTreeViewHoverBgColor(tree, 0xFF2B2F36 if is_dark_theme() else 0xFFEAF3FF)
    DLL.SetTreeViewFont(tree, base.FONT_PTR, base.FONT_LEN, ctypes.c_float(13.0), 500, BOOL(False))
    DLL.EnableTreeViewDragDrop(tree, BOOL(False))
    LOCAL["nav_tree"] = tree
    first_child = 0
    for category in CATEGORY_TREE:
        root_id = add_tree_root(tree, str(category["title"]), str(category["icon"]), str(category["page"]), str(category["desc"]))
        for idx, (title, icon, page_key, desc) in enumerate(category["children"]):
            child_id = add_tree_child(tree, root_id, title, icon, page_key, desc)
            if first_child == 0 and idx == 0:
                first_child = child_id

    cb = DLL._TreeCB(on_nav_selected)
    KEEP.append(cb)
    DLL.SetTreeViewCallback(tree, base.CALLBACK_NODE_SELECTED, cb)
    DLL.ExpandAll(tree)
    if first_child:
        LOCAL["selected_nav_node"] = first_child
        DLL.SetSelectedNode(tree, first_child)
        on_nav_selected(first_child, None)


def build() -> None:
    title_p, title_n, _ = s("🌲 Tree AllDemo Enhanced")
    hwnd = DLL.create_window_bytes(title_p, title_n, 40, 40, WINDOW_W, WINDOW_H)
    STATE["hwnd"] = hwnd
    show_hwnd(hwnd, False)
    bcb = DLL._ButtonCB(base.on_button_click)
    ccb = DLL._ConfirmCB(base.on_confirm)
    KEEP.extend([bcb, ccb])
    DLL.set_button_click_callback(bcb)
    STATE["confirm_cb"] = ccb

    initial_content_h = WINDOW_H - SHELL_TOP - SHELL_BOTTOM_GAP
    sidebar_bg = 0xFF161718 if is_dark_theme() else 0xFFFFFFFF
    host_bg = page_palette()["page_bg"]
    sidebar = DLL.CreatePanel(hwnd, 16, SHELL_TOP, SIDEBAR_W, initial_content_h, sidebar_bg)
    LOCAL["sidebar"] = sidebar
    LOCAL["sidebar_title"] = base.label(sidebar, "📚 组件树", 16, 16, 180, 28, fg=0xFF303133, bg=sidebar_bg, size=18, bold=True)
    LOCAL["sidebar_desc"] = base.label(sidebar, "一级分类 / 二级组件", 16, 40, 200, 18, fg=0xFF909399, bg=sidebar_bg, size=11)

    host = DLL.CreatePanel(hwnd, CONTENT_X, SHELL_TOP, CONTENT_W, initial_content_h, host_bg)
    LOCAL["host"] = host
    LOCAL["header_title"] = base.label(host, "等待选择组件", 24, 18, 760, 30, fg=page_palette()["text"], bg=host_bg, size=20, bold=True)
    LOCAL["header_desc"] = base.label(host, "请从左侧树形框选择一个组件。", 24, 52, 1200, 24, fg=page_palette()["muted"], bg=host_bg, size=13)
    STATE["status"] = base.label(hwnd, "准备就绪。", 16, STATUS_Y, WINDOW_W - 40, 28, fg=page_palette()["muted"], bg=host_bg, size=12)
    build_nav_tree(sidebar)
    apply_shell_theme()
    relayout_shell(WINDOW_W, WINDOW_H, refresh_now=False)
    show_hwnd(hwnd, True)
    refresh_visible_shell()


def main() -> int:
    base.setup()
    bind_extra_apis()
    build()
    DLL.set_message_loop_main_window(STATE["hwnd"])
    base.set_status("🌲 树形框版 alldemo 增强版已启动。")
    DLL.run_message_loop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
