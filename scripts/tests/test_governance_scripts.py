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
RELEASE_EVIDENCE_SCRIPT = SCRIPTS / "validate-release-evidence.py"
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

    def test_level_one_requires_frontend_contract_api_check_and_local_override(self):
        import tempfile

        spec = importlib.util.spec_from_file_location("adoption_level", CHECK_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "AGENTS.md").write_text("read rules/shared\n", encoding="utf-8")
            (repo / "rules" / "codex").mkdir(parents=True)
            (repo / "rules" / "shared").mkdir()
            (repo / "rules" / "VERSION").write_text("1.0.0\n", encoding="utf-8")
            (repo / "rules" / "codex" / "AGENTS.md").write_text("# rules\n", encoding="utf-8")
            (repo / "rules" / "shared" / "00-must-follow.md").write_text("# rules\n", encoding="utf-8")
            (repo / ".cursor" / "rules").mkdir(parents=True)
            (repo / ".cursor" / "rules" / "00-project-overview.mdc").write_text("# overview\n", encoding="utf-8")
            (repo / "package.json").write_text(
                '{"scripts":{"lint":"x","type-check":"x","build":"x"}}\n',
                encoding="utf-8",
            )
            errors = mod.run_stack(repo, "frontend", strict=False, level=1)

        self.assertIn("package.json missing script: api:check", errors)
        self.assertTrue(any("MISSING contract SSOT" in error for error in errors))
        self.assertTrue(any("99-project-local.mdc" in error for error in errors))

    def test_level_two_automatically_requires_governance_package(self):
        repo = ROOT / "examples" / "adoption-fixture" / "frontend"
        result = subprocess.run(
            [
                sys.executable,
                str(CHECK_SCRIPT),
                "--repo",
                str(repo),
                "--stack",
                "frontend",
                "--level",
                "2",
            ],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("common governance incomplete", result.stdout + result.stderr)

    def test_level_two_rejects_missing_real_control_evidence(self):
        import tempfile

        spec = importlib.util.spec_from_file_location("adoption_evidence", CHECK_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "governance-adoption.yaml").write_text(
                "schema_version: 1\nlevel: 2\nowner: team\nreview_due: '2099-01-01'\n"
                "checks:\n"
                "  rules_adoption: {evidence: .github/workflows/missing.yml}\n"
                "  credential_scan: {evidence: .github/workflows/missing.yml}\n"
                "  supply_chain: {evidence: .github/workflows/missing.yml}\n"
                "branch_protection: {enabled: true, evidence: docs/missing.md}\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            mod.check_level_evidence(repo, errors, 2)

        self.assertTrue(any("evidence not found" in error for error in errors))

    def test_frontend_fixture_passes_level_three_evidence(self):
        repo = ROOT / "examples" / "adoption-fixture" / "frontend"
        result = subprocess.run(
            [
                sys.executable,
                str(CHECK_SCRIPT),
                "--repo",
                str(repo),
                "--stack",
                "frontend",
                "--level",
                "3",
                "--governance-dir",
                str(ROOT / "common-governance"),
            ],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_frontend_contract_accepts_json_schema(self):
        import tempfile

        spec = importlib.util.spec_from_file_location("adoption_contract", CHECK_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "contracts").mkdir()
            (repo / "contracts" / "schema.json").write_text("{}\n", encoding="utf-8")
            errors: list[str] = []
            mod.check_contracts(repo, errors, required=True, flexible=True)

        self.assertEqual(errors, [])

    def test_frontend_contract_accepts_declared_https_ssot(self):
        import tempfile

        spec = importlib.util.spec_from_file_location("adoption_contract_url", CHECK_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "AGENTS.md").write_text(
                "Contract SSOT: https://contracts.example.invalid/openapi.yaml\n",
                encoding="utf-8",
            )
            errors: list[str] = []
            mod.check_contracts(repo, errors, required=True, flexible=True)

        self.assertEqual(errors, [])

    def test_package_script_rejects_echo_placeholder(self):
        import tempfile

        spec = importlib.util.spec_from_file_location("adoption_scripts", CHECK_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "package.json").write_text('{"scripts":{"lint":"echo ok"}}\n', encoding="utf-8")
            errors: list[str] = []
            mod.check_package_json_scripts(repo, errors, ("lint",))

        self.assertEqual(errors, ["package.json script is placeholder: lint"])

    def test_backend_level_one_requires_ci_build_evidence(self):
        import tempfile

        spec = importlib.util.spec_from_file_location("adoption_backend_ci", CHECK_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        with tempfile.TemporaryDirectory() as tmp:
            errors: list[str] = []
            mod.check_backend_ci(Path(tmp), errors, required=True)

        self.assertEqual(errors, ["MISSING backend CI evidence running Maven verify/test or Gradle check/test"])

    def test_strict_pr_template_requires_traceability_fields(self):
        import tempfile

        spec = importlib.util.spec_from_file_location("adoption_pr", CHECK_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            template = repo / ".github" / "pull_request_template.md"
            template.parent.mkdir(parents=True)
            template.write_text("# Summary\n", encoding="utf-8")
            errors: list[str] = []
            mod.check_pr_template(repo, errors, strict=True)

        self.assertEqual(len(errors), 4)
        self.assertTrue(any("acceptance criteria" in error for error in errors))

    def test_strict_pr_template_ignores_keywords_only_in_comments(self):
        import tempfile

        spec = importlib.util.spec_from_file_location("adoption_pr_comments", CHECK_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            template = repo / ".github" / "pull_request_template.md"
            template.parent.mkdir(parents=True)
            template.write_text("# Summary\n<!-- requirement acceptance evidence rollback -->\n", encoding="utf-8")
            errors: list[str] = []
            mod.check_pr_template(repo, errors, strict=True)

        self.assertEqual(len(errors), 4)

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

    def test_distributed_package_runs_level_two_adoption_check(self):
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
                    "--level",
                    "2",
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
        self.assertIn("--stack frontend --level 2", workflow)
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


class ReleaseEvidenceTests(unittest.TestCase):
    def test_release_evidence_sample_passes(self):
        result = subprocess.run(
            [
                sys.executable,
                str(RELEASE_EVIDENCE_SCRIPT),
                "--file",
                str(ROOT / "examples" / "release-evidence.yaml"),
            ],
            capture_output=True,
            text=True,
            cwd=ROOT,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_release_evidence_rejects_placeholders_and_untested_rollback(self):
        spec = importlib.util.spec_from_file_location("release_evidence", RELEASE_EVIDENCE_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        invalid = {
            "schema_version": 2,
            "release": {
                "id": "TODO",
                "version": "1.0.0",
                "environment": "production",
                "owner": "team",
                "change_ref": "PR-1",
                "commit_sha": "not-a-sha",
                "artifact_digest": "sha256:bad",
                "approved_at": "2026-08-14T10:00:00+08:00",
                "rules_versions": {"common-governance": "2.0.0"},
            },
            "requirements": [{"id": "REQ-1", "acceptance_evidence": "TBD"}],
            "risk": {"level": "high", "summary": "change", "rollout_evidence": "N/A"},
            "rollback": {"tested": False, "command_or_runbook": "TODO", "owner": "team"},
            "observability": {
                "dashboards": ["dashboard"],
                "alerts": ["alert"],
                "observation_window_minutes": 60,
            },
            "gates": {name: "passed" for name in mod.GATE_NAMES},
            "exceptions": [],
        }
        errors = mod.validate_release_evidence(invalid)

        self.assertTrue(any("release.id" in error for error in errors))
        self.assertTrue(any("acceptance_evidence" in error for error in errors))
        self.assertIn("rollback.tested must be true", errors)
        self.assertTrue(any("risk.rollout_evidence" in error for error in errors))
        self.assertTrue(any("commit_sha" in error for error in errors))
        self.assertTrue(any("artifact_digest" in error for error in errors))

    def test_release_evidence_rejects_unmatched_exception(self):
        spec = importlib.util.spec_from_file_location("release_exception", RELEASE_EVIDENCE_SCRIPT)
        mod = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        spec.loader.exec_module(mod)

        import yaml

        data = yaml.safe_load((ROOT / "examples" / "release-evidence.yaml").read_text(encoding="utf-8"))
        data["gates"]["security"] = "exception"
        errors = mod.validate_release_evidence(data)

        self.assertTrue(any("exception gates lack approved exception records" in error for error in errors))


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
