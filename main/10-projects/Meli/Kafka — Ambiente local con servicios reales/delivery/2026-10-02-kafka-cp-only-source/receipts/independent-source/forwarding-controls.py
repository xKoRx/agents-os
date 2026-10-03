from pathlib import Path
import tempfile,subprocess,os,json,sys,importlib.util
p=Path(__file__).resolve().parent;root=p/'candidate';results=[]
spec=importlib.util.spec_from_file_location('scope_contract',root/'e2e/tests/sandbox-contract.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
spy_text='''#!/usr/bin/env python3
import os,sys,json
from pathlib import Path
with Path(os.environ['L0_CAPTURE']).open('a') as out:out.write(json.dumps({'args':sys.argv[1:]})+'\\n')
raise SystemExit(43)
'''
docker_text='''#!/usr/bin/env python3
import sys,os,json
from pathlib import Path
args=sys.argv[1:]
with Path(os.environ['L0_DOCKER_COMMAND_CAPTURE']).open('a') as out:out.write(json.dumps(args)+'\\n')
if args != ['info','--format','{{.MemTotal}}']:raise SystemExit(99)
print(6442450944)
'''
for suite,scope in [('realIntegrationTest','cp'),('default','cp'),('e2eTest','ecosystem'),('e2eCanonicalPlaymakerTest','ecosystem')]:
 with tempfile.TemporaryDirectory(dir=p,prefix='peer-launch-') as d:
  d=Path(d);bin=d/'bin';bin.mkdir(mode=0o700);spy=bin/'neutral-verifier';spy.write_text(spy_text);spy.chmod(0o700)
  docker=bin/'docker';docker.write_text(docker_text);docker.chmod(0o700)
  capture=d/'capture.jsonl';docker_capture=d/'docker-commands.jsonl';f=m.ControlFixture(d,scope);f.lifecycle.save();env_file=d/'sandbox.env'
  env_file.write_text('\n'.join(k+'='+v for k,v in f.exports().items())+'\n');env_file.chmod(0o600)
  env={'PATH':str(bin)+':'+os.environ['PATH'],'HOME':os.environ['HOME'],'E2E_KVS_ENV_FILE':str(env_file),'E2E_FURY_PYTHON':str(spy),'DOCKER_CONTEXT':'L0-NO-SERVICE','L0_CAPTURE':str(capture),'L0_DOCKER_COMMAND_CAPTURE':str(docker_capture)}
  if suite=='e2eCanonicalPlaymakerTest':env['E2E_PLAYMAKER_CANONICAL_REPO']=str(d)
  args=['bash',str(root/'e2e/run.sh')]+([] if suite=='default' else [suite]);r=subprocess.run(args,env=env,capture_output=True,text=True,timeout=15)
  (p/('launcher-'+suite+'.log')).write_text(r.stdout+r.stderr)
  assert r.returncode==43,(suite,r.returncode,r.stderr)
  calls=[json.loads(x)['args'] for x in capture.read_text().splitlines()]
  assert calls==[[str(root/'e2e/sandbox.py'),'verify','--directory',str(d),'--scope',scope]],calls
  command_calls=[json.loads(x) for x in docker_capture.read_text().splitlines()];assert command_calls==[['info','--format','{{.MemTotal}}']]
  assert not (root/'build').exists()
  results.append({'case':'actual-private-launcher-'+suite,'exit_status':43,'scope':scope,'captured_args':calls[0],'real_Docker_calls':0,'L0_command_shape_checks':len(command_calls),'business':'NOT_EXECUTED_REJECTED_BEFORE_FIXTURE'})
source=(root/'e2e/ci.sh').read_text();functions=source[source.index('clear_family_runtime() {'):source.index('\nrun_managed_family() (')]
for suite,expect_capture in [('realIntegrationTest',True),('e2eCanonicalPlaymakerTest',False)]:
 with tempfile.TemporaryDirectory(dir=p,prefix='peer-ci-') as d:
  d=Path(d);capture=d/'ci-capture.jsonl';spy=d/'neutral-verifier';spy.write_text(spy_text);spy.chmod(0o700)
  prefix='set -euo pipefail\numask 077\nSCRIPT_DIR='+str(root/'e2e')+'\nROOT='+str(root)+'\nCI_PRIVATE_DIR='+str(d)+'\n'
  command=prefix+functions+'\nrun_local_family cp-control '+suite+'\n'
  env={'PATH':os.environ['PATH'],'HOME':os.environ['HOME'],'JAVA_HOME':'/Users/rjara/Library/Java/JavaVirtualMachines/corretto-25.0.4/Contents/Home','DOCKER_CONTEXT':'L0-NO-SERVICE','E2E_FURY_PYTHON':str(spy),'E2E_CP_KVS_SERVICE':'own-cp-alias-control','L0_CAPTURE':str(capture)}
  r=subprocess.run(['bash','-c',command],env=env,capture_output=True,text=True,timeout=15)
  (p/('ci-'+suite+'.log')).write_text(r.stdout+r.stderr)
  assert r.returncode!=0
  gate=json.loads((d/'cp-control/gate.json').read_text());assert gate['exit_status']!=0
  if expect_capture:
   calls=[json.loads(x)['args'] for x in capture.read_text().splitlines()]
   assert len(calls)==1 and calls[0]==[str(root/'e2e/sandbox.py'),'up','--scope','cp','--directory',str(d/'cp-control/sandbox'),'--cp-service','own-cp-alias-control']
   assert gate['sandbox_cleanup_status']==1 and 'CI_SANDBOX_RETAINED' in r.stderr
  else:
   assert not capture.exists() and 'E2E_PM_RESULTS_KVS_SERVICE' in r.stderr and 'E2E_PM_LOCKS_KVS_SERVICE' in r.stderr
   calls=[]
  results.append({'case':'actual-CI-functions-'+suite,'exit_status':r.returncode,'no_PM_inputs':True,'captured_args':calls,'gate':gate,'real_Docker_Gradle_or_API_calls':0,'business':'NOT_EXECUTED_NEUTRAL_GATE_REJECTED_OR_INPUTS_MISSING'})
(p/'forwarding-controls.json').write_text(json.dumps({'status':'PASS','scope':'ACTUAL_PRIVATE_SHELL_SOURCE_WITH_NEUTRAL_PREBUSINESS_REJECTING_GATE_AND_COMMAND_SHAPES_ONLY','records':results,'real_Docker_calls':0,'Gradle_calls':0,'API_calls':0,'business':'NOT_EXECUTED'},indent=2)+'\n')
print(json.dumps({'status':'PASS','actual_launcher_scope_checks':4,'actual_CI_function_checks':2,'real_Docker_or_Gradle_or_APIs':0}))
