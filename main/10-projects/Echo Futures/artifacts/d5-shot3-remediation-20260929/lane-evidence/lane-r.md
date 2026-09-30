# Lane R — recording (F-MGR-01 live decision context-read persistence)

Branch `shot3/lane-r-recording`, worktree `wt-r-recording`. Base: Shot 2 head
`5d02adcf` (Shot 1 frozen at `4c41ee77`). Clean tree at end; nothing pushed.

## Finding addressed

F-MGR-01 (BLOCKER): the LIVE runtime never persisted decision-critical context
reads. `futures_strategy_engine.go handleTrigger` called
`fn.engine.Handle(st, fn.now(), trigger, fn.cfg.ReadModel)`; the sdk engine
created the `marketctx.NewLiveScope` internally and the captured reads became
unreachable — S12 proved replay works IF a corpus exists, but no real LIVE
decision produced one.

## Design summary (what / where / why atomic)

- **Scope ownership moved to the owner** (`v3/core/internal/functions/futures_strategy_engine.go`):
  `handleTrigger` now builds `marketctx.NewLiveScope(fn.cfg.ReadModel)` itself
  and calls the frozen `fn.engine.HandleWithScope(st, fn.now(), trigger, scope)`,
  so `scope.Reads()` (ordered capture-as-consumed corpus, D4-A1 §6.1/§6.2) stays
  reachable. `HandleWithScope` untouched.
- **What is persisted**: a `market.DecisionEvidence` record — run identity
  (`run_id`/`run_mode` from the island's pinned provenance, cross-checked
  against the RUN_START payload, fail-visible on mismatch), owner key
  (strategy id), owner input coordinate (`owner_input_seq`/`runtime_ts` from
  the persisted `strategy.OwnerState` order), trigger identity, decision
  identity (`eval_seq`, `cycle_seq`, ordered `signal_ids`) and the ordered
  `context_reads[]` (ordinal, logical key, observed version, minimal inline
  value, content digest — the frozen minimal model; sealed with a
  `decision_digest`). No DecisionObservation, no snapshots, no new state owner.
- **Where**: as an inline `JournalControl{Kind: DECISION_EVIDENCE}` on the
  EXISTING `echo.futures.market-run-journal.v1` topic, keyed by OwnerKey
  (same egress pattern as `futures_market_stream.go egressJournal`);
  `v3/sdk/futures/market/recording.go` extended ADDITIVELY with the record
  type + typed seal/verify/decode (control-digest mismatch and sealed-content
  mismatch both fail visible). No new topic/service/aggregate/lifecycle.
- **Why atomic**: the evidence egress is sent inside the same handler
  invocation as `persist(st)` and the Signal egress; in StateFun all effects
  of one invocation commit atomically at the checkpoint boundary (D2-06C §16
  recording point) — an evidence build/emit error returns before commit, so
  there is NO durable decision whose replay evidence can be silently lost.
  The vertical bus mirrors the same contract (`busContext` captures egress
  only after the handler returns).
- **Arming**: the frozen RUN_START control (`market.MarketControlEnvelope`,
  test-provisioned per S12) delivered to the strategy island sets a bounded
  identity-only `market.RunRecordingState` under a new ValueSpec
  (`futures_se_recording`). Without it the island behaves exactly as before
  (`emitDecisionEvidence` no-ops) — S12 `TestS12_RunJournal_DeadWithoutRunStart`
  semantics preserved. Stream-scoped controls are absorbed (market island owns
  them). RUN_START redelivery is idempotent (identity-only state rewrite).

## Files changed

- `v3/sdk/futures/market/recording.go` — additive: `DecisionEvidenceKind`,
  `DecisionEvidence` (+Validate/Seal/VerifyDigest),
  `SealDecisionEvidenceControl`, `DecodeDecisionEvidence`.
- `v3/core/internal/functions/futures_strategy_engine.go` — scope ownership,
  RUN_START arming (`handleControl`, `Recording` ValueSpec +
  `StateFuturesSERecording`), `emitDecisionEvidence`.
- `v3/core/internal/futuresruntime/runtime.go` — 1 line: strategy registration
  `States: {fn.Owner, fn.Recording}` (the StateFun Go SDK requires eager
  registration of every ValueSpec a function touches; composition plumbing).
- NEW `v3/core/internal/futuresvertical/s12_live_recording_test.go` —
  acceptance tests (below). `replay_driver.go`, `s12_*` frozen evidence
  untouched; `v3/sdk/futures/strategy/**`, `marketctx/**`, `bus.go`,
  `futures_market_analytics.go`, `operation/provider/gerardmm` untouched.

## Tests added

- `TestS12_LiveDecision_EvidenceFromJournal_ReplaysExactly` — LIVE→journal→
  EXACT_REPLAY over the PRODUCT runtime: RUN_START armed on market+strategy
  islands, real S1 day fed through raw candidate ingress, breakout decision
  committed by the real strategy owner; the corpus is extracted FROM THE
  PERSISTED JOURNAL EGRESS (captured `TopicFuturesRunJournal` records, typed
  `DecodeDecisionEvidence` — never test-built); replay = fresh engine (same
  run id) + exact recorded trigger (recovered from the delivered canonical
  events by the sealed trigger identity) + `marketctx.NewReplayScope(corpus)`
  with the live read model POISONED behind it. Asserts 100% decision identity
  equality (eval_seq/cycle_seq/signal id), 100% semantic equality
  (byte-canonical signal vs the LIVE product egress), exact context-read
  equality (strict-equality `scope.Close()`), and 100% post-state equality vs
  the durable product state.
