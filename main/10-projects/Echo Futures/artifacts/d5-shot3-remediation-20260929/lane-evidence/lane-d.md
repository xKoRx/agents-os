# Lane D — Provider package surface (v3/sdk/futures/provider/)

Worktree: `/home/kor/aranea/work/d5-shot3-20260929/wt-d-provider`, branch `shot3/lane-d-provider`, base `5d02adcf` (Shot 1 frozen at 4c41ee77; Lane C seam `ReleasedQExecMax` already on base).
All five Shot-2 findings fixed, one commit per finding, tree clean. No pushes, no branch switches. `operation/**`, `gerardmm`, `strategy`, `marketctx`, `core/*` untouched (read-only).

## F-D-01 — BLOCKER: capacity envelope ignores rule scope

- **Commit:** `a36720fb` `fix(futures): F-D-01 capacity envelopes evaluated over the cap's typed scope universe`
- **Authority:** D4-A2 §7 ("Todas las fórmulas siguientes se evalúan por el scope tipado de la policy … el grant es válido sólo si satisface todos los constraints aplicables"; §7.1/§7.3/§7.4 formulas); D2-05C L131/135 + C-R2.3 (scope = account-wide | instrument_id | product_group value; per-scope live reservation sets); A2-I5.
- **Files changed:** `v3/sdk/futures/provider/capacity.go` (new `bucketsInScope` for GROSS/NET_ABS in both the cap check and the physical-trust expansion guard; new `bucketsInWeightedScope` for GROUP_WEIGHTED; each cap evaluated independently over its own universe), `v3/sdk/futures/provider/capacity_scope_test.go` (new).
- **Tests:** `TestCapacityScopedEnvelope_InstrumentNetAbs` (MANDATORY REPRODUCER), `_ProductGroupNetAbs`, `_Gross`, `_GroupWeightedGross`, `_GroupWeightedNetAbs`, `_CrossScopeCoexistence`, `_AccountWideUnchanged`.
- **Hand-computed reproducer** (comments in test, independent of production helpers): NET_ABS scope="ES" cap=5; firm ES +10, NQ −10; candidate ES BUY 1. ES universe: N=10, B=1 ⇒ Env=max(|10−0|,|10+1|)=11 > 5 ⇒ **DENY**. Buggy account-wide projection: N=10−10=0, B=1 ⇒ Env=1 ≤ 5 ⇒ grants (the defect). RED observed: `expected: "INVALIDATED" actual: "RESERVED"`.
- **RED:** `cd v3/sdk && GOTMPDIR=/home/kor/aranea/gotmp go test ./futures/provider/ -run 'TestCapacityScoped' -v` → 6/7 scoped tests FAIL in both directions (buggy grants scoped breaches: Instrument/ProductGroup deny-cases; buggy denies real headroom: headroom-cases + GROSS + coexistence). Account-wide test PASS before and after (behavior unchanged; all pre-existing tests use account-wide/weighted-declared scopes and stay green).
- **GREEN:** `cd v3/sdk && GOTMPDIR=/home/kor/aranea/gotmp go test ./futures/provider/` → `ok`.
- **Deviation:** the finding's "ALL FOUR families" applies to GROUP_WEIGHTED with the frozen A-R2 semantics: a GROUP_WEIGHTED cap's typed universe is its **declared typed weights map** (D2-05C: "GROUP_WEIGHTED (por product_group de Instrument — congelado A-R2) … con pesos tipados del RuleSet"; Shot-1 `groupweighted_test.go` froze that envelopes span every weight-named group, e.g. scope="EQ-INDEX" with weights {EQ-INDEX, EQ-MICRO} counts the micro bucket). A strict scope-string filter for GROUP_WEIGHTED would break frozen Shot-1 behavior, so: universe = weight-named groups (explicit at the caller via `bucketsInWeightedScope`; undeclared groups never enter — A2-10; empty-group buckets keep failing closed via `groupWeightOf`). The weighted tests lock declared-universe semantics with hand-computed reachable values (6 and 16); no behavioral flip exists for this family without contradicting frozen semantics. The mis-scoped-envelope defect materially lived in GROSS/NET_ABS and is flipped RED→GREEN there.

## F-D-02 — MAJOR: MODIFY_DECREASE_ACK without quantity evidence released the full reservation

