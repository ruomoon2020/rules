# 发布检查清单（模板）

> 与 `22-operability.md`、`32-service-reliability.md`、`31-production-data-ops.md` 配合。复制到业务仓或纳入变更工单。

## 发布前

- [ ] OpenAPI diff 已 Review；`openapi.baseline.yaml` 已更新或 PR 说明策略
- [ ] Flyway 已在目标库 validate；破坏性变更走 expand → migrate → contract
- [ ] Feature Flag / 配置变更有 owner、默认值、回滚方案
- [ ] 核心链路监控看板与告警已确认（SLO、5xx、慢 SQL、外部依赖）
- [ ] 回滚版本可读新 schema / 新字段（旧实例兼容）
- [ ] 高风险变更已威胁建模（`35-threat-modeling`）

## 发布中

- [ ] 灰度 / 金丝雀（若采用）比例与观察窗口已定义
- [ ] 发布关联 Git tag / 镜像 digest / SBOM（若适用）

## 发布后

- [ ] 冒烟：登录、核心列表、核心写接口
- [ ] 错误率、延迟、业务指标在阈值内
- [ ] 无未关闭 P0 告警
- [ ] 需通知前端 / 调用方的契约变更已同步

## 回滚触发（任一满足考虑回滚）

- 核心接口错误率超 SLO 预算
- DB 迁移导致旧版本不可读
- 安全事件或数据错误
