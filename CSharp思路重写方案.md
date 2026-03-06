# C# TabControl 思路重写方案

## C# TabControl 的工作原理

C# 的 TabControl：
1. **只有一个容器区域**（DisplayRectangle）
2. **所有TabPage的控件都添加到这个容器中**
3. **切换Tab时，只是改变控件的Visible属性**
4. **不创建多个窗口，不涉及窗口位置移动**

## 重写思路

### 当前设计的问题

```
当前设计：
TabControl
├── Tab1内容窗口 (独立窗口，Direct2D渲染)
├── Tab2内容窗口 (独立窗口，Direct2D渲染)  ← 问题：多个窗口重叠
└── Tab3内容窗口 (独立窗口，Direct2D渲染)
```

### 新设计

```
新设计：
TabControl
└── 单一容器窗口
    ├── Tab1的按钮组 (控件集合)
    ├── Tab2的按钮组 (控件集合)  ← 通过显示/隐藏控制
    └── Tab3的按钮组 (控件集合)
```

## 实现方案

### 方案1：单容器 + 控件集合（推荐）

```cpp
struct TabPageContent {
    int index;
    std::wstring title;
    std::vector<ButtonInfo> buttons;  // 这个Tab的按钮
    std::vector<HWND> childWindows;   // 这个Tab的子窗口（如Edit控件）
    bool visible;
};

struct TabControlState {
    HWND hTabControl;
    HWND hParent;
    HWND hContainerWindow;  // 单一容器窗口
    int currentIndex;
    std::vector<TabPageContent> pages;
    TabSwitchCallback callback;
};

// 创建TabControl时，只创建一个容器窗口
HWND hContainer = CreateWindowExW(...);

// 添加Tab时，不创建新窗口，只添加到pages数组
void AddTabItem(...) {
    TabPageContent page;
    page.index = pages.size();
    page.title = title;
    page.visible = false;
    pages.push_back(page);
}

// 在容器窗口中添加按钮
void AddButton(int tabIndex, ...) {
    pages[tabIndex].buttons.push_back(button);
}

// 切换Tab时，只改变按钮的可见性
void UpdateTabLayout() {
    for (auto& page : pages) {
        page.visible = (page.index == currentIndex);
    }
    InvalidateRect(hContainerWindow, nullptr, TRUE);
}

// 绘制时，只绘制当前Tab的按钮
void OnPaint() {
    for (auto& page : pages) {
        if (page.visible) {
            for (auto& button : page.buttons) {
                DrawButton(button);
            }
        }
    }
}
```

### 方案2：使用Panel容器（类似C#）

```cpp
// 为每个Tab创建一个Panel（普通窗口，不使用Direct2D）
HWND CreateTabPanel(HWND hParent, int index) {
    // 使用简单的窗口类，不使用Direct2D
    WNDCLASSW wc = {};
    wc.lpfnWndProc = DefWindowProcW;  // 默认窗口过程
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wc.lpszClassName = L"TabPanelClass";
    RegisterClassW(&wc);
    
    HWND hPanel = CreateWindowExW(
        0,
        L"TabPanelClass",
        L"",
        WS_CHILD | WS_CLIPCHILDREN,  // 初始不可见
        0, 0, 0, 0,
        hParent,
        nullptr,
        GetModuleHandle(nullptr),
        nullptr
    );
    
    return hPanel;
}

// 切换Tab时，只改变Panel的可见性
void SwitchTab(int index) {
    for (int i = 0; i < panels.size(); i++) {
        ShowWindow(panels[i], (i == index) ? SW_SHOW : SW_HIDE);
    }
}
```

## 推荐实现：方案1（单容器 + 控件集合）

这是最接近C# TabControl的方案，也是最简单的。

### 关键代码修改

#### 1. 修改数据结构

```cpp
struct TabPageContent {
    int index;
    std::wstring title;
    std::vector<ButtonInfo> buttons;
    std::vector<HWND> childWindows;
    bool visible;
};

struct TabControlState {
    HWND hTabControl;
    HWND hParent;
    HWND hContainerWindow;  // 单一容器窗口
    ID2D1HwndRenderTarget* render_target;  // 容器的渲染目标
    int currentIndex;
    std::vector<TabPageContent> pages;
    TabSwitchCallback callback;
};
```

