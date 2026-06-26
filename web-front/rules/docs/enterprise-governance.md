# 企业级治理（业务仓落地）

> 本目录 `rules/` 侧重 **AI 编码规则**。组织级 DoD、豁免、Owner 矩阵、供应链与数据分级在 **code-rules monorepo 根**（与 `web-front/` 并列的 `docs/`、`scripts/`）。

## 仅 submodule 本规则包时

业务仓若只有 `rules/`（无 monorepo 根 `docs/`），请从上游仓库额外复制：

| 复制源（monorepo） | 建议目标（业务仓） |
|---|---|
| `docs/definition-of-done.md` 等治理文档 | `docs/code-rules-governance/` |
| `scripts/check-project-adoption.py` | `scripts/` 或 CI 工具目录 |

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

全索引：`docs/README.md`（monorepo 根）。

## 验收

```bash
python scripts/check-project-adoption.py --repo /path/to/your-app --stack frontend --strict
```

发版与 PR 合并标准见 DoD；超预算或跳过门禁须走豁免流程。
