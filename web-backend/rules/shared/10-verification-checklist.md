# Verification Checklist

## 自动化

```bash
mvn verify
# 或
./gradlew check
```

按项目可能包含：test、checkstyle、archunit、openapi-diff、flyway validate。

## 手工检查

1. Controller 未直接注入 Mapper。
2. REST 未返回 Entity；DTO 与 OpenAPI 一致。
3. 写操作有 `@Transactional`；只读 `readOnly=true`。
4. XML 无用户输入 `${}`；排序/列名走白名单。
5. 分页响应含 `total`、`records`，与契约一致。
6. 错误含 `errorCode`、`traceId`；日志无敏感信息。
7. 多库：方言 SQL 已登记 `sql-dialect-matrix.md`；Flyway 脚本对目标库可执行。
8. 新增命名符合 `02-naming.md`。
9. 导入导出、幂等、鉴权按 `14`、`18` 检查（若涉及）。
10. 多租户 / 数据权限 / 缓存 key 与失效策略按 `24` 检查（若涉及）。
11. 定时任务 / 批处理 / 异步补偿按 `25` 检查（若涉及）。
12. CI / 工具门禁与跳过原因按 `23` 检查。
13. 敏感操作审计字段按 `27` 检查（若涉及删除、权限、导入导出、配置变更）。
14. 外部调用超时、分层、非事务内同步调用按 `28` 检查（若涉及第三方）。
15. API 兼容 / deprecated / breaking 按 `05`、`04` 检查（若改契约）。
16. 索引 / 唯一约束 / 大表模糊查询按 `07` 检查（若改 SQL 或表结构）。
17. 测试未连生产库、Testcontainers / fixture 按 `15` 检查。
18. 数据保留 / 脱敏 / 导出按 `29` 检查（若涉及 PII）。
19. 公共抽象 / 新依赖 / 跨模块契约按 `30` 检查 Owner 与 ADR（若涉及架构决策）。
20. 生产数据修复 / 手工 SQL / 回填按 `31` 检查 dry-run、影响行数、审批、回滚和审计。
21. 敏感接口越权测试按 `06`、`15` 检查：未登录、无权限、跨租户、普通用户访问管理员资源。
22. 性能预算按 `16` 检查：数据量上限、索引 / count 策略、P95/P99、异步化或降级方案。
23. 可靠性 / RTO·RPO / 降级 / 演练按 `32` 检查（若涉及核心链路或外部依赖）。
24. CORS / CSRF / Cookie / Swagger·Actuator 生产暴露按 `06` 检查。
25. 依赖许可证 / SBOM / CVE SLA 按 `20` 检查（若新增依赖）。
26. 备份恢复 Runbook / 演练记录按 `docs/backup-restore-runbook.md`、`31` 检查。
27. 归档 / 冷热数据按 `34` 检查（若涉及历史数据）。
28. 威胁建模按 `35` 检查：资产、信任边界、入口点、滥用场景、缓解措施。
29. 加密 / Token / 签名 / 密钥按 `36` 检查：算法、随机数、轮换、吊销、防重放。
30. 服务间认证按 `37` 检查：机器身份、最小权限、Webhook/MQ/Job 审计与幂等。
31. 容器 / K8s / IaC 按 `38` 检查：非 root、非 latest、资源限制、probes、Secret。
32. 事件契约按 `39` 检查：schema、version、兼容、死信、重放。
33. 金额 / 时间 / 精度按 `40` 检查：BigDecimal/最小单位、币种、时区、边界。
34. 字典 / 状态机按 `41` 检查：合法流转、权限、审计、并发。
35. 成本按 `42` 检查：付费调用、大查询、大导出、保留周期、Owner 与清理策略。
36. BOLA/IDOR：按资源 ID 的读/写/删是否校验归属；列表与错误信息是否泄露他人资源存在性（`06`）。
37. SSRF：用户可控 URL 出站是否白名单、禁内网/metadata；Webhook 签名与审计（`28`、`35`）。
38. 可重试写操作是否在 OpenAPI 声明 `Idempotency-Key` 或业务幂等键（`04`、`05`、`18`）。
39. 追踪：W3C `traceparent` 传递；metric 无高基数 label（`09`）。
40. 发版前 `docs/release-checklist.md`；事故复盘模板就绪（`32`）。

## 回复须说明

- 改动文件与接口
- 运行的命令及结果
- 未运行项及原因

Codex：`codex/05-verification.md`。
