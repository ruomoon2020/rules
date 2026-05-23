# Changelog

## 1.10.2 — 2026-05-24

### Added

- 仓库根 `.github/workflows/validate-backend-rules.yml`：改 `web-backend/rules/**` 时自动跑一致性校验。
- 仓库根 `CODEOWNERS`（monorepo 示例）。
- `examples/ci/rules-package-validate.yml`：业务仓嵌入 `rules/` 时的校验 workflow 样板。

### Changed

- `scripts/validate-rules-package.py`：校验 Smoke 核心 P1、Security/Contract 套件与 `evals/README` 一致；校验 README 清单路径与 cursor→shared 引用。
- `docs/monorepo-layout.md`、根 `README.md`：补充规则包 CI 与 CODEOWNERS 说明。

## 1.10.1 — 2026-05-24

### Added

- `scripts/validate-rules-package.py`：校验 VERSION/CHANGELOG、evals 条数与门槛、`smoke-prompts` B 编号覆盖（不计入提示词正文计数）。
- `examples/ci/backend-ci-required.yml`、`examples/ci/backend-ci-optional.yml`：按成熟度拆分 CI 样板。
- `examples/.github/pull_request_template.md`：可直接复制到业务仓 `.github/` 的 PR 模板。

### Changed

- `evals/smoke-prompts.md`、`docs/contributing-rules-package.md`、`RELEASE.md`：明确 smoke-prompts 为索引、不参与 `### Bxx` 正文计数。
- `docs/pull-request-template.md`：指向 `examples/.github/` 落地路径。
- `examples/README.md`、`examples/ci/github-actions-backend.yml`：推荐 required + optional 拆分复制。

## 1.10.0 — 2026-05-24

### Added

- `docs/rule-maturity-model.md`：企业采纳分层 Level 0–3（与包内 L0/L1/L2 架构词区分）。
- `docs/pull-request-template.md`：业务仓 PR 检查清单（契约/DB/安全/SLO/PII/ADR 等）。
- `docs/contributing-rules-package.md`：规则包硬变更清单与 Review 要求。
- `evals/smoke-prompts.md`：Smoke / Security / Contract / Full 套件索引。

### Changed

- `evals/README.md`：回归套件表（Smoke、Security、Contract、Full）与门槛。
- `shared/23-quality-gates.md`、`examples/README.md`、`examples/ci/github-actions-backend.yml`：CI Required / Conditional / Optional 分级。
- `examples/config/SecurityConfig.sample.java`：CSRF、Swagger/Actuator 企业审查醒目说明。
- `RELEASE.md`、`docs/onboarding-new-project.md`、`evals/adoption-checklist.md`、`docs/rules-package-index.md`、`README.md`、`codex/AGENTS.md`：链接新文档与分层 evals 策略。

## 1.9.1 — 2026-05-24

### Changed

- `shared/00-must-follow.md`：将 BOLA/IDOR、SSRF 从 AI 生成小节移入硬安全规则序列，保持 48 条总数不变。
- `shared/06-security-authz.md`：修正限流小节重复编号。
- `docs/codeowners-guidance.md`：补充 `rules/**`、IaC、事件契约、Webhook/Consumer/Job、Crypto/Token/Secret 等高风险路径。
- `docs/compliance-cn-mapping.md`：补充密评/密码应用、供应链安全、运维变更、数据生命周期映射。
- `evals/adoption-checklist.md`：增加企业治理落地项：CODEOWNERS、发版、事故复盘、备份恢复、性能预算、合规映射 Review。

## 1.9.0 — 2026-05-24

### Added

- `docs/owasp-api-top10-mapping.md`：OWASP API Top 10 与 shared 规则映射。
- `docs/compliance-cn-mapping.md`：等保、个保、密评等与规则包对照。
- `docs/release-checklist.md`、`docs/incident-postmortem-template.md`、`docs/codeowners-guidance.md`：发版、事故复盘、CODEOWNERS 指引。
- `evals`：**B51–B54**（幂等头、BOLA/IDOR、SSRF、高基数 metric）。
- `contracts/openapi.yaml`：`Idempotency-Key` 参数组件；创建用户 POST 示例引用。

### Changed

- **不新增** `shared/43+`；扩写 `04`/`05`/`06`/`07`/`09`/`13`/`15`/`24`/`26`/`28`/`32`/`10`（幂等、BOLA、SSRF、W3C trace/RED、读写分离、租户配额、Pact、发版复盘等）。
- `shared/00-must-follow.md`：新增 BOLA/IDOR、SSRF 硬规则（共 48 条）。
- `evals` 门槛：P1 为 **B09–B54 共 46 条，至少 40/46**；核心 P1 日常子集含 B51、B52（≥15/18）。
- `README.md`、`RELEASE.md`、`docs/rules-package-index.md`、`docs/onboarding-new-project.md`、`cursor/00-project-overview.mdc`：同步 1.9.0 与 evals 门槛。
- `contracts/openapi.baseline.yaml`：与 `openapi.yaml` 同步幂等头。

