#!/usr/bin/env python3
"""Validate web-backend/rules package internal consistency.

Counts eval prompts ONLY from evals/prompts.md (### Bxx headings).
smoke-prompts.md is an index: validates B-id coverage, not prompt body count.

Usage (from repo anywhere):
  python web-backend/rules/scripts/validate-rules-package.py
  python web-backend/rules/scripts/validate-rules-package.py --rules-dir path/to/rules
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

PROMPT_HEADING = re.compile(r"^###\s+(B\d+)\s+—", re.MULTILINE)
RUBRIC_ROW = re.compile(r"^\|\s+(B\d+)\s+\|", re.MULTILINE)
RESULTS_ROW = re.compile(r"^\|\s+(B\d+)\s+\|", re.MULTILINE)
THRESHOLD = re.compile(r"(\d+)/(\d+)")
B_ID = re.compile(r"\bB(\d{2})\b")
B_RANGE = re.compile(r"B(\d{2})–B(\d{2})")
VERSION_HEAD = re.compile(r"^##\s+(\d+\.\d+\.\d+)\s+—", re.MULTILINE)
README_PATH = re.compile(r"`((?:shared|docs|codex|cursor|evals|scripts)/[\w./-]+\.(?:md|mdc|py|yml))`")
AGENTS_PATH = re.compile(r"`rules/((?:shared|docs|codex|cursor|evals|scripts)/[\w./-]+\.(?:md|mdc|py|yml))`")
SHARED_REF = re.compile(r"shared/(\d{2}-[\w-]+\.md)")
BARE_SHARED_REF = re.compile(r"(?<![\w/-])(\d{2}-[\w-]+\.md)")
CORE_P1_LINE = re.compile(r"^(B\d+(?:、B\d+)*)\.?\s*$")

# High-risk evals whose rubric must repeat the prompt topic verbatim.  Keep this
# deliberately small and explicit: the goal is to prevent semantic reassignment
# of a scored ID, not to force every pass criterion to duplicate its prompt.
EVAL_TOPIC_GUARDS = {"B19": "高风险导入无确认"}

# Expected smoke core P1 count (Smoke suite)
SMOKE_CORE_P1_COUNT = 20
SECURITY_SUITE = ["B06", "B21", "B26", "B31", "B34", "B39", "B40", "B43", "B44", "B45", "B52", "B53"]
CONTRACT_SUITE = ["B03", "B11", "B25", "B47", "B51"]
BUSINESS_EXTENSION_SUITE = [
    "B55", "B56", "B57", "B58", "B59", "B60", "B61", "B62", "B63",
]

# Files that should mention Full evals threshold (min_pass/total_p1 style)
THRESHOLD_FILES = [
    "README.md",
    "RELEASE.md",
    "evals/README.md",
    "evals/rubric.md",
    "evals/results-template.md",
    "docs/onboarding-new-project.md",
    "docs/rules-package-index.md",
    "cursor/00-project-overview.mdc",
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_prompt_ids(text: str) -> list[str]:
    return PROMPT_HEADING.findall(text)


def extract_smoke_ids(smoke_text: str) -> set[str]:
    ids: set[str] = set()
    for start_s, end_s in B_RANGE.findall(smoke_text):
        start, end = int(start_s), int(end_s)
        for n in range(start, end + 1):
            ids.add(f"B{n:02d}")
    for n in B_ID.findall(smoke_text):
        ids.add(f"B{n}")
    return ids


def parse_p1_threshold(rubric: str) -> tuple[int, int] | None:
    m = re.search(r"P1:\s*>=\s*(\d+)/(\d+)", rubric)
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


def parse_core_p1_line(text: str) -> list[str]:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("B09") and "、" in line:
            return re.findall(r"B\d+", line)
    return []


def parse_smoke_core_p1(smoke_text: str) -> list[str]:
    section = smoke_text.split("## Security")[0]
    ids: list[str] = []
    for line in section.splitlines():
        m = re.match(r"^\|\s+(B\d+)\s+\|", line.strip())
        if m and m.group(1) != "B01–B08":
            bid = m.group(1)
            if "–" not in bid:
                ids.append(bid)
    return ids


def parse_suite_line(text: str, header: str) -> list[str]:
    """Parse smoke-prompts.md section (## Security / ## Contract)."""
    part = text.split(header, 1)
    if len(part) < 2:
        return []
    block = part[1].split("##", 1)[0]
    return re.findall(r"B\d+", block.split("**门槛**")[0])


def expand_b_id_tokens(text: str) -> list[str]:
    """Expand B01, B55–B63 style tokens to sorted unique Bxx list."""
    ids: set[str] = set()
    for m in re.finditer(r"B(\d{2})", text):
        ids.add(f"B{m.group(1)}")
    for m in re.finditer(r"B(\d{2})\s*[–-]\s*B(\d{2})", text):
        lo, hi = int(m.group(1)), int(m.group(2))
        for n in range(lo, hi + 1):
            ids.add(f"B{n:02d}")
    return sorted(ids)


def parse_evals_table_suite(text: str, suite_name: str) -> list[str]:
    """Parse evals/README.md regression table row."""
    m = re.search(rf"\|\s*\*\*{re.escape(suite_name)}\*\*\s*\|\s*([^|]+)\|", text)
    if not m:
        return []
    return expand_b_id_tokens(m.group(1))


# Paths in README that live outside rules/ package (monorepo root)
README_EXTERNAL_PATHS = frozenset({"docs/monorepo-layout.md"})

# Cross-package refs from backend rules → web-front/rules (monorepo layout)
CROSS_FRONT_REF = re.compile(
    r"(?:\.\./web-front/rules/|web-front/rules/)([\w./-]+\.(?:md|mdc))"
)


def monorepo_root(rules_root: Path) -> Path | None:
    """web-backend/rules → repo root (parent of web-backend)."""
    resolved = rules_root.resolve()
    if resolved.name == "rules" and resolved.parent.name == "web-backend":
        return resolved.parent.parent
    return None


def check_cross_package_front_refs(rules_root: Path, errors: list[str]) -> None:
    repo = monorepo_root(rules_root)
    if repo is None:
        return
    front_rules = repo / "web-front" / "rules"
    if not front_rules.is_dir():
        errors.append(f"monorepo web-front/rules not found at {front_rules}")
        return
    seen: set[str] = set()
    for path in rules_root.rglob("*"):
        if not path.is_file() or path.suffix not in {".md", ".mdc"}:
            continue
        for rel in CROSS_FRONT_REF.findall(read(path)):
            if rel in seen:
                continue
            seen.add(rel)
            if not (front_rules / rel).is_file():
                errors.append(
                    f"cross-package ref missing web-front/rules/{rel} "
                    f"(from {path.relative_to(rules_root)})"
                )


def check_readme_paths(root: Path, errors: list[str]) -> None:
    readme = read(root / "README.md")
    skip_prefixes = ("evals/", "examples/")
    for path in README_PATH.findall(readme):
        if path in README_EXTERNAL_PATHS or path.startswith(skip_prefixes):
            continue
        if not (root / path).exists():
            errors.append(f"README.md lists missing path: {path}")


def check_agents_paths(root: Path, errors: list[str]) -> None:
    agents = root / "codex" / "AGENTS.md"
    if not agents.is_file():
        return
    for path in AGENTS_PATH.findall(read(agents)):
        if not (root / path).is_file():
            errors.append(f"codex/AGENTS.md: missing rules/{path}")


def check_cursor_shared_refs(root: Path, errors: list[str]) -> None:
    cursor_dir = root / "cursor"
    if not cursor_dir.is_dir():
        return
    for mdc in cursor_dir.glob("*.mdc"):
        text = read(mdc)
        for rel in SHARED_REF.findall(text):
            if not (root / "shared" / rel).is_file():
                errors.append(f"{mdc.name}: missing shared/{rel}")
        for rel in BARE_SHARED_REF.findall(text):
            if (root / "shared" / rel).is_file():
                errors.append(
                    f"{mdc.name}: bare shared reference {rel}; use rules/shared/..."
                )


def check_eval_topic_guards(prompts: str, rubric: str, errors: list[str]) -> None:
    """Ensure selected high-risk eval IDs cannot be silently repurposed."""
    prompt_topics = {
        match.group(1): match.group(2)
        for match in re.finditer(r"^###\s+(B\d+)\s+—\s+(.+)$", prompts, re.MULTILINE)
    }
    rubric_rows = {
        match.group(1): match.group(2)
        for match in re.finditer(r"^\|\s+(B\d+)\s+\|\s+(.+?)\s+\|$", rubric, re.MULTILINE)
    }
    for eval_id, expected_topic in EVAL_TOPIC_GUARDS.items():
        if prompt_topics.get(eval_id) != expected_topic:
            errors.append(f"{eval_id}: prompt topic must be '{expected_topic}'")
        if expected_topic not in rubric_rows.get(eval_id, ""):
            errors.append(f"{eval_id}: rubric topic must contain '{expected_topic}'")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate rules package consistency")
    parser.add_argument(
        "--rules-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Path to web-backend/rules (default: parent of scripts/)",
    )
    args = parser.parse_args()
    root: Path = args.rules_dir
    errors: list[str] = []

    version_file = root / "VERSION"
    if not version_file.is_file():
        print(f"ERROR: VERSION not found under {root}", file=sys.stderr)
        return 1
    version = read(version_file).strip()

    changelog = read(root / "CHANGELOG.md")
    latest = VERSION_HEAD.search(changelog)
    if not latest or latest.group(1) != version:
        errors.append(f"CHANGELOG latest version != VERSION ({version})")

    prompts = read(root / "evals/prompts.md")
    rubric = read(root / "evals/rubric.md")
    results = read(root / "evals/results-template.md")
    smoke = read(root / "evals/smoke-prompts.md")

    prompt_ids = extract_prompt_ids(prompts)
    rubric_p0 = RUBRIC_ROW.findall(rubric.split("## P1")[0])
    rubric_p1 = RUBRIC_ROW.findall(rubric.split("## P1", 1)[1]) if "## P1" in rubric else []
    rubric_ids = rubric_p0 + rubric_p1
    results_ids = [m for m in RESULTS_ROW.findall(results) if m.startswith("B")]

    p0_count = sum(1 for b in prompt_ids if int(b[1:]) <= 8)
    p1_ids = [b for b in prompt_ids if int(b[1:]) >= 9]
    total = len(prompt_ids)

    if p0_count != 8:
        errors.append(f"prompts.md P0 count {p0_count}, expected 8")
    if len(prompt_ids) != len(set(prompt_ids)):
        errors.append("prompts.md has duplicate B ids")
    if prompt_ids != sorted(prompt_ids, key=lambda x: int(x[1:])):
        errors.append("prompts.md B ids not in ascending order")
    if rubric_p0 != [f"B{i:02d}" for i in range(1, 9)]:
        errors.append(f"rubric P0 ids mismatch: got {len(rubric_p0)}")
    if rubric_p1 != p1_ids:
        errors.append(
            f"rubric P1 ids mismatch prompts: rubric={len(rubric_p1)} prompts_p1={len(p1_ids)}"
        )
    if rubric_ids != prompt_ids:
        errors.append(
            f"rubric all ids mismatch prompts: rubric={len(rubric_ids)} prompts={len(prompt_ids)}"
        )
    if results_ids != prompt_ids:
        errors.append(
            f"results-template ids mismatch prompts: template={len(results_ids)} prompts={len(prompt_ids)}"
        )
    check_eval_topic_guards(prompts, rubric, errors)

    # smoke-prompts: no ### headings expected
    smoke_headings = PROMPT_HEADING.findall(smoke)
    if smoke_headings:
        errors.append(
            f"smoke-prompts.md must not use ### Bxx headings (found {len(smoke_headings)}); use index only"
        )

    smoke_ids = extract_smoke_ids(smoke)
    prompts_set = set(prompt_ids)
    missing = sorted(smoke_ids - prompts_set, key=lambda x: int(x[1:]))
    if missing:
        errors.append(f"smoke-prompts references unknown B ids: {', '.join(missing)}")

    evals_readme = read(root / "evals/README.md")
    core_readme = parse_core_p1_line(
        evals_readme.split("### 核心 P1", 1)[1] if "### 核心 P1" in evals_readme else ""
    )
    core_smoke = parse_smoke_core_p1(smoke)
    if core_readme != core_smoke:
        errors.append(
            f"evals/README core P1 != smoke-prompts Smoke table: "
            f"readme={core_readme} smoke={core_smoke}"
        )
    if len(core_smoke) != SMOKE_CORE_P1_COUNT:
        errors.append(f"smoke core P1 count {len(core_smoke)}, expected {SMOKE_CORE_P1_COUNT}")

    sec_smoke = parse_suite_line(smoke, "## Security")
    sec_readme = parse_evals_table_suite(evals_readme, "Security")
    if sorted(sec_smoke) != sorted(SECURITY_SUITE) or sorted(sec_readme) != sorted(SECURITY_SUITE):
        errors.append(
            f"Security suite mismatch: smoke={sec_smoke} readme={sec_readme} expected={SECURITY_SUITE}"
        )

    con_smoke = parse_suite_line(smoke, "## Contract")
    con_readme = parse_evals_table_suite(evals_readme, "Contract")
    if sorted(con_smoke) != sorted(CONTRACT_SUITE) or sorted(con_readme) != sorted(CONTRACT_SUITE):
        errors.append(
            f"Contract suite mismatch: smoke={con_smoke} readme={con_readme} expected={CONTRACT_SUITE}"
        )

    biz_smoke = parse_suite_line(smoke, "## Business Extension")
    biz_readme = parse_evals_table_suite(evals_readme, "Business Extension")
    if sorted(biz_smoke) != sorted(BUSINESS_EXTENSION_SUITE) or sorted(biz_readme) != sorted(
        BUSINESS_EXTENSION_SUITE
    ):
        errors.append(
            f"Business Extension suite mismatch: smoke={biz_smoke} readme={biz_readme} "
            f"expected={BUSINESS_EXTENSION_SUITE}"
        )

    check_readme_paths(root, errors)
    check_agents_paths(root, errors)
    check_cursor_shared_refs(root, errors)
    check_cross_package_front_refs(root, errors)

    threshold = parse_p1_threshold(rubric)
    if not threshold:
        errors.append("rubric.md missing P1: >= N/M block")
    else:
        min_pass, total_p1 = threshold
        if total_p1 != len(p1_ids):
            errors.append(
                f"rubric P1 total {total_p1} != prompts P1 count {len(p1_ids)}"
            )
        expected_token = f"{min_pass}/{total_p1}"
        for rel in THRESHOLD_FILES:
            text = read(root / rel)
            if expected_token not in text and f">= {min_pass}/{total_p1}" not in text:
                if rel == "evals/rubric.md":
                    continue
                if rel == "evals/results-template.md" and f"__/{total_p1}" in text:
                    continue
                errors.append(f"{rel}: missing threshold token {expected_token}")

    overview = read(root / "cursor/00-project-overview.mdc")
    hard_rules = len(re.findall(r"^\d+\.\s", read(root / "shared/00-must-follow.md"), re.MULTILINE))
    m = re.search(r"当前\s+(\d+)\s+条", overview)
    if m and int(m.group(1)) != hard_rules:
        errors.append(
            f"cursor/00 hard rule count {m.group(1)} != 00-must-follow numbered items {hard_rules}"
        )

    print(f"rules-dir: {root}")
    print(f"VERSION: {version}")
    print(f"prompts: {total} (P0={p0_count}, P1={len(p1_ids)})")
    if threshold:
        print(f"P1 threshold: >={threshold[0]}/{threshold[1]}")
    print(f"smoke-prompts B coverage: {len(smoke_ids)} ids (index only, not prompt count)")

    if errors:
        print("\nFAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("\nOK: rules package consistency checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
