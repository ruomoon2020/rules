#!/usr/bin/env python3
"""Check business project adoption of code-rules packages.

Usage:
  python scripts/check-project-adoption.py --repo ./my-frontend --stack frontend
  python common-governance/scripts/check-project-adoption.py --repo . --stack backend --strict --require-governance

Exit 0 if all required checks pass; 1 otherwise.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - environment failure path
    yaml = None

REQUIRED_FRONTEND_SCRIPTS = ("lint", "type-check", "build")
REQUIRED_MINIAPP_SCRIPTS = ("lint", "type-check", "build:mp-weixin")
REQUIRED_FRONTEND_LEVEL1_SCRIPTS = ("api:check",)
REQUIRED_MINIAPP_LEVEL1_SCRIPTS = ("api:check", "size:check")
GOVERNANCE_REQUIRED_FILES = (
    "README.md",
    "CHANGELOG.md",
    "VERSION",
    "docs/adoption-scorecard.md",
    "docs/ai-tool-security.md",
    "docs/branch-protection.md",
    "docs/business-correctness-review.md",
    "docs/codeowners-matrix.md",
    "docs/compliance-evidence-log.md",
    "docs/data-classification-matrix.md",
    "docs/definition-of-done.md",
    "docs/dod-maturity-mapping.md",
    "docs/git-pr-governance.md",
    "docs/environment-promotion.md",
    "docs/incident-response.md",
    "docs/incident-postmortem-template.md",
    "docs/release-evidence.md",
    "docs/requirements-traceability.md",
    "docs/rule-exception-process.md",
    "docs/slo-alerting-template.md",
    "docs/supply-chain-baseline.md",
    "examples/commitlint.config.cjs.sample",
    "examples/pull_request_template.md",
    "examples/SECURITY.md.sample",
    "examples/adr-template.md",
    "examples/release-evidence.yaml",
    "examples/ci/credential-scan-required.yml",
    "examples/ci/rules-adoption-required.yml",
    "examples/ci/supply-chain-required.yml",
    "examples/governance-adoption.yaml",
    "scripts/check-project-adoption.py",
    "scripts/validate-release-evidence.py",
    "scripts/validate-package.py",
)
VERSION_HEADING = re.compile(r"^##\s+([^\s]+)", re.MULTILINE)
EVIDENCE_URL = re.compile(r"https://[^\s]+$", re.IGNORECASE)
CONTRACT_DECLARATION = re.compile(
    r"(?:contract\s+path|contract\s+ssot|契约\s*(?:路径|ssot))\s*[:：]\s*`?([^`\s]+)",
    re.IGNORECASE,
)
PLACEHOLDER_SCRIPT = re.compile(r"^(?:echo\b|printf\b|true$|exit\s+0$)", re.IGNORECASE)


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


def _declared_contracts(repo: Path) -> list[Path]:
    declarations: list[Path] = []
    candidates = [repo / "AGENTS.md", repo / ".cursor" / "rules" / "99-project-local.mdc"]
    for source in candidates:
        if not source.is_file():
            continue
        for match in CONTRACT_DECLARATION.finditer(source.read_text(encoding="utf-8")):
            value = match.group(1).strip()
            if value.startswith(("http://", "https://")):
                continue
            declared = Path(value)
            declarations.append(declared if declared.is_absolute() else repo / declared)
    return declarations


def _has_external_contract_declaration(repo: Path) -> bool:
    for source in (repo / "AGENTS.md", repo / ".cursor" / "rules" / "99-project-local.mdc"):
        if not source.is_file():
            continue
        for match in CONTRACT_DECLARATION.finditer(source.read_text(encoding="utf-8")):
            if match.group(1).startswith("https://"):
                return True
    return False


def check_contracts(repo: Path, errors: list[str], required: bool, flexible: bool = False) -> None:
    candidates = [
        repo / "contracts" / "openapi.yaml",
        repo / "contracts" / "openapi.yml",
        repo.parent / "contracts" / "openapi.yaml",
        repo.parent / "contracts" / "openapi.yml",
    ]
    if flexible:
        candidates.extend(
            [
                repo / "contracts" / "schema.json",
                repo.parent / "contracts" / "schema.json",
                *_declared_contracts(repo),
            ]
        )
    if any(p.is_file() for p in candidates):
        return
    if flexible and _has_external_contract_declaration(repo):
        return
    if required:
        expected = "contracts/openapi.yaml|openapi.yml|schema.json or declared Contract path"
        errors.append(f"MISSING contract SSOT ({expected})")


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
    existing = next((path for path in paths if path.is_file()), None)
    if existing is None:
        msg = "MISSING PR template (copy from rules/docs/pull-request-template.md)"
        if strict:
            errors.append(msg)
        else:
            print(f"WARN: {msg}")
        return
    if not strict:
        return
    text = existing.read_text(encoding="utf-8")
    heading_patterns = {
        "requirement / issue heading": r"^#{1,6}\s+.*(?:需求|issue|requirements?)",
        "risk / rollback heading": r"^#{1,6}\s+.*(?:风险|risk|回滚|rollback)",
    }
    for label, pattern in heading_patterns.items():
        if not re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
            errors.append(f"PR template missing {label}: {existing.relative_to(repo)}")
    table_lines = [line for line in text.splitlines() if line.lstrip().startswith("|")]
    table_text = "\n".join(table_lines)
    for label, pattern in {
        "acceptance criteria table column": r"验收|acceptance",
        "validation evidence table column": r"验证|证据|validation|evidence",
    }.items():
        if not re.search(pattern, table_text, re.IGNORECASE):
            errors.append(f"PR template missing {label}: {existing.relative_to(repo)}")


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
            continue
        command = scripts.get(name)
        if not isinstance(command, str) or not command.strip() or PLACEHOLDER_SCRIPT.match(command.strip()):
            errors.append(f"package.json script is placeholder: {name}")


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


def _ci_text(repo: Path) -> str:
    candidates = list((repo / ".github" / "workflows").glob("*.yml"))
    candidates.extend((repo / ".github" / "workflows").glob("*.yaml"))
    candidates.extend(
        path for path in (repo / ".gitlab-ci.yml", repo / "Jenkinsfile", repo / "azure-pipelines.yml")
        if path.is_file()
    )
    return "\n".join(path.read_text(encoding="utf-8", errors="replace") for path in candidates)


def check_backend_ci(repo: Path, errors: list[str], required: bool) -> None:
    if not required:
        return
    text = _ci_text(repo)
    if not re.search(r"(?:mvnw?|\.\/mvnw)\s+[^\n]*(?:verify|test)|gradlew(?:\.bat)?\s+[^\n]*(?:check|test)", text, re.IGNORECASE):
        errors.append("MISSING backend CI evidence running Maven verify/test or Gradle check/test")


def check_local_override(repo: Path, errors: list[str], required: bool) -> None:
    local = repo / ".cursor" / "rules" / "99-project-local.mdc"
    if not local.is_file():
        message = "MISSING .cursor/rules/99-project-local.mdc (project paths and adoption Level)"
        if required:
            errors.append(message)
        else:
            print(f"WARN: {message}")


def _load_yaml(path: Path, errors: list[str]) -> dict[str, object]:
    if yaml is None:
        errors.append("PyYAML is required to validate governance-adoption.yaml")
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        errors.append(f"INVALID governance-adoption.yaml: {exc}")
        return {}
    if not isinstance(data, dict):
        errors.append("governance-adoption.yaml root must be an object")
        return {}
    return data


def _check_local_evidence(
    repo: Path,
    ref: object,
    markers: tuple[str, ...],
    label: str,
    errors: list[str],
    allow_url: bool = False,
) -> None:
    if not isinstance(ref, str) or not ref.strip():
        errors.append(f"governance adoption {label}.evidence must be a path or HTTPS URL")
        return
    ref = ref.strip()
    if EVIDENCE_URL.fullmatch(ref):
        if allow_url:
            return
        errors.append(f"governance adoption {label}.evidence must be a repository path")
        return
    path = (repo / ref).resolve()
    try:
        path.relative_to(repo.resolve())
    except ValueError:
        errors.append(f"governance adoption {label}.evidence escapes repository: {ref}")
        return
    if not path.is_file():
        errors.append(f"governance adoption {label}.evidence not found: {ref}")
        return
    text = path.read_text(encoding="utf-8", errors="replace").lower()
    if markers and not any(marker.lower() in text for marker in markers):
        errors.append(f"governance adoption {label}.evidence lacks expected control marker")


def check_level_evidence(repo: Path, errors: list[str], level: int) -> None:
    if level < 2:
        return
    evidence_path = repo / "governance-adoption.yaml"
    if not evidence_path.is_file():
        errors.append("MISSING governance-adoption.yaml (real control evidence for Level 2+)")
        return
    data = _load_yaml(evidence_path, errors)
    if not data:
        return
    if data.get("schema_version") != 1:
        errors.append("governance-adoption.yaml schema_version must be 1")
    declared_level = data.get("level")
    if not isinstance(declared_level, int) or isinstance(declared_level, bool) or declared_level < level:
        errors.append(f"governance-adoption.yaml level must be >= requested Level {level}")
    owner = data.get("owner")
    if not isinstance(owner, str) or owner.strip().lower() in {"", "todo", "tbd"}:
        errors.append("governance-adoption.yaml owner must be meaningful")
    review_due = data.get("review_due")
    try:
        due = dt.date.fromisoformat(str(review_due))
        if due < dt.date.today():
            errors.append("governance-adoption.yaml review_due is expired")
    except ValueError:
        errors.append("governance-adoption.yaml review_due must be YYYY-MM-DD")

    checks = data.get("checks")
    if not isinstance(checks, dict):
        errors.append("governance-adoption.yaml checks must be an object")
        checks = {}
    control_markers = {
        "rules_adoption": ("check-project-adoption.py",),
        "credential_scan": ("gitleaks", "credential"),
        "supply_chain": ("dependency-check", "npm audit", "pnpm audit", "license-checker"),
    }
    for name, markers in control_markers.items():
        control = checks.get(name)
        if not isinstance(control, dict):
            errors.append(f"governance-adoption.yaml checks.{name} must be an object")
            continue
        _check_local_evidence(repo, control.get("evidence"), markers, f"checks.{name}", errors)

    branch = data.get("branch_protection")
    if not isinstance(branch, dict) or branch.get("enabled") is not True:
        errors.append("governance-adoption.yaml branch_protection.enabled must be true")
    else:
        _check_local_evidence(repo, branch.get("evidence"), (), "branch_protection", errors, allow_url=True)

    if level < 3:
        return
    level3 = data.get("level3")
    if not isinstance(level3, dict):
        errors.append("governance-adoption.yaml level3 must be an object")
        return
    _check_local_evidence(repo, level3.get("scorecard"), ("owner", "evidence", "status"), "level3.scorecard", errors)
    items = level3.get("evidence")
    if not isinstance(items, list) or len(items) < 3:
        errors.append("governance-adoption.yaml level3.evidence must contain at least three controls")
        return
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"governance-adoption.yaml level3.evidence[{index}] must be an object")
            continue
        for field in ("area", "owner"):
            value = item.get(field)
            if not isinstance(value, str) or value.strip().lower() in {"", "todo", "tbd"}:
                errors.append(f"governance-adoption.yaml level3.evidence[{index}].{field} must be meaningful")
        if item.get("status") != "complete":
            errors.append(f"governance-adoption.yaml level3.evidence[{index}].status must be complete")
        _check_local_evidence(
            repo,
            item.get("evidence"),
            (),
            f"level3.evidence[{index}]",
            errors,
            allow_url=True,
        )
        review_due = item.get("review_due")
        try:
            due = dt.date.fromisoformat(str(review_due))
            if due < dt.date.today():
                errors.append(f"governance-adoption.yaml level3.evidence[{index}].review_due is expired")
        except ValueError:
            errors.append(f"governance-adoption.yaml level3.evidence[{index}].review_due must be YYYY-MM-DD")


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


def run_stack(repo: Path, stack: str, strict: bool, level: int = 0) -> list[str]:
    errors: list[str] = []
    effective_strict = strict or level >= 2
    check_agents(repo, errors)
    check_rules_package(repo, errors)
    check_cursor_rules(repo, errors)

    if stack == "backend":
        check_build_tool(repo, errors)
        check_contracts(repo, errors, required=True)
        check_backend_ci(repo, errors, required=level >= 1)
    elif stack == "frontend":
        check_package_json_scripts(repo, errors, REQUIRED_FRONTEND_SCRIPTS)
        if level >= 1:
            check_package_json_scripts(repo, errors, REQUIRED_FRONTEND_LEVEL1_SCRIPTS)
        check_contracts(repo, errors, required=level >= 1, flexible=True)
    elif stack == "miniapp":
        check_package_json_scripts(repo, errors, REQUIRED_MINIAPP_SCRIPTS)
        if level >= 1:
            check_package_json_scripts(repo, errors, REQUIRED_MINIAPP_LEVEL1_SCRIPTS)
        check_contracts(repo, errors, required=True)
    else:
        errors.append(f"Unknown stack: {stack}")

    check_codeowners(repo, errors, effective_strict)
    check_pr_template(repo, errors, effective_strict)
    check_local_override(repo, errors, required=level >= 1)
    check_level_evidence(repo, errors, level)
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
        "--level",
        type=int,
        choices=range(0, 4),
        default=0,
        help="Adoption maturity Level 0-3; higher levels enable stricter evidence checks",
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
        print(f"=== Checking {stack} Level {args.level} @ {repo} ===")
        all_errors.extend(run_stack(repo, stack, args.strict, args.level))

    require_governance = args.require_governance or args.level >= 2
    if require_governance or args.governance_dir:
        governance_dir = args.governance_dir or Path("common-governance")
        if not governance_dir.is_absolute():
            governance_dir = repo / governance_dir
        governance_dir = governance_dir.resolve()
        check_governance_package(governance_dir, all_errors, require_governance)

    if all_errors:
        print("\nFAILED:")
        for err in all_errors:
            print(f"  - {err}")
        return 1

    print("\nOK: project adoption checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
