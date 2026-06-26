# 规则成熟度（前端）

DoD × Level 全栈对照：monorepo [`docs/dod-maturity-mapping.md`](../../../../docs/dod-maturity-mapping.md)。

| 等级 | 最低能力 | 证据 |
|---|---|---|
| Level 0 | 能生成页面 | 人工 review |
| Level 1 | schema、权限、四态、基础门禁 | `lint`、`type-check`、rules validator |
| Level 2 | 契约生成、测试、性能预算、审计展示 | `api:check`、测试、Full eval（E01–E43，P1 ≥32/35）；i18n/实时/富文本 PR 加 Platform Extension E41–E43 |
| Level 3 | 指标、持续治理、定期演练 | Web Vitals 看板、规则版本与复盘记录 |

团队不应只以规则数量判定成熟度；每项能力要有可运行的命令、Owner 和回归证据。
