---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures — BT-S01 Backtester V1 Design]]"
  - "[[Echo Futures]]"
aliases:
  - Echo Futures BT-S02
tags:
  - kind/doc
  - project/echo-futures
  - topic/backtester
created: "2026-10-04"
updated: "2026-10-04"
---

# Echo Futures — BT-S02 Backtester V1 Implementation Handoff

## STATE

| Campo | Valor |
| --- | --- |
| Branch | `feature/backtester-v1-s02` (repo `xKoRx/echo`, worktree `/home/kor/aranea/work/bt-s02-20261004/echo`) |
| HEAD cierre | `f41da25cc0b779ea48375198dbedaf932b930a80` — **pusheado a `origin`** (`7b857e33..f41da25c`), working tree limpio |
| Baseline Manager | `7b857e33833d069c9e93cf8e16695ecfc95f1d6a` (revisado, clean al iniciar) |
| Baseline original | `xKoRx/echo@7fbd7e990ac…` |
| Dirty state | Limpio tras el commit de cierre; cero toques a D6/bridge/egress físico |

## CLOSED BLOCKERS (mandato ONE-SHOT de cierre)

### BT-A43 — Generic100K veinte account-days (con BT-A26)

`TestGeneric100KTwentyAccountDaysE2E` (`a43_generic20_test.go`), plan canónico
`Generic100KFixedBudget20Days` (ordinales 1..20, UTC 00:00) materializado con
`MaterializeExperimentPlanV1` y dinero por día variado por el fixture (1→187.50,
2→62.50, 3→195.00, 19→250.00; resto 100.00; la variación es la sonda de
consumo: `q0 = floor(SL / (d0_ticks × tick_value))` fija exactamente una
cantidad por fila). Evidencia sobre el motor real (S1 + GerardMM + SimExecution
TRADE_MODEL):

- 20 account-days cruzados físicamente: revisiones de economics `DAY_OPEN` con
  ids contiguos `ad-20261005..ad-20261024` (día 1 en composición, 2..20 en
  boundaries fase-3).
- Ocho fills exactos, cantidades fijadas por la fila del día: day1 q=3, day2
  q=1, day3 q=2, day19 q=4 — `no hay fallback day2` (día 1 habría medido 1 con
  la fila de day2; día 3 mide 2).
- `Operation abierta conserva su row pinneada`: el ciclo de day2 cruza la
  medianoche UTC y su stop llena a las 00:05Z de day3 con q=1 (fila day2),
  mientras la entrada nueva de day3 mide q=2 (fila day3 rotada en el boundary).
- Decisiones posteriores a day2 (day3) y en el tramo final (day19 de 20).
- Economía exacta hand-computed: gross −675.00, fees 49.80, net −724.80,
  balance `99275.2 USD`; resultado COMPLETE.
- Artifact reproducible: seal + `FinalizeLocal` + `VerifyResultIntegrity`;
  segunda corrida byte-idéntica y `CompareRecords` IDENTICAL.
- Defecto de fixture destapado y documentado en el test: la pérdida del ciclo
  cross-boundary aterriza en el PnL del account-day receptor y
  `ownerRemaining = min(SL, SL+P)` reduce el presupuesto (comportamiento
  correcto del motor; el fixture lo absorbe con SL day3 = 195.00).

### BT-A26 — GAU50 mismo motor/corpus compatible

`TestGAU50SameEngineCausalAdmission` (`a26_gau50_test.go`): dos corridas sobre
el MISMO corpus (lunes+martes, dos ciclos S1) que difieren SOLO en el contexto
provider — `SIMRuleSet`/GENERIC100K vs el RuleSet real congelado
`GAU50EvalV1()` (EARN2TRADE/GAU50, `AssertGAU50EvalV1FrozenShape` verde):

- La misma señal del ciclo 2 (martes 20:55Z = 15:55 CT, dentro del gap
  15:50–17:10 CT) se produce en AMBAS corridas: la restricción no elimina la
  causa, cambia el comportamiento admitido.
- Generic: admite y opera ambos ciclos (4 fills, balance `99710.08 USD`,
  cero DENY). GAU50: el ciclo 1 (09:05 CT, ventana abierta) opera idéntico
  (q=2) y la admisión del ciclo 2 es denegada EN-RUN por el motor provider
  (`DENY_NEW_RISK` en la evidencia, ~20:55Z): cero evaluación post-hoc.
  Balance `99855.04 USD`.
