---
type: project
schema_version: 1
owner: agent
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo Forge]]"
sprint: "[[A26Q2S7]]"
start: 2026-08-15
due:
progress: 94
repo: github.com/xKoRx/symphony
jira:
prs:
aliases:
  - Echo Forge MT5 Metrics
  - MT5 Report Scoring
tags:
  - application/echoforge
  - area/echo
  - kind/project
  - project/echo-forge
  - tech/echo-forge
created: 2026-08-15
updated: 2026-08-19
cssclasses:
  - wide
---

# Echo Forge - Reconciliación y Scoring MT5

> [!info]+ Proyecto de agente
> **Parent:** [[Echo Forge]] · **Contrato arquitectónico:** [[Echo Forge - Arquitectura de Datos y Migración de Persistencia#Strategy-MT5 Binding v1]] · **G0-L:** `CLOSED` · **G0-P:** `MVP_PHYSICAL_DESIGN / CLOSED` · **G1-MT5:** `APPROVED / CLOSED` · **A2 Foundation:** `DONE` · **Rollout:** `SHADOW`.

## 🎯 Objetivo

Convertir el reporte `.htm` de MT5 en evidence normalizada y reproducible, reconciliarla contra la evidence exacta del Reretester, calcular un Score explicable y dejar cualquier Decision de invalidación fuera del scoring hasta que una DecisionPolicy versionada haya sido calibrada y aprobada.

Este proyecto es dueño funcional de parser, normalización MT5, reconciliación, scoring, shadow, calibración y fixtures. No es dueño de la identidad transversal, el modelo físico multi-store ni la migración general de Symphony; esos contratos viven en [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]].

```text
HTM raw
→ parser fail-closed
→ Evaluation MT5 + ArtifactRef + TradeSet + MetricSet MT5
→ Reretester MetricSet baseline + MT5 MetricSet candidate
→ ScoreAlgorithm
→ Score shadow
→ DecisionPolicy aprobada
→ Decision opcional
```

## 📊 Estado actual

- El análisis challenge-first está completo a nivel lógico y no modificó código productivo.
- `Strategy-MT5 Binding v1` quedó publicado una sola vez en la nota arquitectónica; este proyecto registra conformance y no duplica el contrato.
- El fixture all-loss confirmó UTF-16LE, filas multi-métrica, costos firmados y el fail-open del parser legacy. El corpus quedó en 4 fixtures reales build 6090 (all-loss + 3 zero-trade, uno de `example_flow_75` pre-hotfix mmLots y dos de `example_flow_4`); mixed win/loss y variantes locale/build siguen siendo aporte del owner.
- `MetricValue`, el catálogo de métricas y `risk_adjusted_delta.v1` son precedentes reutilizables, pero no prueban equivalencia semántica SQX↔MT5 ni autorizan mutar el algoritmo existente.
- El cierre anterior de G0-P/G1-MT5 fue invalidado y rehecho. El owner aceptó A1 como `APPROVED_WITH_FINAL_AMENDMENTS`: identity/generation de StageExecution, token FlowRun, durability Mongo e imported origin quedaron cerrados; M4 queda `UNBLOCKED_BY_G1` bajo ese contrato, sin RankingSnapshot ni Decision.
- La Foundation A2 de persistencia está `DONE` (`legacy|v1`, default `legacy`). No existe persistence `v1_shadow`. El rollout funcional de este proyecto permanece `SHADOW` (calcular/observar, no enforce).
- **M0-NORMAL/M0-TOP/M1/M2-TOP `CLOSED` tras amendment owner (2026-08-16, `550bdb0`+`00a2d7f`)**: `specs/FEAT-SQX-MT5-RECONCILIATION-SCORING/` con CORPUS (4 fixtures build 6090), INVENTORY, METRIC-MATRIX, SDDs parser/normalización y PLAN slices 1–6. Taxonomía owner aplicada: `COMPARABLE` (net_profit, trades), `COMPARABLE_CONDICIONAL` (ret_dd↔Recovery Factor), `PENDING_VERIFICATION` (drawdown variantes, max_drawdown_pct, sharpe, sqn `NO_BINDING_IDENTIFIED_IN_HTM`, profit_factor, win_rate, expectancy, stagnation, cagr, custom) y sin `NO_COMPARABLE` sin evidencia positiva. Evidencia SQX investigada en código real: plugin Overview exporta stats `StatsKey` y calcula `ret_dd = net/drawdown`; `PctDrawdown` existe en el engine pero no se exporta. Proposal `mt5_validation_delta.v1` PENDING_OWNER y abierta (M5-TOP decide set/pesos).
- **M2-NORMAL/M3 `CLOSED` (2026-08-16, `a3ee934`+`e93d02b`+`a23bbaa`)**: TASKS M3N.0–M3N.18; parser fail-closed `sqx/adapters/mt5/report`; normalización in-memory `sqx/adapters/mt5/normalization` (TradeSet 1IN→1OUT, MetricSets native/derived, NDJSON gzip determinista). Sin persistence, scoring, Decision ni Foundation reabierta. `ParseReportHTML` legacy intacto.
- **M4-TOP `CLOSED` (2026-08-17, `055c599`+`582d62b`+`3ff4077`; iteración correctiva `aac9895`+`065a959`, HEAD remoto verificado)**: frontera persistence/binding materializada en `sqx/adapters/mt5/binding` y congelada en `specs/FEAT-SQX-MT5-RECONCILIATION-SCORING/M4-TOP-DECISIONS.md`. Decisiones: stage real `mt5_backtesting@mt5-backtest.v1`; subject STRATEGY **ref-only** (`mt5-subject.v1` = {schema, strategy_ref}; sin artifacts ni Expert en identidad — correctivo BLOQ-1: artifact SHA jamás contamina subject/slot/EvaluationRef; divergencia bajo misma identidad = CONTRACT_CONFLICT por payload digest; Expert a `scope.observed` provenance); scope canónico `mt5-evaluation-scope.v1`; ArtifactRef HTM completo `OUTPUT/MT5_HTM`; TradeSet payload `<htm_key>.tradeset.ndjson.gz` mismo bucket (INVALID sin agregado ni Decision); MetricSets native/derived durables; saga `PersistEvidence` con **UNKNOWN_COMMIT propagado sin recovery in-band** (correctivo BLOQ-2: reconciliación siempre con contexto fresco vía retry Temporal; regresión con ctx vencido mid-write); **BLOQ-3 cerrado en TOP**: StrategyRef se propaga desde `RegisterStrategy` (retorna `id` hoy descartado; correlación exacta `config_id+minio_key`; prohibida inferencia stem/expert) y FlowIntentToken nace una vez en el intake vía `binding.MintFlowIntentToken()` (UUID v4, sin derivación de IDs/wave); BWC sin dual-write. Fix mecánico incluido: `title_test` M3 apuntaba al `<title>`. Tests contrato + regresiones correctivas PASS + race + vet. M4-NORMAL `CLOSED`; M4 completo `CLOSED`.
- `NOT_COMPARABLE` es un estado analítico de Score; no es cero, fallo técnico ni Decision de invalidación.
- **M5-TOP `CLOSED` (2026-08-17, contrato congelado en `M5-TOP-DECISIONS.md`)**: algoritmo `mt5_fidelity_shadow.v1` / impl `1.0.0` / params `mt5-fidelity-shadow.v1`; required `net_profit`/`trades` 0.5/0.5; baseline = exact Reretester FULL trades → `{net_profit,trades}` SQX_NATIVE (nunca `SelectedMetrics`/`WfmMean`); generation 2; PayloadDigest cubre Diagnostics.
- **M5-NORMAL `CLOSED` y M5 `CLOSED` (2026-08-17, HEAD `78de0b02014b550604a00b2c5ef8d4964661abc4`)**: matrices M5N.1–M5N.10 PASS; fix mecánico aislado `cb3b30d` (`ErrWFMMatrixNotFound` NonRetryable). Sin Decision, thresholds, enforce ni lifecycle. last code suite PASS en `a0c9b4d`; docs-only `78de0b0`.
- **M6-NORMAL `CLOSED` (Attempt 7, owner 2026-08-18/19):** workflow `sqx-main-v1-830a9c9d-4118-4ed8-a705-51e5fa84868e` COMPLETED; 13 Scores durables. Esos `COMPUTED` fueron bajo bypass y no calibran DecisionPolicy.
- **M6-TOP `CLOSED` y M6 `CLOSED` (2026-08-19, HEAD `eba11f0`):** canonical symbol/timeframe/configured period + predicado restaurado en `2fb01df`; corrección posterior config-driven: Score inputs por `TaskSpec.Name`, no primer exporter ni folder/stage. Análisis: `specs/FEAT-SQX-MT5-RECONCILIATION-SCORING/M6-TOP-ANALYSIS.md`.
- **M7 `BLOCKED`.** No DecisionPolicy, no enforce, no lifecycle. Próximo trabajo: [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]] (migración big-bang durable).

