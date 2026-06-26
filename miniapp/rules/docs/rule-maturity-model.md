# 规则成熟度模型（小程序）

团队声明目标 Level，evals 与 CI 按 Level 勾选，避免「规则包全有、业务仓全没」。

| Level | 适用 | 最低要求 |
|---|---|---|
| **0 — 基线** | 新项目首迭代 | `00` + `05`/`06` + `07`；lint、type-check、build:mp-weixin；request 封装 |
| **1 — 标准** | 上线前 / 对外小程序 | Level 0 + `09`/`14`/`21`/`20`；api:check；size:check；Smoke evals P0 8/8 |
| **2 — 企业** | 支付 / 多分包 / 多环境 | Level 1 + `18` playbook；Full M01–M38；PR 模板；`22`/`23`/`25`；Security 5/5 + Resilience 4/4；`docs/observability-metrics.md` |

在 `99-project-local.mdc` 写明：`采纳 Level: 0 | 1 | 2`。
