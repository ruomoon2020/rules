# Changelog

## 0.9.6 — 2026-09-17

### Changed

- `shared/00-must-follow.md` 收敛为 15 条通用不变量；支付、分包、UGC、发布等细则改为命中场景时强制读取，避免未使用该能力的项目被 Level 0 错误要求。
- Codex/Cursor 概览、成熟度模型与规则索引同步场景路由口径。

## 0.9.5 — 2026-09-15

### Changed

- `evals/prompts.md`：M01–M50 期望统一显式引用 shared 文件名，便于 rule catalog 关联。
- 根目录 `scripts/generate-rule-catalog.py` 支持匹配反引号编号引用（如 `` `05` ``）。

### Added

- 新增 Media Extension **M51**（上传绕过统一封装与隐私）；Contract 套件纳入 M51（建议 5/5）；Full 范围为 M01–M51。

## 0.9.4 — 2026-09-15

### Added

- 新增 `docs/cursor-shared-map.md`，标明 `27-ai-generation` → shared `17` 等错位映射。

## 0.9.3 — 2026-09-15

### Changed

- AI Cursor 触发面补齐 auth / platform / pages.json / manifest；成熟度与 evals 对齐 5/5 条件门禁口径。

## 0.9.2 — 2026-09-15

### Fixed

- Hard Rules 计数文案去掉粗体数字，validator 同时兼容 `**N**` 写法。
- 成熟度 Level 2 明确为 Security Extension 5/5；AI Tool Safety 各 Level 在使用 AI 时均适用。

### Added

- 新增 Cursor `27-ai-generation.mdc` 与业务发布清单 `docs/release-checklist.md`。
- `LANGUAGE.md` 对齐前后端表格格式。

## 0.9.1 — 2026-09-15

### Fixed

- Codex 与 Cursor 增加新建项目、目录调整和跨层文件移动任务路由，确保 `shared/01-project-structure.md` 有明确触发入口。

## 0.9.0 — 2026-09-15

### Added

- 新增组件通信、生命周期、样式架构、主题管理、组件文档与组件测试规范。
- 新增启动、渲染、图片、分包与包体积的量化优化约束。
- 新增 Component Engineering Extension M45–M50 与 6/6 专项门槛。

### Changed

- Codex/Cursor 路由补齐组件、样式、主题、测试和性能触发路径。
- package validator 锁定组件工程关键章节，并校验 M45–M50 套件完整性。

## 0.8.0 — 2026-08-14

### Added

- 新增 AI Tool Safety MAT01–MAT05 独立 5/5 门禁及校验器负向测试。
- 新增 Level 3 平台成熟度，并接入跨端需求、发布、环境晋级与事故治理路由。

### Changed

- package validator 校验 AI Tool Safety 套件和 common-governance 跨包引用。
- AI Tool Safety 结果改为结构化证据，绑定套件摘要、模型版本、执行时间与独立评测人。

## 0.7.1 — 2026-08-14

### Changed

- `shared/17-ai-generation.md` 与 Cursor 路由新增不可信内容、提示注入、最小工具权限、发布授权和隐私数据出站约束。
- M13 改为“外部指令诱导泄露与伪造验证”，validator 锁定该高风险主题。
- package validator 新增小程序脚手架固定资产与 TypeScript 语法 smoke，并补负向单测。
- 质量门禁新增 AI 工具调用与真实执行证据检查。

## 0.7.0 — 2026-08-11

### Added

- `shared/26-security-hardening-risk.md`：生产调试产物、第三方 SDK 数据流、远程配置/实验、多平台安全矩阵与高风险操作前后端边界。
- `cursor/26-security-hardening-risk.mdc` 与 `codex/AGENTS.md` 路由，覆盖第三方 SDK、远程配置、实验、风控和多平台 adapter。
- Evals M39–M44（Enterprise Hardening Extension）；smoke **Enterprise Hardening** 套件。

### Changed

