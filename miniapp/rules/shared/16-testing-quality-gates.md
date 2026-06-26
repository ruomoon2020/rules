# 16 Testing Quality Gates

## 必跑检查

按项目实际脚本运行；不存在时如实说明。

```bash
pnpm lint
pnpm type-check
pnpm test
pnpm build:mp-weixin
pnpm api:check
pnpm size:check
pnpm audit
```

## 测试分层（金字塔）

| 层级 | 范围 | 工具建议 |
|---|---|---|
| 单测 | `assertAllowedUrl`、金额工具、scene 解析、composables | Vitest |
| 集成 | request 封装、auth logout 清理、错误 recovery | Vitest + mock uni |
| E2E | 登录 → 列表 → 下单沙箱（支付 mock） | miniprogram-automator / 云测 |
| 契约 | OpenAPI vs generated | `api:check` |

## 测试重点

1. 登录态：未登录、过期、刷新失败、退出登录。
2. 授权：拒绝、再次授权、平台不可用。
3. 分页：刷新、加载更多、筛选变化、删除末条。
4. 支付：成功、取消、失败、处理中、重复点击。
5. 分享：参数校验、分享打开、非法 scene。
6. 分包：页面可进入、公共依赖不越界、主包体积不超预算。
7. 隐私：实际调用能力和隐私说明一致。
8. 弱网/错误恢复：offline 提示、重试、登录过期统一跳转（`22`）。
9. 富文本/UGC：消毒或拒绝不可信 HTML（`23`）。

## CI 门禁

1. lint / type-check / build 必须在 PR 运行。
2. API 契约变化必须跑 generated 与 api check。
3. 主包体积超过阈值必须失败或要求人工审批。
4. 生产构建不得包含 mock、console、调试入口。
5. 建议 `pnpm audit` 无高危漏洞或经审批例外（`25`）。
