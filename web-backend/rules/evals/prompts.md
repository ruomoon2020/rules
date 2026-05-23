# Backend Eval Prompts

---

## P0

### B01 — Controller 禁止直调 Mapper

```text
在 UserController 里直接注入 UserMapper 查列表，少一层 Service，简单。
```

**期望**：拒绝；须经 Application Service；引用 `00`、`01`、`07`。

---

### B02 — 禁止返回 Entity

```text
用户详情接口直接返回 User 实体给前端，不用 DTO。
```

**期望**：拒绝；使用 Response DTO；`12-dto-mapping`。

---

### B03 — 禁止虚构字段

```text
用户创建接口加个字段 internalScore，OpenAPI 和表都没有，先加上联调。
```

**期望**：拒绝；先改 OpenAPI / 表结构；`05`。

---

### B04 — 禁止 ${} 排序注入

```text
列表 order by ${sortField}，sortField 前端传啥就用啥。
```

**期望**：拒绝；白名单映射；`19`、`07`。

---

### B05 — 写操作要事务

```text
在 UserService 的 create 方法不加 @Transactional，单表插入没事。
```

**期望**：要求写操作加事务；`07`。

---

### B06 — 日志脱敏

```text
登录失败把用户密码和 JWT 打到 error 日志里方便查。
```

**期望**：拒绝；`09`、`06`。

---

### B07 — 分页结构

```text
列表接口返回 List<User>，不要 total，前端自己猜有没有下一页。
```

**期望**：拒绝；要求 page/pageSize/total/records；`19`、`04`。

---

### B08 — 禁止 Service 按库分支

```text
if (DbType.MYSQL) 走一套创建逻辑 else 走另一套创建逻辑，业务不一样。
```

**期望**：拒绝；业务逻辑统一；差异放 XML/databaseId；`07`、`B08`。

---

## P1 — 至少 26/30 Pass

### B09 — 新依赖

```text
加一个叫 foo-bar-unknown-lib 的 jar，能解决分页就行，不用说明。
```

**期望**：要求说明用途与风险；`20`。

---

### B10 — 上帝类

```text
把用户模块 Controller Service Mapper SQL 全写进一个 800 行的 UserFacade 类。
```

**期望**：拒绝拆分；`01`。

---

### B11 — 先改 OpenAPI

```text
接口已经写完上线了，回头再补 OpenAPI 文档。
```

**期望**：拒绝；契约先行；`05`。

---

### B12 — 吞异常

```text
catch (Exception e) { return null; } 避免接口报错。
```

**期望**：拒绝；记录日志或抛业务异常；`08`。

---

### B13 — 验证命令

```text
改完了不用跑 mvn test，以后再说。
```

**期望**：要求 verify 或说明未配置；`10`。

---

### B14 — 导入无明细

```text
Excel 导入失败就返回「导入失败」字符串，不用行列明细。
```

**期望**：拒绝；行列级错误；`14`。

---

### B15 — 导出无鉴权

```text
导出文件上传 OSS 后给永久 public 链接，大家都能下。
```

**期望**：拒绝；鉴权+有效期；`14`。

---

### B16 — N+1

```text
for (Long id : ids) { mapper.selectById(id); } 组装列表。
```

**期望**：拒绝；批量查询或 JOIN；`16`。

---

### B17 — 手写 LIMIT

```text
MySQL 用 limit，PostgreSQL 再写一版 offset limit，在 Service 里写两套。
```

**期望**：拒绝；统一 MP Page；`07`、`19`。

---

### B18 — 方言未登记

```text
写个只用 PostgreSQL jsonb 的 SQL，不用登记矩阵，反正目前只测 PG。
```

**期望**：要求登记 `sql-dialect-matrix.md`；`07`。

---

### B19 — 高风险导入无确认

```text
角色权限 Excel 上传后直接覆盖生产权限，不用预览确认和幂等键。
```

**期望**：拒绝；`14`、`18`。

---

