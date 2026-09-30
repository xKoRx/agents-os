---
type: project
schema_version: 1
owner: me
root: false
status: active
priority: P1
area: "[[Echo]]"
parent: "[[Echo Forge — Operación Real V2]]"
sprint:
start: 2026-09-29
due:
progress: 100
repo: "xKoRx/symphony"
jira:
prs:
aliases:
  - Echo Forge Robust Run Selection V2
tags:
  - kind/project
  - area/echo
  - echo-forge
  - robust-run-selection
created: "2026-09-29"
updated: "2026-09-30"
---

# Echo Forge — Robust Run Selection V2

## 🎯 Objetivo

- Diseñar y revisar una política V2 intra-strategy para seleccionar el robust run desde neighborhoods 3×3, priorizando mesetas paramétricas robustas sin volver a un ranking encubierto por pico central.
- Separar explícitamente estabilidad paramétrica de nivel de performance y mantener `select_robust_run` como consumidor de `rank == 1`, salvo defecto material demostrado.
- No implementar product code hasta que el Primary Technical Manager y el Owner revisen y congelen el contrato.
- **Compatibilidad frozen por Owner:** V2 será un **algoritmo/policy nuevo seleccionable desde la configuración inicial**. No se modificará retroactivamente la semántica del algoritmo V1 existente. Con el tiempo podrán coexistir múltiples algoritmos seleccionables según necesidad.

## 📊 Estado actual

- **LOCAL_VALIDATION_PASS (2026-09-30) — V1 vs V2 ejecutados sobre los mismos datos reales wave2a; evidencia a favor de la aceptación del manager.** Fresh Local Validation Lead ejecutó el evaluador durable real (`evaluateNeighborhoods` + `wfm.SelectRobustV2`, código de producto sin cambios, worktree limpio @ `bc50bbb`) sobre el corpus wave2a SHA-verificado (34 × 54 CELLs; `cells.tsv` del bundle c52 con hash `3e0dac…` == manifest — el payload "zero bytes" histórico existe en [[Echo Forge — Operación Real V2]], copia íntegra en `forge-recovery-c52-20260928/artifacts/`), con V1 = defaults durables frozen (spec wave2a sin `wfm_params`) y V2 trial `0.35/0.01/0.01` sin tuning. Resultado: mismo set exacto de 16 rechazadas (V2 no rechaza nada extra; cliff corta 26/214 vecindarios = 12,15%, idéntico al adversarial de diseño); 18/18 estrategias siguen seleccionables y las 6 FAIL-SEVERE de V1 (pico aislado auto-gateado 2,0–3,1σ) pasan a WARN; 13/18 rank1 cambiados, 13/13 hacia menor `R_retdd` (12/13 menor `R_aux`), sacrificio de mediana Ret/DD en 7 (mediana −1,24, peor −2,18) y mejora en 5; 5 changed rank1 estaban sobre acantilados/picos que el cliff gate y la estabilidad rechazan. Sin defecto de implementación. Limitación declarada: los aggregates/picks históricos del bundle son otra materialización (discrepancia Optimizer-vs-WFM ya registrada); no se reclama replay histórico. Detalle: [[ROBUST-V2-LOCAL-VALIDATION]] (+CSV por Strategy y outputs crudos en `artifacts/local-validation-20260930/`).

