#!/usr/bin/env python3
"""Execute real CI family functions in native Bash, with metadata-only API shapes.

The private API executable always fails before SDK/client/service execution.
These controls prove shell scope, gate and retention behavior, never business,
provider ownership, KVS absence, or successful CI/backend execution.
"""
from pathlib import Path
import json
import os
import shlex
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(os.environ.get('CI_FAMILY_CONTRACT_ROOT', Path(__file__).resolve().parents[2]))
CI_SOURCE = Path(os.environ.get('CI_FAMILY_CONTRACT_SOURCE', ROOT / 'e2e/ci.sh')).resolve(strict=True)
BASH = '/bin/bash'


def family_functions():
    source = CI_SOURCE.read_text()
    first = source.index('clear_family_runtime() {\n')
    return source[first:source.index('\nrecord_sources() {', first)]


API_SHAPE = r'''from pathlib import Path
import json,os,sys
arguments=sys.argv[1:]
if len(arguments)<2 or Path(arguments[0]).name!='sandbox.py':
    raise SystemExit(91)
operation=arguments[1]
if operation not in ('up','down'):
    raise SystemExit(92)
directory=Path(arguments[arguments.index('--directory')+1]).resolve(strict=True)
if directory.parent.parent!=Path(os.environ['CONTROL_JOB_DIR']).resolve(strict=True):
    raise SystemExit(93)
trace=Path(os.environ['CONTROL_TRACE'])
with trace.open('a') as output:
    json.dump({'kind':'CONTROL_API_SHAPE_ONLY','arguments':arguments},output)
    output.write('\n')
os.chmod(trace,0o600)
mode=os.environ['CONTROL_API_MODE']
if operation=='up':
    if mode in ('state-down-fail','state-marker'):
        (directory/'state.json').write_text('{"kind":"CONTROL_METADATA_ONLY"}\n')
    if mode=='state-marker':
        marker=Path(os.environ['E2E_RECONCILIATION_DIR'])/'control-unknown.json'
        marker.write_text('{"kind":"CONTROL_RETAINED_MARKER_ONLY"}\n')
    raise SystemExit(13) # No SDK, live API or launcher can be reached.
if mode!='state-down-fail':
    raise SystemExit(94)
raise SystemExit(17) # Deliberately no cleanup/absence certificate.
'''


