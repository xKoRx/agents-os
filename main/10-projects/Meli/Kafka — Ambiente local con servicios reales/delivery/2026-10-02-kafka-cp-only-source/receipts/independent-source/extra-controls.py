from pathlib import Path
import importlib.util,unittest,tempfile,os,json,sys,contextlib,io
from unittest.mock import patch
p=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('scope_contract',p/'candidate/e2e/tests/sandbox-contract.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
s=m.sandbox
class PeerExtraControls(unittest.TestCase):
 def test_unknown_start_preserves_env_and_journal_after_api_shape_absence(self):
  with tempfile.TemporaryDirectory(dir=p,prefix='peer-unknown-') as d:
   f=m.ProvisioningControlFixture(d,'cp');original=f.api_call
   def call(route,method,**kw):
    if route.endswith('/start'):raise TimeoutError('neutral API shape only')
    return original(route,method,**kw)
   f.lifecycle.api.make_api_call=call
   artifact=Path(d)/'sandbox.env';artifact.write_text('PRIVATE_CONTROL_ARTIFACT\n');artifact.chmod(0o600)
   with self.assertRaisesRegex(RuntimeError,'SANDBOX_API_FAILED:TimeoutError'):f.lifecycle.up([['cp']])
   with self.assertRaisesRegex(RuntimeError,'SANDBOX_CLEANUP_FAILED'):f.lifecycle.down()
   disk=json.loads((Path(d)/'state.json').read_text())
   self.assertEqual('FAILED',disk['cleanup']);self.assertTrue(artifact.exists());self.assertEqual(set(),f.existing)
   self.assertTrue(any(x['outcome']=='UNKNOWN' and x['suffix'].endswith('/start') for x in disk['mutations']))
   self.assertEqual(0o600,(Path(d)/'state.json').stat().st_mode&0o777)
   self.assertEqual({s.APPS[0]},{app for app,_,_ in f.calls})
 def test_CLI_down_cross_scope_rejected_before_auth_or_constructor(self):
  for actual,expected in [('cp','ecosystem'),('ecosystem','cp'),(None,'cp')]:
   with self.subTest(actual=actual,expected=expected),tempfile.TemporaryDirectory(dir=p,prefix='peer-cross-down-') as d:
    f=m.ControlFixture(d,actual);f.lifecycle.save()
    argv=['sandbox.py','down','--directory',d,'--scope',expected]
    with patch.object(sys,'argv',argv),patch.object(s,'Lifecycle') as ctor:
     with self.assertRaisesRegex(RuntimeError,'SANDBOX_PROVENANCE_SCOPE_MISMATCH'):s.main()
     ctor.assert_not_called()
 def test_CP_fresh_mapping_change_rejected_even_if_receipt_and_environment_were_valid(self):
  for field,new,code in [('KEY_VALUE_STORE_CP_CONTAINER_NAME','sbox_different','SANDBOX_PROVENANCE_MAPPING_CHANGED'),('KEY_VALUE_STORE_CP_END_POINT_READ','https://different.invalid/read','SANDBOX_CONSUMED_EXPORTS')]:
   with self.subTest(field=field),tempfile.TemporaryDirectory(dir=p,prefix='peer-mapping-') as d:
    f=m.ControlFixture(d,'cp');env=f.exports();f.configs[s.APPS[0]]['configurations'][0]['configuration'][field]=new
    with patch.dict(os.environ,env,clear=True):
     with self.assertRaisesRegex(RuntimeError,code):f.lifecycle.verify('cp')
    self.assertEqual(1,sum(x.endswith('/configurations') for _,x,_ in f.calls))
 def test_scope_expansion_on_partial_down_never_dispatches_mutation(self):
  for kind in ['resources','segments','mutations']:
   with self.subTest(kind=kind),tempfile.TemporaryDirectory(dir=p,prefix='peer-expansion-') as d:
    f=m.ProvisioningControlFixture(d,'cp')
    if kind=='resources':f.lifecycle.state[kind]=m.ControlFixture(d,'ecosystem').lifecycle.state[kind]
    if kind=='segments':f.lifecycle.state[kind]={'E2E_PLAYMAKER_KVS_SEGMENT_ID':'other'}
    if kind=='mutations':f.lifecycle.state[kind]=[{'app':s.APPS[1],'outcome':'UNKNOWN'}]
    with self.assertRaisesRegex(RuntimeError,'SANDBOX_PROVENANCE'):f.lifecycle.down()
    self.assertEqual([],f.calls)
 def test_CLI_default_ecosystem_without_PM_aliases_still_rejects_before_auth(self):
  with tempfile.TemporaryDirectory(dir=p,prefix='peer-default-') as d:
   with patch.object(sys,'argv',['sandbox.py','up','--directory',d,'--cp-service','cp']),patch.object(s,'Lifecycle') as ctor:
    with self.assertRaisesRegex(RuntimeError,'SANDBOX_THREE_OWN_APPLICATION_KVS_ALIASES_REQUIRED'):s.main()
    ctor.assert_not_called()
if __name__=='__main__':unittest.main(verbosity=2)
