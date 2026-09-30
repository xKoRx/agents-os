# Echo Futures — D5 ATP Final Matrix (Macro Shot 3, remediation complete)

> **AMENDED 2026-09-30 — FINAL GATE AMENDMENT** (MKT-07, TERM-03, F-MGR-02, F-MGR-03; Primary Manager gate). Amendment baseline: branch `feature/d5-shot3-remediation`, final SHA `e607b4183e041f8c7603d9b5d0db82c6f09d29a7` (prior `5f9fadde`, +3 commits, tree clean). The rows below reflect the amended tree; the amendment delta is marked per row.

**Baseline:** branch `feature/d5-shot3-remediation`, final SHA `5f9fadde190c3cd85637f746fd45bb703736a7f4` (`git rev-parse HEAD`, tree clean, all Shot 3 fixes merged).
**Method:** every PASS verdict is backed by at least one test that was executed green in this session on the final tree (package `-count=1` runs plus targeted `-run '<Regex>' -v` runs; exact commands under "Commands"). No Shot 1/2 PASS label was inherited.

## Verdict counts (115 rows)

| Verdict | Count (amended) |
|---|---|
| **PASS** | **113** |
| **FAIL** | **0** |
| **INCOMPLETE** | **0** (MKT-07 and TERM-03 closed by the amendment) |
| **DEFERRED_TO_D6** | **2** full rows (EXE-14, SCL-03) + deferred halves noted on REC-03, EXE-01/02/04/08, MKT-11/13, Budgets §20 |

Counting convention: REC-03 is counted once under PASS for the implemented software fail-visible seam; its physical checkpoint-lineage introspection half is DEFERRED_TO_D6 as instructed.

---

## Market identity and replay (MKT-01..16)

