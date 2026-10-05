---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — BT-S01 Backtester V1 Design]]"
  - "[[Echo Futures — BT-S02 Backtester V1 Implementation Handoff]]"
  - "[[Echo Futures — BT-S03 Adversarial Review]]"
  - "[[2026-10-04-bt-s03-etcd-production-incident]]"
aliases:
  - Echo Futures BT-S04
tags:
  - kind/doc
  - project/echo-futures
  - topic/backtester
created: "2026-10-04"
updated: "2026-10-04"
---

# Echo Futures — BT-S04 Final Remediation and Certification

## Propósito

Último implementation shot del programa Backtester V1: corrección de los findings aceptados de BT-S03 (F01–F14 obligatorios, F15/F16 MINOR), reparación de la superficie de seed tests que permitió el incidente ETCD, y recertificación completa del producto. Sin rediseño: BT-S01 frozen es autoridad. Cuatro subagentes NORMAL reales ejecutaron workstreams con ownership exclusivo de archivos; el Lead integró, conservó source truth y ejecutó el gate final.

## State

| Campo | Valor |
| --- | --- |
| Branch | `feature/backtester-v1-s04-remediation` (repo `xKoRx/echo`, worktree `/home/kor/aranea/work/bt-s04-20261004/echo`) |
| HEAD de cierre | `cd451972b242c8933321e03001decd4b6d778c61` — **pusheado a `origin`** (branch nuevo), working tree limpio |
| Baseline | `feature/backtester-v1-s02@f41da25cc0b779ea48375198dbedaf932b930a80` (intacto en origin) |
| Repros adversariales | `codex/bt-s03-adversarial-review@13bb72bbe237aae0d191f26d9c5ca89a5b5b9670`, integrados por cherry-pick `-x` @ `d67456d6` (sólo tests tagged `s03review`; cero mutación productiva del branch de review) |
| Cadena de commits | `9e69c53f` Phase 0 seed safety → `d67456d6` repros → `d308753b` seam F01 → `ff27a86c` F02/F03 → `7b61addd` F01/F04/F05/F06/F07/F09/F13/F14 → `36dfc30f` F08/F10 → `cd451972` F11/F12/F13/F14/F16 |
| Dirty state | Limpio; cero toques a NinjaTrader, AddOns, D6 bundle, ETCD D6, physical egress, cuenta física o gates D6 |
| Toolchain | Go 1.27.1 linux/amd64; go.work declara 1.25.5; sin cambios de toolchain ni dependencias |

## Test safety (Phase 0)

El recovery confirmó que suites amplias podían ejecutar seeds contra el cluster ETCD de producción (`v3/sdk/etcd/echo_seed_test.go`; sin `ETCD_ENDPOINTS` el SDK cae a los endpoints de producción hardcodeados `192.168.31.250-.254:2379`). Phase 0 @ `9e69c53f`, homólogos v1/v2/v3:

1. **Build tag `seeds`**: los seeds config-mutating quedan excluidos de toda suite ordinaria; sin el tag los packages `etcd` no siquiera exponen los tests (`[no test files]` / `no tests to run`).
2. **Env guard `ECHO_SEED_ALLOW`**: el seed exige opt-in inequívoco igual al namespace destino (`ECHO_SEED_ALLOW=production` para producción); sin opt-in falla nombrado ANTES de crear el cliente (cero conexión).
3. **Endpoint guard**: sin `ETCD_ENDPOINTS` explícito el seed se rehúsa (el default sería el cluster de producción); un seed no-production apuntando a un endpoint del cluster de producción se rehúsa (`isProductionClusterHost`).
4. **Aislamiento de red de proceso**: todas las suites del shot se ejecutaron dentro de `unshare --user --map-root-user --net` con sólo loopback y `GOPROXY=off GOSUMDB=off`, siempre con listas explícitas de packages; nunca `go test ./...` desde `v3/sdk`.

Evidencia (todo dentro del namespace sin red): suite ordinaria `go test ./v{1,2,3}/sdk/etcd/ -run TestSeedEchoConfig` → invisible; con `-tags seeds` sin opt-in → ambos seeds fallan con el mensaje de refusal en 0.00s; con opt-in de development y endpoint de producción → refusal nombrado; con opt-in y sin `ETCD_ENDPOINTS` → refusal nombrado. **No se ejecutó el seed real contra producción para probar el guard.** No se ejecutó ningún `go test ./...` desde `v3/sdk` en todo el shot.

