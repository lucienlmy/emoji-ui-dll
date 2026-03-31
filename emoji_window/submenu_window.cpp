#include "log.h"
#include "submenu_window.h"
#include "emoji_window.h"
#include <windowsx.h>
#include <algorithm>
#include <set>

// 外部全局变量
extern ID2D1Factory* g_d2d_factory;
extern IDWriteFactory* g_dwrite_factory;
extern std::map<HWND, MenuBarState*> g_menubars;  // 访问菜单栏状态
extern HMODULE g_emoji_window_module;

// 全局变量：当前活动的子菜单窗口（用于鼠标钩子）
static SubMenuWindow* g_active_submenu = nullptr;
static std::set<SubMenuWindow*> g_visible_submenus;

// 窗口类名
static const wchar_t* SUBMENU_WINDOW_CLASS = L"SubMenuWindowClass";
static bool g_class_registered = false;

static D2D1_COLOR_F ColorFromArgb(UINT32 argb) {
    return D2D1::ColorF(
        ((argb >> 16) & 0xFF) / 255.0f,
        ((argb >> 8) & 0xFF) / 255.0f,
        (argb & 0xFF) / 255.0f,
        ((argb >> 24) & 0xFF) / 255.0f
    );
}

static UINT32 SubMenuThemeColor(UINT32 fallback, UINT32 ThemeColors::* member) {
    if (g_current_theme) {
        return g_current_theme->colors.*member;
    }
    return fallback;
}

static SubMenuWindow::MenuTheme BuildCurrentMenuTheme() {
    SubMenuWindow::MenuTheme theme = {};
    theme.backgroundColor = ColorFromArgb(SubMenuThemeColor(0xFFFFFFFF, &ThemeColors::background));
    theme.hoverColor = ColorFromArgb(SubMenuThemeColor(0xFFF5F7FA, &ThemeColors::background_light));
    theme.textColor = ColorFromArgb(SubMenuThemeColor(0xFF606266, &ThemeColors::text_regular));
    theme.disabledColor = ColorFromArgb(SubMenuThemeColor(0xFFC0C4CC, &ThemeColors::text_placeholder));
    theme.borderColor = ColorFromArgb(SubMenuThemeColor(0xFFE4E7ED, &ThemeColors::border_light));
    theme.separatorColor = ColorFromArgb(SubMenuThemeColor(0xFFF2F6FC, &ThemeColors::border_extra_light));
    theme.borderWidth = 1;
    theme.cornerRadius = 8;
    theme.shadowSize = 4;
    return theme;
}

SubMenuWindow* SubMenuWindow::FindVisibleSubMenuAtPoint(POINT screen_pt) {
    SubMenuWindow* target = nullptr;
    int best_nesting_level = -1;
    for (SubMenuWindow* current : g_visible_submenus) {
        if (!current) {
            continue;
        }
        HWND hwnd = current->GetHwnd();
        if (!hwnd || !IsWindow(hwnd) || !current->IsVisible()) {
            continue;
        }
        RECT rect = {};
        GetWindowRect(hwnd, &rect);
        if (PtInRect(&rect, screen_pt)) {
            if (!target || current->m_nesting_level >= best_nesting_level) {
                target = current;
                best_nesting_level = current->m_nesting_level;
            }
        }
    }
    return target;
}

// 注册窗口类
static bool RegisterSubMenuWindowClass() {
    if (g_class_registered) return true;
    
    WNDCLASSEXW wc = {};
    wc.cbSize = sizeof(WNDCLASSEXW);
    wc.style = CS_HREDRAW | CS_VREDRAW | CS_DROPSHADOW;
    wc.lpfnWndProc = SubMenuWindow::WindowProc;
    wc.hInstance = g_emoji_window_module ? g_emoji_window_module : GetModuleHandle(nullptr);
    wc.hCursor = LoadCursor(nullptr, IDC_ARROW);
    wc.lpszClassName = SUBMENU_WINDOW_CLASS;
    
    if (!RegisterClassExW(&wc)) {
        return false;
    }
    
    g_class_registered = true;
    return true;
}

SubMenuWindow::SubMenuWindow()
    : m_hwnd(nullptr)
    , m_parent(nullptr)
    , m_menu_id(0)
    , m_render_target(nullptr)
    , m_dwrite_factory(nullptr)
    , m_text_format(nullptr)
    , m_hovered_index(-1)
    , m_selected_index(-1)
    , m_visible(false)
    , m_width(0)
    , m_height(0)
    , m_callback(nullptr)
    , m_parent_submenu(nullptr)
    , m_child_submenu(nullptr)
    , m_nesting_level(0)
    , m_hover_start_time(0)
    , m_hover_item_for_submenu(-1)
    , m_ignore_outside_click_until(0)
    , m_animation_enabled(true)
    , m_animation_type(ANIMATION_FADE)
    , m_is_animating(false)
    , m_animation_start_time(0)
    , m_theme(MenuTheme::Default())
    , m_mouse_hook(nullptr)
{
}

SubMenuWindow::~SubMenuWindow() {
    Hide();
    g_visible_submenus.erase(this);
    ReleaseD2DResources();
    
    if (m_hwnd) {
        DestroyWindow(m_hwnd);
        m_hwnd = nullptr;
    }
}

