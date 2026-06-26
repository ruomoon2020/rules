# 规则例外与豁免流程

> 大厂规则体系须同时回答：**谁可以破例、破多久、谁承担风险、如何复查**。适用于技术规则、性能预算、CI 门禁、安全策略的临时例外。

## 原则

1. **默认遵守** `shared/00` 与各端 DoD（见 [`definition-of-done.md`](definition-of-done.md)）。
2. 例外须**书面记录**、**限时**、**有 Owner**，禁止口头永久豁免。
3. 能加补偿控制就不裸豁免（如 WAF、限流、审计、feature flag）。

---

## 豁免单模板

在业务仓 `docs/exceptions/` 或工单系统创建记录，建议字段：

| 字段 | 说明 |
|---|---|
| **ID** | `EXC-YYYY-NNN` |
| **规则 / 门禁** | 如「前端 LCP P75 > 2.5s」「跳过 dependency-check 一次」 |
| **原因** | 业务背景、技术约束 |
| **范围** | 模块 / 路由 / 依赖 / 环境 |
| **申请人** | 开发负责人 |
| **风险接受人** | 须 ≥ Team Lead 或领域 Owner |
| **补偿控制** | 监控、限流、人工复核、feature flag |
| **有效期** | 起止日期；**默认 ≤ 90 天** |
| **复查日** | 到期前 7 天必须复查 |
| **是否 ADR** | 架构级例外须链到 ADR（`30-ownership-adr`） |
| **关闭条件** | 量化指标或交付物 |

### 示例

```markdown
## EXC-2026-012 — 报表页 LCP 超预算

- 规则：`web-front/rules/shared/07-security-performance.md` LCP P75 ≤ 2.5s
- 原因：首屏 10 万行聚合表，虚拟滚动改造排期 Q3
- 范围：`/report/sales` 只读页
- 风险接受人：@frontend-lead
- 补偿：路由级懒加载 + 错误率告警 + 仅内网角色可访问
- 有效期：2026-06-01 ~ 2026-08-31
- 复查：2026-08-24
- ADR：ADR-0042-report-virtual-scroll
```

---

## 审批矩阵

| 例外类型 | 最低审批 | 是否 ADR | 是否安全 Review |
|---|---|---|---|
| 代码风格 / lint 单条 | Tech Lead | 否 | 否 |
| 性能预算（单页 / 单接口） | 领域 Owner + 前端/后端 Owner | 建议 | 否 |
| 跳过测试 / 降低覆盖率 | QA Owner + Tech Lead | 是 | 否 |
| 安全门禁（secret/CVE/许可证） | 安全 Owner | **是** | **是** |
| 生产数据 / 手工 SQL | DBA + 数据 Owner | 是 | 视数据级别 |
| 公共模块 / `common` / 规则包 | 架构 Owner | **是** | 视场景 |
| CI Required 变 Optional | DevOps + 架构 | **是** | 视门禁类型 |

---

## 与现有规则的关系

| 已有片段 | 本流程统一 |
|---|---|
| `07-security-performance` 超预算说明 | 须填豁免单 |
| `30-ownership-adr` | 架构例外 = ADR + 豁免单 |
| `31-production-data-ops` | 生产数据 = 工单 + 豁免单字段 |
| `20-dependency-governance` CVE 无法修复 | 风险登记 = 豁免单 |

---

## 禁止

- 无有效期、无复查日的「永久豁免」
- 用 `// eslint-disable` 批量关闭规则且无跟踪单
- 安全 Critical 未缓解即上线
- 多人共用的豁免单无明确 Owner

## 复查与关闭

1. **复查日**到期：续期须重新审批；否则恢复默认规则。
2. **关闭**：PR 合并修复项后，在豁免单标记 `Closed` 并链到修复 PR；监管相关须同步 [`compliance-evidence-log.md`](compliance-evidence-log.md)。
3. **季度审计**：架构 / 安全每季度导出未关闭豁免清单审查。
