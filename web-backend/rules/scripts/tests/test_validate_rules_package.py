import importlib.util
import tempfile
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "validate-rules-package.py"
SPEC = importlib.util.spec_from_file_location("backend_validator", MODULE_PATH)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)


class ValidateRulesPackageTests(unittest.TestCase):
    def test_b19_topic_guard_rejects_rubric_semantic_drift(self):
        errors: list[str] = []

        validator.check_eval_topic_guards(
            "### B19 — 高风险导入无确认\n",
            "| B19 | 拒绝永久公开错误文件 URL |\n",
            errors,
        )

        self.assertEqual(errors, ["B19: rubric topic must contain '高风险导入无确认'"])

    def test_cursor_rejects_bare_shared_rule_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "cursor").mkdir()
            (root / "shared").mkdir()
            (root / "shared" / "08-exception-errorcodes.md").write_text("# rule\n", encoding="utf-8")
            (root / "cursor" / "08.mdc").write_text(
                "全文：`08-exception-errorcodes.md`\n", encoding="utf-8"
            )
            errors: list[str] = []

            validator.check_cursor_shared_refs(root, errors)

        self.assertEqual(errors, ["08.mdc: bare shared reference 08-exception-errorcodes.md; use rules/shared/..."])

    def test_agents_rejects_missing_rules_path(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "codex").mkdir()
            (root / "codex" / "AGENTS.md").write_text(
                "读取 `rules/shared/missing.md`\n", encoding="utf-8"
            )
            errors: list[str] = []

            validator.check_agents_paths(root, errors)

        self.assertEqual(errors, ["codex/AGENTS.md: missing rules/shared/missing.md"])