### ETCD safety monitor

Read-only vía API HTTP v3, sin exponer secretos. Baseline pre-suites y chequeo post-suites de `/echo/production/postgres/password`: `mod_revision=59390`, `version=62`, `len=10`, `sha256_12=8a36217243c1` — idénticos antes y después (59390 es la restauración CAS del incidente, previa al inicio de S04). Chequeo de todo `/echo/`: `max(mod_revision)=59390` → **cero escrituras ETCD en todo el namespace durante S04**. Sin cambios externos: no hubo abort ni escalado.

## Subagentes (utilización real)

| Agente | Frente | Resultado |
| --- | --- | --- |
| SUBAGENTE B | Shared Operation: F02, F03, cierre F04 original | FIXED; 5 repros verdes; 8 regresiones nuevas; suites operation/functions/provider/accounting verdes; cero adaptación de oráculo; sin cambios de API exportada ni en `domain/execution.go` |
| SUBAGENTE C | Núcleo causal backtester: F01-población, F04, F05, F06, F07, F09, F10-mitad run, F13-mitad cómputo, F14-helpers muertos | FIXED en los 9 ítems; 11 regresiones nuevas; suite backtester completa verde (394s); `ledger.go`/`risk_eval.go` sin diff (cambió el caller, no el ledger) |
| SUBAGENTE D | F08 dataset identity, F10-mitad preflight | FIXED; repros verdes sin tocar oráculos; suite ndjson + preflight + rollover verdes |
| SUBAGENTE A (ola 2) | F11, F12, F13-serialización, F14-CLI, F16, F01-reconstrucción | FIXED; 4 repros verdes; 7 regresiones nuevas; 3 adaptaciones de oráculo documentadas in-file (rechazo anterior, más fail-closed, propiedad preservada); 3 incursiones mecánicas justificadas fuera de ownership (`cmd/echo-backtest/run.go` → `SealResult`; `result_integration_test.go` simetría helper/CLI; `reproduce_test.go` fijaba el formato legacy `btctl` que F16 elimina) |

Ownership por archivos fue disjunto por ola; integración por dependencias (B/D/C en paralelo, A sobre las estructuras expuestas por C). El Lead pre-seedó el seam compartido F01 (`d308753b`) para asegurar un solo writer del struct de identidad.

## Findings BT-S03

