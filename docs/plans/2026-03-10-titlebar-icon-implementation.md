# Titlebar Icon Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Restore the small window icon in the custom-drawn title bar, but only when the window already has an icon set via the existing icon APIs.

**Architecture:** Keep the current custom title bar and icon-setting APIs unchanged. Add a tiny helper in `emoji_window.cpp` to resolve the current window icon from `WM_GETICON` / class icon fallbacks, then render that icon inside `DrawWindowTitleBar()` and shift the title text rectangle only when an icon exists.

**Tech Stack:** C++17, Win32 API, Direct2D/DirectWrite, Visual Studio/MSBuild, existing DLL export surface.

---

### Task 1: Add a failing manual reproduction case definition

**Files:**
- Modify: `docs/plans/2026-03-10-titlebar-icon-design.md`
- Reference: `易语言代码/窗口程序集_主题切换示例.e:20-21`

**Step 1: Write the failing test case description**

Add a short “Regression reproduction” section to the design doc that states:
- Create window with `创建Emoji窗口_字节集_扩展`
- Call `设置窗口图标()`
- Expected before fix: taskbar shows icon, title bar does not
- Expected after fix: both taskbar and title bar show icon

**Step 2: Verify the failure case exists before code changes**

Manual check using the existing example:
- Open `易语言代码/窗口程序集_主题切换示例.e`
- Confirm it creates the window with `创建Emoji窗口_字节集_扩展`
- Confirm it calls `设置窗口图标()` immediately after creation

Expected: this file is the repro entry point for the current bug.

**Step 3: Commit**

```bash
git add docs/plans/2026-03-10-titlebar-icon-design.md
git commit -m "docs: add titlebar icon regression reproduction"
```

### Task 2: Add minimal icon-resolution helper

**Files:**
- Modify: `emoji_window/emoji_window.cpp` near the title-bar helper section around `WindowCreateInit` and `GetTitleBarOffset`
- Test: manual verification through `易语言代码/窗口程序集_主题切换示例.e`

**Step 1: Write the failing test intent**

The behavior to support:
- If the window already has an icon set, custom title bar rendering can resolve it.
- If no icon is set, helper returns `nullptr` and nothing is drawn.

Pseudo-test intent:

```cpp
// expected behavior
HICON icon = GetWindowTitleBarIcon(hwnd);
// returns non-null only when icon exists on the window/class
```

**Step 2: Run verification mentally against current code**

Current code has no helper and no title-bar icon lookup.
Expected: FAIL by inspection because title bar code never queries `WM_GETICON` or class icons.

**Step 3: Write minimal implementation**

Add a small static helper in `emoji_window.cpp`:
- `SendMessage(hwnd, WM_GETICON, ICON_SMALL, 0)`
- fallback `SendMessage(hwnd, WM_GETICON, ICON_BIG, 0)`
- fallback `GetClassLongPtr(hwnd, GCLP_HICONSM)`
- fallback `GetClassLongPtr(hwnd, GCLP_HICON)`
- return `nullptr` if none found

Keep it local to `emoji_window.cpp`.

**Step 4: Build to verify compile success**

Run:

```bash
"/c/Program Files/Microsoft Visual Studio/2022/Community/MSBuild/Current/Bin/MSBuild.exe" "t:/易语言源码/API创建窗口/emoji_window_cpp/emoji_window.sln" /p:Configuration=Release /p:Platform=x64
```

Expected: build succeeds with no new compile errors.

**Step 5: Commit**

```bash
git add emoji_window/emoji_window.cpp
git commit -m "fix: add titlebar icon lookup helper"
```

### Task 3: Draw the icon in the custom title bar

**Files:**
- Modify: `emoji_window/emoji_window.cpp:377-516`
- Test: manual verification through `易语言代码/窗口程序集_主题切换示例.e`

**Step 1: Write the failing test intent**

