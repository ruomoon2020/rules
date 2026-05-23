# 全栈契约（前后端对齐）

> 维护者 / 架构文档；Codex 日常以各自 `rules/shared/05`（后端 OpenAPI）与前端 `12-schema-ssot` 为准。

## 单一来源

```text
contracts/openapi.yaml
  → 后端：实现 Controller/DTO、校验、MockMvc
  → 前端：生成 schema / src/api/generated（按前端项目脚本）
```

## 统一字段

| 字段 | 后端 | 前端 |
|---|---|---|
| `traceId` | MDC + 响应头 `X-Trace-Id`（名以项目为准） | request wrapper、logger |
| `errorCode` | `BusinessException` / `ErrorCodes` | `normalizeError`；枚举见 OpenAPI `BusinessErrorCode` |
| `message` | 用户可读文案 | 提示 UI |
| 分页 `page` / `pageSize` | `Page` 查询 | `19-list-pagination` |
| 分页 `total` / `records` | `IPage` 转换 | `useTable` |
| 权限码 | `@PreAuthorize` | 按钮权限指令 |
| `Idempotency-Key` | 可重试写操作 Header（OpenAPI `#/components/parameters/IdempotencyKey`） | 支付/下单/创建类请求携带 UUID；重试须复用同一键 |

## 错误响应示例

```json
{
  "code": 40001,
  "message": "用户不存在",
  "errorCode": "USER_NOT_FOUND",
  "traceId": "abc123",
  "data": null
}
```

## 发布顺序

1. OpenAPI PR + openapi-diff  
2. 后端发布（兼容旧前端）  
3. 前端 `api:gen` + 联调  

## 参考实现

- 后端样板：`examples/scaffold/`（`ApiResult`、`PageResponse`、`UserController` 与 OpenAPI 对齐）
- 契约占位：`contracts/openapi.yaml`（仓库根）

## 导入导出

后端 `14-file-import-export` 与前端 `14-upload-import-export` 对齐：幂等、错误明细、下载鉴权。

| 能力 | 后端 | 前端 |
|---|---|---|
| 幂等键 | `18-idempotency-concurrency` | 导入任务 `taskId` / 文件 hash |
| 错误明细 | 行列级错误码 + `errorCode` | 表格展示 + 错误报告下载 |
| 下载鉴权 | 短期 token / 鉴权 URL | 禁止缓存永久公开 URL |
| 审计（见下节） | 服务端写入 | 操作完成后刷新记录 / 管理端列表 |

---

## 审计日志（前后端对齐）

> 细则：后端 `shared/27-audit-log.md`；前端导入导出审计 `web-front/rules/shared/14-upload-import-export.md`（权限、审计与日志）；详情页操作记录 `13-form-and-detail.md`。

### 职责划分

| 侧 | 职责 |
|---|---|
| **后端** | 敏感操作**必须**落库（或审计服务）；字段完整；禁止仅用 `log.info` |
| **前端** | 不伪造审计；展示操作记录列表/详情；导入导出后提示成功并引导查看记录；敏感字段脱敏展示 |
| **契约** | 查询类接口在 OpenAPI 定义 `AuditLog`（或等价）DTO，与下表一致 |

### 统一字段映射

后端持久化与 API 响应使用**同一套 camelCase**（与 OpenAPI / 前端 generated 一致）：

| 字段 | 类型（建议） | 后端含义 | 前端展示 |
|---|---|---|---|
| `operatorId` | string | 操作人 ID | 操作人（可联表 `operatorName` 仅展示，不入库审计主字段） |
| `tenantId` | string | 租户 ID（多租户必填） | 租户列（多租户项目） |
| `action` | string | 稳定动作码，如 `USER_DELETE`、`IMPORT_USERS` | 操作类型（走字典 / i18n，**禁止**前端硬编码文案与后端码不一致） |
| `resourceType` | string | 资源类型，如 `User`、`ImportTask` | 模块 / 资源类型 |
| `resourceId` | string | 资源主键 | 资源 ID（列表可省略或折叠） |
| `requestSummary` | string | 条件摘要（筛选、批量数量、文件名等） | 条件摘要 |
| `beforeSummary` | string | 变更前摘要（非敏感明文） | 变更前（详情抽屉） |
| `afterSummary` | string | 变更后摘要 | 变更后 |
| `occurredAt` | string (date-time) | 服务端操作时间 | 操作时间（统一 `utils/format`） |
| `result` | string | `SUCCESS` / `FAIL` | 结果标签 |
| `errorCode` | string | 失败时业务码（可选） | 与全局 `errorCode` 一致，便于对照 |
| `traceId` | string | 与当次 HTTP 请求一致 | 运维排障可跳转日志（不对普通用户强展示） |
| `ip` | string | 客户端 IP | 可选列 |
| `userAgent` | string | 客户端 UA | 一般仅详情展示 |

