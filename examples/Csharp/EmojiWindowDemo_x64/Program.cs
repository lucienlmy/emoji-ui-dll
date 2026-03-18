using System;
using System.Runtime.InteropServices;
using System.Text;

namespace EmojiWindowDemo
{
    class Program
    {
        // 防止 GC 回收
        static EmojiWindowNative.ButtonClickCallback _btnCb;
        static EmojiWindowNative.ListBoxCallback _listCb;
        static EmojiWindowNative.ComboBoxCallback _comboCb;
        static EmojiWindowNative.DataGridCellCallback _cellClickCb, _cellDblClickCb, _selChangedCb, _cellValueCb;
        static EmojiWindowNative.DataGridColumnHeaderCallback _colHeaderCb;
        static EmojiWindowNative.MessageBoxCallback _msgBoxCb;

        static IntPtr hwnd;
        static int labelStatus;

        // 列表框
        static int listBox;
        static int btnListAdd, btnListDel, btnListRead, btnListClear;

        // 组合框
        static int comboReadOnly, comboEditable;
        static int btnComboRead, btnComboSet, btnComboGetText;

        // 表格
        static int grid;
        static int btnGridAdd, btnGridDel, btnGridRead, btnGridSort, btnGridClear;
        static int sortDir = 1;

        // 信息框
        static int btnMsgInfo, btnMsgWarn, btnMsgError, btnMsgConfirm;

        static Random rng = new Random();
        static byte[] U(string s) => EmojiWindowNative.ToUtf8(s);
        static uint ARGB(int a, int r, int g, int b) => EmojiWindowNative.ARGB(a, r, g, b);

        static void ShowStatus(string text)
        {
            byte[] d = U(text);
            EmojiWindowNative.SetLabelText(labelStatus, d, d.Length);
        }

        static int Btn(IntPtr p, byte[] emoji, string text, int x, int y, int bw, int bh, uint color)
        {
            byte[] t = U(text);
            return EmojiWindowNative.create_emoji_button_bytes(p, emoji, emoji.Length, t, t.Length, x, y, bw, bh, color);
        }

        // ===== 回调 =====
        static void OnListBoxSelect(int hListBox, int index)
        {
            var (data, len) = EmojiWindowNative.GetItemText2Call(EmojiWindowNative.GetListItemText, hListBox, index);
            string text = len > 0 ? Encoding.UTF8.GetString(data) : "(空)";
            ShowStatus($"📋 列表框选中: [{index}] {text}");
            Console.WriteLine($"列表框选中: index={index}, text={text}");
        }

        static void OnComboSelect(int hComboBox, int index)
        {
            var (data, len) = EmojiWindowNative.GetItemText2Call(EmojiWindowNative.GetComboItemText, hComboBox, index);
            string text = len > 0 ? Encoding.UTF8.GetString(data) : "(空)";
            ShowStatus($"🔽 组合框选中: [{index}] {text}");
            Console.WriteLine($"组合框选中: index={index}, text={text}");
        }

        static void OnCellClick(int hGrid, int row, int col)
        {
            var (data, len) = EmojiWindowNative.GetCellText2Call(EmojiWindowNative.DataGrid_GetCellText, hGrid, row, col);
            string text = len > 0 ? Encoding.UTF8.GetString(data) : "(空)";
            ShowStatus($"📊 单元格点击: [{row},{col}] = {text}");
        }

        static void OnCellDblClick(int hGrid, int row, int col)
        {
            ShowStatus($"✏️ 双击编辑: [{row},{col}]");
        }

        static void OnSelChanged(int hGrid, int row, int col)
        {
            Console.WriteLine($"选择改变: row={row}, col={col}");
        }

        static void OnColHeaderClick(int hGrid, int col)
        {
            ShowStatus($"🔽 列头点击: 第{col}列");
        }

        static void OnCellValueChanged(int hGrid, int row, int col)
        {
            Console.WriteLine($"值改变: row={row}, col={col}");
        }

        static void OnConfirm(int confirmed)
        {
            ShowStatus(confirmed != 0 ? "✅ 用户点击了确认" : "❌ 用户点击了取消");
            Console.WriteLine($"确认框结果: {confirmed}");
        }

