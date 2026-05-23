# Rules Evals（规则回归评测）

用于验证 AI 是否遵守 `rules/` 约束。建议每季度或规则大版本发布前跑一轮。

## 前置条件

1. 业务仓库已按 `rules/README.md` **方式 A** 落地完整 `rules/`。
2. 已配置 Cursor `.cursor/rules/` 或 Codex 根目录 `AGENTS.md`。
3. 测试仓库具备最小可运行结构：`src/views`、`src/components/base`、`contracts/schema.json`（可用 fixture）。

## 如何执行

1. 打开 `prompts.md`，按编号依次向 AI 发送**固定提示词**（不要改措辞）。
2. 对照 `rubric.md` 判定 Pass / Fail / Partial。
3. 填写 `results-template.md`（复制为带日期的结果文件，如 `results-2026-05-24.md`）。
4. Fail 项回流修改 `shared/` 或 `cursor/`，并更新 `CHANGELOG.md`。

## 通过标准

| 级别 | 用例 | 门槛 |
|---|---|---|
| **P0** | E01–E08（共 8 条） | **8/8** 必须 Pass |
| **P1** | E09–E31（共 23 条） | **至少 21/23** Pass |

- 不允许把 20/23 四舍五入为通过。
- 任一条 Fail 若输出可合并代码，须在真实仓库跑 `pnpm lint` / `type-check` 二次确认。

## 与落地清单关系

`adoption-checklist.md` 用于勾选业务仓规则落地状态，与 evals 互补：前者是清单，后者是行为验证。
