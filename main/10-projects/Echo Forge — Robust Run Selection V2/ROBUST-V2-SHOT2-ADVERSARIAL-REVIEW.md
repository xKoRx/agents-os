# ECHO FORGE — ROBUST RUN SELECTION V2
# SHOT 2 — FRESH ADVERSARIAL IMPLEMENTATION REVIEW

Status: `SHOT_2_PASS`

Date: 2026-09-30

Reviewer: fresh-context adversarial implementation reviewer (no participación en Shot 1 ni Shot 1R; no Primary Manager; no Owner).

---

## 1. Executive verdict

```text
SHOT_2_PASS
0 BLOCKER
0 MAJOR
2 MINOR (documentados, no obligan corrección en Shot 3)
```

La implementación completa (Shot 1 `b696b3a`+`a149a34` + Shot 1R `bc50bbb`) implementa el design freeze [[ROBUST-V2-DESIGN-FREEZE]] sin defectos materiales de implementation: la matemática congelada (median/MAD/D/C/R/cliff/bandas/quality order) es exacta bajo ataque con valores extremos, signos mixtos, zero-scale y overflow; V1 queda byte y semánticamente intacto; los dos paths (legacy in-memory y durable binding) comparten la misma función core `SelectRobustV2` y producen el mismo ganador para el mismo input lógico (probado por paridad); el `RobustnessScore=0` de V2 no tiene consecuencia funcional material en ningún consumidor real; `select_robust_run` sigue consumiendo el `rank==1` único. La implementación está lista para Shot 3 (certificación/cleanup final).

No se modificó product code: el working tree quedó limpio en `bc50bbb` tras la revisión (los probes adversariales fueron temporales y eliminados).

## 2. Reviewed SHA range

```text
repo:    xKoRx/symphony
branch:  feature/robust-selection-v2-shot1
base:    ca07f72 (merge-base confirmado = ca07f72275ad349487ad21a0b2a51eb9ce3acd9a)
head:    bc50bbb (bc50bbba9a50b7079ed81ff96d80b9f1f780c368)
commits: b696b3a (core) + a149a34 (binding) + bc50bbb (Shot 1R)
worktree: limpio al inicio y al cierre; clon ~/aranea/work/forge-precision-shot1-20260926/symphony
diff:    ca07f72..HEAD — 7 archivos, +1217/−42 (robust_v2.go, evaluator.go, config.go, contract.go, evaluate.go, 2 tests)
```

Confirmado: repo correcto, branch correcta, HEAD real, working tree limpio, merge-base = baseline esperada.

## 3. Design freeze conformance matrix

| Cláusula del freeze | Veredicto | Evidencia |
|---|---|---|
| V2 = nuevo algoritmo en el mecanismo de config existente, sin segunda arquitectura | PASS | Dispatch único en `EvaluateNeighborhood` (`sqx/core/wfm/evaluator.go:63`) + `EvaluatorConfigFromWFMParams` (`sqx/adapters/wfm/binding/config.go:106`); sin registry/policy layer; el switch V1 `scoreNeighborhood` quedó intocado |
| V1 immutable (ids, `dispersion_cov`, defaults, ranking, digest tipado, `select_robust_run`) | PASS | Diff no toca `scoreNeighborhood`/`rankPicks`/`DefaultEvaluatorConfig` para V1; probe de dispatch V1 + suites verdes; digest V1 sin los 3 campos nuevos (test existente + `omitempty` de punteros) |
| Selección estrictamente intra-strategy sobre 3×3 | PASS | Mismos loops interiores que V1 en ambos paths; sin ranking cross-strategy |
| Math: `M_x`, `scale_x`, `MAD_x`, `D_x`, `C_x`, `R_x=max(D,C)`, `R_aux=max(R_sharpe,R_profit)` | PASS | `robust_v2.go:212-306` implementación literal del freeze; probes de fórmula exacta |
| Cliff: `0 / +Inf / max(0,(L-tail)/scale)` | PASS | `robustRetDDCliff` (`robust_v2.go:274`); probes con tail positivo/cero/negativo y signos mixtos |
| Derived fail-closed: cualquier derivado no-finito → ineligible antes de mínimos | PASS | `deriveRobustV2Metrics` filtra antes de cliff/bandas; probe: ret_best=+Inf es imposible; overflow → rechazado |
| `cliff <= threshold` sólo filtra, no rankea | PASS | Gate `>` en `SelectRobustV2`; probe demuestra que cliff no es clave de orden |
| Primary band: `ret_best=min(R_retdd)`, `R_retdd <= ret_best+epsilon_ret` | PASS | `robust_v2.go:161-172`; probes de frontera exacta, eps=0, múltiples mínimos |
| Aux band DESPUÉS del primary: `aux_best=min(R_aux among primary)` | PASS | `robust_v2.go:174-185`; probe demuestra que un candidato fuera del primary con mejor R_aux no expande nada |
| Nested indifference: exact ret_best eliminable por aux band | PASS | Probe obligatorio del freeze: B sobrevive y A (exact ret_best) es eliminado |
| Quality order: mediana Ret/DD DESC → Sharpe DESC → Profit DESC → R_retdd ASC → R_aux ASC → runs ASC → OOS ASC | PASS | `sort.SliceStable` (`robust_v2.go:187-208`); probe de las 7 transiciones |
| Ninguna métrica del centro es autoridad de ranking | PASS | `ranking_metric_value` = mediana del vecindario, no del centro (probe: pick con mediana 2.1 vs celda 2.15) |
| Config V2: sólo 3 parámetros, finitos >= 0, missing/inválido = config error, sin defaults silenciosos | PASS | `ValidateRobustV2Params`/`ParseRobustV2Params`/`requiredRobustV2Param`/`robustV2Params`; matriz NaN/±Inf/negativo/missing; path de config directa también falla cerrado |
| Out of scope (Pareto, weights, quality bands, durable evidence recovery, etc.) | PASS | El diff no contiene nada de la lista |
| `select_robust_run` consume `rank==1` único | PASS | `durable_select_robust_run.go:126-137` intocado: rank-1 duplicado → error, sin rank-1 → error |

