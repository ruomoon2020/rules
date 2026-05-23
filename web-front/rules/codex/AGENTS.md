# AGENTS.md

本仓库为企业级 Vue 3 前端项目。Codex 必须以 `rules/` 作为 AI 规则唯一入口，不得使用已废弃的 `rules.md`。

## 每次改代码前必读

1. `rules/codex/01-before-editing.md`
2. `rules/shared/00-must-follow.md`

## 按任务追加阅读

只读与当前任务相关的文件，不要一次加载全部规则。

| 任务 | 必读规则 |
|---|---|
| 任意前端改动 | `rules/codex/01-before-editing.md`、`rules/shared/00-must-follow.md` |
| 架构 / 目录 / 新模块 | `rules/shared/01-project-structure.md` |
| **`src/views/**` 页面（基础）** | `rules/shared/04-ui-patterns.md`、`rules/shared/19-list-pagination.md`、`rules/shared/11-base-components-context.md`、`rules/shared/12-schema-ssot.md`、`rules/codex/02-page-generation.md` |
| views **涉及时追加** | 表单/详情 → `13-form-and-detail.md`；权限/路由/缓存 → `06-state-route-permission.md`；接口字段 → `05-api-contract.md`；命名 → `02-naming.md`；AI 约束 → `09-ai-generation.md` |
| 表单 / 详情页 | `rules/shared/13-form-and-detail.md`、`rules/shared/12-schema-ssot.md` |
| 上传 / 导入 / 导出 / 模板下载 | `rules/shared/14-upload-import-export.md`、`rules/shared/05-api-contract.md`、`rules/shared/06-state-route-permission.md`、`rules/shared/18-logging-observability.md` |
| `src/api/**`、schema、generated | `rules/shared/05-api-contract.md`、`rules/shared/12-schema-ssot.md`、`rules/codex/04-api-and-schema.md` |
| `src/router/**`、`src/store/**`、权限 | `rules/shared/06-state-route-permission.md`、`rules/shared/05-api-contract.md` |
| `src/components/**` | `rules/shared/02-naming.md`、`rules/shared/03-code-style.md`、`rules/shared/04-ui-patterns.md`、`rules/codex/03-component-generation.md` |
| 设计 Token / 视觉 | `rules/shared/16-design-tokens.md`、`rules/shared/04-ui-patterns.md` |
| 壳层 / 菜单 / 布局 | `rules/shared/17-shell-navigation.md`、`rules/shared/06-state-route-permission.md` |
| 安全 / 无障碍 / 性能 | `rules/shared/07-security-performance.md`、`rules/shared/21-error-recovery.md` |
| 日志 / 监控 / 错误上报 | `rules/shared/18-logging-observability.md` |
| 列表分页 / 表格状态 / useTable | `rules/shared/19-list-pagination.md`、`rules/shared/04-ui-patterns.md` |
| 新增 / 升级依赖 | `rules/shared/20-dependency-governance.md`、`rules/shared/07-security-performance.md` |
| 测试 / CI / E2E / 发布 | `rules/shared/15-testing.md`、`rules/shared/08-quality-gates.md`、`rules/shared/21-error-recovery.md` |
| 收尾 / Review | `rules/shared/10-verification-checklist.md`、`rules/codex/05-verification.md` |

Codex 优先读 `rules/shared/*.md` 与 `rules/codex/*.md`。

- 不要依赖 `rules/cursor/*.mdc`（该目录仅供 Cursor）。
- 不要读 `rules/docs/`（如 `migration-from-template.md`），仅供维护者追溯历史章节，**不是**编码执行规则。

## Hard Rules

- 未阅读目标仓库 Base 组件源码或 `rules/shared/11-base-components-context.md` 前，不得编写或重构 `src/views/**`。
- 未阅读 `contracts/schema.json`（或 generated 类型）前，不得新增表单字段、表格列或 DTO。
- `src/views/**` 禁止使用原生 Element Plus（`el-*`、denylist 内 PascalCase 如 `<ElButton>`，以及 `element-plus` / `element-plus/*` import）。
- 禁止虚构 Base 组件 props / events / slots、schema 字段、权限码、路由名。
- 禁止在 Vue 组件内直接 `axios` / `fetch`。
- 禁止显式 `any`；未知类型用 `unknown` 并收窄。
- 禁止无说明引入新依赖；禁止为通过检查而 `as any`。
- 新增或升级依赖前必须遵守 `rules/shared/20-dependency-governance.md`。
- 禁止修改公共组件 API 而不同步所有调用方。
- 禁止把 mock、密钥、调试日志、不安全 `v-html` 带入生产代码。
- 禁止导入 / 导出 schema 外字段、未授权字段或未脱敏敏感字段；文件导入导出须遵守 `rules/shared/14-upload-import-export.md`。
- 单文件不超过 400 行；不得在单文件模板内堆叠 API、权限、表格、表单、弹窗全部逻辑。

## Schema 固定指令

生成或修改 `views/` 下业务页面前：

```text
1. 读取 contracts/schema.json（或执行 pnpm schema:sync 后的最新文件）。
2. 定位当前模块对应 service 的 request/response。
3. 据此生成类型、api 调用、表单字段、表格列。
4. 禁止添加 schema 中不存在的字段；禁止手写与 generated 重复的 interface。
5. UI 仅使用项目 Base 组件；views 禁 el-*、禁 EP PascalCase（见 `00-must-follow` §7）。
```

## 完成前

运行项目中实际存在的脚本；若不存在则明确说明未配置，不得伪造通过结果：

```bash
pnpm lint
pnpm type-check
pnpm test
pnpm build
```

API 或 schema 变更后，若项目有 `pnpm api:check`，必须运行。

详细检查项见 `rules/shared/10-verification-checklist.md` 与 `rules/codex/05-verification.md`。
