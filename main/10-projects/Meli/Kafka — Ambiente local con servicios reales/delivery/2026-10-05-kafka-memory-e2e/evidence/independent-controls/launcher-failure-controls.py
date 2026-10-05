"""Shell/report metadata controls only; no real Docker/Kafka or business execution."""
from pathlib import Path
import json,os,subprocess,tempfile,hashlib
ROOT=Path(__file__).resolve().parent
source=(ROOT/'local-before-controls.sh').read_text();begin=source.index('cleanup() {\n');end=source.index('\ntrap cleanup EXIT',begin)
body=source[begin:end]
records=[]
for name,counts,marker,proof,status,docker_failure in [
 ('nonempty-missing-native-proof',{'tests':1},False,None,0,False),
 ('nonempty-foreign-native-proof',{'tests':1},False,'foreign-run',0,False),
 ('nonempty-retained-UNKNOWN',{'tests':1},True,None,0,False),
 ('empty-selection',{'tests':0},False,None,0,False),
 ('skipped-selection',{'tests':1,'skipped':1},False,None,0,False),
 ('failed-selection',{'tests':1,'failures':1},False,None,0,False),
 ('failed-command',{'tests':1},False,None,1,False),
 ('failed-docker-query',{'tests':1},False,None,0,True)]:
 with tempfile.TemporaryDirectory(prefix='owned-memory-launcher-control-',dir=ROOT) as private:
  directory=Path(private);junit=directory/'junit';junit.mkdir(mode=0o700)
  reconciliation=directory/'retained-work';reconciliation.mkdir(mode=0o700)
  exits=directory/'process-exit-records';exits.mkdir(mode=0o700)
  attributes=' '.join(str(k)+'="'+str(v)+'"' for k,v in counts.items())
  (junit/'TEST-neutral-control.xml').write_text('<testsuite name="NEUTRAL_REPORT_CONTROL_ONLY" '+attributes+'/>\n')
  if marker:(reconciliation/'owned-unknown.json').write_text('{"state":"UNKNOWN","kind":"NEUTRAL_RECONCILIATION_CONTROL_ONLY"}\n')
  if proof:(exits/'test-task-localKafkaE2eTest.json').write_text(json.dumps({'run_id':proof,'kind':'NEUTRAL_INVALID_PROOF_CONTROL_ONLY'})+'\n')
  prelude='''set -euo pipefail
started=true
compose() { printf 'compose:%s\n' "$*" >>"${CONTROL_COMMANDS}"; return 0; }
docker() { printf 'docker:%s\n' "$*" >>"${CONTROL_COMMANDS}"; [[ "${CONTROL_DOCKER_FAIL}" != true ]]; }
'''
  script=prelude+body+'\ntrap cleanup EXIT\nexit '+str(status)+'\n'
  env={'PATH':os.environ['PATH'],'PYTHONDONTWRITEBYTECODE':'1','E2E_EVIDENCE_DIR':str(directory),'E2E_RECONCILIATION_DIR':str(reconciliation),'E2E_PROCESS_EXIT_DIR':str(exits),'E2E_RUN_ID':'local-control-'+name,'E2E_COMPOSE_PROJECT':'owned-neutral-shell-control-only','CONTROL_COMMANDS':str(directory/'commands'),'CONTROL_DOCKER_FAIL':str(docker_failure).lower()}
  result=subprocess.run(['/bin/bash','-c',script],env=env,cwd=directory,capture_output=True,text=True,timeout=10)
  summary=json.loads((directory/'result.json').read_text())
  commands=(directory/'commands').read_text().splitlines()
  records.append({'case':name,'exit':result.returncode,'result':summary,'neutral_compose_down_invoked':any(c.startswith('compose:down ') for c in commands),'own_marker_retained':marker and (reconciliation/'owned-unknown.json').exists(),'real_Docker_Kafka_API_or_business_calls':0})
 assert not directory.exists()
(ROOT/'launcher-failure-controls.json').write_text(json.dumps({'phase':'UNFROZEN_SOURCE_OBSERVATION_ONLY','source_sha256':hashlib.sha256(source.encode()).hexdigest(),'records':records,'owned_FS_directories_reaped':len(records)},indent=2)+'\n')
for result in records:print(json.dumps({'case':result['case'],'exit':result['exit'],'verdict':result['result']['verdict'],'down_called':result['neutral_compose_down_invoked']}))
