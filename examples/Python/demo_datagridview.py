"""
📊 DataGridView 表格控件综合示例
演示：创建表格、添加列/行、设置单元格、读写属性、点击回调
"""
import ctypes
import sys
import os
import time

sys.path.insert(0, os.path.dirname(__file__))

try:
    dll = ctypes.CDLL('./emoji_window.dll')
except OSError:
    print("错误: 无法加载 emoji_window.dll")
    sys.exit(1)

# ========== 函数原型 ==========
# 窗口
dll.create_window_bytes.argtypes = [ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int]
dll.create_window_bytes.restype = ctypes.c_void_p
dll.set_message_loop_main_window.argtypes = [ctypes.c_void_p]
dll.run_message_loop.restype = ctypes.c_int
dll.destroy_window.argtypes = [ctypes.c_void_p]

# 按钮
dll.create_emoji_button_bytes.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint]
dll.create_emoji_button_bytes.restype = ctypes.c_int
BUTTON_CB = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_void_p)
dll.set_button_click_callback.argtypes = [BUTTON_CB]

# 标签
dll.CreateLabel.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_char_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
dll.CreateLabel.restype = ctypes.c_int
dll.SetLabelText.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int]

# DataGridView
dll.CreateDataGridView.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint]
dll.CreateDataGridView.restype = ctypes.c_int

dll.DataGrid_AddTextColumn.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
dll.DataGrid_AddTextColumn.restype = ctypes.c_int
dll.DataGrid_AddCheckBoxColumn.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
dll.DataGrid_AddCheckBoxColumn.restype = ctypes.c_int
dll.DataGrid_AddButtonColumn.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
dll.DataGrid_AddButtonColumn.restype = ctypes.c_int

dll.DataGrid_AddRow.argtypes = [ctypes.c_int]
dll.DataGrid_AddRow.restype = ctypes.c_int
dll.DataGrid_RemoveRow.argtypes = [ctypes.c_int, ctypes.c_int]
dll.DataGrid_ClearRows.argtypes = [ctypes.c_int]

dll.DataGrid_SetCellText.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]
dll.DataGrid_GetCellText.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_void_p, ctypes.c_int]
dll.DataGrid_GetCellText.restype = ctypes.c_int

dll.DataGrid_SetCellChecked.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]
dll.DataGrid_GetCellChecked.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
dll.DataGrid_GetCellChecked.restype = ctypes.c_int

dll.DataGrid_SetCellStyle.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_uint, ctypes.c_uint, ctypes.c_int, ctypes.c_int]

dll.DataGrid_GetSelectedRow.argtypes = [ctypes.c_int]
dll.DataGrid_GetSelectedRow.restype = ctypes.c_int
dll.DataGrid_GetSelectedCol.argtypes = [ctypes.c_int]
dll.DataGrid_GetSelectedCol.restype = ctypes.c_int
dll.DataGrid_SetSelectedCell.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]

dll.DataGrid_GetRowCount.argtypes = [ctypes.c_int]
dll.DataGrid_GetRowCount.restype = ctypes.c_int
dll.DataGrid_GetColumnCount.argtypes = [ctypes.c_int]
dll.DataGrid_GetColumnCount.restype = ctypes.c_int

dll.DataGrid_SetSelectionMode.argtypes = [ctypes.c_int, ctypes.c_int]
dll.DataGrid_SortByColumn.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
dll.DataGrid_SetShowGridLines.argtypes = [ctypes.c_int, ctypes.c_int]
dll.DataGrid_SetDefaultRowHeight.argtypes = [ctypes.c_int, ctypes.c_int]
dll.DataGrid_SetHeaderHeight.argtypes = [ctypes.c_int, ctypes.c_int]
dll.DataGrid_SetColumnWidth.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
dll.DataGrid_SetFreezeHeader.argtypes = [ctypes.c_int, ctypes.c_int]
dll.DataGrid_SetFreezeFirstColumn.argtypes = [ctypes.c_int, ctypes.c_int]
dll.DataGrid_SetColumnHeaderAlignment.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
dll.DataGrid_SetColumnCellAlignment.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
dll.DataGrid_Refresh.argtypes = [ctypes.c_int]

