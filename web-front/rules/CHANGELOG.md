# Changelog

## 1.3.2 — 2026-05-24

### Added

- `shared/20-dependency-governance.md`：依赖新增 / 升级治理、许可证、体积、懒加载与 AI 约束。
- `shared/21-error-recovery.md`：全局异常、路由 chunk 失败、白屏恢复、页面级恢复。
- `cursor/16-dependency-governance.mdc`、`cursor/17-error-recovery.mdc`。
- `evals`：**E29–E31**（依赖治理、chunk 失败恢复、a11y 检查）。

### Changed

- `02-naming.md`：澄清 `list` / `item` 禁止范围；表格数据推荐 `rows` / `tableData` 等。
- `03-code-style.md`：扩展注释规范；命名指向 `02-naming` SSOT。
- `01-project-structure.md`、`06-state-route-permission.md`：交叉引用命名与 URL path kebab-case。
- `cursor/07-review-checklist.mdc`：高频项增加命名检查。
- `evals/adoption-checklist.md`：合并命名落地项，消除与 `15-naming-conventions.mdc` 矛盾表述。
- `08-quality-gates.md`：新增规则到工具 / CI 阻断级别映射表。
- `15-testing.md`：补充测试分层、a11y 自动化、导入导出测试。
- `AGENTS.md`、`README.md`、`00-must-follow.md`、`10-verification-checklist.md`：同步依赖治理与错误恢复入口。
- P1 evals 门槛：**21/23**（E09–E31）。

## 1.3.1 — 2026-05-24

### Added

- `evals`：**E23**（批量删除后清空 selection、修正页码）。
- `cursor/14-upload-import-export.mdc`：上传、导入、导出、模板下载触发摘要。
- `evals`：**E24–E26**（导入模板与错误明细、CSV/Excel 公式注入与脱敏、JSON/Word 安全处理）。
- `evals`：**E27**（高风险导入幂等、影响摘要、二次确认、下载鉴权）。
- `cursor/15-naming-conventions.mdc`：命名、路径、文件、样式、环境变量触发摘要。
- `evals`：**E28**（路径、变量、enum、CSS class、环境变量命名）。

### Changed

- `cursor/13-list-pagination.mdc`：摘要补充批量操作与部分失败反馈。
- `05-api-contract.md`：request wrapper 须经 error normalizer；与 `18-logging-observability.md` 交叉引用。
- `10-verification-checklist.md`：列表检查项含批量部分失败反馈。
- `14-upload-import-export.md`：扩展 Excel / CSV / JSON / Word 导入导出、模板、预校验、错误明细、权限、审计与脱敏规则。
- `codex/AGENTS.md`、`00-must-follow.md`、`10-verification-checklist.md`：补充文件导入导出必读与完成前检查。
- `14-upload-import-export.md`：补充下载链接鉴权/有效期、导入幂等、高风险导入二次确认、错误报告脱敏、时区与数值格式。
- `02-naming.md`：补充 views 路径、测试文件、样式、环境变量、Type / Interface / Enum、权限码与事件名命名。
- `10-verification-checklist.md`：完成前检查加入命名规范。
- P1 evals 门槛：**18/20**（E09–E28）。

## 1.3.0 — 2026-05-24

### Added

- `shared/18-logging-observability.md`：结构化日志字段契约、`event` 命名、脱敏与禁止项。
- `shared/19-list-pagination.md`：列表分页行为、竞态、URL 同步、offset vs cursor。
- `cursor/12-logging-observability.mdc`、`cursor/13-list-pagination.mdc`。
- `evals`：**E18–E22**（日志脱敏、删最后一条回退、请求竞态、图表懒加载、大表格分页）。

### Changed

- `07-security-performance.md`：性能预算参考表、大依赖懒加载清单。
- `00-must-follow.md`：§16/§35 扩展；新增 §48 列表分页硬规则。
- `10-verification-checklist.md`：日志、分页、性能专项检查项。
- `codex/AGENTS.md`：任务路由追加日志 / 分页；列表页必读 `19-list-pagination`。
- P1 evals 门槛：**12/14**（E09–E22）。
- `18-logging-observability.md`：日志示例改为依赖项目 error normalizer，避免 AI 照抄未知错误字段。
- `19-list-pagination.md`：补充批量操作后刷新、selection 清理、部分失败反馈。
- `07-security-performance.md`：性能预算增加超预算说明与豁免依据要求。
- `RELEASE.md`：增加 Cursor shared 引用、eval 门槛一致性检查。

## 1.2.6 — 2026-05-23

### Changed

- 全库对齐 v1.2.5：`ElButton` / `element-plus/*`、双门禁、PascalCase denylist（`AGENTS`、verification、cursor、evals）。
- `evals`：新增 **E17**（拒绝 views 使用 `<ElButton>`）；P1 门槛 **8/9**。
- `codex/AGENTS.md`：合并重复「测试」任务行；Hard Rules 与 Schema 指令补全 PascalCase。
- `examples/README.md`、`03-code-style`、`11-base-components-context`：条款编号与 §5–7 引用修正。
- `README` 硬门禁表、`08-quality-gates`、`cursor/02`：补全 PascalCase 与双门禁说明。

## 1.2.5 — 2026-05-23

### Added

