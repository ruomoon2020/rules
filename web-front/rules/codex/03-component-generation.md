# Codex Component Generation Rules

Use this when creating or modifying shared or business components.

## Component Categories

| Category | Location | Rule |
|---|---|---|
| Base UI | `src/components/base` | Business independent |
| Business component | `src/components/business` or feature-local | May know business concepts |
| Page-local component | `src/views/**/components` | Used by one page or module |

## Base Components

1. Do not depend on business API, business store, route-specific logic, or business fields.
2. Props, emits, and slots must be typed and documented.
3. Support common states: loading, disabled, readonly, empty, error where relevant.
4. Use design tokens, not hardcoded theme values.
5. Meet accessibility rules for keyboard and labels.
6. Breaking changes require migration notes.

## Business Components

1. Keep module-specific logic close to the module.
2. Do not move one-off page code into global components.
3. If reused by multiple pages, document inputs and outputs.

## Verification

Run component tests if configured. For visual components, also inspect affected pages or visual regression output when available.

