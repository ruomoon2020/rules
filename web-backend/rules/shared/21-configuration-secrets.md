# Configuration & Secrets

1. 配置分环境：`application-{profile}.yml`；敏感项来自环境变量/配置中心。
2. 禁止提交：`application-prod.yml` 中的密码、密钥、内网地址。
3. 数据源、Redis、OSS 等连接串外部化。
4. **Feature Flag**（与前端 `00` 一致）：
   - 须有 **owner**、**默认值**、**过期/清理日期**；
   - 命名统一前缀（如 `feature.xxx.enabled`），配置来源统一（配置中心或 `application.yml`，禁止散落硬编码）。
   - **禁止**灰度/实验开关长期存在；到期须删除代码分支与配置。
5. 多库：各 profile 指定 `spring.datasource.url` 与 Flyway locations。
6. 发布与回滚相关开关策略见 `22-operability.md`。
