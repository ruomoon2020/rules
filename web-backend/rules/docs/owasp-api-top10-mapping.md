# OWASP API Security Top 10 → 本规则包映射

> 维护者对照表；不重复条文，仅指向已有 `shared/` 与 evals。基于 [OWASP API Security Top 10](https://owasp.org/API-Security/) 常见条目。

| ID | 风险 | 本规则包落点 | Evals |
|---|---|---|---|
| API1 | Broken Object Level Authorization | `06-security-authz`（BOLA/IDOR）、`24` | B21、B34、**B52** |
| API2 | Broken Authentication | `06`、`36-crypto-key-management` | B06、B44 |
| API3 | Broken Object Property Level Authorization | `13-validation`（Mass Assignment）、`12` DTO | — |
| API4 | Unrestricted Resource Consumption | `06` 限流、`16`、`42`、`18` 幂等 | B26、B50、**B51** |
| API5 | Broken Function Level Authorization | `06` 权限码、`15` 越权测试 | B34 |
| API6 | Unrestricted Access to Sensitive Business Flows | `06`、`22`、`35-threat-modeling` | B26、B43 |
| API7 | Server Side Request Forgery | `28-external-integration`、`35` | **B53** |
| API8 | Security Misconfiguration | `06` Web 安全、`21`、`22`、`38`、`09` 可观测 | B39、B40、B46、**B54** |
| API9 | Improper Inventory Management | `30-ownership-adr`、`05` OpenAPI SSOT | B11、B25 |
| API10 | Unsafe Consumption of APIs | `28`、`20` | B28、B36、B41 |

PR 涉及上表风险时，须在描述中引用对应 shared 文件与测试/审计措施。
