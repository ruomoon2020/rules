# DoD 与采纳成熟度对照（Level 0–3）

> **DoD SSOT**：[`definition-of-done.md`](definition-of-done.md)。**采纳分层 SSOT**：各端 `rules/docs/rule-maturity-model.md`（后端 Level 0–3 最完整）。本文把二者对齐，避免「Level 到了但 DoD 没过」或「DoD 过了但能力未采纳」。

## 六道门禁 × Level

| DoD 门禁 | Level 0 | Level 1 | Level 2 | Level 3 |
|---|---|---|---|---|
| **1. 代码** | Required：lint / compile / build / 分层 | + 单测 / ArchUnit 或 views 扫描 | + 性能预算自检 | + 平台级架构测试 / 多域门禁 |
| **2. 契约** | OpenAPI SSOT；改 API 须 diff | + 消费端 api:gen / api:check | + 事件契约（若有 MQ） | + 多范式 API 治理（`33`） |
| **3. 安全** | 鉴权 / 输入 / secret scan | + dependency audit；PII 脱敏（`29`） | + 威胁建模；越权测试；供应链 Required | + 密评映射；服务间认证 |
| **4. 数据** | migration validate（若改库） | + 生产数据操作工单（`31`） | + 备份演练；归档策略 | + 冷热分层 / 大规模归档 |
| **5. 可观测** | traceId；无敏感日志 | + 指标 / 错误率观察 | + SLO / 告警 Owner（[`slo-alerting-template.md`](slo-alerting-template.md)） | + 成本 / 容量治理 |
| **6. 发布** | PR 说明 + 可回滚 | + release-checklist 核心项 | + 灰度；事故复盘模板 | + 多环境 / 云原生发版 |

**金融 / 政务**：在 Level 1 基础上，Level 2 前须完成 `27`/`29`/`15` 越权与留存，并启用 [`compliance-evidence-log.md`](compliance-evidence-log.md) 留痕。

---

## 后端（Spring Boot）

| Level | DoD 最低集 | CI 样板 | Evals |
|---|---|---|---|
| **0** | 1–2 全绿；3 secret scan | `backend-ci-required.yml` | P0 B01–B08 |
| **1** | + 3 audit；5 traceId；PR 模板 | + `supply-chain-required.yml` | Smoke ≥17/20 |
| **2** | 1–6 核心项；数据 / 发版清单 | + `backend-ci-optional.yml` | Security + Business B55–B63；发版 Full |
| **3** | + SBOM / 镜像扫描 / 事件契约 | 自定义平台 workflow | Full + Contract |

详见 `web-backend/rules/docs/rule-maturity-model.md`。

---

## 管理端（Vue3）

| Level | DoD 最低集 | CI 样板 | Evals |
|---|---|---|---|
| **0** | 1 全绿；2 schema 一致 | lint + `lint:views-el` | P0 E01–E08 |
| **1** | + 3；5 日志脱敏 | + `api:check` | Smoke 核心 P1 ≥10/12 |
| **2** | + 4–6；性能预算 | + `supply-chain-required.yml` | Full P1 ≥32/35；业务 E32–E40 |
| **3** | + RUM / 看板 / 季度演练 | 自定义 | Full + Platform E41–E43 |

i18n / 实时 / 富文本 PR 另跑 **Platform Extension** E41–E43（Level 2 起建议 Required）。

详见 `web-front/rules/docs/rule-maturity-model.md`。

---

## 小程序（uni-app）

| Level | DoD 最低集 | CI 样板 | Evals |
|---|---|---|---|
| **0** | 1 全绿；request 封装 | lint + build:mp-weixin | P0 M01–M08 |
| **1** | + 2 api:check；+ size:check | + api:check | Smoke 核心 P1 ≥10/12 |
| **2** | + 3 隐私；5 指标；6 发版 | + audit；Resilience 套件 | Full M01–M38；M35–M38 |
| **3** | 多平台 / 多环境隔离 | 自定义 | Full + Security 满配 |

详见 `miniapp/rules/docs/rule-maturity-model.md`。

---

## PR 合并判定（简表）

| 变更类型 | 最低 Level | 必过 DoD 节 |
|---|---|---|
| 普通功能 | 0 | 1；若改 API 加 2 |
| 新依赖 | 1 | 1 + 3 + 供应链 CI |
| 权限 / PII | 1 | 1 + 3 + [`data-classification-matrix.md`](data-classification-matrix.md) |
| DB migration | 1 | 1 + 4 |
| 发版 | 2 | 1–6 全勾；豁免须单 |
| 规则包升级 | 维护者 | validate-rules-package + eval manifest + Full evals |

## 相关

- [`definition-of-done.md`](definition-of-done.md)
- [`rule-exception-process.md`](rule-exception-process.md)
- `web-backend/rules/docs/compliance-cn-mapping.md`
