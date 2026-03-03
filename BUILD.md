# C++ DLL 编译指南（32位 / 64位）

## 重要说明

**易语言主要使用 32 位（x86）**，因此需要编译 32 位 DLL。

项目已配置支持：
- ✅ Win32（32位）- 易语言使用
- ✅ x64（64位）- 备用

## 方法1：使用 Visual Studio（推荐）

### 前提条件

1. 安装 Visual Studio 2019 或 2022
   - 下载：https://visualstudio.microsoft.com/downloads/
   - 选择"使用 C++ 的桌面开发"工作负载
   - 确保安装了 Windows 10 SDK

### 编译 32 位 DLL（易语言使用）

1. **打开项目**
   ```
   双击 emoji_window.sln
   ```

2. **选择 32 位配置**
   - 顶部工具栏选择：`Release` | `Win32`
   - **注意**：必须选择 Win32，不是 x64

3. **生成解决方案**
   - 菜单：生成 → 生成解决方案
   - 或按快捷键：`Ctrl + Shift + B`

4. **查找 DLL**
   ```
   编译完成后，32位 DLL 位于：
   emoji_window_cpp\Win32\Release\emoji_window.dll
   ```

5. **复制 DLL**
   ```
   将 emoji_window.dll 复制到易语言项目目录
   ```

### 编译 64 位 DLL（可选）

如果需要 64 位版本：
- 选择：`Release` | `x64`
- DLL 输出到：`x64\Release\emoji_window.dll`

## 方法2：使用命令行（MSBuild）

### 编译 32 位 DLL

打开"Developer Command Prompt for VS 2022"（或 VS 2019），执行：

```cmd
cd /d "t:\易语言源码\API创建窗口\emoji_window_cpp"
msbuild emoji_window.sln /p:Configuration=Release /p:Platform=Win32
```

### 编译 64 位 DLL

```cmd
msbuild emoji_window.sln /p:Configuration=Release /p:Platform=x64
```

## 方法3：使用 cl.exe 直接编译（32位）

如果只想快速编译 32 位 DLL：

```cmd
cd /d "t:\易语言源码\API创建窗口\emoji_window_cpp\emoji_window"

cl /LD /O2 /MT /std:c++17 ^
   /D "WIN32" /D "NDEBUG" /D "_WINDOWS" /D "_USRDLL" ^
   emoji_window.cpp dllmain.cpp ^
   /link /DEF:emoji_window.def ^
   /MACHINE:X86 ^
   d2d1.lib dwrite.lib ^
   /OUT:emoji_window.dll
```

**重要**：必须使用 32 位的开发者命令提示符（x86 Native Tools Command Prompt）

## 输出位置

| 配置 | 输出路径 | 用途 |
|------|---------|------|
| Release \| Win32 | `Win32\Release\emoji_window.dll` | **易语言使用（32位）** |
| Release \| x64 | `x64\Release\emoji_window.dll` | 64位程序使用 |
| Debug \| Win32 | `Win32\Debug\emoji_window.dll` | 32位调试版本 |
| Debug \| x64 | `x64\Debug\emoji_window.dll` | 64位调试版本 |

## 验证 DLL 位数

### 使用 dumpbin

```cmd
dumpbin /HEADERS emoji_window.dll | findstr machine
```

输出：
- `8664 machine (x64)` - 64位
- `14C machine (x86)` - 32位 ✓（易语言需要）

### 使用 PowerShell

```powershell
[System.Reflection.AssemblyName]::GetAssemblyName("emoji_window.dll").ProcessorArchitecture
```

## 常见问题

### 问题1：易语言提示"无法加载 DLL"

**原因**：DLL 是 64 位，易语言是 32 位

**解决**：
1. 确认编译时选择了 `Win32` 平台
2. 使用 dumpbin 验证 DLL 是 32 位
3. 重新编译 32 位版本

### 问题2：找不到 Win32 配置

**原因**：项目文件未正确配置

**解决**：
- 确保使用最新的 emoji_window.vcxproj
- 在 Visual Studio 中：配置管理器 → 检查 Win32 平台

### 问题3：32 位编译出错

**错误**：`Cannot open include file: 'd2d1.h'`

**解决**：
- 确保安装了 Windows 10 SDK
- 32 位和 64 位使用相同的 SDK

### 问题4：链接错误（32位）

**错误**：`unresolved external symbol`

**解决**：
- 确保链接了 d2d1.lib 和 dwrite.lib
- 检查 /MACHINE:X86 参数

### 问题5：运行时错误

**错误**：程序崩溃或无响应

**解决**：
- 使用 Debug 配置编译
- 在 Visual Studio 中调试
- 检查易语言是否正确传递参数

## 编译选项说明

### 32 位 Release 配置

```
/O2          - 最大速度优化
/MT          - 静态链接运行时（无需额外 DLL）
/std:c++17   - C++17 标准
/MACHINE:X86 - 32 位目标平台
d2d1.lib     - Direct2D 库
dwrite.lib   - DirectWrite 库
```

### 输出特性

- **DLL 大小**：约 50-100 KB（32位 Release）
- **依赖**：无需额外运行时（静态链接）
- **平台**：x86（32位）
- **系统要求**：Windows 7+

## 快速编译脚本

创建 `build_32bit.bat`：

```batch
@echo off
echo 正在编译 32 位 DLL...
cd /d "%~dp0"
msbuild emoji_window.sln /p:Configuration=Release /p:Platform=Win32 /v:minimal
if %errorlevel% == 0 (
    echo.
    echo 编译成功！
    echo DLL 位置：Win32\Release\emoji_window.dll
    echo.
    pause
) else (
    echo.
    echo 编译失败！请检查错误信息。
    echo.
    pause
)
```

双击运行即可编译。

## 测试 32 位 DLL

### 1. 验证位数

```cmd
dumpbin /HEADERS Win32\Release\emoji_window.dll | findstr machine
```

应该显示：`14C machine (x86)`

### 2. 验证导出函数

```cmd
dumpbin /EXPORTS Win32\Release\emoji_window.dll
```

应该看到：
```
create_window
create_emoji_button_bytes
set_button_click_callback
run_message_loop
destroy_window
```

### 3. 在易语言中测试

1. 复制 `Win32\Release\emoji_window.dll` 到易语言项目目录
2. 运行 `examples\test.txt` 中的代码
3. 应该看到彩色 Emoji 窗口

## 性能对比

| 平台 | DLL 大小 | 启动速度 | 渲染性能 |
|------|---------|---------|---------|
| 32位 | ~80 KB | 快 | 良好 |
| 64位 | ~90 KB | 快 | 更好 |

**结论**：易语言使用 32 位版本，性能完全够用。

## 下一步

1. ✅ 编译 32 位 DLL（Release | Win32）
2. ✅ 复制到易语言项目
3. ✅ 运行 `examples\test.txt`
4. ✅ 查看彩色 Emoji 效果

## 技术支持

如有问题：
1. 确认选择了 Win32 平台（不是 x64）
2. 使用 dumpbin 验证 DLL 位数
3. 查看编译输出窗口的错误信息
4. 参考 README.md 中的 API 文档
