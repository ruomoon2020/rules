# 04 Page UI Lifecycle

> 应用级 `onLaunch` / 全局错误 / `scene` 见 `20-app-runtime.md`。弱网与统一 error 恢复见 `22-error-recovery-offline.md`。本文仅约束**页面**生命周期。

## 页面骨架

页面建议按以下顺序组织：

1. 导航 / 标题 / 安全区。
2. 核心状态：loading、error、empty、content。
3. 表单 / 列表 / 卡片。
4. 底部操作区。
5. 授权、登录、支付、分享等弹层。

## 生命周期

1. `onLoad`：解析路由参数、初始化页面级不可变上下文。
2. `onShow`：处理返回刷新、登录态恢复、订单状态刷新。
3. `onPullDownRefresh`：只做刷新，不改变筛选条件。
4. `onReachBottom`：只触发下一页加载，须防重复触发。
5. `onHide`：暂停轮询、上报停留时长。
6. `onUnload`：清理 timer、事件监听、长连接、未完成任务。

## 禁止

- 禁止在 `onShow` 无条件重复拉取所有接口。
- 禁止在 `onLoad` 同步处理大数组或大 JSON。
- 禁止把授权弹窗、登录弹窗、业务弹窗互相嵌套成不可恢复状态。
- 禁止忽略页面栈，反复 `navigateTo` 导致返回链路异常。
