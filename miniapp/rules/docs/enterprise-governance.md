# 企业级治理（业务仓落地）

> 本目录 `rules/` 侧重 **AI 编码规则**。组织级 DoD、豁免、Owner 矩阵在 **code-rules monorepo 根** `docs/`。

## 仅 submodule 本规则包时

从上游复制 monorepo `docs/` 治理文档与 `scripts/check-project-adoption.py`。全索引：`docs/README.md`。

## 文档清单

| 主题 | monorepo 路径 |
|---|---|
| Definition of Done | `docs/definition-of-done.md` |
| 豁免流程 | `docs/rule-exception-process.md` |
| CODEOWNERS 矩阵 | `docs/codeowners-matrix.md` |
| 供应链基线 | `docs/supply-chain-baseline.md` |
| 数据分级 | `docs/data-classification-matrix.md` |
| SLO / 告警 | `docs/slo-alerting-template.md`（含小程序指标） |
| DoD × Level | `docs/dod-maturity-mapping.md` |
| 合规证据留痕 | `docs/compliance-evidence-log.md` |

小程序指标细则另见 `docs/observability-metrics.md`。

## 验收

```bash
python scripts/check-project-adoption.py --repo /path/to/miniapp --stack miniapp --strict
```
