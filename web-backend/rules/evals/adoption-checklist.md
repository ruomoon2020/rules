# Adoption Checklist

## 规则包

- [ ] `rules/` 整包可访问
- [ ] 根 `AGENTS.md` ← `codex/AGENTS.md`
- [ ] `.cursor/rules/*.mdc` ← `cursor/`
- [ ] `contracts/openapi.yaml` 与前端共享

## 工程

- [ ] MyBatis-Plus + 分页插件配置
- [ ] Flyway（MySQL + PostgreSQL 若支持多库）
- [ ] ArchUnit 测试（`examples/archunit`）
- [ ] GlobalExceptionHandler + errorCode
- [ ] TraceId Filter / MDC
- [ ] SecurityConfig / CORS / CSRF / Swagger / Actuator 生产策略已确认
- [ ] OpenAPI baseline 已生成，CI diff 策略已确认

## 企业治理

- [ ] CODEOWNERS 已配置，覆盖契约、DB migration、安全、CI、IaC、规则包
- [ ] `docs/release-checklist.md` 已纳入发版流程
- [ ] `docs/incident-postmortem-template.md` 已纳入事故复盘流程
- [ ] `docs/backup-restore-runbook.md` 已按项目填写 RTO/RPO 与演练计划
- [ ] `docs/PERFORMANCE_BUDGET.template.md` 已复制为项目性能预算
- [ ] OWASP API Top 10 与国内合规映射已由安全 / 架构 Owner 过目

## 流程资产

- [ ] `docs/rule-maturity-model.md` 已声明目标 Level
- [ ] `docs/pull-request-template.md` 或已复制 `examples/.github/` 到业务仓 `.github/`
- [ ] CI 已按 Required/Conditional 裁剪（`examples/README.md`）

## 评测

- [ ] **Smoke**：B01–B08 + 核心 P1（≥15/18）；发版前 **Full** B01–B54（P0 8/8，P1 ≥40/46）
