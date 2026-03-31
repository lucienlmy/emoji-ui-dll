# -*- coding: utf-8 -*-
from __future__ import annotations

import base64
import ctypes
import struct
import sys
from ctypes import wintypes
from pathlib import Path

HWND = wintypes.HWND
BOOL = wintypes.BOOL
UINT32 = wintypes.UINT

ALIGN_LEFT = 0
ALIGN_CENTER = 1
GROUPBOX_STYLE_CARD = 1
TAB_HEADER_STYLE_CARD_PLAIN = 2
DTP_YMDHM = 3

TAB_BASIC = 0
TAB_SELECT = 1
TAB_DATA = 2
TAB_TABS = 3

MENU_MSG = 1101
MENU_CONFIRM = 1102
MENU_TAB_BASIC = 1201
MENU_TAB_SELECT = 1202
MENU_TAB_DATA = 1203
MENU_TAB_TABS = 1204

POP_WINDOW_STATUS = 2101
POP_WINDOW_MSG = 2102
POP_GRID_ADD = 2201
POP_GRID_STATUS = 2202
POP_BUTTON_STATUS = 2301
POP_CHECKBOX_TOGGLE = 2401

PNG_BYTES = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADUlEQVQImWP4z8DwHwAFAAH/e+m+7wAAAABJRU5ErkJggg=="
)

STATE: dict[str, object] = {
    "hwnd": None,
    "status": None,
    "main_tab": None,
    "nested_tab": None,
    "checkbox": None,
    "progress": None,
    "grid": None,
    "row_count": 0,
    "grid_dark": True,
    "confirm_cb": None,
}
BUTTON_ACTIONS: dict[int, object] = {}
KEEP: list[object] = []

FONT_RAW = "Microsoft YaHei UI".encode("utf-8")
FONT_BUF = (ctypes.c_ubyte * len(FONT_RAW))(*FONT_RAW)
FONT_PTR = ctypes.cast(FONT_BUF, ctypes.c_void_p)
FONT_LEN = len(FONT_RAW)


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def dll_path() -> Path:
    p = repo_root() / "bin" / "x64" / "Release" / "emoji_window.dll"
    return p if p.is_file() else Path(__file__).resolve().parent / "emoji_window.dll"


def argb(a: int, r: int, g: int, b: int) -> int:
    return ((a & 255) << 24) | ((r & 255) << 16) | ((g & 255) << 8) | (b & 255)


def s(text: str) -> tuple[ctypes.c_void_p, int, object]:
    raw = text.encode("utf-8")
    if not raw:
        return ctypes.c_void_p(), 0, ctypes.c_void_p()
    buf = (ctypes.c_ubyte * len(raw))(*raw)
    return ctypes.cast(buf, ctypes.c_void_p), len(raw), buf


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