- `Resterictions cambian admission/secuencia causalmente`: secuencia, fills y
  economía divergen solo por el RuleSet tipado.
- Nota de fixture: la pérdida del ciclo 1 consume el presupuesto del mismo
  account-day (`ownerRemaining`), por lo que el ciclo 2 corre en su propio
  account-day; calendario fixture con sesión extendida para mantener el venue
  negotiable (la restricción bajo test es la ventana GAU50, no la sesión).

### BT-A28 — Fresh-process determinism

`TestFreshProcessDeterminism` (`a28_fresh_process_test.go`) sobre el kit SD
(mismo build, ImmutableInputs idénticos):

- Secuencia del mandato: A in-proc, A in-proc (baseline), B corpus distinto,
  A in-proc (A/B/A), y luego A en **tres procesos OS recién iniciados** vía el
  binario real `echo-backtest run`.
- Igualdad exacta entre TODAS las instancias A (in-proc y fresh): run id,
  input digest, conteo de records, artifact sha256 (gzip bytes), economía y
  estado final; `CompareRecords` IDENTICAL entre procesos frescos; triple de
  integridad (`records/input_sequence/logical`) igual in-proc vs fresh.
- B difiere en todo (run id, bytes, integridad) in-proc y fresh.
- Los globals/init/singletons/estado de proceso no cambian el resultado.
- Claim cross-build NO emitido (fuera de contrato); el fresh-process
  mismo-build requerido queda demostrado.

### BT-A52 — Large corpus / memory streaming

`TestLargeCorpusStreamingMetrics` (`a52_large_corpus_test.go`), métricas
registradas (test log = evidencia):

| Métrica | N=25.000 | N=100.000 |
| --- | --- | --- |
| HistoricalRecords | 25.000 | 100.000 (4×) |
| Input | 10.102.780 B | 40.477.780 B |
| Partes NDJSON | 4 | 8 |
| Elapsed (motor) | ~15 s | ~85 s |
| Heap tras GC | ~1,02 MB | ~1,06 MB (+0,13 % del crecimiento del input) |
| Peak RSS proceso fresco (`ru_maxrss`) | ~544 MB | ~544 MB (+0 %) |
| Output records | 75.087 | 300.339 |
| Artifact | 2.386.196 B | 9.563.866 B |

- Memoria NO escala como copia del dataset (heap plano y RSS plano con 4× de
  corpus; buffers del adapter acotados, un lookahead por parte).
- Layout equality a escala: mismo corpus lógico como 1 parte vs 8 partes →
  mismo run id, mismos digests input/lógico, mismo censo de evidencia y
  economía; solo el receipt físico difiere (1 vs 8).
- Corrupción falla explícita: payload JSON roto → `NDJSON_RECORD_DECODE`
  nombrado en la admisión del corpus (fail-closed en la primera causa; la
  corrupción de orden se demostró con `NDJSON_ORDER_REGRESSION` en la
  calibración del test).
- Dedup/index: receipt del adapter por parte (sha256+lines+bytes+part) — el
  índice crece con las PARTES, no con el corpus en RAM.

## ACCEPTANCE MATRIX BT-A01..A60

Regla aplicada: PASS = propiedad demostrada por test(s) nombrados en el
baseline `7b857e33` + delta de cierre. Los IDs del plano dominio (SDK) se
apoyan en las suites shared que el driver compone; el delta de cierre añade la
evidencia driver-level que faltaba.

