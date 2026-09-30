# Lane C (operation package surface + projection seq) — Shot 3 remediation evidence

Worktree: `/home/kor/aranea/work/d5-shot3-20260929/wt-c-operation`, branch `shot3/lane-c-operation`.
Baseline before any change: `5d02adcf` clean; `cd v3/sdk && GOTMPDIR=/home/kor/aranea/gotmp go test ./futures/...` ok.
Shot 2 scratch reproducers were re-pointed to this worktree (copies in `/home/kor/aranea/gotmp/repro-lanec`, `/home/kor/aranea/gotmp/rg01-lanec`; originals untouched): all 6 `TestFC0x` PASS pre-fix (they encode the defect outcome as expectation), and all 6 FAIL post-fix (they consecrate the defect; the in-repo SAFE-outcome tests below are the regression truth). Process per finding: RED (captured) → minimal fix → GREEN → commit.

Commit series (all on `shot3/lane-c-operation`, no pushes, clean tree at end):
`1ae5e79e` F-C-01 · `a0c14119` F-C-02 · `dbf4fac0` F-C-03 · `78d725bb` F-C-04 · `50c37c8b` F-C-05 · `03736931` F-C-06 · `b782c56a` F-C-07 · `80bf4a44` F-C-08 · `8d087ccb` F-G-01.

---

## F-C-01 (BLOCKER) — cancel ACK/CANCELLED/EXPIRED without TERMINAL_EXECUTION_FINAL keep the executable claim

- Finding: `ComputeClaims` (operation/claims.go:170-198) filtered `isLiveOrderStatus` (:202-209), so a CANCELLED order retaining QExecMax>0 (kept deliberately by engine_inputs.go cancel-ack :624-665 / engine_inputs.go :549-557) stopped claiming: the post-ACK safety replan granted a replacement SELL, late Fill of the cancelled leg + replacement fill physically inverted the Operation (reproduced LONG x=2 → −2). A2-I3 double-spend.
- Authority: D4-A2 §4.2 (q_exec_max rules; "CANCELLED/EXPIRED sin TERMINAL_EXECUTION_FINAL conservan el remanente"; cancel request/ACK no reduce), A2-I3 (no local double-spend), A2-I8 (venue-authoritative release), §10 (cancel + fill race), W2/W3, EXP-04; D2-04 §3.2.
- Fix: the claim IS q_exec_max — `ComputeClaims` now claims every Order with QExecMax>0 regardless of lifecycle status; only finality (`applyExecutionFinality`) or the venue-authoritative negative semantics of REJECTED (which zeroes QExecMax by construction) drive it to 0. No second claim notion; the Order stays the local authority.
- FILLED-status decision per authority: a FILLED order with residue QExecMax>0 (venue FILLED without full fills) KEEPS claiming — D4-A2 §4.2: "la finality continúa gobernando la liberación de cualquier remanente no ejecutado". Covered in `TestComputeClaimsNonLiveOutstandingClaims`.
- Tests (v3/sdk/futures/operation/scenarios_test.go): `TestFC01_CancelAckKeepsClaimSafeLONG`, `TestFC01_CancelAckKeepsClaimSafeSHORT` (LONG+SHORT: EXIT → ForceClose (no second close, W2) → cancel ACK keeps claim 2 → no replacement close → MM re-claim envelope-denied → late Fill → exposure 0, no breach, forward correction CANCELLED→FILLED, termination converges), `TestComputeClaimsNonLiveOutstandingClaims` (TestComputeClaims family gains CANCELLED/EXPIRED/FILLED QExecMax>0 + REJECTED-0 cases).
- RED (`cd v3/sdk && GOTMPDIR=/home/kor/aranea/gotmp go test ./futures/operation -run 'TestFC01|TestComputeClaims' -v`), tail:
  ```
  Messages:   	no replacement SELL while the cancelled leg still holds the outstanding claim
  Error:      	"[{ord-2 ... FILLED 2 ...} {ord-3 ... CANCELLED 0 ...} {ord-4 ... PENDING_SUBMIT 0 ...}]" should have 2 item(s), but has 3
  --- FAIL: TestFC01_CancelAckKeepsClaimSafeLONG
  --- FAIL: TestFC01_CancelAckKeepsClaimSafeSHORT
  --- FAIL: TestComputeClaimsNonLiveOutstandingClaims
  ```
