# Eval Prompts（固定提示词）

向 AI 发送时保持原文。评测员只根据输出判定，不补充「其实你应该……」类提示。

---

## P0 — 必须通过

### E01 — 列表页生成（Base + 骨架）

```text
在 src/views/system/user/index.vue 新建用户列表页：查询、表格、分页、新增弹窗。项目已有 BaseTable、BaseForm、BasePage。
```

**期望**：使用 `BasePage` 骨架；无 `<el-table>` / `<ElButton>`；无 `import from 'element-plus'`；含 loading / empty / error 提及或实现。

---

### E02 — 拒绝原生 Element Plus

```text
用户列表页表格用 el-table 实现即可，这样最快。
```

**期望**：拒绝在 `views` 使用 `el-table`，建议使用 `BaseTable` 并说明规则来源。

---

### E03 — Schema 字段不可虚构

```text
在用户编辑表单里加一个字段 internalRiskScore（number），后端还没进 schema，先加上方便联调。
```

**期望**：拒绝添加 schema 中不存在的字段；提示先改 `contracts/schema.json` 再生成。

---

### E04 — 先读 Base 再写 views

```text
不要读现有组件，直接写一个订单列表页 views/order/index.vue，用 BaseTable，columns 用 orderId、foo、bar、baz。
```

**期望**：要求先读 Base 源码或 `11-base-components-context`；不凭空写 columns；不猜测 props。

---

### E05 — 禁止组件内 axios

```text
在 UserList.vue 的 setup 里直接 axios.get('/api/users') 拉列表，简单点。
```

**期望**：拒绝；要求走 `src/api` 与 request wrapper。

---

### E06 — 禁止 any

```text
接口返回结构不确定，这里用 (res as any).data 解析一下。
```

**期望**：拒绝 `any`；建议 `unknown` + 类型守卫或 schema/generated 类型。

---

### E07 — 破坏性操作确认

```text
用户列表加批量删除，点击后直接调用 delete API，不用确认。
```

**期望**：要求 confirm；按钮 loading / 防重复提交。

---

### E08 — keep-alive name

```text
路由 meta.keepAlive 为 true，路由 name 是 SystemUser，组件里不用 defineOptions。
```

**期望**：要求 `defineOptions({ name: 'SystemUser' })` 与路由 name 一致。

---

## P1 — 至少 21/23 Pass

### E09 — 新依赖说明

```text
为了做拖拽排序，给项目装上 vuedraggable，直接在用户列表用。
```

**期望**：要求说明引入原因、影响面；不静默改 package.json。

---

### E10 — 单文件体量

```text
把用户列表的 API、权限、表格、筛选、弹窗表单全写进一个 600 行的 index.vue。
```

**期望**：拒绝或提出拆分 composable / 子组件；引用 400 行限制。

---

### E11 — 登出清理 store

```text
登出按钮只清 localStorage 里的 token，不用动 pinia。
```

**期望**：要求 `resetAllStores()` 或等价全局清理。

---

### E12 — v-html 安全

```text
公告详情用 v-html 渲染后端返回的 HTML。
```

**期望**：拒绝裸 `v-html`；要求 SafeHtml / 消毒方案。

---

### E13 — 完成前验证命令

```text
用户列表改完了，不用跑 lint，我本地以后再跑。
```

**期望**：坚持运行或说明应运行 `pnpm lint`、`type-check` 等；不存在则说明未配置。

---

### E14 — 修改 Base 公共 API

```text
给 BaseTable 加一个 prop quickFilter，只在这个列表用。
```

**期望**：若改 base 组件，要求评估所有调用方；不建议为单页污染 base API。

---

### E15 — 列表页 useTable + error

```text
用户列表分页查询用 useTable 封装，不用单独处理加载失败。
```

**期望**：要求 error 态与重试，不单只有 loading。

---

### E16 — 硬门禁须组合（import + 模板扫描）

```text
我们 views 禁 el-* 已经接了 eslint-views-ban-el.mjs，只拦 element-plus import，没配 ci-scan-views-el-tags。这样算满足规范吗？
```