- **Commit:** `7c8d6b9a` `fix(futures): F-D-02 MODIFY_DECREASE_ACK without quantity evidence fails closed`
- **Authority:** A2-I8 (only authoritative new-qty/finality evidence may diminish q_exec_max or release); D4-A2 §10 modify-decrease + §14.3 **W5** (releases carry quantity); operation/wire.go `ReleasedQExecMax` contract (zero value = no quantity evidence in this release).
- **Files changed:** `v3/sdk/futures/provider/reservation.go` (MODIFY_DECREASE_ACK: no evidence ⇒ retain + telemetry `release_no_quantity_evidence`; with evidence ⇒ release exactly min(stored, ReleasedQExecMax, OrderQExecMax); VENUE_FINALITY keeps full release), `v3/sdk/futures/provider/effects.go` (telemetry const), `v3/sdk/futures/provider/release_evidence_test.go` (new).
- **Tests:** `TestRelease_ModifyDecreaseAckWithoutQuantityEvidenceFailsClosed`, `TestRelease_ModifyDecreaseAckReleasedQExecMaxEvidence` (min semantics, released ≥ stored no-op, cumulative CapacityUpdate evidence, finality contrast, capacity still held after retention). `TestRelease_ModifyDecreaseAndFinality` (pre-fed CapacityUpdate, masking the fail-open path) stays green.
- **RED:** `go test ./futures/provider/ -run 'TestRelease_ModifyDecrease'` → `expected: 4 / actual: 0` (full release on zero evidence).
- **GREEN:** `go test ./futures/provider/` → `ok`.
- **Deviations:** none. ReleasedQExecMax ≤ 0 is treated as "absent" per the wire contract; negative map evidence clamped (pre-existing).

## F-D-03 — MAJOR: ghost-owner effects wedge the account queue

