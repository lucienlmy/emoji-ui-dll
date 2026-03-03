.版本 2

.DLL命令 创建Emoji窗口, 整数型, "emoji_window.dll", "create_window"
    .参数 标题, 文本型
    .参数 宽度, 整数型
    .参数 高度, 整数型

.DLL命令 CreateWindowExA, 整数型, "user32.dll", "CreateWindowExA"
    .参数 dwExStyle, 整数型
    .参数 lpClassName, 文本型
    .参数 lpWindowName, 文本型
    .参数 dwStyle, 整数型
    .参数 x, 整数型
    .参数 y, 整数型
    .参数 nWidth, 整数型
    .参数 nHeight, 整数型
    .参数 hWndParent, 整数型
    .参数 hMenu, 整数型
    .参数 hInstance, 整数型
    .参数 lpParam, 整数型

.DLL命令 ShowWindow, 逻辑型, "user32.dll", "ShowWindow"
    .参数 hwnd, 整数型
    .参数 nCmdShow, 整数型

.DLL命令 UpdateWindow, 逻辑型, "user32.dll", "UpdateWindow"
    .参数 hwnd, 整数型

.DLL命令 GetModuleHandleA, 整数型, "kernel32.dll", "GetModuleHandleA"
    .参数 lpModuleName, 整数型

.DLL命令 运行消息循环, 整数型, "emoji_window.dll", "run_message_loop"

.版本 2

.程序集 窗口程序集
.程序集变量 窗口句柄, 整数型
.程序集变量 按钮句柄, 整数型
.程序集变量 TabControl句柄, 整数型

.子程序 _按钮1_被单击
.局部变量 hInstance, 整数型

' 创建主窗口
窗口句柄 ＝ 创建Emoji窗口 ("DLL窗口测试", 800, 600)

调试输出 ("DLL窗口句柄: " ＋ 到文本 (窗口句柄))

.如果真 (窗口句柄 ＝ 0)
    信息框 ("DLL窗口创建失败！", 0, )
    返回 ()
.如果真结束

' 获取模块句柄
hInstance ＝ GetModuleHandleA (0)

' 使用标准 Windows API 创建一个按钮测试
按钮句柄 ＝ CreateWindowExA (0, "BUTTON", "测试按钮", 1342177280, 30, 30, 150, 40, 窗口句柄, 1001, hInstance, 0)
'                                                      WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON

调试输出 ("标准按钮句柄: " ＋ 到文本 (按钮句柄))

.如果真 (按钮句柄 ≠ 0)
    ShowWindow (按钮句柄, 5)  ' SW_SHOW
    UpdateWindow (按钮句柄)
    信息框 ("标准按钮创建成功！句柄: " ＋ 到文本 (按钮句柄), 0, )
.否则
    信息框 ("标准按钮创建失败！", 0, )
.如果真结束

' 创建 TabControl 测试
TabControl句柄 ＝ CreateWindowExA (0, "SysTabControl32", "", 1342177280, 30, 100, 740, 450, 窗口句柄, 1002, hInstance, 0)

调试输出 ("TabControl句柄: " ＋ 到文本 (TabControl句柄))

.如果真 (TabControl句柄 ≠ 0)
    ShowWindow (TabControl句柄, 5)
    UpdateWindow (TabControl句柄)
    信息框 ("TabControl创建成功！句柄: " ＋ 到文本 (TabControl句柄), 0, )
.否则
    信息框 ("TabControl创建失败！", 0, )
.如果真结束

' 运行消息循环
运行消息循环 ()
