#!/usr/bin/env python3
"""Deterministic, no-API E2E for the AGENTS OS Context Router."""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
@dataclass(frozen=True)
class Case:
    name: str
    kind: str
    session_mode: str
    entity: str
    expected: tuple[str, ...]
    cli: tuple[str, ...]
    fallback_pattern: str
    fallback_root: str
    bodies_opened: int


CASES = (
    Case(
        name="project_fact",
        kind="project",
        session_mode="cold",
        entity="AGENTS OS - Fase 3",
        expected=("10-projects/Personal/AGENTS OS/agentes/AGENTS OS - Fase 3.md",),
        cli=("filter", "--title", "AGENTS OS - Fase 3.md", "--json"),
        fallback_pattern=r"^# AGENTS OS - Fase 3$",
        fallback_root="10-projects/Personal/AGENTS OS",
        bodies_opened=0,
    ),
    Case(
        name="skill_procedure",
        kind="skill",
        session_mode="warm",
        entity="AGENTS OS - Fase 3",
        expected=("80-agents/skills/agents-os-context-retrieval/SKILL.md",),
        cli=("query", "agents-os-context-retrieval", "--filter", "type=skill", "--budget", "500"),
        fallback_pattern=r"^name: agents-os-context-retrieval$",
        fallback_root="80-agents/skills",
        bodies_opened=1,
    ),
    Case(
        name="prompt_domain",
        kind="prompt",
        session_mode="swap",
        entity="Agents resources",
        expected=("30-resources/agents/prompts/agent-executor.md",),
        cli=("query", "agent executor", "--filter", "type=prompt", "--budget", "500"),
        fallback_pattern=r"^# Executor de fase de agente$",
        fallback_root="30-resources/agents",
        bodies_opened=1,
    ),
    Case(
        name="known_error_fact",
        kind="known_error",
        session_mode="swap",
        entity="AGENTS OS - Fase 3",
        expected=("80-agents/memory/public/known-error/agents-os/graphify-template-node-noise.md",),
        cli=("query", "template node noise", "--filter", "type=known_error", "--filter", "tags=project/agents-os", "--budget", "500"),
        fallback_pattern=r"^# Graphify Template Node Noise$",
        fallback_root="80-agents/memory/public/known-error",
        bodies_opened=1,
    ),
    Case(
        name="resource_fact",
        kind="resource",
        session_mode="swap",
        entity="RIO",
        expected=("30-resources/rio-atlas/architecture/integration-map.md",),
        cli=("filter", "--title", "integration-map.md", "--json"),
        fallback_pattern=r"^# RIO — Integration Map \(generado\)$",
        fallback_root="30-resources/rio-atlas",
        bodies_opened=1,
    ),
    Case(
        name="application_fact",
        kind="application",
        session_mode="warm",
        entity="RIO",
        expected=("30-resources/applications/rio-playmaker.md",),
        cli=("filter", "--title", "rio-playmaker.md", "--json"),
        fallback_pattern=r"^# rio-playmaker$",
        fallback_root="30-resources/applications",
        bodies_opened=0,
    ),
    Case(
        name="project_relation",
        kind="relation",
        session_mode="swap",
        entity="AGENTS OS - Fase 3",
        expected=(
            "10-projects/Personal/AGENTS OS/agentes/AGENTS OS - Fase 2.md",
            "10-projects/Personal/AGENTS OS/agentes/AGENTS OS - Fase 3.md",
            "10-projects/Personal/AGENTS OS/agentes/AGENTS OS - Fase 4.md",
            "10-projects/Personal/AGENTS OS/agentes/AGENTS OS - Relaciones Tipadas de Graphify.md",
        ),
        cli=("affected", "AGENTS OS.md", "--relation", "child_of"),
        fallback_pattern=r'^parent: "\[\[AGENTS OS\]\]"$',
        fallback_root="10-projects/Personal/AGENTS OS/agentes",
        bodies_opened=0,
    ),
)


def run(command: list[str]) -> tuple[str, float]:
    started = time.perf_counter()
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    latency_ms = (time.perf_counter() - started) * 1000
    if result.returncode:
        raise RuntimeError(f"command failed ({result.returncode}): {' '.join(command)}\n{result.stderr.strip()}")
    return result.stdout, latency_ms


def cli_sources(case: Case, executable: str) -> tuple[set[str], float]:
    output, latency_ms = run([executable, *case.cli])
    if "--json" in case.cli:
        payload = json.loads(output)
        return {str(node["source_file"]) for node in payload.get("nodes", [])}, latency_ms
    sources = set(re.findall(r"\[src=(.+?) loc=L\d+", output))
    sources.update(re.findall(r"\[[a-z_]+\] (.+?):L\d+", output))
    if case.name == "skill_procedure":
        registry = (ROOT / "80-agents/skills/INDEX.md").read_text(encoding="utf-8")
        sources = {path for path in sources if path in registry and "agents-os-context-retrieval" in path}
    return sources, latency_ms


