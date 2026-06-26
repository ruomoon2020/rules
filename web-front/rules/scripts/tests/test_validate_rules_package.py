import importlib.util
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