| ID | Severidad | Disposición | Evidencia de cierre |
| --- | --- | --- | --- |
| BT-S03-F01 | CRITICAL | **FIXED** | Límites causales (`warmup_start/trade_start/end_exclusive`) en `ImmutableInputs`/`BaseImmutableInputs` (epoch ns UTC) poblados en composición y consumidos en reconstrucción; repro seis variantes verde (`TestS03_AstraTimeBoundsParticipateInIdentity`); A/A/B/A, fresh-process y layouts intactos. Host/path/wall-clock/credentials siguen excluidos de identidad |
| BT-S03-F02 | CRITICAL | **FIXED** | Guards de cuenta y contrato físico pinneado ANTES de sidecar/economía/mutación; hecho ajeno = auditoría con identidad original preservada (sin tocar Operation/Runtime/MMState/fills/órdenes/exposición/claims/economía del owner); correlación ausente = UNKNOWN explícito (nunca la Operation actual); 3 repros verdes + 5 regresiones nuevas typed/raw/Apply |
| BT-S03-F03 | MATERIAL | **FIXED** | Orden identidad→ownership→correlación→native dedup→sidecar→economía→handler; duplicado/foreign/unmatched no degrada freshness, no instala revisión ni cambia autoridad; 2 repros verdes + 3 regresiones nuevas; auditoría física conservada |
| BT-S03-F04 | CRITICAL | **FIXED** | Transición instala atómicamente el next context completo (Binding, RuleSet por identidad — autoridad desconocida falla nombrada, terms, MM config, plan rows/selectors, límites, estado operacional, stage, risk seed/mode, autoridad account-day/calendario con fencing del timer viejo); `PRESERVE_STAGE` exige mismo stage; cero commit parcial y cero efectos dependientes en fallo (rollback limpio probado); balance sólo por hechos económicos/cashflows; EOD del contexto viejo exactamente una vez como hijo del control |
| BT-S03-F05 | CRITICAL | **FIXED** | Evaluator conectado al engine causal: terms iniciales en composición, `evaluateStageLifecycle` sobre estado asentado/quiescente, latch una vez por stage, un record `ACCOUNT_LIFECYCLE` por outcome (sin duplicados), terminal breaches, PASS, FAIL, min days, consistency, target, STOP (termina en el outcome asentado) y AWAIT_CONTEXT (park una vez por outcome, control al caller, continuación causal misma cuenta). Sin `PASS=>FUNDED` automático |
| BT-S03-F06 | CRITICAL | **FIXED** | Revalidación de autoridad de mark contra reloj lógico en decisiones/eventos/finalización: ausente/vencido → `PnLFresh=false` + riesgo unresolved + record; detección no condicionada a `unrealized!=0` (marca ausente → `FINAL_VALUATION_UNRESOLVED`); restore por market válido posterior; posición abierta no termina COMPLETE con valoración inválida cuando el corpus declarado no cubrió el horizonte (`OLD_CONTRACT_DATA_UNAVAILABLE`) |
| BT-S03-F07 | MATERIAL | **FIXED** | `same ID + same payload` = no-op idempotente incluso tras transición; `same ID + distinto payload` = `CASHFLOW_IDENTITY_CONFLICT` fatal con capsule; dedup (account,cashflow_id) resuelto antes del digest/contexto; trading PnL intacto |
| BT-S03-F08 | MATERIAL | **FIXED** | `Open` del NDJSON valida corpus_id/version/streams/range contra la selección declarada (`DATASET_IDENTITY_MISMATCH`, fail-closed en frontera del adapter, receipt fuera de identidad lógica, engine sin acoplarse al codec); equivalencia una-parte/chunks/gzip/adapter intacta |
| BT-S03-F09 | MATERIAL | **FIXED** | `Finish()` distingue horizonte completo, business STOP, partial pause (`HORIZON_NOT_REACHED_AWAITING_NEXT_CONTEXT`), short corpus (`HORIZON_NOT_REACHED` / `PLAN_SHORT_OF_HORIZON`), `OLD_CONTRACT_DATA_UNAVAILABLE`, `REQUIRE_FLAT_NOT_MET`, `FINAL_VALUATION_UNRESOLVED`; EOF ≠ COMPLETE; zero-trade covered interval es COMPLETE legítimo (evidencia de cobertura = corpus consumido hasta el boundary, no tick artificial) |
| BT-S03-F10 | MATERIAL | **FIXED** | Preflight (spec.go): total ordering, cadena, prepare<=effective, sucesor inmediato, cobertura del predecesor hasta el handover, config refs/digests resolubles, slots, stream identity, no resurrection ABA. Lado run (run.go): prepare/selección consumen los `strategy_config_refs` declarados con digest en la evidencia; slots/pins conservados (A37/A40/A41 verdes) |
| BT-S03-F11 | MATERIAL | **FIXED** | `input_sha256` recomputado desde los inputs sellados en seal/read/verify (`ErrResultInputDigest` / `ErrResultRunIdentity`); tamper falla nombrado antes de escribir bytes y en read/verify; footer auto-consistente forjado rechazado; idempotencia/conflicto de finalize preservados |
| BT-S03-F12 | MATERIAL | **FIXED** | Result autocontenido salvo corpus/build durables: `resolved_spec` con config resuelta inline, controles declarados y pendientes; `echo-backtest reproduce <result>` reconstruye el RunSpec desde el artifact (`RunSpecFromResult`) y re-admite las admisiones caller-controlled en sus fronteras selladas (§13.1); sin event sourcing ni corpus copiado; Δ artifact ≈ +12.6% en fixture chico, KB-scale independiente del corpus |
| BT-S03-F13 | MATERIAL | **FIXED** | Disposiciones estructuradas `APPLIED / PENDING_AT_HORIZON / REJECTED / CONFLICT` computadas por el engine y selladas en `summary.control_dispositions`; cubre before/at/after end en ambos modos; replay standalone preserva las dispositions byte-idénticas; ningún control se ejecuta fuera del horizonte |
| BT-S03-F14 | KISS | **FIXED** | Los tres helpers muertos borrados (`liveConfigPtr`, `isCashflowDup`, `calendarTransitionKind`; 0 referencias); CLI publish lee/verifica el artifact UNA vez (`ReadResult`+`VerifyResultIntegrity` únicos en `publish.go`) reutilizando count/state/runID; verificación del publisher público intacta; sin abstracciones nuevas ni cleanup general |
| BT-S03-F15 | MINOR | **ACCEPTED_MINOR_OPEN** | No trivial: los adapters productivos ya filtran `[From, end_exclusive)` (el registro en `end_exclusive` nunca llega por selección) y un check nominal de edad de marca en el horizonte rompería contratos frozen (`TestHorizonOpenPositionPolicy` REPORT_RESIDUALS@14:30 con marca@14:25 bajo bucket 5m/max-age 1m; `TestFreshProcessDeterminism` con To declarado < horizonte). El repro adversarial (fuente deliberadamente no-filtrante) queda rojo y explícito. No blocker según mandato |
| BT-S03-F16 | MINOR | **FIXED** | `ReproduceCmd` emite `echo-backtest reproduce --result <artifact> --dataset <ref>` (la CLI real entregada, sin flags no implementados); el comando generado se ejecuta contra el artifact/corpus del repro (`Test_s03_luna1_reproduce_cmd_is_executable` verde) |

