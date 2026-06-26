# 新项目接入（前端）

1. 复制完整 `rules/`，根 `AGENTS.md` 与 `.cursor/rules/`；不要只复制 `.mdc` 而遗漏 shared。
2. 在 `99-project-local.mdc` 写明 views、Base 组件、generated、schema、布局目录和项目脚本。
3. 设定 OpenAPI / schema 的唯一来源，接入 `schema:sync`、`api:gen`、`api:check`（按项目实际脚本）。
4. 确认菜单、路由、按钮权限、字典和后端鉴权的映射；前端权限只改善体验。
5. 接入 `lint`、`type-check`、`test`、`build` 与 rules validator；发版跑 Full eval（E01–E43，P1 ≥32/35）。

全栈字段、发布顺序与业务扩展见 `docs/fullstack-contract.md`、`docs/business-feature-playbook-frontend.md`。

企业级 DoD、豁免、接入验收见 monorepo `docs/definition-of-done.md` 与本包 `docs/enterprise-governance.md`；可执行 `scripts/check-project-adoption.py --stack frontend`。
