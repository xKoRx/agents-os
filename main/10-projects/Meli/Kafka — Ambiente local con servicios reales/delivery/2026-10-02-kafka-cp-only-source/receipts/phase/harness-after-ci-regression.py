#!/usr/bin/env python3
"""Mandatory harness control-flow regressions; no business mocks or E2E certification."""
from pathlib import Path
import subprocess
import sys

for script in ('cleanup-contract.py', 'sandbox-contract.py', 'managed-launcher-contract.py', 'retention-contract.py', 'reconciliation-status-contract.py', 'ci-family-scope-contract.py'):
    result = subprocess.run([sys.executable, str(Path(__file__).with_name(script))], check=False)
    if result.returncode:
        raise SystemExit(result.returncode)
