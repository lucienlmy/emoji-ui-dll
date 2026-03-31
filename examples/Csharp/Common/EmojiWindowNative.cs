using System;
using System.Runtime.InteropServices;
using System.Text;

namespace EmojiWindowDemoCommon
{
    internal static class EmojiWindowNative
    {
        [StructLayout(LayoutKind.Sequential)]
        internal struct Point
        {
            public int X;
            public int Y;
        }

        private const string DllName = "emoji_window.dll";
        private const CallingConvention CallConv = CallingConvention.StdCall;
        private static readonly byte[] EmptyBytes = new byte[0];

        public const int AlignLeft = 0;
        public const int AlignCenter = 1;
        public const int AlignRight = 2;

        public const int CheckBoxStyleDefault = 0;
        public const int CheckBoxStyleFill = 1;
        public const int CheckBoxStyleButton = 2;
        public const int CheckBoxStyleCard = 3;

        public const int RadioStyleDefault = 0;
        public const int RadioStyleBorder = 1;
        public const int RadioStyleButton = 2;

        public const int GroupBoxStyleOutline = 0;
        public const int GroupBoxStyleCard = 1;
        public const int GroupBoxStylePlain = 2;
        public const int GroupBoxStyleHeaderBar = 3;

        public const int TabHeaderStyleLine = 0;
        public const int TabHeaderStyleCard = 1;
        public const int TabHeaderStyleCardPlain = 2;
        public const int TabHeaderStyleSegmented = 3;

        public const int TabPositionTop = 0;
        public const int TabPositionBottom = 1;
        public const int TabPositionLeft = 2;
        public const int TabPositionRight = 3;

        public const int ScaleNone = 0;
        public const int ScaleStretch = 1;
        public const int ScaleFit = 2;
        public const int ScaleCenter = 3;

        public const int PopupTop = 0;
        public const int PopupBottom = 3;
        public const int PopupLeft = 6;
        public const int PopupRight = 9;

        public const int TooltipThemeDark = 0;
        public const int TooltipThemeLight = 1;
        public const int TooltipThemeCustom = 2;

        public const int TooltipTriggerHover = 0;
        public const int TooltipTriggerClick = 1;

        public const int NotifyTopRight = 0;
        public const int NotifyTopLeft = 1;
        public const int NotifyBottomRight = 2;
        public const int NotifyBottomLeft = 3;

        public const int NotifyInfo = 0;
        public const int NotifySuccess = 1;
        public const int NotifyWarning = 2;
        public const int NotifyError = 3;

        public const int HotKeyCtrl = 1;
        public const int HotKeyShift = 2;
        public const int HotKeyAlt = 4;

        public const int DatePrecisionYmd = 1;
        public const int DatePrecisionYmdHm = 3;
        public const int DatePrecisionYmdHms = 4;

        public const int TreeCallbackNodeSelected = 1;
        public const int TreeCallbackNodeExpanded = 2;
        public const int TreeCallbackNodeCollapsed = 3;
        public const int TreeCallbackNodeMoved = 8;

        public const int DataGridSelectionCell = 1;
        public const int DataGridSortAsc = 1;
        public const int DataGridSortDesc = 2;

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void ButtonClickCallback(int buttonId, IntPtr parentHwnd);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void MessageBoxCallback(int confirmed);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void WindowResizeCallback(IntPtr hwnd, int width, int height);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void TabCallback(IntPtr hTabControl, int selectedIndex);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void TabCloseCallback(IntPtr hTabControl, int index);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void TabRightClickCallback(IntPtr hTabControl, int index, int x, int y);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void TabDoubleClickCallback(IntPtr hTabControl, int index);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void CheckBoxCallback(IntPtr hCheckBox, int isChecked);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void RadioButtonCallback(IntPtr hRadioButton, int groupId, int isChecked);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void ProgressBarCallback(IntPtr hProgressBar, int value);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void SliderCallback(IntPtr hSlider, int value);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void SwitchCallback(IntPtr hSwitch, int isChecked);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void NotificationCallback(IntPtr hNotification, int eventType);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void PictureBoxCallback(IntPtr hPictureBox);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void ListBoxCallback(IntPtr hListBox, int index);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void ComboBoxCallback(IntPtr hComboBox, int index);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void HotKeyCallback(IntPtr hHotKey, int vkCode, int modifiers);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void ValueChangedCallback(IntPtr hwnd);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void MenuItemClickCallback(int menuId, int itemId);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void GroupBoxCallback(IntPtr hGroupBox);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void TreeViewCallback(int nodeId, IntPtr context);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void DataGridCellCallback(IntPtr hGrid, int row, int col);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void DataGridColumnHeaderCallback(IntPtr hGrid, int col);