| ID | Estado | Evidencia |
| --- | --- | --- |
| A01 | PASS | Extracción shared Worker A (292 tests shell+SDK); futuresvertical S07/S12 corren los engines extraídos por el production path; shells solo adaptan I/O |
| A02 | PASS | `TestWarmup_S1_Fidelity_ZeroSignals_ZeroCycle`, `TestWarmup_S2_Fidelity_ZeroSignals_IndicatorsIdentical`, `TestDriver_WarmupInsufficientFailsNamed`, `TestS09_WarmupCorpus_*` (core), señales pre-trade_start = 0 en A43 |
| A03 | PASS | S1 acceptance `TestS1_AcS101..AcS118` (freeze exacto, cruce estricto, forming-bar excluida, stop-hit cierra una vez, back-inside re-arma) + orden de señales del engine + E2E (entry cursor llena tras la causa bar-close) |
| A04 | PASS | `TestDriver_DayBoundariesDST` + `FixtureCalendar`/resolver tests (sesión/break; cero barras fuera de grid) |
| A05 | PASS | `TestDriver_SchedulePreflightRejects` + invalidación del timer procesado (`scheduleNextDayBoundary` cancela por identidad) |
| A06 | PASS | Market MKT01–MKT06 (`TestStreamSequencer_*`: identidad vs secuencia, dedup sin seq, trades idénticos legítimos preservados, conflicto de redelivery por digest, epoch sin reset, ladder monotónico + demote/seed) + `TestS12_REC04_RunProvenanceIsolation` + `TestCommandIDDuplicateAndConflict` |
| A07 | PASS | `TestDriver_UnknownStreamFailsNamed` + preflight de spec (catálogo/calendario inválidos) + `TestStreamSequencer_RejectsForeignStream` |
| A08 | PASS | `TestEntry_UnconfiguredDay3FailsClosed` (resolvePlan fail-closed sin default) + `TestDriver_WarmupInsufficientFailsNamed` + `TestMaterializerInputErrors` |
| A09 | PASS | `TestMarketBuyFillsNextCursorAtAskPlusSlip` + economía exacta E2E (fee una vez, `TestLedger_FeesChargedOnceAndDedup`) |
| A10 | PASS | `TestStopSellTriggersOnLastFillsAtBidMinusSlip` + `TestStopGapFillsAtExecutableSide` + `TestStopWaitsForQuoteAfterTrigger` (nunca fill 99.50 inventado) |
| A11 | PASS | Familia `TestFreshness_*` de market (bounds por evidencia, future-skew validado, observaciones monotónicas, liveness no override, bloqueo de ejecución) + `TestQuoteSidesAcrossChunks` (BID no rejuvenece ASK) + `TestLedger_FreshnessCallerDecided` + provenance/cadence declaradas en spec (`ValuationModel.Freshness`, fill `price_source` en evidencia); en TRADE_MODEL no existen quotes canónicas y el BBO se deriva de trades con offsets declarados |
| A12 | PASS | `TestSC_ACKSealsOnlyACKNoFinality`, `TestSC_CancelSealsActionBeforeFinality`, `TestCancelTooLateAfterFill`, `TestCancelBeforeFillStopsMatching` + prefijo completo en comparación |
| A13 | PASS | `TestEngineFMGR04_PartialLateFillRetainsRemainingClaim` + `TestFMGR02_LateFillRaceCannotDoubleCloseOrInvert` + costes/exposición una vez (P3) |
| A14 | PASS | `TestFMGR02_ProtectiveFinalityContinuesProfitExit_LONG/SHORT` + `TestFuturesVertical_ProfitExitContinuesAfterProtectiveFinality` |
| A15 | PASS | Familia `TestRevalidate_*` (egress solo en revalidate válido/exacto; mismatches nunca invalidan retroactivamente) + `TestAdmission_FailClosedTable` + camino PER_ORDER-only directo (sin caps compartidos) |
| A16 | PASS | `TestCommandIDDuplicateAndConflict` + `TestLedger_FeesChargedOnceAndDedup` + `TestFuturesOperationParity_DedupLateForeignRevisionAndConflict` |
| A17 | PASS | `TestEntryExpiry01/02/03` + `TestDriver_FillWinsExpiryDeadline` (fase 4 antes que timer fase 5) |
| A18 | PASS | `TestEvidence01/04/05` + `TestEconUpdate04_NotFreshDeliveryFailsClosed` + orden de efectos (marks primero) |
| A19 | PASS | `TestEvidence06_AccountEconomicsAndQuoteStayDistinctCauses` + `TestEconUpdate03_OneKeyedDeliveryPerUpdate` |
| A20 | PASS | `TestLedger_FIFOExactMultiContract` + `TestLedger_ReversalResidualReal` + `TestSC_P2_DistinctContractsNeverNet` |
| A21 | PASS | Fees opening/closing una vez (ledger) + `TestLedger_UnresolvedMarksFailClosed` (fresh falso prohibido) + cuenta flat = balance (E2Es con ciclos cerrados exactos) |
| A22 | PASS | `TestLedger_DayFormulasOvernightBoundary` + `TestDriver_DayBoundariesDST` + DST/partial del materializador + A43 (posición overnight cruza boundary UTC con fila pinneada) |
| A23 | PASS | `TestSC_P7_DLLAndEODExactness` + `TestSC_P8_GAU50_TwoChicagoDays` + `TestDailyLossFlattenOnlyWhenDeclared` + `TestCapLoweredBelowExposure` + `TestForceCloseTriggerFanout` (breach terminal latcheado; evaluación in-engine antes de nueva señal) |
| A24 | PASS | `TestConsistency_*` (4) + `TestSC_P8_ConsistencyExactThreshold` + `TestEntry_ObjectiveReachedBeforeEntryBlocked` |
| A25 | PASS | `TestClockFired_TripsCutoffWithoutMarketTick` + `TestRequiredFlatWindow_ReopenRetiresOnlyItsOwnLatch` + `TestRequiredFlatWindow_TerminalBreachIsNeverRevived` |
| A26 | PASS | `TestGAU50SameEngineCausalAdmission` (cierre) — restricción cambia admission/ secuencia causalmente; Generic20 = corrida A43 |
| A27 | PASS | `TestHorizonOpenPositionPolicy` (cierre): REQUIRE_FLAT → INCOMPLETE `REQUIRE_FLAT_NOT_MET` sin venta a último precio; REPORT_RESIDUALS → COMPLETE con residuales explícitos; cero ejecuciones inventadas al horizonte |
| A28 | PASS | `TestSDDeterminismSameSpecByteIdentical` + `TestSDDeterminismABA` (in-proc) + `TestFreshProcessDeterminism` (cierre: 3 procesos frescos byte-idénticos) + layout-independent digests (A51/A52) |
| A29 | PASS | `TestEvidence07_MMErrorAbortsAndRetry` + retry=F05 idéntico + `TestSDFailedAttemptNeverCanonical` + idempotencia/conflicto de finalize (`TestFinalizeLocalIdempotentAndConflict`) |
| A30 | PASS | `TestCompareRecords*` (primera divergencia con field path) + `TestReproduceCmdCarriesDigests` + capsule RECORD_MISSING |
| A31 | PASS | `TestReadResultRejectsUnknownKindAndBrokenGaps` + `TestVerifyResultIntegrityCatchesWrongDigest` + tamper (`TestResultWriterIntegrityVerifiedAndTamperDetected`) |
| A32 | PASS | `TestPublishResult*` (create-if-absent, conflicto intacto, idempotente stored-then-lost, size cap, seal check) + conformance suite + vectores SigV4 AWS + probe REAL MinIO (write/read etag). Condicional real: NOT_VERIFIED_ENVIRONMENTAL (declarado abajo) |
| A33 | PASS | `TestCallerControlledAdmissionFrontierReplay` + `TestCorpusShortOfHorizonSealsFailVisible`: AdvanceUntil frontera exacta; ningún control futuro aplicado (`PendingBeyondHorizon` sellado sin aplicar); nada se observa tras el corpus; misma spec → mismo prefijo (determinismo A28) |
| A34 | PASS (protocolo S03/S04) | `bt_f01..f05_test.go` + F-MGR02/04 verticals; disposición sin cambios (abajo) |
| A35 | PASS | `go build` módulos, SDK futures completo, core functions 192, futuresvertical 55s, futures-bridge/projector, backtester completo — todos verdes en el cierre (cero regresión por el delta) |
| A36 | PASS | A52 (counts/bytes/parts/elapsed/heap/RSS/output/artifact/receipt) + `TestBoundedMemory100K`; sin SLA inventado |
| A37 | PASS | `TestRolloverE2E_ThreeContractsOneAccount` (2 selecciones+activaciones, fills pineados al físico vigente, balance/días/IDs continúan, un solo COMPLETE) |
| A38 | PASS | Rollover E2E (A viva durante selección/activación de B; quotes/stop/fill de A solo-A) + `TestSC_P2` (sin neteo cross-contract) |
| A39 | PASS | `TestRollover_Activation_RealS1_FullLifecycle` + `TestDrainCycle_RealS1_CloseFlows_OpenAbsorbed` + `TestWarmupCandidate_IsolatesActiveFlat` + contadores globales conservados |
| A40 | PASS | `TestEngineFMGR04_*` + ADM-03/04 (PendingAdmission supersedes/invalidates) + `DeferredEntryPin` (pin del fence re-validado al promover) + tests de activación strategy |
| A41 | PASS | `TestRollover_SlotLimits_Retired_Replacement` (máx 3 slots; vencido no resucita) + schedule preflight (sucesor no inmediato rechazado) |
| A42 | PASS | `TestCorpusShortOfHorizonSealsFailVisible` (cierre: corpus que termina antes del horizonte sella fail-visible sin sustituir precios; cero evidencia tras el último record) + `TestWarmupCandidate_IsolatesActiveFlat` (prewarm B no genera revisión económica sobre A) |
| A43 | PASS | `TestGeneric100KTwentyAccountDaysE2E` (cierre) — arriba |
| A44 | PASS | `TestDSTFallBackNo24hJumps`/`TestDSTSpringForward`/`TestPartialFirstAndLastDays`/`TestNonUTCTimezone`/`TestActivationBeforeDayBoundaryStepsBack`/`TestMaterializerInputErrors`/`TestSelectorsPerStrategy`/`TestPlanRecordIdentityFields` + pinneado cross-boundary de A43 |
| A45 | PASS | `TestContextTransitionAndStaleDigestFailure` (cierre: transición instala contexto nuevo causalmente con evidencia `RecordAccountContextTransition`) + `TestAccountContextUpdate_AtomicInstall` + `TestLedger_StageSegments` + funded resolve/fail-closed (`TestEntry_FundedUnresolvedFailsClosedAndConfiguredResolves`) + cashflow separado del PnL |
| A46 | PASS | Quiescencia real (`quiescent()`: inventario físico cero, sin ops/claims/pendings; selección futura pendiente bloquea; agenda agotada/ vacía NO bloquea — condición corregida en el cierre) + `CONTEXT_NOT_QUIESCENT` nombrado sin mutación parcial |
| A47 | PASS | `TestAccountContextUpdate_AtomicInstall` + `TestClockFired_TripsCutoffWithoutMarketTick` + `TestNextBoundary_OrderedInstants` (EOD exactamente una vez; contexto viejo no muta el nuevo) |
| A48 | PASS* | Nunca PASS→FUNDED implícito: `TestSC_P5_PassIsNeverAutoFunded` + lifecycle evaluator fail-closed + continuación causal por control (`TestContextTransitionAndStaleDigestFailure`). *Nota declarada: la rama driver de pausa temprana (`awaitingNextContext`) es inerte-fail-safe en V1 porque ningún productor de outcome de stage existe en la composición backtest (el outcome programático pertenece al plano campaign/lifecycle fuera del alcance S02); con `OutcomeStop` la corrida termina en el outcome — sin comportamiento incorrecto posible |
| A49 | PASS | `TestSC_P1_CashflowIsNotTradingPnL` + `TestLedger_CashflowPayoutDebit` + driver: `TestDeclaredControlsOrderingCashflowAndExactContext` (cashflow mueve balance/`NonTradingCashflows`, nunca `RealizedNet`; debit puede disparar safety vía projectEconomics post-cashflow) |
| A50 | PASS | Dedup por identidad de cashflow (`IsCashflowIdentityConflict` → no-op incluso tras otra transición; conflicto fatal visible — ledger `TestLedger_CashflowPayoutDebit`/P1) + evidencia `RecordAccountCashflow` por control |
| A51 | PASS | `TestRunE2E_LayoutIndependence` + suite ndjson (`TestSinglePartIdenticalToChunks`, `TestGzipEqualsPlain`, `TestVerbatimIdentityAcrossPartition`) + equality a escala (A52) |
| A52 | PASS | `TestLargeCorpusStreamingMetrics` (cierre) — arriba |
| A53 | PASS | `TestFuturesOperationParity_TypedIngressDecodeRouting` + `TestFuturesOperationParity_ExecutionUpdateTypedCoreVsHistorical` (mismo MMInput/estado/efectos por ingress tipado Core vs historical) |
| A54 | PASS | `TestFuturesOperationParity_RawFailClosedAndIndependentRestore` (UNAVAILABLE/PnLFresh=false como histórico; solo causa económica válida posterior restaura) |
| A55 | PASS | `TestFuturesOperationParity_DedupLateForeignRevisionAndConflict` + `TestFuturesOperationParity_ErrorRetryDerivesSameIdentity` (guards antes del sidecar; IDs rollback; sin relectura latest ni doble MM) |
| A56 | PASS | Parity con allocators/provenance reales (F03 `NewEngine(run)`; wrapper no añade ExecutableQuoteSource) — mismos paths/semántica, diferencias solo las nombradas por contrato; config MM válida en ambas composiciones (tests parity) |
| A57 | PASS | `TestCallerControlledAdmissionFrontierReplay` (cierre): identidad `bt-c-` por namespace; replay misma secuencia/fronteras → artifacts byte-idénticos; control en/pasado de frontera rechazado; `PendingBeyondHorizon` sellado en footer inputs sin aplicar; nuevos controles tras Finish rechazados. **Dos defectos reales corregidos** (abajo) |
| A58 | PASS | `TestDeclaredControlsOrderingCashflowAndExactContext` + `TestContextTransitionAndStaleDigestFailure` (cierre): orden (effective_at, ordinal, control_id) verificado en evidencia; **expected_context exacto implementado** (`CONTEXT_DIGEST_MISMATCH` nombrado — antes el digest se exigía no-vacío pero nunca se verificaba); controls en fase 2 antes que market |
| A59 | PASS | `TestLedger_StageSegments` (preserve/close/open stage; START_NEW archiva outcome y separa progreso) + `TestSC_P4_RiskSeedIsNotMoney` (seed no crea dinero) + StateModes validados (`controls.go`) |
| A60 | PASS | `TestAccountContextUpdate_AtomicInstall` (instalación atómica sin estados mixtos ni efectos tras error) + binding físico único por run (spec/binding; otro ProviderAccountRef exige otro run) + transición de cierre falla nombrado sin publicar |

