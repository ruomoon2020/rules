# 全栈 Monorepo 推荐布局

```text
product/
├─ contracts/
│  ├─ openapi.yaml              # SSOT：后端 + 管理端 + 小程序共用
│  └─ openapi.baseline.yaml     # CI diff 基线（契约变更后由 Owner 更新）
├─ web-front/
│  ├─ src/                      # Vue 管理端工程
│  └─ rules/                    # 前端规则包
├─ web-backend/
│  ├─ src/main/java/            # Spring Boot 工程
│  └─ rules/                    # 后端规则包
├─ miniapp/
│  ├─ src/                      # uni-app 小程序工程
│  └─ rules/                    # 小程序规则包（miniapp/rules）
├─ AGENTS.md                    # 可选：索引各端；或各子工程独立 AGENTS
└─ README.md
```

## 契约流

```text
contracts/openapi.yaml
  ├─► 后端：实现 + springdoc 校验 + MockMvc 测试
  ├─► 管理端：openapi-generator / schema.json → src/api/generated
  └─► 小程序：api:gen → src/api/generated + api:check
```

## 规则包路径

| 端 | 规则目录 | Codex 入口 |
|---|---|---|
| 管理端 | `web-front/rules/` | 复制 `codex/AGENTS.md` 到工程根 |
| 后端 | `web-backend/rules/` | 同上 |
| 小程序 | `miniapp/rules/` | 同上 |

Cursor：各工程 `.cursor/rules/*.mdc` 来自对应 `rules/cursor/`。

## 联调字段

见 `web-backend/rules/docs/fullstack-contract.md` 与 `web-front/rules/shared/18-logging-observability.md`。

## 规则包版本

前后端 `rules/VERSION` **独立演进**（例如后端 1.7.x、前端 1.3.x），以各目录 `VERSION` 为准。

## 规则包 CI（本 monorepo）

改 `web-backend/rules/**`、`web-front/rules/**` 或 `miniapp/rules/**` 时，GitHub Actions 运行：

```bash
python web-backend/rules/scripts/validate-rules-package.py
python web-front/rules/scripts/validate-rules-package.py
python miniapp/rules/scripts/validate-rules-package.py
```

Workflow：`.github/workflows/validate-rules-packages.yml`（三端各一条 job）。

成熟后台全栈新增业务：后端 `shared/43` + `docs/business-feature-playbook.md`；管理端 `shared/22` + `docs/business-feature-playbook-frontend.md`；小程序 `shared/18` + `docs/business-feature-playbook-miniapp.md`；evals **B55–B63** / **E32–E40** / **M21–M29**（均建议 9/9）；联调见 `web-backend/rules/docs/fullstack-contract.md`。

## 脚手架

- 后端 Java 样板：`web-backend/rules/examples/scaffold/`
- 后端配置/SQL：`web-backend/rules/examples/config/`、`examples/db/`
- 备份恢复 Runbook：`web-backend/rules/docs/backup-restore-runbook.md`
