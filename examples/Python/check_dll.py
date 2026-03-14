"""
DLL 诊断工具
检查 DLL 文件和 Python 环境
"""

import sys
import os
import struct
import ctypes
from pathlib import Path


def check_python_info():
    """检查 Python 信息"""
    print("=" * 60)
    print("Python 环境信息")
    print("=" * 60)
    
    # Python 版本
    print(f"Python 版本: {sys.version}")
    
    # Python 位数
    bits = struct.calcsize('P') * 8
    print(f"Python 位数: {bits} bit")
    
    # Python 路径
    print(f"Python 路径: {sys.executable}")
    
    print()


def check_dll_files():
    """检查 DLL 文件"""
    print("=" * 60)
    print("DLL 文件检查")
    print("=" * 60)
    
    # 可能的 DLL 路径
    paths = [
        "emoji_window.dll",
        "../../x64/Release/emoji_window.dll",
        "../../Release/emoji_window.dll",
        "../../../x64/Release/emoji_window.dll",
        "../../../Release/emoji_window.dll",
    ]
    
    found_dlls = []
    for path in paths:
        if os.path.exists(path):
            abs_path = os.path.abspath(path)
            size = os.path.getsize(path)
            found_dlls.append((path, abs_path, size))
            print(f"✅ 找到: {path}")
            print(f"   绝对路径: {abs_path}")
            print(f"   文件大小: {size:,} 字节")
            
            # 尝试判断 DLL 位数
            try:
                with open(path, 'rb') as f:
                    # 读取 PE 头
                    f.seek(0x3C)
                    pe_offset = int.from_bytes(f.read(4), 'little')
                    f.seek(pe_offset + 4)
                    machine = int.from_bytes(f.read(2), 'little')
                    
                    if machine == 0x014c:
                        print(f"   DLL 位数: 32 bit (x86)")
                    elif machine == 0x8664:
                        print(f"   DLL 位数: 64 bit (x64)")
                    else:
                        print(f"   DLL 位数: 未知 (0x{machine:04X})")
            except Exception as e:
                print(f"   无法读取 DLL 位数: {e}")
            
            print()
    
    if not found_dlls:
        print("❌ 未找到任何 DLL 文件")
        print()
        print("请将 emoji_window.dll 放在以下位置之一：")
        for path in paths:
            print(f"  - {path}")
    
    print()
    return found_dlls


def check_dll_dependencies(dll_path):
    """检查 DLL 依赖项"""
    print("=" * 60)
    print(f"检查 DLL 依赖项: {dll_path}")
    print("=" * 60)
    
    try:
        # 尝试加载 DLL
        dll = ctypes.WinDLL(dll_path)
        print("✅ DLL 加载成功！")
        print()
        return True
    except Exception as e:
        print(f"❌ DLL 加载失败: {e}")
        print()
        print("可能的原因：")
        print("1. Python 位数与 DLL 位数不匹配")
        print("   - 32位 Python 只能加载 32位 DLL")
        print("   - 64位 Python 只能加载 64位 DLL")
        print()
        print("2. 缺少 Visual C++ 运行库")
        print("   - 下载安装: https://aka.ms/vs/17/release/vc_redist.x64.exe (64位)")
        print("   - 下载安装: https://aka.ms/vs/17/release/vc_redist.x86.exe (32位)")
        print()
        print("3. 缺少其他依赖 DLL")
        print("   - d2d1.dll (Direct2D)")
        print("   - dwrite.dll (DirectWrite)")
        print("   - 这些通常由 Windows 10+ 自带")
        print()
        return False


def check_system_dlls():
    """检查系统 DLL"""
    print("=" * 60)
    print("检查系统依赖 DLL")
    print("=" * 60)
    
    system_dlls = [
        "d2d1.dll",
        "dwrite.dll",
        "comctl32.dll",
        "uxtheme.dll",
        "windowscodecs.dll",
        "dwmapi.dll",
    ]
    
    for dll_name in system_dlls:
        try:
            dll = ctypes.WinDLL(dll_name)
            print(f"✅ {dll_name} - 可用")
        except Exception as e:
            print(f"❌ {dll_name} - 不可用: {e}")
    
    print()


def main():
    """主函数"""
    print()
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "DLL 诊断工具" + " " * 31 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    # 1. 检查 Python 信息
    check_python_info()
    
    # 2. 检查 DLL 文件
    found_dlls = check_dll_files()
    
    # 3. 检查系统 DLL
    check_system_dlls()
    
    # 4. 尝试加载 DLL
    if found_dlls:
        print("=" * 60)
        print("尝试加载 DLL")
        print("=" * 60)
        
        for dll_path, abs_path, size in found_dlls:
            success = check_dll_dependencies(dll_path)
            if success:
                print(f"✅ 推荐使用: {dll_path}")
                print()
                break
    
    # 5. 总结
    print("=" * 60)
    print("诊断完成")
    print("=" * 60)
    print()
    print("如果 DLL 加载失败，请按照上述提示解决问题。")
    print()
    
    input("按回车键退出...")


if __name__ == "__main__":
    main()
