# AGENTS.md（Spring Boot 后端）

本仓库为企业级 Spring Boot 后端项目。Codex 必须以 `rules/` 为 AI 规则唯一入口。

## 每次改代码前必读

1. `rules/codex/01-before-editing.md`
2. `rules/shared/00-must-follow.md`

## 按任务追加阅读

| 任务 | 必读规则 |
|---|---|
| 任意后端改动 | `rules/codex/01-before-editing.md`、`rules/shared/00-must-follow.md` |
| 架构 / 新模块 | `rules/shared/01-project-structure.md`、`rules/shared/30-ownership-adr.md` |
| 新 REST 接口 | `rules/shared/04-rest-api-design.md`、`rules/shared/05-openapi-contract.md`、`rules/shared/12-dto-mapping.md`、`rules/shared/08-exception-errorcodes.md`、`rules/codex/02-api-implementation.md` |
| MyBatis / SQL / 多库 | `rules/shared/07-persistence-mybatis.md`、`rules/shared/19-pagination-query.md`、`rules/docs/sql-dialect-matrix.md` |
| 安全 / 权限 | `rules/shared/06-security-authz.md` |
| 导入 / 导出 | `rules/shared/14-file-import-export.md`、`rules/shared/18-idempotency-concurrency.md` |
| 日志 / 监控 | `rules/shared/09-logging-observability.md` |
| 命名 / 风格 | `rules/shared/02-naming.md`、`rules/shared/03-code-style.md` |
| 测试 / CI | `rules/shared/15-testing.md`、`rules/shared/23-quality-gates.md` |
| 性能 / 容量 / 批处理规模 | `rules/shared/16-performance.md`、`rules/shared/19-pagination-query.md` |
| 依赖升级 | `rules/shared/20-dependency-governance.md`、`rules/shared/30-ownership-adr.md` |
| 数据权限 / 缓存 / 多租户 | `rules/shared/24-data-access-cache.md`、`rules/shared/06-security-authz.md` |
| 定时任务 / 批处理 / 异步补偿 | `rules/shared/25-jobs-scheduling.md`、`rules/shared/17-messaging-async.md` |
| 配置 / 密钥 / 运维 / 发布回滚 | `rules/shared/21-configuration-secrets.md`、`rules/shared/22-operability.md` |
| 审计日志 | `rules/shared/27-audit-log.md`、`rules/shared/06-security-authz.md` |
| 外部 HTTP / 第三方 SDK | `rules/shared/28-external-integration.md`、`rules/shared/18-idempotency-concurrency.md`、`rules/shared/30-ownership-adr.md` |
| 隐私与数据生命周期 | `rules/shared/29-data-privacy-lifecycle.md`、`rules/shared/24-data-access-cache.md` |
| 架构决策 / 公共抽象 / Owner | `rules/shared/30-ownership-adr.md` |
| 生产数据修复 / 手工 SQL / 回填 | `rules/shared/31-production-data-ops.md`、`rules/docs/backup-restore-runbook.md`、`rules/shared/27-audit-log.md` |
| 可靠性 / SLO / 降级 / 演练 | `rules/shared/32-service-reliability.md`、`rules/shared/22-operability.md` |
| GraphQL / gRPC / WebSocket / SSE | `rules/shared/33-alternate-api-paradigms.md`、`rules/shared/30-ownership-adr.md` |
| 数据归档 / 冷热分层 | `rules/shared/34-data-archival.md`、`rules/shared/25-jobs-scheduling.md` |
| 威胁建模 / 高风险安全变更 | `rules/shared/35-threat-modeling.md`、`rules/shared/06-security-authz.md` |
| 加密 / Token / 签名 / 密钥 | `rules/shared/36-crypto-key-management.md`、`rules/shared/21-configuration-secrets.md` |
| 服务间认证 / Webhook / MQ 身份 | `rules/shared/37-service-to-service-auth.md`、`rules/shared/36-crypto-key-management.md` |
| 容器 / K8s / IaC | `rules/shared/38-cloud-native-runtime.md`、`rules/shared/23-quality-gates.md` |
| MQ / 事件契约 / Outbox | `rules/shared/39-event-contracts.md`、`rules/shared/17-messaging-async.md` |
| 金额 / 时间 / 时区 / 精度 | `rules/shared/40-money-time-precision.md`、`rules/shared/11-domain-model.md` |
| 字典 / 枚举 / 状态机 | `rules/shared/41-dictionary-state-machine.md`、`rules/shared/05-openapi-contract.md` |
| 成本 / 配额 / 云资源 | `rules/shared/42-cost-governance.md`、`rules/shared/16-performance.md` |
| OWASP / 合规映射 / 发版与事故 | `rules/docs/owasp-api-top10-mapping.md`、`rules/docs/compliance-cn-mapping.md`、`rules/docs/release-checklist.md`、`rules/docs/incident-postmortem-template.md` |
| 新项目采纳分层 / PR 自检 | `rules/docs/rule-maturity-model.md`、`rules/docs/pull-request-template.md` |
| AI 生成复杂后端代码 | `rules/shared/26-ai-generation.md` |
| 收尾 / Review | `rules/shared/10-verification-checklist.md`、`rules/codex/05-verification.md` |

- 不要读 `rules/cursor/*.mdc`（仅供 Cursor）。
- 不要读 `rules/docs/migration-from-template.md`（维护者用）。
- 新项目结构见 `rules/docs/scaffold-module-system.md`。

## Hard Rules（摘要）

- Controller 禁止直接调用 Mapper。
- 禁止 Entity 作为 API  body；OpenAPI 为先。
- 禁止用户输入进入 SQL `${}`；排序白名单。
- 写操作 `@Transactional` 在 Service 层。
- 多库：方言仅在 XML/databaseId/Flyway，禁止 Service 里按库写业务分支。
- 多租户 / 数据权限不得漏条件；缓存必须有 key、TTL、失效策略。
- 定时任务多实例须防重，重试须幂等。
- 敏感操作须结构化审计；禁止事务内同步外部 HTTP。
- 敏感接口须覆盖越权测试；核心接口 / 批处理须说明性能预算与数据量上限。
- 公共架构、依赖、跨模块契约须确认 Owner；触发条件满足时先补 ADR。
- 生产数据修复 / 手工 SQL 必须有 dry-run、影响行数、审批、回滚和审计。
- 高风险安全变更须做威胁建模；密码/Token/签名/密钥禁止弱加密与硬编码。
- 内部服务、Webhook、MQ、Job 不得只信内网；须有机器身份、签名/幂等/审计。
- 金额禁 double/float；时间须明确时区和边界；状态流转不得绕过状态机。
- API breaking / deprecated 遵守 `05`；大表禁止无条件 `%keyword%` 模糊查询。
- 对象级授权（BOLA/IDOR）与 SSRF 出站校验；可重试写操作须幂等键；metric 禁止高基数 label。

## 完成前

```bash
mvn verify
# 或 ./gradlew check
```

详见 `rules/shared/10-verification-checklist.md`。
