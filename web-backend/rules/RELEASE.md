# 规则包发布前 Checklist

## 必做

- [ ] 更新 `VERSION`、`CHANGELOG.md`
- [ ] 核对 `README.md` 文件清单与磁盘一致（含 `docs/onboarding-new-project.md`）
- [ ] 核对 `contracts/openapi.yaml`（monorepo 根）与 `05-openapi-contract` 描述一致
- [ ] 核对 `codex/AGENTS.md` 与 `shared/` 存在性
- [ ] 核对 `cursor/*.mdc` 中 `rules/shared/...` 引用有效
- [ ] 核对 `examples/checkstyle`、`examples/ci`、`examples/scripts` 样板存在且 README 有入口
- [ ] 核对 `evals` 用例数与门槛（README / rubric / prompts 一致）

## 大版本 / 改 Hard Rules 或 ArchUnit 时追加

- [ ] 业务仓跑 `evals/prompts.md` B01–B38，P0 **8/8**、P1 **≥26/30**
- [ ] 多库 CI：至少 MySQL + PostgreSQL 迁移或 Testcontainers 通过

## 不要做

- [ ] 不要把 `docs/migration-from-template.md` 加入 Codex/Cursor 默认读取
- [ ] 生产禁止 `ddl-auto=update`（规则与代码评审双重约束）
