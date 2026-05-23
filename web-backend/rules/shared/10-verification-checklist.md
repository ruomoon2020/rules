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

## 回复须说明

- 改动文件与接口
- 运行的命令及结果
- 未运行项及原因

Codex：`codex/05-verification.md`。
