# AI Generation Rules

用于约束 AI 生成后端代码时的最小行为边界。

1. 不得虚构 Mapper 方法、MyBatis-Plus API、OpenAPI 字段、权限码、错误码。
2. 写 SQL 前阅读既有 XML、Mapper 接口、分页插件与 `databaseId` 配置。
3. 多库场景默认写可移植 SQL；方言 SQL 须登记 `docs/sql-dialect-matrix.md`。
4. 禁止 Controller → Mapper、禁止 Entity 出 API、禁止 Service 中写数据库方言业务分支。
5. 写字段、DTO、错误码、分页结构前先读 `contracts/openapi.yaml` 或项目约定契约。
6. 生成定时任务、缓存、多租户查询、导入导出时，必须追加读取对应 shared 文件。
7. 生成审计、外部调用、DB 索引/迁移、API 废弃字段时，须读 `27`、`28`、`07`、`05`。
8. 生成公共 Starter、新依赖、跨模块抽象时，须读 `30-ownership-adr.md`；生产数据修复 / 手工 SQL 须读 `31-production-data-ops.md`。
9. 涉及 PII、测试数据、缓存 key、日志 / MQ / 备份时，须读 `29-data-privacy-lifecycle.md`。
10. 完成前自检 `10-verification-checklist.md`。
11. 命名见 `02-naming.md`；注释见 `03-code-style.md`。
