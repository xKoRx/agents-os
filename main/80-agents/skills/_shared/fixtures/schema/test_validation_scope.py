#!/usr/bin/env python3
"""Regression test for type-scoped canonical materialization validation."""

from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path


SHARED = Path(__file__).resolve().parents[2]
VAULT_ROOT = SHARED.parents[2]
sys.path.insert(0, str(SHARED / "scripts"))

import validate_schema_contract as validator  # noqa: E402


def main() -> int:
    contract = validator.load_contract()
    original_root = validator.ROOT
    try:
        with tempfile.TemporaryDirectory(prefix="agents-os-schema-scope-") as raw:
            root = Path(raw)
            shutil.copytree(VAULT_ROOT / "70-templates", root / "70-templates")
            shutil.copytree(
                VAULT_ROOT / "80-agents/templates",
                root / "80-agents/templates",
            )
            validator.ROOT = root

            application = root / "70-templates/application.md"
            text = application.read_text(encoding="utf-8")
            application.write_text(
                text.replace(
                    "## 🎯 Responsabilidad (estable)",
                    "## BROKEN unrelated application heading",
                ),
                encoding="utf-8",
            )

            change_log_errors: list[str] = []
            validator.validate_type(
                contract, "change_log", change_log_errors
            )
            if change_log_errors:
                raise AssertionError(
                    "unrelated S2 drift blocked S1 change_log: "
                    + repr(change_log_errors)
                )

            application_errors: list[str] = []
            validator.validate_type(
                contract, "application", application_errors
            )
            if not any(
                "Responsabilidad (estable)" in error
                for error in application_errors
            ):
                raise AssertionError(
                    "requested broken type did not fail closed: "
                    + repr(application_errors)
                )
    finally:
        validator.ROOT = original_root

    print(
        "schema validation scope: unrelated_drift=isolated "
        "requested_type_drift=blocked"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
