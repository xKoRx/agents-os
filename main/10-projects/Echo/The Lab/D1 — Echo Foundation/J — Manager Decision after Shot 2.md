---
type: manager-review
schema_version: 1
status: approved-for-correction
area: "[[Echo]]"
related:
  - "[[I — Independent Verification D1 (Shot 2)]]"
  - "[[D — Acceptance Gate D1]]"
  - "[[F — Continuity D1]]"
tags: [kind/review, area/echo, the-lab, d1]
created: "2026-09-23"
updated: "2026-09-23"
---
# J — Manager Decision after Shot 2

## Decision

Shot 2 evidence is accepted.

D1 remains **NOT PASS** until Shot 3 fixes and independently re-runs the gate.

Accepted findings:

### F-S2-01 — MEDIUM

`StrategyHistoryService.GetHistory` can return a torn read under concurrent replacement because history head and operations are read in separate statements without one consistent read snapshot.

Required correction:
- read head and operation rows within one read-only transaction using a snapshot level that guarantees both queries observe the same committed state;
- `REPEATABLE READ` is the preferred PostgreSQL implementation unless the repo offers an equivalent established abstraction;
- no write lock, no global/distributed lock, no redesign of replacement path.

Acceptance:
- Shot 2 reproducer reaches `torn_head_ops=0` under equivalent or stronger repeated concurrency.

### F-S2-02 — LOW

Gateway history GET serializes times with `time.RFC3339` and loses sub-second precision.

Required correction:
- project persisted operation/history timestamps with `time.RFC3339Nano`;
- this is a fidelity bug fix within `strategy-history.v1`, not a new product semantic or contract version, because the contract already defines RFC3339 instants and precision was not intentionally restricted to seconds.

Acceptance:
- sub-second persisted timestamps round-trip through GET without loss.

## Frozen scope

Shot 3 MUST NOT reopen:
- canonical operation model;
- digest recipes;
- decimal rules;
- migration 064 schema;
- replacement semantics;
- source/period rules;
- StrategyVersion or canonical-symbol authority;
- REFERENCE policy;
- endpoint purpose;
- Forge integration.

Only code/test changes necessary for the two accepted findings and final reconciliation are authorized.

## Final-gate requirement

Shot 3 must:
1. apply both fixes on top of implementation HEAD;
2. incorporate the relevant Shot 2 reproducers as permanent regression tests;
3. re-run all D1 critical tests plus affected regressions;
4. verify clean diff contains no unapproved behavior changes;
5. persist final implementation evidence and final gate decision in Agents-OS;
6. close the session.

D1_PASS may be declared only after Shot 3 evidence satisfies all 18 Acceptance Gate criteria with F-S2-01/F-S2-02 closed.