- `TestS12_LiveDecision_EvidenceFailures_FailVisible` — corrupt read / digest
  mismatch / missing read / unexpected extra read all fail VISIBLY through the
  typed ReplayScope errors (no-signal no-fallback, NotReady downgrade, or
  `IsReplayContextFailure` on Close); plus a tampered journal evidence record
  fails visible at `DecodeDecisionEvidence` (control digest mismatch).
- `TestS12_LiveDecision_RecordingDeadWithoutArming` — market island armed but
  strategy island not: decisions commit, ZERO decision-evidence records
  (opt-in per island, D2-06C §16 admission boundary).

## Evidence (RED → GREEN)

Commands (from `v3/core`): `GOTMPDIR=/home/kor/aranea/gotmp go test
./internal/futuresvertical/ -run 'TestS12_LiveDecision'` (and `-v`), then the
full suites.

RED (before the engine change; recording.go types already additive-only —
defect demonstrated exactly as stated: the persisted journal contains no
decision reads):

```
--- FAIL: TestS12_LiveDecision_EvidenceFromJournal_ReplaysExactly (0.55s)
        Messages: F-MGR-01: no decision-evidence in the persisted journal: the LIVE corpus was never produced
--- FAIL: TestS12_LiveDecision_EvidenceFailures_FailVisible (0.61s)
FAIL  github.com/xKoRx/echo/v3/core/internal/futuresvertical
```

GREEN (after; committed tree):

```
--- PASS: TestS12_LiveDecision_EvidenceFromJournal_ReplaysExactly (0.66s)
--- PASS: TestS12_LiveDecision_EvidenceFailures_FailVisible (0.74s)
  --- PASS: .../mutated_value_with_stale_digest_is_corrupt_corpus
  --- PASS: .../mutated_digest_is_corrupt_corpus
  --- PASS: .../swapped_keys_break_the_recorded_order
  --- PASS: .../dropped_required_read_is_missing
  --- PASS: .../extra_recorded_read_is_unconsumed
--- PASS: TestS12_LiveDecision_RecordingDeadWithoutArming (0.62s)
```

Full suites (exact commands):

- `cd v3/core && GOTMPDIR=/home/kor/aranea/gotmp go test ./internal/functions/... ./internal/futuresvertical/... ./internal/futuresruntime/...`
  → `ok .../functions 0.135s` · `ok .../futuresvertical 22.076s` ·
  `ok .../futuresruntime 0.024s` — ALL GREEN, incl. the frozen S12 evidence
  (`s12_exact_replay_test.go`, `s12_backtest_test.go`,
  `TestS12_RunJournal_OrderedRecordingLive`,
  `TestS12_RunJournal_DeadWithoutRunStart`) unweakened.
- `cd v3/sdk && GOTMPDIR=/home/kor/aranea/gotmp go test ./futures/...` →
  13/13 packages `ok` (market, marketctx, strategy, s1, s2, ...).
- `gofmt -l` clean on the four touched files; `go vet` clean on the three
  core packages.

## Commits

- `d6d1c811` feat(futures): DECISION_EVIDENCE journal record contract (additive)
- `0bcf3906` fix(futures): F-MGR-01 live decision context-read persistence

## Deviations

1. `v3/core/internal/futuresruntime/runtime.go` (outside the listed surface):
   one line adding `fn.Recording` to the strategy-engine registration
   `States`. Justified: the StateFun Go SDK only permits a function to access
   ValueSpecs eagerly registered on its spec (`stateful_function.go`:
   "A function may only access values that have been eagerly registered"),
   and the arming state must be durable per key — an undeclared spec would
   break production registration while passing the in-process bus. No other
   runtime.go change; `Compose`/routing untouched.
2. The durable arming state is a NEW ValueSpec on the strategy owner rather
   than a field on `strategy.OwnerState`: the OwnerState type lives in
   `v3/sdk/futures/strategy/**` (forbidden lane). The ValueSpec holds only
   bounded identity (`market.RunRecordingState`), no journal writer state —
   the decision coordinate is read from the already-durable
   `strategy.OwnerState` (`OwnerInputSeq`/`RuntimeTs`), so no duplicate order
   authority exists.
3. RUN_START is NOT re-journaled inline on the strategy island (the market
   island already journals it; the mandate requires decision-evidence records,
   and omitting keeps the island journal minimal with no second admission
   counter).
4. Limitation declared honestly (not hidden): a fully-consistent forgery of an
   evidence record (re-sealed with a fresh decision_digest) decodes as a valid
   record — content-addressed sealing detects tampering of persisted bytes,
   not a deliberate re-seal. Detection of that class belongs to the
   manifest/journal integrity layer (D2-06C §28 archival), unchanged by this
   lane.
