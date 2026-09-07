#!/usr/bin/env python3
"""Validate an autonomous phased implementation plan without modifying it."""

from __future__ import annotations

import re
import sys
from pathlib import Path


REQUIRED_PROJECT_SECTIONS = (
    "## 📊 Estado actual",
    "## ✅ Tareas",
    "## 📆 Bitácora",
)

REQUIRED_PHASE_LABELS = (
    "Misión exacta",
    "Precondiciones verificables",
    "Lectura obligatoria",
    "Decisiones",
    "Implementación paso a paso",
    "Archivos esperados",
    "No tocar",
    "Spikes permitidos",
    "Tests y asserts",
    "Entregables/Gate",
    "Handoff",
)

PHASE_HEADING = re.compile(
    r"^#{3,5}\s+.*Paquete autónomo Fase\s+(\d+)\b.*$",
    re.MULTILINE | re.IGNORECASE,
)


def error(errors: list[str], message: str) -> None:
    errors.append(f"ERROR: {message}")


def warning(warnings: list[str], message: str) -> None:
    warnings.append(f"WARN: {message}")


def phase_sections(text: str) -> list[tuple[int, str]]:
    matches = list(PHASE_HEADING.finditer(text))
    result: list[tuple[int, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result.append((int(match.group(1)), text[match.start() : end]))
    return result


def resolve_vault_root(plan_path: Path, errors: list[str]) -> Path | None:
    for candidate in (plan_path.parent, *plan_path.parents):
        marker = candidate / "80-agents/agents-os/agents-os.md"
        if marker.is_file():
            return candidate
    error(errors, "cannot resolve VAULT_ROOT from plan location")
    return None


def validate_vault_links(
    text: str, plan_path: Path, errors: list[str]
) -> int:
    refs = set(re.findall(r"`VAULT_ROOT/([^`]+)`", text))
    vault_root = resolve_vault_root(plan_path, errors)
    if vault_root is None:
        return len(refs)

    for raw in sorted(refs):
        line_match = re.search(r":L(\d+)$", raw)
        path_text = raw[: line_match.start()] if line_match else raw
        path = vault_root / path_text
        if not path.exists():
            error(errors, f"missing VAULT_ROOT reference: {path_text}")
            continue
        if line_match and path.is_file():
            requested = int(line_match.group(1))
            line_count = sum(1 for _ in path.open("r", encoding="utf-8", errors="replace"))
            if requested > line_count:
                error(
                    errors,
                    f"line anchor out of range: {path_text}:L{requested} > {line_count}",
                )
    return len(refs)


def validate(plan_path: Path) -> int:
    text = plan_path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    for section in REQUIRED_PROJECT_SECTIONS:
        if section not in text:
            error(errors, f"missing project section: {section}")

    phases = phase_sections(text)
    if not phases:
        error(errors, "no autonomous phase packages found")

    phase_numbers = [number for number, _ in phases]
    if len(set(phase_numbers)) != len(phase_numbers):
        error(errors, f"duplicate phase packages: {phase_numbers}")

    for number, section in phases:
        for label in REQUIRED_PHASE_LABELS:
            if label not in section:
                error(errors, f"F{number} missing label: {label}")
        if "VAULT_ROOT/" not in section:
            error(errors, f"F{number} has no portable VAULT_ROOT source reference")
        if not re.search(rf"^.*T{number}\.\d+", text, re.MULTILINE):
            error(errors, f"F{number} has no atomic tasks")
        if not re.search(rf"^\*\*Despacho Fase {number}\*\*$", text, re.MULTILINE):
            error(errors, f"F{number} has no dispatch block")
        if not re.search(rf"^\|\s*G{number}\s*\|", text, re.MULTILINE):
            error(errors, f"F{number} has no gate-control row")

    open_rows = re.findall(
        r"^\|.*\|\s*`?(?:PROPOSED_FOR_APPROVAL|OPEN DECISION)`?\s*\|",
        text,
        re.MULTILINE,
    )
    if open_rows:
        error(errors, f"ready plan contains {len(open_rows)} open decision row(s)")

    fence_count = len(re.findall(r"^```", text, re.MULTILINE))
    if fence_count % 2:
        error(errors, f"unbalanced fenced code blocks: {fence_count}")

    if "file:///" in text or re.search(r"/(?:Users|home)/", text):
        error(errors, "plan persists a machine-specific vault path")

    link_count = validate_vault_links(text, plan_path, errors)
    if link_count == 0:
        warning(warnings, "plan contains no VAULT_ROOT references")

    for item in warnings + errors:
        print(item)

    print(
        "SUMMARY:"
        f" phases={len(phases)}"
        f" gates={sum(1 for n in phase_numbers if re.search(rf'^\|\s*G{n}\s*\|', text, re.MULTILINE))}"
        f" dispatches={sum(1 for n in phase_numbers if re.search(rf'^\*\*Despacho Fase {n}\*\*$', text, re.MULTILINE))}"
        f" local_refs={link_count}"
        f" errors={len(errors)}"
        f" warnings={len(warnings)}"
    )
    return 1 if errors else 0


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_plan.py <agent-project-note.md>", file=sys.stderr)
        return 2
    plan_path = Path(sys.argv[1]).expanduser().resolve()
    if not plan_path.is_file():
        print(f"ERROR: plan not found: {plan_path}", file=sys.stderr)
        return 2
    return validate(plan_path)


if __name__ == "__main__":
    raise SystemExit(main())
