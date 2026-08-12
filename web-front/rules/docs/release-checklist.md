# 前端发布与回滚 Checklist

> 这是业务项目发布证据模板；规则包自身发版使用根 `RELEASE.md`。

## 发布前

- [ ] lockfile 已提交，生产构建使用固定 Node.js / pnpm 与 frozen install
- [ ] lint、type-check、test、build、api check 已运行；未配置项已说明
- [ ] API breaking change 有兼容窗口、消费方确认和回滚顺序
- [ ] bundle 增量未超预算，或已有 Owner、原因和复测日期
- [ ] 生产 sourcemap 不公开；错误平台上传步骤已验证
- [ ] Feature Flag 有 Owner、默认值、观察指标、清理日期和失败回退值
- [ ] 受监管 Web 场景已验证生产响应头、第三方脚本数据流、嵌入通信来源和 Enterprise Hardening E44–E49
- [ ] 新增数据展示、复制、下载、缓存或埋点已按分级检查
- [ ] 发布版本、Git commit、变更范围和回滚版本可追溯

## 灰度与观察

- [ ] 定义灰度范围、观察窗口、停止条件和决策 Owner
- [ ] 观察 JS 错误率、白屏率、API 失败率及关键业务成功率
- [ ] 核心页面检查登录过期、路由 chunk 失败和错误恢复
- [ ] 高峰期、结算窗口或重大活动的发布冻结策略已确认

## 回滚

- [ ] 上一版本静态资源 / 镜像仍可部署
- [ ] 旧前端可兼容当前后端契约和 schema
- [ ] 缓存、service worker、CDN 入口 HTML 的回退策略已验证
- [ ] 回滚后重新检查错误率、白屏率和关键业务链路

发布失败、回滚或临时绕过门禁时，按 common governance 的豁免与事故流程留痕。
