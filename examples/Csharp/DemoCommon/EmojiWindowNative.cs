using System;
using System.Runtime.InteropServices;
using System.Text;

namespace EmojiWindowDemo
{
    internal static class EmojiWindowNative
    {
        private const string Dll = "emoji_window.dll";
        private const CallingConvention Cc = CallingConvention.StdCall;

        public static byte[] ToUtf8(string text) => string.IsNullOrEmpty(text) ? Array.Empty<byte>() : Encoding.UTF8.GetBytes(text);

        public static string FromUtf8(byte[] bytes)
        {
            if (bytes == null || bytes.Length == 0)
            {
                return string.Empty;
            }

            return Encoding.UTF8.GetString(bytes).TrimEnd('\0');
        }

        public static uint ARGB(int a, int r, int g, int b) => (uint)((a << 24) | (r << 16) | (g << 8) | b);

        public delegate int TextReaderHandle(IntPtr handle, IntPtr buffer, int bufferSize);
        public delegate int TextReaderHandleIndex(IntPtr handle, int index, IntPtr buffer, int bufferSize);
        public delegate int GridTextReader(IntPtr handle, int row, int col, IntPtr buffer, int bufferSize);

        public static string ReadUtf8(TextReaderHandle reader, IntPtr handle)
        {
            int size = reader(handle, IntPtr.Zero, 0);
            if (size <= 0)
            {
                return string.Empty;
            }

            IntPtr buffer = Marshal.AllocHGlobal(size);
            try
            {
                reader(handle, buffer, size);
                byte[] bytes = new byte[size];
                Marshal.Copy(buffer, bytes, 0, size);
                return FromUtf8(bytes);
            }
            finally
            {
                Marshal.FreeHGlobal(buffer);
            }
        }

        public static string ReadUtf8(TextReaderHandleIndex reader, IntPtr handle, int index)
        {
            int size = reader(handle, index, IntPtr.Zero, 0);
            if (size <= 0)
            {
                return string.Empty;
            }

            IntPtr buffer = Marshal.AllocHGlobal(size);
            try
            {
                reader(handle, index, buffer, size);
                byte[] bytes = new byte[size];
                Marshal.Copy(buffer, bytes, 0, size);
                return FromUtf8(bytes);
            }
            finally
            {
                Marshal.FreeHGlobal(buffer);
            }
        }

        public static string ReadUtf8(GridTextReader reader, IntPtr handle, int row, int col)
        {
            int size = reader(handle, row, col, IntPtr.Zero, 0);
            if (size <= 0)
            {
                return string.Empty;
            }

            IntPtr buffer = Marshal.AllocHGlobal(size);
            try
            {
                reader(handle, row, col, buffer, size);
                byte[] bytes = new byte[size];
                Marshal.Copy(buffer, bytes, 0, size);
                return FromUtf8(bytes);
            }
            finally
            {
                Marshal.FreeHGlobal(buffer);
            }
        }