### F01..F05 originales

| Finding | Estado final | Evidencia |
| --- | --- | --- |
| BT-F01 | `CONFIRMED_FIXED_WITH_REGRESSION` | `bt_f01_test.go` + suite provider completa verde en la certificación; no reabierto |
| BT-F02 | `CONFIRMED_FIXED_WITH_REGRESSION` | `bt_f02_test.go` (300 sweeps) verde; orden de familias/keys intacto tras F04/F05 |
| BT-F03 | `CONFIRMED_FIXED_WITH_REGRESSION` | `bt_f03_test.go` verde; provenance de engine intacta (F04-S03 no la tocó) |
| BT-F04 | `CONFIRMED_FIXED_WITH_REGRESSION` | Cerrado vía BT-S03-F02: `bt_f04_test.go` (6 casos) + parity + 5 regresiones nuevas; `TestS03_Luna2_F04_MissingCorrelationDoesNotUseCurrent` verde |
| BT-F05 | `CONFIRMED_FIXED_WITH_REGRESSION` | `bt_f05_test.go` (retry idéntico) verde; cursores dentro del clone intactos |

## Regresiones (finding → test)

- **F01**: `TestS03_Astra_TimeBoundsParticipateInIdentity` (6 variantes) + `TestBT_S04_RunSpecFromResultConsumesSealedEpochs` + conservación de `TestFreshProcessDeterminism`, `TestSDDeterminism*`, `TestRunE2E_LayoutIndependence`.
- **F02/F03/F04-original**: repros `TestS03_Sol1_*` (4) + `TestS03_Luna2_F04_*`; nuevos `TestBTS04_F02_ForeignExecutionAccountAuditOnlyTyped`, `TestBTS04_F02_ForeignContractAuditOnlyTyped`, `TestBTS04_F02_MissingCorrelationStaysUnknownRaw`, `TestBTS04_F02_TerminalAForeignFactsNeverMutateLiveB`, `TestBTS04_F02_ChargedIdentityDedupsAcrossWholeRun`, `TestBTS04_F03_RawDuplicateNeverDowngradesRestoredEvidence`, `TestBTS04_F03_TypedDuplicateAbsorbedBeforeSidecarValidation`, `TestBTS04_F03_UnmatchedOrderCannotInstallSidecarTypedAndRaw` + `bt_f04_test.go`/parity heredados.
- **F04**: repros `Test_s03_sol2_context_transition_installs_next_binding`, `Test_s03_sol2_preserve_stage_rejects_stage_change`; nuevos `TestBT_S04_TransitionRuleSetAuthority`, `TestBT_S04_TransitionExpectedBalanceRollsBackClean`, `TestBT_S04_TransitionEODAtBoundaryFiresExactlyOnce`, `TestBT_S04_AwaitContextContinuationSameAccount` (EVALUATION→FUNDED explícito, misma cuenta, balance preservado) + heredados `TestContextTransitionAndStaleDigestFailure`, `TestAccountContextUpdate_AtomicInstall`, `TestLedger_StageSegments`.
- **F05**: repro `Test_s03_sol2_lifecycle_is_produced_in_engine`; nuevos `TestBT_S04_LifecycleFailTerminalStopsAfterSettlement` (FAIL terminal con asentamiento), `TestBT_S04_LifecycleNilMinimumDaysNeverPasses` (nil jamás habilita PASS), `TestBT_S04_AwaitContextWithoutContextBlocksToHorizon` (pausa ≠ COMPLETE), `TestBT_S04_AwaitContextContinuationSameAccount` (next-context causal); PASS con target real alcanzado en estado asentado en el wiring del repro; min days 0 es contrato del evaluador compartido (suite provider verde; GAU50 fija 0 por fuente); un record por outcome (sin duplicados).
- **F06**: repro `Test_s03_sol2_final_open_position_rejects_stale_mark`; nuevos `TestBT_S04_CashflowAtStaleMarkSettlesNotFreshThenRestores` (timer/cashflow al límite sin tick + restore), `TestBT_S04_ZeroTradeCoveredIntervalCompletes`; missing-mark/unrealized-0 vía `markAuthorityFailure`; contrato retirándose vía `OLD_CONTRACT_DATA_UNAVAILABLE`; heredados `TestLedger_FreshnessCallerDecided`, familia `TestFreshness_*`, A21/A23.
- **F07**: repro `Test_s03_sol2_cashflow_identity_conflict_is_fatal`; nuevo `TestBT_S04_CashflowReplayAndConflictAcrossTransition` (replay no-op pre/post transición + conflicto fatal en ambos) + `TestSC_P1_*` heredado.
- **F08**: repro `Test_s03_luna1_ndjson_selection_identity`; nuevos `TestOpenRejectsForeignCorpusID`, `TestOpenRejectsForeignVersion`, `TestOpenRejectsUnservableRange`, `TestOpenIdentitySelectionLayoutEquivalence`.
- **F09**: repros `TestS03_Astra_EarlyFinishCannotCertifyHorizon`, `Test_s03_luna1_short_corpus_cannot_complete`; nuevos `TestBT_S04_ZeroTradeCoveredIntervalCompletes` (cobertura sin trades legítima), pausa parcial (AWAIT sin contexto); heredados `TestHorizonOpenPositionPolicy`, `TestCorpusShortOfHorizonSealsFailVisible`.
- **F10**: repro `Test_s03_sol2_schedule_preflight_closes_causal_gaps`; nuevos `TestSchedulePreflight_RejectsCausalGaps` (5 subtests), `TestSchedulePreflight_AcceptsOverlappingDrainChain` (A→B→C), `TestSchedulePreflight_AcceptsPredecessorCoverageThroughHandover`, `TestSchedulePreflight_RejectsResurrectionABA` + heredados A37/A40/A41.
- **F11**: repro `Test_s03_luna1_result_input_digest_is_verified` (oráculo adaptado: seal rechaza antes de escribir); nuevos `TestBT_S04_ResultIdentitySealBoundaries`, `TestBT_S04_ResultIdentityReadAndVerifyBoundaries` (forgery byte-level en read; footer forjado + inputs alterados en verify); heredados A31 + `TestFinalizeLocalIdempotentAndConflict`.
- **F12**: repro `TestS03_Astra_ResultReproducesWithoutSiblingSpec` (oráculo original, sin adaptación); nuevos `TestBT_S04_StandaloneReproduceClosedSpec`, `TestBT_S04_StandaloneReproduceCallerControlled` (control aplicado + futuro pendiente, replay de admisiones en fronteras).
- **F13**: repro `Test_s03_luna1_closed_control_at_horizon_is_visible` (oráculo adaptado: disposición estructurada visible EN el artifact sellado); nuevos `TestBT_S04_ControlDispositionsAppliedRejectedPending` (before/at/after end), `TestBT_S04_ReplayPreservesControlDispositionsByteIdentical`.
- **F14**: `grep` = 0 referencias a los tres helpers; `TestBT_S04_PublishCLISingleRead` + conformance `TestPublishResult*` / fake-S3.
- **F16**: repro `Test_s03_luna1_reproduce_cmd_is_executable`; `TestReproduceCmdCarriesDigests` adaptado al formato real (contradicción directa finding-vs-test documentada).