## 🔍 Reality check funcional

| Área | Evidencia observada | Implicancia para este proyecto |
|---|---|---|
| Parser | `sqx/adapters/mt5/parser.go` no decodifica correctamente el fixture UTF-16LE, toma estructuras decorativas como headers y convierte ausencias en cero/`999` | El parser nuevo debe ser DOM/estructura, fail-closed y preservar missing explícito. |
| Resultado MT5 | `MT5BacktestResult` embebe trades y su writer reemplaza por `(wave_key, strategy_id)` | No extender ese agregado como modelo objetivo; adoptar Evaluation, TradeSet y MetricSet una vez aprobado el mínimo físico. |
| Artefactos | `ArtifactRef` actual conserva `key/size/sha256`; el workflow termina conservando basename | El flujo debe propagar el ref completo aprobado por el binding; SHA verifica contenido, no identifica Evaluation. |
| Métricas | Existe catálogo estático y `MetricValue` soporta `nil + missing_reason` | Reutilizar/evolucionar el catálogo; nunca inventar un segundo catálogo MT5 ni representar missing con sentinels. |
| Scoring | `risk_adjusted_delta.v1` compara dos snapshots con required metrics, pesos, scope y componentes | Puede reutilizarse solo si las definiciones SQX/MT5 son equivalentes; de otro modo se crea otro algoritmo versionado. |
| Ranking/decision | Ranking, verdict y state están mezclados en varios aggregates legacy | Este proyecto produce Score. Ranking y Decision existen solo si un caso funcional/policy los requiere. |
| Fixture all-loss | 31 trades; profit `-441,40`; comisión `-63,15`; swap `0`; net profit `-504,55` | Los costos vienen firmados: para este formato `net = profit + commission + swap`. La resta legacy es incorrecta. |
| Imágenes | El HTM referencia cuatro PNG ausentes | Son evidence opcional y diagnóstico; no bloquean parser ni Score salvo que una métrica declare dependencia explícita. |

## 🧠 Challenges funcionales resueltos

1. **Ingestar un HTM no equivale a validar una Strategy.** La ingesta produce Evaluation/evidence; la validación requiere ScoreAlgorithm y la invalidación requiere DecisionPolicy.
2. **El reporte no es el resultado normalizado.** HTM permanece raw en MinIO; Evaluation, TradeSet y MetricSet registran el significado tipado y sus versiones.
3. **No se compara contra “lo último”.** El baseline es un `Reretester MetricSet` referenciado explícitamente por role; wave y strategy name no bastan.
4. **Dos números con el mismo label no son necesariamente comparables.** Unidad, dirección, sample, periodo, moneda, PnL basis, costos, fórmula, execution model y engine/build forman parte del test de compatibilidad.
5. **Favorable no significa fiel.** Conviene conservar por separado una señal de calidad relativa y otra de fidelidad; cualquier score compuesto exige definición y calibración versionadas.
6. **Missing no redistribuye pesos.** Una métrica requerida ausente produce `NOT_COMPARABLE` o un algoritmo distinto; no se cambia silenciosamente `risk_adjusted_delta.v1`.
7. **SQN y Sharpe no se asumen equivalentes.** Necesitan fórmula/ventana verificadas o quedan fuera de v1 con razón explícita.
8. **Shadow no invalida.** Puede no crear Decision o crear `NO_ACTION`; jamás convierte un umbral provisional en `INVALIDATED`.
9. **Las trades son evidence primaria, no métricas.** TradeSet se conserva separado para recalcular MetricSets sin reejecutar MT5.
10. **El parser puede avanzar antes del modelo físico.** Decoder, fixture contract, mapping y goldens son reversibles; persistencia/wiring no.