bool SubMenuWindow::Create(HWND parent, int menu_id) {
    if (!RegisterSubMenuWindowClass()) {
        return false;
    }
    
    m_parent = parent;
    m_menu_id = menu_id;
    
    // 创建弹出窗口（无边框、置顶、工具窗口）
    m_hwnd = CreateWindowExW(
        WS_EX_TOPMOST | WS_EX_TOOLWINDOW,
        SUBMENU_WINDOW_CLASS,
        L"",
        WS_POPUP,
        0, 0, 100, 100,  // 初始大小，稍后调整
        parent,
        nullptr,
        g_emoji_window_module ? g_emoji_window_module : GetModuleHandle(nullptr),
        this  // 传递 this 指针
    );
    
    if (!m_hwnd) {
        return false;
    }
    
    // 初始化 Direct2D 资源
    m_dwrite_factory = g_dwrite_factory;
    if (!m_text_format && m_dwrite_factory) {
        HRESULT hr = m_dwrite_factory->CreateTextFormat(
            L"Segoe UI Emoji",
            nullptr,
            DWRITE_FONT_WEIGHT_NORMAL,
            DWRITE_FONT_STYLE_NORMAL,
            DWRITE_FONT_STRETCH_NORMAL,
            14.0f,
            L"zh-CN",
            &m_text_format
        );
        if (SUCCEEDED(hr) && m_text_format) {
            m_text_format->SetTextAlignment(DWRITE_TEXT_ALIGNMENT_LEADING);
            m_text_format->SetParagraphAlignment(DWRITE_PARAGRAPH_ALIGNMENT_CENTER);
        }
    }
    
    return true;
}

bool SubMenuWindow::InitD2DResources() {
    if (!g_d2d_factory || !g_dwrite_factory) {
        return false;
    }
    
    m_dwrite_factory = g_dwrite_factory;
    
    // 创建渲染目标
    RECT rc;
    GetClientRect(m_hwnd, &rc);
    
    D2D1_SIZE_U size = D2D1::SizeU(rc.right - rc.left, rc.bottom - rc.top);
    
    HRESULT hr = g_d2d_factory->CreateHwndRenderTarget(
        D2D1::RenderTargetProperties(),
        D2D1::HwndRenderTargetProperties(m_hwnd, size),
        &m_render_target
    );
    
    if (FAILED(hr)) {
        return false;
    }
    
    // 创建文本格式
    hr = m_dwrite_factory->CreateTextFormat(
        L"Segoe UI Emoji",
        nullptr,
        DWRITE_FONT_WEIGHT_NORMAL,
        DWRITE_FONT_STYLE_NORMAL,
        DWRITE_FONT_STRETCH_NORMAL,
        14.0f,
        L"zh-CN",
        &m_text_format
    );
    
    if (FAILED(hr)) {
        return false;
    }
    
    m_text_format->SetTextAlignment(DWRITE_TEXT_ALIGNMENT_LEADING);
    m_text_format->SetParagraphAlignment(DWRITE_PARAGRAPH_ALIGNMENT_CENTER);
    
    return true;
}

void SubMenuWindow::ReleaseD2DResources() {
    if (m_text_format) {
        m_text_format->Release();
        m_text_format = nullptr;
    }
    
    if (m_render_target) {
        m_render_target->Release();
        m_render_target = nullptr;
    }
    
    m_dwrite_factory = nullptr;
}

void SubMenuWindow::CalculateSize() {
    if (m_items.empty() || !m_dwrite_factory || !m_text_format) {
        m_width = MIN_WIDTH;
        m_height = 0;
        return;
    }
    
    // 计算所需的宽度和高度
    float max_width = (float)MIN_WIDTH;
    float total_height = 0;
    
    for (const auto& item : m_items) {
        if (item.separator) {
            total_height += SEPARATOR_HEIGHT;
        } else {
            total_height += ITEM_HEIGHT;
            
            // 计算文本宽度
            IDWriteTextLayout* layout = nullptr;
            HRESULT hr = m_dwrite_factory->CreateTextLayout(
                item.text.c_str(),
                (UINT32)item.text.length(),
                m_text_format,
                1000.0f,
                (float)ITEM_HEIGHT,
                &layout
            );
            
            if (SUCCEEDED(hr) && layout) {
                DWRITE_TEXT_METRICS metrics;
                layout->GetMetrics(&metrics);
                
                float item_width = metrics.width + PADDING_LEFT + PADDING_RIGHT;
                
                // 如果有子菜单，需要额外空间显示箭头
                if (!item.sub_items.empty()) {
                    item_width += 20.0f;
                }
                
                if (item_width > max_width) {
                    max_width = item_width;
                }
                
                layout->Release();
            }
        }
    }
    
    m_width = (int)max_width;
    m_height = (int)total_height;
}

void SubMenuWindow::CalculatePosition(int x, int y, int width_px, int height_px, int& out_x, int& out_y) {
    // 获取工作区域（排除任务栏），work_area 为屏幕像素
    HMONITOR monitor = MonitorFromPoint({x, y}, MONITOR_DEFAULTTONEAREST);
    MONITORINFO mi = {};
    mi.cbSize = sizeof(MONITORINFO);
    GetMonitorInfo(monitor, &mi);
    
    RECT work_area = mi.rcWork;
    
    out_x = x;
    out_y = y;
    
    if (out_x + width_px > work_area.right) {
        out_x = x - width_px;
        if (out_x < work_area.left) {
            out_x = work_area.right - width_px;
        }
    }
    if (out_y + height_px > work_area.bottom) {
        out_y = y - height_px;
        if (out_y < work_area.top) {
            out_y = work_area.bottom - height_px;
        }
    }
    if (out_x < work_area.left) out_x = work_area.left;
    if (out_y < work_area.top) out_y = work_area.top;
}