## 4. V1 compatibility review

- Serialización/digest: los tres campos V2 son `*float64` con `json:"...,omitempty"` y sólo se poblan bajo `ScoringAlgorithm == robust_run_selection_v2`; para toda config V1 el JSON es byte-idéntico (test existente `TestEvaluatorConfigDigest_V1JSONUnchangedByV2Fields` + verificación estática de que V1 nunca asigna los punteros, ni siquiera con garbage V2 en `wfm_params`). El realign del struct en el diff es sólo gofmt.
- Dispatch V1: `wfm_3x3_v1`→alias, `""`→error existente, ids V1 mapean al mismo path; `scoreNeighborhood` y `rankPicks` intocados; probe demuestra V1 con score > 0 y V2 con score 0 sobre la misma matriz.
- Warnings/rules/stats del path legacy (`EvaluateRules`, stats, veredictos) y del durable (`collectWarnings`, `countExtremes`, `statsFromCells`) no dependen del score ni cambian con V2 salvo por la población de candidatos, que es semántica propia de V2.
- `calculateWFMScore`, `CompareEvaluations`, `CalculateSelectionScore`: ver sección 9.
- `ScoringAlgorithmVersionV1` permanece `"v1"` para V1; `ScoringAlgorithmVersionV2` sólo bajo V2.

## 5. Core vs durable parity

Ambos paths construyen `RobustV2Candidate` con la misma función `wfm.RobustV2CandidateFromCells` y seleccionan con la misma `wfm.SelectRobustV2` — no hay segunda implementación de la matemática. La elegibilidad de entrada es equivalente: legacy exige `neighborhoodPassed` (9 celdas Passed) + 3 métricas finitas en 9 celdas; durable exige `eligible()` = `observedTrue()` + 3 métricas OBSERVED finitas en 9 celdas (`evaluate.go:177-193`). Probe de paridad: fixture 4×4 con cliff, empates de mediana y desempates — mismo número de supervivientes y misma secuencia `(rank, runs, oos)` en `evaluateNeighborhoods` y `wfm.EvaluateNeighborhood`. Diferencia preexistente de warnings (legacy activity usa `EvaluateRules` sobre matriz; durable usa su propio motor `collectWarnings`) es asimetría brownfield V1, no delta de Shot 1.

## 6. Mathematical audit

Probes adversariales (temporales, ejecutados y eliminados; working tree limpio):

