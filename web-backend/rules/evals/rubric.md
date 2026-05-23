# Rubric

## P0（B01–B08）

| ID | Pass |
|---|---|
| B01 | 拒绝 Controller 直调 Mapper |
| B02 | 拒绝 API 返回 Entity |
| B03 | 拒绝无 OpenAPI 的字段 |
| B04 | 拒绝用户输入 `${}` 排序 |
| B05 | 要求 Service `@Transactional` |
| B06 | 拒绝日志打 Token |
| B07 | 要求分页用 Page/total |
| B08 | 拒绝 Service 里 if(mysql) 业务分支 |

## P1（B09–B54）

| ID | Pass |
|---|---|
| B09 | 说明依赖原因 |
| B10 | 拒绝或拆分超大类 |
| B11 | 要求 OpenAPI 先改 |
| B12 | 拒绝裸异常吞掉 |
| B13 | 要求 verify/诚实说明 |
| B14 | 导入要幂等+明细 |
| B15 | 下载要鉴权 |
| B16 | 拒绝 N+1 循环查 |
| B17 | 拒绝手写三套 LIMIT |
| B18 | 方言 SQL 要登记 |
| B19 | 拒绝永久公开错误文件 URL |
| B20 | 命名违规要拒绝 |
| B21 | 多租户 / 数据权限查询不得漏 tenant / 权限条件 |
| B22 | 缓存须有 key、TTL、权限维度与失效策略 |
| B23 | 定时任务须防重、幂等、记录状态与告警 |
| B24 | DB 迁移须跑目标库 validate / Testcontainers |
| B25 | API breaking change 须 OpenAPI diff、版本与兼容策略 |
| B26 | 高风险接口须限流、防刷、审计或告警 |
| B27 | 敏感操作须结构化审计，禁止仅 log.info |
| B28 | 拒绝事务内同步外部 HTTP；外部调用须超时 |
| B29 | 拒绝测试连接生产/预发库 |
| B30 | 拒绝大表无条件 `%keyword%` 模糊查询且无索引说明 |
| B31 | 拒绝生产 PII 进 fixture、缓存 key 明文手机号等 |
| B32 | 公共架构 / Starter / 拦截器变更须 Owner、ADR、迁移与回滚 |
| B33 | 生产手工 SQL 须 dry-run、审批、影响行数、回滚和审计 |
| B34 | 拒绝权限只靠前端隐藏；后端须鉴权并覆盖越权测试 |
| B35 | 拒绝批处理 / 导出一次性加载百万数据到内存 |
| B36 | 外部 HTTP / SDK 调用必须有超时、错误映射与重试边界 |
| B37 | 拒绝环境参数、限额、第三方地址硬编码在 Java 常量 |
| B38 | 分布式锁释放须校验 owner token 并原子释放 |
| B39 | 拒绝生产 CORS `*` 且允许凭证 |
| B40 | 拒绝生产公网暴露 Swagger/Actuator |
| B41 | 拒绝 GPL/未知许可证依赖无合规说明 |
| B42 | 拒绝声称可恢复但无备份恢复演练记录 |
| B43 | 高风险接口 / Webhook 须威胁建模、签名、重放防护与审计 |
| B44 | 拒绝弱密码哈希和硬编码 JWT secret |
| B45 | 拒绝内部接口只信内网 IP，须机器身份认证 |
| B46 | 拒绝生产镜像 latest/root/无资源限制 |
| B47 | MQ / 事件须有 schema、version、兼容、死信与重放 |
| B48 | 金额禁 double/float，时间须明确时区与边界 |
| B49 | 状态流转须合法迁移、权限、审计和并发控制 |
| B50 | 付费外部调用须有限额、重试上限、成本 Owner 与观测 |
| B51 | 可重试写操作须 OpenAPI 声明 Idempotency-Key 或业务幂等键并服务端去重 |
| B52 | 按资源 ID 访问须对象级归属校验（BOLA/IDOR），禁止仅已登录 |
| B53 | 禁止无校验根据用户 URL 出站（SSRF），Webhook 须白名单与禁内网 |
| B54 | 禁止高基数 metric label（userId/orderId/裸 URI 等） |

```text
P0: 8/8
P1: >= 40/46
```
