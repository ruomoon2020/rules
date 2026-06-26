# Rules Package Alignment Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Eliminate confirmed P0 rule-package drift and make cross-package links and eval semantics mechanically verifiable.

**Architecture:** Keep package content as the source of truth.  Extend the existing Python validators with focused checks rather than introducing a new runtime.  Give the frontend a small local contract summary that links to the backend SSOT, and document deliberately asymmetric rule numbers in that SSOT.

**Tech Stack:** Markdown, Cursor MDC, Python standard library `unittest`.

---

### Task 1: Regression tests for validator helpers

**Files:**
- Create: `web-backend/rules/scripts/tests/test_validate_rules_package.py`
- Create: `web-front/rules/scripts/tests/test_validate_rules_package.py`
- Modify: `web-backend/rules/scripts/validate-rules-package.py`
- Modify: `web-front/rules/scripts/validate-rules-package.py`

- [x] Add failing tests for a mismatched eval topic, a bare Cursor shared reference, and a missing reverse cross-package reference.
- [x] Run the tests and confirm they fail because the helpers do not exist.
- [x] Add the smallest reusable helper functions and wire them into each validator.
- [x] Run the unit tests and each package validator.

### Task 2: Repair confirmed P0 references

**Files:**
- Modify: `web-backend/rules/evals/rubric.md`
- Modify: `web-backend/rules/cursor/04-rest-controller.mdc`
- Modify: `web-backend/rules/cursor/08-exception-logging.mdc`
- Modify: `web-front/rules/README.md`
- Modify: `web-front/rules/codex/AGENTS.md`

- [x] Align B19's topic and pass criterion with its prompt.
- [x] Use package-root paths in Cursor summaries.
- [x] Repair the frontend's cross-package fullstack-contract reference.
- [x] Standardize the documented frontend shell directory on `src/layouts/**`.

### Task 3: Frontend independent-consumption minimum

**Files:**
- Create: `web-front/rules/docs/fullstack-contract.md`
- Modify: `web-backend/rules/docs/fullstack-contract.md`
- Modify: `web-front/rules/shared/22-business-module-extension.md`
- Create: `web-front/rules/cursor/19-platform-boundary.mdc`

- [x] Add a concise frontend contract summary that names the backend document as the complete SSOT.
- [x] Add a cross-package asymmetric-number mapping to the backend SSOT.
- [x] Add missing frontend platform-boundary, data-permission UI, and async-job UI constraints to shared/22.
- [x] Add a narrowly scoped Cursor trigger for platform-owned frontend surfaces.

### Task 4: Verify and record scope

**Files:**
- Modify: `docs/superpowers/plans/2026-06-27-rules-package-alignment.md`

- [x] Run unit tests and all three package validators.
- [x] Mark completed plan steps and record intentionally deferred P2 subjects: OAuth/OIDC, cache/replica, resilience, i18n, streaming, and OWASP-web mapping.

## Deferred P2 adoption roadmap

These topics remain deliberately unimplemented because they need the consuming team's stack and threat model: OAuth2/OIDC token lifecycle and revocation, read/write replica routing and cache failure modes, Resilience4j conventions, i18n/locale, WebSocket/SSE, and OWASP Web mapping.  Adopt each only with a project-specific decision record, concrete verification command, and a corresponding eval or example.