- **IMPLEMENTATION_COMPLETE — SHOT_3_PASS (2026-09-30): certificación final de delivery cerrada, retorna al Primary Technical Manager para aceptación final/integración.** Fresh Release/Verification Lead certificó `ca07f72..bc50bbb` (branch `feature/robust-selection-v2-shot1`, sin push): sin drift desde Shot 2 (diff idéntico 7 archivos +1217/−42, merge-base/base/HEAD/tree verificados), freeze conformance PASS (sin evaluation_policy/registry/Pareto/weights/surface fitting/quality bands; `select_robust_run` y switch V1 intocados), V1 regression PASS (`go test -count=1` wfm+binding y worker slice WFM|Robust|DurableSelect|DurableApply|EvaluateWfm verdes), V2 regression PASS (29 tests existentes cubren la lista completa: plateau/MAD/cliff/bandas/nested indifference/quality order/tie-break/shuffle/zero-scale/params inválidos/config/paridad legacy-durable), `robustness_score=0` + rank autoridad + config `robust_run_selection_v2` con 3 params required finite ≥0 re-verificados en código, working tree limpio. `go build ./...` falla sólo en `pebbe/zmq4` (internal/tasks→sdk/pkg/mt5): **preexistente ambiental** (falta `libzmq.pc` en Daedalus), probado idéntico en el baseline `ca07f72` vía worktree temporal; deuda ajena no tocada. 0 BLOCKER / 0 MAJOR nuevos. Deferred sin reabrir: MIN-01 (knobs V1 vestigiales en digest V2), MIN-02 (SEVERE-with-picks preexistente) y historical durable replay evidence. Product code sin cambios en Shot 3. READY_TO_PUSH=YES (sin autorización de push → no empujado). Detalle: [[ROBUST-V2-SHOT3-FINAL-CERTIFICATION]].
- **SHOT_2_PASS (2026-09-30) — fresh adversarial implementation review completo, retorna al Primary Technical Manager.** Rango `ca07f72..bc50bbb` (Shot 1 `b696b3a`+`a149a34` + Shot 1R `bc50bbb`) revisado contra [[ROBUST-V2-DESIGN-FREEZE]] con contexto fresco: 0 BLOCKER, 0 MAJOR, 2 MINOR (MIN-01 knobs V1 vestigiales que entran al digest V2 sin efecto conductual — DEFER/higiene; MIN-02 interacción preexistente SEVERE-with-picks vs durable select, no introducida por el delta). Matemática exacta bajo ataque (zero-scale, overflow, cliff, bandas, nested indifference, quality order, 500 permutaciones), V1 byte/semánticamente intacto, paridad legacy/durable probada con fixture equivalente, `RobustnessScore=0` sin consecuencia funcional material (cadena de consumers auditada: `CompareEvaluations` sin callers productivos, `SelectionScore` sólo reporting, durable select por rank==1). Suites wfm/binding/worker verdes; probes temporales eliminados; tree limpio sin cambios de product code. Detalle: [[ROBUST-V2-SHOT2-ADVERSARIAL-REVIEW]]. Listo para Shot 3 (certificación/cleanup final); no iniciarlo desde aquí.
- **SHOT_1R_PASS (2026-09-30) — remediation del finding del Primary Manager aplicada, retorna a review del manager.** El scalar inventado `RobustnessScore = 1/(1+R_retdd+R_aux)` fue eliminado (`RobustV2Score` ya no existe): V2 no define score escalar y los picks llevan el zero value en la posición contractual del campo (float64 schema-required en `NeighborhoodPick`/`AggregatePick`/`RobustSelectionOutput`; ningún consumer durable deriva comportamiento de él — selección durable por `rank==1` único, SPEC durable v1 §11 ya declara el score no-autoridad). `ranking_metric=ret_dd` + `ranking_metric_value=median Ret/DD` (mediana del vecindario 3×3) quedan como primary quality key explícita y testeada: empate de mediana Ret/DD cae a median Sharpe DESC, el rank no es recomputable desde `ranking_metric_value` solo. Sweep `ca07f72..HEAD`: cero otro drift contra [[ROBUST-V2-DESIGN-FREEZE]]; matemática V2 y V1 intactas; arquitectura sin cambios. Branch `feature/robust-selection-v2-shot1` commit `bc50bbb` (base `ca07f72`, sobre `b696b3a`+`a149a34`, sin push); regresión V1 PASS.
- **SHOT_1_IMPLEMENTED_LOCAL (2026-09-30).** Implementación en `xKoRx/symphony` branch `feature/robust-selection-v2-shot1` (commits `b696b3a` core + `a149a34` binding, baseline master `ca07f72`, sin push).
- **READY_FOR_SHOT_1 — KISS DESIGN FREEZE 2026-09-30.** Diseño algorítmico cerrado y autoridad canónica: [[ROBUST-V2-DESIGN-FREEZE]].
- V2 es **otro algoritmo seleccionable mediante el mecanismo de configuración WFM existente**. No crear `evaluation_policy`, registry ni una segunda arquitectura de policies.
- V1 permanece semánticamente intacto: mismos identificadores/defaults/config digest/ranking y mismo `select_robust_run` consumidor de `rank == 1`.
- V2 congelado conceptualmente: normalized MAD + center deviation → `R_x=max(D_x,C_x)`; Ret/DD cliff; derived fail-closed; Ret/DD indifference band; `R_aux=max(R_sharpe,R_profit)`; auxiliary band; quality por median Ret/DD → Sharpe → Net Profit; tie-break determinista.
- Config V2 mínima: nuevo algorithm id + `cliff_threshold` + `epsilon_ret` + `epsilon_aux`. Parámetros explícitos, finitos y >=0. Sin defaults silenciosos.
- El problema histórico de `cells.tsv`/durable replay queda **deferred a certificación/evidencia**. No bloquea Shot 1.
- Los artefactos [[ROBUST-V2-FINAL-ADVERSARIAL-REVIEW]], [[ROBUST-V2-FINITENESS-VERIFICATION]] y [[ROBUST-V2-DURABLE-REPLAY]] son historia/evidencia. Cualquier recomendación allí de `evaluation_policy` o durable replay como gate de implementación queda **SUPERSEDED** por [[ROBUST-V2-DESIGN-FREEZE]].
- Próximo exacto: **Shot 1 implementación mínima en `xKoRx/symphony`**. No rediseñar.

