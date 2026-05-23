# Logging & Observability

与前端 `18-logging-observability.md` 字段对齐。

## 结构化字段

| 字段 | 说明 |
|---|---|
| `event` | `domain.resource.action.result` |
| `traceId` | 请求链路，MDC + 响应头回传 |
| `userId` / `tenantId` | 按项目 |
| `durationMs` | 慢接口 |
| `errorCode` | 业务错误 |

使用 SLF4J + Logback；禁止 `System.out`。

## TraceId

1. `Filter` 或 Micrometer Tracing 注入；缺失时生成。
2. 写入 MDC；出站 HTTP 可选传递。
3. 与前端 `traceId` 请求头名称在 `fullstack-contract` 中固定。

## 指标与健康

1. 暴露 Actuator：`health`、`info`（见 `22-operability.md`）。
2. 关键接口 QPS、延迟、错误率接入监控系统（按项目）。

## 禁止

- 密码、Token、完整证件号、完整 body。
- 生产 DEBUG 默认关闭。