        public delegate int GetTextFromIdCallback(int handle, IntPtr buffer, int bufferSize);
        public delegate int GetTextFromHandleCallback(IntPtr handle, IntPtr buffer, int bufferSize);
        public delegate int GetIndexedTextFromHandleCallback(IntPtr handle, int index, IntPtr buffer, int bufferSize);
        public delegate int GetCellTextFromHandleCallback(IntPtr handle, int row, int col, IntPtr buffer, int bufferSize);

        public static byte[] ToUtf8(string text)
        {
            return string.IsNullOrEmpty(text) ? EmptyBytes : Encoding.UTF8.GetBytes(text);
        }

        public static uint ARGB(int a, int r, int g, int b)
        {
            return (uint)(((a & 255) << 24) | ((r & 255) << 16) | ((g & 255) << 8) | (b & 255));
        }

        public static string ReadText(int handle, GetTextFromIdCallback callback)
        {
            int length = callback(handle, IntPtr.Zero, 0);
            if (length <= 0)
            {
                return string.Empty;
            }

            IntPtr buffer = Marshal.AllocHGlobal(length);
            try
            {
                callback(handle, buffer, length);
                byte[] bytes = new byte[length];
                Marshal.Copy(buffer, bytes, 0, length);
                return Encoding.UTF8.GetString(bytes);
            }
            finally
            {
                Marshal.FreeHGlobal(buffer);
            }
        }

        public static string ReadText(IntPtr handle, GetTextFromHandleCallback callback)
        {
            int length = callback(handle, IntPtr.Zero, 0);
            if (length <= 0)
            {
                return string.Empty;
            }

            IntPtr buffer = Marshal.AllocHGlobal(length);
            try
            {
                callback(handle, buffer, length);
                byte[] bytes = new byte[length];
                Marshal.Copy(buffer, bytes, 0, length);
                return Encoding.UTF8.GetString(bytes);
            }
            finally
            {
                Marshal.FreeHGlobal(buffer);
            }
        }

        public static string ReadIndexedText(IntPtr handle, int index, GetIndexedTextFromHandleCallback callback)
        {
            int length = callback(handle, index, IntPtr.Zero, 0);
            if (length <= 0)
            {
                return string.Empty;
            }

            IntPtr buffer = Marshal.AllocHGlobal(length);
            try
            {
                callback(handle, index, buffer, length);
                byte[] bytes = new byte[length];
                Marshal.Copy(buffer, bytes, 0, length);
                return Encoding.UTF8.GetString(bytes);
            }
            finally
            {
                Marshal.FreeHGlobal(buffer);
            }
        }

        public static string ReadCellText(IntPtr handle, int row, int col, GetCellTextFromHandleCallback callback)
        {
            int length = callback(handle, row, col, IntPtr.Zero, 0);
            if (length <= 0)
            {
                return string.Empty;
            }

            IntPtr buffer = Marshal.AllocHGlobal(length);
            try
            {
                callback(handle, row, col, buffer, length);
                byte[] bytes = new byte[length];
                Marshal.Copy(buffer, bytes, 0, length);
                return Encoding.UTF8.GetString(bytes);
            }
            finally
            {
                Marshal.FreeHGlobal(buffer);
            }
        }

        public static Point ClientToScreenPoint(IntPtr hwnd, int x, int y)
        {
            Point point = new Point { X = x, Y = y };
            ClientToScreen(hwnd, ref point);
            return point;
        }

