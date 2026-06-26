# 测试规则

## 单元测试

1. 覆盖 `utils`、复杂 `composable`、带逻辑的 business 组件。
2. 不测试样式快照替代业务逻辑（除非项目有视觉回归约定）。
3. API 层 mock 使用 fixture，不依赖生产数据。
4. composable 测行为和边界，不测试内部实现细节。
5. request wrapper / API 层须测错误归一化、traceId、重试与取消逻辑。

## 组件测试

1. Base 组件测交互与 a11y 关键路径（label、键盘）。
2. 页面测筛选、提交、权限隐藏等核心分支。
3. 表单组件测必填、枚举、异步校验、提交失败保留输入。
4. 表格 / 列表测分页回退、selection 清理、error 重试。

## E2E

1. 核心链路：登录 → 列表 → 新增/编辑 → 登出。
2. 环境账号与数据隔离，见 `08-quality-gates.md`。
3. CI 独立配置，不 flaky 依赖本地状态。
4. E2E 文件使用 `.e2e.ts`；按业务链路命名，如 `system-user.e2e.ts`。
5. 关键链路失败时，保留 trace、截图、视频或日志（按项目配置）。

## Accessibility 自动化

1. 关键页面建议接入 axe / Playwright a11y / 项目等价检查。
2. 纯图标按钮、表单 label、Modal 焦点、键盘操作应有自动化或最小手工记录。
3. a11y 失败若影响主流程操作，应阻断发布。

## 导入导出测试

1. 导入测试覆盖模板字段、必填、枚举、日期、金额、错误明细。
2. CSV / Excel 导出测试覆盖公式注入转义、敏感字段脱敏。
3. 高风险导入测试覆盖幂等、预览确认、重复提交。

## 与契约

- schema / API 变更后跑 `api:check` 与相关单测。
- 破坏性变更须更新 E2E 或注明跳过原因。

## 命令

以项目 `package.json` 为准，常见：

```bash
pnpm test
pnpm test:unit
pnpm test:e2e
pnpm test:a11y
```

门禁汇总见 `08-quality-gates.md`、`10-verification-checklist.md`。
