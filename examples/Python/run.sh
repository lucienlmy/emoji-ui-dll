#!/bin/bash

echo "========================================"
echo "  Emoji Window Python 示例运行脚本"
echo "========================================"
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ 错误：找不到 Python"
        echo "请安装 Python 3.6 或更高版本"
        exit 1
    fi
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

# 显示 Python 版本
echo "检测到的 Python 版本:"
$PYTHON_CMD --version
echo ""

# 检查 Python 位数
echo "检测 Python 位数..."
$PYTHON_CMD -c "import struct; print('Python 位数:', struct.calcsize('P') * 8, 'bit')"
echo ""

# 检查 DLL 文件
echo "检查 DLL 文件..."
if [ -f "emoji_window.dll" ]; then
    echo "✅ 找到 DLL: emoji_window.dll"
elif [ -f "../../x64/Release/emoji_window.dll" ]; then
    echo "✅ 找到 DLL: ../../x64/Release/emoji_window.dll"
elif [ -f "../../Release/emoji_window.dll" ]; then
    echo "✅ 找到 DLL: ../../Release/emoji_window.dll"
else
    echo "⚠️ 警告：未找到 DLL 文件"
    echo "请确保 emoji_window.dll 在以下位置之一："
    echo "  1. 当前目录"
    echo "  2. ../../x64/Release/emoji_window.dll"
    echo "  3. ../../Release/emoji_window.dll"
    echo ""
fi

echo "========================================"
echo "  启动程序"
echo "========================================"
echo ""

$PYTHON_CMD demo.py

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ 程序运行失败！"
    exit 1
fi

echo ""
echo "程序已退出。"