Resumen: **60/60 PASS** (A34 bajo su protocolo frozen S03/S04; A48 con nota
declarada arriba; A32 con su residual ambiental).

## TEST DELTA (comandos y resultados del cierre)

- `go test ./v3/backtester -count=1 -timeout 40m .` → `ok … 362.7s` (suite
  completa: 4 fixes de producción + 7 archivos de test nuevos).
- Archivos nuevos: `a26_gau50_test.go`, `a27_end_policy_test.go`,
  `a28_fresh_process_test.go`, `a43_generic20_test.go`,
  `a52_large_corpus_test.go`, `a57_controls_test.go`.
- Regresión: `go test ./v3/sdk/futures/...` completo ok; core `functions` ok
  (192 tests incl. 6 parity), `futuresruntime` ok, `futuresvertical` ok
  (55.5s, incl. MKT07 + S12 exact-replay); `go build` de módulos ok.
- Corridas manuales de calibración documentadas en los propios tests
  (diagnósticos de fills/señales que fijaron el contrato observado).

## DETERMINISM

Ver BT-A28: in-proc A/A/B/A byte-idéntico (existente) + **fresh-process ×3
mismo-build byte-idéntico** (nuevo), records/id/economía/estado/digests/gzip
iguales; B (corpus distinto) difiere en identidad y bytes en ambos mundos.
Cross-build: NO claim (fuera de contrato).

