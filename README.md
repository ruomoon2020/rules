# Code Rules（全栈 AI 规则）

本仓库包含前端与后端 AI 编码规则包，可独立或组合落地到业务项目。前后端规则包 **VERSION 独立演进**（不必同号），以各目录下 `rules/VERSION` 为准。

| 目录 | 技术栈 | 说明 |
|---|---|---|
| [web-front/rules/](web-front/rules/README.md) | Vue 3 + TypeScript + Element Plus | 前端规则包 |
| [web-backend/rules/](web-backend/rules/README.md) | Spring Boot 3 + MyBatis-Plus + 多数据库 | 后端规则包 |

## 全栈契约（推荐 monorepo）

```text
contracts/openapi.yaml    # 或 openapi + 代码生成
web-front/                # 前端工程 + rules/
web-backend/                # Spring Boot 工程 + rules/
```

前后端字段对齐见 `web-backend/rules/docs/fullstack-contract.md`。

## 快速开始

| 场景 | 文档 |
|---|---|
| 新建前端项目 | `web-front/rules/README.md` |
| 新建后端项目 | `web-backend/rules/docs/onboarding-new-project.md` |
| 共享 API 契约 | `contracts/openapi.yaml` + `openapi.baseline.yaml`（CI diff） |
| 全栈 monorepo 布局 | `docs/monorepo-layout.md` |
| 规则包自动校验 | PR 改任一侧 `rules/**` 时运行 `validate-rules-package.py`（见 `.github/workflows/validate-rules-packages.yml`） |
| 后端 Java 样板 | `web-backend/rules/examples/scaffold/` |