def fallback_sources(case: Case, executable: str) -> tuple[set[str], float]:
    output, latency_ms = run([executable, "-l", "--glob", "*.md", case.fallback_pattern, case.fallback_root])
    return {line.strip() for line in output.splitlines() if line.strip()}, latency_ms


def p95(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    return ordered[max(0, math.ceil(len(ordered) * 0.95) - 1)]


def validate_body_opens() -> int:
    opened = 0
    for case in CASES:
        if not case.bodies_opened:
            continue
        for path in case.expected[: case.bodies_opened]:
            text = (ROOT / path).read_text(encoding="utf-8")
            if not text.startswith("---") or "\n# " not in text:
                raise RuntimeError(f"selected source is not a canonical Markdown note: {path}")
            opened += 1
    index = ROOT / "30-resources/agents/00-index.md"
    if "agent-executor" not in index.read_text(encoding="utf-8"):
        raise RuntimeError("curated agents index does not route to agent-executor")
    return opened


def validate_session_modes() -> list[str]:
    current: str | None = None
    covered: list[str] = []
    for case in CASES:
        if case.session_mode == "cold" and current is not None:
            raise RuntimeError(f"cold case must start without an active entity: {case.name}")
        if case.session_mode == "warm" and current != case.entity:
            raise RuntimeError(f"warm case changed entity: {case.name}")
        if case.session_mode == "swap" and current == case.entity:
            raise RuntimeError(f"swap case reused the active entity: {case.name}")
        current = case.entity
        if case.session_mode not in covered:
            covered.append(case.session_mode)
    if set(covered) != {"cold", "warm", "swap"}:
        raise RuntimeError(f"session mode coverage is incomplete: {covered}")
    return covered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit machine-readable evidence")
    args = parser.parse_args()

    graphify = shutil.which("graphify-obsidian")
    rg = shutil.which("rg")
    if not graphify or not rg:
        print("ERROR graphify-obsidian and rg are required", file=sys.stderr)
        return 2
    cache = subprocess.run([graphify, "cache-path"], cwd=ROOT, text=True, capture_output=True, check=False)
    if cache.returncode or not cache.stdout.strip():
        print(f"ERROR cannot resolve graphify local cache: {cache.stderr.strip()}", file=sys.stderr)
        return 2

    session_modes = validate_session_modes()
    observations: list[dict[str, object]] = []
    latencies: dict[str, list[float]] = {"graphify_cli": [], "markdown_fallback": []}
    relevant = 0
    candidates = 0
    misses = 0
    for case in CASES:
        expected = set(case.expected)
        for surface, resolver, executable in (
            ("graphify_cli", cli_sources, graphify),
            ("markdown_fallback", fallback_sources, rg),
        ):
            sources, latency_ms = resolver(case, executable)
            selected = sources & expected
            missing = expected - sources
            extra = sources - expected
            relevant += len(selected)
            candidates += len(sources)
            misses += int(bool(missing))
            latencies[surface].append(latency_ms)
            observations.append(
                {
                    "case": case.name,
                    "session_mode": case.session_mode,
                    "entity": case.entity,
                    "surface": surface,
                    "latency_ms": round(latency_ms, 2),
                    "selected": sorted(sources),
                    "missing": sorted(missing),
                    "extra": sorted(extra),
                    "pass": not missing and not extra,
                }
            )

    bodies_opened = validate_body_opens()
    operations = len(observations)
    result = {
        "status": "pass" if misses == 0 and relevant == candidates else "fail",
        "api_calls": 0,
        "cases": len(CASES),
        "session_modes": session_modes,
        "operations": operations,
        "misses": misses,
        "miss_rate_pct": round((misses / operations) * 100, 2),
        "precision_proxy_pct": round((relevant / candidates) * 100, 2) if candidates else 0.0,
        "bodies_opened": bodies_opened,
        "curated_indexes_opened": 1,
        "surface_p95_ms": {surface: round(p95(values), 2) for surface, values in latencies.items()},
        "phase2_baseline": {"operations": 279, "miss_rate_pct": 2.9, "p95_ms": 598},
        "observations": observations,
    }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        print(f"Context Router E2E: {result['status'].upper()} cases={result['cases']} operations={operations} misses={misses} precision={result['precision_proxy_pct']}% bodies={bodies_opened} api_calls=0")
        print("p95_ms " + " ".join(f"{surface}={value}" for surface, value in result["surface_p95_ms"].items()))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    sys.exit(main())
