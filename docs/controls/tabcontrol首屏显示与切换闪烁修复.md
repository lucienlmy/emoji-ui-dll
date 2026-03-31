# TabControl 首屏显示与切换闪烁修复

## 问题现象

在 `TabControl` 场景下，曾经同时出现两类问题：

1. 初次打开窗口时，当前 `Tab` 页里的部分组件没有立刻显示，界面出现大块空白。
2. 切换 `Tab` 标签时，整页组件一起闪烁，尤其是按钮、分组框、复选框、表格等控件会明显重刷。

这两个问题看起来像是同一个现象，实际上根因相关但不完全相同。

## 根因分析

### 1. Tab 页内容窗口是独立 HWND

当前 `TabControl` 的每个页内容不是简单的数据容器，而是独立的内容窗口：

- `TabControl` 本身是一个自绘头部窗口
- 每个页内容对应一个 `TabContentD2DClass` 窗口
- 页内既有真实子控件 `HWND`
- 也有部分由父窗口绘制的元素

这意味着切换标签页时，实际发生的是一组窗口的显示、隐藏、移动和重绘。

### 2. 首屏不显示的根因

首屏不显示，本质上是“当前页已经显示出来了，但页内容窗口和它的子树没有完成一次稳定的首绘”。

早期问题主要集中在两点：

- 初始选中页没有在所有组件创建完成后再做一次统一布局与可见页刷新。
- 过度压制重绘后，页窗口虽然被 `ShowWindow` 出来了，但没有完成当前页的正式绘制。

### 3. 切换时闪烁的根因

切换闪烁的直接原因是：同一轮切换中，当前页被重复同步重绘了多次。

典型链路是：

1. `UpdateTabLayout(...)` 中批量 `ShowWindow/HideWindow`
2. 页窗口收到 `WM_SHOWWINDOW`
3. 页窗口又收到 `WM_EW_TABPAGE_VISIBLE`
4. `ApplySelectTab(...)` 和页窗口逻辑继续调用 `RedrawWindow(... RDW_ALLCHILDREN | RDW_UPDATENOW ...)`

结果就是：

- 页容器自己重绘
- 所有子控件也被同步强制重绘
- 同一页在一次切换里被刷多遍

肉眼看到的就是整页组件一起闪。

## 错误做法

这次修复过程中，验证过几种“看起来能减闪烁，但其实会引入新问题”的方案：

### 1. 直接把所有同步重绘都压掉

做法：

- 把 `WM_SHOWWINDOW`
- `WM_EW_TABPAGE_VISIBLE`
- `ApplySelectTab(...)`
- `UpdateTabLayout(...)`

里的强制刷新全部改成 `InvalidateRect(...)` 或 `RDW_NOCHILDREN`

问题：

- 首屏组件容易不显示
- 当前页可能要等鼠标移动、窗口遮挡/恢复后才补画

这就是“有一版切换不闪，但首屏不正常”的根因。

### 2. 用 `WS_EX_COMPOSITED` 硬压闪烁

这个方向也不适合当前结构。

问题：

- 会带来黑块、延迟显示、层级异常
- 对嵌套 `TabControl` 和 D2D 内容窗口不稳定

## 最终解决方案

最终方案不是单纯“多重绘”或“少重绘”，而是把切换流程改成：

### 1. 首屏阶段保证当前页做一次完整布局和显示

在 Python 示例中，所有 `Tab` 和页内控件创建完成后，主动执行：

- `UpdateTabControlLayout(tab)`
- 嵌套 `TabControl` 也执行一次 `UpdateTabControlLayout(...)`
- 显式 `SelectTab(...)` 到目标初始页

这样可以保证：

- 当前页已经被定位到正确区域
- 当前页内容窗口完成首绘
- 嵌套页不会停留在“逻辑选中但视觉没刷出来”的状态

### 2. Tab 切换时使用批处理布局

在 `UpdateTabLayout(...)` 中：

- 用 `BeginDeferWindowPos / DeferWindowPos / EndDeferWindowPos`
- 一次性完成所有页窗口的显示、隐藏和位置更新
- 避免逐个窗口即时刷新

这样可以减少切换过程中的中间态暴露。

### 3. 批处理期间抑制页窗口的重复重绘

新增了 `TabControlState::layoutBatchInProgress` 标志。

作用：

