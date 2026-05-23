# Exception & Error Codes

## 统一模型

1. 使用 `@RestControllerAdvice` 全局处理异常。
2. 业务异常 `BusinessException`（或项目等价）携带 **errorCode**、可选 **httpStatus**。
3. 响应体字段与前端 normalizer 对齐：`code`、`message`、`errorCode`、`traceId`（见 `docs/fullstack-contract.md`）。

## 错误码

1. 格式：`DOMAIN_REASON`，全大写下划线，如 `USER_NOT_FOUND`。
2. 错误码须在枚举或常量类集中维护；禁止魔法字符串散落。
3. 未知系统异常映射为 `INTERNAL_ERROR`，不向客户端暴露堆栈。

## 日志

1. 5xx 记录完整堆栈（含 traceId）；4xx 业务异常按级别记录。
2. 禁止把 SQL、参数中的敏感字段打入 INFO。

## 与 OpenAPI

1. 文档中声明标准错误响应 schema。
2. 新增错误码须更新 `contracts/openapi.yaml` 中 `BusinessErrorCode` 枚举（或项目错误码表），并与 `ErrorCodes` 常量同步。
3. 禁止删除或静默修改已有 `errorCode` 语义（见 `05-openapi-contract.md`）。

## 样板代码

`examples/scaffold/java/common/exception/` — `BusinessException`、`GlobalExceptionHandler`、`ErrorCodes`。

