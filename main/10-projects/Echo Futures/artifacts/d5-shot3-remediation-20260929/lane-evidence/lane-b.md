# Lane B (strategy sdk surface) — Shot 3 remediation evidence

Worktree: /home/kor/aranea/work/d5-shot3-20260929/wt-b-strategy, branch shot3/lane-b-strategy.
Baseline before any change: v3/sdk `go test ./futures/...` ok; v3/core `go test ./internal/futuresvertical/... ./internal/functions/...` ok (72.1s).

---

## F-B-01 — S1 never reports Outcome.CycleOpen (MAJOR)

- Finding: S1 never set `Outcome.CycleOpen`; `engine.HandleWithScope` step 7 (`st.Config.PromotePending(outcome.CycleOpen)`) therefore promoted a pending config on ANY S1 evaluation, including mid-cycle while OPEN_CYCLE_LONG held the frozen config. Reproduced: OPEN_CYCLE_LONG promotes v2 while frozen OR is still v1. S2 already reports `CycleOpen` correctly (s2.go:238). The engine motor itself is correct (TestEngine_ConfigCycleActivation_* uses a scripted module that reports cycleOpen; it validates the motor, not the module).
- Authority: Technical SPEC V1 §23 ("Strategy config according to technical-cycle activation rules"); D4-B3 §13 (technical lifecycle OPEN/CLOSE_ALL — a cycle is open exactly while phase ∈ {OPEN_CYCLE_LONG, OPEN_CYCLE_SHORT}); Functional SPEC V1 §28 ("A Strategy config update follows the frozen cycle transition semantics; it is not silently injected halfway through an active technical cycle").
- Tests added (v3/sdk/futures/strategies/s1/s1_test.go):
  - `TestS1_CycleOpen_ModuleOutcomeAcrossLifecycle` — module-level: drives the REAL S1 directly (state blob handed back each evaluation) and asserts `Outcome.CycleOpen` mirrors the post-evaluation phase at every lifecycle point (ARMED=false; breakout=true; mid-cycle bar=true; stop-hit=false; WAIT_REARM=false; re-arm=false; re-entry=true; back-inside close=false; day rollover with open cycle=false).
  - `TestS1_PendingConfig_PromotesOnlyAtCycleBoundary` — engine integration over the REAL module: pending v2 is NOT promoted by a mid-cycle bar close; it is promoted exactly at the stop-hit evaluation that closes the cycle.
  - fixtures_test.go: extracted `harness.putTradeCurrent` out of `feedTrade` (no behavior change) for direct module evaluations.
- RED (`cd v3/sdk && GOTMPDIR=/home/kor/aranea/gotmp go test ./futures/strategies/s1/ -run 'TestS1_CycleOpen_ModuleOutcomeAcrossLifecycle|TestS1_PendingConfig_PromotesOnlyAtCycleBoundary'`), tail:
  ```
  --- FAIL: TestS1_CycleOpen_ModuleOutcomeAcrossLifecycle (0.01s)
      s1_test.go:560: Messages: the breakout evaluation opens a technical cycle (OPEN_CYCLE_LONG) — Should be true
      s1_test.go:567: Messages: OPEN_CYCLE_LONG after a bar close outside the range — Should be true
      s1_test.go:592: Messages: re-entry breakout opens a new technical cycle
  --- FAIL: TestS1_PendingConfig_PromotesOnlyAtCycleBoundary (0.01s)
      s1_test.go:627: expected: 1, actual: 2 — "OPEN_CYCLE_LONG must not promote the pending config mid-cycle"
  ```
- Fix: v3/sdk/futures/strategies/s1/s1.go — `Module.Evaluate` recomputes `out.CycleOpen = st.Phase == PhaseOpenCycleLong || st.Phase == PhaseOpenCycleShort` after the handler returns (engine.go:258 unchanged; motor already correct).
- GREEN (same command): both PASS; full `go test ./futures/...` ok.
- Files changed: v3/sdk/futures/strategies/s1/s1.go, s1_test.go, fixtures_test.go.
- Commit: db3cf385 `fix(futures): F-B-01 S1 reports Outcome.CycleOpen at the cycle boundary`.
- Deviations: none.

---
## F-B-02 — late admission: expired-at-consumption Signal poisons the owner (MAJOR)

