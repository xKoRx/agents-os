#!/usr/bin/env python3
"""Permanent lifecycle control-flow regressions; no Sandbox/KVS/E2E certificate."""
import contextlib
import importlib.util
import io
import json
import os
import sys
from pathlib import Path
import tempfile
import types
import unittest
from unittest.mock import patch

MODULE_PATH = Path(__file__).resolve().parents[1] / 'sandbox.py'
spec = importlib.util.spec_from_file_location('owned_sandbox_contract', MODULE_PATH)
sandbox = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sandbox)


class ControlFixture:
    """Synthetic API shape only, for ownership and unknown-outcome regression."""
    def __init__(self, directory, scope=None):
        self.lifecycle = sandbox.Lifecycle.__new__(sandbox.Lifecycle)
        self.lifecycle.directory = Path(directory)
        run = 'a' * 32
        self.lifecycle.state = {'schema': 1, 'run_id': run, 'marker': 'Owned Kafka E2E ' + run,
            'status': 'OWNED_CONFIG_GENERATED_NOT_KVS_CERTIFIED', 'segments': {}, 'resources': []}
        if scope is not None:
            self.lifecycle.state['scope'] = scope
        self.configs = {}
        self.calls = []
        applications = sandbox.APPS[:1] if scope == 'cp' else sandbox.APPS
        for app, aliases, instance in zip(applications, [['cp'], ['results', 'locks']], ['1', '2']):
            resource = {'app': app, 'bc': 'e2e-' + run, 'instance': instance, 'create_intent': True,
                        'create_outcome': 'CONFIRMED', 'creation_observed': True,
                        'ownership_verified': True, 'logical_services': aliases,
                        'physical_containers': ['sbox_' + alias for alias in aliases]}
            self.lifecycle.state['resources'].append(resource)
            self.configs[app] = {'configurations': [{'original_service_name': alias, 'configuration': {
                'KEY_VALUE_STORE_' + alias.upper() + '_CONTAINER_NAME': 'sbox_' + alias,
                'KEY_VALUE_STORE_' + alias.upper() + '_END_POINT_READ': 'https://owned.invalid/read',
                'KEY_VALUE_STORE_' + alias.upper() + '_END_POINT_WRITE': 'https://owned.invalid/write'}} for alias in aliases]}
        self.lifecycle.call = self.call

    def call(self, app, suffix, method='GET', body=None, allowed=(200,)):
        self.calls.append((app, suffix, method))
        if suffix.endswith('/configurations'):
            return self.configs[app], 200
        return {'name': 'e2e-' + 'a' * 32, 'description': 'Owned Kafka E2E ' + 'a' * 32}, 200

    def exports(self):
        result = self.lifecycle.base_exports()
        for resource in self.lifecycle.state['resources']:
            self.lifecycle.add_configuration(result, resource, self.configs[resource['app']])
        return result


class ProvisioningControlFixture(ControlFixture):
    """API metadata simulator only: no provider, client storage or business result."""
    def __init__(self, directory, scope=None):
        super().__init__(directory, scope)
        self.lifecycle.state['resources'] = []
        self.lifecycle.state['status'] = 'PREPARING'
        self.existing = set()
        self.cloned = []
        self.lifecycle.api = types.SimpleNamespace(make_api_call=self.api_call)
        self.lifecycle.stored_auth_headers = lambda: {'X-Tiger-Token': 'Bearer synthetic-control-fixture'}
        self.lifecycle.call = types.MethodType(sandbox.Lifecycle.call, self.lifecycle)

    def api_call(self, route, method, **kwargs):
        _, app, suffix = route.split('/', 2)
        self.calls.append((app, suffix, method))
        if suffix == 'bc':
            if method == 'GET':
                return [], 200
            self.existing.add(app)
            return {}, 201
        if suffix == 'bc/e2e-' + self.lifecycle.state['run_id']:
            if method == 'DELETE':
                self.existing.discard(app)
                return {}, 200
            if app not in self.existing:
                return None, 404
            return {'name': 'e2e-' + self.lifecycle.state['run_id'],
                    'description': self.lifecycle.state['marker']}, 200
        if suffix.endswith('/services'):
            self.cloned.append((app, json.loads(kwargs['data'])['name']))
            return {}, 201
        if suffix.endswith('/start'):
            return {'response': '1' if app == sandbox.APPS[0] else '2'}, 200
        if suffix.endswith('/configurations'):
            return self.configs[app], 200
        if suffix.endswith('/instances'):
            return {'instances': [{'id': '1' if app == sandbox.APPS[0] else '2'}]}, 200
        if suffix.endswith('/stop'):
            return {}, 200
        raise AssertionError('unexpected simulator API route')


