from pathlib import Path
import subprocess,json,os,tempfile,hashlib
p=Path(__file__).resolve().parent;root=p/'candidate';results=[]
for phase,source in [('bare-regression',p/'trap-2-ci-bare-variable.before'),('fixed',p/'trap-2-ci-bare-variable.after')]:
 text=source.read_text();functions=text[text.index('clear_family_runtime() {'):text.index('\nrecord_sources() {')]
 cases=['managed-valid-metadata'] if phase=='bare-regression' else ['cp-no-PM-up-fails','PM-missing-inputs','managed-missing-inputs','managed-valid-metadata']
 for case in cases:
  with tempfile.TemporaryDirectory(dir=p,prefix='trap-delta-') as d:
   d=Path(d);capture=d/'capture.jsonl';spy=d/'neutral-verifier'
   spy.write_text('#!/usr/bin/env python3\nimport json,os,sys\nfrom pathlib import Path\nwith Path(os.environ["L0_CAPTURE"]).open("a") as f:f.write(json.dumps(sys.argv[1:])+"\\n")\nraise SystemExit(43)\n');spy.chmod(0o700)
   env={'PATH':os.environ['PATH'],'HOME':os.environ['HOME'],'L0_CAPTURE':str(capture),'JAVA_HOME':'L0_NO_JAVA_EXECUTION','E2E_FURY_PYTHON':str(spy),'DOCKER_CONTEXT':'L0_NO_DOCKER','E2E_CP_KVS_SERVICE':'own-cp-alias-control'}
   if case=='managed-valid-metadata':
    managed=d/'managed.env';kvs=d/'kvs.env';run='a'*32
    managed.write_text('E2E_MANAGED_SCOPE=test-e2e\nE2E_MANAGED_RUN_ID='+run+'\n');managed.chmod(0o600)
    kvs.write_text('E2E_RUN_ID='+run+'\nE2E_KVS_EXCLUSIVE_RUN_ID='+run+'\nE2E_KVS_SANDBOX_PROVENANCE='+str(d/'state.json')+'\n');kvs.chmod(0o600)
    env.update({'E2E_MANAGED_ENV_FILE':str(managed),'E2E_MANAGED_KVS_ENV_FILE':str(kvs)})
    for name in ['cp-functional','playmaker-canonical','playmaker-candidate']:
     x=d/name;x.mkdir(mode=0o700);(x/'gate.json').write_text(json.dumps({'run_id':'b'*32,'exit_status':2,'metadata_fixture_only':True}))
   invocation='run_managed_family' if case.startswith('managed') else 'run_local_family cp-control '+('realIntegrationTest' if case.startswith('cp-') else 'e2eCanonicalPlaymakerTest')
   command='set -euo pipefail\numask 077\nSCRIPT_DIR='+str(root/'e2e')+'\nROOT='+str(root)+'\nCI_PRIVATE_DIR='+str(d)+'\n'+functions+'\n'+invocation+'\n'
   r=subprocess.run(['/bin/bash','-c',command],env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=20)
   log=p/(phase+'-'+case+'.log');log.write_bytes(r.stdout)
   family='managed-oauth-bigqueue' if case.startswith('managed') else 'cp-control';gatefile=d/family/'gate.json'
   assert gatefile.exists(),(case,r.returncode,r.stdout.decode())
   gate=json.loads(gatefile.read_text());calls=[json.loads(x) for x in capture.read_text().splitlines()] if capture.exists() else []
   record={'phase':phase,'case':case,'exit_status':r.returncode,'gate':gate,'captured_args':calls,'stderr':r.stdout.decode().strip(),'log_sha256':hashlib.sha256(r.stdout).hexdigest(),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'real_Docker_Gradle_API_or_business_calls':0}
   if phase=='bare-regression':
    assert r.returncode==gate['exit_status']==127 and 'kvs_run: command not found' in record['stderr'] and calls==[]
   elif case=='cp-no-PM-up-fails':
    assert r.returncode==gate['exit_status']==1 and gate['sandbox_cleanup_status']==1 and 'CI_SANDBOX_RETAINED' in record['stderr']
    assert len(calls)==1 and calls[0]==[str(root/'e2e/sandbox.py'),'up','--scope','cp','--directory',str(d/'cp-control/sandbox'),'--cp-service','own-cp-alias-control']
   elif case=='PM-missing-inputs':
    assert r.returncode==gate['exit_status']==2 and calls==[] and 'E2E_PM_RESULTS_KVS_SERVICE' in record['stderr']
   elif case=='managed-missing-inputs':
    assert r.returncode==gate['exit_status']==2 and calls==[] and 'E2E_MANAGED_ENV_FILE' in record['stderr']
   else:
    assert r.returncode==gate['exit_status']==43 and len(calls)==1 and calls[0][-2:]==['--scope','ecosystem']
   assert 'unbound variable' not in record['stderr']
   results.append(record)
(p/'trap-delta-controls.json').write_text(json.dumps({'status':'PASS_BOTH_FIXES_SOURCE_AND_NEUTRAL_ONLY','records':results,'source_before_RED127_preserved':True,'actual_after_families':4,'real_Docker_Gradle_API_or_business_calls':0},indent=2)+'\n')
print(json.dumps({'status':'PASS','before_RED':127,'after_cases':4,'actual_managed_read_run_parser':'PASS_PRIVATE_0600_ENV_METADATA_ONLY','real_Docker_Gradle_API_or_business_calls':0}))
