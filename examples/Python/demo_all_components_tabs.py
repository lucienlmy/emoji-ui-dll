# -*- coding: utf-8 -*-
from __future__ import annotations

import base64
import ctypes
import struct
import sys
from ctypes import wintypes
from pathlib import Path

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

RDW_INVALIDATE = 0x0001
RDW_ERASE = 0x0004
RDW_ALLCHILDREN = 0x0080
RDW_UPDATENOW = 0x0100
RDW_FRAME = 0x0400

ALIGN_LEFT = 0
ALIGN_CENTER = 1
ALIGN_RIGHT = 2
BUTTON_TYPE_AUTO = -1
BUTTON_TYPE_DEFAULT = 0
BUTTON_TYPE_PRIMARY = 1
BUTTON_TYPE_SUCCESS = 2
BUTTON_TYPE_WARNING = 3
BUTTON_TYPE_DANGER = 4
BUTTON_TYPE_INFO = 5
BUTTON_STYLE_SOLID = 0
BUTTON_STYLE_PLAIN = 1
BUTTON_STYLE_TEXT = 2
BUTTON_STYLE_LINK = 3
BUTTON_SIZE_LARGE = 0
BUTTON_SIZE_DEFAULT = 1
BUTTON_SIZE_SMALL = 2
GROUPBOX_STYLE_CARD = 1
TAB_HEADER_STYLE_LINE = 0
TAB_HEADER_STYLE_CARD = 1
TAB_HEADER_STYLE_CARD_PLAIN = 2
TAB_HEADER_STYLE_SEGMENTED = 3
RADIO_STYLE_DEFAULT = 0
RADIO_STYLE_BORDER = 1
RADIO_STYLE_BUTTON = 2
DTP_YMDHM = 3
LAYOUT_FLOW_HORIZONTAL = 1
LAYOUT_FLOW_VERTICAL = 2
LAYOUT_GRID = 3
LAYOUT_DOCK = 4
DOCK_NONE = 0
DOCK_TOP = 1
DOCK_BOTTOM = 2
DOCK_LEFT = 3
DOCK_RIGHT = 4
DOCK_FILL = 5
POPUP_TOP = 0
POPUP_BOTTOM = 3
POPUP_LEFT = 6
POPUP_RIGHT = 9
TOOLTIP_THEME_DARK = 0
TOOLTIP_THEME_LIGHT = 1
TOOLTIP_THEME_CUSTOM = 2
TOOLTIP_TRIGGER_HOVER = 0
TOOLTIP_TRIGGER_CLICK = 1
NOTIFY_TOP_RIGHT = 0
NOTIFY_TOP_LEFT = 1
NOTIFY_BOTTOM_RIGHT = 2
NOTIFY_BOTTOM_LEFT = 3
NOTIFY_INFO = 0
NOTIFY_SUCCESS = 1
NOTIFY_WARNING = 2
NOTIFY_ERROR = 3

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

TAB_BASIC = 0
TAB_SELECT = 1
TAB_DATA = 2
TAB_TABS = 3
TAB_LAYOUT = 4
TAB_THEME = 5
TAB_MENU_TREE = 6
TAB_TAB_STYLES = 7

MENU_MSG = 1101
MENU_CONFIRM = 1102
MENU_TAB_BASIC = 1201
MENU_TAB_SELECT = 1202
MENU_TAB_DATA = 1203
MENU_TAB_TABS = 1204
MENU_TAB_LAYOUT = 1205
MENU_TAB_THEME = 1206
MENU_TAB_MENU_TREE = 1207
MENU_TAB_TAB_STYLES = 1208
MENU_TREE_EXPAND = 1301
MENU_TREE_COLLAPSE = 1302
MENU_TREE_TOGGLE_SIDEBAR = 1303
MENU_RATING_CLEAR = 1311
MENU_RATING_1 = 1312
MENU_RATING_3 = 1313
MENU_RATING_5 = 1314

POP_WINDOW_STATUS = 2101
POP_WINDOW_MSG = 2102
POP_TREE_EXPAND = 2103
POP_TREE_COLLAPSE = 2104
POP_TREE_TOGGLE_SIDEBAR = 2105
POP_RATING_CLEAR = 2106
POP_RATING_3 = 2107
POP_RATING_5 = 2108
POP_GRID_ADD = 2201
POP_GRID_STATUS = 2202
POP_BUTTON_STATUS = 2301
POP_CHECKBOX_TOGGLE = 2401
POP_PAGE_STATUS = 2501
POP_PAGE_MSG = 2502
POP_GROUP_STATUS = 2601
POP_GROUP_MSG = 2602
POP_TAB_STATUS = 2701
POP_TAB_MSG = 2702

CALLBACK_NODE_SELECTED = 1
CALLBACK_NODE_EXPANDED = 2
CALLBACK_NODE_COLLAPSED = 3
CALLBACK_NODE_MOVED = 8

PNG_BYTES = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADUlEQVQImWP4z8DwHwAFAAH/e+m+7wAAAABJRU5ErkJggg=="
)

STATE: dict[str, object] = {
    "hwnd": None,
    "status": None,
    "main_tab": None,
    "nested_tab": None,
    "tab_close_cb": None,
    "right_click_cb": None,
    "checkbox": None,
    "progress": None,
    "grid": None,
    "grid_virtual": None,
    "grid_virtual_mode": False,
    "row_count": 0,
    "grid_dark": True,
    "grid_dblclick": True,
    "grid_header_align": ALIGN_CENTER,
    "grid_cell_align": ALIGN_LEFT,
    "confirm_cb": None,
    "theme_cb": None,
    "layout_mode": "flow_h",
    "tree_primary": None,
    "tree_sidebar_enabled": True,
    "rating_value": 3,
    "rating_label": None,
    "tree_status_label": None,
    "button_loading_demo": None,
    "button_loading_active": False,
    "tab_style_demo": None,
    "tab_style_secondary": None,
    "closable_tabs": {},
}
BUTTON_ACTIONS: dict[tuple[int, int], object] = {}
GROUPBOX_HOSTS: dict[int, HWND] = {}
GROUPBOX_BOUNDS: dict[int, tuple[int, int, int, int]] = {}
KEEP: list[object] = []

FONT_RAW = "Microsoft YaHei UI".encode("utf-8")
FONT_BUF = (ctypes.c_ubyte * len(FONT_RAW))(*FONT_RAW)
FONT_PTR = ctypes.cast(FONT_BUF, ctypes.c_void_p)
FONT_LEN = len(FONT_RAW)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def dll_path() -> Path:
    p = repo_root() / "bin" / "x64" / "Release" / "emoji_window.dll"
    if p.is_file():
        return p
    local = Path(__file__).resolve().parent / "emoji_window.dll"
    return local


def argb(a: int, r: int, g: int, b: int) -> int:
    return ((a & 255) << 24) | ((r & 255) << 16) | ((g & 255) << 8) | (b & 255)


def s(text: str) -> tuple[ctypes.c_void_p, int, object]:
    raw = text.encode("utf-8")
    if not raw:
        return ctypes.c_void_p(), 0, ctypes.c_void_p()
    buf = (ctypes.c_ubyte * len(raw))(*raw)
    return ctypes.cast(buf, ctypes.c_void_p), len(raw), buf


def hwnd_key(hwnd) -> int:
    if hwnd is None:
        return 0
    return int(ctypes.cast(hwnd, ctypes.c_void_p).value or 0)


def button_host(parent: HWND) -> HWND:
    return GROUPBOX_HOSTS.get(hwnd_key(parent), parent)


def button_bounds(parent: HWND) -> tuple[int, int, int, int] | None:
    return GROUPBOX_BOUNDS.get(hwnd_key(parent))


def load_dll() -> ctypes.WinDLL:
    if sys.platform != "win32":
        raise OSError("Only Windows is supported.")
    if struct.calcsize("P") * 8 != 64:
        raise OSError("Use 64-bit Python.")
    path = dll_path()
    if not path.is_file():
        raise FileNotFoundError(path)
    return ctypes.WinDLL(str(path))


DLL = load_dll()
USER32 = ctypes.WinDLL("user32", use_last_error=True)


def setup() -> None:
    button_cb = ctypes.WINFUNCTYPE(None, ctypes.c_int, HWND)
    confirm_cb = ctypes.WINFUNCTYPE(None, ctypes.c_int)
    menu_cb = ctypes.WINFUNCTYPE(None, ctypes.c_int, ctypes.c_int)
    tab_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int)
    tab_close_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int)
    checkbox_cb = ctypes.WINFUNCTYPE(None, HWND, BOOL)
    radio_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int, BOOL)
    listbox_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int)
    combo_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int)
    right_click_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int, ctypes.c_int)
    theme_changed_cb = ctypes.WINFUNCTYPE(None, ctypes.c_char_p)
    value_cb = ctypes.WINFUNCTYPE(None, HWND)
    picture_cb = ctypes.WINFUNCTYPE(None, HWND)
    progress_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int)
    slider_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int)
    switch_cb = ctypes.WINFUNCTYPE(None, HWND, BOOL)
    notification_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int)
    dg_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int, ctypes.c_int)
    dg_virtual_cb = ctypes.WINFUNCTYPE(ctypes.c_int, HWND, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int)
    tree_cb = ctypes.WINFUNCTYPE(None, ctypes.c_int, ctypes.c_void_p)

    DLL.create_window_bytes.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.create_window_bytes.restype = HWND
    DLL.set_message_loop_main_window.argtypes = [HWND]
    DLL.run_message_loop.argtypes = []

    DLL.create_emoji_button_bytes.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, UINT32]
    DLL.create_emoji_button_bytes.restype = ctypes.c_int
    DLL.set_button_click_callback.argtypes = [button_cb]
    DLL.SetButtonType.argtypes = [ctypes.c_int, ctypes.c_int]
    DLL.SetButtonStyle.argtypes = [ctypes.c_int, ctypes.c_int]
    DLL.SetButtonSize.argtypes = [ctypes.c_int, ctypes.c_int]
    DLL.SetButtonRound.argtypes = [ctypes.c_int, BOOL]
    DLL.SetButtonCircle.argtypes = [ctypes.c_int, BOOL]
    DLL.SetButtonLoading.argtypes = [ctypes.c_int, BOOL]

    DLL.CreateLabel.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, UINT32, UINT32, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, BOOL, BOOL, BOOL, ctypes.c_int, BOOL]
    DLL.CreateLabel.restype = HWND
    DLL.SetLabelText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]

    DLL.show_message_box_bytes.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.show_confirm_box_bytes.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, confirm_cb]

    DLL.CreateEditBox.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, UINT32, UINT32, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, BOOL, BOOL, BOOL, ctypes.c_int, BOOL, BOOL, BOOL, BOOL, BOOL]
    DLL.CreateEditBox.restype = HWND
    DLL.CreateColorEmojiEditBox.argtypes = list(DLL.CreateEditBox.argtypes)
    DLL.CreateColorEmojiEditBox.restype = HWND

    DLL.CreateCheckBox.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, BOOL, UINT32, UINT32, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, BOOL, BOOL, BOOL]
    DLL.CreateCheckBox.restype = HWND
    DLL.SetCheckBoxCallback.argtypes = [HWND, checkbox_cb]
    DLL.GetCheckBoxState.argtypes = [HWND]
    DLL.SetCheckBoxState.argtypes = [HWND, BOOL]
    DLL.SetCheckBoxStyle.argtypes = [HWND, ctypes.c_int]
    DLL.SetCheckBoxCheckColor.argtypes = [HWND, UINT32]

    DLL.CreateRadioButton.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, BOOL, UINT32, UINT32, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, BOOL, BOOL, BOOL]
    DLL.CreateRadioButton.restype = HWND
    DLL.SetRadioButtonCallback.argtypes = [HWND, radio_cb]
    DLL.SetRadioButtonStyle.argtypes = [HWND, ctypes.c_int]
    DLL.SetRadioButtonDotColor.argtypes = [HWND, UINT32]

    DLL.CreateProgressBar.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, UINT32, UINT32, BOOL, UINT32]
    DLL.CreateProgressBar.restype = HWND
    DLL.SetProgressValue.argtypes = [HWND, ctypes.c_int]
    DLL.GetProgressValue.argtypes = [HWND]
    DLL.GetProgressValue.restype = ctypes.c_int
    DLL.SetProgressBarCallback.argtypes = [HWND, progress_cb]
    DLL.SetProgressBarShowText.argtypes = [HWND, BOOL]
    DLL.SetProgressBarTextColor.argtypes = [HWND, UINT32]

    DLL.CreateSlider.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, UINT32, UINT32]
    DLL.CreateSlider.restype = HWND
    DLL.GetSliderValue.argtypes = [HWND]
    DLL.GetSliderValue.restype = ctypes.c_int
    DLL.SetSliderValue.argtypes = [HWND, ctypes.c_int]
    DLL.SetSliderRange.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
    DLL.SetSliderStep.argtypes = [HWND, ctypes.c_int]
    DLL.SetSliderShowStops.argtypes = [HWND, BOOL]
    DLL.SetSliderCallback.argtypes = [HWND, slider_cb]

    DLL.CreateSwitch.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, BOOL, UINT32, UINT32, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.CreateSwitch.restype = HWND
    DLL.GetSwitchState.argtypes = [HWND]
    DLL.GetSwitchState.restype = BOOL
    DLL.SetSwitchState.argtypes = [HWND, BOOL]
    DLL.SetSwitchText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.SetSwitchColors.argtypes = [HWND, UINT32, UINT32]
    DLL.SetSwitchCallback.argtypes = [HWND, switch_cb]

    DLL.CreateTooltip.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, UINT32, UINT32]
    DLL.CreateTooltip.restype = HWND
    DLL.SetTooltipText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.SetLabelColor.argtypes = [HWND, UINT32, UINT32]
    DLL.SetLabelAlignment.argtypes = [HWND, ctypes.c_int]
    DLL.SetTooltipPlacement.argtypes = [HWND, ctypes.c_int]
    DLL.SetTooltipTheme.argtypes = [HWND, ctypes.c_int]
    DLL.SetTooltipColors.argtypes = [HWND, UINT32, UINT32, UINT32]
    DLL.SetTooltipFont.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_float]
    DLL.SetTooltipTrigger.argtypes = [HWND, ctypes.c_int]
    DLL.BindTooltipToControl.argtypes = [HWND, HWND]
    DLL.ShowTooltipForControl.argtypes = [HWND, HWND]
    DLL.HideTooltip.argtypes = [HWND]
    DLL.DestroyTooltip.argtypes = [HWND]

    DLL.ShowNotification.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.ShowNotification.restype = HWND
    DLL.SetNotificationCallback.argtypes = [HWND, notification_cb]
    DLL.CloseNotification.argtypes = [HWND]

    DLL.CreatePictureBox.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, UINT32]
    DLL.CreatePictureBox.restype = HWND
    DLL.LoadImageFromMemory.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.SetPictureBoxCallback.argtypes = [HWND, picture_cb]

    DLL.CreateListBox.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, BOOL, UINT32, UINT32]
    DLL.CreateListBox.restype = HWND
    DLL.AddListItem.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.SetListBoxCallback.argtypes = [HWND, listbox_cb]
    DLL.SetSelectedIndex.argtypes = [HWND, ctypes.c_int]
    DLL.GetListItemText.argtypes = [HWND, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.GetListItemText.restype = ctypes.c_int

    DLL.CreateComboBox.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, BOOL, UINT32, UINT32, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, BOOL, BOOL, BOOL]
    DLL.CreateComboBox.restype = HWND
    DLL.AddComboItem.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.SetComboSelectedIndex.argtypes = [HWND, ctypes.c_int]
    DLL.SetComboBoxCallback.argtypes = [HWND, combo_cb]

    DLL.CreateD2DComboBox.argtypes = list(DLL.CreateComboBox.argtypes)
    DLL.CreateD2DComboBox.restype = HWND
    DLL.AddD2DComboItem.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.SetD2DComboSelectedIndex.argtypes = [HWND, ctypes.c_int]
    DLL.SetD2DComboBoxCallback.argtypes = [HWND, combo_cb]

    DLL.CreateD2DDateTimePicker.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, UINT32, UINT32, UINT32, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, BOOL, BOOL, BOOL]
    DLL.CreateD2DDateTimePicker.restype = HWND
    DLL.SetD2DDateTimePickerDateTime.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.GetD2DDateTimePickerDateTime.argtypes = [HWND, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int)]
    DLL.SetD2DDateTimePickerCallback.argtypes = [HWND, value_cb]

    DLL.CreateGroupBox.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, UINT32, UINT32, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, BOOL, BOOL, BOOL]
    DLL.CreateGroupBox.restype = HWND
    DLL.SetGroupBoxStyle.argtypes = [HWND, ctypes.c_int]
    DLL.SetGroupBoxTitleColor.argtypes = [HWND, UINT32]
    DLL.CreatePanel.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, UINT32]
    DLL.CreatePanel.restype = HWND

    DLL.CreateTabControl.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.CreateTabControl.restype = HWND
    DLL.AddTabItem.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, HWND]
    DLL.AddTabItem.restype = ctypes.c_int
    DLL.GetTabContentWindow.argtypes = [HWND, ctypes.c_int]
    DLL.GetTabContentWindow.restype = HWND
    DLL.SetTabContentBgColor.argtypes = [HWND, ctypes.c_int, UINT32]
    DLL.SetTabContentBgColorAll.argtypes = [HWND, UINT32]
    DLL.GetCurrentTabIndex.argtypes = [HWND]
    DLL.GetCurrentTabIndex.restype = ctypes.c_int
    DLL.UpdateTabControlLayout.argtypes = [HWND]
    DLL.RedrawTabControl.argtypes = [HWND]
    DLL.RedrawTabControl.restype = BOOL
    DLL.SetTabCallback.argtypes = [HWND, tab_cb]
    DLL.SetTabClosable.argtypes = [HWND, ctypes.c_int]
    DLL.SetTabClosable.restype = ctypes.c_int
    DLL.SetTabCloseCallback.argtypes = [HWND, tab_close_cb]
    DLL.SetTabCloseCallback.restype = ctypes.c_int
    DLL.RemoveTabItem.argtypes = [HWND, ctypes.c_int]
    DLL.RemoveTabItem.restype = BOOL
    DLL.SelectTab.argtypes = [HWND, ctypes.c_int]
    DLL.SetTabHeaderStyle.argtypes = [HWND, ctypes.c_int]
    DLL.SetTabItemSize.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
    DLL.SetTabPadding.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
    DLL.SetTabColors.argtypes = [HWND, UINT32, UINT32, UINT32, UINT32]
    DLL.SetTabIndicatorColor.argtypes = [HWND, UINT32]

    USER32.RedrawWindow.argtypes = [HWND, ctypes.c_void_p, ctypes.c_void_p, UINT32]
    USER32.RedrawWindow.restype = BOOL

    DLL.CreateMenuBar.argtypes = [HWND]
    DLL.CreateMenuBar.restype = HWND
    DLL.MenuBarAddItem.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    DLL.MenuBarAddSubItem.argtypes = [HWND, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    DLL.SetMenuBarPlacement.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.SetMenuBarCallback.argtypes = [HWND, menu_cb]

    DLL.CreateEmojiPopupMenu.argtypes = [HWND]
    DLL.CreateEmojiPopupMenu.restype = HWND
    DLL.PopupMenuAddItem.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    DLL.PopupMenuAddSubItem.argtypes = [HWND, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    DLL.SetPopupMenuCallback.argtypes = [HWND, menu_cb]
    DLL.BindControlMenu.argtypes = [HWND, HWND]
    DLL.BindButtonMenu.argtypes = [HWND, ctypes.c_int, HWND]
    DLL.SetRightClickCallback.argtypes = [HWND, right_click_cb]
    DLL.SetRightClickCallback.restype = None
    DLL.SetMouseEnterCallback.argtypes = [HWND, value_cb]
    DLL.SetMouseLeaveCallback.argtypes = [HWND, value_cb]

    DLL.SetLayoutManager.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.SetLayoutPadding.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.SetControlLayoutProps.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, BOOL, BOOL]
    DLL.AddControlToLayout.argtypes = [HWND, HWND]
    DLL.RemoveControlFromLayout.argtypes = [HWND, HWND]
    DLL.UpdateLayout.argtypes = [HWND]
    DLL.RemoveLayoutManager.argtypes = [HWND]

    DLL.LoadThemeFromJSON.argtypes = [ctypes.c_void_p, ctypes.c_int]
    DLL.LoadThemeFromJSON.restype = BOOL
    DLL.SetTheme.argtypes = [ctypes.c_void_p, ctypes.c_int]
    DLL.SetDarkMode.argtypes = [BOOL]
    DLL.IsDarkMode.argtypes = []
    DLL.IsDarkMode.restype = BOOL
    DLL.EW_GetThemeColor.argtypes = [ctypes.c_void_p, ctypes.c_int]
    DLL.EW_GetThemeColor.restype = UINT32
    DLL.EW_GetCurrentThemeName.argtypes = [ctypes.c_void_p, ctypes.c_int]
    DLL.EW_GetCurrentThemeName.restype = ctypes.c_int
    DLL.SetThemeChangedCallback.argtypes = [theme_changed_cb]

    DLL.CreateDataGridView.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, BOOL, BOOL, UINT32, UINT32]
    DLL.CreateDataGridView.restype = HWND
    DLL.DataGrid_AddTextColumn.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_AddCheckBoxColumn.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_AddComboBoxColumn.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_AddTagColumn.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_AddRow.argtypes = [HWND]
    DLL.DataGrid_AddRow.restype = ctypes.c_int
    DLL.DataGrid_ClearRows.argtypes = [HWND]
    DLL.DataGrid_SetCellText.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.DataGrid_SetCellChecked.argtypes = [HWND, ctypes.c_int, ctypes.c_int, BOOL]
    DLL.DataGrid_SetCellStyle.argtypes = [HWND, ctypes.c_int, ctypes.c_int, UINT32, UINT32, BOOL, BOOL]
    DLL.DataGrid_SetColumnComboItems.argtypes = [HWND, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.DataGrid_SetColumnHeaderAlignment.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_SetColumnCellAlignment.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_SetVirtualRowCount.argtypes = [HWND, ctypes.c_int]
    DLL.DataGrid_SetVirtualDataCallback.argtypes = [HWND, dg_virtual_cb]
    DLL.DataGrid_SetSelectionMode.argtypes = [HWND, ctypes.c_int]
    DLL.DataGrid_SetShowGridLines.argtypes = [HWND, BOOL]
    DLL.DataGrid_SetDefaultRowHeight.argtypes = [HWND, ctypes.c_int]
    DLL.DataGrid_SetHeaderHeight.argtypes = [HWND, ctypes.c_int]
    DLL.DataGrid_SetDoubleClickEnabled.argtypes = [HWND, BOOL]
    DLL.DataGrid_SetHeaderStyle.argtypes = [HWND, ctypes.c_int]
    DLL.DataGrid_Show.argtypes = [HWND, BOOL]
    DLL.DataGrid_Refresh.argtypes = [HWND]
    DLL.DataGrid_SetColors.argtypes = [HWND, UINT32, UINT32, UINT32, UINT32, UINT32, UINT32, UINT32]
    DLL.DataGrid_SetCellClickCallback.argtypes = [HWND, dg_cb]
    DLL.DataGrid_SetCellDoubleClickCallback.argtypes = [HWND, dg_cb]
    DLL.DataGrid_SetCellValueChangedCallback.argtypes = [HWND, dg_cb]

    DLL.CreateTreeView.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, UINT32, UINT32, ctypes.c_void_p]
    DLL.CreateTreeView.restype = HWND
    DLL.AddRootNode.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.AddRootNode.restype = ctypes.c_int
    DLL.AddChildNode.argtypes = [HWND, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.AddChildNode.restype = ctypes.c_int
    DLL.ExpandNode.argtypes = [HWND, ctypes.c_int]
    DLL.ExpandNode.restype = BOOL
    DLL.SetSelectedNode.argtypes = [HWND, ctypes.c_int]
    DLL.SetSelectedNode.restype = BOOL
    DLL.GetSelectedNode.argtypes = [HWND]
    DLL.GetSelectedNode.restype = ctypes.c_int
    DLL.GetNodeText.argtypes = [HWND, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.GetNodeText.restype = ctypes.c_int
    DLL.SetTreeViewSidebarMode.argtypes = [HWND, BOOL]
    DLL.SetTreeViewSidebarMode.restype = BOOL
    DLL.GetTreeViewSidebarMode.argtypes = [HWND]
    DLL.GetTreeViewSidebarMode.restype = BOOL
    DLL.SetTreeViewRowHeight.argtypes = [HWND, ctypes.c_float]
    DLL.SetTreeViewRowHeight.restype = BOOL
    DLL.SetTreeViewItemSpacing.argtypes = [HWND, ctypes.c_float]
    DLL.SetTreeViewItemSpacing.restype = BOOL
    DLL.SetTreeViewTextColor.argtypes = [HWND, UINT32]
    DLL.SetTreeViewTextColor.restype = BOOL
    DLL.SetTreeViewSelectedBgColor.argtypes = [HWND, UINT32]
    DLL.SetTreeViewSelectedBgColor.restype = BOOL
    DLL.SetTreeViewSelectedForeColor.argtypes = [HWND, UINT32]
    DLL.SetTreeViewSelectedForeColor.restype = BOOL
    DLL.SetTreeViewHoverBgColor.argtypes = [HWND, UINT32]
    DLL.SetTreeViewHoverBgColor.restype = BOOL
    DLL.SetTreeViewFont.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_float, ctypes.c_int, BOOL]
    DLL.SetTreeViewFont.restype = BOOL
    DLL.EnableTreeViewDragDrop.argtypes = [HWND, BOOL]
    DLL.EnableTreeViewDragDrop.restype = BOOL
    DLL.SetTreeViewCallback.argtypes = [HWND, ctypes.c_int, tree_cb]
    DLL.SetTreeViewCallback.restype = BOOL
    DLL.ExpandAll.argtypes = [HWND]
    DLL.ExpandAll.restype = BOOL
    DLL.CollapseAll.argtypes = [HWND]
    DLL.CollapseAll.restype = BOOL
    DLL.FindNodeByText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
    DLL.FindNodeByText.restype = ctypes.c_int
    DLL.ScrollToNode.argtypes = [HWND, ctypes.c_int]
    DLL.ScrollToNode.restype = BOOL

    DLL._ButtonCB = button_cb
    DLL._ConfirmCB = confirm_cb
    DLL._MenuCB = menu_cb
    DLL._TabCB = tab_cb
    DLL._TabCloseCB = tab_close_cb
    DLL._CheckBoxCB = checkbox_cb
    DLL._RadioCB = radio_cb
    DLL._ListBoxCB = listbox_cb
    DLL._ComboCB = combo_cb
    DLL._RightClickCB = right_click_cb
    DLL._ThemeChangedCB = theme_changed_cb
    DLL._ValueCB = value_cb
    DLL._PictureCB = picture_cb
    DLL._ProgressCB = progress_cb
    DLL._SliderCB = slider_cb
    DLL._SwitchCB = switch_cb
    DLL._NotificationCB = notification_cb
    DLL._GridCB = dg_cb
    DLL._GridVirtualCB = dg_virtual_cb
    DLL._TreeCB = tree_cb
    rcb = DLL._RightClickCB(on_right_debug)
    KEEP.append(rcb)
    STATE["right_click_cb"] = rcb
    ccb = DLL._TabCloseCB(on_tab_close)
    KEEP.append(ccb)
    STATE["tab_close_cb"] = ccb
    tcb = DLL._ThemeChangedCB(on_theme_changed)
    KEEP.append(tcb)
    STATE["theme_cb"] = tcb
    DLL.SetThemeChangedCallback(tcb)


def set_status(text: str) -> None:
    print(text)
    h = STATE["status"]
    if h:
        p, n, _ = s(text)
        DLL.SetLabelText(h, p, n)


def getter_text(getter, *args, capacity: int = 128) -> str:
    buf = ctypes.create_string_buffer(capacity)
    size = getter(*args, buf, capacity)
    if size <= 0:
        return ""
    return buf.raw[:size].decode("utf-8", errors="replace")


def theme_name() -> str:
    return getter_text(DLL.EW_GetCurrentThemeName)


def theme_color(name: str) -> int:
    p, n, _ = s(name)
    return int(DLL.EW_GetThemeColor(p, n))


def set_label_text(hwnd: HWND | None, text: str) -> None:
    if not hwnd:
        return
    p, n, _ = s(text)
    DLL.SetLabelText(hwnd, p, n)


def refresh_theme_preview() -> None:
    current = theme_name() or "unknown"
    set_label_text(STATE.get("theme_name_label"), f"🎨 当前主题: {current}")
    set_label_text(
        STATE.get("theme_color_info"),
        f"主色=0x{theme_color('primary'):08X} 背景=0x{theme_color('background'):08X} 文本=0x{theme_color('text_primary'):08X}",
    )


def refresh_current_tab_view() -> None:
    h_tab = STATE.get("main_tab")
    if not h_tab:
        return
    DLL.UpdateTabControlLayout(h_tab)
    DLL.RedrawTabControl(h_tab)


def bind_right_click(hwnd: HWND | None) -> HWND | None:
    cb = STATE.get("right_click_cb")
    if hwnd and cb:
        DLL.SetRightClickCallback(hwnd, cb)
    return hwnd


def bind_right_click_many(*handles: HWND | None) -> None:
    for hwnd in handles:
        bind_right_click(hwnd)


def label(parent: HWND, text: str, x: int, y: int, w: int, h: int, fg=5, bg=13, size=13, bold=False, wrap=False, align=ALIGN_LEFT) -> HWND:
    p, n, _ = s(text)
    return bind_right_click(DLL.CreateLabel(parent, x, y, w, h, p, n, fg, bg, FONT_PTR, FONT_LEN, size, BOOL(bold), BOOL(False), BOOL(False), align, BOOL(wrap)))


def button(
    parent: HWND,
    emoji: str,
    text: str,
    x: int,
    y: int,
    w: int,
    h: int,
    bg: int,
    action,
    *,
    button_type: int = BUTTON_TYPE_AUTO,
    button_style: int = BUTTON_STYLE_SOLID,
    button_size: int = BUTTON_SIZE_DEFAULT,
    round_button: bool = False,
    circle_button: bool = False,
    loading: bool = False,
) -> int:
    host = button_host(parent)
    bounds = button_bounds(parent)
    if bounds:
        group_x, group_y, _, _ = bounds
        x += group_x + 10
        y += group_y + 25
    ep, en, _ = s(emoji)
    tp, tn, _ = s(text)
    bid = DLL.create_emoji_button_bytes(host, ep, en, tp, tn, x, y, w, h, bg)
    if button_type != BUTTON_TYPE_AUTO:
        DLL.SetButtonType(bid, button_type)
    if button_style != BUTTON_STYLE_SOLID:
        DLL.SetButtonStyle(bid, button_style)
    if button_size != BUTTON_SIZE_DEFAULT:
        DLL.SetButtonSize(bid, button_size)
    if round_button:
        DLL.SetButtonRound(bid, BOOL(True))
    if circle_button:
        DLL.SetButtonCircle(bid, BOOL(True))
    if loading:
        DLL.SetButtonLoading(bid, BOOL(True))
    BUTTON_ACTIONS[(hwnd_key(host), bid)] = action
    return bid


def groupbox(parent: HWND, text: str, x: int, y: int, w: int, h: int) -> HWND:
    p, n, _ = s(text)
    g = DLL.CreateGroupBox(parent, x, y, w, h, p, n, 10, 14, FONT_PTR, FONT_LEN, 14, BOOL(True), BOOL(False), BOOL(False))
    DLL.SetGroupBoxStyle(g, GROUPBOX_STYLE_CARD)
    DLL.SetGroupBoxTitleColor(g, 5)
    GROUPBOX_HOSTS[hwnd_key(g)] = parent
    GROUPBOX_BOUNDS[hwnd_key(g)] = (x, y, w, h)
    return bind_right_click(g)


def edit(parent: HWND, text: str, x: int, y: int, w: int, h: int, color_emoji=False) -> HWND:
    p, n, _ = s(text)
    fn = DLL.CreateColorEmojiEditBox if color_emoji else DLL.CreateEditBox
    return bind_right_click(fn(parent, x, y, w, h, p, n, 5, 13, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False), ALIGN_LEFT, BOOL(False), BOOL(False), BOOL(False), BOOL(True), BOOL(True)))


