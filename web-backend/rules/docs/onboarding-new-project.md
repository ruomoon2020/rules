# 新建 Spring Boot 项目落地指南

> 维护者与架构 onboarding；AI 日常读 `README.md`、`codex/AGENTS.md`。

## 0. 选择成熟度目标

按 `docs/rule-maturity-model.md` 声明目标 **Level**（建议：首个迭代 Level 0，核心域上线前 Level 1–2）。不必一次接入全部 42 个 shared 文件。

## 1. 复制规则包

```text
your-backend/
├─ AGENTS.md                 ← rules/codex/AGENTS.md
├─ rules/                    ← 整包 web-backend/rules
├─ contracts/openapi.yaml    ← 可与 monorepo 根 contracts/ 同步
├─ .cursor/rules/*.mdc
└─ src/main/java/...
```

## 2. 推荐技术选型

- Java 17+、Spring Boot 3.x
- MyBatis-Plus 3.x + Flyway
- 数据库：MySQL 8、PostgreSQL 15（按环境启用）
- MapStruct、Springdoc/OpenAPI、ArchUnit、Testcontainers

## 3. 最小包结构

见 `docs/scaffold-module-system.md`，先落地 `modules/system` 一个域。

## 4. 源码与配置样板

- `examples/scaffold/` — common + `modules/system` Java 与 Mapper XML
- `examples/pom-dependencies.sample.xml` — Maven 依赖参考
- `examples/config/application-mybatis.sample.yml`
- `examples/config/MybatisPlusConfig.sample.java`
- `examples/config/SecurityConfig.sample.java`
- `docs/backup-restore-runbook.md`、`docs/PERFORMANCE_BUDGET.template.md`

## 5. 硬门禁接入

1. `examples/archunit/LayeredArchitectureTest.java` → `src/test/java`
2. `mvn verify` 进 CI
3. OpenAPI diff（契约 PR 必跑）
4. Flyway：MySQL + PostgreSQL 各跑迁移（若声明多库）

## 6. 与前端联调

1. 共用 `contracts/openapi.yaml`
2. 后端先发兼容版本 → 前端 `api:gen`
3. 对齐 `traceId`、`errorCode`、分页字段（`docs/fullstack-contract.md`）

## 7. 验证

- `evals/adoption-checklist.md` 按目标 Level 勾选
- 日常：**Smoke**（`evals/smoke-prompts.md`）；发版：**Full** B01–B54（P0 8/8，P1 ≥40/46）
- 业务仓 PR：复制 `rules/examples/.github/` → 仓库根 `.github/`
- 契约 baseline：首次稳定后生成 `contracts/openapi.baseline.yaml` 供 CI diff（见 `examples/README.md`）
