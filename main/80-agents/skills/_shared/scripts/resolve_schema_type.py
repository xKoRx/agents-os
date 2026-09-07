#!/usr/bin/env python3
"""Resolve an AGENTS OS note type to its canonical template and version."""

from __future__ import annotations

import json
import sys

sys.dont_write_bytecode = True

from validate_schema_contract import load_contract


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: resolve_schema_type.py <type>", file=sys.stderr)
        return 2
    requested = sys.argv[1]
    contract = load_contract()
    matches = [
        (system, spec)
        for system, config in contract["systems"].items()
        for note_type, spec in config["types"].items()
        if note_type == requested
    ]
    if not matches:
        print(f"ERROR unknown schema type: {requested}", file=sys.stderr)
        return 1
    if len(matches) != 1:
        print(f"ERROR ambiguous schema type: {requested}", file=sys.stderr)
        return 1
    system, spec = matches[0]
    if not spec.get("template"):
        reason = spec.get("exemption", {}).get("reason", "non-creatable")
        print(f"ERROR type {requested} has no canonical template: {reason}", file=sys.stderr)
        return 1
    print(json.dumps({
        "type": requested,
        "system": system,
        "schema_version": contract["schema_versions"]["current"],
        "template": spec["template"],
    }, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
