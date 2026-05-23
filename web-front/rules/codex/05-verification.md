# Codex Verification Rules

收尾前必读 **`rules/shared/10-verification-checklist.md`**（与 Cursor Review 共用）。

## 命令

运行项目实际存在的 scripts，例如：

```bash
pnpm lint
pnpm type-check
pnpm test
pnpm build
pnpm api:check
```

不存在则说明未配置，不得伪造通过。

## 最终回复

- 改了什么、哪些文件
- 运行了哪些命令及结果
- 未运行的命令及原因
