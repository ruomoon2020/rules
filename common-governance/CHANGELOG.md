# Changelog

## 2.0.0 — 2026-08-14

- `release-evidence.yaml` 升级到 schema v2，强制 commit SHA、产物摘要、规则版本、带时区批准时间与结构化豁免。
- Level 2/3 改为核验 `governance-adoption.yaml` 引用的 CI、凭据扫描、供应链、分支保护和平台治理证据，不再只检查治理包或 Scorecard 是否存在。
- 新增环境晋级、事故响应和跨端事故复盘模板，并纳入 DoD、成熟度和发布包。
- 新增规则采纳 Required workflow 与采纳证据样板；PR 模板检查升级为标题和追踪表结构校验。
- 管理端契约检查支持 OpenAPI、JSON Schema 和项目声明路径；后端 Level 1 要求 CI 构建证据。

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
