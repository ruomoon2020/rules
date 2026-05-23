# Audit Log Rules

企业后台须对高风险操作留**不可篡改、可检索**的审计记录。与业务日志（`09-logging-observability.md`）分离：审计面向合规与追责，业务日志面向排障。

## 必须审计的操作

至少包含（按项目扩展）：

| 类别 | 示例 |
|---|---|
| 身份与权限 | 登录成功/失败、登出、密码重置、MFA |
| 授权变更 | 角色/权限/数据范围变更、用户启停 |
| 数据变更 | 单条/批量删除、批量更新、状态强制变更 |
| 导入导出 | 导入、导出、下载敏感报表 |
| 配置 | 系统参数、Feature Flag、密钥轮换（不记明文） |
| 跨租户 | 跨租户查询、代操作、租户切换 |

低频敏感操作也须审计，不得因「很少用」省略。

## 审计字段（建议模型）

| 字段 | 说明 |
|---|---|
| `operatorId` | 操作人 ID |
| `tenantId` | 租户 ID（多租户必填） |
| `action` | 稳定动作码，如 `USER_DELETE` |
| `resourceType` | 资源类型，如 `User` |
| `resourceId` | 资源主键 |
| `beforeSummary` / `afterSummary` | 变更前后摘要（非完整敏感明文） |
| `requestSummary` | 条件摘要（导出筛选、批量 ID 数量等） |
| `ip` | 客户端 IP |
| `userAgent` | 可选 |
| `traceId` | 与请求链路一致 |
| `result` | `SUCCESS` / `FAIL` + 业务错误码 |
| `occurredAt` | 操作时间（服务端） |

禁止在审计中记录：密码、Token、完整证件号、完整银行卡号、密钥明文。

## 存储与生命周期

1. 审计表 / 审计服务与普通业务表分离；**禁止**业务接口允许普通用户删除审计记录。
2. 保留周期按合规要求配置（如 180 天～数年）；到期归档而非物理删除（除非法规允许）。
3. 审计写入失败：
   - **阻断型**（权限变更、删除、导出敏感数据）：应失败并告警，禁止静默成功。
   - **记录型**（只读查询类可选审计）：可降级为异步补写 + 告警，须在项目文档中声明。

## 实现约定

1. 审计逻辑放在 application 层或专用 `AuditService`，禁止仅在 Controller `log.info` 代替。
2. 管理端查询 API 与 DTO 以 `contracts/openapi.yaml` 中 `AuditLog*` 为准；表结构参考 `examples/db/migration/*/V2__init_system_audit_log.sql`。
3. 写入样板：`examples/scaffold/java/modules/system/application/audit/`（`AuditRecorder`、`UserService.delete` 演示）。
4. 与 `14-file-import-export.md` 导入导出审计字段对齐；前后端字段名与展示映射见 `docs/fullstack-contract.md` §审计日志。
5. 跨租户操作须额外记录 `reason` 或工单号（若项目要求），见 `24-data-access-cache.md`。

## 禁止

- 用 `log.info` 代替结构化审计。
- 审计记录含敏感明文或可逆凭证。
- 允许通过管理接口批量清空审计表且无超级管理员双人复核。