## GENERIC20

Ver BT-A43: veinte rows/selectores digeridos con boundaries físicos
`ad-20261005..ad-20261024`, sizing por fila observado en `filled_qty`
(3/1/2/4), sin fallback day2, fila pinneada preservada a través del boundary
con Operation abierta, decisiones day3 y day19, economía exacta, COMPLETE,
artifact reproducible.

## LARGE CORPUS

Ver BT-A52: tabla de métricas arriba (records, bytes, partes, elapsed, heap,
RSS por-proceso, output, artifact, receipt); corpus nunca en RAM; sides quote
a través de chunks cubiertos por `TestQuoteSidesAcrossChunks` (semántica) y
equality 1-vs-8 partes a escala (orden); corrupción schema/order falla
explícita con código nombrado.

## PRODUCTION FIXES DEL CIERRE (acceptance-mandated, con regresión verde)

1. `expected_context exacto` (A58): `controls.go` añade `contextIdentity` +
   digest canónico `{context_id, stage_id}`; `applyContextTransition`/
   `applyCashflow` fallan `CONTEXT_DIGEST_MISMATCH` si el control no nombra el
   contexto instalado (antes el digest era requerido-no-vacío pero jamás
   verificado); la identidad instalada rota con cada transición.
2. Quiescencia de transición (A46): la condición de agenda estaba invertida
   (`selectionIdx >= len(schedule)` rechazaba SIEMPRE con agenda vacía); ahora
   bloquea solo una selección futura pendiente; agenda agotada/vacía nunca es
   deuda de quiescencia.
