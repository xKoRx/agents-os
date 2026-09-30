# Lane G — runtime / read-model / publisher / recovery remediation evidence (D5 Shot 3, Wave 2)

Worktree: `/home/kor/aranea/work/d5-shot3-20260929/wt-g-runtime`, branch `shot3/lane-g-runtime`.
Surfaces: `v3/core/internal/futuresruntime/` (IDs, read-model feed), the
read-model snapshot bound, the production routing/publisher seam
(`echo/operation` ingress), and the REC-03 recovery seam.
Constraints honored: `v3/sdk/futures/**`, `v3/futures-bridge/**`,
`futures_market_analytics.go`, `bus.go`, `futures_strategy_engine.go` and all
S12 evidence test files untouched; Lane R's `Registrations()` states lines in
`futuresruntime/runtime.go` preserved.

Commits (in order):

- `5c98b7e2` fix(futures): F-G-02 LIVE composes UUIDv7 ID allocation, deterministic allocator only for deterministic runs
- `6ac7ca04` fix(futures): F-G-04 bound read-model closed bars per stream/timeframe
- `0ad4826c` fix(futures): F-G-06 quarantine unaddressable-key execution-events records at the echo/operation ingress
- `871ea133` fix(futures): F-G-08 REC-03 cold-recovery fail-visible seam (COLD_RECOVERY_REQUIRED)

(Repaired locally before any push: the first F-G-04 commit had missed the
`Compose` feed wiring line — history was rewritten to `6ac7ca04` so every
finding commit builds standalone; verified with a throwaway worktree at
`6ac7ca04`, `go build ./...` OK.)

Final suites (fresh, `-count=1`):

- `cd v3/core && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 ./internal/...`
  → ok: internal, automation, functions, futuresruntime, futuresvertical (S12 incl.).
- `cd v3/sdk && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 ./futures/...`
  → all 13 packages ok.
- `cd v3/futures-projector && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 ./...` → ok.
- `cd v3/futures-bridge && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 ./...` → ok.
- `go vet` clean on futuresruntime, functions, futuresvertical, cmd/echo-core.
- Frozen evidence still green: `TestS12_Backtest_DoubleRun_Deterministic` PASS,
  `TestS12_REC04_RunProvenanceIsolation` PASS.

---

## F-G-02 (MAJOR) — LIVE composed with the deterministic ID allocator (unshared counter race, restart collisions)

- **Finding:** `Compose` injected `DeterministicIDAllocator` unconditionally;
  production (`cmd/echo-core/main.go:538` → `Compose`) minted `fop-000001`
  identities in LIVE: not UUIDv7, shared counters without a mutex (data race),
  colliding with historical ids after restart.
- **Authority:** D2-04 §2.1 (operation_id UUIDv7, `utils.GenerateUUIDv7`),
  §2.2 (order_id = client_order_id UUIDv7, idempotency key); deterministic
  allocator remains only for deterministic runs.
- **Tests:** new `internal/futuresruntime/ids_test.go`:
  `TestCompose_LiveIDsAreUUIDv7`, `TestCompose_BacktestIDsRemainDeterministic`,
  `TestCompose_ExactReplayIDsRemainDeterministic`,
  `TestCompose_ExplicitIDAllocatorOverride`,
  `TestDeterministicIDAllocator_ConcurrentAllocationsUnique` (-race);
  `TestCompose_RegistersAllSixOwners` updated to pin the LIVE UUIDv7 format
  (per the finding note).
- **RED:** `cd v3/core && GOTMPDIR=/home/kor/aranea/gotmp go test ./internal/futuresruntime/ -run 'TestCompose_LiveIDsAreUUIDv7' -v`
  ```
  Error: Received unexpected error: invalid UUID length: 10
  Messages: LIVE operation_id must be a UUID, got "fop-000001"
  --- FAIL: TestCompose_LiveIDsAreUUIDv7
  ```
  and `-race`:
  ```
  WARNING: DATA RACE ... DeterministicIDAllocator.NewOperationID() ids.go:25
  Messages: duplicate identity "fop-000016" under concurrency
  --- FAIL: TestDeterministicIDAllocator_ConcurrentAllocationsUnique
  ```