# 回调
CELL_CLICK_CB = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int, ctypes.c_int)
dll.DataGrid_SetCellClickCallback.argtypes = [ctypes.c_int, CELL_CLICK_CB]
CELL_DBLCLICK_CB = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int, ctypes.c_int)
dll.DataGrid_SetCellDoubleClickCallback.argtypes = [ctypes.c_int, CELL_DBLCLICK_CB]
SEL_CHANGED_CB = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int, ctypes.c_int)
dll.DataGrid_SetSelectionChangedCallback.argtypes = [ctypes.c_int, SEL_CHANGED_CB]
COL_HEADER_CB = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int)
dll.DataGrid_SetColumnHeaderClickCallback.argtypes = [ctypes.c_int, COL_HEADER_CB]
CELL_VALUE_CB = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_int, ctypes.c_int)
dll.DataGrid_SetCellValueChangedCallback.argtypes = [ctypes.c_int, CELL_VALUE_CB]

dll.DataGrid_Enable.argtypes = [ctypes.c_int, ctypes.c_int]
dll.DataGrid_Show.argtypes = [ctypes.c_int, ctypes.c_int]
dll.DataGrid_SetBounds.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]

# 信息框
dll.show_message_box_bytes.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int, ctypes.c_char_p, ctypes.c_int]

def ARGB(a, r, g, b):
    return ((a & 0xFF) << 24) | ((r & 0xFF) << 16) | ((g & 0xFF) << 8) | (b & 0xFF)

def u(s):
    return s.encode('utf-8')

# ========== 全局变量 ==========
grid = 0
label_status = 0
main_win = None
btn_add_row = 0
btn_del_row = 0
btn_read_cell = 0
btn_sort = 0
btn_clear = 0
sort_dir = [1]  # 1=升序, 2=降序

# ========== 回调函数 ==========
def on_cell_click(hGrid, row, col):
    print(f"📊 单元格点击: 行={row}, 列={col}")
    # 读取单元格文本
    size = dll.DataGrid_GetCellText(hGrid, row, col, None, 0)
    if size > 0:
        buf = ctypes.create_string_buffer(size)
        dll.DataGrid_GetCellText(hGrid, row, col, buf, size)
        text = buf.raw[:size].decode('utf-8', errors='replace')
        msg = f"📍 点击了 [{row},{col}]: {text}"
    else:
        msg = f"📍 点击了 [{row},{col}]: (空)"
    status = u(msg)
    dll.SetLabelText(label_status, status, len(status))

def on_cell_dblclick(hGrid, row, col):
    print(f"📊 单元格双击: 行={row}, 列={col}")
    msg = u(f"✏️ 双击编辑 [{row},{col}]")
    dll.SetLabelText(label_status, msg, len(msg))

def on_selection_changed(hGrid, row, col):
    print(f"📊 选择改变: 行={row}, 列={col}")

def on_col_header_click(hGrid, col):
    print(f"📊 列头点击: 列={col}")
    msg = u(f"🔽 列头点击: 第{col}列")
    dll.SetLabelText(label_status, msg, len(msg))

def on_cell_value_changed(hGrid, row, col):
    print(f"📊 值改变: 行={row}, 列={col}")

# 保持回调引用
_cell_click_cb = CELL_CLICK_CB(on_cell_click)
_cell_dblclick_cb = CELL_DBLCLICK_CB(on_cell_dblclick)
_sel_changed_cb = SEL_CHANGED_CB(on_selection_changed)
_col_header_cb = COL_HEADER_CB(on_col_header_click)
_cell_value_cb = CELL_VALUE_CB(on_cell_value_changed)

