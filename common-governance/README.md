# Common Governance Package

跨前端、后端、小程序和其他技术栈复用的治理发布包。它约束 DoD、例外、Owner、供应链、数据分级、Git / PR 和发布证据，不替代各端编码规则，也不要求 AI 每次读取全部文档。

## 安装

将整个 `common-governance/` 复制、发布或以独立子模块放到业务仓根：

```text
your-project/
├─ AGENTS.md
├─ rules/                  # 对应技术栈规则包
├─ common-governance/      # 本包
├─ .cursor/rules/
└─ ...
```

项目在根 `AGENTS.md` 或 README 中声明采纳 Level；只有命中合并、发布、例外、数据分级、供应链等任务时才读取对应治理文档。

## 内容

| 入口 | 用途 |
|---|---|
| `docs/definition-of-done.md` | 合并与发布 DoD |
| `docs/rule-exception-process.md` | 门禁例外和到期复查 |
| `docs/codeowners-matrix.md` | 强制 Review 路由 |
| `docs/supply-chain-baseline.md` | 依赖、许可证、SBOM 和漏洞处置 |
| `docs/data-classification-matrix.md` | 跨端数据分级与出站控制 |
| `docs/slo-alerting-template.md` | SLO、告警和演练证据模板 |
| `docs/dod-maturity-mapping.md` | DoD 与 Level 0–3 映射 |
| `docs/adoption-scorecard.md` | 采纳成熟度、Owner 和到期复查 |
| `docs/compliance-evidence-log.md` | 合规证据留痕模板 |
| `docs/branch-protection.md` | Required Checks 与紧急流程 |
| `docs/git-pr-governance.md` | Commit、PR 和本地 hook / CI 边界 |
| `examples/` | PR、commitlint、SECURITY、ADR 与 Required CI 样板 |
| `examples/ci/credential-scan-required.yml` | 凭据泄露扫描 Required Check |
| `examples/ci/supply-chain-required.yml` | 锁文件、依赖漏洞与许可证 Required Check |
| `scripts/check-project-adoption.py` | 业务仓规则与治理接入验收 |

`docs/` 是从 code-rules 根目录 SSOT 生成的发布副本。维护者不得直接修改包内副本，应修改根 `docs/` 后运行同步脚本。

文档中出现的 `web-front/rules/`、`web-backend/rules/`、`miniapp/rules/` 路径是对应技术栈的扩展依据；业务仓未安装该端规则包时可忽略，不应改写治理结论。

## 验证

业务仓验证发布文件与 manifest 的一致性：

```bash
python common-governance/scripts/validate-package.py
```

code-rules 维护者验证副本未漂移：

```bash
python scripts/sync-common-governance.py
```

业务仓强制验收：

```bash
python common-governance/scripts/check-project-adoption.py --repo . --stack frontend --strict --require-governance
```

`--require-governance` 会校验固定资产清单、版本和 SHA-256；只存在同名文件不算通过。SHA-256 用于发现复制或发布漂移，不替代来自可信发布渠道的签名或 release checksum。
