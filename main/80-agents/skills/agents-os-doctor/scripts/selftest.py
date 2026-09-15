#!/usr/bin/env python3
"""Integration-focused selftests for the unified Doctor orchestrator."""

from __future__ import annotations

import contextlib
import io
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import aggregate


def structural_doc(high: int = 0, medium: int = 0, low: int = 0) -> dict:
    findings = []
    for severity, count in (("HIGH", high), ("MEDIUM", medium), ("LOW", low)):
        findings.extend({"severity": severity, "check": severity.lower(), "path": "x.md", "message": "observed"} for _ in range(count))
    return {"counts": {"high": high, "medium": medium, "low": low}, "startup_estimated_tokens": 10, "findings": findings}


def component(name: str, verdict: str = "PASS", execution: str = "OK", warn: int = 0, skip: int = 0) -> dict:
    return {
        "name": name, "execution_status": execution, "verdict": verdict,
        "pass_count": 1 if verdict == "PASS" else 0,
        "fail_count": 1 if verdict == "FAIL" else 0,
        "warn_count": warn or (1 if verdict == "WARN" else 0),
        "skip_count": skip or (1 if verdict == "SKIP" else 0),
        "finding_count": 0, "metrics": {}, "source_entrypoint": "provider.py",
        "records": [], "findings": [], **({"execution_error": "boom"} if execution == "ERROR" else {}),
    }


class AggregateTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory(prefix="doctor-selftest-")
        self.root = Path(self.temp.name)
        (self.root / "80-agents/agents-os").mkdir(parents=True)
        (self.root / aggregate.MARKER).write_text("marker", encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def install_provider(self, name: str) -> Path:
        path = self.root / aggregate.PROVIDERS[name]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("# fake", encoding="utf-8")
        return path

    def test_verdict_and_overall_semantics(self) -> None:
        self.assertEqual(aggregate.verdict_from_counts({"pass": 0, "fail": 1, "warn": 2, "skip": 0}), "FAIL")
        self.assertEqual(aggregate.verdict_from_counts({"pass": 0, "fail": 0, "warn": 1, "skip": 0}), "WARN")
        self.assertEqual(aggregate.verdict_from_counts({"pass": 1, "fail": 0, "warn": 0, "skip": 4}), "PASS")
        self.assertEqual(aggregate.verdict_from_counts({"pass": 0, "fail": 0, "warn": 0, "skip": 4}), "SKIP")
        self.assertEqual(aggregate.overall([component("a"), component("b", "WARN")]), {"execution_status": "OK", "verdict": "WARN"})
        self.assertEqual(aggregate.overall([component("a", "FAIL"), component("b", execution="ERROR")]), {"execution_status": "ERROR", "verdict": "FAIL"})

    def test_structural_mapping_preserves_low_as_information(self) -> None:
        result = aggregate.structural_component(structural_doc(medium=1, low=1), "doctor.py")
        self.assertEqual(result["verdict"], "WARN")
        self.assertEqual(result["warn_count"], 1)
        self.assertEqual(result["metrics"]["low"], 1)
        self.assertEqual([item["status"] for item in result["findings"]], ["WARN", "INFO"])
        low_only = aggregate.structural_component(structural_doc(low=2), "doctor.py")
        self.assertEqual(low_only["verdict"], "PASS")
        self.assertEqual(low_only["warn_count"], 0)
        self.assertEqual([item["status"] for item in low_only["findings"]], ["INFO", "INFO"])
        report = {"overall": {"execution_status": "OK", "verdict": "PASS"}, "strict": True, "components": [low_only]}
        self.assertEqual(aggregate.exit_code(report), 0)
        self.assertEqual(aggregate.actionable_findings({"components": [low_only]}, 5), [])

    def test_provider_arguments_respect_live_ownership(self) -> None:
        source = Path("provider.py")
        self.assertIn("--no-live", aggregate.provider_args("conformance", source, self.root, False))
        self.assertNotIn("--no-live", aggregate.provider_args("conformance", source, self.root, True))
        self.assertIn("--live", aggregate.provider_args("context", source, self.root, True))
        self.assertNotIn("--live", aggregate.provider_args("canonical", source, self.root, True))
        self.assertIn("--no-write", aggregate.provider_args("canonical", source, self.root, False))

    def test_external_provider_fail_is_execution_ok(self) -> None:
        self.install_provider("conformance")
        payload = {"scenarios": [{"id": "COLD", "level": "L1", "state": "FAIL", "details": "broken", "evidence": ["proof"]}], "counts": {"PASS": 0, "FAIL": 1, "WARN": 0, "SKIP": 0}}
        completed = subprocess.CompletedProcess([], 1, json.dumps(payload), "summary")
        with mock.patch.object(aggregate.subprocess, "run", return_value=completed):
            result = aggregate.external_component("conformance", self.root, False)
        self.assertEqual((result["execution_status"], result["verdict"]), ("OK", "FAIL"))
        self.assertEqual(result["findings"][0]["check_id"], "COLD")

    def test_context_provider_owns_fidelity_gate_record_and_count(self) -> None:
        self.install_provider("context")
        payload = {"fidelity_gate": "FAIL", "scenarios": [{"id": "RULES-FIDELITY-ANCHORS", "verdict": "FAIL", "details": "anchors drifted", "evidence": ["x"]}], "counts": {"pass": 0, "fail": 1, "warn": 0, "skip": 0}, "totals": {}}
        completed = subprocess.CompletedProcess([], 1, json.dumps(payload), "")
        with mock.patch.object(aggregate.subprocess, "run", return_value=completed):
            result = aggregate.external_component("context", self.root, False)
        self.assertEqual(result["verdict"], "FAIL")
        self.assertEqual(result["fail_count"], 1)
        self.assertEqual(len(result["records"]), 1)
        self.assertEqual(result["findings"][0]["check_id"], "RULES-FIDELITY-ANCHORS")

    def test_canonical_findings_are_flattened_without_reinterpretation(self) -> None:
        self.install_provider("canonical")
        nested = {"status": "WARN", "observed": "duplicate", "evidence": ["line"], "category": "CANONICALITY", "severity": "WARN", "path": "a.md", "confidence": "EXACT", "expected": "unique"}
        payload = {"checks": [{"check_id": "CL-06", "category": "CANONICALITY", "severity": "FAIL", "verdict": "WARN", "details": "one", "findings": [nested]}], "counts": {"pass": 0, "fail": 0, "warn": 1, "skip": 0, "findings": 1}}
        completed = subprocess.CompletedProcess([], 0, json.dumps(payload), "")
        with mock.patch.object(aggregate.subprocess, "run", return_value=completed):
            result = aggregate.external_component("canonical", self.root, False)
        finding = result["findings"][0]
        self.assertEqual((finding["status"], finding["confidence"], finding["expected"]), ("WARN", "EXACT", "unique"))

    def test_provider_errors_are_isolated(self) -> None:
        self.assertEqual(aggregate.external_component("context", self.root, False)["execution_status"], "ERROR")
        self.install_provider("context")
        cases = [
            subprocess.CompletedProcess([], 0, "not-json", ""),
            subprocess.CompletedProcess([], 2, json.dumps({"scenarios": [], "counts": {}}), "bad root"),
            subprocess.CompletedProcess([], 0, json.dumps({"scenarios": [], "counts": {"fail": 1}}), ""),
        ]
        for completed in cases:
            with mock.patch.object(aggregate.subprocess, "run", return_value=completed):
                self.assertEqual(aggregate.external_component("context", self.root, False)["execution_status"], "ERROR")
        with mock.patch.object(aggregate.subprocess, "run", side_effect=subprocess.TimeoutExpired([], 30)):
            self.assertIn("timed out", aggregate.external_component("context", self.root, False)["execution_error"])
        with mock.patch.object(aggregate.subprocess, "run", side_effect=OSError("no python")):
            self.assertIn("could not start", aggregate.external_component("context", self.root, False)["execution_error"])

    def test_build_report_is_sequential_continues_after_error_and_tracks_movement(self) -> None:
        calls = []
        responses = [component("conformance", execution="ERROR"), component("context"), component("canonical", "WARN")]
        heads = iter(("aaa", "bbb"))
        def external(name: str, root: Path, live: bool) -> dict:
            calls.append(name)
            return responses[len(calls) - 1]
        with mock.patch.object(aggregate, "external_component", side_effect=external):
            report = aggregate.build_report(self.root, list(aggregate.COMPONENT_ORDER), False, False, lambda _: structural_doc(), lambda _: next(heads))
        self.assertEqual(calls, ["conformance", "context", "canonical"])
        self.assertFalse(report["baseline_stable"])
        self.assertEqual(report["overall"], {"execution_status": "ERROR", "verdict": "WARN"})

    def test_structural_crash_does_not_stop_external_provider(self) -> None:
        with mock.patch.object(aggregate, "external_component", return_value=component("context")) as external:
            report = aggregate.build_report(self.root, ["structural", "context"], False, False, lambda _: 1 / 0, lambda _: None)
        self.assertEqual(report["components"][0]["execution_status"], "ERROR")
        external.assert_called_once()
        self.assertIsNone(report["baseline_stable"])

    def test_human_output_is_bounded_and_cross_provider(self) -> None:
        report = {"baseline_start": None, "baseline_end": None, "baseline_stable": None, "live": False, "overall": {"execution_status": "OK", "verdict": "FAIL"}, "components": []}
        for name in aggregate.COMPONENT_ORDER:
            item = component(name, "FAIL")
            item["findings"] = [aggregate.normalized_finding(name, f"{name}-{n}", "FAIL", "x" * 240, []) for n in range(400)]
            item["finding_count"] = 400
            if name == "structural":
                item["metrics"] = {"high": 1, "medium": 0, "low": 0}
            report["components"].append(item)
        output = aggregate.human_summary(report, max_findings=5)
        self.assertEqual(sum(line.startswith("- ") for line in output.splitlines()), 5)
        self.assertIn("conformance/conformance-0", output)
        self.assertLess(len(output), 2000)

    def test_context_summary_and_exit_policy(self) -> None:
        metrics = {"always_load": {"estimated_tokens": 10}, "scope_pack": {"meli": {"estimated_tokens": 2}, "aranea": {"estimated_tokens": 3}}}
        self.assertIn("DEFAULT≈10", aggregate.context_summary(metrics))
        self.assertEqual(aggregate.context_summary({"always_load": {"estimated_tokens": 10}, "scope_pack": {}}), "DEFAULT≈10 estimated_tokens")
        self.assertIsNone(aggregate.context_summary({}))
        base = {"overall": {"execution_status": "OK", "verdict": "PASS"}, "strict": False, "components": [component("x", skip=1)]}
        self.assertEqual(aggregate.exit_code(base), 0)
        base["strict"] = True
        self.assertEqual(aggregate.exit_code(base), 1)
        base["overall"] = {"execution_status": "OK", "verdict": "FAIL"}
        self.assertEqual(aggregate.exit_code(base), 1)
        base["overall"] = {"execution_status": "ERROR", "verdict": "PASS"}
        self.assertEqual(aggregate.exit_code(base), 2)

    def test_main_filters_component_emits_json_and_rejects_bad_root(self) -> None:
        fake_report = {"schema_version": 1, "tool": "agents-os-doctor", "vault_root": str(self.root), "baseline_start": None, "baseline_end": None, "baseline_stable": None, "live": False, "strict": False, "overall": {"execution_status": "OK", "verdict": "PASS"}, "components": [component("context")]}
        output = io.StringIO()
        with mock.patch.object(aggregate, "build_report", return_value=fake_report) as build, contextlib.redirect_stdout(output):
            code = aggregate.main(["--component", "context", "--json", "--vault-root", str(self.root)], lambda _: structural_doc())
        self.assertEqual(code, 0)
        self.assertEqual(json.loads(output.getvalue())["tool"], "agents-os-doctor")
        self.assertEqual(build.call_args.args[1], ["context"])
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(aggregate.main(["--vault-root", str(self.root / "missing")], lambda _: structural_doc()), 2)

    def test_build_report_does_not_mutate_vault(self) -> None:
        before = {path.relative_to(self.root): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        with mock.patch.object(aggregate, "external_component", return_value=component("canonical")):
            aggregate.build_report(self.root, ["structural", "canonical"], False, False, lambda _: structural_doc(), lambda _: None)
        after = {path.relative_to(self.root): path.read_bytes() for path in self.root.rglob("*") if path.is_file()}
        self.assertEqual(before, after)

    def test_portable_default_providers_skip_absent_domains_without_error(self) -> None:
        source_root = Path(__file__).resolve().parents[4]
        runtime_files = [
            "80-agents/tools/conformance-harness/agents_os_conformance.py",
            "80-agents/tools/conformance-harness/rules.py",
            "80-agents/tools/context-budget/context_budget.py",
        ]
        for rel in runtime_files:
            target = self.root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_root / rel, target)
        registry = self.root / "30-resources/agents/domain-router-registry.md"
        registry.parent.mkdir(parents=True, exist_ok=True)
        registry.write_text("| domain | areas | router | evidence markers |\n|---|---|---|---|\n", encoding="utf-8")

        conformance = subprocess.run(
            ["python3", str(self.root / runtime_files[0]), "--json", "--no-write", "--no-live", "--scenario", "COLD-MELI", "--vault-root", str(self.root)],
            capture_output=True, text=True, timeout=30,
        )
        self.assertIn(conformance.returncode, (0, 1))
        conformance_doc = json.loads(conformance.stdout)
        scoped = next(item for item in conformance_doc["scenarios"] if item["id"] == "COLD-MELI")
        self.assertEqual(scoped["state"], "SKIP")
        self.assertIn("no instalado", scoped["details"])
        self.assertEqual(conformance_doc["context_baseline"]["scope_packs"], {})

        context = subprocess.run(
            ["python3", str(self.root / runtime_files[2]), "--json", "--no-write", "--scenario", "CTX-02", "--vault-root", str(self.root)],
            capture_output=True, text=True, timeout=30,
        )
        self.assertIn(context.returncode, (0, 1))
        context_doc = json.loads(context.stdout)
        scoped_context = next(item for item in context_doc["scenarios"] if item["id"] == "CTX-02")
        self.assertEqual(scoped_context["verdict"], "SKIP")
        self.assertIn("no instalado", scoped_context["details"])


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(AggregateTests)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    print(f"doctor integration selftest: {result.testsRun - len(result.failures) - len(result.errors)}/{result.testsRun} PASS")
    raise SystemExit(0 if result.wasSuccessful() else 1)
