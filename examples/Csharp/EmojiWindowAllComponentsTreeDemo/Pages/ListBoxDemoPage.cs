using System;
using System.Collections.Generic;

namespace EmojiWindowDemo
{
    internal static class ListBoxDemoPage
    {
        public static void Build(AllDemoShell shell, IntPtr page)
        {
            var app = shell.App;

            app.GroupBox(16, 16, 1048, 500, "📋 ListBox 主展示区", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(1080, 16, 384, 500, "🧪 项目 / 选中 / 配色", DemoTheme.Border, DemoTheme.Background, page);
            app.GroupBox(16, 540, 1448, 208, "📘 ListBox API 说明", DemoTheme.Border, DemoTheme.Background, page);

            app.Label(40, 56, 980, 24, "这一页把 ListBox 本体放大为主展示区，重点演示项目列表、选中反馈、配色切换和列表内容修改。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);

            string[] defaultItems =
            {
                "📎 文档中心",
                "🚀 发布任务",
                "🧩 主题切换",
                "🧪 回归测试",
                "🗂️ 资源整理",
                "🧾 组件打包",
                "📄 变更记录",
                "✅ 发布复核"
            };
            var items = new List<string>(defaultItems);
            int generatedItemCounter = items.Count;

            IntPtr list = EmojiWindowNative.CreateListBox(page, 40, 104, 620, 340, 0, DemoTheme.Text, DemoTheme.Background);
            IntPtr readout = app.Label(688, 104, 340, 184, "等待读取列表框属性。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);
            IntPtr stateLabel = app.Label(40, 470, 920, 24, "ListBox 页状态会显示在这里。", DemoTheme.Primary, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(688, 304, 340, 46, "左侧直接展示更大的列表区，便于验证滚动、选中高亮、可见项目数量和真实组件观感。", DemoTheme.Muted, DemoTheme.Background, 12, PageCommon.AlignLeft, true, page);

            bool enabled = true;

            void ReloadItems(int selectedIndex)
            {
                int currentCount = EmojiWindowNative.GetListItemCount(list);
                for (int i = currentCount - 1; i >= 0; i--)
                {
                    EmojiWindowNative.RemoveListItem(list, i);
                }

                foreach (string item in items)
                {
                    byte[] text = app.U(item);
                    EmojiWindowNative.AddListItem(list, text, text.Length);
                }

                if (items.Count > 0)
                {
                    int safeIndex = Math.Max(0, Math.Min(selectedIndex, items.Count - 1));
                    EmojiWindowNative.SetSelectedIndex(list, safeIndex);
                }
            }

            void Refresh(string note)
            {
                int index = EmojiWindowNative.GetSelectedIndex(list);
                int count = EmojiWindowNative.GetListItemCount(list);
                string text = index >= 0 ? EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetListItemText, list, index) : "(无选中)";
                shell.SetLabelText(readout, $"count={count}  selected={index}\r\nselected_text={text}\r\nenabled={enabled}\r\n{note}");
                shell.SetLabelText(stateLabel, note);
                shell.SetStatus(note);
            }

            void RestoreAll()
            {
                items.Clear();
                items.AddRange(defaultItems);
                generatedItemCounter = items.Count;
                enabled = true;
                EmojiWindowNative.EnableListBox(list, 1);
                EmojiWindowNative.SetListBoxColors(list, DemoTheme.Text, DemoTheme.Background, DemoTheme.SurfacePrimary, DemoTheme.Surface);
                ReloadItems(1);
                Refresh("ListBox 页面已恢复默认状态");
            }

            var callback = app.Pin(new EmojiWindowNative.ListBoxCallback((handle, index) =>
            {
                string text = index >= 0 ? EmojiWindowNative.ReadUtf8(EmojiWindowNative.GetListItemText, handle, index) : "(无选中)";
                Refresh("ListBox 回调: " + text);
            }));
            EmojiWindowNative.SetListBoxCallback(list, callback);

            ReloadItems(1);
            EmojiWindowNative.SetListBoxColors(list, DemoTheme.Text, DemoTheme.Background, DemoTheme.SurfacePrimary, DemoTheme.Surface);

            app.Button(1104, 94, 116, 34, "新增一项", "➕", DemoColors.Green, () =>
            {
                generatedItemCounter++;
                items.Add("🆕 新增项目 " + generatedItemCounter);
                ReloadItems(items.Count - 1);
                Refresh("已向 ListBox 新增一项");
            }, page);
            app.Button(1232, 94, 116, 34, "读取选中", "📖", DemoColors.Blue, () => Refresh("已读取当前选中项"), page);
            app.Button(1360, 94, 80, 34, "第 3 项", "3", DemoColors.Orange, () =>
            {
                if (items.Count == 0)
                {
                    Refresh("当前没有可选项目");
                    return;
                }

                EmojiWindowNative.SetSelectedIndex(list, Math.Min(2, items.Count - 1));
                Refresh("程序已选中第 3 项");
            }, page);

            app.Button(1104, 138, 116, 34, "删除选中", "🗑", DemoColors.Red, () =>
            {
                int index = EmojiWindowNative.GetSelectedIndex(list);
                if (index < 0 || index >= items.Count)
                {
                    Refresh("请先选中一项");
                    return;
                }

                items.RemoveAt(index);
                ReloadItems(Math.Min(index, items.Count - 1));
                Refresh("已删除当前选中项");
            }, page);
            app.Button(1232, 138, 116, 34, "蓝色方案", "💙", DemoColors.Blue, () =>
            {
                EmojiWindowNative.SetListBoxColors(list, DemoTheme.Text, DemoTheme.Background, DemoTheme.SurfacePrimary, DemoTheme.Surface);
                Refresh("ListBox 已切到蓝色方案");
            }, page);
            app.Button(1360, 138, 80, 34, "暖色", "🟠", DemoColors.Orange, () =>
            {
                EmojiWindowNative.SetListBoxColors(list, DemoTheme.Text, DemoTheme.Background, DemoTheme.SurfaceWarning, DemoTheme.Surface);
                Refresh("ListBox 已切到暖色方案");
            }, page);

            app.Button(1104, 182, 116, 34, "改选中项", "✏️", DemoColors.Purple, () =>
            {
                int index = EmojiWindowNative.GetSelectedIndex(list);
                if (index < 0 || index >= items.Count)
                {
                    Refresh("请先选中一项再修改");
                    return;
                }

                items[index] = "✏️ 已修改 " + (index + 1);
                ReloadItems(index);
                Refresh("已修改当前选中项文本");
            }, page);
            app.Button(1232, 182, 116, 34, "顶部插入", "⬆️", DemoColors.Green, () =>
            {
                generatedItemCounter++;
                items.Insert(0, "📌 顶部插入项 " + generatedItemCounter);
                ReloadItems(0);
                Refresh("已在顶部插入一个新项目");
            }, page);
            app.Button(1360, 182, 80, 34, "末项改名", "📝", DemoColors.Gray, () =>
            {
                if (items.Count == 0)
                {
                    Refresh("当前没有可修改的项目");
                    return;
                }

                items[items.Count - 1] = "🧾 末项已改名";
                ReloadItems(items.Count - 1);
                Refresh("已修改最后一项文本");
            }, page);

            app.Button(1104, 226, 116, 34, "禁用/启用", "🚫", DemoColors.Gray, () =>
            {
                enabled = !enabled;
                EmojiWindowNative.EnableListBox(list, enabled ? 1 : 0);
                Refresh("ListBox 启用状态已切换");
            }, page);
            app.Button(1232, 226, 116, 34, "刷新主题", "🎨", DemoColors.Green, () =>
            {
                EmojiWindowNative.SetListBoxColors(list, DemoTheme.Text, DemoTheme.Background, DemoTheme.SurfacePrimary, DemoTheme.Surface);
                Refresh("ListBox 配色已按主题刷新");
            }, page);
            app.Button(1360, 226, 80, 34, "恢复", "↩", DemoColors.Blue, RestoreAll, page);

            app.Label(40, 576, 1320, 22, "1. AddListItem / RemoveListItem / GetListItemCount：操作列表项目。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 610, 1320, 22, "2. GetSelectedIndex / SetSelectedIndex / GetListItemText：读取和设置当前选中项。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);
            app.Label(40, 644, 1320, 22, "3. SetListBoxCallback / SetListBoxColors / EnableListBox：处理回调、配色和启用状态。", DemoTheme.Text, DemoTheme.Background, 12, PageCommon.AlignLeft, false, page);

            void ApplyTheme()
            {
                EmojiWindowNative.SetListBoxColors(list, DemoTheme.Text, DemoTheme.Background, DemoTheme.SurfacePrimary, DemoTheme.Surface);
            }

            shell.RegisterPageThemeHandler(page, ApplyTheme);
            ApplyTheme();
            Refresh("ListBox 页面已重排，可直接测试项目、选中、配色和内容修改。");
        }
    }
}
