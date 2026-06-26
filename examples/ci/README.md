# CI 样板（monorepo 根）

| 文件 | 复制目标 | 用途 |
|---|---|---|
| [`supply-chain-required.yml`](supply-chain-required.yml) | `.github/workflows/supply-chain-required.yml` | audit + OWASP + license-checker（Required 供应链） |

各端规则包另有 `web-*/rules/examples/ci/`（业务构建、rules 包校验等）。

详见 [`docs/supply-chain-baseline.md`](../docs/supply-chain-baseline.md)。