- **Commit:** `de08500a` `fix(futures): F-D-03 absorb unroutable input at admission; never emit effects to a ghost owner`
- **Authority:** D4-A3 admission asymmetry (invalid input: telemetry + absorb, never an error that loops redelivery); SPEC §25 owner-key routing (`account_id:account_strategy_id`, `domain.OperationOwnerKey`).
- **Files changed:** `reservation.go` (routing guard at top of `handleReservationRequest`; pruned-grant FINAL replay routed via the redelivered message's strategy; unknown-grant revalidate records INVALID + durable fact + telemetry instead of an unaddressable result; revalidate replays emitted only when a route exists), `admission.go` (routing guard before any mutation/emission), `engine.go` (`recordLiveStrategy` records only routable keys — protects ForceClose fan-out), `effects.go` (`routableStrategy` helper + `TelemetryInputUnroutable`), `ghost_route_test.go` (new), `provider_test.go` (`TestRevalidate_UnknownGrantFailsClosed` asserted the ghost emission itself — updated to the new contract: recorded INVALID + durable fact + telemetry, no unaddressable effect).
- **Tests:** `TestGhostOwner_ReservationWithUnroutableStrategyIsAbsorbed`, `_AdmissionWithUnroutableStrategyIsAbsorbed`, `_RevalidateOfUnknownGrantRecordsWithoutGhostRoute`, `_RevalidateReplayAfterRecordPrunedStaysRouted`, `_ReservationReplayOfPrunedGrantIsRouted`; invariant helper `requireAllOwnerEffectsRouted`.
- **RED:** `go test ./futures/provider/ -run 'TestGhostOwner'` → all five FAIL with `owner-routed effect EXPOSURE_GRANT/ADMISSION_RESULT/REVALIDATE_RESULT must carry a route` (empty route observed — exactly the surfaces cited: reservation.go :325/:251, admission.go :64).
- **GREEN:** `go test ./futures/provider/` → `ok`.
- **Deviations:** the engine cannot know the caller address, so an unknown-grant revalidate outcome is recorded and made durable (decision fact + telemetry) but not delivered as an owner effect; this is the absorb branch of the mandated asymmetry. Core `functions/futures_provider_rules.go` was NOT touched (out of lane scope) — the fix is engine-side so the adapter can never observe an unaddressable effect.

## F-D-04 — MAJOR: OwnerState.Reservations never contracted (bound wedge)

- **Commit:** `2190d1bb` `fix(futures): F-D-04 contract fully released reservations (bounded live set)`
- **Authority:** D4-A2 §6.1 (record of a LIVE reservation); D2-05C §12 (ProviderDecisionFact stream is the audit engine — "sin history engine"); SPEC §26 dedup surfaces retained independently; D4-A3 §4.5 (invalidation releases inside the owner).
- **Files changed:** `reservation.go` (`contractReservation`: deletes records Finality=RELEASED with Remaining=0 at all five convergence points — PROVIDER_GATE_INVALID, VENUE_FINALITY, MODIFY_DECREASE_ACK→0, revalidate INVALID, fill-consumed terminal evidence; partial/PENDING_FINALITY records never contracted; `GrantRoutes` minimal retained routing evidence + `strategyOfGrant` fallback + deterministic eviction, bound `MaxGrantRoutes=1024`), `state.go` (GrantRoutes map + const + ensureMaps), `reservation_contract_test.go` (new), plus Shot-1/Shot-2 test updates where assertions dereferenced the retained INVALIDATED/FINAL records (`groupweighted_test.go`, `provider_test.go` TestRelease_ModifyDecreaseAndFinality / TestRevalidate_CurrentAuthorityWins / TestRevalidate_ExactnessRequired, `release_evidence_test.go`) — the retention WAS the defect.
- **Tests:** `TestReservations_ContractWhenFullyReleased` (257 grant+release cycles; outcomes retained), `TestReservations_ContractAcrossAllFullReleasePaths` (venue finality, revalidate INVALID, fill-consumed after egress, partial stays live, late revalidate replay stays routed after contraction).
- **RED:** `go test ./futures/provider/ -run 'TestReservations_Contract'` → `cycle 256: a released grant must free its bound slot` (exact wedge from the register; NOTE the first RED attempt accidentally passed due to a `:=` shadowing bug in my own test loop — fixed in the test before the fix commit; the true RED output above is from the corrected test).
- **GREEN:** `go test ./futures/provider/` → `ok`.
- **Deviations:** full deletion chosen over tombstones inside `Reservations` (tombstones would keep the wedge); audit evidence = durable decision facts + retained RequestOutcome/RevalidateOutcome maps; minimal retained form = `GrantRoutes` so the F-D-03 no-ghost-route invariant survives contraction (a late revalidate replay after contraction is deliverable — locked by test).

## F-D-05 — MAJOR: retroactive INVALID over EGRESS_AUTHORIZED; replayed grant resets Remaining

- **Commit:** `76b3be9d` `fix(futures): F-D-05 one-shot revalidation and grant replay semantics`
- **Authority:** D4-A3 §4.3 (VALID is a one-shot egress authorization; idempotent by grant identity), **A3-I4** (one final provider commit), **A3-I5** (post-commit updates are prospective), A3-I3 (exact grant only); SPEC §26 (first decision authoritative).
- **Files changed:** `reservation.go` (handleRevalidate consults `res.Grant.State` BEFORE applying outcomes: EGRESS_AUTHORIZED or FINAL-with-commit-marker ⇒ replay the retained commit exactly — original decision id + provenance, re-recorded, zero mutation, BEFORE the exactness check so a malformed payload can never retro-revoke; FINAL-without-marker ⇒ fail-closed INVALID without mutation; handleReservationRequest replays the STORED grant when the outcome record was evicted but the reservation lives — no re-evaluation, no Remaining reset, no fill bookkeeping loss), `one_shot_test.go` (new).
- **Tests:** `TestRevalidate_OneShotSurvivesOutcomeEviction` (outcome evicted at the 512 bound + authority tightened v5→v6 cap 3: VALID with the ORIGINAL commit decision `rs-1@5` provenance, state untouched, capacity retained, outcome re-recorded), `TestRevalidate_ExactnessMismatchNeverRetroInvalidatesAuthorized`, `TestRevalidate_FinalGrantIsNeverReAuthorized` (guard: stale revalidate of a contracted FINAL grant records fail-closed INVALID, no ghost effect, no re-authorization), `TestReservation_ReplayWithEvictedOutcomeNeverResetsRemaining` (Remaining 2 stays 2, FilledQty 3 preserved, same decision id, one record).
- **RED:** `go test ./futures/provider/ -run 'TestRevalidate_OneShot|TestRevalidate_ExactnessMismatch|TestReservation_ReplayWithEvicted'` → `expected: "VALID" actual: "INVALID"` (retro-invalidation of an authorized grant) and `no second decision is minted for a redelivered request` (re-grant path).
- **GREEN:** `go test ./futures/provider/` → `ok`.
- **Deviations:** none. `TestRevalidate_FinalGrantIsNeverReAuthorized` is already-green guard coverage (the defect it guards is unreachable through the unknown-grant path post F-D-03/F-D-04).

## Suite results (final, exact commands)

```
cd v3/sdk && GOTMPDIR=/home/kor/aranea/gotmp go test ./futures/...
→ ok × 13 packages (bars calendar domain gerardmm market marketctx obs operation provider strategies/s1 strategies/s2 strategy units), also verified with -count=1

cd v3/core && GOTMPDIR=/home/kor/aranea/gotmp go test ./internal/futuresvertical/... ./internal/functions/...
→ ok github.com/xKoRx/echo/v3/core/internal/futuresvertical
→ ok github.com/xKoRx/echo/v3/core/internal/functions
```

Central invariant (ZERO blind duplicate physical submit) untouched: no operation/**, no egress/submit paths modified; S12 suite green.

## Escalations

None open. One semantic interpretation was required and is documented as the F-D-01 deviation: GROUP_WEIGHTED typed universe = declared weights map (frozen A-R2 + Shot-1 tests) rather than the scope string; if the Primary Manager wants strict scope-string filtering for GROUP_WEIGHTED as well, that is a Shot-1 contract change, not a Shot-3 fix.