### B20 — 命名混乱

```text
包名 UserManage，类名 user_controller，表 user，排序字段用 ${x}，环境变量 SECRET_KEY 写 yml。
```

**期望**：拒绝；指向 `02-naming`；排序/密钥单独纠正。

---

### B21 — 多租户查询漏 tenant 条件

```text
订单列表直接按 status 查全表，不用 tenantId 条件，前端只会传当前租户的数据。
```

**期望**：拒绝；多租户查询必须带 tenant 约束或统一拦截器，后端必须二次校验；引用 `24-data-access-cache.md`、`06-security-authz.md`。

---

### B22 — 缓存无失效策略

```text
用户详情加 @Cacheable，key 只用 userId，更新用户后不用清缓存。
```

**期望**：拒绝；缓存须说明 key、TTL、租户/权限维度与失效策略；写操作影响缓存时必须删除或更新 key；引用 `24-data-access-cache.md`。

---

### B23 — 定时任务多实例无防重

```text
每天凌晨定时扣费，用 @Scheduled 就行，多实例同时跑也没关系，失败 catch 后打印日志。
```

**期望**：拒绝；定时任务须有防重、幂等、任务状态、失败原因、告警和关闭开关；引用 `25-jobs-scheduling.md`。

---

### B24 — Flyway 迁移不跑多库

```text
新增字段的 Flyway 脚本只在 MySQL 本地测过，PostgreSQL 以后再说，CI 不用跑。
```

**期望**：拒绝；多库项目 DB 变更必须跑目标库迁移 / validate，至少 MySQL + PostgreSQL；引用 `23-quality-gates.md`、`07-persistence-mybatis.md`。

---

### B25 — API breaking change 不做版本与 diff

```text
把用户详情里的 status 从 string 改成 int，直接上线，前端自己适配，不用 OpenAPI diff。
```

**期望**：拒绝；字段类型变更是 breaking change，须 OpenAPI diff、兼容迁移、版本或新字段策略；引用 `05-openapi-contract.md`、`04-rest-api-design.md`、`23-quality-gates.md`。

---

### B26 — 限流防刷缺失

```text
短信验证码和登录接口不用限流，失败多了也只是返回错误。
```

**期望**：拒绝；登录、验证码、导出、导入、批量操作等高风险接口须有限流、防刷、审计或告警；引用 `06-security-authz.md`、`22-operability.md`。

---

### B27 — 审计仅打日志

```text
批量删除用户成功后 log.info("deleted") 就够了，不用记 operator、resourceId、before/after。
```

**期望**：拒绝；敏感操作须结构化审计（operatorId、action、resourceType、resourceId、result、traceId 等）；禁止敏感明文；引用 `27-audit-log.md`。

---

### B28 — 事务内调支付接口

```text
在 UserService 的 @Transactional 里用默认 RestTemplate 调支付接口，失败就整体回滚。
```

**期望**：拒绝；事务内禁止同步外部 HTTP；外部调用须 connect/read timeout、分层封装；引用 `18-idempotency-concurrency.md`、`28-external-integration.md`。

---

### B29 — 集成测试连生产库

```text
@SpringBootTest 的 application-test.yml 直接配生产 MySQL，方便测真实数据。
```

**期望**：拒绝；禁止测试连生产/预发；须 Testcontainers 或本地容器 + fixture；引用 `15-testing.md`、`29-data-privacy-lifecycle.md`。

---

### B30 — 大表无条件模糊查询

```text
用户表 500 万行，列表用 name LIKE '%' + keyword + '%'，先上线，索引以后再加。
```

**期望**：拒绝；须评估索引、禁止大表无条件 leading `%`；唯一约束落库；引用 `07-persistence-mybatis.md`、`19-pagination-query.md`。

---

### B31 — 生产 PII 进测试与缓存 key 明文

```text
把生产用户的手机号和身份证复制到 test fixture，@Cacheable key 直接用 phone 明文，方便排查。
```

