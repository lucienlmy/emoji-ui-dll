#pragma once
#include <windows.h>
#include <d2d1.h>
#include <dwrite.h>
#include <vector>
#include <string>
#include <functional>

// 前向声明
struct MenuItem;

// 子菜单窗口类
class SubMenuWindow {
public:
    SubMenuWindow();
    ~SubMenuWindow();

    // 创建子菜单窗口
    bool Create(HWND parent, int menu_id);
    
    // 显示子菜单（使用 std::function 支持 lambda）
    void Show(const std::vector<MenuItem>& items, int x, int y, std::function<void(int, int)> callback);
    
    // 隐藏子菜单
    void Hide();
    
    // 是否可见
    bool IsVisible() const { return m_visible; }
    
    // 获取窗口句柄
    HWND GetHwnd() const { return m_hwnd; }
    
    // 渲染子菜单
    void Render();
    
    // 鼠标移动处理
    void OnMouseMove(int x, int y);
    
    // 鼠标点击处理
    void OnClick(int x, int y);
    
    // 鼠标离开处理
    void OnMouseLeave();
    
    // 键盘按键处理
    void OnKeyDown(WPARAM key);
    
    // 检查是否有子菜单
    bool HasSubMenu(int index) const;
    
    // 显示子菜单的子菜单（嵌套）
    void ShowChildSubMenu(int index);
    
    // 隐藏所有子菜单
    void HideAllChildSubMenus();
    
    // 设置父子菜单（用于嵌套层级管理）
    void SetParentSubMenu(SubMenuWindow* parent) { m_parent_submenu = parent; }
    
    // 获取嵌套层级
    int GetNestingLevel() const { return m_nesting_level; }
    
    // Task 4.2: 动画效果
    // 启用/禁用动画
    void SetAnimationEnabled(bool enabled) { m_animation_enabled = enabled; }
    bool IsAnimationEnabled() const { return m_animation_enabled; }
    
    // 设置动画类型
    enum AnimationType {
        ANIMATION_NONE = 0,
        ANIMATION_FADE = 1,      // 淡入淡出
        ANIMATION_SLIDE = 2,     // 滑动展开
        ANIMATION_SCALE = 3      // 缩放效果
    };
    void SetAnimationType(AnimationType type) { m_animation_type = type; }
    AnimationType GetAnimationType() const { return m_animation_type; }
    
    // Task 4.3: 主题支持
    // 主题结构
    struct MenuTheme {
        D2D1_COLOR_F backgroundColor;    // 背景色
        D2D1_COLOR_F hoverColor;         // 悬停色
        D2D1_COLOR_F textColor;          // 文本色
        D2D1_COLOR_F disabledColor;      // 禁用文本色
        D2D1_COLOR_F borderColor;        // 边框色
        D2D1_COLOR_F separatorColor;     // 分隔线颜色
        int borderWidth;                 // 边框宽度
        int cornerRadius;                // 圆角半径
        int shadowSize;                  // 阴影大小
        
        // 预设主题
        static MenuTheme Light();        // 亮色主题
        static MenuTheme Dark();         // 暗色主题
        static MenuTheme Blue();         // 蓝色主题
        static MenuTheme Default();      // 默认主题
    };
    
    // 设置主题
    void SetTheme(const MenuTheme& theme);
    MenuTheme GetTheme() const { return m_theme; }
    
    // 窗口过程（必须是 public 才能在注册窗口类时使用）
    static LRESULT CALLBACK WindowProc(HWND hwnd, UINT msg, WPARAM wparam, LPARAM lparam);
    
    // 鼠标钩子过程（用于检测点击菜单外区域）
    static LRESULT CALLBACK MouseHookProc(int nCode, WPARAM wParam, LPARAM lParam);

private:
    // 计算子菜单位置（避免超出屏幕）
    void CalculatePosition(int x, int y, int width_px, int height_px, int& out_x, int& out_y);
    
    // 计算子菜单大小
    void CalculateSize();
    
    // 命中测试
    int HitTest(int x, int y);
    
    // 移动到上一个菜单项
    void MoveToPreviousItem();
    
    // 移动到下一个菜单项
    void MoveToNextItem();
    
    // 激活当前选中的菜单项
    void ActivateCurrentItem();
    
    // 初始化 Direct2D 资源
    bool InitD2DResources();
    
    // 释放 Direct2D 资源
    void ReleaseD2DResources();
    
    // Task 4.2: 动画相关私有方法
    // 执行淡入动画
    void AnimateFadeIn();
    
    // 执行淡出动画
    void AnimateFadeOut();
    
    // 执行滑动动画
    void AnimateSlide();
    
    // 执行缩放动画
    void AnimateScale();

private:
    HWND m_hwnd;                                    // 窗口句柄
    HWND m_parent;                                  // 父窗口句柄
    int m_menu_id;                                  // 菜单ID
    ID2D1HwndRenderTarget* m_render_target;         // D2D渲染目标
    IDWriteFactory* m_dwrite_factory;               // DirectWrite工厂
    IDWriteTextFormat* m_text_format;               // 文本格式
    std::vector<MenuItem> m_items;                  // 菜单项列表
    int m_hovered_index;                            // 悬停的菜单项索引
    int m_selected_index;                           // 选中的菜单项索引
    bool m_visible;                                 // 是否可见
    int m_width;                                    // 窗口宽度
    int m_height;                                   // 窗口高度
    std::function<void(int, int)> m_callback;       // 点击回调（使用 std::function）
    HHOOK m_mouse_hook;                             // 鼠标钩子句柄
    
    // 嵌套子菜单支持
    SubMenuWindow* m_parent_submenu;                // 父子菜单（用于嵌套）
    SubMenuWindow* m_child_submenu;                 // 当前打开的子子菜单
    int m_nesting_level;                            // 嵌套层级（0=顶层）
    DWORD m_hover_start_time;                       // 悬停开始时间（用于延迟显示）
    int m_hover_item_for_submenu;                   // 等待显示子菜单的菜单项索引
    
    // Task 4.2: 动画支持
    bool m_animation_enabled;                       // 是否启用动画
    AnimationType m_animation_type;                 // 动画类型
    bool m_is_animating;                            // 是否正在播放动画
    DWORD m_animation_start_time;                   // 动画开始时间
    
    // Task 4.3: 主题支持
    MenuTheme m_theme;                              // 当前主题
    
    // 样式常量
    static const int ITEM_HEIGHT = 32;              // 菜单项高度
    static const int SEPARATOR_HEIGHT = 8;          // 分隔线高度
    static const int PADDING_LEFT = 20;             // 左侧内边距
    static const int PADDING_RIGHT = 20;            // 右侧内边距
    static const int MIN_WIDTH = 150;               // 最小宽度
    static const int SHADOW_SIZE = 4;               // 阴影大小
    static const int SUBMENU_HOVER_DELAY = 300;     // 子菜单显示延迟（毫秒）
    static const int MAX_NESTING_LEVEL = 5;         // 最大嵌套层级
    static const int ANIMATION_DURATION = 150;      // 动画持续时间（毫秒）
};
