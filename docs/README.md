# 企业级治理文档索引

> 与三端 `rules/` **并列**的 monorepo 级资产；业务仓若只 submodule 某一端 `rules/`，须额外复制本目录与 [`scripts/`](../scripts/README.md) 到业务仓或 CI 可访问路径。

## 文档

| 文档 | 用途 |
|---|---|
| [`definition-of-done.md`](definition-of-done.md) | 跨端 DoD（代码 / 契约 / 安全 / 数据 / 可观测 / 发布） |
| [`rule-exception-process.md`](rule-exception-process.md) | 例外与豁免流程 |
| [`codeowners-matrix.md`](codeowners-matrix.md) | 按变更类型的 Review 矩阵 |
| [`supply-chain-baseline.md`](supply-chain-baseline.md) | 供应链强制基线 |
| [`data-classification-matrix.md`](data-classification-matrix.md) | 数据分类分级跨端表 |
| [`slo-alerting-template.md`](slo-alerting-template.md) | 管理端 / 小程序 SLO 与告警 |
| [`dod-maturity-mapping.md`](dod-maturity-mapping.md) | DoD × 采纳 Level 0–3 对照 |
| [`compliance-evidence-log.md`](compliance-evidence-log.md) | 合规证据留痕模板（金融 / 政务） |
| [`monorepo-layout.md`](monorepo-layout.md) | 全栈 monorepo 推荐布局 |

## 脚本

| 脚本 | 用途 |
|---|---|
| [`scripts/check-project-adoption.py`](../scripts/check-project-adoption.py) | 业务仓接入验收 |
| [`examples/ci/supply-chain-required.yml`](../examples/ci/supply-chain-required.yml) | 供应链 Required CI 样板 |

## 业务仓最小落地

```bash
# 复制治理文档（示例）
mkdir -p docs/code-rules-governance
cp docs/definition-of-done.md docs/rule-exception-process.md docs/codeowners-matrix.md docs/code-rules-governance/

# 接入验收
python scripts/check-project-adoption.py --repo . --stack frontend --strict
```

各规则包内链：`web-*/rules/docs/enterprise-governance.md`。
