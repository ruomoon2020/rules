# Scripts

## validate-rules-package.py

校验规则包内部一致性（**不**执行 AI evals 对话）。

```bash
# 在 web-backend/rules 目录
python scripts/validate-rules-package.py

# 指定 rules 根目录（业务仓嵌入 rules/ 时）
python rules/scripts/validate-rules-package.py --rules-dir rules
```

### 检查项

| 项 | 说明 |
|---|---|
| VERSION ↔ CHANGELOG | 最新版本一致 |
| evals 计数 | 仅 `prompts.md` 的 `### Bxx` 计条数；`rubric` / `results-template` 对齐 |
| smoke-prompts | **索引**：禁止 `### Bxx`；B 编号须存在于 prompts |
| 套件 | Smoke 核心 P1、Security、Contract 与 `evals/README.md` 一致 |
| 门槛 | 多文件 `40/46`（随 rubric 动态）一致 |
| 硬规则 | `00` 条数与 `cursor/00-project-overview.mdc` 一致 |
| README 清单 | `shared/`、`docs/` 等路径存在（排除 monorepo 外链路径） |
| cursor | `shared/NN-*.md` 引用存在 |

### CI

| 场景 | Workflow |
|---|---|
| 本 monorepo | 仓库根 `.github/workflows/validate-rules-packages.yml` |
| 业务仓 | 复制 `examples/ci/rules-package-validate.yml` |
