# CP-only documentation review

**CHANGES_REQUESTED: three consistency edits.** The CP-only command and execution status are documented without claiming production, full E2E, actual KVS or CI job success. Both dirty document hashes match the supplied update plan. This review ran no commands against SDK, APIs, Docker or Gradle and edited no repository files.

1. CP `meli/features/20261001-real-e2e/3-tasks/tasks.md:77` still says the blocker is clone403. Current evidence is login required at `2026-10-02T15:31:37Z`, with zero network calls. State login renewal, then actual clone recheck; permission remediation applies only if403 repeats.
2. KL `docs/04-troubleshooting/kafka-real-e2e.md:99` says the351-row checkpoint still has ten PM NONE. That is the historicaleee5b909 cut. The new3bea cut already states304FULL/29PARTIAL/18NONE and seven FULL/three PARTIAL frontier preparation. Label the old count historical or use the current preparation, keeping every capability NOT_EXECUTED.
3. KL same file`:116` unconditionally asks enabling clone403 and renewing Spellbook. Separate the immediate CP login/recheck path from formal review and later ecosystem identity/runner actions.

The CP command uses `sandbox.py up --scope cp --cp-service <own alias>`, then its private `sandbox.env` and `run.sh realIntegrationTest`. Later ecosystem families explicitly require a fresh ecosystem receipt and aliases. Scope capture receipts agree with that split; their neutral verifier exits are not suite executions. The72-count receipt matches25+8+11+5+16+7 and is source/metadata-only; the CP compile receipt is compile-only. This review inspected those receipts and did not reproduce their controls.

Sandbox2/CI source review remains a separate pending peer. Actual CP business and KVS allocation remain NOT_EXECUTED. Detailed pinned input/evidence hashes are in [review.json](review.json).
