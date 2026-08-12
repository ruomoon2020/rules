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

    def test_l0_scope_rejects_numbered_high_level_rule(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "shared").mkdir()
            (root / "shared" / "00-must-follow.md").write_text(
                "## 条件触发路由（不计入 Level 0 硬规则）\n"
                "1. 见 42-cost-governance.md\n",
                encoding="utf-8",
            )
            errors: list[str] = []

            validator.check_l0_hard_rule_scope(root, errors)

        self.assertEqual(
            errors,
            ["00-must-follow.md: non-L0 shared rule numbered as L0: 42-cost-governance.md"],
        )

    def test_l0_scope_rejects_high_level_topic_without_file_reference(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "shared").mkdir()
            (root / "shared" / "00-must-follow.md").write_text(
                "1. 所有项目必须完成威胁建模。\n"
                "## 条件触发路由（不计入 Level 0 硬规则）\n",
                encoding="utf-8",
            )
            errors: list[str] = []

            validator.check_l0_hard_rule_scope(root, errors)

        self.assertEqual(
            errors,
            ["00-must-follow.md: high-level topic numbered as L0: 威胁建模"],
        )
