# Examples（硬门禁样板）

业务仓接入参考；路径相对于后端项目根。

## ArchUnit 分层

复制 `archunit/LayeredArchitectureTest.java` 到 `src/test/java/...`，按包名修改。

```bash
mvn test -Dtest=LayeredArchitectureTest
```

规则：Controller 不依赖 Mapper、不使用 `@Transactional`；domain 不依赖 Spring Web（可按项目调整）。

## Checkstyle

复制 `checkstyle/checkstyle-snippet.xml` 片段到项目 Checkstyle 配置。

## CI 样板

复制 `ci/github-actions-backend.yml` 到 `.github/workflows/backend-quality-gates.yml`，按项目 Maven / Gradle、数据库、OpenAPI baseline 路径调整。

## OpenAPI

```bash
# 示例：破坏性变更检测（工具按项目选择）
npx @redocly/cli diff contracts/openapi.yaml contracts/openapi.baseline.yaml
```

## Flyway 多库 CI

对 MySQL、PostgreSQL 各执行：

```bash
mvn -Dflyway.url=... flyway:migrate
```

或使用 Testcontainers（见 `15-testing.md`）。

## 危险 `${}` 扫描（可选）

```bash
# 人工审查：禁止未在白名单工具类中的 ${}
rg '\$\{' src/main/resources/mapper
```

## 生产数据修复

- `scripts/data-fix-template.sql` — dry-run、影响行数、备份表、执行与回滚草案。
- `scripts/data-fix-runbook.md` — 工单、Owner、执行窗口、验证与复盘记录。

规则见 `shared/31-production-data-ops.md`。

## 配置样板

- `config/application-mybatis.sample.yml` — 数据源、MP、Flyway
- `config/MybatisPlusConfig.sample.java` — 分页插件、databaseId
- `db/migration/mysql/`、`postgresql/` — Flyway 建表示例

## Java 源码样板

`scaffold/` — `UserController`、`UserService`、`UserMapper`、DTO、MapStruct、`ApiResult`、`GlobalExceptionHandler` 等。复制后改包名。

## 新建项目

见 `docs/onboarding-new-project.md`、`docs/scaffold-module-system.md`。

全栈目录见仓库根 `docs/monorepo-layout.md`。

## Maven 脚本示例

见 `package-scripts.sample.json`。
