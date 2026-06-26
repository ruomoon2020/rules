import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "validate-rules-package.py"
SPEC = importlib.util.spec_from_file_location("miniapp_validator", MODULE_PATH)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)


class ValidateRulesPackageTests(unittest.TestCase):
    def test_cursor_rejects_bare_shared_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "shared").mkdir()
            (root / "shared" / "23-content-safety.md").write_text("# content\n", encoding="utf-8")
            (root / "cursor").mkdir()
            (root / "cursor" / "sample.mdc").write_text(
                "全文：`23-content-safety.md`\n", encoding="utf-8"
            )
            errors: list[str] = []

            validator.check_cursor_shared_refs(root, errors)

        self.assertEqual(
            errors,
            ["sample.mdc: bare shared reference 23-content-safety.md; use rules/shared/..."],
        )

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

    def test_resilience_extension_suite_matches_smoke_index(self):
        rules_root = Path(__file__).parents[2]
        smoke = validator.read(rules_root / "evals" / "smoke-prompts.md")
        evals_readme = validator.read(rules_root / "evals" / "README.md")

        smoke_ids = validator.parse_suite_line(smoke, "## Resilience")
        readme_ids = validator.parse_evals_table_suite(evals_readme, "Resilience Extension")

        self.assertEqual(sorted(smoke_ids), sorted(validator.RESILIENCE_EXTENSION_SUITE))
        self.assertEqual(sorted(readme_ids), sorted(validator.RESILIENCE_EXTENSION_SUITE))