class LifecycleControlContract(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix='sandbox-control-regression-')
        self.addCleanup(self.directory.cleanup)
        self.fixture = ControlFixture(self.directory.name)

    def test_exact_consumed_exports_pass_only_with_both_fresh_application_configs(self):
        with patch.dict(os.environ, self.fixture.exports(), clear=True):
            self.fixture.lifecycle.verify()
        self.assertEqual(sum(suffix.endswith('/configurations') for _, suffix, _ in self.fixture.calls), 2)

    def test_owned_receipt_cannot_authorize_foreign_consumed_exports(self):
        for key, value in [('KEY_VALUE_STORE_CP_CONTAINER_NAME', 'sbox_foreign'),
                           ('KEY_VALUE_STORE_CP_END_POINT_WRITE', 'https://foreign.invalid'),
                           ('E2E_KVS_CONTAINER_NAME', 'foreign'), ('E2E_RUN_ID', 'b' * 32),
                           ('E2E_KVS_SEGMENT_ID', 'unexpected'), ('E2E_SANDBOX_INSTANCE', '999')]:
            with self.subTest(key=key):
                environment = self.fixture.exports()
                environment[key] = value
                with patch.dict(os.environ, environment, clear=True):
                    with self.assertRaisesRegex(RuntimeError, 'SANDBOX_CONSUMED_EXPORTS'):
                        self.fixture.lifecycle.verify()

    def test_inherited_additional_toolkit_mapping_is_rejected(self):
        environment = self.fixture.exports()
        environment['KEY_VALUE_STORE_OTHER_CONTAINER_NAME'] = 'sbox_other'
        with patch.dict(os.environ, environment, clear=True):
            with self.assertRaisesRegex(RuntimeError, 'SANDBOX_CONSUMED_EXPORTS'):
                self.fixture.lifecycle.verify()

    def test_fresh_logical_alias_change_is_rejected_even_if_physical_multiset_matches(self):
        environment = self.fixture.exports()
        self.fixture.configs[sandbox.APPS[0]]['configurations'][0]['original_service_name'] = 'foreign'
        with patch.dict(os.environ, environment, clear=True):
            with self.assertRaisesRegex(RuntimeError, 'SANDBOX_PROVENANCE_LOGICAL_MAPPING_CHANGED'):
                self.fixture.lifecycle.verify()

    def test_early404_cannot_certify_unresolved_creation(self):
        for outcome in ['UNKNOWN', 'CONFIRMED']:
            with self.subTest(outcome=outcome):
                resource = self.fixture.lifecycle.state['resources'][0]
                resource['create_outcome'], resource['creation_observed'] = outcome, False
                self.fixture.lifecycle.require_owned = lambda resource: None
                with self.assertRaisesRegex(RuntimeError, 'SANDBOX_CLEANUP_FAILED'):
                    self.fixture.lifecycle.down()
                self.assertEqual(self.fixture.lifecycle.state['cleanup'], 'FAILED')
                self.assertEqual(resource['cleanup_error'], 'SANDBOX_CREATION_OUTCOME_UNRESOLVED')

    def test_observed_creation_then_absence_can_certify_cleanup(self):
        self.fixture.lifecycle.require_owned = lambda resource: None
        self.fixture.lifecycle.down()
        self.assertEqual(self.fixture.lifecycle.state['cleanup'], 'CERTIFIED_API_ABSENCE')

    def test_bc_absence_cannot_resolve_unknown_non_create_mutations(self):
        for method, suffix in [('POST', 'bc/run/services'), ('PUT', 'bc/run/start'),
                               ('PUT', 'bc/run/instances/1/stop'), ('DELETE', 'bc/run')]:
            with self.subTest(method=method, suffix=suffix):
                self.fixture.lifecycle.state['mutations'] = [{'app': sandbox.APPS[0], 'suffix': suffix,
                                                             'method': method, 'outcome': 'UNKNOWN'}]
                self.fixture.lifecycle.require_owned = lambda resource: None
                with self.assertRaisesRegex(RuntimeError, 'SANDBOX_CLEANUP_FAILED'):
                    self.fixture.lifecycle.down()
                self.assertEqual(self.fixture.lifecycle.state['cleanup'], 'FAILED')

    def test_cleanup_continues_after_one_resource_ownership_fails(self):
        attempted = []
        def ownership(resource):
            attempted.append(resource['app'])
            if resource['app'] == sandbox.APPS[0]:
                raise RuntimeError('SANDBOX_OWNERSHIP_VERIFICATION_FAILED')
            return None
        self.fixture.lifecycle.require_owned = ownership
        with self.assertRaisesRegex(RuntimeError, 'SANDBOX_CLEANUP_FAILED'):
            self.fixture.lifecycle.down()
        self.assertEqual(attempted, list(sandbox.APPS))

    def test_missing_or_expired_stored_auth_fails_without_request_or_login(self):
        credentials = types.SimpleNamespace(TIGER_TOKEN_KEY='token', ZT_TOKEN_KEY='zt',
            get_credentials=lambda: {}, get=lambda key, snapshot: None, tiger_token_expired=lambda snapshot: True)
        with patch.dict('sys.modules', {'furycli.core.helpers': types.SimpleNamespace(credentials=credentials)}):
            with self.assertRaisesRegex(RuntimeError, 'SANDBOX_FURY_LOGIN_REQUIRED'):
                self.fixture.lifecycle.stored_auth_headers()
        self.assertEqual(self.fixture.calls, [])

    def test_actual_api_call_disables_implicit_authentication_and_retries(self):
        calls = []
        self.fixture.lifecycle.api = types.SimpleNamespace(make_api_call=lambda *args, **kwargs: (calls.append(kwargs) or {}, 200))
        self.fixture.lifecycle.stored_auth_headers = lambda: {'X-Tiger-Token': 'Bearer synthetic-control-fixture'}
        sandbox.Lifecycle.call(self.fixture.lifecycle, sandbox.APPS[0], 'bc')
        self.assertIs(calls[0]['authenticate'], False)
        self.assertIs(calls[0]['retry'], False)
        self.assertEqual(calls[0]['timeout'], 20)


