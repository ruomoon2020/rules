# Codex API 与 Schema 规则

Use this when editing API files, request wrappers, schema, generated clients, or pages that depend on API fields.

Also read `rules/shared/12-schema-ssot.md`.

## Source of Truth

Use this order:

```text
contracts/schema.json
  -> src/api/generated
  -> src/api/* thin wrappers
  -> views / components
```

## Editing Rules

1. Do not manually edit `src/api/generated`.
2. If generated types are wrong, update the contract source and regenerate.
3. Keep handwritten API files thin; they compose generated clients and add business-friendly names.
4. Keep request interceptors responsible for token, traceId, error normalization, and download handling.
5. Do not show UI messages from the low-level API layer.

## Schema Change Review

When schema changes, inspect:

- removed fields
- renamed fields
- required field changes
- enum additions or removals
- response wrapper changes
- pagination shape changes

Breaking changes require migration notes and rollback awareness.

## Commands

Run when available:

```bash
pnpm schema:sync
pnpm api:gen
pnpm api:check
pnpm type-check
```

If a command is missing, report that the project has not wired the corresponding gate yet.
