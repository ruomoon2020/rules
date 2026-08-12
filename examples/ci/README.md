# CI 样板（monorepo 根）

| 文件 | 复制目标 | 用途 |
|---|---|---|
| [`supply-chain-required.yml`](supply-chain-required.yml) | `.github/workflows/supply-chain-required.yml` | 单锁文件校验 + audit + 固定版本 OWASP / license-checker |
| [`../../common-governance/examples/ci/credential-scan-required.yml`](../../common-governance/examples/ci/credential-scan-required.yml) | `.github/workflows/credential-scan-required.yml` | 凭据泄露扫描（Required） |

发布时该供应链样板同步到 `common-governance/examples/ci/`；各端规则包另有 `web-*/rules/examples/ci/`（业务构建、rules 包校验等）。

详见 [`docs/supply-chain-baseline.md`](../../docs/supply-chain-baseline.md)。
