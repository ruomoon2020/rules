# 全栈 Monorepo 推荐布局

```text
product/
├─ contracts/
│  └─ openapi.yaml              # SSOT：前后端共用
├─ web-front/
│  ├─ src/                      # Vue 工程
│  └─ rules/                    # 前端规则包（或 git submodule rules/web-front/rules）
├─ web-backend/
│  ├─ src/main/java/            # Spring Boot 工程
│  └─ rules/                    # 后端规则包
├─ AGENTS.md                    # 可选：索引前后端；或各子工程独立 AGENTS
└─ README.md
```

## 契约流

```text
contracts/openapi.yaml
  ├─► 后端：实现 + springdoc 校验 + MockMvc 测试
  └─► 前端：openapi-generator / schema.json → src/api/generated
```

## 规则包路径

| 端 | 规则目录 | Codex 入口 |
|---|---|---|
| 前端 | `web-front/rules/` | 复制 `codex/AGENTS.md` 到前端根或 monorepo 根 |
| 后端 | `web-backend/rules/` | 同上 |

Cursor：各工程 `.cursor/rules/*.mdc` 来自对应 `rules/cursor/`。

## 联调字段

见 `web-backend/rules/docs/fullstack-contract.md` 与 `web-front/rules/shared/18-logging-observability.md`。

## 脚手架

- 后端 Java 样板：`web-backend/rules/examples/scaffold/`
- 后端配置/SQL：`web-backend/rules/examples/config/`、`examples/db/`
