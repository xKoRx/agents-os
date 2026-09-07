#!/usr/bin/env python3
"""Validate the AGENTS OS executable schema contract and template coverage."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CONTRACT_PATH = ROOT / "80-agents/skills/_shared/schema-contract.md"
START = "<!-- AGENTS_OS_SCHEMA_START -->"
END = "<!-- AGENTS_OS_SCHEMA_END -->"


def load_contract() -> dict:
    text = CONTRACT_PATH.read_text(encoding="utf-8")
    try:
        payload = text.split(START, 1)[1].split(END, 1)[0]
    except IndexError as exc:
        raise ValueError("schema markers are missing or duplicated") from exc
    match = re.search(r"```json\s*(\{.*\})\s*```", payload, re.DOTALL)
    if not match:
        raise ValueError("strict JSON block not found between schema markers")
    return json.loads(match.group(1))


def parse_note(path: Path) -> tuple[dict[str, str], str, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return {}, text, ""
    try:
        block, body = text[4:].split("\n---", 1)
    except ValueError:
        return {}, text, ""
    fields: dict[str, str] = {}
    for match in re.finditer(
        r"(?m)^([A-Za-z_][A-Za-z0-9_-]*):[ \t]*(.*?)[ \t]*$", block
    ):
        fields[match.group(1)] = match.group(2).strip().strip("\"'")
    return fields, body, block


def expected_fields(contract: dict, system: str, spec: dict) -> set[str]:
    envelope = contract["envelope"]
    return (
        set(envelope["common"]["required"])
        | set(envelope[system]["required"])
        | set(spec["required"])
    )


def validate_template(
    contract: dict,
    system: str,
    note_type: str,
    spec: dict,
    errors: list[str],
) -> str | None:
    template = spec.get("template")
    exemption = spec.get("exemption")
    if bool(template) == bool(exemption):
        errors.append(
            f"{system}.{note_type}: define exactly one of template or exemption"
        )
        return None
    for key in ("required", "optional", "forbidden", "sections"):
        if key not in spec or not isinstance(spec[key], list):
            errors.append(f"{system}.{note_type}: '{key}' must be a list")
    if exemption:
        if not exemption.get("kind") or not exemption.get("reason"):
            errors.append(f"{system}.{note_type}: incomplete exemption")
        return None

    path = ROOT / template
    if not path.is_file():
        errors.append(f"{system}.{note_type}: missing template {template}")
        return template
    root = contract["systems"][system]["template_root"].rstrip("/") + "/"
    if not template.startswith(root):
        errors.append(f"{system}.{note_type}: template crosses boundary: {template}")

    fields, body, block = parse_note(path)
    if fields.get("type") != note_type:
        errors.append(
            f"{template}: type={fields.get('type')!r}, expected {note_type!r}"
        )
    current = str(contract["schema_versions"]["current"])
    if fields.get("schema_version") != current:
        errors.append(
            f"{template}: schema_version={fields.get('schema_version')!r}, "
            f"expected {current}"
        )
    missing = sorted(expected_fields(contract, system, spec) - set(fields))
    if missing:
        errors.append(f"{template}: missing required declarations {missing}")
    forbidden = (
        set(contract["envelope"]["common"]["forbidden"])
        | set(contract["envelope"][system]["forbidden"])
        | set(spec["forbidden"])
    ) & set(fields)
    if forbidden:
        errors.append(f"{template}: forbidden declarations {sorted(forbidden)}")
    kind_tag = "kind/" + note_type.replace("_", "-")
    if kind_tag not in block:
        errors.append(f"{template}: missing canonical tag {kind_tag}")
    if system == "s1" and "scope/" not in block:
        errors.append(f"{template}: missing scope/<scope> tag placeholder")
    for heading in spec["sections"]:
        if heading not in body:
            errors.append(f"{template}: missing required section {heading!r}")
    status = fields.get("status")
    statuses = spec.get("statuses", [])
    if status and statuses and status not in statuses:
        errors.append(f"{template}: status {status!r} not in {statuses}")
    return template


def validate_fixture(contract: dict, item: dict, errors: list[str]) -> None:
    rel = item["path"]
    expect = item["expect"]
    path = ROOT / rel
    if not path.is_file():
        errors.append(f"fixture missing: {rel}")
        return
    fields, _, block = parse_note(path)
    version = fields.get("schema_version")
    if version is None:
        actual = "legacy"
    else:
        supported = {str(v) for v in contract["schema_versions"]["supported"]}
        note_type = fields.get("type")
        system = next(
            (s for s, cfg in contract["systems"].items()
             if note_type in cfg["types"]),
            None,
        )
        if not system or version not in supported:
            actual = "invalid"
        else:
            spec = contract["systems"][system]["types"][note_type]
            missing = expected_fields(contract, system, spec) - set(fields)
            forbidden = (
                set(contract["envelope"]["common"]["forbidden"])
                | set(contract["envelope"][system]["forbidden"])
                | set(spec["forbidden"])
            ) & set(fields)
            statuses = spec.get("statuses", [])
            bad_status = bool(
                fields.get("status") and statuses
                and fields["status"] not in statuses
            )
            kind_tag = "kind/" + note_type.replace("_", "-")
            actual = (
                "valid"
                if not missing and not forbidden and not bad_status
                and kind_tag in block
                else "invalid"
            )
    if actual != expect:
        errors.append(f"{rel}: expected {expect}, got {actual}")


def validate_type(
    contract: dict,
    requested_type: str,
    errors: list[str],
) -> tuple[str | None, str | None]:
    """Validate only the contract slice required to create one note type."""
    matches = [
        (system, spec)
        for system, config in contract["systems"].items()
        for note_type, spec in config["types"].items()
        if note_type == requested_type
    ]
    if len(matches) != 1:
        errors.append(f"unknown or ambiguous schema type: {requested_type}")
        return None, None
    system, spec = matches[0]
    template = validate_template(
        contract, system, requested_type, spec, errors
    )
    return system, template


def validate_lint_config(contract: dict, errors: list[str]) -> None:
    config = contract.get("lint")
    if not isinstance(config, dict):
        errors.append("lint: configuration is missing")
        return
    required = {
        "baseline", "fingerprint_algorithm", "strict_policy", "gate_policy",
        "legacy_policy", "legacy_required", "semantic_rules",
    }
    missing = sorted(required - set(config))
    if missing:
        errors.append(f"lint: missing configuration keys {missing}")
    if config.get("fingerprint_algorithm") != "sha256":
        errors.append("lint: fingerprint_algorithm must be sha256")
    supported_rules = set(config.get("semantic_rules", []))
    used_rules = {
        rule
        for system in contract.get("systems", {}).values()
        for spec in system.get("types", {}).values()
        for rule in spec.get("rules", [])
    }
    unknown_rules = sorted(used_rules - supported_rules)
    if unknown_rules:
        errors.append(f"lint: unsupported semantic rules {unknown_rules}")
    legacy = config.get("legacy_required", {})
    if not isinstance(legacy, dict) or not all(key in legacy for key in ("s1", "s2", "types")):
        errors.append("lint: legacy_required must define s1, s2, and types")
    baseline_rel = config.get("baseline")
    if not isinstance(baseline_rel, str) or Path(baseline_rel).is_absolute():
        errors.append("lint: baseline must be a vault-relative path")
        return
    baseline_path = ROOT / baseline_rel
    if not baseline_path.is_file():
        errors.append(f"lint: baseline missing: {baseline_rel}")
        return
    try:
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        errors.append(f"lint: invalid baseline JSON: {exc}")
        return
    expected = {
        "format_version": 1,
        "contract_version": contract.get("contract_version"),
        "schema_version": contract.get("schema_versions", {}).get("current"),
        "fingerprint_algorithm": "sha256",
        "scope_paths": [],
    }
    mismatches = sorted(key for key, value in expected.items() if baseline.get(key) != value)
    if mismatches:
        errors.append(f"lint: baseline metadata mismatch {mismatches}")
    fingerprints = baseline.get("fingerprints")
    if not isinstance(fingerprints, list) or fingerprints != sorted(set(fingerprints)):
        errors.append("lint: baseline fingerprints must be a sorted unique list")
    counts = baseline.get("counts", {})
    if isinstance(fingerprints, list) and counts.get("ERROR", 0) + counts.get("WARN", 0) != len(fingerprints):
        errors.append("lint: baseline counts do not match fingerprints")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate the AGENTS OS executable schema contract"
    )
    parser.add_argument(
        "--type",
        dest="requested_type",
        help="validate only the contract slice needed to create this note type",
    )
    args = parser.parse_args()

    errors: list[str] = []
    try:
        contract = load_contract()
    except (ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR contract parse: {exc}")
        return 1

    current = contract["schema_versions"]["current"]
    supported = contract["schema_versions"]["supported"]
    if current not in supported:
        errors.append("current schema version must be supported")

    if args.requested_type:
        system, template = validate_type(
            contract, args.requested_type, errors
        )
        print(
            "AGENTS OS schema contract: "
            f"scope=type:{args.requested_type} version={current} "
            f"system={system or 'unresolved'} "
            f"template={template or 'none'} errors={len(errors)}"
        )
        for error in errors:
            print(f"ERROR {error}")
        return 1 if errors else 0

    canonical_templates: dict[str, str] = {}
    type_count = 0
    for system, config in contract["systems"].items():
        for note_type, spec in config["types"].items():
            type_count += 1
            template = validate_template(
                contract, system, note_type, spec, errors
            )
            if template:
                previous = canonical_templates.get(template)
                if previous:
                    errors.append(
                        f"canonical template reused by {previous} and {system}.{note_type}: "
                        f"{template}"
                    )
                canonical_templates[template] = f"{system}.{note_type}"

    accounted = set(canonical_templates)
    for item in contract.get("derived_templates", []):
        rel = item["path"]
        accounted.add(rel)
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"derived template missing: {rel}")
            continue
        fields, _, _ = parse_note(path)
        if fields.get("type") != item["type"]:
            errors.append(f"{rel}: derived template type mismatch")
        if fields.get("schema_version") != str(current):
            errors.append(f"{rel}: derived template version mismatch")
        if not item.get("reason"):
            errors.append(f"{rel}: derived template needs a reason")
    for item in contract.get("fragments", []):
        accounted.add(item["path"])
        if not (ROOT / item["path"]).is_file():
            errors.append(f"fragment missing: {item['path']}")
        if not item.get("reason"):
            errors.append(f"{item['path']}: fragment needs a reason")

    discovered = {
        str(path.relative_to(ROOT))
        for root in ("70-templates", "80-agents/templates")
        for path in (ROOT / root).glob("*.md")
    }
    for rel in sorted(discovered - accounted):
        errors.append(f"unmapped template or fragment: {rel}")
    for rel in sorted(accounted - discovered):
        errors.append(f"contract maps absent template or fragment: {rel}")

    for fixture in contract.get("fixtures", []):
        validate_fixture(contract, fixture, errors)

    validate_lint_config(contract, errors)

    creation = contract.get("creation", {})
    materializer = creation.get("materializer")
    if not materializer or not (ROOT / materializer).is_file():
        errors.append("canonical creation materializer is missing")
    for rel in creation.get("entrypoints", []):
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"creation entrypoint missing: {rel}")
        elif "materialize_schema_note.py" not in path.read_text(encoding="utf-8"):
            errors.append(f"creation entrypoint bypasses materializer: {rel}")

    print(
        "AGENTS OS schema contract: "
        f"version={current} types={type_count} "
        f"canonical_templates={len(canonical_templates)} "
        f"derived={len(contract.get('derived_templates', []))} "
        f"fragments={len(contract.get('fragments', []))} "
        f"fixtures={len(contract.get('fixtures', []))} "
        f"creation_entrypoints={len(creation.get('entrypoints', []))} "
        f"errors={len(errors)}"
    )
    for error in errors:
        print(f"ERROR {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
