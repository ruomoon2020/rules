# 企业级治理（业务仓落地）

> 本目录 `rules/` 侧重 **AI 编码规则**。组织级 DoD、豁免、Owner 矩阵、供应链与数据分级在 **code-rules monorepo 根**。

## 仅 submodule 本规则包时

从上游仓库复制 `docs/*.md`（治理 6 件套）与 `scripts/check-project-adoption.py` 到业务仓。详见 monorepo `docs/README.md`。

## 文档清单

| 主题 | monorepo 路径 |
|---|---|
| Definition of Done | `docs/definition-of-done.md` |
| 豁免流程 | `docs/rule-exception-process.md` |
| CODEOWNERS 矩阵 | `docs/codeowners-matrix.md` |
| 供应链基线 | `docs/supply-chain-baseline.md` |
| 数据分级 | `docs/data-classification-matrix.md` |
| SLO / 告警 | `docs/slo-alerting-template.md` |
| DoD × Level | `docs/dod-maturity-mapping.md` |
| 合规证据留痕 | `docs/compliance-evidence-log.md` |

后端 SLO 细则另见本包 `shared/32-service-reliability.md`、`docs/release-checklist.md`。

## 验收

```bash
python scripts/check-project-adoption.py --repo /path/to/backend --stack backend --strict
```