        [UnmanagedFunctionPointer(Cc)] public delegate void ButtonClickCallback(int buttonId, IntPtr parentHwnd);
        [UnmanagedFunctionPointer(Cc)] public delegate void MessageBoxCallback(int confirmed);
        [UnmanagedFunctionPointer(Cc)] public delegate void TabCallback(IntPtr hTabControl, int selectedIndex);
        [UnmanagedFunctionPointer(Cc)] public delegate void TabCloseCallback(IntPtr hTabControl, int index);
        [UnmanagedFunctionPointer(Cc)] public delegate void WindowResizeCallback(IntPtr hwnd, int width, int height);
        [UnmanagedFunctionPointer(Cc)] public delegate void WindowCloseCallback(IntPtr hwnd);
        [UnmanagedFunctionPointer(Cc)] public delegate void MenuItemClickCallback(int menuId, int itemId);
        [UnmanagedFunctionPointer(Cc)] public delegate void EditBoxKeyCallback(IntPtr hEdit, int keyCode, int keyDown, int shift, int ctrl, int alt);
        [UnmanagedFunctionPointer(Cc)] public delegate void CheckBoxCallback(IntPtr hCheckBox, int checkedState);
        [UnmanagedFunctionPointer(Cc)] public delegate void ProgressBarCallback(IntPtr hProgressBar, int value);
        [UnmanagedFunctionPointer(Cc)] public delegate void PictureBoxCallback(IntPtr hPictureBox);
        [UnmanagedFunctionPointer(Cc)] public delegate void RadioButtonCallback(IntPtr hRadioButton, int groupId, int checkedState);
        [UnmanagedFunctionPointer(Cc)] public delegate void SliderCallback(IntPtr hSlider, int value);
        [UnmanagedFunctionPointer(Cc)] public delegate void SwitchCallback(IntPtr hSwitch, int checkedState);
        [UnmanagedFunctionPointer(Cc)] public delegate void NotificationCallback(IntPtr hNotification, int eventType);
        [UnmanagedFunctionPointer(Cc)] public delegate void ListBoxCallback(IntPtr hListBox, int index);
        [UnmanagedFunctionPointer(Cc)] public delegate void ComboBoxCallback(IntPtr hComboBox, int index);
        [UnmanagedFunctionPointer(Cc)] public delegate void HotKeyCallback(IntPtr hHotKey, int vkCode, int modifiers);
        [UnmanagedFunctionPointer(Cc)] public delegate void ValueChangedCallback(IntPtr hwnd);
        [UnmanagedFunctionPointer(Cc)] public delegate void DataGridCellCallback(IntPtr hGrid, int row, int col);
        [UnmanagedFunctionPointer(Cc)] public delegate void DataGridColumnHeaderCallback(IntPtr hGrid, int col);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr create_window_bytes_ex(byte[] title, int titleLen, int x, int y, int width, int height, uint titlebarColor, uint clientBgColor);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void set_message_loop_main_window(IntPtr hwnd);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int run_message_loop();
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetWindowTitle(IntPtr hwnd, IntPtr buffer, int bufferSize);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetWindowBounds(IntPtr hwnd, out int x, out int y, out int width, out int height);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetWindowBounds(IntPtr hwnd, int x, int y, int width, int height);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void set_window_title(IntPtr hwnd, byte[] titleUtf8, int titleLen);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void set_window_titlebar_color(IntPtr hwnd, uint color);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetWindowResizeCallback(WindowResizeCallback callback);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetWindowCloseCallback(WindowCloseCallback callback);

