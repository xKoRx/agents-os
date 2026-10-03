#!/usr/bin/env bash
set -euo pipefail
umask 077
readonly SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly ROOT="$(cd -- "${SCRIPT_DIR}/.." && pwd)"
readonly COMPONENT="${1:-all}"
case "${COMPONENT}" in all|journey|gcp|bigqueue) ;; *) echo MANAGED_INVALID_COMPONENT >&2; exit 2;; esac
: "${E2E_MANAGED_ENV_FILE:?MANAGED_PRIVATE_CONFIG_REQUIRED}"
managed_exports="$(python3 - "${E2E_MANAGED_ENV_FILE}" <<'PYCONFIG'
from pathlib import Path
import re,stat,sys
path=Path(sys.argv[1])
if stat.S_IMODE(path.stat().st_mode)&0o077: raise SystemExit('MANAGED_FILE_MUST_BE_MODE_0600')
seen=set()
for raw in path.read_text().splitlines():
 if not raw.strip() or raw.lstrip().startswith('#'): continue
 name,separator,value=raw.partition('=');name=name.strip()
 if not separator or not (re.fullmatch(r'E2E_MANAGED_[A-Z0-9_]+',name) or re.fullmatch(r'BIGQUEUE_TOPIC_[A-Z0-9_]+',name) or name=='E2E_FURY_PYTHON'):
  raise SystemExit('MANAGED_INVALID_CONFIG_EXPORT')
 if name in seen: raise SystemExit('MANAGED_DUPLICATE_CONFIG_EXPORT')
 seen.add(name); value=value.strip()
 if any(ord(char)<32 or ord(char)==127 for char in value): raise SystemExit('MANAGED_INVALID_CONFIG_EXPORT')
 if value.startswith(('"',"'")):
  if len(value)<2 or value[-1]!=value[0]: raise SystemExit('MANAGED_INVALID_CONFIG_EXPORT')
  value=value[1:-1]
 print(name+'='+value)
PYCONFIG
)"
while IFS= read -r export_line; do [[ -n "${export_line}" ]] && export "${export_line}"; done <<<"${managed_exports}"
unset managed_exports export_line
: "${E2E_MANAGED_SCOPE:?MANAGED_EXPLICIT_NONPROD_SCOPE_REQUIRED}"
: "${E2E_MANAGED_RUN_ID:?MANAGED_RUN_ID_REQUIRED}"
if [[ ! "${E2E_MANAGED_RUN_ID}" =~ ^[a-z0-9][a-z0-9_-]{7,63}$ ]]; then echo MANAGED_INVALID_RUN_ID >&2; exit 2; fi
if [[ ! "${E2E_MANAGED_SCOPE}" =~ (test|nonprod) || "${E2E_MANAGED_SCOPE}" =~ (^|[-_])(prod|production|stage|staging|stg)([-_]|$) ]]; then
  echo MANAGED_EXPLICIT_NONPROD_SCOPE_REQUIRED >&2; exit 2
fi
if [[ "${COMPONENT}" == all || "${COMPONENT}" == journey ]]; then
  : "${E2E_KVS_ENV_FILE:?MANAGED_OWNED_SANDBOX_CONFIG_REQUIRED}"
  sandbox_exports="$(python3 - "${E2E_KVS_ENV_FILE}" <<'PYSANDBOX'
import os,re,stat,sys
from pathlib import Path
path=Path(sys.argv[1])
if stat.S_IMODE(path.stat().st_mode)&0o077: raise SystemExit('MANAGED_KVS_FILE_MUST_BE_MODE_0600')
allowed={'E2E_KVS_CONTAINER_NAME','E2E_KVS_SEGMENT_ID','E2E_PLAYMAKER_ACTION_RESULTS_CONTAINER','E2E_PLAYMAKER_ACTION_LOCKS_CONTAINER','E2E_PLAYMAKER_KVS_SEGMENT_ID','E2E_PLAYMAKER_SANDBOX_BC','E2E_PLAYMAKER_SANDBOX_INSTANCE','E2E_SANDBOX_BC','E2E_SANDBOX_INSTANCE','E2E_RUN_ID','E2E_KVS_EXCLUSIVE_RUN_ID','E2E_KVS_SANDBOX_PROVENANCE'}
seen=set()
for raw in path.read_text().splitlines():
 if not raw.strip() or raw.lstrip().startswith('#'): continue
 name,separator,value=raw.partition('=');name=name.strip();value=value.strip()
 if not separator or not(re.fullmatch(r'KEY_VALUE_STORE_[A-Z0-9_]+',name) or name in allowed): raise SystemExit('MANAGED_INVALID_SANDBOX_EXPORT')
 if name in seen: raise SystemExit('MANAGED_DUPLICATE_SANDBOX_EXPORT')
 seen.add(name)
 if any(ord(char)<32 or ord(char)==127 for char in value): raise SystemExit('MANAGED_INVALID_SANDBOX_EXPORT')
 if value.startswith(('"',"'")):
  if len(value)<2 or value[-1]!=value[0]: raise SystemExit('MANAGED_INVALID_SANDBOX_EXPORT')
  value=value[1:-1]
 if name=='E2E_RUN_ID' and os.environ.get(name) not in (None,'',value): raise SystemExit('MANAGED_SANDBOX_RUN_ID_MISMATCH')
 print(name+'='+value)
