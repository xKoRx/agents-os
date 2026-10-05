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
cases=['complete-control-metadata','intent-owner-PID-float','actual-worker-file-PID-float','actual-worker-file-schema-bool','actual-worker-file-owner-PID-float']
records=[]
for name in cases:
 with tempfile.TemporaryDirectory(prefix='own-local-proof-control-',dir=ROOT) as private:
  out=Path(private);(out/'junit').mkdir(mode=0o700);(out/'process-exit-records').mkdir(mode=0o700);td=out/'test-workers'/('task-'+TASK);td.mkdir(parents=True,mode=0o700)
  (out/'test-workers').chmod(0o700)
  p=copy.deepcopy(P);i=copy.deepcopy(I);w=copy.deepcopy(W);status=0;cleanup='PASS';tests=1;skip=0
  if name=='intent-owner-PID-float':i['owner_pid']=float(i['owner_pid'])
  elif name=='wrong-run':p['run_id']='foreign-run'
  elif name=='wrong-task':p['task']='realIntegrationTest'
  elif name=='wrong-primary':p['primary_classes']={}
  elif name=='bad-owner-PID-bool':p['owner_pid']=True;i['owner_pid']=True;w['process_owner_pid']=True
  elif name=='bad-worker-PID-bool':w['pid']=True
  elif name=='bad-worker-PID-float':w['pid']=float(w['pid'])
  elif name=='worker-owner-mismatch':w['process_owner_pid']=identity['pid']
  elif name=='worker-birth-file-mismatch':w['process_start_instant']='invalid-birth'
  elif name=='worker-gradle-id-missing':w.pop('gradle_worker_id')
  elif name=='worker-native-still-alive':w['pid']=os.getpid();w['process_start_instant']=identity['owner_birth']
  elif name=='counts-bool':p['test_count']=True
  elif name=='failed-command':status=1
  elif name=='retained-cleanup':cleanup='RETAINED'
  elif name=='skipped-XML':skip=1
  elif name=='empty-XML':tests=0;p['test_count']=0
  elif name=='owner-birth-empty':p['owner_start_instant']='';i['owner_start_instant']='';w['process_owner_start_instant']=''
  elif name=='worker-birth-invalid':w['process_start_instant']='not-a-native-instant'
  elif name=='proof-schema-bool':p['schema_version']=True
  elif name=='worker-schema-bool':w['schema_version']=True
  p['workers']=[copy.deepcopy(w)]
  if name=='duplicate-worker':p['workers'].append(copy.deepcopy(w))
  task=out/'process-exit-records'/('test-task-'+TASK+'.json');owner=td/'owner-intent.json';record=td/('worker-'+str(w['pid'])+'.json')
  (out/'junit'/'TEST-neutral.xml').write_text('<testsuite name="CONTROL_ONLY" tests="'+str(tests)+'" failures="0" errors="0" skipped="'+str(skip)+'"/>\n')
  if name!='missing-proof':task.write_text(json.dumps(p)+'\n')
  if name!='missing-intent':owner.write_text(json.dumps(i)+'\n')
  if name!='missing-worker':
   actual=copy.deepcopy(w)
   if name=='worker-birth-file-mismatch':actual['process_start_instant']=identity['birth']
   elif name=='actual-worker-file-PID-float':actual['pid']=float(actual['pid'])
   elif name=='actual-worker-file-schema-bool':actual['schema_version']=True
   elif name=='actual-worker-file-owner-PID-float':actual['process_owner_pid']=float(actual['process_owner_pid'])
   record.write_text(json.dumps(actual)+'\n')
  if name=='worker-file-public':record.chmod(0o644)
  elif name=='worker-file-symlink':target=td/'other-private.json';record.rename(target);record.symlink_to(target)
  process=subprocess.run([sys.executable,str(ROOT/'e2e/verify-local-result.py'),str(out),str(status),cleanup,RUN],cwd=out,env={'PATH':os.environ['PATH'],'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True,timeout=10)
  value=json.loads((out/'result.json').read_text())
  expected='PASS' if name=='complete-control-metadata' else 'FAIL'
  records.append({'case':name,'expected':expected,'actual':value['verdict'],'exit':process.returncode,'native_task_proof':value['native_task_proof'],'control_outcome':'PASS' if value['verdict']==expected else 'FAIL'})
 assert not out.exists()
result={'scope':'CLI_METADATA_PRIVATE_FS_AND_OWN_NATIVE_PROCESS_ONLY_NOT_ACTUAL_GRADLE_OR_BACKEND','native_identity':identity,'native_child_exit_status':worker.returncode,'actual_own_native_child_absent':True,'controls':records,'own_FS_directories_absent':len(records),'real_Gradle_Kafka_Docker_Fury_API_business_calls':0}
(ROOT/'additional-tuple-controls.json').write_text(json.dumps(result,indent=2)+'\n')
for r in records:print(json.dumps(r))