- Finding: a canonical input admitted late (trigger older than the 5m validity window) yields `valid_until <= created_at`; `sig.Validate` hard-failed the whole evaluation (engine.go:245-249) AFTER the in-memory trigger dedup had advanced. The production caller (v3/core/internal/functions/futures_strategy_engine.go:156-158) persists owner state only on success, so the dedup was never persisted: every redelivery reproduced the identical hard error — infinite redelivery, owner blocked.
- Authority: D4-B3 §11 (frozen semantics): `valid_until = next canonical 5m bucket close strictly after trigger event_ts`; "Si la OPEN llega a echo/operation después de valid_until, el guard existente la descarta. Strategy no simula fill ni fija execution price." => the frozen semantics is DISCARD at the guard (absorb), no fill simulation, nothing else. Implemented exactly that at the earliest guard: the engine drops an already-expired Signal instead of erroring.
- Determinism: `created_at = st.RuntimeTs` (journal-derived admitted logical time, identical in LIVE/EXACT_REPLAY) and `valid_until` is module-deterministic, so the same (state, trigger, runtime_ts) always absorbs — same-input/same-output preserved. The technical evaluation stands (module state advanced deterministically; e.g. a stale stop-hit still moves S1 to WAIT_REARM with the cycle closed); the redelivered input is absorbed as `duplicate_trigger` once the state (with dedup) persists. In-window signals and LIVE fail-closed behavior are unchanged (absorption only fires when `!sig.ValidUntil.After(sig.CreatedAt)`, the same predicate `domain.Signal.Validate` enforces).
- Tests added:
  - v3/sdk/futures/strategy/engine_test.go `TestEngine_ExpiredAtConsumption_SignalAbsorbed_NoPoisonLoop` — motor level (scripted module): expired OPEN draft absorbed (no error, no signal, eval + technical cycle counted, zero emitted), redelivery absorbed as `duplicate_trigger`.
  - v3/sdk/futures/strategies/s1/s1_test.go `TestS1_LateAdmission_ExpiredSignal_Absorbed_NoHardError` — REAL S1: breakout at 10:03, runtime clock jumped to 10:45, stale 10:20 stop-hit trade (valid_until 10:25) absorbed; module state WAIT_REARM; redelivery `duplicate_trigger`; a fresh 10:47 trade evaluates normally (owner unblocked).
- RED (`cd v3/sdk && GOTMPDIR=/home/kor/aranea/gotmp go test ./futures/strategy/ -run TestEngine_ExpiredAtConsumption` and `./futures/strategies/s1/ -run TestS1_LateAdmission`), tails:
  ```
  engine_test.go:332: Received unexpected error:
      strategy: TEST_SPEC_V1 signal 0 invalid: domain: signal e52cccc... valid_until must be after created_at
    Messages: an expired-at-consumption signal must be absorbed, not fail the evaluation
  s1_test.go:658: Received unexpected error:
      strategy: S1_NY_ORB_30M_V1 signal 0 invalid: domain: signal 6d88abb... valid_until must be after created_at
    Messages: an expired-at-consumption CLOSE_ALL must be absorbed, not fail the owner
  ```
