# 单选按钮控件 (RadioButton)

[← 返回主文档](../../README.md)

## 概述

Element UI 风格的单选按钮控件,支持分组互斥选择。同一分组内只能选中一个按钮。

## API 文档

### 创建单选按钮

```c++
HWND __stdcall CreateRadioButton(
    HWND hParent,
    int x, int y, int width, int height,
    const unsigned char* text_bytes, int text_len,
    int group_id,
    BOOL checked,
    UINT32 fg_color,
    UINT32 bg_color
);
```

**参数说明:**

| 参数 | 说明 |
|------|------|
| `hParent` | 父窗口句柄 |
| `x, y` | 控件位置 |
| `width, height` | 控件尺寸 |
| `text_bytes` | UTF-8 编码的文本字节集指针 |
| `text_len` | 文本字节集长度 |
| `group_id` | 分组ID(相同ID的单选按钮互斥) |
| `checked` | 初始选中状态(TRUE=选中, FALSE=未选中) |
| `fg_color` | 前景色(ARGB格式) |
| `bg_color` | 背景色(ARGB格式) |

**返回值:** 单选按钮控件句柄

### 获取/设置状态

```c++
BOOL __stdcall GetRadioButtonState(HWND hRadioButton);
void __stdcall SetRadioButtonState(HWND hRadioButton, BOOL checked);
```

### 设置回调

```c++
typedef void (__stdcall *RadioButtonCallback)(HWND hRadioButton, int group_id, BOOL checked);
void __stdcall SetRadioButtonCallback(HWND hRadioButton, RadioButtonCallback callback);
```

**回调参数:**
- `hRadioButton`: 触发回调的单选按钮句柄
- `group_id`: 分组ID
- `checked`: 选中状态

### 其他操作

```c++
void __stdcall EnableRadioButton(HWND hRadioButton, BOOL enable);
void __stdcall ShowRadioButton(HWND hRadioButton, BOOL show);
void __stdcall SetRadioButtonText(HWND hRadioButton, const unsigned char* text_bytes, int text_len);
void __stdcall SetRadioButtonBounds(HWND hRadioButton, int x, int y, int width, int height);
```

## 样式说明

单选按钮采用 Element UI 设计规范:

- 圆形按钮尺寸: 14x14 像素
- 选中颜色: #409EFF(Element UI 主色)
- 边框颜色: #DCDFE6(默认) / #409EFF(悬停/选中)
- 禁用颜色: #C0C4CC
- 文本字体: Microsoft YaHei UI, 14px
- 文本间距: 单选按钮右侧 8px

## 分组机制

- 相同 `group_id` 的单选按钮属于同一组
- 同一组内只能有一个按钮被选中
- 选中一个按钮会自动取消同组其他按钮的选中状态
- 不同组的单选按钮互不影响

## 易语言示例

```
.版本 2

.程序集变量 窗口句柄, 整数型
.程序集变量 单选按钮1, 整数型
.程序集变量 单选按钮2, 整数型
.程序集变量 单选按钮3, 整数型
.程序集变量 单选按钮4, 整数型
.程序集变量 单选按钮5, 整数型
.程序集变量 标签1, 整数型

.子程序 _启动窗口_创建完毕

窗口句柄 = 创建Emoji窗口 ("单选按钮示例", 500, 400)

' 创建第一组单选按钮(性别选择, group_id=1)
创建标签_辅助 (窗口句柄, 20, 20, 200, 30, "性别选择:", #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE)

单选按钮1 = 创建单选按钮_辅助 (窗口句柄, 20, 50, 100, 30, "男", 1, 真, #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE)
单选按钮2 = 创建单选按钮_辅助 (窗口句柄, 130, 50, 100, 30, "女", 1, 假, #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE)
单选按钮3 = 创建单选按钮_辅助 (窗口句柄, 240, 50, 100, 30, "保密", 1, 假, #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE)

' 设置第一组回调
设置单选按钮回调 (单选按钮1, &单选按钮回调)
设置单选按钮回调 (单选按钮2, &单选按钮回调)
设置单选按钮回调 (单选按钮3, &单选按钮回调)

' 创建第二组单选按钮(会员等级, group_id=2)
创建标签_辅助 (窗口句柄, 20, 100, 200, 30, "会员等级:", #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE)

单选按钮4 = 创建单选按钮_辅助 (窗口句柄, 20, 130, 120, 30, "普通会员", 2, 真, #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE)
单选按钮5 = 创建单选按钮_辅助 (窗口句柄, 150, 130, 120, 30, "VIP会员", 2, 假, #COLOR_TEXT_PRIMARY, #COLOR_BG_WHITE)

' 设置第二组回调
设置单选按钮回调 (单选按钮4, &单选按钮回调)
设置单选按钮回调 (单选按钮5, &单选按钮回调)

' 创建状态显示标签
标签1 = 创建标签_辅助 (窗口句柄, 20, 200, 460, 150, "当前选择:" + #换行符 + "性别: 男" + #换行符 + "会员等级: 普通会员", #COLOR_TEXT_PRIMARY, #COLOR_BG_LIGHT, , , , , , , 真)

运行消息循环 ()


.子程序 单选按钮回调, , 公开, stdcall
.参数 句柄, 整数型
.参数 分组ID, 整数型
.参数 选中, 逻辑型
.局部变量 性别文本, 文本型
.局部变量 等级文本, 文本型

.如果真 (选中)
    .如果真 (分组ID = 1)
        ' 性别选择组
        .如果真 (句柄 = 单选按钮1)
            性别文本 = "男"
        .如果真结束
        .如果真 (句柄 = 单选按钮2)
            性别文本 = "女"
        .如果真结束
        .如果真 (句柄 = 单选按钮3)
            性别文本 = "保密"
        .如果真结束
        
        ' 获取当前会员等级
        .如果真 (获取单选按钮状态 (单选按钮4))
            等级文本 = "普通会员"
        .否则
            等级文本 = "VIP会员"
        .如果真结束
        
        设置标签文本_辅助 (标签1, "当前选择:" + #换行符 + "性别: " + 性别文本 + #换行符 + "会员等级: " + 等级文本)
    .如果真结束
    
    .如果真 (分组ID = 2)
        ' 会员等级选择组
        .如果真 (句柄 = 单选按钮4)
            等级文本 = "普通会员"
        .否则
            等级文本 = "VIP会员"
        .如果真结束
        
        ' 获取当前性别
        .如果真 (获取单选按钮状态 (单选按钮1))
            性别文本 = "男"
        .如果真结束
        .如果真 (获取单选按钮状态 (单选按钮2))
            性别文本 = "女"
        .如果真结束
        .如果真 (获取单选按钮状态 (单选按钮3))
            性别文本 = "保密"
        .如果真结束
        
        设置标签文本_辅助 (标签1, "当前选择:" + #换行符 + "性别: " + 性别文本 + #换行符 + "会员等级: " + 等级文本)
    .如果真结束
.如果真结束
```

## 注意事项

⚠️ **重要提示**:

1. 同一分组内的单选按钮必须使用相同的 `group_id`
2. 不同分组使用不同的 `group_id` 以避免冲突
3. 每个分组至少应有一个按钮默认选中
4. 文本必须使用 UTF-8 编码的字节集

## 相关文档

- [复选框](checkbox.md)
- [分组框](groupbox.md)
