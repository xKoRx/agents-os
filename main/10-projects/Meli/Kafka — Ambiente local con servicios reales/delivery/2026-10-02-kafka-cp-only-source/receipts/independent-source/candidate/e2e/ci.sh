#!/usr/bin/env bash
set -euo pipefail
umask 077
readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
raw_ci_directory="$(mktemp -d "${TMPDIR:-/tmp}/rio-ci-job.XXXXXX")"
readonly CI_PRIVATE_DIR="$(python3 -c 'from pathlib import Path; import sys; print(Path(sys.argv[1]).resolve(strict=True))' "${raw_ci_directory}")"
unset raw_ci_directory
readonly CI_JOB_ID="${GITHUB_RUN_ID:-local}_$(python3 -c 'import os,uuid; print(os.environ.get("GITHUB_RUN_ATTEMPT",uuid.uuid4().hex))')"
readonly CP_SHA="$(git -C "${ROOT}" rev-parse HEAD)"
readonly PUBLIC_DIR="${ROOT}/build/ci-e2e-public"
overall=0
control_status=0

clear_family_runtime() {
  local variable
  while IFS= read -r variable; do
    case "${variable}" in
      E2E_FURY_PYTHON|E2E_CP_KVS_SERVICE|E2E_PM_RESULTS_KVS_SERVICE|E2E_PM_LOCKS_KVS_SERVICE|\
      E2E_PLAYMAKER_CANONICAL_REPO|E2E_PLAYMAKER_CANDIDATE_REPO|E2E_PLAYMAKER_ENV_FILE|\
      E2E_ENTITY_SERVICE_BASE_URL|E2E_ENTITY_SERVICE_TEMPLATE_RECEIPT_FILE|\
      E2E_PLAYMAKER_DENIED_IDENTITY_TEMPLATE_FILE|E2E_MANAGED_ENV_FILE|E2E_MANAGED_KVS_ENV_FILE) ;;
      E2E_*|KEY_VALUE_STORE_*|BIGQUEUE_TOPIC_*) unset "${variable}" ;;
    esac
  done < <(compgen -e)
  unset ARTIFACT_DELIVERY_FILE_PREFIX SCOPE SCOPE_SUFFIX
}

require_inputs() {
  local variable missing=""
  for variable in "$@"; do
    [[ -n "${!variable:-}" ]] || missing+="${variable},"
  done
  if [[ -n "${missing}" ]]; then
    echo "CI_GATE_BLOCKED:${family_name}:MISSING:${missing%,}" >&2
    return 2
  fi
}

write_gate() {
  python3 - "${family_dir}/gate.json" "${family_name}" "$1" "${family_run:-}" "${family_cleanup_status:-}" <<'PYGATE'
import json,os,sys
from pathlib import Path
path=Path(sys.argv[1])
value={'schema_version':1,'family':sys.argv[2],'exit_status':int(sys.argv[3]),
       'run_id':sys.argv[4] or None,'sandbox_cleanup_status':int(sys.argv[5]) if sys.argv[5] else None}
with path.open('x') as output:
    json.dump(value,output,indent=2);output.write('\n');output.flush();os.fsync(output.fileno())
PYGATE
}

cleanup_owned_sandbox() {
  local status=0
  if [[ -f "${sandbox_dir}/state.json" ]]; then
    if ! python3 "${SCRIPT_DIR}/reconciliation-status.py" "${E2E_RECONCILIATION_DIR}" >"${family_dir}/reconciliation-final.log" 2>&1; then
      status=1
    elif [[ "${launcher_attempted}" == true ]]; then
      # Any failed/unknown launcher is retained even if it left no visible intent marker.
      if [[ "${launcher_status}" != 0 ]] || [[ ! -f "${EVIDENCE_DIR}/cleanup.txt" ]] \
          || [[ "$(cat "${EVIDENCE_DIR}/cleanup.txt")" != "CLEANUP_CERTIFIED:rio-kafka-e2e-${family_run}" ]]; then
        status=1
      elif ! python3 "${SCRIPT_DIR}/kvs-mutation-proof.py" all-final \
          --directory "${EVIDENCE_DIR}/kvs-observation" --run "${family_run}" \
          --process-exits "${EVIDENCE_DIR}/process-exits.json" >"${family_dir}/ci-final-proof.json" 2>"${family_dir}/ci-final-proof.log"; then
        status=1
      fi
    fi
    if [[ "${status}" == 0 ]]; then
      "${E2E_FURY_PYTHON}" "${SCRIPT_DIR}/sandbox.py" down --directory "${sandbox_dir}" \
        >"${family_dir}/sandbox-down.log" 2>&1 || status=1
    fi
  fi
  if [[ ! -f "${sandbox_dir}/state.json" ]]; then
    if [[ "${sandbox_attempted}" == true ]]; then status=1;
    else printf 'NOT_ATTEMPTED\n' >"${family_dir}/sandbox-cleanup.status"; return 0; fi
  fi
  printf '%s\n' "${status}" >"${family_dir}/sandbox-cleanup.status" || status=1
  family_cleanup_status="${status}"
  [[ "${status}" == 0 ]] || echo "CI_SANDBOX_RETAINED:${family_name}" >&2
  return "${status}"
}

