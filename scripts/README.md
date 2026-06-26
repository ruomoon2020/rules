# Monorepo 脚本

| 脚本 | 用途 |
|---|---|
| [`generate-eval-topic-manifest.py`](generate-eval-topic-manifest.py) | 从 `evals/prompts.md` + `rubric.md` 生成 `topic-manifest.yaml` |
| [`eval_topic_manifest.py`](eval_topic_manifest.py) | 共享库：manifest 生成与校验（被各端 validator 引用） |
| [`check-project-adoption.py`](check-project-adoption.py) | **业务仓**接入验收：AGENTS、rules、cursor、契约、CI 脚本 |

CI 自测：`examples/adoption-fixture/frontend/` + `python -m unittest discover -s scripts/tests`。

## 业务仓接入检查

```bash
# 前端仓
python scripts/check-project-adoption.py --repo /path/to/frontend --stack frontend

# 后端仓（严格：CODEOWNERS + PR 模板必填）
python scripts/check-project-adoption.py --repo /path/to/backend --stack backend --strict

# 小程序
python scripts/check-project-adoption.py --repo /path/to/miniapp --stack miniapp
```

## Eval topic manifest

改 `evals/prompts.md` 或 `rubric.md` 后：

```bash
python scripts/generate-eval-topic-manifest.py --all
python web-front/rules/scripts/validate-rules-package.py
```

依赖：`pip install pyyaml`（CI 已装 Python 3.12；若缺 PyYAML 见 workflow）。

## 治理文档

见 [`docs/definition-of-done.md`](../docs/definition-of-done.md) 与 [`docs/rule-exception-process.md`](../docs/rule-exception-process.md)。