#### 2. 创建TabControl

```cpp
extern "C" HWND __stdcall CreateTabControl(HWND hParent, int x, int y, int width, int height) {
    // ... 创建TabControl ...
    
    // 创建单一容器窗口
    HWND hContainer = CreateWindowExW(
        0,
        L"EmojiTabContentClass",
        L"",
        WS_CHILD | WS_VISIBLE | WS_CLIPCHILDREN,
        0, 0, 0, 0,
        hParent,
        nullptr,
        GetModuleHandle(nullptr),
        nullptr
    );
    
    state->hContainerWindow = hContainer;
    
    // 创建容器的渲染目标
    // ...
    
    return hTabControl;
}
```

#### 3. 添加Tab

```cpp
extern "C" int __stdcall AddTabItem(HWND hTabControl, ...) {
    // 不创建新窗口，只添加到pages数组
    TabPageContent page;
    page.index = pages.size();
    page.title = title;
    page.visible = false;
    
    state->pages.push_back(page);
    
    // 添加Tab项到TabControl
    TCITEMW tci = {};
    tci.mask = TCIF_TEXT;
    tci.pszText = (LPWSTR)title.c_str();
    TabCtrl_InsertItem(hTabControl, page.index, &tci);
    
    return page.index;
}
```

#### 4. 添加按钮

```cpp
extern "C" int __stdcall AddButtonToTab(HWND hTabControl, int tabIndex, ...) {
    auto it = g_tab_controls.find(hTabControl);
    if (it == g_tab_controls.end()) return -1;
    
    TabControlState* state = it->second;
    if (tabIndex < 0 || tabIndex >= state->pages.size()) return -1;
    
    ButtonInfo button;
    // ... 设置按钮属性 ...
    
    state->pages[tabIndex].buttons.push_back(button);
    
    return button.id;
}
```

#### 5. 切换Tab

```cpp
void UpdateTabLayout(TabControlState* state) {
    // 只改变可见性标志
    for (auto& page : state->pages) {
        page.visible = (page.index == state->currentIndex);
        
        // 隐藏/显示子窗口
        for (HWND hChild : page.childWindows) {
            ShowWindow(hChild, page.visible ? SW_SHOW : SW_HIDE);
        }
    }
    
    // 重绘容器
    InvalidateRect(state->hContainerWindow, nullptr, TRUE);
}
```

#### 6. 绘制

```cpp
case WM_PAINT: {
    // 只绘制当前可见Tab的按钮
    state->render_target->BeginDraw();
    state->render_target->Clear(D2D1::ColorF(0xF5F5FA, 1.0f));
    
    for (auto& page : state->pages) {
        if (page.visible) {
            for (auto& button : page.buttons) {
                DrawButton(state->render_target, state->dwrite_factory, button);
            }
        }
    }
    
    state->render_target->EndDraw();
}
```

## 优势

1. **只有一个容器窗口** - 不存在窗口重叠问题
2. **只有一个渲染目标** - 不存在渲染冲突
3. **简单的可见性控制** - 通过标志位控制绘制
4. **完全模仿C# TabControl** - 设计清晰，易于理解

## 需要修改的API

由于数据结构改变，需要修改以下API：

```cpp
// 旧API：添加Tab时自动创建内容窗口
AddTabItem(hTabControl, title, 0);  // hContentWindow参数废弃

// 新API：添加按钮到指定Tab
AddButtonToTab(hTabControl, tabIndex, emoji, text, x, y, w, h, color);

// 新API：添加子窗口到指定Tab
AddChildWindowToTab(hTabControl, tabIndex, hChildWindow);
```

## 总结

这个方案完全模仿C# TabControl的设计：
- 单一容器
- 控件集合
- 可见性控制

不再有多窗口重叠的问题，从根本上解决了Direct2D渲染冲突。
