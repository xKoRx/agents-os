from pathlib import Path
import subprocess,os,json,hashlib,sys
p=Path(__file__).resolve().parent;name=sys.argv[1]
args=['python3',str(p/name/'e2e/tests/sandbox-contract.py')]
if name=='baseline-red':args+=['ScopeControlContract.test_cp_receipt_verifies_only_CP_fresh_configuration_without_PM','ScopeControlContract.test_cp_rejects_PM_API_call_and_mutation_receipt']
temp=p/(name+'-temp');temp.mkdir(mode=0o700);env=os.environ.copy();env['TMPDIR']=str(temp)
r=subprocess.run(args,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=40)
(p/(name+'.log')).write_bytes(r.stdout)
d={'name':name,'command':args,'exit_status':r.returncode,'log_sha256':hashlib.sha256(r.stdout).hexdigest(),'scope':'API_METADATA_SIMULATOR_AND_PRIVATE_FS_ONLY_NO_BACKEND'}
(p/(name+'.json')).write_text(json.dumps(d,indent=2)+'\n');print(json.dumps(d));print(r.stdout.decode()[-1700:])
assert r.returncode==(1 if name=='baseline-red' else 0)
assert not list(temp.iterdir());temp.rmdir()
