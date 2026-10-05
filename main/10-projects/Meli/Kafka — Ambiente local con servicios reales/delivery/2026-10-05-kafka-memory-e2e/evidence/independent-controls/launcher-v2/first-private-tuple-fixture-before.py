"""Native shell/private JSON control inputs; no Docker/Kafka/Gradle/native proof certificate."""
from pathlib import Path
import json,os,subprocess,tempfile,hashlib,copy
os.umask(0o077)
ROOT=Path(__file__).resolve().parent
source=(ROOT/'local.sh').read_text();begin=source.index('cleanup() {\n');end=source.index('\ntrap cleanup EXIT',begin);body=source[begin:end]
RUN='memory-neutral-report-control'
def complete_proof():
 return {'schema_version':1,'kind':'ACTUAL_GRADLE_TEST_TASK_COMPLETION','run_id':RUN,'task':'localKafkaE2eTest','owner_pid':99001,'owner_start_instant':'2026-10-05T00:00:00Z','gradle_version':'9.3.1','primary_classes':{'org.gradle.api.internal.tasks.testing.worker.ForkingTestDefinitionProcessor':'ebdbf25204440cfa88ec70783126625a40b31890ac3808d22e8b55f016b544c3','org.gradle.process.internal.worker.DefaultWorkerProcess':'75175385ef55b0418ab460a3835fc6e55fc3fc9af64c078cceac1b82b81e5101'},'task_outcome':'SUCCESS_WITH_WORKERS_REAPED_NORMAL_EXIT','test_count':1,'failed_count':0,'skipped_count':0,'workers':[{'schema_version':1,'kind':'OWNED_JUNIT_TEST_WORKER','run_id':RUN,'task':'localKafkaE2eTest','pid':99002,'process_start_instant':'2026-10-05T00:00:01Z','process_owner_pid':99001,'process_owner_start_instant':'2026-10-05T00:00:00Z','process_owner_kind':'GRADLE_TEST_WORKER_NORMAL_EXIT','gradle_worker_id':'1'}]}
skeleton={'kind':'ACTUAL_GRADLE_TEST_TASK_COMPLETION','run_id':RUN,'task':'localKafkaE2eTest','task_outcome':'SUCCESS_WITH_WORKERS_REAPED_NORMAL_EXIT','test_count':1,'failed_count':0,'skipped_count':0,'workers':[{'run_id':RUN,'task':'localKafkaE2eTest'}]}
foreign=complete_proof();foreign['run_id']='foreign-run'
wrongTask=complete_proof();wrongTask['task']='realIntegrationTest'
wrongTotals=complete_proof();wrongTotals['test_count']=2
wrongWorkerRun=complete_proof();wrongWorkerRun['workers'][0]['run_id']='foreign-run'
wrongWorkerOwner=complete_proof();wrongWorkerOwner['workers'][0]['process_owner_pid']=99999
forcedWorker=complete_proof();forcedWorker['task_outcome']='FORCED_KILL'
wrongWorkerPid=complete_proof();wrongWorkerPid['workers'][0]['pid']=True
cases=[
 ('missing-proof',None,{},'clean',0,False,'FAIL'),('foreign-proof',foreign,{},'clean',0,False,'FAIL'),
 ('wrong-task',wrongTask,{},'clean',0,False,'FAIL'),('wrong-counts',wrongTotals,{},'clean',0,False,'FAIL'),
 ('wrong-worker-run',wrongWorkerRun,{},'clean',0,False,'FAIL'),('forced-task',forcedWorker,{},'clean',0,False,'FAIL'),
 ('retained-UNKNOWN',complete_proof(),{},'retained',0,False,'FAIL'),('missing-reconciliation',complete_proof(),{},'missing',0,False,'FAIL'),
 ('public-reconciliation',complete_proof(),{},'public',0,False,'FAIL'),
 ('empty',complete_proof(),{'tests':0},'clean',0,False,'FAIL'),('skipped',complete_proof(),{'skipped':1},'clean',0,False,'FAIL'),
 ('failed',complete_proof(),{'failures':1},'clean',0,False,'FAIL'),('bad-command',complete_proof(),{},'clean',1,False,'FAIL'),
 ('bad-docker-query',complete_proof(),{},'clean',0,True,'FAIL'),
 ('complete-metadata-shape',complete_proof(),{},'clean',0,False,'PASS'),
 ('incomplete-worker-native-shape',skeleton,{},'clean',0,False,'FAIL'),
 ('wrong-worker-owner',wrongWorkerOwner,{},'clean',0,False,'FAIL'),
 ('boolean-worker-PID',wrongWorkerPid,{},'clean',0,False,'FAIL')]
