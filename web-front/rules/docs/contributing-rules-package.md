# 规则包变更治理（维护者）

> 修改 `web-front/rules/**` 时适用。

## 硬变更清单

- [ ] `VERSION`、`CHANGELOG.md`
- [ ] `README.md` 文件清单与磁盘一致
- [ ] `codex/AGENTS.md`、`cursor/*.mdc` 引用有效
- [ ] `evals/prompts.md`、`evals/rubric.md`、`evals/results-template.md` **仅此三文件**按 `### Exx` 计数
- [ ] `evals/smoke-prompts.md`：**只校验 E 编号覆盖**，禁止 `### Exx` 标题
- [ ] `evals/README.md` 回归套件表与 smoke 一致
- [ ] `RELEASE.md`
- [ ] `node examples/run-ci-scan-fixtures.mjs` 通过
- [ ] `python scripts/validate-rules-package.py` 通过

## Evals 计数约定

| 文件 | 计入提示词条数 |
|---|---|
| `evals/prompts.md` | **是**（SSOT） |
| `evals/rubric.md` | 是 |
| `evals/results-template.md` | 是 |
| `evals/smoke-prompts.md` | **否**（套件索引） |

## 发版

见 `RELEASE.md`；大版本须跑 **Full** evals E01–E31。
