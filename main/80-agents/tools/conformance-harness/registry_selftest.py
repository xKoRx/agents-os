#!/usr/bin/env python3
"""Selftest for the optional, fail-closed domain router registry."""
from __future__ import annotations

import rules


HEADER = """| Domain | Areas | Router | Evidence markers |
|---|---|---|---|
"""


def route(domain: str, area: str, marker: str) -> str:
    return "| `%s` | `[[%s]]` | `30-resources/agents/skills/%s-agent-dev/SKILL.md` | `%s` |\n" % (
        domain, area, domain, marker)


def main() -> int:
    original = rules.DOMAIN_ROUTES
    try:
        rules.DOMAIN_ROUTES = rules.parse_domain_registry(HEADER)
        selected, _ = rules.domain_gate(None)
        assert selected is None, "empty registry must resolve DEFAULT"

        rules.DOMAIN_ROUTES = rules.parse_domain_registry(HEADER + route("alpha", "Area A", "tool-alpha"))
        selected, _ = rules.domain_gate({"title": "A", "area": "[[Area A]]"})
        assert selected == "alpha", "one exact area match must select one router"
        selected, _ = rules.domain_gate(None, task_evidence="run tool-alpha")
        assert selected == "alpha", "one task marker must select one router"

        rules.DOMAIN_ROUTES = rules.parse_domain_registry(
            HEADER + route("alpha", "Area A", "shared") + route("beta", "Area A", "shared"))
        selected, note = rules.domain_gate({"title": "A", "area": "[[Area A]]"})
        assert selected is None and "multiple" in note, "multiple area matches must fail closed"
        selected, note = rules.domain_gate(None, task_evidence="shared")
        assert selected is None and "multiple" in note, "multiple evidence matches must fail closed"
    finally:
        rules.DOMAIN_ROUTES = original
    print("registry selftest: PASS (0/1/>1)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
