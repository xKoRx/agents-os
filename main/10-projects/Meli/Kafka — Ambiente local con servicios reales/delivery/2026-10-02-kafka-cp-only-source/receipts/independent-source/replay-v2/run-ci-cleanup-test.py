from pathlib import Path
import importlib.util,json,os,unittest
pack=Path(__file__).resolve().parent
os.environ['CI_FAMILY_CONTRACT_ROOT']=str(pack)
os.environ['CI_FAMILY_CONTRACT_SOURCE']=str(pack/'e2e/ci.sh')
spec=importlib.util.spec_from_file_location('private_ci_test_cleanup',pack/'e2e/tests/ci-family-scope-contract.py')
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
class Result(unittest.TextTestResult):
    def __init__(self,*a,**kw):super().__init__(*a,**kw);self.cleanups=[]
    def stopTest(self,test):
        self.cleanups.append({'case':test._testMethodName,'own_temporary_directory':str(test.directory),'observed_absent':not test.directory.exists()})
        super().stopTest(test)
result=unittest.TextTestRunner(verbosity=1,resultclass=Result).run(unittest.defaultTestLoader.loadTestsFromTestCase(module.CiFamilyScopeContract))
assert result.wasSuccessful()
assert len(result.cleanups)==11 and all(c['observed_absent'] for c in result.cleanups)
(pack/'candidate-own-FS-cleanup.json').write_text(json.dumps({'status':'PASS_OWN_NEUTRAL_FS_ABSENCE_ONLY','tests':result.testsRun,'cleanups':result.cleanups,'backend_absence_certification':False},indent=2)+'\n')