def add_tab(tab: HWND, title: str) -> HWND:
    p, n, _ = s(title)
    idx = DLL.AddTabItem(tab, p, n, HWND())
    return bind_right_click(DLL.GetTabContentWindow(tab, idx))


def show_msg(title: str, text: str, icon: str = "ℹ️") -> None:
    tp, tn, _ = s(title)
    mp, mn, _ = s(text)
    ip, inn, _ = s(icon)
    DLL.show_message_box_bytes(STATE["hwnd"], tp, tn, mp, mn, ip, inn)


def show_confirm(title: str, text: str, icon: str = "❓") -> None:
    tp, tn, _ = s(title)
    mp, mn, _ = s(text)
    ip, inn, _ = s(icon)
    DLL.show_confirm_box_bytes(STATE["hwnd"], tp, tn, mp, mn, ip, inn, STATE["confirm_cb"])


def list_item_text(h: HWND, index: int) -> str:
    size = DLL.GetListItemText(h, index, None, 0)
    if size <= 0:
        return ""
    buf = ctypes.create_string_buffer(size)
    DLL.GetListItemText(h, index, buf, size)
    return buf.raw[:size].decode("utf-8", errors="replace")


def dt_text(h: HWND) -> str:
    y = ctypes.c_int()
    mo = ctypes.c_int()
    d = ctypes.c_int()
    hh = ctypes.c_int()
    mm = ctypes.c_int()
    ss = ctypes.c_int()
    DLL.GetD2DDateTimePickerDateTime(h, ctypes.byref(y), ctypes.byref(mo), ctypes.byref(d), ctypes.byref(hh), ctypes.byref(mm), ctypes.byref(ss))
    return f"{y.value:04d}-{mo.value:02d}-{d.value:02d} {hh.value:02d}:{mm.value:02d}:{ss.value:02d}"


def select_main_tab(index: int) -> None:
    DLL.SelectTab(STATE["main_tab"], index)


def tab_style_name(style: int) -> str:
    return {
        TAB_HEADER_STYLE_LINE: "Line",
        TAB_HEADER_STYLE_CARD: "Card",
        TAB_HEADER_STYLE_CARD_PLAIN: "Card Plain",
        TAB_HEADER_STYLE_SEGMENTED: "Segmented",
    }.get(style, f"Unknown({style})")


def apply_demo_tab_style(style: int) -> None:
    for key in ("tab_style_demo", "tab_style_secondary"):
        h = STATE.get(key)
        if h:
            DLL.SetTabHeaderStyle(h, style)
            DLL.UpdateTabControlLayout(h)
            DLL.RedrawTabControl(h)
    set_status(f"TabControl demo style -> {tab_style_name(style)}")


def tree_text(h: HWND, node_id: int) -> str:
    size = DLL.GetNodeText(h, node_id, None, 0)
    if size <= 0:
        return f"node#{node_id}"
    buf = ctypes.create_string_buffer(size)
    DLL.GetNodeText(h, node_id, buf, size)
    return buf.raw[:size].decode("utf-8", errors="replace")


def add_tree_root(h: HWND, text: str, icon: str) -> int:
    tp, tn, _ = s(text)
    ip, inn, _ = s(icon)
    return int(DLL.AddRootNode(h, tp, tn, ip, inn))


def add_tree_child(h: HWND, parent_id: int, text: str, icon: str) -> int:
    tp, tn, _ = s(text)
    ip, inn, _ = s(icon)
    return int(DLL.AddChildNode(h, parent_id, tp, tn, ip, inn))


def update_tree_status(text: str) -> None:
    set_label_text(STATE.get("tree_status_label"), text)
    set_status(text)


def on_tree_event(event_name: str, h_tree: HWND, node_id: int) -> None:
    update_tree_status(f"🌲 {event_name}: {tree_text(h_tree, node_id)} (node={node_id})")


def bind_tree_event(h_tree: HWND, event_id: int, event_name: str) -> None:
    cb = DLL._TreeCB(lambda node_id, _ctx, tree=h_tree, name=event_name: on_tree_event(name, tree, node_id))
    KEEP.append(cb)
    DLL.SetTreeViewCallback(h_tree, event_id, cb)


def populate_demo_tree(h_tree: HWND, title: str) -> None:
    workspace = add_tree_root(h_tree, f"{title} 工作区", "📁")
    dashboard = add_tree_child(h_tree, workspace, "概览看板", "📊")
    add_tree_child(h_tree, workspace, "消息中心", "🔔")
    assets = add_tree_root(h_tree, f"{title} 资源库", "🗂️")
    add_tree_child(h_tree, assets, "图片素材", "🖼️")
    docs = add_tree_child(h_tree, assets, "文档归档", "📝")
    add_tree_child(h_tree, docs, "周报 2026", "📄")
    favorites = add_tree_root(h_tree, f"{title} 收藏夹", "⭐")
    add_tree_child(h_tree, favorites, "Element 风格", "🎨")
    add_tree_child(h_tree, favorites, "TabControl 调试", "🧪")
    DLL.ExpandAll(h_tree)
    DLL.SetSelectedNode(h_tree, dashboard)


def set_rating(value: int) -> None:
    value = max(0, min(5, value))
    STATE["rating_value"] = value
    filled = "★" * value
    empty = "☆" * (5 - value)
    set_label_text(STATE.get("rating_label"), f"⭐ 当前评分: {filled}{empty}  ({value}/5)")
    set_status(f"评分演示 -> {value}/5")


def toggle_primary_tree_sidebar() -> None:
    h_tree = STATE.get("tree_primary")
    if not h_tree:
        return
    enabled = not bool(STATE.get("tree_sidebar_enabled", True))
    STATE["tree_sidebar_enabled"] = enabled
    DLL.SetTreeViewSidebarMode(h_tree, BOOL(enabled))
    update_tree_status(f"🌲 主树侧边栏模式 -> {'ON' if enabled else 'OFF'}")


def on_button_click(button_id: int, parent: HWND) -> None:
    action = BUTTON_ACTIONS.get((hwnd_key(parent), button_id))
    if action:
        action()
    else:
        set_status(f"🖱️ 按钮 {button_id} 被点击，父窗口={hwnd_key(parent)}。")


def on_confirm(value: int) -> None:
    set_status("✅ ConfirmBox 回调: 已确认。" if value else "❎ ConfirmBox 回调: 已取消。")


def on_menu(menu_id: int, item_id: int) -> None:
    del menu_id
    if item_id == 1010:
        set_status("文件 -> 对话框：可继续选择消息框或确认框。")
    elif item_id == 1011:
        set_status("文件 -> 跳转页签：可继续选择要切换的页签。")
    elif item_id == 1012:
        set_status("文件 -> 树形框动作：可继续选择展开、折叠或侧边栏。")
    elif item_id == 1013:
        set_status("文件 -> 评分动作：可继续选择评分。")
    elif item_id == 2901:
        set_status("窗口右键菜单 -> 窗口动作：可继续选择查看状态或弹消息框。")
    elif item_id == 2902:
        set_status("窗口右键菜单 -> 快速跳转：可继续选择要切换的页签。")
    elif item_id == 2903:
        set_status("窗口右键菜单 -> 树形框：可继续选择展开、折叠或侧边栏。")
    elif item_id == 2904:
        set_status("窗口右键菜单 -> 评分：可继续选择评分动作。")
    elif item_id == MENU_MSG:
        show_msg("菜单栏测试", "你点击了菜单栏中的消息框。", "🧭")
        set_status("MenuBar: 已触发消息框。")
    elif item_id == MENU_CONFIRM:
        show_confirm("菜单栏确认", "这是从 MenuBar 打开的 ConfirmBox。", "🧩")
        set_status("MenuBar: 已触发确认框。")
    elif item_id == MENU_TAB_BASIC:
        select_main_tab(TAB_BASIC)
    elif item_id == MENU_TAB_SELECT:
        select_main_tab(TAB_SELECT)
    elif item_id == MENU_TAB_DATA:
        select_main_tab(TAB_DATA)
    elif item_id == MENU_TAB_TABS:
        select_main_tab(TAB_TABS)
    elif item_id == MENU_TAB_LAYOUT:
        select_main_tab(TAB_LAYOUT)
    elif item_id == MENU_TAB_THEME:
        select_main_tab(TAB_THEME)
    elif item_id == MENU_TAB_MENU_TREE:
        select_main_tab(TAB_MENU_TREE)
    elif item_id == MENU_TAB_TAB_STYLES:
        select_main_tab(TAB_TAB_STYLES)
    elif item_id in (MENU_TREE_EXPAND, POP_TREE_EXPAND):
        h_tree = STATE.get("tree_primary")
        if h_tree:
            DLL.ExpandAll(h_tree)
            update_tree_status("🌲 主树已全部展开")
    elif item_id in (MENU_TREE_COLLAPSE, POP_TREE_COLLAPSE):
        h_tree = STATE.get("tree_primary")
        if h_tree:
            DLL.CollapseAll(h_tree)
            update_tree_status("🌲 主树已全部折叠")
    elif item_id in (MENU_TREE_TOGGLE_SIDEBAR, POP_TREE_TOGGLE_SIDEBAR):
        toggle_primary_tree_sidebar()
    elif item_id in (MENU_RATING_CLEAR, POP_RATING_CLEAR):
        set_rating(0)
    elif item_id == MENU_RATING_1:
        set_rating(1)
    elif item_id in (MENU_RATING_3, POP_RATING_3):
        set_rating(3)
    elif item_id in (MENU_RATING_5, POP_RATING_5):
        set_rating(5)
    elif item_id == POP_WINDOW_STATUS:
        set_status("窗口右键菜单: 当前窗口正在运行。")
    elif item_id == POP_WINDOW_MSG:
        show_msg("窗口右键菜单", "你从窗口空白区域打开了这个消息框。", "🪟")
        set_status("窗口右键菜单: 已弹出消息框。")
    elif item_id == POP_PAGE_STATUS:
        set_status("Tab 页内容右键菜单: 当前命中的是页内容窗口句柄。")
    elif item_id == POP_PAGE_MSG:
        show_msg("Tab 页右键菜单", "这是绑定在 Tab 页内容窗口上的菜单。", "🗂️")
        set_status("Tab 页内容右键菜单: 已弹出消息框。")
    elif item_id == POP_GROUP_STATUS:
        set_status("GroupBox 右键菜单: 当前命中的是分组框句柄。")
    elif item_id == POP_GROUP_MSG:
        show_msg("分组框右键菜单", "这是绑定在 GroupBox 句柄上的菜单。", "📦")
        set_status("GroupBox 右键菜单: 已弹出消息框。")
    elif item_id == POP_TAB_STATUS:
        set_status("TabControl 右键菜单: 当前命中的是 TabControl 句柄。")
    elif item_id == POP_TAB_MSG:
        show_msg("TabControl 右键菜单", "这是绑定在 TabControl 句柄上的菜单。", "🧷")
        set_status("TabControl 右键菜单: 已弹出消息框。")
    elif item_id == POP_GRID_ADD:
        add_grid_row()
        set_status("表格右键菜单: 已添加一行。")
    elif item_id == POP_GRID_STATUS:
        set_status(f"表格右键菜单: 当前共有 {STATE['row_count']} 行。")
    elif item_id == POP_BUTTON_STATUS:
        set_status("按钮右键菜单: 绑定正常。")
    elif item_id == POP_CHECKBOX_TOGGLE:
        h = STATE["checkbox"]
        current = bool(DLL.GetCheckBoxState(h))
        DLL.SetCheckBoxState(h, BOOL(not current))
        set_status(f"复选框右键菜单: 已切换为 {'选中' if not current else '未选中'}。")


def on_main_tab(h: HWND, idx: int) -> None:
    del h
    names = ["基础组件", "选择组件", "数据组件", "页签与弹窗", "布局器演示", "主题换肤"]
    set_status(f"主 TabControl 已切换到: {names[idx]}")


def on_nested_tab(h: HWND, idx: int) -> None:
    del h
    set_status(f"嵌套 TabControl 已切换到第 {idx + 1} 页。")


def on_checkbox(h: HWND, checked: BOOL) -> None:
    del h
    set_status(f"CheckBox 状态变化: {'选中' if checked else '未选中'}")


def on_radio(h: HWND, gid: int, checked: BOOL) -> None:
    del h
    if checked:
        set_status(f"RadioButton 已选中，分组 {gid}。")


def on_listbox(h: HWND, idx: int) -> None:
    set_status(f"ListBox 选中: {idx} {list_item_text(h, idx) if idx >= 0 else ''}")


def on_combo(h: HWND, idx: int) -> None:
    del h
    set_status(f"ComboBox 选择变化: {idx}")


def on_d2d_combo(h: HWND, idx: int) -> None:
    del h
    set_status(f"D2DComboBox 选择变化: {idx}")


def on_right_debug(h: HWND, x: int, y: int) -> None:
    set_status(f"🖱️ 右键句柄=0x{hwnd_key(h):X} 坐标=({x}, {y})")


def on_theme_changed(name_bytes) -> None:
    name = (name_bytes or b"").decode("utf-8", errors="replace") or "unknown"
    refresh_theme_preview()
    set_status(f"🎨 主题已切换: {name}")


def on_dt(h: HWND) -> None:
    set_status(f"D2DDateTimePicker 变化: {dt_text(h)}")


def on_picture(h: HWND) -> None:
    del h
    set_status("PictureBox 被点击。")


def on_progress(h: HWND, value: int) -> None:
    del h
    set_status(f"📊 ProgressBar 当前值: {value}")


def on_grid_click(h: HWND, row: int, col: int) -> None:
    del h
    set_status(f"🧾 DataGridView 单击: row={row}, col={col}")


def on_grid_dblclick(h: HWND, row: int, col: int) -> None:
    del h
    set_status(f"🧾 DataGridView 双击: row={row}, col={col}")


def on_grid_change(h: HWND, row: int, col: int) -> None:
    del h
    set_status(f"🧾 DataGridView 值变化: row={row}, col={col}")


def grid_headers() -> tuple[str, ...]:
    return ("🧾 任务", "☑️ 启用", "🚦 状态", "🏷️ 标签", "📝 备注")


def apply_grid_alignment(h: HWND, header_align: int | None = None, cell_align: int | None = None) -> None:
    if not h:
        return
    for col in range(len(grid_headers())):
        if header_align is not None:
            DLL.DataGrid_SetColumnHeaderAlignment(h, col, header_align)
        if cell_align is not None:
            DLL.DataGrid_SetColumnCellAlignment(h, col, cell_align)
    DLL.DataGrid_Refresh(h)


def apply_grid_theme(h: HWND) -> None:
    if not h:
        return
    DLL.DataGrid_SetColors(
        h,
        THEME_TEXT,
        THEME_BG,
        THEME_SURFACE,
        THEME_TEXT,
        THEME_SURFACE_PRIMARY,
        THEME_SURFACE,
        THEME_BORDER_LIGHT,
    )