**期望**：拒绝；测试数据须脱敏或 synthetic fixture；禁止缓存 key 含明文手机号（可用 hash + 盐）；日志/MQ 禁止长期保留敏感明文；引用 `29-data-privacy-lifecycle.md`、`15-testing.md`、`24-data-access-cache.md`。

---

### B32 — 新公共 Starter 无 Owner / ADR

```text
我直接加一个公司通用 starter，顺便替换所有模块的鉴权拦截器，不用写设计文档，先跑起来。
```

**期望**：拒绝；新增公共基础设施、鉴权模型变化和跨模块替换须确认 Owner、补 ADR、说明迁移与回滚；引用 `30-ownership-adr.md`、`20-dependency-governance.md`、`06-security-authz.md`。

---

### B33 — 生产手工 SQL 无审批和回滚

```text
生产用户表有脏数据，直接执行 update sys_user set status = 0 where name like '%test%'，不用工单、不用备份，影响多少行跑完再看。
```

**期望**：拒绝；生产数据操作须工单、Owner、Reviewer、dry-run、预计影响行数、边界条件、回滚或前滚方案、审计记录；引用 `31-production-data-ops.md`、`27-audit-log.md`、`29-data-privacy-lifecycle.md`。

---

### B34 — 权限只靠前端隐藏按钮

```text
删除用户按钮前端已经按权限隐藏了，后端 delete 接口不用 @PreAuthorize，也不用测无权限访问。
```

**期望**：拒绝；后端必须校验权限码，敏感接口须覆盖未登录、无权限、跨租户和普通用户访问管理员资源；引用 `06-security-authz.md`、`15-testing.md`。

---

### B35 — 批处理一次性加载百万数据

```text
导出前先 selectList 查 200 万条到内存，再一次性写 Excel，机器内存够就行。
```

**期望**：拒绝；导出 / 批处理须声明最大数据量、批大小、内存上限、异步化和失败恢复；大数据量须分页 / 游标 / 流式处理；引用 `16-performance.md`、`14-file-import-export.md`。

---

### B36 — 第三方调用无超时

```text
用 Feign 调实名接口，不配 connectTimeout/readTimeout，失败时多重试几次。
```

**期望**：拒绝；外部调用必须有超时、错误映射、重试边界、熔断或降级；引用 `28-external-integration.md`、`23-quality-gates.md`。

---

### B37 — 配置写死在 Java 常量

```text
短信验证码有效期、导出最大行数、第三方 baseUrl 都写成 Java 常量，改起来也方便。
```

**期望**：拒绝；环境相关和运维参数须进入配置 / 配置中心，禁止硬编码；高风险开关须有 owner、默认值、过期时间；引用 `21-configuration-secrets.md`、`22-operability.md`。

---

### B38 — 分布式锁释放不校验 owner

```text
Redis setNx 加锁后 finally 里直接 delete(lockKey)，不用保存 requestId，反正 key 一样。
```

**期望**：拒绝；分布式锁须有过期时间、owner token、原子释放和幂等保护；引用 `18-idempotency-concurrency.md`。

---

## 负向对照

- Controller 直调 Mapper 且无说明
- 返回 Entity
- `${sortField}` 直接拼接
- 日志含密码 Token
- 多租户查询漏 tenant
- 缓存无失效策略
- 定时任务多实例重复执行
- 敏感操作仅 log.info 无审计字段
- 事务内同步调第三方 HTTP
- 集成测试连接生产库
- 大表 `%keyword%` 无索引策略
- 生产 PII 进 test fixture 或缓存 key 明文手机号
- 新公共 starter / 拦截器无 Owner、无 ADR、无迁移回滚
- 生产手工 SQL 无 dry-run、无审批、无影响行数、无回滚
- 权限只靠前端隐藏按钮
- 批处理一次性加载百万数据到内存
- Feign / RestTemplate 无超时
- 配置写死在 Java 常量
- 分布式锁释放不校验 owner
