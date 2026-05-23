# Testing

## 单元测试

1. Service 逻辑 Mock Mapper；覆盖分支与异常。
2. Mapper 复杂 SQL：使用内嵌 DB 或 **Testcontainers**（优先于共享开发库）。

## 集成测试

1. `@SpringBootTest` + MockMvc 测 Controller 契约。
2. **Testcontainers**：至少 MySQL 或 PostgreSQL 之一与生产一致；多库项目 **两种库均须**跑迁移 + 核心 SQL 用例（CI matrix）。
3. 测试数据使用 **fixture / builder / `@Sql`**，禁止依赖共享环境脏数据或执行顺序。
4. **禁止**测试用例依赖 `@Order` 或隐式执行顺序（JUnit 5 默认并行友好）。
5. **禁止**集成测试连接生产或预发数据库；`application-test.yml` 仅指向容器或本地 Testcontainers。
6. 敏感接口须包含越权测试：未登录、无权限、跨租户、普通用户访问管理员资源（见 `06-security-authz.md`）。

## 契约

1. OpenAPI 与 MockMvc 响应结构一致。
2. 改 OpenAPI 须更新测试或契约测。
3. **消费者驱动契约**（推荐）：Spring Cloud Contract / Pact 等，由 `contracts/openapi.yaml` 或契约件驱动前后端/服务间测试；CI 按项目启用，未配置须在 PR 说明。
4. 敏感接口越权用例须与 `06` BOLA/IDOR 场景一致（他人 `id`、跨租户）。

## ArchUnit

运行 `examples/archunit` 分层规则（Controller 不依赖 Mapper 等）。

## CI 质量门禁

```bash
mvn verify
# 或 ./gradlew check
```

PR 必跑建议包含：

- 单元测试 + 集成测试（Testcontainers 覆盖 MySQL/PostgreSQL 若多库）
- Checkstyle / Spotless
- ArchUnit
- OpenAPI diff / Spectral
- Flyway validate（各支持库）

脚本不存在时不得伪造「已通过」。跳过门禁须按 `23-quality-gates.md` 说明原因。

## 测试数据与隐私

1. 测试数据不得含未脱敏的生产 PII（见 `29-data-privacy-lifecycle.md`）。
2. 导出/导入相关测试使用最小 fixture 文件，禁止提交真实业务导出件。
