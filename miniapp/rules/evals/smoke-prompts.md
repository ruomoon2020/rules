# Evals 套件索引（非独立提示词）

> 正文均在 `prompts.md`；本文件仅定义**套件范围**与**门槛**，避免复制导致 drift。
>
> **维护说明**：本文件是**索引**，不要用 `### Mxx` 标题（否则自动计数脚本会误判为提示词正文）。
> 发版校验时：只检查此处引用的 **M 编号是否都在 `prompts.md` 存在**，**不计入**提示词条数。
> 自动化：`python scripts/validate-rules-package.py`（见 `docs/contributing-rules-package.md`）。

## Smoke（日常）

| ID | 章节 |
|---|---|
| M01–M08 | P0 全量 |
| M09 | 新依赖 |
| M11 | logout 清理 |
| M13 | 验证命令 |
| M14 | 分包依赖 |
| M15 | 金额精度 |
| M16 | 主包体积 |
| M17 | platform adapter |
| M18 | 列表四态 |
| M19 | 离页清理 |
| M20 | pages.json |

**门槛**：P0 **8/8**；上表 P1 **>= 10/12** Pass。

## Security（隐私 / 分享 / 日志 / App·网络·环境 PR）

M06、M07、M12、M18、M30、M31、M32、M33、M34

**门槛**：建议 **9/9** Pass。

## Contract（OpenAPI / generated / 支付契约 PR）

M03、M05、M08、M15

**门槛**：建议 **4/4** Pass。

## Business Extension（新业务分包 PR）

M21、M22、M23、M24、M25、M26、M27、M28、M29

**门槛**：建议 **9/9** Pass。

## Resilience（错误恢复 / UGC / 可观测 PR）

M35、M36、M37、M38

**门槛**：建议 **4/4** Pass。

## Full（发版 / 规则包升级）

M01–M38，见 `prompts.md` 全文。

**门槛**：P0 **8/8**；核心 P1 **>= 10/12**；Security / Resilience Extension 建议满配（见 `rubric.md`）。
