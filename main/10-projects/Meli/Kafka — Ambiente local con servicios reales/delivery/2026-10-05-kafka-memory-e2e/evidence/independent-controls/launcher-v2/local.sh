#!/usr/bin/env bash
# CP local functional E2E: actual Kafka, per-process map, no Fury Sandbox.
set -euo pipefail
umask 077
readonly ROOT="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "${ROOT}"
for dependency in docker python3 java rg; do
  command -v "${dependency}" >/dev/null || { echo "LOCAL_E2E_COMMAND_REQUIRED:${dependency}" >&2; exit 2; }
done
: "${DOCKER_CONTEXT:?LOCAL_E2E_EXPLICIT_DOCKER_CONTEXT_REQUIRED}"
export E2E_RUN_ID="$(python3 -c 'import uuid; print(uuid.uuid4().hex)')"
export SCOPE=local SCOPE_SUFFIX=local
export E2E_COMPOSE_PROJECT="rio-kafka-memory-${E2E_RUN_ID}"
export E2E_COMPOSE_FILE="${ROOT}/e2e/compose.yaml"
export E2E_EVIDENCE_DIR="${ROOT}/build/local-e2e/${E2E_RUN_ID}"
mkdir -m 700 -p "${E2E_EVIDENCE_DIR}"
export E2E_RECONCILIATION_DIR="${E2E_EVIDENCE_DIR}/retained-work"
export E2E_TEST_WORKER_DIR="${E2E_EVIDENCE_DIR}/test-workers"
export E2E_PROCESS_EXIT_DIR="${E2E_EVIDENCE_DIR}/process-exit-records"
mkdir -m 700 "${E2E_RECONCILIATION_DIR}" "${E2E_TEST_WORKER_DIR}" "${E2E_PROCESS_EXIT_DIR}"
export E2E_ENV_FILE="${E2E_EVIDENCE_DIR}/compose.env"
export E2E_KRAFT_CLUSTER_ID="$(python3 -c 'import uuid,base64; print(base64.urlsafe_b64encode(uuid.uuid4().bytes).decode().rstrip("="))')"
base_port="${E2E_KAFKA_BASE_PORT:-39092}"
python3 - "${base_port}" <<'PY'
import socket,sys
base=int(sys.argv[1])
if not 1024<=base<=65531: raise SystemExit('LOCAL_E2E_INVALID_PORTS')
for port in range(base,base+5):
 with socket.socket() as probe:
  try: probe.bind(('127.0.0.1',port))
  except OSError: raise SystemExit('LOCAL_E2E_OWNED_PORT_UNAVAILABLE')
PY
for broker in 1 2 3 4 5; do
  port=$((base_port + broker - 1))
  export "E2E_KAFKA_PORT_${broker}=${port}"
  printf 'E2E_KAFKA_PORT_%s=%s\n' "${broker}" "${port}" >>"${E2E_ENV_FILE}"
done
export E2E_BOOTSTRAP_SERVERS="127.0.0.1:${base_port}"
export E2E_KAFKA_BROKER_CONTAINER_PREFIX="${E2E_COMPOSE_PROJECT}-broker"
architecture="$(docker info --format '{{.Architecture}}')"
if [[ "${architecture}" == aarch64 || "${architecture}" == arm64 ]]; then export E2E_JAVA_TOOL_OPTIONS=-XX:UseSVE=0; fi
[[ "$(docker info --format '{{.MemTotal}}')" -ge 5368709120 ]] || { echo LOCAL_E2E_DOCKER_5GIB_REQUIRED >&2; exit 2; }
printf 'E2E_RUN_ID=%s\nE2E_KRAFT_CLUSTER_ID=%s\nE2E_JAVA_TOOL_OPTIONS=%s\n' "${E2E_RUN_ID}" "${E2E_KRAFT_CLUSTER_ID}" "${E2E_JAVA_TOOL_OPTIONS:-}" >>"${E2E_ENV_FILE}"
for kind in DEPLOYMENT_RESULT ACTION_RESULT DEPLOYMENT_TRIGGER ACTION_TRIGGER DEPLOYMENT_RESULT_DLT ACTION_RESULT_DLT; do
  lower="$(printf '%s' "${kind}" | tr '[:upper:]' '[:lower:]')"
  export "E2E_${kind}_TOPIC=e2e_${E2E_RUN_ID}_${lower}"
