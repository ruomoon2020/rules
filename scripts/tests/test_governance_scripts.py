import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
CHECK_SCRIPT = SCRIPTS / "check-project-adoption.py"


class CheckProjectAdoptionTests(unittest.TestCase):
    def test_frontend_fixture_passes(self):
        repo = ROOT / "examples" / "adoption-fixture" / "frontend"
        result = subprocess.run(
            [sys.executable, str(CHECK_SCRIPT), "--repo", str(repo), "--stack", "frontend"],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


class EvalTopicManifestTests(unittest.TestCase):
    def test_suite_drift_detection_logic(self):
        sys.path.insert(0, str(SCRIPTS))
        import eval_topic_manifest as etm

        rules_root = ROOT / "web-front" / "rules"
        live = etm.live_smoke_suites(rules_root, "E")
        self.assertIn("Security", live)
        tampered = dict(live)
        tampered["Security"] = ["E99"]
        errors: list[str] = []
        for name, live_ids in live.items():
            if sorted(tampered.get(name, [])) != sorted(live_ids):
                errors.append(name)
        self.assertIn("Security", errors)

    def test_frontend_manifest_suites_in_sync(self):
        sys.path.insert(0, str(SCRIPTS))
        import eval_topic_manifest as etm

        rules_root = ROOT / "web-front" / "rules"
        manifest = etm.load_manifest(rules_root / "evals" / "topic-manifest.yaml")
        live = etm.live_smoke_suites(rules_root, "E")
        for name, live_ids in live.items():
            self.assertEqual(
                sorted((manifest.get("suites") or {}).get(name, [])),
                sorted(live_ids),
                name,
            )
