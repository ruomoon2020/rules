# Code Rules（全栈 AI 规则）

本仓库包含 Web 前端、后端与小程序 AI 编码规则包，可独立或组合落地到业务项目。各规则包 **VERSION 独立演进**（不必同号），以各目录下 `rules/VERSION` 为准。

| 目录 | 技术栈 | 说明 |
|---|---|---|
| [web-front/rules/](web-front/rules/README.md) | Vue 3 + TypeScript + Element Plus | 前端规则包 |
| [web-backend/rules/](web-backend/rules/README.md) | Spring Boot 3 + MyBatis-Plus + 多数据库 | 后端规则包 |
| [miniapp/rules/](miniapp/rules/README.md) | Vue 3 + TypeScript + uni-app + Vite | 小程序规则包 |

## 这些 README 怎么看

| README | 作用 | 读者 |
|---|---|---|
| 本文件 | 全栈规则包总览、组合部署、前后端协作方式 | 架构 / 项目负责人 / 规则维护者 |
| `web-front/rules/README.md` | 前端规则怎么部署、Codex/Cursor 怎么用、怎么写页面 | 前端团队 / AI |
| `web-backend/rules/README.md` | 后端规则怎么部署、Codex/Cursor 怎么用、怎么写业务接口 | 后端团队 / AI |
| `miniapp/rules/README.md` | 小程序规则怎么部署、登录授权/分包/支付分享怎么约束 | 小程序团队 / AI |

原则：**外层 README 不替代各规则包 README**。真正写代码时，AI 先读对应业务仓的 `AGENTS.md`，再按任务读少量规则。

## 推荐目录结构

### 全栈 monorepo

适合一个仓库同时放前端、后端、契约和规则。

```text
your-monorepo/
├─ contracts/
│  ├─ openapi.yaml
│  └─ openapi.baseline.yaml
├─ web-front/
│  ├─ AGENTS.md
│  ├─ rules/
│  ├─ .cursor/rules/
│  └─ src/
├─ web-backend/
│  ├─ AGENTS.md
│  ├─ rules/
│  ├─ .cursor/rules/
│  └─ src/main/java/
└─ docs/
```

前后端字段、权限码、分页、审计、导入导出、业务模块扩展对齐见：

- `web-backend/rules/docs/fullstack-contract.md`
- `web-front/rules/docs/business-feature-playbook-frontend.md`
- `web-backend/rules/docs/business-feature-playbook.md`

### 前后端分仓

适合前端仓、后端仓独立发布。

```text
frontend-repo/
├─ AGENTS.md
├─ rules/
├─ .cursor/rules/
└─ contracts/ 或 generated API

backend-repo/
├─ AGENTS.md
├─ rules/
├─ .cursor/rules/
└─ contracts/openapi.yaml
```

要求：

1. OpenAPI / schema 有一个明确 SSOT。
2. 前端 `api:gen` 来源与后端契约一致。
3. 两边规则版本可以不同，但 fullstack contract 要由同一 Owner 维护。
4. 发版前至少跑后端 Contract / Business Extension 与前端 schema / build 检查。

## 部署步骤

### 后端规则包

1. 将 `web-backend/rules/` 整包复制或作为 submodule 放入后端仓 `rules/`。
2. 复制 `web-backend/rules/codex/AGENTS.md` 到后端仓根 `AGENTS.md`。
3. 复制 `web-backend/rules/cursor/*.mdc` 到后端仓 `.cursor/rules/`。
4. 按需接入 `examples/` 中的 ArchUnit、Checkstyle、OpenAPI diff、CI 样板。
5. 运行 `python rules/scripts/validate-rules-package.py`。

详细说明见 `web-backend/rules/README.md`。

### 前端规则包

1. 将 `web-front/rules/` 整包复制或作为 submodule 放入前端仓 `rules/`。
2. 复制 `web-front/rules/codex/AGENTS.md` 到前端仓根 `AGENTS.md`。
3. 复制 `web-front/rules/cursor/*.mdc` 到前端仓 `.cursor/rules/`。
4. 接入 `examples/` 中 views 禁 Element Plus、schema check、CI 扫描样板。
5. 运行 `python rules/scripts/validate-rules-package.py`。

详细说明见 `web-front/rules/README.md`。

### 小程序规则包

1. 将 `miniapp/rules/` 整包复制或作为 submodule 放入小程序仓 `rules/`。
2. 复制 `miniapp/rules/codex/AGENTS.md` 到小程序仓根 `AGENTS.md`。
3. 复制 `miniapp/rules/cursor/*.mdc` 到小程序仓 `.cursor/rules/`。
4. 复制 `miniapp/rules/examples/99-project-local.mdc.sample` 到 `.cursor/rules/99-project-local.mdc` 并按项目修改。
5. 接入 lint、type-check、`build:mp-weixin`、api check 和包体积检查。

