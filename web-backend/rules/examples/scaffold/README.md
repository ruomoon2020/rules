# Java 源码样板

**非可运行模块**：复制到业务项目后修改包名 `com.company.product`，补全依赖与 Security 配置。

| 路径 | 说明 |
|---|---|
| `java/common/` | 统一响应、异常、traceId、`audit/AuditContext` |
| `java/modules/system/` | 用户域 + 审计读写（`AuditRecorder`、`AuditLog*` API） |
| `java/test/` | `UserControllerIT`、`AuditLogControllerIT` 集成测试样板 |
| `db/migration/*/V2__init_system_audit_log.sql` | 审计表样板，字段对齐 OpenAPI |
| `resources/mapper/system/UserMapper.xml` | 可移植列表 SQL |

配套：`docs/scaffold-module-system.md`、`../config/`、`../db/migration/`。
