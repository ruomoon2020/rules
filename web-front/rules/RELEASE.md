# 规则包发布前 Checklist

维护者发版 `rules/` 时按序执行。

## 必做

- [ ] 更新 `VERSION`
- [ ] 更新 `CHANGELOG.md`（含破坏性变更说明）
- [ ] 运行 `node rules/examples/run-ci-scan-fixtures.mjs`（全部通过）
- [ ] 核对 `README.md`「完整文件清单」与磁盘文件一致
- [ ] 核对 `codex/AGENTS.md` 任务表与 `shared/` 文件存在性一致
- [ ] 核对 `cursor/*.mdc` 中的 `rules/shared/...` 引用均存在，且 frontmatter `globs` 能覆盖目标场景
- [ ] 核对 `README.md`、`evals/README.md`、`evals/rubric.md`、`evals/prompts.md` 的用例数量与通过门槛一致

## 大版本 / 改 ci-scan 或 Hard Rules 时追加

- [ ] 在测试业务仓跑 `evals/prompts.md` **E01–E31**，P0 **8/8**、P1 **至少 21/23**
- [ ] 通知业务仓同步 `rules/` 或升级 submodule 版本

## 不要做

- [ ] 不要把 `docs/migration-from-template.md` 加入 Codex/Cursor 默认读取路径
- [ ] 不要在业务仓 CI 的 `lint:views-el` 上使用 `--allow-empty`