done
python3 - "${E2E_EVIDENCE_DIR}/cloud-provider.json" "${E2E_BOOTSTRAP_SERVERS}" <<'PY'
import json,sys
from pathlib import Path
Path(sys.argv[1]).write_text(json.dumps({'cloud_provider':{'gcp':{'segmentation':{'legacy':{'clusters':[{'key':'e2e-gcp-default','component_template_code':'gcp-kafka-topic','bootstrap_servers':sys.argv[2],'teams':['all']}]}}}}}))
PY
export CLOUD_PROVIDER_CONFIG_LOCATION="file:${E2E_EVIDENCE_DIR}/cloud-provider.json"
# Source hashes include untracked candidate files, without reading credentials/caches.
python3 - "${ROOT}" "${E2E_EVIDENCE_DIR}/source.json" <<'PY'
import hashlib,json,subprocess,sys
from pathlib import Path
root=Path(sys.argv[1]); entries={}
for raw in subprocess.check_output(['git','ls-files','-z','--cached','--others','--exclude-standard'],cwd=root).split(b'\0'):
 if raw:
  name=raw.decode(); path=root/name
  if path.is_file(): entries[name]=hashlib.sha256(path.read_bytes()).hexdigest()
Path(sys.argv[2]).write_text(json.dumps({'commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip(),'files':entries},sort_keys=True,indent=2)+'\n')
PY
compose() { docker compose --project-name "${E2E_COMPOSE_PROJECT}" --env-file "${E2E_ENV_FILE}" --file "${E2E_COMPOSE_FILE}" "$@"; }
started=false
cleanup() {
  local status="$?" cleanup_status=PASS resource retained=false
  trap - EXIT
  if ! python3 "${ROOT}/e2e/reconciliation-status.py" "${E2E_RECONCILIATION_DIR}" >"${E2E_EVIDENCE_DIR}/reconciliation.txt" 2>&1; then
    status=1; cleanup_status=RETAINED; retained=true
  fi
  if [[ "${started}" == true && "${retained}" == false ]]; then
    compose logs --no-color --tail 100 >"${E2E_EVIDENCE_DIR}/broker.log" 2>&1 || status=1
    compose down --volumes --remove-orphans >"${E2E_EVIDENCE_DIR}/cleanup.log" 2>&1 || { status=1; cleanup_status=FAIL; }
    for resource in container network volume; do
      if [[ "${resource}" == container ]]; then
        leftovers="$(docker ps --all --quiet --filter "label=com.docker.compose.project=${E2E_COMPOSE_PROJECT}")" || { status=1; cleanup_status=FAIL; }
      else
        leftovers="$(docker "${resource}" ls --quiet --filter "label=com.docker.compose.project=${E2E_COMPOSE_PROJECT}")" || { status=1; cleanup_status=FAIL; }
      fi
      [[ -z "${leftovers}" ]] || { status=1; cleanup_status=FAIL; }
    done
  fi
  if python3 - "${E2E_EVIDENCE_DIR}" "${status}" "${cleanup_status}" "${E2E_RUN_ID}" <<'PY'
import json,sys,xml.etree.ElementTree as ET
from pathlib import Path
out=Path(sys.argv[1]); totals=dict(tests=0,failures=0,errors=0,skipped=0)
for report in (out/'junit').glob('TEST-*.xml'):
 node=ET.parse(report).getroot()
 for key in totals: totals[key]+=int(node.get(key,0))
status=int(sys.argv[2]); proof_valid=False
try:
 proof=json.loads((out/'process-exit-records'/'test-task-localKafkaE2eTest.json').read_text())
 proof_valid=(proof.get('kind')=='ACTUAL_GRADLE_TEST_TASK_COMPLETION' and proof.get('run_id')==sys.argv[4]
  and proof.get('task')=='localKafkaE2eTest' and proof.get('task_outcome')=='SUCCESS_WITH_WORKERS_REAPED_NORMAL_EXIT'
  and proof.get('test_count')==totals['tests'] and proof.get('failed_count')==0 and proof.get('skipped_count')==0
  and bool(proof.get('workers')) and all(w.get('run_id')==sys.argv[4] and w.get('task')=='localKafkaE2eTest' for w in proof['workers']))
except (OSError,ValueError,KeyError,TypeError): pass
verdict='PASS' if status==0 and sys.argv[3]=='PASS' and proof_valid and totals['tests']>0 and not any(totals[k] for k in ('failures','errors','skipped')) else 'FAIL' 
(out/'result.json').write_text(json.dumps(dict(run_id=sys.argv[4],family='CP_LOCAL_KAFKA_MEMORY',backend='PER_INSTANCE_MEMORY',verdict=verdict,command_exit=status,cleanup=sys.argv[3],native_task_proof=proof_valid,totals=totals),indent=2)+'\n')
if verdict!='PASS': raise SystemExit(1)
PY
  then :; else status=1; fi
  echo "LOCAL_E2E_EVIDENCE:${E2E_EVIDENCE_DIR}"
  exit "${status}"
}
trap cleanup EXIT
started=true
compose up --detach --wait --wait-timeout 240 >"${E2E_EVIDENCE_DIR}/startup.log" 2>&1
# Docker health alone does not prove host connectivity (e.g. a broken Colima forwarder).
python3 - "${base_port}" <<'PYHOST'
import socket,sys,time
base=int(sys.argv[1]); deadline=time.monotonic()+30
while True:
 try:
  for port in range(base,base+5):
   with socket.create_connection(('127.0.0.1',port),1): pass
  break
 except OSError:
  if time.monotonic()>=deadline: raise SystemExit('LOCAL_E2E_HOST_KAFKA_PORTS_UNREACHABLE')
  time.sleep(.2)
PYHOST
compose exec --no-TTY broker1 /opt/kafka/bin/kafka-broker-api-versions.sh --bootstrap-server broker1:19092 >"${E2E_EVIDENCE_DIR}/readiness.txt"
[[ "$(rg -c 'id: [1-5] rack:' "${E2E_EVIDENCE_DIR}/readiness.txt")" == 5 ]] || { echo LOCAL_E2E_FIVE_BROKERS_REQUIRED >&2; exit 1; }
for kind in DEPLOYMENT_RESULT ACTION_RESULT DEPLOYMENT_TRIGGER ACTION_TRIGGER DEPLOYMENT_RESULT_DLT ACTION_RESULT_DLT; do
  topic_variable="E2E_${kind}_TOPIC"
  compose exec --no-TTY broker1 /opt/kafka/bin/kafka-topics.sh --bootstrap-server broker1:19092 --create --topic "${!topic_variable}" --partitions 3 --replication-factor 3 >>"${E2E_EVIDENCE_DIR}/topics.txt"
done
rm -rf -- build/test-results/localKafkaE2eTest
set +e
./gradlew --no-daemon --console=plain localKafkaE2eTest "$@" >"${E2E_EVIDENCE_DIR}/gradle.log" 2>&1
status="$?"
set -e
mkdir -p "${E2E_EVIDENCE_DIR}/junit"
python3 e2e/sanitize-evidence.py build/test-results/localKafkaE2eTest "${E2E_EVIDENCE_DIR}/junit" || status=1
exit "${status}"