## 1.8.0 — 2026-05-24

### Added

- `shared/35-threat-modeling.md`：高风险接口、Webhook、外部回调、跨租户、PII 等威胁建模。
- `shared/36-crypto-key-management.md`：密码哈希、Token、签名、随机数、密钥轮换与吊销。
- `shared/37-service-to-service-auth.md`：内部服务调用、Webhook、MQ、Job 的机器身份与最小权限。
- `shared/38-cloud-native-runtime.md`：容器、K8s、Helm/Terraform/IaC 运行时安全。
- `shared/39-event-contracts.md`：Topic/Event schema、版本、兼容、Outbox、死信与重放。
- `shared/40-money-time-precision.md`：金额、币种、时间、时区、账期与精度。
- `shared/41-dictionary-state-machine.md`：字典、枚举、状态码、状态机与主数据。
- `shared/42-cost-governance.md`：付费外部调用、大查询、大导出、日志/归档/备份成本治理。
- `cursor/27`–`cursor/34`：对应 35–42 的 Cursor 触发规则。
- `evals`：**B43–B50**（威胁建模、弱加密、内部接口、运行时、事件契约、金额时间、状态机、成本）。

### Changed

- `README.md`、`codex/AGENTS.md`、`docs/rules-package-index.md`：同步 35–42 规则入口。
- `shared/00-must-follow.md`：新增 35–42 对应硬规则，全文重新编号至 46 条。
- `shared/10-verification-checklist.md`、`shared/26-ai-generation.md`：补充高阶治理收尾检查与 AI 读取顺序。
- `evals` 门槛：P1 为 **B09–B50 共 42 条，至少 36/42**。

## 1.7.1 — 2026-05-24

### Added

- 仓库根 `contracts/openapi.baseline.yaml`（与 `openapi.yaml` 同步，供 CI openapi-diff）。
- `docs/rules-package-index.md`：shared 01–34 与 docs 附录索引。

### Changed

- `05-openapi-contract.md`、`examples/README.md`、`RELEASE.md`：baseline 维护说明。
- `30-ownership-adr.md`：ADR 触发条件补充非 REST 范式。
- `07-persistence-mybatis.md`：交叉引用 `34-data-archival.md`。
- `docs/monorepo-layout.md`：baseline 路径、规则包版本独立说明。
- `examples/archunit`：application 不得依赖 api 包。
- `AuditLogController`：补充 `@PreAuthorize` 样板说明。

## 1.7.0 — 2026-05-24

### Added

- `shared/32-service-reliability.md`：SLO/错误预算、降级、RTO/RPO、告警、故障演练。
- `shared/33-alternate-api-paradigms.md`：GraphQL/gRPC/WebSocket/SSE 默认禁止、ADR 要求。
- `shared/34-data-archival.md`：大表归档、冷热分层、归档任务与 API 行为。
- `docs/backup-restore-runbook.md`：备份频率、恢复演练、审批、脱敏恢复、校验清单。
- `examples/config/SecurityConfig.sample.java`。
- `cursor/24-service-reliability.mdc`、`25-alternate-api-paradigms.mdc`、`26-data-archival.mdc`。
- `evals`：**B39–B42**（CORS、Swagger/Actuator 暴露、GPL 依赖、无恢复演练）。

### Changed

- `20-dependency-governance.md`：SBOM、许可证白黑名单、abandoned 包、传递依赖、CVE SLA。
- `06-security-authz.md`：CORS、CSRF、安全头、Cookie、登录态、Swagger/Actuator 生产规则。
- `31-production-data-ops.md`：链到 backup runbook 与 `32`。
- `00-must-follow.md`：可靠性、非 REST 范式、归档硬规则（38 条）。
- `AuditLogService` 接入 `AuditLogMapper` 分页查询；`UserService.delete` 先审计后删除。
- `scaffold-module-system.md`：SecurityConfig 指向 examples 样板。
- `evals` 门槛 **≥29/34**；`evals/README.md` 增加核心 P1 日常子集。
- `README.md`、`examples/README.md`、`23-quality-gates.md`：CI 样板须裁剪、禁止伪造通过。

## 1.6.1 — 2026-05-24

### Added

- `examples/scaffold/`：`AuditRecorder`、`AuditLogRecorder`、`AuditRecordCommand`、`AuditLog` 实体与 `UserService.delete` 审计写入演示。
- `examples/scaffold/java/common/audit/AuditContext.java`。
- `docs/PERFORMANCE_BUDGET.template.md`。
- `contracts/openapi.yaml`：`BusinessErrorCode` 枚举（与 `ErrorCodes` 对齐）。

