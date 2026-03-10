# Task Plan

## Goal
更新 GitHub README 与论坛发布文档：按当前 `易语言代码/DLL命令.e` 同步 README 中新增命令的易语言声明示例，更新截图展示，补充 QQ 交流群与更新同步说明，加入打赏与联系方式，并在 `docs/` 下新增一份不含特殊表情的论坛发布文档。

## Phases
- [x] Phase 1: 探查项目上下文、README 现状、截图资源、打赏联系方式来源
- [x] Phase 2: 与用户确认“新增命令”范围，并确定采用方案 A
- [x] Phase 3: 形成设计定稿
- [ ] Phase 4: 写入设计文档到 `docs/plans/`
- [ ] Phase 5: 写入实施计划到 `docs/plans/`
- [ ] Phase 6: 等待用户选择执行方式，再开始实际修改 README 和新增论坛文档

## Constraints
- README 面向 GitHub，需要段落分明、结构清晰
- 论坛发布文档不能包含特殊表情
- README 中新增命令声明示例以 `易语言代码/DLL命令.e` 为准
- 截图来源固定为 `imgs/`
- 打赏与联系方式来源固定为 `docs/打赏和联系方式.md`
- 未获用户要求前，不创建 git commit

## Errors Encountered
| Error | Attempt | Resolution |
|---|---:|---|
| `session-catchup.py` 路径第一次调用失败 | 1 | 改为直接使用实际 skill 目录路径；后续仅保留手动规划文件 |
| 并行工具调用因单个参数错误被取消 | 1 | 改为拆分后重试，继续读取 README / DLL命令 / docs |
