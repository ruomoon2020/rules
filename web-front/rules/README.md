# Frontend AI Rules

版本见 `VERSION`，变更见 `CHANGELOG.md`。维护者发版见 `RELEASE.md`。

本目录是前端项目 AI 编码规则的**唯一执行入口**。

- **Codex**：`codex/AGENTS.md` → 复制到业务仓库根目录 `AGENTS.md`。
- **Cursor**：`cursor/*.mdc` → 复制到业务仓库 `.cursor/rules/`。
- **共用**：`shared/` 为 Codex 与 Cursor 的 SSOT；Cursor 的 `.mdc` 多为触发摘要，正文以 `shared/` 为准。
- **历史来源**：旧母文档仅作迁移期来源记录，AI 日常不直接当执行规则读取；规则包应可独立使用。

## 使用原则

1. 必须先遵守 `shared/00-must-follow.md`。
2. 按任务追加阅读，避免一次加载全部规则。
3. 冲突优先级：安全与合规 > `00-must-follow` > 项目本地配置（ESLint 等）> 场景规则。
4. 规则只写可执行约束；长篇说明留在设计文档或业务仓 README。
5. 语言约定见 `LANGUAGE.md`（shared/codex 中文，cursor 正文中文）。

## 规则层级（维护时遵守）

```text
L0  shared/00-must-follow.md          — 可拒 PR 的硬规则
L1  shared/01–21 等场景文件          — 细节与流程
L2  codex/*.md、cursor/*.mdc         — 任务索引 + 触发摘要（不重复 L1 全文）
```

## 落地方式（三选一，团队择一写进 onboarding）

### 方式 A — 整包同步（推荐）

将整个 `rules/` 目录放入业务仓库（submodule、子目录或内部 npm 包）。保证：

- 根目录或约定路径存在 `rules/shared/`、`rules/codex/`。
- `AGENTS.md` 内容来自 `rules/codex/AGENTS.md`，其中路径 `rules/shared/...` 可解析。
- `.cursor/rules/*.mdc` 来自 `rules/cursor/`，且 `.mdc` 内 `Read rules/shared/...` 可解析。

### 方式 B — 仅复制 Cursor + 根 AGENTS

复制 `cursor/*.mdc` 与 `AGENTS.md` 时，**必须**同步 `shared/`（或把 shared 要点内联进 `.mdc`），否则 `Read rules/shared/...` 会断链。

### 方式 C — Cursor `@` 引用

保留 `rules/` 在固定路径，在对话中用 `@rules/shared/00-must-follow.md` 等显式拉取；仍建议方式 A。

## Codex 读取顺序

1. `codex/01-before-editing.md`
2. `shared/00-must-follow.md`
3. 按 `AGENTS.md` 任务表追加 `shared/`、`codex/`
4. 收尾：`shared/10-verification-checklist.md`、`codex/05-verification.md`

## Cursor 说明

- 复制 `cursor/*.mdc` 到 `.cursor/rules/`。
- 除 `00-project-overview.mdc` 外，其余规则用 `globs` 触发，避免 `alwaysApply: true`。
- 编辑 `src/views/**/*.vue` 时可能同时命中多条规则，属正常；以 `shared/` 为准，`.mdc` 保持简短。

## 完整文件清单