### Changed

- `shared/26-ai-generation.md`：补充 `29`、`30`、`31` 读取要求。
- `shared/08-exception-errorcodes.md`、`shared/16-performance.md`、`shared/27-audit-log.md`：交叉引用 OpenAPI 错误码与审计写入样板。
- `docs/migration-from-template.md`、`evals/README.md`（B28/B36 等重叠说明）。
- `examples/archunit/LayeredArchitectureTest.java`：Controller 禁止 `@Transactional`、domain 禁止依赖 Spring Web。
- 根 `README.md`：注明前后端规则包版本独立演进。

## 1.6.0 — 2026-05-24

### Added

- `examples/checkstyle/checkstyle-snippet.xml`：最小 Checkstyle 样板。
- `examples/ci/github-actions-backend.yml`：Maven verify、OpenAPI diff、gitleaks、dependency-check、Flyway validate 样板。
- `docs/adr/0000-template.md`：ADR 模板。
- `examples/scripts/data-fix-template.sql`、`examples/scripts/data-fix-runbook.md`：生产数据修复 SQL 与执行 Runbook 样板。
- `evals`：**B34–B38**（后端越权、批处理内存、外部调用超时、硬编码配置、分布式锁 owner）。

### Changed

- `cursor/06-security-authz.mdc` 重命名为 `cursor/09-security-authz.mdc`，消除 Cursor 规则编号重复。
- `shared/06-security-authz.md`、`shared/15-testing.md`：补充敏感接口越权测试要求。
- `shared/16-performance.md`：补充容量、P95/P99、导入导出 / 批处理规模、索引 / count 策略。
- `shared/23-quality-gates.md`、`shared/30-ownership-adr.md`、`shared/31-production-data-ops.md`：补齐样板入口。
- `shared/00-must-follow.md`：新增越权测试、性能预算硬规则，全文重新编号至 35 条。
- `evals` 门槛：P1 为 **B09–B38 共 30 条，至少 26/30**。

## 1.5.0 — 2026-05-24

### Added

- `shared/30-ownership-adr.md`：Owner、ADR 触发条件、公共能力废弃与迁移。
- `shared/31-production-data-ops.md`：生产数据修复、手工 SQL、批量回填、备份恢复的审批 / dry-run / 回滚 / 审计规则。
- `cursor/22-ownership-adr.mdc`、`cursor/23-production-data-ops.mdc`。
- `evals`：**B32–B33**（公共 Starter 无 Owner/ADR、生产手工 SQL 无审批回滚）。

### Changed

- `codex/AGENTS.md`：任务表改为完整 `rules/...` 路径，新增架构决策与生产数据操作入口。
- `shared/00-must-follow.md`：新增 Owner/ADR 与生产数据操作硬规则，全文重新编号至 33 条。
- `shared/10-verification-checklist.md`：补充 Owner/ADR、生产数据操作收尾检查。
- `evals` 门槛：P1 为 **B09–B33 共 25 条，至少 22/25**。

## 1.4.3 — 2026-05-24

### Added

- `cursor/21-data-privacy-lifecycle.mdc`：PII、测试数据、日志/缓存/MQ/备份生命周期。
- `evals`：**B31**（生产 PII 进 fixture、缓存 key 明文手机号等）。
- `examples/scaffold/java/test/AuditLogControllerIT.sample.java`：审计查询结构、404 错误码、禁 DELETE。

### Changed

- `shared/00-must-follow.md`：新增第 16 条硬规则引用 `29-data-privacy-lifecycle.md`；全文重新编号至 31 条。
- `evals` 门槛：P1 为 **B09–B31 共 23 条，至少 19/23**。
- **1.4.0–1.4.2** 发布日期修正为 **2026-05-24**（消除与 1.3.0 日期倒挂）。

## 1.4.2 — 2026-05-24

### Added

- `contracts/openapi.yaml`：`GET /api/v1/system/audit-logs`、`GET .../{id}` 及 `AuditLog*` schema。
- `examples/scaffold/`：`AuditLogController`、`AuditLogService`、DTO；`db/migration/*/V2__init_system_audit_log.sql`。

### Changed

- `docs/fullstack-contract.md`：OpenAPI 审计节改为已落地说明。
- `docs/scaffold-module-system.md`、`examples/scaffold/README.md`：审计样板路径。

## 1.4.1 — 2026-05-24

### Changed

- `docs/fullstack-contract.md`：补充审计日志前后端字段映射、导入导出对齐、`traceId` 关联与 OpenAPI 推荐。
- `shared/27-audit-log.md`、`web-front/shared/14-upload-import-export.md`：交叉引用全栈契约。