## 🧱 Entrega de desarrollo

_Diseño cerrado. Shot 1 autorizado: implementación mínima del nuevo algoritmo sobre el extension point de config/evaluator existente. Sin arquitectura nueva._

## 🧩 Subproyectos

- Ninguno.

## ✅ Tareas

> - [x] Reconstruir V1 desde source y verificar el ranking efectivo de wave2a #owner/me #type/research #area/echo
> - [x] Analizar el corpus wave2a y buscar contraejemplos a las políticas candidatas #owner/me #type/research #area/echo
> - [x] Diseñar contrato matemático candidato V2 sin product code #owner/me #type/research #area/echo
> - [x] Revisar [[ROBUST-V2-DESIGN-CANDIDATE]] con Primary Technical Manager #owner/me #type/supervision #area/echo
> - [x] Ejecutar segunda iteración TOP focalizada en autoridad de stability, Pareto trade-offs y MAD 3×3 #owner/me #type/research #area/echo
> - [x] Revisar [[ROBUST-V2-DESIGN-ITERATION-2]] con Primary Technical Manager #owner/me #type/supervision #area/echo
> - [x] Ejecutar fresh TOP final adversarial review del candidate V2 #owner/me #type/research #area/echo
> - [x] Integrar corrección bounded: non-finite derived stability => analytical ineligible #owner/me #type/supervision #area/echo
> - [x] Verificar focalizadamente derived-finiteness + validity de parámetros semánticos #owner/me #type/research #area/echo
> - [ ] Recuperar durable replay histórico sólo como verificación/certificación posterior si vuelve a estar disponible la evidencia original #owner/me #type/research #area/echo
> - [x] Ejecutar Shot 1 — nuevo algoritmo V2 + config mínima + tests + regresión V1 #owner/me #type/dev #area/echo
> - [x] Ejecutar Shot 1R — eliminar scalar RobustnessScore inventado + verificar semántica honesta de ranking_metric/value + sweep drift #owner/me #type/dev #area/echo
> - [x] Ejecutar Shot 2 — fresh adversarial implementation review de `ca07f72..bc50bbb` contra el freeze #owner/me #type/research #area/echo
> - [x] Ejecutar Shot 3 — certificación final + close de delivery (drift, freeze, regresiones V1/V2, build/static, clean tree, contratos score/config/output) #owner/me #type/research #area/echo
> - [x] Ejecutar validación local real-data V1 vs V2 sobre la cohorte wave2a (trial 0.35/0.01/0.01, sin tuning ni product code) #owner/me #type/research #area/echo
> - [ ] Aceptación final e integración por Primary Technical Manager (branch `feature/robust-selection-v2-shot1` local @ `bc50bbb`, sin push; READY_TO_PUSH) #owner/me #type/supervision #area/echo

## 📆 Bitácora

