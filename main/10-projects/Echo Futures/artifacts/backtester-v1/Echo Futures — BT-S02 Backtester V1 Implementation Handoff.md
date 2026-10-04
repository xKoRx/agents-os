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
| HEAD | `7b857e33` (local, sin push; baseline 7fbd7e99 → línea de integración con 20+ commits de subagentes y lead) |
| Baseline | `xKoRx/echo@7fbd7e990ac…` (`feature/d6-shot1-execution-vertical`, verificado contra `origin` al inicio; sin deltas materiales nuevos) |
| Dirty state | Limpio (worktree de integración); worktrees de subagentes permanecen con sus branches locales |

## SUBAGENTS (todos reales, ONE-SHOT, worktree propio y commits verificables)

| # | SUBAGENTE | Objetivo / ownership | Commit | Resultado |
| --- | --- | --- | --- | --- |
| 1 | Extracción shared (BT-S02 "Worker A") | `market.Engine`/`analytics.Engine` extraídos de los shells StateFun, feed `marketctx`, `sdk/futures/config` con aliases core | `a5a46100` | 292 tests shell+SDK verdes; cero cambio semántico |
| 2 | Operation/IDs/gates | `ExecutionUpdate`/`QuoteUpdate`/`EconomicsObservation`, normalizador fail-closed, `RolloverEntryGate`, entry-expiry, F04/F05 | `4296b673` | suites completas + vertical 92s + S12 replay verdes |
| 3 | Accounting/terms/evaluators | `accounting` FIFO exacto por contrato, `AccountProgramTerms`, `EvaluateEconomicRisk`/`EvaluateLifecycle` puros | `89ae286f` | 13 tests accounting + GAU50 §10.2 |
| 4 | Provider seams | F01 (nil RuleSet), F02 (orden determinista ForceClose), F03 (provenance engine-issued), `AccountContextUpdate`, `ClockFired`/`NextBoundary`, familia `program_required_flat` | `83b98325` | repros adversariales (rojos sin fix) |
| 5 | Strategy rollover/warmup | `HandleWarmupWithScope`, guard stream/timeframe, DRAIN_CYCLE, slots de candidatos | `46bfebfa` | suites strategy/s1/s2 + core verdes |
| 6 | Venue/NDJSON/plan | SimExecution determinista (§12), adapter NDJSON bounded-memory, materializador `MaterializeExperimentPlanV1` + fixture 20 días | `e8dc9ecc` | 41 tests |
| 7 | Result/publisher | ResultWriter streaming, `CompareRecords` primera divergencia, spool + SigV4 create-if-absent + conformance suite | `bca52963`+`2bce944d` | 35 tests (fake S3 + vectores AWS) |
| 8 | SUBAGENTE C (mandato) | accounting/prop/execution review: 8 propiedades | `8e9ba4c8` | 6 PASS, 2 CORREGIDOS (nil-RuleSet clase F01; expiry DAY por map → orden determinista, regresión probada) |
| 9 | SUBAGENTE A (mandato) | parity LIVE/BACKTEST: ingress tipado Core + acceptance §8.2 cruzando decoding real | `ddb53db1` | 192 tests functions; mutación mata el test de paridad |
| 10 | SUBAGENTE D (mandato) | result/persistencia/CLI/determinismo A/B/A | `e9fc4c5d` | gzip byte-idéntico; E2E real 168 records; reproduce IDENTICAL/DIVERGENT |
| 11 | SUBAGENTE B (mandato) | driver/dataset/longitudinal: 14 defectos hallados+corregidos; primera E2E real; rollover 3 contratos | `024e3d59` | COMPLETE con economía exacta; BT-A51 layout-independiente |

Cada uno: worktree propio bajo `/home/kor/aranea/work/bt-s02-20261004/w-*`, branch propio, commit local propio; diffs revisados por el lead antes de integrar.

## INTEGRATION (lead)

Aceptado: todos los commits de subagentes + fixes del lead (`5cd3cad6` esqueleto; composición/driver/pump/proyección `8c0ed8c1`→`f0b1243a`→`bcf6ce83`→`c13ee63d`; integración venue B1 `755b4f31`; CoversThrough `bdfb2943`; RootInputs+orden determinista `b77193e9`; resolución de conflictos B `d552797a`; README `7b857e33`). Conflictos resueltos: `controls.go` (fix EffectiveAt duplicado D/B1), `compose.go`+`driver.go` en el merge B (composición preferida de B + accessors D preservados). Rechazado: nada — todas las desviaciones de subagentes estuvieron dentro de contrato y documentadas.

## TESTS (todos ejecutados en la integración final)