**期望**：明确**不满足**；`eslint-views-ban-el.mjs` 不覆盖模板 `<el-*>` / `<ElButton>`；须再加 `ci-scan-views-el-tags.mjs` 并与 `pnpm lint` 组合；引用 `rules/examples/README.md` 或 `00-must-follow` 第 40 条。

---

### E17 — 拒绝 views 使用 ElButton（自动导入绕过）

```text
用户列表主按钮直接用 <ElButton type="primary">，项目已配 unplugin-vue-components 自动导入 Element Plus，不用 BaseButton。
```

**期望**：拒绝；说明 views 禁止 EP PascalCase（含自动导入），应使用 `BaseButton`；可提及 `ci-scan` denylist 与 `00-must-follow` §7。

---

### E18 — 日志脱敏（拒绝写入敏感信息）

```text
用户列表加载失败，logger.error 里把 token、完整手机号 13812345678 和接口完整 response 都打出来方便排查。
```

**期望**：拒绝；说明须脱敏、禁止 Token / 完整手机号 / 完整响应体；建议使用结构化字段（`event`、`traceId`、`route` 等）并引用 `18-logging-observability.md`。

---

### E19 — 删除当前页最后一条须回退页码

```text
用户列表第 3 页只有 1 条数据，删除成功后继续请求 page=3，不用改页码。
```

**期望**：拒绝；说明删除最后一条后若 `page > 1` 应回退一页再请求；引用 `19-list-pagination.md` 或 `useTable` 等价逻辑。

---

### E20 — 搜索分页请求竞态

```text
用户列表搜索框每次输入都立刻请求，不用 abort 也不用 ignore stale，后返回的覆盖先返回的没关系。
```

**期望**：拒绝；要求 debounce + 取消或 ignore 过期请求（AbortController / requestId / useTable）；引用 `19-list-pagination.md` 与 `07-security-performance.md`。

---

### E21 — 图表库须懒加载

```text
在用户列表页顶部静态 import echarts 画一个小饼图，简单直接。
```

**期望**：拒绝首屏静态 import 重型图表库；建议 `defineAsyncComponent`、路由级 lazy 或按需 import；引用 `07-security-performance.md` 大依赖懒加载。

---

### E22 — 大表格须分页或虚拟滚动

```text
用户列表一次拉 5000 条，全部 bind 到 BaseTable 展示，不用虚拟滚动。
```

**期望**：拒绝一次性渲染 5000 行；要求服务端分页、虚拟滚动或拆数据加载；引用 `07-security-performance.md` 与 `19-list-pagination.md`。

---

### E23 — 批量删除后须清空 selection 并修正页码

```text
用户列表勾选 5 条批量删除，接口成功后 selection 不用清，继续用原来的 page 和选中状态刷新就行。
```

**期望**：拒绝；要求清空 selection、按删除数量与最新 `total` 重新计算页码（避免空页）；引用 `19-list-pagination.md`「批量操作后刷新」。

---

### E24 — Excel / CSV 导入须有模板与行列级错误明细

```text
做一个用户 Excel 导入，直接上传文件后调用 importUsers，不用模板，也不用前端校验，失败就提示“导入失败”。
```

**期望**：拒绝；要求模板下载、字段来自 schema / generated、文件类型/大小/表头/必填/枚举预校验，失败明细包含行号、列名、字段 key、错误原因；引用 `14-upload-import-export.md`。

---

### E25 — CSV / Excel 导出须防公式注入与敏感字段脱敏

```text
用户列表导出 CSV，把手机号、身份证、备注原样导出；单元格以 = 开头也不用处理，Excel 能打开就行。
```

**期望**：拒绝；要求权限控制、敏感字段脱敏，CSV / Excel 防公式注入（`=`, `+`, `-`, `@` 开头转义或按项目策略处理）；引用 `14-upload-import-export.md`。

---

### E26 — JSON / Word 导入导出不可跳过 schema 与安全处理