3. Identidad de dos fases CALLER_CONTROLLED (A57): `NewRun` llamaba
   `DeriveRunID(mode, inputs, nil)` incondicionalmente → `CALLER_CONTROLLED`
   fallaba SIEMPRE en composición ("requires base immutable inputs"); ahora la
   derivación elige base-vs-full según modo.
4. Horizonte half-open de controls (A57/A33): un control con
   `effective_at >= end_exclusive` se aplicaba; ahora queda admitido-pending y
   se sella con los inputs (mismo principio que el day-boundary).

## FINDINGS F01..F05 (sin inflar estado)

| Finding | Estado | Evidencia |
| --- | --- | --- |
| F01 nil RuleSet | `CONFIRMED_FIXED_WITH_REGRESSION_CANDIDATE` | sin cambios: guard `consistency.go` + `bt_f01_test.go` + guard análogo lifecycle (SUBAGENTE C) |
| F02 ForceClose nondeterminista | `CONFIRMED_FIXED_WITH_REGRESSION_CANDIDATE` | sin cambios: `bt_f02_test.go` 300 sweeps |
| F03 provenance fabricada | `CONFIRMED_FIXED_WITH_REGRESSION_CANDIDATE` | sin cambios: `NewEngine(run)` + `bt_f03_test.go` |
| F04 fill tardío/ajeno | `CONFIRMED_FIXED_WITH_REGRESSION_CANDIDATE` | sin cambios: `bt_f04_test.go` 6 casos + parity |
| F05 IDs fuera del clone | `CONFIRMED_FIXED_WITH_REGRESSION_CANDIDATE` | sin cambios: `bt_f05_test.go` retry=idéntico |