- Fix: v3/sdk/futures/strategy/engine.go — step 6 drops the built Signal when `!sig.ValidUntil.After(sig.CreatedAt)` (before `sig.Validate`); `StrategyCycleSeq` advance for `NewCycle` drafts is kept because the technical cycle did open in module state (consistent with F-B-01's CycleOpen report); `SignalsEmitted`/egress count only delivered signals.
- GREEN: both PASS; full `go test ./futures/...` ok (0 non-ok lines).
- Files changed: v3/sdk/futures/strategy/engine.go, engine_test.go; v3/sdk/futures/strategies/s1/s1_test.go.
- Commit: 357d0f00 `fix(futures): F-B-02 absorb expired-at-consumption Signals (no poison loop)`.
- Deviations: none. Note: S2 (valid_until = bucket close + 5m) had the same latent poison class; the fix is module-agnostic and covers it without touching s2.go (S2 has no module-level change).

---
## F-B-03 — technical stop computed across a grid gap (MAJOR)

- Finding: `technicalReference` (s1.go, the §6 closed-context read) validated only reach-back (`rng.Bars[0] <= premarket start`), not contiguity: an intra-window gap produced an INCORRECT technical stop instead of fail-closed. Repro: drop the 08:30 bar (day low 97.00) from the served range → OPEN emitted with `technical_stop 97.25` (the next bar's low).
- Authority: D4-B3 §6 — CLOSED_CONTEXT_BARS(t) over `[premarket_start, previous_closed_bar(t)]` with "sólo se admiten barras cerradas con cobertura demostrable"; an accumulated extreme over a gapped grid is not demonstrable coverage. Per the accepted finding: on gap → no technical stop (fail-closed omission), never a wrong stop.
- Tests added (v3/sdk/futures/strategies/s1/s1_test.go `TestS1_ContextGridGap_FailClosed_NoStop`, 3 subtests):
  - ExtremeHolderBarMissing (08:30 dropped): today a wrong 97.25 stop/OPEN; must be no stop + `S1_CLOSED_CONTEXT_UNPROVABLE` + stays ARMED.
  - NonExtremeGap (08:20 dropped): value would be unchanged (97) but coverage is unprovable → still fail-closed.
  - PremarketStartSlotMissing (08:00 dropped): the slot exactly at the premarket start is part of the window.
- RED tail (subtest 1, `go test ./futures/strategies/s1/ -run TestS1_ContextGridGap`):
  ```
  Messages: a gapped grid must not produce a (wrong 97.25) stop — Should be empty, but was [{... "observed_low":"97.25" ... "technical_stop":"97.25" ...}]
  ```
- Fix: v3/sdk/futures/strategies/s1/s1.go `technicalReference` — after prevIdx resolution: the first bar at/after the premarket start must be exactly at the start (grid alignment already enforced by resolveDay), and every consecutive pair through prevIdx must be exactly one canonical 5m slot apart (`barTF.Duration()`); any violation → `ReasonClosedContextUnprovable`.
- Fixture casualties (all the SAME defect class — expected values computed over a gapped feed), repaired with justification:
  1. `v3/sdk/futures/strategies/s1/s1_test.go` TestS1_AcS112: the re-entry scenario never fed the 10:00-10:05 bucket, so the re-entry stop window carried a gap at 10:00. Repaired by feeding the canonical 10:00 bar (close outside the frozen range; scenario semantics untouched; expectations unchanged).
  2. `v3/core/internal/futuresvertical/fixtures_test.go` s1SetupTrades: comment claims "04:00..09:25" (=66 buckets) but code fed 54 (04:00..08:25) → 12 missing slots (08:30..09:25). Repaired 54→66.
  3. `v3/core/internal/futuresvertical/s12_exact_replay_test.go` s12S1ReadModel/s12AllS1Bars: same 54→66 repair; range version "range@60"→"range@72".
- Golden re-pin justification (sanctioned by the task for "a wrong stop from F-B-03 in the fixtures"): the recorded S1 golden decision (stop 21695) was computed across the fixture's hole — the premarket extreme between 08:30 and 09:25 was unproven, exactly the defect class F-B-03 removes. Repairing the feed to the comment's own intended geometry (66 contiguous buckets, all flat @21700) keeps every golden VALUE byte-identical — `"intent": "OPEN"`, `"run_mode": "LIVE"`, `"technical_stop": "21695"` — and moves only `"strategy_eval_seq"` 61→73 (the warm-up now legitimately runs 72 bar-close evaluations instead of 60). Exact-replay 100% equality holds (`AssertExactReplay`) and BACKTEST double-run determinism holds (`TestS12_Backtest_DoubleRun_Deterministic`), both green.
- GREEN: `go test ./futures/...` (sdk) ok; `go test ./internal/futuresvertical/... ./internal/functions/...` (core) ok — 27/27 vertical tests PASS, 0 fail, 0 skip.
- Files changed: v3/sdk/futures/strategies/s1/s1.go, s1_test.go; v3/core/internal/futuresvertical/fixtures_test.go, s12_exact_replay_test.go (test-fixture data only).
- Commit: 72250a3d `fix(futures): F-B-03 S1 technical reference demands a contiguous closed-bar grid`.
- Deviations: the futuresvertical/S12 test edits above are the sanctioned re-pin; no production code outside v3/sdk/futures/strategy/** was touched.

---
## F-TOP-02 — replay context failures degraded into silent NotReadyReason (MAJOR)

- Finding: S1 degraded typed ReplayScope failures (MISSING/MISMATCH reads) into silent fail-closed `NotReadyReason`s (s1.go `readyForBreakout` :583-599 swallowing readiness/current/session errors; `technicalReference` swallowing the BarRange error). MKT-12 requires a "deterministic replay failure" and Technical SPEC V1 §8.3 lists missing/unresolvable reads as HARD failures. s2.go was checked: it has NO decision-context reads (bars-only accumulation from triggers), so no change was needed there.
- Authority: Technical SPEC V1 §8.3 (EXACT_REPLAY hard failures: "required read missing; ... recorded read cannot be resolved to its exact value"); ATP MKT-12 ("Expected: deterministic replay failure, never fallback to current/latest state"); marketctx.ReplayScope contract (fail-visible typed errors; `marketctx.IsReplayContextFailure`).
- Fix: v3/sdk/futures/strategies/s1/s1.go — one guard `ctxReadErr(err)`: typed replay context failures propagate as hard errors (`s1: replay context read failed: %w`) from BOTH `readyForBreakout` (now returns `(bool, error)`; called with error check in `onTrade`) and `technicalReference` (now returns `(*technicalReference, string, error)`; hard error returned to `Evaluate`, which the engine already propagates). LIVE `ReadNotAvailableError` misses keep the frozen fail-closed NotReady/`S1_CLOSED_CONTEXT_UNPROVABLE` behavior — unchanged.
- Tests added (v3/sdk/futures/strategies/s1/s1_test.go `TestS1_ReplayContextFailure_HardError_NotNotReady`):
  - MissingRecordedRead (corpus minus the BarRange read) → hard error, `IsReplayContextFailure`, nil evaluation.
  - EmptyCorpus → hard error on the first unrecorded read.
  - LiveReadMiss control → NO error, `Ready=false`, `S1_CLOSED_CONTEXT_UNPROVABLE` (LIVE behavior pinned unchanged).
- RED (`go test ./futures/strategies/s1/ -run TestS1_ReplayContextFailure`), tail:
  ```
  --- FAIL: .../MissingRecordedRead_IsHardError: An error is expected but got nil. — a typed replay failure is a hard error, not a silent NotReadyReason
  --- FAIL: .../EmptyCorpus_IsHardError: An error is expected but got nil. — the first unrecorded read fails the replay loudly
  --- PASS: .../LiveReadMiss_StillFailsClosedNotReady   (control already green before the fix)
  ```
- Sanctioned S12 re-pin (justification): `v3/core/internal/futuresvertical/s12_exact_replay_test.go` `TestS12_ReplayFailures_FailVisible` asserted the defective downgrade — its own case-table comment said `// modules downgrade context failures to NotReadyReason (F-TOP-02)`. The swap_keys/drop_last cases and the empty-corpus block now demand the typed HARD failure (`require.Error` + `marketctx.IsReplayContextFailure` + MISSING/MISMATCH in the message + nil evaluation); the mutate_* construction-failure cases and the extra_read/Close-UNUSED case are unchanged, and the no-fallback direction is preserved (nothing is ever evaluated from current state on a corrupt corpus). No golden decision bytes are involved in these cases.
- GREEN: full `go test ./futures/...` (sdk) ok; core `go test ./internal/futuresvertical/... ./internal/functions/...` ok.
- Files changed: v3/sdk/futures/strategies/s1/s1.go, s1_test.go; v3/core/internal/futuresvertical/s12_exact_replay_test.go (test expectations only).
- Commit: a361d66b `fix(futures): F-TOP-02 propagate typed replay context failures as hard errors in S1`.
- Deviations: none beyond the sanctioned re-pin above.

---
## Final verification (all fresh, -count=1)

- `cd v3/sdk && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 ./futures/...` → all ok (gerardmm, market, marketctx, obs, operation, provider, strategies/s1, strategies/s2, strategy, units).
- `cd v3/core && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 ./internal/futuresvertical/... ./internal/functions/...` → ok (futuresvertical 34.5s), ok (functions).
- Goldens after the sanctioned re-pins: TestS12_S1_ExactReplay_Golden_Breakout PASS (intent OPEN / run_mode LIVE / technical_stop 21695 byte-identical; strategy_eval_seq 73 re-pinned), TestS12_S1_ExactReplay_SecondDecision PASS, TestS12_S2_ExactReplay_Golden_Pullback PASS (untouched), TestS12_Backtest_DoubleRun_Deterministic PASS (byte-identical double run).
- Tree clean; 4 commits on shot3/lane-b-strategy on top of Shot 2 infrastructure (9275fa74): db3cf385, 357d0f00, 72250a3d, a361d66b. No pushes, no branch switches, no rebases.

## Escalation / deviations summary

1. F-B-03 forced a GOLDEN RE-PIN (task-sanctioned path "…unless the expected demonstrably encoded a defect (e.g., a wrong stop from F-B-03 in the fixtures)"): the S12/vertical S1 fixture fed 54 premarket buckets while its own comment claimed 04:00..09:25 (66), silently gapping 08:30..09:25 inside the frozen reference window — the recorded 21695 golden decision was computed across that hole. Repaired to the intended contiguous feed; every golden VALUE byte-identical; only strategy_eval_seq 61→73 (consequence of the correct 72-bar warm-up). Exact-replay equality and BACKTEST double-run determinism hold.
2. F-TOP-02 forced a minimal S12 EXPECTATION re-pin: TestS12_ReplayFailures_FailVisible asserted the defective silent NotReady downgrade (its case table literally annotated the cases as F-TOP-02). Re-pinned to demand the typed hard error; no golden decision bytes involved.
3. S1 unit acceptance fixture AcS112 was missing the canonical 10:00 bucket (same F-B-03 defect class); repaired, expectations unchanged.
4. s2.go required NO change for any finding (S2 already reported CycleOpen; S2 performs no decision-context reads; F-B-02 is engine-level and covers S2's latent poison class).
5. No escalations remain: all four ACCEPTED findings are fixed with regression tests; no closure is faked.