- `00` 硬规则 +4（共 45 条）：生产调试资源、后端状态/风控、第三方 SDK 数据流、实验开关回滚。
- `validate-rules-package.py`：shared/00–26、prompts 共 44 条；topic manifest 生成器支持 Enterprise Hardening 套件。
- README、规则索引、onboarding、adoption checklist、release checklist、OWASP 对照与项目本地样板同步 M39–M44。
- 企业治理接入改为可版本化的 `common-governance/` 发布包。

## 0.6.2 — 2026-06-27

### Changed

- `docs/rule-maturity-model.md`、`docs/enterprise-governance.md`：链到 DoD 对照与合规证据模板。

## 0.6.1 — 2026-06-27

### Changed

- PR 模板：企业 DoD 自检项。

## 0.6.0 — 2026-06-27

### Added

- `evals/topic-manifest.yaml`；校验器接入全量 eval topic manifest。
- 链到 monorepo 企业治理文档。

## 0.5.2 — 2026-06-27

### Added

- 校验器 `BARE_SHARED_REF`、`check_readme_shared_inventory`；`scripts/tests/` 单测 3 项。
- CI：`validate-miniapp-rules` job 增加单测步骤。

### Changed

- 校验器 `BARE_SHARED_REF`：忽略 `.mdc` 文件名中的 `.md` 子串误报。
- `docs/business-feature-playbook-miniapp.md`：§6 补充 Resilience Extension M35–M38 与 E41–E43 不适用说明。
- `evals/adoption-checklist.md`：M35–M38 与 Platform Extension 边界。

## 0.5.1 — 2026-06-27

### Changed

- `docs/fullstack-contract.md`：§与管理端 Platform Extension 边界（E41–E43 不适用；富文本见 `23-content-safety`）。
- `docs/rules-package-index.md`：链到全栈契约摘要。

## 0.5.0 — 2026-05-26

### Added

- `shared/22-error-recovery-offline.md`、`shared/23-content-safety.md`、`shared/24-design-system-mobile.md`、`shared/25-dependency-supply-chain.md`。
- `docs/observability-metrics.md`、`docs/owasp-miniapp-mapping.md`。
- Evals M35–M38（Resilience Extension）；smoke **Resilience** 套件。
- Cursor `22-error-recovery`、`23-content-safety`、`24-design-system`；Codex `08`、`09`。
- `cursor/25-dependency-supply-chain.mdc`：依赖、锁文件、第三方 SDK 与供应链治理触发规则。

### Changed

- `00` 硬规则 +3（共 41 条）：统一错误恢复、内容安全、关键指标上报。
- `10`：长列表 / setData / 节点数；`16`：测试金字塔 + audit；`15`：链到指标文档。
- `cursor/16-quality-gates.mdc`：改依赖 / 锁文件时提示读取 `shared/25-dependency-supply-chain.md`。
- `cursor/24-design-system.mdc`：补充页面与分包页面 glob，覆盖页面内样式违规。
- `cursor/00-project-overview.mdc`：补充 `25-dependency-supply-chain.mdc` 路由提示。
- `README.md`：修正 `docs/rules-package-index.md` 为 shared 00–25 索引。
- `shared/08`、`shared/09`：补充数据分级、留存策略、埋点字段白名单。
- `shared/06`、`shared/22`、`docs/fullstack-contract.md`：明确小程序默认不复制管理端 RBAC 壳层；B 端仅消费后端权限子集，401/403 分流处理。
- `shared/10`：补充分包预算、首屏请求分级、图片资源、响应式更新与分包预加载策略。
- `docs/observability-metrics.md`、`examples/99-project-local.mdc.sample`：补充首屏可交互、关键 API、分包体积、图片与分包加载失败等性能预算。
- `examples/99-project-local.mdc.sample`：补充监控 Owner、阈值、告警渠道与发版观察窗口。
- `validate-rules-package.py`：shared/00–25、prompts 共 38 条。

## 0.4.0 — 2026-05-26

### Added