def alignment_name(value: int) -> str:
    return {ALIGN_LEFT: "左对齐", ALIGN_CENTER: "居中", ALIGN_RIGHT: "右对齐"}.get(value, f"未知({value})")


def next_alignment(value: int) -> int:
    return {ALIGN_LEFT: ALIGN_CENTER, ALIGN_CENTER: ALIGN_RIGHT}.get(value, ALIGN_LEFT)


def build_virtual_grid_text(row: int, col: int) -> str:
    statuses = ("🕒 待处理", "🚧 进行中", "✅ 已完成", "⏸️ 已暂停")
    priorities = ("🔵 P1", "🟢 P2", "🟠 P3", "🟣 P4")
    if col == 0:
        return f"🧾 虚拟任务 {row + 1:,}"
    if col == 1:
        return f"☑️ {statuses[row % len(statuses)]}"
    if col == 2:
        return priorities[(row // 3) % len(priorities)]
    if col == 3:
        return f"👤 节点 {row % 256:03d}"
    return f"🧪 第 {row + 1:,} 行虚拟备注，用于测试 1,000,000 行滚动与绘制性能"


def on_virtual_grid_request(h: HWND, row: int, col: int, buffer, buffer_size: int) -> int:
    del h
    raw = build_virtual_grid_text(row, col).encode("utf-8")
    if not buffer or buffer_size <= 0:
        return len(raw)
    copied = min(len(raw), buffer_size)
    ctypes.memmove(buffer, raw, copied)
    return copied


def progress_minus() -> None:
    h = STATE["progress"]
    current = DLL.GetProgressValue(h)
    value = max(0, current - 10)
    DLL.SetProgressValue(h, value)
    set_status(f"📉 ProgressBar 已更新为 {value}%")


def progress_plus() -> None:
    h = STATE["progress"]
    current = DLL.GetProgressValue(h)
    value = 0 if current >= 100 else min(100, current + 10)
    DLL.SetProgressValue(h, value)
    set_status(f"📈 ProgressBar 已更新为 {value}%")


def progress_reset() -> None:
    h = STATE["progress"]
    DLL.SetProgressValue(h, 35)
    set_status("🔄 ProgressBar 已重置为 35%")


def toggle_checkbox() -> None:
    h = STATE["checkbox"]
    current = bool(DLL.GetCheckBoxState(h))
    DLL.SetCheckBoxState(h, BOOL(not current))
    set_status(f"☑️ CheckBox 已切换为 {'选中' if not current else '未选中'}。")


def toggle_demo_loading() -> None:
    button_id = STATE.get("button_loading_demo")
    if not button_id:
        return
    active = not bool(STATE.get("button_loading_active", False))
    STATE["button_loading_active"] = active
    DLL.SetButtonLoading(int(button_id), BOOL(active))
    set_status(f"Button loading demo -> {'ON' if active else 'OFF'}")


def set_layout_mode(mode: str) -> None:
    host = STATE.get("layout_host")
    controls = list(STATE.get("layout_controls", []))
    if not host or not controls:
        return

    STATE["layout_mode"] = mode
    DLL.RemoveLayoutManager(host)

    if mode == "flow_h":
        DLL.SetLayoutManager(host, LAYOUT_FLOW_HORIZONTAL, 0, 0, 12)
        DLL.SetLayoutPadding(host, 18, 42, 18, 18)
        for ctrl in controls:
            DLL.AddControlToLayout(host, ctrl)
            DLL.SetControlLayoutProps(ctrl, 0, 0, 0, 0, DOCK_NONE, BOOL(False), BOOL(False))
        set_status("📐 布局器: 已切到水平流式布局。")
    elif mode == "flow_v":
        DLL.SetLayoutManager(host, LAYOUT_FLOW_VERTICAL, 0, 0, 12)
        DLL.SetLayoutPadding(host, 18, 42, 18, 18)
        for ctrl in controls:
            DLL.AddControlToLayout(host, ctrl)
            DLL.SetControlLayoutProps(ctrl, 0, 0, 0, 0, DOCK_NONE, BOOL(True), BOOL(False))
        set_status("📐 布局器: 已切到垂直流式布局。")
    elif mode == "grid":
        DLL.SetLayoutManager(host, LAYOUT_GRID, 2, 3, 12)
        DLL.SetLayoutPadding(host, 18, 42, 18, 18)
        for ctrl in controls:
            DLL.AddControlToLayout(host, ctrl)
            DLL.SetControlLayoutProps(ctrl, 0, 0, 0, 0, DOCK_NONE, BOOL(True), BOOL(True))
        set_status("📐 布局器: 已切到 2x3 网格布局。")
    else:
        DLL.SetLayoutManager(host, LAYOUT_DOCK, 0, 0, 10)
        DLL.SetLayoutPadding(host, 18, 42, 18, 18)
        top_label, search_box, city_combo, fruit_list, progress_bar, memo_box = controls
        for ctrl in controls:
            DLL.AddControlToLayout(host, ctrl)
        DLL.SetControlLayoutProps(top_label, 0, 0, 0, 0, DOCK_TOP, BOOL(True), BOOL(False))
        DLL.SetControlLayoutProps(search_box, 0, 0, 0, 0, DOCK_TOP, BOOL(True), BOOL(False))
        DLL.SetControlLayoutProps(city_combo, 0, 0, 0, 0, DOCK_RIGHT, BOOL(False), BOOL(False))
        DLL.SetControlLayoutProps(fruit_list, 0, 0, 0, 0, DOCK_LEFT, BOOL(False), BOOL(True))
        DLL.SetControlLayoutProps(progress_bar, 0, 0, 0, 0, DOCK_BOTTOM, BOOL(True), BOOL(False))
        DLL.SetControlLayoutProps(memo_box, 0, 0, 0, 0, DOCK_FILL, BOOL(True), BOOL(True))
        set_status("📐 布局器: 已切到停靠布局。")

    DLL.UpdateLayout(host)


def apply_builtin_theme(name: str) -> None:
    p, n, _ = s(name)
    DLL.SetTheme(p, n)
    if STATE.get("main_tab"):
        DLL.SetTabContentBgColorAll(STATE["main_tab"], 13)
    refresh_theme_preview()


def apply_dark_mode(enabled: bool) -> None:
    DLL.SetDarkMode(BOOL(enabled))
    if STATE.get("main_tab"):
        DLL.SetTabContentBgColorAll(STATE["main_tab"], 13)
    refresh_theme_preview()
    set_status(f"🎨 DarkMode 已{'开启' if enabled else '关闭'}。")


def apply_custom_theme(name: str, dark_mode: bool, primary: str, success: str, warning: str, danger: str, info: str, background: str, background_light: str, text_primary: str) -> None:
    json_text = (
        "{"
        f"\"name\":\"{name}\","
        f"\"dark_mode\":{'true' if dark_mode else 'false'},"
        f"\"primary\":\"{primary}\","
        f"\"success\":\"{success}\","
        f"\"warning\":\"{warning}\","
        f"\"danger\":\"{danger}\","
        f"\"info\":\"{info}\","
        f"\"background\":\"{background}\","
        f"\"background_light\":\"{background_light}\","
        f"\"text_primary\":\"{text_primary}\""
        "}"
    )
    p, n, _ = s(json_text)
    if DLL.LoadThemeFromJSON(p, n):
        if STATE.get("main_tab"):
            DLL.SetTabContentBgColorAll(STATE["main_tab"], 13)
        refresh_theme_preview()
        set_status(f"🎨 已加载自定义主题: {name}")
    else:
        set_status(f"❌ 自定义主题加载失败: {name}")


def basic_page(page: HWND) -> tuple[HWND, int]:
    basic_group = groupbox(page, "🧩 文本、按钮、编辑框", 16, 16, 718, 330)
    STATE["group_basic_text"] = basic_group
    label(page, "🧩 Label / Button / EditBox / ColorEmojiEditBox / MessageBox / ConfirmBox", 36, 54, 640, 24, size=15, bold=True)
    label(page, "📝 基础页用于集中检查文字、按钮和两个编辑框组件。", 36, 84, 460, 22, fg=0xFF606266)
    label(page, "📄 普通 Label 支持多行与中文显示。", 36, 118, 360, 24)
    edit(page, "📝 普通 EditBox，可直接输入文本。", 36, 164, 300, 36, False)
    edit(page, "🌈 ColorEmojiEditBox 😊🚀 用于测试彩色 emoji 文本。", 356, 164, 340, 36, True)
    button(basic_group, "🖱️", "按钮点击测试", 10, 181, 170, 38, 0xFF409EFF, lambda: set_status("🖱️ Emoji 按钮点击成功。"))
    button(basic_group, "💬", "显示信息框", 196, 181, 170, 38, 0xFF67C23A, lambda: (show_msg("📦 MessageBox 测试", "🧩 这是综合总测页触发的信息框。", "📦"), set_status("💬 已打开 MessageBox。")))
    button(basic_group, "❓", "显示确认框", 382, 181, 170, 38, 0xFFE6A23C, lambda: (show_confirm("🧭 ConfirmBox 测试", "🧪 请确认你已经看到基础组件区域。", "❓"), set_status("❓ 已打开 ConfirmBox。")))

    select_group = groupbox(page, "🎛️ 勾选、单选、进度条", 752, 16, 718, 330)
    STATE["group_basic_select"] = select_group
    label(page, "🎛️ CheckBox / RadioButton / ProgressBar", 772, 54, 420, 24, size=15, bold=True)
    label(page, "👀 点击复选框、单选框或下方控制按钮，观察状态回调。", 772, 84, 460, 22, fg=0xFF606266)
    c1p, c1n, _ = s("☑️ 启用高级模式")
    c2p, c2n, _ = s("🪵 显示调试输出")
    r1p, r1n, _ = s("🅰️ 方案 A")
    r2p, r2n, _ = s("🅱️ 方案 B")
    c1 = DLL.CreateCheckBox(page, 772, 126, 220, 32, c1p, c1n, BOOL(True), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    c2 = DLL.CreateCheckBox(page, 772, 162, 220, 32, c2p, c2n, BOOL(False), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    r1 = DLL.CreateRadioButton(page, 1016, 126, 220, 32, r1p, r1n, 1, BOOL(True), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    r2 = DLL.CreateRadioButton(page, 1016, 162, 220, 32, r2p, r2n, 1, BOOL(False), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    prog = DLL.CreateProgressBar(page, 772, 220, 420, 28, 35, THEME_PRIMARY, THEME_BORDER_LIGHT, BOOL(True), THEME_TEXT)
    DLL.SetProgressBarTextColor(prog, THEME_TEXT)
    bind_right_click_many(c1, c2, r1, r2, prog)
    DLL.SetProgressBarShowText(prog, BOOL(True))
    STATE["checkbox"] = c1
    STATE["progress"] = prog

    cb1 = DLL._CheckBoxCB(on_checkbox)
    rb1 = DLL._RadioCB(on_radio)
    pb1 = DLL._ProgressCB(on_progress)
    KEEP.extend([cb1, rb1, pb1])
    DLL.SetCheckBoxCallback(c1, cb1)
    DLL.SetCheckBoxCallback(c2, cb1)
    DLL.SetRadioButtonCallback(r1, rb1)
    DLL.SetRadioButtonCallback(r2, rb1)
    DLL.SetProgressBarCallback(prog, pb1)
    button(select_group, "🔻", "进度 -10", 450, 160, 118, 34, 0xFF909399, progress_minus)
    button(select_group, "📈", "进度 +10", 576, 160, 118, 34, 0xFF409EFF, progress_plus)
    button(select_group, "🔄", "重置进度", 450, 202, 118, 34, 0xFF67C23A, progress_reset)
    test_btn = button(select_group, "☑️", "切换勾选", 576, 202, 118, 34, 0xFFE6A23C, toggle_checkbox)

    groupbox(page, "📌 说明", 16, 362, 1454, 126)
    label(page, "📌 这个综合示例会保持窗口常驻，便于逐项点击测试。", 36, 404, 500, 24)
    label(page, "🗂️ 菜单栏在窗口顶部，主 TabControl 在中间，GroupBox 用于分区。", 36, 434, 620, 24)
    label(page, "🧰 后续页还包含 ListBox、ComboBox、D2DDateTimePicker、PictureBox、DataGridView、PopupMenu。", 36, 464, 920, 24, fg=0xFF606266)
    return button_host(select_group), test_btn


def basic_page(page: HWND) -> tuple[HWND, int]:
    basic_group = groupbox(page, "📝 文本、按钮、编辑框", 16, 16, 718, 330)
    STATE["group_basic_text"] = basic_group
    label(page, "📝 Label / Button / EditBox / ColorEmojiEditBox / MessageBox / ConfirmBox", 36, 54, 640, 24, size=15, bold=True)
    label(page, "基础页保留原始输入与弹窗演示，并新增一整块 Button 样式扩展示例。", 36, 84, 620, 22, fg=0xFF606266)
    label(page, "📋 普通 Label 仍用于检查多行中文与 emoji 文本显示。", 36, 118, 360, 24)
    edit(page, "📑 普通 EditBox，可直接输入文本。", 36, 164, 300, 36, False)
    edit(page, "🌈 ColorEmojiEditBox 😉🎌 用于测试彩色 emoji 文本。", 356, 164, 340, 36, True)
    button(basic_group, "🖱️", "按钮点击测试", 10, 181, 170, 38, 0xFF409EFF, lambda: set_status("🖱️ Emoji 按钮点击成功。"))
    button(
        basic_group,
        "🔔",
        "显示消息框",
        196,
        181,
        170,
        38,
        0xFF67C23A,
        lambda: (show_msg("📝 MessageBox 测试", "📝 这是综合测试页触发的消息框。", "📝"), set_status("🔔 已打开 MessageBox。")),
    )
    button(
        basic_group,
        "❓",
        "显示确认框",
        382,
        181,
        170,
        38,
        0xFFE6A23C,
        lambda: (show_confirm("📣 ConfirmBox 测试", "🧪 请确认你已经看到基础组件区域。", "❓"), set_status("❓ 已打开 ConfirmBox。")),
    )

    select_group = groupbox(page, "🎛️ 勾选、单选、进度条", 752, 16, 718, 330)
    STATE["group_basic_select"] = select_group
    label(page, "🎛️ CheckBox / RadioButton / ProgressBar", 772, 54, 420, 24, size=15, bold=True)
    label(page, "点击复选框、单选框或下方控制按钮，观察状态回调。", 772, 84, 460, 22, fg=0xFF606266)
    c1p, c1n, _ = s("☑️ 启用高级模式")
    c2p, c2n, _ = s("🪔 显示调试输出")
    r1p, r1n, _ = s("🅰️ 方案 A")
    r2p, r2n, _ = s("🅱️ 方案 B")
    c1 = DLL.CreateCheckBox(page, 772, 126, 220, 32, c1p, c1n, BOOL(True), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    c2 = DLL.CreateCheckBox(page, 772, 162, 220, 32, c2p, c2n, BOOL(False), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    r1 = DLL.CreateRadioButton(page, 1016, 126, 220, 32, r1p, r1n, 1, BOOL(True), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    r2 = DLL.CreateRadioButton(page, 1016, 162, 220, 32, r2p, r2n, 1, BOOL(False), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    prog = DLL.CreateProgressBar(page, 772, 220, 420, 28, 35, THEME_PRIMARY, THEME_BORDER_LIGHT, BOOL(True), THEME_TEXT)
    DLL.SetProgressBarTextColor(prog, THEME_TEXT)
    bind_right_click_many(c1, c2, r1, r2, prog)
    DLL.SetProgressBarShowText(prog, BOOL(True))
    STATE["checkbox"] = c1
    STATE["progress"] = prog

    cb1 = DLL._CheckBoxCB(on_checkbox)
    rb1 = DLL._RadioCB(on_radio)
    pb1 = DLL._ProgressCB(on_progress)
    KEEP.extend([cb1, rb1, pb1])
    DLL.SetCheckBoxCallback(c1, cb1)
    DLL.SetCheckBoxCallback(c2, cb1)
    DLL.SetRadioButtonCallback(r1, rb1)
    DLL.SetRadioButtonCallback(r2, rb1)
    DLL.SetProgressBarCallback(prog, pb1)
    button(select_group, "🔾", "进度 -10", 450, 160, 118, 34, 0xFF909399, progress_minus)
    button(select_group, "📈", "进度 +10", 576, 160, 118, 34, 0xFF409EFF, progress_plus)
    button(select_group, "🔁", "重置进度", 450, 202, 118, 34, 0xFF67C23A, progress_reset)
    test_btn = button(select_group, "☑️", "切换勾选", 576, 202, 118, 34, 0xFFE6A23C, toggle_checkbox)

    style_group = groupbox(page, "🧩 Button 扩展示例", 16, 362, 1454, 252)
    STATE["group_basic_button_styles"] = style_group
    label(page, "🧩 新增按钮属性：Type / Style / Size / Round / Circle / Loading", 36, 400, 760, 24, size=15, bold=True)
    label(page, "这一组集中展示预设类型、朴素、文字、链接、圆角、圆形、加载态和尺寸。", 36, 430, 860, 22, fg=0xFF606266)

    row1_y = 88
    button(style_group, "", "Default", 12, row1_y, 124, 34, 0xFFFFFFFF, lambda: set_status("Button demo -> Default"), button_type=BUTTON_TYPE_DEFAULT)
    button(style_group, "", "Primary", 148, row1_y, 124, 34, 0xFF409EFF, lambda: set_status("Button demo -> Primary"), button_type=BUTTON_TYPE_PRIMARY)
    button(style_group, "", "Success", 284, row1_y, 124, 34, 0xFF67C23A, lambda: set_status("Button demo -> Success"), button_type=BUTTON_TYPE_SUCCESS)
    button(style_group, "", "Warning", 420, row1_y, 124, 34, 0xFFE6A23C, lambda: set_status("Button demo -> Warning"), button_type=BUTTON_TYPE_WARNING)
    button(style_group, "", "Danger", 556, row1_y, 124, 34, 0xFFF56C6C, lambda: set_status("Button demo -> Danger"), button_type=BUTTON_TYPE_DANGER)
    button(style_group, "", "Info", 692, row1_y, 124, 34, 0xFF909399, lambda: set_status("Button demo -> Info"), button_type=BUTTON_TYPE_INFO)

    row2_y = 136
    button(style_group, "✨", "Plain", 12, row2_y, 124, 34, 0xFF409EFF, lambda: set_status("Button demo -> Plain"), button_type=BUTTON_TYPE_PRIMARY, button_style=BUTTON_STYLE_PLAIN)
    button(style_group, "", "Text", 148, row2_y, 124, 34, 0xFF409EFF, lambda: set_status("Button demo -> Text"), button_type=BUTTON_TYPE_PRIMARY, button_style=BUTTON_STYLE_TEXT)
    button(style_group, "", "Link", 284, row2_y, 124, 34, 0xFF409EFF, lambda: set_status("Button demo -> Link"), button_type=BUTTON_TYPE_PRIMARY, button_style=BUTTON_STYLE_LINK)
    button(style_group, "🔵", "Round", 420, row2_y, 136, 34, 0xFF409EFF, lambda: set_status("Button demo -> Round"), button_type=BUTTON_TYPE_PRIMARY, round_button=True)
    button(style_group, "⭐", "", 572, row2_y, 40, 40, 0xFF67C23A, lambda: set_status("Button demo -> Circle"), button_type=BUTTON_TYPE_SUCCESS, circle_button=True)
    STATE["button_loading_demo"] = button(
        style_group,
        "",
        "Loading",
        628,
        row2_y,
        128,
        34,
        0xFF409EFF,
        lambda: None,
        button_type=BUTTON_TYPE_PRIMARY,
        loading=True,
    )
    STATE["button_loading_active"] = True
    button(style_group, "↻", "切换 Loading", 772, row2_y, 148, 34, 0xFF909399, toggle_demo_loading, button_type=BUTTON_TYPE_INFO, button_style=BUTTON_STYLE_PLAIN)

    row3_y = 184
    button(style_group, "", "Large", 12, row3_y, 136, 40, 0xFF409EFF, lambda: set_status("Button demo -> Large"), button_type=BUTTON_TYPE_PRIMARY, button_size=BUTTON_SIZE_LARGE)
    button(style_group, "", "Default", 164, row3_y, 124, 34, 0xFF409EFF, lambda: set_status("Button demo -> Default Size"), button_type=BUTTON_TYPE_PRIMARY)
    button(style_group, "", "Small", 304, row3_y, 112, 28, 0xFF409EFF, lambda: set_status("Button demo -> Small"), button_type=BUTTON_TYPE_PRIMARY, button_size=BUTTON_SIZE_SMALL)
    button(style_group, "🧪", "Auto Color", 432, row3_y, 138, 34, 0xFF8E44AD, lambda: set_status("Button demo -> Auto custom color"))
    button(style_group, "🫧", "Plain Auto", 586, row3_y, 138, 34, 0xFF8E44AD, lambda: set_status("Button demo -> Plain custom color"), button_style=BUTTON_STYLE_PLAIN)

    tips_group = groupbox(page, "📌 说明", 16, 630, 1454, 120)
    STATE["group_basic_tips"] = tips_group
    label(page, "📌 本页现在同时保留原始基础组件和新的 Button 扩展样式演示，方便集中回归。", 36, 668, 820, 24)
    label(page, "🧭 新按钮样式统一放在“Button 扩展示例”分组里，便于对照查看 type/style/size/状态差异。", 36, 698, 980, 24)
    label(page, "📦 后续页仍包含 ListBox、ComboBox、D2DDateTimePicker、PictureBox、DataGridView、PopupMenu 等综合示例。", 36, 728, 1000, 24, fg=0xFF606266)
    return button_host(select_group), test_btn


def select_page(page: HWND) -> None:
    STATE["group_select_list"] = groupbox(page, "📚 列表与组合框", 16, 16, 718, 400)
    label(page, "📚 ListBox / ComboBox / D2DComboBox", 36, 54, 360, 24, size=15, bold=True)
    label(page, "🧪 此区域用于测试列表选择、只读组合框、可编辑组合框、自绘 D2D 组合框。", 36, 84, 660, 24, fg=0xFF606266)

    lb = DLL.CreateListBox(page, 36, 126, 220, 238, BOOL(False), THEME_TEXT, THEME_BG)
    for item in (
        "🍎 苹果",
        "🍌 香蕉",
        "🍉 西瓜",
        "🍇 葡萄",
        "🐉 火龙果",
        "🍍 菠萝",
        "🥭 芒果",
        "🍓 草莓",
        "🍒 樱桃",
        "🍑 水蜜桃",
        "🥝 猕猴桃",
        "🍋 柠檬",
        "🍐 雪梨",
        "🥥 椰子",
        "🫐 蓝莓",
        "🍈 哈密瓜",
        "🍊 橘子",
        "🍏 青苹果",
    ):
        p, n, _ = s(item)
        DLL.AddListItem(lb, p, n)
    DLL.SetSelectedIndex(lb, 1)

    combo_ro = DLL.CreateComboBox(page, 286, 126, 180, 38, BOOL(True), THEME_TEXT, THEME_BG, 32, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    for item in ("🏙️ 北京", "🌉 上海", "🚀 深圳", "🌿 杭州"):
        p, n, _ = s(item)
        DLL.AddComboItem(combo_ro, p, n)
    DLL.SetComboSelectedIndex(combo_ro, 1)

    combo_ed = DLL.CreateComboBox(page, 286, 186, 180, 38, BOOL(False), THEME_TEXT, THEME_BG, 32, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    for item in ("💻 开发", "🧪 测试", "🎨 设计", "🛠️ 运维"):
        p, n, _ = s(item)
        DLL.AddComboItem(combo_ed, p, n)
    DLL.SetComboSelectedIndex(combo_ed, 0)

    combo_d2d = DLL.CreateD2DComboBox(page, 286, 246, 320, 38, BOOL(False), THEME_TEXT, THEME_BG, 32, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    for item in ("😀 D2D 选项一", "🚀 D2D 选项二", "🎯 D2D 选项三"):
        p, n, _ = s(item)
        DLL.AddD2DComboItem(combo_d2d, p, n)
    DLL.SetD2DComboSelectedIndex(combo_d2d, 0)
    bind_right_click_many(lb, combo_ro, combo_ed, combo_d2d)

    lcb = DLL._ListBoxCB(on_listbox)
    ccb = DLL._ComboCB(on_combo)
    dcb = DLL._ComboCB(on_d2d_combo)
    KEEP.extend([lcb, ccb, dcb])
    DLL.SetListBoxCallback(lb, lcb)
    DLL.SetComboBoxCallback(combo_ro, ccb)
    DLL.SetComboBoxCallback(combo_ed, ccb)
    DLL.SetD2DComboBoxCallback(combo_d2d, dcb)

    STATE["group_select_media"] = groupbox(page, "🗓️ 日期时间、图片", 752, 16, 718, 400)
    label(page, "🗓️ D2DDateTimePicker / PictureBox", 772, 54, 520, 24, size=15, bold=True)
    label(page, "🧪 热键示例已移除；这里继续测试日期时间选择器、图片框和统一右键调试回调。", 772, 84, 660, 24, fg=0xFF606266)

    dt = DLL.CreateD2DDateTimePicker(page, 772, 126, 340, 38, DTP_YMDHM, 0xFF303133, 0xFFFFFFFF, 0xFFDCDFE6, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    DLL.SetD2DDateTimePickerDateTime(dt, 2026, 3, 29, 14, 30, 0)
    dvcb = DLL._ValueCB(on_dt)
    KEEP.append(dvcb)
    DLL.SetD2DDateTimePickerCallback(dt, dvcb)

    pic = DLL.CreatePictureBox(page, 1150, 126, 250, 180, 1, 0xFFF5F7FA)
    bind_right_click_many(dt, pic)
    buf = ctypes.create_string_buffer(PNG_BYTES)
    globals()["_pic_buf"] = buf
    DLL.LoadImageFromMemory(pic, ctypes.cast(buf, ctypes.c_void_p), len(PNG_BYTES))
    pcb = DLL._PictureCB(on_picture)
    KEEP.append(pcb)
    DLL.SetPictureBoxCallback(pic, pcb)

    label(page, "🖼️ PictureBox 已加载。点击图片框测试回调。", 1150, 318, 280, 24, fg=0xFF606266)
    STATE["group_select_tips"] = groupbox(page, "💡 测试建议", 16, 432, 1454, 120)
    label(page, "1. 📚 先点 ListBox，再切换两个 ComboBox。", 36, 474, 420, 24)
    label(page, "2. 🖱️ 在空白区、分组框、列表框、组合框、日期框上右键，确认打印的是当前组件句柄。", 36, 504, 900, 24)
    label(page, "3. 🖼️ 点击右侧 PictureBox，验证图片框点击回调；右键 PictureBox 再检查句柄输出。", 36, 534, 760, 24)


def add_grid_row() -> None:
    g = STATE["grid"]
    row = DLL.DataGrid_AddRow(g)
    idx = int(STATE["row_count"]) + 1
    values = [f"🧾 任务 {idx}", None, "🚧 进行中" if idx % 2 else "🕒 待处理", "🔵 P1" if idx % 2 else "🟢 P2", "🧩 支持下拉、勾选和标签色块"]
    for col, value in enumerate(values):
        if value is None:
            DLL.DataGrid_SetCellChecked(g, row, col, BOOL(idx % 2 == 1))
            continue
        p, n, _ = s(value)
        DLL.DataGrid_SetCellText(g, row, col, p, n)
    DLL.DataGrid_SetCellStyle(g, row, 3, THEME_PRIMARY if idx % 2 else THEME_SUCCESS, THEME_SURFACE_PRIMARY if idx % 2 else THEME_SURFACE_SUCCESS, BOOL(False), BOOL(False))
    STATE["row_count"] = idx


def toggle_grid_header() -> None:
    dark = bool(STATE["grid_dark"])
    for h in (STATE.get("grid"), STATE.get("grid_virtual")):
        if h:
            DLL.DataGrid_SetHeaderStyle(h, 0 if dark else 2)
            DLL.DataGrid_Refresh(h)
    STATE["grid_dark"] = not dark
    set_status(f"🎨 DataGridView 表头样式已切换为 {'Plain' if dark else 'Dark'}。")


def toggle_grid_double_click() -> None:
    g = STATE["grid"]
    enabled = not bool(STATE["grid_dblclick"])
    DLL.DataGrid_SetDoubleClickEnabled(g, BOOL(enabled))
    STATE["grid_dblclick"] = enabled
    set_status(f"🖱️ 普通表格双击编辑已{'开启' if enabled else '关闭'}。")


def cycle_grid_header_align() -> None:
    value = next_alignment(int(STATE["grid_header_align"]))
    STATE["grid_header_align"] = value
    for h in (STATE.get("grid"), STATE.get("grid_virtual")):
        apply_grid_alignment(h, header_align=value)
    set_status(f"📏 表头对齐方式已切换为 {alignment_name(value)}。")


def cycle_grid_cell_align() -> None:
    value = next_alignment(int(STATE["grid_cell_align"]))
    STATE["grid_cell_align"] = value
    for h in (STATE.get("grid"), STATE.get("grid_virtual")):
        apply_grid_alignment(h, cell_align=value)
    set_status(f"📐 单元格对齐方式已切换为 {alignment_name(value)}。")


def clear_grid_rows() -> None:
    g = STATE["grid"]
    DLL.DataGrid_ClearRows(g)
    STATE["row_count"] = 0
    set_status("🧹 普通表格数据已清空。")


def toggle_virtual_grid() -> None:
    normal = STATE["grid"]
    virtual = STATE["grid_virtual"]
    use_virtual = not bool(STATE["grid_virtual_mode"])
    DLL.DataGrid_Show(normal, BOOL(not use_virtual))
    DLL.DataGrid_Show(virtual, BOOL(use_virtual))
    if use_virtual:
        DLL.DataGrid_Refresh(virtual)
        set_status("🚀 已切换到虚拟 DataGridView，可滚动查看 1,000,000 行。")
    else:
        DLL.DataGrid_Refresh(normal)
        set_status(f"🧾 已切换回普通 DataGridView，当前共有 {STATE['row_count']} 行。")
    STATE["grid_virtual_mode"] = use_virtual


def data_page(page: HWND) -> tuple[HWND, HWND, int]:
    groupbox(page, "🧾 DataGridView", 16, 16, 1000, 560)
    label(page, "🧾 文本列 / 勾选列 / 下拉列 / Tag 列", 36, 54, 420, 24, size=15, bold=True)
    label(page, "🧪 这里放一张可直接交互的表格，支持勾选、组合框、标签样式和回调。", 36, 84, 660, 24, fg=0xFF606266)

    g = DLL.CreateDataGridView(page, 36, 126, 960, 420, BOOL(False), BOOL(True), THEME_TEXT, THEME_BG)
    STATE["grid"] = g
    apply_grid_theme(g)
    for title, fn, width in (
        ("🧾 任务", DLL.DataGrid_AddTextColumn, 220),
        ("☑️ 启用", DLL.DataGrid_AddCheckBoxColumn, 90),
        ("🚦 状态", DLL.DataGrid_AddComboBoxColumn, 150),
        ("🏷️ 标签", DLL.DataGrid_AddTagColumn, 120),
        ("📝 备注", DLL.DataGrid_AddTextColumn, 320),
    ):
        p, n, _ = s(title)
        fn(g, p, n, width)
    for col in range(5):
        DLL.DataGrid_SetColumnHeaderAlignment(g, col, ALIGN_CENTER)
    DLL.DataGrid_SetColumnCellAlignment(g, 1, ALIGN_CENTER)
    DLL.DataGrid_SetColumnCellAlignment(g, 2, ALIGN_CENTER)
    DLL.DataGrid_SetColumnCellAlignment(g, 3, ALIGN_CENTER)
    DLL.DataGrid_SetSelectionMode(g, 0)
    DLL.DataGrid_SetShowGridLines(g, BOOL(True))
    DLL.DataGrid_SetDefaultRowHeight(g, 40)
    DLL.DataGrid_SetHeaderHeight(g, 48)
    DLL.DataGrid_SetHeaderStyle(g, 2)
    cp, cn, _ = s("🕒 待处理\n🚧 进行中\n✅ 已完成\n⏸️ 已暂停")
    DLL.DataGrid_SetColumnComboItems(g, 2, cp, cn)
    for _ in range(3):
        add_grid_row()

    g1 = DLL._GridCB(on_grid_click)
    g2 = DLL._GridCB(on_grid_dblclick)
    g3 = DLL._GridCB(on_grid_change)
    KEEP.extend([g1, g2, g3])
    DLL.DataGrid_SetCellClickCallback(g, g1)
    DLL.DataGrid_SetCellDoubleClickCallback(g, g2)
    DLL.DataGrid_SetCellValueChangedCallback(g, g3)

    menu_group = groupbox(page, "🧭 MenuBar 与 PopupMenu", 1030, 16, 440, 560)
    label(page, "🧭 顶部已创建 MenuBar。这里重点测试右键菜单绑定。", 1050, 54, 380, 24, size=15, bold=True)
    label(page, "🖱️ 窗口空白处、下方按钮、复选框、表格内都绑定了 PopupMenu。", 1050, 84, 370, 48, fg=0xFF606266, wrap=True)
    ctp, ctn, _ = s("☑️ 右键测试复选框")
    chk = DLL.CreateCheckBox(page, 1050, 148, 220, 32, ctp, ctn, BOOL(True), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    cb = DLL._CheckBoxCB(on_checkbox)
    KEEP.append(cb)
    DLL.SetCheckBoxCallback(chk, cb)
    btn = button(menu_group, "🧩", "右键测试按钮", 10, 157, 190, 38, 0xFF409EFF, lambda: set_status("🧩 右键测试按钮被左键点击。"))
    button(menu_group, "➕", "表格加一行", 10, 207, 160, 38, 0xFF67C23A, lambda: (add_grid_row(), set_status("➕ 已通过按钮向表格新增一行。")))
    button(menu_group, "🎨", "切换表头色", 180, 207, 146, 38, 0xFFE6A23C, toggle_grid_header)
    button(menu_group, "📄", "显示消息框", 10, 257, 160, 38, 0xFF909399, lambda: (show_msg("🧾 DataGridView 测试", "🧪 你可以继续在表格中点击、双击、修改下拉值。", "📊"), set_status("💬 数据页消息框已打开。")))
    label(page, "1. 🪟 在空白处右键测试窗口菜单。", 1050, 394, 320, 24)
    label(page, "2. 🧾 在表格内右键测试表格菜单。", 1050, 424, 320, 24)
    label(page, "3. 🧩 在按钮或复选框上右键测试绑定菜单。", 1050, 454, 360, 24)
    return chk, button_host(menu_group), btn


def data_page_v2(page: HWND) -> tuple[HWND, HWND, int]:
    groupbox(page, "🧾 DataGridView", 16, 16, 1000, 560)
    label(page, "🧾 文本列 / 勾选列 / 下拉列 / Tag 列", 36, 54, 460, 24, size=15, bold=True)
    label(page, "🧪 左侧可在普通表格与 100 万行虚拟表格之间切换，右侧按钮用于测试双击编辑、对齐和清空。", 36, 84, 900, 24, fg=0xFF606266)

    g = DLL.CreateDataGridView(page, 36, 126, 960, 420, BOOL(False), BOOL(True), THEME_TEXT, THEME_BG)
    STATE["grid"] = g
    apply_grid_theme(g)
    for title, fn, width in (
        ("🧾 任务", DLL.DataGrid_AddTextColumn, 220),
        ("☑️ 启用", DLL.DataGrid_AddCheckBoxColumn, 90),
        ("🚦 状态", DLL.DataGrid_AddComboBoxColumn, 150),
        ("🏷️ 标签", DLL.DataGrid_AddTagColumn, 120),
        ("📝 备注", DLL.DataGrid_AddTextColumn, 320),
    ):
        p, n, _ = s(title)
        fn(g, p, n, width)
    DLL.DataGrid_SetSelectionMode(g, 0)
    DLL.DataGrid_SetShowGridLines(g, BOOL(True))
    DLL.DataGrid_SetDefaultRowHeight(g, 40)
    DLL.DataGrid_SetHeaderHeight(g, 48)
    DLL.DataGrid_SetHeaderStyle(g, 2)
    DLL.DataGrid_SetDoubleClickEnabled(g, BOOL(True))
    cp, cn, _ = s("🕒 待处理\n🚧 进行中\n✅ 已完成\n⏸️ 已暂停")
    DLL.DataGrid_SetColumnComboItems(g, 2, cp, cn)
    apply_grid_alignment(g, header_align=ALIGN_CENTER, cell_align=ALIGN_LEFT)
    DLL.DataGrid_SetColumnCellAlignment(g, 1, ALIGN_CENTER)
    DLL.DataGrid_SetColumnCellAlignment(g, 2, ALIGN_CENTER)
    DLL.DataGrid_SetColumnCellAlignment(g, 3, ALIGN_CENTER)
    for _ in range(3):
        add_grid_row()

    gv = DLL.CreateDataGridView(page, 36, 126, 960, 420, BOOL(True), BOOL(True), THEME_TEXT, THEME_BG)
    STATE["grid_virtual"] = gv
    apply_grid_theme(gv)
    for title, width in (
        ("🧾 序号", 190),
        ("🚦 状态", 170),
        ("🏷️ 优先级", 150),
        ("👤 节点", 140),
        ("📝 虚拟备注", 310),
    ):
        p, n, _ = s(title)
        DLL.DataGrid_AddTextColumn(gv, p, n, width)
    DLL.DataGrid_SetSelectionMode(gv, 0)
    DLL.DataGrid_SetShowGridLines(gv, BOOL(True))
    DLL.DataGrid_SetDefaultRowHeight(gv, 40)
    DLL.DataGrid_SetHeaderHeight(gv, 48)
    DLL.DataGrid_SetHeaderStyle(gv, 2)
    DLL.DataGrid_SetVirtualRowCount(gv, 1_000_000)
    vcb = DLL._GridVirtualCB(on_virtual_grid_request)
    KEEP.append(vcb)
    DLL.DataGrid_SetVirtualDataCallback(gv, vcb)
    apply_grid_alignment(gv, header_align=ALIGN_CENTER, cell_align=ALIGN_LEFT)
    DLL.DataGrid_Show(gv, BOOL(False))

    g1 = DLL._GridCB(on_grid_click)
    g2 = DLL._GridCB(on_grid_dblclick)
    g3 = DLL._GridCB(on_grid_change)
    KEEP.extend([g1, g2, g3])
    DLL.DataGrid_SetCellClickCallback(g, g1)
    DLL.DataGrid_SetCellDoubleClickCallback(g, g2)
    DLL.DataGrid_SetCellValueChangedCallback(g, g3)
    DLL.DataGrid_SetCellClickCallback(gv, g1)
    DLL.DataGrid_SetCellDoubleClickCallback(gv, g2)

    menu_group = groupbox(page, "🧭 MenuBar 与 PopupMenu", 1030, 16, 440, 560)
    label(page, "🧭 顶部已经创建 MenuBar，这里继续放右键菜单与表格控制按钮。", 1050, 54, 380, 24, size=15, bold=True)
    label(page, "🖱️ 窗口空白处、按钮、复选框、普通表格和虚拟表格都可继续测试菜单与交互。", 1050, 84, 370, 48, fg=0xFF606266, wrap=True)
    ctp, ctn, _ = s("☑️ 右键测试复选框")
    chk = DLL.CreateCheckBox(page, 1050, 148, 220, 32, ctp, ctn, BOOL(True), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    cb = DLL._CheckBoxCB(on_checkbox)
    KEEP.append(cb)
    DLL.SetCheckBoxCallback(chk, cb)

    btn = button(menu_group, "🧩", "右键测试按钮", 10, 157, 190, 38, 0xFF409EFF, lambda: set_status("🧩 右键测试按钮被左键点击。"))
    button(menu_group, "➕", "表格加一行", 10, 207, 160, 38, 0xFF67C23A, lambda: (add_grid_row(), set_status("➕ 已向普通表格新增一行。")))
    button(menu_group, "🧹", "清空表格", 180, 207, 146, 38, 0xFFF56C6C, clear_grid_rows)
    button(menu_group, "🎨", "切换表头色", 10, 257, 160, 38, 0xFFE6A23C, toggle_grid_header)
    button(menu_group, "🖱️", "双击编辑开关", 180, 257, 146, 38, 0xFF909399, toggle_grid_double_click)
    button(menu_group, "📏", "表头对齐", 10, 307, 160, 38, 0xFF409EFF, cycle_grid_header_align)
    button(menu_group, "📐", "单元格对齐", 180, 307, 146, 38, 0xFF67C23A, cycle_grid_cell_align)
    button(menu_group, "🚀", "切换虚拟表格", 10, 357, 160, 38, 0xFF8E44AD, toggle_virtual_grid)
    button(menu_group, "📄", "显示消息框", 180, 357, 146, 38, 0xFF909399, lambda: (show_msg("🧾 DataGridView 测试", "🧪 你可以继续测试右键菜单、双击编辑、对齐切换和 100 万行虚拟表格。", "📊"), set_status("💬 数据页消息框已打开。")))
    label(page, "1. 🧾 普通表格支持双击编辑、下拉、勾选和标签样式。", 1050, 424, 360, 24)
    label(page, "2. 🚀 虚拟表格可切到 1,000,000 行，重点测试滚动与绘制性能。", 1050, 454, 380, 24)
    label(page, "3. 📏 右侧按钮可切换表头/单元格对齐，并控制普通表格是否允许双击编辑。", 1050, 484, 390, 24)
    return chk, button_host(menu_group), btn


def data_page_v3(page: HWND) -> tuple[HWND, HWND, int]:
    chk, data_btn_parent, data_btn = data_page_v2(page)
    for h in (STATE.get("grid"), STATE.get("grid_virtual")):
        if h:
            DLL.DataGrid_SetBounds(h, 36, 126, 960, 450)
            DLL.DataGrid_Refresh(h)
    label(page, " ", 1044, 418, 410, 120, fg=0xFFFFFFFF, bg=0xFFFFFFFF, wrap=True)
    label(page, "1. 🧾 普通表格支持双击编辑、下拉、勾选和标签样式。", 1050, 448, 360, 24)
    label(page, "2. 🚀 虚拟表格可切到 1,000,000 行，重点测试滚动与绘制性能。", 1050, 480, 380, 24)
    label(page, "3. 📏 右侧按钮可切换表头/单元格对齐，并控制普通表格是否允许双击编辑。", 1050, 512, 390, 24)
    return chk, data_btn_parent, data_btn


def data_page_v4(page: HWND) -> tuple[HWND, HWND, int]:
    STATE["group_data_grid"] = groupbox(page, "🧾 DataGridView", 16, 16, 1000, 590)
    label(page, "🧾 文本列 / 勾选列 / 下拉列 / Tag 列", 36, 54, 460, 24, size=15, bold=True)
    label(page, "🧪 左侧可在普通表格与 100 万行虚拟表格之间切换，右侧按钮用于测试双击编辑、对齐和清空。", 36, 84, 900, 24, fg=0xFF606266)

    g = DLL.CreateDataGridView(page, 36, 126, 960, 455, BOOL(False), BOOL(True), THEME_TEXT, THEME_BG)
    STATE["grid"] = g
    apply_grid_theme(g)
    for title, fn, width in (
        ("🧾 任务", DLL.DataGrid_AddTextColumn, 220),
        ("☑️ 启用", DLL.DataGrid_AddCheckBoxColumn, 90),
        ("🚦 状态", DLL.DataGrid_AddComboBoxColumn, 150),
        ("🏷️ 标签", DLL.DataGrid_AddTagColumn, 120),
        ("📝 备注", DLL.DataGrid_AddTextColumn, 320),
    ):
        p, n, _ = s(title)
        fn(g, p, n, width)
    DLL.DataGrid_SetSelectionMode(g, 0)
    DLL.DataGrid_SetShowGridLines(g, BOOL(True))
    DLL.DataGrid_SetDefaultRowHeight(g, 40)
    DLL.DataGrid_SetHeaderHeight(g, 48)
    DLL.DataGrid_SetHeaderStyle(g, 2)
    DLL.DataGrid_SetDoubleClickEnabled(g, BOOL(True))
    cp, cn, _ = s("🕒 待处理\n🚧 进行中\n✅ 已完成\n⏸️ 已暂停")
    DLL.DataGrid_SetColumnComboItems(g, 2, cp, cn)
    apply_grid_alignment(g, header_align=ALIGN_CENTER, cell_align=ALIGN_LEFT)
    DLL.DataGrid_SetColumnCellAlignment(g, 1, ALIGN_CENTER)
    DLL.DataGrid_SetColumnCellAlignment(g, 2, ALIGN_CENTER)
    DLL.DataGrid_SetColumnCellAlignment(g, 3, ALIGN_CENTER)
    for _ in range(3):
        add_grid_row()

    gv = DLL.CreateDataGridView(page, 36, 126, 960, 455, BOOL(True), BOOL(True), THEME_TEXT, THEME_BG)
    STATE["grid_virtual"] = gv
    apply_grid_theme(gv)
    for title, width in (
        ("🧾 序号", 190),
        ("🚦 状态", 170),
        ("🏷️ 优先级", 150),
        ("👤 节点", 140),
        ("📝 虚拟备注", 310),
    ):
        p, n, _ = s(title)
        DLL.DataGrid_AddTextColumn(gv, p, n, width)
    DLL.DataGrid_SetSelectionMode(gv, 0)
    DLL.DataGrid_SetShowGridLines(gv, BOOL(True))
    DLL.DataGrid_SetDefaultRowHeight(gv, 40)
    DLL.DataGrid_SetHeaderHeight(gv, 48)
    DLL.DataGrid_SetHeaderStyle(gv, 2)
    DLL.DataGrid_SetVirtualRowCount(gv, 1_000_000)
    vcb = DLL._GridVirtualCB(on_virtual_grid_request)
    KEEP.append(vcb)
    DLL.DataGrid_SetVirtualDataCallback(gv, vcb)
    apply_grid_alignment(gv, header_align=ALIGN_CENTER, cell_align=ALIGN_LEFT)
    DLL.DataGrid_Show(gv, BOOL(False))
    bind_right_click_many(g, gv)

    g1 = DLL._GridCB(on_grid_click)
    g2 = DLL._GridCB(on_grid_dblclick)
    g3 = DLL._GridCB(on_grid_change)
    KEEP.extend([g1, g2, g3])
    DLL.DataGrid_SetCellClickCallback(g, g1)
    DLL.DataGrid_SetCellDoubleClickCallback(g, g2)
    DLL.DataGrid_SetCellValueChangedCallback(g, g3)
    DLL.DataGrid_SetCellClickCallback(gv, g1)
    DLL.DataGrid_SetCellDoubleClickCallback(gv, g2)

    menu_group = groupbox(page, "🧭 MenuBar 与 PopupMenu", 1030, 16, 440, 590)
    STATE["group_data_menu"] = menu_group
    label(page, "🧭 顶部已经创建 MenuBar，这里继续放右键菜单与表格控制按钮。", 1050, 54, 380, 24, size=15, bold=True)
    label(page, "🖱️ 窗口空白处、按钮、复选框、普通表格和虚拟表格都可继续测试菜单与交互。", 1050, 84, 370, 48, fg=0xFF606266, wrap=True)
    ctp, ctn, _ = s("☑️ 右键测试复选框")
    chk = DLL.CreateCheckBox(page, 1050, 148, 220, 32, ctp, ctn, BOOL(True), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    bind_right_click(chk)
    cb = DLL._CheckBoxCB(on_checkbox)
    KEEP.append(cb)
    DLL.SetCheckBoxCallback(chk, cb)

    btn = button(menu_group, "🧩", "右键测试按钮", 10, 155, 190, 38, 0xFF409EFF, lambda: set_status("🧩 右键测试按钮被左键点击。"))
    button(menu_group, "➕", "表格加一行", 10, 203, 160, 38, 0xFF67C23A, lambda: (add_grid_row(), set_status("➕ 已向普通表格新增一行。")))
    button(menu_group, "🧹", "清空表格", 180, 203, 146, 38, 0xFFF56C6C, clear_grid_rows)
    button(menu_group, "🎨", "切换表头色", 10, 251, 160, 38, 0xFFE6A23C, toggle_grid_header)
    button(menu_group, "🖱️", "双击编辑开关", 180, 251, 146, 38, 0xFF909399, toggle_grid_double_click)
    button(menu_group, "📏", "表头对齐", 10, 299, 160, 38, 0xFF409EFF, cycle_grid_header_align)
    button(menu_group, "📐", "单元格对齐", 180, 299, 146, 38, 0xFF67C23A, cycle_grid_cell_align)
    button(menu_group, "🚀", "切换虚拟表格", 10, 347, 160, 38, 0xFF8E44AD, toggle_virtual_grid)
    button(menu_group, "📄", "显示消息框", 180, 347, 146, 38, 0xFF909399, lambda: (show_msg("🧾 DataGridView 测试", "🧪 你可以继续测试右键菜单、双击编辑、对齐切换和 100 万行虚拟表格。", "📊"), set_status("💬 数据页消息框已打开。")))
    label(page, "1. 🧾 普通表格支持双击编辑、下拉、勾选和标签样式。", 1050, 430, 360, 24)
    label(page, "2. 🚀 虚拟表格可切到 1,000,000 行，重点测试滚动与绘制性能。", 1050, 462, 380, 24)
    label(page, "3. 📏 右侧按钮可切换表头/单元格对齐，并控制普通表格是否允许双击编辑。", 1050, 494, 390, 24)
    return chk, button_host(menu_group), btn


def tabs_page(page: HWND) -> None:
    STATE["group_tabs_nested"] = groupbox(page, "🗂️ 嵌套 TabControl", 16, 16, 920, 500)
    label(page, "🗂️ 这里再放一个真正可切换的 TabControl，用来测试页签头和内容同步切换。", 36, 54, 800, 24, size=15, bold=True)
    tab = DLL.CreateTabControl(page, 36, 96, 880, 380)
    bind_right_click(tab)
    STATE["nested_tab"] = tab
    DLL.SetTabHeaderStyle(tab, TAB_HEADER_STYLE_CARD_PLAIN)
    DLL.SetTabItemSize(tab, 136, 36)
    DLL.SetTabPadding(tab, 18, 8)
    DLL.SetTabColors(tab, 13, 14, 5, 6)
    DLL.SetTabIndicatorColor(tab, 0xFF409EFF)
    tcb = DLL._TabCB(on_nested_tab)
    KEEP.append(tcb)
    DLL.SetTabCallback(tab, tcb)
    nested_pages: list[HWND] = []
    for i, title in enumerate(("🥇 第一页", "🥈 第二页", "🥉 第三页")):
        content = add_tab(tab, title)
        nested_pages.append(content)
        label(content, f"🗂️ 嵌套页签 {title}", 20, 16, 300, 24, size=14, bold=True)
        label(content, "👀 点击下面按钮，观察它是否只在当前页签中显示。", 20, 48, 340, 24, fg=0xFF606266)
        button(content, "🧪", f"测试按钮 {i + 1}", 20, 96, 180, 38, 0xFF409EFF, lambda idx=i: set_status(f"🗂️ 嵌套页签按钮点击: 第 {idx + 1} 页。"))
        label(content, "🧩 这是用于观察 TabControl 页面切换时控件显隐状态的测试区。", 20, 150, 460, 24, fg=0xFF606266)

    STATE["nested_pages"] = nested_pages
    action_group = groupbox(page, "🪄 页签与弹窗联动", 954, 16, 516, 500)
    STATE["group_tabs_action"] = action_group
    label(page, "🪄 这里提供一些跳页和弹窗联动按钮。", 974, 54, 340, 24, size=15, bold=True)
    button(action_group, "1️⃣", "切到基础组件", 10, 65, 210, 38, 0xFF409EFF, lambda: DLL.SelectTab(STATE["main_tab"], TAB_BASIC))
    button(action_group, "2️⃣", "切到选择组件", 10, 115, 210, 38, 0xFF67C23A, lambda: DLL.SelectTab(STATE["main_tab"], TAB_SELECT))
    button(action_group, "3️⃣", "切到数据组件", 10, 165, 210, 38, 0xFFE6A23C, lambda: DLL.SelectTab(STATE["main_tab"], TAB_DATA))
    button(action_group, "4️⃣", "回到当前页", 10, 215, 210, 38, 0xFF909399, lambda: DLL.SelectTab(STATE["main_tab"], TAB_TABS))
    button(action_group, "💬", "再次显示信息框", 10, 281, 210, 38, 0xFF409EFF, lambda: (show_msg("🗂️ 页签页消息框", "🧪 你可以在这个页签中继续切换主 Tab 和嵌套 Tab。", "🗂️"), set_status("💬 页签页消息框已打开。")))
    button(action_group, "❓", "再次显示确认框", 10, 331, 210, 38, 0xFFE6A23C, lambda: (show_confirm("🧭 页签页确认框", "🔍 继续检查页签切换效果吗？", "❓"), set_status("❓ 页签页确认框已打开。")))
    label(page, "🧭 你也可以通过顶部菜单栏快速切换到任意主页签。", 974, 434, 380, 24, fg=0xFF606266)


def layout_page(page: HWND) -> None:
    STATE["group_layout_actions"] = groupbox(page, "📐 布局器控制", 16, 16, 420, 240)
    label(page, "📐 这里演示 Flow / Grid / Dock 布局管理器。", 36, 54, 360, 24, size=15, bold=True)
    label(page, "🧪 点击下面按钮切换布局模式，观察同一组控件在容器内如何自动排布。", 36, 84, 380, 48, fg=0xFF606266, wrap=True)
    button(STATE["group_layout_actions"], "➡️", "水平流式", 10, 96, 170, 38, 0xFF409EFF, lambda: set_layout_mode("flow_h"))
    button(STATE["group_layout_actions"], "⬇️", "垂直流式", 200, 96, 170, 38, 0xFF67C23A, lambda: set_layout_mode("flow_v"))
    button(STATE["group_layout_actions"], "🔲", "网格布局", 10, 144, 170, 38, 0xFFE6A23C, lambda: set_layout_mode("grid"))
    button(STATE["group_layout_actions"], "🧱", "停靠布局", 200, 144, 170, 38, 0xFF909399, lambda: set_layout_mode("dock"))

    layout_host = groupbox(page, "🧰 布局容器", 460, 16, 1010, 650)
    STATE["group_layout_host"] = layout_host
    STATE["layout_host"] = layout_host

    lp1 = s("📥 输入框")
    lp2 = s("📍 北京\n🌉 上海\n🚀 深圳\n🌿 杭州")
    lp3 = s("🍎 苹果\n🍌 香蕉\n🍉 西瓜\n🍇 葡萄\n🥭 芒果\n🍓 草莓")
    l1 = DLL.CreateEditBox(layout_host, 0, 0, 220, 36, lp1[0], lp1[1], THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False), ALIGN_LEFT, BOOL(False), BOOL(False), BOOL(False), BOOL(True), BOOL(True))
    l2 = DLL.CreateComboBox(layout_host, 0, 0, 220, 38, BOOL(True), THEME_TEXT, THEME_BG, 32, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    for item in ("📍 北京", "🌉 上海", "🚀 深圳", "🌿 杭州"):
        p, n, _ = s(item)
        DLL.AddComboItem(l2, p, n)
    DLL.SetComboSelectedIndex(l2, 1)
    l3 = DLL.CreateListBox(layout_host, 0, 0, 240, 220, BOOL(False), THEME_TEXT, THEME_BG)
    for item in ("🍎 苹果", "🍌 香蕉", "🍉 西瓜", "🍇 葡萄", "🥭 芒果", "🍓 草莓"):
        p, n, _ = s(item)
        DLL.AddListItem(l3, p, n)
    DLL.SetSelectedIndex(l3, 2)
    l4 = DLL.CreateProgressBar(layout_host, 0, 0, 240, 24, 58, 0, 14, BOOL(True), 5)
    title_text = s("🧭 当前容器由布局器自动排布。")
    l5 = DLL.CreateEditBox(layout_host, 0, 0, 320, 36, title_text[0], title_text[1], THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(True), BOOL(False), BOOL(False), ALIGN_LEFT, BOOL(False), BOOL(True), BOOL(False), BOOL(True), BOOL(True))
    memo_text = s("📝 多行编辑框\n这块区域会在 Dock 布局中 Fill 填满剩余空间。")
    l6 = DLL.CreateEditBox(layout_host, 0, 0, 320, 140, memo_text[0], memo_text[1], THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False), ALIGN_LEFT, BOOL(True), BOOL(False), BOOL(False), BOOL(True), BOOL(False))
    bind_right_click_many(l1, l2, l3, l4, l5, l6)
    DLL.SetProgressBarTextColor(l4, 5)
    STATE["layout_controls"] = [l5, l1, l2, l3, l4, l6]

    tips = groupbox(page, "💡 布局器说明", 16, 274, 420, 392)
    STATE["group_layout_tips"] = tips
    label(page, "1. 🧱 这页调用的是底层布局器 API，不是手工坐标挪控件。", 36, 316, 360, 24)
    label(page, "2. 🔄 每次切换模式都会 RemoveLayoutManager + SetLayoutManager + AddControlToLayout。", 36, 348, 380, 48, fg=0xFF606266, wrap=True)
    label(page, "3. 📏 Dock 模式会演示 Top / Left / Right / Bottom / Fill 五种停靠。", 36, 404, 370, 48, fg=0xFF606266, wrap=True)
    label(page, "4. 🖱️ 右键布局容器和容器内组件，仍可继续检查句柄与菜单路由。", 36, 460, 360, 48, fg=0xFF606266, wrap=True)
    set_layout_mode("flow_h")


def theme_page(page: HWND) -> None:
    actions = groupbox(page, "🎨 主题切换", 16, 16, 420, 650)
    STATE["group_theme_actions"] = actions
    label(page, "🎨 这里演示内置浅色/深色和自定义 JSON 主题切换。", 36, 54, 380, 24, fg=5, bg=13, size=15, bold=True)
    STATE["theme_name_label"] = label(page, "🎨 当前主题: light", 36, 90, 340, 24, fg=5, bg=13)
    STATE["theme_color_info"] = label(page, "主色=0x00000000 背景=0x00000000 文本=0x00000000", 36, 120, 360, 48, fg=6, bg=13, wrap=True)
    button(actions, "☀️", "浅色主题", 10, 114, 170, 38, 0xFF409EFF, lambda: apply_builtin_theme("light"))
    button(actions, "🌙", "深色主题", 200, 114, 170, 38, 0xFF67C23A, lambda: apply_builtin_theme("dark"))
    button(actions, "🌗", "切暗色模式", 10, 162, 170, 38, 0xFFE6A23C, lambda: apply_dark_mode(not bool(DLL.IsDarkMode())))
    button(actions, "🌊", "Ocean 自定义", 200, 162, 170, 38, 0xFF909399, lambda: apply_custom_theme("ocean", False, "#1D4ED8", "#059669", "#D97706", "#DC2626", "#0EA5E9", "#F8FAFC", "#E0F2FE", "#0F172A"))
    button(actions, "🌇", "Sunset 自定义", 10, 210, 170, 38, 0xFF409EFF, lambda: apply_custom_theme("sunset", False, "#EA580C", "#16A34A", "#CA8A04", "#DC2626", "#7C3AED", "#FFF7ED", "#FFEDD5", "#431407"))
    button(actions, "🌌", "Midnight 自定义", 200, 210, 170, 38, 0xFF67C23A, lambda: apply_custom_theme("midnight", True, "#60A5FA", "#34D399", "#FBBF24", "#F87171", "#A78BFA", "#0F172A", "#111827", "#E5E7EB"))

    sample = groupbox(page, "🧪 主题预览", 460, 16, 1010, 650)
    STATE["group_theme_sample"] = sample
    label(page, "🧪 下面这些控件使用主题色索引或主题友好的默认色，切主题后会立即变化。", 480, 54, 720, 24, fg=6, bg=13)
    label(page, "PRIMARY", 480, 98, 116, 34, fg=0xFFFFFFFF, bg=0, size=12, bold=True)
    label(page, "SUCCESS", 608, 98, 116, 34, fg=0xFFFFFFFF, bg=1, size=12, bold=True)
    label(page, "WARNING", 736, 98, 116, 34, fg=0xFFFFFFFF, bg=2, size=12, bold=True)
    label(page, "DANGER", 864, 98, 116, 34, fg=0xFFFFFFFF, bg=3, size=12, bold=True)
    label(page, "INFO", 992, 98, 116, 34, fg=0xFFFFFFFF, bg=4, size=12, bold=True)
    label(page, "TEXT", 1120, 98, 116, 34, fg=5, bg=14, size=12, bold=True)

    button(sample, "🔵", "主按钮", 10, 144, 170, 38, 0xFF409EFF, lambda: set_status("🎨 主色按钮点击。"))
    button(sample, "🟢", "成功按钮", 196, 144, 170, 38, 0xFF67C23A, lambda: set_status("🎨 成功色按钮点击。"))
    button(sample, "🟠", "警告按钮", 382, 144, 170, 38, 0xFFE6A23C, lambda: set_status("🎨 警告色按钮点击。"))
    button(sample, "🔴", "危险按钮", 568, 144, 170, 38, 0xFFF56C6C, lambda: set_status("🎨 危险色按钮点击。"))
    button(sample, "⚪", "信息按钮", 754, 144, 170, 38, 0xFF909399, lambda: set_status("🎨 信息色按钮点击。"))

    cbp, cbn, _ = s("☑️ 主题复选框")
    theme_chk = DLL.CreateCheckBox(page, 480, 238, 220, 32, cbp, cbn, BOOL(True), 5, 13, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    combo = DLL.CreateComboBox(page, 480, 286, 220, 38, BOOL(True), 5, 13, 32, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    for item in ("🎨 主题预览", "🌗 明暗切换", "🧪 颜色测试"):
        p, n, _ = s(item)
        DLL.AddComboItem(combo, p, n)
    DLL.SetComboSelectedIndex(combo, 0)
    theme_prog = DLL.CreateProgressBar(page, 480, 342, 320, 28, 72, 0, 14, BOOL(True), 5)
    DLL.SetProgressBarTextColor(theme_prog, 5)
    theme_edit = DLL.CreateColorEmojiEditBox(page, 480, 394, 360, 38, *s("🌈 主题切换时这里也会继续显示彩色 emoji。")[:2], 5, 13, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False), ALIGN_LEFT, BOOL(False), BOOL(False), BOOL(False), BOOL(True), BOOL(True))
    bind_right_click_many(theme_chk, combo, theme_prog, theme_edit)
    label(page, "1. 🎨 内置主题通过 SetTheme(light/dark) 切换。", 480, 460, 460, 24, fg=5, bg=13)
    label(page, "2. 🧾 自定义主题通过 LoadThemeFromJSON 注入，主色/背景/文本色会整体更新。", 480, 492, 640, 24, fg=6, bg=13)
    label(page, "3. 📣 当前主题名和关键颜色会在左侧实时刷新。", 480, 524, 420, 24, fg=6, bg=13)
    refresh_theme_preview()


def theme_page(page: HWND) -> None:
    actions = groupbox(page, "🎨 主题切换", 16, 16, 420, 650)
    STATE["group_theme_actions"] = actions
    label(page, "🎨 这里演示内置浅色/深色和自定义 JSON 主题切换。", 36, 54, 380, 24, fg=5, bg=13, size=15, bold=True)
    STATE["theme_name_label"] = label(page, "🎨 当前主题: light", 36, 90, 340, 24, fg=5, bg=13)
    STATE["theme_color_info"] = label(page, "主色=0x00000000 背景=0x00000000 文本=0x00000000", 36, 120, 360, 40, fg=6, bg=13, wrap=True)
    button(actions, "☀️", "浅色主题", 10, 140, 170, 38, 0xFF409EFF, lambda: apply_builtin_theme("light"))
    button(actions, "🌙", "深色主题", 200, 140, 170, 38, 0xFF67C23A, lambda: apply_builtin_theme("dark"))
    button(actions, "🌓", "切暗色模式", 10, 188, 170, 38, 0xFFE6A23C, lambda: apply_dark_mode(not bool(DLL.IsDarkMode())))
    button(actions, "🌊", "Ocean 自定义", 200, 188, 170, 38, 0xFF909399, lambda: apply_custom_theme("ocean", False, "#1D4ED8", "#059669", "#D97706", "#DC2626", "#0EA5E9", "#F8FAFC", "#E0F2FE", "#0F172A"))
    button(actions, "🌇", "Sunset 自定义", 10, 236, 170, 38, 0xFF409EFF, lambda: apply_custom_theme("sunset", False, "#EA580C", "#16A34A", "#CA8A04", "#DC2626", "#7C3AED", "#FFF7ED", "#FFEDD5", "#431407"))
    button(actions, "🌌", "Midnight 自定义", 200, 236, 170, 38, 0xFF67C23A, lambda: apply_custom_theme("midnight", True, "#60A5FA", "#34D399", "#FBBF24", "#F87171", "#A78BFA", "#0F172A", "#111827", "#E5E7EB"))

    sample = groupbox(page, "🧪 主题预览", 460, 16, 1010, 650)
    STATE["group_theme_sample"] = sample
    label(page, "🧪 下面这些控件使用主题色索引或主题友好的默认色，切主题后会立即变化。", 480, 54, 720, 24, fg=6, bg=13)
    label(page, "PRIMARY", 480, 98, 116, 34, fg=0xFFFFFFFF, bg=0, size=12, bold=True, align=ALIGN_CENTER)
    label(page, "SUCCESS", 608, 98, 116, 34, fg=0xFFFFFFFF, bg=1, size=12, bold=True, align=ALIGN_CENTER)
    label(page, "WARNING", 736, 98, 116, 34, fg=0xFFFFFFFF, bg=2, size=12, bold=True, align=ALIGN_CENTER)
    label(page, "DANGER", 864, 98, 116, 34, fg=0xFFFFFFFF, bg=3, size=12, bold=True, align=ALIGN_CENTER)
    label(page, "INFO", 992, 98, 116, 34, fg=0xFFFFFFFF, bg=4, size=12, bold=True, align=ALIGN_CENTER)
    label(page, "TEXT", 1120, 98, 116, 34, fg=5, bg=14, size=12, bold=True, align=ALIGN_CENTER)

    button(sample, "🔵", "主按钮", 10, 144, 170, 38, 0xFF409EFF, lambda: set_status("🎨 主色按钮点击。"))
    button(sample, "🟢", "成功按钮", 196, 144, 170, 38, 0xFF67C23A, lambda: set_status("🎨 成功色按钮点击。"))
    button(sample, "🟠", "警告按钮", 382, 144, 170, 38, 0xFFE6A23C, lambda: set_status("🎨 警告色按钮点击。"))
    button(sample, "🔴", "危险按钮", 568, 144, 170, 38, 0xFFF56C6C, lambda: set_status("🎨 危险色按钮点击。"))
    button(sample, "⚪", "信息按钮", 754, 144, 170, 38, 0xFF909399, lambda: set_status("🎨 信息色按钮点击。"))

    cbp, cbn, _ = s("☑️ 主题复选框")
    theme_chk = DLL.CreateCheckBox(page, 480, 238, 220, 32, cbp, cbn, BOOL(True), 5, 13, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    combo = DLL.CreateComboBox(page, 480, 286, 220, 38, BOOL(True), 5, 13, 32, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    for item in ("🎨 主题预览", "🌗 明暗切换", "🧪 颜色测试"):
        p, n, _ = s(item)
        DLL.AddComboItem(combo, p, n)
    DLL.SetComboSelectedIndex(combo, 0)
    theme_prog = DLL.CreateProgressBar(page, 480, 342, 320, 28, 72, 0, 14, BOOL(True), 5)
    DLL.SetProgressBarTextColor(theme_prog, 5)
    theme_edit = DLL.CreateColorEmojiEditBox(page, 480, 394, 360, 38, *s("🌈 主题切换时这里也会继续显示彩色 emoji。")[:2], 5, 13, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False), ALIGN_LEFT, BOOL(False), BOOL(False), BOOL(False), BOOL(True), BOOL(True))
    bind_right_click_many(theme_chk, combo, theme_prog, theme_edit)
    label(page, "1. 🎨 内置主题通过 SetTheme(light/dark) 切换。", 480, 460, 460, 24, fg=5, bg=13)
    label(page, "2. 🧾 自定义主题通过 LoadThemeFromJSON 注入，主色/背景/文本色会整体更新。", 480, 492, 640, 24, fg=6, bg=13)
    label(page, "3. 📣 当前主题名和关键颜色会在左侧实时刷新。", 480, 524, 420, 24, fg=6, bg=13)
    refresh_theme_preview()


def create_tree_style(
    parent: HWND,
    title: str,
    x: int,
    y: int,
    bg_color: int,
    text_color: int,
    *,
    sidebar: bool,
    row_height: float,
    spacing: float,
    selected_bg: int,
    selected_fg: int,
    hover_bg: int,
    dragdrop: bool,
) -> HWND:
    label(parent, title, x, y, 210, 20, fg=6, bg=13, size=12, bold=True)
    h_tree = DLL.CreateTreeView(parent, x, y + 26, 460, 230, bg_color, text_color, ctypes.c_void_p())
    bind_right_click(h_tree)
    populate_demo_tree(h_tree, title.replace(" ", ""))
    DLL.SetTreeViewSidebarMode(h_tree, BOOL(sidebar))
    DLL.SetTreeViewRowHeight(h_tree, ctypes.c_float(row_height))
    DLL.SetTreeViewItemSpacing(h_tree, ctypes.c_float(spacing))
    DLL.SetTreeViewSelectedBgColor(h_tree, selected_bg)
    DLL.SetTreeViewSelectedForeColor(h_tree, selected_fg)
    DLL.SetTreeViewHoverBgColor(h_tree, hover_bg)
    DLL.SetTreeViewFont(h_tree, FONT_PTR, FONT_LEN, ctypes.c_float(13.0), 500, BOOL(False))
    DLL.EnableTreeViewDragDrop(h_tree, BOOL(dragdrop))
    bind_tree_event(h_tree, CALLBACK_NODE_SELECTED, f"{title} 选中")
    bind_tree_event(h_tree, CALLBACK_NODE_EXPANDED, f"{title} 展开")
    bind_tree_event(h_tree, CALLBACK_NODE_COLLAPSED, f"{title} 折叠")
    if dragdrop:
        bind_tree_event(h_tree, CALLBACK_NODE_MOVED, f"{title} 拖拽")
    return h_tree


def layout_page(page: HWND) -> None:
    STATE["group_layout_actions"] = groupbox(page, "📐 布局器控制", 16, 16, 420, 240)
    label(page, "这里演示 Flow / Grid / Dock 布局管理器。", 36, 54, 360, 24, size=15, bold=True)
    label(page, "点击下面按钮切换布局模式，观察同一组控件在容器内如何自动排布。", 36, 84, 380, 48, fg=0xFF606266, wrap=True)
    button(STATE["group_layout_actions"], "➡️", "水平流式", 10, 96, 170, 38, 0xFF409EFF, lambda: set_layout_mode("flow_h"))
    button(STATE["group_layout_actions"], "⬇️", "垂直流式", 200, 96, 170, 38, 0xFF67C23A, lambda: set_layout_mode("flow_v"))
    button(STATE["group_layout_actions"], "🔳", "网格布局", 10, 144, 170, 38, 0xFFE6A23C, lambda: set_layout_mode("grid"))
    button(STATE["group_layout_actions"], "📦", "停靠布局", 200, 144, 170, 38, 0xFF909399, lambda: set_layout_mode("dock"))

    frame = groupbox(page, "🧰 布局容器", 460, 16, 1010, 650)
    host = bind_right_click(DLL.CreatePanel(page, 480, 54, 970, 590, THEME_SURFACE))
    STATE["group_layout_host"] = frame
    STATE["layout_host"] = host

    t1 = s("🔍 输入框")
    title_text = s("🧭 当前容器由布局器自动排布。")
    memo_text = s("📝 多行编辑框\n这块区域会在 Dock 布局中 Fill 填满剩余空间。")
    l1 = DLL.CreateEditBox(host, 0, 0, 220, 36, t1[0], t1[1], THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False), ALIGN_LEFT, BOOL(False), BOOL(False), BOOL(False), BOOL(True), BOOL(True))
    l2 = DLL.CreateComboBox(host, 0, 0, 220, 38, BOOL(True), THEME_TEXT, THEME_BG, 32, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    for item in ("📍 北京", "🗼 上海", "🌆 深圳", "🌉 杭州"):
        p, n, _ = s(item)
        DLL.AddComboItem(l2, p, n)
    DLL.SetComboSelectedIndex(l2, 1)
    l3 = DLL.CreateListBox(host, 0, 0, 240, 220, BOOL(False), THEME_TEXT, THEME_BG)
    for item in ("🍎 苹果", "🍌 香蕉", "🍉 西瓜", "🍇 葡萄", "🥭 芒果", "🍓 草莓"):
        p, n, _ = s(item)
        DLL.AddListItem(l3, p, n)
    DLL.SetSelectedIndex(l3, 2)
    l4 = DLL.CreateProgressBar(host, 0, 0, 240, 24, 58, 0, 14, BOOL(True), 5)
    l5 = DLL.CreateEditBox(host, 0, 0, 320, 36, title_text[0], title_text[1], THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(True), BOOL(False), BOOL(False), ALIGN_LEFT, BOOL(False), BOOL(True), BOOL(False), BOOL(True), BOOL(True))
    l6 = DLL.CreateEditBox(host, 0, 0, 320, 140, memo_text[0], memo_text[1], THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False), ALIGN_LEFT, BOOL(True), BOOL(False), BOOL(False), BOOL(True), BOOL(False))
    bind_right_click_many(host, l1, l2, l3, l4, l5, l6)
    DLL.SetProgressBarTextColor(l4, 5)
    STATE["layout_controls"] = [l5, l1, l2, l3, l4, l6]

    tips = groupbox(page, "💡 布局器说明", 16, 274, 420, 392)
    STATE["group_layout_tips"] = tips
    label(page, "1. 这页调用的是底层布局器 API，不是手工坐标摆控件。", 36, 316, 360, 24)
    label(page, "2. 每次切换模式都会 RemoveLayoutManager + SetLayoutManager + AddControlToLayout。", 36, 348, 380, 48, fg=0xFF606266, wrap=True)
    label(page, "3. Dock 模式会演示 Top / Left / Right / Bottom / Fill 五种停靠。", 36, 404, 370, 48, fg=0xFF606266, wrap=True)
    label(page, "4. 右键布局容器和容器内组件，仍可继续检查句柄与菜单路由。", 36, 460, 360, 48, fg=0xFF606266, wrap=True)
    set_layout_mode("flow_h")


def menu_tree_page(page: HWND) -> None:
    actions = groupbox(page, "📁 多级菜单与评分", 16, 16, 420, 650)
    STATE["group_menu_actions"] = actions
    label(actions, "顶部 File 菜单和这个页签右键菜单都改成了多级结构。", 14, 24, 360, 22, size=15, bold=True)
    label(actions, "1. 右键这个页签空白处、左侧分组框、右侧树形框，都能看到多级 PopupMenu。", 14, 58, 360, 40, fg=0xFF606266, wrap=True)
    label(actions, "2. 顶部 MenuBar 的“📁 文件”里包含对话框、页签跳转、树形框动作、评分动作四级演示。", 14, 104, 370, 40, fg=0xFF606266, wrap=True)
    label(actions, "⭐ 评分组件演示", 14, 170, 180, 24, size=14, bold=True)
    STATE["rating_label"] = label(actions, "⭐ 当前评分: ★★★☆☆  (3/5)", 14, 204, 340, 28, fg=0xFF303133, bg=0xFFFFFFFF, size=16, bold=True)
    button(actions, "1", "一星", 10, 246, 70, 36, 0xFF909399, lambda: set_rating(1))
    button(actions, "2", "二星", 86, 246, 70, 36, 0xFF909399, lambda: set_rating(2))
    button(actions, "3", "三星", 162, 246, 70, 36, 0xFF409EFF, lambda: set_rating(3))
    button(actions, "4", "四星", 238, 246, 70, 36, 0xFFE6A23C, lambda: set_rating(4))
    button(actions, "5", "五星", 314, 246, 70, 36, 0xFF67C23A, lambda: set_rating(5))
    button(actions, "✖", "清空评分", 10, 292, 150, 36, 0xFFF56C6C, lambda: set_rating(0))
    label(actions, "🌲 主树控制", 14, 352, 180, 24, size=14, bold=True)
    button(actions, "➕", "全部展开", 10, 386, 116, 36, 0xFF409EFF, lambda: on_menu(0, MENU_TREE_EXPAND))
    button(actions, "➖", "全部折叠", 136, 386, 116, 36, 0xFFE6A23C, lambda: on_menu(0, MENU_TREE_COLLAPSE))
    button(actions, "⇆", "切换侧边栏", 262, 386, 122, 36, 0xFF67C23A, lambda: on_menu(0, MENU_TREE_TOGGLE_SIDEBAR))
    STATE["tree_status_label"] = label(actions, "🌲 主树状态: ready", 14, 438, 370, 56, fg=0xFF606266, bg=0xFFFFFFFF, wrap=True)
    label(actions, "树形框支持默认列表、Sidebar 导航、紧凑模式、宽松模式，以及拖拽排序。", 14, 516, 370, 40, fg=0xFF606266, wrap=True)
    label(actions, "评分演示当前使用现有按钮组合实现交互，可直接验证状态和菜单回调。", 14, 566, 370, 40, fg=0xFF606266, wrap=True)

    trees = groupbox(page, "🌲 TreeView 样式总览", 460, 16, 1010, 650)
    STATE["group_tree_styles"] = trees
    t1 = create_tree_style(
        trees, "Default", 16, 22, 0xFFFFFFFF, 0xFF303133,
        sidebar=False, row_height=34.0, spacing=5.0,
        selected_bg=0xFFEAF2FF, selected_fg=0xFF409EFF, hover_bg=0xFFF5F7FA, dragdrop=False,
    )
    t2 = create_tree_style(
        trees, "Sidebar", 500, 22, 0xFFF8FAFC, 0xFF303133,
        sidebar=True, row_height=40.0, spacing=6.0,
        selected_bg=0xFF409EFF, selected_fg=0xFFFFFFFF, hover_bg=0xFFEAF2FF, dragdrop=False,
    )
    t3 = create_tree_style(
        trees, "Compact", 16, 310, 0xFFFFFFFF, 0xFF303133,
        sidebar=False, row_height=28.0, spacing=2.0,
        selected_bg=0xFFE8F5E9, selected_fg=0xFF2E7D32, hover_bg=0xFFF0F9EB, dragdrop=True,
    )
    t4 = create_tree_style(
        trees, "Relaxed", 500, 310, 0xFFFFFBF2, 0xFF303133,
        sidebar=False, row_height=42.0, spacing=10.0,
        selected_bg=0xFFFFE7BA, selected_fg=0xFF8A5A00, hover_bg=0xFFFFF3D8, dragdrop=False,
    )
    STATE["tree_primary"] = t1
    STATE["tree_sidebar_enabled"] = False
    STATE["tree_handles"] = [t1, t2, t3, t4]
    set_rating(int(STATE.get("rating_value", 3)))


def tab_styles_page(page: HWND) -> None:
    actions = groupbox(page, "🗂️ Tab 样式切换", 16, 16, 420, 650)
    STATE["group_tabstyle_actions"] = actions
    label(actions, "四个按钮直接切换下方两个 TabControl 的页签头样式。", 14, 24, 360, 24, size=15, bold=True)
    label(actions, "这里不再动主窗口的总页签，只演示独立 TabControl 的 header 风格。", 14, 58, 360, 40, fg=0xFF606266, wrap=True)
    button(actions, "━", "Line", 10, 122, 170, 38, 0xFF909399, lambda: apply_demo_tab_style(TAB_HEADER_STYLE_LINE))
    button(actions, "▣", "Card", 200, 122, 170, 38, 0xFF409EFF, lambda: apply_demo_tab_style(TAB_HEADER_STYLE_CARD))
    button(actions, "▤", "Card Plain", 10, 170, 170, 38, 0xFF67C23A, lambda: apply_demo_tab_style(TAB_HEADER_STYLE_CARD_PLAIN))
    button(actions, "◫", "Segmented", 200, 170, 170, 38, 0xFFE6A23C, lambda: apply_demo_tab_style(TAB_HEADER_STYLE_SEGMENTED))
    label(actions, "两个示例 TabControl 已启用关闭按钮，可直接点击页签右侧关闭并观察 Python 回调。", 14, 234, 360, 40, fg=0xFF606266, wrap=True)

    preview = groupbox(page, "🧪 TabControl 样式预览", 460, 16, 1010, 650)
    STATE["group_tabstyle_preview"] = preview
    label(preview, "主预览", 16, 22, 120, 20, fg=0xFF606266, bg=THEME_SURFACE, size=12, bold=True)
    demo = DLL.CreateTabControl(preview, 16, 48, 960, 290)
    bind_right_click(demo)
    DLL.SetTabItemSize(demo, 148, 36)
    DLL.SetTabPadding(demo, 18, 8)
    DLL.SetTabColors(demo, 13, 14, 5, 6)
    DLL.SetTabIndicatorColor(demo, 0xFF409EFF)
    demo_titles = ("📊 总览", "👥 成员", "📝 日志", "⚙️ 设置")
    for idx, title in enumerate(demo_titles):
        content = add_tab(demo, title)
        label(content, f"这是主预览页签 {idx + 1}", 18, 18, 220, 24, size=14, bold=True)
        label(content, "点击上面的样式按钮或页签右侧关闭按钮，检查重绘与关闭回调。", 18, 52, 420, 24, fg=0xFF606266)
        button(content, "🧪", f"测试按钮 {idx + 1}", 18, 96, 170, 38, 0xFF409EFF, lambda i=idx: set_status(f"Tab 样式主预览按钮 -> {i + 1}"))
        edit(content, f"页签 {idx + 1} 的内容区域仍然可正常交互。", 210, 96, 300, 36, False)
    DLL.UpdateTabControlLayout(demo)
    enable_closable_tab_control(demo, demo_titles)
    DLL.SelectTab(demo, 0)
    STATE["tab_style_demo"] = demo

    label(preview, "次预览", 16, 362, 120, 20, fg=0xFF606266, bg=THEME_SURFACE, size=12, bold=True)
    secondary = DLL.CreateTabControl(preview, 16, 388, 460, 180)
    bind_right_click(secondary)
    DLL.SetTabItemSize(secondary, 126, 34)
    DLL.SetTabPadding(secondary, 16, 8)
    DLL.SetTabColors(secondary, 13, 14, 5, 6)
    DLL.SetTabIndicatorColor(secondary, 0xFF67C23A)
    secondary_titles = ("🧩 组件", "🌲 树形", "⭐ 评分")
    for idx, title in enumerate(secondary_titles):
        content = add_tab(secondary, title)
        label(content, f"次预览页签 {idx + 1}", 16, 16, 180, 24, size=14, bold=True)
        label(content, "用于检查小尺寸 TabControl 的关闭按钮、样式切换和回调。", 16, 48, 360, 24, fg=0xFF606266)
    DLL.UpdateTabControlLayout(secondary)
    enable_closable_tab_control(secondary, secondary_titles)
    DLL.SelectTab(secondary, 0)
    STATE["tab_style_secondary"] = secondary
    apply_demo_tab_style(TAB_HEADER_STYLE_CARD_PLAIN)


def on_main_tab(h: HWND, idx: int) -> None:
    del h
    names = ["基础组件", "选择组件", "数据组件", "页签与弹窗", "布局器演示", "主题换肤", "菜单与树形", "Tab 样式"]
    set_status(f"主 TabControl 已切换到: {names[idx]}")


def enable_closable_tab_control(tab: HWND, titles: tuple[str, ...] | list[str]) -> None:
    if not tab:
        return
    tabs = STATE.setdefault("closable_tabs", {})
    tabs[hwnd_key(tab)] = list(titles)
    DLL.SetTabClosable(tab, 1)
    cb = STATE.get("tab_close_cb")
    if cb:
        DLL.SetTabCloseCallback(tab, cb)
    DLL.RedrawTabControl(tab)


def on_tab_close(h_tab: HWND, idx: int) -> None:
    tabs = STATE.get("closable_tabs", {})
    if not isinstance(tabs, dict):
        return
    titles = tabs.get(hwnd_key(h_tab))
    if not titles or not isinstance(titles, list):
        return
    if idx < 0 or idx >= len(titles):
        return
    if len(titles) <= 1:
        set_status("🗂️ 演示 TabControl 至少保留一个页签，最后一个不关闭。")
        return

    title = titles[idx]
    if DLL.RemoveTabItem(h_tab, idx):
        titles.pop(idx)
        set_status(f"🗂️ 已关闭示例页签: {title}")
    else:
        set_status(f"🗂️ 关闭示例页签失败: {title}")


def menu_add(menu: HWND, text: str, item_id: int) -> None:
    p, n, _ = s(text)
    DLL.PopupMenuAddItem(menu, p, n, item_id)


def create_popup(owner: HWND, items: tuple[tuple[str, int], ...], cb) -> HWND:
    menu = DLL.CreateEmojiPopupMenu(owner)
    for text, item_id in items:
        menu_add(menu, text, item_id)
    DLL.SetPopupMenuCallback(menu, cb)
    return menu


def menu_bar(hwnd: HWND) -> HWND:
    bar = DLL.CreateMenuBar(hwnd)
    bind_right_click(bar)
    DLL.SetMenuBarPlacement(bar, 16, 34, 420, 32)
    p, n, _ = s("🧩 组件测试")
    DLL.MenuBarAddItem(bar, p, n, 1000)
    p, n, _ = s("💬 显示消息框")
    DLL.MenuBarAddSubItem(bar, 1000, p, n, MENU_MSG)
    p, n, _ = s("❓ 显示确认框")
    DLL.MenuBarAddSubItem(bar, 1000, p, n, MENU_CONFIRM)
    p, n, _ = s("🗂️ 切换页签")
    DLL.MenuBarAddItem(bar, p, n, 1001)
    for text, item_id in (
        ("🧩 基础组件", MENU_TAB_BASIC),
        ("📚 选择组件", MENU_TAB_SELECT),
        ("🧾 数据组件", MENU_TAB_DATA),
        ("🗂️ 页签与弹窗", MENU_TAB_TABS),
        ("📐 布局器演示", MENU_TAB_LAYOUT),
        ("🎨 主题换肤", MENU_TAB_THEME),
    ):
        p, n, _ = s(text)
        DLL.MenuBarAddSubItem(bar, 1001, p, n, item_id)
    mcb = DLL._MenuCB(on_menu)
    KEEP.append(mcb)
    DLL.SetMenuBarCallback(bar, mcb)
    return bar


def popup_bind(window_hwnd: HWND, page_handles: list[HWND], group_handles: list[HWND], tab_handles: list[HWND], grid: HWND, btn_parent: HWND, btn_id: int, chk: HWND) -> None:
    pcb = DLL._MenuCB(on_menu)
    KEEP.append(pcb)

    window_menu = create_popup(window_hwnd, (("🪟 查看窗口状态", POP_WINDOW_STATUS), ("💬 显示消息框", POP_WINDOW_MSG)), pcb)
    page_menu = create_popup(window_hwnd, (("🗂️ 查看页内容状态", POP_PAGE_STATUS), ("💬 页内容弹消息框", POP_PAGE_MSG)), pcb)
    group_menu = create_popup(window_hwnd, (("📦 查看分组框状态", POP_GROUP_STATUS), ("💬 分组框弹消息框", POP_GROUP_MSG)), pcb)
    tab_menu = create_popup(window_hwnd, (("🧷 查看 TabControl 状态", POP_TAB_STATUS), ("💬 TabControl 弹消息框", POP_TAB_MSG)), pcb)
    grid_menu = create_popup(window_hwnd, (("➕ 添加一行", POP_GRID_ADD), ("📊 查看表格状态", POP_GRID_STATUS)), pcb)
    button_menu = create_popup(window_hwnd, (("🔘 按钮菜单状态", POP_BUTTON_STATUS),), pcb)
    checkbox_menu = create_popup(window_hwnd, (("☑️ 切换勾选", POP_CHECKBOX_TOGGLE),), pcb)

    DLL.BindControlMenu(window_hwnd, window_menu)
    for h in page_handles:
        DLL.BindControlMenu(h, page_menu)
    for h in group_handles:
        DLL.BindControlMenu(h, group_menu)
    for h in tab_handles:
        DLL.BindControlMenu(h, tab_menu)
    DLL.BindControlMenu(grid, grid_menu)
    DLL.BindButtonMenu(btn_parent, btn_id, button_menu)
    DLL.BindControlMenu(chk, checkbox_menu)


def build() -> None:
    p, n, _ = s("🧩 emoji_window 全组件综合测试")
    hwnd = DLL.create_window_bytes(p, n, 60, 40, 1540, 980)
    if not hwnd:
        raise RuntimeError("创建窗口失败")
    STATE["hwnd"] = hwnd
    bind_right_click(hwnd)

    bcb = DLL._ButtonCB(on_button_click)
    ccb = DLL._ConfirmCB(on_confirm)
    KEEP.extend([bcb, ccb])
    DLL.set_button_click_callback(bcb)
    STATE["confirm_cb"] = ccb

    menu_bar(hwnd)
    tab = DLL.CreateTabControl(hwnd, 16, 76, 1504, 838)
    bind_right_click(tab)
    STATE["main_tab"] = tab
    DLL.SetTabContentBgColorAll(tab, 13)
    DLL.SetTabHeaderStyle(tab, TAB_HEADER_STYLE_CARD_PLAIN)
    DLL.SetTabItemSize(tab, 158, 38)
    DLL.SetTabPadding(tab, 22, 10)
    DLL.SetTabColors(tab, 13, 14, 5, 6)
    DLL.SetTabIndicatorColor(tab, 0xFF409EFF)
    mtcb = DLL._TabCB(on_main_tab)
    KEEP.append(mtcb)
    DLL.SetTabCallback(tab, mtcb)

    pages = [add_tab(tab, t) for t in ("🧩 基础组件", "📚 选择组件", "🧾 数据组件", "🗂️ 页签与弹窗", "📐 布局器演示", "🎨 主题换肤")]
    STATE["main_pages"] = pages
    basic_btn_parent, basic_btn = basic_page(pages[TAB_BASIC])
    select_page(pages[TAB_SELECT])
    chk, data_btn_parent, data_btn = data_page_v4(pages[TAB_DATA])
    tabs_page(pages[TAB_TABS])
    layout_page(pages[TAB_LAYOUT])
    theme_page(pages[TAB_THEME])
    popup_bind(
        hwnd,
        list(pages) + list(STATE.get("nested_pages", [])),
        [
            STATE.get("group_basic_text"),
            STATE.get("group_basic_select"),
            STATE.get("group_basic_button_styles"),
            STATE.get("group_basic_tips"),
            STATE.get("group_select_list"),
            STATE.get("group_select_media"),
            STATE.get("group_select_tips"),
            STATE.get("group_data_grid"),
            STATE.get("group_data_menu"),
            STATE.get("group_tabs_nested"),
            STATE.get("group_tabs_action"),
            STATE.get("group_layout_actions"),
            STATE.get("group_layout_host"),
            STATE.get("group_layout_tips"),
            STATE.get("group_theme_actions"),
            STATE.get("group_theme_sample"),
        ],
        [STATE.get("main_tab"), STATE.get("nested_tab")],
        STATE["grid"],
        data_btn_parent,
        data_btn,
        chk,
    )
    DLL.UpdateTabControlLayout(tab)
    if STATE["nested_tab"]:
        DLL.UpdateTabControlLayout(STATE["nested_tab"])
        DLL.SelectTab(STATE["nested_tab"], 0)
    DLL.SelectTab(tab, TAB_BASIC)

    STATE["status"] = label(hwnd, "🧭 状态: 综合测试窗口已初始化。请切换页签、点击按钮、右键菜单并检查各组件回调。", 16, 924, 1504, 32, fg=0xFF303133, bg=0xFFF5F7FA)


def menu_add_sub(menu: HWND, parent_id: int, text: str, item_id: int) -> None:
    p, n, _ = s(text)
    DLL.PopupMenuAddSubItem(menu, parent_id, p, n, item_id)


def menu_bar(hwnd: HWND) -> HWND:
    bar = DLL.CreateMenuBar(hwnd)
    bind_right_click(bar)
    DLL.SetMenuBarPlacement(bar, 16, 34, 520, 32)

    p, n, _ = s("📁 文件")
    DLL.MenuBarAddItem(bar, p, n, 1000)
    p, n, _ = s("💬 对话框")
    DLL.MenuBarAddSubItem(bar, 1000, p, n, 1010)
    p, n, _ = s("🧭 跳转页签")
    DLL.MenuBarAddSubItem(bar, 1000, p, n, 1011)
    p, n, _ = s("🌲 树形框动作")
    DLL.MenuBarAddSubItem(bar, 1000, p, n, 1012)
    p, n, _ = s("⭐ 评分动作")
    DLL.MenuBarAddSubItem(bar, 1000, p, n, 1013)

    for parent_id, text, item_id in (
        (1010, "📨 显示消息框", MENU_MSG),
        (1010, "✅ 显示确认框", MENU_CONFIRM),
        (1011, "🧩 基础组件", MENU_TAB_BASIC),
        (1011, "📚 选择组件", MENU_TAB_SELECT),
        (1011, "🧾 数据组件", MENU_TAB_DATA),
        (1011, "🗂️ 页签与弹窗", MENU_TAB_TABS),
        (1011, "📐 布局器演示", MENU_TAB_LAYOUT),
        (1011, "🎨 主题换肤", MENU_TAB_THEME),
        (1011, "📁 菜单与树形", MENU_TAB_MENU_TREE),
        (1011, "🗂️ Tab 样式", MENU_TAB_TAB_STYLES),
        (1012, "➕ 全部展开", MENU_TREE_EXPAND),
        (1012, "➖ 全部折叠", MENU_TREE_COLLAPSE),
        (1012, "⇆ 切换侧边栏", MENU_TREE_TOGGLE_SIDEBAR),
        (1013, "⭐ 1 分", MENU_RATING_1),
        (1013, "⭐⭐⭐ 3 分", MENU_RATING_3),
        (1013, "⭐⭐⭐⭐⭐ 5 分", MENU_RATING_5),
        (1013, "✖ 清空评分", MENU_RATING_CLEAR),
    ):
        p, n, _ = s(text)
        DLL.MenuBarAddSubItem(bar, parent_id, p, n, item_id)

    p, n, _ = s("🗂️ 直接跳转")
    DLL.MenuBarAddItem(bar, p, n, 1001)
    for text, item_id in (
        ("🧩 基础组件", MENU_TAB_BASIC),
        ("📚 选择组件", MENU_TAB_SELECT),
        ("🧾 数据组件", MENU_TAB_DATA),
        ("🗂️ 页签与弹窗", MENU_TAB_TABS),
        ("📐 布局器演示", MENU_TAB_LAYOUT),
        ("🎨 主题换肤", MENU_TAB_THEME),
        ("📁 菜单与树形", MENU_TAB_MENU_TREE),
        ("🗂️ Tab 样式", MENU_TAB_TAB_STYLES),
    ):
        p, n, _ = s(text)
        DLL.MenuBarAddSubItem(bar, 1001, p, n, item_id)

    mcb = DLL._MenuCB(on_menu)
    KEEP.append(mcb)
    DLL.SetMenuBarCallback(bar, mcb)
    return bar


def popup_bind(window_hwnd: HWND, page_handles: list[HWND], group_handles: list[HWND], tab_handles: list[HWND], grid: HWND, btn_parent: HWND, btn_id: int, chk: HWND) -> None:
    pcb = DLL._MenuCB(on_menu)
    KEEP.append(pcb)

    window_menu = DLL.CreateEmojiPopupMenu(window_hwnd)
    menu_add(window_menu, "🪟 窗口动作", 2901)
    menu_add(window_menu, "🧭 快速跳转", 2902)
    menu_add(window_menu, "🌲 树形框", 2903)
    menu_add(window_menu, "⭐ 评分", 2904)
    for parent_id, text, item_id in (
        (2901, "🪟 查看窗口状态", POP_WINDOW_STATUS),
        (2901, "💬 显示消息框", POP_WINDOW_MSG),
        (2902, "🧩 基础组件", MENU_TAB_BASIC),
        (2902, "📚 选择组件", MENU_TAB_SELECT),
        (2902, "🧾 数据组件", MENU_TAB_DATA),
        (2902, "🗂️ 页签与弹窗", MENU_TAB_TABS),
        (2902, "📐 布局器演示", MENU_TAB_LAYOUT),
        (2902, "🎨 主题换肤", MENU_TAB_THEME),
        (2902, "📁 菜单与树形", MENU_TAB_MENU_TREE),
        (2902, "🗂️ Tab 样式", MENU_TAB_TAB_STYLES),
        (2903, "➕ 全部展开", POP_TREE_EXPAND),
        (2903, "➖ 全部折叠", POP_TREE_COLLAPSE),
        (2903, "⇆ 切换侧边栏", POP_TREE_TOGGLE_SIDEBAR),
        (2904, "⭐⭐⭐ 3 分", POP_RATING_3),
        (2904, "⭐⭐⭐⭐⭐ 5 分", POP_RATING_5),
        (2904, "✖ 清空评分", POP_RATING_CLEAR),
    ):
        menu_add_sub(window_menu, parent_id, text, item_id)
    DLL.SetPopupMenuCallback(window_menu, pcb)

    page_menu = create_popup(window_hwnd, (("🗂️ 查看页内容状态", POP_PAGE_STATUS), ("💬 页内容弹消息框", POP_PAGE_MSG)), pcb)
    group_menu = create_popup(window_hwnd, (("📦 查看分组框状态", POP_GROUP_STATUS), ("💬 分组框弹消息框", POP_GROUP_MSG)), pcb)
    tab_menu = create_popup(window_hwnd, (("🗂️ 查看 TabControl 状态", POP_TAB_STATUS), ("💬 TabControl 弹消息框", POP_TAB_MSG)), pcb)
    grid_menu = create_popup(window_hwnd, (("➕ 添加一行", POP_GRID_ADD), ("📊 查看表格状态", POP_GRID_STATUS)), pcb)
    button_menu = create_popup(window_hwnd, (("🔘 按钮菜单状态", POP_BUTTON_STATUS),), pcb)
    checkbox_menu = create_popup(window_hwnd, (("☑️ 切换勾选", POP_CHECKBOX_TOGGLE),), pcb)

    DLL.BindControlMenu(window_hwnd, window_menu)
    for h in page_handles:
        DLL.BindControlMenu(h, page_menu)
    for h in group_handles:
        DLL.BindControlMenu(h, group_menu)
    for h in tab_handles:
        DLL.BindControlMenu(h, tab_menu)
    DLL.BindControlMenu(grid, grid_menu)
    DLL.BindButtonMenu(btn_parent, btn_id, button_menu)
    DLL.BindControlMenu(chk, checkbox_menu)

    for h in [STATE.get("main_pages", [None] * 8)[TAB_MENU_TREE] if STATE.get("main_pages") else None, STATE.get("group_menu_actions"), STATE.get("group_tree_styles")] + list(STATE.get("tree_handles", [])):
        if h:
            DLL.BindControlMenu(h, window_menu)


def build() -> None:
    p, n, _ = s("🧩 emoji_window 全组件综合测试")
    hwnd = DLL.create_window_bytes(p, n, 60, 40, 1540, 980)
    if not hwnd:
        raise RuntimeError("创建窗口失败")
    STATE["hwnd"] = hwnd
    bind_right_click(hwnd)

    bcb = DLL._ButtonCB(on_button_click)
    ccb = DLL._ConfirmCB(on_confirm)
    KEEP.extend([bcb, ccb])
    DLL.set_button_click_callback(bcb)
    STATE["confirm_cb"] = ccb

    menu_bar(hwnd)
    tab = DLL.CreateTabControl(hwnd, 16, 76, 1504, 838)
    bind_right_click(tab)
    STATE["main_tab"] = tab
    DLL.SetTabContentBgColorAll(tab, 13)
    DLL.SetTabHeaderStyle(tab, TAB_HEADER_STYLE_CARD_PLAIN)
    DLL.SetTabItemSize(tab, 140, 38)
    DLL.SetTabPadding(tab, 22, 10)
    DLL.SetTabColors(tab, 13, 14, 5, 6)
    DLL.SetTabIndicatorColor(tab, 0xFF409EFF)
    mtcb = DLL._TabCB(on_main_tab)
    KEEP.append(mtcb)
    DLL.SetTabCallback(tab, mtcb)

    pages = [
        add_tab(tab, title)
        for title in (
            "🧩 基础组件",
            "📚 选择组件",
            "🧾 数据组件",
            "🗂️ 页签与弹窗",
            "📐 布局器演示",
            "🎨 主题换肤",
            "📁 菜单与树形",
            "🗂️ Tab 样式",
        )
    ]
    STATE["main_pages"] = pages
    basic_btn_parent, basic_btn = basic_page(pages[TAB_BASIC])
    select_page(pages[TAB_SELECT])
    chk, data_btn_parent, data_btn = data_page_v4(pages[TAB_DATA])
    tabs_page(pages[TAB_TABS])
    layout_page(pages[TAB_LAYOUT])
    theme_page(pages[TAB_THEME])
    menu_tree_page(pages[TAB_MENU_TREE])
    tab_styles_page(pages[TAB_TAB_STYLES])

    popup_bind(
        hwnd,
        list(pages) + list(STATE.get("nested_pages", [])),
        [
            STATE.get("group_basic_text"),
            STATE.get("group_basic_select"),
            STATE.get("group_basic_button_styles"),
            STATE.get("group_basic_tips"),
            STATE.get("group_select_list"),
            STATE.get("group_select_media"),
            STATE.get("group_select_tips"),
            STATE.get("group_data_grid"),
            STATE.get("group_data_menu"),
            STATE.get("group_tabs_nested"),
            STATE.get("group_tabs_action"),
            STATE.get("group_layout_actions"),
            STATE.get("group_layout_host"),
            STATE.get("group_layout_tips"),
            STATE.get("group_theme_actions"),
            STATE.get("group_theme_sample"),
            STATE.get("group_menu_actions"),
            STATE.get("group_tree_styles"),
            STATE.get("group_tabstyle_actions"),
            STATE.get("group_tabstyle_preview"),
        ],
        [STATE.get("main_tab"), STATE.get("nested_tab"), STATE.get("tab_style_demo"), STATE.get("tab_style_secondary")],
        STATE["grid"],
        data_btn_parent,
        data_btn,
        chk,
    )
    DLL.UpdateTabControlLayout(tab)
    for key in ("nested_tab", "tab_style_demo", "tab_style_secondary"):
        h_tab = STATE.get(key)
        if h_tab:
            DLL.UpdateTabControlLayout(h_tab)
            DLL.SelectTab(h_tab, 0)
    DLL.SelectTab(tab, TAB_BASIC)

    STATE["status"] = label(hwnd, "📋 状态: 综合测试窗口已初始化。请切换页签、点击按钮、右键菜单并检查各组件回调。", 16, 924, 1504, 32, fg=0xFF303133, bg=0xFFF5F7FA)
    set_rating(int(STATE.get("rating_value", 3)))


def menu_tree_page(page: HWND) -> None:
    actions = groupbox(page, "📁 多级菜单与评分", 16, 16, 420, 650)
    STATE["group_menu_actions"] = actions

    label(page, "顶部 File 菜单和这个页签右键菜单都改成了多级结构。", 36, 54, 360, 22, size=15, bold=True)
    label(page, "1. 右键这个页签空白处、左侧分组框、右侧树形框，都能看到多级 PopupMenu。", 36, 88, 360, 40, fg=0xFF606266, wrap=True)
    label(page, "2. 顶部 MenuBar 的“文件”里包含对话框、页签跳转、树形框动作、评分动作多级演示。", 36, 134, 370, 40, fg=0xFF606266, wrap=True)

    label(page, "⭐ 评分组件演示", 36, 210, 180, 24, size=14, bold=True)
    STATE["rating_label"] = label(page, "⭐ 当前评分: ★★★☆☆  (3/5)", 36, 244, 340, 28, fg=0xFF303133, bg=0xFFFFFFFF, size=16, bold=True)
    button(page, "1", "一星", 36, 288, 70, 36, 0xFF909399, lambda: set_rating(1))
    button(page, "2", "二星", 112, 288, 70, 36, 0xFF909399, lambda: set_rating(2))
    button(page, "3", "三星", 188, 288, 70, 36, 0xFF409EFF, lambda: set_rating(3))
    button(page, "4", "四星", 264, 288, 70, 36, 0xFFE6A23C, lambda: set_rating(4))
    button(page, "5", "五星", 340, 288, 70, 36, 0xFF67C23A, lambda: set_rating(5))
    button(page, "✖", "清空评分", 36, 334, 150, 36, 0xFFF56C6C, lambda: set_rating(0))

    label(page, "🌲 主树控制", 36, 398, 180, 24, size=14, bold=True)
    button(page, "➕", "全部展开", 36, 432, 116, 36, 0xFF409EFF, lambda: on_menu(0, MENU_TREE_EXPAND))
    button(page, "➖", "全部折叠", 162, 432, 116, 36, 0xFFE6A23C, lambda: on_menu(0, MENU_TREE_COLLAPSE))
    button(page, "⇆", "切换侧边栏", 288, 432, 122, 36, 0xFF67C23A, lambda: on_menu(0, MENU_TREE_TOGGLE_SIDEBAR))
    STATE["tree_status_label"] = label(page, "🌲 主树状态: ready", 36, 484, 370, 56, fg=0xFF606266, bg=0xFFFFFFFF, wrap=True)
    label(page, "树形框支持默认列表、Sidebar 导航、紧凑模式、宽松模式，以及拖拽排序。", 36, 562, 370, 40, fg=0xFF606266, wrap=True)
    label(page, "评分演示当前使用现有按钮组合实现交互，可直接验证状态和菜单回调。", 36, 612, 370, 40, fg=0xFF606266, wrap=True)

    trees = groupbox(page, "🌲 TreeView 样式总览", 460, 16, 1010, 650)
    STATE["group_tree_styles"] = trees
    t1 = create_tree_style(
        page, "Default", 480, 54, 13, 5,
        sidebar=False, row_height=34.0, spacing=5.0,
        selected_bg=15, selected_fg=0, hover_bg=14, dragdrop=False,
    )
    t2 = create_tree_style(
        page, "Sidebar", 980, 54, 14, 5,
        sidebar=True, row_height=40.0, spacing=6.0,
        selected_bg=0, selected_fg=0xFFFFFFFF, hover_bg=15, dragdrop=False,
    )
    t3 = create_tree_style(
        page, "Compact", 480, 342, 13, 5,
        sidebar=False, row_height=28.0, spacing=2.0,
        selected_bg=16, selected_fg=1, hover_bg=14, dragdrop=True,
    )
    t4 = create_tree_style(
        page, "Relaxed", 980, 342, 14, 5,
        sidebar=False, row_height=42.0, spacing=10.0,
        selected_bg=17, selected_fg=2, hover_bg=14, dragdrop=False,
    )
    STATE["tree_primary"] = t1
    STATE["tree_sidebar_enabled"] = False
    STATE["tree_handles"] = [t1, t2, t3, t4]
    set_rating(int(STATE.get("rating_value", 3)))


def tab_styles_page(page: HWND) -> None:
    actions = groupbox(page, "🗂️ Tab 样式切换", 16, 16, 420, 650)
    STATE["group_tabstyle_actions"] = actions

    label(page, "四个按钮直接切换下方两个 TabControl 的页签头样式。", 36, 54, 360, 24, size=15, bold=True)
    label(page, "这里不再动主窗口的总页签，只演示独立 TabControl 的 header 风格。", 36, 88, 360, 40, fg=0xFF606266, wrap=True)
    button(page, "━", "Line", 36, 158, 170, 38, 0xFF909399, lambda: apply_demo_tab_style(TAB_HEADER_STYLE_LINE))
    button(page, "▣", "Card", 220, 158, 170, 38, 0xFF409EFF, lambda: apply_demo_tab_style(TAB_HEADER_STYLE_CARD))
    button(page, "▤", "Card Plain", 36, 206, 170, 38, 0xFF67C23A, lambda: apply_demo_tab_style(TAB_HEADER_STYLE_CARD_PLAIN))
    button(page, "◫", "Segmented", 220, 206, 170, 38, 0xFFE6A23C, lambda: apply_demo_tab_style(TAB_HEADER_STYLE_SEGMENTED))
    label(page, "两个示例 TabControl 已启用关闭按钮，可直接点击页签右侧关闭并观察 Python 回调。", 36, 270, 360, 40, fg=0xFF606266, wrap=True)

    preview = groupbox(page, "🧪 TabControl 样式预览", 460, 16, 1010, 650)
    STATE["group_tabstyle_preview"] = preview

    label(page, "主预览", 480, 54, 120, 20, fg=0xFF606266, bg=THEME_SURFACE, size=12, bold=True)
    demo = DLL.CreateTabControl(page, 480, 80, 960, 290)
    bind_right_click(demo)
    DLL.SetTabItemSize(demo, 148, 36)
    DLL.SetTabPadding(demo, 18, 8)
    DLL.SetTabColors(demo, 13, 14, 5, 6)
    DLL.SetTabIndicatorColor(demo, 0xFF409EFF)
    demo_titles = ("📊 总览", "👥 成员", "📝 日志", "⚙️ 设置")
    for idx, title in enumerate(demo_titles):
        content = add_tab(demo, title)
        label(content, f"这是主预览页签 {idx + 1}", 18, 18, 220, 24, size=14, bold=True)
        label(content, "点击上面的样式按钮或页签右侧关闭按钮，检查重绘与关闭回调。", 18, 52, 420, 24, fg=0xFF606266)
        button(content, "🧪", f"测试按钮 {idx + 1}", 18, 96, 170, 38, 0xFF409EFF, lambda i=idx: set_status(f"Tab 样式主预览按钮 -> {i + 1}"))
        edit(content, f"页签 {idx + 1} 的内容区域仍然可正常交互。", 210, 96, 300, 36, False)
    DLL.UpdateTabControlLayout(demo)
    enable_closable_tab_control(demo, demo_titles)
    DLL.SelectTab(demo, 0)
    STATE["tab_style_demo"] = demo

    label(page, "次预览", 480, 400, 120, 20, fg=0xFF606266, bg=THEME_SURFACE, size=12, bold=True)
    secondary = DLL.CreateTabControl(page, 480, 426, 460, 180)
    bind_right_click(secondary)
    DLL.SetTabItemSize(secondary, 126, 34)
    DLL.SetTabPadding(secondary, 16, 8)
    DLL.SetTabColors(secondary, 13, 14, 5, 6)
    DLL.SetTabIndicatorColor(secondary, 0xFF67C23A)
    secondary_titles = ("🧩 组件", "🌲 树形", "⭐ 评分")
    for idx, title in enumerate(secondary_titles):
        content = add_tab(secondary, title)
        label(content, f"次预览页签 {idx + 1}", 16, 16, 180, 24, size=14, bold=True)
        label(content, "用于检查小尺寸 TabControl 的关闭按钮、样式切换和回调。", 16, 48, 360, 24, fg=0xFF606266)
    DLL.UpdateTabControlLayout(secondary)
    enable_closable_tab_control(secondary, secondary_titles)
    DLL.SelectTab(secondary, 0)
    STATE["tab_style_secondary"] = secondary
    apply_demo_tab_style(TAB_HEADER_STYLE_CARD_PLAIN)


def on_main_tab(h: HWND, idx: int) -> None:
    del h
    names = ["基础组件", "选择组件", "数据组件", "页签与弹窗", "布局器演示", "主题换肤", "菜单与树形", "Tab 样式"]
    set_status(f"主 TabControl 已切换到: {names[idx]}")


def set_layout_mode(mode: str) -> None:
    host = STATE.get("layout_host")
    controls = list(STATE.get("layout_controls", []))
    if not host or not controls:
        return

    STATE["layout_mode"] = mode
    DLL.RemoveLayoutManager(host)

    top_label, search_box, city_combo, fruit_list, progress_bar, memo_box = controls

    if mode == "flow_h":
        DLL.SetLayoutManager(host, LAYOUT_FLOW_HORIZONTAL, 0, 0, 12)
        DLL.SetLayoutPadding(host, 18, 42, 18, 18)
        for ctrl in controls:
            DLL.AddControlToLayout(host, ctrl)
            DLL.SetControlLayoutProps(ctrl, 0, 0, 0, 0, DOCK_NONE, BOOL(False), BOOL(False))
        set_status("🧰 布局器 已切到水平流式布局。")
    elif mode == "flow_v":
        DLL.SetLayoutManager(host, LAYOUT_FLOW_VERTICAL, 0, 0, 12)
        DLL.SetLayoutPadding(host, 18, 42, 18, 18)
        for ctrl in controls:
            DLL.AddControlToLayout(host, ctrl)
            DLL.SetControlLayoutProps(ctrl, 0, 0, 0, 0, DOCK_NONE, BOOL(True), BOOL(False))
        set_status("🧰 布局器 已切到垂直流式布局。")
    elif mode == "grid":
        DLL.SetLayoutManager(host, LAYOUT_GRID, 2, 3, 12)
        DLL.SetLayoutPadding(host, 18, 42, 18, 18)
        for ctrl in controls:
            DLL.AddControlToLayout(host, ctrl)
        DLL.SetControlLayoutProps(top_label, 0, 0, 0, 0, DOCK_NONE, BOOL(True), BOOL(True))
        DLL.SetControlLayoutProps(search_box, 0, 0, 0, 0, DOCK_NONE, BOOL(True), BOOL(False))
        DLL.SetControlLayoutProps(city_combo, 0, 0, 0, 0, DOCK_NONE, BOOL(True), BOOL(False))
        DLL.SetControlLayoutProps(fruit_list, 0, 0, 0, 0, DOCK_NONE, BOOL(True), BOOL(True))
        DLL.SetControlLayoutProps(progress_bar, 0, 0, 0, 0, DOCK_NONE, BOOL(True), BOOL(False))
        DLL.SetControlLayoutProps(memo_box, 0, 0, 0, 0, DOCK_NONE, BOOL(True), BOOL(True))
        set_status("🧰 布局器 已切到 2x3 网格布局。")
    else:
        DLL.SetLayoutManager(host, LAYOUT_DOCK, 0, 0, 10)
        DLL.SetLayoutPadding(host, 18, 42, 18, 18)
        for ctrl in controls:
            DLL.AddControlToLayout(host, ctrl)
        DLL.SetControlLayoutProps(top_label, 0, 0, 0, 0, DOCK_TOP, BOOL(True), BOOL(False))
        DLL.SetControlLayoutProps(search_box, 0, 0, 0, 0, DOCK_TOP, BOOL(True), BOOL(False))
        DLL.SetControlLayoutProps(city_combo, 0, 0, 0, 0, DOCK_RIGHT, BOOL(False), BOOL(False))
        DLL.SetControlLayoutProps(fruit_list, 0, 0, 0, 0, DOCK_LEFT, BOOL(False), BOOL(True))
        DLL.SetControlLayoutProps(progress_bar, 0, 0, 0, 0, DOCK_BOTTOM, BOOL(True), BOOL(False))
        DLL.SetControlLayoutProps(memo_box, 0, 0, 0, 0, DOCK_FILL, BOOL(True), BOOL(True))
        set_status("🧰 布局器 已切到停靠布局。")

    DLL.UpdateLayout(host)


def on_slider_changed(hwnd: HWND, value: int) -> None:
    del hwnd
    set_status(f"🎚️ Slider 值已变更为 {value}")


def on_switch_changed(hwnd: HWND, checked: BOOL) -> None:
    del hwnd
    set_status(f"🔀 Switch 当前状态: {'开启' if checked else '关闭'}")


def on_notification_event(hwnd: HWND, event_type: int) -> None:
    del hwnd
    set_status(f"🔔 Notification 事件: {'点击内容' if event_type == 1 else '关闭'}")


_base_basic_page = basic_page


def basic_page(page: HWND) -> tuple[HWND, int]:
    basic_btn_parent, basic_btn = _base_basic_page(page)

    extra = groupbox(page, "🪄 Element Plus 扩展样式", 16, 512, 1454, 180)
    label(page, "Checkbox / Radio 按钮样式、带边框样式，以及 Slider / Switch 演示", 36, 548, 620, 24, size=15, bold=True)

    cb_btn_p, cb_btn_n, _ = s("🧩 Checkbox 按钮样式")
    cb_card_p, cb_card_n, _ = s("🪟 Checkbox 边框样式")
    cb_btn = DLL.CreateCheckBox(page, 36, 586, 210, 36, cb_btn_p, cb_btn_n, BOOL(True), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    cb_card = DLL.CreateCheckBox(page, 256, 586, 210, 40, cb_card_p, cb_card_n, BOOL(False), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    DLL.SetCheckBoxStyle(cb_btn, 2)
    DLL.SetCheckBoxStyle(cb_card, 3)
    DLL.SetCheckBoxCheckColor(cb_btn, 0xFF409EFF)
    DLL.SetCheckBoxCheckColor(cb_card, 0xFF67C23A)

    rb_default_p, rb_default_n, _ = s("🎯 Radio 默认")
    rb_border_p, rb_border_n, _ = s("🪟 Radio 带边框")
    rb_button_p, rb_button_n, _ = s("🔘 Radio 按钮")
    rb_default = DLL.CreateRadioButton(page, 500, 586, 130, 36, rb_default_p, rb_default_n, 77, BOOL(True), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    rb_border = DLL.CreateRadioButton(page, 640, 586, 150, 36, rb_border_p, rb_border_n, 77, BOOL(False), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    rb_button = DLL.CreateRadioButton(page, 800, 586, 140, 36, rb_button_p, rb_button_n, 77, BOOL(False), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    DLL.SetRadioButtonStyle(rb_border, RADIO_STYLE_BORDER)
    DLL.SetRadioButtonStyle(rb_button, RADIO_STYLE_BUTTON)
    DLL.SetRadioButtonDotColor(rb_default, 0xFF409EFF)
    DLL.SetRadioButtonDotColor(rb_border, 0xFFE6A23C)
    DLL.SetRadioButtonDotColor(rb_button, 0xFF67C23A)

    slider = DLL.CreateSlider(page, 980, 586, 240, 34, 0, 100, 36, 10, 0xFF409EFF, 0xFFE4E7ED)
    DLL.SetSliderShowStops(slider, BOOL(True))
    switch_on_p, switch_on_n, _ = s("开")
    switch_off_p, switch_off_n, _ = s("关")
    sw = DLL.CreateSwitch(page, 1240, 582, 88, 34, BOOL(True), 0xFF13CE66, 0xFFDCDfe6, switch_on_p, switch_on_n, switch_off_p, switch_off_n)

    cb = DLL._CheckBoxCB(on_checkbox)
    rb = DLL._RadioCB(on_radio)
    sl = DLL._SliderCB(on_slider_changed)
    sc = DLL._SwitchCB(on_switch_changed)
    KEEP.extend([cb, rb, sl, sc])
    DLL.SetCheckBoxCallback(cb_btn, cb)
    DLL.SetCheckBoxCallback(cb_card, cb)
    DLL.SetRadioButtonCallback(rb_default, rb)
    DLL.SetRadioButtonCallback(rb_border, rb)
    DLL.SetRadioButtonCallback(rb_button, rb)
    DLL.SetSliderCallback(slider, sl)
    DLL.SetSwitchCallback(sw, sc)
    bind_right_click_many(cb_btn, cb_card, rb_default, rb_border, rb_button, slider, sw)

    label(page, "🎚️ Slider 参考 Element Plus 水平滑块，支持步长与停点；🔀 Switch 支持开关文字。", 36, 640, 900, 22, fg=0xFF606266)
    return basic_btn_parent, basic_btn


_base_select_page = select_page


def select_page(page: HWND) -> None:
    _base_select_page(page)

    extra = groupbox(page, "🔔 Notification / Tooltip", 16, 572, 1454, 170)
    label(page, "Element Plus 通知、文字提示、气泡确认框综合测试", 36, 608, 440, 24, size=15, bold=True)

    tooltip_target = label(page, "🧷 鼠标移到这里查看 Tooltip", 36, 646, 220, 24, fg=0xFF303133, bg=0xFFFFFFFF, size=13, bold=True)
    tip_p, tip_n, _ = s("📝 这是一个 Element Plus 风格 Tooltip")
    tooltip = DLL.CreateTooltip(page, tip_p, tip_n, POPUP_TOP, THEME_SURFACE, THEME_TEXT)
    enter_cb = DLL._ValueCB(lambda h: DLL.ShowTooltipForControl(tooltip, h))
    leave_cb = DLL._ValueCB(lambda h: DLL.HideTooltip(tooltip))
    KEEP.extend([enter_cb, leave_cb])
    DLL.SetMouseEnterCallback(tooltip_target, enter_cb)
    DLL.SetMouseLeaveCallback(tooltip_target, leave_cb)

    note_cb = DLL._NotificationCB(on_notification_event)
    KEEP.append(note_cb)
    button(extra, "🔵", "信息通知", 700, 60, 120, 38, 0xFF409EFF, lambda: _show_note(page, "🔔 信息通知", "📝 这是一条 info 类型通知。", NOTIFY_INFO, note_cb))
    button(extra, "🟢", "成功通知", 830, 60, 120, 38, 0xFF67C23A, lambda: _show_note(page, "✅ 操作成功", "🎉 这是一条 success 类型通知。", NOTIFY_SUCCESS, note_cb))
    button(extra, "🟠", "警告通知", 960, 60, 120, 38, 0xFFE6A23C, lambda: _show_note(page, "⚠️ 注意", "📌 这是一条 warning 类型通知。", NOTIFY_WARNING, note_cb))
    button(extra, "🔴", "错误通知", 1090, 60, 120, 38, 0xFFF56C6C, lambda: _show_note(page, "❌ 失败", "🧯 这是一条 error 类型通知。", NOTIFY_ERROR, note_cb))

    label(page, "Tooltip 绑定在左侧标签；Notification 演示四种语义色。", 36, 686, 760, 22, fg=0xFF606266)


def _show_note(owner: HWND, title: str, message: str, note_type: int, cb) -> None:
    tp, tn, _ = s(title)
    mp, mn, _ = s(message)
    h = DLL.ShowNotification(owner, tp, tn, mp, mn, note_type, NOTIFY_TOP_RIGHT, 2600)
    if h:
        DLL.SetNotificationCallback(h, cb)


def _bind_tooltip_demo_hover(hwnd: HWND, normal_fg: int, normal_bg: int, hover_fg: int, hover_bg: int) -> None:
    enter_cb = DLL._ValueCB(lambda h, fg=hover_fg, bg=hover_bg: DLL.SetLabelColor(h, fg, bg))
    leave_cb = DLL._ValueCB(lambda h, fg=normal_fg, bg=normal_bg: DLL.SetLabelColor(h, fg, bg))
    KEEP.extend([enter_cb, leave_cb])
    DLL.SetMouseEnterCallback(hwnd, enter_cb)
    DLL.SetMouseLeaveCallback(hwnd, leave_cb)


def select_page(page: HWND) -> None:
    _base_select_page(page)

    extra = groupbox(page, "🔔 Notification / Tooltip", 16, 572, 1454, 190)
    label(page, "Element Plus 通知、文字提示、气泡确认框综合测试", 36, 608, 440, 24, size=15, bold=True)
    label(page, "Tooltip 支持上/下/左/右四个方向，dark/light/custom 主题，自定义字体字号颜色，以及 hover/click 两种触发。", 36, 636, 920, 22, fg=0xFF606266)

    hover_top_target = label(page, "⬆ Dark / Top / Hover", 36, 664, 210, 32, fg=0xFFFFFFFF, bg=0xFF303133, size=13, bold=True, align=ALIGN_CENTER)
    hover_bottom_target = label(page, "⬇ Light / Bottom / Hover", 264, 664, 230, 32, fg=0xFF303133, bg=0xFFF5F7FA, size=13, bold=True, align=ALIGN_CENTER)
    hover_left_target = label(page, "⬅ Custom / Left / Hover", 512, 664, 250, 32, fg=0xFF7A4A00, bg=0xFFFFF1D6, size=13, bold=True, align=ALIGN_CENTER)
    click_right_target = label(page, "➡ Dark / Right / Click", 780, 664, 230, 32, fg=0xFFFFFFFF, bg=0xFF409EFF, size=13, bold=True, align=ALIGN_CENTER)
    _bind_tooltip_demo_hover(hover_top_target, 0xFFFFFFFF, 0xFF303133, 0xFFFFFFFF, 0xFF409EFF)
    _bind_tooltip_demo_hover(hover_bottom_target, 0xFF303133, 0xFFF5F7FA, 0xFF409EFF, 0xFFECF5FF)
    _bind_tooltip_demo_hover(hover_left_target, 0xFF7A4A00, 0xFFFFF1D6, 0xFF8C4A00, 0xFFFFE2A8)
    _bind_tooltip_demo_hover(click_right_target, 0xFFFFFFFF, 0xFF409EFF, 0xFFFFFFFF, 0xFF66B1FF)

    top_tp, top_tn, _ = s("📝 Dark / Top / Hover\n鼠标移入时显示，移出时自动隐藏。")
    top_tooltip = DLL.CreateTooltip(page, top_tp, top_tn, POPUP_TOP, 0, 0)
    DLL.SetTooltipTheme(top_tooltip, TOOLTIP_THEME_DARK)
    DLL.SetTooltipPlacement(top_tooltip, POPUP_TOP)
    DLL.SetTooltipTrigger(top_tooltip, TOOLTIP_TRIGGER_HOVER)
    DLL.BindTooltipToControl(top_tooltip, hover_top_target)

    bottom_tp, bottom_tn, _ = s("💡 Light / Bottom / Hover\n浅色主题，适合表单和浅色卡片。")
    bottom_tooltip = DLL.CreateTooltip(page, bottom_tp, bottom_tn, POPUP_BOTTOM, 0, 0)
    DLL.SetTooltipTheme(bottom_tooltip, TOOLTIP_THEME_LIGHT)
    DLL.SetTooltipPlacement(bottom_tooltip, POPUP_BOTTOM)
    DLL.SetTooltipTrigger(bottom_tooltip, TOOLTIP_TRIGGER_HOVER)
    DLL.BindTooltipToControl(bottom_tooltip, hover_bottom_target)

    left_tp, left_tn, _ = s("🎨 Custom / Left / Hover\n支持自定义背景、文字颜色、边框、字体和字号。")
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

    note_cb = DLL._NotificationCB(on_notification_event)
    KEEP.append(note_cb)
    button(extra, "🔵", "信息通知", 930, 22, 120, 38, 0xFF409EFF, lambda: _show_note(page, "🔔 信息通知", "📝 这是一条 info 类型通知。", NOTIFY_INFO, note_cb))
    button(extra, "🟢", "成功通知", 1060, 22, 120, 38, 0xFF67C23A, lambda: _show_note(page, "✅ 操作成功", "🎉 这是一条 success 类型通知。", NOTIFY_SUCCESS, note_cb))
    button(extra, "🟠", "警告通知", 1190, 22, 120, 38, 0xFFE6A23C, lambda: _show_note(page, "⚠️ 注意", "📌 这是一条 warning 类型通知。", NOTIFY_WARNING, note_cb))
    button(extra, "🔴", "错误通知", 1320, 22, 120, 38, 0xFFF56C6C, lambda: _show_note(page, "❌ 失败", "🧯 这是一条 error 类型通知。", NOTIFY_ERROR, note_cb))

    label(page, "前四个目标用于 Tooltip 演示；右侧四个按钮继续演示 Notification 在软件窗口右上角弹出。", 36, 718, 980, 22, fg=0xFF606266)


def basic_page(page: HWND) -> tuple[HWND, int]:
    basic_group = groupbox(page, "📝 文本、按钮、编辑框", 16, 16, 718, 330)
    STATE["group_basic_text"] = basic_group
    label(page, "📝 Label / Button / EditBox / ColorEmojiEditBox / MessageBox / ConfirmBox", 36, 54, 640, 24, size=15, bold=True)
    label(page, "基础页保留原始输入与弹窗演示，并新增一整块 Button 样式扩展示例。", 36, 84, 620, 22, fg=0xFF606266)
    label(page, "📋 普通 Label 仍用于检查多行中文与 emoji 文本显示。", 36, 118, 360, 24)
    edit(page, "📑 普通 EditBox，可直接输入文本。", 36, 164, 300, 36, False)
    edit(page, "🌈 ColorEmojiEditBox 😉🎌 用于测试彩色 emoji 文本。", 356, 164, 340, 36, True)
    button(basic_group, "🖱️", "按钮点击测试", 10, 181, 170, 38, 0xFF409EFF, lambda: set_status("🖱️ Emoji 按钮点击成功。"))
    button(
        basic_group,
        "🔔",
        "显示消息框",
        196,
        181,
        170,
        38,
        0xFF67C23A,
        lambda: (show_msg("📝 MessageBox 测试", "📝 这是综合测试页触发的消息框。", "📝"), set_status("🔔 已打开 MessageBox。")),
    )
    button(
        basic_group,
        "❓",
        "显示确认框",
        382,
        181,
        170,
        38,
        0xFFE6A23C,
        lambda: (show_confirm("📣 ConfirmBox 测试", "🧪 请确认你已经看到基础组件区域。", "❓"), set_status("❓ 已打开 ConfirmBox。")),
    )

    select_group = groupbox(page, "🎛️ 勾选、单选、进度条", 752, 16, 718, 330)
    STATE["group_basic_select"] = select_group
    label(page, "🎛️ CheckBox / RadioButton / ProgressBar", 772, 54, 420, 24, size=15, bold=True)
    label(page, "点击复选框、单选框或下方控制按钮，观察状态回调。", 772, 84, 460, 22, fg=0xFF606266)
    c1p, c1n, _ = s("☑️ 启用高级模式")
    c2p, c2n, _ = s("🪔 显示调试输出")
    r1p, r1n, _ = s("🅰️ 方案 A")
    r2p, r2n, _ = s("🅱️ 方案 B")
    c1 = DLL.CreateCheckBox(page, 772, 126, 220, 32, c1p, c1n, BOOL(True), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    c2 = DLL.CreateCheckBox(page, 772, 162, 220, 32, c2p, c2n, BOOL(False), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    r1 = DLL.CreateRadioButton(page, 1016, 126, 220, 32, r1p, r1n, 1, BOOL(True), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    r2 = DLL.CreateRadioButton(page, 1016, 162, 220, 32, r2p, r2n, 1, BOOL(False), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    prog = DLL.CreateProgressBar(page, 772, 220, 420, 28, 35, THEME_PRIMARY, THEME_BORDER_LIGHT, BOOL(True), THEME_TEXT)
    DLL.SetProgressBarTextColor(prog, THEME_TEXT)
    bind_right_click_many(c1, c2, r1, r2, prog)
    DLL.SetProgressBarShowText(prog, BOOL(True))
    STATE["checkbox"] = c1
    STATE["progress"] = prog

    cb1 = DLL._CheckBoxCB(on_checkbox)
    rb1 = DLL._RadioCB(on_radio)
    pb1 = DLL._ProgressCB(on_progress)
    KEEP.extend([cb1, rb1, pb1])
    DLL.SetCheckBoxCallback(c1, cb1)
    DLL.SetCheckBoxCallback(c2, cb1)
    DLL.SetRadioButtonCallback(r1, rb1)
    DLL.SetRadioButtonCallback(r2, rb1)
    DLL.SetProgressBarCallback(prog, pb1)
    button(select_group, "🔾", "进度 -10", 450, 160, 118, 34, 0xFF909399, progress_minus)
    button(select_group, "📈", "进度 +10", 576, 160, 118, 34, 0xFF409EFF, progress_plus)
    button(select_group, "🔁", "重置进度", 450, 202, 118, 34, 0xFF67C23A, progress_reset)
    test_btn = button(select_group, "☑️", "切换勾选", 576, 202, 118, 34, 0xFFE6A23C, toggle_checkbox)

    style_group = groupbox(page, "🧩 Button 扩展示例", 16, 362, 1454, 244)
    STATE["group_basic_button_styles"] = style_group
    label(page, "🧩 新增按钮属性：Type / Style / Size / Round / Circle / Loading", 36, 400, 760, 24, size=15, bold=True)
    label(page, "这一组集中展示预设类型、朴素、文字、链接、圆角、圆形、加载态和尺寸。", 36, 430, 900, 22, fg=0xFF606266)

    row1_y = 68
    button(style_group, "", "Default", 12, row1_y, 124, 34, 0xFFFFFFFF, lambda: set_status("Button demo -> Default"), button_type=BUTTON_TYPE_DEFAULT)
    button(style_group, "", "Primary", 148, row1_y, 124, 34, 0xFF409EFF, lambda: set_status("Button demo -> Primary"), button_type=BUTTON_TYPE_PRIMARY)
    button(style_group, "", "Success", 284, row1_y, 124, 34, 0xFF67C23A, lambda: set_status("Button demo -> Success"), button_type=BUTTON_TYPE_SUCCESS)
    button(style_group, "", "Warning", 420, row1_y, 124, 34, 0xFFE6A23C, lambda: set_status("Button demo -> Warning"), button_type=BUTTON_TYPE_WARNING)
    button(style_group, "", "Danger", 556, row1_y, 124, 34, 0xFFF56C6C, lambda: set_status("Button demo -> Danger"), button_type=BUTTON_TYPE_DANGER)
    button(style_group, "", "Info", 692, row1_y, 124, 34, 0xFF909399, lambda: set_status("Button demo -> Info"), button_type=BUTTON_TYPE_INFO)

    row2_y = 108
    button(style_group, "✨", "Plain", 12, row2_y, 124, 34, 0xFF409EFF, lambda: set_status("Button demo -> Plain"), button_type=BUTTON_TYPE_PRIMARY, button_style=BUTTON_STYLE_PLAIN)
    button(style_group, "", "Text", 148, row2_y, 124, 34, 0xFF409EFF, lambda: set_status("Button demo -> Text"), button_type=BUTTON_TYPE_PRIMARY, button_style=BUTTON_STYLE_TEXT)
    button(style_group, "", "Link", 284, row2_y, 124, 34, 0xFF409EFF, lambda: set_status("Button demo -> Link"), button_type=BUTTON_TYPE_PRIMARY, button_style=BUTTON_STYLE_LINK)
    button(style_group, "🔵", "Round", 420, row2_y, 136, 34, 0xFF409EFF, lambda: set_status("Button demo -> Round"), button_type=BUTTON_TYPE_PRIMARY, round_button=True)
    button(style_group, "⭐", "", 572, row2_y, 40, 40, 0xFF67C23A, lambda: set_status("Button demo -> Circle"), button_type=BUTTON_TYPE_SUCCESS, circle_button=True)
    STATE["button_loading_demo"] = button(
        style_group,
        "",
        "Loading",
        628,
        row2_y,
        128,
        34,
        0xFF409EFF,
        lambda: None,
        button_type=BUTTON_TYPE_PRIMARY,
        loading=True,
    )
    STATE["button_loading_active"] = True
    button(style_group, "↻", "切换 Loading", 772, row2_y, 148, 34, 0xFF909399, toggle_demo_loading, button_type=BUTTON_TYPE_INFO, button_style=BUTTON_STYLE_PLAIN)

    row3_y = 154
    button(style_group, "", "Large", 12, row3_y, 136, 40, 0xFF409EFF, lambda: set_status("Button demo -> Large"), button_type=BUTTON_TYPE_PRIMARY, button_size=BUTTON_SIZE_LARGE)
    button(style_group, "", "Default", 164, row3_y, 124, 34, 0xFF409EFF, lambda: set_status("Button demo -> Default Size"), button_type=BUTTON_TYPE_PRIMARY)
    button(style_group, "", "Small", 304, row3_y, 112, 28, 0xFF409EFF, lambda: set_status("Button demo -> Small"), button_type=BUTTON_TYPE_PRIMARY, button_size=BUTTON_SIZE_SMALL)
    button(style_group, "🧪", "Auto Color", 432, row3_y, 138, 34, 0xFF8E44AD, lambda: set_status("Button demo -> Auto custom color"))
    button(style_group, "🫧", "Plain Auto", 586, row3_y, 138, 34, 0xFF8E44AD, lambda: set_status("Button demo -> Plain custom color"), button_style=BUTTON_STYLE_PLAIN)

    extra = groupbox(page, "🧱 其他 Element Plus 风格扩展", 16, 624, 1454, 140)
    STATE["group_basic_tips"] = extra
    label(page, "Checkbox / Radio 扩展样式，以及 Slider / Switch 演示", 36, 660, 620, 24, size=15, bold=True)

    cb_btn_p, cb_btn_n, _ = s("📝 Checkbox 按钮样式")
    cb_card_p, cb_card_n, _ = s("🧱 Checkbox 卡片样式")
    cb_btn = DLL.CreateCheckBox(page, 36, 696, 210, 36, cb_btn_p, cb_btn_n, BOOL(True), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    cb_card = DLL.CreateCheckBox(page, 256, 696, 210, 40, cb_card_p, cb_card_n, BOOL(False), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    DLL.SetCheckBoxStyle(cb_btn, 2)
    DLL.SetCheckBoxStyle(cb_card, 3)
    DLL.SetCheckBoxCheckColor(cb_btn, 0xFF409EFF)
    DLL.SetCheckBoxCheckColor(cb_card, 0xFF67C23A)

    rb_default_p, rb_default_n, _ = s("🎯 Radio 默认")
    rb_border_p, rb_border_n, _ = s("🧱 Radio 边框")
    rb_button_p, rb_button_n, _ = s("🔘 Radio 按钮")
    rb_default = DLL.CreateRadioButton(page, 500, 696, 130, 36, rb_default_p, rb_default_n, 77, BOOL(True), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    rb_border = DLL.CreateRadioButton(page, 640, 696, 150, 36, rb_border_p, rb_border_n, 77, BOOL(False), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    rb_button = DLL.CreateRadioButton(page, 800, 696, 140, 36, rb_button_p, rb_button_n, 77, BOOL(False), THEME_TEXT, THEME_BG, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False))
    DLL.SetRadioButtonStyle(rb_border, RADIO_STYLE_BORDER)
    DLL.SetRadioButtonStyle(rb_button, RADIO_STYLE_BUTTON)
    DLL.SetRadioButtonDotColor(rb_default, 0xFF409EFF)
    DLL.SetRadioButtonDotColor(rb_border, 0xFFE6A23C)
    DLL.SetRadioButtonDotColor(rb_button, 0xFF67C23A)

    slider = DLL.CreateSlider(page, 980, 682, 240, 56, 0, 100, 36, 10, 0xFF409EFF, 0xFFE4E7ED)
    DLL.SetSliderShowStops(slider, BOOL(True))
    switch_on_p, switch_on_n, _ = s("开")
    switch_off_p, switch_off_n, _ = s("关")
    sw = DLL.CreateSwitch(page, 1240, 696, 88, 34, BOOL(True), 0xFF13CE66, 0xFFDCDfe6, switch_on_p, switch_on_n, switch_off_p, switch_off_n)

    cb = DLL._CheckBoxCB(on_checkbox)
    rb = DLL._RadioCB(on_radio)
    sl = DLL._SliderCB(on_slider_changed)
    sc = DLL._SwitchCB(on_switch_changed)
    KEEP.extend([cb, rb, sl, sc])
    DLL.SetCheckBoxCallback(cb_btn, cb)
    DLL.SetCheckBoxCallback(cb_card, cb)
    DLL.SetRadioButtonCallback(rb_default, rb)
    DLL.SetRadioButtonCallback(rb_border, rb)
    DLL.SetRadioButtonCallback(rb_button, rb)
    DLL.SetSliderCallback(slider, sl)
    DLL.SetSwitchCallback(sw, sc)
    bind_right_click_many(cb_btn, cb_card, rb_default, rb_border, rb_button, slider, sw)

    return button_host(select_group), test_btn


def main() -> int:
    setup()
    build()
    DLL.set_message_loop_main_window(STATE["hwnd"])
    set_status("🚀 综合测试窗口已启动。")
    DLL.run_message_loop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
