---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[A — Manager Freeze D4]]"
tags:
  - kind/doc
  - area/echo
  - the-lab
  - d4
created: "2026-09-25"
updated: "2026-09-25"
---

# B — Manager Review Shot 1 — D4

## Reviewed identities

```text
baseline master = 372af59a7b83604781346613da01e3d510ea1360
manager freeze  = 8c4a52266bbd615990fec4f2f5b8dbfc727b9b16
shot1 candidate = 2af4b21f9a06a8086f26fc54f229ebb12fba10b5
handoff commit  = be1fa0d786b7f91e4761429826f7be77899432bc
```

Independent GitHub compare confirms candidate is exactly one implementation commit ahead of the manager freeze.

## Accepted implementation direction

- Gateway history boundary mounted through real NewServer assembly.
- Durable currentness derived from strategy_history_state vs required default lab_curves.
- Automatic refresh remains inside existing lab-worker; no new infrastructure/schema.
- Recalculation reuses LabCurveService and D3 transaction/advisory-lock atomicity.
- SCHEDULED lab_job_runs observability extended with input/result digests.
- systemd --user DEV unit is consistent with the Environment Contract.
- Source metadata removal of explicit role admin is directionally correct.

## Manager decisions after handoff

### TEST_CHANGE_REQUEST

`APPROVED`.

Authorized exact edit only:

- `--triggered-by CLI` -> `--triggered-by MANUAL`
- expected TriggeredBy `CLI` -> `MANUAL`

Negative enum coverage remains in the new D4 test; do not duplicate it.

Approval was persisted in the repository TCR in a documentation-only post-candidate commit.

### Hasura MATERIAL_CONTRADICTION

`ACCEPTED AS REAL`.

Independent source inspection confirms versioned V3 metadata contains no event_triggers, object_relationships or array_relationships, while the Environment Contract §5.7 records operational DEV metadata with event triggers/relationships and a repaired Hasura→Gateway propagation flow.

Manager decision:

`OPTION 1 — BACK-PORT LIVE OPERATIONAL METADATA INTO VERSIONED SOURCE`.

Option 2 (permanent fused apply preserving live-only metadata) is rejected because it perpetuates configuration drift and contradicts the frozen D4 requirement that versioned source be reproducibly applicable.

Rules for back-port:

- Start from a fresh read-only export of current DEV metadata.
- Reconcile only operational objects belonging to existing Echo V3 tracked surfaces and certified DEV behavior.
- Preserve event triggers, GraphQL relationships, custom root fields and config_operator permissions required by current Echo Front/Gateway behavior.
- DO NOT commit secrets, bearer values, admin secret, DEV IPs or environment-specific credentials.
- Environment-specific trigger webhook/header values must use Hasura metadata environment-variable mechanisms (e.g. webhook/header from env) or an already-established equivalent source-safe mechanism.
- If the Hasura runtime cannot consume source-safe env indirection without an infrastructure mutation outside the Environment Contract, return the exact blocker; do not commit literals.
- Final physical gate is full `hasura metadata apply` from versioned source with no filtering, followed by consistency + account/config propagation smoke.
- Take/export a pre-apply metadata backup and preserve rollback path.

## Shot 1 manager verdict

`SHOT1_CANDIDATE_PASS` from the implementor is NOT accepted yet.

Reason:

1. G02 is not satisfied: complete versioned metadata was not physically applied, and source is known incomplete relative to certified DEV metadata.
2. The full lab-worker test suite remains red until the approved TCR edit is applied.

The functional auto-refresh E2E evidence is accepted as strong candidate evidence, not final certification.

Current manager posture:

```text
SOURCE          = PENDING
REMOTE_BASELINE = PASS
MAIN            = PENDING
DEV_PHYSICAL    = PENDING
AUTHENTIC_DATA  = PENDING
PROD            = PENDING
```

DEV_PHYSICAL remains PENDING globally despite the refresh path passing, because the frozen Hasura physical sub-gate is still unexecuted.

## Mandatory Shot 2 attack once Shot 1 is complete

Verifier must specifically probe a failure after curve publication but before/failing `lab_job_runs.FinishSucceeded`: current code commits analytical state before job-run finalization. Verify whether this can leave a RUNNING audit row while the version becomes CURRENT and therefore is never retried/finalized.

Also attack simultaneous refresh callers for duplicate unnecessary work; advisory locking protects correctness but currentness is evaluated before lock acquisition.

## Next exact

Continue the SAME Shot 1 context only for:
- approved TCR edit;
- source-authoritative Hasura reconciliation;
- full unfiltered DEV metadata apply + propagation smoke;
- rerun all gates;
- produce a replacement exact candidate SHA.

No other product changes are authorized.
