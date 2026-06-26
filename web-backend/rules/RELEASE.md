# 规则包发布前 Checklist

> 维护者改 `rules/**` 的完整清单见 `docs/contributing-rules-package.md`。

## 必做

- [ ] 更新 `VERSION`、`CHANGELOG.md`
- [ ] 核对 `README.md` 文件清单与磁盘一致（含 `docs/onboarding-new-project.md`）
- [ ] 核对 `contracts/openapi.yaml`（monorepo 根）与 `05-openapi-contract` 描述一致
- [ ] 若契约有变更：确认 `openapi.baseline.yaml` 已更新或 PR 说明 diff 策略
- [ ] 核对 `codex/AGENTS.md` 与 `shared/` 存在性
- [ ] 核对 `cursor/*.mdc` 中 `rules/shared/...` 引用有效
- [ ] 核对 `examples/checkstyle`、`examples/ci`、`examples/scripts` 样板存在且 README 有入口
- [ ] 核对 `evals` 用例数与门槛（**计数 SSOT**：`prompts.md` + `rubric.md` + `results-template.md`；`smoke-prompts.md` **只校验 B 编号覆盖，不计入条数**）
- [ ] 运行 `python scripts/validate-rules-package.py` 通过
- [ ] 若改核心 P1 列表：同步 `evals/smoke-prompts.md` 与 `evals/README.md` 套件表
- [ ] 改 eval 主题后：运行 monorepo `python scripts/generate-eval-topic-manifest.py --rules-dir web-backend/rules` 并提交 `evals/topic-manifest.yaml`

## 大版本 / 改 Hard Rules 或 ArchUnit 时追加

- [ ] 跑 **Full** evals：`evals/prompts.md` B01–B63，P0 **8/8**、P1 **≥49/55**（日常可用 Smoke，见 `evals/README.md`）
- [ ] 多库 CI：至少 MySQL + PostgreSQL 迁移或 Testcontainers 通过

## 不要做

- [ ] 不要把 `docs/migration-from-template.md` 加入 Codex/Cursor 默认读取
- [ ] 生产禁止 `ddl-auto=update`（规则与代码评审双重约束）
