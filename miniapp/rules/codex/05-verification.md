# 05 Verification

完成前检查：

1. 是否遵守 `shared/00-must-follow.md`。
2. 是否没有页面直调 `uni.request`、`uni.login`、支付、订阅消息。
3. 是否遵守域名白名单 / HTTPS / web-view 约束（`21`）。
4. `App.vue` 是否无 onLaunch 阻塞重业务；全局错误有兜底（`20`）。
5. 是否没有手写 generated 字段或改 generated 文件。
6. 是否处理登录过期、授权拒绝、弱网、超时、重复点击、离页。
7. 是否影响主包体积或分包边界。
8. 是否同步 `pages.json` / `manifest.json`。
9. 体验/审核版是否未连接生产 API 与支付（`19`）。
10. 是否清理生产 mock、console、调试入口。
11. 弱网/401 是否走统一 recovery（`22`）；富文本/UGC 是否消毒（`23`）。

按项目实际存在的脚本运行：

```bash
pnpm lint
pnpm type-check
pnpm test
pnpm build:mp-weixin
pnpm api:check
```

缺少脚本时说明“项目未配置”，不得伪造通过结果。
