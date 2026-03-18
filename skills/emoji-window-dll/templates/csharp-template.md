# C# emoji_window.dll 代码模板

## 模板 1：基础使用模板

```csharp
using System;
using System.Runtime.InteropServices;
using System.Text;

namespace EmojiWindowDemo
{
    class Program
    {
        static EmojiWindowNative.ButtonClickCallback _btnCb;

        static IntPtr hwnd;
        static int labelStatus;
        static int btnGenerate, btnCopy;

        static byte[] U(string s) => EmojiWindowNative.ToUtf8(s);
        static uint ARGB(int a, int r, int g, int b) => EmojiWindowNative.ARGB(a, r, g, b);

        static void ShowStatus(string text)
        {
            byte[] d = U(text);
            EmojiWindowNative.SetLabelText(labelStatus, d, d.Length);
        }

        static int Btn(IntPtr parent, byte[] emoji, string text, int x, int y, int w, int h, uint color)
        {
            byte[] t = U(text);
            return EmojiWindowNative.create_emoji_button_bytes(parent, emoji, emoji.Length, t, t.Length, x, y, w, h, color);
        }

        static void OnButtonClick(int buttonId, IntPtr parentHwnd)
        {
            if (buttonId == btnGenerate)
            {
                ShowStatus("🚀 正在生成...");
                byte[] t = U("💡 提示"), m = U("生成完成！🎉"), ic = U("✅");
                EmojiWindowNative.show_message_box_bytes(hwnd, t, t.Length, m, m.Length, ic, ic.Length);
            }
            else if (buttonId == btnCopy)
            {
                ShowStatus("📋 已复制到剪贴板");
            }
        }

        static void Main(string[] args)
        {
            byte[] f = U("微软雅黑");
            uint BLUE = ARGB(255, 64, 158, 255);
            uint GREEN = ARGB(255, 103, 194, 58);
            uint BLACK = ARGB(255, 0, 0, 0);
            uint TRANS = ARGB(0, 0, 0, 0);

            // 创建窗口
            byte[] title = U("🎨 我的应用 - C# Demo");
            hwnd = EmojiWindowNative.create_window_bytes(title, title.Length, 800, 600);
            if (hwnd == IntPtr.Zero) { Console.WriteLine("创建窗口失败"); return; }

            // 状态标签
            byte[] hint = U("💡 点击按钮查看效果");
            labelStatus = EmojiWindowNative.CreateLabel(
                hwnd, 20, 20, 760, 30,
                hint, hint.Length, BLACK, ARGB(255, 240, 248, 255),
                f, f.Length, 13, 0, 0, 0, 0, 0
            );

            // 按钮
            btnGenerate = Btn(hwnd, new byte[] { 0xf0, 0x9f, 0x9a, 0x80 }, "生成", 20, 60, 120, 40, BLUE);
            btnCopy = Btn(hwnd, new byte[] { 0xf0, 0x9f, 0x93, 0x8b }, "复制", 150, 60, 120, 40, GREEN);

            // 设置回调（必须保存引用防止 GC）
            _btnCb = OnButtonClick;
            EmojiWindowNative.set_button_click_callback(_btnCb);

            // 运行消息循环
            EmojiWindowNative.set_message_loop_main_window(hwnd);
            Console.WriteLine("窗口已创建，进入消息循环...");
            EmojiWindowNative.run_message_loop();
        }
    }
}
```

## 模板 2：委托和回调模板