        static void OnButtonClick(int buttonId, IntPtr parentHwnd)
        {
            // 列表框操作
            if (buttonId == btnListAdd)
            {
                int count = EmojiWindowNative.GetListItemCount(listBox);
                string[] emojis = {"🎨","🔧","📱","🧪","📦","🎯","🚀","💡"};
                string emoji = emojis[count % emojis.Length];
                byte[] t = U($"{emoji} 新项目-{count + 1}");
                EmojiWindowNative.AddListItem(listBox, t, t.Length);
                ShowStatus($"✅ 已添加列表项 #{count + 1}");
            }
            else if (buttonId == btnListDel)
            {
                int sel = EmojiWindowNative.GetSelectedIndex(listBox);
                if (sel >= 0) { EmojiWindowNative.RemoveListItem(listBox, sel); ShowStatus($"🗑️ 已删除列表项 [{sel}]"); }
                else ShowStatus("⚠️ 请先选中一项再删除");
            }
            else if (buttonId == btnListRead)
            {
                int sel = EmojiWindowNative.GetSelectedIndex(listBox);
                int count = EmojiWindowNative.GetListItemCount(listBox);
                if (sel >= 0)
                {
                    var (data, len) = EmojiWindowNative.GetItemText2Call(EmojiWindowNative.GetListItemText, listBox, sel);
                    ShowStatus($"📖 [{sel}] = {Encoding.UTF8.GetString(data)} (共{count}项)");
                }
                else ShowStatus($"📖 未选中任何项 (共{count}项)");
            }
            else if (buttonId == btnListClear)
            {
                EmojiWindowNative.ClearListBox(listBox);
                ShowStatus("🧹 已清空列表框");
            }
            // 组合框操作
            else if (buttonId == btnComboRead)
            {
                int idx = EmojiWindowNative.GetComboSelectedIndex(comboReadOnly);
                int count = EmojiWindowNative.GetComboItemCount(comboReadOnly);
                if (idx >= 0)
                {
                    var (data, len) = EmojiWindowNative.GetItemText2Call(EmojiWindowNative.GetComboItemText, comboReadOnly, idx);
                    ShowStatus($"📖 只读组合框: [{idx}] = {Encoding.UTF8.GetString(data)} (共{count}项)");
                }
                else ShowStatus($"📖 只读组合框未选中 (共{count}项)");
            }
            else if (buttonId == btnComboSet)
            {
                byte[] t = U($"✏️ 自定义文本-{rng.Next(1, 100)}");
                EmojiWindowNative.SetComboBoxText(comboEditable, t, t.Length);
                ShowStatus("✏️ 已设置可编辑组合框文本");
            }
            else if (buttonId == btnComboGetText)
            {
                var (data, len) = EmojiWindowNative.GetComboText2Call(EmojiWindowNative.GetComboBoxText, comboEditable);
                string text = len > 0 ? Encoding.UTF8.GetString(data) : "(空)";
                ShowStatus($"📖 可编辑组合框文本: {text}");
            }
            // 表格操作
            else if (buttonId == btnGridAdd)
            {
                int rowCount = EmojiWindowNative.DataGrid_GetRowCount(grid);
                int row = EmojiWindowNative.DataGrid_AddRow(grid);
                string[] items = { $"🆕 项目-{rowCount + 1}", $"📝 描述-{rowCount + 1}", "⏳ 待处理" };
                for (int i = 0; i < items.Length; i++) { byte[] t = U(items[i]); EmojiWindowNative.DataGrid_SetCellText(grid, row, i, t, t.Length); }
                byte[] btnTxt = U("📋 详情"); EmojiWindowNative.DataGrid_SetCellText(grid, row, 4, btnTxt, btnTxt.Length);
                ShowStatus($"✅ 已添加第 {rowCount + 1} 行");
            }
            else if (buttonId == btnGridDel)
            {
                int sel = EmojiWindowNative.DataGrid_GetSelectedRow(grid);
                if (sel >= 0) { EmojiWindowNative.DataGrid_RemoveRow(grid, sel); ShowStatus($"🗑️ 已删除第 {sel} 行"); }
                else ShowStatus("⚠️ 请先选中一行再删除");
            }
            else if (buttonId == btnGridRead)
            {
                int selR = EmojiWindowNative.DataGrid_GetSelectedRow(grid);
                int selC = EmojiWindowNative.DataGrid_GetSelectedCol(grid);
                if (selR >= 0 && selC >= 0)
                {
                    var (data, len) = EmojiWindowNative.GetCellText2Call(EmojiWindowNative.DataGrid_GetCellText, grid, selR, selC);
                    string text = len > 0 ? Encoding.UTF8.GetString(data) : "(空)";
                    ShowStatus($"📖 [{selR},{selC}] = {text}");
                }
                else ShowStatus("⚠️ 请先选中一个单元格");
            }
            else if (buttonId == btnGridSort)
            {
                EmojiWindowNative.DataGrid_SortByColumn(grid, 0, sortDir);
                string d = sortDir == 1 ? "升序 ⬆️" : "降序 ⬇️";
                ShowStatus($"🔄 按第0列{d}排序");
                sortDir = sortDir == 1 ? 2 : 1;
            }
            else if (buttonId == btnGridClear)
            {
                EmojiWindowNative.DataGrid_ClearRows(grid);
                ShowStatus("🧹 已清空所有行");
            }
            // 信息框
            else if (buttonId == btnMsgInfo)
            {
                byte[] t = U("💡 提示"), m = U("这是一个信息提示框\n支持emoji和中文 🎉"), ic = U("ℹ️");
                EmojiWindowNative.show_message_box_bytes(hwnd, t, t.Length, m, m.Length, ic, ic.Length);
            }
            else if (buttonId == btnMsgWarn)
            {
                byte[] t = U("⚠️ 警告"), m = U("这是一个警告框\n请注意操作安全 🔒"), ic = U("⚠️");
                EmojiWindowNative.show_message_box_bytes(hwnd, t, t.Length, m, m.Length, ic, ic.Length);
            }
            else if (buttonId == btnMsgError)
            {
                byte[] t = U("❌ 错误"), m = U("这是一个错误提示框\n操作失败 😢"), ic = U("❌");
                EmojiWindowNative.show_message_box_bytes(hwnd, t, t.Length, m, m.Length, ic, ic.Length);
            }
            else if (buttonId == btnMsgConfirm)
            {
                byte[] t = U("🤔 确认"), m = U("确定要执行此操作吗？\n此操作不可撤销 ⚠️"), ic = U("❓");
                EmojiWindowNative.show_confirm_box_bytes(hwnd, t, t.Length, m, m.Length, ic, ic.Length, _msgBoxCb);
            }
        }