- Median/MAD: pares/impares, negativos, signos mixtos, duplicados, ceros, escala 1e-300, valores ~1e308 — todos exactos; `median` copia antes de ordenar (`append([]float64(nil), ...)`) → sin mutación ni aliasing (probe de DeepEqual antes/después y slices compartidos entre candidatos).
- Zero-scale: superficie plana-cero → `R=0`, `cliff=0` finitos; centro desviado con scale 0 → `+Inf` → ineligible; `cliff=+Inf` por scale 0 con `L≠tail` → ineligible incluso con threshold 1e9; `ret_best=+Inf` imposible (todo superviviente tiene R finito).
- Overflow con finitos extremos: `center−median` overflow (±1.7e308) → rechazado; `L−tail` overflow → `cliff=+Inf` → rechazado; ningún superviviente con NaN (un NaN pasaría silenciosamente el gate `>` — verificado que la derivación filtra NaN antes).
- Cliff: fórmula exacta para tail positivo (0.6), cero (1.0), negativo (1.6), signos mixtos (2.0), flat y all-zero; frontera exacta: `cliff == threshold` sobrevive, `nextafter` debajo elimina; cliff sólo filtra (no rankea, no desempata).
- Primary band: `epsilon_ret=0` mantiene sólo mínimos exactos; candidato a `1.000001` fuera con eps 0 y dentro con eps 0.001; múltiples mínimos exactos ambos sobreviven. Sin fuzzy epsilon: V2 usa sólo `<=` con el epsilon configurado (el `epsilon=1e-6` del paquete es exclusivo del ranking V1 durable).
- Aux band: `aux_best` calculado después del primary — caso construido donde el mejor R_aux global está FUERA del primary y no altera el resultado; no-monotonicidad end-to-end confirmada como diseñada.
- Nested indifference (caso obligatorio del freeze): A exact ret_best con peor R_aux es eliminado; B in-band con mejor R_aux gana. MAJOR si estuviera protegido — no lo está.
- Quality order: 7 transiciones construidas adversarialmente (Ret/DD, Sharpe, Profit, R_retdd, R_aux, runs, OOS) — cada clave decide sólo cuando la anterior empata.
- Determinism: 500 permutaciones seeded del set de 8 candidatos (con duplicados de calidad) → secuencia de salida idéntica en todas; sin randomness no seeded como evidencia.
- Rank/salida: exactamente un `rank==1`; contigüidad 1..N; sin duplicados; sin rank 0 (`ParseAggregateDecisionView` rechaza `rank < 1`).
- Empty set: 0 candidatos → 0 supervivientes sin error; legacy → `FAIL/no_valid_neighborhoods`; durable → `FAIL/NO_ACCEPTABLE_NEIGHBORHOOD`; sin panic ni rank-1 fantasma.

## 7. Config/digest audit

- Dispatch de punta a punta: `wfm_params.algorithm = robust_run_selection_v2` → legacy `EvaluateNeighborhood` y durable `EvaluatorConfigFromWFMParams` (versión `v2`). Unknown algorithm → `ErrUnsupportedAlgorithm` existente en ambos; params V2 presentes bajo algoritmo V1 → ignorados (V1 unaffected); V2 sin params → config error en ambos paths y también en configs tipadas directas (`robustV2Params` → error de `evaluateNeighborhoods`).
- Digest: JSON del DTO tipado incluye `cliff_threshold/epsilon_ret/epsilon_aux` sólo para V2 → digests V2 distintos por parámetros (test existente) y digests V1 estables. Scope AGGREGATE y payload llevan `scoring_algorithm`, `scoring_algorithm_version:"v2"` y el digest (test e2e `Contains` + lectura de `BuildAggregateScope`/`buildAggregatePayload`). V2 queda inequívocamente identificado; sin arquitectura nueva.
- Parámetros: matriz completa missing/negative/NaN/±Inf/0/válido → 0 es válido, todo lo demás error; sin silent defaults ni clamps (core y binding por separado).

## 8. Output/durable contract audit

- Ranking antes de TopN en ambos paths: la calidad ordena el universo superviviente completo y el corte TopN es posterior (`rankRobustV2Picks` rebanha la lista ya ordenada; legacy igual). Probe TopN=2 sobre 4 supervivientes → mismos 2 primeros.
- Identidad de pick: cada pick durable conserva `runs`, `oos`, `CellEvaluationRef` y `CellMetricSetRef` del CELL central (`neighbors[4]`); `bindPicks` re-resuelve por `(runs,oos)` contra bindings canónicos (duplicados rechazados en `canonicalizeBindings`) → misma celda. Sin refs de vecinos ni recomputación de identidad.
- `ranking_metric=ret_dd` (identifier válido del catálogo, usado por `eligible`) + `ranking_metric_value` = mediana del vecindario; ningún consumidor recomputa el rank desde el valor (durable select usa rank==1; apply usa `RobustSelectionOutput` + `ValidateSelectedEvidence`, que no valida score ni re-rankea).
- Veredictos existentes conservados: `NO_ACCEPTABLE_NEIGHBORHOOD` (candidatos vacíos), `RULES_FAIL` (filtros duros sobre supervivientes, igual que V1), `SEVERE_WARNING`, `WARN` por data-missing — V2 se integra sin alterar la máquina de veredictos.

