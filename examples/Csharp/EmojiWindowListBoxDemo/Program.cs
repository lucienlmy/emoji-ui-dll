using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowListBoxDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new ListBoxDemoApp().Run();
        }
    }

    internal sealed class ListBoxDemoApp : DemoApp
    {
        private IntPtr _listBox;
        private EmojiWindowNative.ListBoxCallback _listCallback;

        public ListBoxDemoApp()
            : base("EmojiWindow ListBox Demo - C# .NET 4.0", 860, 560)
        {
        }

        protected override void Build()
        {
            CreateHeader("ListBox 控件示例", "演示添加、删除、读取、选择和回调。");

            CreateGroupBox(WindowHandle, "ListBox 舞台", 18, 84, 400, 420, ColorPrimary);
            _listBox = EmojiWindowNative.CreateListBox(WindowHandle, 46, 153, 340, 260, false, ColorText, ColorWhite);
            SeedItems();

            _listCallback = new EmojiWindowNative.ListBoxCallback(OnListSelected);
            EmojiWindowNative.SetListBoxCallback(_listBox, _listCallback);

            IntPtr ops = CreateGroupBox(WindowHandle, "ListBox 操作", 438, 84, 380, 420, ColorSuccess);
            AddButton(ops, "➕", "添加项", 18, 46, 110, 34, ColorPrimary, AddItem);
            AddButton(ops, "➖", "删除选中", 142, 46, 110, 34, ColorSuccess, RemoveSelected);
            AddButton(ops, "📖", "读取选中", 18, 94, 110, 34, ColorWarning, ReadSelected);
            AddButton(ops, "🧹", "清空", 142, 94, 110, 34, ColorDanger, ClearItems);
            AddButton(ops, "1️⃣", "选中第一项", 18, 142, 110, 34, ColorPrimary, delegate { EmojiWindowNative.SetSelectedIndex(_listBox, 0); SetStatus("已选中第一项。"); });
            AddButton(ops, "🎨", "改配色", 142, 142, 110, 34, ColorSuccess, delegate { EmojiWindowNative.SetListBoxColors(_listBox, ColorPrimary, ColorCard); SetStatus("ListBox 配色已更新。"); });
        }

        private void SeedItems()
        {
            string[] items = new string[] { "📦 项目列表", "🧪 自动化测试", "🎨 界面优化", "🚀 发布准备" };
            int i;
            for (i = 0; i < items.Length; i++)
            {
                byte[] bytes = U(items[i]);
                EmojiWindowNative.AddListItem(_listBox, bytes, bytes.Length);
            }

            EmojiWindowNative.SetSelectedIndex(_listBox, 0);
        }

        private void AddItem()
        {
            string text = "🆕 新项 " + (EmojiWindowNative.GetListItemCount(_listBox) + 1);
            byte[] bytes = U(text);
            EmojiWindowNative.AddListItem(_listBox, bytes, bytes.Length);
            SetStatus("已添加列表项。");
        }

        private void RemoveSelected()
        {
            int index = EmojiWindowNative.GetSelectedIndex(_listBox);
            if (index >= 0)
            {
                EmojiWindowNative.RemoveListItem(_listBox, index);
                SetStatus("已删除第 " + index + " 项。");
            }
            else
            {
                SetStatus("当前没有选中项。");
            }
        }

        private void ReadSelected()
        {
            int index = EmojiWindowNative.GetSelectedIndex(_listBox);
            if (index >= 0)
            {
                SetStatus("选中项: " + EmojiWindowNative.ReadIndexedText(_listBox, index, EmojiWindowNative.GetListItemText));
            }
            else
            {
                SetStatus("当前没有选中项。");
            }
        }

        private void ClearItems()
        {
            EmojiWindowNative.ClearListBox(_listBox);
            SetStatus("列表已清空。");
        }

        private void OnListSelected(IntPtr hListBox, int index)
        {
            SetStatus("ListBox 回调: index=" + index);
        }
    }
}
