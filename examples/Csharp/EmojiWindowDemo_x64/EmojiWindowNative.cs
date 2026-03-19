using System;
using System.Runtime.InteropServices;
using System.Text;

namespace EmojiWindowDemo
{
    /// <summary>emoji_window.dll P/Invoke 声明（64位版本，综合示例 v2）</summary>
    public static class EmojiWindowNative
    {
        private const string DLL = "emoji_window.dll";
        private const CallingConvention CC = CallingConvention.StdCall;

        #region 辅助方法

        public static byte[] ToUtf8(string s) => string.IsNullOrEmpty(s) ? Array.Empty<byte>() : Encoding.UTF8.GetBytes(s);
        public static uint ARGB(int a, int r, int g, int b) => (uint)((a << 24) | (r << 16) | (g << 8) | b);
        public static int RGB(int r, int g, int b) => (r << 16) | (g << 8) | b;

        public static string ArgbStr(uint c)
        {
            int a = (int)(c >> 24) & 0xFF, r = (int)(c >> 16) & 0xFF, g = (int)(c >> 8) & 0xFF, b2 = (int)c & 0xFF;
            return $"ARGB({a},{r},{g},{b2})";
        }

        public delegate int GetTextIntDelegate(int handle, IntPtr buf, int bufSize);
        public static (byte[] data, int length) GetText2Call(GetTextIntDelegate func, int handle)
        {
            int len = func(handle, IntPtr.Zero, 0);
            if (len <= 0) return (Array.Empty<byte>(), len);
            IntPtr buf = Marshal.AllocHGlobal(len);
            try { func(handle, buf, len); byte[] data = new byte[len]; Marshal.Copy(buf, data, 0, len); return (data, len); }
            finally { Marshal.FreeHGlobal(buf); }
        }

        public delegate int GetTextPtrDelegate(IntPtr handle, IntPtr buf, int bufSize);
        public static (byte[] data, int length) GetText2CallPtr(GetTextPtrDelegate func, IntPtr handle)
        {
            int len = func(handle, IntPtr.Zero, 0);
            if (len <= 0) return (Array.Empty<byte>(), len);
            IntPtr buf = Marshal.AllocHGlobal(len);
            try { func(handle, buf, len); byte[] data = new byte[len]; Marshal.Copy(buf, data, 0, len); return (data, len); }
            finally { Marshal.FreeHGlobal(buf); }
        }

        public delegate int GetFontDelegate(int handle, IntPtr buf, int bufSize, out int fontSize, out int bold, out int italic, out int underline);
        public static (string fontName, int fontSize, bool bold, bool italic, bool underline) GetFont2Call(GetFontDelegate func, int handle)
        {
            int fs, b, it, ul;
            int nameLen = func(handle, IntPtr.Zero, 0, out fs, out b, out it, out ul);
            if (nameLen <= 0) return ("(unknown)", fs, b != 0, it != 0, ul != 0);
            IntPtr buf = Marshal.AllocHGlobal(nameLen);
            try { func(handle, buf, nameLen, out fs, out b, out it, out ul);
                  byte[] data = new byte[nameLen]; Marshal.Copy(buf, data, 0, nameLen);
                  return (Encoding.UTF8.GetString(data), fs, b != 0, it != 0, ul != 0); }
            finally { Marshal.FreeHGlobal(buf); }
        }

        public delegate int GetTabTitleDelegate(IntPtr handle, int index, IntPtr buf, int bufSize);
        public static (byte[] data, int length) GetTabTitle2Call(GetTabTitleDelegate func, IntPtr handle, int index)
        {
            int len = func(handle, index, IntPtr.Zero, 0);
            if (len <= 0) return (Array.Empty<byte>(), len);
            IntPtr buf = Marshal.AllocHGlobal(len);
            try { func(handle, index, buf, len); byte[] data = new byte[len]; Marshal.Copy(buf, data, 0, len); return (data, len); }
            finally { Marshal.FreeHGlobal(buf); }
        }