```csharp
using System;
using System.Runtime.InteropServices;
using System.Text;

namespace EmojiWindowDemo
{
    class Program
    {
        // 必须用 static 字段保存委托引用，防止 GC 回收导致崩溃
        static EmojiWindowNative.ButtonClickCallback _btnCb;
        static EmojiWindowNative.MessageBoxCallback _msgBoxCb;
        static EmojiWindowNative.CheckBoxCallback _checkCb;
        static EmojiWindowNative.ListBoxCallback _listCb;
        static EmojiWindowNative.ComboBoxCallback _comboCb;
        static EmojiWindowNative.DataGridCellCallback _cellClickCb;
        static EmojiWindowNative.DataGridColumnHeaderCallback _colHeaderCb;

        static IntPtr hwnd;
        static byte[] U(string s) => EmojiWindowNative.ToUtf8(s);

        // ===== 按钮点击回调 =====
        static void OnButtonClick(int buttonId, IntPtr parentHwnd)
        {
            Console.WriteLine($"按钮点击: ID={buttonId}");
        }

        // ===== 确认框回调 =====
        static void OnConfirm(int confirmed)
        {
            Console.WriteLine(confirmed != 0 ? "用户确认" : "用户取消");
        }

        // ===== 复选框回调 =====
        static void OnCheckBoxChanged(int checkBoxId, int isChecked)
        {
            Console.WriteLine($"复选框 {checkBoxId}: {(isChecked != 0 ? "选中" : "未选中")}");
        }

        // ===== 列表框选中回调 =====
        static void OnListBoxSelect(int hListBox, int index)
        {
            var (data, len) = EmojiWindowNative.GetItemText2Call(EmojiWindowNative.GetListItemText, hListBox, index);
            string text = len > 0 ? Encoding.UTF8.GetString(data) : "(空)";
            Console.WriteLine($"列表框选中: [{index}] {text}");
        }

        // ===== 组合框选中回调 =====
        static void OnComboSelect(int hComboBox, int index)
        {
            var (data, len) = EmojiWindowNative.GetItemText2Call(EmojiWindowNative.GetComboItemText, hComboBox, index);
            string text = len > 0 ? Encoding.UTF8.GetString(data) : "(空)";
            Console.WriteLine($"组合框选中: [{index}] {text}");
        }

        // ===== 表格单元格点击回调 =====
        static void OnCellClick(int hGrid, int row, int col)
        {
            var (data, len) = EmojiWindowNative.GetCellText2Call(EmojiWindowNative.DataGrid_GetCellText, hGrid, row, col);
            string text = len > 0 ? Encoding.UTF8.GetString(data) : "(空)";
            Console.WriteLine($"单元格点击: [{row},{col}] = {text}");
        }

        // ===== 列头点击回调 =====
        static void OnColHeaderClick(int hGrid, int col)
        {
            Console.WriteLine($"列头点击: 第{col}列");
        }

        static void Main(string[] args)
        {
            byte[] title = U("🎨 回调示例");
            hwnd = EmojiWindowNative.create_window_bytes(title, title.Length, 800, 600);

            // 注册回调（赋值给 static 字段）
            _btnCb = OnButtonClick;
            _msgBoxCb = OnConfirm;
            _checkCb = OnCheckBoxChanged;
            _listCb = OnListBoxSelect;
            _comboCb = OnComboSelect;
            _cellClickCb = OnCellClick;
            _colHeaderCb = OnColHeaderClick;

            EmojiWindowNative.set_button_click_callback(_btnCb);

            // 显示确认框
            byte[] t = U("🤔 确认"), m = U("确定要执行吗？"), ic = U("❓");
            EmojiWindowNative.show_confirm_box_bytes(hwnd, t, t.Length, m, m.Length, ic, ic.Length, _msgBoxCb);

            EmojiWindowNative.set_message_loop_main_window(hwnd);
            EmojiWindowNative.run_message_loop();
        }
    }
}
```

## 模板 3：两次调用辅助方法使用模板

EmojiWindowNative 中提供了 `GetText2Call` 系列辅助方法，封装"两次调用"模式。