- **GREEN:** same package with `-race` → all PASS; `futuresvertical` suite ok.
- **Files changed:** `futuresruntime/ids.go` (mutex),
  `futuresruntime/runtime.go` (`defaultIDAllocator` by RunMode:
  LIVE→`functions.UUIDv7IDAllocator`; BACKTEST/EXACT_REPLAY→deterministic;
  fail-closed `WithIDAllocator` override for deterministic drivers),
  `futuresruntime/ids_test.go`, `futuresruntime/runtime_test.go`,
  `futuresvertical/harness.go` (deterministic driver pins the deterministic
  allocator explicitly, keeping S12 byte-determinism).
- **Deviations:** the vertical harness (virtual clock, scripted input) keeps
  deterministic ids by explicit pin — it is a deterministic run per D2-04
  §2.2, not a LIVE deployment; production path is unchanged plain `Compose`
  and now mints UUIDv7 in LIVE.

## F-G-04 (MAJOR) — read-model bars accumulate every closed bar (unbounded with run duration)

- **Finding:** `ReadModelFeed.ApplyBarsSnapshot` fed every closed bar of every
  compacted snapshot into `SnapshotReadModel.bars` (sdk, frozen, no eviction
  API) → hot state grows with run duration.
- **Authority:** Budgets V1 §4.1 HARD ACCEPTANCE BUDGET (bounded by declared
  lookbacks, never run duration; no unbounded all-history).
- **Consumers read:** `readModelMarket.Mark/Ready` (latest-only current +
  readiness), strategy reads via `marketctx` scopes — S1 `BarRange(…,128)`,
  S2 H4 SMA50 (51+ closed H4) + 20 5m; no `Bar(barID)` reader exists outside
  the interface.
- **Tests:** new `internal/futuresruntime/feed_bars_test.go`:
  `TestReadModelFeed_BarsBoundedPerTimeframe`,
  `TestReadModelFeed_BarReadsIdenticalWithinReachableWindow`,
  `TestReadModelFeed_DefaultBarRetentionBound`.
- **RED:** (API surface added with old behavior first)
  ```
  Messages: bar beyond the retention bound must be evicted (Budgets §4.1)
  --- FAIL: TestReadModelFeed_BarsBoundedPerTimeframe
  ```
- **GREEN:** `go test ./internal/futuresruntime/` ok; `futuresvertical` (S12
  goldens + exact-replay equality) ok.
- **Files changed:** `futuresruntime/views.go` (`boundedBarStore` per
  (stream,timeframe), oldest-first eviction; `Model()` now serves a
  `marketctx.ReadModel` wrapper — current/readiness/range/session delegate to
  the shared snapshot model, `Bar` reads the bounded store),
  `futuresruntime/snapshot.go` (config-driven `BarRetention`, negative
  invalid; zero → `DefaultBarRetention` 256 ≥ largest configured reach-back
  S1 128 / S2 60 H4 + 20 5m), `futuresruntime/runtime.go` (Compose wiring),
  `feed_bars_test.go`.
- **Deviations:** the frozen sdk `SnapshotReadModel` keeps latest-only /
  replaced-per-snapshot views; the bounded closed-bar store lives in the feed
  (the only mutable accumulation point I own). Reads inside the retained
  window are byte-identical to the unbounded form (exact-replay equality
  asserted).

## F-G-06 (MAJOR) — path-1 fill published without account_strategy_id → infinite ghost-address redelivery

- **Finding:** production publisher (`futures-bridge/adapters/kafka/
  publisher.go` ← `capabilities/adapter.go CorrelationKey()`, frozen for this
  lane) keys a Fill with unresolvable account_strategy_id by the BARE account;
  production `module.yaml` ingresses every `echo.execution-events.v1` record
  into `echo/operation`; `ParseOperationOwnerKey` failed and returned the
  error → StateFun redelivered forever against the ghost address. The
  correlation filter existed only in the vertical harness bridge.
- **Authority:** D2-07 §17 three-path split; D2-07C §14 (key = op key,
  ingress directo a echo/operation).
- **Tests:** new `internal/functions/futures_operation_owner_gate_test.go`:
  `TestFuturesOperationFn_UnaddressableOwnerKeyQuarantined` (bare account /
  empty account segment / empty strategy segment),
  `TestFuturesOperationFn_OwnerPathLiveAfterQuarantine`.
