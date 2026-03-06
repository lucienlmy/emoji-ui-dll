# 简化方案 - 删除TabControl，只保留编辑框

## 方案说明

由于TabControl的Direct2D渲染与子窗口冲突问题难以解决，我们采用简化方案：

1. **删除所有TabControl相关代码**
2. **保留基本窗口和编辑框功能**
3. **如果需要Tab功能，使用易语言自带的Tab控件**

## 需要删除的代码

### emoji_window.h

删除以下内容：
- `typedef void (__stdcall *TAB_CALLBACK)(...)`
- `struct TabPageInfo`
- `struct TabControlState`
- `extern std::map<HWND, TabControlState*> g_tab_controls;`
- 所有 TabControl 相关的函数声明（CreateTabControl, AddTabItem, 等）

### emoji_window.cpp

删除以下内容：
- `std::map<HWND, TabControlState*> g_tab_controls;`
- 所有 TabControl 相关的函数实现
- `TabControlParentSubclassProc` 函数
- `UpdateTabLayout` 函数

### emoji_window.def

删除以下导出：
- CreateTabControl
- AddTabItem
- RemoveTabItem
- SetTabCallback
- GetCurrentTabIndex
- SelectTab
- GetTabCount
- GetTabContentWindow
- DestroyTabControl
- AddChildWindowToCurrentTab

## 保留的功能

1. ✅ 创建基本窗口
2. ✅ 创建Emoji按钮
3. ✅ 创建编辑框（支持Emoji）
4. ✅ 消息框（信息提示框、确认框）

## 替代方案

如果需要Tab功能，使用易语言自带的超级列表框或Tab控件：

```易语言
' 使用易语言自带的Tab控件
超级列表框1.加入表项 ("按钮", , , )
超级列表框1.加入表项 ("编辑框", , , )

' 在列表框选择改变事件中切换显示
.子程序 _超级列表框1_列表项被选择
    .判断开始 (超级列表框1.现行选中项 ＝ 0)
        ' 显示按钮区域
        编辑框1.可视 ＝ 假
        按钮区域.可视 ＝ 真
    .判断 (超级列表框1.现行选中项 ＝ 1)
        ' 显示编辑框区域
        按钮区域.可视 ＝ 假
        编辑框1.可视 ＝ 真
    .判断结束
```

## 是否继续？

请确认是否要我执行删除操作，或者你想尝试其他方案？