### 导入 / 导出专项（与前端 `14` 对齐）

前端要求：操作人、时间、模块、条件摘要、文件名、任务 ID、结果。映射如下：

| 前端 `14` 描述 | 后端审计字段 |
|---|---|
| 操作人 | `operatorId`（+ 展示名由用户服务解析，不写审计明文 PII） |
| 时间 | `occurredAt` |
| 模块 | `resourceType` + `action`（如 `IMPORT` / `EXPORT`） |
| 条件摘要 | `requestSummary` |
| 文件名 | 写入 `requestSummary` 或扩展字段 `fileName`（须在 OpenAPI 与 DB 同时约定） |
| 任务 ID | 异步任务：`resourceId` = `taskId`，或 `resourceType` = `ImportTask` |
| 结果 | `result` + 失败时 `errorCode` |

`action` 建议枚举在 OpenAPI `components/schemas` 或团队字典文档维护，前后端共用（与 API 枚举扩展策略见 `05-openapi-contract.md`）。

### 与 `traceId` / 错误体关系

1. 业务 API 响应中的 `traceId`（见上节）与审计记录中的 `traceId` **同名同值**，便于从 UI 操作记录关联到网关 / 应用日志。
2. 审计**禁止**记录：密码、Token、完整证件号、完整银行卡号、密钥明文（后端 `27`、前端 `14` 日志节一致）。
3. 审计查询接口的成功响应仍使用统一 `ApiResult` 包装；单条审计 DTO **不要**套用业务 Entity。

### OpenAPI（已落地）

仓库根 `contracts/openapi.yaml` 已包含：

| 路径 | operationId | 说明 |
|---|---|---|
| `GET /api/v1/system/audit-logs` | `systemAuditLogPage` | 分页；筛选 `action`、`resourceType`、`operatorId`、`result`、时间范围 |
| `GET /api/v1/system/audit-logs/{id}` | `systemAuditLogDetail` | 详情（含 `beforeSummary`、`afterSummary`、`ip`、`userAgent`） |

Schema：`AuditLogSummaryResponse`（列表）、`AuditLogResponse`（详情）、`AuditResult`（`SUCCESS` / `FAIL`）。  
可选展示字段 `operatorName`、`fileName` 已标为 optional，新增字段须向后兼容。  
Java 样板 DTO / Controller 见 `examples/scaffold/java/modules/system/api/` 下 `AuditLog*`。

### 必审操作（全栈一致）

以下操作后端**必须**写审计；前端若有对应按钮，须在 PR 中确认不会跳过二次确认 / 权限校验：

- 登录成功/失败、权限与角色变更、用户启停  
- 单条/批量删除、批量更新、强制状态变更  
- 导入、导出、敏感报表下载  
- 系统配置、Feature Flag（不记密钥明文）  
- 跨租户操作（另见 `24-data-access-cache`）

### 审计失败策略（联调须知）

| 场景 | 后端 | 前端 |
|---|---|---|
| 阻断型（删数据、改权限、导出敏感） | 审计写入失败 → API 失败 | 展示错误，**不得**提示成功 |
| 记录型（可选查询审计） | 可异步补写 + 告警（项目文档声明） | 列表可延迟刷新 |

---

## 参考规则路径

| 主题 | 后端 | 前端 |
|---|---|---|
| OpenAPI SSOT | `shared/05-openapi-contract.md` | `shared/12-schema-ssot.md` |
| 审计写入 | `shared/27-audit-log.md` | `shared/14-upload-import-export.md` §权限、审计与日志 |
| 操作记录 UI | — | `shared/13-form-and-detail.md` |
| 日志 traceId | `shared/09-logging-observability.md` | `shared/18-logging-observability.md` |