run_local_family() (
  local family_name="$1" task="$2" family_dir="${CI_PRIVATE_DIR}/$1" family_run=""
  local sandbox_dir="${family_dir}/sandbox" sandbox_attempted=false launcher_attempted=false launcher_status=2 family_cleanup_status=""
  local status=0
  clear_family_runtime
  mkdir -m 700 "${family_dir}" "${sandbox_dir}" "${family_dir}/temporary" "${family_dir}/evidence" "${family_dir}/reconciliation" || exit 2
  export TMPDIR="${family_dir}/temporary"
  export E2E_RECONCILIATION_DIR="${family_dir}/reconciliation"
  export E2E_EVIDENCE_DIR="${family_dir}/evidence"
  readonly EVIDENCE_DIR="${E2E_EVIDENCE_DIR}"
  finish_local_family() {
    local original="$?"
    trap - EXIT
    cleanup_owned_sandbox || original=1
    write_gate "${original}" || original=1
    exit "${original}"
  }
  trap finish_local_family EXIT
  require_inputs JAVA_HOME DOCKER_CONTEXT E2E_FURY_PYTHON E2E_CP_KVS_SERVICE || exit 2
  if [[ "${task}" != realIntegrationTest ]]; then
    require_inputs E2E_PM_RESULTS_KVS_SERVICE E2E_PM_LOCKS_KVS_SERVICE E2E_PLAYMAKER_ENV_FILE E2E_ENTITY_SERVICE_BASE_URL E2E_ENTITY_SERVICE_TEMPLATE_RECEIPT_FILE \
      E2E_PLAYMAKER_DENIED_IDENTITY_TEMPLATE_FILE || exit 2
    local checkout_variable=E2E_PLAYMAKER_CANONICAL_REPO
    [[ "${task}" != e2eCandidatePlaymakerTest ]] || checkout_variable=E2E_PLAYMAKER_CANDIDATE_REPO
    require_inputs "${checkout_variable}" || exit 2
    for private_file in "${E2E_PLAYMAKER_ENV_FILE}" "${E2E_ENTITY_SERVICE_TEMPLATE_RECEIPT_FILE}" "${E2E_PLAYMAKER_DENIED_IDENTITY_TEMPLATE_FILE}"; do
      [[ -f "${private_file}" && ! -L "${private_file}" ]] || exit 2
    done
  fi
  sandbox_attempted=true
  local sandbox_args=(up --scope cp --directory "${sandbox_dir}" --cp-service "${E2E_CP_KVS_SERVICE}")
  if [[ "${task}" != realIntegrationTest ]]; then
    sandbox_args=(up --scope ecosystem --directory "${sandbox_dir}" --cp-service "${E2E_CP_KVS_SERVICE}"
      --pm-results-service "${E2E_PM_RESULTS_KVS_SERVICE}" --pm-locks-service "${E2E_PM_LOCKS_KVS_SERVICE}")
  fi
  "${E2E_FURY_PYTHON}" "${SCRIPT_DIR}/sandbox.py" "${sandbox_args[@]}" >"${family_dir}/sandbox-up.log" 2>&1 || exit 2
  export E2E_KVS_ENV_FILE="${sandbox_dir}/sandbox.env"
  family_run="$(python3 "${SCRIPT_DIR}/bind-ci-family-inputs.py" read-run --file "${E2E_KVS_ENV_FILE}" --name E2E_RUN_ID)" || exit 2
  export E2E_RUN_ID="${family_run}"
  if [[ "${task}" != realIntegrationTest ]]; then
    mkdir -m 700 "${family_dir}/bindings" || exit 2
    python3 "${SCRIPT_DIR}/bind-ci-family-inputs.py" bind --run "${family_run}" --directory "${family_dir}/bindings" \
      --entity-template "${E2E_ENTITY_SERVICE_TEMPLATE_RECEIPT_FILE}" \
      --denied-template "${E2E_PLAYMAKER_DENIED_IDENTITY_TEMPLATE_FILE}" >"${family_dir}/bindings.log" 2>&1 || exit 2
    export E2E_ENTITY_SERVICE_RECEIPT_FILE="${family_dir}/bindings/entity-receipt.json"
    export E2E_PLAYMAKER_DENIED_IDENTITY_FILE="${family_dir}/bindings/denied-identity.json"
  fi
  launcher_attempted=true
  launcher_status=0
  "${SCRIPT_DIR}/run.sh" "${task}" >"${family_dir}/run.log" 2>&1 || launcher_status="$?"
  exit "${launcher_status}"
)

