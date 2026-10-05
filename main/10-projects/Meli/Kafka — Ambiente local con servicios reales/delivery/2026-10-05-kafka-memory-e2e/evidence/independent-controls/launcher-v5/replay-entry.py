from pathlib import Path
import subprocess,json,hashlib,tempfile,os
b=Path(__file__).resolve().parent;os.umask(0o077)
s=(b/'e2e/run.sh').read_text();old=subprocess.check_output(['git','show','7f1720d950446638ff9b15a0e4e167f3e8e26e43:e2e/run.sh'],cwd='/private/tmp/kafka-e2e-memory-20261005/cp',text=True)
remote=s[s.index('readonly SUITE='):];prior=old[old.index('readonly SUITE='):];assert remote==prior
records=[]
with tempfile.TemporaryDirectory(prefix='entry-controls-',dir=b) as tmp:
 p=Path(tmp);(p/'e2e').mkdir(mode=0o700);(p/'e2e/run.sh').write_text(s);(p/'e2e/local.sh').write_text('#!/bin/bash\npython3 -c \'import json,sys;print(json.dumps(sys.argv[1:]))\' "$@"\n');(p/'e2e/local.sh').chmod(0o700)
 for name,args,expect in [('default',[],[]),('explicit-local',['localKafkaE2eTest','--tests','A B'],['--tests','A B']),('remote-cp',['realIntegrationTest'],None),('remote-pm',['e2eTest'],None),('remote-canonical',['e2eCanonicalPlaymakerTest'],None),('remote-candidate',['e2eCandidatePlaymakerTest'],None)]:
  env={'PATH':'/usr/bin:/bin','E2E_PLAYMAKER_CANONICAL_REPO':str(p/'canonical'),'E2E_PLAYMAKER_CANDIDATE_REPO':str(p/'candidate')}
  if expect is not None:env['PATH']=os.environ['PATH']
  r=subprocess.run(['/bin/bash',str(p/'e2e/run.sh'),*args],env=env,text=True,capture_output=True,timeout=5)
  ok=(r.returncode==0 and json.loads(r.stdout)==expect) if expect is not None else r.returncode==2 and r.stderr.strip()=='REAL_E2E_MISSING_COMMAND:docker'
  records.append({'case':name,'exit':r.returncode,'control_outcome':'PASS' if ok else 'FAIL','actual_local_arguments':json.loads(r.stdout) if expect is not None else None,'actual_remote_pre_business_gate':r.stderr.strip() if expect is None else None})
 assert all(r['control_outcome']=='PASS' for r in records)
assert not p.exists()
d={'scope':'ACTUAL_NATIVE_BASH_ENTRY_BRANCH_WITH_NEUTRAL_LOCAL_ARGUMENT_STUB_NO_DOCKER_GRADLE_OR_REMOTE_API','source_sha256':hashlib.sha256(s.encode()).hexdigest(),'remote_suffix_byte_identical_to_base':True,'base':'7f1720d950446638ff9b15a0e4e167f3e8e26e43','controls':records,'own_FS_absent':True}
(b/'entry-controls.json').write_text(json.dumps(d,indent=2)+'\n')
for row in records:print(json.dumps(row))
