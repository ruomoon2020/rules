# Changelog

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