- `element-plus-pascal-denylist.mjs`：views 禁止 EP PascalCase 组件（防 unplugin 自动导入绕过）。
- `RELEASE.md`：维护者发版 checklist。
- Fixtures：`PascalCaseElButton`、`MultipleInOne`、`CustomElPrefix`。

### Changed

- `ci-scan-views-el-tags.mjs`：同文件报告全部违规；输出 `file:line:column`；扫描 EP denylist。
- `shared/00-must-follow.md`：第 7 条明确禁止 views 使用 `<ElButton>` 等 EP PascalCase。
- `codex/AGENTS.md`：明确不读 `rules/docs/`。
- `examples/README.md`：更新检测清单与输出格式。

## 1.2.4 — 2026-05-23

### Added

- `examples/fixtures/ci-scan-project/` + `run-ci-scan-fixtures.mjs`：ci-scan 回归测试。
- 动态组件检测：`is="el-*"`；`:is` / `v-bind:is` 使用捕获组匹配引号。

### Changed

- `eslint-views-ban-el.mjs`：`patterns` 禁止 `element-plus/*`；globs 含 `packages/**/src/views`。
- `ci-scan-views-el-tags.mjs`：导出 `runCiScan` / `scanTemplate` 等供测试；`PLAIN_IS_RE` 补全。
- `README.md`、`examples/README.md`：CI 推荐接入顺序与 PR 必跑说明。

## 1.2.3 — 2026-05-23

### Added

- `ci-scan-views-el-tags.mjs`：`--allow-empty`；无 views 根目录默认 `exit(1)`。
- `ci-scan`：仅扫 `<template>`、去除 HTML 注释、检测 `:is="'el-*'"`。
- `docs/migration-from-template.md`：历史章节对照（维护者专用）。

### Changed

- `ci-scan`：`--root` / `--include` 使用 `resolve`，支持绝对路径。
- `evals`：通过门槛改为 **P0 8/8**、**P1 至少 7/8**。
- `README.md`：历史映射迁至 `docs/`，主 README 更精简。

### Removed

- `examples/eslint-views-full.mjs`（易误解；仅用 `eslint-views-ban-el.mjs` + `ci-scan`）。

## 1.2.2 — 2026-05-23

### Added

- `evals/prompts.md` **E16**：验证「仅 ESLint import 门禁」不满足 views 禁 `el-*`。

### Changed

- `README.md`：规则层级 L1 更正为 `shared/01–17`。
- `ci-scan-views-el-tags.mjs`：仅扫描 `src/views` 与 `packages/<pkg>/src/views`；支持 `--include`；扩展跳过目录。
- `evals/rubric.md`、`results-template.md`：P1 用例增至 8 条（含 E16）。

### Removed

- `examples/eslint-views-ban-el-tags.mjs`（易误解为 ESLint 规则；以 `ci-scan` + `examples/README.md` 为准）。

## 1.2.1 — 2026-05-23

### Added

- `shared/16-design-tokens.md`、`17-shell-navigation.md`：规则包可独立执行，不依赖旧母文档。
- `examples/ci-scan-views-el-tags.mjs`：CI 扫描 views 模板 `<el-*>`。
- `LANGUAGE.md`：中英文维护约定。

### Changed

- `codex/AGENTS.md`：views 任务拆为基础 4 文件 + 涉及时追加。
- 全部 `cursor/*.mdc` 正文改中文；`07-review-checklist` 内联 8 条高频检查。
- `README.md`、`examples/`：明确 import 与模板标签须组合门禁。
- `00-must-follow.md` 第 39 条：要求 import + 模板双门禁。
- `09-shell-navigation.mdc`：补齐 `packages/**` router / layout globs。

## 1.2.0 — 2026-05-23

### Added

- `evals/`：回归提示词（E01–E15）、评分标准、结果模板、落地勾选清单。
- `shared/13-form-and-detail.md`、`14-upload-import-export.md`、`15-testing.md`：母文档 §15–17、§33 精简执行版。
- `examples/package-scripts.sample.json`：推荐门禁 scripts 命名参考。

### Changed

- `codex/AGENTS.md`：任务表增加表单、上传、测试场景。
- `README.md`：evals 说明、新 shared 文件、母文档映射扩展。

## 1.1.0 — 2026-05-23

### Added

- `shared/10-verification-checklist.md`：统一验证清单（Codex / Review 共用）。
- `shared/11-base-components-context.md`、`shared/12-schema-ssot.md`：Codex 与 Cursor 共用 SSOT。
- `cursor/03-ui-design-system.mdc`、`cursor/09-shell-navigation.mdc`：补齐母文档 §42 部分缺口。
- `examples/eslint-views-ban-el.mjs`：views 禁 `element-plus` 的 ESLint 样板。

### Changed

- `codex/AGENTS.md`：完整任务路由表；Hard Rules 对齐母文档 §41。
- `README.md`：落地方式、文件清单、§42 差异、规则层级说明。
- `shared/09-ai-generation.md`、`shared/00-must-follow.md`：补充 AI 体量与依赖约束。
- `cursor/00-project-overview.mdc`：中文概览与落地说明。
- `cursor/10-base-components.mdc`、`cursor/11-schema-ssot.mdc`：改为引用 shared SSOT。
- `codex/05-verification.md`、`cursor/07-review-checklist.mdc`：指向统一验证清单。
- `cursor/01-architecture.mdc`：增加 `packages/**` glob。

## 1.0.0

- 初始规则包：shared / codex / cursor 三层结构。