run_managed_family() (
  local family_name=managed-oauth-bigqueue family_dir="${CI_PRIVATE_DIR}/managed-oauth-bigqueue"
  local family_run="" family_cleanup_status=""
  clear_family_runtime
  mkdir -m 700 "${family_dir}" "${family_dir}/temporary" "${family_dir}/evidence" "${family_dir}/reconciliation" || exit 2
  export TMPDIR="${family_dir}/temporary" E2E_EVIDENCE_DIR="${family_dir}/evidence"
  export E2E_RECONCILIATION_DIR="${family_dir}/reconciliation"
  finish_managed_family() {
    local original="$?"
    trap - EXIT
    write_gate "${original}" || original=1
    exit "${original}"
  }
  trap finish_managed_family EXIT
  require_inputs JAVA_HOME E2E_FURY_PYTHON E2E_MANAGED_ENV_FILE E2E_MANAGED_KVS_ENV_FILE || exit 2
  family_run="$(python3 "${SCRIPT_DIR}/bind-ci-family-inputs.py" read-run --file "${E2E_MANAGED_ENV_FILE}" --name E2E_MANAGED_RUN_ID)" || exit 2
  local kvs_run
  kvs_run="$(python3 "${SCRIPT_DIR}/bind-ci-family-inputs.py" read-run --file "${E2E_MANAGED_KVS_ENV_FILE}" --name E2E_RUN_ID)" || exit 2
  [[ "${family_run}" == "${kvs_run}" ]] || exit 2
  python3 - "${CI_PRIVATE_DIR}" "${family_run}" <<'PYDISTINCT' || exit 2
import json,sys
from pathlib import Path
root=Path(sys.argv[1])
for name in ('cp-functional','playmaker-canonical','playmaker-candidate'):
    if json.loads((root/name/'gate.json').read_text()).get('run_id') == sys.argv[2]:
        raise SystemExit(2)
PYDISTINCT
  # Fixed managed inputs are never rebound or deleted by the local-family lifecycle.
  export E2E_KVS_ENV_FILE="${E2E_MANAGED_KVS_ENV_FILE}"
  "${SCRIPT_DIR}/managed.sh" all >"${family_dir}/run.log" 2>&1
)

record_sources() {
  python3 - "${CI_PRIVATE_DIR}/job.json" "${CI_JOB_ID}" "${CP_SHA}" "${control_status}" <<'PYJOB'
import json,os,re,subprocess,sys
from pathlib import Path
sources={'cp':sys.argv[3]}
for name,variable in [('playmaker-canonical','E2E_PLAYMAKER_CANONICAL_REPO'),('playmaker-candidate','E2E_PLAYMAKER_CANDIDATE_REPO')]:
    repo=os.environ.get(variable)
    if repo:
        probe=subprocess.run(['git','-C',repo,'rev-parse','HEAD'],capture_output=True,text=True)
        sha=probe.stdout.strip()
        if probe.returncode==0 and re.fullmatch('[a-f0-9]{40}',sha): sources[name]=sha
with Path(sys.argv[1]).open('x') as output:
    json.dump({'schema_version':1,'job_id':sys.argv[2],'sources':sources,'control_exit_status':int(sys.argv[4])},output,indent=2)
    output.write('\n');output.flush();os.fsync(output.fileno())
PYJOB
}

# Neutral controls are an additional required gate; they cannot certify backend business.
python3 "${SCRIPT_DIR}/tests/harness-contract.py" >"${CI_PRIVATE_DIR}/harness-control.log" 2>&1 || control_status="$?"
[[ "${control_status}" == 0 ]] || overall=1
for family in cp-functional playmaker-canonical playmaker-candidate managed-oauth-bigqueue; do
  gate_status=0
  case "${family}" in
    cp-functional) run_local_family "${family}" realIntegrationTest || gate_status="$?" ;;
    playmaker-canonical) run_local_family "${family}" e2eCanonicalPlaymakerTest || gate_status="$?" ;;
    playmaker-candidate) run_local_family "${family}" e2eCandidatePlaymakerTest || gate_status="$?" ;;
    managed-oauth-bigqueue) run_managed_family || gate_status="$?" ;;
  esac
  echo "CI_GATE_STATUS:${family}:${gate_status}"
  [[ "${gate_status}" == 0 ]] || overall=1
done
record_sources || overall=1
mkdir -p "${ROOT}/build"
python3 "${SCRIPT_DIR}/publish-ci-evidence.py" publish --job-directory "${CI_PRIVATE_DIR}" \
  --destination "${PUBLIC_DIR}" --job-id "${CI_JOB_ID}" --cp-sha "${CP_SHA}" || overall=1
# Private receipts/logs/resources are retained for reconciliation; this path is never an upload input.
exit "${overall}"
