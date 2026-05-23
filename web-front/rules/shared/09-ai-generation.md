# AI Generation Rules

用于约束 Codex、Cursor、Copilot 等 AI 生成代码。

## 基本原则

1. AI 不能自由发挥项目架构。
2. AI 不能凭空创造字段、Props、Slots、权限码、路由名。
3. AI 必须优先读取项目已有组件、schema、类型和工具函数。
4. AI 输出必须能被 lint、type-check、schema check 验证。

## 代码体量与结构

1. 单文件不超过 400 行；超出须拆 composable 或子组件。
2. 禁止在单文件模板内堆叠 API、权限、表格、表单、弹窗全部逻辑。
3. 禁止无说明引入新依赖。
4. 禁止修改公共组件 API 而不同步所有调用方。
5. 列表页优先 `useTable`（或项目等价封装），须含 error 态与重试；分页行为见 `shared/19-list-pagination.md`。

## 页面生成前

生成或修改 `src/views/**` 前：

1. 阅读 `shared/11-base-components-context.md` 或 Base 源码。
2. 阅读 `shared/12-schema-ssot.md` 或 `contracts/schema.json`。
3. 确认路由 `name`；需要缓存时写 `defineOptions({ name })`。
4. 确认权限码、字典、错误处理模式。
5. 确认使用 Base 组件，不用原生 Element Plus。

未阅读 Base 定义与 schema 前，不得开始编写业务页面。

## 双轨约束

软约束：先读 `shared/11-base-components-context.md`、`shared/12-schema-ssot.md`。

硬门禁：`pnpm lint`、`pnpm type-check`、`pnpm api:check`、CI（见 `shared/08-quality-gates.md`）。

## 禁止行为

1. 禁止在 `views` 中写 `<el-table>`、`<ElButton>` 等原生 Element Plus（含自动导入的 PascalCase）。
2. 禁止虚构 `BaseTable` 列字段或 props。
3. 禁止跳过 request wrapper。
4. 禁止 `as any` 通过检查。
5. 禁止把 mock、调试代码留在生产路径。
6. 禁止删除权限、安全、错误处理以简化实现。
7. 禁止在日志中写入 Token、完整手机号等敏感信息；须用结构化 logger（见 `18-logging-observability.md`）。
8. 列表页须处理分页回退与请求竞态（见 `19-list-pagination.md`）。

## 输出前自检

见 `shared/10-verification-checklist.md`。