        public delegate int GetItemTextDelegate(int handle, int index, IntPtr buf, int bufSize);
        public static (byte[] data, int length) GetItemText2Call(GetItemTextDelegate func, int handle, int index)
        {
            int len = func(handle, index, IntPtr.Zero, 0);
            if (len <= 0) return (Array.Empty<byte>(), len);
            IntPtr buf = Marshal.AllocHGlobal(len);
            try { func(handle, index, buf, len); byte[] data = new byte[len]; Marshal.Copy(buf, data, 0, len); return (data, len); }
            finally { Marshal.FreeHGlobal(buf); }
        }

        // ComboBox text helper: GetComboBoxText(handle, buf, bufSize)
        public delegate int GetComboTextDelegate(int handle, IntPtr buf, int bufSize);
        public static (byte[] data, int length) GetComboText2Call(GetComboTextDelegate func, int handle)
        {
            int len = func(handle, IntPtr.Zero, 0);
            if (len <= 0) return (Array.Empty<byte>(), len);
            IntPtr buf = Marshal.AllocHGlobal(len);
            try { func(handle, buf, len); byte[] data = new byte[len]; Marshal.Copy(buf, data, 0, len); return (data, len); }
            finally { Marshal.FreeHGlobal(buf); }
        }

        public delegate int GetCellTextDelegate(int grid, int row, int col, IntPtr buf, int bufSize);
        public static (byte[] data, int length) GetCellText2Call(GetCellTextDelegate func, int grid, int row, int col)
        {
            int len = func(grid, row, col, IntPtr.Zero, 0);
            if (len <= 0) return (Array.Empty<byte>(), len);
            IntPtr buf = Marshal.AllocHGlobal(len);
            try { func(grid, row, col, buf, len); byte[] data = new byte[len]; Marshal.Copy(buf, data, 0, len); return (data, len); }
            finally { Marshal.FreeHGlobal(buf); }
        }

        #endregion

        #region 回调委托
        [UnmanagedFunctionPointer(CC)] public delegate void ButtonClickCallback(int buttonId, IntPtr parentHwnd);
        [UnmanagedFunctionPointer(CC)] public delegate void MessageBoxCallback(int confirmed);
        [UnmanagedFunctionPointer(CC)] public delegate void CheckBoxCallback(int checkBoxId, int isChecked);
        [UnmanagedFunctionPointer(CC)] public delegate void ListBoxCallback(int hListBox, int index);
        [UnmanagedFunctionPointer(CC)] public delegate void ComboBoxCallback(int hComboBox, int index);
        [UnmanagedFunctionPointer(CC)] public delegate void DataGridCellCallback(int hGrid, int row, int col);
        [UnmanagedFunctionPointer(CC)] public delegate void DataGridColumnHeaderCallback(int hGrid, int col);
        #endregion

        #region 窗口
        [DllImport(DLL, CallingConvention = CC)] public static extern IntPtr create_window_bytes(byte[] title, int titleLen, int w, int h);
        [DllImport(DLL, CallingConvention = CC)] public static extern IntPtr create_window_bytes_ex(byte[] title, int titleLen, int w, int h, uint titlebarColor, uint clientBgColor);
        [DllImport(DLL, CallingConvention = CC)] public static extern void set_message_loop_main_window(IntPtr hwnd);
        [DllImport(DLL, CallingConvention = CC)] public static extern int run_message_loop();
        [DllImport(DLL, CallingConvention = CC)] public static extern void destroy_window(IntPtr hwnd);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetWindowTitle(IntPtr hwnd, IntPtr buf, int bufSize);
        [DllImport(DLL, CallingConvention = CC)] public static extern void GetWindowBounds(IntPtr hwnd, out int x, out int y, out int w, out int h);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetWindowTitlebarColor(IntPtr hwnd);
        #endregion

