import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "validate-rules-package.py"
SPEC = importlib.util.spec_from_file_location("frontend_validator", MODULE_PATH)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)


class ValidateRulesPackageTests(unittest.TestCase):
    def test_frontend_checks_missing_backend_cross_package_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            front_rules = repo / "web-front" / "rules"
            front_rules.mkdir(parents=True)
            (front_rules / "README.md").write_text(
                "见 `web-backend/rules/docs/missing.md`\n", encoding="utf-8"
            )
            backend_rules = repo / "web-backend" / "rules"
            backend_rules.mkdir(parents=True)
            errors: list[str] = []

            validator.check_cross_package_backend_refs(front_rules, errors)

        self.assertEqual(
            errors,
            ["cross-package ref missing web-backend/rules/docs/missing.md (from README.md)"],
        )

    def test_agents_rejects_missing_rules_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "codex").mkdir()
            (root / "codex" / "AGENTS.md").write_text(
                "读取 `rules/docs/missing.md`\n", encoding="utf-8"
            )
            errors: list[str] = []

            validator.check_agents_paths(root, errors)

        self.assertEqual(errors, ["codex/AGENTS.md: missing rules/docs/missing.md"])

    def test_eval_topic_guard_detects_prompt_drift(self):
        prompts = "### E41 — 错误主题\n"
        rubric = "| E41 | 硬编码业务文案 |\n"
        errors: list[str] = []

        validator.check_eval_topic_guards(prompts, rubric, errors)

        self.assertTrue(any("E41: prompt topic must be" in error for error in errors))

    def test_eval_topic_guard_detects_rubric_drift(self):
        prompts = "### E42 — Token 放 WebSocket URL\n"
        rubric = "| E42 | 拒绝把 token 放进 query |\n"
        errors: list[str] = []

        validator.check_eval_topic_guards(prompts, rubric, errors)

        self.assertTrue(any("E42: rubric topic must contain" in error for error in errors))

    def test_cursor_rejects_bare_shared_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "shared").mkdir()
            (root / "shared" / "23-i18n-locale.md").write_text("# i18n\n", encoding="utf-8")
            (root / "cursor").mkdir()
            (root / "cursor" / "sample.mdc").write_text(
                "全文：`23-i18n-locale.md`\n", encoding="utf-8"
            )
            errors: list[str] = []

            validator.check_cursor_shared_refs(root, errors)

        self.assertEqual(
            errors,
            ["sample.mdc: bare shared reference 23-i18n-locale.md; use rules/shared/..."],
        )

    def test_platform_extension_suite_matches_smoke_index(self):
        rules_root = Path(__file__).parents[2]
        smoke = validator.read(rules_root / "evals" / "smoke-prompts.md")
        evals_readme = validator.read(rules_root / "evals" / "README.md")

        smoke_ids = validator.parse_suite_line(smoke, "## Platform Extension")
        readme_ids = validator.parse_evals_table_suite(evals_readme, "Platform Extension")

        self.assertEqual(sorted(smoke_ids), sorted(validator.PLATFORM_EXTENSION_SUITE))
        self.assertEqual(sorted(readme_ids), sorted(validator.PLATFORM_EXTENSION_SUITE))

    def test_readme_must_list_all_shared_files(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "shared").mkdir()
            (root / "shared" / "00-must-follow.md").write_text("# x\n", encoding="utf-8")
            (root / "shared" / "99-missing-from-readme.md").write_text("# y\n", encoding="utf-8")
            (root / "README.md").write_text(
                "| `shared/00-must-follow.md` | hard |\n", encoding="utf-8"
            )
            errors: list[str] = []

            validator.check_readme_shared_inventory(root, errors)

        self.assertEqual(
            errors,
            ["README.md file inventory missing shared/99-missing-from-readme.md"],
        )

    def test_topic_manifest_matches_live_evals(self):
        rules_root = Path(__file__).parents[2]
        repo_scripts = rules_root.parent.parent / "scripts"
        sys.path.insert(0, str(repo_scripts))
        import eval_topic_manifest as etm

        errors: list[str] = []
        etm.check_manifest(rules_root, "E", errors)
        self.assertEqual(errors, [])