## 1.4.0 — 2026-05-24

### Added

- `shared/27-audit-log.md`：审计必审操作、字段模型、失败阻断策略。
- `shared/28-external-integration.md`：外部 HTTP/SDK 超时、重试、熔断、分层、traceId。
- `shared/29-data-privacy-lifecycle.md`：敏感分级、保留周期、软删、测试脱敏。
- `cursor/19-audit-log.mdc`、`cursor/20-external-integration.mdc`。
- `evals`：**B27–B30**（审计、事务内外部调用、测试禁连生产、大表模糊查询）。

### Changed

- `05-openapi-contract.md`、`04-rest-api-design.md`：API 兼容策略细则（deprecated、枚举扩展、breaking 表、版本策略）。
- `07-persistence-mybatis.md`：索引与约束、expand/migrate/contract 引用、大表模糊查询。
- `18-idempotency-concurrency.md`：事务边界、分布式锁、乐观锁错误码、Outbox 引用。
- `17-messaging-async.md`、`21-configuration-secrets.md`、`22-operability.md`：事务消息、Feature Flag、发布回滚与 DB 三阶段。
- `15-testing.md`：Testcontainers、fixture、禁顺序、禁连生产/预发库。
- `00-must-follow.md`、`10-verification-checklist.md`、`06-security-authz.md`、`23-quality-gates.md`、`26-ai-generation.md`、`codex/AGENTS.md`：同步 27–29 与增强条目。
- `evals` 门槛：P1 为 **B09–B30 共 22 条，至少 18/22**。

## 1.3.0 — 2026-05-24

### Added

- `shared/23-quality-gates.md`：规则到工具 / CI 阻断级别映射。
- `shared/24-data-access-cache.md`：多租户、数据权限、缓存一致性、脱敏。
- `shared/25-jobs-scheduling.md`：定时任务、批处理、异步补偿。
- `shared/26-ai-generation.md`：AI 生成后端代码约束，替代重复编号的 `09-ai-generation.md`。
- `cursor/16-quality-gates.mdc`、`cursor/17-data-access-cache.mdc`、`cursor/18-jobs-scheduling.mdc`。
- `evals`：**B21–B26**（租户/数据权限、缓存失效、任务防重、多库迁移、API breaking、限流防刷）。

### Changed

- `README.md`、`AGENTS.md`、`00-must-follow.md`、`10-verification-checklist.md`：同步 23–25 规则入口。
- `06-security-authz.md`、`22-operability.md`：补充高风险接口限流、防刷与告警。
- `16-performance.md`、`17-messaging-async.md`：交叉引用缓存与任务规则。
- `evals` 门槛修正：P1 为 **B09–B26 共 18 条，至少 16/18**。

## 1.2.0 — 2026-05-24

### Added

- `examples/scaffold/`：common（ApiResult、异常、TraceId）+ `modules/system` 完整 Java/XML 样板。
- `examples/pom-dependencies.sample.xml`：Spring Boot / MP / Flyway / MapStruct / ArchUnit 依赖参考。
- `examples/scaffold/java/test/UserControllerIT.sample.java`：MockMvc 集成测试样板。
- `cursor/03-validation.mdc`。
- 仓库根 `docs/monorepo-layout.md`：全栈目录与契约流。

### Changed

- `docs/scaffold-module-system.md`、`onboarding-new-project.md`：指向 scaffold 源码。

## 1.1.0 — 2026-05-24

### Added

- `docs/onboarding-new-project.md`、`docs/scaffold-module-system.md`：新项目落地与包结构样板。
- `examples/config/`：MyBatis-Plus、`application` 配置样板。
- `examples/db/migration/`：MySQL / PostgreSQL 建表示例。
- `cursor/06-security-authz.mdc`、`cursor/13-pagination-query.mdc`。
- `contracts/openapi.yaml`：用户模块 CRUD + 统一响应/分页模型。

### Changed

- `shared/12-dto-mapping.md`：扩展 MapStruct、分页转换、OpenAPI 对齐。

## 1.0.0 — 2026-05-24

### Added

- 初始 Spring Boot 3 后端规则包：MyBatis-Plus + 多数据库（MySQL / PostgreSQL）。
- `shared/00`–`22` 场景规则（`07` 为 MyBatis-Plus + 多库）、`codex/` 任务路由、`cursor/*.mdc` 触发摘要。
- `evals` B01–B20（P0 8/8，P1 至少 16/18）。
- `examples/` ArchUnit 分层样板、`checkstyle` 片段、CI 说明。
- `docs/fullstack-contract.md`、`docs/sql-dialect-matrix.md` 与前端契约对齐说明。
