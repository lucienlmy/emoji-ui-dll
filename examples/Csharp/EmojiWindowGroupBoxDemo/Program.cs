using System;
using EmojiWindowDemoCommon;

namespace EmojiWindowGroupBoxDemo
{
    internal static class Program
    {
        [STAThread]
        private static void Main()
        {
            new GroupBoxDemoApp().Run();
        }
    }

    internal sealed class GroupBoxDemoApp : DemoApp
    {
        private IntPtr _group;
        private IntPtr _groupLabel;
        private IntPtr _groupButtonLabel;
        private int _styleIndex;
        private bool _visible;

        public GroupBoxDemoApp()
            : base("EmojiWindow GroupBox Demo - C# .NET 4.0", 940, 560)
        {
            _visible = true;
        }

        protected override void Build()
        {
            CreateHeader("GroupBox 控件示例", "演示标题、样式、边界以及组内子控件。");

            _group = CreateGroupBox(WindowHandle, "主分组框", 18, 86, 520, 260, ColorPrimary);
            _groupLabel = CreateLabel(_group, "这个标签位于 GroupBox 内部，用于观察样式和布局变化。", 18, 40, 440, 40, ColorText, ColorWhite, 12, false, true, EmojiWindowNative.AlignLeft);
            _groupButtonLabel = CreateLabel(_group, "点击下面的操作按钮可修改标题、样式、颜色和尺寸。", 18, 90, 440, 22, ColorMuted, ColorWhite, 11, false, false, EmojiWindowNative.AlignLeft);
            AddButton(_group, "🧪", "组内按钮", 18, 134, 120, 34, ColorSuccess, delegate { SetStatus("点击了 GroupBox 内按钮。"); });

            IntPtr ops = CreateGroupBox(WindowHandle, "GroupBox 操作", 560, 86, 340, 260, ColorWarning);
            AddButton(ops, "✏️", "改标题", 18, 40, 120, 34, ColorPrimary, RenameGroup);
            AddButton(ops, "🧱", "切样式", 152, 40, 120, 34, ColorSuccess, ToggleStyle);
            AddButton(ops, "🎨", "改标题色", 18, 88, 120, 34, ColorWarning, RecolorTitle);
            AddButton(ops, "📐", "改尺寸", 152, 88, 120, 34, ColorDanger, ResizeGroup);
            AddButton(ops, "👁️", "显隐", 18, 136, 120, 34, ColorPrimary, ToggleVisible);
            AddButton(ops, "📖", "读标题", 152, 136, 120, 34, ColorSuccess, ReadTitle);
        }

        private void RenameGroup()
        {
            byte[] title = U("标题已更新的 GroupBox");
            EmojiWindowNative.SetGroupBoxTitle(_group, title, title.Length);
            SetStatus("GroupBox 标题已更新。");
        }

        private void ToggleStyle()
        {
            _styleIndex = (_styleIndex + 1) % 4;
            EmojiWindowNative.SetGroupBoxStyle(_group, _styleIndex);
            SetStatus("GroupBox style=" + _styleIndex);
        }

        private void RecolorTitle()
        {
            EmojiWindowNative.SetGroupBoxTitleColor(_group, ColorDanger);
            SetStatus("GroupBox 标题色已切到红色。");
        }

        private void ResizeGroup()
        {
            EmojiWindowNative.SetGroupBoxBounds(_group, 18, 86, 600, 300);
            SetStatus("GroupBox 尺寸已放大。");
        }

        private void ToggleVisible()
        {
            _visible = !_visible;
            EmojiWindowNative.ShowGroupBox(_group, _visible);
            SetStatus("主 GroupBox 已" + (_visible ? "显示" : "隐藏"));
        }

        private void ReadTitle()
        {
            SetStatus("当前标题: " + EmojiWindowNative.ReadText(_group, EmojiWindowNative.GetGroupBoxTitle));
        }
    }
}