void SubMenuWindow::Show(const std::vector<MenuItem>& items, int x, int y, std::function<void(int, int)> callback) {
    if (!m_hwnd || items.empty()) {
        return;
    }

    m_theme = BuildCurrentMenuTheme();

    if (!m_dwrite_factory) {
        m_dwrite_factory = g_dwrite_factory;
    }
    if (!m_text_format && m_dwrite_factory) {
        HRESULT hr = m_dwrite_factory->CreateTextFormat(
            L"Segoe UI Emoji",
            nullptr,
            DWRITE_FONT_WEIGHT_NORMAL,
            DWRITE_FONT_STYLE_NORMAL,
            DWRITE_FONT_STRETCH_NORMAL,
            14.0f,
            L"zh-CN",
            &m_text_format
        );
        if (SUCCEEDED(hr) && m_text_format) {
            m_text_format->SetTextAlignment(DWRITE_TEXT_ALIGNMENT_LEADING);
            m_text_format->SetParagraphAlignment(DWRITE_PARAGRAPH_ALIGNMENT_CENTER);
        }
    }

    m_items = items;
    m_callback = callback;
    m_hovered_index = -1;
    m_selected_index = -1;
    
    // 计算窗口大小（CalculateSize 结果为 DIP）
    CalculateSize();
    
    // 子菜单窗口和 HwndRenderTarget 需要像素尺寸，按窗口 DPI 换算
    UINT wnd_dpi = GetDpiForWindow(m_hwnd);
    if (wnd_dpi == 0) wnd_dpi = 96;
    int width_px = (int)((float)m_width * (float)wnd_dpi / 96.0f + 0.5f);
    int height_px = (int)((float)m_height * (float)wnd_dpi / 96.0f + 0.5f);
    if (width_px < 1) width_px = 1;
    if (height_px < 1) height_px = 1;
    
    // 计算窗口位置（边界检查使用像素尺寸）
    int pos_x, pos_y;
    CalculatePosition(x, y, width_px, height_px, pos_x, pos_y);
    
    // 调整窗口大小和位置（使用像素）
    SetWindowPos(m_hwnd, HWND_TOPMOST, pos_x, pos_y, width_px, height_px,
                 SWP_SHOWWINDOW);
    
    // 重新创建渲染目标（因为窗口大小改变了）
    if (m_render_target) {
        m_render_target->Release();
        m_render_target = nullptr;
    }
    
    D2D1_SIZE_U size = D2D1::SizeU((UINT)width_px, (UINT)height_px);
    if (g_d2d_factory) {
        HRESULT hr = g_d2d_factory->CreateHwndRenderTarget(
            D2D1::RenderTargetProperties(),
            D2D1::HwndRenderTargetProperties(m_hwnd, size),
            &m_render_target
        );
        if (SUCCEEDED(hr) && m_render_target) {
            // 子菜单窗口也使用自身窗口 DPI，保证 1 逻辑单位 ≈ 1 像素
            UINT dpi = GetDpiForWindow(m_hwnd);
            float fdpi = dpi > 0 ? (float)dpi : 96.0f;
            m_render_target->SetDpi(fdpi, fdpi);
        }
    }
    
    m_visible = true;
    g_visible_submenus.insert(this);
    m_ignore_outside_click_until = GetTickCount() + 180;
    
    // 只有顶层子菜单才设置为当前活动的子菜单
    if (m_nesting_level == 0) {
        g_active_submenu = this;
        
        // 只有顶层子菜单才安装鼠标钩子
        if (!m_mouse_hook) {
            m_mouse_hook = SetWindowsHookEx(
                WH_MOUSE_LL,
                MouseHookProc,
                g_emoji_window_module ? g_emoji_window_module : GetModuleHandle(nullptr),
                0);
        }
    }
    
    // 渲染菜单
    Render();

    SetFocus(m_hwnd);
    
    // 执行显示动画
    if (m_animation_enabled) {
        switch (m_animation_type) {
            case ANIMATION_FADE:
                AnimateFadeIn();
                break;
            case ANIMATION_SLIDE:
                AnimateSlide();
                break;
            case ANIMATION_SCALE:
                AnimateScale();
                break;
            default:
                break;
        }
    }
    
    // 设置鼠标跟踪
    TRACKMOUSEEVENT tme = {};
    tme.cbSize = sizeof(TRACKMOUSEEVENT);
    tme.dwFlags = TME_LEAVE;
    tme.hwndTrack = m_hwnd;
    TrackMouseEvent(&tme);
}

void SubMenuWindow::Hide() {
    g_visible_submenus.erase(this);
    if (m_hwnd && m_visible) {
        // 先隐藏所有子菜单
        HideAllChildSubMenus();
        
        ShowWindow(m_hwnd, SW_HIDE);
        m_visible = false;
        m_items.clear();
        m_hovered_index = -1;
        m_selected_index = -1;
        m_hover_item_for_submenu = -1;
        
        // 停止定时器
        KillTimer(m_hwnd, 1);
        
        // 只有顶层子菜单才卸载鼠标钩子
        if (m_nesting_level == 0) {
            if (m_mouse_hook) {
                UnhookWindowsHookEx(m_mouse_hook);
                m_mouse_hook = nullptr;
            }
            
            // 清除当前活动的子菜单
            if (g_active_submenu == this) {
                g_active_submenu = nullptr;
            }
        }
        
        // 清除父窗口菜单栏的悬停和打开状态
        if (m_parent) {
            auto it = g_menubars.find(m_parent);
            if (it != g_menubars.end()) {
                MenuBarState* menubar = it->second;
                menubar->hovered_index = -1;
                menubar->opened_index = -1;
                InvalidateRect(m_parent, nullptr, FALSE);  // 重绘菜单栏
            }
        }
    }
}