class ScopeControlContract(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory(prefix='sandbox-scope-control-')
        self.addCleanup(self.directory.cleanup)
        self.fixture = ControlFixture(self.directory.name, 'cp')

    def verify(self, fixture=None, expected=None, extras=None):
        fixture = fixture or self.fixture
        environment = fixture.exports()
        environment.update(extras or {})
        with patch.dict(os.environ, environment, clear=True):
            if expected is None:
                fixture.lifecycle.verify()
            else:
                fixture.lifecycle.verify(expected)

    def test_cp_receipt_verifies_only_CP_fresh_configuration_without_PM(self):
        self.verify()
        self.assertEqual({app for app, _, _ in self.fixture.calls}, {sandbox.APPS[0]})
        self.assertEqual(sum(path.endswith('/configurations') for _, path, _ in self.fixture.calls), 1)
        self.assertFalse(any(key.startswith('E2E_PLAYMAKER_') for key in self.fixture.exports()))

    def test_cp_up_provisions_only_CP_and_single_alias(self):
        fixture = ProvisioningControlFixture(self.directory.name, 'cp')
        fixture.lifecycle.up([['cp']])
        self.assertEqual({app for app, _, _ in fixture.calls}, {sandbox.APPS[0]})
        self.assertEqual(fixture.cloned, [(sandbox.APPS[0], 'cp')])
        self.assertEqual(len(fixture.lifecycle.state['resources']), 1)
        self.assertEqual(fixture.lifecycle.state['scope'], 'cp')
        exports = dict(line.split('=', 1) for line in (Path(self.directory.name) / 'sandbox.env').read_text().splitlines())
        self.assertFalse(any(key.startswith('E2E_PLAYMAKER_') for key in exports))
        self.verify(fixture)
        fixture.lifecycle.down()
        self.assertEqual(fixture.lifecycle.state['cleanup'], 'CERTIFIED_API_ABSENCE')
        self.assertEqual(fixture.existing, set())

    def test_CLI_cp_single_alias_and_default_ecosystem_persist_scope(self):
        for mode in ['cp', 'ecosystem']:
            with self.subTest(mode=mode), tempfile.TemporaryDirectory(prefix='sandbox-cli-scope-') as directory:
                fixture = ProvisioningControlFixture(directory, mode)
                argv = ['sandbox.py', 'up', '--directory', directory, '--cp-service', 'cp']
                if mode == 'cp':
                    argv += ['--scope', 'cp']
                else:
                    argv += ['--pm-results-service', 'results', '--pm-locks-service', 'locks']
                def construct(path, state):
                    fixture.lifecycle.directory, fixture.lifecycle.state = path, state
                    return fixture.lifecycle
                with patch.object(sys, 'argv', argv), patch.object(sandbox, 'Lifecycle', side_effect=construct), contextlib.redirect_stdout(io.StringIO()):
                    sandbox.main()
                state = json.loads((Path(directory) / 'state.json').read_text())
                self.assertEqual(state['scope'], mode)
                self.assertEqual({item['app'] for item in state['resources']}, set(sandbox.APPS[:1] if mode == 'cp' else sandbox.APPS))
                self.assertEqual(len(fixture.cloned), 1 if mode == 'cp' else 3)

    def test_legacy_receipt_stays_ecosystem_and_explicit_ecosystem_passes(self):
        legacy = ControlFixture(self.directory.name)
        self.assertNotIn('scope', legacy.lifecycle.state)
        self.verify(legacy, 'ecosystem')
        self.assertEqual({app for app, _, _ in legacy.calls}, set(sandbox.APPS))

    def test_expected_scope_rejects_both_cross_family_directions_and_legacy_downgrade_before_API(self):
        for receipt, expected in [(self.fixture, 'ecosystem'),
                                  (ControlFixture(self.directory.name, 'ecosystem'), 'cp'),
                                  (ControlFixture(self.directory.name), 'cp')]:
            with self.subTest(expected=expected):
                with self.assertRaisesRegex(RuntimeError, 'SANDBOX_PROVENANCE_SCOPE_MISMATCH'):
                    self.verify(receipt, expected)
                self.assertEqual(receipt.calls, [])

    def test_invalid_persisted_scope_is_rejected(self):
        for invalid in [None, '', 'CP', 'other', True, 1, []]:
            with self.subTest(scope=invalid):
                self.fixture.lifecycle.state['scope'] = invalid
                with self.assertRaisesRegex(RuntimeError, 'SANDBOX_PROVENANCE_SCOPE_INVALID'):
                    self.fixture.lifecycle.verify()
                self.assertEqual(self.fixture.calls, [])

    def test_cp_rejects_PM_resource_and_duplicate_CP_resource_before_API(self):
        for resource in [ControlFixture(self.directory.name).lifecycle.state['resources'][1],
                         dict(self.fixture.lifecycle.state['resources'][0])]:
            with self.subTest(app=resource['app']):
                self.fixture.lifecycle.state['resources'].append(resource)
                with self.assertRaisesRegex(RuntimeError, 'SANDBOX_PROVENANCE_RESOURCE_NOT_OWNED'):
                    self.fixture.lifecycle.verify()
                self.assertEqual(self.fixture.calls, [])
                self.fixture.lifecycle.state['resources'].pop()

    def test_cp_rejects_extra_alias_and_PM_segment_in_receipt(self):
        resource = self.fixture.lifecycle.state['resources'][0]
        resource['logical_services'].append('results')
        with self.assertRaisesRegex(RuntimeError, 'SANDBOX_PROVENANCE_LOGICAL_MAPPING_INVALID'):
            self.fixture.lifecycle.verify()
        resource['logical_services'].pop()
        self.fixture.lifecycle.state['segments']['E2E_PLAYMAKER_KVS_SEGMENT_ID'] = 'pm'
        with self.assertRaisesRegex(RuntimeError, 'SANDBOX_PROVENANCE_SEGMENTS_OUTSIDE_SCOPE'):
            self.fixture.lifecycle.verify()
        self.assertEqual(self.fixture.calls, [])

    def test_cp_rejects_each_PM_mapping_consumed_from_environment(self):
        for key in ['E2E_PLAYMAKER_ACTION_RESULTS_CONTAINER', 'E2E_PLAYMAKER_ACTION_LOCKS_CONTAINER',
                    'E2E_PLAYMAKER_SANDBOX_BC', 'E2E_PLAYMAKER_SANDBOX_INSTANCE',
                    'E2E_PLAYMAKER_KVS_SEGMENT_ID', 'KEY_VALUE_STORE_RESULTS_CONTAINER_NAME']:
            with self.subTest(key=key):
                with self.assertRaisesRegex(RuntimeError, 'SANDBOX_CONSUMED_EXPORTS'):
                    self.verify(extras={key: 'foreign-control-metadata'})

    def test_cp_rejects_PM_API_call_and_mutation_receipt(self):
        fixture = ProvisioningControlFixture(self.directory.name, 'cp')
        with self.assertRaisesRegex(RuntimeError, 'SANDBOX_APPLICATION_NOT_OWNED'):
            fixture.lifecycle.call(sandbox.APPS[1], 'bc', 'POST', {}, allowed=(201,))
        self.assertEqual(fixture.calls, [])
        self.fixture.lifecycle.state['mutations'] = [{'app': sandbox.APPS[1], 'outcome': 'HTTP_200'}]
        with self.assertRaisesRegex(RuntimeError, 'SANDBOX_PROVENANCE_MUTATION_OUTSIDE_SCOPE'):
            self.fixture.lifecycle.down()
        self.assertEqual(self.fixture.calls, [])

    def test_cp_up_rejects_excess_services_before_API(self):
        fixture = ProvisioningControlFixture(self.directory.name, 'cp')
        with self.assertRaisesRegex(RuntimeError, 'SANDBOX_PROVENANCE_LOGICAL_MAPPING_INVALID'):
            fixture.lifecycle.up([['cp'], ['results', 'locks']])
        self.assertEqual(fixture.calls, [])

    def test_cp_partial_and_ecosystem_partial_cleanup_allow_only_observed_own_resources(self):
        for mode in ['cp', 'ecosystem']:
            with self.subTest(mode=mode):
                fixture = ControlFixture(self.directory.name, mode)
                fixture.lifecycle.state['resources'] = fixture.lifecycle.state['resources'][:1]
                fixture.lifecycle.state['status'] = 'PREPARING'
                fixture.lifecycle.require_owned = lambda resource: None
                fixture.lifecycle.down()
                self.assertEqual(fixture.lifecycle.state['cleanup'], 'CERTIFIED_API_ABSENCE')
                with self.assertRaisesRegex(RuntimeError, 'SANDBOX_PROVENANCE|SANDBOX_PROVENANCE_INCOMPLETE'):
                    fixture.lifecycle.verify()

    def test_cp_partial_unknown_creation_and_unknown_mutation_still_fail_cleanup(self):
        for unknown in ['creation', 'mutation']:
            with self.subTest(unknown=unknown):
                fixture = ControlFixture(self.directory.name, 'cp')
                fixture.lifecycle.state['status'] = 'PREPARING'
                if unknown == 'creation':
                    fixture.lifecycle.state['resources'][0]['creation_observed'] = False
                    fixture.lifecycle.state['resources'][0]['create_outcome'] = 'UNKNOWN'
                else:
                    fixture.lifecycle.state['mutations'] = [{'app': sandbox.APPS[0], 'outcome': 'UNKNOWN'}]
                fixture.lifecycle.require_owned = lambda resource: None
                with self.assertRaisesRegex(RuntimeError, 'SANDBOX_CLEANUP_FAILED'):
                    fixture.lifecycle.down()
                self.assertEqual(fixture.lifecycle.state['cleanup'], 'FAILED')

    def test_CLI_cp_rejects_missing_alias_or_PM_inputs_before_auth_or_API(self):
        for options, code in [([], 'SANDBOX_CP_OWN_KVS_ALIAS_REQUIRED'),
                             (['--cp-service', 'cp', '--pm-results-service', 'results'], 'SANDBOX_CP_SCOPE_FORBIDS_PLAYMAKER_INPUTS'),
                             (['--cp-service', 'cp', '--pm-locks-service', 'locks'], 'SANDBOX_CP_SCOPE_FORBIDS_PLAYMAKER_INPUTS'),
                             (['--cp-service', 'cp', '--pm-segment', 'pm'], 'SANDBOX_CP_SCOPE_FORBIDS_PLAYMAKER_INPUTS')]:
            with self.subTest(options=options):
                argv = ['sandbox.py', 'up', '--scope', 'cp', '--directory', self.directory.name] + options
                with patch.object(sys, 'argv', argv), patch.object(sandbox, 'Lifecycle') as constructor:
                    with self.assertRaisesRegex(RuntimeError, code):
                        sandbox.main()
                    constructor.assert_not_called()

    def test_CLI_expected_ecosystem_rejects_CP_receipt_before_auth_or_API(self):
        self.fixture.lifecycle.save()
        argv = ['sandbox.py', 'verify', '--scope', 'ecosystem', '--directory', self.directory.name]
        with patch.object(sys, 'argv', argv), patch.object(sandbox, 'Lifecycle') as constructor:
            with self.assertRaisesRegex(RuntimeError, 'SANDBOX_PROVENANCE_SCOPE_MISMATCH'):
                sandbox.main()
            constructor.assert_not_called()


if __name__ == '__main__':
    unittest.main(verbosity=1)
