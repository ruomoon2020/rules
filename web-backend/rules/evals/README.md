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
| P1 | B09–B63 | **至少 49/55** |

## 回归套件（企业分层）

| 套件 | 范围 | 门槛 | 场景 |
|---|---|---|---|
| **Smoke** | B01–B08 + 核心 P1 20 条 | P0 8/8；核心 P1 ≥17/20 | 日常 PR、AI 快速回归 |
| **Security** | B06、B21、B26、B31、B34、B39、B40、B43、B44、B45、B52、B53 | 建议 12/12 | 鉴权 / 安全 / 隐私 / 外部集成 PR |
| **Contract** | B03、B11、B25、B47、B51 | 建议 5/5 | OpenAPI / 事件契约 / 幂等头 PR |
| **Business Extension** | B55–B63 | 建议 9/9 | 成熟后台新增业务 / CRUD / 树表主子表 / CodeGen PR |
| **Full** | B01–B63 | P0 8/8；P1 ≥49/55 | **发版**、规则包升级、大版本 |

索引（不复制正文）：`smoke-prompts.md`（**不计入** `### Bxx` 提示词计数；校验见 `scripts/validate-rules-package.py`）。

### 核心 P1（= Smoke 中的 20 条）

B09、B11、B21、B25、B27、B28、B29、B31、B34、B36、B39、B40、B43、B44、B45、B48、B51、B52、B55、B58。

发版前仍须跑 **Full**（B01–B63）。

### 与前端 Business Extension 对照（联调 / 双端 PR）

| 后端 | 前端 | 主题 |
|---|---|---|
| B55 | E32 | 不污染公共 / 壳层 |
| B56 | E33 | 复用平台菜单 / 权限 / 字典 |
| B57 | E34 | CodeGen 后须补齐 |
| B58 | E35 | 列表 / 详情 / 导出权限一致 |
| B59 | E36 | 导出审计与下载鉴权 UI |
| B60 | E37 | 导入任务状态，禁止伪造成功 |
| B61 | E38 | 树表父节点禁选非法项 |
| B62 | E39 | 主子表失败态与回滚一致 |
| B63 | E40 | 禁止改 generator 全局 Vue 模板 |

双端新增业务、树表、主子表、导入导出或 CodeGen PR 必须同时跑 B55–B63 与 E32–E40；仅 Smoke 不代表该场景已回归。

## 用例说明（部分重叠）

| 用例 | 侧重点 |
|---|---|
| B28 vs B36 | B28：事务内同步外部调用；B36：Feign/HTTP 超时与重试边界 |
| B18 并发 vs B38 | B18：方言/SQL 登记；B38：分布式锁释放须校验 owner token |
| B29 vs B31 | B29：测试连生产库；B31：fixture PII、缓存 key 明文等隐私生命周期 |
| B43 vs B45 | B43：高风险入口威胁建模；B45：服务间机器身份认证 |
| B44 vs B37 | B44：密码/Token/密钥；B37：普通配置外部化 |
| B27 vs B52 | B27：审计字段；B52：对象级授权（BOLA/IDOR） |
| B28 vs B53 | B28：事务内外部调用；B53：用户可控 URL 出站（SSRF） |
| B39 vs B54 | B39：限流；B54：metric 高基数 label |
| B55 vs B32 | B55：业务模块污染公共层；B32：公共架构变更治理 |
| B57 vs B11 | B57：CodeGen 后补齐平台能力；B11：OpenAPI 先行 |
| B61 vs B21 | B61：树表父子租户 / 数据权限；B21：列表多租户条件 |
| B62 vs B05 | B62：主子表事务与孤儿数据；B05：写操作事务边界 |
| B63 vs B32 | B63：generator 全局模板；B32：公共架构变更治理 |
