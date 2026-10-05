"""Actual helper CLI + native owned PID death + private FS; proof metadata is explicitly control-only."""
from pathlib import Path
import subprocess,json,os,sys,copy,tempfile,hashlib
os.umask(0o077)
ROOT=Path(__file__).resolve().parent;TASK='localKafkaE2eTest';RUN='memory-native-control-run'
JAVA='/Users/rjara/Library/Java/JavaVirtualMachines/corretto-25.0.4/Contents/Home/bin/java'
worker=subprocess.Popen([JAVA,'-Xmx64m',str(ROOT/'NativeIdentity.java')],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
identity=json.loads(worker.stdout.readline());stdout,stderr=worker.communicate('\n',timeout=10)
assert worker.returncode==0 and identity['owner_pid']==os.getpid()
try:os.kill(identity['pid'],0);raise AssertionError('Own child was not reaped')
except ProcessLookupError:pass
PRIMARY={'org.gradle.api.internal.tasks.testing.worker.ForkingTestDefinitionProcessor':'ebdbf25204440cfa88ec70783126625a40b31890ac3808d22e8b55f016b544c3','org.gradle.process.internal.worker.DefaultWorkerProcess':'75175385ef55b0418ab460a3835fc6e55fc3fc9af64c078cceac1b82b81e5101'}
W={'schema_version':1,'kind':'OWNED_JUNIT_TEST_WORKER','run_id':RUN,'task':TASK,'pid':identity['pid'],'process_start_instant':identity['birth'],'process_owner_pid':identity['owner_pid'],'process_owner_start_instant':identity['owner_birth'],'process_owner_kind':'GRADLE_TEST_WORKER_NORMAL_EXIT','gradle_worker_id':'1'}
P={'schema_version':1,'kind':'ACTUAL_GRADLE_TEST_TASK_COMPLETION','run_id':RUN,'task':TASK,'owner_pid':identity['owner_pid'],'owner_start_instant':identity['owner_birth'],'gradle_version':'9.3.1','primary_classes':PRIMARY,'task_outcome':'SUCCESS_WITH_WORKERS_REAPED_NORMAL_EXIT','test_count':1,'failed_count':0,'skipped_count':0,'workers':[W]}
I={'schema_version':1,'kind':'OWNED_GRADLE_TEST_TASK_INTENT','run_id':RUN,'task':TASK,'owner_pid':identity['owner_pid'],'owner_start_instant':identity['owner_birth']}

source=(ROOT/'e2e/local.sh').read_text();a=source.index('cleanup() {\n');z=source.index('\ntrap cleanup EXIT',a);cleanup_body=source[a:z]
records=[]
cases=['complete-control-metadata','retained-UNKNOWN','missing-reconciliation','public-reconciliation','missing-proof','command-failed','docker-query-failed','compose-down-failed']
for name in cases:
 with tempfile.TemporaryDirectory(prefix='actual-cleanup-control-',dir=ROOT) as private:
  out=Path(private);(out/'junit').mkdir(mode=0o700);(out/'process-exit-records').mkdir(mode=0o700);td=out/'test-workers'/('task-'+TASK);td.mkdir(parents=True,mode=0o700);(out/'test-workers').chmod(0o700);recon=out/'retained-work';recon.mkdir(mode=0o700)
  p=copy.deepcopy(P);i=copy.deepcopy(I);w=copy.deepcopy(W)
  (out/'junit'/'TEST-neutral.xml').write_text('<testsuite name="CONTROL_ONLY" tests="1" failures="0" errors="0" skipped="0"/>\n')
  if name!='missing-proof':(out/'process-exit-records'/('test-task-'+TASK+'.json')).write_text(json.dumps(p)+'\n')
  (td/'owner-intent.json').write_text(json.dumps(i)+'\n');(td/('worker-'+str(w['pid'])+'.json')).write_text(json.dumps(w)+'\n')
  if name=='retained-UNKNOWN':(recon/'own-control.json').write_text('{"kind":"CONTROL_ONLY","state":"UNKNOWN"}\n')
  elif name=='missing-reconciliation':recon.rmdir()
  elif name=='public-reconciliation':recon.chmod(0o755)
  prelude='''set -euo pipefail
started=true
compose() { printf 'compose:%s\n' "$*" >>"${CONTROL_COMMANDS}"; [[ "${1}" != down || "${CONTROL_DOWN_FAIL}" != true ]]; }
docker() { printf 'docker:%s\n' "$*" >>"${CONTROL_COMMANDS}"; [[ "${CONTROL_QUERY_FAIL}" != true ]]; }
'''
  script=prelude+cleanup_body+'\ntrap cleanup EXIT\nexit '+('1' if name=='command-failed' else '0')+'\n'
  env={'PATH':os.environ['PATH'],'PYTHONDONTWRITEBYTECODE':'1','ROOT':str(ROOT),'E2E_EVIDENCE_DIR':str(out),'E2E_RECONCILIATION_DIR':str(recon),'E2E_RUN_ID':RUN,'E2E_COMPOSE_PROJECT':'neutral-no-docker-project','CONTROL_COMMANDS':str(out/'commands'),'CONTROL_QUERY_FAIL':str(name=='docker-query-failed').lower(),'CONTROL_DOWN_FAIL':str(name=='compose-down-failed').lower()}
  cp=subprocess.run(['/bin/bash','-c',script],env=env,cwd=out,capture_output=True,text=True,timeout=10)
  result=json.loads((out/'result.json').read_text());commands=(out/'commands').read_text().splitlines() if (out/'commands').exists() else [];down=any(s.startswith('compose:down ') for s in commands)
  expected='PASS' if name=='complete-control-metadata' else 'FAIL';retained=name in ['retained-UNKNOWN','missing-reconciliation','public-reconciliation']
  ok=result['verdict']==expected and (cp.returncode==0)==(expected=='PASS') and (not retained or (not down and result['cleanup']=='RETAINED'))
  records.append({'case':name,'verdict':result['verdict'],'exit':cp.returncode,'cleanup':result['cleanup'],'neutral_down_called':down,'native_task_proof':result['native_task_proof'],'control_outcome':'PASS' if ok else 'FAIL'})
 assert not out.exists()
result={'scope':'ACTUAL_BASH_CLEANUP_PLUS_ACTUAL_PYTHON_CLI_PRIVATE_FS_AND_OWN_NATIVE_PROCESS_WITH_NEUTRAL_COMPOSE_DOCKER_COMMAND_STANDINS','local_source_sha256':hashlib.sha256(source.encode()).hexdigest(),'native_child_exit_status':worker.returncode,'actual_own_native_child_absent':True,'own_FS_directories_absent':len(records),'controls':records,'real_Gradle_Kafka_Docker_Fury_API_business_calls':0}
(ROOT/'cleanup-controls.json').write_text(json.dumps(result,indent=2)+'\n')
for row in records:print(json.dumps(row))
