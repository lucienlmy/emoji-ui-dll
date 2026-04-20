# -*- coding: utf-8 -*-
from __future__ import annotations

import ctypes
import os
import struct
import sys
import threading
import time
from ctypes import wintypes
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except OSError:
        pass

HWND = wintypes.HWND
UINT32 = wintypes.UINT
BOOL = wintypes.BOOL

USER32 = ctypes.WinDLL("user32", use_last_error=True)
WM_CLOSE = 0x0010

SW_SHOW = 5


def argb(a: int, r: int, g: int, b: int) -> int:
    return ((a & 255) << 24) | ((r & 255) << 16) | ((g & 255) << 8) | (b & 255)


def utf8_buf(text: str):
    raw = text.encode("utf-8")
    if not raw:
        return ctypes.c_void_p(), 0, None
    buf = (ctypes.c_ubyte * len(raw))(*raw)
    return ctypes.cast(buf, ctypes.c_void_p), len(raw), buf


def dll_path() -> Path:
    root = Path(__file__).resolve().parents[2]
    p = root / "bin" / "x64" / "Release" / "emoji_window.dll"
    if p.is_file():
        return p
    local = Path(__file__).resolve().parent / "emoji_window.dll"
    return local


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

# Window
DLL.create_window_bytes_ex.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, UINT32, UINT32]
DLL.create_window_bytes_ex.restype = HWND
DLL.set_window_icon_bytes.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
DLL.set_window_titlebar_color.argtypes = [HWND, UINT32]
DLL.SetWindowBackgroundColor.argtypes = [HWND, UINT32]
DLL.SetTitleBarTextColor.argtypes = [HWND, UINT32]
DLL.SetWindowResizeCallback.argtypes = [ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int, ctypes.c_int)]
DLL.SetWindowCloseCallback.argtypes = [ctypes.WINFUNCTYPE(None, HWND)]
DLL.set_message_loop_main_window.argtypes = [HWND]
DLL.run_message_loop.argtypes = []
DLL.run_message_loop.restype = ctypes.c_int
DLL.destroy_window.argtypes = [HWND]

# Tab
DLL.CreateTabControl.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
DLL.CreateTabControl.restype = HWND
DLL.AddTabItem.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, HWND]
DLL.AddTabItem.restype = ctypes.c_int
DLL.GetTabContentWindow.argtypes = [HWND, ctypes.c_int]
DLL.GetTabContentWindow.restype = HWND
DLL.SetTabItemSize.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
DLL.SetTabHeaderStyle.argtypes = [HWND, ctypes.c_int]
DLL.SetTabPosition.argtypes = [HWND, ctypes.c_int]
DLL.SetTabAlignment.argtypes = [HWND, ctypes.c_int]
DLL.SetTabScrollable.argtypes = [HWND, ctypes.c_int]
DLL.SetTabClosable.argtypes = [HWND, ctypes.c_int]
DLL.SetTabFont.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_float]
DLL.SetTabColors.argtypes = [HWND, UINT32, UINT32, UINT32, UINT32]
DLL.SetTabIndicatorColor.argtypes = [HWND, UINT32]
DLL.SetTabPadding.argtypes = [HWND, ctypes.c_int, ctypes.c_int]
DLL.SetTabControlBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
DLL.SelectTabImmediate.argtypes = [HWND, ctypes.c_int]
DLL.GetTabCount.argtypes = [HWND]
DLL.GetTabCount.restype = ctypes.c_int
DLL.RedrawTabControl.argtypes = [HWND]
DLL.RedrawTabControl.restype = BOOL
DLL.SetTabCallback.argtypes = [HWND, ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int)]

# Button
DLL.create_emoji_button_bytes.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, UINT32]
DLL.create_emoji_button_bytes.restype = ctypes.c_int
DLL.SetButtonBounds.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
DLL.SetButtonBackgroundColor.argtypes = [ctypes.c_int, UINT32]
DLL.SetButtonTextColor.argtypes = [ctypes.c_int, UINT32]
DLL.SetButtonBorderColor.argtypes = [ctypes.c_int, UINT32]
DLL.SetButtonHoverColors.argtypes = [ctypes.c_int, UINT32, UINT32, UINT32]
DLL.ShowButton.argtypes = [ctypes.c_int, ctypes.c_int]

# Label
DLL.CreateLabel.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, UINT32, UINT32, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
DLL.CreateLabel.restype = HWND
DLL.SetLabelText.argtypes = [HWND, ctypes.c_void_p, ctypes.c_int]
DLL.SetLabelBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
DLL.ShowLabel.argtypes = [HWND, ctypes.c_int]