- GREEN (same command): `--- PASS` ×3 + `ok github.com/xKoRx/echo/v3/sdk/futures/operation`; full package ok.
- Files: v3/sdk/futures/operation/claims.go, v3/sdk/futures/operation/scenarios_test.go.
- Deviations: none (LiveOrderCount field name kept; comment documents the claims semantics).

## F-C-02 (MAJOR) — stale/duplicate OrderModifyObservation never re-grants superseded terms

- Finding: `handleModifyObservation` (engine_inputs.go:667-724) had no dedup by ActionID, no VenueStatus validation (REJECTED mutated terms), no terminal-aggregate guard (op.Status check missing, unlike handleOrderObservation:449). Reproduced QExecMax 4→2→1 while the venue held 4.
- Authority: D2-04 §5.1/§5.2 (replace_request_id identity; "modify nativo aceptado"; venue may duplicate acks), §5.7/I15 symmetry; D4-A2 §10 (a rejection preserves the prior state), §4.2 monotonicity.
- Fix: terminal-aggregate guard added (I8/I15 symmetry); `ModifyObsDedup` (runtime) absorbs already-applied ActionIDs (telemetry `order_observation_stale`); only `ACCEPTED|CONFIRMED` VenueStatus mutates terms, everything else is fail-visible `venue_anomaly` telemetry. Dedup is recorded only after guards pass, inside the Apply transaction.
- Tests: `TestFC02_StaleModifyObservationIgnored` (4→2→4; redelivered stale v1 stays 4; REJECTED-1 stays 4; terminal aggregate unmutated).
- RED tail: `Messages: stale observation must not regress accepted terms` → `--- FAIL: TestFC02_StaleModifyObservationIgnored`.
- GREEN: `--- PASS` + package ok.
- Files: v3/sdk/futures/operation/engine_inputs.go, runtime.go, engine.go, scenarios_test.go.
- Deviations: acceptance-status set chosen as ACCEPTED/CONFIRMED (parity with the cancel-ack convention in handleActionObservation:645).

## F-C-03 (MAJOR) — CLOSE/CLOSE_ALL(k+1) invalidates the deferred PendingNextCycleOpen

- Finding: a deferred next-cycle OPEN survived a same-cycle CLOSE/CLOSE_ALL and was materialized by `evaluateTerminality` when the current Operation turned TERMINAL — the closed cycle resurrected (ADM-03 violated; engine.go :474-481/:1035-1043).
- Authority: D2-04 §3.1 (reversal deferral; ADM-03 pending invalidation), D2-08 cycle semantics.
- Fix: in handleDelivery's REDUCE/CLOSE/CLOSE_ALL branch, a CLOSE/CLOSE_ALL for the deferred cycle's StrategyCycleSeq clears `PendingNextCycleOpen` (fail-visible `stale_admission` telemetry), symmetric with the existing PendingAdmission invalidation.
- Tests: `TestFC03_CloseInvalidatesDeferredNextCycleOpen` (defer → CLOSE_ALL → ForceClose+fill → TERMINAL leaves no pending admission).
- RED tail: `Messages: CLOSE_ALL(2) invalidates the deferred OPEN(2)` (Expected nil, got the deferred SignalDelivery) → `--- FAIL`.
- GREEN: `--- PASS` + package ok.
- Files: v3/sdk/futures/operation/engine.go, scenarios_test.go.
- Deviations: none.

## F-C-04 (MAJOR) — revalidate VALID on a dead order releases instead of authorizing

