using System;
using System.Runtime.InteropServices;
using System.Text;

namespace EmojiWindowTabControlDemo
{
    internal static class EmojiWindowNative
    {
        private const string DllName = "emoji_window.dll";
        private const CallingConvention CallConv = CallingConvention.StdCall;
        private static readonly byte[] EmptyBytes = new byte[0];

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void ButtonClickCallback(int buttonId, IntPtr parentHwnd);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void TabCallback(IntPtr hTabControl, int selectedIndex);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void TabCloseCallback(IntPtr hTabControl, int index);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void TabRightClickCallback(IntPtr hTabControl, int index, int x, int y);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void TabDoubleClickCallback(IntPtr hTabControl, int index);

        [UnmanagedFunctionPointer(CallConv)]
        public delegate void WindowResizeCallback(IntPtr hwnd, int width, int height);

        public static byte[] ToUtf8(string text)
        {
            return string.IsNullOrEmpty(text) ? EmptyBytes : Encoding.UTF8.GetBytes(text);
        }

        public static uint ARGB(int a, int r, int g, int b)
        {
            return (uint)(((a & 255) << 24) | ((r & 255) << 16) | ((g & 255) << 8) | (b & 255));
        }

        public static string GetTabTitleString(IntPtr hTab, int index)
        {
            int length = GetTabTitle(hTab, index, IntPtr.Zero, 0);
            if (length <= 0)
            {
                return string.Empty;
            }

            IntPtr buffer = Marshal.AllocHGlobal(length);
            try
            {
                GetTabTitle(hTab, index, buffer, length);
                byte[] bytes = new byte[length];
                Marshal.Copy(buffer, bytes, 0, length);
                return Encoding.UTF8.GetString(bytes);
            }
            finally
            {
                Marshal.FreeHGlobal(buffer);
            }
        }

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr create_window_bytes_ex(byte[] titleBytes, int titleLen, int x, int y, int width, int height, uint titlebarColor, uint clientBgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void set_message_loop_main_window(IntPtr hwnd);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int run_message_loop();

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int CreateLabel(IntPtr parent, int x, int y, int width, int height, byte[] text, int textLen, uint fgColor, uint bgColor, byte[] fontName, int fontNameLen, int fontSize, int bold, int italic, int underline, int align, int wordWrap);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetLabelText(int label, byte[] text, int textLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateGroupBox(IntPtr parent, int x, int y, int width, int height, byte[] title, int titleLen, uint borderColor, uint bgColor, byte[] fontName, int fontNameLen, int fontSize, int bold, int italic, int underline);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int CreateEditBox(IntPtr parent, int x, int y, int width, int height, byte[] text, int textLen, uint fgColor, uint bgColor, byte[] fontName, int fontNameLen, int fontSize, int bold, int italic, int underline, int alignment, int multiline, int readOnly, int password, int hasBorder, int verticalCenter);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetEditBoxText(int hEdit, byte[] text, int textLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetEditBoxBounds(int hEdit, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int create_emoji_button_bytes(IntPtr parent, byte[] emoji, int emojiLen, byte[] text, int textLen, int x, int y, int width, int height, uint bgColor);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void set_button_click_callback(ButtonClickCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetButtonBounds(int buttonId, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr CreateTabControl(IntPtr hParent, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int AddTabItem(IntPtr hTabControl, byte[] titleBytes, int titleLen, IntPtr hContentWindow);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int InsertTabItem(IntPtr hTabControl, int index, byte[] titleBytes, int titleLen, IntPtr hContentWindow);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool RemoveTabItem(IntPtr hTabControl, int index);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int RemoveAllTabs(IntPtr hTabControl);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int MoveTabItem(IntPtr hTabControl, int fromIndex, int toIndex);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetTabCallback(IntPtr hTabControl, TabCallback callback);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetCurrentTabIndex(IntPtr hTabControl);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool SelectTab(IntPtr hTabControl, int index);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetTabCount(IntPtr hTabControl);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern IntPtr GetTabContentWindow(IntPtr hTabControl, int index);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void DestroyTabControl(IntPtr hTabControl);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void UpdateTabControlLayout(IntPtr hTabControl);

        [DllImport(DllName, CallingConvention = CallConv)]
        [return: MarshalAs(UnmanagedType.Bool)]
        public static extern bool RedrawTabControl(IntPtr hTabControl);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetTabTitle(IntPtr hTabControl, int index, IntPtr buffer, int bufferSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabTitle(IntPtr hTabControl, int index, byte[] titleBytes, int titleLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetTabControlBounds(IntPtr hTabControl, out int x, out int y, out int width, out int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabControlBounds(IntPtr hTabControl, int x, int y, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetTabControlVisible(IntPtr hTabControl);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int ShowTabControl(IntPtr hTabControl, int visible);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int EnableTabControl(IntPtr hTabControl, int enabled);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabItemSize(IntPtr hTabControl, int width, int height);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabFont(IntPtr hTabControl, byte[] fontName, int fontNameLen, float fontSize);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabColors(IntPtr hTabControl, uint selectedBg, uint unselectedBg, uint selectedText, uint unselectedText);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabIndicatorColor(IntPtr hTabControl, uint color);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabPadding(IntPtr hTabControl, int horizontal, int vertical);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabHeaderStyle(IntPtr hTabControl, int style);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int EnableTabItem(IntPtr hTabControl, int index, int enabled);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetTabItemEnabled(IntPtr hTabControl, int index);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int ShowTabItem(IntPtr hTabControl, int index, int visible);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabItemIcon(IntPtr hTabControl, int index, byte[] iconBytes, int iconLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabContentBgColor(IntPtr hTabControl, int index, uint color);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabContentBgColorAll(IntPtr hTabControl, uint color);

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
        public static extern int SetTabPosition(IntPtr hTabControl, int position);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabAlignment(IntPtr hTabControl, int align);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int SetTabScrollable(IntPtr hTabControl, int scrollable);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetTabIndexByTitle(IntPtr hTabControl, byte[] titleBytes, int titleLen);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int GetTabEnabled(IntPtr hTabControl);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern int IsTabItemSelected(IntPtr hTabControl, int index);

        [DllImport(DllName, CallingConvention = CallConv)]
        public static extern void SetWindowResizeCallback(WindowResizeCallback callback);
    }
}
