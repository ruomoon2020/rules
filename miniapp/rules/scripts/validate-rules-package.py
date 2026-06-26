#!/usr/bin/env python3
"""Validate miniapp/rules package internal consistency.

Counts eval prompts ONLY from evals/prompts.md (### Mxx headings).
smoke-prompts.md is an index: validates M-id coverage, not prompt body count.

Usage:
  python miniapp/rules/scripts/validate-rules-package.py
  python rules/scripts/validate-rules-package.py --rules-dir rules
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ID_PREFIX = "M"
PROMPT_HEADING = re.compile(rf"^###\s+({ID_PREFIX}\d+)\s+—", re.MULTILINE)
RUBRIC_ROW = re.compile(rf"^\|\s+({ID_PREFIX}\d+)\s+\|", re.MULTILINE)
RESULTS_ROW = re.compile(rf"^\|\s+({ID_PREFIX}\d+)\s+\|", re.MULTILINE)
ID_TOKEN = re.compile(rf"\b{ID_PREFIX}(\d{{2}})\b")
ID_RANGE = re.compile(rf"{ID_PREFIX}(\d{{2}})–{ID_PREFIX}(\d{{2}})")
VERSION_HEAD = re.compile(r"^##\s+(\d+\.\d+\.\d+)\s+—", re.MULTILINE)
README_PATH = re.compile(r"`((?:shared|docs|codex|cursor|evals|scripts)/[\w./-]+\.(?:md|mdc|py|yml|mjs))`")
SHARED_REF = re.compile(r"shared/(\d{2}-[\w-]+\.md)")

P0_COUNT = 8
P0_MAX_NUM = 8
SMOKE_CORE_P1_COUNT = 10
SECURITY_SUITE = [
    "M06", "M07", "M12", "M18", "M30", "M31", "M32", "M33", "M34",
]
CONTRACT_SUITE = ["M03", "M05", "M08", "M15"]
BUSINESS_EXTENSION_SUITE = [
    "M21", "M22", "M23", "M24", "M25", "M26", "M27", "M28", "M29",
]
SECURITY_EXTENSION_SUITE = ["M30", "M31", "M32", "M33", "M34"]
RESILIENCE_EXTENSION_SUITE = ["M35", "M36", "M37", "M38"]
TOTAL_PROMPTS = 38
SHARED_MAX_NUM = 25

THRESHOLD_FILES = [
    "README.md",
    "RELEASE.md",
    "evals/README.md",
    "evals/rubric.md",
    "evals/results-template.md",
    "cursor/00-project-overview.mdc",
]

README_EXTERNAL_PATHS = frozenset()
README_SKIP_PREFIXES = ("evals/", "examples/", "cursor/")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def extract_prompt_ids(text: str) -> list[str]:
    return PROMPT_HEADING.findall(text)


def extract_smoke_ids(smoke_text: str) -> set[str]:
    ids: set[str] = set()
    for start_s, end_s in ID_RANGE.findall(smoke_text):
        start, end = int(start_s), int(end_s)
        for n in range(start, end + 1):
            ids.add(f"{ID_PREFIX}{n:02d}")
    for n in ID_TOKEN.findall(smoke_text):
        ids.add(f"{ID_PREFIX}{n}")
    return ids


def parse_p1_threshold(rubric: str) -> tuple[int, int] | None:
    m = re.search(r">=\s*(\d+)/(\d+)", rubric.split("汇总公式")[-1])
    if m:
        return int(m.group(1)), int(m.group(2))
    return None


def parse_core_p1_line(text: str) -> list[str]:
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("M09") and "、" in line:
            return re.findall(r"M\d+", line)
    return []


def parse_smoke_core_p1(smoke_text: str) -> list[str]:
    section = smoke_text.split("## Security")[0]
    ids: list[str] = []
    for line in section.splitlines():
        m = re.match(rf"^\|\s+({ID_PREFIX}\d+)\s+\|", line.strip())
        if m and "–" not in m.group(1):
            num = int(m.group(1)[1:])
            if num > P0_MAX_NUM:
                ids.append(m.group(1))
    return ids


def parse_suite_line(text: str, header: str) -> list[str]:
    part = text.split(header, 1)
    if len(part) < 2:
        return []
    block = part[1].split("##", 1)[0]
    return re.findall(r"M\d+", block.split("**门槛**")[0])


def parse_evals_table_suite(text: str, suite_name: str) -> list[str]:
    m = re.search(rf"\|\s*\*\*{re.escape(suite_name)}\*\*\s*\|\s*([^|]+)\|", text)
    if not m:
        return []
    raw = m.group(1)
    ids: set[str] = set()
    for n in re.findall(rf"{ID_PREFIX}(\d{{2}})", raw):
        ids.add(f"{ID_PREFIX}{n}")
    for m2 in re.finditer(rf"{ID_PREFIX}(\d{{2}})\s*[–-]\s*{ID_PREFIX}(\d{{2}})", raw):
        lo, hi = int(m2.group(1)), int(m2.group(2))
        for n in range(lo, hi + 1):
            ids.add(f"{ID_PREFIX}{n:02d}")
    return sorted(ids)


def check_readme_paths(root: Path, errors: list[str]) -> None:
    readme = read(root / "README.md")
    for path in README_PATH.findall(readme):
        if path in README_EXTERNAL_PATHS or path.startswith(README_SKIP_PREFIXES):
            continue
        if "*" in path:
            continue
        if not (root / path).exists():
            errors.append(f"README.md lists missing path: {path}")


def check_cursor_shared_refs(root: Path, errors: list[str]) -> None:
    cursor_dir = root / "cursor"
    if not cursor_dir.is_dir():
        return
    for mdc in cursor_dir.glob("*.mdc"):
        for rel in SHARED_REF.findall(read(mdc)):
            if not (root / "shared" / rel).is_file():
                errors.append(f"{mdc.name}: missing shared/{rel}")


def check_shared_numbered_files(root: Path, errors: list[str]) -> None:
    shared_dir = root / "shared"
    if not (shared_dir / "00-must-follow.md").is_file():
        errors.append("missing shared/00-must-follow.md")
    for n in range(1, SHARED_MAX_NUM + 1):
        if not list(shared_dir.glob(f"{n:02d}-*.md")):
            errors.append(f"missing shared/{n:02d}-*.md")


def check_agents_shared_refs(root: Path, errors: list[str]) -> None:
    agents = read(root / "codex/AGENTS.md")
    for rel in SHARED_REF.findall(agents):
        if not (root / "shared" / rel).is_file():
            errors.append(f"AGENTS.md: missing shared/{rel}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate miniapp rules package consistency")
    parser.add_argument(
        "--rules-dir",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
    )
    args = parser.parse_args()
    root: Path = args.rules_dir
    errors: list[str] = []

    version = read(root / "VERSION").strip()
    changelog = read(root / "CHANGELOG.md")
    latest = VERSION_HEAD.search(changelog)
    if not latest or latest.group(1) != version:
        errors.append(f"CHANGELOG latest version != VERSION ({version})")

    prompts = read(root / "evals/prompts.md")
    rubric = read(root / "evals/rubric.md")
    results = read(root / "evals/results-template.md")
    smoke_path = root / "evals/smoke-prompts.md"
    smoke = read(smoke_path) if smoke_path.is_file() else ""

    prompt_ids = extract_prompt_ids(prompts)
    rubric_p0 = RUBRIC_ROW.findall(rubric.split("## P1")[0])
    rubric_p1 = RUBRIC_ROW.findall(rubric.split("## P1", 1)[1]) if "## P1" in rubric else []
    rubric_ids = rubric_p0 + rubric_p1
    results_ids = [m for m in RESULTS_ROW.findall(results) if m.startswith(ID_PREFIX)]

    p0_ids = [e for e in prompt_ids if int(e[1:]) <= P0_MAX_NUM]
    p1_ids = [e for e in prompt_ids if P0_MAX_NUM < int(e[1:]) <= 20]
    biz_ids = [e for e in prompt_ids if 21 <= int(e[1:]) <= 29]
    sec_ext_ids = [e for e in prompt_ids if 30 <= int(e[1:]) <= 34]
    res_ext_ids = [e for e in prompt_ids if 35 <= int(e[1:]) <= 38]
    total = len(prompt_ids)

    if total != TOTAL_PROMPTS:
        errors.append(f"prompts.md total {total}, expected {TOTAL_PROMPTS}")
    if len(p0_ids) != P0_COUNT:
        errors.append(f"prompts.md P0 count {len(p0_ids)}, expected {P0_COUNT}")
    if len(p1_ids) != 12:
        errors.append(f"prompts.md core P1 count {len(p1_ids)}, expected 12")
    if sorted(biz_ids) != BUSINESS_EXTENSION_SUITE:
        errors.append(f"prompts.md Business Extension mismatch: {biz_ids}")
    if sorted(sec_ext_ids) != SECURITY_EXTENSION_SUITE:
        errors.append(f"prompts.md Security Extension mismatch: {sec_ext_ids}")
    if sorted(res_ext_ids) != RESILIENCE_EXTENSION_SUITE:
        errors.append(f"prompts.md Resilience Extension mismatch: {res_ext_ids}")
    if prompt_ids != sorted(prompt_ids, key=lambda x: int(x[1:])):
        errors.append("prompts.md M ids not in ascending order")
    if rubric_p0 != [f"{ID_PREFIX}{i:02d}" for i in range(1, P0_COUNT + 1)]:
        errors.append(f"rubric P0 ids mismatch: got {len(rubric_p0)}")
    if rubric_p1 != p1_ids + biz_ids + sec_ext_ids + res_ext_ids:
        errors.append("rubric P1+Biz+Sec+Res mismatch prompts")
    if rubric_ids != prompt_ids:
        errors.append("rubric all ids mismatch prompts")
    if results_ids != prompt_ids:
        errors.append("results-template ids mismatch prompts")

    if smoke_path.is_file():
        if PROMPT_HEADING.findall(smoke):
            errors.append("smoke-prompts.md must not use ### Mxx headings")
        smoke_ids = extract_smoke_ids(smoke)
        missing = sorted(set(smoke_ids) - set(prompt_ids), key=lambda x: int(x[1:]))
        if missing:
            errors.append(f"smoke-prompts unknown M ids: {', '.join(missing)}")

        evals_readme = read(root / "evals/README.md")
        core_readme = parse_core_p1_line(
            evals_readme.split("### 核心 P1", 1)[1] if "### 核心 P1" in evals_readme else ""
        )
        core_smoke = parse_smoke_core_p1(smoke)
        if core_readme and core_readme != core_smoke:
            errors.append("evals/README core P1 != smoke table")
        if len(core_smoke) != SMOKE_CORE_P1_COUNT:
            errors.append(f"smoke core P1 count {len(core_smoke)}, expected {SMOKE_CORE_P1_COUNT}")

        sec_smoke = parse_suite_line(smoke, "## Security")
        sec_readme = parse_evals_table_suite(evals_readme, "Security")
        if sorted(sec_smoke) != sorted(SECURITY_SUITE) or sorted(sec_readme) != sorted(SECURITY_SUITE):
            errors.append("Security suite mismatch")

        con_smoke = parse_suite_line(smoke, "## Contract")
        con_readme = parse_evals_table_suite(evals_readme, "Contract")
        if sorted(con_smoke) != sorted(CONTRACT_SUITE) or sorted(con_readme) != sorted(CONTRACT_SUITE):
            errors.append("Contract suite mismatch")

        biz_smoke = parse_suite_line(smoke, "## Business Extension")
        biz_readme = parse_evals_table_suite(evals_readme, "Business Extension")
        if sorted(biz_smoke) != sorted(BUSINESS_EXTENSION_SUITE) or sorted(biz_readme) != sorted(
            BUSINESS_EXTENSION_SUITE
        ):
            errors.append("Business Extension suite mismatch")

        res_smoke = parse_suite_line(smoke, "## Resilience")
        res_readme = parse_evals_table_suite(evals_readme, "Resilience")
        if sorted(res_smoke) != sorted(RESILIENCE_EXTENSION_SUITE) or sorted(res_readme) != sorted(
            RESILIENCE_EXTENSION_SUITE
        ):
            errors.append("Resilience suite mismatch")

    check_readme_paths(root, errors)
    check_shared_numbered_files(root, errors)
    check_cursor_shared_refs(root, errors)
    check_agents_shared_refs(root, errors)

    threshold = parse_p1_threshold(rubric)
    if not threshold:
        errors.append("rubric.md missing P1 >= N/M block")
    else:
        min_pass, total_p1 = threshold
        core_p1_count = 12
        if total_p1 != core_p1_count:
            errors.append(f"rubric P1 total {total_p1} != core P1 {core_p1_count}")
        token = f"{min_pass}/{total_p1}"
        for rel in THRESHOLD_FILES:
            text = read(root / rel)
            if token not in text and f"至少 {token}" not in text:
                if rel == "evals/rubric.md":
                    continue
                if rel == "evals/results-template.md" and f"__/{total_p1}" in text:
                    continue
                errors.append(f"{rel}: missing threshold {token}")

    overview_path = root / "cursor/00-project-overview.mdc"
    if overview_path.is_file():
        hard_rules = len(re.findall(r"^\d+\.\s", read(root / "shared/00-must-follow.md"), re.MULTILINE))
        m = re.search(r"当前\s+(\d+)\s+条", read(overview_path))
        if m and int(m.group(1)) != hard_rules:
            errors.append(f"cursor/00 hard rule count != 00 ({hard_rules})")

    print(f"rules-dir: {root}")
    print(f"VERSION: {version}")
    print(
        f"prompts: {total} (P0={len(p0_ids)}, P1={len(p1_ids)}, "
        f"Biz={len(biz_ids)}, SecExt={len(sec_ext_ids)}, ResExt={len(res_ext_ids)})"
    )
    if threshold:
        print(f"P1 threshold: >={threshold[0]}/{threshold[1]}")
    if smoke_path.is_file():
        print(f"smoke-prompts M coverage: {len(extract_smoke_ids(smoke))} ids (index only)")

    if errors:
        print("\nFAILED:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print("\nOK: miniapp rules package consistency checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