详细说明见 `miniapp/rules/README.md` 与 `miniapp/rules/docs/onboarding-new-project.md`。

## Codex / Cursor 使用方式

### Codex

Codex 只看业务仓根 `AGENTS.md`。不要让它一次读全部 `shared/`。

推荐提示：

```text
后端：新增 CRM 客户模块，RuoYi-Vue-Plus 二开，按 43 + playbook。
前端：新增 CRM 客户列表页，按 shared/22 + frontend playbook。
全栈：先改 OpenAPI，再后端实现，再前端 api:gen + 页面联调。
公共层：改 common 拦截器，按 43 公共模块例外 + 30 ADR。
```

### Cursor

Cursor 靠 `.cursor/rules/*.mdc` 的 `alwaysApply` 和 `globs` 触发。

建议：

- 只保留概览规则 `alwaysApply: true`。
- 业务模块靠路径 glob 触发。
- 公共层 / generator 由专门边界规则触发。
- 项目路径差异用业务仓 `99-project-local.mdc` 描述。

## 业务仓本地覆盖层

通用规则包无法知道每个项目的真实包名、Base 组件路径、OpenAPI 路径和成熟度目标。每个业务仓建议额外补一层本地配置。

后端 `AGENTS.md` 可追加：

```md
## 本项目约定

- 业务模块路径：`src/main/java/com/acme/modules/{biz}/`
- 成熟后台栈：RuoYi-Vue-Plus 5.x
- OpenAPI：`contracts/openapi.yaml`
- 采纳 Level：1
```

前端 `.cursor/rules/99-project-local.mdc`：复制 `web-front/rules/examples/99-project-local.mdc.sample` 并按项目修改。

后端 `.cursor/rules/99-project-local.mdc`：复制 `web-backend/rules/examples/99-project-local.mdc.sample` 并按项目修改。

小程序 `.cursor/rules/99-project-local.mdc`：复制 `miniapp/rules/examples/99-project-local.mdc.sample` 并按项目修改（目标平台、分包路径、主包预算、登录态与隐私路径）。

本地覆盖层只写项目路径、技术栈、脚本名，不要复制大段 shared 规则。

## 怎么写真实业务

### 成熟后台新增 CRUD

1. 后端先确认是否复用平台用户、权限、字典、日志、文件、任务、租户、数据权限、CodeGen。
2. 先改 `contracts/openapi.yaml`。
3. 后端实现 Controller / Service / Mapper / 权限 / 审计 / 数据权限。
4. 前端执行 schema / api 生成，使用 Base 组件实现列表、表单、详情。
5. 菜单、路由、按钮权限码三端一致。
6. 导入导出、树表、主子表按前后端 playbook 检查。
7. 跑后端 Business Extension evals 与前端 lint / type-check / build。

关键文档：

- `web-backend/rules/shared/43-business-module-extension.md`
- `web-backend/rules/docs/business-feature-playbook.md`
- `web-front/rules/shared/22-business-module-extension.md`
- `web-front/rules/docs/business-feature-playbook-frontend.md`
- `web-backend/rules/docs/fullstack-contract.md`

### 普通接口 + 页面

1. OpenAPI 先行。
2. 后端不返回 Entity，前端不手写 generated 类型。
3. 分页字段、错误码、traceId、权限码一致。
4. 前端列表四态、删除末条回退页码、错误恢复完整。
5. 后端跑 `mvn verify`，前端跑 `pnpm lint` / `type-check` / `build`。

## 验证与 CI

| 范围 | 命令 / 套件 |
|---|---|
| 后端规则包 | `python web-backend/rules/scripts/validate-rules-package.py` |
| 前端规则包 | `python web-front/rules/scripts/validate-rules-package.py` |
| 小程序规则包 | `python miniapp/rules/scripts/validate-rules-package.py` |
| 后端业务仓 | `mvn verify` 或 `./gradlew check` |
| 前端业务仓 | `pnpm lint`、`pnpm type-check`、`pnpm build` |
| 小程序业务仓 | `pnpm lint`、`pnpm type-check`、`pnpm build:mp-weixin`、`pnpm api:check` |
| 后端成熟业务扩展 | Business Extension B55–B63（建议 9/9） |
| 前端成熟业务扩展 | Business Extension E32–E40（建议 9/9） |
| 前端发版 / 大改规则 | Smoke / Full evals（E01–E40，P1 ≥29/32） |
| 全栈契约 | OpenAPI diff + 前端 api:gen / api:check |

