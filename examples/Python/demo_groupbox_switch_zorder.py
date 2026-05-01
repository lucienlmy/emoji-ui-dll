# -*- coding: utf-8 -*-
from __future__ import annotations

import sys

import demo_all_components_tabs as base

if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except OSError:
        pass

HWND = base.HWND
BOOL = base.BOOL
DLL = base.DLL
KEEP = base.KEEP


def main() -> int:
    base.setup()

    title_p, title_n, _ = base.s("GroupBox + Switch z-order demo")
    hwnd = DLL.create_window_bytes(title_p, title_n, 140, 140, 820, 430)
    base.STATE["hwnd"] = hwnd

    base.label(hwnd, "Switch 被 GroupBox 覆盖验证", 36, 34, 520, 34, fg=5, bg=13, size=20, bold=True)
    base.label(
        hwnd,
        "这个 demo 先创建 Switch，再创建覆盖同一区域的 GroupBox。修复生效时，开关仍可见且可点击。",
        36,
        74,
        720,
        28,
        fg=6,
        bg=13,
    )

    on_p, on_n, _ = base.s("开")
    off_p, off_n, _ = base.s("关")
    switch = DLL.CreateSwitch(
        hwnd,
        142,
        192,
        144,
        40,
        BOOL(True),
        0xFF409EFF,
        0xFFDCDfe6,
        on_p,
        on_n,
        off_p,
        off_n,
    )

    group_title_p, group_title_n, _ = base.s("后创建的 GroupBox 装饰层")
    group = DLL.CreateGroupBox(
        hwnd,
        72,
        132,
        640,
        170,
        group_title_p,
        group_title_n,
        10,
        14,
        base.FONT_PTR,
        base.FONT_LEN,
        14,
        BOOL(True),
        BOOL(False),
        BOOL(False),
    )
    DLL.SetGroupBoxStyle(group, base.GROUPBOX_STYLE_CARD)
    DLL.SetGroupBoxTitleColor(group, 5)

    status = base.label(hwnd, "点击开关验证回调。当前状态: 开", 72, 330, 640, 26, fg=4, bg=13)
    base.STATE["status"] = status

    def on_switch(_hwnd: HWND, checked: BOOL) -> None:
        base.set_label_text(status, f"Switch 回调已触发，当前状态: {'开' if checked else '关'}")

    cb = DLL._SwitchCB(on_switch)
    KEEP.append(cb)
    DLL.SetSwitchCallback(switch, cb)

    DLL.set_message_loop_main_window(hwnd)
    DLL.run_message_loop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
