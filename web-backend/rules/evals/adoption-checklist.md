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

## 评测

- [ ] B01–B38，P0 8/8，P1 ≥26/30