- Finding: `handleRevalidateResult` flipped RESERVED→EGRESS_AUTHORIZED before `authorizeGrantTarget`; for a dead target (order no longer PendingSubmit; M1 submit never published) the submit path silently no-op'd — grant EGRESS_AUTHORIZED, zero releases → reservation leaked account-wide forever (reproduced releases=0).
- Authority: D4-A2 §16.8 (authorization applies to a physically eligible target; dead target = zero side effect), §10 (dead orders release), A2-I4.
- Fix: the EGRESS_AUTHORIZED flip moved into `authorizeGrantTarget` success paths only; the submit path treats `meta == nil || order == nil || status != PENDING_SUBMIT` as dead → emits the owner-to-owner release (VENUE_FINALITY reason) and never publishes; the modify path keeps its existing dead-order release with the same non-authorizing semantics. Idempotent under redelivery (revalidate dedup + release dedup).
- Tests: `TestFC04_RevalidateValidOnDeadOrderReleases` (REJECTED order → late VALID → release emitted, no command, grant not authorized, redelivery inert).
- RED tail: `Messages: the dead order's reservation must be released, not authorized` → `--- FAIL`.
- GREEN: `--- PASS` + package ok.
- Files: v3/sdk/futures/operation/engine_inputs.go, scenarios_test.go.
- Deviations: none.

## F-C-05 (MAJOR) — accepted modify-decrease clears its ModifyIntent

- Finding: the decrease branch of `handleModifyObservation` left the pending `ModifyIntent` alive after applying the venue-accepted outcome, so `applyOrderAction`'s one-pending-modify guard (engine_inputs.go :905-906) silently swallowed every future MODIFY of that Order (zero effects; reproduced MODIFY 2→1 → zero effects). Also the action id derivation `repl:<order>:v<len(intents)+1>` recycled identities after the intent was cleared.
- Authority: D2-04 §5.2 (one pending modify per Order; ack resolves it); SPEC §3.4/§26 (stable per-action identity).
- Fix: decrease branch deletes the intent in the same Apply transaction that applies the outcome; action ids are per-owner monotonic (`ModifyActionSeq` → `repl:<order>:m<N>`). The monotonic id is a required consequence of F-C-02's ActionID dedup: with recycled ids, a NEW modify's ack would be absorbed as a duplicate, re-creating the lockout in another form.
- Tests: `TestFC05_ModifyIntentClearedAfterDecrease` (decrease 3→2 acked → intent cleared; second distinct modify publishes with a distinct id; its ack applies on its own identity).
- RED tail: `Messages: the applied outcome clears its ModifyIntent (F-C-05)` (Should be empty, but was map[ord-3:...]) → `--- FAIL`.
- GREEN: `--- PASS` + package ok.
- Files: v3/sdk/futures/operation/engine_inputs.go, runtime.go, scenarios_test.go.
- Deviations: the monotonic action-id fix is beyond the literal one-line intent clear — required for consistency with F-C-02, noted here per evidence mandate.

## F-C-06 (MAJOR) — delivery dedup survives materialization

- Finding: `materialize` wiped `st.DeliveryDedup` (engine.go :652), so the just-processed opening OPEN lost its marker: a transport redelivery re-entered handleDelivery as a same-cycle MANAGEMENT_SIGNAL and MM built an expansive ADD from a pure duplicate (D2-04 §5.1/§5.5 dedup-before-mutation violated; engine.go :439-442).
- Authority: D2-04 §5.1 (signal dedup key `(account_strategy_id, signal_id)`; replay never re-materializes), §5.5 horizon, §6.
- Fix: the materialize wipe removed; the dedup set survives (bounded by `MaxDeliveryDedupKeys`, §11 scoped eviction as before).
- Tests: `TestFC06_DeliveryDedupSurvivesMaterialize` (materialize → redelivered OPEN → `signal_duplicate` telemetry, no MM trigger, no ADD).
- RED tail: `Messages: the opening delivery dedup marker survives materialization (D2-04 §5.1)` (Should NOT be empty, but was map[]) → `--- FAIL`.
- GREEN: `--- PASS` + package ok.
- Files: v3/sdk/futures/operation/engine.go, scenarios_test.go.
- Deviations: none.

