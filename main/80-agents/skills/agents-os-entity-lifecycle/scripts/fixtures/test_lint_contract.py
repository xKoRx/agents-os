#!/usr/bin/env python3
"""End-to-end regression tests for the contract-driven lint and baseline gate."""

from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[5]
FIXTURES = Path(__file__).resolve().parent
LINT = FIXTURES.parent / "lint.py"
SCHEMA_FIXTURES = ROOT / "80-agents/skills/_shared/fixtures/schema"


def run(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(LINT), *args], cwd=ROOT, text=True, capture_output=True, check=False)


def require(result: subprocess.CompletedProcess[str], code: int, *needles: str) -> None:
    output = result.stdout + result.stderr
    if result.returncode != code:
        raise AssertionError(f"expected exit {code}, got {result.returncode}:\n{output}")
    for needle in needles:
        if needle not in output:
            raise AssertionError(f"missing {needle!r}:\n{output}")


def digest_tree(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        digest.update(str(path.relative_to(root)).encode("utf-8"))
        digest.update(path.read_bytes())
    return digest.hexdigest()


def valid_project() -> str:
    return """---
type: project
schema_version: 1
owner: me
root: true
status: active
area: \"[[Personal]]\"
priority: P2
progress: 0
tags:
  - kind/project
created: 2026-08-10
updated: 2026-08-10
---

# Baseline Fixture

## 🎯 Objetivo

## 📊 Estado actual

## ✅ Tareas

## 📆 Bitácora
"""


def main() -> int:
    before = digest_tree(FIXTURES)
    require(run("--check", str(FIXTURES / "valid")), 0, "ERROR=0 WARN=0")
    require(run("--check", str(FIXTURES / "invalid")), 1, "[field-type]", "[forbidden-tag]", "[missing-section]", "[source-location]", "[unknown-type]")
    require(run("--strict", str(SCHEMA_FIXTURES / "valid/project-v1.md")), 0, "ERROR=0 WARN=0")
    require(run("--strict", str(SCHEMA_FIXTURES / "legacy/project-unversioned.md")), 1, "[legacy-modified]")
    require(run("--strict", str(SCHEMA_FIXTURES / "invalid/project-v2.md")), 1, "[schema-version]")
    after = digest_tree(FIXTURES)
    if before != after:
        raise AssertionError("lint modified its fixture corpus")
    with tempfile.TemporaryDirectory(prefix="agents-os-lint-gate-") as raw:
        corpus = Path(raw)
        (corpus / "valid.md").write_text(valid_project(), encoding="utf-8")
        inherited = corpus / "inherited-debt.md"
        inherited.write_text("# Missing frontmatter\n", encoding="utf-8")
        emitted = run("--emit-baseline", str(corpus))
        require(emitted, 0, '"ERROR": 0', '"WARN": 1')
        baseline = corpus / "baseline.json"
        baseline.write_text(emitted.stdout, encoding="utf-8")
        require(run("--gate", "--baseline", str(baseline), str(corpus)), 0, "new=0", "GO: no-new-debt")
        inherited.unlink()
        require(run("--gate", "--baseline", str(baseline), str(corpus)), 0, "new=0", "resolved=1")
        (corpus / "new-debt.md").write_text("# Missing frontmatter\n", encoding="utf-8")
        require(run("--gate", "--baseline", str(baseline), str(corpus)), 1, "new=1", "NO-GO")
    with tempfile.TemporaryDirectory(prefix="agents-os-lint-strict-gate-") as raw:
        corpus = Path(raw)
        (corpus / "valid.md").write_text(valid_project(), encoding="utf-8")
        emitted = run("--emit-baseline", str(corpus))
        require(emitted, 0, '"ERROR": 0', '"WARN": 0', '"fingerprints": []')
        baseline = corpus / "baseline.json"
        baseline.write_text(emitted.stdout, encoding="utf-8")
        require(run("--gate", "--baseline", str(baseline), str(corpus)), 0, "new=0", "GO: no-new-debt")
        (corpus / "invalid.md").write_text("# Missing frontmatter\n", encoding="utf-8")
        require(run("--gate", "--baseline", str(baseline), str(corpus)), 1, "new=1", "NO-GO")
    print("lint contract tests: fixtures=green strict=green read_only=green no_new_debt=green strict_gate=green")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