def setup() -> None:
    button_cb = ctypes.WINFUNCTYPE(None, ctypes.c_int, HWND)
    confirm_cb = ctypes.WINFUNCTYPE(None, ctypes.c_int)
    menu_cb = ctypes.WINFUNCTYPE(None, ctypes.c_int, ctypes.c_int)
    tab_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int)
    checkbox_cb = ctypes.WINFUNCTYPE(None, HWND, BOOL)
    radio_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int, BOOL)
    listbox_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int)
    combo_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int)
    hotkey_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int, ctypes.c_int)
    value_cb = ctypes.WINFUNCTYPE(None, HWND)
    picture_cb = ctypes.WINFUNCTYPE(None, HWND)
    progress_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int)
    dg_cb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int, ctypes.c_int)

    DLL.create_window_bytes.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.create_window_bytes.restype = HWND
    DLL.set_message_loop_main_window.argtypes = [HWND]
    DLL.run_message_loop.argtypes = []

    DLL.create_emoji_button_bytes.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, UINT32]
    DLL.create_emoji_button_bytes.restype = ctypes.c_int
    DLL.set_button_click_callback.argtypes = [button_cb]

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

    DLL.CreateRadioButton.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, BOOL, UINT32, UINT32, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, BOOL, BOOL, BOOL]
    DLL.CreateRadioButton.restype = HWND
    DLL.SetRadioButtonCallback.argtypes = [HWND, radio_cb]

    DLL.CreateProgressBar.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, UINT32, UINT32, BOOL, UINT32]
    DLL.CreateProgressBar.restype = HWND
    DLL.SetProgressValue.argtypes = [HWND, ctypes.c_int]
    DLL.GetProgressValue.argtypes = [HWND]
    DLL.GetProgressValue.restype = ctypes.c_int
    DLL.SetProgressBarCallback.argtypes = [HWND, progress_cb]
    DLL.SetProgressBarShowText.argtypes = [HWND, BOOL]

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

    DLL.CreateHotKeyControl.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, UINT32, UINT32]
    DLL.CreateHotKeyControl.restype = HWND
    DLL.SetHotKey.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
    DLL.SetHotKeyCallback.argtypes = [HWND, hotkey_cb]

    DLL.CreateGroupBox.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, UINT32, UINT32, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, BOOL, BOOL, BOOL]
    DLL.CreateGroupBox.restype = HWND
    DLL.SetGroupBoxStyle.argtypes = [HWND, ctypes.c_int]
    DLL.SetGroupBoxTitleColor.argtypes = [HWND, UINT32]

    DLL.CreateTabControl.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.CreateTabControl.restype = HWND
    DLL.AddTabItem.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, HWND]
    DLL.AddTabItem.restype = ctypes.c_int
    DLL.GetTabContentWindow.argtypes = [HWND, ctypes.c_int]
    DLL.GetTabContentWindow.restype = HWND
    DLL.SetTabCallback.argtypes = [HWND, tab_cb]
    DLL.SelectTab.argtypes = [HWND, ctypes.c_int]
    DLL.SetTabHeaderStyle.argtypes = [HWND, ctypes.c_int]
    DLL.SetTabItemSize.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
    DLL.SetTabPadding.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
    DLL.SetTabColors.argtypes = [HWND, UINT32, UINT32, UINT32, UINT32]
    DLL.SetTabIndicatorColor.argtypes = [HWND, UINT32]

    DLL.CreateMenuBar.argtypes = [HWND]
    DLL.CreateMenuBar.restype = HWND
    DLL.MenuBarAddItem.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    DLL.MenuBarAddSubItem.argtypes = [HWND, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    DLL.SetMenuBarPlacement.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
    DLL.SetMenuBarCallback.argtypes = [HWND, menu_cb]

    DLL.CreateEmojiPopupMenu.argtypes = [HWND]
    DLL.CreateEmojiPopupMenu.restype = HWND
    DLL.PopupMenuAddItem.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    DLL.SetPopupMenuCallback.argtypes = [HWND, menu_cb]
    DLL.BindControlMenu.argtypes = [HWND, HWND]
    DLL.BindButtonMenu.argtypes = [HWND, ctypes.c_int, HWND]

    DLL.CreateDataGridView.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, BOOL, BOOL, UINT32, UINT32]
    DLL.CreateDataGridView.restype = HWND
    DLL.DataGrid_AddTextColumn.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_AddCheckBoxColumn.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_AddComboBoxColumn.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_AddTagColumn.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_AddRow.argtypes = [HWND]
    DLL.DataGrid_AddRow.restype = ctypes.c_int
    DLL.DataGrid_SetCellText.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.DataGrid_SetCellChecked.argtypes = [HWND, ctypes.c_int, ctypes.c_int, BOOL]
    DLL.DataGrid_SetCellStyle.argtypes = [HWND, ctypes.c_int, ctypes.c_int, UINT32, UINT32, BOOL, BOOL]
    DLL.DataGrid_SetColumnComboItems.argtypes = [HWND, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
    DLL.DataGrid_SetColumnHeaderAlignment.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_SetColumnCellAlignment.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
    DLL.DataGrid_SetSelectionMode.argtypes = [HWND, ctypes.c_int]
    DLL.DataGrid_SetShowGridLines.argtypes = [HWND, BOOL]
    DLL.DataGrid_SetDefaultRowHeight.argtypes = [HWND, ctypes.c_int]
    DLL.DataGrid_SetHeaderHeight.argtypes = [HWND, ctypes.c_int]
    DLL.DataGrid_SetHeaderStyle.argtypes = [HWND, ctypes.c_int]
    DLL.DataGrid_SetCellClickCallback.argtypes = [HWND, dg_cb]
    DLL.DataGrid_SetCellDoubleClickCallback.argtypes = [HWND, dg_cb]
    DLL.DataGrid_SetCellValueChangedCallback.argtypes = [HWND, dg_cb]

    DLL._ButtonCB = button_cb
    DLL._ConfirmCB = confirm_cb
    DLL._MenuCB = menu_cb
    DLL._TabCB = tab_cb
    DLL._CheckBoxCB = checkbox_cb
    DLL._RadioCB = radio_cb
    DLL._ListBoxCB = listbox_cb
    DLL._ComboCB = combo_cb
    DLL._HotKeyCB = hotkey_cb
    DLL._ValueCB = value_cb
    DLL._PictureCB = picture_cb
    DLL._ProgressCB = progress_cb
    DLL._GridCB = dg_cb


def set_status(text: str) -> None:
    print(text)
    h = STATE["status"]
    if h:
        p, n, _ = s(text)
        DLL.SetLabelText(h, p, n)


def label(parent: HWND, text: str, x: int, y: int, w: int, h: int, fg=0xFF303133, bg=0xFFFFFFFF, size=13, bold=False, wrap=False) -> HWND:
    p, n, _ = s(text)
    return DLL.CreateLabel(parent, x, y, w, h, p, n, fg, bg, FONT_PTR, FONT_LEN, size, BOOL(bold), BOOL(False), BOOL(False), ALIGN_LEFT, BOOL(wrap))


def button(parent: HWND, emoji: str, text: str, x: int, y: int, w: int, h: int, bg: int, action) -> int:
    ep, en, _ = s(emoji)
    tp, tn, _ = s(text)
    bid = DLL.create_emoji_button_bytes(parent, ep, en, tp, tn, x, y, w, h, bg)
    BUTTON_ACTIONS[bid] = action
    return bid


def groupbox(parent: HWND, text: str, x: int, y: int, w: int, h: int) -> HWND:
    p, n, _ = s(text)
    g = DLL.CreateGroupBox(parent, x, y, w, h, p, n, 0xFFEBEEF5, 0xFFFFFFFF, FONT_PTR, FONT_LEN, 14, BOOL(True), BOOL(False), BOOL(False))
    DLL.SetGroupBoxStyle(g, GROUPBOX_STYLE_CARD)
    DLL.SetGroupBoxTitleColor(g, 0xFF303133)
    return g


def edit(parent: HWND, text: str, x: int, y: int, w: int, h: int, color_emoji=False) -> HWND:
    p, n, _ = s(text)
    fn = DLL.CreateColorEmojiEditBox if color_emoji else DLL.CreateEditBox
    return fn(parent, x, y, w, h, p, n, 0xFF303133, 0xFFFFFFFF, FONT_PTR, FONT_LEN, 13, BOOL(False), BOOL(False), BOOL(False), ALIGN_LEFT, BOOL(False), BOOL(False), BOOL(False), BOOL(True), BOOL(True))


def add_tab(tab: HWND, title: str) -> HWND:
    p, n, _ = s(title)
    idx = DLL.AddTabItem(tab, p, n, HWND())
    return DLL.GetTabContentWindow(tab, idx)


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

