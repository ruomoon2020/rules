# 17 AI Generation

## AI 写代码前

1. 先确认任务类型：页面、App 运行时、API/网络、登录态、分包、隐私、支付、分享、性能、发版环境。
2. 先读 `00-must-follow.md`，再按任务读取对应 shared。
3. 涉及字段时先读 OpenAPI / schema / generated 类型。
4. 涉及平台能力时先读 `11-platform-differences.md` 和对应能力规则。

## 禁止 AI 行为

1. 禁止虚构 API 字段、generated 类型、页面路径、分包名、`pages.json` 未登记路由。
2. 禁止为了省事直接在页面写 `uni.request`、`uni.login`、支付、订阅消息。
3. 禁止生成未声明隐私用途的授权调用。
4. 禁止无依据引入 UI 库、SDK、加密库、埋点库。
5. 禁止把 Web 管理后台规则机械套到小程序。
6. 禁止把 tabBar 页放进分包；禁止未评估体积即往主包加 SDK / 大图。
7. 禁止伪造 lint / build / api:check 通过结果。

## 生成后自检

1. 是否走统一 request / auth / platform / privacy。
2. 是否处理拒绝、失败、超时、重复点击、离页。
3. 是否影响主包体积。
4. 是否有验证命令和未验证说明。
