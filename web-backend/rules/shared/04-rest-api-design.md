# REST API Design Rules

## 资源与动词

1. 资源名复数名词；路径版本前缀 `/api/v1`（按项目约定）。
2. 查询用 `GET`；创建 `POST`；全量更新 `PUT`；部分更新 `PATCH`；删除 `DELETE`。
3. 批量操作：`POST /users/batch-delete` 等，须在 OpenAPI 描述清楚。

## 统一响应

成功与失败结构见 `08-exception-errorcodes.md`，典型：

```json
{
  "code": 0,
  "message": "ok",
  "data": { },
  "traceId": "..."
}
```

列表分页 `data`：

```json
{
  "records": [],
  "total": 100,
  "page": 1,
  "pageSize": 20
}
```

与前端 `19-list-pagination` 对齐。

## 幂等

1. 创建类接口若支持重试，使用 `Idempotency-Key` 或业务幂等键，见 `18-idempotency-concurrency.md`。
2. `PUT` 按资源 ID 幂等；`POST` 非幂等须文档说明。

## 版本与兼容

1. 破坏性变更升版本或新路径；OpenAPI diff 进 CI。
2. **字段只增不改语义**：新字段默认可选；禁止在未升版本时改变既有字段含义。
3. 废弃字段走 OpenAPI `deprecated: true`，保留至少一个版本周期；细则见 `05-openapi-contract.md`。
4. 枚举只允许扩展新值，禁止删除或静默改已有枚举含义。
5. `nullable`、`required`、类型变化均属 breaking，须版本策略与迁移说明。
6. API 版本策略（URL `/api/v1`、Header、兼容字段）项目选一种并文档化，禁止混用无说明。
7. 删除接口须有替代方案、下线时间与前端/调用方通知记录。
