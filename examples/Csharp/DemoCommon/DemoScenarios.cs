using System;
using System.IO;
using System.Runtime.InteropServices;

namespace EmojiWindowDemo
{
    internal static partial class DemoScenarios
    {
        public static void Build(DemoKind kind, DemoApp app)
        {
            switch (kind)
            {
                case DemoKind.Button: BuildButtonDemo(app); break;
                case DemoKind.CheckBox: BuildCheckBoxDemo(app); break;
                case DemoKind.ColorEmojiEditBox: BuildColorEmojiEditBoxDemo(app); break;
                case DemoKind.ComboBox: BuildComboBoxDemo(app); break;
                case DemoKind.ConfirmBox: BuildConfirmBoxDemo(app); break;
                case DemoKind.D2DComboBox: BuildD2DComboBoxDemo(app); break;
                case DemoKind.DataGridView: BuildDataGridViewDemo(app); break;
                case DemoKind.DateTimePicker: BuildDateTimePickerDemo(app); break;
                case DemoKind.EditBox: BuildEditBoxDemo(app); break;
                case DemoKind.GroupBox: BuildGroupBoxDemo(app); break;
                case DemoKind.HotKey: BuildHotKeyDemo(app); break;
                case DemoKind.Label: BuildLabelDemo(app); break;
                case DemoKind.ListBox: BuildListBoxDemo(app); break;
                case DemoKind.MenuBar: BuildMenuBarDemo(app); break;
                case DemoKind.MessageBox: BuildMessageBoxDemo(app); break;
                case DemoKind.Notification: BuildNotificationDemo(app); break;
                case DemoKind.Panel: BuildPanelDemo(app); break;
                case DemoKind.PictureBox: BuildPictureBoxDemo(app); break;
                case DemoKind.PopupMenu: BuildPopupMenuDemo(app); break;
                case DemoKind.ProgressBar: BuildProgressBarDemo(app); break;
                case DemoKind.RadioButton: BuildRadioButtonDemo(app); break;
                case DemoKind.Slider: BuildSliderDemo(app); break;
                case DemoKind.Switch: BuildSwitchDemo(app); break;
                case DemoKind.TabControl: BuildTabControlDemo(app); break;
                case DemoKind.Tooltip: BuildTooltipDemo(app); break;
                case DemoKind.TreeView: BuildTreeViewDemo(app); break;
                case DemoKind.Window: BuildWindowDemo(app); break;
                default: throw new ArgumentOutOfRangeException(nameof(kind), kind, null);
            }
        }

        private static void BuildButtonDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowButtonDemo - C# x64", 780, 420, DemoColors.Blue);
            app.CreateStatusBar("按钮示例：点击不同按钮查看状态变化");
            app.Label(24, 24, 360, 28, "按钮演示：主要、成功、警告、危险、加载态", DemoColors.Black, DemoColors.Transparent, 14);

            int primary = app.Button(24, 72, 150, 42, "主要按钮", "🚀", DemoColors.Blue, () => app.SetStatus("点击了主要按钮"));
            int success = app.Button(190, 72, 150, 42, "成功按钮", "✅", DemoColors.Green, () => app.SetStatus("点击了成功按钮"));
            int warning = app.Button(356, 72, 150, 42, "警告按钮", "⚠️", DemoColors.Orange, () => app.SetStatus("点击了警告按钮"));
            app.Button(522, 72, 150, 42, "危险按钮", "🛑", DemoColors.Red, () => app.SetStatus("点击了危险按钮"));

            app.Button(24, 132, 150, 38, "切换加载态", "⏳", DemoColors.Purple, () =>
            {
                EmojiWindowNative.SetButtonLoading(primary, 1);
                app.SetStatus("已将“主要按钮”切换为加载态");
            });

            app.Button(190, 132, 150, 38, "修改文本", "✏️", DemoColors.Cyan, () =>
            {
                byte[] text = app.U("文本已更新");
                EmojiWindowNative.SetButtonText(success, text, text.Length);
                app.SetStatus("已修改“成功按钮”的文本");
            });

            app.Button(356, 132, 150, 38, "换背景色", "🎨", DemoColors.Gray, () =>
            {
                EmojiWindowNative.SetButtonBackgroundColor(warning, DemoColors.Red);
                app.SetStatus("已把“警告按钮”改成红色背景");
            });
        }

        private static void BuildCheckBoxDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowCheckBoxDemo - C# x64", 760, 420, DemoColors.Green);
            app.CreateStatusBar("复选框示例：勾选任意项会立即更新状态栏");

            IntPtr cb1 = EmojiWindowNative.CreateCheckBox(app.Window, 24, 72, 220, 34, app.U("启用自动刷新"), app.U("启用自动刷新").Length, 1, DemoColors.Black, DemoColors.Transparent, app.U("微软雅黑"), app.U("微软雅黑").Length, 13, 0, 0, 0);
            IntPtr cb2 = EmojiWindowNative.CreateCheckBox(app.Window, 24, 112, 220, 34, app.U("允许多标签"), app.U("允许多标签").Length, 1, DemoColors.Black, DemoColors.Transparent, app.U("微软雅黑"), app.U("微软雅黑").Length, 13, 0, 0, 0);
            IntPtr cb3 = EmojiWindowNative.CreateCheckBox(app.Window, 24, 152, 220, 34, app.U("启动时恢复上次会话"), app.U("启动时恢复上次会话").Length, 0, DemoColors.Black, DemoColors.Transparent, app.U("微软雅黑"), app.U("微软雅黑").Length, 13, 0, 0, 0);

