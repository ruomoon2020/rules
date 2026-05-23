# Codex Before Editing Rules

改前端代码前执行。

## First

1. `rules/shared/00-must-follow.md`
2. 判断任务类型：页面、组件、API、路由/权限、安全/性能、Review。
3. 按 `rules/codex/AGENTS.md` 任务表只读相关 `shared/`、`codex/` 文件。

## Context To Gather

- 目标模块现有目录与文件
- Base 组件真实 API（`shared/11-base-components-context.md` 或源码）
- schema / generated 类型（`shared/12-schema-ssot.md`）
- 已有 composable：`useTable`、`useDialog`、`useRequest` 等
- 路由 `name`、权限码、字典来源
- `package.json` 中实际 scripts 名称

## Do Not Start Until

- 明确改动所属分层（views / components / api / store）
- 明确字段是否来自 schema / generated
- 明确是否 keep-alive 及路由 `name`
- 明确项目验证命令名称