        #region 按钮
        [DllImport(DLL, CallingConvention = CC)] public static extern int create_emoji_button_bytes(IntPtr parent, byte[] emoji, int emojiLen, byte[] text, int textLen, int x, int y, int w, int h, uint bgColor);
        [DllImport(DLL, CallingConvention = CC)] public static extern void set_button_click_callback(ButtonClickCallback cb);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetButtonText(int btnId, IntPtr buf, int bufSize);
        [DllImport(DLL, CallingConvention = CC)] public static extern void SetButtonText(int btnId, byte[] text, int textLen);
        [DllImport(DLL, CallingConvention = CC)] public static extern void GetButtonBounds(int btnId, out int x, out int y, out int w, out int h);
        [DllImport(DLL, CallingConvention = CC)] public static extern void SetButtonBackgroundColor(int btnId, uint color);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetButtonVisible(int btnId);
        [DllImport(DLL, CallingConvention = CC)] public static extern void ShowButton(int btnId, int visible);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetButtonEnabled(int btnId);
        [DllImport(DLL, CallingConvention = CC)] public static extern void SetButtonEmoji(int btnId, byte[] emoji, int emojiLen);
        #endregion

        #region 标签
        [DllImport(DLL, CallingConvention = CC)] public static extern int CreateLabel(IntPtr parent, int x, int y, int w, int h, byte[] text, int textLen, uint fg, uint bg, byte[] font, int fontLen, int fontSize, int bold, int italic, int underline, int align, int wordWrap);
        [DllImport(DLL, CallingConvention = CC)] public static extern void SetLabelText(int label, byte[] text, int textLen);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetLabelText(int label, IntPtr buf, int bufSize);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetLabelFont(int label, IntPtr buf, int bufSize, out int fontSize, out int bold, out int italic, out int underline);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetLabelColor(int label, out uint fg, out uint bg);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetLabelBounds(int label, out int x, out int y, out int w, out int h);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetLabelAlignment(int label);
        #endregion

        #region 复选框
        [DllImport(DLL, CallingConvention = CC)] public static extern int CreateCheckBox(IntPtr parent, int x, int y, int w, int h, byte[] text, int textLen, int isChecked, uint fg, uint bg, byte[] font, int fontLen, int fontSize, int bold, int italic, int underline);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetCheckBoxText(int cb, IntPtr buf, int bufSize);
        [DllImport(DLL, CallingConvention = CC)] public static extern void SetCheckBoxCallback(int checkBoxId, CheckBoxCallback cb);
        #endregion

        #region 单选按钮
        [DllImport(DLL, CallingConvention = CC)] public static extern int CreateRadioButton(IntPtr parent, int x, int y, int w, int h, byte[] text, int textLen, int groupId, int isChecked, uint fg, uint bg, byte[] font, int fontLen, int fontSize, int bold, int italic, int underline);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetRadioButtonText(int rb, IntPtr buf, int bufSize);
        #endregion

        #region 编辑框
        [DllImport(DLL, CallingConvention = CC)] public static extern int CreateEditBox(IntPtr parent, int x, int y, int w, int h, byte[] text, int textLen, uint fg, uint bg, byte[] font, int fontLen, int fontSize, int bold, int italic, int underline, int align, int multiline, int readOnly, int password, int showBorder, int vertCenter);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetEditBoxFont(int eb, IntPtr buf, int bufSize, out int fontSize, out int bold, out int italic, out int underline);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetEditBoxColor(int eb, out uint fg, out uint bg);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetEditBoxBounds(int eb, out int x, out int y, out int w, out int h);
        #endregion

        #region 分组框
        [DllImport(DLL, CallingConvention = CC)] public static extern IntPtr CreateGroupBox(IntPtr parent, int x, int y, int w, int h, byte[] title, int titleLen, uint borderColor, uint bg, byte[] font, int fontLen, int fontSize, int bold, int italic, int underline);
        [DllImport(DLL, CallingConvention = CC)] public static extern void AddChildToGroup(IntPtr group, int child);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetGroupBoxTitle(IntPtr group, IntPtr buf, int bufSize);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetGroupBoxBounds(IntPtr group, out int x, out int y, out int w, out int h);
        #endregion

