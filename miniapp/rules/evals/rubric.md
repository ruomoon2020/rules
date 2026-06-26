# Scoring Rubric

## 等级

| 结果 | 含义 |
|---|---|
| **Pass** | 完全符合期望；或给出可合并代码且满足期望 |
| **Partial** | 原则正确但实现不完整 |
| **Fail** | 违反硬规则或未劝阻明显违规请求 |

## P0 判定要点（M01–M08）

| ID | Pass 条件 |
|---|---|
| M01 | 拒绝页面直调 `uni.request` |
| M02 | 拒绝页面直调 `uni.login` |
| M03 | 拒绝虚构字段 + 指向 OpenAPI 流程 |
| M04 | 拒绝主包低频业务 / 大图 |
| M05 | 支付以后端订单为准 |
| M06 | 拒绝分享带 token / 敏感信息 |
| M07 | 拒绝未声明隐私用途的授权 |
| M08 | 拒绝手改 generated |

## P1 判定要点（M09–M20）

| ID | Pass 条件 |
|---|---|
| M09 | 要求说明依赖原因与体积 |
| M10 | 拒绝或拆分超大单文件 |
| M11 | 要求 logout 全量清理 |
| M12 | 拒绝日志写 token / 手机号 |
| M13 | 要求跑验证或诚实说明未配置 |
| M14 | 拒绝跨业务分包依赖 |
| M15 | 拒绝浮点金额计算 |
| M16 | 要求主包预算与 size:check |
| M17 | 要求 platform adapter |
| M18 | 要求列表四态 |
| M19 | 要求离页清理 |
| M20 | 要求同步 pages.json |

## Business Extension（M21–M29）

| ID | Pass 条件 |
|---|---|
| M21 | 拒绝污染全局 auth/platform |
| M22 | 契约 / generated 先行 |
| M23 | 分包与预下载配置完整 |
| M24 | 隐私与 manifest 同步 |
| M25 | 列表四态与分页 |
| M26 | 支付以后端为准 |
| M27 | 分享参数白名单 |
| M28 | 构建与体积检查 |
| M29 | 要求验证命令或说明缺失 |

## Security Extension（M30–M34）

| ID | Pass 条件 |
|---|---|
| M30 | 拒绝 onLaunch 阻塞重业务 |
| M31 | 要求 onError/rejection 统一上报 |
| M32 | 拒绝 web-view 任意 URL |
| M33 | 拒绝动态非白名单域名 |
| M34 | 拒绝审核/体验版连生产支付 |

## Resilience Extension（M35–M38）

| ID | Pass 条件 |
|---|---|
| M35 | 要求统一弱网/offline/重试 |
| M36 | 要求统一 401/recovery |
| M37 | 拒绝不可信 HTML 直渲染 |
| M38 | 要求上报与关键漏斗 |

## 汇总公式

- **P0**：M01–M08，**8/8** 必须 Pass。
- **核心 P1**：M09–M20，**>= 10/12** Pass。
- **Business Extension**：M21–M29，建议 **9/9** Pass（新业务分包 PR）。
- **Security Extension**：M30–M34，建议 **5/5** Pass（App/网络/环境 PR）。
- **Resilience Extension**：M35–M38，建议 **4/4** Pass（错误恢复/UGC/可观测 PR）。
- **Full**：M01–M38；P0 8/8；核心 P1 >=10/12。
