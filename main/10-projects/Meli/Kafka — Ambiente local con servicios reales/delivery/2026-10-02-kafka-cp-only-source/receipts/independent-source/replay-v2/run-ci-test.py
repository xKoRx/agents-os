from pathlib import Path
import importlib.util,json,os,sys,unittest
pack=Path(__file__).resolve().parent
os.environ['CI_FAMILY_CONTRACT_ROOT']=str(pack)
case=sys.argv[1]
sources={'candidate':pack/'e2e/ci.sh','baseline-3bea':pack/'before/baseline-3bea.sh','scoped-before-trap':pack/'before/scoped-before-trap.sh','bare-variable-before':pack/'before/bare-variable-before.sh'}
os.environ['CI_FAMILY_CONTRACT_SOURCE']=str(sources[case])
spec=importlib.util.spec_from_file_location('private_ci_test',pack/'e2e/tests/ci-family-scope-contract.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class Result(unittest.TextTestResult):
    def __init__(self,*args,**kwargs):super().__init__(*args,**kwargs);self.records=[]
    def addSuccess(self,test):
        super().addSuccess(test);self.records.append({'test':test._testMethodName,'status':'PASS','own_FS_removed':not test.directory.exists()})
    def addFailure(self,test,err):
        super().addFailure(test,err);self.records.append({'test':test._testMethodName,'status':'FAIL','failure':self._exc_info_to_string(err,test),'own_FS_removed':not test.directory.exists()})
    def addError(self,test,err):
        super().addError(test,err);self.records.append({'test':test._testMethodName,'status':'ERROR','error':self._exc_info_to_string(err,test),'own_FS_removed':not test.directory.exists()})
suite=unittest.defaultTestLoader.loadTestsFromTestCase(module.CiFamilyScopeContract)
if case=='bare-variable-before':suite=unittest.TestSuite([module.CiFamilyScopeContract('test_managed_bound_private_runs_reach_neutral_transport_and_preserve_failure')])
result=unittest.TextTestRunner(verbosity=2,resultclass=Result).run(suite)
# Success/failure callbacks precede unittest cleanups; assert absence after all cleanup instead.
for record in result.records:record.pop('own_FS_removed',None)
value={'case':case,'source':str(sources[case]),'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'records':result.records,'scope':'NATIVE_SHELL_PRIVATE_FS_METADATA_ONLY','remote_API_Docker_Gradle_business_calls':0}
(pack/(case+'-ci-tests.json')).write_text(json.dumps(value,indent=2)+'\n')
raise SystemExit(not result.wasSuccessful())