本仓库 CI：PR 改任一端 `rules/**` 时运行对应 `validate-rules-package.py`（含 miniapp），见 `.github/workflows/validate-rules-packages.yml`。

## 业务仓落地 Checklist

把规则包复制到真实项目后，按下面顺序检查。建议由项目 Owner 在首个 PR 中一次性完成。

### 必做

- [ ] 后端仓存在 `rules/`、根 `AGENTS.md`、`.cursor/rules/*.mdc`。
- [ ] 前端仓存在 `rules/`、根 `AGENTS.md`、`.cursor/rules/*.mdc`。
- [ ] 小程序仓存在 `rules/`、根 `AGENTS.md`、`.cursor/rules/*.mdc`。
- [ ] 根 `AGENTS.md` 中的路径能解析到 `rules/shared/...`、`rules/codex/...`。
- [ ] Cursor 只保留概览类规则 `alwaysApply: true`；不要把所有 `.mdc` 都设为 alwaysApply。
- [ ] 已补业务仓本地覆盖层：真实包名、业务模块路径、Base 组件路径、OpenAPI / schema 路径、采纳 Level。
- [ ] OpenAPI / schema 的 SSOT 已写清楚，前后端不各维护一份字段定义。
- [ ] 后端接入 `mvn verify` / `./gradlew check`，前端接入 `pnpm lint`、`type-check`、`build`。
- [ ] 小程序接入 `pnpm lint`、`type-check`、`build:mp-weixin`、api check 和包体积检查。
- [ ] 业务 PR 模板已复制或等价接入，能覆盖契约、权限、数据权限、审计、导入导出和回滚。
- [ ] 成熟后台新增业务时，后端跑 Business Extension B55–B63、前端跑 E32–E40（均建议 9/9）。

### 推荐

- [ ] 后端接入 ArchUnit、Checkstyle、OpenAPI diff、Flyway validate。
- [ ] 前端接入 schema / api check、views 禁 Element Plus 扫描。
- [ ] CODEOWNERS 覆盖契约、DB migration、安全、CI、规则包。
- [ ] 新项目声明采纳 Level：前端 / 后端至少 Level 0，成熟后台二开建议 Level 1。
- [ ] 发版前跑后端 Full evals；前端规则大改后跑 Smoke / Full。

## 常见误用

| 误用 | 后果 | 正确做法 |
|---|---|---|
| 只复制 `AGENTS.md`，不复制 `rules/` | AI 读不到 shared 全文，容易幻觉补规则 | 整包复制 `rules/`，或保证路径可解析 |
| 所有 `.mdc` 都 `alwaysApply: true` | 上下文膨胀，规则互相干扰 | 只让概览 alwaysApply，其余靠 globs |
| 让 AI 一次读完全部 shared | 慢、贵、容易丢重点 | 按任务包 / 路径触发读取 |
| 业务仓不写本地路径 | Cursor / Codex 只能猜包名和目录 | 加 `99-project-local.mdc` 与本项目约定 |
| 前后端各写字段 | 字段、权限码、分页、错误码漂移 | OpenAPI / schema 作为 SSOT |
| CodeGen 后直接上线 | 漏权限、审计、数据权限、测试 | 按前后端 playbook 补齐 |
| 改 common / system 做单业务 | 平台层污染，后续升级困难 | 业务进业务模块；平台变更走 ADR |

## 快速开始

| 场景 | 文档 |
|---|---|
| 新建前端项目 | `web-front/rules/README.md` |
| 新建后端项目 | `web-backend/rules/docs/onboarding-new-project.md` |
| 新建小程序项目 | `miniapp/rules/docs/onboarding-new-project.md` |
| 共享 API 契约 | `contracts/openapi.yaml` + `openapi.baseline.yaml`（CI diff） |
| 全栈 monorepo 布局 | `docs/monorepo-layout.md` |
| 规则包自动校验 | PR 改任一侧 `rules/**` 时运行 `validate-rules-package.py`（见 `.github/workflows/validate-rules-packages.yml`） |
| 后端 Java 样板 | `web-backend/rules/examples/scaffold/` |

## 维护规则包

维护建议：

1. 不要把所有规则合成一个大文件。
2. 不要把所有 `.mdc` 设成 `alwaysApply: true`。
3. 新增 shared 编号文件时，同步 README、AGENTS、Cursor、evals、release checklist。
4. 改 eval 数量时，同步 prompts、rubric、results-template、smoke、README 和校验脚本。
5. 外层 README 只写全栈部署和协作，不复制前后端规则全文。