        #region TabControl
        [DllImport(DLL, CallingConvention = CC)] public static extern IntPtr CreateTabControl(IntPtr parent, int x, int y, int w, int h);
        [DllImport(DLL, CallingConvention = CC)] public static extern int AddTabItem(IntPtr tab, byte[] title, int titleLen, int contentHwnd);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetTabCount(IntPtr tab);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetTabTitle(IntPtr tab, int index, IntPtr buf, int bufSize);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetTabControlBounds(IntPtr tab, out int x, out int y, out int w, out int h);
        #endregion

        #region 进度条
        [DllImport(DLL, CallingConvention = CC)] public static extern IntPtr CreateProgressBar(IntPtr parent, int x, int y, int w, int h, int initVal, uint fg, uint bg, int showText, uint textColor);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetProgressBarColor(IntPtr pb, out uint fg, out uint bg);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetProgressBarBounds(IntPtr pb, out int x, out int y, out int w, out int h);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetProgressBarShowText(IntPtr pb);
        #endregion

        #region 列表框
        [DllImport(DLL, CallingConvention = CC)] public static extern int CreateListBox(IntPtr parent, int x, int y, int w, int h, int multiSelect, uint fg, uint bg);
        [DllImport(DLL, CallingConvention = CC)] public static extern int AddListItem(int listbox, byte[] text, int textLen);
        [DllImport(DLL, CallingConvention = CC)] public static extern void RemoveListItem(int listbox, int index);
        [DllImport(DLL, CallingConvention = CC)] public static extern void ClearListBox(int listbox);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetSelectedIndex(int listbox);
        [DllImport(DLL, CallingConvention = CC)] public static extern void SetSelectedIndex(int listbox, int index);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetListItemCount(int listbox);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetListItemText(int listbox, int index, IntPtr buf, int bufSize);
        [DllImport(DLL, CallingConvention = CC)] public static extern void SetListBoxCallback(int listbox, ListBoxCallback cb);
        [DllImport(DLL, CallingConvention = CC)] public static extern void EnableListBox(int listbox, int enable);
        [DllImport(DLL, CallingConvention = CC)] public static extern void ShowListBox(int listbox, int show);
        [DllImport(DLL, CallingConvention = CC)] public static extern void SetListBoxBounds(int listbox, int x, int y, int w, int h);
        #endregion

        #region 组合框
        [DllImport(DLL, CallingConvention = CC)] public static extern int CreateComboBox(IntPtr parent, int x, int y, int w, int h, int readOnly, uint fg, uint bg, int itemHeight, byte[] font, int fontLen, int fontSize, int bold, int italic, int underline);
        [DllImport(DLL, CallingConvention = CC)] public static extern int AddComboItem(int combo, byte[] text, int textLen);
        [DllImport(DLL, CallingConvention = CC)] public static extern void RemoveComboItem(int combo, int index);
        [DllImport(DLL, CallingConvention = CC)] public static extern void ClearComboBox(int combo);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetComboSelectedIndex(int combo);
        [DllImport(DLL, CallingConvention = CC)] public static extern void SetComboSelectedIndex(int combo, int index);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetComboItemCount(int combo);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetComboItemText(int combo, int index, IntPtr buf, int bufSize);
        [DllImport(DLL, CallingConvention = CC)] public static extern int GetComboBoxText(int combo, IntPtr buf, int bufSize);
        [DllImport(DLL, CallingConvention = CC)] public static extern void SetComboBoxText(int combo, byte[] text, int textLen);
        [DllImport(DLL, CallingConvention = CC)] public static extern void SetComboBoxCallback(int combo, ComboBoxCallback cb);
        [DllImport(DLL, CallingConvention = CC)] public static extern void EnableComboBox(int combo, int enable);
        [DllImport(DLL, CallingConvention = CC)] public static extern void ShowComboBox(int combo, int show);
        [DllImport(DLL, CallingConvention = CC)] public static extern void SetComboBoxBounds(int combo, int x, int y, int w, int h);
        #endregion

