# CP-only E2E checkpoint — 2026-10-02

WORK_BRANCH_PENDING, source verification PASS; complete physical CP E2E NOT_EXECUTED/BLOCKED.
The owner prioritizes Kafka CP; ecosystem follows separately. This delta uses the same real CP
business, five owned Kafka brokers, production Toolkit Sandbox KVS and Kafka results.

`e2e/sandbox.py up --scope cp --cp-service <CP-own-alias>` provisions only CP resources.
The launcher and direct Gradle preflight require matching scope; ecosystem requires its own
receipt and services. Scope-less legacy receipts remain ecosystem. Required dependencies fail
explicitly, with no no-op KVS, business mock, file result or skip.

CP suite compilation PASS. Mandatory `validateRealE2eHarness` ran72 source/metadata controls
PASS:25 Sandbox,8 managed launcher,11 CI,5 cleanup,16 retention,7 filesystem. Independent source
review repeated baseline10/11 failures and the bare-variable1/1 failure, then candidate11/11 PASS;
both P2 findings closed,0 drift. Documentation delta independently PASS. These controls stop
before SDK/service business and do not certify E2E or an actual corporate CI job.

Immediate external gate: stored-auth read-only guard required Fury login on
2026-10-02T15:31:37Z, with0 network calls or exposed credentials. After interactive renewal,
recheck the own CP alias `triggers-status-nonprod`: previous authenticated clone returned403,
while both owned BCs were removed with DELETE200/GET404. No instance was allocated or KVS written.
The former403 is historical, not a current authenticated recheck.

After preparing the own Sandbox file, from this checkout:

```sh
E2E_KVS_ENV_FILE=/absolute/private/sandbox.env ./e2e/run.sh realIntegrationTest
```

See [runner instructions](../../../../e2e/README.md) for startup, prerequisites and cleanup.
Run the actual Toolkit server contract and full suite; independently repeat from a clean checkout.
Every complete capability remains NOT_EXECUTED. The wrapper CI dispatcher still aggregates four
families; its local controls do not establish a standalone CP-only corporate job.

[Machine receipt](cp-only-scope-checkpoint.json) pins sources, commands, outcomes and review hashes.
Raw neutral RED/GREEN receipts are retained in the separate CP-only supplement under the AGENTS OS
project delivery directory; the earlier blocked delivery bundle is historical and immutable.
