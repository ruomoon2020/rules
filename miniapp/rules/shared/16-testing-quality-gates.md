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

## 组件测试规范

1. Base 组件覆盖默认渲染、关键 props、emits payload、slots、`v-model`、禁用/加载/错误状态和主要交互。
2. Vue Test Utils 按用户可见行为断言，优先通过文本、可访问名称或稳定 `data-testid` 查询。
3. uni API、时间、网络和随机数可注入或 mock；每个用例后恢复 timer、mock、EventBus 和全局监听。
4. Provide/Inject 覆盖有 provider 与缺少 provider 的路径；Pinia 组件使用独立 testing store。
5. 生命周期测试覆盖监听注册/注销、异步竞态、卸载后不更新和 KeepAlive 激活/停用（若使用）。
6. 快照只用于稳定、低变化结构或主题变量输出，并配合行为断言；快照变化必须人工审阅。
7. 组件 bug 先补复现测试；新增 Base 组件需要测试，例外记录 Owner 和到期时间。

推荐 Vitest + Vue Test Utils；小程序环境使用项目统一的 uni API mock 或 adapter 替身。E2E 工具由项目覆盖层按目标平台选择。

### 快照测试

快照仅作为行为测试的补充；保持结构小而稳定，变更必须人工审阅，不为通过 CI 盲目更新。

## 覆盖与稳定性

1. 覆盖率阈值由项目覆盖层定义，同时关注 statements / branches / functions / lines。
2. 核心 Base 组件、登录、权限、提交与支付链路的分支覆盖不低于项目全局阈值。
3. flaky test 应固定时钟、网络、数据和平台版本后修复，不以增加重试掩盖。
4. E2E 至少覆盖主成功、拒绝/失败和弱网恢复链路；交易使用沙箱或后端 mock。

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
6. AI / 工具输出须核对不可信内容、最小权限、外部写入授权、敏感数据出站和真实执行证据（`17`）。
7. 修改 Base 组件时运行组件测试；修改主题基础值时运行主题/关键组件测试和目标平台视觉验证。
8. CI 分离快速门禁与构建/E2E；必需 job 返回确定状态，不允许失败后仍视为通过。