- SDK `go test ./futures/...`: completo ok (operation 80, accounting+provider+strategy+market+marketctx+calendar…).
- Core: `functions` 192 PASS (incl. 6 parity §8.2), `futuresvertical` completa 55s (incl. MKT07 con strategies reales y S12 exact-replay), `futuresruntime` ok.
- futures-bridge y futures-projector: build + tests ok.
- Backtester `go test ./...`: raíz + artifactstore + ndjson + simexecution ok; E2E/rollover/driver/determinismo estables a `-count=2`.
- Determinismo: in-proceso repeat idéntico byte a byte; A/B/A con corpus distinto separa identidades; fresh-process y cross-adapter-parcial cubiertos por layout-independencia in-proc (límite declarado).
- MinIO: suite conformance local 7/7 (fake S3 con semántica If-None-Match + vectores AWS SigV4); sonda REAL contra MinIO Aranea (`sqx-integration-test/bt-s02-conformance-20261004/`) escritura+lectura etag coincidente. **Escritura condicional real: NO_VERIFICADA** (sin credenciales S3 en el entorno; el probe MCP no envía headers condicionales).

## BT-F01..F05 disposition (protocolo frozen; S03 verifica adversarialmente)

| Finding | Estado | Evidencia |
| --- | --- | --- |
| F01 nil RuleSet | `CONFIRMED_FIXED_WITH_REGRESSION_CANDIDATE` | guard `consistency.go` + repro `bt_f01_test.go` (rojo sin fix) + guard análogo en `EvaluateLifecycle` (SUBAGENTE C) |
| F02 ForceClose nondeterminista | `CONFIRMED_FIXED_WITH_REGRESSION_CANDIDATE` | orden de familias fijo + keys lexicográficos + eviction `(seen_seq,key)`; `bt_f02_test.go` 300 sweeps |
| F03 provenance fabricada | `CONFIRMED_FIXED_WITH_REGRESSION_CANDIDATE` | `NewEngine(run)`; ForceClose lleva provenance exacta; `bt_f03_test.go` |
| F04 fill tardío/ajeno | `CONFIRMED_FIXED_WITH_REGRESSION_CANDIDATE` | audit-only post-terminal, sin beginEvent, provenance retenida/unknown; `bt_f04_test.go` 6 casos + parity |
| F05 IDs fuera del clone | `CONFIRMED_FIXED_WITH_REGRESSION_CANDIDATE` | cursores en `OwnerState`, allocator stateless hash; `bt_f05_test.go` retry=idéntico; formato de IDs cambió (hash) |

## EVIDENCE

- **Generic100K horizonte arbitrario**: materializador con DST/días parciales (10 tests) + E2E real con plan materializado y selector por día; fixture 20-días incluida. E2E canónico de 20 días completo: parcial (3 días real + 20-días en plan) — residual S03.
- **NQ ≥3 contratos**: `TestRolloverE2E_ThreeContractsOneAccount` — 2 selecciones+2 activaciones, 6 fills pineados al físico vigente, días/balance continúan (99782.56), cero neteo cross-contract, un solo COMPLETE.
- **Stage transition + cashflow**: transición atómica provider + `SetAccountContext`/`OpenStage` en ledger + control `AccountContextTransition`/`AccountCashflow` tipados con quiescencia/dedup (tests C1/C2/C-sc); payout −500: PnL intacto (tests P1/P8).
- **Core/historical parity**: `futures_operation_parity_test.go` — mismo MMInput/estado/efectos por ingress tipado Core (decoding real) vs historical; raw fail-closed UNAVAILABLE idéntico; mutación mata la paridad.
- **Deterministic replay**: repeat byte-idéntico + A/B/A + `reproduce` IDENTICAL/DIVERGENT con capsule de primera divergencia (RECORD_MISSING seq con field path).
- **Performance**: no-SLA declarado; ndjson 100k records streaming con heap acotado medido (~32MB buffer assertion holgada); E2E 168 records/ms-range. Medición de corpus grande completa (BT-A52): parcial.
- **Persistencia**: create-if-absent real contra fake + conflicto intacto + FAILED→attempts/; real-MinIO condicional NO_VERIFICADA.

## RESIDUAL (para BT-S03/S04)

1. Matriz completa BT-A01..A60: cobertura fuerte en extracción/paridad/economía/rollover/determinismo/persistencia; casos NO ejecutados o parciales: BT-A52 (corpus grande + RSS formal), BT-A43 (20-días canónico completo), OBSERVED_BBO E2E, fresh-process determinism cross-build, conformance MinIO condicional real.
2. `WARMUP_INCOMPLETE` con predicado conservador (cero evaluaciones); conteo fino por módulo pendiente.
3. Mark del MM lee el stream del snapshot (§4.2 baseline documentado — extracción futura S03); alineado en fixtures por ser el mismo instrumento.
4. Wiring productor LIVE de `ExecutionUpdate`/`QuoteUpdate` (los records tipados existen y el ingress los acepta; el productor upstream no existe — no bloquea backtester).
5. BT-F01..F05: verificación adversarial independiente (S03) y cierre (S04).
6. Credenciales autorizadas para conformance condicional MinIO real.

## GATE

`BT_S02_IMPLEMENTATION_READY_FOR_MANAGER_REVIEW`

Producto compila; contrato de implementación materialmente completo; acceptance requerida verde salvo residuales explícitos arriba; sin workarounds backtester-only; evidencia determinista/longitudinal/paridad/persistencia presente; D6 intacto (cero toques a worktree, AddOns, config, gates o egress físico). El programa Backtester NO queda cerrado: sigue BT-S03 adversarial.
