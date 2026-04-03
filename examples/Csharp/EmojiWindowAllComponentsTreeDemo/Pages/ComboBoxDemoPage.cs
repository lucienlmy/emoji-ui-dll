using System;

namespace EmojiWindowDemo
{
    internal static class ComboBoxDemoPage
    {
        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;
            byte[] font = app.U("Microsoft YaHei UI");

            app.GroupBox(16, 16, 980, 520, "普通 ComboBox 舞台区", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(1020, 16, 444, 520, "项目 / 文本 / 颜色 / 状态", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(16, 558, 1448, 220, "ComboBox API 说明", DemoTheme.Border, DemoTheme.Background, page);

            app.Label(40, 56, 930, 24, "这一页只保留普通 ComboBox。左侧分只读和可编辑两种模式，右侧集中操作下方可编辑框。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            app.Label(56, 104, 180, 20, "只读 ComboBox", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            IntPtr readOnlyCombo = EmojiWindowNative.CreateComboBox(page, 56, 128, 560, 38, 1, DemoTheme.Text, DemoTheme.Background, 32, font, font.Length, 13, 0, 0, 0);
            app.Label(56, 212, 180, 20, "可编辑 ComboBox", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            IntPtr editCombo = EmojiWindowNative.CreateComboBox(page, 56, 236, 560, 38, 0, DemoTheme.Text, DemoTheme.Background, 32, font, font.Length, 13, 0, 0, 0);

            string[] readOnlyItems = { "北京", "上海", "深圳", "杭州" };
            string[] editItems = { "默认方案", "主题模式", "紧急文案", "高亮标记" };
            foreach (string item in readOnlyItems)
            {
                byte[] text = app.U(item);
                EmojiWindowNative.AddComboItem(readOnlyCombo, text, text.Length);
            }
            foreach (string item in editItems)
            {
                byte[] text = app.U(item);
                EmojiWindowNative.AddComboItem(editCombo, text, text.Length);
            }

            EmojiWindowNative.SetComboSelectedIndex(readOnlyCombo, 1);
            EmojiWindowNative.SetComboSelectedIndex(editCombo, 1);
            EmojiWindowNative.SetComboBoxColors(readOnlyCombo, DemoTheme.Text, DemoTheme.Background, DemoTheme.SurfacePrimary, DemoTheme.Surface);
            EmojiWindowNative.SetComboBoxColors(editCombo, DemoTheme.Text, DemoTheme.Background, DemoTheme.SurfacePrimary, DemoTheme.Surface);

            app.Label(56, 292, 900, 38, "只读框用于对照模式；右侧操作默认作用于下方可编辑 ComboBox。你手动选择或输入后，读数区会同步刷新。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr readout = app.Label(40, 348, 920, 96, "等待读取 ComboBox 状态。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr state = app.Label(40, 470, 920, 22, "组合框页面状态会显示在这里。", DemoTheme.Primary, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            int editX = 56;
            int editY = 236;
            int editW = 560;
            int editH = 38;
            int nextItemId = 1;
            bool editEnabled = true;
            string editColorMode = "theme";

            string ReadItemText(IntPtr combo, int index)
            {
                if (index < 0)
                {
                    return "(无选中)";
                }

                return EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetComboItemText, combo, index);
            }

            void ApplyEditColors()
            {
                switch (editColorMode)
                {
                    case "cool":
                        EmojiWindowNative.SetComboBoxColors(editCombo, DemoTheme.Primary, DemoTheme.SurfacePrimary, DemoTheme.Primary, DemoTheme.Surface);
                        break;
                    case "warm":
                        EmojiWindowNative.SetComboBoxColors(editCombo, DemoTheme.Warning, DemoTheme.SurfaceWarning, DemoTheme.Warning, DemoTheme.Surface);
                        break;
                    default:
                        EmojiWindowNative.SetComboBoxColors(editCombo, DemoTheme.Text, DemoTheme.Background, DemoTheme.SurfacePrimary, DemoTheme.Surface);
                        break;
                }
            }

            void Refresh(string note)
            {
                EmojiWindowNative.GetComboBoxColors(readOnlyCombo, out uint roFg, out uint roBg, out uint roSel, out uint roHover);
                EmojiWindowNative.GetComboBoxColors(editCombo, out uint edFg, out uint edBg, out uint edSel, out uint edHover);

                int roIndex = EmojiWindowNative.GetComboSelectedIndex(readOnlyCombo);
                int edIndex = EmojiWindowNative.GetComboSelectedIndex(editCombo);
                int roCount = EmojiWindowNative.GetComboItemCount(readOnlyCombo);
                int edCount = EmojiWindowNative.GetComboItemCount(editCombo);
                string editVisible = Win32Native.IsWindowVisible(editCombo) ? "显示" : "隐藏";
                string enabledText = editEnabled ? "启用" : "禁用";

                shell.SetLabelText(
                    readout,
                    $"只读: count={roCount} selected={roIndex} selected_text={ReadItemText(readOnlyCombo, roIndex)} text={EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetComboBoxText, readOnlyCombo)}\r\n" +
                    $"编辑: count={edCount} selected={edIndex} selected_text={ReadItemText(editCombo, edIndex)} text={EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetComboBoxText, editCombo)}\r\n" +
                    $"编辑 bounds=({editX}, {editY}, {editW}, {editH}) {editVisible}/{enabledText} fg/bg={PageCommon.FormatColor(edFg)}/{PageCommon.FormatColor(edBg)} select/hover={PageCommon.FormatColor(edSel)}/{PageCommon.FormatColor(edHover)}\r\n" +
                    $"只读 fg/bg={PageCommon.FormatColor(roFg)}/{PageCommon.FormatColor(roBg)} select/hover={PageCommon.FormatColor(roSel)}/{PageCommon.FormatColor(roHover)}");
                shell.SetLabelText(state, note);
                shell.SetStatus(note);
            }

            void RestoreItems()
            {
                EmojiWindowNative.ClearComboBox(editCombo);
                foreach (string item in editItems)
                {
                    byte[] text = app.U(item);
                    EmojiWindowNative.AddComboItem(editCombo, text, text.Length);
                }
                EmojiWindowNative.SetComboSelectedIndex(editCombo, 1);
            }

            var callback = app.Pin(new EmojiWindowNative.ComboBoxCallback((handle, index) =>
            {
                string text = index >= 0 ? EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetComboItemText, handle, index) : "(无选中)";
                Refresh("ComboBox 回调: " + text);
            }));
            EmojiWindowNative.SetComboBoxCallback(readOnlyCombo, callback);
            EmojiWindowNative.SetComboBoxCallback(editCombo, callback);

            app.Label(1044, 56, 220, 22, "只读框导航", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Button(1044, 94, 116, 34, "第 1 项", "1", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetComboSelectedIndex(readOnlyCombo, 0);
                Refresh("只读 ComboBox 已选中第 1 项");
            }, page);
            app.Button(1172, 94, 116, 34, "第 3 项", "3", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetComboSelectedIndex(readOnlyCombo, 2);
                Refresh("只读 ComboBox 已选中第 3 项");
            }, page);
            app.Button(1300, 94, 124, 34, "读取选中", "i", DemoColors.Gray, () => Refresh("已读取只读 ComboBox 状态"), page);

            app.Label(1044, 148, 220, 22, "编辑框项目", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Button(1044, 182, 116, 34, "新增项目", "+", DemoColors.Green, () =>
            {
                string value = "新增项目 " + nextItemId++;
                byte[] text = app.U(value);
                EmojiWindowNative.AddComboItem(editCombo, text, text.Length);
                EmojiWindowNative.SetComboSelectedIndex(editCombo, EmojiWindowNative.GetComboItemCount(editCombo) - 1);
                Refresh("可编辑 ComboBox 已新增项目");
            }, page);
            app.Button(1172, 182, 116, 34, "删除末项", "-", DemoColors.Red, () =>
            {
                int count = EmojiWindowNative.GetComboItemCount(editCombo);
                if (count > 0)
                {
                    EmojiWindowNative.RemoveComboItem(editCombo, count - 1);
                    if (EmojiWindowNative.GetComboItemCount(editCombo) > 0)
                    {
                        EmojiWindowNative.SetComboSelectedIndex(editCombo, Math.Max(0, EmojiWindowNative.GetComboItemCount(editCombo) - 1));
                    }
                    Refresh("可编辑 ComboBox 已删除最后一项");
                }
                else
                {
                    Refresh("可编辑 ComboBox 当前没有可删除的项目");
                }
            }, page);
            app.Button(1300, 182, 124, 34, "恢复列表", "R", DemoColors.Blue, () =>
            {
                RestoreItems();
                Refresh("可编辑 ComboBox 列表已恢复默认");
            }, page);

            app.Label(1044, 236, 220, 22, "文本与配色", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Button(1044, 270, 116, 34, "写入网址", "U", DemoColors.Orange, () =>
            {
                byte[] text = app.U("https://emoji-window.demo/tree");
                EmojiWindowNative.SetComboBoxText(editCombo, text, text.Length);
                Refresh("可编辑 ComboBox 已写入树形页地址");
            }, page);
            app.Button(1172, 270, 116, 34, "蓝色方案", "B", DemoColors.Blue, () =>
            {
                editColorMode = "cool";
                ApplyEditColors();
                Refresh("可编辑 ComboBox 已切到蓝色方案");
            }, page);
            app.Button(1300, 270, 124, 34, "暖色方案", "W", DemoColors.Orange, () =>
            {
                editColorMode = "warm";
                ApplyEditColors();
                Refresh("可编辑 ComboBox 已切到暖色方案");
            }, page);

            app.Label(1044, 324, 220, 22, "布局与状态", DemoTheme.Text, DemoTheme.Background, 14, PageCommon.AlignLeft, false, page);
            app.Button(1044, 358, 116, 34, "右移 80", ">", DemoColors.Green, () =>
            {
                editX = 136;
                EmojiWindowNative.SetComboBoxBounds(editCombo, editX, editY, editW, editH);
                Refresh("可编辑 ComboBox 已整体右移");
            }, page);
            app.Button(1172, 358, 116, 34, "改宽 420", "W", DemoColors.Gray, () =>
            {
                editW = 420;
                EmojiWindowNative.SetComboBoxBounds(editCombo, editX, editY, editW, editH);
                Refresh("可编辑 ComboBox 宽度已改为 420");
            }, page);
            app.Button(1300, 358, 124, 34, "禁用/启用", "E", DemoColors.Purple, () =>
            {
                editEnabled = !editEnabled;
                EmojiWindowNative.EnableComboBox(editCombo, editEnabled ? 1 : 0);
                Refresh("可编辑 ComboBox 启用状态已切换");
            }, page);
            app.Button(1044, 402, 116, 34, "显示/隐藏", "V", DemoColors.Gray, () =>
            {
                EmojiWindowNative.ShowComboBox(editCombo, Win32Native.IsWindowVisible(editCombo) ? 0 : 1);
                Refresh("可编辑 ComboBox 可见状态已切换");
            }, page);
            app.Button(1172, 402, 252, 34, "恢复布局与主题色", "T", DemoColors.Blue, () =>
            {
                editX = 56;
                editY = 236;
                editW = 560;
                editH = 38;
                editEnabled = true;
                editColorMode = "theme";
                EmojiWindowNative.SetComboBoxBounds(editCombo, editX, editY, editW, editH);
                EmojiWindowNative.ShowComboBox(editCombo, 1);
                EmojiWindowNative.EnableComboBox(editCombo, 1);
                ApplyEditColors();
                Refresh("可编辑 ComboBox 布局与主题色已恢复");
            }, page);

            app.Label(40, 582, 1320, 24, "1. GetComboItemCount / GetComboSelectedIndex / GetComboItemText / GetComboBoxText：读取项目数、选中项、选中文本和当前文本。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 616, 1320, 24, "2. AddComboItem / RemoveComboItem / ClearComboBox：直接操作下拉项目列表。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 650, 1320, 24, "3. SetComboBoxText / SetComboSelectedIndex：修改输入区文本并切换选中项。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 684, 1320, 24, "4. SetComboBoxColors / GetComboBoxColors / SetComboBoxBounds：切换颜色方案并调整布局。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 718, 1320, 24, "5. EnableComboBox / ShowComboBox：演示启用态和可见态切换；启用状态在页面侧显式维护。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            void ApplyTheme()
            {
                EmojiWindowNative.SetComboBoxColors(readOnlyCombo, DemoTheme.Text, DemoTheme.Background, DemoTheme.SurfacePrimary, DemoTheme.Surface);
                if (editColorMode == "theme")
                {
                    ApplyEditColors();
                }
            }

            shell.RegisterPageThemeHandler(page, ApplyTheme);
            ApplyTheme();
            Refresh("ComboBox 页面已重排，可直接测试项目、文本、颜色和状态。");
        }
    }
}
