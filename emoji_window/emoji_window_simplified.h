#pragma once

#include <windows.h>
#include <d2d1.h>
#include <dwrite.h>
#include <string>
#include <vector>
#include <map>

#pragma comment(lib, "d2d1.lib")
#pragma comment(lib, "dwrite.lib")

// Button click callback type (stdcall)
// 参数: button_id - 按钮ID, parent_hwnd - 父窗口句柄
typedef void (__stdcall *ButtonClickCallback)(int button_id, HWND parent_hwnd);

// Message box callback type (confirmed: 1=OK, 0=Cancel)
typedef void (__stdcall *MessageBoxCallback)(int confirmed);

// ========== 编辑框样式和配置 ==========

// 文本对齐方式
enum EmojiEditTextAlignment {
    EDIT_ALIGN_LEFT = 0,
    EDIT_ALIGN_CENTER = 1,
    EDIT_ALIGN_RIGHT = 2
};

// 边框样式
enum EmojiEditBorderStyle {
    EDIT_BORDER_NONE = 0,       // 无边框
    EDIT_BORDER_SINGLE = 1,     // 单线边框
    EDIT_BORDER_ROUNDED = 2     // 圆角边框
};

// 滚动条样式
enum EmojiEditScrollStyle {
    EDIT_SCROLL_NONE = 0,       // 无滚动条
    EDIT_SCROLL_VERTICAL = 1,   // 垂直滚动条
    EDIT_SCROLL_HORIZONTAL = 2, // 水平滚动条
    EDIT_SCROLL_BOTH = 3        // 双向滚动条
};

// 编辑框状态
struct EmojiEditState {
    HWND hwnd;
    HWND hParent;
    ID2D1HwndRenderTarget* render_target;
    IDWriteFactory* dwrite_factory;
    IDWriteTextFormat* text_format;
    IDWriteTextLayout* text_layout;

    std::wstring text;
    std::wstring font_name;
    float font_size;
    DWRITE_FONT_WEIGHT font_weight;

    UINT32 text_color;
    UINT32 bg_color;
    UINT32 border_color;
    UINT32 selection_color;
    UINT32 cursor_color;

    EmojiEditTextAlignment text_alignment;
    EmojiEditBorderStyle border_style;
    EmojiEditScrollStyle scroll_style;
    bool multiline;
    bool word_wrap;
    bool readonly;
    float corner_radius;

    int cursor_pos;
    int selection_start;
    int selection_end;
    bool has_selection;

    int scroll_x;
    int scroll_y;
    int line_height;
    int max_scroll_x;
    int max_scroll_y;

    bool is_focused;
    bool cursor_visible;
    bool cursor_blink_state;

    int x, y, width, height;
};

// Button structure
struct EmojiButton {
    int id;
    std::wstring emoji;
    std::wstring text;
    int x, y, width, height;
    UINT32 bg_color;
    bool is_hovered;
    bool is_pressed;

    bool ContainsPoint(int px, int py) const {
        return px >= x && px <= x + width && py >= y && py <= y + height;
    }
};

// Window state
struct WindowState {
    HWND hwnd;
    ID2D1HwndRenderTarget* render_target;
    IDWriteFactory* dwrite_factory;
    std::vector<EmojiButton> buttons;
};

// Message box button type
enum MsgBoxButtonType {
    MSGBOX_OK = 0,
    MSGBOX_OKCANCEL = 1
};

// Message box state
struct MsgBoxState {
    HWND hwnd;
    HWND parent_hwnd;
    ID2D1HwndRenderTarget* render_target;
    IDWriteFactory* dwrite_factory;
    std::wstring title;
    std::wstring message;
    std::wstring icon_emoji;
    MsgBoxButtonType button_type;
    MessageBoxCallback callback;
    EmojiButton ok_button;
    EmojiButton cancel_button;
    bool result;
};

// Global variables
extern std::map<HWND, WindowState*> g_windows;
extern std::map<HWND, MsgBoxState*> g_msgboxes;
extern std::map<HWND, EmojiEditState*> g_edits;
extern ButtonClickCallback g_button_callback;

