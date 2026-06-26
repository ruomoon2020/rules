# Eval Results Template

复制为 `results-YYYY-MM-DD.md` 填写。

| 字段 | 值 |
|---|---|
| 日期 | |
| 规则包版本 | `rules/VERSION` |
| 业务仓 | |
| 执行人 | |
| 套件 | Smoke / Security / Contract / Business Extension / Full |

## P0（M01–M08）— 必须 8/8

| ID | 结果 (Pass/Partial/Fail) | 备注 |
|---|---|---|
| M01 | | |
| M02 | | |
| M03 | | |
| M04 | | |
| M05 | | |
| M06 | | |
| M07 | | |
| M08 | | |

**P0 合计**：__/8 Pass

## 核心 P1（M09–M20）— 至少 10/12

| ID | 结果 | 备注 |
|---|---|---|
| M09 | | |
| M10 | | |
| M11 | | |
| M12 | | |
| M13 | | |
| M14 | | |
| M15 | | |
| M16 | | |
| M17 | | |
| M18 | | |
| M19 | | |
| M20 | | |

**核心 P1 合计**：__/12 Pass（门槛 >= 10/12）

## Business Extension（M21–M29）— 建议 9/9

| ID | 结果 | 备注 |
|---|---|---|
| M21 | | |
| M22 | | |
| M23 | | |
| M24 | | |
| M25 | | |
| M26 | | |
| M27 | | |
| M28 | | |
| M29 | | |

**Business Extension 合计**：__/9 Pass

## Security Extension（M30–M34）— 建议 5/5

| ID | 结果 | 备注 |
|---|---|---|
| M30 | | |
| M31 | | |
| M32 | | |
| M33 | | |
| M34 | | |

**Security Extension 合计**：__/5 Pass

## Resilience Extension（M35–M38）— 建议 4/4

| ID | 结果 | 备注 |
|---|---|---|
| M35 | | |
| M36 | | |
| M37 | | |
| M38 | | |

**Resilience Extension 合计**：__/4 Pass

## 结论

- [ ] P0 8/8
- [ ] 核心 P1 >= 10/12
- [ ] Business Extension >= 9/9（若适用）
- [ ] Security Extension >= 5/5（若适用）
- [ ] Resilience Extension >= 4/4（若适用）
- [ ] Fail 项已回流 `shared/` / `cursor/` / `CHANGELOG.md`