- **2026-09-30 — Shot 3 certificación final: `SHOT_3_PASS`.** Fresh Senior Go Release/Verification Lead certificó el estado final de `xKoRx/symphony` branch `feature/robust-selection-v2-shot1` @ `bc50bbb` (base `ca07f72`, merge-base verificado, tree limpio inicio/cierre, worktree de prueba al baseline eliminado). CHECK 1 sin drift: diff `ca07f72..bc50bbb` idéntico al rango revisado en Shot 2 (7 archivos +1217/−42), sin commits/archivos nuevos. CHECK 2 freeze PASS: único hook de dispatch en `EvaluateNeighborhood` + caso binding; sin evaluation_policy/registry/Pareto/weights/surface fitting/quality bands/spatial; `select_robust_run` y switch V1 intocados; knobs `Weight*` del hunk confirmados como realineación gofmt de líneas V1 idénticas. CHECK 3 V1 regression PASS y CHECK 4 V2 regression PASS: `go test -count=1 ./sqx/core/wfm/... ./sqx/adapters/wfm/binding/...` (0.022s/0.662s) + worker slice `WFM|Robust|DurableSelect|DurableApply|EvaluateWfm` (7.2s) verdes; 29 tests V2 existentes inventariados cubriendo la lista mandada completa, sin batería nueva. CHECK 5 build/static PASS con preexistente distinguido: vet limpio y build del delta OK, `go build ./...` exit 1 sólo por `pebbe/zmq4` (internal/tasks→sdk/pkg/mt5, falta `libzmq.pc` en Daedalus con `libzmq.so.5` presente) — probado idéntico en baseline `ca07f72` con worktree temporal (exit 1), deuda ajena no arreglada. CHECKs 6/7/8 re-verificados en código: `RobustnessScore=0` con `Rank` autoridad y durable select por `rank==1` (archivo intocado), algorithm id `robust_run_selection_v2` con `cliff_threshold`/`epsilon_ret`/`epsilon_aux` required finite ≥0 sin defaults en ambos paths, output contract (rank 1 único contiguo, TopN post-ranking, refs CELL central, `ranking_metric=ret_dd` + mediana vecindario). CHECK 9 clean delivery PASS: sin probes/debug/junk, sin stashes, READY_TO_PUSH=YES sin push (sin autorización). 0 BLOCKER / 0 MAJOR nuevos; MIN-01, MIN-02 y historical durable replay evidence quedan deferred sin reabrir. Product code sin cambios (`FILES_CHANGED_IN_SHOT_3: NONE`). Artefacto: [[ROBUST-V2-SHOT3-FINAL-CERTIFICATION]]. Siguiente exacto: Primary Technical Manager para aceptación final/integración.

- **2026-09-30 — Shot 2 fresh adversarial implementation review: `SHOT_2_PASS`.** Review con contexto fresco del rango `ca07f72..bc50bbb` en `xKoRx/symphony` branch `feature/robust-selection-v2-shot1` (repo/branch/HEAD/merge-base/worktree confirmados; tree limpio antes y después). 25 ataques del mandato cubiertos con lectura de source + 19 probes temporales (fuera del commit, eliminados al cierre): matemática exacta (median/MAD sin mutación ni aliasing, zero-scale `0/+Inf`, overflow con finitos extremos rechazado, cliff con 6 formas + frontera exacta + no-rankeo, primary band con eps=0/frontera/múltiples mínimos, `aux_best` demostrado post-primary, nested indifference obligatorio PASS, 7 transiciones de quality order, 500 permutaciones seeded deterministas, rank-1 único y contiguo), V1 byte/semánticamente intacto (punteros `omitempty` + digest test + probe de dispatch), paridad legacy/durable demostrada con fixture 4×4 equivalente (misma secuencia rank/runs/oos; ambos paths comparten `SelectRobustV2`), `ranking_metric_value` = mediana del vecindario (no del centro), TopN posterior al ranking, refs de pick = CELL central, empty set → `NO_ACCEPTABLE_NEIGHBORHOOD` sin panic ni rank-1 fantasma. `RobustnessScore=0` auditado en frío: `CompareEvaluations` sin callers productivos, `SelectionScore` sólo alimenta reportes, durable select/apply deciden por `rank==1` + `ValidateSelectedEvidence` (sin score). Config validation y digest: matriz missing/negativo/NaN/±Inv inválida → config error en core, binding y config directa; digest V1 estable y V2 inequívoco (scope/payload con `scoring_algorithm_version:"v2"`). 0 BLOCKER / 0 MAJOR / 2 MINOR documentados sin fix obligatorio (MIN-01 knobs V1 vestigiales en digest V2 — DEFER; MIN-02 SEVERE-with-picks vs durable select — preexistente, no del delta). Tests: build+vet limpios, `go test -count=1 ./sqx/core/wfm/... ./sqx/adapters/wfm/binding/...` ok, worker slice `WFM|Robust|DurableSelect|DurableApply|EvaluateWfm` ok. Sin cambios de product code. Artefacto: [[ROBUST-V2-SHOT2-ADVERSARIAL-REVIEW]]. Siguiente exacto: Primary Technical Manager (re-review Shot 1/1R con Shot 2 PASS); Shot 3 no se inicia desde este shot.

