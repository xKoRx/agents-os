#!/usr/bin/env python3
"""Materialize a new canonical AGENTS OS note from its contracted template."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True

from validate_schema_contract import CONTRACT_PATH, ROOT, load_contract


VALIDATOR = ROOT / "80-agents/skills/_shared/scripts/validate_schema_contract.py"
FORBIDDEN_TARGET_ROOTS = {
    "40-archive",
    "70-templates",
    "80-agents/templates",
    "outputs",
}


def resolve_type(contract: dict, requested: str) -> tuple[str, dict]:
    matches = [
        (system, spec)
        for system, config in contract["systems"].items()
        for note_type, spec in config["types"].items()
        if note_type == requested
    ]
    if len(matches) != 1:
        raise ValueError(
            f"unknown or ambiguous schema type: {requested}"
        )
    system, spec = matches[0]
    if not spec.get("template"):
        reason = spec.get("exemption", {}).get("reason", "non-creatable")
        raise ValueError(f"type {requested} is not canonically creatable: {reason}")
    return system, spec


def validate_target(raw: str) -> tuple[Path, str]:
    candidate = Path(raw)
    if candidate.is_absolute() or candidate.suffix != ".md":
        raise ValueError("target must be a vault-relative .md path")
    target = (ROOT / candidate).resolve()
    try:
        rel = str(target.relative_to(ROOT))
    except ValueError as exc:
        raise ValueError("target escapes VAULT_ROOT") from exc
    parts = Path(rel).parts
    if not parts or parts[0] in FORBIDDEN_TARGET_ROOTS:
        raise ValueError(f"target root is not canonical-create eligible: {rel}")
    if any(part.startswith(".") for part in parts) or "fixtures" in parts:
        raise ValueError(f"target is excluded from canonical creation: {rel}")
    if target.exists():
        raise ValueError(f"refusing to overwrite existing note: {rel}")
    return target, rel


def render(template: str, title: str) -> str:
    today = dt.date.today().isoformat()
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    rendered = template.replace("{{date:YYYY-MM-DD}}", today)
    rendered = rendered.replace("{{title}}", title).replace("{{slug}}", slug)
    rendered = re.sub(
        r"(?m)^(created|updated): YYYY-MM-DD$",
        lambda match: f"{match.group(1)}: {today}",
        rendered,
    )
    rendered = rendered.replace("# Session Feedback - YYYY-MM-DD", f"# Session Feedback - {today}")
    return rendered


def validate_contract(note_type: str) -> None:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, str(VALIDATOR), "--type", note_type],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        raise ValueError(
            "schema contract gate is red: " + result.stdout.strip()
        )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create a canonical note from the executable schema contract"
    )
    parser.add_argument("type", help="contracted note type")
    parser.add_argument("target", help="vault-relative target .md path")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--dry-run", action="store_true", help="validate and resolve only")
    mode.add_argument("--stdout", action="store_true", help="render without writing")
    args = parser.parse_args()

    try:
        validate_contract(args.type)
        contract = load_contract()
        system, spec = resolve_type(contract, args.type)
        target, rel = validate_target(args.target)
        template_rel = spec["template"]
        template_text = (ROOT / template_rel).read_text(encoding="utf-8")
        rendered = render(template_text, target.stem)
    except ValueError as exc:
        print(f"ERROR {exc}", file=sys.stderr)
        return 1

    result = {
        "contract": str(CONTRACT_PATH.relative_to(ROOT)),
        "schema_version": contract["schema_versions"]["current"],
        "system": system,
        "target": rel,
        "template": template_rel,
        "type": args.type,
    }
    if args.dry_run:
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0
    if args.stdout:
        sys.stdout.write(rendered)
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        with target.open("x", encoding="utf-8") as handle:
            handle.write(rendered)
    except FileExistsError:
        print(f"ERROR refusing to overwrite existing note: {rel}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