- **RED:**
  ```
  Messages: an unaddressable-key record must be quarantined, never redelivered
  Error: Received unexpected error: domain: "acct-1" is not an account_id:account_strategy_id key
  --- FAIL (all 3 ghost-address subtests)
  ```
- **GREEN:** `go test ./internal/functions/` ok.
- **Files changed:** `functions/futures_operation.go` (ingress correlation
  gate: unaddressable owner id ⇒ fail-visible `Error` telemetry with
  `quarantined=true` attribute + drop, `return nil` — never a redelivery
  request), `futures_operation_owner_gate_test.go`.
- **Deviations / escalation:** the finding's prescribed fix location ("the
  production publisher") is `v3/futures-bridge`, FROZEN for this lane
  ("futures-bridge (Lane F done)"). The publisher-side rule "never publish on
  the operation path without a resolvable account_strategy_id" therefore
  could NOT be ported there; the shipped fix is the Core-side production
  ingress gate (the receiver of path 1, which I own), which converts the
  infinite redelivery loop into a fail-visible quarantine. The bridge-side
  `CorrelationKey` bare-account fallback for uncorrelated Fills remains a
  contract violation upstream and is ESCALATED to the bridge owner (Lane F /
  Primary Manager): recommended = quarantine-at-source + telemetry, never the
  bare-account key for correlated families.

## F-G-08 (MAJOR) — REC-03 cold recovery: no implementation, no test

- **Finding:** zero occurrences of `COLD_RECOVERY_REQUIRED` in the repo
  (`grep -rn COLD_RECOVERY_REQUIRED v3/ | wc -l` → 0); no fail-visible cold
  seam, no failure injection.
- **Authority:** ATP §12 REC-03 (Gate D5): "Remove required execution
  checkpoint/authority. Expected fail-visible `COLD_RECOVERY_REQUIRED`; no
  reconstructed trading state from projections."
- **Seam implemented (vs ATP, exactly):**
  - `futuresruntime/recovery.go`: `ContinuityEvidence{PriorRunRef,
    RuntimeContinuityRef}`; `EvaluateColdRecovery` — durable prior-run
    execution evidence present WITHOUT the matching runtime continuity pin
    (the required execution checkpoint/authority) ⇒ typed
    `ColdRecoveryRequiredError` carrying the `COLD_RECOVERY_REQUIRED` token;
    fresh deployment (no prior evidence) and pinned lineage (REC-01 restart)
    compose normally. `ComposeWithRecoveryGate` refuses BEFORE any owner is
    built or registered — no silent start, and there is deliberately NO
    reconstruction path from projections (the refusal is the contract).
  - Production wiring `cmd/echo-core/main.go`
    (`registerFuturesIfConfigured`): reads `futures/recovery/prior_run` and
    `futures/recovery/runtime_continuity` from the etcd config plane, surfaces
    `tel.Error(... "futures cold recovery required (REC-03)", reason,
    prior_run_ref)` and exits fail-fast — owners are never registered.
  - **DEFERRED_TO_D6 explicitly:** physical checkpoint-lineage introspection
    (proving the Flink checkpoint carries the lineage bit-for-bit) and the
    automation that maintains the two config-plane pins across deployments;
    the D5 seam carries the identity pins and the fail-visible refusal.
- **Tests:** new `internal/futuresruntime/recovery_test.go`:
  `TestREC03_ColdRecoveryInjection_PriorEvidenceWithoutContinuity`,
  `TestREC03_ColdRecoveryInjection_ContinuityMismatch`,
  `TestREC03_ContinuityPinPasses`, `TestREC03_FreshDeploymentPasses`,
  `TestREC03_SeamPrecedesComposition` (refused start composes nothing; pinned
  start registers the six owners).
- **RED:** the seam did not exist:
  ```
  undefined: EvaluateColdRecovery / ContinuityEvidence / ColdRecoveryRequiredError
  FAIL github.com/xKoRx/echo/v3/core/internal/futuresruntime [build failed]
  ```
  (plus the pre-fix grep evidence of zero occurrences).
- **GREEN:** `go test ./internal/futuresruntime/ -run TestREC03 -v` → 5/5 PASS.
- **Files changed:** `futuresruntime/recovery.go`, `recovery_test.go`,
  `cmd/echo-core/main.go`.
- **Deviations:** none beyond the explicit D6 deferral above. No generic
  recovery framework was built (two pins, one pure evaluation, one refusal
  path).