        [DllImport(Dll, CallingConvention = Cc)] public static extern int create_emoji_button_bytes(IntPtr parent, byte[] emoji, int emojiLen, byte[] text, int textLen, int x, int y, int width, int height, uint bgColor);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void set_button_click_callback(ButtonClickCallback callback);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetButtonText(int buttonId, byte[] text, int textLen);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetButtonBackgroundColor(int buttonId, uint color);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetButtonLoading(int buttonId, int loading);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateLabel(IntPtr parent, int x, int y, int width, int height, byte[] text, int textLen, uint fgColor, uint bgColor, byte[] fontName, int fontNameLen, int fontSize, int bold, int italic, int underline, int alignment, int wordWrap);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetLabelText(IntPtr hLabel, byte[] text, int textLen);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetLabelColor(IntPtr hLabel, uint fgColor, uint bgColor);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateEditBox(IntPtr parent, int x, int y, int width, int height, byte[] text, int textLen, uint fgColor, uint bgColor, byte[] fontName, int fontNameLen, int fontSize, int bold, int italic, int underline, int alignment, int multiline, int readOnly, int password, int hasBorder, int verticalCenter);
        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateColorEmojiEditBox(IntPtr parent, int x, int y, int width, int height, byte[] text, int textLen, uint fgColor, uint bgColor, byte[] fontName, int fontNameLen, int fontSize, int bold, int italic, int underline, int alignment, int multiline, int readOnly, int password, int hasBorder, int verticalCenter);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetEditBoxText(IntPtr hEdit, IntPtr buffer, int bufferSize);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetEditBoxText(IntPtr hEdit, byte[] text, int textLen);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetEditBoxKeyCallback(IntPtr hEdit, EditBoxKeyCallback callback);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateCheckBox(IntPtr parent, int x, int y, int width, int height, byte[] text, int textLen, int checkedState, uint fgColor, uint bgColor, byte[] fontName, int fontNameLen, int fontSize, int bold, int italic, int underline);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetCheckBoxState(IntPtr hCheckBox);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetCheckBoxState(IntPtr hCheckBox, int checkedState);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetCheckBoxCallback(IntPtr hCheckBox, CheckBoxCallback callback);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetCheckBoxText(IntPtr hCheckBox, IntPtr buffer, int bufferSize);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateRadioButton(IntPtr parent, int x, int y, int width, int height, byte[] text, int textLen, int groupId, int checkedState, uint fgColor, uint bgColor, byte[] fontName, int fontNameLen, int fontSize, int bold, int italic, int underline);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetRadioButtonState(IntPtr hRadioButton);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetRadioButtonCallback(IntPtr hRadioButton, RadioButtonCallback callback);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetRadioButtonText(IntPtr hRadioButton, IntPtr buffer, int bufferSize);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateProgressBar(IntPtr parent, int x, int y, int width, int height, int initialValue, uint fgColor, uint bgColor, int showText, uint textColor);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetProgressValue(IntPtr hProgressBar, int value);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetProgressValue(IntPtr hProgressBar);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetProgressIndeterminate(IntPtr hProgressBar, int indeterminate);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetProgressBarCallback(IntPtr hProgressBar, ProgressBarCallback callback);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateListBox(IntPtr parent, int x, int y, int width, int height, int multiSelect, uint fgColor, uint bgColor);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int AddListItem(IntPtr hListBox, byte[] text, int textLen);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void RemoveListItem(IntPtr hListBox, int index);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetSelectedIndex(IntPtr hListBox);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetSelectedIndex(IntPtr hListBox, int index);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetListItemCount(IntPtr hListBox);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetListItemText(IntPtr hListBox, int index, IntPtr buffer, int bufferSize);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetListBoxCallback(IntPtr hListBox, ListBoxCallback callback);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateComboBox(IntPtr parent, int x, int y, int width, int height, int readOnly, uint fgColor, uint bgColor, int itemHeight, byte[] fontName, int fontNameLen, int fontSize, int bold, int italic, int underline);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int AddComboItem(IntPtr hComboBox, byte[] text, int textLen);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetComboSelectedIndex(IntPtr hComboBox);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetComboSelectedIndex(IntPtr hComboBox, int index);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetComboItemText(IntPtr hComboBox, int index, IntPtr buffer, int bufferSize);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetComboBoxText(IntPtr hComboBox, IntPtr buffer, int bufferSize);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetComboBoxText(IntPtr hComboBox, byte[] text, int textLen);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetComboBoxCallback(IntPtr hComboBox, ComboBoxCallback callback);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateMenuBar(IntPtr hWindow);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int MenuBarAddItem(IntPtr hMenuBar, byte[] text, int textLen, int itemId);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int MenuBarAddSubItem(IntPtr hMenuBar, int parentItemId, byte[] text, int textLen, int itemId);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetMenuBarPlacement(IntPtr hMenuBar, int x, int y, int width, int height);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetMenuBarCallback(IntPtr hMenuBar, MenuItemClickCallback callback);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int MenuBarUpdateSubItemText(IntPtr hMenuBar, int parentItemId, int itemId, byte[] text, int textLen);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateEmojiPopupMenu(IntPtr hOwner);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int PopupMenuAddItem(IntPtr hPopupMenu, byte[] text, int textLen, int itemId);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int PopupMenuAddSubItem(IntPtr hPopupMenu, int parentItemId, byte[] text, int textLen, int itemId);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void BindControlMenu(IntPtr hControl, IntPtr hPopupMenu);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void BindButtonMenu(IntPtr hParent, int buttonId, IntPtr hPopupMenu);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void ShowContextMenu(IntPtr hPopupMenu, int x, int y);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetPopupMenuCallback(IntPtr hPopupMenu, MenuItemClickCallback callback);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateGroupBox(IntPtr parent, int x, int y, int width, int height, byte[] title, int titleLen, uint borderColor, uint bgColor, byte[] fontName, int fontNameLen, int fontSize, int bold, int italic, int underline);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetGroupBoxTitle(IntPtr hGroupBox, byte[] title, int titleLen);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetGroupBoxTitleColor(IntPtr hGroupBox, uint titleColor);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetGroupBoxStyle(IntPtr hGroupBox, int style);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateTabControl(IntPtr parent, int x, int y, int width, int height);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int AddTabItem(IntPtr hTabControl, byte[] title, int titleLen, IntPtr hContentWindow);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int RemoveTabItem(IntPtr hTabControl, int index);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetTabCallback(IntPtr hTabControl, TabCallback callback);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetCurrentTabIndex(IntPtr hTabControl);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int SelectTab(IntPtr hTabControl, int index);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetTabCount(IntPtr hTabControl);
        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr GetTabContentWindow(IntPtr hTabControl, int index);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int SetTabItemSize(IntPtr hTabControl, int width, int height);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int SetTabColors(IntPtr hTabControl, uint selectedBg, uint unselectedBg, uint selectedText, uint unselectedText);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int SetTabIndicatorColor(IntPtr hTabControl, uint color);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int SetTabPadding(IntPtr hTabControl, int horizontal, int vertical);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int SetTabClosable(IntPtr hTabControl, int closable);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int SetTabScrollable(IntPtr hTabControl, int scrollable);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int SetTabAlignment(IntPtr hTabControl, int alignment);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int SetTabCloseCallback(IntPtr hTabControl, TabCloseCallback callback);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreatePictureBox(IntPtr parent, int x, int y, int width, int height, int scaleMode, uint bgColor);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int LoadImageFromFile(IntPtr hPictureBox, byte[] filePath, int pathLen);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void ClearImage(IntPtr hPictureBox);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetImageOpacity(IntPtr hPictureBox, float opacity);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetPictureBoxCallback(IntPtr hPictureBox, PictureBoxCallback callback);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetPictureBoxScaleMode(IntPtr hPictureBox, int scaleMode);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateSlider(IntPtr parent, int x, int y, int width, int height, int minValue, int maxValue, int value, int step, uint activeColor, uint bgColor);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetSliderValue(IntPtr hSlider);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetSliderValue(IntPtr hSlider, int value);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetSliderShowStops(IntPtr hSlider, int showStops);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetSliderColors(IntPtr hSlider, uint activeColor, uint bgColor, uint buttonColor);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetSliderCallback(IntPtr hSlider, SliderCallback callback);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateSwitch(IntPtr parent, int x, int y, int width, int height, int checkedState, uint activeColor, uint inactiveColor, byte[] activeText, int activeTextLen, byte[] inactiveText, int inactiveTextLen);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetSwitchState(IntPtr hSwitch);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetSwitchState(IntPtr hSwitch, int checkedState);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetSwitchText(IntPtr hSwitch, byte[] activeText, int activeTextLen, byte[] inactiveText, int inactiveTextLen);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetSwitchCallback(IntPtr hSwitch, SwitchCallback callback);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateTooltip(IntPtr owner, byte[] text, int textLen, int placement, uint bgColor, uint fgColor);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetTooltipTheme(IntPtr hTooltip, int themeMode);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetTooltipColors(IntPtr hTooltip, uint bgColor, uint fgColor, uint borderColor);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetTooltipFont(IntPtr hTooltip, byte[] fontName, int fontNameLen, float fontSize);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void BindTooltipToControl(IntPtr hTooltip, IntPtr hTarget);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void ShowTooltipForControl(IntPtr hTooltip, IntPtr hTarget);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void HideTooltip(IntPtr hTooltip);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr ShowNotification(IntPtr owner, byte[] title, int titleLen, byte[] message, int messageLen, int type, int position, int durationMs);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetNotificationCallback(IntPtr hNotification, NotificationCallback callback);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateD2DComboBox(IntPtr parent, int x, int y, int width, int height, int readOnly, uint fgColor, uint bgColor, int itemHeight, byte[] fontName, int fontNameLen, int fontSize, int bold, int italic, int underline);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int AddD2DComboItem(IntPtr hComboBox, byte[] text, int textLen);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetD2DComboItemText(IntPtr hComboBox, int index, IntPtr buffer, int bufferSize);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetD2DComboText(IntPtr hComboBox, IntPtr buffer, int bufferSize);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetD2DComboText(IntPtr hComboBox, byte[] text, int textLen);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetD2DComboSelectedIndex(IntPtr hComboBox, int index);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetD2DComboBoxCallback(IntPtr hComboBox, ComboBoxCallback callback);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetD2DComboBoxColors(IntPtr hComboBox, uint fgColor, uint bgColor, uint selectColor, uint hoverColor, uint borderColor, uint buttonColor);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateD2DDateTimePicker(IntPtr parent, int x, int y, int width, int height, int initialPrecision, uint fgColor, uint bgColor, uint borderColor, byte[] fontName, int fontNameLen, int fontSize, int bold, int italic, int underline);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void GetD2DDateTimePickerDateTime(IntPtr hPicker, out int year, out int month, out int day, out int hour, out int minute, out int second);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetD2DDateTimePickerDateTime(IntPtr hPicker, int year, int month, int day, int hour, int minute, int second);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetD2DDateTimePickerCallback(IntPtr hPicker, ValueChangedCallback callback);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetD2DDateTimePickerPrecision(IntPtr hPicker, int precision);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateHotKeyControl(IntPtr parent, int x, int y, int width, int height, uint fgColor, uint bgColor);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void GetHotKey(IntPtr hHotKey, out int vkCode, out int modifiers);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetHotKey(IntPtr hHotKey, int vkCode, int modifiers);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void ClearHotKey(IntPtr hHotKey);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetHotKeyCallback(IntPtr hHotKey, HotKeyCallback callback);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetHotKeyColors(IntPtr hHotKey, uint fgColor, uint bgColor, uint borderColor);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreatePanel(IntPtr parent, int x, int y, int width, int height, uint bgColor);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void SetPanelBackgroundColor(IntPtr hPanel, uint bgColor);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetPanelBackgroundColor(IntPtr hPanel, out uint bgColor);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateTreeView(IntPtr parent, int x, int y, int width, int height, uint bgColor, uint textColor, IntPtr callbackContext);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int AddRootNode(IntPtr hTreeView, byte[] text, int textLen, byte[] icon, int iconLen);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int AddChildNode(IntPtr hTreeView, int parentId, byte[] text, int textLen, byte[] icon, int iconLen);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int ExpandAll(IntPtr hTreeView);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int CollapseAll(IntPtr hTreeView);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int SetSelectedNode(IntPtr hTreeView, int nodeId);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetSelectedNode(IntPtr hTreeView);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int SetNodeText(IntPtr hTreeView, int nodeId, byte[] text, int textLen);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int GetNodeText(IntPtr hTreeView, int nodeId, IntPtr buffer, int bufferSize);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int SetNodeChecked(IntPtr hTreeView, int nodeId, int checkedState);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int SetTreeViewSidebarMode(IntPtr hTreeView, int enable);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int SetTreeViewRowHeight(IntPtr hTreeView, float height);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int SetTreeViewItemSpacing(IntPtr hTreeView, float spacing);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int SetTreeViewTextColor(IntPtr hTreeView, uint argb);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int SetTreeViewSelectedBgColor(IntPtr hTreeView, uint argb);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int SetTreeViewSelectedForeColor(IntPtr hTreeView, uint argb);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int SetTreeViewHoverBgColor(IntPtr hTreeView, uint argb);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int ScrollToNode(IntPtr hTreeView, int nodeId);