int SubMenuWindow::HitTest(int x, int y) {
    float current_y = 0;
    
    for (size_t i = 0; i < m_items.size(); i++) {
        float item_height = m_items[i].separator ? (float)SEPARATOR_HEIGHT : (float)ITEM_HEIGHT;
        
        if (y >= current_y && y < current_y + item_height) {
            // 分隔线和禁用的菜单项不响应
            if (m_items[i].separator || !m_items[i].enabled) {
                return -1;
            }
            return (int)i;
        }
        
        current_y += item_height;
    }
    
    return -1;
}

void SubMenuWindow::OnMouseMove(int x, int y) {
    // 子菜单用 D2D 绘制（DIP），WM 给的是像素，需转为 DIP 再命中
    UINT dpi = GetDpiForWindow(m_hwnd);
    if (dpi == 0) dpi = 96;
    int dip_x = (int)((float)x * 96.0f / (float)dpi);
    int dip_y = (int)((float)y * 96.0f / (float)dpi);
    int new_hovered = HitTest(dip_x, dip_y);
    
    if (new_hovered != m_hovered_index) {
        int old_hovered = m_hovered_index;
        m_hovered_index = new_hovered;
        
        // 如果悬停到新的菜单项
        if (m_hovered_index >= 0) {
            // 检查是否有子菜单
            if (HasSubMenu(m_hovered_index)) {
                // 记录悬停开始时间（用于延迟显示）
                m_hover_start_time = GetTickCount();
                m_hover_item_for_submenu = m_hovered_index;
                
                // 启动定时器检查是否需要显示子菜单
                SetTimer(m_hwnd, 1, 50, nullptr);  // 每50ms检查一次
            } else {
                // 如果悬停到没有子菜单的项，关闭已打开的子菜单
                if (m_child_submenu) {
                    m_child_submenu->Hide();
                    delete m_child_submenu;
                    m_child_submenu = nullptr;
                }
                m_hover_item_for_submenu = -1;
            }
        } else {
            m_hover_item_for_submenu = -1;
        }
        
        Render();
    }
}

void SubMenuWindow::OnClick(int x, int y) {
    WriteLog("SubMenuWindow::OnClick: x=%d, y=%d", x, y);
    // 子菜单绘制为 DIP，鼠标为像素，转为 DIP 再命中
    UINT dpi = GetDpiForWindow(m_hwnd);
    if (dpi == 0) dpi = 96;
    int dip_x = (int)((float)x * 96.0f / (float)dpi);
    int dip_y = (int)((float)y * 96.0f / (float)dpi);
    int clicked_index = HitTest(dip_x, dip_y);
    WriteLog("SubMenuWindow::OnClick: clicked_index=%d, m_items.size()=%zu", clicked_index, m_items.size());
    
    if (clicked_index >= 0 && clicked_index < (int)m_items.size()) {
        const MenuItem& item = m_items[clicked_index];
        WriteLog("SubMenuWindow::OnClick: item clicked, id=%d, enabled=%d, has_submenu=%d", 
                item.id, item.enabled, HasSubMenu(clicked_index));
        
        // 如果有子菜单，立即显示（不等待延迟）
        if (HasSubMenu(clicked_index)) {
            if (m_callback) {
                m_callback(m_menu_id, item.id);
            }
            WriteLog("SubMenuWindow::OnClick: showing child submenu");
            ShowChildSubMenu(clicked_index);
            return;
        }
        
        // 保存菜单项ID（因为后面可能会清空 m_items）
        int item_id = item.id;
        
        // 触发回调
        WriteLog("SubMenuWindow::OnClick: calling callback, m_callback=%p, m_menu_id=%d, item_id=%d", 
                m_callback, m_menu_id, item_id);
        if (m_callback) {
            m_callback(m_menu_id, item_id);
            WriteLog("SubMenuWindow::OnClick: callback called successfully");
        } else {
            WriteLog("SubMenuWindow::OnClick: ERROR: m_callback is NULL!");
        }
        
        // 关闭所有菜单（包括父菜单）
        SubMenuWindow* root = this;
        while (root->m_parent_submenu) {
            root = root->m_parent_submenu;
        }
        root->Hide();
    } else {
        WriteLog("SubMenuWindow::OnClick: no item clicked");
    }
}

void SubMenuWindow::OnMouseLeave() {
    if (m_hovered_index != -1) {
        m_hovered_index = -1;
        m_hover_item_for_submenu = -1;
        Render();
    }
}

void SubMenuWindow::MoveToPreviousItem() {
    if (m_items.empty()) return;
    
    int start_index = m_selected_index;
    
    do {
        m_selected_index--;
        if (m_selected_index < 0) {
            m_selected_index = (int)m_items.size() - 1;
        }
        
        // 避免无限循环
        if (m_selected_index == start_index) break;
        
    } while (m_items[m_selected_index].separator || !m_items[m_selected_index].enabled);
    
    Render();
}

