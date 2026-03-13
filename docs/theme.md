# 主题系统

[← 返回主文档](../README.md)

## 概述

支持亮色/暗色主题切换，可从 JSON 文件加载自定义主题。切换主题时所有控件自动刷新。

## API 文档

### 从 JSON 加载主题

```c++
BOOL __stdcall LoadThemeFromJSON(
    const unsigned char* json_bytes,
    int json_len
);
```

### 从文件加载主题

```c++
BOOL __stdcall LoadThemeFromFile(
    const unsigned char* file_path_bytes,
    int path_len
);
```

### 设置主题

```c++
void __stdcall SetTheme(
    const unsigned char* theme_name_bytes,
    int name_len
);
```

### 设置暗色模式

```c++
void __stdcall SetDarkMode(BOOL dark_mode);
```

### 获取主题颜色

```c++
UINT32 __stdcall EW_GetThemeColor(
    const unsigned char* color_name_bytes,
    int name_len
);
```

### 获取主题字体

```c++
int __stdcall EW_GetThemeFont(
    int font_type,          // 0=标题 1=正文 2=等宽
    unsigned char* buffer,
    int buffer_size
);

int __stdcall GetThemeFontSize(int font_type);
```

### 获取主题尺寸

```c++
int __stdcall GetThemeSize(int size_type);
// size_type: 0=圆角半径 1=边框宽度 2=控件高度 3=小间距 4=中间距 5=大间距
```

### 查询当前主题

```c++
BOOL __stdcall IsDarkMode();
int  __stdcall EW_GetCurrentThemeName(unsigned char* buffer, int buffer_size);
```

### 主题切换回调

```c++
typedef void (__stdcall *ThemeChangedCallback)();
void __stdcall SetThemeChangedCallback(ThemeChangedCallback callback);
```

## 主题 JSON 格式

```json
{
  "name": "my_theme",
  "dark_mode": false,
  "primary": "#409EFF",
  "success": "#67C23A",
  "warning": "#E6A23C",
  "danger": "#F56C6C",
  "info": "#909399",
  "text_primary": "#303133",
  "text_regular": "#606266",
  "text_secondary": "#909399",
  "text_placeholder": "#C0C4CC",
  "border_base": "#DCDFE6",
  "border_light": "#E4E7ED",
  "border_lighter": "#EBEEF5",
  "background": "#FFFFFF",
  "background_light": "#F5F7FA",
  "border_radius": 4,
  "title_size": 16,
  "body_size": 14
}
```

## 内置主题

项目提供两个内置主题文件：

- `themes/light.json` - 亮色主题（Element UI 标准配色）
- `themes/dark.json` - 暗色主题

## 主题颜色名称常量

| 常量 | 值 | 说明 |
|------|-----|------|
| `THEME_COLOR_PRIMARY` | "primary" | 主色 |
| `THEME_COLOR_SUCCESS` | "success" | 成功色 |
| `THEME_COLOR_WARNING` | "warning" | 警告色 |
| `THEME_COLOR_DANGER` | "danger" | 危险色 |
| `THEME_COLOR_INFO` | "info" | 信息色 |
| `THEME_COLOR_TEXT_PRIMARY` | "text_primary" | 主要文本色 |
| `THEME_COLOR_TEXT_REGULAR` | "text_regular" | 常规文本色 |
| `THEME_COLOR_BACKGROUND` | "background" | 背景色 |

## 易语言使用示例

```
' 切换到暗色主题
设置暗色模式 (真)

' 切换到亮色主题
设置暗色模式 (假)

' 从JSON加载自定义主题
json字节集 = 编码_Ansi到Utf8 (`{"name":"purple","primary":"#7C3AED",...}`)
从JSON加载主题 (取变量数据地址 (json字节集), 取字节集长度 (json字节集))

' 从文件加载主题
路径字节集 = 编码_Ansi到Utf8 ("themes/dark.json")
从文件加载主题 (取变量数据地址 (路径字节集), 取字节集长度 (路径字节集))
```

## 主题系统特性

- ✅ 即时切换：切换主题后所有控件立即刷新
- ✅ JSON 配置：使用 JSON 格式定义主题，易于编辑
- ✅ 文件加载：支持从外部文件加载主题
- ✅ 完整覆盖：主题影响所有控件类型
- ✅ 状态保持：切换主题不会丢失控件的状态数据
- ✅ 回调通知：主题切换时可触发回调函数

## 相关文档

- [控件列表](../README.md#完整控件列表)
- [常见问题](faq.md)