def on_button_click(button_id, parent_hwnd):
    global grid, sort_dir
    if button_id == btn_add_row:
        # 添加一行带emoji的数据
        row_count = dll.DataGrid_GetRowCount(grid)
        row = dll.DataGrid_AddRow(grid)
        items = [
            f"🆕 新项目-{row_count+1}",
            f"📝 描述内容-{row_count+1}",
            f"⏳ 待处理",
        ]
        for ci, txt in enumerate(items):
            t = u(txt)
            dll.DataGrid_SetCellText(grid, row, ci, t, len(t))
        msg = u(f"✅ 已添加第 {row_count+1} 行")
        dll.SetLabelText(label_status, msg, len(msg))
        print(f"添加行: {row}")

    elif button_id == btn_del_row:
        sel = dll.DataGrid_GetSelectedRow(grid)
        if sel >= 0:
            dll.DataGrid_RemoveRow(grid, sel)
            msg = u(f"🗑️ 已删除第 {sel} 行")
            dll.SetLabelText(label_status, msg, len(msg))
        else:
            msg = u("⚠️ 请先选中一行再删除")
            dll.SetLabelText(label_status, msg, len(msg))

    elif button_id == btn_read_cell:
        sel_row = dll.DataGrid_GetSelectedRow(grid)
        sel_col = dll.DataGrid_GetSelectedCol(grid)
        if sel_row >= 0 and sel_col >= 0:
            size = dll.DataGrid_GetCellText(grid, sel_row, sel_col, None, 0)
            if size > 0:
                buf = ctypes.create_string_buffer(size)
                dll.DataGrid_GetCellText(grid, sel_row, sel_col, buf, size)
                text = buf.raw[:size].decode('utf-8', errors='replace')
                msg = u(f"📖 [{sel_row},{sel_col}] = {text}")
            else:
                msg = u(f"📖 [{sel_row},{sel_col}] = (空)")
            dll.SetLabelText(label_status, msg, len(msg))
        else:
            msg = u("⚠️ 请先选中一个单元格")
            dll.SetLabelText(label_status, msg, len(msg))

    elif button_id == btn_sort:
        dll.DataGrid_SortByColumn(grid, 0, sort_dir[0])
        d = "升序 ⬆️" if sort_dir[0] == 1 else "降序 ⬇️"
        msg = u(f"🔄 按第0列{d}排序")
        dll.SetLabelText(label_status, msg, len(msg))
        sort_dir[0] = 2 if sort_dir[0] == 1 else 1

    elif button_id == btn_clear:
        dll.DataGrid_ClearRows(grid)
        msg = u("🧹 已清空所有行")
        dll.SetLabelText(label_status, msg, len(msg))

_btn_cb = BUTTON_CB(on_button_click)