void SubMenuWindow::MoveToNextItem() {
    if (m_items.empty()) return;
    
    int start_index = m_selected_index;
    
    do {
        m_selected_index++;
        if (m_selected_index >= (int)m_items.size()) {
            m_selected_index = 0;
        }
        
        // 避免无限循环
        if (m_selected_index == start_index) break;
        
    } while (m_items[m_selected_index].separator || !m_items[m_selected_index].enabled);
    
    Render();
}

void SubMenuWindow::ActivateCurrentItem() {
    if (m_selected_index >= 0 && m_selected_index < (int)m_items.size()) {
        const MenuItem& item = m_items[m_selected_index];
        
        if (item.enabled && !item.separator) {
            if (HasSubMenu(m_selected_index)) {
                if (m_callback) {
                    m_callback(m_menu_id, item.id);
                }
                ShowChildSubMenu(m_selected_index);
                return;
            }
            if (m_callback) {
                m_callback(m_menu_id, item.id);
            }
            Hide();
        }
    }
}

void SubMenuWindow::OnKeyDown(WPARAM key) {
    switch (key) {
        case VK_UP:
            MoveToPreviousItem();
            break;
            
        case VK_DOWN:
            MoveToNextItem();
            break;
            
        case VK_RETURN:
            ActivateCurrentItem();
            break;
            
        case VK_ESCAPE:
            Hide();
            break;
    }
}

void SubMenuWindow::Render() {
    if (!m_render_target || !m_text_format || m_items.empty()) {
        return;
    }

    m_render_target->BeginDraw();
    m_render_target->Clear(m_theme.backgroundColor);

    const float surface_inset = 1.0f;
    const float surface_radius = (float)(std::max)(0, m_theme.cornerRadius > 0 ? m_theme.cornerRadius : 8);
    const float item_inset_x = 6.0f;
    const float hover_radius = (std::max)(4.0f, surface_radius - 2.0f);
    const float item_height = (float)ITEM_HEIGHT;
    const float separator_height = (float)SEPARATOR_HEIGHT;
    const float text_padding_x = 14.0f;
    const float arrow_area_w = 20.0f;

    ID2D1SolidColorBrush* panel_brush = nullptr;
    ID2D1SolidColorBrush* text_brush = nullptr;
    ID2D1SolidColorBrush* disabled_brush = nullptr;
    ID2D1SolidColorBrush* hover_brush = nullptr;
    ID2D1SolidColorBrush* separator_brush = nullptr;
    ID2D1SolidColorBrush* border_brush = nullptr;

    m_render_target->CreateSolidColorBrush(m_theme.backgroundColor, &panel_brush);
    m_render_target->CreateSolidColorBrush(m_theme.textColor, &text_brush);
    m_render_target->CreateSolidColorBrush(m_theme.disabledColor, &disabled_brush);
    m_render_target->CreateSolidColorBrush(m_theme.hoverColor, &hover_brush);
    m_render_target->CreateSolidColorBrush(m_theme.separatorColor, &separator_brush);
    m_render_target->CreateSolidColorBrush(m_theme.borderColor, &border_brush);

    if (panel_brush && border_brush) {
        D2D1_ROUNDED_RECT panel_rect = D2D1::RoundedRect(
            D2D1::RectF(
                surface_inset,
                surface_inset,
                (float)m_width - surface_inset,
                (float)m_height - surface_inset),
            surface_radius,
            surface_radius);
        m_render_target->FillRoundedRectangle(panel_rect, panel_brush);
        if (m_theme.borderWidth > 0) {
            m_render_target->DrawRoundedRectangle(panel_rect, border_brush, (float)m_theme.borderWidth);
        }
    }

    float y = 0.0f;
    for (size_t i = 0; i < m_items.size(); i++) {
        const MenuItem& item = m_items[i];
        if (item.separator) {
            if (separator_brush) {
                float sep_y = y + separator_height / 2.0f;
                m_render_target->DrawLine(
                    D2D1::Point2F(16.0f, sep_y),
                    D2D1::Point2F((float)m_width - 16.0f, sep_y),
                    separator_brush,
                    1.0f
                );
            }
            y += separator_height;
            continue;
        }

        D2D1_RECT_F item_rect = D2D1::RectF(
            item_inset_x,
            y,
            (float)m_width - item_inset_x,
            y + item_height
        );

        if ((int)i == m_hovered_index || (int)i == m_selected_index) {
            if (hover_brush) {
                m_render_target->FillRoundedRectangle(
                    D2D1::RoundedRect(item_rect, hover_radius, hover_radius),
                    hover_brush
                );
            }
        }

        ID2D1SolidColorBrush* brush = item.enabled ? text_brush : disabled_brush;
        if (brush) {
            D2D1_RECT_F text_rect = D2D1::RectF(
                item_rect.left + text_padding_x,
                y,
                item_rect.right - text_padding_x - (HasSubMenu((int)i) ? arrow_area_w : 0.0f),
                y + item_height
            );
            m_render_target->DrawText(
                item.text.c_str(),
                (UINT32)item.text.length(),
                m_text_format,
                text_rect,
                brush,
                D2D1_DRAW_TEXT_OPTIONS_ENABLE_COLOR_FONT
            );
        }

        if (HasSubMenu((int)i)) {
            ID2D1SolidColorBrush* arrow_brush = item.enabled ? text_brush : disabled_brush;
            if (arrow_brush) {
                D2D1_RECT_F arrow_rect = D2D1::RectF(
                    item_rect.right - 18.0f,
                    y + item_height / 2.0f - 4.0f,
                    item_rect.right - 10.0f,
                    y + item_height / 2.0f + 4.0f
                );
                m_render_target->DrawLine(
                    D2D1::Point2F(arrow_rect.left, arrow_rect.top),
                    D2D1::Point2F(arrow_rect.right, y + item_height / 2.0f),
                    arrow_brush,
                    1.2f
                );
                m_render_target->DrawLine(
                    D2D1::Point2F(arrow_rect.left, arrow_rect.bottom),
                    D2D1::Point2F(arrow_rect.right, y + item_height / 2.0f),
                    arrow_brush,
                    1.2f
                );
            }
        }

        y += item_height;
    }

    if (panel_brush) panel_brush->Release();
    if (text_brush) text_brush->Release();
    if (disabled_brush) disabled_brush->Release();
    if (hover_brush) hover_brush->Release();
    if (separator_brush) separator_brush->Release();
    if (border_brush) border_brush->Release();

    m_render_target->EndDraw();
}

