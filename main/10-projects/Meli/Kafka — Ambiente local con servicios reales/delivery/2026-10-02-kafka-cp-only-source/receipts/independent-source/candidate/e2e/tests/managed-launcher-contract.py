#!/usr/bin/env python3
"""Exercises real managed-launcher boundaries/teardown; L0 only, never provider evidence."""
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / 'e2e/managed.sh'
RUN = '1234567890abcdef1234567890abcdef'

class ManagedLauncherContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='rio-managed-launcher-contract-')
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)
        self.managed = self.directory / 'managed.env'
        self.sandbox = self.directory / 'sandbox.env'
        self.write(self.managed, f'E2E_MANAGED_SCOPE=test-e2e\nE2E_MANAGED_RUN_ID={RUN}\n')
        self.write(self.sandbox, f'E2E_RUN_ID={RUN}\nE2E_KVS_EXCLUSIVE_RUN_ID={RUN}\n'
                   f'E2E_KVS_SANDBOX_PROVENANCE={self.directory}/state.json\n')

    def write(self, path, content):
        path.write_text(content)
        path.chmod(0o600)

    def invoke(self, component='journey', extra=None):
        env = {'PATH': os.environ['PATH'], 'HOME': os.environ['HOME'],
               'E2E_MANAGED_ENV_FILE': str(self.managed), 'E2E_KVS_ENV_FILE': str(self.sandbox)}
        env.update(extra or {})
        return subprocess.run(['bash', str(SCRIPT), component], env=env, capture_output=True,
                              text=True, timeout=15)

    def rejected(self, code, **kwargs):
        result = self.invoke(**kwargs)
        self.assertNotEqual(0, result.returncode)
        self.assertIn(code, result.stderr)
        self.assertNotIn('TEST_EVIDENCE_PUBLISHED', result.stdout)

    def test_managed_file_requires_private_permissions(self):
        self.managed.chmod(0o644)
        self.rejected('MANAGED_FILE_MUST_BE_MODE_0600')

    def test_duplicate_managed_export_cannot_override_gate(self):
        with self.managed.open('a') as file: file.write('E2E_MANAGED_SCOPE=production\n')
        self.rejected('MANAGED_DUPLICATE_CONFIG_EXPORT')

    def test_production_scope_and_literal_shell_text_are_rejected_without_eval(self):
        marker = self.directory / 'must-not-exist'
        self.write(self.managed, f'E2E_MANAGED_SCOPE="$(touch {marker})"\nE2E_MANAGED_RUN_ID={RUN}\n')
        self.rejected('MANAGED_EXPLICIT_NONPROD_SCOPE_REQUIRED')
        self.assertFalse(marker.exists())
        self.write(self.managed, f'E2E_MANAGED_SCOPE=production-test\nE2E_MANAGED_RUN_ID={RUN}\n')
        self.rejected('MANAGED_EXPLICIT_NONPROD_SCOPE_REQUIRED')

    def test_journey_and_all_require_the_full_sandbox_exports(self):
        for component in ('journey', 'all'):
            self.rejected('MANAGED_OWNED_SANDBOX_CONFIG_REQUIRED', component=component,
                          extra={'E2E_KVS_ENV_FILE': ''})

    def test_duplicate_and_unapproved_sandbox_exports_are_rejected(self):
        original = self.sandbox.read_text()
        self.write(self.sandbox, original + f'E2E_RUN_ID={RUN}\n')
        self.rejected('MANAGED_DUPLICATE_SANDBOX_EXPORT')
        self.write(self.sandbox, original + 'JAVA_TOOL_OPTIONS=unapproved\n')
        self.rejected('MANAGED_INVALID_SANDBOX_EXPORT')

    def test_run_mismatch_and_inherited_run_override_are_rejected(self):
        self.write(self.sandbox, self.sandbox.read_text().replace(RUN, 'a' * 32))
        self.rejected('MANAGED_RUN_SANDBOX_OWNERSHIP_MISMATCH')
        self.rejected('MANAGED_SANDBOX_RUN_ID_MISMATCH', extra={'E2E_RUN_ID': RUN})

    def test_actual_verifier_receives_consumed_exports_and_its_failure_stops_before_gradle(self):
        # The executable is a gate-control fixture, explicitly not a Fury/KVS substitute.
        observed = self.directory / 'observed.json'
        spy = self.directory / 'verifier.py'
        spy.write_text('#!/usr/bin/env python3\nimport json,os,sys\nfrom pathlib import Path\n'
                       'Path(os.environ["L0_OBSERVED"]).write_text(json.dumps({"args":sys.argv[1:],'
                       '"run":os.environ.get("E2E_RUN_ID"),"kv":os.environ.get("KEY_VALUE_STORE_OWN_1_END_POINT_READ")}))\n'
                       'raise SystemExit(43)\n')
        spy.chmod(0o700)
        with self.managed.open('a') as file: file.write(f'E2E_FURY_PYTHON={spy}\n')
        with self.sandbox.open('a') as file: file.write('KEY_VALUE_STORE_OWN_1_END_POINT_READ=literal-gate-fixture\n')
        result = self.invoke(extra={'L0_OBSERVED': str(observed)})
        self.assertEqual(43, result.returncode)
        data = json.loads(observed.read_text())
        self.assertEqual([str(ROOT/'e2e/sandbox.py'), 'verify', '--directory', str(self.directory), '--scope', 'ecosystem'], data['args'])
        self.assertEqual(RUN, data['run'])
        self.assertEqual('literal-gate-fixture', data['kv'])
        self.assertNotIn('TEST_EVIDENCE_PUBLISHED', result.stdout)

    def test_exit_trap_preserves_failure_and_fails_on_each_cleanup_error(self):
        source = SCRIPT.read_text()
        start = source.index('publish_and_cleanup() {')
        end = source.index('\non_managed_exit() {', start)
        actual_function = source[start:end]
        for original, sanitize, remove, receipt in [(0,0,0,0),(7,0,0,0),(0,5,0,0),(0,0,9,0),(0,0,0,1)]:
            evidence = self.directory / f'evidence-{original}-{sanitize}-{remove}-{receipt}'
            evidence.mkdir()
            if receipt: (evidence/'mutation-status.txt').mkdir()
            private = self.directory / f'private-{original}-{sanitize}-{remove}-{receipt}'
            private.mkdir()
            reconciliation = evidence / "reconciliation"
            reconciliation.mkdir(mode=0o700)
            script = f'''set +e
SCRIPT_DIR={json.dumps(str(ROOT/'e2e'))}
ROOT={json.dumps(str(ROOT))}
EVIDENCE_DIR={json.dumps(str(evidence))}
PRIVATE_DIR={json.dumps(str(private))}
E2E_RECONCILIATION_DIR={json.dumps(str(reconciliation))}
test_task=managedControlplaneJourneyTest
python3() {{ if [[ "$1" == */sanitize-evidence.py ]]; then return {sanitize}; else command python3 "$@"; fi; }}
rm() {{ if [[ {remove} != 0 ]]; then return {remove}; fi; command rm "$@"; }}
{actual_function}
(exit {original})
publish_and_cleanup
exit $?
'''
            result = subprocess.run(['bash','-c',script],capture_output=True,text=True,timeout=10)
            expected = original if not(sanitize or remove or receipt) else 1
            self.assertEqual(expected,result.returncode,(original,sanitize,remove,receipt,result.stderr))
            self.assertEqual(bool(remove),private.exists())

if __name__ == '__main__':
    unittest.main()
