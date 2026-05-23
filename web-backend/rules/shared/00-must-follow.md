# Must Follow Rules（后端）

违反即拒 PR。细节见其他 `shared/` 文件。

## 架构与分层

1. 依赖方向：`api(Controller)` → `application(Service)` → `domain` → `infrastructure(Mapper)`；禁止反向与跨层短路。
2. **禁止** Controller / Facade 直接注入 `Mapper` / `Repository`。
3. `domain` 禁止依赖 Spring Web、MyBatis、HTTP Client 实现细节。
4. 模块间禁止循环依赖；公共能力放 `common`，业务按 `modules/{bounded-context}` 划分。

## API 与契约

5. 对外 REST 以 **`contracts/openapi.yaml`**（或项目约定 OpenAPI 路径）为 SSOT；改接口先改契约再实现。
6. **禁止**将持久化 `Entity` 作为 REST 请求/响应体；对外仅 `Request` / `Response` DTO。
7. 统一响应包装与错误体见 `08-exception-errorcodes.md`；`errorCode` 与前端约定一致。
8. 分页入参/出参须与 OpenAPI 一致（`page`、`pageSize`、`total`、`records`），见 `19-pagination-query.md`。

## 持久化（MyBatis-Plus）

9. 简单 CRUD 使用 MP `BaseMapper` + `IService`；复杂 SQL 使用 XML，见 `07-persistence-mybatis.md`。
10. **禁止**在 Java 代码中拼接 SQL 字符串；动态条件用 `Wrapper` 或 XML + `#{}`。
11. **禁止**将用户输入直接传入 XML `${}`；排序字段、列名须白名单校验。
12. 写操作事务边界在 **application/service** 层 `@Transactional`；禁止在 Controller 开事务。
13. 多数据库差异仅出现在 **方言 XML / databaseId / Flyway 分库脚本**，禁止 Service 层 `if (mysql)` 分支业务逻辑。

## 安全

14. 默认鉴权；敏感操作须权限码 + 审计日志（字段与必审操作见 `27-audit-log.md`）。
15. 禁止日志、异常信息输出密码、Token、完整证件号、完整请求/响应体。
16. 敏感数据、PII、测试数据及日志 / 缓存 / MQ / 备份中的数据生命周期须遵守 `29-data-privacy-lifecycle.md`。
17. 禁止 SQL 注入；禁止拼接 `order by ${field}` 未经白名单处理。

## 配置与密钥

18. 禁止将生产密钥、AK/SK、数据库密码提交 Git；使用环境变量或配置中心。
19. 生产禁止 `spring.jpa.hibernate.ddl-auto=update` 及等价「自动改表」。

## 工程门禁

20. 提交前运行项目已配置的 `mvn verify` / `./gradlew check`（含 test、checkstyle、archunit 若配置）。
21. 契约变更须 OpenAPI diff / 兼容性 Review；破坏性变更须版本与迁移说明（细则见 `05-openapi-contract.md`）。
22. 新增 / 升级依赖须遵守 `20-dependency-governance.md`。
23. 多租户 / 数据权限 / 缓存一致性须遵守 `24-data-access-cache.md`。
24. 定时任务、批处理、异步补偿须遵守 `25-jobs-scheduling.md`。
25. 公共架构、跨模块契约、基础设施依赖须确认 Owner；触发条件满足时须补 ADR（见 `30-ownership-adr.md`）。
26. 生产数据修复、手工 SQL、批量回填须有 dry-run、影响行数、审批、回滚或前滚方案与审计（见 `31-production-data-ops.md`）。
27. 敏感接口须覆盖未登录、无权限、跨租户、普通用户访问管理员资源等越权测试（见 `06-security-authz.md`、`15-testing.md`）。
28. 核心接口、导入导出、批处理须说明性能预算、数据量上限、索引 / count 策略与降级方案（见 `16-performance.md`）。
29. 唯一业务约束须数据库唯一索引；大表禁止无条件 `LIKE '%keyword%'`（见 `07-persistence-mybatis.md`）。
30. 事务内禁止同步外部 HTTP/MQ；分布式锁须过期时间与释放校验（见 `18-idempotency-concurrency.md`）。
31. 外部集成须超时、错误映射、禁止 Controller 直调 SDK（见 `28-external-integration.md`）。
32. 测试禁止连接生产/预发库；多库须 Testcontainers 验证迁移（见 `15-testing.md`）。

## AI 生成

33. 写 Mapper / SQL 前阅读项目 MP 配置、`Mapper` 接口与 XML 既有模式；禁止虚构 MP API。
34. 写字段、DTO 前阅读 OpenAPI；禁止添加契约中不存在的字段。
35. 输出前自检 `10-verification-checklist.md`。
