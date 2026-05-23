# Rules Adoption Checklist

业务仓库落地规则包时勾选。

## 规则包文件（复制到业务仓）

- [ ] 整包 `rules/` 可访问（推荐 submodule 或子目录）
- [ ] 根目录 `AGENTS.md` ← `rules/codex/AGENTS.md`
- [ ] `.cursor/rules/*.mdc` ← `rules/cursor/`
- [ ] `rules/shared/` 路径可被 AI 解析

## AI 规则落地项

- [x] AGENTS.md（规则包 `codex/AGENTS.md`）
- [x] `.cursor/rules/10-base-components` → `10-base-components.mdc` + `shared/11-base-components-context.md`
- [x] `.cursor/rules/11-schema-ssot` → `11-schema-ssot.mdc` + `shared/12-schema-ssot.md`
- [x] `.cursor/rules/00-project-overview.mdc`
- [x] `.cursor/rules/01-architecture.mdc`
- [x] `.cursor/rules/03-ui-design-system.mdc`
- [x] `.cursor/rules/04-component-usage.mdc`
- [x] `.cursor/rules/05-api-state-error.mdc`
- [x] 命名 → `15-naming-conventions.mdc`（触发）+ `shared/02-naming.md`（SSOT）
- [x] Review → `07-review-checklist.mdc` + `shared/10-verification-checklist.md`
- [x] 日志 → `12-logging-observability.mdc` + `shared/18-logging-observability.md`
- [x] 列表分页 → `13-list-pagination.mdc` + `shared/19-list-pagination.md`
- [x] 上传 / 导入 / 导出 → `14-upload-import-export.mdc` + `shared/14-upload-import-export.md`
- [x] 依赖治理 → `16-dependency-governance.mdc` + `shared/20-dependency-governance.md`
- [x] 错误恢复 → `17-error-recovery.mdc` + `shared/21-error-recovery.md`

## 硬门禁（业务项目侧，非 rules 包内）

- [ ] ESLint `views` 禁 `element-plus` 及 `element-plus/*` import（`eslint-views-ban-el.mjs`）
- [ ] CI 扫描 `views` 模板 `<el-*>`（`ci-scan-views-el-tags.mjs`，**勿**加 `--allow-empty`）
- [ ] 已跑 `node rules/examples/run-ci-scan-fixtures.mjs`（规则包发版 / 升级后）
- [ ] `@typescript-eslint/no-explicit-any`
- [ ] `contracts/schema.json` + `api:check`
- [ ] CI：`lint` / `type-check` / `build`
- [ ] `resetAllStores()` 登出实现

## 评测

- [ ] 已跑 `evals/prompts.md` 一轮并记录 `results-*.md`
- [ ] P0 **8/8**，P1 **至少 21/23**（含 E17–E31 日志/分页/性能/批量/导入导出/命名/依赖/错误恢复/a11y）
