# ROBUST-V2 — LOCAL REAL-DATA VALIDATION (V1 vs V2)

Status: `LOCAL_VALIDATION_PASS` · Date: 2026-09-30 · Ejecución local en Daedalus (workspace, sin tocar flota ni product code).

## Dataset

- Cohorte: **wave2a** de Echo Forge (opción A del mandato) — 34 Strategies NDX L H1 SQX v1, resultados reales del Optimizer (recovery C5.2, flota Zeus/Kronos, 2026-09-29).
- Input: `10-projects/Echo Forge — Operación Real V2/artifacts/c52-wave2a-20260929/cells.tsv` — 1.836 CELLs = 34 × 54, grid `runs {5,6,7,8,9,10} × OOS {20,22,24,26,28,30,32,34,36}`, con `stability.passed` + 9 métricas OOS por celda. SHA256 verificado contra el manifest del bundle (`3e0dac89…`, coincide byte a byte con la copia original en `~/aranea/work/forge-recovery-c52-20260928/artifacts/`).
- Hallazgo de lineage (importante, no bloqueante): la copia de `cells.tsv` en Agents-OS **no está vacía** — el payload con el hash `3e0dac…` declarado por `SHA256SUMS.txt` existe y es íntegro. El finding histórico "cells.tsv zero bytes" corresponde a otra copia; la evidencia durable del corpus wave2a está disponible, lo que además desbloquea a futuro la tarea deferred de durable replay. En contra: los `aggregates.tsv`/`picks.tsv` del mismo bundle corresponden a **otra materialización** (discrepancia Optimizer-vs-WFM ya registrada el 2026-09-29): los valores/centros de los picks históricos no se reproducen desde `cells.tsv` (p.ej. 8.11.487 sharpe 1,41 durable vs 1,11 en cells.tsv). Por eso esta validación **no reclama identidad histórica byte a byte**; compara V1 vs V2 sobre un input único, real y autoconsistente.

## Execution method

Worktree limpio de `origin/feature/robust-selection-v2-shot1` @ `bc50bbba9a50b7079ed81ff96d80b9f1f780c368` (HEAD verificado, `git status` clean; sdk sibling symlink). Probe temporal no-commiteado (patrón Shot-2, eliminado al cierre) dentro de `sqx/adapters/wfm/binding` que ejecuta el **código de producto real**: `evaluateNeighborhoods` (el evaluador durable determinista que despacha V1/V2 en producción) para veredictos/picks, y `wfm.SelectRobustV2` con parámetros permisivos (`MaxFloat64`) para telemetría por-vecindario con las fórmulas frozen exactas (sin reimplementación). Los sets de sobrevivientes del probe se asertaron contra los picks reales de V2 en las 34 estrategias (PASS). Sin Stores/PG/Temporal: la frontera durable (persistencia) no participa; el cálculo es el mismo que el del worker.

## Effective V1 config

`DefaultEvaluatorConfig()` — los defaults durables frozen: `wfm_3x3_v1` + `dispersion_cov`, `ranking_metric=sharpe_ratio`, `top_n=3`, `min_consistency=0.90`, `weight_center=0.4`, `weight_neighbors=0.6`, caps CoV sin tope, reglas default (outliers ret_dd < 1.0 / k=3, variabilidad global 0.50, pico aislado 2σ, OOS trades/netprofit CoV 0.30), sin metric filters. Justificación: el spec de wave2a (`flow-recovery-c52-wave2a.json`) declara `evaluate_wfm` **sin `wfm_params`** → `EvaluatorConfigFromWFMParams` cae a los defaults. Digest del config efectivo: `sha256:57cdb0c5…`.

## V2 trial config (TRIAL, NO producción)

`robust_run_selection_v2` con `cliff_threshold=0.35`, `epsilon_ret=0.01`, `epsilon_aux=0.01` — valores de prueba del mandato, no defaults ni freeze. Digest: `sha256:24daf87d…`.

## Aggregate result

| Métrica | V1 | V2 |
|---|---|---|
| Estrategias totales | 34 | 34 |
| Con picks (veredicto consumible) | 18 (12 WARN + 6 FAIL-SEVERE-with-picks) | 18 (18 WARN) |
| Sin picks | 16 (`NO_ACCEPTABLE_NEIGHBORHOOD`) | 16 (`NO_ACCEPTABLE_NEIGHBORHOOD`) — **mismo set exacto** |
| Veredictos PASS / WARN / FAIL | 0 / 12 / 22 | 0 / 18 / 16 |
| FAIL por `SEVERE_WARNING` | 6 | **0** |
| rank1 igual / cambiado (sobre picks) | — | 5 iguales / 13 cambiados |
| V1 seleccionada → V2 rechazada | — | **0** |
| V1 rechazada → V2 seleccionada (nivel pick) | — | 0; **a nivel veredicto: 6** (las 6 FAIL-SEVERE de V1 pasan a WARN en V2) |

Lectura clave: V2 no rechaza nada que V1 aceptara. El delta viene de (a) la calidad del pick (13/18 cambiados) y (b) la interacción con el warning de pico aislado: V1 elegía el pico, se auto-gateaba con SEVERE (2,0–3,1σ) y quedaba FAIL; V2 elige la meseta y el warning no se dispara → la estrategia vuelve al funnel.

## Clasificación de rechazos V2 (STEP 9)

