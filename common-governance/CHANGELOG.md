# Changelog

## 2.4.3 — 2026-09-17

- 接入校验拒绝仅手动触发、明确停用的控制工作流，并拒绝把契约文件当作构建产物证明。
- Level 2/3 结果明确限定为仓内结构与声明证据校验；平台当前设置和实际执行须单独核对。
- 平台证据将三类 PR Required Checks 与产物信任发布门禁分开，避免把仅在发布标签运行的 job 设置为 PR 必需状态。
- 债务基线默认拒绝零文件扫描；确需允许时须声明理由。

## 2.4.2 — 2026-09-15

- 新增 `scripts/prepare-ai-eval-run.py`：打印套件 digest、写出 fail-by-default 骨架，明确不调用模型、不自动满分。
- AI 工具安全文档补充评测准备命令。

## 2.4.1 — 2026-09-15

- 新增 `examples/ci/ai-eval-results-required.yml`：校验已提交的 AI Tool Safety 结果，明确不调用模型。
- 发布包纳入 `examples/ai-eval-results.yaml`；接入指南与执行边界文档补齐入口。

## 2.4.0 — 2026-09-15

- AI Tool Safety 5/5 改为条件门禁（发版 / 规则包升级 / 高风险 AI），不再作为 Level 0 采纳控制。
- 控制目录 1.3.0：每条控制标注 `verification_kind`（evidence / presence / manual）；`CR-AI-001` 升至 Level 2 并带 `gate`。
- `ai-tool-security.md` 补充评测执行边界与 MCP / 写操作硬约束。
- DoD、成熟度对照与 Scorecard 同步区分「行为边界」与「5/5 套件」。

## 2.3.0 — 2026-09-15

- 接入指南改回仓库根 `common-governance/`，并随包分发 `project-adoption-guide.md`。
- 统一 SBOM / AI Tool Safety 的 Level 口径；分支保护清单补齐四门 Required Checks。
- 控制目录升至 1.2.0：AI Safety 归 Level 0（使用 AI 时），并补充凭据扫描、债务基线、PR 治理、SLO 与跨项目 Scorecard。
- 债务基线强制 `baseline_commit` / `captured_at` / `owner` / `scan_command` 元数据。
- 新增豁免 Required CI 样板 `examples/ci/exceptions-required.yml`。

## 2.2.0 — 2026-09-15

- 根 PR 模板补齐需求、验收条件、影响面、实现和验证证据追踪矩阵。
- 新增实际 PR 描述机器校验，拒绝空追踪行、风险等级多选或漏选及未清理占位符。
- 新增机器可读豁免样板和校验器，强制 90 天期限、审批、补偿控制、到期与关闭证据。
- 项目严格接入检查拒绝仍声明为 sample/placeholder 的 CODEOWNERS。
- 源仓 CODEOWNERS 替换为当前仓库真实维护账号，治理 CI 增加每周定时审计。

## 2.1.0 — 2026-09-15

- 新增目标规则与存量迁移基线，明确当前采纳门禁和目标差距审计双通道。
- 新增可配置债务基线检查器，支持正则计数和路径白名单两类不可增长指标。
- 项目采纳检查新增 `--report-only`，保留差距输出但用于非阻断的目标审计。
- 新增项目覆盖层、契约现状和迁移基线样板。
- 新增债务基线 Required workflow 样板。

## 2.0.0 — 2026-08-14

- `release-evidence.yaml` 升级到 schema v2，强制 commit SHA、产物摘要、规则版本、带时区批准时间与结构化豁免。
- Level 2/3 改为核验 `governance-adoption.yaml` 引用的 CI、凭据扫描、供应链、分支保护和平台治理证据，不再只检查治理包或 Scorecard 是否存在。
- 新增环境晋级、事故响应和跨端事故复盘模板，并纳入 DoD、成熟度和发布包。
- 新增规则采纳 Required workflow 与采纳证据样板；PR 模板检查升级为标题和追踪表结构校验。
- 管理端契约检查支持 OpenAPI、JSON Schema 和项目声明路径；后端 Level 1 要求 CI 构建证据。
- CI 样板固定第三方 action 完整 commit SHA，并强制顶层只读权限；新增 workflow 安全校验。
- 新增 SBOM、构建 provenance / attestation workflow，发布证据绑定真实产物摘要和信任材料。
- Level 2 平台证据升级为结构化快照，校验组织 MFA、最小默认权限、主干保护和生产非自审。
- 新增 SSDF 1.1、ASVS 5.0.0、OSPS Baseline、SLSA 1.1 的版本化控制目录与校验器。
- AI Tool Safety 增加机器结果 schema，绑定模型版本、独立评测人与被测套件摘要。

## 1.3.0 — 2026-08-14

- 新增需求追踪、业务正确性评审、AI 工具安全和结构化发布证据四份治理基线。
- 新增 `release-evidence.yaml` 样板与机器校验脚本，拒绝占位证据、未测试回滚和高风险无灰度。
- 项目采用检查新增 `--level 0..3`：Level 1 强化本地覆盖与契约脚本，Level 2 强制治理包和评审资产，Level 3 强制项目成熟度证据。
- PR 模板新增需求追踪矩阵和业务正确性复核。

## 1.2.0 — 2026-08-13

- 凭据扫描固定到已签名发布版本，并增加默认规则正反 canary，避免 scanner 静默空跑。
- 将供应链 Required workflow 纳入发布包、manifest、接入检查与测试。
- Node 供应链门禁拒绝无锁文件、多锁文件和未定义的 Yarn 退化路径；固定许可证与 Maven 扫描器版本。
- 分发文档统一使用包内接入脚本和 `--require-governance`。

## 1.1.0 — 2026-08-12

- 提供固定 CLI 版本、release checksum 校验、只读权限和完整历史 checkout 的凭据扫描 Required workflow 样板。
- 将 workflow 纳入固定资产 manifest、发布包一致性校验和 YAML / version-pinning 单测。

## 1.0.0 — 2026-08-11

- 首次提供可分发的跨栈治理包。
- 根 `docs/` 保持唯一维护源；同步脚本生成文档副本和 SHA-256 manifest。
- 提供包内一致性校验、独立接入检查、PR 模板和 Conventional Commits 配置样板。
- manifest 覆盖文档、版本、说明、样板和脚本；固定资产缺失或 checksum 漂移均拒绝通过。
- 提供不含组织联系方式和既有决策结论的 SECURITY、ADR 可填写模板。