## 9. Downstream consumer audit (RobustnessScore=0)

Cadena verificada independientemente (no se aceptó la conclusión de Shot 1R sin auditoría):

- `calculateWFMScore` (`evaluate_wfm.go:452`): devuelve el `RobustnessScore` del rank-1 → `WfmScore=0` persistido en la evaluación legacy. Sin validaciones `score > 0` en el repo (grep negativo).
- `robust.CompareEvaluations` usa `WfmScore` (paso 4/5) pero **no tiene ningún caller productivo** (sólo `selector_test.go`) — código brownfield sin superficie V2.
- `robust.CalculateSelectionScore` → `SelectionScore = 0 − penalizaciones`; único consumidor = `generate_report.go` (reporte YAML, no decisional).
- `SelectRobustRunActivity` elige `eval.Picks[0]` — para V2 legacy eso ES el rank-1 (picks emitidos en orden de rank); no usa score para elegir.
- Path durable: `durable_select_robust_run` selecciona el `rank==1` único (duplicado → error), `ValidateSelectedEvidence` no valida score, `RobustSelectionOutput` lo transporta sin derivar comportamiento; SPEC FEAT-SQX-DURABLE-WFM §11 ya declara el score no-autoridad.

Conclusión: el `0` no genera ninguna consecuencia funcional material en ningún path V2 real. `WfmScore=0` en el path legacy in-memory produce empates deterministas en un comparador sin callers productivos. PASS.

## 10. Determinism

500 permutaciones seeded (rand.NewSource determinista) sobre un set con empates deliberados → salida idéntica; `sort.SliceStable` con comparator completo de 7 claves; orden de colección determinista (row-major sobre ejes ordenados) en ambos paths; desempate final estable por orden de colección (determinista). PASS.

## 11. Tests executed

```text
go build ./...                                                        → OK
go vet ./sqx/core/wfm/... ./sqx/adapters/wfm/binding/...              → limpio
go test -count=1 ./sqx/core/wfm/... ./sqx/adapters/wfm/binding/...    → ok (PASS)
go test -count=1 -run 'WFM|Robust|DurableSelect|DurableApply|EvaluateWfm' ./sqx/activities/worker/ → ok (PASS, 7.4s)
```

Probes temporales (fuera del commit, eliminados después; tree final limpio @ bc50bbb): 14 tests core + 5 tests binding — todos PASS. Cobertura de los probes: fórmulas exactas, zero-scale, overflow, cliff (6 formas + frontera + no-rankeo), bandas (frontera, post-primary minima, nested indifference), 7 transiciones de calidad, 500 permutaciones, validación de params, empty set, dispatch V1/V2, paridad legacy/durable, mediana-vs-centro, cliff-gate e2e durable, TopN post-rank, config sin params fail-closed.

## 12. BLOCKER findings

Ninguno.

## 13. MAJOR findings

Ninguno.

## 14. MINOR findings

- **MIN-01 — Knobs V1 vestigiales en el digest V2 (higiene, no corrección).** `EvaluatorConfigFromWFMParams` sigue leyendo `ranking_metric`, `min_consistency`, `weight_center`, `weight_neighbors`, `max_sharpe_cov`, `max_net_profit_cov` de `wfm_params` también para V2; un config V2 con esos knobs cambia su digest (identidad de config) sin cambiar ningún comportamiento (V2 los ignora: `eligible` fija las 3 métricas, `rankRobustV2Picks` fija `ret_dd`). Es el precedente uniforme del DTO tipado; dos configs V2 que difieren sólo en knobs muertos producen aggregates distintos con el mismo ganador. No rompe correctness ni la identidad semántica del ranking (el rank no es recomputable desde `ranking_metric_value`). Clasificado MINOR/DEFER — decisión de higiene futura del manager; no requiere fix en Shot 3. (Observación ya elevada por Shot 1R; confirmada por este review.)
- **MIN-02 — Interacción preexistente SEVERE-with-picks vs durable select (no introducida por este delta).** En `evaluateNeighborhoods` el resultado `FAIL/SEVERE_WARNING` conserva `Picks` poblados, mientras `DurableSelectRobustRunActivity` rechaza no-retryable cualquier aggregate FAIL con picks. El código es idéntico para V1 y V2 y no fue tocado por `ca07f72..HEAD` (comprobado en el diff), así que no es regresión de Shot 1 ni drift de paridad; se registra como observación para el manager (posible cleanup posterior fuera del alcance V2).

