# Validation

1. Controller 入参 `@Valid` / `@Validated`。
2. 分组：`Create` / `Update` 使用 validation groups。
3. 校验消息与 OpenAPI `description` 一致；支持 i18n（按项目）。
4. 业务规则（跨字段）在 Service 校验，返回明确 `errorCode`。
5. 枚举使用契约枚举，禁止魔法字符串。
