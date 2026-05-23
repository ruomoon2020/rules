# Backend Evals

## 前置

1. 业务仓已落地完整 `rules/`。
2. 具备 Spring Boot 最小结构：`modules/*/api`、`application`、`mapper`。
3. 有 `contracts/openapi.yaml`（可用 fixture）。

## 执行

1. `prompts.md` 固定提示词。
2. `rubric.md` 判定。
3. `results-template.md` 记录。

## 门槛

| 级别 | 范围 | 门槛 |
|---|---|---|
| P0 | B01–B08 | **8/8** |
| P1 | B09–B38 | **至少 26/30** |

## 用例说明（部分重叠）

| 用例 | 侧重点 |
|---|---|
| B28 vs B36 | B28：事务内同步外部调用；B36：Feign/HTTP 超时与重试边界 |
| B18 并发 vs B38 | B18：方言/SQL 登记；B38：分布式锁释放须校验 owner token |
| B29 vs B31 | B29：测试连生产库；B31：fixture PII、缓存 key 明文等隐私生命周期 |