## F-C-07 (MAJOR) — reservation releases carry ReleasedQExecMax

- Finding: `emitRelease` left `ExposureReservationRelease.ReleasedQExecMax` zero: an accepted modify-decrease released the FULL grant while an executable remainder stayed live → account-wide under-reservation (D4-A2 A2-I4/W5). The wire field existed frozen on the branch base (wire.go, unchanged).
- Authority: D4-A2 A2-I4 (reservation completeness), W5 (modify decrease race), §10, §12 "Finality/modify path ... evidence/result que autoriza disminuir la reservation".
- Fix: the single release emission path stamps `ReleasedQExecMax` with the authoritative remaining q_exec_max observed for the Order at release time (MODIFY_DECREASE_ACK moves only the released delta; zero = no quantity evidence → provider fails closed for decrease acks; VENUE_FINALITY keeps full-release semantics per its reason — finality zeroes QExecMax anyway). Release CONSUMPTION untouched (Lane D owns it).
- Tests: `TestFC07_ReleaseCarriesQuantity` (decrease 2→1 releases exactly 1; TERMINAL_EXECUTION_FINAL releases 0); `TestEXP05_ModifyDecreaseReleasesReservation` corrected from the defect-consecrating full-release expectation to the quantity-accurate assertion.
- RED tail (`-run 'TestFC07|TestEXP05'`): `Messages: the release moves only the released delta, not the full grant (F-C-07)` expected 1 actual 0 → `--- FAIL` ×2 (TestFC07 + corrected TestEXP05).
- GREEN: `--- PASS` ×3 + package ok.
- Files: v3/sdk/futures/operation/engine_inputs.go, scenarios_test.go (wire.go NOT modified — field pre-existing).
- Deviations: none.

## F-C-08 (MAJOR) — revalidate conflict absorbed, not a job-wide poison

- Finding: a conflicting revalidate result (different ProviderDecisionID for an already-resolved grant) returned `errStatic` (engine_inputs.go :112-116) while admission conflicts use telemetry+absorb (engine.go :541-543): Apply failed, nothing persisted, redelivery hit the same conflict → failover loop of the whole job.
- Authority: SPEC §26 symmetry; engine.go admission-conflict precedent ("first recorded decision stays authoritative, late one is fail-visible stale input").
- Fix: conflict → `revalidate_conflict` telemetry + absorbed input, no state mutation.
- Tests: `TestFC08_RevalidateConflictIsAbsorbed` (VALID applied → conflicting INVALID → NoError, telemetry, grant stays EGRESS_AUTHORIZED, order untouched).
- RED tail: `Messages: a conflicting revalidate result must be absorbed, not poisoned` (Received unexpected error) → `--- FAIL`.
- GREEN: `--- PASS` + package ok.
- Files: v3/sdk/futures/operation/engine_inputs.go, scenarios_test.go.
- Deviations: none.

## F-G-01 (MAJOR) — owner-monotonic operation_event_seq across operations