| 文件 | 职责 | 何时读 |
|---|---|---|
| `shared/00-must-follow.md` | 硬规则 | 始终 |
| `shared/01-project-structure.md` | 目录与依赖 | 新模块、架构调整 |
| `shared/02-naming.md` | 命名、路径、变量、样式、环境变量 | 新文件、重命名 |
| `shared/03-code-style.md` | TS / Vue / import | 写代码 |
| `shared/04-ui-patterns.md` | 页面骨架与 UI | 做页面 |
| `shared/05-api-contract.md` | API 与契约 | 接口、表单、表格字段 |
| `shared/06-state-route-permission.md` | 路由 / Store / 权限 | 路由、登录、权限 |
| `shared/07-security-performance.md` | 安全 / a11y / 性能 | 安全、体验、性能相关 |
| `shared/08-quality-gates.md` | 测试 / CI / 发布 | 提测、发布 |
| `shared/09-ai-generation.md` | AI 行为约束 | AI 生成代码 |
| `shared/10-verification-checklist.md` | 完成前检查 | 收尾 |
| `shared/11-base-components-context.md` | Base 组件锚定 | 写 `views` 前 |
| `shared/12-schema-ssot.md` | Schema 锚定 | 写字段 / API 前 |
| `shared/13-form-and-detail.md` | 表单 / 详情页 | 表单、详情场景 |
| `shared/14-upload-import-export.md` | 上传 / Excel / CSV / JSON / Word 导入导出 | 文件、模板与批量数据 |
| `shared/15-testing.md` | 测试约定 | 写测、改契约后 |
| `shared/16-design-tokens.md` | 设计 Token | 样式、主题 |
| `shared/17-shell-navigation.md` | 壳层 / 菜单 / 特殊页型 | layout、router |
| `shared/18-logging-observability.md` | 结构化日志 / 监控 | 错误处理、埋点 |
| `shared/19-list-pagination.md` | 列表分页与竞态 | 列表页、useTable |
| `shared/20-dependency-governance.md` | 依赖治理 | 新增 / 升级依赖 |
| `shared/21-error-recovery.md` | 错误恢复 / 白屏治理 | 全局异常、路由失败 |
| `LANGUAGE.md` | 中英维护约定 | 维护规则时 |
| `codex/AGENTS.md` | Codex 入口与路由 | Codex 会话开始 |
| `codex/01-before-editing.md` | 改前上下文 | 任意改动 |
| `codex/02-page-generation.md` | 页面生成 | `views` |
| `codex/03-component-generation.md` | 组件生成 | `components` |
| `codex/04-api-and-schema.md` | API / schema | `api`、契约 |
| `codex/05-verification.md` | Codex 验证说明 | 收尾 |
| `cursor/*.mdc` | Cursor 触发摘要 | 按 glob 自动 |
| `evals/prompts.md` | AI 规则回归提示词 | 发版前 / 季度 |
| `evals/smoke-prompts.md` | 回归套件索引（不计提示词正文） | 日常 Smoke |
| `evals/adoption-checklist.md` | 业务仓落地勾选 | 新项目 onboarding |
| `scripts/validate-rules-package.py` | 规则包一致性校验 | 发版前 |
| `scripts/README.md` | 校验脚本说明 | 维护者 |
| `docs/contributing-rules-package.md` | 维护者变更治理 | 改 rules |
| `examples/ci/rules-package-validate.yml` | 业务仓 CI 校验样板 | 嵌入 rules/ |
| `RELEASE.md` | 维护者发版 checklist | 发版前 |
| `docs/migration-from-template.md` | 历史章节对照（维护者） | 不供 AI 读取 |
| `examples/ci-scan-views-el-tags.mjs` 等 | 硬门禁样板 | 业务仓 CI 接入 |
| `examples/run-ci-scan-fixtures.mjs` | ci-scan 回归 | 规则包发版前 |

## 规则评测（evals）

发版或大改 `shared/` 后，在测试仓库执行 `evals/prompts.md` 中 **E01–E31**，按 `evals/rubric.md` 记分，结果记入 `evals/results-YYYY-MM-DD.md`（由 `results-template.md` 复制）。

通过门槛：**P0 8/8 Pass**，**P1 至少 21/23 Pass**。日常 **Smoke**、发版 **Full**（见 `evals/README.md`、`evals/smoke-prompts.md`）。

维护者发版前运行 `python scripts/validate-rules-package.py`；本 monorepo 见 `.github/workflows/validate-rules-packages.yml`。

维护者若需旧模板章节对照，见 `docs/migration-from-template.md`（AI 不读）。

全栈 monorepo 与后端规则见仓库根 [docs/monorepo-layout.md](../../docs/monorepo-layout.md)、[web-backend/rules/README.md](../../web-backend/rules/README.md)。

## 软约束与硬门禁

- **软约束**：写 `views` 前读 `11-base-components-context`、`12-schema-ssot`。
- **硬门禁**：业务项目用 ESLint、type-check、schema check、CI 保证违规即失败；样板见 `examples/`。

## 硬门禁样板

见 `examples/README.md`，须**组合**使用：

| 能力 | 文件 |
|---|---|
| 禁 `import 'element-plus'` 及 `element-plus/*` | `eslint-views-ban-el.mjs` |
| 禁模板 `<el-*>`、动态 `is`、denylist 内 `<ElButton>` 等 | `ci-scan-views-el-tags.mjs` + `element-plus-pascal-denylist.mjs`（CI **勿**加 `--allow-empty`） |
| scripts 示例 | `package-scripts.sample.json` |

### CI 推荐接入顺序（业务仓）

1. 将 `rules/examples/eslint-views-ban-el.mjs` 并入 ESLint flat config（覆盖 `src/views` 与 `packages/**/src/views`）。
2. 在 `package.json` 增加并接入 **PR 必跑** 链路（不要只放 nightly / 可选 job）：

```json
{
  "scripts": {
    "lint": "eslint . && pnpm lint:views-el",
    "lint:views-el": "node ./rules/examples/ci-scan-views-el-tags.mjs"
  }
}
```

3. 发版前在规则包目录执行：`node rules/examples/run-ci-scan-fixtures.mjs`。

仅接 ESLint 而不跑 `ci-scan`，无法覆盖模板标签；`lint:views-el` 应与 `lint` 同级进入 PR 检查。
