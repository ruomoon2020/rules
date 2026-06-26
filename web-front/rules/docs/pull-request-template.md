# 前端 Pull Request 模板

## 变更

- [ ] 页面 / 组件 / 契约 / 平台边界改动范围：
- [ ] 是否涉及菜单、路由、权限、字典、导入导出或异步任务：

## 契约与安全

- [ ] 字段来自 schema / generated；未手改 generated
- [ ] 后端鉴权与前端权限展示一致
- [ ] 无密钥、生产地址、未脱敏敏感信息

## 验证

- [ ] `pnpm lint`
- [ ] `pnpm type-check`
- [ ] `pnpm test`
- [ ] `pnpm build`
- [ ] `pnpm api:check`（若适用）
- [ ] Rules eval（Smoke / Business Extension / Full）：