Este cierre no encontró regresión nueva de F01–F05; S03 los verifica
adversarialmente de forma independiente.

## ENVIRONMENTAL RESIDUAL (solo lo que requiere entorno/credenciales externos)

1. `REAL_CONDITIONAL_WRITE = NOT_VERIFIED_ENVIRONMENTAL`: conformance
   condicional MinIO real sin credenciales S3 autorizadas en el entorno.
   Mantenido fake-S3 conditional + SigV4 vectors + probe real no-condicional.
   NO bloquea (BT-S01 lo contempla explícitamente). No se declara PASS.
2. Provisioning/upstream físico LIVE de `ExecutionUpdate`/`QuoteUpdate`: NO
   certificado (fuera de S02); el ingress tipado Core → shared
   normalization/path y su paridad contra el adapter historical SÍ están
   probados (A53–A56). D6 intacto.
3. La nota declarada de A48 (rama driver de pausa AWAIT_CONTEXT sin productor
   de outcome en la composición V1) — limitación de alcance contractual, no
   ambiental, documentada en la matriz.

## GATE

`BT_S02_IMPLEMENTATION_READY_FOR_MANAGER_REVIEW`

Los cuatro blockers del Manager están cerrados con evidencia física (A43/A26,
A28 fresh-process, A52 con métricas reales), la matriz obligatoria
BT-A01..A60 queda reconciliada 60/60 PASS sin gaps escondidos (A34 conserva su
protocolo S03/S04; A32 mantiene su residual ambiental declarado; A48 con nota
de alcance), y el delta de producción del cierre (4 fixes con tests rojos→
verdes o defectos estructurales demostrados) mantiene la suite completa del
paquete y todas las regresiones SDK/core en verde. D6 intacto. NO se inicia
BT-S03.
