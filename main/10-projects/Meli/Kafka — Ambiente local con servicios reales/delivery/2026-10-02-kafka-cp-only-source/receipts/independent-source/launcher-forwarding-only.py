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
(p/'launcher-forwarding-controls.json').write_text(json.dumps({'status':'PASS','scope':'ACTUAL_PRIVATE_LAUNCHER_NEUTRAL_REJECTING_GATE_ONLY','records':results,'Docker_API_calls':0,'Gradle_calls':0,'business':'NOT_EXECUTED'},indent=2)+'\n')
print(json.dumps({'launcher_cases':len(results),'status':'PASS','business':'NOT_EXECUTED'}))
