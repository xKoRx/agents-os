#!/usr/bin/env python3
"""Thin, read-only aggregation for AGENTS OS health providers."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Optional


MARKER = "80-agents/agents-os/agents-os.md"
PROVIDER_TIMEOUT_SECONDS = 30
COMPONENT_ORDER = ("structural", "conformance", "context", "canonical")
PROVIDERS = {
    "conformance": "80-agents/tools/conformance-harness/agents_os_conformance.py",
    "context": "80-agents/tools/context-budget/context_budget.py",
    "canonical": "80-agents/tools/canonical-linter/canonical_linter.py",
}
VERDICT_ORDER = {"SKIP": 0, "PASS": 1, "WARN": 2, "FAIL": 3}


def git_head(root: Path) -> Optional[str]:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=root, text=True,
            capture_output=True, check=False, timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    return result.stdout.strip() if result.returncode == 0 else None


def verdict_from_counts(counts: dict[str, int]) -> str:
    if counts["fail"]:
        return "FAIL"
    if counts["warn"]:
        return "WARN"
    if counts["pass"]:
        return "PASS"
    return "SKIP"


def error_component(name: str, source: str, message: str) -> dict[str, Any]:
    return {
        "name": name,
        "execution_status": "ERROR",
        "verdict": "SKIP",
        "pass_count": 0,
        "fail_count": 0,
        "warn_count": 0,
        "skip_count": 0,
        "finding_count": 0,
        "metrics": {},
        "source_entrypoint": source,
        "records": [],
        "findings": [],
        "execution_error": message[:500],
    }


def normalized_finding(
    provider: str,
    check_id: str,
    status: str,
    details: str,
    evidence: Any,
    **extra: Any,
) -> dict[str, Any]:
    finding = {
        "provider": provider,
        "check_id": check_id,
        "status": status,
        "observed": details,
        "evidence": evidence,
    }
    finding.update({key: value for key, value in extra.items() if value not in (None, "")})
    return finding


def structural_component(doc: dict[str, Any], source: str) -> dict[str, Any]:
    raw = doc["counts"]
    counts = {
        "pass": 1 if not raw["high"] and not raw["medium"] else 0,
        "fail": raw["high"],
        "warn": raw["medium"],
        "skip": 0,
    }
    findings = [
        normalized_finding(
            "structural", item["check"],
            "FAIL" if item["severity"] == "HIGH" else "WARN" if item["severity"] == "MEDIUM" else "INFO",
            item["message"], [], component=item["check"], severity=item["severity"], path=item["path"],
        )
        for item in doc["findings"]
    ]
    return {
        "name": "structural",
        "execution_status": "OK",
        "verdict": verdict_from_counts(counts),
        "pass_count": counts["pass"],
        "fail_count": counts["fail"],
        "warn_count": counts["warn"],
        "skip_count": 0,
        "finding_count": len(doc["findings"]),
        "metrics": {"high": raw["high"], "medium": raw["medium"], "low": raw["low"], "startup_estimated_tokens": doc["startup_estimated_tokens"]},
        "source_entrypoint": source,
        "records": doc["findings"],
        "findings": findings,
    }


def provider_args(name: str, source: Path, root: Path, live: bool) -> list[str]:
    args = [sys.executable, str(source), "--json", "--no-write", "--vault-root", str(root)]
    if name == "conformance" and not live:
        args.append("--no-live")
    if name == "context" and live:
        args.append("--live")
    return args


def records_and_counts(name: str, doc: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, int]]:
    records = doc.get("checks" if name == "canonical" else "scenarios")
    raw_counts = doc.get("counts")
    if not isinstance(records, list) or not isinstance(raw_counts, dict):
        raise ValueError("provider JSON lacks records or counts")
    return records, {key: int(raw_counts.get(key, raw_counts.get(key.upper(), 0))) for key in ("pass", "fail", "warn", "skip")}


def external_findings(name: str, records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for record in records:
        check_id = str(record.get("check_id") or record.get("id") or "unknown")
        verdict = str(record.get("verdict") or record.get("state") or "SKIP").upper()
        nested = record.get("findings") if name == "canonical" else None
        if isinstance(nested, list) and nested:
            for item in nested:
                output.append(normalized_finding(
                    name, check_id, str(item.get("status") or verdict).upper(),
                    str(item.get("observed") or item.get("details") or record.get("details") or ""),
                    item.get("evidence") or record.get("evidence") or [],
                    component=item.get("category") or record.get("category"),
                    severity=item.get("severity") or record.get("severity"),
                    path=item.get("path"), confidence=item.get("confidence"),
                    expected=item.get("expected"), recommended_action=item.get("recommended_action"),
                ))
        elif verdict != "PASS":
            output.append(normalized_finding(
                name, check_id, verdict, str(record.get("details") or record.get("skip_reason") or ""),
                record.get("evidence") or [], component=record.get("category") or record.get("level"),
                severity=record.get("severity"),
            ))
    return output


def external_component(name: str, root: Path, live: bool) -> dict[str, Any]:
    source_rel = PROVIDERS[name]
    source = root / source_rel
    if not source.is_file():
        return error_component(name, source_rel, "provider entrypoint is missing")
    try:
        result = subprocess.run(
            provider_args(name, source, root, live), cwd=root, text=True,
            capture_output=True, check=False, timeout=PROVIDER_TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired:
        return error_component(name, source_rel, f"provider timed out after {PROVIDER_TIMEOUT_SECONDS}s")
    except OSError as exc:
        return error_component(name, source_rel, f"provider could not start: {type(exc).__name__}: {exc}")
    try:
        doc = json.loads(result.stdout)
        records, counts = records_and_counts(name, doc)
    except (ValueError, TypeError, json.JSONDecodeError) as exc:
        return error_component(name, source_rel, f"invalid provider JSON: {exc}")
    if result.returncode not in (0, 1):
        return error_component(name, source_rel, f"provider exit {result.returncode}: {result.stderr.strip()}")
    if (result.returncode == 1) != bool(counts["fail"]):
        return error_component(name, source_rel, "provider exit code contradicts its FAIL count")
    findings = external_findings(name, records)
    return {
        "name": name,
        "execution_status": "OK",
        "verdict": verdict_from_counts(counts),
        "pass_count": counts["pass"],
        "fail_count": counts["fail"],
        "warn_count": counts["warn"],
        "skip_count": counts["skip"],
        "finding_count": int(doc.get("counts", {}).get("findings", len(findings))),
        "metrics": doc.get("totals") or doc.get("context_baseline") or {},
        "source_entrypoint": source_rel,
        "records": records,
        "findings": findings,
    }


def overall(components: list[dict[str, Any]]) -> dict[str, str]:
    execution = "ERROR" if any(item["execution_status"] == "ERROR" for item in components) else "OK"
    valid = [item["verdict"] for item in components if item["execution_status"] == "OK"]
    verdict = max(valid, key=lambda item: VERDICT_ORDER[item]) if valid else "SKIP"
    return {"execution_status": execution, "verdict": verdict}


def build_report(
    root: Path,
    selected: list[str],
    live: bool,
    strict: bool,
    structural_runner: Callable[[Path], dict[str, Any]],
    head_reader: Callable[[Path], Optional[str]] = git_head,
) -> dict[str, Any]:
    start = head_reader(root)
    components: list[dict[str, Any]] = []
    for name in selected:
        if name == "structural":
            source = "80-agents/skills/agents-os-doctor/scripts/doctor.py"
            try:
                components.append(structural_component(structural_runner(root), source))
            except Exception as exc:
                components.append(error_component(name, source, f"structural provider crashed: {type(exc).__name__}: {exc}"))
        else:
            components.append(external_component(name, root, live))
    end = head_reader(root)
    stable = start == end if start is not None and end is not None else None
    return {
        "schema_version": 1,
        "tool": "agents-os-doctor",
        "vault_root": str(root),
        "baseline_start": start,
        "baseline_end": end,
        "baseline_stable": stable,
        "live": live,
        "strict": strict,
        "overall": overall(components),
        "components": components,
    }


def context_summary(metrics: dict[str, Any]) -> Optional[str]:
    always = metrics.get("always_load") or {}
    packs = metrics.get("scope_pack") or {}
    if not always:
        return None
    parts = ["DEFAULT≈%s" % always.get("estimated_tokens", "?")]
    parts.extend("%s≈%s" % (domain.upper(), values.get("estimated_tokens", "?"))
                 for domain, values in sorted(packs.items()))
    return " · ".join(parts) + " estimated_tokens"


def actionable_findings(report: dict[str, Any], limit: int) -> list[dict[str, Any]]:
    """Select a bounded cross-provider sample without letting one corpus dominate."""
    selected: list[dict[str, Any]] = []
    remaining: list[dict[str, Any]] = []
    for status in ("FAIL", "WARN"):
        for component in report["components"]:
            candidates = [item for item in component["findings"] if item["status"] == status]
            if candidates:
                selected.append(candidates[0])
                remaining.extend(candidates[1:])
    if len(selected) < limit:
        remaining.sort(key=lambda item: (0 if item["status"] == "FAIL" else 1, item["provider"], item["check_id"]))
        selected.extend(remaining[:limit - len(selected)])
    return selected[:limit]


def human_summary(report: dict[str, Any], max_findings: int = 5) -> str:
    start = (report["baseline_start"] or "unknown")[:9]
    end = (report["baseline_end"] or "unknown")[:9]
    stability = "stable" if report["baseline_stable"] is True else "moved" if report["baseline_stable"] is False else "unknown"
    lines = ["AGENTS-OS DOCTOR", f"baseline: {start} → {end} ({stability})", f"mode: read-only / {'live' if report['live'] else 'non-live'}", ""]
    for item in report["components"]:
        label = item["name"].upper().ljust(12)
        if item["execution_status"] == "ERROR":
            lines.append(f"{label} ERROR  {item['execution_error']}")
            continue
        counts = f"{item['pass_count']} pass · {item['fail_count']} fail · {item['warn_count']} warn · {item['skip_count']} skip"
        if item["name"] == "structural":
            metrics = item["metrics"]
            counts = f"{metrics['high']} high · {metrics['medium']} medium · {metrics['low']} low"
        elif item["name"] == "canonical":
            counts += f" · {item['finding_count']} findings"
        lines.append(f"{label} {item['verdict'].ljust(5)}  {counts}")
        if item["name"] == "context":
            summary = context_summary(item["metrics"])
            if summary:
                lines.append(" " * 14 + summary)
    health = report["overall"]["verdict"]
    execution = report["overall"]["execution_status"]
    lines.extend(["", f"OVERALL      {health}" + (" · execution ERROR" if execution == "ERROR" else "")])
    actionable = actionable_findings(report, max_findings)
    if actionable:
        lines.extend(["", "Top actionable findings:"])
        for finding in actionable:
            detail = str(finding.get("observed") or "").replace("\n", " ")[:180]
            lines.append(f"- {finding['provider']}/{finding['check_id']} [{finding['status']}] {detail}")
        lines.append("Use --json for machine-readable detail.")
    return "\n".join(lines)


def exit_code(report: dict[str, Any]) -> int:
    if report["overall"]["execution_status"] == "ERROR":
        return 2
    if report["overall"]["verdict"] == "FAIL":
        return 1
    if report["strict"] and any(item["warn_count"] or item["skip_count"] for item in report["components"]):
        return 1
    return 0


def main(argv: Optional[list[str]], structural_runner: Callable[[Path], dict[str, Any]]) -> int:
    parser = argparse.ArgumentParser(description="Unified, read-only AGENTS OS health surface")
    parser.add_argument("--component", choices=(*COMPONENT_ORDER, "all"), default="all")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--strict", action="store_true", help="exit non-zero on WARN or SKIP without mutating verdicts")
    parser.add_argument("--live", action="store_true", help="enable provider-owned read-only live observations")
    parser.add_argument("--vault-root")
    args = parser.parse_args(argv)
    default_root = Path(__file__).resolve().parents[4]
    root = Path(args.vault_root).expanduser().resolve() if args.vault_root else default_root
    if not (root / MARKER).is_file():
        print(f"ERROR: VAULT_ROOT does not contain {MARKER}: {root}", file=sys.stderr)
        return 2
    selected = list(COMPONENT_ORDER if args.component == "all" else (args.component,))
    report = build_report(root, selected, args.live, args.strict, structural_runner)
    if args.json:
        json.dump(report, sys.stdout, indent=2, ensure_ascii=False)
        print()
    else:
        print(human_summary(report))
    return exit_code(report)