records=[]
for name,proof,counts,mode,status,query in cases:
 with tempfile.TemporaryDirectory(prefix='owned-launcher-v2-control-',dir=ROOT) as temp:
  directory=Path(temp);junit=directory/'junit';junit.mkdir(mode=0o700);recon=directory/'retained-work';recon.mkdir(mode=0o700);exits=directory/'process-exit-records';exits.mkdir(mode=0o700)
  allcounts={'tests':1,'failures':0,'errors':0,'skipped':0};allcounts.update(counts)
  attrs=' '.join(str(k)+'="'+str(v)+'"' for k,v in allcounts.items());(junit/'TEST-control-only.xml').write_text('<testsuite name="NEUTRAL_REPORT_METADATA_ONLY" '+attrs+'/>\n')
  if proof:(exits/'test-task-localKafkaE2eTest.json').write_text(json.dumps(proof)+'\n')
  if mode=='retained':(recon/'owned-unknown.json').write_text('{"kind":"SOURCE_CONTROL_ONLY","state":"UNKNOWN"}\n')
  elif mode=='missing':recon.rmdir()
  elif mode=='public':recon.chmod(0o755)
  prelude='''set -euo pipefail
started=true
compose() { printf 'compose:%s\n' "$*" >>"${CONTROL_COMMANDS}"; return 0; }
docker() { printf 'docker:%s\n' "$*" >>"${CONTROL_COMMANDS}"; [[ "${CONTROL_QUERY_FAIL}" != true ]]; }
'''
  script=prelude+body+'\ntrap cleanup EXIT\nexit '+str(status)+'\n'
  env={'PATH':os.environ['PATH'],'PYTHONDONTWRITEBYTECODE':'1','ROOT':str(ROOT),'E2E_EVIDENCE_DIR':str(directory),'E2E_RECONCILIATION_DIR':str(recon),'E2E_PROCESS_EXIT_DIR':str(exits),'E2E_RUN_ID':RUN,'E2E_COMPOSE_PROJECT':'neutral-shell-control-only','CONTROL_COMMANDS':str(directory/'commands'),'CONTROL_QUERY_FAIL':str(query).lower()}
  process=subprocess.run(['/bin/bash','-c',script],env=env,cwd=directory,capture_output=True,text=True,timeout=10)
  result=json.loads((directory/'result.json').read_text());commands=(directory/'commands').read_text().splitlines() if (directory/'commands').exists() else []
  record={'case':name,'expected_control_verdict':('FAIL' if name not in ['complete-metadata-shape'] else 'PASS'),'actual_verdict':result['verdict'],'exit':process.returncode,'cleanup':result['cleanup'],'native_task_proof':result['native_task_proof'],'neutral_down_called':any(c.startswith('compose:down ') for c in commands),'control_outcome':'PASS' if result['verdict']==('PASS' if name=='complete-metadata-shape' else 'FAIL') else 'FAIL','scope':'SOURCE_METADATA_ONLY_NO_RUNTIME_NATIVE_OR_BACKEND_PROOF'}
  records.append(record)
 assert not directory.exists()
(ROOT/'controls.json').write_text(json.dumps({'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'records':records,'native_shell':'/bin/bash3.2','own_FS_absence_cases':len(records),'real_API_Docker_Kafka_Gradle_business_calls':0},indent=2)+'\n')
for record in records:print(json.dumps(record))