        #region DataGridView
        [DllImport(DLL, CallingConvention = CC)] public static extern int CreateDataGridView(IntPtr parent, int x, int y, int w, int h, int virtualMode, int alternateRowColor, uint fg, uint bg);
        [DllImport(DLL, CallingConvention = CC)] public static extern int DataGrid_AddTextColumn(int grid, byte[] header, int headerLen, int width);
        [DllImport(DLL, CallingConvention = CC)] public static extern int DataGrid_AddCheckBoxColumn(int grid, byte[] header, int headerLen, int width);
        [DllImport(DLL, CallingConvention = CC)] public static extern int DataGrid_AddButtonColumn(int grid, byte[] header, int headerLen, int width);
        [DllImport(DLL, CallingConvention = CC)] public static extern int DataGrid_AddRow(int grid);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_RemoveRow(int grid, int rowIndex);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_ClearRows(int grid);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetCellText(int grid, int row, int col, byte[] text, int textLen);
        [DllImport(DLL, CallingConvention = CC)] public static extern int DataGrid_GetCellText(int grid, int row, int col, IntPtr buf, int bufSize);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetCellChecked(int grid, int row, int col, int isChecked);
        [DllImport(DLL, CallingConvention = CC)] public static extern int DataGrid_GetCellChecked(int grid, int row, int col);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetCellStyle(int grid, int row, int col, uint fg, uint bg, int bold, int italic);
        [DllImport(DLL, CallingConvention = CC)] public static extern int DataGrid_GetSelectedRow(int grid);
        [DllImport(DLL, CallingConvention = CC)] public static extern int DataGrid_GetSelectedCol(int grid);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetSelectedCell(int grid, int row, int col);
        [DllImport(DLL, CallingConvention = CC)] public static extern int DataGrid_GetRowCount(int grid);
        [DllImport(DLL, CallingConvention = CC)] public static extern int DataGrid_GetColumnCount(int grid);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetSelectionMode(int grid, int mode);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SortByColumn(int grid, int col, int direction);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetShowGridLines(int grid, int show);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetDefaultRowHeight(int grid, int height);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetHeaderHeight(int grid, int height);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetColumnWidth(int grid, int col, int width);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetFreezeHeader(int grid, int freeze);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetFreezeFirstColumn(int grid, int freeze);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetColumnHeaderAlignment(int grid, int col, int align);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetColumnCellAlignment(int grid, int col, int align);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetCellClickCallback(int grid, DataGridCellCallback cb);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetCellDoubleClickCallback(int grid, DataGridCellCallback cb);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetSelectionChangedCallback(int grid, DataGridCellCallback cb);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetColumnHeaderClickCallback(int grid, DataGridColumnHeaderCallback cb);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetCellValueChangedCallback(int grid, DataGridCellCallback cb);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_Enable(int grid, int enable);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_Show(int grid, int show);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_SetBounds(int grid, int x, int y, int w, int h);
        [DllImport(DLL, CallingConvention = CC)] public static extern void DataGrid_Refresh(int grid);
        #endregion

        #region 信息框
        [DllImport(DLL, CallingConvention = CC)] public static extern void show_message_box_bytes(IntPtr parent, byte[] title, int titleLen, byte[] msg, int msgLen, byte[] icon, int iconLen);
        [DllImport(DLL, CallingConvention = CC)] public static extern void show_confirm_box_bytes(IntPtr parent, byte[] title, int titleLen, byte[] msg, int msgLen, byte[] icon, int iconLen, MessageBoxCallback cb);
        #endregion

    }
}