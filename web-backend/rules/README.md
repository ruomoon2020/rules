# Backend AI Rules（Spring Boot）

版本见 `VERSION`，变更见 `CHANGELOG.md`，发版见 `RELEASE.md`。

企业级 **Spring Boot 3 + Java 17+ + MyBatis-Plus** 规则包，支持 **MySQL、PostgreSQL** 等多数据库（方言 SQL 与迁移分治）。

- **Codex**：`codex/AGENTS.md` → 复制到后端仓库根目录 `AGENTS.md`
- **Cursor**：`cursor/*.mdc` → 复制到 `.cursor/rules/`
- **SSOT**：`shared/`；Cursor 摘要指向 shared，不重复全文

## 规则层级

```text
L0  shared/00-must-follow.md
L1  shared/01–31
L2  codex/*.md、cursor/*.mdc
```

## 落地（推荐方式 A）

1. 整包 `rules/` 放入后端仓库（submodule 或子目录）。
2. 复制 `codex/AGENTS.md` → 根 `AGENTS.md`。
3. 复制 `cursor/*.mdc` → `.cursor/rules/`。
4. 与前端共享 `contracts/openapi.yaml`（见 `docs/fullstack-contract.md`）。
5. 接入 `examples/` 中 ArchUnit、Checkstyle、OpenAPI diff。

## 持久化栈（本包默认）

| 项 | 约定 |
|---|---|
| ORM | MyBatis-Plus 3.x |
| 复杂 SQL | MyBatis XML（`resources/mapper/**`） |
| 多库 | `databaseId` + `mapper/dialect/{mysql,postgresql}/` |
| 迁移 | Flyway（`db/migration/`，可按库分子目录） |
| 分页 | MP `Page` / `IPage`，与 OpenAPI 对齐 |

## 完整文件清单

| 文件 | 职责 |
|---|---|
| `shared/00-must-follow.md` | 硬规则 |
| `shared/01-project-structure.md` | 包结构与依赖 |
| `shared/02-naming.md` | 命名 |
| `shared/03-code-style.md` | Java 风格与注释 |
| `shared/04-rest-api-design.md` | REST 设计 |
| `shared/05-openapi-contract.md` | OpenAPI SSOT |
| `shared/06-security-authz.md` | 安全与权限 |
| `shared/07-persistence-mybatis.md` | MyBatis-Plus、XML、多库 |
| `shared/08-exception-errorcodes.md` | 异常与错误码 |
| `shared/09-logging-observability.md` | 日志与 traceId |
| `shared/10-verification-checklist.md` | 收尾检查 |
| `shared/11-domain-model.md` | 领域与 Entity |
| `shared/12-dto-mapping.md` | DTO / MapStruct |
| `shared/13-validation.md` | Bean Validation |
| `shared/14-file-import-export.md` | 导入导出 |
| `shared/15-testing.md` | 测试 |
| `shared/16-performance.md` | 性能 |
| `shared/17-messaging-async.md` | 消息与异步（可选） |
| `shared/18-idempotency-concurrency.md` | 幂等与并发 |
| `shared/19-pagination-query.md` | 分页与排序白名单 |
| `shared/20-dependency-governance.md` | 依赖治理 |
| `shared/21-configuration-secrets.md` | 配置与密钥 |
| `shared/22-operability.md` | 可运维性 |
| `shared/23-quality-gates.md` | 质量门禁 / CI 映射 |
| `shared/24-data-access-cache.md` | 数据权限 / 多租户 / 缓存 |
| `shared/25-jobs-scheduling.md` | 定时任务 / 批处理 |
| `shared/26-ai-generation.md` | AI 生成约束 |
| `shared/27-audit-log.md` | 审计日志 |
| `shared/28-external-integration.md` | 外部 HTTP / 第三方 |
| `shared/29-data-privacy-lifecycle.md` | 隐私与数据生命周期 |
| `shared/30-ownership-adr.md` | 架构归属 / ADR |
| `shared/31-production-data-ops.md` | 生产数据操作 / 手工 SQL |
| `evals/*` | AI 行为回归 B01–B38 |
| `examples/scaffold/` | Java 源码样板（system 用户域） |
| `examples/*` | ArchUnit、Checkstyle、CI、配置、Flyway、POM 依赖、数据修复样板 |
| `docs/fullstack-contract.md` | 前后端契约 |
| `docs/sql-dialect-matrix.md` | 方言 SQL 登记 |
| `docs/onboarding-new-project.md` | 新项目落地步骤 |
| `docs/scaffold-module-system.md` | system 模块目录样板 |
| `docs/adr/0000-template.md` | ADR 模板 |
| `docs/PERFORMANCE_BUDGET.template.md` | 性能预算模板 |
| 仓库根 `docs/monorepo-layout.md` | 全栈 monorepo 布局 |

## Evals

**P0 8/8**，**P1 至少 26/30**（B09–B38）。见 `evals/README.md`。
