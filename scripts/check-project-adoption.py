#!/usr/bin/env python3
"""Check business project adoption of code-rules packages.

Usage:
  python scripts/check-project-adoption.py --repo . --stack backend,frontend
  python scripts/check-project-adoption.py --repo ./my-frontend --stack frontend

Exit 0 if all required checks pass; 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REQUIRED_BACKEND_SCRIPTS = ("verify", "test")
REQUIRED_FRONTEND_SCRIPTS = ("lint", "type-check", "build")
REQUIRED_MINIAPP_SCRIPTS = ("lint", "type-check", "build:mp-weixin")


def check_exists(repo: Path, rel: str, errors: list[str], label: str) -> bool:
    path = repo / rel
    if not path.exists():
        errors.append(f"MISSING {label}: {rel}")
        return False
    return True


def check_agents(repo: Path, errors: list[str]) -> None:
    agents = repo / "AGENTS.md"
    if not agents.is_file():
        errors.append("MISSING AGENTS.md at repository root")
        return
    text = agents.read_text(encoding="utf-8")
    if "rules/" not in text and "rules/shared" not in text:
        errors.append("AGENTS.md should reference rules/ paths")


def check_cursor_rules(repo: Path, errors: list[str]) -> None:
    cursor_dir = repo / ".cursor" / "rules"
    if not cursor_dir.is_dir():
        errors.append("MISSING .cursor/rules/ directory")
        return
    mdc_files = list(cursor_dir.glob("*.mdc"))
    if not mdc_files:
        errors.append("MISSING .cursor/rules/*.mdc (copy from rules/cursor/)")
    overview = cursor_dir / "00-project-overview.mdc"
    if not overview.is_file():
        errors.append("MISSING .cursor/rules/00-project-overview.mdc")


def check_rules_package(repo: Path, errors: list[str]) -> None:
    rules = repo / "rules"
    if not rules.is_dir():
        errors.append("MISSING rules/ directory (submodule or copy)")
        return
    version = rules / "VERSION"
    if not version.is_file():
        errors.append("MISSING rules/VERSION")
    agents = rules / "codex" / "AGENTS.md"
    if not agents.is_file():
        errors.append("MISSING rules/codex/AGENTS.md")
    shared = rules / "shared" / "00-must-follow.md"
    if not shared.is_file():
        errors.append("MISSING rules/shared/00-must-follow.md")


def check_contracts(repo: Path, errors: list[str], required: bool) -> None:
    candidates = [
        repo / "contracts" / "openapi.yaml",
        repo.parent / "contracts" / "openapi.yaml",
    ]
    if any(p.is_file() for p in candidates):
        return
    if required:
        errors.append("MISSING contracts/openapi.yaml (SSOT)")


def check_codeowners(repo: Path, errors: list[str], strict: bool) -> None:
    paths = [repo / "CODEOWNERS", repo / ".github" / "CODEOWNERS"]
    if not any(p.is_file() for p in paths):
        msg = "MISSING CODEOWNERS (see docs/codeowners-matrix.md)"
        if strict:
            errors.append(msg)
        else:
            print(f"WARN: {msg}")


def check_pr_template(repo: Path, errors: list[str], strict: bool) -> None:
    paths = [
        repo / ".github" / "pull_request_template.md",
        repo / ".github" / "PULL_REQUEST_TEMPLATE.md",
        repo / "docs" / "pull-request-template.md",
    ]
    if not any(p.is_file() for p in paths):
        msg = "MISSING PR template (copy from rules/docs/pull-request-template.md)"
        if strict:
            errors.append(msg)
        else:
            print(f"WARN: {msg}")


def check_package_json_scripts(repo: Path, errors: list[str], required: tuple[str, ...]) -> None:
    pkg = repo / "package.json"
    if not pkg.is_file():
        errors.append("MISSING package.json")
        return
    data = json.loads(pkg.read_text(encoding="utf-8"))
    scripts = data.get("scripts") or {}
    for name in required:
        if name not in scripts:
            errors.append(f"package.json missing script: {name}")


def check_pom(repo: Path, errors: list[str]) -> None:
    pom = repo / "pom.xml"
    if not pom.is_file():
        errors.append("MISSING pom.xml for backend project")
        return
    text = pom.read_text(encoding="utf-8")
    if "maven-surefire-plugin" not in text and "spring-boot" not in text:
        print("WARN: pom.xml may lack standard test/build plugins")


def check_local_override(repo: Path, errors: list[str]) -> None:
    local = repo / ".cursor" / "rules" / "99-project-local.mdc"
    if not local.is_file():
        print("WARN: missing .cursor/rules/99-project-local.mdc (project paths)")


def run_stack(repo: Path, stack: str, strict: bool) -> list[str]:
    errors: list[str] = []
    check_agents(repo, errors)
    check_rules_package(repo, errors)
    check_cursor_rules(repo, errors)

    if stack == "backend":
        check_pom(repo, errors)
        check_contracts(repo, errors, required=True)
    elif stack == "frontend":
        check_package_json_scripts(repo, errors, REQUIRED_FRONTEND_SCRIPTS)
        check_contracts(repo, errors, required=False)
    elif stack == "miniapp":
        check_package_json_scripts(repo, errors, REQUIRED_MINIAPP_SCRIPTS)
        check_contracts(repo, errors, required=True)
    else:
        errors.append(f"Unknown stack: {stack}")

    check_codeowners(repo, errors, strict)
    check_pr_template(repo, errors, strict)
    check_local_override(repo, errors)
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path("."), help="Business repository root")
    parser.add_argument(
        "--stack",
        default="frontend",
        help="Comma-separated: backend, frontend, miniapp",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat CODEOWNERS / PR template as required",
    )
    args = parser.parse_args()
    repo = args.repo.resolve()
    if not repo.is_dir():
        print(f"Not a directory: {repo}", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for stack in [s.strip() for s in args.stack.split(",") if s.strip()]:
        print(f"=== Checking {stack} @ {repo} ===")
        all_errors.extend(run_stack(repo, stack, args.strict))

    if all_errors:
        print("\nFAILED:")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print("\nOK: project adoption checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