```csharp
using System;
using System.Runtime.InteropServices;
using System.Text;

namespace EmojiWindowDemo
{
    class Program
    {
        static byte[] U(string s) => EmojiWindowNative.ToUtf8(s);

        static void Main(string[] args)
        {
            byte[] title = U("🔍 文本获取示例");
            IntPtr hwnd = EmojiWindowNative.create_window_bytes(title, title.Length, 800, 600);

            // 创建按钮
            byte[] emoji = U("📢"), text = U("测试按钮");
            int btnId = EmojiWindowNative.create_emoji_button_bytes(
                hwnd, emoji, emoji.Length, text, text.Length,
                20, 20, 150, 50, EmojiWindowNative.ARGB(255, 64, 158, 255)
            );

            // ===== GetText2Call: 获取按钮文本 =====
            {
                var (data, len) = EmojiWindowNative.GetText2Call(EmojiWindowNative.GetButtonText, btnId);
                string btnText = len > 0 ? Encoding.UTF8.GetString(data) : "(空)";
                Console.WriteLine($"按钮文本: {btnText}");
            }

            // ===== GetText2CallPtr: 获取窗口标题（IntPtr 句柄版本）=====
            {
                var (data, len) = EmojiWindowNative.GetText2CallPtr(EmojiWindowNative.GetWindowTitle, hwnd);
                string winTitle = len > 0 ? Encoding.UTF8.GetString(data) : "(空)";
                Console.WriteLine($"窗口标题: {winTitle}");
            }

            // ===== GetItemText2Call: 获取列表框/组合框项文本 =====
            {
                int listBox = EmojiWindowNative.CreateListBox(hwnd, 20, 80, 300, 150, 0,
                    EmojiWindowNative.ARGB(255, 0, 0, 0), EmojiWindowNative.ARGB(255, 255, 255, 255));
                byte[] item = U("🎨 UI设计");
                EmojiWindowNative.AddListItem(listBox, item, item.Length);

                var (data, len) = EmojiWindowNative.GetItemText2Call(EmojiWindowNative.GetListItemText, listBox, 0);
                string itemText = len > 0 ? Encoding.UTF8.GetString(data) : "(空)";
                Console.WriteLine($"列表项文本: {itemText}");
            }

            // ===== GetCellText2Call: 获取表格单元格文本 =====
            {
                int grid = EmojiWindowNative.CreateDataGridView(hwnd, 20, 250, 700, 200, 0, 1,
                    EmojiWindowNative.ARGB(255, 0, 0, 0), EmojiWindowNative.ARGB(255, 255, 255, 255));
                byte[] h = U("📋 名称");
                EmojiWindowNative.DataGrid_AddTextColumn(grid, h, h.Length, 200);
                int row = EmojiWindowNative.DataGrid_AddRow(grid);
                byte[] cell = U("🎨 UI设计稿");
                EmojiWindowNative.DataGrid_SetCellText(grid, row, 0, cell, cell.Length);

                var (data, len) = EmojiWindowNative.GetCellText2Call(EmojiWindowNative.DataGrid_GetCellText, grid, 0, 0);
                string cellText = len > 0 ? Encoding.UTF8.GetString(data) : "(空)";
                Console.WriteLine($"单元格文本: {cellText}");
            }

            // ===== GetComboText2Call: 获取组合框编辑框文本 =====
            {
                byte[] f = U("微软雅黑");
                int combo = EmojiWindowNative.CreateComboBox(hwnd, 350, 80, 200, 30, 0,
                    EmojiWindowNative.ARGB(255, 0, 0, 0), EmojiWindowNative.ARGB(255, 255, 255, 255),
                    28, f, f.Length, 12, 0, 0, 0);
                byte[] ct = U("✏️ 自定义文本");
                EmojiWindowNative.SetComboBoxText(combo, ct, ct.Length);

                var (data, len) = EmojiWindowNative.GetComboText2Call(EmojiWindowNative.GetComboBoxText, combo);
                string comboText = len > 0 ? Encoding.UTF8.GetString(data) : "(空)";
                Console.WriteLine($"组合框文本: {comboText}");
            }

            EmojiWindowNative.set_message_loop_main_window(hwnd);
            EmojiWindowNative.run_message_loop();
        }
    }
}
```

