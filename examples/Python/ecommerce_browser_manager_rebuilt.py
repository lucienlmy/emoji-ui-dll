# -*- coding: utf-8 -*-
from __future__ import annotations

import ctypes
import csv
import hashlib
import json
import os
import platform
import socket
import struct
import subprocess
import time
import urllib.request
from ctypes import wintypes
from dataclasses import dataclass
from pathlib import Path

HWND = wintypes.HWND
UINT32 = wintypes.UINT
BOOL = wintypes.BOOL
VK_RETURN = 13
CALLBACK_NODE_SELECTED = 1

SW_SHOW = 5
SW_HIDE = 0
WM_SETREDRAW = 0x000B
RDW_INVALIDATE = 0x0001
RDW_ERASE = 0x0004
RDW_ALLCHILDREN = 0x0080
RDW_FRAME = 0x0400
RDW_UPDATENOW = 0x0100

USER32 = ctypes.windll.user32

TITLE_BAR_HEIGHT = 32
WINDOW_WIDTH = 1440
WINDOW_HEIGHT = 900

OUTER = 16
GAP = 12
RAIL_W = 152
DRAWER_W = 360
CARDS_H = 96
SWITCH_H = 44
TOOLBAR_H = 42
CONTEXT_H = 36
BOTTOM_H = 26
STAT_CARD_H = 84


def argb(a: int, r: int, g: int, b: int) -> int:
    return ((a & 255) << 24) | ((r & 255) << 16) | ((g & 255) << 8) | (b & 255)


def clamp(value: int, low: int, high: int) -> int:
    return max(low, min(high, value))


def shift_color(color: int, delta: int) -> int:
    a = (color >> 24) & 255
    r = clamp(((color >> 16) & 255) + delta, 0, 255)
    g = clamp(((color >> 8) & 255) + delta, 0, 255)
    b = clamp((color & 255) + delta, 0, 255)
    return argb(a, r, g, b)


def mix_color(base: int, target: int, ratio: float) -> int:
    ratio = max(0.0, min(1.0, ratio))
    a = (base >> 24) & 255
    br, bg, bb = (base >> 16) & 255, (base >> 8) & 255, base & 255
    tr, tg, tb = (target >> 16) & 255, (target >> 8) & 255, target & 255
    r = int(br * (1.0 - ratio) + tr * ratio)
    g = int(bg * (1.0 - ratio) + tg * ratio)
    b = int(bb * (1.0 - ratio) + tb * ratio)
    return argb(a, r, g, b)


def color_brightness(color: int) -> int:
    r = (color >> 16) & 255
    g = (color >> 8) & 255
    b = color & 255
    return int(r * 0.299 + g * 0.587 + b * 0.114)


def utf8_buffer(text: str) -> tuple[ctypes.c_void_p, int, object | None]:
    raw = text.encode("utf-8")
    if not raw:
        return ctypes.c_void_p(), 0, None
    buf = (ctypes.c_ubyte * len(raw))(*raw)
    return ctypes.cast(buf, ctypes.c_void_p), len(raw), buf


def bytes_buffer(data: bytes) -> tuple[ctypes.c_void_p, int, object | None]:
    if not data:
        return ctypes.c_void_p(), 0, None
    buf = (ctypes.c_ubyte * len(data)).from_buffer_copy(data)
    return ctypes.cast(buf, ctypes.c_void_p), len(data), buf


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def dll_path() -> Path:
    primary = repo_root() / "bin" / "x64" / "Release" / "emoji_window.dll"
    fallback = Path(__file__).resolve().parent / "emoji_window.dll"
    return primary if primary.is_file() else fallback


def icon_path() -> Path:
    path = repo_root() / "examples" / "Csharp" / "EmojiWindowEcommerceMultiAccountDemo" / "favicon.ico"
    if path.is_file():
        return path
    return Path(__file__).resolve().parent / "谷歌.ico"


FONT_YAHEI_RAW = "Microsoft YaHei UI".encode("utf-8")
FONT_YAHEI_BUF = (ctypes.c_ubyte * len(FONT_YAHEI_RAW))(*FONT_YAHEI_RAW)
FONT_YAHEI_PTR = ctypes.cast(FONT_YAHEI_BUF, ctypes.c_void_p)
FONT_YAHEI_LEN = len(FONT_YAHEI_RAW)

FONT_SEGOE_RAW = "Segoe UI".encode("utf-8")
FONT_SEGOE_BUF = (ctypes.c_ubyte * len(FONT_SEGOE_RAW))(*FONT_SEGOE_RAW)
FONT_SEGOE_PTR = ctypes.cast(FONT_SEGOE_BUF, ctypes.c_void_p)
FONT_SEGOE_LEN = len(FONT_SEGOE_RAW)


@dataclass
class MetricCard:
    panel: HWND
    accent: HWND
    divider: HWND
    footer: HWND
    value: HWND
    title: HWND
    hint: HWND
    badge: HWND
    accent_color: int


@dataclass
class StatCard:
    panel: HWND
    value: HWND
    caption: HWND


@dataclass
class AccountMiniCard:
    panel: HWND
    title: HWND
    meta: HWND
    status: HWND


@dataclass
class AccountRecord:
    id: int
    checked: bool
    account: str
    channel: str
    store: str
    note: str
    status: str
    url: str


class NativeApi:
    def __init__(self) -> None:
        if struct.calcsize("P") * 8 != 64:
            raise OSError("Please use 64-bit Python.")
        path = dll_path()
        if not path.is_file():
            raise FileNotFoundError(path)
        self.dll = ctypes.WinDLL(str(path))
        self._setup()

    def _setup(self) -> None:
        dll = self.dll
        self.ButtonClickCallback = ctypes.WINFUNCTYPE(None, ctypes.c_int, HWND)
        self.WindowResizeCallback = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int, ctypes.c_int)
        self.EditKeyCallback = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int)
        self.GridCellCallback = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int, ctypes.c_int)
        self.TreeViewCallback = ctypes.WINFUNCTYPE(None, ctypes.c_int, ctypes.c_void_p)

        dll.create_window_bytes_ex.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, UINT32, UINT32]
        dll.create_window_bytes_ex.restype = HWND
        dll.set_message_loop_main_window.argtypes = [HWND]
        dll.run_message_loop.argtypes = []
        dll.set_window_icon_bytes.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
        dll.set_window_title.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
        dll.set_window_titlebar_color.argtypes = [HWND, UINT32]
        dll.SetTitleBarTextColor.argtypes = [HWND, UINT32]
        dll.SetWindowBackgroundColor.argtypes = [HWND, UINT32]
        dll.ShowEmojiWindow.argtypes = [HWND, ctypes.c_int]
        dll.SetWindowResizeCallback.argtypes = [self.WindowResizeCallback]

        dll.create_emoji_button_bytes.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, UINT32]
        dll.create_emoji_button_bytes.restype = ctypes.c_int
        dll.set_button_click_callback.argtypes = [self.ButtonClickCallback]
        dll.SetButtonText.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
        dll.SetButtonEmoji.argtypes = [ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
        dll.SetButtonBounds.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        dll.SetButtonStyle.argtypes = [ctypes.c_int, ctypes.c_int]
        dll.SetButtonSize.argtypes = [ctypes.c_int, ctypes.c_int]
        dll.SetButtonRound.argtypes = [ctypes.c_int, ctypes.c_int]
        dll.SetButtonBackgroundColor.argtypes = [ctypes.c_int, UINT32]
        dll.SetButtonBorderColor.argtypes = [ctypes.c_int, UINT32]
        dll.SetButtonTextColor.argtypes = [ctypes.c_int, UINT32]
        dll.SetButtonHoverColors.argtypes = [ctypes.c_int, UINT32, UINT32, UINT32]
        dll.ShowButton.argtypes = [ctypes.c_int, ctypes.c_int]

        dll.CreateLabel.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, UINT32, UINT32, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        dll.CreateLabel.restype = HWND
        dll.SetLabelText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
        dll.SetLabelColor.argtypes = [HWND, UINT32, UINT32]
        dll.SetLabelBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]

        dll.CreateEditBox.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, UINT32, UINT32, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        dll.CreateEditBox.restype = HWND
        dll.GetEditBoxText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
        dll.GetEditBoxText.restype = ctypes.c_int
        dll.SetEditBoxText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
        dll.SetEditBoxKeyCallback.argtypes = [HWND, self.EditKeyCallback]
        dll.SetEditBoxColor.argtypes = [HWND, UINT32, UINT32]
        dll.SetEditBoxBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]

        dll.CreatePanel.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, UINT32]
        dll.CreatePanel.restype = HWND
        dll.SetPanelBackgroundColor.argtypes = [HWND, UINT32]

        dll.CreateTreeView.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, UINT32, UINT32, ctypes.c_void_p]
        dll.CreateTreeView.restype = HWND
        dll.AddRootNode.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
        dll.AddRootNode.restype = ctypes.c_int
        dll.AddChildNode.argtypes = [HWND, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
        dll.AddChildNode.restype = ctypes.c_int
        dll.ExpandAll.argtypes = [HWND]
        dll.ExpandAll.restype = BOOL
        dll.SetSelectedNode.argtypes = [HWND, ctypes.c_int]
        dll.SetSelectedNode.restype = BOOL
        dll.SetTreeViewSidebarMode.argtypes = [HWND, BOOL]
        dll.SetTreeViewSidebarMode.restype = BOOL
        dll.SetTreeViewRowHeight.argtypes = [HWND, ctypes.c_float]
        dll.SetTreeViewRowHeight.restype = BOOL
        dll.SetTreeViewItemSpacing.argtypes = [HWND, ctypes.c_float]
        dll.SetTreeViewItemSpacing.restype = BOOL
        dll.SetTreeViewTextColor.argtypes = [HWND, UINT32]
        dll.SetTreeViewTextColor.restype = BOOL
        dll.SetTreeViewBackgroundColor.argtypes = [HWND, UINT32]
        dll.SetTreeViewBackgroundColor.restype = BOOL
        dll.SetTreeViewSelectedBgColor.argtypes = [HWND, UINT32]
        dll.SetTreeViewSelectedBgColor.restype = BOOL
        dll.SetTreeViewSelectedForeColor.argtypes = [HWND, UINT32]
        dll.SetTreeViewSelectedForeColor.restype = BOOL
        dll.SetTreeViewHoverBgColor.argtypes = [HWND, UINT32]
        dll.SetTreeViewHoverBgColor.restype = BOOL
        dll.SetTreeViewFont.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_float, ctypes.c_int, BOOL]
        dll.SetTreeViewFont.restype = BOOL
        dll.SetTreeViewCallback.argtypes = [HWND, ctypes.c_int, self.TreeViewCallback]
        dll.SetTreeViewCallback.restype = BOOL

        dll.CreateComboBox.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, UINT32, UINT32, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        dll.CreateComboBox.restype = HWND
        dll.AddComboItem.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
        dll.ClearComboBox.argtypes = [HWND]
        dll.GetComboItemCount.argtypes = [HWND]
        dll.GetComboItemCount.restype = ctypes.c_int
        dll.GetComboSelectedIndex.argtypes = [HWND]
        dll.GetComboSelectedIndex.restype = ctypes.c_int
        dll.SetComboSelectedIndex.argtypes = [HWND, ctypes.c_int]
        dll.GetComboItemText.argtypes = [HWND, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
        dll.GetComboItemText.restype = ctypes.c_int
        dll.SetComboBoxText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
        dll.SetComboBoxBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        dll.SetComboBoxColors.argtypes = [HWND, UINT32, UINT32, UINT32, UINT32]

        dll.CreateDataGridView.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, UINT32, UINT32]
        dll.CreateDataGridView.restype = HWND
        dll.DataGrid_AddCheckBoxColumn.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
        dll.DataGrid_AddTextColumn.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_int]
        dll.DataGrid_AddRow.argtypes = [HWND]
        dll.DataGrid_AddRow.restype = ctypes.c_int
        dll.DataGrid_ClearRows.argtypes = [HWND]
        dll.DataGrid_SetBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        dll.DataGrid_SetCellText.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
        dll.DataGrid_SetCellChecked.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int]
        dll.DataGrid_GetCellChecked.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
        dll.DataGrid_GetCellChecked.restype = ctypes.c_int
        dll.DataGrid_SetHeaderHeight.argtypes = [HWND, ctypes.c_int]
        dll.DataGrid_SetDefaultRowHeight.argtypes = [HWND, ctypes.c_int]
        dll.DataGrid_SetColors.argtypes = [HWND, UINT32, UINT32, UINT32, UINT32, UINT32, UINT32, UINT32]
        dll.DataGrid_SetFreezeHeader.argtypes = [HWND, ctypes.c_int]
        dll.DataGrid_SetShowGridLines.argtypes = [HWND, ctypes.c_int]
        dll.DataGrid_SetSelectionMode.argtypes = [HWND, ctypes.c_int]
        dll.DataGrid_SetColumnHeaderAlignment.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
        dll.DataGrid_SetColumnCellAlignment.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
        dll.DataGrid_SetColumnWidth.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
        dll.DataGrid_SetSelectedCell.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
        dll.DataGrid_SetCellClickCallback.argtypes = [HWND, self.GridCellCallback]
        dll.DataGrid_SetCellValueChangedCallback.argtypes = [HWND, self.GridCellCallback]
        dll.DataGrid_SetSelectionChangedCallback.argtypes = [HWND, self.GridCellCallback]
        dll.DataGrid_Refresh.argtypes = [HWND]
        dll.DataGrid_ExportCSV.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
        dll.DataGrid_ExportCSV.restype = ctypes.c_int