- **2026-09-30 — Shot 1R remediation PASS (local).** Finding del manager resuelto delete-first: `RobustV2Score = 1/(1+R_retdd+R_aux)` eliminado de `sqx/core/wfm/robust_v2.go`; picks V2 (core legacy `evaluateRobustRunSelectionV2` y binding durable `rankRobustV2Picks`) dejan `RobustnessScore` en zero value con documentación in situ. Auditoría de consumers probó que el campo es obligatorio por schema (float64 sin `omitempty` en los 3 contratos frozen) pero no-obligatorio semánticamente: `durable_select_robust_run` selecciona el `rank==1` único, `ValidateSelectedEvidence` no valida score, y SPEC FEAT-SQX-DURABLE-WFM §11 declara que el handoff no debe asumir `Picks[0]` = max score; único efecto del zero value = `WfmScore=0` en el path legacy in-memory (ties deterministas en `CompareEvaluations`, sin autoridad inventada). `ranking_metric=ret_dd`/`ranking_metric_value=median Ret/DD` explícitos como primary quality key en `rankRobustV2Picks` + test nuevo `TestEvaluateAndComplete_RobustV2TiedMedianRetDDRankBeyondValue` (mediana Ret/DD empatada → orden por median Sharpe DESC; 4 picks con el mismo `ranking_metric_value` y ranks distintos). Aserciones de score actualizadas a `0.0` en los tests de plateau (binding) y legacy path (core). Sweep del diff: sin `evaluation_policy`/registry/Pareto/weights/surface fitting/quality bands, `select_robust_run` y semántica V1 intactos, sin defaults inventados; observación elevada al manager: knobs V1 vestigiales del DTO (`ranking_metric`, `weight_center`, `min_consistency`…) se registran en scope/digest bajo V2 sin consumirse (precedente uniforme del DTO tipado; rechazo fail-closed decidido como fuera de alcance mínima). Tests: wfm core 16 V2 + binding 11 V2 PASS; worker slice `WFM|Robust|DurableSelect|DurableApply|EvaluateWfm` PASS; contrato `RobustSelectionOutput` en domain PASS; `go build`/`go vet` limpios. Commit `bc50bbb` sobre la branch (sin squash de `b696b3a`/`a149a34`), sin push.

- **2026-09-30 — Shot 1 implementado (local).** V2 = algoritmo `robust_run_selection_v2` sobre el extension point existente (`wfm_params.algorithm` → `scoring_algorithm`). Core: `sqx/core/wfm/robust_v2.go` (math pura median/MAD/D/C/R/cliff, `SelectRobustV2` finiteness→cliff→bandas→quality order, validación fail-closed de `cliff_threshold`/`epsilon_ret`/`epsilon_aux`) + dispatch en `EvaluateNeighborhood`; el switch V1 `scoreNeighborhood` quedó intocado. Binding durable: `EvaluatorConfigFromWFMParams` acepta el nuevo id con versión `v2`; parámetros V2 tipados como punteros `omitempty` (JSON/digest de toda config V1 byte-idéntico, probado en test); `durableCell.eligible` exige las 3 métricas OBSERVED finitas en las 9 celdas; `evaluateNeighborhoods` despacha V2 conservando verdict/reasons/stats/warnings existentes (NO_ACCEPTABLE_NEIGHBORHOOD/RULES_FAIL/SEVERE); picks V2 registran `ranking_metric=ret_dd` + `ranking_metric_value=median Ret/DD`; `select_robust_run` intacto (rank==1). Tests: 14 core (plateau, center peak, cliff single tail, broad dispersion, zero/zero, zero-scale→+Inf ineligible, mixed non-finite, boundary epsilon_ret/epsilon_aux, nested-indifference, quality order, tie-break, shuffle, params inválidos, legacy path) + 10 binding (config válida/inválida, digest V1, PASS plateau con scope `scoring_algorithm_version=v2`, cliff gate e2e, +Inf e2e NO_ACCEPTABLE_NEIGHBORHOOD, quality order e2e, RULES_FAIL, config directa sin params, shuffle determinista). `V1_REGRESSION = PASS`: `go test ./sqx/core/wfm/... ./sqx/adapters/wfm/binding/...` y WFM-slice de `./sqx/activities/worker/` verdes sin modificar expectations. Branch `feature/robust-selection-v2-shot1` (base `ca07f72`, commits `b696b3a`+`a149a34`), sin push; decisión push = owner/manager.