## 模板 4：多控件完整应用模板

```csharp
using System;
using System.Runtime.InteropServices;
using System.Text;

namespace EmojiWindowDemo
{
    class Program
    {
        static EmojiWindowNative.ButtonClickCallback _btnCb;
        static EmojiWindowNative.ListBoxCallback _listCb;
        static EmojiWindowNative.ComboBoxCallback _comboCb;
        static EmojiWindowNative.DataGridCellCallback _cellClickCb;
        static EmojiWindowNative.MessageBoxCallback _msgBoxCb;

        static IntPtr hwnd;
        static int labelStatus;
        static int listBox, comboBox, grid;
        static int btnAdd, btnDel, btnRead, btnClear, btnMsgInfo, btnMsgConfirm;

        static byte[] U(string s) => EmojiWindowNative.ToUtf8(s);
        static uint ARGB(int a, int r, int g, int b) => EmojiWindowNative.ARGB(a, r, g, b);

        static void ShowStatus(string text)
        {
            byte[] d = U(text);
            EmojiWindowNative.SetLabelText(labelStatus, d, d.Length);
        }

        static int Btn(IntPtr p, byte[] emoji, string text, int x, int y, int w, int h, uint color)
        {
            byte[] t = U(text);
            return EmojiWindowNative.create_emoji_button_bytes(p, emoji, emoji.Length, t, t.Length, x, y, w, h, color);
        }

        static void OnButtonClick(int buttonId, IntPtr parentHwnd)
        {
            if (buttonId == btnAdd)
            {
                int count = EmojiWindowNative.GetListItemCount(listBox);
                string[] emojis = { "🎨", "🔧", "📱", "🧪", "📦", "🎯" };
                byte[] t = U($"{emojis[count % emojis.Length]} 项目-{count + 1}");
                EmojiWindowNative.AddListItem(listBox, t, t.Length);
                ShowStatus($"✅ 已添加列表项 #{count + 1}");
            }
            else if (buttonId == btnDel)
            {
                int sel = EmojiWindowNative.GetSelectedIndex(listBox);
                if (sel >= 0) { EmojiWindowNative.RemoveListItem(listBox, sel); ShowStatus($"🗑️ 已删除 [{sel}]"); }
                else ShowStatus("⚠️ 请先选中一项");
            }
            else if (buttonId == btnRead)
            {
                int sel = EmojiWindowNative.GetSelectedIndex(listBox);
                if (sel >= 0)
                {
                    var (data, len) = EmojiWindowNative.GetItemText2Call(EmojiWindowNative.GetListItemText, listBox, sel);
                    ShowStatus($"📖 [{sel}] = {Encoding.UTF8.GetString(data)}");
                }
                else ShowStatus("⚠️ 未选中项");
            }
            else if (buttonId == btnClear)
            {
                EmojiWindowNative.ClearListBox(listBox);
                ShowStatus("🧹 已清空");
            }
            else if (buttonId == btnMsgInfo)
            {
                byte[] t = U("💡 提示"), m = U("这是信息框\n支持emoji 🎉"), ic = U("ℹ️");
                EmojiWindowNative.show_message_box_bytes(hwnd, t, t.Length, m, m.Length, ic, ic.Length);
            }
            else if (buttonId == btnMsgConfirm)
            {
                byte[] t = U("🤔 确认"), m = U("确定要执行吗？\n此操作不可撤销 ⚠️"), ic = U("❓");
                EmojiWindowNative.show_confirm_box_bytes(hwnd, t, t.Length, m, m.Length, ic, ic.Length, _msgBoxCb);
            }
        }

        static void OnListSelect(int hListBox, int index)
        {
            var (data, len) = EmojiWindowNative.GetItemText2Call(EmojiWindowNative.GetListItemText, hListBox, index);
            string text = len > 0 ? Encoding.UTF8.GetString(data) : "(空)";
            ShowStatus($"📋 选中: [{index}] {text}");
        }

        static void OnComboSelect(int hComboBox, int index)
        {
            var (data, len) = EmojiWindowNative.GetItemText2Call(EmojiWindowNative.GetComboItemText, hComboBox, index);
            string text = len > 0 ? Encoding.UTF8.GetString(data) : "(空)";
            ShowStatus($"🔽 组合框: [{index}] {text}");
        }

        static void OnCellClick(int hGrid, int row, int col)
        {
            var (data, len) = EmojiWindowNative.GetCellText2Call(EmojiWindowNative.DataGrid_GetCellText, hGrid, row, col);
            string text = len > 0 ? Encoding.UTF8.GetString(data) : "(空)";
            ShowStatus($"📊 [{row},{col}] = {text}");
        }

        static void OnConfirm(int confirmed)
        {
            ShowStatus(confirmed != 0 ? "✅ 已确认" : "❌ 已取消");
        }

        static void Main(string[] args)
        {
            byte[] f = U("微软雅黑");
            uint WHITE = ARGB(255, 255, 255, 255), BLACK = ARGB(255, 0, 0, 0);
            uint BLUE = ARGB(255, 64, 158, 255), GREEN = ARGB(255, 103, 194, 58);
            uint RED = ARGB(255, 245, 108, 108), ORANGE = ARGB(255, 230, 162, 60);
            uint GRAY = ARGB(255, 144, 147, 153), TRANS = ARGB(0, 0, 0, 0);

            // 创建窗口
            byte[] title = U("📊📋🔽💬 综合示例 - C# x86");
            hwnd = EmojiWindowNative.create_window_bytes(title, title.Length, 1000, 700);
            if (hwnd == IntPtr.Zero) { Console.WriteLine("创建窗口失败"); return; }

            // 状态标签
            byte[] hint = U("💡 点击按钮操作各控件");
            labelStatus = EmojiWindowNative.CreateLabel(hwnd, 10, 10, 980, 30, hint, hint.Length, BLACK, ARGB(255, 240, 248, 255), f, f.Length, 13, 0, 0, 0, 0, 0);

            // ===== 列表框 =====
            byte[] grpTitle = U("📋 列表框");
            EmojiWindowNative.CreateGroupBox(hwnd, 10, 50, 350, 300, grpTitle, grpTitle.Length, ARGB(255, 100, 149, 237), ARGB(255, 250, 250, 250), f, f.Length, 13, 1, 0, 0);

            listBox = EmojiWindowNative.CreateListBox(hwnd, 20, 80, 330, 180, 0, BLACK, WHITE);
            string[] items = { "🎨 UI设计", "🔧 后端开发", "📱 移动端", "🧪 测试", "📦 部署" };
            foreach (var item in items) { byte[] t = U(item); EmojiWindowNative.AddListItem(listBox, t, t.Length); }
            EmojiWindowNative.SetSelectedIndex(listBox, 0);

            btnAdd = Btn(hwnd, new byte[] { 0xe2, 0x9e, 0x95 }, "添加", 20, 270, 80, 32, BLUE);
            btnDel = Btn(hwnd, new byte[] { 0xf0, 0x9f, 0x97, 0x91, 0xef, 0xb8, 0x8f }, "删除", 105, 270, 80, 32, RED);
            btnRead = Btn(hwnd, new byte[] { 0xf0, 0x9f, 0x93, 0x96 }, "读取", 190, 270, 80, 32, GREEN);
            btnClear = Btn(hwnd, new byte[] { 0xf0, 0x9f, 0xa7, 0xb9 }, "清空", 275, 270, 70, 32, GRAY);

            // ===== 组合框 =====
            byte[] grpCombo = U("🔽 组合框");
            EmojiWindowNative.CreateGroupBox(hwnd, 370, 50, 620, 120, grpCombo, grpCombo.Length, ORANGE, ARGB(255, 250, 250, 250), f, f.Length, 13, 1, 0, 0);

            comboBox = EmojiWindowNative.CreateComboBox(hwnd, 380, 80, 300, 30, 1, BLACK, WHITE, 28, f, f.Length, 12, 0, 0, 0);
            string[] comboItems = { "🎨 设计模式", "🔧 开发模式", "🧪 测试模式", "🚀 发布模式" };
            foreach (var item in comboItems) { byte[] t = U(item); EmojiWindowNative.AddComboItem(comboBox, t, t.Length); }
            EmojiWindowNative.SetComboSelectedIndex(comboBox, 0);

            // ===== 表格 =====
            byte[] grpGrid = U("📊 DataGridView");
            EmojiWindowNative.CreateGroupBox(hwnd, 370, 180, 620, 350, grpGrid, grpGrid.Length, BLUE, ARGB(255, 250, 250, 250), f, f.Length, 13, 1, 0, 0);

            grid = EmojiWindowNative.CreateDataGridView(hwnd, 380, 210, 600, 250, 0, 1, BLACK, WHITE);
            byte[][] cols = { U("📋 名称"), U("📝 描述"), U("🏷️ 状态") };
            int[] widths = { 180, 220, 100 };
            for (int i = 0; i < cols.Length; i++) EmojiWindowNative.DataGrid_AddTextColumn(grid, cols[i], cols[i].Length, widths[i]);
            byte[] chkH = U("✅ 选择"); EmojiWindowNative.DataGrid_AddCheckBoxColumn(grid, chkH, chkH.Length, 70);
            byte[] btnH = U("🔧 操作"); EmojiWindowNative.DataGrid_AddButtonColumn(grid, btnH, btnH.Length, 90);

            EmojiWindowNative.DataGrid_SetDefaultRowHeight(grid, 34);
            EmojiWindowNative.DataGrid_SetHeaderHeight(grid, 38);
            EmojiWindowNative.DataGrid_SetShowGridLines(grid, 1);
            EmojiWindowNative.DataGrid_SetFreezeHeader(grid, 1);
            EmojiWindowNative.DataGrid_SetSelectionMode(grid, 1);

            string[,] data = {
                { "🎨 UI设计稿", "📐 完成首页", "✅ 完成" },
                { "🔧 后端API", "🌐 用户认证", "⏳ 进行中" },
                { "📱 移动适配", "📲 响应布局", "❌ 未开始" },
            };
            for (int r = 0; r < data.GetLength(0); r++)
            {
                int row = EmojiWindowNative.DataGrid_AddRow(grid);
                for (int c = 0; c < 3; c++) { byte[] t = U(data[r, c]); EmojiWindowNative.DataGrid_SetCellText(grid, row, c, t, t.Length); }
                byte[] bt = U("📋 详情"); EmojiWindowNative.DataGrid_SetCellText(grid, row, 4, bt, bt.Length);
            }

            // ===== 信息框按钮 =====
            byte[] grpMsg = U("💬 信息框");
            EmojiWindowNative.CreateGroupBox(hwnd, 10, 360, 350, 120, grpMsg, grpMsg.Length, GREEN, ARGB(255, 250, 250, 250), f, f.Length, 13, 1, 0, 0);
            btnMsgInfo = Btn(hwnd, new byte[] { 0xf0, 0x9f, 0x92, 0xa1 }, "信息", 20, 400, 100, 35, BLUE);
            btnMsgConfirm = Btn(hwnd, new byte[] { 0xf0, 0x9f, 0xa4, 0x94 }, "确认框", 130, 400, 100, 35, GREEN);

            // 注册回调
            _btnCb = OnButtonClick;
            _listCb = OnListSelect;
            _comboCb = OnComboSelect;
            _cellClickCb = OnCellClick;
            _msgBoxCb = OnConfirm;

            EmojiWindowNative.set_button_click_callback(_btnCb);
            EmojiWindowNative.SetListBoxCallback(listBox, _listCb);
            EmojiWindowNative.SetComboBoxCallback(comboBox, _comboCb);
            EmojiWindowNative.DataGrid_SetCellClickCallback(grid, _cellClickCb);

            // 运行
            EmojiWindowNative.set_message_loop_main_window(hwnd);
            Console.WriteLine("综合示例窗口已创建");
            EmojiWindowNative.run_message_loop();
        }
    }
}
```