Behavior to support:
- When an icon is available, it appears at the left side of the custom title bar.
- It is vertically centered.
- It does not overlap the title text.

Pseudo-test intent:

```cpp
// expected layout
// icon at left margin, title text starts after icon + spacing
```

**Step 2: Verify current implementation fails this**

Current `DrawWindowTitleBar()` only draws:
- background
- titlebar buttons
- title text

Expected: FAIL by inspection because no icon rendering exists.

**Step 3: Write minimal implementation**

In `DrawWindowTitleBar()`:
- Resolve `HICON` via the new helper
- If icon exists:
  - get small icon size using `GetSystemMetrics(SM_CXSMICON)` and `GetSystemMetrics(SM_CYSMICON)`
  - draw it at left margin around `10px`
  - vertically center within `state->titlebar_height`
- Shift title text left edge from current `10px` to `10 + icon_width + 8`
- If no icon exists, keep left edge at `10px`

Implementation should be minimal and not refactor unrelated title bar code.

**Step 4: Build to verify compile success**

Run:

```bash
"/c/Program Files/Microsoft Visual Studio/2022/Community/MSBuild/Current/Bin/MSBuild.exe" "t:/易语言源码/API创建窗口/emoji_window_cpp/emoji_window.sln" /p:Configuration=Release /p:Platform=x64
```

Expected: build succeeds.

**Step 5: Manual verify the bug is fixed**

Use the existing repro example:
- Run the 易语言 example that uses `创建Emoji窗口_字节集_扩展`
- Confirm title bar now shows the icon
- Confirm taskbar still shows the icon
- Confirm title text does not overlap icon

Expected: PASS.

**Step 6: Commit**

```bash
git add emoji_window/emoji_window.cpp
git commit -m "fix: render window icon in custom titlebar"
```

### Task 4: Verify no regressions in windows without icons

**Files:**
- Reference: any example creating a window without calling `设置窗口图标()`
- Modify: `docs/plans/2026-03-10-titlebar-icon-design.md`

**Step 1: Define the regression check**

Expected behavior:
- Windows without `设置窗口图标()` still render normally
- No blank placeholder is shown
- Title text uses original left margin when no icon exists

**Step 2: Verify manually**

Open and run an example that creates a window without calling `设置窗口图标()`.

Expected: title bar renders normally with no visual placeholder.

**Step 3: Record verification note**

Append a short verification note to the design doc summarizing:
- icon case passes
- no-icon case passes
- taskbar icon unchanged

**Step 4: Commit**

```bash
git add docs/plans/2026-03-10-titlebar-icon-design.md
git commit -m "docs: record titlebar icon verification"
```

### Task 5: Final verification before completion

**Files:**
- Modify: `emoji_window/emoji_window.cpp`
- Modify: `docs/plans/2026-03-10-titlebar-icon-design.md`
- Plan file: `docs/plans/2026-03-10-titlebar-icon-implementation.md`

**Step 1: Run final build verification**

Run:

```bash
"/c/Program Files/Microsoft Visual Studio/2022/Community/MSBuild/Current/Bin/MSBuild.exe" "t:/易语言源码/API创建窗口/emoji_window_cpp/emoji_window.sln" /p:Configuration=Release /p:Platform=x64
```

Expected: `Build succeeded`.

**Step 2: Run final manual checklist**

Manual checklist:
- [ ] `创建Emoji窗口_字节集_扩展` + `设置窗口图标()` shows title bar icon
- [ ] Taskbar icon still displays
- [ ] Title text is aligned and not overlapping
- [ ] No-icon windows show no placeholder
- [ ] Titlebar buttons still work

**Step 3: Commit final implementation state**

```bash
git add emoji_window/emoji_window.cpp docs/plans/2026-03-10-titlebar-icon-design.md docs/plans/2026-03-10-titlebar-icon-implementation.md
git commit -m "fix: restore titlebar icon for custom windows"
```