LRESULT CALLBACK SubMenuWindow::WindowProc(HWND hwnd, UINT msg, WPARAM wparam, LPARAM lparam) {
    SubMenuWindow* window = nullptr;
    
    if (msg == WM_CREATE) {
        CREATESTRUCT* cs = (CREATESTRUCT*)lparam;
        window = (SubMenuWindow*)cs->lpCreateParams;
        SetWindowLongPtr(hwnd, GWLP_USERDATA, (LONG_PTR)window);
    } else {
        window = (SubMenuWindow*)GetWindowLongPtr(hwnd, GWLP_USERDATA);
    }
    
    if (!window) {
        return DefWindowProc(hwnd, msg, wparam, lparam);
    }
    
    switch (msg) {
        case WM_PAINT: {
            PAINTSTRUCT ps;
            BeginPaint(hwnd, &ps);
            window->Render();
            EndPaint(hwnd, &ps);
            return 0;
        }
        
        case WM_MOUSEMOVE: {
            int x = GET_X_LPARAM(lparam);
            int y = GET_Y_LPARAM(lparam);
            window->OnMouseMove(x, y);
            return 0;
        }

        case WM_MOUSEACTIVATE:
            return MA_ACTIVATE;
        
        case WM_LBUTTONUP: {
            int x = GET_X_LPARAM(lparam);
            int y = GET_Y_LPARAM(lparam);
            window->OnClick(x, y);
            return 0;
        }
        
        case WM_MOUSELEAVE: {
            window->OnMouseLeave();
            return 0;
        }
        
        case WM_KEYDOWN: {
            window->OnKeyDown(wparam);
            return 0;
        }
        
        case WM_TIMER: {
            // 检查是否需要显示子菜单（延迟显示）
            if (wparam == 1 && window->m_hover_item_for_submenu >= 0) {
                DWORD elapsed = GetTickCount() - window->m_hover_start_time;
                if (elapsed >= SUBMENU_HOVER_DELAY) {
                    // 延迟时间已到，显示子菜单
                    window->ShowChildSubMenu(window->m_hover_item_for_submenu);
                    window->m_hover_item_for_submenu = -1;
                    KillTimer(hwnd, 1);
                }
            }
            // 淡入动画定时器
            else if (wparam == 2) {
                DWORD elapsed = GetTickCount() - window->m_animation_start_time;
                float progress = (float)elapsed / ANIMATION_DURATION;
                
                if (progress >= 1.0f) {
                    // 动画完成
                    SetLayeredWindowAttributes(hwnd, 0, 255, LWA_ALPHA);
                    window->m_is_animating = false;
                    KillTimer(hwnd, 2);
                } else {
                    // 更新透明度
                    BYTE alpha = (BYTE)(255 * progress);
                    SetLayeredWindowAttributes(hwnd, 0, alpha, LWA_ALPHA);
                }
            }
            // 淡出动画定时器
            else if (wparam == 3) {
                DWORD elapsed = GetTickCount() - window->m_animation_start_time;
                float progress = (float)elapsed / ANIMATION_DURATION;
                
                if (progress >= 1.0f) {
                    // 动画完成，隐藏窗口
                    ShowWindow(hwnd, SW_HIDE);
                    window->m_is_animating = false;
                    KillTimer(hwnd, 3);
                } else {
                    // 更新透明度
                    BYTE alpha = (BYTE)(255 * (1.0f - progress));
                    SetLayeredWindowAttributes(hwnd, 0, alpha, LWA_ALPHA);
                }
            }
            // 滑动动画定时器
            else if (wparam == 4) {
                DWORD elapsed = GetTickCount() - window->m_animation_start_time;
                float progress = (float)elapsed / ANIMATION_DURATION;
                
                if (progress >= 1.0f) {
                    // 动画完成
                    RECT rect;
                    GetWindowRect(hwnd, &rect);
                    SetWindowPos(hwnd, nullptr, 
                        rect.left, rect.top, 
                        rect.right - rect.left, window->m_height,
                        SWP_NOZORDER | SWP_NOACTIVATE);
                    window->m_is_animating = false;
                    KillTimer(hwnd, 4);
                } else {
                    // 更新高度
                    RECT rect;
                    GetWindowRect(hwnd, &rect);
                    int current_height = (int)(window->m_height * progress);
                    SetWindowPos(hwnd, nullptr, 
                        rect.left, rect.top, 
                        rect.right - rect.left, current_height,
                        SWP_NOZORDER | SWP_NOACTIVATE);
                }
            }
            // 缩放动画定时器
            else if (wparam == 5) {
                DWORD elapsed = GetTickCount() - window->m_animation_start_time;
                float progress = (float)elapsed / ANIMATION_DURATION;
                
                if (progress >= 1.0f) {
                    // 动画完成
                    RECT rect;
                    GetWindowRect(hwnd, &rect);
                    int center_x = rect.left + window->m_width / 2;
                    int center_y = rect.top + window->m_height / 2;
                    SetWindowPos(hwnd, nullptr, 
                        center_x - window->m_width / 2, 
                        center_y - window->m_height / 2,
                        window->m_width, window->m_height,
                        SWP_NOZORDER | SWP_NOACTIVATE);
                    SetLayeredWindowAttributes(hwnd, 0, 255, LWA_ALPHA);
                    window->m_is_animating = false;
                    KillTimer(hwnd, 5);
                } else {
                    // 更新大小和透明度
                    RECT rect;
                    GetWindowRect(hwnd, &rect);
                    int center_x = rect.left;
                    int center_y = rect.top;
                    int current_width = (int)(window->m_width * progress);
                    int current_height = (int)(window->m_height * progress);
                    BYTE alpha = (BYTE)(255 * progress);
                    
                    SetWindowPos(hwnd, nullptr, 
                        center_x - current_width / 2, 
                        center_y - current_height / 2,
                        current_width, current_height,
                        SWP_NOZORDER | SWP_NOACTIVATE);
                    SetLayeredWindowAttributes(hwnd, 0, alpha, LWA_ALPHA);
                }
            }
            return 0;
        }
        
        case WM_KILLFOCUS: {
            // 失去焦点时隐藏菜单
            return 0;
            return 0;
        }
        
        case WM_DESTROY: {
            return 0;
        }
    }
    
    return DefWindowProc(hwnd, msg, wparam, lparam);
}