## Certification

Comandos ejecutados desde la raíz del repo en `unshare --user --map-root-user --net` (loopback only) con `GOPROXY=off GOSUMDB=off`, `-count=1`, secuencialmente. Logs: workspace externo `bt-s04-20261004/reports/` (`certification.log`, `certification-summary.txt`, `product-evidence-named.log`, `s03-repros-red-baseline.log`, `s03-repros-after-wave1.log`, `s03-repros-after-wave2.log`, `a52-isolated-final.log`).

| Suite | Comando | Resultado |
| --- | --- | --- |
| CLI build | `go build ./v3/backtester/cmd/echo-backtest` | PASS |
| Builds por módulo | `go build ./...` en cada módulo de go.work | Todos los módulos v3 OK (sdk, core, backtester, bridge, e2e, futures-bridge, futures-projector, gateway, lab-worker, toolkit); fallos SOLO en legados `v1/agent`, `v1/core`, `v1/sdk` (pb generado ausente) y `v2/gateway` — **idénticos en el baseline `f41da25c`** (preexistentes, fuera de alcance S04; S04 no toca archivos que esos módulos importen) |
| SDK futures | `go test ./v3/sdk/futures/...` | PASS exit 0 |
| Backtester completo | `go test ./v3/backtester/...` | PASS: paquete principal 396.5s (a52 incluido), artifactstore 0.3s, ndjson 6.0s, simexecution 0.0s |
| Core | `go test ./v3/core/internal/functions ./v3/core/internal/futuresruntime ./v3/core/internal/futuresvertical` | PASS: functions 0.24s, futuresruntime 0.03s, futuresvertical 56.4s |
| Consumers | `go test ./v3/futures-bridge/... ./v3/futures-projector/...` | PASS exit 0 (local-only; sin certificación D6) |
| Repros tagged S03 | `go test -tags s03review ./v3/backtester ./v3/core/internal/functions ./v3/sdk/futures/provider ./v3/sdk/futures/operation -run '^(TestS03_\|Test_s03_)'` | **23/24 PASS**; único rojo `Test_s03_luna1_market_at_end_exclusive` (F15 MINOR abierto). Baseline de entrada: 20 rojos contra `f41da25c` — el rojo era la autoridad y quedó verde sin debilitar asserts |
| Evidencia nominal | 23 tests nombrados (Generic20, GAU50, rollover, determinism, lifecycle, context, cashflow, cobertura, standalone reproduce, tamper, dispositions, publish) | 23/23 PASS |