## ARGB 颜色参考

```csharp
// Element UI 配色
uint PRIMARY = EmojiWindowNative.ARGB(255, 64, 158, 255);   // #409EFF 蓝
uint SUCCESS = EmojiWindowNative.ARGB(255, 103, 194, 58);   // #67C23A 绿
uint WARNING = EmojiWindowNative.ARGB(255, 230, 162, 60);   // #E6A23C 橙
uint DANGER  = EmojiWindowNative.ARGB(255, 245, 108, 108);  // #F56C6C 红
uint INFO    = EmojiWindowNative.ARGB(255, 144, 147, 153);  // #909399 灰

uint BLACK = EmojiWindowNative.ARGB(255, 0, 0, 0);
uint WHITE = EmojiWindowNative.ARGB(255, 255, 255, 255);
uint TRANS = EmojiWindowNative.ARGB(0, 0, 0, 0);
```

## 常用 Emoji UTF-8 字节数组

```csharp
// 当 C# 字符串在 DLL 中无法正确显示时，使用原始 UTF-8 字节
byte[] emoji_rocket   = new byte[] { 0xf0, 0x9f, 0x9a, 0x80 };  // 🚀
byte[] emoji_star     = new byte[] { 0xe2, 0xad, 0x90 };         // ⭐
byte[] emoji_thumb    = new byte[] { 0xf0, 0x9f, 0x91, 0x8d };   // 👍
byte[] emoji_heart    = new byte[] { 0xe2, 0x9d, 0xa4, 0xef, 0xb8, 0x8f }; // ❤️
byte[] emoji_fire     = new byte[] { 0xf0, 0x9f, 0x94, 0xa5 };   // 🔥
byte[] emoji_smile    = new byte[] { 0xf0, 0x9f, 0x98, 0x80 };   // 😀
byte[] emoji_check    = new byte[] { 0xe2, 0x9c, 0x85 };         // ✅
byte[] emoji_cross    = new byte[] { 0xe2, 0x9d, 0x8c };         // ❌
byte[] emoji_warning  = new byte[] { 0xe2, 0x9a, 0xa0, 0xef, 0xb8, 0x8f }; // ⚠️
byte[] emoji_info     = new byte[] { 0xe2, 0x84, 0xb9, 0xef, 0xb8, 0x8f }; // ℹ️
byte[] emoji_gear     = new byte[] { 0xe2, 0x9a, 0x99, 0xef, 0xb8, 0x8f }; // ⚙️
byte[] emoji_palette  = new byte[] { 0xf0, 0x9f, 0x8e, 0xa8 };   // 🎨
byte[] emoji_wrench   = new byte[] { 0xf0, 0x9f, 0x94, 0xa7 };   // 🔧
byte[] emoji_plus     = new byte[] { 0xe2, 0x9e, 0x95 };         // ➕
byte[] emoji_trash    = new byte[] { 0xf0, 0x9f, 0x97, 0x91, 0xef, 0xb8, 0x8f }; // 🗑️
byte[] emoji_book     = new byte[] { 0xf0, 0x9f, 0x93, 0x96 };   // 📖
byte[] emoji_broom    = new byte[] { 0xf0, 0x9f, 0xa7, 0xb9 };   // 🧹
byte[] emoji_bulb     = new byte[] { 0xf0, 0x9f, 0x92, 0xa1 };   // 💡
byte[] emoji_clipboard = new byte[] { 0xf0, 0x9f, 0x93, 0x8b };  // 📋
byte[] emoji_question = new byte[] { 0xf0, 0x9f, 0xa4, 0x94 };   // 🤔
```