        static void Main(string[] args)
        {
            byte[] f = U("微软雅黑");
            uint WHITE = ARGB(255,255,255,255), BLACK = ARGB(255,0,0,0);
            uint BLUE = ARGB(255,64,158,255), GREEN = ARGB(255,103,194,58);
            uint RED = ARGB(255,245,108,108), ORANGE = ARGB(255,230,162,60);
            uint GRAY = ARGB(255,144,147,153), TRANS = ARGB(0,0,0,0);

            // 创建主窗口
            byte[] title = U("📊📋🔽💬 四控件综合示例 - C# x64");
            hwnd = EmojiWindowNative.create_window_bytes(title, title.Length, 1100, 750);
            if (hwnd == IntPtr.Zero) { Console.WriteLine("创建窗口失败"); return; }

            // 状态标签
            byte[] hint = U("💡 点击按钮操作各控件，查看属性和回调效果");
            labelStatus = EmojiWindowNative.CreateLabel(hwnd, 10, 10, 1080, 35, hint, hint.Length, BLACK, ARGB(255,240,248,255), f, f.Length, 13, 0, 0, 0, 0, 0);

            // ===== 左侧：列表框区域 =====
            byte[] grpListTitle = U("📋 列表框示例");
            IntPtr grpList = EmojiWindowNative.CreateGroupBox(hwnd, 10, 55, 350, 320, grpListTitle, grpListTitle.Length, ARGB(255,100,149,237), ARGB(255,250,250,250), f, f.Length, 13, 1, 0, 0);

            listBox = EmojiWindowNative.CreateListBox(hwnd, 20, 85, 330, 200, 0, BLACK, WHITE);
            // 添加初始项
            string[] listItems = { "🎨 UI设计", "🔧 后端开发", "📱 移动端", "🧪 测试", "📦 部署", "🎯 需求分析" };
            foreach (var item in listItems) { byte[] t = U(item); EmojiWindowNative.AddListItem(listBox, t, t.Length); }
            EmojiWindowNative.SetSelectedIndex(listBox, 0);

            btnListAdd = Btn(hwnd, new byte[]{0xe2,0x9e,0x95}, "添加", 20, 295, 80, 32, BLUE);
            btnListDel = Btn(hwnd, new byte[]{0xf0,0x9f,0x97,0x91,0xef,0xb8,0x8f}, "删除", 105, 295, 80, 32, RED);
            btnListRead = Btn(hwnd, new byte[]{0xf0,0x9f,0x93,0x96}, "读取", 190, 295, 80, 32, GREEN);
            btnListClear = Btn(hwnd, new byte[]{0xf0,0x9f,0xa7,0xb9}, "清空", 275, 295, 70, 32, GRAY);

            // ===== 右上：组合框区域 =====
            byte[] grpComboTitle = U("🔽 组合框示例");
            IntPtr grpCombo = EmojiWindowNative.CreateGroupBox(hwnd, 370, 55, 720, 150, grpComboTitle, grpComboTitle.Length, ARGB(255,230,162,60), ARGB(255,250,250,250), f, f.Length, 13, 1, 0, 0);

            // 只读组合框
            byte[] lblRO = U("只读:");
            EmojiWindowNative.CreateLabel(hwnd, 380, 85, 40, 28, lblRO, lblRO.Length, BLACK, TRANS, f, f.Length, 12, 0, 0, 0, 0, 0);
            comboReadOnly = EmojiWindowNative.CreateComboBox(hwnd, 425, 83, 250, 30, 1, BLACK, WHITE, 28, f, f.Length, 12, 0, 0, 0);
            string[] comboItems = { "🎨 设计模式", "🔧 开发模式", "🧪 测试模式", "🚀 发布模式" };
            foreach (var item in comboItems) { byte[] t = U(item); EmojiWindowNative.AddComboItem(comboReadOnly, t, t.Length); }
            EmojiWindowNative.SetComboSelectedIndex(comboReadOnly, 0);

            // 可编辑组合框
            byte[] lblEdit = U("可编辑:");
            EmojiWindowNative.CreateLabel(hwnd, 380, 120, 50, 28, lblEdit, lblEdit.Length, BLACK, TRANS, f, f.Length, 12, 0, 0, 0, 0, 0);
            comboEditable = EmojiWindowNative.CreateComboBox(hwnd, 435, 118, 240, 30, 0, BLACK, WHITE, 28, f, f.Length, 12, 0, 0, 0);
            string[] editItems = { "📝 选项A", "📝 选项B", "📝 选项C" };
            foreach (var item in editItems) { byte[] t = U(item); EmojiWindowNative.AddComboItem(comboEditable, t, t.Length); }

            btnComboRead = Btn(hwnd, new byte[]{0xf0,0x9f,0x93,0x96}, "读取选中", 700, 83, 100, 28, GREEN);
            btnComboSet = Btn(hwnd, new byte[]{0xe2,0x9c,0x8f}, "设置文本", 810, 83, 100, 28, BLUE);
            btnComboGetText = Btn(hwnd, new byte[]{0xf0,0x9f,0x93,0x96}, "获取文本", 920, 83, 100, 28, ORANGE);

            // ===== 中间：表格区域 =====
            byte[] grpGridTitle = U("📊 DataGridView 表格示例");
            IntPtr grpGrid = EmojiWindowNative.CreateGroupBox(hwnd, 370, 215, 720, 370, grpGridTitle, grpGridTitle.Length, ARGB(255,64,158,255), ARGB(255,250,250,250), f, f.Length, 13, 1, 0, 0);

            grid = EmojiWindowNative.CreateDataGridView(hwnd, 380, 245, 700, 280, 0, 1, BLACK, WHITE);

            // 添加列
            byte[][] colHeaders = { U("📋 项目名称"), U("📝 描述"), U("🏷️ 状态") };
            int[] colWidths = { 180, 220, 100 };
            for (int i = 0; i < colHeaders.Length; i++) EmojiWindowNative.DataGrid_AddTextColumn(grid, colHeaders[i], colHeaders[i].Length, colWidths[i]);
            byte[] chkH = U("✅ 选择"); EmojiWindowNative.DataGrid_AddCheckBoxColumn(grid, chkH, chkH.Length, 70);
            byte[] btnH = U("🔧 操作"); EmojiWindowNative.DataGrid_AddButtonColumn(grid, btnH, btnH.Length, 90);

            EmojiWindowNative.DataGrid_SetDefaultRowHeight(grid, 34);
            EmojiWindowNative.DataGrid_SetHeaderHeight(grid, 38);
            EmojiWindowNative.DataGrid_SetShowGridLines(grid, 1);
            EmojiWindowNative.DataGrid_SetFreezeHeader(grid, 1);
            EmojiWindowNative.DataGrid_SetSelectionMode(grid, 1);
            for (int i = 0; i < 5; i++) EmojiWindowNative.DataGrid_SetColumnHeaderAlignment(grid, i, 1);

            // 填充数据
            string[,] gridData = {
                { "🎨 UI设计稿", "📐 完成首页设计", "✅ 已完成" },
                { "🔧 后端API", "🌐 用户认证接口", "⏳ 进行中" },
                { "📱 移动端适配", "📲 响应式布局", "⏳ 进行中" },
                { "🧪 单元测试", "🔍 覆盖率>80%", "❌ 未开始" },
                { "📦 打包部署", "🚀 CI/CD流水线", "❌ 未开始" },
            };
            for (int r = 0; r < gridData.GetLength(0); r++)
            {
                int row = EmojiWindowNative.DataGrid_AddRow(grid);
                for (int c = 0; c < 3; c++) { byte[] t = U(gridData[r, c]); EmojiWindowNative.DataGrid_SetCellText(grid, row, c, t, t.Length); }
                byte[] bt = U("📋 详情"); EmojiWindowNative.DataGrid_SetCellText(grid, row, 4, bt, bt.Length);
            }
            EmojiWindowNative.DataGrid_SetCellChecked(grid, 0, 3, 1);
            EmojiWindowNative.DataGrid_SetCellStyle(grid, 0, 2, ARGB(255,103,194,58), 0, 1, 0);
            EmojiWindowNative.DataGrid_SetCellStyle(grid, 3, 2, ARGB(255,245,108,108), 0, 0, 0);
            EmojiWindowNative.DataGrid_SetCellStyle(grid, 4, 2, ARGB(255,245,108,108), 0, 0, 0);

            btnGridAdd = Btn(hwnd, new byte[]{0xe2,0x9e,0x95}, "添加行", 380, 535, 90, 32, BLUE);
            btnGridDel = Btn(hwnd, new byte[]{0xf0,0x9f,0x97,0x91,0xef,0xb8,0x8f}, "删除行", 480, 535, 90, 32, RED);
            btnGridRead = Btn(hwnd, new byte[]{0xf0,0x9f,0x93,0x96}, "读取", 580, 535, 90, 32, GREEN);
            btnGridSort = Btn(hwnd, new byte[]{0xf0,0x9f,0x94,0x84}, "排序", 680, 535, 90, 32, ORANGE);
            btnGridClear = Btn(hwnd, new byte[]{0xf0,0x9f,0xa7,0xb9}, "清空", 780, 535, 90, 32, GRAY);

            // ===== 底部：信息框区域 =====
            byte[] grpMsgTitle = U("💬 信息框示例");
            IntPtr grpMsg = EmojiWindowNative.CreateGroupBox(hwnd, 10, 385, 350, 200, grpMsgTitle, grpMsgTitle.Length, ARGB(255,103,194,58), ARGB(255,250,250,250), f, f.Length, 13, 1, 0, 0);

            byte[] msgHint = U("点击按钮弹出不同类型的信息框\n支持emoji图标和中文内容");
            EmojiWindowNative.CreateLabel(hwnd, 20, 415, 330, 45, msgHint, msgHint.Length, GRAY, TRANS, f, f.Length, 12, 0, 0, 0, 0, 1);

            btnMsgInfo = Btn(hwnd, new byte[]{0xf0,0x9f,0x92,0xa1}, "信息", 20, 470, 80, 35, BLUE);
            btnMsgWarn = Btn(hwnd, new byte[]{0xe2,0x9a,0xa0,0xef,0xb8,0x8f}, "警告", 105, 470, 80, 35, ORANGE);
            btnMsgError = Btn(hwnd, new byte[]{0xe2,0x9d,0x8c}, "错误", 190, 470, 80, 35, RED);
            btnMsgConfirm = Btn(hwnd, new byte[]{0xf0,0x9f,0xa4,0x94}, "确认框", 275, 470, 80, 35, GREEN);

            // 属性信息标签
            int listCount = EmojiWindowNative.GetListItemCount(listBox);
            int comboCount = EmojiWindowNative.GetComboItemCount(comboReadOnly);
            int gridRows = EmojiWindowNative.DataGrid_GetRowCount(grid);
            int gridCols = EmojiWindowNative.DataGrid_GetColumnCount(grid);
            byte[] info = U($"📊 列表框:{listCount}项 | 组合框:{comboCount}项 | 表格:{gridRows}行x{gridCols}列 | 🖱️ 点击交互查看回调效果");
            EmojiWindowNative.CreateLabel(hwnd, 10, 600, 1080, 30, info, info.Length, GRAY, TRANS, f, f.Length, 12, 0, 0, 0, 0, 0);

            // 读取属性验证
            byte[] propInfo = U($"📋 属性验证: 列表框选中={EmojiWindowNative.GetSelectedIndex(listBox)}, 组合框选中={EmojiWindowNative.GetComboSelectedIndex(comboReadOnly)}, 表格选中行={EmojiWindowNative.DataGrid_GetSelectedRow(grid)}, 复选框[0,3]={EmojiWindowNative.DataGrid_GetCellChecked(grid, 0, 3)}");
            EmojiWindowNative.CreateLabel(hwnd, 10, 635, 1080, 25, propInfo, propInfo.Length, ARGB(255,100,149,237), TRANS, f, f.Length, 11, 0, 0, 0, 0, 0);

            // 设置回调
            _btnCb = OnButtonClick;
            _listCb = OnListBoxSelect;
            _comboCb = OnComboSelect;
            _cellClickCb = OnCellClick;
            _cellDblClickCb = OnCellDblClick;
            _selChangedCb = OnSelChanged;
            _colHeaderCb = OnColHeaderClick;
            _cellValueCb = OnCellValueChanged;
            _msgBoxCb = OnConfirm;

            EmojiWindowNative.set_button_click_callback(_btnCb);
            EmojiWindowNative.SetListBoxCallback(listBox, _listCb);
            EmojiWindowNative.SetComboBoxCallback(comboReadOnly, _comboCb);
            EmojiWindowNative.SetComboBoxCallback(comboEditable, _comboCb);
            EmojiWindowNative.DataGrid_SetCellClickCallback(grid, _cellClickCb);
            EmojiWindowNative.DataGrid_SetCellDoubleClickCallback(grid, _cellDblClickCb);
            EmojiWindowNative.DataGrid_SetSelectionChangedCallback(grid, _selChangedCb);
            EmojiWindowNative.DataGrid_SetColumnHeaderClickCallback(grid, _colHeaderCb);
            EmojiWindowNative.DataGrid_SetCellValueChangedCallback(grid, _cellValueCb);

            EmojiWindowNative.set_message_loop_main_window(hwnd);
            Console.WriteLine("四控件综合示例窗口已创建，进入消息循环...");
            EmojiWindowNative.run_message_loop();
        }
    }
}