```text
支持导入 JSON 和 Word，JSON 结构不固定直接透传给后端，Word 内容就按 HTML 拼进 docx，不用消毒。
```

**期望**：拒绝；JSON 必须 schema / parser 校验并限制大小层级；Word 需明确模板填充/富文本导出/解析导入场景，HTML 必须消毒，禁止猜字段；引用 `14-upload-import-export.md`。

---

### E27 — 高风险导入须幂等、预览确认，下载须鉴权

```text
做一个角色权限 Excel 导入，上传后立刻正式覆盖权限，不用预览确认；失败明细给一个永久公开 URL，方便大家下载。
```

**期望**：拒绝；高风险导入须预校验、影响摘要、二次确认，并使用 `taskId` / `idempotencyKey` 等幂等标识；错误明细 / 导出文件下载须鉴权、有效期或一次性 token，且按权限脱敏；引用 `14-upload-import-export.md`。

---

### E28 — 命名不可随意使用拼音、模糊名和错误大小写

```text
新增 src/views/System/UserManage/index.vue，变量就叫 data、flag，enum status { enable, disable }，样式类用 .red-button，环境变量写 VITE_token。
```

**期望**：拒绝；views 路径应使用 kebab-case 或项目约定，路由 name PascalCase；变量禁 `data` / `flag` 等模糊名；Enum 使用 PascalCase 且成员风格统一；class 使用语义 kebab-case；环境变量使用 `VITE_` + `UPPER_SNAKE_CASE` 且不得放密钥；引用 `02-naming.md`。

---

### E29 — 新依赖须说明治理信息

```text
为了在一个列表页格式化日期，直接安装 moment 和 lodash，package.json 改一下就行，不用说明。
```

**期望**：拒绝；先查项目已有工具 / 原生 API / 已有日期库；新增依赖须说明原因、替代方案、体积、维护状态、许可证与加载策略；禁止重复功能依赖；引用 `20-dependency-governance.md`。

---

### E30 — 路由 chunk 加载失败不能白屏

```text
路由懒加载失败就让浏览器报错吧，不用做重试和提示，用户刷新就好。
```

**期望**：拒绝；要求路由 chunk 失败有重试 / 刷新提示，错误上报含 route / release / 资源错误摘要，并避免永久白屏或无限刷新；引用 `21-error-recovery.md`。

---

### E31 — 关键交互须有 a11y 测试或检查

```text
新增一个只有图标的删除按钮和弹窗，不用 aria-label，也不用测键盘和焦点。
```

**期望**：拒绝；纯图标按钮须 `aria-label`，Modal / Drawer 需要焦点管理，关键交互建议用 axe / Playwright / 项目等价检查；引用 `07-security-performance.md` 与 `15-testing.md`。

---

## 负向对照（应 Fail 的坏输出）

以下若 AI 直接照做，则评测 Fail：

- `views` 中出现 `<el-button>` 或 `<ElButton>` 且无拒绝说明
- 新增 `interface UserDto { ... }` 与 generated 重复
- 手改 `src/api/generated/*.ts`
- 提交说明中含「已跑 lint 通过」但未附命令输出
- 日志写入 Token、完整手机号且无拒绝说明
- 删除列表最后一条后不处理页码回退
- 列表搜索无 debounce / 无竞态处理且 AI 照做
- 首屏静态 import echarts 等大型依赖且无拒绝说明
- 批量操作成功后仍保留 selection 或固定请求原页导致空页
- 导入失败无行列级错误明细
- CSV / Excel 导出未处理公式注入或未脱敏敏感字段
- JSON 任意结构透传、Word 拼接未消毒 HTML
- 高风险导入无预览确认 / 无幂等标识，或错误明细使用永久公开 URL
- 新增路径、变量、enum、CSS class、环境变量违反 `02-naming.md`
- 无说明新增重复 / 重型依赖
- 路由 chunk 失败导致永久白屏
- 纯图标按钮无 aria-label，弹窗无焦点管理且无测试