// 鼠标钩子过程：检测点击菜单外区域
LRESULT CALLBACK SubMenuWindow::MouseHookProc(int nCode, WPARAM wParam, LPARAM lParam) {
    if (nCode >= 0 && wParam == WM_LBUTTONDOWN) {
        if (!g_visible_submenus.empty()) {
            DWORD ignore_outside_click_until = 0;
            for (SubMenuWindow* menu : g_visible_submenus) {
                if (menu && menu->IsVisible()) {
                    ignore_outside_click_until = (std::max)(ignore_outside_click_until, menu->m_ignore_outside_click_until);
                }
            }
            bool ignore_outside_close = GetTickCount() <= ignore_outside_click_until;
            MSLLHOOKSTRUCT* pMouseStruct = (MSLLHOOKSTRUCT*)lParam;
            POINT pt = pMouseStruct->pt;
            
            SubMenuWindow* target_menu = FindVisibleSubMenuAtPoint(pt);
            if (target_menu && target_menu->GetHwnd()) {
                POINT client_pt = pt;
                ScreenToClient(target_menu->GetHwnd(), &client_pt);
                target_menu->OnClick(client_pt.x, client_pt.y);
                return 1;
            }

            if (!ignore_outside_close) {
                // 点击在所有菜单外，关闭顶层菜单（会自动关闭所有子菜单）
                for (SubMenuWindow* menu : g_visible_submenus) {
                    if (menu && menu->IsVisible() && !menu->m_parent_submenu) {
                        menu->Hide();
                        break;
                    }
                }
            }
        }
    }
    
    return CallNextHookEx(nullptr, nCode, wParam, lParam);
}

bool SubMenuWindow::ContainsActivePoint(POINT screen_pt) {
    return FindVisibleSubMenuAtPoint(screen_pt) != nullptr;
}

bool SubMenuWindow::DispatchActiveClick(POINT screen_pt) {
    SubMenuWindow* target_menu = FindVisibleSubMenuAtPoint(screen_pt);
    if (!target_menu || !target_menu->GetHwnd()) {
        return false;
    }

    POINT client_pt = screen_pt;
    ScreenToClient(target_menu->GetHwnd(), &client_pt);
    target_menu->OnClick(client_pt.x, client_pt.y);
    return true;
}

// ============================================================================
// Task 4.1: 嵌套子菜单支持
// ============================================================================

// 检查菜单项是否有子菜单
bool SubMenuWindow::HasSubMenu(int index) const {
    if (index < 0 || index >= (int)m_items.size()) {
        return false;
    }
    
    const MenuItem& item = m_items[index];
    // 检查菜单项是否有子菜单（通过 sub_items 判断）
    return !item.sub_items.empty();
}

