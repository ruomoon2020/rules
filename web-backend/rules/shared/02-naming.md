# Naming Rules（Java / Spring）

## 总原则

1. 英文语义命名；包名全小写；类名 PascalCase。
2. 同一概念全项目一词；先看项目既有约定，再按本文件。
3. 禁止 `Manager`、`Helper`、`Util` 膨胀；优先领域名 + 职责。

## 包与类

| 类型 | 规则 | 示例 |
|---|---|---|
| 包 | 小写，点分隔 | `modules.system.application` |
| Controller | `*Controller` | `UserController` |
| Service | `*Service` / `*AppService` | `UserService` |
| Mapper | `*Mapper` | `UserMapper` |
| Entity | 单数名词 | `User` |
| Request DTO | `*Request` | `UserCreateRequest` |
| Response DTO | `*Response` / `*VO` | `UserPageResponse` |
| 异常 | `*Exception` | `BusinessException` |
| 常量类 | `*Constants` | `ErrorCodes` |

## 方法与变量

| 动作 | 前缀 |
|---|---|
| 查询单条 | `get` / `find` |
| 查询列表/分页 | `list` / `page` / `query` |
| 新增 | `create` / `add` |
| 更新 | `update` |
| 删除 | `delete` / `remove` |
| 是否存在 | `exists` |
| 导入导出 | `import` / `export` |

布尔：`is`、`has`、`can`。禁止裸名 `data`、`flag`、`result`（除局部极短作用域）。

## 数据库

1. 表名：小写 + 下划线，单数或团队统一复数，全项目一致。
2. 列名：下划线；外键 `xxx_id`。
3. Mapper 方法名与 XML `id` 一致。

## 错误码与权限

1. 业务错误码：`DOMAIN_RESOURCE_REASON`，如 `USER_NOT_FOUND`（与 `08` 一致）。
2. 权限码：`domain:resource:action`，如 `system:user:create`（与前端对齐）。

## REST 与 OpenAPI

1. 路径 kebab-case 复数资源：`/api/v1/system/users`。
2. 查询参数 camelCase，与 DTO 字段一致。
