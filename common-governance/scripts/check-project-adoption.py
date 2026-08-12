#!/usr/bin/env python3
"""Check business project adoption of code-rules packages.

Usage:
  python scripts/check-project-adoption.py --repo ./my-frontend --stack frontend
  python common-governance/scripts/check-project-adoption.py --repo . --stack backend --strict --require-governance

Exit 0 if all required checks pass; 1 otherwise.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

REQUIRED_BACKEND_SCRIPTS = ("verify", "test")
REQUIRED_FRONTEND_SCRIPTS = ("lint", "type-check", "build")
REQUIRED_MINIAPP_SCRIPTS = ("lint", "type-check", "build:mp-weixin")
GOVERNANCE_REQUIRED_FILES = (
    "README.md",
    "CHANGELOG.md",
    "VERSION",
    "docs/adoption-scorecard.md",
    "docs/branch-protection.md",
    "docs/codeowners-matrix.md",
    "docs/compliance-evidence-log.md",
    "docs/data-classification-matrix.md",
    "docs/definition-of-done.md",
    "docs/dod-maturity-mapping.md",
    "docs/git-pr-governance.md",
    "docs/rule-exception-process.md",
    "docs/slo-alerting-template.md",
    "docs/supply-chain-baseline.md",
    "examples/commitlint.config.cjs.sample",
    "examples/pull_request_template.md",
    "examples/SECURITY.md.sample",
    "examples/adr-template.md",
    "examples/ci/credential-scan-required.yml",
    "examples/ci/supply-chain-required.yml",
    "scripts/check-project-adoption.py",
    "scripts/validate-package.py",
)
VERSION_HEADING = re.compile(r"^##\s+([^\s]+)", re.MULTILINE)


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


def _is_gradle_project(repo: Path) -> bool:
    has_wrapper = (repo / "gradlew").is_file()
    has_build = (repo / "build.gradle").is_file() or (repo / "build.gradle.kts").is_file()
    return has_wrapper and has_build


def _is_maven_project(repo: Path) -> bool:
    return (repo / "pom.xml").is_file()


def check_build_tool(repo: Path, errors: list[str]) -> None:
    if _is_maven_project(repo):
        text = (repo / "pom.xml").read_text(encoding="utf-8")
        if "maven-surefire-plugin" not in text and "spring-boot" not in text:
            print("WARN: pom.xml may lack standard test/build plugins")
        return
    if _is_gradle_project(repo):
        return
    errors.append(
        "MISSING backend build file: pom.xml or Gradle wrapper (gradlew + build.gradle*)"
    )


def check_local_override(repo: Path, errors: list[str]) -> None:
    local = repo / ".cursor" / "rules" / "99-project-local.mdc"
    if not local.is_file():
        print("WARN: missing .cursor/rules/99-project-local.mdc (project paths)")


def check_governance_package(path: Path, errors: list[str], required: bool) -> None:
    findings: list[str] = []
    required_files = GOVERNANCE_REQUIRED_FILES + ("MANIFEST.json",)
    missing = [rel for rel in required_files if not (path / rel).is_file()]
    findings.extend(f"missing {rel}" for rel in missing)

    manifest_path = path / "MANIFEST.json"
    manifest: dict[str, object] = {}
    if manifest_path.is_file():
        try:
            raw_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            findings.append(f"invalid MANIFEST.json: {exc}")
        else:
            if isinstance(raw_manifest, dict):
                manifest = raw_manifest
            else:
                findings.append("MANIFEST.json root must be an object")

    files = manifest.get("files") if manifest else None
    if manifest and not isinstance(files, dict):
        findings.append("MANIFEST.json files must be an object")
    elif isinstance(files, dict):
        expected_entries = set(GOVERNANCE_REQUIRED_FILES)
        listed_entries = set(files)
        for rel in sorted(expected_entries - listed_entries):
            findings.append(f"manifest missing {rel}")
        for rel in sorted(listed_entries - expected_entries):
            findings.append(f"manifest unexpected {rel}")
        for rel, expected_hash in files.items():
            candidate = (path / rel).resolve()
            try:
                candidate.relative_to(path.resolve())
            except ValueError:
                findings.append(f"manifest path escapes package: {rel}")
                continue
            if not candidate.is_file():
                continue
            actual_hash = hashlib.sha256(candidate.read_bytes()).hexdigest()
            if actual_hash != expected_hash:
                findings.append(f"checksum mismatch {rel}")

    version_path = path / "VERSION"
    if manifest and version_path.is_file():
        version = version_path.read_text(encoding="utf-8").strip()
        if manifest.get("version") != version:
            findings.append("manifest version does not match VERSION")
        changelog_path = path / "CHANGELOG.md"
        if changelog_path.is_file():
            latest = VERSION_HEADING.search(changelog_path.read_text(encoding="utf-8"))
            if not latest or latest.group(1) != version:
                findings.append("CHANGELOG latest version does not match VERSION")

    if not findings:
        return
    message = f"common governance incomplete at {path}: {', '.join(findings)}"
    if required:
        errors.append(message)
    else:
        print(f"WARN: {message}")


def run_stack(repo: Path, stack: str, strict: bool) -> list[str]:
    errors: list[str] = []
    check_agents(repo, errors)
    check_rules_package(repo, errors)
    check_cursor_rules(repo, errors)

    if stack == "backend":
        check_build_tool(repo, errors)
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
    parser.add_argument(
        "--require-governance",
        action="store_true",
        help="Require a complete common-governance package",
    )
    parser.add_argument(
        "--governance-dir",
        type=Path,
        help="Governance package path, relative paths resolve under --repo (default: common-governance)",
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

    if args.require_governance or args.governance_dir:
        governance_dir = args.governance_dir or Path("common-governance")
        if not governance_dir.is_absolute():
            governance_dir = repo / governance_dir
        governance_dir = governance_dir.resolve()
        check_governance_package(governance_dir, all_errors, args.require_governance)

    if all_errors:
        print("\nFAILED:")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print("\nOK: project adoption checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