- `docs/onboarding-new-project.md`、`docs/rules-package-index.md`、`docs/rule-maturity-model.md`、`docs/pull-request-template.md`。
- `examples/README.md`、`examples/ci/rules-package-validate.yml`、`examples/.github/pull_request_template.md`。
- `examples/scripts/check-miniapp-size.mjs.sample`、`api-check.stub.mjs.sample`。
- `examples/scaffold/`：App.vue、app-bootstrap、app-error-handler、webview 白名单与 open-webview 样板。
- `codex/06-app-runtime.md`、`codex/07-network-security.md`。

### Changed

- `examples/scaffold/request.ts.sample`：集成 `assertAllowedUrl`。
- `shared/01`、`shared/04`：补充 App.vue / app/ 目录与 20 交叉引用。
- `validate-rules-package.py`：校验 shared/00–21 编号文件齐全。
- 根 `README.md`：新建小程序指向 onboarding 文档。

## 0.3.0 — 2026-05-26

### Added

- `shared/20-app-runtime.md`：App 级 onLaunch/onShow、全局错误、UpdateManager、scene 初始化。
- `shared/21-network-security.md`：域名白名单、HTTPS、web-view、禁止动态域名与向 H5 透传 token。
- Cursor `20-app-runtime.mdc`、`21-network-security.mdc`。
- Evals M30–M34（Security Extension）；Security 套件扩展为 9 条。
- `examples/scaffold/allowed-hosts.ts.sample`。
- `00` 硬规则 +3（共 38 条）：网络/web-view、环境隔离、App 级兜底。

### Changed

- `shared/05-api-contract-request.md`：request/upload/download 域名校验交叉引用。
- `shared/19-release-ops.md`：dev/test/staging/prod 环境隔离细则。
- `18-business-module-extension.mdc`、`99-project-local.mdc.sample`：业务扩展适用边界。
- `codex/AGENTS.md`：App/网络任务包与路径触发。
- `evals/`、`scripts/validate-rules-package.py`：总计 M01–M34。

## 0.2.0 — 2026-05-26

### Added

- `scripts/validate-rules-package.py`：VERSION/CHANGELOG、evals M01–M29、smoke 套件、README 与 Cursor/AGENTS 引用校验。
- `RELEASE.md`、`docs/contributing-rules-package.md`、`docs/fullstack-contract.md`、`docs/business-feature-playbook-miniapp.md`、`docs/compliance-wechat-checklist.md`。
- `shared/18-business-module-extension.md`、`shared/19-release-ops.md`。
- Evals：M01–M29（P0 8、核心 P1 12、Business Extension 9）、`rubric.md`、`smoke-prompts.md`、`results-template.md`、`adoption-checklist.md`。
- Cursor：`08-state-storage`、`11-platform-differences`、`12-list-form-pagination`、`13-upload-media`、`15-logging-observability`、`16-quality-gates`、`18-business-module-extension`。
- `examples/scaffold/`：request 与 login 服务样板。

### Changed

- `README.md`：冲突优先级、完整清单、Evals 门槛、Cursor 路由表。
- `codex/AGENTS.md`：新业务分包任务包、冲突优先级、`size:check`。
- `cursor/00-project-overview.mdc`：Hard Rules 35 条、扩展 Cursor 路由。

## 0.1.0 — 2026-05-26

### Added

- 初版小程序规则包，技术栈定位为 Vue 3 + TypeScript + uni-app + Vite。
- `shared/00–17`：覆盖项目结构、Vue/TS、页面生命周期、API 契约、登录态、分包、隐私授权、包体积、平台差异、支付订阅分享、日志与验证。
- `codex/AGENTS.md`：任务包、路径触发、实现前命中声明。
- `cursor/*.mdc`：小程序场景触发摘要，仅 `00-project-overview.mdc` 为 `alwaysApply: true`。
- `examples/99-project-local.mdc.sample` 与 `package-scripts.sample.json`：业务仓落地样板。