def main():
    global grid, label_status, main_win
    global btn_add_row, btn_del_row, btn_read_cell, btn_sort, btn_clear

    print("=" * 60)
    print("📊 DataGridView 表格控件综合示例")
    print("=" * 60)

    title = u("📊 DataGridView 表格示例 - emoji_window")
    main_win = dll.create_window_bytes(title, len(title), 850, 620)
    if not main_win:
        print("❌ 创建窗口失败")
        return

    font = u("Microsoft YaHei UI")

    # 状态标签
    status_text = u("💡 提示：点击表格单元格查看内容，双击编辑")
    label_status = dll.CreateLabel(main_win, 20, 10, 810, 30, status_text, len(status_text),
        ARGB(255,50,50,50), ARGB(255,245,247,250), font, len(font), 13, 0, 0, 0, 0, 0)

    # 创建表格 (虚拟模式=0, 隔行变色=1)
    grid = dll.CreateDataGridView(main_win, 20, 50, 810, 400, 0, 1,
        ARGB(255,48,49,51), ARGB(255,255,255,255))

    # 添加列（带emoji列头）
    cols = [
        ("📋 项目名称", 200),
        ("📝 描述", 250),
        ("🏷️ 状态", 120),
    ]
    for header, width in cols:
        h = u(header)
        dll.DataGrid_AddTextColumn(grid, h, len(h), width)

    # 添加复选框列
    chk_header = u("✅ 选择")
    dll.DataGrid_AddCheckBoxColumn(grid, chk_header, len(chk_header), 80)

    # 添加按钮列
    btn_header = u("🔧 操作")
    dll.DataGrid_AddButtonColumn(grid, btn_header, len(btn_header), 100)

    # 设置外观
    dll.DataGrid_SetDefaultRowHeight(grid, 36)
    dll.DataGrid_SetHeaderHeight(grid, 40)
    dll.DataGrid_SetShowGridLines(grid, 1)
    dll.DataGrid_SetFreezeHeader(grid, 1)
    dll.DataGrid_SetSelectionMode(grid, 1)  # 整行选择

    # 列头居中
    for i in range(5):
        dll.DataGrid_SetColumnHeaderAlignment(grid, i, 1)

    # 填充示例数据
    data = [
        ("🎨 UI设计稿", "📐 完成首页设计", "✅ 已完成"),
        ("🔧 后端API", "🌐 用户认证接口", "⏳ 进行中"),
        ("📱 移动端适配", "📲 响应式布局", "⏳ 进行中"),
        ("🧪 单元测试", "🔍 覆盖率>80%", "❌ 未开始"),
        ("📦 打包部署", "🚀 CI/CD流水线", "❌ 未开始"),
        ("📊 数据分析", "📈 用户行为统计", "⏳ 进行中"),
    ]
    for name, desc, status in data:
        row = dll.DataGrid_AddRow(grid)
        for ci, txt in enumerate([name, desc, status]):
            t = u(txt)
            dll.DataGrid_SetCellText(grid, row, ci, t, len(t))
        # 设置按钮列文本
        btn_txt = u("📋 详情")
        dll.DataGrid_SetCellText(grid, row, 4, btn_txt, len(btn_txt))

    # 设置已完成行的样式（绿色）
    dll.DataGrid_SetCellStyle(grid, 0, 2, ARGB(255,103,194,58), 0, 1, 0)
    # 设置未开始行的样式（红色）
    dll.DataGrid_SetCellStyle(grid, 3, 2, ARGB(255,245,108,108), 0, 0, 0)
    dll.DataGrid_SetCellStyle(grid, 4, 2, ARGB(255,245,108,108), 0, 0, 0)

    # 勾选第一行复选框
    dll.DataGrid_SetCellChecked(grid, 0, 3, 1)

    # 设置回调
    dll.DataGrid_SetCellClickCallback(grid, _cell_click_cb)
    dll.DataGrid_SetCellDoubleClickCallback(grid, _cell_dblclick_cb)
    dll.DataGrid_SetSelectionChangedCallback(grid, _sel_changed_cb)
    dll.DataGrid_SetColumnHeaderClickCallback(grid, _col_header_cb)
    dll.DataGrid_SetCellValueChangedCallback(grid, _cell_value_cb)

    # 按钮组
    btns = [
        ("➕", "添加行", 20, ARGB(255,64,158,255)),
        ("🗑️", "删除行", 140, ARGB(255,245,108,108)),
        ("📖", "读取单元格", 260, ARGB(255,103,194,58)),
        ("🔄", "排序", 400, ARGB(255,230,162,60)),
        ("🧹", "清空", 510, ARGB(255,144,147,153)),
    ]
    btn_ids = []
    for emoji, text, x, color in btns:
        e = u(emoji)
        t = u(text)
        bid = dll.create_emoji_button_bytes(main_win, e, len(e), t, len(t), x, 470, 110, 35, color)
        btn_ids.append(bid)

    btn_add_row, btn_del_row, btn_read_cell, btn_sort, btn_clear = btn_ids
    dll.set_button_click_callback(_btn_cb)

    # 读取属性并打印
    print(f"\n--- 📊 表格属性 ---")
    print(f"行数: {dll.DataGrid_GetRowCount(grid)}")
    print(f"列数: {dll.DataGrid_GetColumnCount(grid)}")
    print(f"选中行: {dll.DataGrid_GetSelectedRow(grid)}")
    print(f"复选框[0,3]: {dll.DataGrid_GetCellChecked(grid, 0, 3)}")

    # 读取单元格文本
    size = dll.DataGrid_GetCellText(grid, 0, 0, None, 0)
    if size > 0:
        buf = ctypes.create_string_buffer(size)
        dll.DataGrid_GetCellText(grid, 0, 0, buf, size)
        print(f"单元格[0,0]: {buf.raw[:size].decode('utf-8', errors='replace')}")

    # 信息标签
    info = u("📊 表格支持：文本列、复选框列、按钮列 | 🖱️ 单击选中，双击编辑 | 🔄 点击列头排序")
    dll.CreateLabel(main_win, 20, 520, 810, 50, info, len(info),
        ARGB(255,144,147,153), ARGB(0,0,0,0), font, len(font), 12, 0, 0, 0, 0, 1)

    dll.set_message_loop_main_window(main_win)
    print("\n✅ 进入消息循环...")
    dll.run_message_loop()
    print("程序退出。")

if __name__ == "__main__":
    main()