            var callback = app.Pin(new EmojiWindowNative.CheckBoxCallback((handle, checkedState) =>
            {
                string text = EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetCheckBoxText, handle);
                app.SetStatus(text + (checkedState != 0 ? "：已选中" : "：未选中"));
            }));
            EmojiWindowNative.SetCheckBoxCallback(cb1, callback);
            EmojiWindowNative.SetCheckBoxCallback(cb2, callback);
            EmojiWindowNative.SetCheckBoxCallback(cb3, callback);

            app.Button(280, 72, 150, 38, "读取状态", "📋", DemoColors.Blue, () =>
            {
                string status = string.Format("自动刷新={0}，多标签={1}，恢复会话={2}",
                    EmojiWindowNative.GetCheckBoxState(cb1),
                    EmojiWindowNative.GetCheckBoxState(cb2),
                    EmojiWindowNative.GetCheckBoxState(cb3));
                app.SetStatus(status);
            });

            app.Button(280, 120, 150, 38, "切换第三项", "🔁", DemoColors.Orange, () =>
            {
                int newState = EmojiWindowNative.GetCheckBoxState(cb3) == 0 ? 1 : 0;
                EmojiWindowNative.SetCheckBoxState(cb3, newState);
                app.SetStatus("已切换“启动时恢复上次会话”");
            });
        }

        private static void BuildColorEmojiEditBoxDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowColorEmojiEditBoxDemo - C# x64", 860, 460, DemoColors.Purple);
            app.CreateStatusBar("彩色 Emoji 编辑框示例：按 Enter 或点击按钮读取文本");

            IntPtr edit = app.EditBox(24, 72, 800, 42, "欢迎使用 😄 彩色 Emoji 编辑框 🌈", false, false, false, true);
            IntPtr multi = app.EditBox(24, 132, 800, 140, "这里支持多行输入：\r\n1. 彩色 emoji 😀\r\n2. 中文文本\r\n3. x64 运行", true, false, false, true);

            var keyCallback = app.Pin(new EmojiWindowNative.EditBoxKeyCallback((handle, keyCode, keyDown, shift, ctrl, alt) =>
            {
                if (keyDown != 0 && keyCode == 13)
                {
                    app.SetStatus("单行文本：" + EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetEditBoxText, edit));
                }
            }));
            EmojiWindowNative.SetEditBoxKeyCallback(edit, keyCallback);

            app.Button(24, 292, 140, 38, "读取文本", "📖", DemoColors.Blue, () => app.SetStatus("读取结果：" + EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetEditBoxText, edit)));
            app.Button(178, 292, 160, 38, "写入示例文本", "✏️", DemoColors.Green, () =>
            {
                byte[] text = app.U("新的内容 🎉 依然支持彩色 emoji 🚀");
                EmojiWindowNative.SetEditBoxText(edit, text, text.Length);
                app.SetStatus("已写入新的单行文本");
            });
            app.Button(352, 292, 180, 38, "重置多行内容", "🧹", DemoColors.Orange, () =>
            {
                byte[] text = app.U("已重置多行内容：\r\n- emoji 😎\r\n- 中文说明\r\n- 回车读取");
                EmojiWindowNative.SetEditBoxText(multi, text, text.Length);
                app.SetStatus("多行编辑框已重置");
            });
        }

        private static void BuildComboBoxDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowComboBoxDemo - C# x64", 820, 420, DemoColors.Cyan);
            app.CreateStatusBar("组合框示例：包含只读组合框和可编辑组合框");

            IntPtr readOnlyCombo = EmojiWindowNative.CreateComboBox(app.Window, 24, 64, 300, 34, 1, DemoColors.Black, DemoColors.White, 30, app.U("微软雅黑"), app.U("微软雅黑").Length, 13, 0, 0, 0);
            foreach (string item in new[] { "首页 🏠", "设置 ⚙️", "收藏 ⭐", "下载 ⬇️" })
            {
                byte[] text = app.U(item);
                EmojiWindowNative.AddComboItem(readOnlyCombo, text, text.Length);
            }
            EmojiWindowNative.SetComboSelectedIndex(readOnlyCombo, 0);

            IntPtr editCombo = EmojiWindowNative.CreateComboBox(app.Window, 24, 152, 300, 34, 0, DemoColors.Black, DemoColors.White, 30, app.U("微软雅黑"), app.U("微软雅黑").Length, 13, 0, 0, 0);
            foreach (string item in new[] { "https://www.example.com", "https://github.com", "https://openai.com" })
            {
                byte[] text = app.U(item);
                EmojiWindowNative.AddComboItem(editCombo, text, text.Length);
            }

            var comboCallback = app.Pin(new EmojiWindowNative.ComboBoxCallback((handle, index) =>
            {
                if (index >= 0)
                {
                    app.SetStatus("当前选中：" + EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetComboItemText, handle, index));
                }
            }));
            EmojiWindowNative.SetComboBoxCallback(readOnlyCombo, comboCallback);
            EmojiWindowNative.SetComboBoxCallback(editCombo, comboCallback);

            app.Button(360, 64, 140, 36, "读取选中", "📋", DemoColors.Blue, () =>
            {
                int index = EmojiWindowNative.GetComboSelectedIndex(readOnlyCombo);
                string text = index >= 0 ? EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetComboItemText, readOnlyCombo, index) : "(未选中)";
                app.SetStatus("只读组合框：" + text);
            });

            app.Button(360, 112, 160, 36, "填入新网址", "🌐", DemoColors.Green, () =>
            {
                byte[] text = app.U("https://emoji-window.demo/tab");
                EmojiWindowNative.SetComboBoxText(editCombo, text, text.Length);
                app.SetStatus("已向可编辑组合框填入网址");
            });

            app.Button(360, 160, 160, 36, "读取文本", "📖", DemoColors.Orange, () => app.SetStatus("当前文本：" + EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetComboBoxText, editCombo)));
        }

        private static void BuildConfirmBoxDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowConfirmBoxDemo - C# x64", 620, 300, DemoColors.Orange);
            app.CreateStatusBar("确认框示例：点击按钮弹出确认框");

            var confirmCallback = app.Pin(new EmojiWindowNative.MessageBoxCallback(confirmed => app.SetStatus(confirmed != 0 ? "用户点击了确认" : "用户点击了取消")));
            app.Button(24, 130, 160, 40, "删除当前标签", "🗑️", DemoColors.Red, () =>
            {
                byte[] title = app.U("确认操作");
                byte[] message = app.U("确定要删除当前标签页吗？");
                byte[] icon = app.U("❓");
                EmojiWindowNative.show_confirm_box_bytes(app.Window, title, title.Length, message, message.Length, icon, icon.Length, confirmCallback);
            });
        }

        private static void BuildD2DComboBoxDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowD2DComboBoxDemo - C# x64", 840, 380, DemoColors.Purple);
            app.CreateStatusBar("D2D 组合框示例：验证彩色 Emoji 组合框");

            IntPtr combo = EmojiWindowNative.CreateD2DComboBox(app.Window, 24, 72, 340, 36, 0, DemoColors.Black, DemoColors.White, 34, app.U("微软雅黑"), app.U("微软雅黑").Length, 14, 0, 0, 0);
            foreach (string item in new[] { "😀 默认主题", "🌤️ 浅色主题", "🌙 深色主题", "🎨 自定义主题" })
            {
                byte[] text = app.U(item);
                EmojiWindowNative.AddD2DComboItem(combo, text, text.Length);
            }
            EmojiWindowNative.SetD2DComboSelectedIndex(combo, 0);
            EmojiWindowNative.SetD2DComboBoxColors(combo, DemoColors.Black, DemoColors.White, DemoColors.LightBlue, DemoColors.Yellow, DemoColors.Border, DemoColors.Blue);

            var comboCallback = app.Pin(new EmojiWindowNative.ComboBoxCallback((handle, index) =>
            {
                if (index >= 0)
                {
                    app.SetStatus("D2D 选中：" + EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetD2DComboItemText, handle, index));
                }
            }));
            EmojiWindowNative.SetD2DComboBoxCallback(combo, comboCallback);

            app.Button(390, 72, 150, 36, "读取当前值", "📖", DemoColors.Blue, () => app.SetStatus("当前文本：" + EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetD2DComboText, combo)));
            app.Button(390, 120, 170, 36, "填入自定义主题", "✏️", DemoColors.Green, () =>
            {
                byte[] text = app.U("🧩 企业蓝主题");
                EmojiWindowNative.SetD2DComboText(combo, text, text.Length);
                app.SetStatus("已写入自定义文本");
            });
        }

        private static void BuildDataGridViewDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowDataGridViewDemo - C# x64", 980, 620, DemoColors.Blue);
            app.CreateStatusBar("DataGridView 示例：点击单元格或列头查看状态变化");

            IntPtr grid = EmojiWindowNative.CreateDataGridView(app.Window, 24, 72, 920, 420, 0, 1, DemoColors.Black, DemoColors.White);
            EmojiWindowNative.DataGrid_AddTextColumn(grid, app.U("任务"), app.U("任务").Length, 220);
            EmojiWindowNative.DataGrid_AddTextColumn(grid, app.U("描述"), app.U("描述").Length, 280);
            EmojiWindowNative.DataGrid_AddTextColumn(grid, app.U("状态"), app.U("状态").Length, 150);
            EmojiWindowNative.DataGrid_AddCheckBoxColumn(grid, app.U("完成"), app.U("完成").Length, 90);
            EmojiWindowNative.DataGrid_AddButtonColumn(grid, app.U("操作"), app.U("操作").Length, 120);
            EmojiWindowNative.DataGrid_SetDefaultRowHeight(grid, 34);
            EmojiWindowNative.DataGrid_SetHeaderHeight(grid, 38);
            EmojiWindowNative.DataGrid_SetShowGridLines(grid, 1);
            EmojiWindowNative.DataGrid_SetSelectionMode(grid, 1);

            AddGridRow(app, grid, "浏览器框架", "修复新标签切换", "进行中", 0, "查看");
            AddGridRow(app, grid, "地址栏", "增加前进后退", "已完成", 1, "详情");
            AddGridRow(app, grid, "打包", "固定 x64", "已完成", 1, "详情");

            var cellCallback = app.Pin(new EmojiWindowNative.DataGridCellCallback((handle, row, col) =>
            {
                app.SetStatus(string.Format("单元格 [{0},{1}] = {2}", row, col, EmojiWindowNative.ReadUtf8(EmojiWindowNative.DataGrid_GetCellText, handle, row, col)));
            }));
            var headerCallback = app.Pin(new EmojiWindowNative.DataGridColumnHeaderCallback((handle, col) => app.SetStatus("点击了第 " + col + " 列的表头")));
            EmojiWindowNative.DataGrid_SetCellClickCallback(grid, cellCallback);
            EmojiWindowNative.DataGrid_SetColumnHeaderClickCallback(grid, headerCallback);

            app.Button(24, 510, 120, 36, "新增一行", "➕", DemoColors.Green, () =>
            {
                AddGridRow(app, grid, "新增任务", "运行时追加的数据", "待处理", 0, "打开");
                app.SetStatus("已新增一行");
            });

            app.Button(158, 510, 120, 36, "删除选中行", "🗑️", DemoColors.Red, () =>
            {
                int row = EmojiWindowNative.DataGrid_GetSelectedRow(grid);
                if (row >= 0)
                {
                    EmojiWindowNative.DataGrid_RemoveRow(grid, row);
                    app.SetStatus("已删除第 " + row + " 行");
                }
                else
                {
                    app.SetStatus("当前没有选中行");
                }
            });

            app.Button(292, 510, 120, 36, "按任务排序", "🔽", DemoColors.Orange, () =>
            {
                EmojiWindowNative.DataGrid_SortByColumn(grid, 0, 1);
                app.SetStatus("已按第 0 列升序排序");
            });
        }

        private static void AddGridRow(DemoApp app, IntPtr grid, string title, string description, string status, int done, string actionText)
        {
            int row = EmojiWindowNative.DataGrid_AddRow(grid);
            byte[] t1 = app.U(title);
            byte[] t2 = app.U(description);
            byte[] t3 = app.U(status);
            byte[] t4 = app.U(actionText);
            EmojiWindowNative.DataGrid_SetCellText(grid, row, 0, t1, t1.Length);
            EmojiWindowNative.DataGrid_SetCellText(grid, row, 1, t2, t2.Length);
            EmojiWindowNative.DataGrid_SetCellText(grid, row, 2, t3, t3.Length);
            EmojiWindowNative.DataGrid_SetCellChecked(grid, row, 3, done);
            EmojiWindowNative.DataGrid_SetCellText(grid, row, 4, t4, t4.Length);
        }

        private static void BuildDateTimePickerDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowDateTimePickerDemo - C# x64", 760, 320, DemoColors.Cyan);
            app.CreateStatusBar("日期时间选择器示例");

            IntPtr picker = EmojiWindowNative.CreateD2DDateTimePicker(app.Window, 24, 72, 300, 38, 5, DemoColors.Black, DemoColors.White, DemoColors.Border, app.U("微软雅黑"), app.U("微软雅黑").Length, 13, 0, 0, 0);
            EmojiWindowNative.SetD2DDateTimePickerDateTime(picker, 2026, 4, 1, 10, 30, 45);
            var callback = app.Pin(new EmojiWindowNative.ValueChangedCallback(handle =>
            {
                EmojiWindowNative.GetD2DDateTimePickerDateTime(handle, out int year, out int month, out int day, out int hour, out int minute, out int second);
                app.SetStatus(string.Format("当前值：{0:D4}-{1:D2}-{2:D2} {3:D2}:{4:D2}:{5:D2}", year, month, day, hour, minute, second));
            }));
            EmojiWindowNative.SetD2DDateTimePickerCallback(picker, callback);

            app.Button(352, 72, 150, 36, "读取当前时间", "📖", DemoColors.Blue, () =>
            {
                EmojiWindowNative.GetD2DDateTimePickerDateTime(picker, out int year, out int month, out int day, out int hour, out int minute, out int second);
                app.SetStatus(string.Format("{0:D4}-{1:D2}-{2:D2} {3:D2}:{4:D2}:{5:D2}", year, month, day, hour, minute, second));
            });

            app.Button(352, 120, 150, 36, "切到今天", "📅", DemoColors.Green, () =>
            {
                DateTime now = DateTime.Now;
                EmojiWindowNative.SetD2DDateTimePickerDateTime(picker, now.Year, now.Month, now.Day, now.Hour, now.Minute, now.Second);
                app.SetStatus("已切换到当前系统时间");
            });

            app.Button(352, 168, 150, 36, "只显示日期", "🧭", DemoColors.Orange, () =>
            {
                EmojiWindowNative.SetD2DDateTimePickerPrecision(picker, 2);
                app.SetStatus("已把精度改为“年月日”");
            });
        }

        private static void BuildEditBoxDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowEditBoxDemo - C# x64", 860, 460, DemoColors.Blue);
            app.CreateStatusBar("普通编辑框示例：单行回车读取，多行支持换行");

            IntPtr single = app.EditBox(24, 72, 780, 40, "请输入地址或关键字");
            IntPtr multi = app.EditBox(24, 132, 780, 160, "多行编辑框内容\r\n- 第一行\r\n- 第二行", true);

            var callback = app.Pin(new EmojiWindowNative.EditBoxKeyCallback((handle, keyCode, keyDown, shift, ctrl, alt) =>
            {
                if (handle == single && keyDown != 0 && keyCode == 13)
                {
                    app.SetStatus("回车读取：" + EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetEditBoxText, single));
                }
            }));
            EmojiWindowNative.SetEditBoxKeyCallback(single, callback);

            app.Button(24, 314, 140, 36, "读取单行", "📖", DemoColors.Blue, () => app.SetStatus("单行内容：" + EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetEditBoxText, single)));
            app.Button(178, 314, 140, 36, "覆盖单行", "✏️", DemoColors.Green, () =>
            {
                byte[] text = app.U("https://emoji-window.local");
                EmojiWindowNative.SetEditBoxText(single, text, text.Length);
                app.SetStatus("已写入新的单行内容");
            });
            app.Button(332, 314, 150, 36, "读取多行", "📋", DemoColors.Orange, () => app.SetStatus("多行长度：" + EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetEditBoxText, multi).Length));
        }

        private static void BuildGroupBoxDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowGroupBoxDemo - C# x64", 820, 460, DemoColors.Green);
            app.CreateStatusBar("GroupBox 示例：控件仍然挂在主窗口上，避免直接 parent 到 GroupBox 句柄");

            IntPtr group1 = app.GroupBox(24, 56, 360, 240, "安全布局区 A", DemoColors.Blue, DemoColors.Surface);
            IntPtr group2 = app.GroupBox(408, 56, 360, 240, "安全布局区 B", DemoColors.Orange, DemoColors.Surface);
            EmojiWindowNative.SetGroupBoxTitleColor(group1, DemoColors.Blue);
            EmojiWindowNative.SetGroupBoxTitleColor(group2, DemoColors.Orange);

            app.Label(40, 92, 320, 60, "注意：这里的 Label / Button 都直接创建在主窗口上，只是视觉上放进分组框区域里。", DemoColors.Gray, DemoColors.Transparent, 12, 0, true);
            app.Label(424, 92, 320, 60, "这样可以避开你说的 C# GroupBox 子控件空白问题。", DemoColors.Gray, DemoColors.Transparent, 12, 0, true);

            app.Button(40, 176, 140, 36, "改左侧标题", "✏️", DemoColors.Blue, () =>
            {
                byte[] title = app.U("已改名的分组 A");
                EmojiWindowNative.SetGroupBoxTitle(group1, title, title.Length);
                app.SetStatus("左侧 GroupBox 标题已修改");
            });

            app.Button(424, 176, 140, 36, "切样式", "🧩", DemoColors.Orange, () =>
            {
                EmojiWindowNative.SetGroupBoxStyle(group2, 1);
                app.SetStatus("右侧 GroupBox 样式已切换");
            });
        }

        private static void BuildHotKeyDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowHotKeyDemo - C# x64", 760, 340, DemoColors.Purple);
            app.CreateStatusBar("热键控件示例");

            IntPtr hotKey = EmojiWindowNative.CreateHotKeyControl(app.Window, 24, 72, 260, 36, DemoColors.Black, DemoColors.White);
            EmojiWindowNative.SetHotKeyColors(hotKey, DemoColors.Black, DemoColors.White, DemoColors.Border);

            var callback = app.Pin(new EmojiWindowNative.HotKeyCallback((handle, vkCode, modifiers) => app.SetStatus("当前热键：" + FormatHotKey(vkCode, modifiers))));
            EmojiWindowNative.SetHotKeyCallback(hotKey, callback);

            app.Button(320, 72, 150, 36, "设为 Ctrl+Shift+S", "⌨️", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetHotKey(hotKey, 0x53, 3);
                app.SetStatus("已设置为 Ctrl+Shift+S");
            });

            app.Button(320, 120, 120, 36, "读取热键", "📖", DemoColors.Green, () =>
            {
                EmojiWindowNative.GetHotKey(hotKey, out int vkCode, out int modifiers);
                app.SetStatus("读取结果：" + FormatHotKey(vkCode, modifiers));
            });

            app.Button(320, 168, 120, 36, "清空", "🧹", DemoColors.Red, () =>
            {
                EmojiWindowNative.ClearHotKey(hotKey);
                app.SetStatus("热键已清空");
            });
        }

        private static string FormatHotKey(int vkCode, int modifiers)
        {
            if (vkCode == 0)
            {
                return "(未设置)";
            }

            string text = string.Empty;
            if ((modifiers & 2) != 0) text += "Ctrl+";
            if ((modifiers & 1) != 0) text += "Shift+";
            if ((modifiers & 4) != 0) text += "Alt+";
            return text + ((char)vkCode).ToString().ToUpperInvariant();
        }

        private static void BuildLabelDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowLabelDemo - C# x64", 820, 420, DemoColors.Cyan);
            app.CreateStatusBar("标签示例：左对齐、居中、自动换行");

            IntPtr left = app.Label(24, 72, 240, 40, "左对齐标签：适合状态说明", DemoColors.Black, DemoColors.LightBlue, 13, 0);
            IntPtr center = app.Label(288, 72, 240, 40, "居中标签：当前页", DemoColors.Black, DemoColors.Yellow, 13, 1);
            app.Label(24, 132, 504, 76, "自动换行标签：这个 demo 用来验证 Label 在 C# x64 下仍可正常显示中文、Emoji 和多行内容，不会因为项目丢失而变成“未找到”。", DemoColors.Black, DemoColors.LightGreen, 12, 0, true);

            app.Button(560, 72, 160, 36, "改中间文字", "✏️", DemoColors.Blue, () =>
            {
                byte[] text = app.U("居中标签：已更新 ✅");
                EmojiWindowNative.SetLabelText(center, text, text.Length);
                app.SetStatus("已更新居中标签");
            });

            app.Button(560, 120, 160, 36, "改左侧颜色", "🎨", DemoColors.Orange, () =>
            {
                EmojiWindowNative.SetLabelColor(left, DemoColors.White, DemoColors.Red);
                app.SetStatus("左侧标签前景/背景色已切换");
            });
        }

        private static void BuildListBoxDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowListBoxDemo - C# x64", 760, 460, DemoColors.Blue);
            app.CreateStatusBar("列表框示例");

            IntPtr list = EmojiWindowNative.CreateListBox(app.Window, 24, 72, 300, 260, 0, DemoColors.Black, DemoColors.White);
            foreach (string item in new[] { "首页 🏠", "下载管理 ⬇️", "书签 ⭐", "设置 ⚙️", "关于 ℹ️" })
            {
                byte[] text = app.U(item);
                EmojiWindowNative.AddListItem(list, text, text.Length);
            }
            EmojiWindowNative.SetSelectedIndex(list, 0);

            var callback = app.Pin(new EmojiWindowNative.ListBoxCallback((handle, index) =>
            {
                string text = index >= 0 ? EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetListItemText, handle, index) : "(无)";
                app.SetStatus("当前选中：" + text);
            }));
            EmojiWindowNative.SetListBoxCallback(list, callback);

            app.Button(360, 72, 120, 36, "添加项", "➕", DemoColors.Green, () =>
            {
                int count = EmojiWindowNative.GetListItemCount(list);
                byte[] text = app.U("新增项 " + (count + 1));
                EmojiWindowNative.AddListItem(list, text, text.Length);
                app.SetStatus("已新增一项");
            });

            app.Button(360, 120, 120, 36, "读取项", "📖", DemoColors.Blue, () =>
            {
                int index = EmojiWindowNative.GetSelectedIndex(list);
                app.SetStatus(index >= 0 ? EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetListItemText, list, index) : "(未选中)");
            });

            app.Button(360, 168, 120, 36, "删除项", "🗑️", DemoColors.Red, () =>
            {
                int index = EmojiWindowNative.GetSelectedIndex(list);
                if (index >= 0)
                {
                    EmojiWindowNative.RemoveListItem(list, index);
                    app.SetStatus("已删除第 " + index + " 项");
                }
                else
                {
                    app.SetStatus("请先选中一项");
                }
            });
        }

        private static void BuildMenuBarDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowMenuBarDemo - C# x64", 900, 420, DemoColors.Blue);
            app.CreateStatusBar("菜单栏示例：点击菜单项观察回调");

            IntPtr menuBar = EmojiWindowNative.CreateMenuBar(app.Window);
            EmojiWindowNative.SetMenuBarPlacement(menuBar, 0, 32, 900, 34);
            EmojiWindowNative.MenuBarAddItem(menuBar, app.U("文件"), app.U("文件").Length, 100);
            EmojiWindowNative.MenuBarAddItem(menuBar, app.U("工具"), app.U("工具").Length, 200);
            EmojiWindowNative.MenuBarAddSubItem(menuBar, 100, app.U("打开项目"), app.U("打开项目").Length, 101);
            EmojiWindowNative.MenuBarAddSubItem(menuBar, 100, app.U("退出"), app.U("退出").Length, 102);
            EmojiWindowNative.MenuBarAddSubItem(menuBar, 200, app.U("开发者工具"), app.U("开发者工具").Length, 201);
            EmojiWindowNative.MenuBarAddSubItem(menuBar, 200, app.U("工具箱"), app.U("工具箱").Length, 202);

            var callback = app.Pin(new EmojiWindowNative.MenuItemClickCallback((menuId, itemId) => app.SetStatus(string.Format("菜单回调：menu_id={0}, item_id={1}", menuId, itemId))));
            EmojiWindowNative.SetMenuBarCallback(menuBar, callback);

            app.Label(24, 92, 520, 50, "菜单栏单独创建在窗口顶部，下方按钮只是为了验证 C# 项目没有丢失。", DemoColors.Gray, DemoColors.Transparent, 12, 0, true);
            app.Button(24, 170, 160, 36, "改“工具箱”文字", "✏️", DemoColors.Orange, () =>
            {
                byte[] text = app.U("扩展工具箱");
                EmojiWindowNative.MenuBarUpdateSubItemText(menuBar, 200, 202, text, text.Length);
                app.SetStatus("已更新菜单项文字");
            });
        }

        private static void BuildMessageBoxDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowMessageBoxDemo - C# x64", 660, 320, DemoColors.Blue);
            app.CreateStatusBar("消息框示例");

            app.Button(24, 72, 120, 40, "信息框", "ℹ️", DemoColors.Blue, () => ShowMessage(app, "信息", "这里是信息提示框", "ℹ️"));
            app.Button(158, 72, 120, 40, "警告框", "⚠️", DemoColors.Orange, () => ShowMessage(app, "警告", "这里是警告提示框", "⚠️"));
            app.Button(292, 72, 120, 40, "错误框", "❌", DemoColors.Red, () => ShowMessage(app, "错误", "这里是错误提示框", "❌"));
        }

        private static void ShowMessage(DemoApp app, string title, string message, string icon)
        {
            byte[] titleBytes = app.U(title);
            byte[] messageBytes = app.U(message);
            byte[] iconBytes = app.U(icon);
            EmojiWindowNative.show_message_box_bytes(app.Window, titleBytes, titleBytes.Length, messageBytes, messageBytes.Length, iconBytes, iconBytes.Length);
            app.SetStatus("已弹出消息框：" + title);
        }

        private static void BuildNotificationDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowNotificationDemo - C# x64", 760, 320, DemoColors.Cyan);
            app.CreateStatusBar("通知示例：弹出不同类型的通知");

            var callback = app.Pin(new EmojiWindowNative.NotificationCallback((handle, eventType) => app.SetStatus("通知事件类型：" + eventType)));
            app.Button(24, 72, 140, 40, "成功通知", "✅", DemoColors.Green, () => ShowNotification(app, callback, "成功", "标签页已创建", 0));
            app.Button(178, 72, 140, 40, "警告通知", "⚠️", DemoColors.Orange, () => ShowNotification(app, callback, "警告", "当前地址为空", 1));
            app.Button(332, 72, 140, 40, "错误通知", "❌", DemoColors.Red, () => ShowNotification(app, callback, "错误", "网页加载失败", 2));
        }

        private static void ShowNotification(DemoApp app, EmojiWindowNative.NotificationCallback callback, string title, string message, int type)
        {
            byte[] titleBytes = app.U(title);
            byte[] messageBytes = app.U(message);
            IntPtr notification = EmojiWindowNative.ShowNotification(app.Window, titleBytes, titleBytes.Length, messageBytes, messageBytes.Length, type, 1, 2500);
            if (notification != IntPtr.Zero)
            {
                EmojiWindowNative.SetNotificationCallback(notification, callback);
            }

            app.SetStatus("已弹出通知：" + title);
        }

        private static void BuildPanelDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowPanelDemo - C# x64", 860, 420, DemoColors.Green);
            app.CreateStatusBar("Panel 示例：切换面板背景色");

            IntPtr panelA = EmojiWindowNative.CreatePanel(app.Window, 24, 72, 240, 180, DemoColors.LightBlue);
            IntPtr panelB = EmojiWindowNative.CreatePanel(app.Window, 288, 72, 240, 180, DemoColors.LightGreen);
            IntPtr panelC = EmojiWindowNative.CreatePanel(app.Window, 552, 72, 240, 180, DemoColors.Yellow);

            app.Label(40, 90, 180, 24, "蓝色面板", DemoColors.Black);
            app.Label(304, 90, 180, 24, "绿色面板", DemoColors.Black);
            app.Label(568, 90, 180, 24, "黄色面板", DemoColors.Black);

            app.Button(24, 280, 150, 36, "面板 A 变红", "🎨", DemoColors.Red, () =>
            {
                EmojiWindowNative.SetPanelBackgroundColor(panelA, DemoColors.LightRed);
                app.SetStatus("面板 A 已改成浅红色");
            });

            app.Button(188, 280, 150, 36, "面板 B 变蓝", "🎨", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetPanelBackgroundColor(panelB, DemoColors.LightBlue);
                app.SetStatus("面板 B 已改成浅蓝色");
            });

            app.Button(352, 280, 160, 36, "读取面板 C", "📖", DemoColors.Orange, () =>
            {
                EmojiWindowNative.GetPanelBackgroundColor(panelC, out uint color);
                app.SetStatus("面板 C 当前背景色 ARGB=" + color);
            });
        }

        private static void BuildPictureBoxDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowPictureBoxDemo - C# x64", 920, 560, DemoColors.Blue);
            app.CreateStatusBar("PictureBox 示例：自动尝试加载 examples/Csharp/Demo截图.png");

            IntPtr picture = EmojiWindowNative.CreatePictureBox(app.Window, 24, 72, 620, 380, 2, DemoColors.White);
            var callback = app.Pin(new EmojiWindowNative.PictureBoxCallback(handle => app.SetStatus("点击了 PictureBox")));
            EmojiWindowNative.SetPictureBoxCallback(picture, callback);

            TryLoadDemoImage(app, picture);

            app.Button(676, 72, 160, 36, "重新加载图片", "🖼️", DemoColors.Blue, () => TryLoadDemoImage(app, picture));
            app.Button(676, 120, 160, 36, "清空图片", "🧹", DemoColors.Red, () =>
            {
                EmojiWindowNative.ClearImage(picture);
                app.SetStatus("图片已清空");
            });
            app.Button(676, 168, 160, 36, "拉伸模式", "↔️", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetPictureBoxScaleMode(picture, 1);
                app.SetStatus("已切换到拉伸模式");
            });
            app.Button(676, 216, 160, 36, "半透明", "🌫️", DemoColors.Orange, () =>
            {
                EmojiWindowNative.SetImageOpacity(picture, 0.5f);
                app.SetStatus("图片透明度已设为 0.5");
            });
        }

        private static void TryLoadDemoImage(DemoApp app, IntPtr picture)
        {
            string file = app.FindFileUpwards("Demo截图.png");
            if (string.IsNullOrEmpty(file))
            {
                app.SetStatus("未找到 Demo截图.png");
                return;
            }

            byte[] path = app.U(file);
            int result = EmojiWindowNative.LoadImageFromFile(picture, path, path.Length);
            app.SetStatus(result != 0 ? "已加载图片：" + Path.GetFileName(file) : "图片加载失败");
        }

        private static void BuildPopupMenuDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowPopupMenuDemo - C# x64", 760, 380, DemoColors.Orange);
            app.CreateStatusBar("弹出菜单示例：右键编辑框或点击按钮直接显示");

            IntPtr popup = EmojiWindowNative.CreateEmojiPopupMenu(app.Window);
            EmojiWindowNative.PopupMenuAddItem(popup, app.U("刷新"), app.U("刷新").Length, 1001);
            EmojiWindowNative.PopupMenuAddItem(popup, app.U("复制链接"), app.U("复制链接").Length, 1002);
            EmojiWindowNative.PopupMenuAddSubItem(popup, 1002, app.U("复制标题"), app.U("复制标题").Length, 1003);
            var callback = app.Pin(new EmojiWindowNative.MenuItemClickCallback((menuId, itemId) => app.SetStatus(string.Format("弹出菜单回调：menu_id={0}, item_id={1}", menuId, itemId))));
            EmojiWindowNative.SetPopupMenuCallback(popup, callback);

            IntPtr edit = app.EditBox(24, 72, 320, 38, "在这里右键试试");
            EmojiWindowNative.BindControlMenu(edit, popup);

            int button = app.Button(24, 132, 180, 36, "直接显示弹出菜单", "📋", DemoColors.Blue, () =>
            {
                EmojiWindowNative.ShowContextMenu(popup, 120, 180);
                app.SetStatus("已主动显示弹出菜单");
            });
            EmojiWindowNative.BindButtonMenu(app.Window, button, popup);
        }

        private static void BuildProgressBarDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowProgressBarDemo - C# x64", 760, 320, DemoColors.Green);
            app.CreateStatusBar("进度条示例");

            IntPtr progress = EmojiWindowNative.CreateProgressBar(app.Window, 24, 72, 520, 30, 35, DemoColors.Blue, DemoColors.LightBlue, 1, DemoColors.Black);
            var callback = app.Pin(new EmojiWindowNative.ProgressBarCallback((handle, value) => app.SetStatus("当前进度：" + value + "%")));
            EmojiWindowNative.SetProgressBarCallback(progress, callback);

            app.Button(24, 126, 120, 36, "25%", "🔹", DemoColors.Blue, () => EmojiWindowNative.SetProgressValue(progress, 25));
            app.Button(158, 126, 120, 36, "75%", "🔷", DemoColors.Green, () => EmojiWindowNative.SetProgressValue(progress, 75));
            app.Button(292, 126, 140, 36, "不确定模式", "⏳", DemoColors.Orange, () =>
            {
                EmojiWindowNative.SetProgressIndeterminate(progress, 1);
                app.SetStatus("已切换到不确定模式");
            });
            app.Button(446, 126, 120, 36, "读取值", "📖", DemoColors.Gray, () => app.SetStatus("当前值：" + EmojiWindowNative.GetProgressValue(progress) + "%"));
        }

        private static void BuildRadioButtonDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowRadioButtonDemo - C# x64", 760, 380, DemoColors.Blue);
            app.CreateStatusBar("单选按钮示例");

            IntPtr r1 = EmojiWindowNative.CreateRadioButton(app.Window, 24, 72, 220, 34, app.U("标签页模式"), app.U("标签页模式").Length, 1, 1, DemoColors.Black, DemoColors.Transparent, app.U("微软雅黑"), app.U("微软雅黑").Length, 13, 0, 0, 0);
            IntPtr r2 = EmojiWindowNative.CreateRadioButton(app.Window, 24, 112, 220, 34, app.U("单窗口模式"), app.U("单窗口模式").Length, 1, 0, DemoColors.Black, DemoColors.Transparent, app.U("微软雅黑"), app.U("微软雅黑").Length, 13, 0, 0, 0);
            IntPtr r3 = EmojiWindowNative.CreateRadioButton(app.Window, 24, 152, 220, 34, app.U("隐私模式"), app.U("隐私模式").Length, 1, 0, DemoColors.Black, DemoColors.Transparent, app.U("微软雅黑"), app.U("微软雅黑").Length, 13, 0, 0, 0);

            var callback = app.Pin(new EmojiWindowNative.RadioButtonCallback((handle, groupId, checkedState) =>
            {
                if (checkedState != 0)
                {
                    app.SetStatus("当前模式：" + EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetRadioButtonText, handle));
                }
            }));
            EmojiWindowNative.SetRadioButtonCallback(r1, callback);
            EmojiWindowNative.SetRadioButtonCallback(r2, callback);
            EmojiWindowNative.SetRadioButtonCallback(r3, callback);

            app.Button(300, 72, 150, 36, "读取当前", "📖", DemoColors.Blue, () =>
            {
                string current = EmojiWindowNative.GetRadioButtonState(r1) != 0 ? EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetRadioButtonText, r1) :
                    EmojiWindowNative.GetRadioButtonState(r2) != 0 ? EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetRadioButtonText, r2) :
                    EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetRadioButtonText, r3);
                app.SetStatus("当前选中：" + current);
            });
        }

        private static void BuildSliderDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowSliderDemo - C# x64", 780, 340, DemoColors.Purple);
            app.CreateStatusBar("滑块示例");

            IntPtr slider = EmojiWindowNative.CreateSlider(app.Window, 24, 82, 420, 36, 0, 100, 35, 5, DemoColors.Blue, DemoColors.LightBlue);
            EmojiWindowNative.SetSliderShowStops(slider, 1);
            EmojiWindowNative.SetSliderColors(slider, DemoColors.Blue, DemoColors.LightBlue, DemoColors.Orange);
            var callback = app.Pin(new EmojiWindowNative.SliderCallback((handle, value) => app.SetStatus("滑块值：" + value)));
            EmojiWindowNative.SetSliderCallback(slider, callback);

            app.Button(24, 150, 120, 36, "设为 0", "⏮️", DemoColors.Gray, () => EmojiWindowNative.SetSliderValue(slider, 0));
            app.Button(158, 150, 120, 36, "设为 50", "⏯️", DemoColors.Blue, () => EmojiWindowNative.SetSliderValue(slider, 50));
            app.Button(292, 150, 120, 36, "设为 100", "⏭️", DemoColors.Green, () => EmojiWindowNative.SetSliderValue(slider, 100));
            app.Button(426, 150, 120, 36, "读取值", "📖", DemoColors.Orange, () => app.SetStatus("当前值：" + EmojiWindowNative.GetSliderValue(slider)));
        }

        private static void BuildSwitchDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowSwitchDemo - C# x64", 760, 320, DemoColors.Cyan);
            app.CreateStatusBar("开关示例");

            IntPtr sw = EmojiWindowNative.CreateSwitch(app.Window, 24, 72, 120, 40, 1, DemoColors.Green, DemoColors.Gray, app.U("开启"), app.U("开启").Length, app.U("关闭"), app.U("关闭").Length);
            var callback = app.Pin(new EmojiWindowNative.SwitchCallback((handle, checkedState) => app.SetStatus(checkedState != 0 ? "当前状态：开启" : "当前状态：关闭")));
            EmojiWindowNative.SetSwitchCallback(sw, callback);

            app.Button(180, 72, 120, 36, "切换状态", "🔁", DemoColors.Blue, () =>
            {
                int current = EmojiWindowNative.GetSwitchState(sw);
                EmojiWindowNative.SetSwitchState(sw, current == 0 ? 1 : 0);
                app.SetStatus("已切换开关状态");
            });

            app.Button(180, 120, 150, 36, "改显示文字", "✏️", DemoColors.Orange, () =>
            {
                EmojiWindowNative.SetSwitchText(sw, app.U("启用"), app.U("启用").Length, app.U("停用"), app.U("停用").Length);
                app.SetStatus("已修改开关文字");
            });
        }

        private static void BuildTabControlDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowTabControlDemo - C# x64", 900, 620, DemoColors.Blue);
            app.CreateStatusBar("TabControl 示例：支持新增、切换、关闭当前页");

            IntPtr tab = EmojiWindowNative.CreateTabControl(app.Window, 24, 80, 840, 460);
            EmojiWindowNative.SetTabItemSize(tab, 140, 38);
            EmojiWindowNative.SetTabPadding(tab, 18, 10);
            EmojiWindowNative.SetTabColors(tab, DemoColors.Blue, DemoColors.Surface, DemoColors.White, DemoColors.Black);
            EmojiWindowNative.SetTabIndicatorColor(tab, DemoColors.Orange);
            EmojiWindowNative.SetTabClosable(tab, 1);
            EmojiWindowNative.SetTabScrollable(tab, 1);
            EmojiWindowNative.SetTabAlignment(tab, 0);

            AddDemoTab(app, tab, "首页");
            AddDemoTab(app, tab, "设置");
            AddDemoTab(app, tab, "收藏");

            var callback = app.Pin(new EmojiWindowNative.TabCallback((handle, selectedIndex) => app.SetStatus("当前切换到第 " + selectedIndex + " 个标签")));
            var closeCallback = app.Pin(new EmojiWindowNative.TabCloseCallback((handle, index) => app.SetStatus("内置关闭按钮关闭了第 " + index + " 个标签")));
            EmojiWindowNative.SetTabCallback(tab, callback);
            EmojiWindowNative.SetTabCloseCallback(tab, closeCallback);
            EmojiWindowNative.SelectTab(tab, 0);

            app.Button(24, 32, 120, 34, "新增标签", "➕", DemoColors.Green, () =>
            {
                int index = AddDemoTab(app, tab, "新标签 " + (EmojiWindowNative.GetTabCount(tab) + 1));
                EmojiWindowNative.SelectTab(tab, index);
                app.SetStatus("已新增并切换到第 " + index + " 个标签");
            });

            app.Button(158, 32, 140, 34, "关闭当前标签", "🗑️", DemoColors.Red, () =>
            {
                int index = EmojiWindowNative.GetCurrentTabIndex(tab);
                if (EmojiWindowNative.GetTabCount(tab) > 1 && index >= 0)
                {
                    EmojiWindowNative.RemoveTabItem(tab, index);
                    app.SetStatus("已关闭第 " + index + " 个标签");
                }
                else
                {
                    app.SetStatus("至少保留一个标签页");
                }
            });

            app.Button(312, 32, 140, 34, "切到下一个", "➡️", DemoColors.Blue, () =>
            {
                int count = EmojiWindowNative.GetTabCount(tab);
                int current = EmojiWindowNative.GetCurrentTabIndex(tab);
                if (count > 0)
                {
                    int next = (current + 1) % count;
                    EmojiWindowNative.SelectTab(tab, next);
                    app.SetStatus("已切换到第 " + next + " 个标签");
                }
            });
        }

        private static int AddDemoTab(DemoApp app, IntPtr tab, string title)
        {
            byte[] titleBytes = app.U(title);
            int index = EmojiWindowNative.AddTabItem(tab, titleBytes, titleBytes.Length, IntPtr.Zero);
            IntPtr page = EmojiWindowNative.GetTabContentWindow(tab, index);
            app.Label(24, 24, 360, 30, title + " 内容区", DemoColors.Black, DemoColors.Transparent, 14, 0, false, page);
            app.Label(24, 64, 520, 60, "这里验证的是 C# x64 下 TabControl 可以正常创建内容窗口、添加标签、切换标签。", DemoColors.Gray, DemoColors.Transparent, 12, 0, true, page);
            return index;
        }

        private static void BuildTooltipDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowTooltipDemo - C# x64", 760, 340, DemoColors.Orange);
            app.CreateStatusBar("Tooltip 示例");

            app.Button(24, 72, 160, 40, "悬停查看提示", "💡", DemoColors.Blue, () => app.SetStatus("按钮被点击"));
            IntPtr edit = app.EditBox(24, 132, 260, 38, "地址栏也绑定了提示");

            IntPtr tip = EmojiWindowNative.CreateTooltip(app.Window, app.U("在这里输入网址并按回车"), app.U("在这里输入网址并按回车").Length, 0, DemoColors.Black, DemoColors.White);
            EmojiWindowNative.SetTooltipTheme(tip, 1);
            EmojiWindowNative.SetTooltipFont(tip, app.U("微软雅黑"), app.U("微软雅黑").Length, 12f);
            EmojiWindowNative.SetTooltipColors(tip, DemoColors.Blue, DemoColors.White, DemoColors.Border);
            EmojiWindowNative.BindTooltipToControl(tip, edit);

            app.Button(220, 72, 140, 40, "主动显示提示", "📍", DemoColors.Green, () =>
            {
                EmojiWindowNative.ShowTooltipForControl(tip, edit);
                app.SetStatus("已主动显示编辑框提示");
            });

            app.Button(374, 72, 120, 40, "隐藏提示", "🙈", DemoColors.Red, () =>
            {
                EmojiWindowNative.HideTooltip(tip);
                app.SetStatus("已隐藏 Tooltip");
            });
        }

        private static void BuildTreeViewDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowTreeViewDemo - C# x64", 860, 520, DemoColors.Green);
            app.CreateStatusBar("TreeView 示例：验证树节点创建与样式接口");

            IntPtr tree = EmojiWindowNative.CreateTreeView(app.Window, 24, 72, 320, 360, DemoColors.White, DemoColors.Black, IntPtr.Zero);
            EmojiWindowNative.SetTreeViewSidebarMode(tree, 1);
            EmojiWindowNative.SetTreeViewRowHeight(tree, 30f);
            EmojiWindowNative.SetTreeViewItemSpacing(tree, 6f);
            EmojiWindowNative.SetTreeViewTextColor(tree, DemoColors.Black);
            EmojiWindowNative.SetTreeViewSelectedBgColor(tree, DemoColors.Blue);
            EmojiWindowNative.SetTreeViewSelectedForeColor(tree, DemoColors.White);
            EmojiWindowNative.SetTreeViewHoverBgColor(tree, DemoColors.Yellow);

            int root1 = EmojiWindowNative.AddRootNode(tree, app.U("工作区"), app.U("工作区").Length, app.U("📁"), app.U("📁").Length);
            int root2 = EmojiWindowNative.AddRootNode(tree, app.U("书签"), app.U("书签").Length, app.U("⭐"), app.U("⭐").Length);
            int child1 = EmojiWindowNative.AddChildNode(tree, root1, app.U("多标签浏览器"), app.U("多标签浏览器").Length, app.U("🌐"), app.U("🌐").Length);
            int child2 = EmojiWindowNative.AddChildNode(tree, root1, app.U("控件示例"), app.U("控件示例").Length, app.U("🧩"), app.U("🧩").Length);
            EmojiWindowNative.AddChildNode(tree, root2, app.U("OpenAI"), app.U("OpenAI").Length, app.U("🤖"), app.U("🤖").Length);
            EmojiWindowNative.SetNodeChecked(tree, child2, 1);
            EmojiWindowNative.ExpandAll(tree);

            app.Button(380, 72, 140, 36, "全部展开", "📂", DemoColors.Blue, () =>
            {
                EmojiWindowNative.ExpandAll(tree);
                app.SetStatus("已展开全部节点");
            });
            app.Button(380, 120, 140, 36, "全部折叠", "📁", DemoColors.Orange, () =>
            {
                EmojiWindowNative.CollapseAll(tree);
                app.SetStatus("已折叠全部节点");
            });
            app.Button(380, 168, 150, 36, "选中“控件示例”", "🎯", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetSelectedNode(tree, child2);
                EmojiWindowNative.ScrollToNode(tree, child2);
                app.SetStatus("已选中“控件示例”");
            });
            app.Button(380, 216, 140, 36, "读取选中节点", "📖", DemoColors.Gray, () =>
            {
                int nodeId = EmojiWindowNative.GetSelectedNode(tree);
                string text = nodeId >= 0 ? ReadTreeNodeText(tree, nodeId) : "(无)";
                app.SetStatus("当前节点：" + text);
            });
            app.Button(380, 264, 160, 36, "改“多标签浏览器”", "✏️", DemoColors.Red, () =>
            {
                byte[] text = app.U("多标签浏览器 Demo");
                EmojiWindowNative.SetNodeText(tree, child1, text, text.Length);
                app.SetStatus("已修改节点文字");
            });
        }

        private static string ReadTreeNodeText(IntPtr tree, int nodeId)
        {
            int size = EmojiWindowNative.GetNodeText(tree, nodeId, IntPtr.Zero, 0);
            if (size <= 0)
            {
                return string.Empty;
            }

            IntPtr buffer = Marshal.AllocHGlobal(size);
            try
            {
                EmojiWindowNative.GetNodeText(tree, nodeId, buffer, size);
                byte[] bytes = new byte[size];
                Marshal.Copy(buffer, bytes, 0, size);
                return EmojiWindowNative.FromUtf8(bytes);
            }
            finally
            {
                Marshal.FreeHGlobal(buffer);
            }
        }

        private static void BuildWindowDemo(DemoApp app)
        {
            app.CreateWindow("EmojiWindowWindowDemo - C# x64", 820, 420, DemoColors.Blue);
            app.CreateStatusBar("窗口示例：标题、大小、标题栏颜色都可以动态修改");

            IntPtr boundsLabel = app.Label(24, 72, 520, 28, "窗口信息将跟随大小变化更新", DemoColors.Black, DemoColors.Transparent, 13);
            UpdateWindowInfo(app, boundsLabel);

            var resizeCallback = app.Pin(new EmojiWindowNative.WindowResizeCallback((hwnd, width, height) =>
            {
                UpdateWindowInfo(app, boundsLabel);
                app.SetStatus(string.Format("窗口大小已变更为 {0} x {1}", width, height));
            }));
            var closeCallback = app.Pin(new EmojiWindowNative.WindowCloseCallback(hwnd => Console.WriteLine("WindowDemo 已收到关闭回调")));
            EmojiWindowNative.SetWindowResizeCallback(resizeCallback);
            EmojiWindowNative.SetWindowCloseCallback(closeCallback);

            app.Button(24, 120, 160, 36, "改窗口标题", "✏️", DemoColors.Blue, () =>
            {
                byte[] title = app.U("已修改标题的窗口 Demo");
                EmojiWindowNative.set_window_title(app.Window, title, title.Length);
                UpdateWindowInfo(app, boundsLabel);
                app.SetStatus("窗口标题已更新");
            });

            app.Button(198, 120, 160, 36, "改标题栏颜色", "🎨", DemoColors.Green, () =>
            {
                EmojiWindowNative.set_window_titlebar_color(app.Window, DemoColors.Purple);
                app.SetStatus("标题栏颜色已切到紫色");
            });

            app.Button(372, 120, 160, 36, "移动并缩放", "📐", DemoColors.Orange, () =>
            {
                EmojiWindowNative.SetWindowBounds(app.Window, 160, 110, 900, 460);
                UpdateWindowInfo(app, boundsLabel);
                app.SetStatus("窗口位置和大小已调整");
            });
        }

        private static void UpdateWindowInfo(DemoApp app, IntPtr label)
        {
            EmojiWindowNative.GetWindowBounds(app.Window, out int x, out int y, out int width, out int height);
            string title = EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetWindowTitle, app.Window);
            byte[] text = app.U(string.Format("标题：{0} | 位置：({1}, {2}) | 大小：{3} x {4}", title, x, y, width, height));
            EmojiWindowNative.SetLabelText(label, text, text.Length);
        }
    }
}
