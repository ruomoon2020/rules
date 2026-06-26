# 03 Vue3 TypeScript uni-app

## 基础

1. Vue 文件必须使用 `<script setup lang="ts">`。
2. TypeScript 必须开启 strict；禁止显式 `any`。
3. props、emits、slots 必须显式类型。
4. computed 不得产生副作用；副作用放入事件或生命周期。
5. 禁止在模板中写复杂表达式；复杂逻辑放 computed 或函数。

## uni-app 约束

1. 使用 `uni-*` 能力前先确认平台兼容性。
2. 条件编译只允许出现在 adapter 或极少量入口文件；页面内不得密集出现。
3. 生命周期逻辑必须短小，复杂流程交给 composable / service。
4. 不直接操作 DOM；优先使用 uni-app 与小程序能力。
5. 不依赖浏览器专属 API，除非明确只在 H5 条件编译内使用。

## 类型与 generated

1. API request / response 类型来自 generated。
2. 外部参数、scene、二维码参数先用 `unknown` 接收，再校验为内部类型。
3. 支付、金额、时间、状态字段必须使用明确类型，禁止用宽泛 `string` 混过。