// Export functions (stdcall calling convention)
extern "C" {
    HWND __stdcall create_window(const char* title, int width, int height);

    int __stdcall create_emoji_button_bytes(
        HWND parent,
        const unsigned char* emoji_bytes,
        int emoji_len,
        const unsigned char* text_bytes,
        int text_len,
        int x, int y, int width, int height,
        UINT32 bg_color
    );

    void __stdcall set_button_click_callback(ButtonClickCallback callback);
    int __stdcall run_message_loop();
    void __stdcall destroy_window(HWND hwnd);
    void __stdcall set_window_icon(HWND hwnd, const char* icon_path);

    // Message box
    void __stdcall show_message_box_bytes(
        HWND parent,
        const unsigned char* title_bytes,
        int title_len,
        const unsigned char* message_bytes,
        int message_len,
        const unsigned char* icon_bytes,
        int icon_len
    );

    // Confirm box
    void __stdcall show_confirm_box_bytes(
        HWND parent,
        const unsigned char* title_bytes,
        int title_len,
        const unsigned char* message_bytes,
        int message_len,
        const unsigned char* icon_bytes,
        int icon_len,
        MessageBoxCallback callback
    );

    // ========== EmojiEdit 编辑框功能 ==========

    HWND __stdcall CreateEmojiEdit(HWND hParent, int x, int y, int width, int height);
    BOOL __stdcall SetEmojiEditText(HWND hEdit, const unsigned char* text_bytes, int text_len);
    int __stdcall GetEmojiEditTextLength(HWND hEdit);
    int __stdcall GetEmojiEditText(HWND hEdit, unsigned char* buffer, int buffer_size);
    BOOL __stdcall SetEmojiEditFont(HWND hEdit, const unsigned char* font_name_bytes, int font_name_len, float font_size, int font_weight);
    BOOL __stdcall SetEmojiEditColors(HWND hEdit, UINT32 text_color, UINT32 bg_color, UINT32 border_color, UINT32 selection_color, UINT32 cursor_color);
    BOOL __stdcall SetEmojiEditStyle(HWND hEdit, int text_alignment, int border_style, int scroll_style, BOOL multiline, BOOL word_wrap, BOOL readonly, float corner_radius);
    BOOL __stdcall SetEmojiEditScroll(HWND hEdit, int scroll_x, int scroll_y);
    BOOL __stdcall GetEmojiEditScrollInfo(HWND hEdit, int* max_scroll_x, int* max_scroll_y, int* current_scroll_x, int* current_scroll_y);
    BOOL __stdcall SetEmojiEditSelection(HWND hEdit, int start_pos, int end_pos);
    BOOL __stdcall GetEmojiEditSelection(HWND hEdit, int* start_pos, int* end_pos);
    BOOL __stdcall SetEmojiEditCursorPos(HWND hEdit, int pos);
    int __stdcall GetEmojiEditCursorPos(HWND hEdit);
    void __stdcall SetEmojiEditFocus(HWND hEdit, BOOL focused);
    void __stdcall ClearEmojiEdit(HWND hEdit);
    void __stdcall DestroyEmojiEdit(HWND hEdit);
}

// Internal functions
LRESULT CALLBACK WindowProc(HWND hwnd, UINT msg, WPARAM wparam, LPARAM lparam);
LRESULT CALLBACK MsgBoxProc(HWND hwnd, UINT msg, WPARAM wparam, LPARAM lparam);
void DrawButton(ID2D1HwndRenderTarget* rt, IDWriteFactory* factory, const EmojiButton& button);
void DrawMsgBox(ID2D1HwndRenderTarget* rt, IDWriteFactory* factory, MsgBoxState* state);
std::wstring Utf8ToWide(const unsigned char* bytes, int len);
D2D1_COLOR_F ColorFromUInt32(UINT32 color);
UINT32 LightenColor(UINT32 color, float factor);
UINT32 DarkenColor(UINT32 color, float factor);
HWND CreateMessageBoxWindow(HWND parent, const std::wstring& title, const std::wstring& message,
                            const std::wstring& icon, MsgBoxButtonType type, MessageBoxCallback callback);
void CloseMessageBox(HWND hwnd, bool result);

// EmojiEdit 内部辅助函数
LRESULT CALLBACK EmojiEditProc(HWND hwnd, UINT msg, WPARAM wparam, LPARAM lparam);
void DrawEmojiEdit(EmojiEditState* state);
void UpdateEmojiEditLayout(EmojiEditState* state);
void UpdateEmojiEditScrollInfo(EmojiEditState* state);
int CharFromPoint(EmojiEditState* state, int x, int y);
void PointFromChar(EmojiEditState* state, int char_pos, int* x, int* y);
void DeleteSelection(EmojiEditState* state);
std::wstring GetSelectedText(EmojiEditState* state);
void MoveCursor(EmojiEditState* state, int new_pos, bool shift_pressed);
void ScrollToCursor(EmojiEditState* state);
