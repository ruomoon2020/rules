# 新建 Spring Boot 项目落地指南

> 维护者与架构 onboarding；AI 日常读 `README.md`、`codex/AGENTS.md`。

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

- `evals/adoption-checklist.md` 勾选
- 跑 `evals/prompts.md` B01–B38（P0 8/8，P1 ≥26/30）