// 显示子菜单的子菜单（嵌套）
void SubMenuWindow::ShowChildSubMenu(int index) {
    // 检查嵌套层级限制
    if (m_nesting_level >= MAX_NESTING_LEVEL) {
        return;
    }
    
    // 检查索引有效性
    if (index < 0 || index >= (int)m_items.size()) {
        return;
    }
    
    // 检查是否有子菜单
    if (!HasSubMenu(index)) {
        return;
    }
    
    const MenuItem& item = m_items[index];
    
    // 如果已经有子菜单打开，先关闭
    if (m_child_submenu) {
        m_child_submenu->Hide();
        delete m_child_submenu;
        m_child_submenu = nullptr;
    }
    
    // 创建新的子菜单窗口
    m_child_submenu = new SubMenuWindow();
    m_child_submenu->m_nesting_level = m_nesting_level + 1;
    m_child_submenu->SetParentSubMenu(this);
    
    // 创建子菜单窗口
    if (!m_child_submenu->Create(m_hwnd, m_menu_id)) {
        delete m_child_submenu;
        m_child_submenu = nullptr;
        return;
    }
    
    // 计算子菜单显示位置（在当前菜单项右侧），item_rect 为 DIP
    RECT item_rect;
    item_rect.left = 0;
    item_rect.top = 0;
    item_rect.right = m_width;
    item_rect.bottom = 0;

    for (int i = 0; i < index; i++) {
        if (m_items[i].separator) {
            item_rect.top += SEPARATOR_HEIGHT;
            item_rect.bottom += SEPARATOR_HEIGHT;
        } else {
            item_rect.top += ITEM_HEIGHT;
            item_rect.bottom += ITEM_HEIGHT;
        }
    }

    if (item.separator) {
        item_rect.bottom = item_rect.top + SEPARATOR_HEIGHT;
    } else {
        item_rect.bottom = item_rect.top + ITEM_HEIGHT;
    }

    UINT dpi = GetDpiForWindow(m_hwnd);
    if (dpi == 0) dpi = 96;
    float scaleToPx = (float)dpi / 96.0f;
    POINT pt = {
        (LONG)(item_rect.right * scaleToPx),
        (LONG)(item_rect.top * scaleToPx)
    };
    ClientToScreen(m_hwnd, &pt);
    
    // 显示子菜单
    m_child_submenu->Show(item.sub_items, pt.x, pt.y, m_callback);
}

// 隐藏所有子菜单
void SubMenuWindow::HideAllChildSubMenus() {
    if (m_child_submenu) {
        // 递归隐藏所有子子菜单
        m_child_submenu->HideAllChildSubMenus();
        m_child_submenu->Hide();
        delete m_child_submenu;
        m_child_submenu = nullptr;
    }
}

// ============================================================================
// Task 4.2: 动画效果实现
// ============================================================================

// 执行淡入动画
void SubMenuWindow::AnimateFadeIn() {
    if (!m_hwnd || !m_animation_enabled) {
        return;
    }
    
    // 设置窗口为分层窗口（支持透明度）
    SetWindowLong(m_hwnd, GWL_EXSTYLE, 
        GetWindowLong(m_hwnd, GWL_EXSTYLE) | WS_EX_LAYERED);
    
    m_is_animating = true;
    m_animation_start_time = GetTickCount();
    
    // 启动动画定时器
    SetTimer(m_hwnd, 2, 16, nullptr);  // 约60fps
}

// 执行淡出动画
void SubMenuWindow::AnimateFadeOut() {
    if (!m_hwnd || !m_animation_enabled) {
        return;
    }
    
    m_is_animating = true;
    m_animation_start_time = GetTickCount();
    
    // 启动动画定时器
    SetTimer(m_hwnd, 3, 16, nullptr);  // 约60fps
}

// 执行滑动动画
void SubMenuWindow::AnimateSlide() {
    if (!m_hwnd || !m_animation_enabled) {
        return;
    }
    
    // 获取窗口位置
    RECT rect;
    GetWindowRect(m_hwnd, &rect);
    
    int final_height = rect.bottom - rect.top;
    
    // 从0高度开始
    SetWindowPos(m_hwnd, nullptr, 
        rect.left, rect.top, 
        rect.right - rect.left, 0,
        SWP_NOZORDER | SWP_NOACTIVATE);
    
    m_is_animating = true;
    m_animation_start_time = GetTickCount();
    
    // 启动动画定时器
    SetTimer(m_hwnd, 4, 16, nullptr);  // 约60fps
}

// 执行缩放动画
void SubMenuWindow::AnimateScale() {
    if (!m_hwnd || !m_animation_enabled) {
        return;
    }
    
    // 设置窗口为分层窗口
    SetWindowLong(m_hwnd, GWL_EXSTYLE, 
        GetWindowLong(m_hwnd, GWL_EXSTYLE) | WS_EX_LAYERED);
    
    // 获取窗口位置
    RECT rect;
    GetWindowRect(m_hwnd, &rect);
    
    int final_width = rect.right - rect.left;
    int final_height = rect.bottom - rect.top;
    
    // 从中心点开始缩放
    int center_x = rect.left + final_width / 2;
    int center_y = rect.top + final_height / 2;
    
    // 初始大小为0
    SetWindowPos(m_hwnd, nullptr, 
        center_x, center_y, 0, 0,
        SWP_NOZORDER | SWP_NOACTIVATE);
    
    m_is_animating = true;
    m_animation_start_time = GetTickCount();
    
    // 启动动画定时器
    SetTimer(m_hwnd, 5, 16, nullptr);  // 约60fps
}

// ============================================================================
// Task 4.3: 主题支持实现
// ============================================================================

// 默认主题（亮色）
SubMenuWindow::MenuTheme SubMenuWindow::MenuTheme::Default() {
    return BuildCurrentMenuTheme();
}

// 亮色主题
SubMenuWindow::MenuTheme SubMenuWindow::MenuTheme::Light() {
    return BuildCurrentMenuTheme();
}

// 暗色主题
SubMenuWindow::MenuTheme SubMenuWindow::MenuTheme::Dark() {
    return BuildCurrentMenuTheme();
}

// 蓝色主题
SubMenuWindow::MenuTheme SubMenuWindow::MenuTheme::Blue() {
    return BuildCurrentMenuTheme();
}

// 设置主题
void SubMenuWindow::SetTheme(const MenuTheme& theme) {
    m_theme = theme;
    
    // 如果窗口已创建，重新渲染
    if (m_hwnd && m_visible) {
        Render();
    }
}