- `UpdateTabLayout(...)` 批量切换页窗口前先置 `true`
- 批量切换完成后再置回 `false`
- 页窗口在 `WM_SHOWWINDOW` 中如果发现当前处于批处理阶段，就不立刻做整页同步重绘

这样避免了：

- `ShowWindow`
- `WM_SHOWWINDOW`
- 页树刷新

三条路径在同一轮切换里互相叠加。

### 4. 切换完成后，只同步重绘当前页容器本身

当前页切换完成后：

- 页容器自身执行一次正式重绘
- 不再对整棵子控件树使用 `RDW_ALLCHILDREN | RDW_UPDATENOW` 强制连刷

### 5. 子控件改为单独失效，而不是同步整页强刷

新增了一个递归失效逻辑，用于对可见子树逐个做无擦背景的失效标记：

- 只标记需要重绘
- 不在同一帧强迫所有子控件同步 `UpdateNow`

这样做的效果是：

- 当前页背景和父绘制元素会立刻正确出现
- 子控件会通过正常消息循环补画
- 不会看到整页控件一起“白一下”

### 6. 页内容窗口增加 `WS_CLIPCHILDREN`

页内容窗口创建和接管现有内容窗口时，统一补上：

- `WS_CLIPSIBLINGS`
- `WS_CLIPCHILDREN`

这样父页窗口在绘制自己的背景时，不会去覆盖子控件区域，进一步减少闪烁。

## 关键修改点

主要修改文件：

- `emoji_window/emoji_window.cpp`
- `emoji_window/emoji_window.h`
- `examples/Python/demo_all_components_tabs.py`

关键位置：

### `emoji_window/emoji_window.h`

在 `TabControlState` 中增加：

```cpp
bool layoutBatchInProgress;
```

用于标记当前是否处于页切换批处理阶段。

### `emoji_window/emoji_window.cpp`

涉及的核心函数：

- `UpdateTabLayout(...)`
- `ApplySelectTab(...)`
- `RefreshVisibleTabWindowTree(...)`
- `TabContentWindowProc(...)`
- `CreateTabControl(...)`
- `AddTabItem(...)`

核心思路：

1. 切换页时先批量布局
2. 批处理期间抑制 `WM_SHOWWINDOW` 的重复刷新
3. 批处理结束后只正式刷新当前页
4. 子控件采用递归失效，不再整页同步强刷

### `examples/Python/demo_all_components_tabs.py`

示例代码负责保证“首屏初始页真的被选中并布局完成”。

同时该示例还修复了一个测试阶段问题：

- Windows 控制台默认 `gbk`
- `print` emoji 状态文本时可能触发 `UnicodeEncodeError`

因此脚本启动时对 `stdout/stderr` 做了 `utf-8` 容错配置，避免测试窗口刚打开就退出，影响对 GUI 的判断。

## 方案总结

这次问题的正确解决思路是：

- 不要靠“疯狂重绘”解决首屏空白
- 也不要靠“全面禁掉重绘”解决切换闪烁
- 而是把 `Tab` 切换变成一笔完整事务：
  - 批量切换可见页
  - 抑制切换中间态重绘
  - 切换完成后只刷新当前页
  - 子控件用正常失效链路补画

## 适用范围

该方案适用于以下场景：

- `TabControl` 页内容是独立 `HWND`
- 页内存在较多真实子控件
- 同时混合父窗口绘制元素和子控件窗口
- 存在嵌套 `TabControl`
- 使用 D2D 自绘页容器

## 验证结果

修复后验证结果：

- 初次打开窗口时，当前页组件完整显示
- 切换主 `TabControl` 时组件不再整页闪烁
- 切换嵌套 `TabControl` 时也不再出现明显整页闪烁
- 保留了当前页正常刷新能力，没有再退化成“必须鼠标移动后才显示”

## 后续维护建议

后续如果继续扩展 `TabControl`，建议遵守下面几条：

1. 不要在 `WM_SHOWWINDOW`、`WM_SIZE`、切换回调里同时对同一页做多次 `RedrawWindow(...ALLCHILDREN...)`。
2. 优先把页切换当作一次批处理事务来做。
3. 父页窗口自己绘制时，尽量加 `WS_CLIPCHILDREN`，避免覆盖真实子控件区域。
4. 如果新增嵌套控件树，优先走“失效标记”而不是“同步整树强刷”。
5. 首屏初始化阶段，要在所有页和控件创建完成后，再显式做一次当前页布局和选中。
