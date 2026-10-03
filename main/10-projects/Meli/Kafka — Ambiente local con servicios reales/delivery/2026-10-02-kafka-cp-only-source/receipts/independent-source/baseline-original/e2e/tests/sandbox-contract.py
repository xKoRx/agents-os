#!/usr/bin/env python3
"""Permanent lifecycle control-flow regressions; no Sandbox/KVS/E2E certificate."""
import importlib.util
import os
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
    def __init__(self, directory):
        self.lifecycle = sandbox.Lifecycle.__new__(sandbox.Lifecycle)
        self.lifecycle.directory = Path(directory)
        run = 'a' * 32
        self.lifecycle.state = {'schema': 1, 'run_id': run, 'marker': 'Owned Kafka E2E ' + run,
            'status': 'OWNED_CONFIG_GENERATED_NOT_KVS_CERTIFIED', 'segments': {}, 'resources': []}
        self.configs = {}
        self.calls = []
        for app, aliases, instance in zip(sandbox.APPS, [['cp'], ['results', 'locks']], ['1', '2']):
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


if __name__ == '__main__':
    unittest.main(verbosity=1)