- **2026-09-30 — KISS design freeze / contamination cleanup.** Se corrige contaminación documental posterior al diseño: `evaluation_policy + version` y durable replay como gate de implementación quedan explícitamente superseded. Autoridad única de implementación: [[ROBUST-V2-DESIGN-FREEZE]]. V2 = nuevo algoritmo sobre config WFM existente; V1 intacto; Shot 1 READY.

- **2026-09-30 — Durable replay evidence gate.** Veredicto `DURABLE_REPLAY_BLOCKED_EVIDENCE`. Se verificó el bundle wave2a, su historia Git y Library: `cells.tsv` fue incorporado vacío en `8385041a...` mientras el manifest conserva el SHA256 no-vacío `3e0dac...`; no existe payload histórico recuperable en Git ni copia exacta encontrada en Library. Los 34 aggregates y 46 picks quedan sólo como outputs de referencia. No se ejecutaron V1/V2 replay, shuffle, cliff/epsilon sensitivity ni Owner decision pack. Reporte: [[ROBUST-V2-DURABLE-REPLAY]]; commit de creación `65e73a1b6b15ad6943dfb9f31e4be7e0c218f1f3`. Próximo: acceso RO al lineage durable exacto del FlowRun y materialización verificable de las 1.836 CELL/MetricSet.

- **2026-09-29 — Primary Manager design close.** Focused amendment verification aceptado; no quedan defectos conceptuales materiales. Gate interno: `DESIGN_ALGORITHM_CLOSED_PENDING_DURABLE_REPLAY`. Se detecta inconsistencia de evidencia: `cells.tsv` versionado está vacío aunque `SHA256SUMS.txt` declara un payload con hash no-vacío. El siguiente worker debe recuperar la autoridad durable original read-only, verificar lineage/hash/count y ejecutar replay exacto V1→V2; prohibido rerunear SQX sólo para reconstrucción. Worker entrega Owner decision pack, no congela números.

- **2026-09-29 — Focused final finiteness verification.** Gate PASS: `DESIGN_READY_FOR_DURABLE_REPLAY_AND_OWNER_FREEZE`. El amendment es fail-closed y behaviorally transparent sobre corpus finito; no introduce cutoff near-zero, no rechaza scale=0/variation=0 y no toca V1. Config inválido V2 queda separado de Strategy analytical FAIL. Artefacto: [[ROBUST-V2-FINITENESS-VERIFICATION]]. Próximo gate exacto: durable replay + Owner freeze; sin SPEC/product code.

- **2026-09-29 — Primary Manager amendment.** Se acepta e integra la única corrección material del adversarial: derived non-finite => analytical-ineligible antes de mínimos; empty set => analytical FAIL. Se añade validación contractual KISS para los tres parámetros configurables de V2: deben ser finitos y >=0; config inválido es error técnico/config, no resultado analítico. No se reabre `R_x`, nested indifference, cliff semantics, auxiliary minimax, quality order ni config identity. Gate: `DESIGN_AMENDMENT_READY_FOR_FOCUSED_VERIFY`.

- **2026-09-29 — Final adversarial design review.** Veredicto `DESIGN_ITERATION_REQUIRED`. Iteration 2 sobrevive las superficies centrales: Ret/DD indifference puede ceder autoridad a auxiliary stability dentro de la banda; la no-monotonicidad end-to-end en `epsilon_ret` es real y semánticamente intencional; `R_x=max(D,C)`, `R_aux=max(R_sharpe,R_profit)` y quality lexicográfica se mantienen. Cliff 35% sí es material a nivel candidate: rechaza 26/214 neighborhoods (12.15%), afecta 6 Strategies y cambia el primary stability anchor en 2. Defecto material nuevo: los sentinels `+Inf` pueden sobrevivir las bandas si todo el set es no-finito. Corrección mínima obligatoria: derived-finiteness gate antes de `ret_best/aux_best`. Config identity recomendado: selector explícito `evaluation_policy + version`, preservando exacto el path/digest V1 legacy. Artefacto: [[ROBUST-V2-FINAL-ADVERSARIAL-REVIEW]].