class CiFamilyScopeContract(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='rio-ci-family-control-')
        self.addCleanup(self.temporary.cleanup)
        self.directory = Path(self.temporary.name).resolve(strict=True)
        self.job = self.directory / 'job'
        self.job.mkdir(mode=0o700)
        self.trace = self.directory / 'api-shape.jsonl'
        self.api_shape = self.directory / 'private-api-shape'
        self.api_shape.write_text('#!' + sys.executable + '\n' + API_SHAPE)
        self.api_shape.chmod(0o700)
        self.script_dir = self.directory / 'scripts'
        self.script_dir.mkdir(mode=0o700)
        for name in ['reconciliation-status.py', 'bind-ci-family-inputs.py']:
            (self.script_dir / name).write_bytes((ROOT / 'e2e' / name).read_bytes())
        # Only the executable transport boundary is replaced in this private tree.
        # The family, read-run parser, distinct-run guard and EXIT code remain real.
        self.managed_trace = self.directory / 'managed-control.json'
        managed_shape = self.script_dir / 'managed.sh'
        managed_shape.write_text('#!' + sys.executable + '\n' + r'''from pathlib import Path
import json,os,sys
if sys.argv[1:]!=['all']:
    raise SystemExit(95)
Path(os.environ['CONTROL_MANAGED_TRACE']).write_text(json.dumps({
    'kind':'CONTROL_TRANSPORT_ONLY', 'arguments':sys.argv[1:],
    'kvs_environment_file':os.environ.get('E2E_KVS_ENV_FILE')})+'\n')
raise SystemExit(29) # Never start SDK/services or produce business output.
''')
        managed_shape.chmod(0o700)
        self.environment = {
            'PATH': os.pathsep.join([str(Path(sys.executable).parent), '/usr/bin', '/bin']),
            'CONTROL_JOB_DIR': str(self.job), 'CONTROL_TRACE': str(self.trace),
            'CONTROL_API_MODE': 'no-state', 'JAVA_HOME': str(self.directory / 'unconsumed-jdk-shape'),
            'DOCKER_CONTEXT': 'unconsumed-control-only', 'E2E_FURY_PYTHON': str(self.api_shape),
            'E2E_CP_KVS_SERVICE': 'own-cp-control-alias',
            'CONTROL_MANAGED_TRACE': str(self.managed_trace),
        }

    def run_family(self, family='cp-functional', task='realIntegrationTest', managed=False):
        # Extraction is byte-exact. No CI guard or EXIT body is replaced by a fake.
        prelude = 'set -euo pipefail\numask 077\n'
        prelude += 'readonly SCRIPT_DIR=' + shlex.quote(str(self.script_dir)) + '\n'
        prelude += 'readonly CI_PRIVATE_DIR=' + shlex.quote(str(self.job)) + '\n'
        sentinels = ['family_name', 'task', 'family_dir', 'family_run', 'sandbox_dir',
                     'sandbox_attempted', 'launcher_attempted', 'launcher_status',
                     'family_cleanup_status', 'status', 'checkout_variable', 'kvs_run',
                     'EVIDENCE_DIR', 'E2E_RUN_ID', 'KEY_VALUE_STORE_CONTROL_CONTAINER_NAME']
        for variable in sentinels:
            prelude += variable + '=parent_sentinel\n'
        prelude += 'sandbox_args=(parent_sentinel)\n'
        prelude += 'export E2E_RUN_ID KEY_VALUE_STORE_CONTROL_CONTAINER_NAME\n'
        call = 'run_managed_family' if managed else ('run_local_family ' + shlex.quote(family) + ' ' + shlex.quote(task))
        script = prelude + family_functions() + '\ncontrol_result=0\n'
        script += call + ' || control_result=$?\n'
        for variable in sentinels:
            script += '[[ "${' + variable + '}" == parent_sentinel ]] || exit 85\n'
        script += '[[ "${sandbox_args[*]}" == parent_sentinel ]] || exit 86\n'
        script += 'printf "PARENT_SENTINELS_INTACT\\n"\nexit "${control_result}"\n'
        self.result = subprocess.run([BASH, '-c', script], env=self.environment,
                                     capture_output=True, text=True, timeout=10)
        self.family_dir = self.job / ('managed-oauth-bigqueue' if managed else family)
        self.assertIn('PARENT_SENTINELS_INTACT', self.result.stdout)
        gate_path = self.family_dir / 'gate.json'
        self.assertTrue(gate_path.is_file(), 'real EXIT function failed to write gate.json: ' + self.result.stderr)
        self.gate = json.loads(gate_path.read_text())
        self.calls = [json.loads(line)['arguments'] for line in self.trace.read_text().splitlines()] if self.trace.exists() else []
        self.assertEqual(self.gate['family'], self.family_dir.name)
        self.assertEqual(self.gate['exit_status'], self.result.returncode)
        self.assertNotIn('unbound variable', self.result.stderr)

    def assert_retained(self, state=False):
        self.assertEqual(self.result.returncode, 1)
        self.assertEqual(self.gate['sandbox_cleanup_status'], 1)
        self.assertEqual((self.family_dir / 'sandbox-cleanup.status').read_text(), '1\n')
        self.assertTrue((self.family_dir / 'sandbox').is_dir())
        self.assertEqual((self.family_dir / 'sandbox/state.json').exists(), state)
        self.assertIn('CI_SANDBOX_RETAINED:' + self.family_dir.name, self.result.stderr)
        self.assertEqual(self.gate['run_id'], None)

    def test_CP_without_PM_reaches_up_with_exact_cp_scope_and_writes_gate(self):
        self.run_family()
        self.assertEqual(len(self.calls), 1)
        arguments = self.calls[0]
        self.assertEqual(arguments[1:4], ['up', '--scope', 'cp'])
        self.assertEqual(arguments[arguments.index('--cp-service') + 1], 'own-cp-control-alias')
        self.assertFalse(any(argument.startswith('--pm-') for argument in arguments))
        self.assert_retained()

    def test_missing_CP_alias_has_no_API_and_gate_2(self):
        del self.environment['E2E_CP_KVS_SERVICE']
        self.run_family()
        self.assertEqual(self.result.returncode, 2)
        self.assertEqual(self.calls, [])
        self.assertEqual(self.gate['sandbox_cleanup_status'], None)
        self.assertEqual((self.family_dir / 'sandbox-cleanup.status').read_text(), 'NOT_ATTEMPTED\n')

    def test_attempt_without_state_retains_unknown_and_cannot_certify_absence(self):
        self.run_family()
        self.assert_retained()
        self.assertEqual([arguments[1] for arguments in self.calls], ['up'])
        self.assertTrue((self.family_dir / 'sandbox-up.log').is_file())
        self.assertFalse((self.family_dir / 'sandbox-down.log').exists())

    def test_own_metadata_state_down_failure_is_retained_with_gate_1(self):
        self.environment['CONTROL_API_MODE'] = 'state-down-fail'
        self.run_family()
        self.assert_retained(state=True)
        self.assertEqual([arguments[1] for arguments in self.calls], ['up', 'down'])
        self.assertEqual((self.family_dir / 'reconciliation-final.log').read_text(), 'RECONCILIATION_STATUS:CLEAN\n')

    def test_retained_marker_blocks_down_and_false_absence(self):
        self.environment['CONTROL_API_MODE'] = 'state-marker'
        self.run_family()
        self.assert_retained(state=True)
        self.assertEqual([arguments[1] for arguments in self.calls], ['up'])
        self.assertTrue((self.family_dir / 'reconciliation/control-unknown.json').is_file())
        self.assertEqual((self.family_dir / 'reconciliation-final.log').read_text(), 'RECONCILIATION_STATUS:RETAINED\n')
        self.assertFalse((self.family_dir / 'sandbox-down.log').exists())

    def test_missing_canonical_PM_inputs_has_no_API_and_gate_2(self):
        self.run_family('playmaker-canonical', 'e2eCanonicalPlaymakerTest')
        self.assertEqual(self.result.returncode, 2)
        self.assertEqual(self.calls, [])
        self.assertIn('E2E_PM_RESULTS_KVS_SERVICE', self.result.stderr)
        self.assertEqual((self.family_dir / 'sandbox-cleanup.status').read_text(), 'NOT_ATTEMPTED\n')

    def test_missing_candidate_PM_inputs_has_no_API_and_gate_2(self):
        self.run_family('playmaker-candidate', 'e2eCandidatePlaymakerTest')
        self.assertEqual(self.result.returncode, 2)
        self.assertEqual(self.calls, [])
        self.assertIn('E2E_PM_LOCKS_KVS_SERVICE', self.result.stderr)

    def test_missing_managed_inputs_has_no_API_and_gate_2(self):
        self.run_family(managed=True)
        self.assertEqual(self.result.returncode, 2)
        self.assertEqual(self.calls, [])
        self.assertIn('E2E_MANAGED_ENV_FILE', self.result.stderr)
        self.assertEqual(self.gate['run_id'], None)
        self.assertEqual(self.gate['sandbox_cleanup_status'], None)

    def test_configured_PM_keeps_ecosystem_scope_and_three_aliases(self):
        for name in ['caller-shape', 'entity-template-shape', 'denied-template-shape']:
            path = self.directory / name
            path.write_text('CONTROL_UNCONSUMED_INPUT_SHAPE_ONLY\n')
            path.chmod(0o600)
        self.environment.update({
            'E2E_PM_RESULTS_KVS_SERVICE': 'own-results-control-alias',
            'E2E_PM_LOCKS_KVS_SERVICE': 'own-locks-control-alias',
            'E2E_PLAYMAKER_ENV_FILE': str(self.directory / 'caller-shape'),
            'E2E_ENTITY_SERVICE_BASE_URL': 'https://unconsumed-control.invalid',
            'E2E_ENTITY_SERVICE_TEMPLATE_RECEIPT_FILE': str(self.directory / 'entity-template-shape'),
            'E2E_PLAYMAKER_DENIED_IDENTITY_TEMPLATE_FILE': str(self.directory / 'denied-template-shape'),
            'E2E_PLAYMAKER_CANDIDATE_REPO': str(self.directory / 'unconsumed-repo-shape'),
        })
        self.run_family('playmaker-candidate', 'e2eCandidatePlaymakerTest')
        self.assert_retained()
        self.assertEqual(len(self.calls), 1)
        arguments = self.calls[0]
        self.assertEqual(arguments[1:4], ['up', '--scope', 'ecosystem'])
        for flag, expected in [('--cp-service', 'own-cp-control-alias'),
                               ('--pm-results-service', 'own-results-control-alias'),
                               ('--pm-locks-service', 'own-locks-control-alias')]:
            self.assertEqual(arguments[arguments.index(flag) + 1], expected)

    def test_missing_runtime_interpreter_has_no_API_and_parent_sentinels_survive(self):
        del self.environment['E2E_FURY_PYTHON']
        self.run_family()
        self.assertEqual(self.result.returncode, 2)
        self.assertEqual(self.calls, [])
        self.assertIn('E2E_FURY_PYTHON', self.result.stderr)

    def test_managed_bound_private_runs_reach_neutral_transport_and_preserve_failure(self):
        run = 'c' * 32
        for name in ['cp-functional', 'playmaker-canonical', 'playmaker-candidate']:
            family = self.job / name
            family.mkdir(mode=0o700)
            (family / 'gate.json').write_text(json.dumps({'run_id': 'a' * 32}) + '\n')
        managed_env = self.directory / 'managed.env'
        managed_kvs = self.directory / 'managed-kvs.env'
        managed_env.write_text('E2E_MANAGED_RUN_ID=' + run + '\n')
        managed_kvs.write_text('E2E_RUN_ID=' + run + '\n')
        for path in [managed_env, managed_kvs]:
            path.chmod(0o600)
        self.environment.update({'E2E_MANAGED_ENV_FILE': str(managed_env),
                                 'E2E_MANAGED_KVS_ENV_FILE': str(managed_kvs)})
        self.run_family(managed=True)
        self.assertEqual(self.result.returncode, 29)
        self.assertEqual(self.gate['run_id'], run)
        self.assertEqual(self.gate['sandbox_cleanup_status'], None)
        self.assertEqual(self.calls, [])
        self.assertEqual(json.loads(self.managed_trace.read_text()), {
            'kind': 'CONTROL_TRANSPORT_ONLY', 'arguments': ['all'],
            'kvs_environment_file': str(managed_kvs)})
        self.assertNotIn('command not found', self.result.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=1)
