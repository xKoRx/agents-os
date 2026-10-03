# CP-SCOPE-1 author handoff

Frozen files: `e2e/sandbox.py` and `e2e/tests/sandbox-contract.py` only. See `freeze.sha256`, `freeze.json`, `two-files.patch`, and durable before backups.

CP provisioning uses `up --scope cp --cp-service <own-cp-alias>` and only the CP application/alias. Ecosystem remains the default with both applications/results+locks; receipts without scope remain ecosystem. Verification binds optional `--scope` exactly, rejects inherited PM exports and out-of-scope resources/segments/mutations, and requires fresh generated configuration. `down` uses receipt scope, permits partial own creation, and retains unresolved UNKNOWN/cleanup failures.

10 previous controls unchanged in AST; 15 new scope controls. Original baseline 10 PASS, two meaningful new controls RED against original helper, private candidate and exact published source 25 PASS. Syntax two files/help/diff check PASS. All controls use explicit metadata/API-shape simulation; no business output was created. First HTTP201 baseline refinement log preserved separately.

No remote API, Docker, Gradle, or commit. Physical CP/KVS suite remains NOT_EXECUTED; known external clone403 remains. Root owns build/run/CI/README integration. Independent Fault peer required before acceptance; no self-certification of business or cleanup runtime.
