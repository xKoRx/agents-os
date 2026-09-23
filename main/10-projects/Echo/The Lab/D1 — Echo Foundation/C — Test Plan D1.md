---
type: test-plan
schema_version: 1
status: approved-for-implementation
area: "[[Echo]]"
related:
  - "[[A — Technical SPEC D1]]"
  - "[[B — Implementation Plan D1]]"
tags: [kind/test, area/echo, the-lab, d1]
created: "2026-09-23"
updated: "2026-09-23"
---
# C — Test Plan D1

## Principle

D1 tests certify Echo capability, not Forge physical compatibility.

Synthetic fixtures are valid for unit/contract/PG integration. They MUST NOT be reported as authentic producer evidence.

## 1. Unit / contract

Required cases:

1. valid LONG closed trade.
2. valid SHORT closed trade.
3. missing each required field fails.
4. invalid/zero/negative entry, exit, SL, TP, volume fails.
5. LONG invalid geometry fails.
6. SHORT invalid geometry fails.
7. closed_at < opened_at fails; equality is accepted.
8. invalid decimal wire fails; no float JSON path.
9. currency malformed fails.
10. unsupported side/unit fails.
11. optional initial_risk_money omitted succeeds; zero/negative fails when supplied.
12. exact economics `net = gross + commission + swap`.
13. mismatched economics fails.
14. duplicate source_trade_id within training fails.
15. duplicate source_trade_id within pre_real fails.
16. same source_trade_id across SQX and MT5 is allowed.
17. training opened_at at/after A fails.
18. pre_real opened_at before A fails.
19. with B set, pre_real opened_at at/after B fails.
20. B absent allows pre_real after A.
21. deterministic record digest.
22. deterministic dataset digest independent of input ordering after canonical sort.
23. count mismatch fails.
24. dataset digest mismatch fails.
25. history digest changes for meaningful A/B/instrument/dataset change.

## 2. Strategy/symbol authority

26. existing StrategyVersion accepted.
27. unknown StrategyVersion -> not found.
28. known canonical instrument accepted.
29. unknown/noncanonical instrument rejected.
30. no new symbol/alias authority is created by history ingestion.

## 3. PostgreSQL integration

31. migrations up/down or repository-standard migration verification succeeds on isolated PG.
32. constraints reject invalid direct rows.
33. first history creates state + exact SQX/MT5 counts.
34. readback equals normalized contract fields.
35. unique StrategyVersion/source/source_trade_id enforced.
36. opened_at range query ordered and correct.
37. closed_at range query ordered and correct.
38. exact same history_digest replay -> zero row churn.
39. changed valid PUT replaces all SQX+MT5 imported rows.
40. replacement never deletes REFERENCE.
41. failure after delete but before complete insert rolls back old rows and old history state.
42. concurrent replacement is serialized/convergent; no mixed dataset.
43. no N-per-row external DB round-trip implementation for bulk load.

## 4. HTTP / application integration

44. first valid PUT -> 201 + HISTORY_READY.
45. exact replay -> 200 + UNCHANGED.
46. valid changed PUT -> 200 + REPLACED.
47. malformed wire -> 400.
48. missing version -> 404.
49. semantic dataset failure -> 422 with no mutation.
50. oversized request -> 413 according to configured limit.
51. DB unavailable -> 503/retryable using existing error contract.
52. auth missing/invalid rejected according to existing service-auth policy.
53. response digests/counts match persisted state.
54. no activation/provisioning/capital/journal write is triggered.

## 5. Regression

Run the relevant existing SDK/contracts, PostgreSQL, Gateway, E03/E04/E05 tests affected by compilation or imports.

A legacy test failing because it encodes a superseded E05 operation shape must not be blindly deleted. The developer must classify it:
- unrelated regression -> fix implementation;
- direct consumer of superseded S0 operation shape -> adapt to new version or document for cleanup without restoring dual authority.

## 6. Evidence to capture

- baseline and final commit;
- migration number/path;
- package/file list;
- test commands;
- pass/fail counts;
- PostgreSQL row counts for first/replay/replacement/rollback;
- one response example with secrets removed;
- proof REFERENCE untouched;
- proof no trading side effects;
- unresolved blockers.

No screenshot/UI evidence required D1.