        [DllImport(Dll, CallingConvention = Cc)] public static extern IntPtr CreateDataGridView(IntPtr parent, int x, int y, int width, int height, int virtualMode, int alternateRowColor, uint fgColor, uint bgColor);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int DataGrid_AddTextColumn(IntPtr hGrid, byte[] header, int headerLen, int width);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int DataGrid_AddCheckBoxColumn(IntPtr hGrid, byte[] header, int headerLen, int width);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int DataGrid_AddButtonColumn(IntPtr hGrid, byte[] header, int headerLen, int width);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int DataGrid_AddRow(IntPtr hGrid);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void DataGrid_RemoveRow(IntPtr hGrid, int rowIndex);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void DataGrid_SetCellText(IntPtr hGrid, int row, int col, byte[] text, int textLen);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int DataGrid_GetCellText(IntPtr hGrid, int row, int col, IntPtr buffer, int bufferSize);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void DataGrid_SetCellChecked(IntPtr hGrid, int row, int col, int checkedState);
        [DllImport(Dll, CallingConvention = Cc)] public static extern int DataGrid_GetSelectedRow(IntPtr hGrid);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void DataGrid_SetSelectionMode(IntPtr hGrid, int mode);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void DataGrid_SortByColumn(IntPtr hGrid, int col, int direction);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void DataGrid_SetShowGridLines(IntPtr hGrid, int show);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void DataGrid_SetDefaultRowHeight(IntPtr hGrid, int height);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void DataGrid_SetHeaderHeight(IntPtr hGrid, int height);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void DataGrid_SetCellClickCallback(IntPtr hGrid, DataGridCellCallback callback);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void DataGrid_SetColumnHeaderClickCallback(IntPtr hGrid, DataGridColumnHeaderCallback callback);

        [DllImport(Dll, CallingConvention = Cc)] public static extern void show_message_box_bytes(IntPtr parent, byte[] title, int titleLen, byte[] message, int messageLen, byte[] icon, int iconLen);
        [DllImport(Dll, CallingConvention = Cc)] public static extern void show_confirm_box_bytes(IntPtr parent, byte[] title, int titleLen, byte[] message, int messageLen, byte[] icon, int iconLen, MessageBoxCallback callback);
    }
}
