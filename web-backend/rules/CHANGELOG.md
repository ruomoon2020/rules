# Changelog

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
