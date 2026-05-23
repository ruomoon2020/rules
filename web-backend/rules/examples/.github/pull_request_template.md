# Pull Request 模板

> **落地**：将本目录 `examples/.github/` 复制到业务仓根目录 `.github/`（保留 `pull_request_template.md` 文件名即可）。
> 维护者说明见 `rules/docs/pull-request-template.md`。

---

## 变更摘要

<!-- 1–3 句话说明做什么、为什么 -->

## 变更类型（勾选）

- [ ] API / OpenAPI
- [ ] DB / Flyway / 数据修复
- [ ] 安全 / 鉴权 / 权限码
- [ ] 依赖 / 许可证
- [ ] 定时任务 / 批处理 / MQ
- [ ] 配置 / 密钥 / IaC / 容器
- [ ] 仅文档 / 规则包
- [ ] 其他：__________

---

## 必填检查

### 契约与 API

- [ ] 已更新 `contracts/openapi.yaml`（或项目约定路径）
- [ ] 已运行 OpenAPI diff / Spectral（或说明 skip 原因）：__________
- [ ] 破坏性变更已标注 `deprecated` / 版本策略 / 迁移说明（`05-openapi-contract.md`）
- [ ] 可重试写操作已声明 `Idempotency-Key` 或业务幂等键（若适用）

### 数据与持久化

- [ ] Flyway 脚本已 `validate`；多库项目已在 MySQL + PostgreSQL（或 Testcontainers）验证（若改库）
- [ ] 无用户输入进入 SQL `${}`；排序/列名白名单
- [ ] 生产数据修复（若有）：已附 dry-run、影响行数、审批、回滚（`31-production-data-ops.md`）

### 安全与权限

- [ ] 敏感接口已覆盖：未登录 / 无权限 / 跨租户 / BOLA（他人资源 id）（`06`、`15`）
- [ ] 数据权限 / 多租户条件与列表、导出一致（`24`）
- [ ] 无密码、Token、完整 PII 写入日志或异常
- [ ] 用户可控 URL 出站已防 SSRF（若适用）（`28`）

### 质量与性能

- [ ] 已运行：`mvn verify` / `./gradlew check`（结果：Pass / Fail — 链接：__________）
- [ ] ArchUnit / Checkstyle（若项目启用）已通过或说明未配置
- [ ] 核心接口 / 批处理 / 导入导出已说明性能预算或数据量上限（`16`、`docs/PERFORMANCE_BUDGET.template.md`）
- [ ] SLO / 降级 / 外部依赖超时（若改核心链路）（`32`、`28`）

### 合规与审计

- [ ] 涉及 PII / 导出 / 留存：已对照 `29-data-privacy-lifecycle.md`
- [ ] 敏感操作（删改权限、导入导出、配置变更等）已落审计（`27`）
- [ ] 高风险变更（支付、Webhook、跨租户）：已威胁建模或链接记录（`35`）

### 治理

- [ ] 公共抽象 / 新依赖 / breaking API：已确认 Owner；需 ADR 时已补（`30`）
- [ ] 已请求 CODEOWNERS 对应 Reviewer（契约 / DB / security / CI / rules）
- [ ] 规则包变更（若改 `rules/**`）：见 `rules/docs/contributing-rules-package.md`

---

## 已运行命令（粘贴或链接 CI）

```text
# 示例
mvn verify
npx @redocly/cli diff contracts/openapi.baseline.yaml contracts/openapi.yaml
```

---

## 风险与回滚

<!-- 上线风险、功能开关、回滚步骤 -->

## 关联

- Issue / 工单：
- ADR：
- 性能预算 / Runbook：
