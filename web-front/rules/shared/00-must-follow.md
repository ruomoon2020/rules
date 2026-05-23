# Must Follow Rules

这些是违反即拒 PR 的硬规则。不要把 UI 细节放进本文件；细节规则见其他 shared 文件。

## 架构与依赖

1. `apps` 可依赖 `packages`，`packages` 禁止依赖 `apps`。
2. `components/base` 禁止依赖业务 API、业务 store、业务字段。
3. `utils` 禁止依赖 Vue 组件实例、DOM、路由实例。
4. 页面私有代码就近放置；跨页面复用后再沉淀到公共目录。

## 页面与组件

5. `src/views/**` 禁止直接使用 `el-*` 标签。
6. `src/views/**` 禁止直接从 `element-plus` 及 `element-plus/*` 引入组件。
7. `src/views/**` 禁止使用 Element Plus 的 PascalCase 组件（如 `<ElButton>`、`<ElTable>`）；即使用 `unplugin-vue-components` 自动导入也不得以原生 EP 组件出现在 views。须使用项目 `Base*` 组件。
8. 业务页面优先使用 `Base*` 组件，不重复封装表格、弹窗、筛选、表单。
9. AI 或人工都不得虚构 `BaseTable`、`BaseForm`、`BaseDialog` 的 Props、Events、Slots。
10. 标准列表页必须遵守 `shared/04-ui-patterns.md` 的页面骨架。
11. destructive 操作必须有确认；异步提交按钮必须有 loading。
12. 所有页面必须处理 loading、empty、error、permission 基本状态。

## TypeScript 与代码

13. 禁止显式 `any`；未知类型使用 `unknown` 加类型守卫。
14. 禁止在业务代码中绕过类型检查。
15. 禁止超长相对路径；优先使用 project alias。
16. 禁止复制粘贴大段重复逻辑；列表页分页、查询、选择优先使用 `useTable`，且须包含 error 态与重试；分页行为见 `shared/19-list-pagination.md`。
17. `keepAlive` 页面必须 `defineOptions({ name })`，且与路由 `name` 一致。
18. 单文件不超过 400 行；超出须拆 composable 或子组件。
19. 禁止在单文件内堆叠 API、权限、表格、表单、弹窗全部逻辑。
20. 禁止无说明引入新依赖；新增 / 升级依赖须遵守 `shared/20-dependency-governance.md`；修改公共组件 API 须同步所有调用方。

## API 与数据契约

21. 组件内禁止直接 `axios` / `fetch` 调接口。
22. API 必须走 `src/api` 与统一 request wrapper。
23. 表单字段、表格列、DTO 类型必须先读 `contracts/schema.json` 或 generated 类型。
24. 禁止手写与 `src/api/generated` 冲突或重复的 interface。
25. 禁止修改 `src/api/generated`；应修改契约源后重新生成。
26. API 契约变更必须有 generated diff，字段删除、必填变化、枚举变化必须 Review。
27. 未知枚举值必须有 fallback 展示。

## 状态、权限与缓存

28. 登出必须调用 `resetAllStores()` 或等价全局清理。
29. 权限判断不能只依赖前端；前端只做展示与交互收敛。
30. 按钮权限必须使用统一指令或 helper。
31. 敏感信息禁止明文持久化；Token 存储策略按项目安全要求执行。

## 安全

32. 禁止裸用 `v-html`；必须使用 `SafeHtml` / `safeHtml()` 与 DOMPurify 等消毒方案。
33. 禁止提交密钥、私有 Token、内网生产地址。
34. 生产包禁止包含 mock handler、假数据开关、调试面板。
35. 日志与埋点禁止上报密码、完整证件号、未脱敏手机号等敏感数据；生产禁止散落 `console.*`，错误日志格式见 `shared/18-logging-observability.md`。
36. 生产 sourcemap 不得公开暴露在 CDN。

## 样式与可访问性

37. 业务组件禁止硬编码主题色；必须使用设计 Token。
38. UI 可访问性和性能要求见 `shared/07-security-performance.md`。

## 工程门禁

39. 提交前必须运行项目已配置的 lint、type-check、test、build 等门禁。
40. `views` 硬门禁须同时覆盖：`element-plus` / `element-plus/*` import（ESLint）、模板 `<el-*>` 与 EP PascalCase denylist（`ci-scan-views-el-tags.mjs`，CI 勿用 `--allow-empty`）；样板见 `rules/examples/`。
41. `pnpm api:check` 应拦截 schema / generated 类型不一致。
42. 体积门禁、依赖 audit、E2E、发布规则见 `shared/08-quality-gates.md`。
43. Feature Flag 必须有 owner、默认值、创建原因、清理日期。

## AI 生成

44. 写 `views/**` 前必须阅读 Base 源码或 `shared/11-base-components-context.md`；未阅读不得开写。
45. 写字段、表单、表格、API 前必须阅读 `shared/12-schema-ssot.md` 或 `contracts/schema.json`。
46. AI 不得因为示例代码存在 `el-*` 或 `<ElButton>` 就在业务页面继续使用原生 Element Plus。
47. AI 输出前自检见 `shared/10-verification-checklist.md`。
48. 列表页分页、筛选、排序须有单一数据源；筛选或 pageSize 变化须回第一页；列表请求须防竞态；详见 `shared/19-list-pagination.md`。
49. 文件导入 / 导出不得绕过 schema、权限、脱敏与审计；Excel / CSV / JSON / Word 规则见 `shared/14-upload-import-export.md`。
50. 全局错误、路由 chunk 失败、登录过期、白屏恢复不得散落在页面中重复实现；详见 `shared/21-error-recovery.md`。
