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

    title_p, title_n, _ = base.s("GroupBox + Slider z-order demo")
    hwnd = DLL.create_window_bytes(title_p, title_n, 120, 120, 820, 430)
    base.STATE["hwnd"] = hwnd

    base.label(hwnd, "Slider 被 GroupBox 覆盖验证", 36, 34, 520, 34, fg=5, bg=13, size=20, bold=True)
    base.label(
        hwnd,
        "这个 demo 先创建 Slider，再创建覆盖同一区域的 GroupBox。修复生效时，滑块仍可见且可拖动。",
        36,
        74,
        720,
        28,
        fg=6,
        bg=13,
    )

    slider = DLL.CreateSlider(hwnd, 116, 196, 540, 48, 0, 100, 35, 5, 0xFF409EFF, 0xFFE4E7ED)
    DLL.SetSliderShowStops(slider, BOOL(True))

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

    status = base.label(hwnd, "拖动滑块验证回调。当前值: 35", 72, 330, 640, 26, fg=4, bg=13)
    base.STATE["status"] = status

    def on_slider(_hwnd: HWND, value: int) -> None:
        base.set_label_text(status, f"Slider 回调已触发，当前值: {value}")

    cb = DLL._SliderCB(on_slider)
    KEEP.append(cb)
    DLL.SetSliderCallback(slider, cb)

    DLL.set_message_loop_main_window(hwnd)
    DLL.run_message_loop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