# Edit
DLL.CreateEditBox.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int, UINT32, UINT32, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
DLL.CreateEditBox.restype = HWND
DLL.SetEditBoxColor.argtypes = [HWND, UINT32, UINT32]
DLL.SetEditBoxBounds.argtypes = [HWND, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
DLL.ShowEditBox.argtypes = [HWND, ctypes.c_int]


class State:
    hwnd: HWND | None = None
    tab: HWND | None = None
    content: HWND | None = None
    current_index: int = 0
    width: int = 1200
    height: int = 780
    buttons: list[int] = []
    edit: HWND | None = None
    labels: list[HWND] = []
    running: bool = True
    log: list[str] = []


STATE = State()
KEEP: list[object] = []


def log(msg: str) -> None:
    print(msg, flush=True)
    STATE.log.append(msg)


def create_button(parent: HWND, text: str, x: int, y: int) -> int:
    tp, tn, _ = utf8_buf(text)
    button_id = int(DLL.create_emoji_button_bytes(parent, ctypes.c_void_p(), 0, tp, tn, x, y, 32, 32, argb(255, 244, 247, 252)))
    DLL.SetButtonBackgroundColor(button_id, argb(255, 244, 247, 252))
    DLL.SetButtonTextColor(button_id, argb(255, 92, 100, 110))
    DLL.SetButtonBorderColor(button_id, argb(255, 244, 247, 252))
    DLL.SetButtonHoverColors(button_id, argb(255, 232, 238, 246), argb(255, 232, 238, 246), argb(255, 66, 133, 244))
    DLL.ShowButton(button_id, 1)
    return button_id


def create_label(parent: HWND, text: str, x: int, y: int, w: int, h: int, size: int, fg: int) -> HWND:
    tp, tn, _ = utf8_buf(text)
    fp, fn, _ = utf8_buf("Microsoft YaHei UI")
    hwnd = DLL.CreateLabel(parent, x, y, w, h, tp, tn, fg, argb(255, 255, 255, 255), fp, fn, size, 0, 0, 0, 0, 0)
    DLL.ShowLabel(hwnd, 1)
    return hwnd


def create_ui() -> None:
    title_ptr, title_len, keep = utf8_buf("Python TabControl Resize Selftest")
    KEEP.append(keep)
    STATE.hwnd = DLL.create_window_bytes_ex(title_ptr, title_len, -1, -1, STATE.width, STATE.height, argb(255, 223, 226, 230), argb(255, 246, 248, 252))
    if not STATE.hwnd:
        raise RuntimeError("create_window_bytes_ex failed")

    font_ptr, font_len, keep_font = utf8_buf("Microsoft YaHei UI")
    KEEP.append(keep_font)
    DLL.set_window_titlebar_color(STATE.hwnd, argb(255, 223, 226, 230))
    DLL.SetTitleBarTextColor(STATE.hwnd, argb(255, 32, 33, 36))
    DLL.SetWindowBackgroundColor(STATE.hwnd, argb(255, 246, 248, 252))

    STATE.tab = DLL.CreateTabControl(STATE.hwnd, 0, 0, STATE.width, STATE.height - 62)
    DLL.SetTabItemSize(STATE.tab, 188, 34)
    DLL.SetTabHeaderStyle(STATE.tab, 2)
    DLL.SetTabPosition(STATE.tab, 0)
    DLL.SetTabAlignment(STATE.tab, 0)
    DLL.SetTabScrollable(STATE.tab, 1)
    DLL.SetTabClosable(STATE.tab, 1)
    DLL.SetTabFont(STATE.tab, font_ptr, font_len, ctypes.c_float(11.5))
    DLL.SetTabColors(STATE.tab, argb(255, 255, 255, 255), argb(255, 232, 234, 237), argb(255, 32, 33, 36), argb(255, 95, 99, 104))
    DLL.SetTabIndicatorColor(STATE.tab, argb(255, 32, 33, 36))
    DLL.SetTabPadding(STATE.tab, 14, 3)

    tabcb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int)(on_tab_changed)
    closecb = ctypes.WINFUNCTYPE(None, HWND)(on_window_close)
    resizecb = ctypes.WINFUNCTYPE(None, HWND, ctypes.c_int, ctypes.c_int)(on_window_resize)
    KEEP.extend([tabcb, closecb, resizecb])
    DLL.SetTabCallback(STATE.tab, tabcb)
    DLL.SetWindowCloseCallback(closecb)
    DLL.SetWindowResizeCallback(resizecb)

    tp, tn, keep_title = utf8_buf("google.com/")
    KEEP.append(keep_title)
    idx = int(DLL.AddTabItem(STATE.tab, tp, tn, HWND()))
    if idx < 0:
        raise RuntimeError("AddTabItem failed")
    STATE.current_index = idx
    STATE.content = DLL.GetTabContentWindow(STATE.tab, idx)
    if not STATE.content:
        raise RuntimeError("GetTabContentWindow failed")

    STATE.buttons = [
        create_button(STATE.content, "<", 20, 14),
        create_button(STATE.content, ">", 56, 14),
        create_button(STATE.content, "R", 92, 14),
        create_button(STATE.content, "H", 128, 14),
    ]

    ep, en, keep_edit = utf8_buf("https://www.google.com/")
    KEEP.append(keep_edit)
    STATE.edit = DLL.CreateEditBox(STATE.content, 172, 12, STATE.width - 220, 34, ep, en, argb(255, 32, 33, 36), argb(255, 255, 255, 255), font_ptr, font_len, 13, 0, 0, 0, 0, 0, 0, 0, 1, 1)
    DLL.SetEditBoxColor(STATE.edit, argb(255, 32, 33, 36), argb(255, 255, 255, 255))
    DLL.ShowEditBox(STATE.edit, 1)

    STATE.labels = [
        create_label(STATE.content, "新标签页", 32, 84, 720, 40, 28, argb(255, 32, 33, 36)),
        create_label(STATE.content, "已输入地址：https://www.google.com/", 32, 132, 900, 26, 12, argb(255, 95, 99, 104)),
        create_label(STATE.content, "页面状态：Python 自测脚本", 32, 176, 900, 24, 12, argb(255, 66, 133, 244)),
        create_label(STATE.content, "Current URL: https://www.google.com/", 32, 230, 980, 24, 12, argb(255, 95, 99, 104)),
        create_label(STATE.content, "Current Tab: 1", 32, 260, 980, 24, 12, argb(255, 95, 99, 104)),
        create_label(STATE.content, "Toolbar Actions: Back / Forward / Refresh / Home", 32, 290, 980, 24, 12, argb(255, 95, 99, 104)),
    ]

    layout_content()
    DLL.SelectTabImmediate(STATE.tab, idx)
    DLL.RedrawTabControl(STATE.tab)
    log("UI created")