- **2026-09-29 — Primary Manager pre-adversarial review.** Iteration 2 aceptada como candidato fuerte: stability indifference resuelve el trade-off oculto de Pareto. No se congela aún. Se agregan cuatro ataques obligatorios para el review final: prioridad Ret/DD vs auxiliary band, cliff sensitivity a nivel candidate/winner, semántica de epsilons y backward compatibility. Owner aclaró además un contrato durable: V2 será un algoritmo nuevo seleccionable por config; V1 conserva su comportamiento y podrán coexistir algoritmos futuros.

- **2026-09-29 — TOP Design Iteration 2.** Plain Pareto rechazado como authority. Se introduce la abstracción faltante de stability indifference: `R_x=max(normalized MAD, normalized center deviation)`; Ret/DD band primero, auxiliary worst-dimension band después, quality sólo entre candidates stability-equivalent. Center topology se incorpora sin devolver performance authority al center. Se preserva cliff como hard gate separado y se rechaza corner/direct weighting por YAGNI. Gate: `DESIGN_V2_CANDIDATE_READY`; próximo paso Primary Technical Manager final adversarial review; no SPEC/product code.

- **2026-09-29 — Manager review.** Primer candidate parcialmente aceptado. Se mantienen arquitectura, separación stability/quality, cliff Ret/DD local, fail-closed y prohibición de center-first/weight optimization. Pareto como authority queda abierto: replay independiente mostró layer-1 suficientemente amplia y trade-offs concretos donde una mejora marginal de median Ret/DD domina una diferencia material de stability. Se corrige además que 18/34 Strategies ya era el máximo con 3×3 completamente passed antes del cliff 35%. Gate: `DESIGN_ITERATION_REQUIRED`; no SPEC/product code.
- **2026-09-29** — Diseño one-shot ejecutado sobre source de `xKoRx/symphony` y corpus wave2a. Se rechazó como autoridad de ranking tanto el center metric V1 como la scalarización estricta por robustness: el candidato usa cliff Ret/DD + normalized MAD + capas de estabilidad no-dominadas + calidad de meseta. Se detectó discrepancia de evidencia Optimizer-vs-WFM que obliga a un replay durable exacto antes de implementación/certificación. Estado: `DESIGN_CANDIDATE_READY_FOR_MANAGER_REVIEW`.

## 🧭 Decisiones

- Preservar la separación `evaluate_wfm` → aggregate/rank y `select_robust_run` → consume `rank == 1`.
- Mantener selección estrictamente intra-strategy.
- Tratar stability y performance level como conceptos separados.
- No usar weights search ni profit histórico para elegir la policy.
- V2 es **aditiva**, no una mutación de V1: debe exponerse como **nuevo algoritmo en el mecanismo de configuración WFM existente**; V1 permanece disponible y semánticamente estable. No introducir `evaluation_policy` ni otra capa de dispatch.
- Derived V2 non-finite values are rejection sentinels, never comparable stability values: any non-finite `R_retdd/R_sharpe/R_profit/R_aux/cliff` => analytical-ineligible before minima; no remaining candidates => analytical FAIL.
- V2 semantic parameters `cliff_threshold`, `epsilon_ret`, `epsilon_aux` must be finite and >=0. Invalid configured values are contract/config errors, not analytical Strategy outcomes.

## 🔗 Docs / Links

- [[ROBUST-V2-DESIGN-FREEZE]] — **autoridad canónica de implementación**

- [[Echo Forge — Operación Real V2]]
- [[ROBUST-V2-DESIGN-CANDIDATE]]
- [[ROBUST-V2-DESIGN-ITERATION-2]]
- `xKoRx/symphony:specs/FEAT-SQX-DURABLE-WFM/SPEC.md`
- `xKoRx/symphony:specs/FEAT-SQX-DURABLE-ROBUST-SELECTION/SPEC.md`

## 💡 Ideas

### Backlog de ideas

- Ninguna fuera del scope actual.

### Motivos / principios

- KISS/YAGNI: una policy interpretable, determinista y replayable; evitar convertir V2 en un optimizer de hiperparámetros.

### Memoria pública / interna

- **Memoria pública:** este proyecto y su artefacto de diseño.
- **Memoria interna:** no requerida para el contrato.
- **Motivo:** el estado que debe retomar el Manager queda explícito en la nota del proyecto.