952 vecindarios interiores 3×3 (34 × 28): 738 `NEIGHBORHOOD_NOT_PASSED` (no existe 3×3 completo con las 9 celdas passed+elegibles — idéntico criterio de elegibilidad que V1), 26 `CLIFF_REJECTED` (12,15% de los 214 vecindarios analíticamente válidos — exactamente el 26/214 del adversarial review del diseño), 154 `PRIMARY_BAND`, 2 `AUX_BAND`, 32 `SURVIVOR`. Estrategias rechazadas por V2: 0 por cliff/bandas a nivel Strategy — las 16 rechazadas lo son por no tener ni un vecindario completo elegible (mismo set que V1). **V2 no es demasiado agresivo en esta cohorte: el cliff gate only corta candidatos concretos (26), nunca una Strategy completa que V1 hubiera aceptado.**

## Cambios V1→V2 (STEP 8/11, 13 casos)

Todos los 13 cambios se movieron a **menor `R_retdd` (13/13)** y 12/13 a menor `R_aux`. Sacrificio de median Ret/DD: 7 estrategias (mediana −1,24; peor caso −2,18 en 7.51.646, que además estaba en cliff), 5 mejoraron, 1 empató. Tres V1-centers estaban directamente en un acantilado Ret/DD y V2 los rechaza por cliff: 1.8.669 (0,392), 6.24.638 (0,364), 7.51.646 (0,403).

## 5 casos más interesantes (STEP 12)

1. **Strategy_7.51.646** — cambio fuerte + cliff. V1 8/34 (median Ret/DD 17,50; R_retdd 0,459; cliff 0,403). V2 8/32 (median Ret/DD 15,32; R_retdd 0,142; cliff 0,158). Los vecinos con mayor mediana (6/32 y 6/34 con 23,67) fueron rechazados por cliff (0,377/0,430 > 0,35): el gate protege exactamente lo que fue diseñado a proteger. Sacrificio −12,5% de mediana por ~3× estabilidad y sin acantilado.
2. **Strategy_8.11.487** — pico vs meseta + veredicto. V1 6/26 era un pico aislado 3,07σ → SEVERE → FAIL (excluida del funnel). V2 8/22: meseta casi perfecta (R_retdd 0,0062, cliff 0,037), WARN. 4 sobrevivientes empatados en calidad; el tie-break frozen (R_retdd ASC tras 3 empates de mediana) eligió (8,22) de forma determinista.
3. **Strategy_3.31.576** — V2 sin sacrificio. V1 8/34 (mediana 9,22; R_retdd 0,440) vs V2 7/22 (mediana 11,26; R_retdd 0,048): +2,04 de mediana Y 9× menos dispersión. El centro que V1 había elegido era lo peor de ambos mundos.
4. **Strategy_2.76.686** — nested indifference. V1 6/28 (mediana 22,02; R_retdd 0,112; R_aux 0,046) vs V2 6/30 (mediana 21,91; R_retdd 0,032; R_aux 0,286). El centro V2 tiene 6× peor R_aux pero gana porque la banda primaria (Ret/DD-indiference) es la autoridad y dentro de ella mandó la mediana Ret/DD; el set primario era aux-uniforme-alto. Semántica frozen operando tal cual.
5. **Strategy_6.41.479** — indiferencia pura. V1 8/22 (mediana 21,534; R_retdd 0,100; FAIL-SEVERE 2,51σ) vs V2 9/22 (misma mediana 21,534; R_retdd 0,0195; WARN). Mediana idéntica, V2 se mueve una fila en runs por estabilidad — el caso libro de "plateau vs peak sin costo de calidad".

## Sanity findings (STEP 13)

- **`LOCAL_VALIDATION_FOUND_IMPLEMENTATION_DEFECT`: NO.** Sets de sobrevivientes == picks reales en 34/34 (asertado en runtime); rank-1 único; tie-breaks deterministas observados (8.11.487); cliff deja pasar exactamente lo que el freeze define; dependencia del orden de input descartada (colección row-major determinista + sort estable con tie-break completo por runs/OOS; Shot 2 además probó 500 permutaciones).
- No-material: 2.25.400 gana con cliff 0,3497 — a 0,0003 del umbral 0,35. No es defecto, pero es el caso canónico de sensibilidad al parámetro para cuando el Owner decida mover `cliff_threshold`.
- `WARNING_DATA_MISSING` (34) en ambos lados: preexistente (campo stability score ausente en esta data), idéntico V1/V2, no afecta.
- Discrepancia de materialización del bundle (aggregates/picks vs cells.tsv) descrita en Dataset: preexistente y registrada; esta validación no la hereda porque compara V1 vs V2 sobre el mismo input.

## Conclusión

Con datos reales wave2a y el mismo input exacto para ambos algoritmos, V2 selecciona las mismas 16 no-elegibles, acepta a las mismas 18 estrategias (además desbloquea las 6 que V1 se auto-gateaba por pico aislado) y en 13/18 cambia el run seleccionado hacia mesetas con R_retdd estrictamente menor, sacrificando mediana Ret/DD en 7 casos (mediana −1,24, peor −2,18) y mejorándola en 5. El cliff 0,35 corta 26/214 vecindarios (12,15%, coincide con el adversarial de diseño) y bloquea 3 picks de V1 que estaban sentados sobre acantilados Ret/DD. Sin defectos de implementación; sin rechazos excesivos; comportamiento consistente con el freeze. Los números 0.35/0.01/0.01 se observaron tal cual, sin tuning.

## Artefactos

- `ROBUST-V2-LOCAL-VALIDATION.csv` — una fila por Strategy (este directorio).
- `artifacts/local-validation-20260930/` — outputs crudos del probe: `strategies.tsv`, `v1_candidates.tsv`, `v2_candidates.tsv` (952 filas con stage), `details.json`, `five_cases.json`, `v2_stage_counts.json`.
- Corpus de entrada: `c52-wave2a-20260929/cells.tsv` (SHA verificado) en [[Echo Forge — Operación Real V2]].