Nota ambiental: `TestLargeCorpusStreamingMetrics` (A52) es sensible a contención de `ru_maxrss` del proceso hijo cuando la suite corre bajo carga paralela de agentes (falla idénticamente en HEAD y en el árbol S04 bajo esa condición; preexistente). En la certificación secuencial pasó dentro de la suite completa y en aislamiento (351.9s; heap plano ~1.05–1.10 MB y RSS 639 MB con 4× de corpus — métricas del baseline S02 reproducidas).

## Product evidence

- **Generic20**: `TestGeneric100KTwentyAccountDaysE2E` PASS (20 account-days, sizing por fila, economía exacta, COMPLETE reproducible).
- **GAU50**: `TestGAU50SameEngineCausalAdmission` PASS (admisión denegada EN-RUN por el RuleSet real; mismo motor/corpus).
- **Rollover NQH→NQM→NQU**: `TestRolloverE2E_ThreeContractsOneAccount` PASS (continuidad de balance/días/IDs, fills pineados, un solo COMPLETE) + preflight de schedule nuevo.
- **Context**: `TestBT_S04_AwaitContextContinuationSameAccount` PASS (EVALUATION→FUNDED explícito por el caller, misma cuenta, balance/ledger preservados) + transición atómica RuleSet/EOD/boundary.
- **Lifecycle**: PASS/FAIL/STOP/AWAIT_CONTEXT todos con wiring real (4 tests nuevos + repro); sin `PASS=>FUNDED` implícito.
- **Cashflows**: idempotente/conflicto pre y post transición (`TestBT_S04_CashflowReplayAndConflictAcrossTransition`) + P1 heredado.
- **Determinism**: `TestFreshProcessDeterminism` PASS (A/A/B/A + tres procesos OS frescos byte-idénticos vía CLI real), layouts alternativos idénticos (1 parte/chunks/gzip/segundo adapter), replay standalone byte-idéntico con dispositions incluidas.
- **Reproduction standalone**: artifact COMPLETE + corpus original + CLI real → `IDENTICAL` sin archivo lateral, CLOSED_SPEC y CALLER_CONTROLLED (incluye control aplicado y pendiente).
- **Result integrity**: tamper de digest/inputs rechazado nombrado en seal/read/verify; finalize idempotente/conflicto intacto.
- **Persistence**: conformance local/fake-S3 (create-if-absent, conflicto, idempotencia, size cap) + attempts separados del key canónico.

