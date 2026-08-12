# Monorepo 脚本

| 脚本 | 用途 |
|---|---|
| [`generate-eval-topic-manifest.py`](generate-eval-topic-manifest.py) | 从 `evals/prompts.md` + `rubric.md` 生成 `topic-manifest.yaml` |
| [`eval_topic_manifest.py`](eval_topic_manifest.py) | 共享库：manifest 生成与校验（被各端 validator 引用） |
| [`check-project-adoption.py`](check-project-adoption.py) | **业务仓**接入验收：AGENTS、rules、cursor、契约；后端接受 `pom.xml` 或 `gradlew` + `build.gradle*` |
| [`sync-common-governance.py`](sync-common-governance.py) | 从根 `docs/` 生成 / 校验 `common-governance/` 发布包，防双 SSOT 漂移 |
| [`validate-repository.py`](validate-repository.py) | 校验维护文件尾随空白、Markdown 本地链接和 YAML 语法 |

CI 自测：`examples/adoption-fixture/frontend/`、`examples/adoption-fixture/backend-gradle/` + `python -m unittest discover -s scripts/tests`。

## 业务仓接入检查

```bash
# 前端仓
python scripts/check-project-adoption.py --repo /path/to/frontend --stack frontend

# 后端仓（严格：CODEOWNERS + PR 模板必填）
python scripts/check-project-adoption.py --repo /path/to/backend --stack backend --strict

# Gradle 后端自测 fixture
python scripts/check-project-adoption.py --repo examples/adoption-fixture/backend-gradle --stack backend

# 小程序
python scripts/check-project-adoption.py --repo /path/to/miniapp --stack miniapp

# 企业项目：同时强制 common governance
python common-governance/scripts/check-project-adoption.py --repo /path/to/frontend --stack frontend --strict --require-governance

# 维护者：校验 common governance 与根 docs 一致
python scripts/sync-common-governance.py
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
