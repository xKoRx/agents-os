---
type: change_log
schema_version: 1
scope: session
created: "2026-09-12"
updated: "2026-09-12"
area: "[[Echo]]"
project: "[[Echo — E-02 Control Safety, Auth and Journal Recovery]]"
application: "[[Echo — Live Platform V1]]"
entities:
  - "[[Echo — E-02 Control Safety, Auth and Journal Recovery]]"
related:
  - "[[Echo — Live Platform V1]]"
aliases: []
confidence: verified
source_session: "2026-09-12 manager park E-02 physical gates for MCP rollout"
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo E-02 physical gates parked during MCP rollout

## Cambio

- **Tipo:** state / dependency-management
- E-02 source-review head remains `xKoRx/echo` `feature/e02-control-safety-journal-recovery` @ `f7ddea18`.
- Source/contract corrections are complete enough to park implementation work; E-02 is **not CLOSED**, **not verifier-ready**, and is intentionally held at `PHYSICAL_PARTIAL` while Aranea MCP access is completed.

## Pending certification authority

Retomar antes de Independent Verifier:

1. **PostgreSQL 17 real** — migration 062 up/down/up, quarantine repository, duplicate/conflict/CLOSE-before-OPEN, outage/recovery and replay-facts against real PG.
2. **Hasura develop physical** — apply E-02 metadata, auth hook JSON session variables, READ/CONFIG positive cases, CONTROL/webhook negative cases, readonly/config_operator permission matrix. `aranea-hasura-dev-rw` is now available; `aranea-hasura-prod-ro` remains observation-only.
3. **Kafka real** — demonstrate required `PublishSync` paths and evidence that journal retry/replay-facts emits zero commands.
4. **Flink/StateFun develop physical** — kill/restart pre/post journal persistence, redelivery without fact loss or duplicate durable journal effects.
5. **Final source/regression drift check** after physical gates.
6. Then: Independent Verifier → controlled integration → E-02 DONE → E-06 unlock.

## Scheduling decision

- Kafka/Flink MCP installation is **not a prerequisite to continue the Echo roadmap**. Their absence blocks only E-02 physical certification/closure.
- E-05 Analytics Convergence A0 may proceed in parallel because its roadmap dependency is E-01/S0, not E-02 physical certification.
- Do not reopen E-02 source while parked unless a physical gate exposes a material defect.

## Guardrails

- No mock may substitute a physical PASS.
- No production write via Hasura; PROD surface is RO.
- DEV writes are allowed only for the exact E-02 certification actions when resumed.
- No verifier or master integration until all required physical gates are PASS.