class RedrawScope:
    def __init__(self, hwnd: HWND) -> None:
        self.handle = int(ctypes.cast(hwnd, ctypes.c_void_p).value or 0)
        USER32.SendMessageW(self.handle, WM_SETREDRAW, 0, 0)

    def __enter__(self) -> "RedrawScope":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        USER32.SendMessageW(self.handle, WM_SETREDRAW, 1, 0)
        USER32.RedrawWindow(self.handle, None, None, RDW_INVALIDATE | RDW_ERASE | RDW_FRAME | RDW_ALLCHILDREN | RDW_UPDATENOW)


class BrowserManagerApp:
    KPI_TITLES = ["今日在线", "运行中", "异常账号", "待处理", "店铺数", "代理正常率"]
    KPI_HINTS = ["实时在线账号", "已启动浏览器", "建议优先处理", "等待处理任务", "已绑定店铺", "代理健康度"]
    KPI_BADGES = ["OPS", "LIVE", "RISK", "TODO", "SHOP", "NET"]
    PAGE_THEMES = {
        "browser": {"emoji": "🌐", "title": "浏览器容器", "accent": argb(255, 56, 107, 235), "titlebar": argb(255, 43, 83, 154)},
        "account": {"emoji": "👥", "title": "账号总览", "accent": argb(255, 15, 163, 177), "titlebar": argb(255, 17, 116, 124)},
        "proxy": {"emoji": "🌍", "title": "代理 / IP", "accent": argb(255, 14, 165, 233), "titlebar": argb(255, 17, 94, 129)},
        "fingerprint": {"emoji": "🧬", "title": "环境指纹", "accent": argb(255, 217, 119, 6), "titlebar": argb(255, 146, 64, 14)},
        "risk": {"emoji": "🛡️", "title": "风险中心", "accent": argb(255, 239, 68, 68), "titlebar": argb(255, 153, 27, 27)},
        "logs": {"emoji": "📝", "title": "操作日志", "accent": argb(255, 99, 102, 241), "titlebar": argb(255, 67, 56, 202)},
    }
    KPI_COLORS = [
        argb(255, 59, 130, 246),
        argb(255, 34, 197, 94),
        argb(255, 239, 68, 68),
        argb(255, 245, 158, 11),
        argb(255, 6, 182, 212),
        argb(255, 59, 130, 246),
    ]

    def __init__(self) -> None:
        self.native = NativeApi()
        self.dll = self.native.dll
        self.width = WINDOW_WIDTH
        self.height = WINDOW_HEIGHT
        self.dark_mode = False
        self.drawer_open = False
        self.current_view = "browser"
        self.browser_running = False
        self.selected_account_id: int | None = None
        self.next_account_id = 100
        self.visible_ids: list[int] = []
        self.operation_logs: list[str] = []
        self.runtime_snapshot: dict[str, str] = {}
        self.runtime_geo: dict[str, str] = {}
        self.last_runtime_refresh = 0.0

        self.accounts: list[AccountRecord] = []
        self.cards: list[MetricCard] = []
        self.recent_account_buttons: list[int] = []
        self.nav_buttons: dict[str, int] = {}
        self.nav_tree_nodes: dict[int, tuple[str, bool]] = {}
        self.nav_view_to_node: dict[str, int] = {}
        self.page_panels: dict[str, HWND] = {}
        self.page_controls: dict[str, dict[str, object]] = {}
        self.button_actions: dict[int, callable] = {}

        self.window: HWND | None = None
        self.nav_panel: HWND | None = None
        self.nav_tree: HWND | None = None
        self.drawer_panel: HWND | None = None
        self.content_panel: HWND | None = None
        self.switch_panel: HWND | None = None
        self.toolbar_panel: HWND | None = None
        self.context_panel: HWND | None = None
        self.workspace_panel: HWND | None = None
        self.status_panel: HWND | None = None
        self.page_host: HWND | None = None

        self.lbl_nav_title: HWND | None = None
        self.lbl_nav_hint: HWND | None = None
        self.lbl_sidebar_title: HWND | None = None
        self.lbl_drawer_detail_title: HWND | None = None
        self.lbl_switch_title: HWND | None = None
        self.lbl_workspace_title: HWND | None = None
        self.lbl_workspace_subtitle: HWND | None = None
        self.lbl_context: HWND | None = None
        self.lbl_status: HWND | None = None
        self.drawer_detail_labels: list[HWND] = []

        self.txt_switch_search: HWND | None = None
        self.txt_url: HWND | None = None
        self.txt_drawer_search: HWND | None = None
        self.cmb_drawer_status: HWND | None = None
        self.grid: HWND | None = None

        self.btn_more_accounts = 0
        self.btn_theme = 0
        self.btn_launch = 0
        self.btn_stop = 0
        self.btn_refresh_page = 0
        self.btn_relogin = 0
        self.btn_open_product = 0
        self.btn_clear_cache = 0
        self.btn_drawer_add = 0
        self.btn_drawer_import = 0
        self.btn_drawer_export = 0
        self.btn_drawer_refresh = 0
        self.btn_drawer_select_all = 0
        self.btn_drawer_batch_start = 0
        self.btn_drawer_batch_stop = 0
        self.btn_drawer_batch_delete = 0
        self._suppress_nav_callback = False

        self._button_click_cb = self.native.ButtonClickCallback(self.on_button_click)
        self._tree_selected_cb = self.native.TreeViewCallback(self.on_nav_tree_selected)
        self._window_resize_cb = self.native.WindowResizeCallback(self.on_window_resize)
        self._edit_key_cb = self.native.EditKeyCallback(self.on_edit_key)
        self._grid_cell_click_cb = self.native.GridCellCallback(self.on_grid_cell_click)
        self._grid_value_changed_cb = self.native.GridCellCallback(self.on_grid_value_changed)
        self._grid_selection_changed_cb = self.native.GridCellCallback(self.on_grid_selection_changed)

    def run(self) -> None:
        self.seed_accounts()
        self.refresh_runtime_data(False)
        self.create_window()
        with RedrawScope(self.window):
            self.create_controls()
            self.apply_theme()
            self.apply_filters("已加载账号数据。")
            self.layout()
        self.dll.SetEditBoxKeyCallback(self.txt_url, self._edit_key_cb)
        self.dll.SetEditBoxKeyCallback(self.txt_switch_search, self._edit_key_cb)
        self.dll.SetEditBoxKeyCallback(self.txt_drawer_search, self._edit_key_cb)
        self.dll.set_button_click_callback(self._button_click_cb)
        self.dll.SetWindowResizeCallback(self._window_resize_cb)
        self.dll.ShowEmojiWindow(self.window, 1)
        self.dll.set_message_loop_main_window(self.window)
        self.dll.run_message_loop()

    def create_window(self) -> None:
        title_ptr, title_len, title_keep = utf8_buffer("电商多账号浏览器管理器")
        self._title_keep = title_keep
        self.window = self.dll.create_window_bytes_ex(title_ptr, title_len, -1, -1, self.width, self.height, argb(255, 38, 70, 124), argb(255, 241, 245, 250))
        if not self.window:
            raise RuntimeError("create_window_bytes_ex failed")
        self.dll.SetTitleBarTextColor(self.window, argb(255, 255, 255, 255))
        icon = icon_path()
        if icon.is_file():
            icon_ptr, icon_len, icon_keep = bytes_buffer(icon.read_bytes())
            self._icon_keep = icon_keep
            self.dll.set_window_icon_bytes(self.window, icon_ptr, icon_len)

    def create_controls(self) -> None:
        self.create_kpis()
        self.nav_panel = self.dll.CreatePanel(self.window, 0, 0, 100, 100, argb(255, 255, 255, 255))
        self.drawer_panel = self.dll.CreatePanel(self.window, 0, 0, 100, 100, argb(255, 255, 255, 255))
        self.content_panel = self.dll.CreatePanel(self.window, 0, 0, 100, 100, argb(255, 255, 255, 255))
        self.switch_panel = self.dll.CreatePanel(self.content_panel, 0, 0, 100, 100, argb(255, 248, 250, 252))
        self.toolbar_panel = self.dll.CreatePanel(self.content_panel, 0, 0, 100, 100, argb(255, 255, 255, 255))
        self.context_panel = self.dll.CreatePanel(self.content_panel, 0, 0, 100, 100, argb(255, 248, 250, 252))
        self.workspace_panel = self.dll.CreatePanel(self.content_panel, 0, 0, 100, 100, argb(255, 255, 255, 255))
        self.page_host = self.dll.CreatePanel(self.workspace_panel, 0, 0, 100, 100, argb(255, 222, 228, 238))
        self.status_panel = self.dll.CreatePanel(self.content_panel, 0, 0, 100, 100, argb(255, 248, 250, 252))

        self.lbl_nav_title = self.label(self.nav_panel, "功能菜单", 12, True)
        self.lbl_nav_hint = self.label(self.nav_panel, "点击父级可展开 / 收起", 10, False)
        self.lbl_switch_title = self.label(self.switch_panel, "账号切换", 11, True)
        self.lbl_workspace_title = self.label(self.workspace_panel, "工作区", 20, True)
        self.lbl_workspace_subtitle = self.label(self.workspace_panel, "当前页面：浏览器容器", 12, False)
        self.lbl_context = self.label(self.context_panel, "当前账号：- | 店铺：- | 代理：- | 指纹：- | 风险：-", 11, False)
        self.lbl_status = self.label(self.status_panel, "", 11, False)

        self.create_nav_buttons()
        self.create_switch_strip()
        self.create_toolbar()
        self.create_drawer()
        self.create_pages()

    def create_kpis(self) -> None:
        for index in range(6):
            panel = self.dll.CreatePanel(self.window, 0, 0, 100, CARDS_H, argb(255, 255, 255, 255))
            accent = self.dll.CreatePanel(panel, 0, 0, 100, 6, self.KPI_COLORS[index])
            divider = self.dll.CreatePanel(panel, 0, 0, 100, 1, argb(255, 226, 232, 240))
            footer = self.dll.CreatePanel(panel, 0, 0, 100, 28, argb(255, 248, 250, 252))
            value = self.label(panel, "0", 24, True, self.KPI_COLORS[index], argb(255, 255, 255, 255))
            title = self.label(panel, self.KPI_TITLES[index], 11, False)
            hint = self.label(panel, self.KPI_HINTS[index], 10, False)
            badge = self.label(panel, self.KPI_BADGES[index], 9, True, argb(255, 255, 255, 255), self.KPI_COLORS[index])
            self.cards.append(MetricCard(panel, accent, divider, footer, value, title, hint, badge, self.KPI_COLORS[index]))

    def create_nav_buttons(self) -> None:
        tree_bg = argb(255, 255, 255, 255)
        tree_text = argb(255, 51, 65, 85)
        self.nav_tree = self.dll.CreateTreeView(self.nav_panel, 0, 0, 100, 100, tree_bg, tree_text, ctypes.c_void_p())
        self.dll.SetTreeViewSidebarMode(self.nav_tree, 1)
        self.dll.SetTreeViewRowHeight(self.nav_tree, ctypes.c_float(34.0))
        self.dll.SetTreeViewItemSpacing(self.nav_tree, ctypes.c_float(4.0))
        self.dll.SetTreeViewFont(self.nav_tree, FONT_YAHEI_PTR, FONT_YAHEI_LEN, ctypes.c_float(12.0), 400, 0)
        workbench_root = self.add_tree_root("工作台 · 3", "📊")
        env_root = self.add_tree_root("环境与安全 · 3", "🧩")
        self.add_tree_child(workbench_root, "浏览器容器", "🌐", "browser", False)
        self.add_tree_child(workbench_root, "账号列表", "👥", "account", True)
        self.add_tree_child(workbench_root, "操作日志", "📝", "logs", False)
        self.add_tree_child(env_root, "代理网络", "🌍", "proxy", False)
        self.add_tree_child(env_root, "环境指纹", "🧬", "fingerprint", False)
        self.add_tree_child(env_root, "风险中心", "🛡️", "risk", False)
        self.dll.ExpandAll(self.nav_tree)
        self.dll.SetTreeViewCallback(self.nav_tree, CALLBACK_NODE_SELECTED, self._tree_selected_cb)

    def create_switch_strip(self) -> None:
        for _ in range(4):
            self.recent_account_buttons.append(self.button(self.switch_panel, "", argb(255, 59, 130, 246)))
        self.txt_switch_search = self.edit(self.switch_panel, "搜索账号...")
        self.btn_more_accounts = self.button(self.switch_panel, "更多账号", argb(255, 148, 163, 184), self.toggle_drawer)

    def create_toolbar(self) -> None:
        self.txt_url = self.edit(self.toolbar_panel, "https://admin.shopify.com/")
        self.btn_theme = self.button(self.toolbar_panel, "🌙", argb(255, 148, 163, 184), self.toggle_theme)
        self.btn_launch = self.button(self.toolbar_panel, "启动", argb(255, 59, 130, 246), self.on_launch_browser)
        self.btn_stop = self.button(self.toolbar_panel, "停止", argb(255, 245, 158, 11), self.on_stop_browser)
        self.btn_refresh_page = self.button(self.toolbar_panel, "刷新", argb(255, 148, 163, 184), self.on_refresh_page)
        self.btn_relogin = self.button(self.toolbar_panel, "重登", argb(255, 148, 163, 184), self.on_relogin)
        self.btn_open_product = self.button(self.toolbar_panel, "商品页", argb(255, 34, 197, 94), self.on_open_product)
        self.btn_clear_cache = self.button(self.toolbar_panel, "清缓存", argb(255, 148, 163, 184), self.on_clear_cache)

    def create_drawer(self) -> None:
        self.lbl_sidebar_title = self.label(self.drawer_panel, "账号管理", 13, True)
        self.txt_drawer_search = self.edit(self.drawer_panel, "搜索账号/备注/店铺")
        self.cmb_drawer_status = self.combo(self.drawer_panel, ["全部状态", "运行中", "空闲", "异常", "登录中"])
        self.btn_drawer_add = self.button(self.drawer_panel, "新增", argb(255, 59, 130, 246), self.on_add_account)
        self.btn_drawer_import = self.button(self.drawer_panel, "导入", argb(255, 148, 163, 184), self.on_import_accounts)
        self.btn_drawer_export = self.button(self.drawer_panel, "导出", argb(255, 148, 163, 184), self.on_export_accounts)
        self.btn_drawer_refresh = self.button(self.drawer_panel, "刷新", argb(255, 148, 163, 184), self.on_query)
        self.btn_drawer_select_all = self.button(self.drawer_panel, "全选", argb(255, 148, 163, 184), self.on_toggle_select_all)
        self.btn_drawer_batch_start = self.button(self.drawer_panel, "批量启动", argb(255, 34, 197, 94), lambda: self.bulk_update_status("运行中"))
        self.btn_drawer_batch_stop = self.button(self.drawer_panel, "批量停止", argb(255, 245, 158, 11), lambda: self.bulk_update_status("空闲"))
        self.btn_drawer_batch_delete = self.button(self.drawer_panel, "批量删除", argb(255, 239, 68, 68), self.on_batch_delete)
        self.grid = self.dll.CreateDataGridView(self.drawer_panel, 0, 0, 100, 100, 0, 1, argb(255, 31, 41, 55), argb(255, 255, 255, 255))
        self.lbl_drawer_detail_title = self.label(self.drawer_panel, "当前选中账号", 12, True)
        for _ in range(4):
            self.drawer_detail_labels.append(self.label(self.drawer_panel, "", 10, False))
        self.setup_grid()

    def create_pages(self) -> None:
        for key in ("browser", "account", "proxy", "fingerprint", "risk", "logs"):
            panel = self.dll.CreatePanel(self.page_host, 0, 0, 100, 100, argb(255, 222, 228, 238))
            self.page_panels[key] = panel
            self.page_controls[key] = {}
        self.create_browser_page()
        self.create_info_page("account", "账号总览", "账号详情卡、店铺信息、最近操作与账号标签。", ("渠道", "状态", "店铺"), 7)
        self.create_info_page("proxy", "代理 / IP", "代理池、当前出口 IP、地区、连通性与测试动作。", ("出口IP", "地区", "代理状态"), 7, ("测试代理", self.on_test_proxy))
        self.create_info_page("fingerprint", "环境指纹", "UA、时区、WebRTC、Canvas、配置文件与隔离状态。", ("配置", "WebRTC", "Canvas"), 7, ("刷新指纹", self.on_refresh_fingerprint))
        self.create_info_page("risk", "风险中心", "风险告警、异常计数与最近触发记录。", ("异常账号", "登录中", "总体风险"), 7, ("标记已读", self.on_mark_risk_reviewed))
        self.create_logs_page()

    def create_browser_page(self) -> None:
        page = self.page_panels["browser"]
        controls = self.page_controls["browser"]
        controls["title"] = self.label(page, "浏览器宿主区", 20, True)
        controls["subtitle"] = self.label(page, "这里接入浏览器宿主窗口，仅在浏览器容器页面显示。", 12, False)
        controls["body"] = self.dll.CreatePanel(page, 0, 0, 100, 100, argb(255, 250, 252, 255))
        controls["canvas_title"] = self.label(controls["body"], "", 18, True)
        controls["canvas_subtitle"] = self.label(controls["body"], "", 11, False)
        controls["host_frame"] = self.dll.CreatePanel(controls["body"], 0, 0, 100, 100, argb(255, 255, 255, 255))
        controls["host_tabbar"] = self.dll.CreatePanel(controls["host_frame"], 0, 0, 100, 100, argb(255, 241, 245, 250))
        controls["host_tab"] = self.label(controls["host_tabbar"], "", 11, True)
        controls["host_toolbar"] = self.dll.CreatePanel(controls["host_frame"], 0, 0, 100, 100, argb(255, 248, 250, 252))
        controls["host_toolbar_left"] = self.label(controls["host_toolbar"], "←  →  ↻", 10, False)
        controls["host_url"] = self.label(controls["host_toolbar"], "", 10, False)
        controls["host_state"] = self.label(controls["host_toolbar"], "", 10, True)
        controls["host_canvas"] = self.dll.CreatePanel(controls["host_frame"], 0, 0, 100, 100, argb(255, 246, 248, 252))
        controls["host_viewport_frame"] = self.dll.CreatePanel(controls["host_canvas"], 0, 0, 100, 100, argb(255, 214, 223, 238))
        controls["host_viewport"] = self.dll.CreatePanel(controls["host_viewport_frame"], 0, 0, 100, 100, argb(255, 255, 255, 255))
        controls["host_canvas_title"] = self.label(controls["host_viewport"], "Browser Host Placeholder", 16, True)
        controls["host_canvas_subtitle"] = self.label(controls["host_viewport"], "这里后续接入真实浏览器窗口 / 宿主句柄。", 11, False)
        controls["host_skeletons"] = [self.dll.CreatePanel(controls["host_viewport"], 0, 0, 100, 100, argb(255, 229, 236, 246)) for _ in range(4)]
        controls["lines"] = [self.label(controls["host_canvas"], "", 10, False) for _ in range(2)]
        controls["insight_left"] = self.dll.CreatePanel(controls["body"], 0, 0, 100, 100, argb(255, 245, 248, 253))
        controls["insight_left_title"] = self.label(controls["insight_left"], "会话检查", 12, True)
        controls["insight_left_lines"] = [self.label(controls["insight_left"], "", 10, False) for _ in range(4)]
        controls["insight_right"] = self.dll.CreatePanel(controls["body"], 0, 0, 100, 100, argb(255, 245, 248, 253))
        controls["insight_right_title"] = self.label(controls["insight_right"], "建议动作", 12, True)
        controls["insight_right_lines"] = [self.label(controls["insight_right"], "", 10, False) for _ in range(4)]
        controls["summary_title"] = self.label(page, "运行摘要", 12, True)
        controls["summary_cards"] = [self.stat_card(page) for _ in range(3)]
        controls["task_queue"] = self.dll.CreatePanel(controls["body"], 0, 0, 100, 100, argb(255, 245, 248, 253))
        controls["task_queue_title"] = self.label(controls["task_queue"], "任务队列", 12, True)
        controls["task_queue_lines"] = [self.label(controls["task_queue"], "", 10, False) for _ in range(4)]
        controls["recent_title"] = self.label(page, "最近账号", 12, True)
        controls["recent_cards"] = [self.account_mini_card(page) for _ in range(2)]

    def create_info_page(self, key: str, title: str, subtitle: str, card_captions: tuple[str, str, str], line_count: int, action: tuple[str, callable] | None = None) -> None:
        page = self.page_panels[key]
        controls = self.page_controls[key]
        controls["title"] = self.label(page, title, 20, True)
        controls["subtitle"] = self.label(page, subtitle, 12, False)
        controls["cards"] = [self.stat_card(page) for _ in range(3)]
        for card, caption in zip(controls["cards"], card_captions):
            self.set_stat_card(card, "-", caption)
        controls["body"] = self.dll.CreatePanel(page, 0, 0, 100, 100, argb(255, 250, 252, 255))
        controls["lines"] = [self.label(controls["body"], "", 11, False) for _ in range(line_count)]
        if action:
            controls["action"] = self.button(page, action[0], argb(255, 59, 130, 246), action[1])

    def create_logs_page(self) -> None:
        page = self.page_panels["logs"]
        controls = self.page_controls["logs"]
        controls["title"] = self.label(page, "操作日志", 20, True)
        controls["subtitle"] = self.label(page, "时间线、过滤摘要与导出。", 12, False)
        controls["body"] = self.dll.CreatePanel(page, 0, 0, 100, 100, argb(255, 250, 252, 255))
        controls["lines"] = [self.label(controls["body"], "", 11, False) for _ in range(8)]
        controls["action"] = self.button(page, "导出日志", argb(255, 34, 197, 94), self.on_export_logs)

    def add_tree_root(self, text: str, icon: str) -> int:
        text_ptr, text_len, text_keep = utf8_buffer(text)
        icon_ptr, icon_len, icon_keep = utf8_buffer(icon)
        self._tree_keep = (text_keep, icon_keep)
        return int(self.dll.AddRootNode(self.nav_tree, text_ptr, text_len, icon_ptr, icon_len))

    def add_tree_child(self, parent_id: int, text: str, icon: str, view: str, opens_drawer: bool) -> int:
        text_ptr, text_len, text_keep = utf8_buffer(text)
        icon_ptr, icon_len, icon_keep = utf8_buffer(icon)
        self._tree_child_keep = (text_keep, icon_keep)
        node_id = int(self.dll.AddChildNode(self.nav_tree, parent_id, text_ptr, text_len, icon_ptr, icon_len))
        self.nav_tree_nodes[node_id] = (view, opens_drawer)
        self.nav_view_to_node[view] = node_id
        return node_id

    def setup_grid(self) -> None:
        for header, width, is_check in (("选", 34, True), ("账号", 92, False), ("店铺", 72, False), ("备注", 86, False), ("状态", 56, False)):
            ptr, ln, keep = utf8_buffer(header)
            self._grid_keep = keep
            if is_check:
                self.dll.DataGrid_AddCheckBoxColumn(self.grid, ptr, ln, width)
            else:
                self.dll.DataGrid_AddTextColumn(self.grid, ptr, ln, width)
        self.dll.DataGrid_SetHeaderHeight(self.grid, 34)
        self.dll.DataGrid_SetDefaultRowHeight(self.grid, 34)
        self.dll.DataGrid_SetFreezeHeader(self.grid, 1)
        self.dll.DataGrid_SetShowGridLines(self.grid, 1)
        self.dll.DataGrid_SetSelectionMode(self.grid, 1)
        self.dll.DataGrid_SetColumnHeaderAlignment(self.grid, 0, 1)
        self.dll.DataGrid_SetColumnCellAlignment(self.grid, 0, 1)
        self.dll.DataGrid_SetCellClickCallback(self.grid, self._grid_cell_click_cb)
        self.dll.DataGrid_SetCellValueChangedCallback(self.grid, self._grid_value_changed_cb)
        self.dll.DataGrid_SetSelectionChangedCallback(self.grid, self._grid_selection_changed_cb)

    def seed_accounts(self) -> None:
        seeds = [
            ("brand_site_01", "Shopify", "独立站A", "品牌站 / 大促页", "运行中", "https://admin.shopify.com/"),
            ("shop_jp_001", "Amazon", "日本站A", "活动专用", "登录中", "https://sellercentral-japan.amazon.com/"),
            ("shop_uk_003", "Shopify", "英国站B", "高客单品", "异常", "https://admin.shopify.com/store/uk"),
            ("shop_us_001", "Amazon", "美国站A", "主账号 / 独享代理", "运行中", "https://sellercentral.amazon.com/"),
            ("shop_us_002", "Amazon", "美国站B", "备用账号 / 广告", "空闲", "https://sellercentral.amazon.com/advertising"),
            ("shop_us_008", "Amazon", "美国站A", "FBA 补货", "空闲", "https://sellercentral.amazon.com/inventory"),
        ]
        for item in seeds:
            self.accounts.append(AccountRecord(self.next_id(), False, *item))
        self.selected_account_id = self.accounts[0].id

    def next_id(self) -> int:
        value = self.next_account_id
        self.next_account_id += 1
        return value

    def layout(self) -> None:
        cards_y = TITLE_BAR_HEIGHT + 8
        content_y = cards_y + CARDS_H + 10
        content_h = self.height - content_y - OUTER - BOTTOM_H
        self.layout_kpis(cards_y)

        self.move(self.nav_panel, OUTER, content_y, RAIL_W, content_h)
        self.layout_nav_panel(content_h)

        content_x = OUTER + RAIL_W + GAP
        content_w = self.width - content_x - OUTER
        self.move(self.content_panel, content_x, content_y, content_w, content_h)

        drawer_w = DRAWER_W if self.drawer_open else 0
        if drawer_w:
            drawer_y = content_y + SWITCH_H + GAP + TOOLBAR_H + GAP + CONTEXT_H + GAP
            drawer_h = content_h - (SWITCH_H + GAP + TOOLBAR_H + GAP + CONTEXT_H + GAP)
            self.move(self.drawer_panel, content_x, drawer_y, drawer_w, drawer_h)
            self.layout_drawer(drawer_w, drawer_h)
            self.show(self.drawer_panel, True)
        else:
            self.move(self.drawer_panel, -2000, -2000, 1, 1)
            self.show(self.drawer_panel, False)

        inner_offset_x = drawer_w + GAP if drawer_w else 0
        work_x = inner_offset_x
        work_w = content_w - inner_offset_x

        self.move(self.switch_panel, 0, 0, content_w, SWITCH_H)
        self.layout_switch_strip(content_w)
        self.move(self.toolbar_panel, work_x, SWITCH_H + GAP, work_w, TOOLBAR_H)
        self.layout_toolbar(work_w)
        self.move(self.context_panel, work_x, SWITCH_H + GAP + TOOLBAR_H + GAP, work_w, CONTEXT_H)
        self.dll.SetLabelBounds(self.lbl_context, 12, 8, work_w - 24, 18)

        workspace_y = SWITCH_H + GAP + TOOLBAR_H + GAP + CONTEXT_H + GAP
        workspace_h = content_h - (SWITCH_H + GAP + TOOLBAR_H + GAP + CONTEXT_H + GAP)
        self.move(self.workspace_panel, work_x, workspace_y, work_w, workspace_h)
        self.dll.SetLabelBounds(self.lbl_workspace_title, 0, 0, work_w, 30)
        self.dll.SetLabelBounds(self.lbl_workspace_subtitle, 0, 30, work_w, 20)
        self.move(self.page_host, 0, 58, work_w, workspace_h - 58)
        self.layout_pages(work_w, workspace_h - 58)

        self.move(self.status_panel, 0, content_h - BOTTOM_H, content_w, BOTTOM_H)
        self.dll.SetLabelBounds(self.lbl_status, 8, 4, content_w - 16, 16)

    def layout_drawer(self, width: int, height: int) -> None:
        self.dll.SetLabelBounds(self.lbl_sidebar_title, 16, 14, width - 32, 22)
        self.dll.SetEditBoxBounds(self.txt_drawer_search, 16, 44, width - 32, 34)
        self.dll.SetComboBoxBounds(self.cmb_drawer_status, 16, 86, width - 32, 34)

        row_gap = 8
        btn_w = (width - 32 - row_gap) // 2
        y1 = 132
        y2 = 174
        y3 = 216
        self.dll.SetButtonBounds(self.btn_drawer_add, 16, y1, btn_w, 34)
        self.dll.SetButtonBounds(self.btn_drawer_import, 16 + btn_w + row_gap, y1, btn_w, 34)
        self.dll.SetButtonBounds(self.btn_drawer_export, 16, y2, btn_w, 34)
        self.dll.SetButtonBounds(self.btn_drawer_refresh, 16 + btn_w + row_gap, y2, btn_w, 34)
        self.dll.SetButtonBounds(self.btn_drawer_select_all, 16, y3, btn_w, 34)
        self.dll.SetButtonBounds(self.btn_drawer_batch_start, 16 + btn_w + row_gap, y3, btn_w, 34)
        self.dll.SetButtonBounds(self.btn_drawer_batch_stop, 16, y3 + 42, btn_w, 34)
        self.dll.SetButtonBounds(self.btn_drawer_batch_delete, 16 + btn_w + row_gap, y3 + 42, btn_w, 34)

        grid_y = y3 + 92
        detail_h = 112
        self.dll.DataGrid_SetBounds(self.grid, 16, grid_y, width - 32, height - grid_y - detail_h - 24)
        self.apply_grid_column_widths(width - 32)
        detail_y = height - detail_h
        self.dll.SetLabelBounds(self.lbl_drawer_detail_title, 16, detail_y, width - 32, 18)
        for idx, label in enumerate(self.drawer_detail_labels):
            self.dll.SetLabelBounds(label, 16, detail_y + 24 + idx * 20, width - 32, 18)

    def layout_kpis(self, y: int) -> None:
        width = self.width - OUTER * 2
        card_w = (width - GAP * 5) // 6
        for index, card in enumerate(self.cards):
            x = OUTER + index * (card_w + GAP)
            self.move(card.panel, x, y, card_w, CARDS_H)
            self.move(card.accent, 0, 0, card_w, 6)
            self.move(card.divider, 14, 58, card_w - 28, 1)
            self.move(card.footer, 0, 59, card_w, CARDS_H - 59)
            self.dll.SetLabelBounds(card.badge, card_w - 68, 12, 52, 18)
            self.dll.SetLabelBounds(card.value, 14, 16, card_w - 28, 28)
            self.dll.SetLabelBounds(card.title, 14, 40, card_w - 28, 18)
            self.dll.SetLabelBounds(card.hint, 14, 72, card_w - 28, 14)

    def layout_nav_panel(self, height: int) -> None:
        self.dll.SetLabelBounds(self.lbl_nav_title, 16, 14, RAIL_W - 32, 20)
        self.dll.SetLabelBounds(self.lbl_nav_hint, 16, 34, RAIL_W - 32, 14)
        self.move(self.nav_tree, 12, 58, RAIL_W - 24, height - 72)

    def layout_switch_strip(self, width: int) -> None:
        self.dll.SetLabelBounds(self.lbl_switch_title, 0, 12, 78, 18)
        x = 86
        chip_w = 122
        for button in self.recent_account_buttons:
            self.dll.SetButtonBounds(button, x, 6, chip_w, 32)
            x += chip_w + 8
        self.dll.SetButtonBounds(self.btn_more_accounts, width - 104, 6, 104, 32)
        search_w = max(220, width - x - 116)
        self.dll.SetEditBoxBounds(self.txt_switch_search, x, 6, search_w, 32)

    def layout_toolbar(self, width: int) -> None:
        button_specs = [
            (self.btn_launch, 96),
            (self.btn_stop, 72),
            (self.btn_refresh_page, 72),
            (self.btn_relogin, 72),
            (self.btn_open_product, 104),
            (self.btn_clear_cache, 88),
        ]
        theme_w = 40
        button_gap = 8
        total_button_w = sum(item[1] for item in button_specs) + button_gap * len(button_specs) + theme_w
        url_w = max(320, width - total_button_w - 12)
        self.dll.SetEditBoxBounds(self.txt_url, 0, 4, url_w, 34)
        x = url_w + 12
        for button_id, button_w in button_specs:
            self.dll.SetButtonBounds(button_id, x, 4, button_w, 34)
            x += button_w + button_gap
        self.dll.SetButtonBounds(self.btn_theme, width - theme_w, 4, theme_w, 34)

    def layout_pages(self, width: int, height: int) -> None:
        for panel in self.page_panels.values():
            self.move(panel, 0, 0, width, height)
        for view in self.page_panels:
            controls = self.page_controls[view]
            self.dll.SetLabelBounds(controls["title"], 20, 18, width - 40, 30)
            self.dll.SetLabelBounds(controls["subtitle"], 20, 48, width - 40, 22)
        browser_controls = self.page_controls["browser"]
        side_w = max(236, min(284, width // 4))
        main_w = width - 40 - side_w - GAP
        side_x = 20 + main_w + GAP
        body_h = height - 104
        self.move(browser_controls["body"], 20, 84, main_w, body_h)
        self.dll.SetLabelBounds(browser_controls["canvas_title"], 20, 18, main_w - 40, 28)
        self.dll.SetLabelBounds(browser_controls["canvas_subtitle"], 20, 48, main_w - 40, 20)
        host_y = 86
        host_h = 188
        self.move(browser_controls["host_frame"], 20, host_y, main_w - 40, host_h)
        self.move(browser_controls["host_tabbar"], 0, 0, main_w - 40, 30)
        self.dll.SetLabelBounds(browser_controls["host_tab"], 16, 8, main_w - 120, 18)
        self.move(browser_controls["host_toolbar"], 0, 30, main_w - 40, 34)
        self.dll.SetLabelBounds(browser_controls["host_toolbar_left"], 16, 10, 72, 18)
        self.dll.SetLabelBounds(browser_controls["host_url"], 96, 10, main_w - 240, 18)
        self.dll.SetLabelBounds(browser_controls["host_state"], main_w - 136, 10, 108, 18)
        self.move(browser_controls["host_canvas"], 12, 72, main_w - 64, host_h - 84)
        canvas_w = main_w - 64
        canvas_h = host_h - 84
        self.move(browser_controls["host_viewport_frame"], 0, 0, canvas_w, 74)
        self.move(browser_controls["host_viewport"], 1, 1, canvas_w - 2, 72)
        self.dll.SetLabelBounds(browser_controls["host_canvas_title"], 14, 12, canvas_w - 28, 20)
        self.dll.SetLabelBounds(browser_controls["host_canvas_subtitle"], 14, 32, canvas_w - 28, 16)
        skeleton_widths = [canvas_w - 100, canvas_w - 140, canvas_w - 170, 92]
        for idx, panel in enumerate(browser_controls["host_skeletons"]):
            self.move(panel, 14, 54 + idx * 4, max(36, skeleton_widths[idx]), 6)
        for i, lbl in enumerate(browser_controls["lines"]):
            self.dll.SetLabelBounds(lbl, 8, 82 + i * 14, canvas_w - 16, 14)
        insight_y = host_y + host_h + 14
        insight_w = (main_w - 52) // 2
        insight_h = 108
        self.move(browser_controls["insight_left"], 20, insight_y, insight_w, insight_h)
        self.move(browser_controls["insight_right"], 32 + insight_w, insight_y, insight_w, insight_h)
        self.dll.SetLabelBounds(browser_controls["insight_left_title"], 14, 14, insight_w - 28, 20)
        self.dll.SetLabelBounds(browser_controls["insight_right_title"], 14, 14, insight_w - 28, 20)
        for i, lbl in enumerate(browser_controls["insight_left_lines"]):
            self.dll.SetLabelBounds(lbl, 14, 42 + i * 18, insight_w - 28, 16)
        for i, lbl in enumerate(browser_controls["insight_right_lines"]):
            self.dll.SetLabelBounds(lbl, 14, 42 + i * 18, insight_w - 28, 16)
        queue_y = insight_y + insight_h + 14
        queue_h = max(86, body_h - queue_y - 18)
        self.move(browser_controls["task_queue"], 20, queue_y, main_w - 40, queue_h)
        self.dll.SetLabelBounds(browser_controls["task_queue_title"], 16, 14, main_w - 72, 20)
        for i, lbl in enumerate(browser_controls["task_queue_lines"]):
            self.dll.SetLabelBounds(lbl, 16, 42 + i * 16, main_w - 72, 16)
        self.dll.SetLabelBounds(browser_controls["summary_title"], side_x, 86, side_w, 20)
        for idx, card in enumerate(browser_controls["summary_cards"]):
            self.move(card.panel, side_x, 112 + idx * 68, side_w, 60)
            self.dll.SetLabelBounds(card.value, 14, 10, side_w - 28, 22)
            self.dll.SetLabelBounds(card.caption, 14, 34, side_w - 28, 16)
        recent_y = 112 + len(browser_controls["summary_cards"]) * 68
        self.dll.SetLabelBounds(browser_controls["recent_title"], side_x, recent_y, side_w, 20)
        card_y = recent_y + 26
        for idx, card in enumerate(browser_controls["recent_cards"]):
            self.move(card.panel, side_x, card_y + idx * 74, side_w, 68)
            self.dll.SetLabelBounds(card.title, 14, 12, side_w - 28, 22)
            self.dll.SetLabelBounds(card.meta, 14, 34, side_w - 28, 14)
            self.dll.SetLabelBounds(card.status, 14, 50, side_w - 28, 14)
        for view in ("account", "proxy", "fingerprint", "risk"):
            controls = self.page_controls[view]
            card_w = (width - 40 - GAP * 2) // 3
            for idx, card in enumerate(controls["cards"]):
                self.move(card.panel, 20 + idx * (card_w + GAP), 84, card_w, STAT_CARD_H)
                self.dll.SetLabelBounds(card.value, 14, 12, card_w - 28, 24)
                self.dll.SetLabelBounds(card.caption, 14, 40, card_w - 28, 18)
            self.move(controls["body"], 20, 180, width - 40, height - 232)
            for i, lbl in enumerate(controls["lines"]):
                self.dll.SetLabelBounds(lbl, 20, 18 + i * 32, width - 80, 22)
            if "action" in controls:
                self.dll.SetButtonBounds(controls["action"], 20, height - 44, 110, 32)
        logs = self.page_controls["logs"]
        self.move(logs["body"], 20, 84, width - 40, height - 136)
        for i, lbl in enumerate(logs["lines"]):
            self.dll.SetLabelBounds(lbl, 20, 18 + i * 30, width - 80, 22)
        self.dll.SetButtonBounds(logs["action"], 20, height - 44, 110, 32)

    def apply_theme(self) -> None:
        current_theme = self.current_page_theme()
        brand = int(current_theme["accent"])
        titlebar_brand = int(current_theme["titlebar"])
        page = argb(255, 17, 24, 39) if self.dark_mode else argb(255, 244, 247, 252)
        surface = argb(255, 30, 41, 59) if self.dark_mode else argb(255, 255, 255, 255)
        soft = argb(255, 36, 47, 67) if self.dark_mode else argb(255, 246, 249, 253)
        body = argb(255, 22, 31, 44) if self.dark_mode else argb(255, 252, 253, 255)
        text = argb(255, 226, 232, 240) if self.dark_mode else argb(255, 22, 34, 56)
        muted = argb(255, 148, 163, 184) if self.dark_mode else argb(255, 104, 119, 143)
        nav_surface = argb(255, 23, 37, 64) if self.dark_mode else argb(255, 22, 43, 76)
        nav_soft = argb(255, 31, 52, 88) if self.dark_mode else argb(255, 29, 56, 96)
        card_bg = argb(255, 32, 44, 66) if self.dark_mode else argb(255, 244, 248, 255)
        section_bg = argb(255, 34, 48, 72) if self.dark_mode else argb(255, 240, 245, 252)
        input_bg = argb(255, 30, 41, 59) if self.dark_mode else argb(255, 255, 255, 255)
        secondary_btn = argb(255, 47, 64, 92) if self.dark_mode else argb(255, 233, 240, 251)
        page_tint = mix_color(page, brand, 0.06 if not self.dark_mode else 0.16)
        page_host_bg = mix_color(page, brand, 0.1 if not self.dark_mode else 0.22)
        switch_bg = mix_color(surface, brand, 0.03 if not self.dark_mode else 0.12)
        context_bg = mix_color(section_bg, brand, 0.06 if not self.dark_mode else 0.18)
        title_text = argb(255, 255, 255, 255)

        window_title = f"电商多账号浏览器管理器 · {current_theme['emoji']} {current_theme['title']}"
        title_ptr, title_len, title_keep = utf8_buffer(window_title)
        self._window_title_keep = title_keep
        self.dll.set_window_title(self.window, title_ptr, title_len)
        self.dll.set_window_titlebar_color(self.window, mix_color(titlebar_brand, argb(255, 15, 23, 42), 0.35) if self.dark_mode else titlebar_brand)
        self.dll.SetTitleBarTextColor(self.window, title_text)
        self.dll.SetWindowBackgroundColor(self.window, page)
        self.dll.SetPanelBackgroundColor(self.nav_panel, nav_surface)
        self.dll.SetPanelBackgroundColor(self.drawer_panel, surface)
        self.dll.SetPanelBackgroundColor(self.content_panel, page_tint)
        self.dll.SetPanelBackgroundColor(self.toolbar_panel, surface)
        self.dll.SetPanelBackgroundColor(self.workspace_panel, page_tint)
        self.dll.SetPanelBackgroundColor(self.switch_panel, switch_bg)
        self.dll.SetPanelBackgroundColor(self.context_panel, context_bg)
        self.dll.SetPanelBackgroundColor(self.status_panel, page_tint)
        self.dll.SetPanelBackgroundColor(self.page_host, page_host_bg)

        self.dll.SetLabelColor(self.lbl_nav_title, argb(255, 255, 255, 255), nav_surface)
        self.dll.SetLabelColor(self.lbl_nav_hint, mix_color(argb(255, 255, 255, 255), nav_surface, 0.35), nav_surface)
        self.dll.SetLabelColor(self.lbl_switch_title, mix_color(text, brand, 0.22), switch_bg)
        self.dll.SetLabelColor(self.lbl_sidebar_title, text, surface)
        self.dll.SetLabelColor(self.lbl_workspace_title, mix_color(text, brand, 0.28), page_tint)
        self.dll.SetLabelColor(self.lbl_workspace_subtitle, muted, page_tint)
        self.dll.SetLabelColor(self.lbl_context, text, context_bg)
        self.dll.SetLabelColor(self.lbl_status, muted, page_tint)

        self.paint_button(self.btn_theme, secondary_btn)
        self.paint_button(self.btn_launch, brand)
        self.paint_button(self.btn_stop, argb(255, 245, 158, 11))
        self.paint_button(self.btn_refresh_page, secondary_btn)
        self.paint_button(self.btn_relogin, secondary_btn)
        self.paint_button(self.btn_open_product, argb(255, 34, 197, 94))
        self.paint_button(self.btn_clear_cache, secondary_btn)
        self.paint_button(self.btn_more_accounts, secondary_btn)
        if self.nav_tree:
            hover = nav_soft
            selected_bg = brand
            selected_fg = argb(255, 255, 255, 255)
            self.dll.SetTreeViewBackgroundColor(self.nav_tree, nav_surface)
            self.dll.SetTreeViewTextColor(self.nav_tree, argb(255, 234, 240, 252))
            self.dll.SetTreeViewSelectedBgColor(self.nav_tree, selected_bg)
            self.dll.SetTreeViewSelectedForeColor(self.nav_tree, selected_fg)
            self.dll.SetTreeViewHoverBgColor(self.nav_tree, hover)
        for button in (self.btn_drawer_add, self.btn_drawer_import, self.btn_drawer_export, self.btn_drawer_refresh, self.btn_drawer_select_all, self.btn_drawer_batch_start, self.btn_drawer_batch_stop, self.btn_drawer_batch_delete):
            color = {
                self.btn_drawer_add: brand,
                self.btn_drawer_batch_start: argb(255, 34, 197, 94),
                self.btn_drawer_batch_stop: argb(255, 245, 158, 11),
                self.btn_drawer_batch_delete: argb(255, 239, 68, 68),
            }.get(button, secondary_btn)
            self.paint_button(button, color)
        for card in self.cards:
            metric_bg = mix_color(card.accent_color, argb(255, 255, 255, 255), 0.9) if not self.dark_mode else mix_color(card.accent_color, surface, 0.78)
            metric_footer_bg = mix_color(metric_bg, argb(255, 255, 255, 255), 0.5) if not self.dark_mode else mix_color(metric_bg, argb(255, 255, 255, 255), 0.08)
            metric_divider = mix_color(card.accent_color, muted, 0.35) if not self.dark_mode else mix_color(card.accent_color, argb(255, 255, 255, 255), 0.22)
            metric_text = mix_color(text, card.accent_color, 0.35) if not self.dark_mode else argb(255, 255, 255, 255)
            self.dll.SetPanelBackgroundColor(card.panel, metric_bg)
            self.dll.SetPanelBackgroundColor(card.footer, metric_footer_bg)
            self.dll.SetPanelBackgroundColor(card.divider, metric_divider)
            self.dll.SetLabelColor(card.value, card.accent_color, metric_bg)
            self.dll.SetLabelColor(card.title, metric_text, metric_bg)
            self.dll.SetLabelColor(card.hint, mix_color(muted, card.accent_color, 0.12), metric_footer_bg)
            self.dll.SetLabelColor(card.badge, argb(255, 255, 255, 255), card.accent_color)

        self.dll.SetEditBoxColor(self.txt_switch_search, text, input_bg)
        self.dll.SetEditBoxColor(self.txt_url, text, input_bg)
        self.dll.SetEditBoxColor(self.txt_drawer_search, text, input_bg)
        self.dll.SetComboBoxColors(self.cmb_drawer_status, text, input_bg, soft, soft)
        self.dll.DataGrid_SetColors(self.grid, text, input_bg, soft, muted, mix_color(brand, argb(255, 255, 255, 255), 0.84), soft, mix_color(muted, argb(255, 255, 255, 255), 0.6))

        for view_key, controls in self.page_controls.items():
            view_theme = self.PAGE_THEMES.get(view_key, current_theme)
            view_brand = int(view_theme["accent"])
            view_page_bg = mix_color(page_host_bg, view_brand, 0.06 if not self.dark_mode else 0.12)
            view_card_bg = mix_color(surface, view_brand, 0.08 if not self.dark_mode else 0.18)
            view_section_bg = mix_color(soft, view_brand, 0.08 if not self.dark_mode else 0.16)
            self.dll.SetLabelColor(controls["title"], mix_color(text, view_brand, 0.32), view_page_bg)
            self.dll.SetLabelColor(controls["subtitle"], mix_color(muted, view_brand, 0.08), view_page_bg)
            if "body" in controls:
                self.dll.SetPanelBackgroundColor(controls["body"], view_page_bg)
            for label in controls.get("lines", []):
                self.dll.SetLabelColor(label, text, view_page_bg)
            for card in controls.get("cards", []) + controls.get("summary_cards", []):
                themed_card_bg = mix_color(card_bg, view_brand, 0.12 if not self.dark_mode else 0.18)
                self.dll.SetPanelBackgroundColor(card.panel, themed_card_bg)
                self.dll.SetLabelColor(card.value, view_brand, themed_card_bg)
                self.dll.SetLabelColor(card.caption, muted, themed_card_bg)
            if "summary_title" in controls:
                self.dll.SetLabelColor(controls["summary_title"], mix_color(text, view_brand, 0.24), view_page_bg)
            if "canvas_title" in controls:
                self.dll.SetLabelColor(controls["canvas_title"], mix_color(text, view_brand, 0.22), view_page_bg)
            if "canvas_subtitle" in controls:
                self.dll.SetLabelColor(controls["canvas_subtitle"], muted, view_page_bg)
            if "host_frame" in controls:
                host_canvas_bg = mix_color(view_page_bg, view_brand, 0.08 if not self.dark_mode else 0.12)
                host_border_bg = mix_color(view_brand, argb(255, 255, 255, 255), 0.72) if not self.dark_mode else argb(255, 61, 77, 102)
                host_view_bg = argb(255, 255, 255, 255) if not self.dark_mode else argb(255, 18, 26, 38)
                skeleton_bg = mix_color(view_brand, argb(255, 255, 255, 255), 0.82) if not self.dark_mode else argb(255, 52, 66, 86)
                self.dll.SetPanelBackgroundColor(controls["host_frame"], view_card_bg)
                self.dll.SetPanelBackgroundColor(controls["host_tabbar"], mix_color(view_brand, argb(255, 255, 255, 255), 0.9) if not self.dark_mode else view_section_bg)
                self.dll.SetPanelBackgroundColor(controls["host_toolbar"], view_section_bg)
                self.dll.SetPanelBackgroundColor(controls["host_canvas"], host_canvas_bg)
                self.dll.SetPanelBackgroundColor(controls["host_viewport_frame"], host_border_bg)
                self.dll.SetPanelBackgroundColor(controls["host_viewport"], host_view_bg)
                for panel in controls.get("host_skeletons", []):
                    self.dll.SetPanelBackgroundColor(panel, skeleton_bg)
                self.dll.SetLabelColor(controls["host_tab"], mix_color(text, view_brand, 0.22), view_section_bg)
                self.dll.SetLabelColor(controls["host_toolbar_left"], muted, view_section_bg)
                self.dll.SetLabelColor(controls["host_url"], text, view_section_bg)
                self.dll.SetLabelColor(controls["host_state"], view_brand, view_section_bg)
                self.dll.SetLabelColor(controls["host_canvas_title"], text, host_view_bg)
                self.dll.SetLabelColor(controls["host_canvas_subtitle"], muted, host_view_bg)
                for label in controls.get("lines", []):
                    self.dll.SetLabelColor(label, muted, host_canvas_bg)
            if "insight_left" in controls:
                left_bg = mix_color(argb(255, 34, 197, 94), argb(255, 255, 255, 255), 0.9) if not self.dark_mode else view_section_bg
                self.dll.SetPanelBackgroundColor(controls["insight_left"], left_bg)
                self.dll.SetLabelColor(controls["insight_left_title"], text, left_bg)
                for label in controls.get("insight_left_lines", []):
                    self.dll.SetLabelColor(label, text, left_bg)
            if "insight_right" in controls:
                right_bg = mix_color(argb(255, 245, 158, 11), argb(255, 255, 255, 255), 0.9) if not self.dark_mode else view_section_bg
                self.dll.SetPanelBackgroundColor(controls["insight_right"], right_bg)
                self.dll.SetLabelColor(controls["insight_right_title"], text, right_bg)
                for label in controls.get("insight_right_lines", []):
                    self.dll.SetLabelColor(label, text, right_bg)
            if "task_queue" in controls:
                queue_bg = mix_color(view_brand, argb(255, 255, 255, 255), 0.93) if not self.dark_mode else view_section_bg
                self.dll.SetPanelBackgroundColor(controls["task_queue"], queue_bg)
                self.dll.SetLabelColor(controls["task_queue_title"], text, queue_bg)
                for label in controls.get("task_queue_lines", []):
                    self.dll.SetLabelColor(label, text, queue_bg)
            if "recent_title" in controls:
                self.dll.SetLabelColor(controls["recent_title"], mix_color(text, view_brand, 0.24), view_page_bg)
            for card in controls.get("recent_cards", []):
                self.dll.SetPanelBackgroundColor(card.panel, view_card_bg)
                self.dll.SetLabelColor(card.title, text, view_card_bg)
                self.dll.SetLabelColor(card.meta, muted, view_card_bg)
                self.dll.SetLabelColor(card.status, view_brand, view_card_bg)
            if "action" in controls:
                self.paint_button(controls["action"], view_brand if controls["action"] != self.page_controls["logs"]["action"] else argb(255, 34, 197, 94))

        self.set_button_emoji(self.btn_theme, "☀️" if self.dark_mode else "🌙")
        self.update_metrics()
        self.refresh_recent_account_buttons()
        self.render_workspace()

    def refresh_runtime_data(self, force_network: bool) -> None:
        now = time.time()
        if not force_network and self.runtime_snapshot and now - self.last_runtime_refresh < 30:
            return
        snap: dict[str, str] = {}
        snap["hostname"] = socket.gethostname()
        snap["timezone"] = self.detect_timezone()
        snap["proxy"] = self.detect_proxy_config()
        snap["local_ip"] = self.detect_local_ip()
        snap["user_agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/123 Safari/537.36"
        snap["canvas"] = hashlib.md5(f"{platform.machine()}|{platform.version()}".encode()).hexdigest()[:10].upper()
        snap["device_hash"] = hashlib.sha256(f"{platform.node()}|{snap['local_ip']}|{platform.platform()}".encode()).hexdigest()[:12].upper()
        snap["cookie_root"] = str((Path.home() / ".emoji_window_profiles").resolve())
        snap["webrtc"] = snap["local_ip"] or "-"
        snap["public_ip"] = "-"
        if force_network or not self.runtime_geo:
            snap["public_ip"], self.runtime_geo = self.query_public_ip_geo()
        elif self.runtime_geo:
            snap["public_ip"] = self.runtime_geo.get("ip", "-")
        self.runtime_snapshot = snap
        self.last_runtime_refresh = now

    def detect_timezone(self) -> str:
        try:
            result = subprocess.run(["tzutil", "/g"], capture_output=True, text=True, timeout=2, check=False)
            value = (result.stdout or "").strip()
            return value or "Local"
        except Exception:
            return "Local"

    def detect_proxy_config(self) -> str:
        env_proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("HTTP_PROXY")
        if env_proxy:
            return env_proxy
        try:
            result = subprocess.run(["netsh", "winhttp", "show", "proxy"], capture_output=True, text=True, timeout=2, check=False)
            output = (result.stdout or "").strip()
            if "Direct access" in output or "直接访问" in output:
                return "Direct access"
            return output.splitlines()[-1].strip() if output else "-"
        except Exception:
            return "-"

    def detect_local_ip(self) -> str:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.connect(("8.8.8.8", 80))
            value = sock.getsockname()[0]
            sock.close()
            return value
        except Exception:
            return "-"

    def query_public_ip_geo(self) -> tuple[str, dict[str, str]]:
        try:
            with urllib.request.urlopen("https://ipwho.is/", timeout=2.5) as response:
                payload = json.loads(response.read().decode("utf-8", errors="replace"))
            ip = str(payload.get("ip") or "-")
            geo = {
                "ip": ip,
                "country": str(payload.get("country") or "-"),
                "city": str(payload.get("city") or "-"),
                "timezone": str((payload.get("timezone") or {}).get("id") or "-"),
                "asn": str((payload.get("connection") or {}).get("asn") or "-"),
                "org": str((payload.get("connection") or {}).get("org") or "-"),
            }
            return ip, geo
        except Exception:
            return "-", {}

    def proxy_profile(self, account: AccountRecord | None) -> dict[str, str]:
        self.refresh_runtime_data(False)
        snap = self.runtime_snapshot
        geo = self.runtime_geo or {}
        if not account:
            return {"exit_ip": "-", "region": "-", "timezone": "-", "asn": "-", "proxy_type": "-", "latency": "-", "status": "No account"}
        proxy_text = snap.get("proxy", "-")
        proxy_type = "Direct" if proxy_text in {"-", "Direct access"} else ("SOCKS" if "socks" in proxy_text.lower() else "HTTP/HTTPS")
        status = "High risk" if account.status == "异常" else ("Need review" if proxy_type == "Direct" or snap.get("public_ip") == "-" else "Healthy")
        region = " / ".join(part for part in [geo.get("country", "-"), geo.get("city", "-")] if part and part != "-").strip(" /") or "-"
        return {
            "exit_ip": snap.get("public_ip", "-"),
            "region": region,
            "timezone": geo.get("timezone") or snap.get("timezone", "-"),
            "asn": geo.get("asn") or geo.get("org") or "-",
            "proxy_type": proxy_type,
            "latency": "Updated after test",
            "status": status,
        }

    def fingerprint_profile(self, account: AccountRecord | None) -> dict[str, str]:
        self.refresh_runtime_data(False)
        snap = self.runtime_snapshot
        if not account:
            return {"profile_name": "-", "browser_profile": "-", "user_agent": "-", "webrtc": "-", "canvas": "-", "timezone_align": "-", "cookie_isolation": "-"}
        return {
            "profile_name": f"{account.channel}-profile-{account.id % 9 + 1}",
            "browser_profile": f"profile_{account.account}",
            "user_agent": snap.get("user_agent", "-"),
            "webrtc": snap.get("webrtc", "-"),
            "canvas": snap.get("canvas", "-"),
            "timezone_align": self.proxy_profile(account)["timezone"],
            "cookie_isolation": f"{snap.get('cookie_root', '-')}/{account.account}",
        }

    def risk_items(self, account: AccountRecord | None) -> list[str]:
        if not account:
            return ["未选择账号，无法评估风险。"]
        proxy = self.proxy_profile(account)
        items = []
        if account.status == "异常":
            items.append("账号状态异常，建议重新登录并更换代理。")
        if account.status == "登录中":
            items.append("账号处于登录中，短时间内不要切换过多代理。")
        if proxy["proxy_type"] == "Direct":
            items.append("当前未检测到代理配置，存在本机直连风险。")
        if proxy["exit_ip"] == "-" or proxy["region"] == "-":
            items.append("公网 IP 或地理位置未识别成功，建议执行一次代理测试。")
        items.append(f"设备摘要：{self.runtime_snapshot.get('device_hash', '-')}/{self.runtime_snapshot.get('canvas', '-')}")
        items.append("最近 24 小时未发现 Cookie 串用。")
        return items[:6]

    def apply_filters(self, status_message: str) -> None:
        keyword = self.get_text(self.txt_drawer_search).strip().lower()
        status_text = self.combo_selected_text(self.cmb_drawer_status)
        self.visible_ids = []
        for account in self.accounts:
            if status_text and status_text != "全部状态" and account.status != status_text:
                continue
            if keyword and keyword not in f"{account.account} {account.store} {account.note}".lower():
                continue
            self.visible_ids.append(account.id)
        if self.selected_account_id not in self.visible_ids and self.visible_ids:
            self.selected_account_id = self.visible_ids[0]
        self.update_metrics()
        self.refresh_recent_account_buttons()
        self.populate_grid()
        self.render_workspace()
        self.set_status(status_message)

    def populate_grid(self) -> None:
        self.dll.DataGrid_ClearRows(self.grid)
        selected_row = -1
        for row_index, account in enumerate(self.visible_accounts()):
            row = self.dll.DataGrid_AddRow(self.grid)
            self.dll.DataGrid_SetCellChecked(self.grid, row, 0, 1 if account.checked else 0)
            for col, text in enumerate((account.account, account.store, account.note, account.status), start=1):
                ptr, ln, keep = utf8_buffer(text)
                self._grid_text_keep = keep
                self.dll.DataGrid_SetCellText(self.grid, row, col, ptr, ln)
            if account.id == self.selected_account_id:
                selected_row = row_index
        if selected_row >= 0:
            self.dll.DataGrid_SetSelectedCell(self.grid, selected_row, 1)
        self.dll.DataGrid_Refresh(self.grid)

    def visible_accounts(self) -> list[AccountRecord]:
        visible = set(self.visible_ids)
        return [item for item in self.accounts if item.id in visible]

    def refresh_recent_account_buttons(self) -> None:
        recent = self.accounts[:4]
        for button, account in zip(self.recent_account_buttons, recent):
            self.set_button_text(button, account.account)
            self.button_actions[button] = lambda acc=account: self.select_account(acc.id)
            self.paint_button(button, argb(255, 56, 107, 235) if account.id == self.selected_account_id else argb(255, 233, 240, 251))
        for button in self.recent_account_buttons[len(recent):]:
            self.set_button_text(button, "")
            self.paint_button(button, argb(255, 233, 240, 251))

    def select_account(self, account_id: int) -> None:
        self.selected_account_id = account_id
        self.render_workspace()
        self.set_status(f"已切换账号 {self.current_account().account}")

    def current_account(self) -> AccountRecord | None:
        return next((item for item in self.accounts if item.id == self.selected_account_id), None)

    def sync_nav_tree_selection(self) -> None:
        if not self.nav_tree:
            return
        target_view = "account" if self.drawer_open else self.current_view
        node_id = self.nav_view_to_node.get(target_view)
        if node_id:
            self._suppress_nav_callback = True
            self.dll.SetSelectedNode(self.nav_tree, node_id)
            self._suppress_nav_callback = False

    def on_nav_tree_selected(self, node_id: int, _context) -> None:
        if self._suppress_nav_callback:
            return
        info = self.nav_tree_nodes.get(node_id)
        if not info:
            return
        view, opens_drawer = info
        self.drawer_open = opens_drawer
        self.current_view = view
        self.apply_theme()
        self.layout()

    def switch_view(self, view: str) -> None:
        self.current_view = view
        if view != "account":
            self.drawer_open = False
        self.apply_theme()
        self.layout()
        self.sync_nav_tree_selection()

    def toggle_drawer(self) -> None:
        self.drawer_open = not self.drawer_open
        self.current_view = "account" if self.drawer_open else "browser"
        self.apply_theme()
        self.layout()
        self.sync_nav_tree_selection()

    def render_workspace(self) -> None:
        account = self.current_account()
        proxy = self.proxy_profile(account)
        fp = self.fingerprint_profile(account)
        risk = "高" if account and account.status == "异常" else "中" if account and account.status == "登录中" else "低"
        current_theme = self.current_page_theme()
        self.set_label_text(self.lbl_workspace_title, f"{current_theme['emoji']} 工作区")
        self.set_label_text(self.lbl_workspace_subtitle, f"当前页面：{current_theme['title']}")
        self.set_label_text(self.lbl_context, f"当前账号：{account.account if account else '-'} | 店铺：{account.store if account else '-'} | 代理：{proxy['exit_ip']} | 指纹：{fp['profile_name']} | 风险：{risk}")
        for view, panel in self.page_panels.items():
            self.show(panel, view == self.current_view)
        self.sync_nav_tree_selection()
        self.render_browser_page(account, proxy, fp, risk)
        self.render_account_page(account)
        self.render_proxy_page(proxy)
        self.render_fingerprint_page(fp)
        self.render_risk_page(account)
        self.render_logs_page()

    def render_browser_page(self, account: AccountRecord | None, proxy: dict[str, str], fp: dict[str, str], risk: str) -> None:
        c = self.page_controls["browser"]
        self.set_label_text(c["title"], f"🌐 浏览器宿主区{(' / ' + account.account) if account else ''}")
        self.set_label_text(c["subtitle"], "这里接入浏览器宿主窗口，仅在浏览器容器页面显示。")
        self.set_label_text(c["canvas_title"], f"当前会话：{account.account if account else '-'}")
        self.set_label_text(c["canvas_subtitle"], "这里作为浏览器挂载位，下面直接串联任务队列、会话检查和最近活跃账号。")
        self.set_label_text(c["host_tab"], f"● {account.account if account else '未选择账号'}")
        self.set_label_text(c["host_url"], self.get_text(self.txt_url))
        self.set_label_text(c["host_state"], "子窗口已就绪" if self.browser_running else "等待挂载")
        self.set_label_text(c["host_canvas_title"], "浏览器挂载区")
        self.set_label_text(c["host_canvas_subtitle"], "真实浏览器窗口将嵌入在此区域；当前先展示会话占位、状态与关键上下文。")
        lines = [
            f"子窗口边框：已创建占位框架，等待宿主句柄挂载",
            f"代理出口：{proxy['exit_ip']}  |  风险：{risk}  |  指纹：{fp['profile_name']}",
        ]
        self.set_label_lines(c["lines"], lines)
        self.set_stat_card(c["summary_cards"][0], account.channel if account else "-", "渠道")
        self.set_stat_card(c["summary_cards"][1], proxy["status"], "网络")
        self.set_stat_card(c["summary_cards"][2], "已启动" if self.browser_running else "未启动", "浏览器")
        checklist_lines = [
            f"账号状态：{account.status if account else '-'}",
            f"代理类型：{proxy['proxy_type']}",
            f"时区：{proxy['timezone']}",
            f"Cookie隔离：{fp['cookie_isolation']}",
        ]
        action_lines = [
            "1. 启动浏览器并检查登录态",
            "2. 确认代理出口与目标站点地区一致",
            "3. 打开商品页后再执行广告或补货任务",
            f"4. 当前风险偏好：{risk}",
        ]
        self.set_label_lines(c["insight_left_lines"], checklist_lines)
        self.set_label_lines(c["insight_right_lines"], action_lines)
        task_queue_lines = [
            f"1. {'继续监控 Shopify 后台登录态' if self.browser_running else '启动浏览器并进入后台首页'}",
            f"2. 检查 {account.store if account else '-'} 的代理连通性与地区一致性",
            f"3. {'打开商品页并更新库存' if account and account.channel == 'Shopify' else '进入 Seller Central 检查广告 / FBA 任务'}",
            f"4. 最后操作：{self.operation_logs[-1] if self.operation_logs else '暂无记录'}",
        ]
        self.set_label_lines(c["task_queue_lines"], task_queue_lines)
        recent_accounts = self.accounts[:2]
        for card, item in zip(c["recent_cards"], recent_accounts):
            self.set_account_mini_card(
                card,
                item.account,
                f"{item.store} / {item.channel}",
                f"{item.status} · {'当前账号' if item.id == self.selected_account_id else '最近活跃'}",
            )
        for card in c["recent_cards"][len(recent_accounts):]:
            self.set_account_mini_card(card, "-", "-", "-")

    def render_account_page(self, account: AccountRecord | None) -> None:
        c = self.page_controls["account"]
        self.set_label_text(c["title"], "👥 账号总览")
        self.set_stat_card(c["cards"][0], account.channel if account else "-", "渠道")
        self.set_stat_card(c["cards"][1], account.status if account else "-", "状态")
        self.set_stat_card(c["cards"][2], account.store if account else "-", "店铺")
        lines = [
            f"账号：{account.account if account else '-'}",
            f"渠道：{account.channel if account else '-'}",
            f"店铺：{account.store if account else '-'}",
            f"备注：{account.note if account else '-'}",
            f"状态：{account.status if account else '-'}",
            f"最近操作：{self.operation_logs[-1] if self.operation_logs else '暂无记录'}",
            f"账号标签：{'高优先级 / 独立环境' if account else '-'}",
        ]
        self.set_label_lines(c["lines"], lines)
        self.render_drawer_details(account)

    def render_proxy_page(self, proxy: dict[str, str]) -> None:
        c = self.page_controls["proxy"]
        self.set_label_text(c["title"], "🌍 代理 / IP")
        self.set_stat_card(c["cards"][0], proxy["exit_ip"], "出口IP")
        self.set_stat_card(c["cards"][1], proxy["region"], "地区")
        self.set_stat_card(c["cards"][2], proxy["status"], "代理状态")
        lines = [
            f"出口IP：{proxy['exit_ip']}",
            f"地区：{proxy['region']}",
            f"时区：{proxy['timezone']}",
            f"ASN：{proxy['asn']}",
            f"代理类型：{proxy['proxy_type']}",
            f"延迟：{proxy['latency']}",
            f"健康度：{proxy['status']}",
        ]
        self.set_label_lines(c["lines"], lines)

    def render_fingerprint_page(self, fp: dict[str, str]) -> None:
        c = self.page_controls["fingerprint"]
        self.set_label_text(c["title"], "🧬 环境指纹")
        self.set_stat_card(c["cards"][0], fp["browser_profile"], "配置")
        self.set_stat_card(c["cards"][1], fp["webrtc"], "WebRTC")
        self.set_stat_card(c["cards"][2], fp["canvas"], "Canvas")
        lines = [
            f"指纹方案：{fp['profile_name']}",
            f"浏览器配置：{fp['browser_profile']}",
            f"User-Agent：{fp['user_agent']}",
            f"WebRTC：{fp['webrtc']}",
            f"Canvas：{fp['canvas']}",
            f"时区对齐：{fp['timezone_align']}",
            f"Cookie隔离：{fp['cookie_isolation']}",
        ]
        self.set_label_lines(c["lines"], lines)

    def render_risk_page(self, account: AccountRecord | None) -> None:
        c = self.page_controls["risk"]
        self.set_label_text(c["title"], "🛡️ 风险中心")
        abnormal = sum(1 for item in self.accounts if item.status == "异常")
        logging_in = sum(1 for item in self.accounts if item.status == "登录中")
        self.set_stat_card(c["cards"][0], str(abnormal), "异常账号")
        self.set_stat_card(c["cards"][1], str(logging_in), "登录中")
        self.set_stat_card(c["cards"][2], "需关注" if abnormal or logging_in else "稳定", "总体风险")
        lines = self.risk_items(account) + [f"异常账号数：{abnormal}"]
        self.set_label_lines(c["lines"], lines)

    def render_logs_page(self) -> None:
        c = self.page_controls["logs"]
        self.set_label_text(c["title"], "📝 操作日志")
        lines = list(reversed(self.operation_logs[-8:])) if self.operation_logs else ["暂无操作日志。"]
        self.set_label_lines(c["lines"], lines)

    def render_drawer_details(self, account: AccountRecord | None) -> None:
        lines = [
            f"账号：{account.account if account else '-'}",
            f"店铺：{account.store if account else '-'}",
            f"状态：{account.status if account else '-'}",
            f"备注：{account.note if account else '-'}",
        ]
        self.set_label_lines(self.drawer_detail_labels, lines)

    def update_metrics(self) -> None:
        online = sum(1 for item in self.accounts if item.status in ("运行中", "登录中"))
        running = sum(1 for item in self.accounts if item.status == "运行中")
        abnormal = sum(1 for item in self.accounts if item.status == "异常")
        pending = sum(1 for item in self.accounts if item.status in ("登录中", "异常", "空闲"))
        stores = len({item.store for item in self.accounts})
        proxy_ok = 0 if not self.accounts else int(round((len(self.accounts) - abnormal) * 100 / len(self.accounts)))
        values = [str(online), str(running), str(abnormal), str(pending), str(stores), f"{proxy_ok}%"]
        for card, value, hint in zip(self.cards, values, self.KPI_HINTS):
            self.set_label_text(card.value, value)
            self.set_label_text(card.hint, hint)

    def on_button_click(self, button_id: int, parent: HWND) -> None:
        action = self.button_actions.get(button_id)
        if action:
            action()

    def on_window_resize(self, hwnd: HWND, width: int, height: int) -> None:
        if int(ctypes.cast(hwnd, ctypes.c_void_p).value or 0) != int(ctypes.cast(self.window, ctypes.c_void_p).value or 0):
            return
        if width <= 0 or height <= 0:
            return
        self.width = width
        self.height = height
        with RedrawScope(self.window):
            self.layout()

    def on_edit_key(self, h_edit: HWND, key_code: int, key_down: int, shift: int, ctrl: int, alt: int) -> None:
        if key_code != VK_RETURN or not key_down:
            return
        handle = int(ctypes.cast(h_edit, ctypes.c_void_p).value or 0)
        if handle == int(ctypes.cast(self.txt_url, ctypes.c_void_p).value or 0):
            self.append_log("浏览器", f"导航到 {self.get_text(self.txt_url)}")
            self.render_workspace()
            return
        if handle == int(ctypes.cast(self.txt_switch_search, ctypes.c_void_p).value or 0):
            keyword = self.get_text(self.txt_switch_search).strip().lower()
            if keyword:
                target = next((item for item in self.accounts if keyword in item.account.lower() or keyword in item.store.lower()), None)
                if target:
                    self.select_account(target.id)
                    self.append_log("切换", f"搜索切换到 {target.account}")
            return
        if handle == int(ctypes.cast(self.txt_drawer_search, ctypes.c_void_p).value or 0):
            self.on_query()

    def on_grid_cell_click(self, h_grid: HWND, row: int, col: int) -> None:
        if row < 0 or row >= len(self.visible_ids):
            return
        self.select_account(self.visible_ids[row])
        if col == 0:
            checked = self.dll.DataGrid_GetCellChecked(self.grid, row, 0) != 0
            self.current_account().checked = checked

    def on_grid_value_changed(self, h_grid: HWND, row: int, col: int) -> None:
        if col == 0 and 0 <= row < len(self.visible_ids):
            self.current_account().checked = self.dll.DataGrid_GetCellChecked(self.grid, row, 0) != 0

    def on_grid_selection_changed(self, h_grid: HWND, row: int, col: int) -> None:
        if 0 <= row < len(self.visible_ids):
            self.select_account(self.visible_ids[row])

    def on_query(self) -> None:
        self.apply_filters("已应用筛选条件。")

    def on_add_account(self) -> None:
        account = AccountRecord(self.next_id(), False, f"shop_auto_{self.next_account_id:03d}", "Amazon", "美国站A", "新广告位", "空闲", "https://sellercentral.amazon.com/")
        self.accounts.insert(0, account)
        self.selected_account_id = account.id
        self.append_log("账号", f"新增账号 {account.account}")
        self.apply_filters(f"已新增账号 {account.account}")

    def on_import_accounts(self) -> None:
        for suffix in ("01", "02"):
            self.accounts.append(AccountRecord(self.next_id(), False, f"import_{suffix}", "Shopify", "独立站A", "导入批次", "运行中", "https://admin.shopify.com/"))
        self.append_log("账号", "导入 2 条示例账号")
        self.apply_filters("已导入示例账号")

    def on_export_accounts(self) -> None:
        path = Path(__file__).resolve().parent / "_accounts_export.csv"
        with path.open("w", newline="", encoding="utf-8-sig") as fh:
            writer = csv.writer(fh)
            writer.writerow(["账号", "渠道", "店铺", "备注", "状态", "URL"])
            for item in self.visible_accounts():
                writer.writerow([item.account, item.channel, item.store, item.note, item.status, item.url])
        self.append_log("导出", f"导出账号 -> {path.name}")
        self.set_status(f"已导出账号到 {path.name}")

    def on_toggle_select_all(self) -> None:
        target = not all(item.checked for item in self.visible_accounts()) if self.visible_ids else False
        for item in self.visible_accounts():
            item.checked = target
        self.populate_grid()

    def bulk_update_status(self, status: str) -> None:
        for item in self.accounts:
            if item.checked:
                item.status = status
        self.append_log("批量", f"批量更新为 {status}")
        self.apply_filters(f"已批量更新为 {status}")

    def on_batch_delete(self) -> None:
        checked_ids = {item.id for item in self.accounts if item.checked}
        self.accounts = [item for item in self.accounts if item.id not in checked_ids]
        self.append_log("批量", f"批量删除 {len(checked_ids)} 个账号")
        self.apply_filters("已删除勾选账号")

    def toggle_theme(self) -> None:
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        self.layout()

    def on_launch_browser(self) -> None:
        if self.current_account():
            self.browser_running = True
            self.current_account().status = "运行中"
            self.append_log("浏览器", f"启动 {self.current_account().account}")
            self.render_workspace()

    def on_stop_browser(self) -> None:
        self.browser_running = False
        self.append_log("浏览器", "停止当前浏览器")
        self.render_workspace()

    def on_refresh_page(self) -> None:
        self.append_log("浏览器", "刷新当前页面")
        self.render_workspace()

    def on_relogin(self) -> None:
        if self.current_account():
            self.current_account().status = "登录中"
            self.append_log("浏览器", f"重登 {self.current_account().account}")
            self.render_workspace()

    def on_open_product(self) -> None:
        if self.current_account():
            self.current_account().url = "https://admin.shopify.com/store/products" if self.current_account().channel == "Shopify" else "https://sellercentral.amazon.com/inventory"
            self.set_edit_text(self.txt_url, self.current_account().url)
            self.append_log("浏览器", f"打开商品页 {self.current_account().account}")
            self.render_workspace()

    def on_clear_cache(self) -> None:
        self.append_log("浏览器", "清理缓存")
        self.render_workspace()

    def on_test_proxy(self) -> None:
        self.refresh_runtime_data(True)
        self.append_log("代理", f"测试代理 {self.proxy_profile(self.current_account())['exit_ip']}")
        self.render_workspace()

    def on_refresh_fingerprint(self) -> None:
        self.refresh_runtime_data(False)
        self.append_log("指纹", "刷新指纹配置")
        self.render_workspace()

    def on_mark_risk_reviewed(self) -> None:
        self.append_log("风控", "风险项已标记为已读")
        self.render_workspace()

    def on_export_logs(self) -> None:
        path = Path(__file__).resolve().parent / "_operation_logs.txt"
        path.write_text("\n".join(self.operation_logs), encoding="utf-8")
        self.append_log("日志", f"导出日志 -> {path.name}")
        self.render_workspace()

    def append_log(self, category: str, message: str) -> None:
        self.operation_logs.append(f"[{category}] {message}")
        if len(self.operation_logs) > 50:
            self.operation_logs = self.operation_logs[-50:]
        self.set_status(message)

    def button(self, parent: HWND, text: str, bg: int | None, action=None) -> int:
        emoji_ptr, emoji_len, emoji_keep = utf8_buffer("")
        text_ptr, text_len, text_keep = utf8_buffer(text)
        self._button_keep = (emoji_keep, text_keep)
        button_id = self.dll.create_emoji_button_bytes(parent, emoji_ptr, emoji_len, text_ptr, text_len, 0, 0, 100, 34, bg or argb(255, 148, 163, 184))
        if action is not None:
            self.button_actions[button_id] = action
        self.dll.ShowButton(button_id, 1)
        return button_id

    def label(self, parent: HWND, text: str, size: int, bold: bool, fg: int | None = None, bg: int | None = None) -> HWND:
        text_ptr, text_len, keep = utf8_buffer(text)
        self._label_keep = keep
        return self.dll.CreateLabel(parent, 0, 0, 100, 20, text_ptr, text_len, fg or argb(255, 31, 41, 55), bg or argb(255, 255, 255, 255), FONT_YAHEI_PTR, FONT_YAHEI_LEN, size, 1 if bold else 0, 0, 0, 0, 0)

    def edit(self, parent: HWND, text: str) -> HWND:
        text_ptr, text_len, keep = utf8_buffer(text)
        self._edit_keep = keep
        return self.dll.CreateEditBox(parent, 0, 0, 100, 34, text_ptr, text_len, argb(255, 31, 41, 55), argb(255, 255, 255, 255), FONT_SEGOE_PTR, FONT_SEGOE_LEN, 10, 0, 0, 0, 0, 0, 0, 0, 1, 1)

    def combo(self, parent: HWND, items: list[str]) -> HWND:
        combo = self.dll.CreateComboBox(parent, 0, 0, 100, 34, 1, argb(255, 31, 41, 55), argb(255, 255, 255, 255), 32, FONT_SEGOE_PTR, FONT_SEGOE_LEN, 11, 0, 0, 0)
        self.dll.ClearComboBox(combo)
        for item in items:
            ptr, ln, keep = utf8_buffer(item)
            self._combo_keep = keep
            self.dll.AddComboItem(combo, ptr, ln)
        self.dll.SetComboSelectedIndex(combo, 0)
        return combo

    def stat_card(self, parent: HWND) -> StatCard:
        panel = self.dll.CreatePanel(parent, 0, 0, 100, STAT_CARD_H, argb(255, 250, 252, 255))
        value = self.label(panel, "-", 18, True)
        caption = self.label(panel, "-", 10, False)
        return StatCard(panel, value, caption)

    def account_mini_card(self, parent: HWND) -> AccountMiniCard:
        panel = self.dll.CreatePanel(parent, 0, 0, 100, 84, argb(255, 250, 252, 255))
        title = self.label(panel, "-", 12, True)
        meta = self.label(panel, "-", 10, False)
        status = self.label(panel, "-", 10, False)
        return AccountMiniCard(panel, title, meta, status)

    def set_stat_card(self, card: StatCard, value: str, caption: str) -> None:
        self.set_label_text(card.value, value)
        self.set_label_text(card.caption, caption)

    def set_account_mini_card(self, card: AccountMiniCard, title: str, meta: str, status: str) -> None:
        self.set_label_text(card.title, title)
        self.set_label_text(card.meta, meta)
        self.set_label_text(card.status, status)

    def set_label_lines(self, labels: list[HWND], lines: list[str]) -> None:
        for index, label in enumerate(labels):
            self.set_label_text(label, lines[index] if index < len(lines) else "")

    def apply_grid_column_widths(self, inner_width: int) -> None:
        if not self.grid or inner_width < 220:
            return
        base = [30, 88, 62, 80, 48]
        total = sum(base)
        widths: list[int] = []
        used = 0
        for item in base[:-1]:
            value = max(30, (item * inner_width + total // 2) // total)
            widths.append(value)
            used += value
        widths.append(max(30, inner_width - used))
        if sum(widths) != inner_width:
            widths[-1] += inner_width - sum(widths)
        for column, width in enumerate(widths):
            self.dll.DataGrid_SetColumnWidth(self.grid, column, width)

    def current_page_theme(self) -> dict[str, object]:
        return self.PAGE_THEMES.get(self.current_view, self.PAGE_THEMES["browser"])

    def paint_button(self, button_id: int, bg: int) -> None:
        self.dll.SetButtonStyle(button_id, 0)
        self.dll.SetButtonSize(button_id, 1)
        self.dll.SetButtonRound(button_id, 10)
        self.dll.SetButtonBackgroundColor(button_id, bg)
        self.dll.SetButtonBorderColor(button_id, shift_color(bg, -18))
        text_color = argb(255, 22, 34, 56) if color_brightness(bg) >= 175 else argb(255, 255, 255, 255)
        self.dll.SetButtonTextColor(button_id, text_color)
        self.dll.SetButtonHoverColors(button_id, shift_color(bg, 10), shift_color(bg, 4), text_color)

    def set_button_text(self, button_id: int, text: str) -> None:
        ptr, ln, keep = utf8_buffer(text)
        self._set_button_keep = keep
        self.dll.SetButtonText(button_id, ptr, ln)

    def set_button_emoji(self, button_id: int, emoji: str) -> None:
        ptr, ln, keep = utf8_buffer(emoji)
        self._set_emoji_keep = keep
        self.dll.SetButtonEmoji(button_id, ptr, ln)

    def set_label_text(self, hwnd: HWND, text: str) -> None:
        ptr, ln, keep = utf8_buffer(text)
        self._set_label_keep = keep
        self.dll.SetLabelText(hwnd, ptr, ln)

    def set_edit_text(self, hwnd: HWND, text: str) -> None:
        ptr, ln, keep = utf8_buffer(text)
        self._set_edit_keep = keep
        self.dll.SetEditBoxText(hwnd, ptr, ln)

    def get_text(self, hwnd: HWND) -> str:
        size = self.dll.GetEditBoxText(hwnd, None, 0)
        if size <= 0:
            return ""
        buf = (ctypes.c_ubyte * size)()
        self.dll.GetEditBoxText(hwnd, ctypes.cast(buf, ctypes.c_void_p), size)
        return bytes(buf[:size]).decode("utf-8", errors="replace")

    def combo_selected_text(self, hwnd: HWND) -> str:
        index = self.dll.GetComboSelectedIndex(hwnd)
        if index < 0:
            return ""
        size = self.dll.GetComboItemText(hwnd, index, None, 0)
        if size <= 0:
            return ""
        buf = (ctypes.c_ubyte * size)()
        self.dll.GetComboItemText(hwnd, index, ctypes.cast(buf, ctypes.c_void_p), size)
        return bytes(buf[:size]).decode("utf-8", errors="replace")

    def move(self, hwnd: HWND, x: int, y: int, width: int, height: int) -> None:
        USER32.MoveWindow(int(ctypes.cast(hwnd, ctypes.c_void_p).value or 0), x, y, width, height, True)

    def show(self, hwnd: HWND, visible: bool) -> None:
        USER32.ShowWindow(int(ctypes.cast(hwnd, ctypes.c_void_p).value or 0), SW_SHOW if visible else SW_HIDE)

    def set_status(self, text: str) -> None:
        self.set_label_text(self.lbl_status, text)


def main() -> None:
    BrowserManagerApp().run()