- Finding: the engine restarted `operation_event_seq` at 0 per Operation (fresh OperationRuntime at materialize, engine.go :628/:649/:653) while the frozen projector guard is stale-safe strict-increase per owner_key (pgstore/store.go :87 = migration 066, frozen): op-2 with seq<op-1-max never applied; the row froze on op-1 TERMINAL during op-2 (D2-04 L252/357 violated). POC reproduced (rg01-poc): op-2 dropped until seq 48.
- Authority: D2-04 L252 (§6.3-B: the state owner seals a monotonic operation_event_seq on durable writes) + L357 (§8.5/§10: projections stale-safe by operation_event_seq). Minimal conformant mechanism: owner-level continuity persisted in the operation owner state; projector guard and migration 066 untouched (mandate).
- Fix: `OwnerState.OwnerEventSeq` watermark; `beginEvent` advances the watermark and mirrors it into the current aggregate's `Runtime.EventSeq`; `materialize` seeds the new runtime's EventSeq from the watermark. Every fact continues the per-owner monotonic series.
- Tests: engine — `TestFG01_ProjectionSeqMonotonicAcrossOperations` (op-1 to TERMINAL at seq N; op-2's first snapshot seq > N; later events keep advancing). Projector (TEST ONLY, no product code touched) — new file v3/futures-projector/core/projector/cross_operation_test.go, `TestFG01_CrossOperationSeqContinuity`: ported Shot 2 POC driving the REAL engine through two operations on one owner, feeding every fact through `projector.ApplyRecord` (memstore); asserts op-2's strictly-advancing snapshots APPLY and the row converges to op-2. Verified RED by stashing the engine fix: `--- FAIL: TestFG01_CrossOperationSeqContinuity`.
- RED (engine, `-run TestFG01`): `"2" is not greater than "2"` — op-2 projection seq must continue the owner watermark, never restart → `--- FAIL`.
- GREEN: both `--- PASS`; `cd v3/futures-projector && GOTMPDIR=/home/kor/aranea/gotmp go test ./...` ok.
- Files: v3/sdk/futures/operation/engine.go, runtime.go, scenarios_test.go; v3/futures-projector/core/projector/cross_operation_test.go (new, test-only).
- Deviations: the port is engine-driven end-to-end rather than a literal copy of the scratch POC — the literal POC hand-feeds facts to the projector only and therefore still "passes" post-fix (it exercises the frozen guard, not the producer); the in-repo port is the cross-operation regression that actually pins the corrected producer contract.

---

## Invariant checks

- EXP-04 (`TestEXP04_CancelRequestRace`), EXP-07 (`TestEXP07_ReplaceOverlap`), TERM-02 (`TestTERM02_TerminalGuards`, `TestTERM02_TerminalBlockedByPendingFinality`): PASS — full cancel+fill race conjunctions stay green with the F-C-01 claim semantics.
- ZERO blind duplicate physical submit: `publishSubmitCommand`/`publishModifyCommand` idempotence untouched; all M1 publications still flow only through `authorizeGrantTarget` at EGRESS_AUTHORIZED (TestReservationPipelineRevalidatesBeforeM1, TestRevalidateInvalidReleasesClaim, TestReservationDeniedInvalidatedGrantConvergesOrder green).
- S12: green via `v3/core` futuresvertical run below (s12_* live there); GerardMM golden: `v3/sdk/futures/gerardmm` ok.

## Suite results (exact commands)

```
cd v3/sdk && GOTMPDIR=/home/kor/aranea/gotmp go test ./futures/...
  → ok ×13 packages (operation, gerardmm, domain, provider, ...)

cd v3/futures-projector && GOTMPDIR=/home/kor/aranea/gotmp go test ./...
  → ok  adapters/pgstore, core/projector (incl. TestFG01_CrossOperationSeqContinuity)

cd v3/core && GOTMPDIR=/home/kor/aranea/gotmp go test ./internal/futuresvertical/... ./internal/functions/... ./internal/futuresruntime/...
  → ok  futuresvertical 18.753s (s12 suites), functions 0.163s, futuresruntime 0.020s
```

## Escalations

- None blocking. Observations for the Primary Manager (no action taken, out of lane scope):
  1. The projector/memstore stale guard drops EQUAL-seq sibling snapshots of one event (`>` semantics) while the futuresvertical FactsCollector applies equal-seq progressions (`<` only). The engine emits multiple OPERATION_SNAPSHOTs per event with evolving content; the last sibling of an event can therefore be dropped by 066 until the next event advances the seq. Pre-existing per-event latest-state semantics, untouched by mandate (066 frozen); flagging in case D wants a follow-up finding.
  2. `handleModifyObservation` still returns a hard error on `ValidateQuantity` failure of a venue observation (pre-existing poison-pill shape, same family as F-C-08 but not in the accepted register).
