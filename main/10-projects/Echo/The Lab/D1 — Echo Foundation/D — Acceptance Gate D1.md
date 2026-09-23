---
type: gate
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[A — Technical SPEC D1]]"
  - "[[C — Test Plan D1]]"
tags: [kind/gate, area/echo, the-lab, d1]
created: "2026-09-23"
updated: "2026-09-23"
---
# D — Acceptance Gate D1

## D1_PASS

D1 passes only when all are true:

1. Technical SPEC is implemented without unapproved semantic deviation.
2. Canonical operation/history migrations apply in isolated DEV/PG test.
3. Shared SDK exposes producer-agnostic versioned history contract.
4. Existing StrategyVersion authority is reused.
5. Existing canonical-symbol authority is reused.
6. History endpoint accepts a valid complete SQX+MT5 snapshot and persists it.
7. Persisted operation is exactly one closed trade / one row.
8. SL and TP are required.
9. Replay with identical history is no-op.
10. Valid changed PUT atomically replaces SQX+MT5.
11. Invalid operation rejects the complete request.
12. Forced mid-replacement failure preserves previous dataset.
13. REFERENCE rows are never touched by imported-history replacement.
14. Readback/range query works.
15. Unit + PG integration + HTTP/contract suites pass.
16. Relevant existing Echo regression tests pass or any superseded-contract test is explicitly classified without reinstating old architecture.
17. No PROD, journal mutation, activation, provisioning, capital or broker side effect.
18. Agents-OS implementation evidence and feedback are persisted.

Forge authentic integration is NOT a D1_PASS criterion.

## D1_BLOCKED

Only valid when a frozen SPEC invariant is impossible due to a concrete current Echo authority contradiction that the developer cannot solve without changing M01-M12.

A blocker MUST include:
- exact file/table/constraint;
- reproducer;
- why an implementation-level workaround is unsafe;
- smallest proposed decision change.

External Forge readiness is not D1_BLOCKED.

## D1_FAIL

Any of:
- partial history commit;
- second durable trade authority;
- TradeSet dual-write;
- accepting missing required trade data;
- accepting noncanonical symbol;
- touching REFERENCE during import replace;
- changing product decisions without approval;
- tests skipped while claiming PASS;
- synthetic fixture described as authentic producer evidence;
- trading/PROD side effect.