        [DllImport("user32.dll", SetLastError = true)]
        [return: MarshalAs(UnmanagedType.Bool)]
        private static extern bool ClientToScreen(IntPtr hWnd, ref Point lpPoint);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr create_window_bytes(byte[] titleBytes, int titleLen, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr create_window_bytes_ex(byte[] titleBytes, int titleLen, int x, int y, int width, int height, uint titlebarColor, uint clientBgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void set_message_loop_main_window(IntPtr hwnd);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int run_message_loop();

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void destroy_window(IntPtr hwnd);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetWindowTitle(IntPtr hwnd, IntPtr buffer, int bufferSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetWindowBounds(IntPtr hwnd, out int x, out int y, out int width, out int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetWindowBounds(IntPtr hwnd, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetWindowVisible(IntPtr hwnd);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ShowEmojiWindow(IntPtr hwnd, int visible);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetWindowTitlebarColor(IntPtr hwnd);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetWindowResizeCallback(WindowResizeCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int create_emoji_button_bytes(IntPtr parent, byte[] emojiBytes, int emojiLen, byte[] textBytes, int textLen, int x, int y, int width, int height, uint bgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void set_button_click_callback(ButtonClickCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetButtonText(int buttonId, IntPtr buffer, int bufferSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetButtonText(int buttonId, byte[] textBytes, int textLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetButtonEmoji(int buttonId, IntPtr buffer, int bufferSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetButtonEmoji(int buttonId, byte[] emojiBytes, int emojiLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetButtonBounds(int buttonId, out int x, out int y, out int width, out int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetButtonBounds(int buttonId, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern uint GetButtonBackgroundColor(int buttonId);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetButtonBackgroundColor(int buttonId, uint color);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetButtonTextColor(int buttonId, uint color);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetButtonType(int buttonId, int type);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetButtonStyle(int buttonId, int style);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ShowButton(int buttonId, [MarshalAs(UnmanagedType.Bool)] bool visible);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool GetButtonEnabled(int buttonId);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void EnableButton(IntPtr parentHwnd, int buttonId, [MarshalAs(UnmanagedType.Bool)] bool enable);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateLabel(IntPtr parent, int x, int y, int width, int height, byte[] textBytes, int textLen, uint fgColor, uint bgColor, byte[] fontBytes, int fontLen, int fontSize, [MarshalAs(UnmanagedType.Bool)] bool bold, [MarshalAs(UnmanagedType.Bool)] bool italic, [MarshalAs(UnmanagedType.Bool)] bool underline, int align, [MarshalAs(UnmanagedType.Bool)] bool wordWrap);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetLabelText(IntPtr hLabel, IntPtr buffer, int bufferSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetLabelText(IntPtr hLabel, byte[] textBytes, int textLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetLabelFont(IntPtr hLabel, byte[] fontBytes, int fontLen, int fontSize, [MarshalAs(UnmanagedType.Bool)] bool bold, [MarshalAs(UnmanagedType.Bool)] bool italic, [MarshalAs(UnmanagedType.Bool)] bool underline);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetLabelColor(IntPtr hLabel, uint fgColor, uint bgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetLabelBounds(IntPtr hLabel, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ShowLabel(IntPtr hLabel, [MarshalAs(UnmanagedType.Bool)] bool show);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetLabelAlignment(IntPtr hLabel);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateEditBox(IntPtr parent, int x, int y, int width, int height, byte[] textBytes, int textLen, uint fgColor, uint bgColor, byte[] fontBytes, int fontLen, int fontSize, [MarshalAs(UnmanagedType.Bool)] bool bold, [MarshalAs(UnmanagedType.Bool)] bool italic, [MarshalAs(UnmanagedType.Bool)] bool underline, int alignment, [MarshalAs(UnmanagedType.Bool)] bool multiline, [MarshalAs(UnmanagedType.Bool)] bool readOnly, [MarshalAs(UnmanagedType.Bool)] bool password, [MarshalAs(UnmanagedType.Bool)] bool hasBorder, [MarshalAs(UnmanagedType.Bool)] bool verticalCenter);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateColorEmojiEditBox(IntPtr parent, int x, int y, int width, int height, byte[] textBytes, int textLen, uint fgColor, uint bgColor, byte[] fontBytes, int fontLen, int fontSize, [MarshalAs(UnmanagedType.Bool)] bool bold, [MarshalAs(UnmanagedType.Bool)] bool italic, [MarshalAs(UnmanagedType.Bool)] bool underline, int alignment, [MarshalAs(UnmanagedType.Bool)] bool multiline, [MarshalAs(UnmanagedType.Bool)] bool readOnly, [MarshalAs(UnmanagedType.Bool)] bool password, [MarshalAs(UnmanagedType.Bool)] bool hasBorder, [MarshalAs(UnmanagedType.Bool)] bool verticalCenter);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetEditBoxText(IntPtr hEdit, IntPtr buffer, int bufferSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetEditBoxText(IntPtr hEdit, byte[] textBytes, int textLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetEditBoxColor(IntPtr hEdit, uint fgColor, uint bgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetD2DEditBoxColor(IntPtr hEdit, uint fgColor, uint bgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetEditBoxBounds(IntPtr hEdit, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void EnableEditBox(IntPtr hEdit, [MarshalAs(UnmanagedType.Bool)] bool enable);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ShowEditBox(IntPtr hEdit, [MarshalAs(UnmanagedType.Bool)] bool show);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetEditBoxAlignment(IntPtr hEdit, int alignment);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateCheckBox(IntPtr parent, int x, int y, int width, int height, byte[] textBytes, int textLen, [MarshalAs(UnmanagedType.Bool)] bool isChecked, uint fgColor, uint bgColor, byte[] fontBytes, int fontLen, int fontSize, [MarshalAs(UnmanagedType.Bool)] bool bold, [MarshalAs(UnmanagedType.Bool)] bool italic, [MarshalAs(UnmanagedType.Bool)] bool underline);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool GetCheckBoxState(IntPtr hCheckBox);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetCheckBoxState(IntPtr hCheckBox, [MarshalAs(UnmanagedType.Bool)] bool isChecked);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetCheckBoxCallback(IntPtr hCheckBox, CheckBoxCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void EnableCheckBox(IntPtr hCheckBox, [MarshalAs(UnmanagedType.Bool)] bool enable);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ShowCheckBox(IntPtr hCheckBox, [MarshalAs(UnmanagedType.Bool)] bool show);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetCheckBoxText(IntPtr hCheckBox, byte[] textBytes, int textLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetCheckBoxBounds(IntPtr hCheckBox, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetCheckBoxText(IntPtr hCheckBox, IntPtr buffer, int bufferSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetCheckBoxColor(IntPtr hCheckBox, uint fgColor, uint bgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetCheckBoxCheckColor(IntPtr hCheckBox, uint color);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetCheckBoxStyle(IntPtr hCheckBox, int style);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetCheckBoxStyle(IntPtr hCheckBox);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateRadioButton(IntPtr parent, int x, int y, int width, int height, byte[] textBytes, int textLen, int groupId, [MarshalAs(UnmanagedType.Bool)] bool isChecked, uint fgColor, uint bgColor, byte[] fontBytes, int fontLen, int fontSize, [MarshalAs(UnmanagedType.Bool)] bool bold, [MarshalAs(UnmanagedType.Bool)] bool italic, [MarshalAs(UnmanagedType.Bool)] bool underline);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool GetRadioButtonState(IntPtr hRadioButton);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetRadioButtonState(IntPtr hRadioButton, [MarshalAs(UnmanagedType.Bool)] bool isChecked);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetRadioButtonCallback(IntPtr hRadioButton, RadioButtonCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetRadioButtonText(IntPtr hRadioButton, byte[] textBytes, int textLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetRadioButtonBounds(IntPtr hRadioButton, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetRadioButtonText(IntPtr hRadioButton, IntPtr buffer, int bufferSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetRadioButtonColor(IntPtr hRadioButton, uint fgColor, uint bgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetRadioButtonDotColor(IntPtr hRadioButton, uint color);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetRadioButtonStyle(IntPtr hRadioButton, int style);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateProgressBar(IntPtr parent, int x, int y, int width, int height, int initialValue, uint fgColor, uint bgColor, [MarshalAs(UnmanagedType.Bool)] bool showText, uint textColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetProgressValue(IntPtr hProgressBar, int value);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetProgressValue(IntPtr hProgressBar);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetProgressIndeterminate(IntPtr hProgressBar, [MarshalAs(UnmanagedType.Bool)] bool indeterminate);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetProgressBarColor(IntPtr hProgressBar, uint fgColor, uint bgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetProgressBarTextColor(IntPtr hProgressBar, uint textColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetProgressBarCallback(IntPtr hProgressBar, ProgressBarCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void EnableProgressBar(IntPtr hProgressBar, [MarshalAs(UnmanagedType.Bool)] bool enable);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ShowProgressBar(IntPtr hProgressBar, [MarshalAs(UnmanagedType.Bool)] bool show);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetProgressBarBounds(IntPtr hProgressBar, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetProgressBarShowText(IntPtr hProgressBar, [MarshalAs(UnmanagedType.Bool)] bool showText);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateSlider(IntPtr parent, int x, int y, int width, int height, int minValue, int maxValue, int value, int step, uint activeColor, uint bgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetSliderValue(IntPtr hSlider);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetSliderValue(IntPtr hSlider, int value);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetSliderRange(IntPtr hSlider, int minValue, int maxValue);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetSliderStep(IntPtr hSlider, int step);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetSliderShowStops(IntPtr hSlider, [MarshalAs(UnmanagedType.Bool)] bool showStops);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetSliderColors(IntPtr hSlider, uint activeColor, uint bgColor, uint buttonColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetSliderColors(IntPtr hSlider, out uint activeColor, out uint bgColor, out uint buttonColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetSliderCallback(IntPtr hSlider, SliderCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void EnableSlider(IntPtr hSlider, [MarshalAs(UnmanagedType.Bool)] bool enable);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ShowSlider(IntPtr hSlider, [MarshalAs(UnmanagedType.Bool)] bool show);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetSliderBounds(IntPtr hSlider, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateSwitch(IntPtr parent, int x, int y, int width, int height, [MarshalAs(UnmanagedType.Bool)] bool isChecked, uint activeColor, uint inactiveColor, byte[] activeTextBytes, int activeTextLen, byte[] inactiveTextBytes, int inactiveTextLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool GetSwitchState(IntPtr hSwitch);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetSwitchState(IntPtr hSwitch, [MarshalAs(UnmanagedType.Bool)] bool isChecked);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetSwitchText(IntPtr hSwitch, byte[] activeTextBytes, int activeTextLen, byte[] inactiveTextBytes, int inactiveTextLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetSwitchColors(IntPtr hSwitch, uint activeColor, uint inactiveColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetSwitchTextColors(IntPtr hSwitch, uint activeTextColor, uint inactiveTextColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetSwitchColors(IntPtr hSwitch, out uint activeColor, out uint inactiveColor, out uint activeTextColor, out uint inactiveTextColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetSwitchCallback(IntPtr hSwitch, SwitchCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void EnableSwitch(IntPtr hSwitch, [MarshalAs(UnmanagedType.Bool)] bool enable);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ShowSwitch(IntPtr hSwitch, [MarshalAs(UnmanagedType.Bool)] bool show);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetSwitchBounds(IntPtr hSwitch, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateTooltip(IntPtr owner, byte[] textBytes, int textLen, int placement, uint bgColor, uint fgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetTooltipText(IntPtr hTooltip, byte[] textBytes, int textLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetTooltipPlacement(IntPtr hTooltip, int placement);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetTooltipTheme(IntPtr hTooltip, int themeMode);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetTooltipColors(IntPtr hTooltip, uint bgColor, uint fgColor, uint borderColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetTooltipFont(IntPtr hTooltip, byte[] fontBytes, int fontLen, float fontSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetTooltipTrigger(IntPtr hTooltip, int triggerMode);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void BindTooltipToControl(IntPtr hTooltip, IntPtr hTarget);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ShowTooltipForControl(IntPtr hTooltip, IntPtr hTarget);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void HideTooltip(IntPtr hTooltip);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DestroyTooltip(IntPtr hTooltip);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr ShowNotification(IntPtr owner, byte[] titleBytes, int titleLen, byte[] messageBytes, int messageLen, int type, int position, int durationMs);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetNotificationCallback(IntPtr hNotification, NotificationCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void CloseNotification(IntPtr hNotification);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreatePictureBox(IntPtr parent, int x, int y, int width, int height, int scaleMode, uint bgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool LoadImageFromFile(IntPtr hPictureBox, byte[] pathBytes, int pathLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool LoadImageFromMemory(IntPtr hPictureBox, byte[] imageBytes, int imageLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ClearImage(IntPtr hPictureBox);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetImageOpacity(IntPtr hPictureBox, float opacity);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetPictureBoxCallback(IntPtr hPictureBox, PictureBoxCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void EnablePictureBox(IntPtr hPictureBox, [MarshalAs(UnmanagedType.Bool)] bool enable);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ShowPictureBox(IntPtr hPictureBox, [MarshalAs(UnmanagedType.Bool)] bool show);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetPictureBoxBounds(IntPtr hPictureBox, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetPictureBoxScaleMode(IntPtr hPictureBox, int scaleMode);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetPictureBoxBackgroundColor(IntPtr hPictureBox, uint bgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateListBox(IntPtr parent, int x, int y, int width, int height, [MarshalAs(UnmanagedType.Bool)] bool multiSelect, uint fgColor, uint bgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int AddListItem(IntPtr hListBox, byte[] textBytes, int textLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void RemoveListItem(IntPtr hListBox, int index);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ClearListBox(IntPtr hListBox);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetSelectedIndex(IntPtr hListBox);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetSelectedIndex(IntPtr hListBox, int index);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetListItemCount(IntPtr hListBox);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetListItemText(IntPtr hListBox, int index, IntPtr buffer, int bufferSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetListBoxCallback(IntPtr hListBox, ListBoxCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void EnableListBox(IntPtr hListBox, [MarshalAs(UnmanagedType.Bool)] bool enable);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ShowListBox(IntPtr hListBox, [MarshalAs(UnmanagedType.Bool)] bool show);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetListBoxBounds(IntPtr hListBox, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetListBoxColors(IntPtr hListBox, uint fgColor, uint bgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateComboBox(IntPtr parent, int x, int y, int width, int height, [MarshalAs(UnmanagedType.Bool)] bool readOnly, uint fgColor, uint bgColor, int itemHeight, byte[] fontBytes, int fontLen, int fontSize, [MarshalAs(UnmanagedType.Bool)] bool bold, [MarshalAs(UnmanagedType.Bool)] bool italic, [MarshalAs(UnmanagedType.Bool)] bool underline);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateD2DComboBox(IntPtr parent, int x, int y, int width, int height, [MarshalAs(UnmanagedType.Bool)] bool readOnly, uint fgColor, uint bgColor, int itemHeight, byte[] fontBytes, int fontLen, int fontSize, [MarshalAs(UnmanagedType.Bool)] bool bold, [MarshalAs(UnmanagedType.Bool)] bool italic, [MarshalAs(UnmanagedType.Bool)] bool underline);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int AddD2DComboItem(IntPtr hComboBox, byte[] textBytes, int textLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ClearD2DComboBox(IntPtr hComboBox);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetD2DComboSelectedIndex(IntPtr hComboBox);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetD2DComboSelectedIndex(IntPtr hComboBox, int index);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetD2DComboItemCount(IntPtr hComboBox);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetD2DComboItemText(IntPtr hComboBox, int index, IntPtr buffer, int bufferSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetD2DComboText(IntPtr hComboBox, IntPtr buffer, int bufferSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetD2DComboText(IntPtr hComboBox, byte[] textBytes, int textLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetD2DComboBoxCallback(IntPtr hComboBox, ComboBoxCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetD2DComboBoxColors(IntPtr hComboBox, uint fgColor, uint bgColor, uint selectColor, uint hoverColor, uint borderColor, uint buttonColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int AddComboItem(IntPtr hComboBox, byte[] textBytes, int textLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void RemoveComboItem(IntPtr hComboBox, int index);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ClearComboBox(IntPtr hComboBox);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetComboSelectedIndex(IntPtr hComboBox);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetComboSelectedIndex(IntPtr hComboBox, int index);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetComboItemCount(IntPtr hComboBox);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetComboItemText(IntPtr hComboBox, int index, IntPtr buffer, int bufferSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetComboBoxCallback(IntPtr hComboBox, ComboBoxCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void EnableComboBox(IntPtr hComboBox, [MarshalAs(UnmanagedType.Bool)] bool enable);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ShowComboBox(IntPtr hComboBox, [MarshalAs(UnmanagedType.Bool)] bool show);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetComboBoxBounds(IntPtr hComboBox, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetComboBoxText(IntPtr hComboBox, IntPtr buffer, int bufferSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetComboBoxText(IntPtr hComboBox, byte[] textBytes, int textLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetComboBoxColors(IntPtr hComboBox, uint fgColor, uint bgColor, uint borderColor, uint buttonColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateD2DDateTimePicker(IntPtr parent, int x, int y, int width, int height, int precision, uint fgColor, uint bgColor, uint borderColor, byte[] fontBytes, int fontLen, int fontSize, [MarshalAs(UnmanagedType.Bool)] bool bold, [MarshalAs(UnmanagedType.Bool)] bool italic, [MarshalAs(UnmanagedType.Bool)] bool underline);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetD2DDateTimePickerPrecision(IntPtr hPicker);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetD2DDateTimePickerPrecision(IntPtr hPicker, int precision);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void GetD2DDateTimePickerDateTime(IntPtr hPicker, out int year, out int month, out int day, out int hour, out int minute, out int second);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetD2DDateTimePickerDateTime(IntPtr hPicker, int year, int month, int day, int hour, int minute, int second);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetD2DDateTimePickerCallback(IntPtr hPicker, ValueChangedCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void EnableD2DDateTimePicker(IntPtr hPicker, [MarshalAs(UnmanagedType.Bool)] bool enable);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ShowD2DDateTimePicker(IntPtr hPicker, [MarshalAs(UnmanagedType.Bool)] bool show);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetD2DDateTimePickerBounds(IntPtr hPicker, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetD2DDateTimePickerColors(IntPtr hPicker, uint fgColor, uint bgColor, uint borderColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateHotKeyControl(IntPtr parent, int x, int y, int width, int height, uint fgColor, uint bgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void GetHotKey(IntPtr hHotKey, out int vkCode, out int modifiers);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetHotKey(IntPtr hHotKey, int vkCode, int modifiers);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ClearHotKey(IntPtr hHotKey);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetHotKeyCallback(IntPtr hHotKey, HotKeyCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void EnableHotKeyControl(IntPtr hHotKey, [MarshalAs(UnmanagedType.Bool)] bool enable);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ShowHotKeyControl(IntPtr hHotKey, [MarshalAs(UnmanagedType.Bool)] bool show);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetHotKeyControlBounds(IntPtr hHotKey, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetHotKeyColors(IntPtr hHotKey, uint fgColor, uint bgColor, uint borderColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateGroupBox(IntPtr parent, int x, int y, int width, int height, byte[] titleBytes, int titleLen, uint borderColor, uint bgColor, byte[] fontBytes, int fontLen, int fontSize, [MarshalAs(UnmanagedType.Bool)] bool bold, [MarshalAs(UnmanagedType.Bool)] bool italic, [MarshalAs(UnmanagedType.Bool)] bool underline);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void AddChildToGroup(IntPtr hGroupBox, IntPtr hChild);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void RemoveChildFromGroup(IntPtr hGroupBox, IntPtr hChild);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetGroupBoxTitle(IntPtr hGroupBox, byte[] titleBytes, int titleLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void EnableGroupBox(IntPtr hGroupBox, [MarshalAs(UnmanagedType.Bool)] bool enable);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ShowGroupBox(IntPtr hGroupBox, [MarshalAs(UnmanagedType.Bool)] bool show);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetGroupBoxBounds(IntPtr hGroupBox, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetGroupBoxCallback(IntPtr hGroupBox, GroupBoxCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetGroupBoxTitle(IntPtr hGroupBox, IntPtr buffer, int bufferSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetGroupBoxStyle(IntPtr hGroupBox);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetGroupBoxTitleColor(IntPtr hGroupBox, uint color);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetGroupBoxStyle(IntPtr hGroupBox, int style);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreatePanel(IntPtr parent, int x, int y, int width, int height, uint bgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetPanelBackgroundColor(IntPtr hPanel, uint bgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetPanelBackgroundColor(IntPtr hPanel);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateTabControl(IntPtr parent, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int AddTabItem(IntPtr hTabControl, byte[] titleBytes, int titleLen, IntPtr hContentWindow);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int InsertTabItem(IntPtr hTabControl, int index, byte[] titleBytes, int titleLen, IntPtr hContentWindow);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool RemoveTabItem(IntPtr hTabControl, int index);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetCurrentTabIndex(IntPtr hTabControl);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SelectTab(IntPtr hTabControl, int index);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetTabCount(IntPtr hTabControl);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetTabTitle(IntPtr hTabControl, int index, IntPtr buffer, int bufferSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabTitle(IntPtr hTabControl, int index, byte[] titleBytes, int titleLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabHeaderStyle(IntPtr hTabControl, int style);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabPosition(IntPtr hTabControl, int position);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabAlignment(IntPtr hTabControl, int alignment);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabScrollable(IntPtr hTabControl, int scrollable);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabItemSize(IntPtr hTabControl, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabFont(IntPtr hTabControl, byte[] fontBytes, int fontLen, float fontSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabColors(IntPtr hTabControl, uint selectedBg, uint unselectedBg, uint selectedText, uint unselectedText);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabIndicatorColor(IntPtr hTabControl, uint color);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabPadding(IntPtr hTabControl, int horizontal, int vertical);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabClosable(IntPtr hTabControl, int closable);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabCloseCallback(IntPtr hTabControl, TabCloseCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabRightClickCallback(IntPtr hTabControl, TabRightClickCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabDraggable(IntPtr hTabControl, int draggable);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabDoubleClickCallback(IntPtr hTabControl, TabDoubleClickCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetTabCallback(IntPtr hTabControl, TabCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void UpdateTabControlLayout(IntPtr hTabControl);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool RedrawTabControl(IntPtr hTabControl);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateMenuBar(IntPtr hWindow);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DestroyMenuBar(IntPtr hMenuBar);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int MenuBarAddItem(IntPtr hMenuBar, byte[] textBytes, int textLen, int itemId);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int MenuBarAddSubItem(IntPtr hMenuBar, int parentItemId, byte[] textBytes, int textLen, int itemId);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetMenuBarPlacement(IntPtr hMenuBar, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetMenuBarCallback(IntPtr hMenuBar, MenuItemClickCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool MenuBarUpdateSubItemText(IntPtr hMenuBar, int parentItemId, int itemId, byte[] textBytes, int textLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateEmojiPopupMenu(IntPtr hOwner);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DestroyEmojiPopupMenu(IntPtr hPopupMenu);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int PopupMenuAddItem(IntPtr hPopupMenu, byte[] textBytes, int textLen, int itemId);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int PopupMenuAddSubItem(IntPtr hPopupMenu, int parentItemId, byte[] textBytes, int textLen, int itemId);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void BindControlMenu(IntPtr hControl, IntPtr hPopupMenu);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void BindButtonMenu(IntPtr hParent, int buttonId, IntPtr hPopupMenu);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void ShowContextMenu(IntPtr hPopupMenu, int x, int y);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetPopupMenuCallback(IntPtr hPopupMenu, MenuItemClickCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateDataGridView(IntPtr parent, int x, int y, int width, int height, [MarshalAs(UnmanagedType.Bool)] bool virtualMode, [MarshalAs(UnmanagedType.Bool)] bool alternateRowColor, uint fgColor, uint bgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int DataGrid_AddTextColumn(IntPtr hGrid, byte[] headerBytes, int headerLen, int width);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int DataGrid_AddCheckBoxColumn(IntPtr hGrid, byte[] headerBytes, int headerLen, int width);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int DataGrid_AddButtonColumn(IntPtr hGrid, byte[] headerBytes, int headerLen, int width);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int DataGrid_AddRow(IntPtr hGrid);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_RemoveRow(IntPtr hGrid, int rowIndex);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_ClearRows(IntPtr hGrid);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int DataGrid_GetRowCount(IntPtr hGrid);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_SetCellText(IntPtr hGrid, int row, int col, byte[] textBytes, int textLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int DataGrid_GetCellText(IntPtr hGrid, int row, int col, IntPtr buffer, int bufferSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_SetCellChecked(IntPtr hGrid, int row, int col, [MarshalAs(UnmanagedType.Bool)] bool isChecked);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool DataGrid_GetCellChecked(IntPtr hGrid, int row, int col);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_SetCellStyle(IntPtr hGrid, int row, int col, uint fgColor, uint bgColor, int bold, int italic);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int DataGrid_GetSelectedRow(IntPtr hGrid);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int DataGrid_GetSelectedCol(IntPtr hGrid);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_SetSelectedCell(IntPtr hGrid, int row, int col);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_SetSelectionMode(IntPtr hGrid, int mode);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_SortByColumn(IntPtr hGrid, int col, int direction);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_SetShowGridLines(IntPtr hGrid, int show);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_SetDefaultRowHeight(IntPtr hGrid, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_SetHeaderHeight(IntPtr hGrid, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_SetColumnWidth(IntPtr hGrid, int col, int width);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_SetFreezeHeader(IntPtr hGrid, int freeze);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_SetColumnHeaderAlignment(IntPtr hGrid, int col, int align);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_SetColumnCellAlignment(IntPtr hGrid, int col, int align);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_SetCellClickCallback(IntPtr hGrid, DataGridCellCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_SetCellDoubleClickCallback(IntPtr hGrid, DataGridCellCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_SetSelectionChangedCallback(IntPtr hGrid, DataGridCellCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_SetColumnHeaderClickCallback(IntPtr hGrid, DataGridColumnHeaderCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_SetCellValueChangedCallback(IntPtr hGrid, DataGridCellCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_Enable(IntPtr hGrid, int enable);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_Show(IntPtr hGrid, int show);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_SetBounds(IntPtr hGrid, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DataGrid_Refresh(IntPtr hGrid);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateTreeView(IntPtr parent, int x, int y, int width, int height, uint bgColor, uint textColor, IntPtr callbackContext);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int AddRootNode(IntPtr hTreeView, byte[] textBytes, int textLen, byte[] iconBytes, int iconLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int AddChildNode(IntPtr hTreeView, int parentId, byte[] textBytes, int textLen, byte[] iconBytes, int iconLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool ExpandNode(IntPtr hTreeView, int nodeId);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool CollapseNode(IntPtr hTreeView, int nodeId);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool ExpandAll(IntPtr hTreeView);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool CollapseAll(IntPtr hTreeView);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetSelectedNode(IntPtr hTreeView, int nodeId);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetSelectedNode(IntPtr hTreeView);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetNodeText(IntPtr hTreeView, int nodeId, byte[] textBytes, int textLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetNodeText(IntPtr hTreeView, int nodeId, IntPtr buffer, int bufferSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetNodeChecked(IntPtr hTreeView, int nodeId, [MarshalAs(UnmanagedType.Bool)] bool isChecked);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool GetNodeChecked(IntPtr hTreeView, int nodeId);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetTreeViewSidebarMode(IntPtr hTreeView, [MarshalAs(UnmanagedType.Bool)] bool enable);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool GetTreeViewSidebarMode(IntPtr hTreeView);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetTreeViewRowHeight(IntPtr hTreeView, float height);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetTreeViewItemSpacing(IntPtr hTreeView, float spacing);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetTreeViewTextColor(IntPtr hTreeView, uint color);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetTreeViewSelectedBgColor(IntPtr hTreeView, uint color);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetTreeViewSelectedForeColor(IntPtr hTreeView, uint color);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetTreeViewHoverBgColor(IntPtr hTreeView, uint color);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetTreeViewFont(IntPtr hTreeView, byte[] fontBytes, int fontLen, float fontSize, int weight, [MarshalAs(UnmanagedType.Bool)] bool italic);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool EnableTreeViewDragDrop(IntPtr hTreeView, [MarshalAs(UnmanagedType.Bool)] bool enable);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SetTreeViewCallback(IntPtr hTreeView, int callbackType, TreeViewCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void show_message_box_bytes(IntPtr parent, byte[] titleBytes, int titleLen, byte[] messageBytes, int messageLen, byte[] iconBytes, int iconLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void show_confirm_box_bytes(IntPtr parent, byte[] titleBytes, int titleLen, byte[] messageBytes, int messageLen, byte[] iconBytes, int iconLen, MessageBoxCallback callback);
    }
}
