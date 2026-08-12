# Changelog

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