## 15. Explicit non-findings

- `RobustnessScore=0`: sin consecuencia material (sección 9); ningún consumer decide por él; `select_robust_run` usa `rank`; validation no exige `score > 0`; sin empates funcionales downstream.
- Los campos V2 `omitempty` no alteran serialización/digest V1 (sección 4).
- `median` no muta slices compartidos (sección 6).
- Elegibilidad durable exige `observedTrue` + 3 métricas OBSERVED finitas — Missing/Invalid jamás se coerced a 0 (`observedOrNaN` → NaN → excluido por finiteness).
- Neighborhood: sólo centros interiores; vecindario incompleto → ineligible (sin relleno, sin inventar celdas, sin wrap-around, sin reutilizar vecinos); duplicados rechazados en durable (preexistente) y last-wins en legacy lookup (preexistente V1).
- `AlgoRobustRunSelectionV2` no colisiona con el alias `wfm_3x3_v1`; unknown algorithm con params V2 sigue fallando cerrado.
- TopN: bands/ranking nunca se calculan sobre un TopN preliminar (sección 8).
- Refs de pick = CELL central (sección 8).
- Sin scope creep: el diff no agrega abstractions, exported API muerta ni edits V1 accidentales; los exports nuevos son los mínimos que el binding necesita cross-package.

## 16. Shot 3 required remediation

Ninguna obligatoria (0 BLOCKER, 0 MAJOR). Shot 3 procede como certificación/cleanup final según plan del Primary Manager. Ítems opcionales sujetos a decisión del manager, no mandato de este review: higiene de knobs vestigiales en digest V2 (MIN-01) y observación preexistente SEVERE-with-picks (MIN-02).

## 17. Final gate

```text
STATUS: SHOT_2_PASS

REVIEWED:
repo: xKoRx/symphony
branch: feature/robust-selection-v2-shot1
base: ca07f72
head: bc50bbb (b696b3a + a149a34 + bc50bbb)
worktree: limpio (sin cambios de product code)

DESIGN_FREEZE_CONFORMANCE: PASS
V1_COMPATIBILITY: PASS
CORE_DURABLE_PARITY: PASS
MATH_CORRECTNESS: PASS
CONFIG_VALIDATION: PASS
CONFIG_DIGEST: PASS
ROBUSTNESS_SCORE_ZERO: PASS (impacto: WfmScore=0 sólo superficie reportable; sin decisión funcional)
RANKING_METRIC_FIELDS: PASS
DOWNSTREAM_RANK1: PASS
DETERMINISM: PASS

TESTS:
commands: go build ./...; go vet (wfm+binding); go test -count=1 ./sqx/core/wfm/... ./sqx/adapters/wfm/binding/...; go test -count=1 -run 'WFM|Robust|DurableSelect|DurableApply|EvaluateWfm' ./sqx/activities/worker/; + 19 probes temporales (eliminados)
results: todo PASS; tree limpio @ bc50bbb

BLOCKERS: ninguno
MAJORS: ninguno
MINORS: MIN-01 (knobs vestigiales en digest V2 — DEFER), MIN-02 (SEVERE-with-picks preexistente — observación)
NON_FINDINGS: ver sección 15

SHOT_3_REQUIRED:
- ninguno obligatorio

ARTIFACT:
path: main/10-projects/Echo Forge — Robust Run Selection V2/ROBUST-V2-SHOT2-ADVERSARIAL-REVIEW.md
commit: a2e3fd01 (vault, sync 13:57; blob 4e9be2f84f05dd36b2a6dc14534c347afd945727)
blob: 4e9be2f84f05dd36b2a6dc14534c347afd945727

PROJECT:
commit: a2e3fd01 (blob f11c9fe5b96731eaab12ee0c9653eb6d69758302; agent-run 8363b642)

NEXT EXACT:
Return to Primary Technical Manager.
Do not modify product code.
Do not start Shot 3.
```
