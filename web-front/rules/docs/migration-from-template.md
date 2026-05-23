# 从历史规范模板迁移

> **维护者文档**：AI 执行不读本文件。日常入口为 `../README.md` 与 `../shared/`。  
> 规则包稳定后，旧「企业级前端项目规范模板」可从业务仓移除；本表仅保留章节对照。

## 旧章节 → 当前 rules 文件

| 旧规范主题 | shared | codex | cursor |
|---|---|---|---|
| §2-3 架构与目录 | `01-project-structure.md` | `01-before-editing.md` | `01-architecture.mdc` |
| §5-7 Token / 布局 / 壳层 | `16-design-tokens.md`, `17-shell-navigation.md`, `04-ui-patterns.md` | — | `03-ui-design-system.mdc`, `09-shell-navigation.mdc` |
| §18 API / Schema | `05-api-contract.md`, `12-schema-ssot.md` | `04-api-and-schema.md` | `05-api-state-error.mdc`, `11-schema-ssot.mdc` |
| §20-21 路由 / 权限 | `06-state-route-permission.md` | `02-page-generation.md` | `05-api-state-error.mdc` |
| §25-26 命名 / 风格 | `02-naming.md`, `03-code-style.md` | `05-verification.md` | `02-vue3-typescript.mdc`, `04-component-usage.mdc`, `15-naming-conventions.mdc` |
| §27 组件 | `04-ui-patterns.md`, `11-base-components-context.md` | `03-component-generation.md` | `04-component-usage.mdc`, `10-base-components.mdc` |
| §30-32 安全 / 性能 | `07-security-performance.md`, `20-dependency-governance.md`, `21-error-recovery.md` | `05-verification.md` | `06-security-performance.mdc`, `16-dependency-governance.mdc`, `17-error-recovery.mdc` |
| 日志 / 监控 | `18-logging-observability.md` | — | `12-logging-observability.mdc` |
| 列表分页 / 竞态 | `19-list-pagination.md` | `02-page-generation.md` | `13-list-pagination.mdc` |
| §37-39 CI / 发布 | `08-quality-gates.md`, `15-testing.md` | `05-verification.md` | `07-review-checklist.mdc` |
| §41 AI 编码 | `09-ai-generation.md` | `AGENTS.md`, `02-page-generation.md` | `10-base-components.mdc`, `11-schema-ssot.mdc` |
| §15–16 表单 / 详情 | `13-form-and-detail.md` | `02-page-generation.md` | — |
| §17 上传 / 导入 / 导出 | `14-upload-import-export.md` | — | `14-upload-import-export.mdc` |
| §33 测试 | `15-testing.md` | `05-verification.md` | — |

## 与早期 Cursor 推荐文件名的差异

| 早期推荐项 | 本规则包 | 说明 |
|---|---|---|
| `02-vue3-element-plus.mdc` | `02-vue3-typescript.mdc` | 含 views 禁 `el-*` |
| `06-naming-style.mdc` | `15-naming-conventions.mdc` + `shared/02-naming.md` | 命名细则以 shared 为准 |
| `07-security-permission.mdc` | `06-security-performance.mdc` | 含安全与 a11y |
| `docs/00-*.md` 等 | 未拆入 rules | 按业务项目单独维护 |