PYSANDBOX
)"
  while IFS= read -r export_line; do [[ -n "${export_line}" ]] && export "${export_line}"; done <<<"${sandbox_exports}"
  unset sandbox_exports export_line
  : "${E2E_RUN_ID:?MANAGED_SANDBOX_RUN_ID_REQUIRED}"
  : "${E2E_KVS_EXCLUSIVE_RUN_ID:?MANAGED_EXCLUSIVE_SANDBOX_REQUIRED}"
  [[ "${E2E_MANAGED_RUN_ID}" == "${E2E_RUN_ID}" && "${E2E_RUN_ID}" == "${E2E_KVS_EXCLUSIVE_RUN_ID}" ]] || { echo MANAGED_RUN_SANDBOX_OWNERSHIP_MISMATCH >&2; exit 2; }
  : "${E2E_KVS_SANDBOX_PROVENANCE:?MANAGED_SANDBOX_PROVENANCE_REQUIRED}"
  : "${E2E_FURY_PYTHON:?MANAGED_AUTHENTICATED_FURY_PYTHON_REQUIRED}"
  "${E2E_FURY_PYTHON}" "${SCRIPT_DIR}/sandbox.py" verify --directory "$(dirname -- "${E2E_KVS_SANDBOX_PROVENANCE}")" --scope ecosystem
fi
export SCOPE="${E2E_MANAGED_SCOPE}" SCOPE_SUFFIX="${E2E_MANAGED_SCOPE}"
case "${COMPONENT}" in gcp) test_task=managedGcpOAuthTest;; bigqueue) test_task=managedBigQueueTest;; journey) test_task=managedControlplaneJourneyTest;; all) test_task=managedIntegrationTest;; esac
raw_evidence_dir="${E2E_EVIDENCE_DIR:-${ROOT}/build/managed-e2e/${E2E_MANAGED_RUN_ID}/${COMPONENT}}"
mkdir -m 700 -p "${raw_evidence_dir}"
readonly EVIDENCE_DIR="$(python3 -c 'from pathlib import Path; import sys; print(Path(sys.argv[1]).resolve(strict=True))' "${raw_evidence_dir}")"
unset raw_evidence_dir
export E2E_RECONCILIATION_DIR="${E2E_RECONCILIATION_DIR:-${EVIDENCE_DIR}/retained-work}"
mkdir -m 700 -p "${E2E_RECONCILIATION_DIR}"
if ! python3 "${SCRIPT_DIR}/reconciliation-status.py" "${E2E_RECONCILIATION_DIR}"; then
  echo "MANAGED_RETAINED_WORK_RECONCILIATION_REQUIRED:${E2E_RECONCILIATION_DIR}" >&2
  exit 2
fi
readonly PRIVATE_DIR="$(mktemp -d "${TMPDIR:-/tmp}/rio-managed-e2e.XXXXXX")"
publish_and_cleanup() {
  local original="$?"
  python3 "${SCRIPT_DIR}/sanitize-evidence.py" "${ROOT}/build/test-results/${test_task}" "${EVIDENCE_DIR}/junit" || original=1
  # A launcher receipt cannot certify future provider deletion. The registry remains hard-closed.
  printf 'PROVIDER_MUTATION_AND_CLEANUP_NOT_CERTIFIED\n' >"${EVIDENCE_DIR}/mutation-status.txt" || original=1
  if ! python3 "${SCRIPT_DIR}/reconciliation-status.py" "${E2E_RECONCILIATION_DIR}"; then
    echo "MANAGED_RETAINED_IN_FLIGHT_WORK:${PRIVATE_DIR}" >&2; original=1
    printf 'RECONCILIATION_REQUIRED:%s\n' "${PRIVATE_DIR}" >"${EVIDENCE_DIR}/retained-runtime.txt" || original=1
  elif ! rm -rf -- "${PRIVATE_DIR}"; then
    echo "MANAGED_PRIVATE_CLEANUP_FAILED:${PRIVATE_DIR}" >&2; original=1
  fi
  echo "TEST_EVIDENCE_PUBLISHED:${EVIDENCE_DIR}"
  return "${original}"
}
on_managed_exit() { local original="$?"; trap - EXIT; publish_and_cleanup || original=1; exit "${original}"; }
trap on_managed_exit EXIT
# Toolkit SCP has precedence over env: the journey must receive a new empty normal watcher root.
export ARTIFACT_DELIVERY_FILE_PREFIX="${PRIVATE_DIR}/artifacts"
mkdir -m 700 "${ARTIFACT_DELIVERY_FILE_PREFIX}"
printf 'run_id=%s\ncp_sha=%s\nscope=%s\ncomponent=%s\n' "${E2E_MANAGED_RUN_ID}" "$(git -C "${ROOT}" rev-parse HEAD)" "${E2E_MANAGED_SCOPE}" "${COMPONENT}" >"${EVIDENCE_DIR}/ledger.txt"
cd "${ROOT}"
rm -rf -- "${ROOT}/build/test-results/${test_task}"
if ! ./gradlew --no-daemon "${test_task}" --console=plain >"${PRIVATE_DIR}/managed.log" 2>&1; then
  python3 - "${PRIVATE_DIR}/managed.log" <<'PYDIAGNOSTIC'
from pathlib import Path
import re,sys
codes=re.findall(r'MANAGED_[A-Z0-9_:]+|SANDBOX_GATE_FAILED:[A-Za-z0-9_:]+',Path(sys.argv[1]).read_text(errors='replace'))
for code in list(dict.fromkeys(codes))[:5]: print(code,file=sys.stderr)
PYDIAGNOSTIC
  echo "MANAGED_GATE_FAILED:${COMPONENT}: check required capabilities and verified provider lifecycle" >&2
  exit 1
fi
