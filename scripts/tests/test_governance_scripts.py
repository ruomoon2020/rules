import importlib.util
import io
import re
import shutil
import subprocess
import sys
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPTS = ROOT / "scripts"
CHECK_SCRIPT = SCRIPTS / "check-project-adoption.py"
SYNC_GOVERNANCE_SCRIPT = SCRIPTS / "sync-common-governance.py"
COMMON_GOVERNANCE_VALIDATOR = ROOT / "common-governance" / "scripts" / "validate-package.py"
REPOSITORY_VALIDATOR = SCRIPTS / "validate-repository.py"


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

    def test_backend_gradle_fixture_passes(self):
        repo = ROOT / "examples" / "adoption-fixture" / "backend-gradle"
        result = subprocess.run(
            [sys.executable, str(CHECK_SCRIPT), "--repo", str(repo), "--stack", "backend"],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_backend_accepts_gradle_wrapper(self):
        import tempfile

        spec = importlib.util.spec_from_file_location("adoption", CHECK_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "gradlew").write_text("#!/bin/sh\n", encoding="utf-8")
            (repo / "build.gradle.kts").write_text("plugins { java }\n", encoding="utf-8")
            errors: list[str] = []
            mod.check_build_tool(repo, errors)
        self.assertEqual(errors, [])

    def test_required_governance_rejects_missing_package(self):
        import tempfile

        spec = importlib.util.spec_from_file_location("adoption", CHECK_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        with tempfile.TemporaryDirectory() as tmp:
            errors: list[str] = []
            mod.check_governance_package(Path(tmp) / "missing", errors, required=True)
            self.assertEqual(len(errors), 1)
            self.assertIn("common governance incomplete", errors[0])

    def test_common_governance_package_passes(self):
        spec = importlib.util.spec_from_file_location("adoption", CHECK_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        errors: list[str] = []
        mod.check_governance_package(ROOT / "common-governance", errors, required=True)
        self.assertEqual(errors, [])

    def test_required_governance_rejects_invalid_manifest(self):
        spec = importlib.util.spec_from_file_location("adoption", CHECK_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            package = Path(tmp) / "common-governance"
            shutil.copytree(ROOT / "common-governance", package)
            (package / "MANIFEST.json").write_text("corrupt", encoding="utf-8")
            errors: list[str] = []
            mod.check_governance_package(package, errors, required=True)

        self.assertEqual(len(errors), 1)
        self.assertIn("invalid MANIFEST.json", errors[0])

    def test_required_governance_rejects_non_object_manifest(self):
        spec = importlib.util.spec_from_file_location("adoption", CHECK_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            package = Path(tmp) / "common-governance"
            shutil.copytree(ROOT / "common-governance", package)
            (package / "MANIFEST.json").write_text("[]\n", encoding="utf-8")
            errors: list[str] = []
            mod.check_governance_package(package, errors, required=True)

        self.assertEqual(len(errors), 1)
        self.assertIn("MANIFEST.json root must be an object", errors[0])

    def test_required_governance_rejects_checksum_drift(self):
        spec = importlib.util.spec_from_file_location("adoption", CHECK_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            package = Path(tmp) / "common-governance"
            shutil.copytree(ROOT / "common-governance", package)
            with (package / "README.md").open("a", encoding="utf-8") as stream:
                stream.write("\ndrift\n")
            errors: list[str] = []
            mod.check_governance_package(package, errors, required=True)

        self.assertEqual(len(errors), 1)
        self.assertIn("checksum mismatch README.md", errors[0])

    def test_common_governance_ssot_is_in_sync(self):
        result = subprocess.run(
            [sys.executable, str(SYNC_GOVERNANCE_SCRIPT)],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn(b"\r\n", (ROOT / "common-governance" / "MANIFEST.json").read_bytes())
        self.assertEqual(
            (ROOT / "scripts" / "check-project-adoption.py").read_bytes(),
            (ROOT / "common-governance" / "scripts" / "check-project-adoption.py").read_bytes(),
        )

    def test_common_governance_package_consistency(self):
        result = subprocess.run(
            [sys.executable, str(COMMON_GOVERNANCE_VALIDATOR)],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_distributed_validator_rejects_checksum_drift(self):
        import tempfile

        spec = importlib.util.spec_from_file_location(
            "common_governance_validator", COMMON_GOVERNANCE_VALIDATOR
        )
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        with tempfile.TemporaryDirectory() as tmp:
            package = Path(tmp) / "common-governance"
            shutil.copytree(ROOT / "common-governance", package)
            with (package / "README.md").open("a", encoding="utf-8") as stream:
                stream.write("\ndrift\n")
            mod.ROOT = package
            output = io.StringIO()
            with redirect_stdout(output), redirect_stderr(output):
                result = mod.main()

        self.assertEqual(result, 1)
        self.assertIn("checksum mismatch README.md", output.getvalue())

    def test_distributed_package_runs_strict_adoption_check(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp) / "frontend"
            shutil.copytree(ROOT / "examples" / "adoption-fixture" / "frontend", repo)
            package = repo / "common-governance"
            shutil.copytree(ROOT / "common-governance", package)
            result = subprocess.run(
                [
                    sys.executable,
                    str(package / "scripts" / "check-project-adoption.py"),
                    "--repo",
                    str(repo),
                    "--stack",
                    "frontend",
                    "--strict",
                    "--require-governance",
                ],
                capture_output=True,
                text=True,
                cwd=repo,
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_credential_scan_workflow_is_pinned_and_read_only(self):
        import yaml

        workflow_path = (
            ROOT / "common-governance" / "examples" / "ci" / "credential-scan-required.yml"
        )
        workflow_text = workflow_path.read_text(encoding="utf-8")
        workflow = yaml.safe_load(workflow_text)

        self.assertEqual(workflow["permissions"], {"contents": "read"})
        steps = workflow["jobs"]["scan"]["steps"]
        checkout = next(step for step in steps if step.get("uses") == "actions/checkout@v4")
        self.assertEqual(checkout["with"]["fetch-depth"], 0)
        self.assertEqual(workflow["env"]["GITLEAKS_VERSION"], "8.30.0")
        install = next(step for step in steps if step.get("name") == "Install pinned scanner")
        self.assertIn("sha256sum --check", install["run"])
        canary = next(step for step in steps if step.get("name") == "Verify scanner behavior")
        self.assertIn("must-detect.txt", canary["run"])
        self.assertIn('if [ "${status}" -ne 1 ]', canary["run"])
        scanner = next(step for step in steps if step.get("name") == "Scan repository history")
        self.assertEqual(scanner["run"], "gitleaks git --redact --verbose .")

    def test_supply_chain_workflow_rejects_ambiguous_node_lockfiles(self):
        import yaml

        source = ROOT / "examples" / "ci" / "supply-chain-required.yml"
        distributed = (
            ROOT / "common-governance" / "examples" / "ci" / "supply-chain-required.yml"
        )
        self.assertEqual(source.read_bytes(), distributed.read_bytes())
        workflow = yaml.safe_load(source.read_text(encoding="utf-8"))
        self.assertEqual(workflow["permissions"], {"contents": "read"})
        steps = workflow["jobs"]["node-dependency-policy"]["steps"]
        lockfile = next(step for step in steps if step.get("name") == "Validate Node lockfile")
        self.assertIn('"${#locks[@]}" -ne 1', lockfile["run"])
        self.assertIn("does not silently approximate Yarn audits", lockfile["run"])
        licenses = next(step for step in steps if step.get("name") == "Check production licenses")
        self.assertIn("license-checker@25.0.1", licenses["run"])
        maven = workflow["jobs"]["maven-dependency-check"]["steps"][-1]
        self.assertIn("dependency-check-maven:12.2.2:check", maven["run"])

    def test_governance_workflow_runs_strict_fixture_command(self):
        workflow = (ROOT / ".github" / "workflows" / "validate-rules-packages.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn("--strict --require-governance", workflow)
        self.assertRegex(
            workflow,
            re.compile(r"cp -R common-governance .*adoption-fixture/frontend/common-governance"),
        )
        self.assertIn("python scripts/validate-repository.py", workflow)
        self.assertIn("actionlint/cmd/actionlint@v1.7.12", workflow)

    def test_repository_hygiene_validator_passes(self):
        result = subprocess.run(
            [sys.executable, str(REPOSITORY_VALIDATOR)],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_repository_hygiene_validator_rejects_broken_artifacts(self):
        import tempfile

        spec = importlib.util.spec_from_file_location("repository_validator", REPOSITORY_VALIDATOR)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "broken.md").write_text(
                "[missing](missing.md)\ntrailing space \n", encoding="utf-8"
            )
            (root / "broken.yml").write_text("items: [\n", encoding="utf-8")
            errors, links, yaml_files = mod.validate_repository(root)

        self.assertEqual(links, 1)
        self.assertEqual(yaml_files, 1)
        self.assertTrue(any("trailing whitespace" in error for error in errors))
        self.assertTrue(any("missing local link" in error for error in errors))
        self.assertTrue(any("invalid YAML" in error for error in errors))


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

    def test_generated_manifests_use_lf(self):
        for rel in (
            "web-front/rules/evals/topic-manifest.yaml",
            "web-backend/rules/evals/topic-manifest.yaml",
            "miniapp/rules/evals/topic-manifest.yaml",
        ):
            self.assertNotIn(b"\r\n", (ROOT / rel).read_bytes(), rel)
