# 02 Naming

## 文件与目录

1. 目录使用 kebab-case：`subpackages/order-detail/`。
2. 页面文件使用 `index.vue`，页面目录表达语义：`pages/home/index.vue`。
3. 组件文件使用 PascalCase：`BaseSafeArea.vue`、`OrderCard.vue`。
4. composable 使用 `useXxx.ts`：`useOrderList.ts`。
5. service 使用领域名：`order.service.ts`、`payment.service.ts`。
6. platform adapter 使用能力名：`payment.adapter.ts`、`share.adapter.ts`。
7. storage key 统一在 `stores/` 或 `auth/keys.ts` 管理，禁止散落字符串。

## 变量与类型

1. 类型 / interface 使用 PascalCase：`OrderListItem`、`LoginSession`。
2. enum 或常量对象使用业务语义：`OrderStatus`、`PaymentChannel`。
3. API 方法使用动词开头：`fetchOrderPage`、`submitOrder`、`queryPaymentStatus`。
4. boolean 使用 `is/has/can/should` 前缀。
5. 事件名使用 kebab-case：`update:model-value`、`submit-success`。

## 小程序命名

1. 页面路由 path 必须稳定，不因标题变化而重命名。
2. 分包 root 使用业务域：`subpackages/order`、`subpackages/member`。
3. 订阅消息模板、支付场景、分享来源须有枚举或常量，不得使用魔法字符串。
