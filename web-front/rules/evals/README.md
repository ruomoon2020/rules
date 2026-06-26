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
| **P1** | E09–E40（共 32 条） | **至少 29/32** Pass |

## 回归套件（企业分层）

| 套件 | 范围 | 门槛 | 场景 |
|---|---|---|---|
| **Smoke** | E01–E08 + 核心 P1 12 条 | P0 8/8；核心 P1 ≥10/12 | 日常 PR、AI 快速回归 |
| **Security** | E12、E18、E25、E27 | 建议 4/4 | 安全 / 隐私 / 导入导出 PR |
| **Contract** | E03、E04、E05、E26 | 建议 4/4 | Schema / API / 字段 PR |
| **Business Extension** | E32–E40 | 建议 9/9 | 成熟后台新增业务页 / CRUD / 树表主子表 PR |
| **Full** | E01–E40 | P0 8/8；P1 ≥29/32 | **发版**、规则包升级 |

索引（不复制正文）：`smoke-prompts.md`（**不计入** `### Exx` 计数；校验见 `scripts/validate-rules-package.py`）。

### 核心 P1（= Smoke 中的 12 条）

E09、E13、E15、E16、E17、E18、E22、E24、E27、E28、E29、E30。

发版前仍须跑 **Full**（E01–E40）。

### 与后端 Business Extension 对照（联调 / 双端 PR）

| 后端 | 前端 | 主题 |
|---|---|---|
| B55 | E32 | 不污染公共 / 壳层 |
| B56 | E33 | 复用平台菜单 / 权限 / 字典 |
| B57 | E34 | CodeGen 后须补齐 |
| B58 | E35 | 列表 / 详情 / 导出权限一致 |
| B59 | E36 | 导出审计与下载鉴权 UI |
| B60 | E37 | 导入任务状态，禁止伪造成功 |
| B61 | E38 | 树表父节点禁选非法项 |
| B62 | E39 | 主子表失败态与回滚一致 |
| B63 | E40 | 禁止改 generator 全局 Vue 模板 |

- 不允许把 20/23 四舍五入为通过。
- 任一条 Fail 若输出可合并代码，须在真实仓库跑 `pnpm lint` / `type-check` 二次确认。

## 与落地清单关系

`adoption-checklist.md` 用于勾选业务仓规则落地状态，与 evals 互补：前者是清单，后者是行为验证。