| ATP case | Verdict | Evidence (tests run green this session) | Note |
|---|---|---|---|
| MKT-01 canonical identity ≠ seq | PASS | `TestStreamSequencer_CanonicalIdentityDiffersFromSequence_MKT01` (sdk/futures/market); `TestFuturesMarketStream_CanonicalForwardAndSeqAssignment_MKT01` (core/functions) | Seq is transport position; canonical identity separate; no path treats `stream_seq` as semantic identity |
| MKT-02 same-seq conflict | PASS | `TestFuturesMarketAnalytics_SameSeqDifferentFactConflict_MKT02`; `TestFuturesMarketStream_ConflictFailsVisible_MKT02`; `TestStreamSequencer_RedeliveryConflictOnDigestMismatch_MKT02`; `TestDownstreamGuard_Scenarios_MKT02_MKT03` | `MARKET_IDENTITY_CONFLICT` fail-visible; no silent mutation |
| MKT-03 duplicate delivery | PASS | `TestFuturesMarketAnalytics_CanonicalRedeliveryNoOp_MKT03`; `TestFuturesMarketStream_DuplicateAbsorbedPreCanonical_MKT03`; `TestFuturesMarketAnalytics_CanonicalForward_RedeliveryNoDuplicateForward` | Pre-mutation NOOP guard; analytics/Strategy state unchanged |
| MKT-04 packet with N entries | PASS | `TestStreamSequencer_SourceIdentityDedupConsumesNoSeq_MKT04` | Class-B packet with 2 positional entries → 2 canonical events with distinct seq; equivalent-member replay absorbed pre-canonical, consumes no seq |
| MKT-05 legitimate identical trades | PASS | `TestStreamSequencer_LegitimateIdenticalTradesPreserved_MKT05`; `TestFuturesMarketStream_ClassCIngressIdentityOnly_MKT05` | Identity-only dedup for class C; no content-hash suppression |
| MKT-06 authority switch | PASS | `TestFuturesMarketStream_EpochBarrierDemotesAndSeeds_MKT06`; `TestCurrentStateLadders_EpochDemoteSeed_MKT06`; `TestBuilder_EpochDiscipline_MKT06`; `TestFuturesMarketAnalytics_EpochBarrierDiscardsForming_MKT06` | Same stream_id, new epoch, no Contract rollover; forming state discarded, current state seeded independently |
| MKT-07 rollover ≠ source switch | PASS (**amended**: was INCOMPLETE) | `TestFuturesVertical_MKT07_ContractRolloverDiffersFromSourceSwitch` (futuresvertical, executed green on the amended tree): Operation O live pinned to NQZ6; a serving-authority SOURCE SWITCH on the same contract leaves O live, pinned and TRADING (fresh quote → bounded add with A's identity); the owner mapping rolls NQ→NQH7: O stays pinned to A through the rollover and closes on A, and the new demand materializes on B (ContractSnapshot + pinned external ref + M1 commands carry B). Reuses the frozen pinning seams (`ResolveContract` at materialization, `PinnedBinding`); no rollover service, no migration, no new owner | Dedicated deterministic fixture executed on the final tree |
| MKT-08 crash/recovery ordering | PASS | `TestJournalBuilder_OrderAssertions`; `TestFuturesVertical_BridgeRestart_NoDuplicateSubmit`; `TestFuturesVertical_CoreRedelivery_Idempotent`; `TestFuturesMarketStream_RuntimeClockNeverRegresses` | Same accepted facts, same order, no duplicated canonical fact across restart/redelivery |
| MKT-09 late correction | PASS | `TestFuturesMarketAnalytics_LateCorrectionProjectionOnly_MKT09`; `TestBuilder_LateCorrectionWindow_MKT09`; `TestS1_AcS118_LateCorrection_DoesNotReevaluate`; `TestS2_A10_LateCorrection_NoReevaluation` | Projection moves to X′; prior decision on X retained; no retroactive Signal |
| MKT-10 ContextRead capture | PASS | `TestLiveScope_CaptureMemoizationSparseReadSet_MKT10` (sdk/futures/marketctx); `TestS12_LiveDecision_EvidenceFromJournal_ReplaysExactly` | Capture-as-consumed, dense ordinals, memoization, foreign-stream absent |
| MKT-11 exact replay context | PASS | `TestReplayScope_ExactReplay_MKT10_MKT11`; `TestS12_S1_ExactReplay_Golden_Breakout`; `TestS12_S2_ExactReplay_Golden_Pullback`; `TestS12_Backtest_DoubleRun_Deterministic` | Byte-identical replay incl. poisoned live state; physical recorded-run golden = D6 |
| MKT-12 missing/extra read | PASS | `TestReplayScope_MissingReadFailsVisible_MKT12`; `TestReplayScope_ExtraReadFailsVisible_MKT12`; `TestReplayScope_OrderMismatchFailsVisible`; `TestS12_ReplayFailures_FailVisible` | F-TOP-02 fixed on Shot 3: typed HARD replay failures surface (no silent NotReady downgrade); no fallback to latest state |
| MKT-13 replay anchor | PASS | `TestReplayAnchor_FailVisible_MKT13`; `TestS12_ReplayAnchor_MissingCorruptWrongDigest`; `TestRunManifest_ImmutableInitial_DigestVerified`; `TestS12_RunJournal_OrderedRecordingLive` | Missing anchor / corrupt digest fail-visible; anchor sealed in live manifest; physical golden run = D6 |
| MKT-14 timer close without next tick | PASS | `TestFuturesMarketAnalytics_BarClosedDeliveryOnNaturalClose_MKT01_MKT14`; `TestBuilder_NaturalCloseAndTimerClose_MKT14` (sdk/futures/bars); `TestFuturesVertical_TimerFiresAtBoundary_BoundedQuiescence` | **Changed vs Shot 2 (was FAIL F-A-01/02)**: real SendAfter timers with generation cancel; bar closes on time, delivered on the production path |
| MKT-15 internal break grid | PASS | `TestFuturesMarketAnalytics_InternalBreakTruncatesAndResumesGrid_MKT15`; `TestBuilder_InternalBreakTruncation_MKT15` | **Changed vs Shot 2 (was FAIL mechanism)**: truncation at break, no bars during break, same grid resumes, no reset. Open note (F-B-06, left unfixed by decision): the analytics side fires the BreakEnd session transition (`futures_market_analytics.go` `deliver(..., calendar.TransitionBreakEnd)`), but no strategy module ever receives/consumes a BreakEnd delivery — bar-grid semantics unaffected; strategy-side BreakEnd delivery remains an open gap |
| MKT-16 stale last-known ≠ READY | PASS | `TestFuturesMarketAnalytics_ReadinessMirroredFromFeed_MKT16`; `TestFuturesMarketStream_ReadinessEventsInOrder_MKT16`; `TestCurrentStateLadders_MonotonicInsideEpoch_MKT16`; `TestS1_NotReady_FailClosedForNewRisk` | New Signals blocked while not-ready; stale exposed as-of. **Amended (F-MGR-03)**: the QUOTE ladder now has a producer path — stale/last-known quotes are absorbed fail-visibly by the owner before any MM evaluation (`TestQuoteNotif03_StaleAndFutureEvidenceAbsorbed`, `TestQuoteTrigger_NotReadyOrMissingMarkFailsClosed`); readiness ladder remains feed-authority |

## Calendar/session (CAL-01..04)

| ATP case | Verdict | Evidence | Note |
|---|---|---|---|
| CAL-01 DST wall-clock | PASS | `TestNamedTradingWindow_DSTWallClockPreserved_CAL01` (sdk/futures/calendar) | IANA zone resolution, no fixed UTC offset |
| CAL-02 holiday / early close | PASS | `TestResolver_DatedOverrideTruncatesAvailability_CAL02`; `TestBuilder_HolidayAndEarlyClose` (sdk/futures/bars) | Dated override truncates; no hardcoded holiday logic |
| CAL-03 account day ≠ session date | PASS | `TestResolvedSession_SessionDateDiffersFromCivilDate_CAL03`; `TestFuturesVertical_AccountDayTargetExit` (vertical, production path) | GerardMM economics key on account day; strategy bars/session on exchange calendar |
| CAL-04 unresolved calendar | PASS | `TestResolver_UnresolvedCalendarFailsClosed_CAL04` | Fail closed, no default 24x7. Calendar hot path (Shot 2 F-A-03/04) now fixed: `TestFuturesMarketAnalytics_CalendarUpsertRearmsSessionChain`, `TestFuturesMarketAnalytics_CalendarAuthorityDeterministic` |

## S1 (S1-01..13)

| ATP case | Verdict | Evidence | Note |
|---|---|---|---|
| S1-01 exact opening range | PASS | `TestS1_AcS101_ExactOpeningRange_FreezeArms` (sdk/futures/strategies/s1) | OR extrema of the six bars only |
| S1-02 OR incomplete | PASS | `TestS1_AcS102_IncompleteRange_InvalidDay` | Missing/invalid bar → no OPEN |
| S1-03 LONG strict breakout | PASS | `TestS1_AcS103_StrictCrossing_OnlyExactBreak` | Touch at boundary does not open; exactly one LONG OPEN with frozen provenance |
| S1-04 SHORT strict breakout | PASS | `TestS1_AcS105_ShortStop_PremarketHighThroughPreviousClosed` (SHORT opens on strict cross below OR low 99.25 via trade at 99); strictness-at-boundary asserted on the long mirror in `TestS1_AcS103_StrictCrossing_OnlyExactBreak` | Symmetric touch-side equality for the short boundary is exercised via the shared strict-crossing predicate, not asserted with its own dedicated short-side touch fixture |
| S1-05 LONG technical stop | PASS | `TestS1_AcS104_LongStop_PremarketLowThroughPreviousClosed` (+ forming-bar exclusion half in same test and `TestS1_AcS106_FormingBarExcluded_FromStop`) | min low P..previous closed; forming excluded |
| S1-06 SHORT technical stop | PASS | `TestS1_AcS105_ShortStop_PremarketHighThroughPreviousClosed` | max high over same interval = 104.00 |
| S1-07 missing premarket config | PASS | `TestS1_AcS107_MissingPremarketConfig_FailClosed`; `TestS1_PremarketAfterOpen_FailClosed` | Fail closed, no invented hour |
| S1-08 stop adverse-side validation | PASS | `TestS1_AcS108_StopValidation_FailClosed` | Setup invalid, no OPEN |
| S1-09 technical stop close | PASS | `TestS1_AcS109_StopHitClose_CloseAllOnce` | CLOSE_ALL once; no double-fire |
| S1-10 back-inside close | PASS | `TestS1_AcS110_BackInsideClose_ReArms` | Per frozen S1 semantics; same bar cannot also open |
| S1-11 re-arm | PASS | `TestS1_AcS112_WaitRearm_OnlyClosedInsideRange` | Re-arm only at the defined later bar |
| S1-12 new day reset | PASS | `TestS1_AcS113_NewDayReset_ClosesOpenCycleFirst` | Required CLOSE_ALL before reset; clean new-day OR. Shot 2 F-B-01 (CycleOpen invisible) fixed: `TestS1_CycleOpen_ModuleOutcomeAcrossLifecycle` |
| S1-13 no profit target | PASS | `TestS1_AcS115_NoProfitTargetField` | Technical stop present, no target field. Shot 2 F-B-03 (stop grid gaps) fixed: `TestS1_ContextGridGap_FailClosed_NoStop` |

## S2 (S2-01..09)

| ATP case | Verdict | Evidence | Note |
|---|---|---|---|
| S2-01 warm-up | PASS | `TestS2_S201_Warmup`; `TestS2_Indicators_ExactBoundaries` (sdk/futures/strategies/s2) | 50 insufficient / 51 enables trend; 19 insufficient / 20 enables Bollinger |
| S2-02 H4 trend both directions | PASS | `TestS2_S202_TrendBothDirections` | SMA50/current-vs-previous both ways |
| S2-03 same-boundary H4 visibility | PASS | `TestS2_S203_SameBoundaryH4Visibility` | Previous eligible H4 used; new H4 visible next 5m decision |
| S2-04 LONG pullback OPEN | PASS | `TestS2_A1_LongPullbackOpen` (+ negatives `TestS2_A2..A5`) | One LONG OPEN, exact technical stop |
| S2-05 SHORT pullback OPEN | PASS | `TestS2_A8_ShortPullbackOpen` (+ `TestS2_A9_ShortTouchWithoutRecovery`) | Symmetric |
| S2-06 basis return close | PASS | `TestS2_S206_BasisReturnClose_NeverATarget` | CLOSE_ALL both directions; basis never a target field |
| S2-07 trend invalidation close | PASS | `TestS2_S207_TrendInvalidationClose` | CLOSE_ALL |
| S2-08 re-arm | PASS | `TestS2_A7_BasisReturn_ReArm`; `TestS2_A6_DuplicatePullbackWhileDisarmed` | No duplicate OPEN before exact re-arm conditions |
| S2-09 no Gerard target | PASS | `TestS2_A1_Details_NoTargetField`; `TestS2_S206_BasisReturnClose_NeverATarget` | Signal details and GerardMM input carry no monetary target |

## Signal/fan-out/admission (SIG, ADM)

| ATP case | Verdict | Evidence | Note |
|---|---|---|---|
| SIG-01 deterministic signal identity | PASS | `TestDeriveSignalID_DeterministicIdentity_Scenarios` (sdk/futures/domain); `TestS1_AcS116_DeterministicReplay_SameSignals`; dedup keyed on `signal_id` in `TestFuturesSignalFanout_OpenDelivery_EnabledOnly` | Same run/trigger/eval → same id across restart/replay |
| SIG-02 0..N ordered signals | PASS | `TestFuturesStrategyEngine_EvaluationSignalEgressAndFanoutRouting` (core/functions); `TestS12_RunJournal_OrderedRecordingLive` | Stable order preserved, incl. no-signal evaluation |
| SIG-03 disabled binding | PASS | `TestFuturesSignalFanout_OpenDelivery_EnabledOnly`; `TestFuturesSignalFanout_ManagementClose_ReachesDisabledBinding` | No OPEN to disabled binding; management close still reaches |
| SIG-04 target-set config race | PASS | `TestFuturesSignalFanout_TargetSetVersionRace` | Deterministic target set + final local guard; older sets absorbed (`TestFuturesStrategyEngine_ConfigCycleActivation`). Shot 2 F-B-05 (foreign/expired signal accepted) fixed: `TestS1_LateAdmission_ExpiredSignal_Absorbed_NoHardError` |
| ADM-01 OPEN ALLOW | PASS | `TestADM01_OpenAllowMaterializesOnce` (sdk/futures/operation); `TestFuturesOperationFn_OpenAllowPublishesCommand` | One materialization after remaining guards; no Operation before ALLOW |
| ADM-02 OPEN DENY | PASS | `TestADM02_OpenDenyLeavesNoOperation`; `TestFuturesVertical_ProviderDeny` | Pending cleared, decision durable, zero Operation |
| ADM-03 CLOSE invalidates pending | PASS | `TestADM03_CloseInvalidatesPendingAdmission`; `TestFC03_CloseInvalidatesDeferredNextCycleOpen` | Shot 2 F-C-03 fixed: late ALLOW no-op after CLOSE |
| ADM-04 OPEN(k+1) supersedes k | PASS | `TestADM04_NextCycleSupersedesPending` | Only current cycle can materialize |
| ADM-05 no generic backlog | PASS | `TestADM05_NoBacklogCycleLag` | Bounded fail-closed cycle lag; no unbounded queue |

## GerardMM economics (MM-01..18)

| ATP case | Verdict | Evidence | Note |
|---|---|---|---|
| MM-01 evaluation day 1 | PASS | `TestEntry_EvaluationDay1AndDay2` (sdk/futures/gerardmm) | SL=2000, TP=1500 exact |
| MM-02 evaluation day 2 | PASS | `TestEntry_EvaluationDay1AndDay2` | Same expected values |
| MM-03 unconfigured day | PASS | `TestEntry_UnconfiguredDay3FailsClosed` | Zero new risk, explicit fail-closed reason |
| MM-04 unresolved funded config | PASS | `TestEntry_FundedUnresolvedFailsClosedAndConfiguredResolves` | No invented defaults |
| MM-05 account-day objective | PASS | `TestFormulas_ObjectiveAndHeadroom` | 750 PnL / 1500 TP → remaining 750 |
| MM-06 target reached before entry | PASS | `TestEntry_ObjectiveReachedBeforeEntryBlocked` | No new-risk Order |
| MM-07 loss headroom | PASS | `TestEntry_PriorLossShrinksPriorProfitDoesNotEnlarge`; `TestEntry_ProviderHardHeadroomConstrains` | −600 → 1400 headroom |
| MM-08 prior profit doesn't enlarge SL | PASS | `TestEntry_PriorLossShrinksPriorProfitDoesNotEnlarge` | +1000 → 2000, not 3000 |
| MM-09 account-wide PnL moves objective | PASS | `TestFormulas_ObjectiveAndHeadroom` + `TestAccountEconomicsTrigger_BelowObjectiveNoTermination` (economics delivered as account-wide `AccountDayCurrentPnLMoney` input; no portfolio reconstruction exists in the module) | Objective varies with account-wide P_day by input contract; MM holds no per-Operation portfolio state |
| MM-10 dynamic target mark | PASS | `TestTargetMarkDerivedAndNeverPersisted`; quote-evidence sizing `TestEntry_LongSizesFromAsk`/`TestEntry_ShortSizesFromBid` | Formula + conservative rounding; never persisted authority. **Amended (F-MGR-03)**: the QUOTE notification seam now serves authoritative/current quote evidence through the decision-scoped MarketContext (`TestQuoteNotif01_InvokesMMWithScopedMid`, vertical quote E2E); real external feed certification stays D6 |
| MM-11 initial sizing exactness | PASS | `TestEntry_LongSizesFromAsk`; `TestEntry_ShortSizesFromBid`; exact-quantity invalid→deny via `TestEXP08_NoSilentResize` (sdk/futures/operation); production sizing path `TestFuturesVertical_PartialFill` | No silent clipping |
| MM-12 adverse branch bounded | PASS | `TestAdverseBranchBoundedNoTopUp`; **amended (F-MGR-03)**: `TestQuoteTrigger_AdverseThresholdExactlyOneBoundedAdd` + vertical quote E2E | Bounded exact adds, branch lock, no inter-Operation state; reachable on the QUOTE trigger between Fill/OrderFinal events |
| MM-13 favorable branch bounded | PASS | `TestFavorableBranchBounded`; **amended (F-MGR-03)**: `TestQuoteTrigger_FavorableThresholdExactlyOneBoundedPyramid` + vertical favorable E2E | Symmetric; one bounded pyramid per ordinal, branch-locked |
| MM-14 partial add no top-up | PASS | `TestAdverseBranchBoundedNoTopUp` (partial fill consumes the ordinal; no top-up while executable quantity remains) | Per GMM-I10 |
| MM-15 protective stop never loosens | PASS | `TestProtectiveStopNeverLoosens`; `TestProtectiveBreakEvenAfterFavorableFill` | Only toward lower risk |
| MM-16 provider denied add | PASS | `TestProviderDeniedAddLocksNewRisk`; revalidation conflict absorbed `TestFC08_RevalidateConflictIsAbsorbed` (+ malformed-observation variant `TestFC08_Dup_MalformedModifyObservationAbsorbedNotPoison`, Shot 3 F-C-08) | No physical command; new-risk progression blocked |
| MM-17 profit termination precedence | PASS | `TestProfitTerminationPrecedenceOverAdd`; `TestAccountEconomicsTrigger_ProfitCrossingExitsWithoutNewFacts`; production `TestFuturesVertical_EconomicsUpdateCrossingTP_ExitsWithoutNewFacts` | Termination wins, no add |
| MM-18 stale economic snapshot | PASS | `TestEntry_StaleOrMissingEconomicsFailsClosed`; `TestAccountEconomicsTrigger_StalePnLFailClosed`; keyed freshness `TestEconUpdate04_NotFreshDeliveryFailsClosed` | New risk fail closed; exit path stays available (`TestStrategyCloseWinsWithoutEconomics`). Shot 2 F-E-01..04 fixed: economics trigger live, `TestEntry_NoRuleSetAuthorityDeniesNewRisk`/`TestRuleSetAvailable_FalseKeepsExitWorking`, `TestAdd_PerOrderCapRespectedExactQuantityEligible`, executable-side sizing |

## Local executable exposure (EXP-01..08)

| ATP case | Verdict | Evidence | Note |
|---|---|---|---|
| EXP-01 two concurrent REDUCE | PASS | `TestEXP01_TwoConcurrentReduces`; `TestComputeClaimsNonLiveOutstandingClaims` | Combined reachable q_exec_max ≤ reducible exposure, incl. CANCELLED/EXPIRED claims (Shot 2 F-C-01 accounting fixed) |
| EXP-02 EXIT + ForceClose | PASS | `TestEXP02_ExitPlusForceClose` | No second full close |
| EXP-03 partial fill transfers claim | PASS | `TestEXP03_PartialFillTransfersClaim`; `TestFillTransfer_NoEnvelopeWideningAndIdempotent` (sdk/futures/provider) | Exact transfer, no optimistic release |
| EXP-04 cancel request race | PASS | `TestEXP04_CancelRequestRace`; `TestFC01_CancelAckKeepsClaimSafeLONG`/`TestFC01_CancelAckKeepsClaimSafeSHORT` | **Changed vs Shot 2 (was FAIL F-C-01)**: claim held until authoritative finality/quantity reduction; late fill applied |
| EXP-05 modify decrease | PASS | `TestEXP05_ModifyDecrease`; `TestFC05_ModifyIntentClearedAfterDecrease`; `TestFC07_ReleaseCarriesQuantity`; `TestRelease_ModifyDecreaseAckWithoutQuantityEvidenceFailsClosed` (sdk/futures/provider) | **Changed vs Shot 2 (was FAIL F-C-07)**: release now fail-closed without quantity evidence; quantity-carrying ack releases |
| EXP-06 modify increase | PASS | `TestEXP06_ModifyIncrease` | Delta passes local safety + provider reservation before authorization |
| EXP-07 replace overlap | PASS | `TestEXP07_ReplaceOverlap`; stale-observation half `TestFC02_StaleModifyObservationIgnored` | Envelope covers both legs until old leg final |
| EXP-08 no silent resize | PASS | `TestEXP08_NoSilentResize` | Deny; no auto-reduced command |

## Provider account-wide capacity (PRV-01..11)

| ATP case | Verdict | Evidence | Note |
|---|---|---|---|
| PRV-01 GROSS reservation | PASS | `TestReservation_GrossSerializedRace`; `TestCapacityScopedEnvelope_Gross` (sdk/futures/provider) | Serialized owner prevents over-cap; account-wide envelope unchanged by scoped caps |
| PRV-02 NET_ABS opposite exposure | PASS | `TestReservation_NetAbsOppositeExposure`; `TestCapacityScopedEnvelope_InstrumentNetAbs` | Unsafe exact grant denied under valid worst-case ordering |
| PRV-03 exits under NET_ABS | PASS | `TestReservation_NetAbsOppositeExposure`; `TestCapacityScopedEnvelope_ProductGroupNetAbs`; `TestReservation_GroupWeighted_NoImplicitCrossProductNetting` | Reducing orders participate in the envelope regardless of EXIT label |
| PRV-04 GROUP_WEIGHTED | PASS | `TestReservation_GroupWeighted`; `TestWeightedGroupEnvelope_Formulas`; `TestCapacityScopedEnvelope_GroupWeightedGross`/`_GroupWeightedNetAbs`/`_CrossScopeCoexistence` | Exact typed weighted cap; **Shot 2 F-D-01 (scope dimension) fixed** |
| PRV-05 fill reservation transfer | PASS | `TestFillTransfer_NoEnvelopeWideningAndIdempotent` | Fill consumes reservation without widening |
| PRV-06 stale grant vs new RuleSet | PASS | `TestRevalidate_CurrentAuthorityWins`; `TestFuturesVertical_StaleGrantInvalidation` | Final authority wins; invalid grant never crosses M1 |
| PRV-07 revalidation always traverses owner | PASS | `TestReservationPipelineRevalidatesBeforeM1` (sdk/futures/operation) | No local-skip optimization |
| PRV-08 egress authorization boundary | PASS | `TestRevalidate_ValidIsTheEgressAuthorizationPoint`; `TestNoEgressCommittedNaming` | `egress_authorized` only; nothing names `egress_committed`; not yet physically submitted |
| PRV-09 position mismatch | PASS | `TestPhysicalUntrustedCutsOnlyExpandingGrants` | New risk fail closed where trust requires; no Position→Operation attribution |
| PRV-10 cap lowered below exposure | PASS | `TestCapLoweredBelowExposure` | Enlarging risk denied; over-limit visible; no auto liquidation (`TestDailyLossFlattenOnlyWhenDeclared`) |
| PRV-11 complete RuleSet read-only to MM | PASS | `TestRuleSetStoredComplete`; `TestTombstonedRuleSetDeniesAuthority` | Full RuleSet visible read-only; provider owner remains authority. Shot 2 F-D-02/04/05 fixed: `TestRelease_ModifyDecreaseAckWithoutQuantityEvidenceFailsClosed`, `TestRevalidate_OneShotSurvivesOutcomeEviction`, ghost-route `TestGhostOwner_*`, contract `TestReservations_ContractAcrossAllFullReleasePaths` |

## ForceClose and terminality (TERM-01..05)

| ATP case | Verdict | Evidence | Note |
|---|---|---|---|
| TERM-01 ForceClose is intent | PASS | `TestFuturesVertical_ProviderForceClose` (intent recorded, never instant terminality, real safety exit through M1); `TestTerminalViaMMIntent`; `TestForceCloseTriggerFanout` (sdk/futures/provider) | Non-terminal until guards complete |
| TERM-02 terminal guards | PASS | `TestTERM02_TerminalGuards`; `TestTERM02_TerminalBlockedByPendingFinality` (sdk/futures/operation) | Each missing guard independently blocks |
| TERM-03 bridge down | PASS (**amended**: was INCOMPLETE) | `TestFuturesVertical_TERM03_ForceCloseWhileBridgeDown` (futuresvertical, executed green on the amended tree): active Operation + nonzero exposure + SimExecution edge NOT READY (`Adapter.SimulateDisconnect`) + ForceClose → termination intent persists (never instant terminality), NO synthetic success/fabricated Fill/blind submit (exposure + venue order counts unchanged, the in-flight command refused fail-visibly), readiness condition visible. Reconnect → reconciliation barrier FIRST (frozen 11-step order), the journaled cancel reconciled against the physical venue state, at-least-once M1 topic replay continues the closure → TERMINAL(SAFETY_FLATTEN), zero exposure, exactly one exit fill. EXE-09/restart tests reused as infrastructure, not as substitutes | Exact SimExecution integration evidence executed on the final tree; harness seam fix: the events→Core finality surface no longer fabricates TERMINAL_EXECUTION_FINAL for an order the venue never saw (fabricated finality released the claim and looped the §19 safety replan against a dead edge) |
| TERM-04 direction immutable | PASS | `TestTERM04_DirectionImmutableOnBreach` | Breach visible, direction unchanged, no synthetic reversal |
| TERM-05 terminal not revived | PASS | `TestTERM05_TerminalNotRevived`; `TestTerminalOperationAlwaysNoAction` (sdk/futures/gerardmm) | Late physical fact preserved; aggregate stays terminal |

## Execution M1/M2 (EXE-01..14)

| ATP case | Verdict | Evidence | Note |
|---|---|---|---|
| EXE-01 M1 state/command atomicity | PASS | `TestFuturesVertical_BridgeRestart_NoDuplicateSubmit`; `TestFuturesVertical_CoreRedelivery_Idempotent`; `TestFuturesVertical_FactsRedeliveryCatchUp`; `TestReservationPipelineRevalidatesBeforeM1`; `TestF4_PreTransportCrashRecoveryDoesNotLivelock` | No visible command without committed state; no duplicate from recovery. Real Kafka EXACTLY_ONCE/read_committed config behavior = D6 (ATP §15); offset-commit/at-least-once redelivery is seam-tested only (see F-F-02 note) |
| EXE-02 sim normal submit | PASS | `TestEXE02_SimNormalSubmit` (futures-bridge/internal/session) | Full path to one physical-sim order; transport = in-process seam (`TestF2_ConsumerConfigNoSkipNoAutoCommit` etc.), real broker = D6 |
| EXE-03 fast MARKET fill before ACK | PASS | `TestEXE03_FillBeforeACK` | Fill preserved and correlated; state converges |
| EXE-04 side effect then crash | PASS | `TestEXE04_SideEffectThenCrashSuppressesDuplicate`; `TestF4_PreTransportCrashRecoveryDoesNotLivelock` | Same client_order_id reconciled; second submit suppressed. Real adapter = D6 |
| EXE-05 ambiguous submit | PASS | `TestEXE05_AmbiguousSubmitBlocksNewRisk`; `TestF1_NewSubmitWhileAmbiguousNotTransmitted` | **Changed vs Shot 2 (was FAIL F-F-01)**: journal AMBIGUOUS, new risk OFF, no blind retry, no new transmit under ambiguity |
| EXE-06 definite reject | PASS | `TestEXE06_DefiniteReject` | Terminal per adapter contract; no fabricated fill |
| EXE-07 cancel/fill race | PASS | `TestEXE07_CancelFillRace` | Finality waits for authoritative terminal evidence + executions |
| EXE-08 replace | PASS | `TestEXE08_ReplaceStableActionID` | Stable action IDs, exact physical identities, no hidden atomicity claim. Selected real adapter capability = D6 |
| EXE-09 reconnect barrier | PASS | `TestEXE09_ReconnectBarrierOrderAndGating` | New risk OFF until full reconciliation; no auto-resubmit |
| EXE-10 manual order/activity | PASS | `TestEXE10_ManualActivityIsObservationOnly`; `TestF3_UnknownLiveOrderQuarantinedFailVisible` | Observation/mismatch only; no attribution |
| EXE-11 duplicate fill realtime/history | PASS | `TestEXE11_DuplicateFillRealtimeHistory` | One fill fact per native execution identity (Shot 2 F-F-06 residue closed; cross-restart variant also green in `TestFuturesVertical_BridgeRestart_NoDuplicateSubmit`) |
| EXE-12 adapter without stable execution identity | PASS | `TestEXE12_UnknownCapabilityFailsExactGate` | Exact eligibility false; no heuristic identity |
| EXE-13 hot binding change | PASS | `TestEXE13_HotBindingChangePinsLiveOrder`; `TestDefenceInDepth_AccountMismatchDropped` | Old order on old pinned binding; no silent remap |
| EXE-14 double-owner detection | DEFERRED_TO_D6 | Gate is D6 operational per ATP. Partial config-level evidence exists green: `TestOptionsValidate_Table` case `duplicate_account_is_double_owner` (futures-bridge/core/config) | Config reject is tested; operational fencing/telemetry = D6 |

## Recovery / projection (REC-01..04)

| ATP case | Verdict | Evidence | Note |
|---|---|---|---|
| REC-01 Core normal restart | PASS | `TestFuturesVertical_BridgeRestart_NoDuplicateSubmit`; `TestFuturesVertical_CoreRedelivery_Idempotent`; `TestFuturesVertical_FactsRedeliveryCatchUp`; `TestFuturesOperationFn_ForceCloseAndTerminality` (state rehydration) | Checkpoint/Kafka authority; PG projection never a recovery authority |
| REC-02 projector idempotency | PASS | `TestRedeliverySameBatchIdenticalState`; `TestStaleSnapshotNoOp`; `TestCatchUpOutOfOrderConvergence`; `TestConsumerLevelRedeliveryNoOpThroughPipeline`; `TestFillDedupOnIdentity`; `TestFG01_CrossOperationSeqContinuity` (futures-projector/core/projector) | One logical row/fact; stale `operation_event_seq` ignored. Known frozen-constraint limitation (migration 066): equal-seq sibling snapshots of one event can be dropped until the next event; converges; documented (`cross_operation_test.go`) |
| REC-03 cold recovery missing evidence | PASS (software seam) / DEFERRED_TO_D6 (physical) | `TestREC03_ColdRecoveryInjection_PriorEvidenceWithoutContinuity`; `TestREC03_ColdRecoveryInjection_ContinuityMismatch`; `TestREC03_ContinuityPinPasses`; `TestREC03_FreshDeploymentPasses`; `TestREC03_SeamPrecedesComposition` (core/internal/futuresruntime/recovery_test.go) | Fail-visible `COLD_RECOVERY_REQUIRED`, no reconstructed trading state. **Changed vs Shot 2 (was INCOMPLETE F-G-08)**: software fail-visible seam now implemented and tested. Physical checkpoint-lineage introspection = D6 |
| REC-04 run provenance isolation | PASS | `TestS12_REC04_RunProvenanceIsolation`; `TestS12_Backtest_DoubleRun_Deterministic` | LIVE/REPLAY/BACKTEST facts cannot cross-contaminate |

## Scale / Budgets

| ATP case | Verdict | Evidence | Note |
|---|---|---|---|
| SCL-01 200-account fan-out (structural) | PASS | `TestFuturesVertical_FanoutN200_Structural`; `TestFuturesSignalFanout_Scale_StructuralN200`; `TestPinAccountStrategyIDCorrelationOnly` | One evaluation, one Signal, one shared computation, 200 deliveries, 200 independent M1 commands; no 200x market multiplication. Numeric measurement = D6 |
| SCL-02 account isolation | PASS | `TestFuturesVertical_FanoutN200_Structural` (per-account owners materialize/work independently); `TestDefenceInDepth_AccountMismatchDropped` (bridge); `TestGhostOwner_ReservationWithUnroutableStrategyIsAbsorbed` (provider) | Heavy/blocked account cannot mutate another account's state or reservations |
| SCL-03 reconnect storm | DEFERRED_TO_D6 | Gate is D6 per ATP; D5-side bounded-reconciliation evidence: `TestEXE09_ReconnectBarrierOrderAndGating`, `TestFuturesVertical_BridgeRestart_NoDuplicateSubmit` | Storm-scale latency/resource targets measured in D6 |
| Budgets §20 (obs points) | PASS (structural) / measurement DEFERRED_TO_D6 | `TestFuturesVertical_ObsBudgetPointsFiredThroughProductionPath` | Obs points wired and fired through the production path; numeric latency/perf measurement = D6 |

---

## Verdicts that changed vs the Shot 2 matrix

- **MKT-14: FAIL → PASS** — F-A-01/02 fixed: real timer scheduling (SendAfter + generation cancel/replace); green through unit, bar-builder, and the production vertical path.
- **MKT-15: FAIL (mechanism) → PASS** — F-A-03 fixed: deterministic calendar authority + session-chain re-arm; break truncation/resume green. Caveat: strategy-level BreakEnd delivery (F-B-06, MINOR) left unfixed by decision — noted on the row.
- **Calendar hot path (CAL family note): FAIL → PASS** — calendar upsert re-arms session chain deterministically on the hot path.
- **MKT-12 loudness (F-TOP-02): FAIL → PASS** — typed HARD replay failures now surface instead of silently downgrading to NotReady.
- **S1: 11/13 → 13/13** — F-B-01 CycleOpen outcome (`TestS1_CycleOpen_ModuleOutcomeAcrossLifecycle`) and F-B-03 grid-gap fail-closed (`TestS1_ContextGridGap_FailClosed_NoStop`) fixed.
- **SIG: 3/4 → 4/4** — F-B-05 fixed: late/expired signal absorbed without hard error.
- **ADM: 4/5 → 5/5** — F-C-03 fixed: deferred OPEN invalidated by CLOSE (`TestFC03_CloseInvalidatesDeferredNextCycleOpen`).
- **EXP: partial FAIL → 8/8** — F-C-01 (cancel-ack claim safety, non-live outstanding claims accounting) and F-C-07 (release fail-closed without quantity evidence) fixed.
- **PRV: partial FAIL → 11/11** — F-D-01 (scope-aware capacity), F-D-02 (release fail-closed), F-D-04 (reservation contraction/ghost-route contract), F-D-05 (one-shot revalidate survives eviction) fixed.
- **MM: 14/18 → 18/18** — F-E-01 (economics trigger / live TP), F-E-02 (RuleSetAvailable fail-closed with exit kept alive), F-E-03 (per-order caps on adds), F-E-04 (executable-side sizing) fixed.
- **EXE: partial FAIL → 13 PASS + EXE-14 D6** — F-F-01 (ambiguous-submit new-risk gate + no new transmit) and F-F-06 residue (duplicate fill identity across restart) fixed.
- **REC-03: INCOMPLETE → PASS (software seam)** — implemented as a software fail-visible seam with tests (`core/internal/futuresruntime/recovery_test.go`); physical checkpoint-lineage introspection stays DEFERRED_TO_D6.
- **FC-08 poison loop (F-C-08) and FG-06 quarantine (F-G-06)** — new Shot 3 fixes, both green (`TestFC08_Dup_MalformedModifyObservationAbsorbedNotPoison`, `TestFG06_UnattributableOperationEventQuarantinedNotPublished`).

## Standing open items (reflected in rows above)

1. **REC-03 physical lineage = D6** (software seam PASS).
2. **F-F-02**: real-Kafka at-least-once redelivery/commit semantics are seam-tested only (`adapters/kafka` TestF2_* — no broker in D5); real broker = D6 (noted on EXE-01/EXE-02).
3. **BreakEnd strategy-delivery gap** (F-B-06, MINOR, left unfixed by decision): analytics fires the BreakEnd session transition; strategies never receive a BreakEnd delivery (noted on MKT-15).
4. **Projector migration-066**: equal-seq sibling snapshots of one event can be dropped until the next event; converges; frozen migration constraint, documented (noted on REC-02).
5. **QUOTE producer (amended by F-MGR-03)**: the runtime seam now exists — market_analytics fans accepted canonical QUOTE rungs to config-declared operation routes, the owner gates staleness/dedup, and MM evaluates through the decision-scoped MarketContext; deterministic Sim/in-process evidence only, per the amendment. Real external market-feed certification remains D6.

## D6 carry (unchanged from ATP §15, plus Shot 3 deferrals)

Real Kafka EXACTLY_ONCE/read_committed config behavior; golden exact replay of a physically recorded run; 100–200 account capacity/resource benchmark; M2 journal physical durability semantics; selected real adapter native semantics; EXE-14 double-owner operational fencing; SCL-03 reconnect storm measurement; physical latency distributions at the wired budget points; physical checkpoint-lineage introspection (REC-03).

---

## Commands (all executed in this session against the final tree; every run reported `ok` / zero FAIL)

```text
# baseline
cd /home/kor/aranea/work/d5-foundations-20260929/echo && git rev-parse HEAD
#   → 5f9fadde190c3cd85637f746fd45bb703736a7f4  (branch feature/d5-shot3-remediation)

# full module suites
cd v3/core              && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 ./internal/functions/ ./internal/futuresvertical/ ./internal/futuresruntime/
cd v3/sdk               && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 ./futures/...
cd v3/futures-bridge    && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 ./...
cd v3/futures-projector && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 ./...

# targeted verbose evidence
cd v3/core/internal/functions        && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v -run 'TestFuturesMarketAnalytics' ./
cd v3/core/internal/functions        && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v -run 'TestFuturesSignalFanout|TestFuturesStrategyEngine|TestFuturesOperationFn' ./
cd v3/core/internal/futuresvertical  && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v -run 'TestS12|TimerFires|FanoutN200|Restart|Redelivery|BudgetPoints|AccountDay|UnknownManualPosition' ./
cd v3/core/internal/futuresvertical  && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v -run 'TestFuturesVertical_S1_FullSimPath|TestFuturesVertical_S2_FullSimPath|TestFuturesVertical_StaleGrantInvalidation|TestFuturesVertical_ProviderDeny|TestFuturesVertical_ProviderForceClose|TestFuturesVertical_TechnicalCloseAll|TestFuturesVertical_ThreePathSplitAtTheHarnessSeam|TestFuturesVertical_PositionObservationsRideProjectorTopic|TestFuturesVertical_PartialFill|TestFuturesVertical_EconomicsUpdate|TestPinAccountStrategyIDCorrelationOnly' ./
cd v3/core/internal/futuresruntime   && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v -run 'REC03' ./
cd v3/sdk/futures/market             && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v ./
cd v3/sdk/futures/bars               && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v -run 'MKT' ./
cd v3/sdk/futures/calendar           && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v -run 'CAL' ./
cd v3/sdk/futures/marketctx          && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v ./
cd v3/sdk/futures/domain             && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v -run 'DeriveSignalID' ./
cd v3/sdk/futures/strategies/s1      && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v ./
cd v3/sdk/futures/strategies/s2      && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v ./
cd v3/sdk/futures/operation          && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v ./
cd v3/sdk/futures/provider           && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v ./
cd v3/sdk/futures/gerardmm           && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v ./
cd v3/futures-bridge                 && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v ./internal/session/ ./adapters/kafka/ ./core/config/
cd v3/futures-projector              && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v ./core/projector/ ./adapters/pgstore/
```

### Amendment evidence commands (2026-09-30, executed against `e607b418`)

```text
cd v3/core/internal/futuresvertical && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v -run 'TestFuturesVertical_MKT07|TestFuturesVertical_TERM03|TestFuturesVertical_ProfitExitContinues|TestFuturesVertical_QuoteTrigger|TestFuturesVertical_EconomicsUpdate' ./
cd v3/sdk/futures/gerardmm          && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v -run 'TestFMGR02|TestQuoteTrigger' ./
cd v3/sdk/futures/operation         && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v -run 'TestEngineFinality|TestQuoteNotif' ./
cd v3/core/internal/futuresvertical && GOTMPDIR=/home/kor/aranea/gotmp go test -count=1 -v -run 'TestS12' ./          # 13/13
# full regression §9: sdk futures 13 pkgs, core functions/vertical/runtime, futures-bridge, futures-projector — all ok
```

**Status (amended): D5 ATP FINAL MATRIX — 113 PASS / 0 FAIL / 0 INCOMPLETE / 2 DEFERRED_TO_D6 full rows (EXE-14, SCL-03), over 115 cases, + D6 halves on REC-03, EXE-01/02/04/08, MKT-11/13, Budgets §20.** Amendment closure: MKT-07 PASS, TERM-03 PASS, F-MGR-02 CLOSED, F-MGR-03 CLOSED @ `e607b418` (every amended verdict backed by tests executed green on the final tree).