## 🔗 Contrato consumido y conformance

Fuente canónica: [[Echo Forge - Arquitectura de Datos y Migración de Persistencia#Strategy-MT5 Binding v1]]. Si esta lista contradice la fuente, manda la fuente y el gate se reabre.

| Invariante consumida | Conformance MT5 |
|---|---|
| Strategy y Wave no forman la identidad del reporte | Se exige `strategy_ref`; `canonical_strategy_id` queda como external key, `logical_type` se reutiliza para agrupación/policies y `wave_key` queda como contexto. |
| Origin + participation | El FlowRun MT5 registra participación/reprocessing sin reemplazar el FlowRun donde nació la Strategy ni duplicarla. |
| MT5 backtest es una StageExecution | Retry técnico conserva la intención; rerun deliberado crea otra ejecución/evaluación. La clave física sigue gated. |
| Backtest exitoso produce una Evaluation MT5 | Evaluation contiene scope/producer y referencias; no contiene Score ni Decision. |
| HTM es ArtifactRef completo | Requiere store/bucket/object_key/size/sha256/content_type; no basename. |
| Trades y métricas se separan | Parser produce TradeSet y uno o más MetricSets; no embebe todas las trades en MetricSet. |
| Dirección Evaluation←children | MetricSet y TradeSet guardan `evaluation_ref`; Evaluation no mantiene arrays autoritativos mutables de children. |
| Baseline es explícito | Score input role `baseline` referencia Reretester MetricSet; role `candidate` referencia MT5 MetricSet. |
| Missing/comparability son estados | `MISSING`, `INVALID` y `NOT_COMPARABLE` no se convierten en `0`, `999` ni Decision. |
| Recovery cruza stores | Evidence persiste antes de completar StageExecution; retry recupera por identidad lógica aprobada. |

## 📜 Contrato funcional MT5

### Input de ingesta

```yaml
strategy_ref: required after G1-MT5
flow_run_ref: required after G1-MT5
stage_execution_ref: required after G1-MT5
input_artifacts:
  - exact executable/strategy lineage refs available from the workflow
report_artifact:
  store: minio
  bucket: required
  object_key: required
  size: required
  sha256: required
  content_type: text/html
parser_contract:
  parser_version: required
  expected_encodings/locales/builds: explicit allow-list or supported matrix
```

### Output de ingesta

```yaml
evaluation:
  stage: mt5_backtest
  scope: engine, build, broker, instrument, timeframe, period, deposit, currency, leverage, tick_model, costs, pnl_basis, locale, timezone
  artifacts: HTM and exact inputs by role
trade_set:
  evaluation_ref: required canonical parent reference
  normalized orders/deals/trades evidence or externalized payload ref
  parser/schema version and exact counts
metric_sets:
  evaluation_ref: required canonical parent reference
  MT5_NATIVE: observed values
  DERIVED_VALIDATION: independently derived values
  CUSTOM_RJARA: separate shadow evidence
diagnostics:
  structural, missing, reconciliation and optional-artifact diagnostics
```

Native, derived y custom no se pisan. Un valor nativo y su derivación de auditoría pueden coexistir bajo definitions distintas o roles explícitos.

### Contrato de comparación y Score

```yaml
score_algorithm:
  algorithm_id: approved immutable version
  inputs:
    baseline: exact Reretester MetricSet ref
    candidate: exact MT5 MetricSet ref
  comparability_predicate: required
score:
  status: COMPUTED|NOT_COMPARABLE|INVALID_INPUT
  value: typed or null
  components: raw values, normalized signals, weights and reasons
  provenance: algorithm, implementation, parameter set and input refs
decision:
  absent or NO_ACTION during shadow unless an approved policy explicitly runs
```

El modelo general admite N ScoreInputs con roles declarados. El algoritmo v1 observado usa exactamente dos; no se generaliza su semántica bajo el mismo ID.

## 📐 Scope comparable

| Dimensión | Regla v1 |
|---|---|
| Strategy | Misma `strategy_ref`; el external key solo ayuda a resolver lineage. |
| Stage/evidence | Baseline de Reretester explícito y candidate MT5 explícito; nunca selección por latest. |
| Instrument/timeframe | Igualdad o transformación declarada por el algoritmo; por defecto exacta. |
| Period/sample | Fechas y sample equivalentes; FULL/IS/OOS no se mezclan. |
| Capital/currency | Igualdad o normalización versionada demostrable. |
| PnL/costs | Misma base y convención de signos; comisiones/swap/spread declarados. |
| Execution model | Tick model, broker/build y demás factores relevantes registrados; incompatibilidad produce `NOT_COMPARABLE`. |
| Metric semantics | Definition/version, unidad, dirección, fórmula y ventana compatibles. |

## 📚 Catálogo funcional inicial

| Grupo | Tratamiento |
|---|---|
| Nativas prioritarias | `net_profit`, `drawdown`, `profit_factor`, `sharpe_ratio`, `trades`, `win_rate`, `expectancy`, `stagnation`; importar solo con label/unidad/scope verificados. |
| Derivables de auditoría | PnL y costos, trade count, win rate, PF, expectancy, curva closed-trade, DD cerrado, monthly PnL y `ret_dd`; conservar separados de nativos. |
| Compatibilidad pendiente | `sqn_score`, Sharpe derivado y ratios cuya fórmula SQX/MT5 no esté demostrada; `null + missing_reason` o definition distinta. |
| `CUSTOM_RJARA` | `rr_recent_max_win_loss_v1`, recovery de peor racha mensual y cobertura de año negativo; evidence shadow hasta contar con ventanas/fixtures suficientes. |

## 🧮 Hipótesis de scoring a especificar, no aprobadas para enforce

La señal simétrica existente es un candidato de reutilización:

```text
si candidate == 0 y baseline == 0: signal = 0
signal(candidate, baseline, direction) = clamp((candidate - baseline) / (abs(candidate) + abs(baseline)), -1, 1)
si lower_is_better: signal = -signal
```

- `quality_delta_score` puede mapear la calidad relativa sobre `0..100` si el algoritmo y sus required metrics quedan aceptados.
- `fidelity_score` puede medir distancia absoluta sin premiar divergencia favorable.
- `preservation_score` y `mt5_validation_score.v1` siguen siendo hipótesis funcionales; requieren SPEC, casos frontera y calibración antes de considerarse contrato.
- Los pesos risk-first existentes (`ret_dd` 25%, `profit_factor` 20%, `sharpe_ratio` 20%, `sqn_score` 15%, `drawdown` 15%, `net_profit` 5%) no se heredan automáticamente si SQN/Sharpe o el scope no son comparables.

## 🧪 Fixtures y mapping requerido

| Fixture | Estado | Cobertura |
|---|---|---|
| `example_flow_75` zero-trade (pre-hotfix mmLots) | DISPONIBLE | UTF-16LE, ausencia de operaciones, métricas degeneradas/missing. |
| `repo:symphony/mt5-export.htm` all-loss | DISPONIBLE | UTF-16LE, build 6090, filas multi-métrica, Orders/Deals, 31 trades, costos firmados, PF 0.00. |
| `example_flow_4` zero-trade ×2 (`Strategy_7_1_15/27`) | DISPONIBLE | Misma forma estructural con Expert/Inputs/CustomComment distintos; regresión de estabilidad. |
| Mixed win/loss | FALTANTE | PF/R:R/recovery no degenerados, rachas y reconciliación positiva/negativa. |
| Locale/build alternativos | PENDIENTE_DE_EVIDENCIA | Decimales, labels, encoding y estructura variantes. |

Fuente canónica del corpus: `specs/FEAT-SQX-MT5-RECONCILIATION-SCORING/CORPUS.md` (checksums, provenance y expectativas por campo).

Cada fixture debe tener checksum, provenance, encoding/locale/build, expected structural counts y expectativas por campo. La matriz SDD debe mapear `campo HTM → valor tipado → definition/source → scope → cardinalidad → missing rule → query consumidora`.

## 🚦 Gates

| Gate | Estado | Condición |
|---|---|---|
| G0-L arquitectura | `APPROVED_BY_OWNER / CLOSED` | Modelo lógico y amendments owner vigentes. |
| G0-P arquitectura | `MVP_PHYSICAL_DESIGN / CLOSED` | A1 v1 + final amendments está congelada para implementación. |
| G1-MT5 físico | `APPROVED / CLOSED` | Conformance 19/19 PASS; Foundation A2 `DONE` (`legacy|v1`). M4 adopta A1 + Foundation y mantiene RankingSnapshot/Decision fuera. |
| G2-REAL-WORKLOAD | `BLOCKED_BY_SHADOW_WAVES` | Workload real valida assumptions y alimenta ajustes de Arquitectura. |
| M1 parser/normalización | `CLOSED` | SDDs fail-closed escritos, verificados contra corpus y corregidos por amendment owner (`SPEC-PARSER`, `SPEC-NORMALIZATION`); sin writers ni IDs gated. |
| M2-NORMAL TASKS | `CLOSED` | `TASKS.md` atomiza PLAN slices 1–2; M4+ fuera. |
| M3 parser implementation | `CLOSED` | Parser + normalización in-memory verificados; VERIFICATION PASS. Persistence/scoring siguen M4+. |
| M4-TOP persistence binding | `CLOSED` | Frontera durable MT5 cerrada en `sqx/adapters/mt5/binding` + `M4-TOP-DECISIONS.md`; subject/scope/producer contract/TradeSet/MetricSets/recovery/BWC sin ambigüedad. |
| M4-NORMAL wiring | `CLOSED` | Wiring/tests Foundation adoptados; M4 completo `CLOSED`. |
| M5-TOP scoring contract | `CLOSED` | Comparability y `mt5_fidelity_shadow.v1` congelados; baseline exact Reretester. |
| M5-NORMAL verification | `CLOSED` | Matrices M5N.1–M5N.10 PASS; M5 completo `CLOSED`. |
| M6-NORMAL shadow waves | `CLOSED` | Attempt 7 E2E COMPLETED; 13 Scores bajo bypass. |
| M6-TOP semantic close | `CLOSED` | Canonical symbol/timeframe, CFX configured period, predicado restaurado. Ver `M6-TOP-ANALYSIS.md`. |
| Enforce | `BLOQUEADO` | Calibración, falsos descartes, policy versionada y aprobación humana. M7 `BLOCKED`. |

## ✅ Tareas

### M0-NORMAL — Corpus e inventario

**Modelo recomendado: NORMAL** · **Por qué:** extracción mecánica con contrato claro. · **Puede ejecutar:** fixtures, checksums, locale/build, HTML fields y expected counts. · **Debe escalar a TOP si:** aparece estructura ambigua o exige cambiar semántica.

- [x] **M0N.1 — Verificar brownfield y registrar binding/conformance sin duplicarlo** #owner/agent #type/research #area/echo
- [x] **M0N.2 — Completar corpus mixed/locale/build con checksum, provenance y expectativas** #owner/agent #type/research #area/echo — CORPUS.md; mixed/locale quedan como gaps owner documentados
- [x] **M0N.3 — Completar inventario mecánico campo HTM→raw/typed candidate** #owner/agent #type/research #area/echo — INVENTORY.md

### M0-TOP — Mapping semántico

**Modelo recomendado: TOP** · **Por qué:** equivalencia MetricDefinition y comparability SQX↔MT5. · **Puede ejecutar:** native/derived/missing, units, scope y formulas. · **Debe escalar a TOP si:** siempre; no delegar decisiones semánticas a NORMAL.

- [x] **M0T.1 — Cerrar matriz HTM↔MetricDefinition↔SQX y resolver SQN/Sharpe/pesos candidatos** #owner/agent #type/design #area/echo — METRIC-MATRIX.md corregida por amendment owner: SQN `PENDING_VERIFICATION/NO_BINDING_IDENTIFIED_IN_HTM`, Sharpe `PENDING_VERIFICATION`, pesos proposal PENDING_OWNER abierta

### M1 — SPEC parser y normalización

**Modelo recomendado: TOP** · **Por qué:** contrato fail-closed, TradeSet/MetricSet/provenance y casos límite. · **Puede ejecutar:** RCA/BUGFIX UTF-16/DOM/costos y CHANGE missing/normalización. · **Debe escalar a TOP si:** siempre durante authoring/verificación contractual.

- [x] **M1.1 — Escribir y verificar SDD separados de parser y normalización sin persistencia definitiva** #owner/agent #type/spec #area/echo — SPEC-PARSER.md + SPEC-NORMALIZATION.md

### M2 — PLAN y TASKS

**Modelo recomendado: TOP para PLAN; NORMAL para atomización** · **Por qué:** boundaries/BWC/dependency ordering requieren juicio; tareas mecánicas no. · **Puede ejecutar:** TOP define slices/rollback, NORMAL descompone archivos/tests/comandos. · **Debe escalar a TOP si:** una task reabre interface, schema o dependency.

- [x] **M2T.1 — Crear PLAN por slices parser, evidence, artifact propagation, persistence, scoring y rollout** #owner/agent #type/plan #area/echo — PLAN.md slices 1–6 (M3→M6); corregido por amendment (sin legacy projection desde v1; consumer brownfield `deviation_activity` documentado)
- [x] **M2N.1 — Crear TASKS atómicas; writers declaran dependencia G1-MT5** #owner/agent #type/plan #area/echo — TASKS.md M3N.0–M3N.18; M4+ explícitamente fuera

### M3 — Parser implementation

**Modelo recomendado: NORMAL** · **Por qué:** SPEC cerrada y trabajo local determinista. · **Puede ejecutar:** decoder/DOM, mapping aprobado y goldens. · **Debe escalar a TOP si:** fixtures contradicen estructura, missing o fórmula.

- [x] **M3.1 — Implementar parser fail-closed y preservar raw + typed + missing status** #owner/agent #type/dev #area/echo — `sqx/adapters/mt5/report` + `normalization`
- [x] **M3.2 — Validar zero/all-loss/mixed/locales y `-441,40 + -63,15 + 0 = -504,55`** #owner/agent #type/test #area/echo — all-loss/zero-trade PASS; mixed/locales siguen gaps owner, no inventados

### M4 — Persistence y binding (`UNBLOCKED_BY_G1`; secuencialmente después de M0–M3)

**Modelo recomendado: TOP para primera boundary; NORMAL para wiring/tests** · **Por qué:** Evaluation/TradeSet/MetricSet/ArtifactRef/recovery cruzan stores. · **Puede ejecutar:** TOP adopta G1-MT5 y Foundation `legacy|v1`; NORMAL completa adapters y pruebas repetitivas. · **Debe escalar a TOP si:** cambia identity, idempotency, BWC o recovery.

- [x] **M4T.1 — Adoptar IDs/envelope G1-MT5, direction Evaluation←children y recovery StageExecution↔evidence** #owner/agent #type/dev #area/echo — `sqx/adapters/mt5/binding` (contract/scope/subject/evidence/persist + tests); decisiones en `M4-TOP-DECISIONS.md`
- [x] **M4N.1 — Implementar wiring/repositories/tests aprobados y propagar ArtifactRef completo** #owner/agent #type/dev #area/echo — M4-NORMAL CLOSED en sesión previa; M4 completo CLOSED

### M5 — Reconciliation y ScoreAlgorithm

**Modelo recomendado: TOP para contrato/implementación inicial; NORMAL para matrices de tests** · **Por qué:** comparability, N-input contract y fórmula son decisiones caras. · **Puede ejecutar:** TOP scoring reproducible; NORMAL casos parametrizados. · **Debe escalar a TOP si:** una métrica o scope no es equivalente.

- [x] **M5T.1 — Especificar e implementar comparability predicate, ScoreAlgorithm versionado y Score shadow** #owner/agent #type/dev #area/echo — `mt5_fidelity_shadow.v1` (`core/evaluation/mt5_fidelity.go`, bridge baseline `binding/baseline.go`, Score `adapters/mt5/scoring`, activity `mt5_score_shadow_v1`, wiring en `generic_workflow.go`); decisiones en `M5-TOP-DECISIONS.md`
- [x] **M5N.1 — Expandir tests parametrizados sin redistribuir required metrics ni mezclar `CUSTOM_RJARA`** #owner/agent #type/test #area/echo — M5N.1–M5N.10 CLOSED; evidencia `M5-NORMAL.md` + `VERIFICATION.md`

### M6 — Shadow verification y G2

**Modelo recomendado: NORMAL para waves/evidence; TOP para interpretación** · **Por qué:** ejecución es mecánica, calibración/feedback no. · **Puede ejecutar:** NORMAL recopila workload/scores; TOP interpreta distributions, errores y assumptions. · **Debe escalar a TOP si:** aparece drift, falsa comparabilidad o cambio arquitectónico.

- [x] **M6N.1 — Ejecutar waves shadow y recopilar workload, duplicates, latency, reprocessing y recovery** #owner/agent #type/test #area/echo — Attempt 7 CLOSED como M6-NORMAL
- [x] **M6T.1 — Analizar false positives/negatives, comparability y feedback para G2-REAL-WORKLOAD** #owner/agent #type/test #area/echo — `M6-TOP-ANALYSIS.md`

### M7 — Calibration, DecisionPolicy y enforce

**Modelo recomendado: TOP** · **Por qué:** thresholds, falsos descartes, policy y lifecycle requieren juicio experto y owner. · **Puede ejecutar:** propuesta versionada y verificación final. · **Debe escalar a TOP si:** siempre; NORMAL no decide thresholds ni enforce.

- [ ] **M7.1 — Calibrar parameter set/DecisionPolicy y pedir aprobación owner antes de enforce** #owner/agent #type/design #area/echo

## ✅ Criterios de aceptación

- Los encodings/locales soportados tienen golden; una estructura desconocida falla con diagnóstico y sin datos parciales silenciosos.
- El fixture all-loss reconcilia exactamente counts y `-441,40 + -63,15 + 0 = -504,55`; ausencia, infinito y casos sin pérdidas no usan `0/999` como sentinel.
- Native, derived y custom nunca se sobrescriben; todo null tiene status/reason y version/provenance.
- Cada Score referencia el baseline/candidate exacto, valida scope antes de calcular y reconcilia value contra componentes, pesos y parameter set.
- Reingesta/retry no duplica evidence; reevaluación deliberada crea otra Evaluation según el contrato aprobado.
- El modo shadow no altera lifecycle de Strategy ni materializa invalidación automática.
- El pipeline durable usa exclusivamente el blueprint A1 aprobado y comienza solo después de M0–M3, aunque G1-MT5 ya esté cerrado.

## 🚫 Fuera de alcance

- Rediseñar compilación/backtest MT5, exporter SQX, buckets/keys MinIO o la arquitectura transversal desde esta nota.
- Inferir trades, equity intratrade o métricas que el HTM no demuestra.
- Crear IDs/collections/tablas distintos de A1 o saltarse la secuencia M0–M3 antes de M4.
- Mutar `risk_adjusted_delta.v1`, hardcodear thresholds o presentar el score heurístico como performance futura.
- Implementar código productivo en esta revisión documental.

## 🧭 Decisiones

### Cerradas en esta iteración

- El binding tiene una sola fuente canónica en arquitectura; MT5 registra conformance.
- G0-L está cerrado con `logical_type` reutilizado, origin + participation y direction Evaluation←MetricSet/TradeSet.
- Evaluation, MetricSet, TradeSet, Score y Decision son conceptos separados.
- El baseline se referencia exactamente; no se resuelve por “latest”.
- `NOT_COMPARABLE` no es cero ni Decision.
- Shadow no invalida y Score no gobierna lifecycle.
- Parser/fixtures pueden avanzar antes del modelo físico; writers no.

### Pendientes de owner/evidencia

- Aportar fixture mixed win/loss y confirmar locales/builds reales.
- Resolver equivalencia SQN/Sharpe y aceptar o reemplazar el algoritmo/pesos candidatos.
- Aprobar parameter set, thresholds y DecisionPolicy solo después de waves shadow/calibración.

## 📆 Bitácora

- **2026-08-15** — Proyecto creado para ingesta HTM, reconciliación y scoring conservador en shadow.
- **2026-08-15** — Auditoría brownfield confirmó fixture zero-trade, fixture all-loss UTF-16LE, parser fail-open, costos firmados y ArtifactRef truncado por basename.
- **2026-08-15** — Revisión challenge-first v0.3: el proyecto queda separado de arquitectura, consume el binding canónico por referencia, distingue Evaluation/MetricSet/TradeSet/Score/Decision y bloquea persistencia hasta G1-MT5.
- **2026-08-15** — Owner aprueba G0-L con amendments: `logical_type` conserva su nombre/semántica; FlowRunStrategy preserva origin + participation; MetricSet/TradeSet referencian Evaluation sin arrays inversos autoritativos; RankingSnapshot deja storage de entries abierto. Fases reorganizadas M0–M7 por modelo TOP/NORMAL; G0-P pasa a diseño físico MVP y G2 recibe la medición real posterior.
- **2026-08-16** — Arquitectura cerró A1/G0-P y la matriz de conformance cerró `G1-MT5 = APPROVED / CLOSED`. M4 queda desbloqueado para adoptar el diseño cuando complete M0–M3; el próximo trabajo real sigue siendo M0N.2–M0N.3. Shadow, comparability y enforce conservan sus gates.
- **2026-08-16** — Corrección de cierre: la primera aprobación física se invalidó por blueprint incompleto y fue supersedida por `A1 — PHYSICAL MODEL v1`; la nueva conformance excluye RankingSnapshot/Decision, confirma Core/adapters sin cambios SDK y vuelve a cerrar G0-P/G1-MT5 con M4 habilitado bajo contrato.
- **2026-08-16** — Amendments finales owner cerrados sin reabrir G0-L: StageExecution formula/unique, `flow_intent_token`, durability Mongo majority, imported origin y rollback sin legacy gaps. Conformance `19/19 PASS`; G0-P/G1-MT5 permanecen cerrados y M4 queda `UNBLOCKED_BY_G1` después de M0→M1→M2→M3.
- **2026-08-16** — `ARCHITECTURE FREEZE` registrado: limpieza final no cambia conformance ni secuencia. G0-P/G1 permanecen cerrados; el próximo trabajo MT5 sigue siendo M0N.2, M0N.3 y M0T.1.
- **2026-08-16** — Foundation A2 de persistencia queda CLOSED/DONE (`8336122`, `legacy|v1`). Este proyecto es el trabajo activo: M0N.2, M0N.3 y M0T.1. El shadow de scoring se mantiene; no hay persistence `v1_shadow`. M4 sigue después de M0–M3.
- **2026-08-16** — M0+M1+M2T ejecutados y commiteados (`0b96e63`, `specs/FEAT-SQX-MT5-RECONCILIATION-SCORING/`). Corpus ampliado a 4 fixtures reales (hallazgo: 2 HTM de `example_flow_4` en Downloads, ambos zero-trade pre-hotfix; all-loss y zero-trade comparten Expert con mmLots 0.0 vs 0.1 — evidence real del caso dos-ejecuciones-misma-identidad). Inventario campo↔typed completo (formatos compuestos `v (p%)`/`p% (v)`/`n ($v)`, fila totales Deals, `Margin Level` sin valor). Matriz semántica: `net_profit` COMPARABLE; `drawdown/max_dd_pct/win_rate/PF/expectancy` COMPARABLE_CONDICIONAL (basis SQX a verificar en M5); `ret_dd/sharpe/sqn/stagnation` NO_COMPARABLE_V1; `risk_adjusted_delta.v1` no reutilizable (predicado same-stage) → proposal `mt5_validation_delta.v1` PENDING_OWNER. SDDs parser/normalización fail-closed sin persistencia. PLAN slices 1–6. Pesos, fixture mixed y locale/build esperan owner sin bloquear M2N/M3. Próximo paso exacto: M2N.1.
- **2026-08-16** — **Amendment owner (micro-corrección TOP)** aplicado y pusheado (`550bdb0` semántico + `00a2d7f` cierre; HEAD remoto verificado `00a2d7f`): taxonomía nueva COMPARABLE/COMPARABLE_CONDICIONAL/PENDING_VERIFICATION/NO_COMPARABLE (solo con evidencia positiva; ninguna fila la usa). Correcciones: Sharpe y SQN pasan a PENDING_VERIFICATION (sin afirmar fórmulas MT5 no demostradas; `sqn_score` queda `NO_BINDING_IDENTIFIED_IN_HTM` y prohibido mapear Z-Score↔SQN); contradicción GP/GL resuelta (basis no se concluye del corpus; GL observado coincide con el neto, Σprofit-only -441.40; all-loss no distingue bases de PF); 4 variantes DD preservadas con nombres canónicos (`equity_dd_max_money`, `equity_dd_pct_at_max_money`, `equity_dd_max_pct`, `equity_dd_money_at_max_pct` + `balance_*`); `ret_dd`↔Recovery Factor COMPARABLE_CONDICIONAL (plugin calcula `ret_dd = net/drawdown`, verificado en `EchoForgeOverviewExporter.overviewFromStats`; MT5 RF = net/DD verificado; condición: variante DD); TradeSet assembly fail-closed solo patrón demostrado 1in→1out (cualquier ambigüedad → `INVALID/UNPROVEN_ASSEMBLY_PATTERN`, sin soporte universal para patrones no demostrados); `trade_key` ahora source-based `sha256(canonical(open_deal_id + ordered close_deal_ids))`; PLAN sin legacy projection desde v1 (consumer brownfield real identificado: `deviation_activity.go` lee `LoadMT5BacktestResult`; writer `mt5_activities.go` es camino legacy) y proposal de scoring abierta para M5-TOP. M0-NORMAL/M0-TOP/M1/M2-TOP `CLOSED`; M2-NORMAL `READY / NOT STARTED`.
- **2026-08-16** — M2-NORMAL + M3 CLOSED y pusheados (`a3ee934` TASKS + cleanup SPECS deviation-filter; `e93d02b` parser/normalizer; `a23bbaa` VERIFICATION/cierre). HEAD remoto `a23bbaaaf051dab5e84d0a106dd9be90cb949794`. Tests report/normalization + race + vet + legacy parser PASS; staticcheck OMITTED. Gaps abiertos: mixed, locales/builds, PF/win-rate basis, Sharpe MT5, SQN binding, Drawdown SQX, scoring/DecisionPolicy. Próximo: M4-TOP READY / NOT STARTED. Foundation no reabierta.
- **2026-08-17** — M4-TOP CLOSED y pusheado (`055c599` fix test M3 + `582d62b` docs decisiones + `3ff4077` boundary code). Preflight: el fix M3 (`e45bb98`) tenía una regresión mecánica — `title_test` reemplazaba `>Strategy Tester Report<`, que matchea primero el `<title>` fuera de las tablas, no el heading real de la tabla 0; corregido a `<b>Strategy Tester Report</b>` y todo M3 PASS. Reality check con código: stage real `mt5_backtesting` (activity `mt5_backtest_artifact`), ArtifactRef completo se pierde en `generic_workflow.go:2937` (basename), `mt5_backtest_results` Mongo sólo la escribe el flujo adaptive legacy, Foundation cableada pero `_ = durable` sin consumidor, sin producer de StrategyRef en el flujo artifact. Boundary: paquete `sqx/adapters/mt5/binding` — `mt5-backtest.v1`, subject STRATEGY, scope `mt5-evaluation-scope.v1`, saga `PersistEvidence` con guards fail-closed, payload MinIO colocado, CAS complete. INVALID sin TradeSet ni Decision. Tests contrato + race + vet PASS; gofmt/diff-check PASS; staticcheck omitido. Gap documentado: port sin transición Fail durable (Foundation no se reabre).
- **2026-08-17** — **Iteración correctiva M4-TOP** (3 findings de review, `aac9895` code + `065a959` docs; HEAD remoto `065a9593359e01dc5ba3825c7c869a3fe8417e8c` verificado, tree clean). **BLOQ-1**: artifact SHA contaminaba Evaluation identity vía `SubjectSnapshot.InputArtifacts` → subject ahora ref-only (`BuildSubject(strategyRef)`, digest de {schema, strategy_ref}); Expert desafiado y movido a `scope.observed` provenance; confirmado contra Foundation que el slot STRATEGY usa token `ref:<StrategyRef>` (el digest sólo entra en `NewEvaluationRef`); artifacts completos siguen en evidence y ligan el payload digest → misma identidad + artifacts distintos = CONTRACT_CONFLICT; regresiones `TestEvaluationIdentity_IgnoresArtifacts` y `TestEvidenceDigestStillBindsArtifacts`. **BLOQ-2**: `putWithRecovery` reutilizaba el ctx capturado → eliminado; UNKNOWN_COMMIT propaga de inmediato (`putImmutable`) y la reconciliación con ctx fresco ocurre por retry Temporal (decisión documentada: mínima y compatible; no factory de recovery-contexts); regresión `TestPersistEvidence_UnknownCommitNeverRecoversOnExpiredContext` (deadline vencido mid-write, cero `Load*` sobre ctx muerto, convergencia con reentrada fresca). **BLOQ-3**: StrategyRef y FlowIntentToken cerrados en TOP (§2.10 del decisions doc): StrategyRef se propaga desde `RegisterStrategy` (`postgres_registry.go:86` ya retorna `id` con `RETURNING`; caller `steps.go:840` lo descarta; correlación exacta `config_id+minio_key`; prohibida inferencia stem/expert — `ArtifactStem` es opaco y no revierte CanonicalStrategyID); FlowIntentToken nace una vez en el intake del watcher vía `binding.MintFlowIntentToken()` (UUID v4 sin derivación; viaja durable→workflow inputs; retry/continue-as-new lo preservan; rerun = nuevo intake = nuevo token); M4N rehecho a M4N.1–M4N.9 puramente mecánico. Verificación completa 6 suites + race + vet + gofmt + diff-check PASS.
- **2026-08-17** — **M5-TOP CLOSED y pusheado** (`90c58cf` docs + `60cf20a` feat + `e7f2c5a` test; HEAD remoto `e7f2c5a217708a5187a2ff67449068bac0c3fcae` verificado, tree clean). Preflight HEAD inicial `69f48c9` (parent `9cb4ded` ajeno preservado). Reality check: no existe MetricSet Foundation del lado SQX; el único resultado durable de la estrategia efectivamente exportada a MT5 es `selected_robust_runs.SelectedMetrics` (sin scope de comparability); `risk_adjusted_delta.v1` no reutilizable (same-stage + `symmetricSignal` premia mejora, no mide fidelidad) → algoritmo nuevo de FIDELIDAD `mt5_fidelity_shadow.v1` (required metrics net_profit/trades 0.5/0.5, `signal = 1 − |c−b|/(|c|+|b|)`, score 0..100). Baseline: materialización Foundation con stage explícito `sqx_baseline_materialize@sqx-baseline.v1` (subject STRATEGY ref-only, scope `sqx-baseline-scope.v1` con dims legacy explícitamente MISSING) desde `SelectedRobustRunKey` recomputado determinísticamente. Candidate: MetricSet `MT5_NATIVE` exacto del reconcile (retorna `MetricSetRefs`). Predicado cross-stage congelado; scope/métrica REQUIRED ausente → NOT_COMPARABLE con razón tipada; sin redistribución de pesos. Score immutable por `NewScoreRef` (CreatedAt fuera de identidad); PutScore ACK/duplicate/CONTRACT_CONFLICT/UNKNOWN_COMMIT. Wiring `mt5_score_shadow_v1` tras `mt5_reconcile_v1`. Shadow absoluto (test: sólo escribe evaluation+metric_set+score). Gap documentado: los Scores reales serán NOT_COMPARABLE por scope gaps del baseline legacy (currency/period/pnl_basis/sample) hasta que el producer SQX los exporte — M6 recolecta evidencia para la v2. Suites: core/evaluation, domain, adapters/mt5 (incluye binding+scoring), metadata-mongo, worker, workflows + race + vet + gofmt + diff-check PASS; staticcheck OMITTED (tool ausente); `tools/` build falla por condición preexistente (múltiples main).
- **2026-08-17** — **M5-NORMAL CLOSED y M5 CLOSED** (HEAD remoto `78de0b02014b550604a00b2c5ef8d4964661abc4`, tree clean). Preflight HEAD `68d569bd991a6e3023684e2de8b9e93e245f0a17`. Fallo mecánico M5-TOP (clasificación A): `ErrWFMMatrixNotFound` dejó de ser NonRetryable tras el bridge Reretester; fix aislado `cb3b30d` sin reinterpretar TOP. Tests: `9a5eaac` matrices fidelity/comparability/goldens; `a0c9b4d` bridge Reretester/SHA/activity; `78de0b0` docs. Exact path verificado: selected_robust_run_key → unique FULL → MinIO key/SHA → trades → `{net_profit,trades}` → SQX_NATIVE. WFM SelectedMetrics no usado como baseline. Diagnostics en PayloadDigest. Generation 2. Production activity con currency/period missing → durable `NOT_COMPARABLE` (correcto; no copy desde MT5). Shadow guard: Decision/thresholds/enforce/lifecycle NO. `staticcheck` INFRA_BLOCKED. Próximo: M6-NORMAL READY / NOT STARTED. Proyecto de agente permanece abierto.
- **2026-08-19** — **M6-TOP CLOSED y M6 CLOSED**. HEAD inicial `34cbe79`. Bypass de instrument/timeframe/period eliminado. Canonical symbol reutiliza catálogo Echo lowercase + alias `xauusd_darwinex`. Timeframe lowercase único. Configured period = CFX `Data/Setups` (`2016-01-04`→`2026-06-05` en example; no first/last trade; no OOS; no additional markets). Predicado completo restaurado. Baseline exact Reretester intacto. Folders dinámicos auditados. `mt5_fidelity_shadow.v1` no se mutó: útil solo como baseline experimental. Attempt 7 (13 Scores) no calibra DecisionPolicy; con predicado real sería `NOT_COMPARABLE` por periodo SQX vs MT5 julio 2026. Tests evaluation/runtime/mt5/worker/workflows + race + vet PASS. M7 BLOCKED. Listo para review humana. Próximo: [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]].
- **2026-08-18** — Checkpoint M6-NORMAL, **no cerrado**. Direct-cutover Foundation + binding StrategyRef/SelectedRobustRunKey en Attempts 2–6. Attempt 6: 11 Scores `NOT_COMPARABLE` (XAUUSD_darwinex/h1 vs XAUUSD/H1 + periodo SQX missing). Owner pidió bypass temporal de esas 4 puertas para probar el comparador: `8f0cfa0` + deploy `0.2.53` + wave `m6-shadow-20260818-007` / `example_flow_16` / `sqx-main-v1-830a9c9d-4118-4ed8-a705-51e5fa84868e` COMPLETED 26m12s; 13 Scores `COMPUTED` (p.ej. 17.1875 con net_profit 434 vs -225). M6-NORMAL/M6-TOP/M7 siguen abiertos. Pausa: arquitectura. Decision [[2026-08-18-echo-forge-mt5-fidelity-scope-bypass]].

## 🔗 Referencias

- [[Echo Forge]]
- [[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]
- [[Echo Forge - Etapa 6]]
- [[Echo Forge - Cierre de Etapa 4]]
- [[2026-08-15-mt5-html-parser-fail-open-signed-costs]]
- [[echo-forge]]
- Repo `xKoRx/symphony` @ `34cbe79` + working tree M6-TOP: `specs/FEAT-SQX-MT5-RECONCILIATION-SCORING/M6-TOP-ANALYSIS.md` · `sqx/core/evaluation/canonical_scope.go` · `sqx/core/runtime/cfx_configured_period.go`