def layout_content() -> None:
    if not STATE.content:
        return
    w = max(320, STATE.width)
    content_w = w - 64
    address_w = max(120, w - 160 - 36)
    for i, button in enumerate(STATE.buttons):
        DLL.SetButtonBounds(button, 20 + i * 36, 14, 32, 32)
    if STATE.edit:
        DLL.SetEditBoxBounds(STATE.edit, 160, 8, address_w, 34)
        DLL.ShowEditBox(STATE.edit, 1)
    y_map = [84, 132, 176, 230, 260, 290]
    h_map = [40, 26, 24, 24, 24, 24]
    for hwnd, y, h in zip(STATE.labels, y_map, h_map):
        DLL.SetLabelBounds(hwnd, 32, y, content_w, h)


def on_tab_changed(h_tab: HWND, index: int) -> None:
    STATE.current_index = index
    log(f"tab changed: {index}")


def on_window_close(hwnd: HWND) -> None:
    STATE.running = False
    log("window closed")


def on_window_resize(hwnd: HWND, width: int, height: int) -> None:
    if hwnd != STATE.hwnd:
        return
    if width <= 1 or height <= 1:
        return
    STATE.width = max(320, width)
    STATE.height = max(240, height)
    DLL.SetTabControlBounds(STATE.tab, 0, 0, STATE.width, STATE.height - 62)
    layout_content()
    if DLL.GetTabCount(STATE.tab) > 0:
        DLL.SelectTabImmediate(STATE.tab, STATE.current_index)
    DLL.RedrawTabControl(STATE.tab)
    log(f"resize callback: {width}x{height}")


def drive_resize_and_close() -> None:
    time.sleep(1.0)
    sizes = [
        (980, 640),
        (1280, 820),
        (900, 620),
        (1400, 900),
        (1100, 700),
    ]
    for w, h in sizes:
        if not STATE.running or not STATE.hwnd:
            return
        log(f"resize -> {w}x{h}")
        USER32.MoveWindow(STATE.hwnd, 40, 40, w, h, True)
        time.sleep(0.5)
    time.sleep(1.0)
    if STATE.hwnd:
        log("post WM_CLOSE")
        USER32.PostMessageW(STATE.hwnd, WM_CLOSE, 0, 0)
    time.sleep(2.0)
    if STATE.running:
        log("force exit after timeout")
        os._exit(0)


def main() -> int:
    create_ui()
    DLL.set_message_loop_main_window(STATE.hwnd)
    t = threading.Thread(target=drive_resize_and_close, daemon=True)
    t.start()
    rc = int(DLL.run_message_loop())
    log(f"message loop exited: rc={rc}")
    return rc


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"SELFTEST FAILED: {exc}", flush=True)
        raise