## KISS

Eliminado exactamente: `liveConfigPtr`, `isCashflowDup`, `calendarTransitionKind` (0 referencias en `v3/`); duplicación de `artifactState` en CLI; doble `ReadResult+VerifyResultIntegrity` de `cmdPublish`. `ledger.go` y `risk_eval.go` quedaron sin diff (el fix F06 cambió el caller). Además se añadió la caché O(1) `RunState.lastRev` para eliminar una proyección cuadrática introducida por la revalidación de riesgo por revisión (necesaria para mantener a52 en rango). Sin abstracciones nuevas; sin cleanup general.

## D6 concurrency

| Chequeo | Resultado |
| --- | --- |
| Refresh inicial (inicio S04) | `origin/feature/d6-shot1-execution-vertical` = `d08a30ce9815f820fda7132e20dc42cc345eb8e8` — sin delta nuevo desde el mandato |
| Refresh final (pre-gate) | Mismo `d08a30ce` — cero commits nuevos; delta D6 total desde S03: sólo `v3/futures-bridge/adapters/ninjatrader/*` y `reallane_barrier_test.go` |
| Intersección con S04 | NINGUNA (S04 tocó `v3/sdk/futures/operation`, `v3/backtester/**`, seeds test-only de `v{1,2,3}/sdk/etcd`) |

```text
D6_CONCURRENT_DELTA = NON_CONFLICTING
D6_CONCURRENT_CONFLICT = NO
```

Sin merge/cherry-pick preventivo; sin certificación del gate físico D6 (fuera de alcance); las suites de consumers corrieron local-only.

## Environmental residual

1. `REAL_CONDITIONAL_WRITE = NOT_VERIFIED_ENVIRONMENTAL` (sin credenciales S3 autorizadas; se mantienen fake-S3 conditional + vectores SigV4 + conformance; heredado de S02/S03, sin cambios).
2. Módulos legados `v1/agent`, `v1/core`, `v1/sdk`, `v2/gateway` no compilan — preexistente en el baseline `f41da25c` (verificado en el worktree del baseline), fuera del alcance del programa Backtester V1.
3. `TestLargeCorpusStreamingMetrics` sensible a contención (ver Certification); PASS en certificación secuencial y aislada.
4. Provisioning/upstream físico LIVE de economía sigue fuera de scope (frozen).

## Known limitations

Sólo las ya frozen: sin cross-build determinism claim; sin portfolio multicurrency/FX; sin LIMIT/native MODIFY; sin Campaign Simulator/bankroll; sin checkpoints durables/resume; fixtures Generic20/GAU50 son fixtures de modelo; `BT-S03-F15` MINOR abierto (defensa driver contra adapter no-filtrante, documentado arriba). La limitación S02 de A48 (rama AWAIT_CONTEXT sin productor de outcome) quedó RESUELTA por F05: el wiring existe y está probado.

## Subagent execution

Cuatro subagentes NORMAL reales (B/C/D en ola 1 paralela; A en ola 2), ownership de archivos disjunto, integración por dependencias, repros tagged frozen para subagentes (adaptaciones de oráculo centralizadas y documentadas por el agente owner con justificación in-file). Ningún subagente ejecutó git destructivo, seeds, ni acceso a red/infraexterna.

BT_S04_FINAL_CERTIFICATION_PASS
