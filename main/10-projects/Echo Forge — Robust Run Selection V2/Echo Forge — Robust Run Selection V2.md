---
type: project
schema_version: 1
owner: me
root: false
status: review
priority: P1
area: "[[Echo]]"
parent: "[[Echo Forge — Operación Real V2]]"
sprint:
start: 2026-09-29
due:
progress: 90
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
updated: "2026-09-29"
---

# Echo Forge — Robust Run Selection V2

## 🎯 Objetivo

- Diseñar y revisar una política V2 intra-strategy para seleccionar el robust run desde neighborhoods 3×3, priorizando mesetas paramétricas robustas sin volver a un ranking encubierto por pico central.
- Separar explícitamente estabilidad paramétrica de nivel de performance y mantener `select_robust_run` como consumidor de `rank == 1`, salvo defecto material demostrado.
- No implementar product code hasta que el Primary Technical Manager y el Owner revisen y congelen el contrato.
- **Compatibilidad frozen por Owner:** V2 será un **algoritmo/policy nuevo seleccionable desde la configuración inicial**. No se modificará retroactivamente la semántica del algoritmo V1 existente. Con el tiempo podrán coexistir múltiples algoritmos seleccionables según necesidad.

## 📊 Estado actual

- **DURABLE_REPLAY_BLOCKED_EVIDENCE — 2026-09-30.** El exact durable replay se detuvo en el evidence gate: el `cells.tsv` versionado sigue en 0 bytes aunque `SHA256SUMS.txt` declara `3e0dac89805df320d416820cf57f067d8bddf766fb74b151bc64c88cb81a76d1`; la historia Git demuestra que el bundle entró en `8385041a88c17ed0aaba577115bac0c45b429012` sin payload CELL recuperable, y la búsqueda en Library no encontró una copia exacta independiente. `aggregates.tsv`, `picks.tsv` y el audit preservan outputs V1, pero no reemplazan la autoridad de las 1.836 CELL/MetricSet. V1 replay = NOT_RUN; V2 replay/sensitivity = NOT_RUN. Próximo exacto: recuperar read-only las 1.836 CELL + 34 AGGREGATE del FlowRun `80647dc2-848a-4150-842e-cc6947eed87c` desde su lineage durable original y recién entonces reanudar V1→V2. Sin valores Owner congelados, sin SPEC ni product code. Artefacto: [[ROBUST-V2-DURABLE-REPLAY]].

- **DESIGN_ALGORITHM_CLOSED_PENDING_DURABLE_REPLAY — PRIMARY MANAGER 2026-09-29.** El Primary Manager acepta el focused verification: no quedan defectos conceptuales materiales en la policy V2. El diseño algorítmico queda cerrado; sólo faltan evidence replay y decisiones Owner de materialidad. Focused final verification PASS: el derived-finiteness gate cierra el único fail-open material sin cambiar la policy finita de Iteration 2. Todo candidate con `R_retdd`, `R_sharpe`, `R_profit`, `R_aux` o `cliff` no finito queda analytical-ineligible antes de cualquier mínimo; empty set => analytical FAIL. `cliff_threshold`, `epsilon_ret` y `epsilon_aux` se validan sólo en V2 como finitos y >= 0; config inválido es contract/config failure. Casos all-nonfinite, mixed finite/nonfinite, auxiliary nonfinite, cliff nonfinite, near-zero finite, zero-scale/zero-variation, raw invalid, config invalid, finite-corpus non-regression y V1 compatibility quedaron PASS.
- Candidate V2 recomendado: `R_x = max(normalized MAD_x, normalized |center_x - median_x|)`; cliff Ret/DD permanece hard gate separado; stability authority se implementa conceptualmente mediante dos indifference bands ancladas a mínimos intra-strategy: primero `R_retdd <= min(R_retdd)+epsilon_ret`, luego `R_aux=max(R_sharpe,R_profit) <= min(R_aux)+epsilon_aux`. Quality sólo decide después de ambas equivalencias.
- La topología V2 se mantiene KISS: se agrega center representativeness porque el CELL aplicado físicamente es el centro; no se agregan edge weights, surface fitting ni pesos distintos para corner/direct neighbor sin evidencia.
- Quality se mantiene deliberadamente lexicográfica después de stability equivalence: median Ret/DD → median Sharpe → median Net Profit. No se agrega quality band en V2; el replay adversarial no encontró en los probes realizados un caso donde <1% de ventaja median Ret/DD dentro de los stability bands ocultara >5% de Sharpe o >10% de Net Profit.
- Cliff threshold sigue abierto. Replay Optimizer correctamente separado: 18/34 Strategies son pre-cliff eligible; cliff 25% elimina todos los candidates de 4, 30% de 3, 35% de 0 y 40% de 0. Por tanto 35% sigue candidate, no frozen.
- `epsilon_ret`, `epsilon_aux` y cliff threshold son decisiones semánticas Owner; no deben ajustarse mirando qué winner gusta más.
- Exact durable replay sigue pendiente: Optimizer y WFM pueden diferir por re-evaluación. Antes de SPEC freeze se exige reproducir V1 desde CELL/MetricSet durable exacto y aplicar la V2 corregida offline sobre la misma autoridad.
- **Evidence integrity finding del Manager:** `artifacts/c52-wave2a-20260929/cells.tsv` actualmente versionado en Agents-OS se lee con **0 bytes**, mientras `SHA256SUMS.txt` declara para `cells.tsv` el SHA256 `3e0dac89805df320d416820cf57f067d8bddf766fb74b151bc64c88cb81a76d1`. Por tanto ese archivo Git no puede usarse como bundle durable exacto. El replay debe recuperar/materializar la autoridad CELL/MetricSet original desde la evidencia durable real (DB/MinIO/export original), verificar lineage/hash/count y no rerunear SQX sólo para reconstruir V1.
- Artefacto vigente: [[ROBUST-V2-FINITENESS-VERIFICATION]].
- Manager pre-review: Iteration 2 resuelve el defecto principal de Pareto y queda aceptada como candidato para adversarial final, no frozen. El adversarial debe atacar especialmente (1) la semántica de que el auxiliary band pueda excluir al exact Ret/DD-stability winner una vez dentro de `epsilon_ret`; (2) sensibilidad de cliff a nivel candidate/winner, no sólo Strategy survival; (3) parámetros `epsilon_ret/epsilon_aux` como materiality semantics y no tuning; y (4) compatibilidad: V2 debe ser un algoritmo nuevo seleccionable por config sin cambiar V1.
- Próximo exacto: **exact durable replay + Owner decision pack**: recuperar la autoridad durable CELL/MetricSet faltante, reproducir V1 exactamente, aplicar V2 corregida offline y producir breakpoints/sensitivity para `cliff_threshold`, `epsilon_ret` y `epsilon_aux`. El worker NO congela números; vuelve al Primary Manager/Owner. No SPEC ni implementación todavía.

## 🧱 Entrega de desarrollo

_No aplica todavía — esta fase es exclusivamente diseño pre-implementación. Repo objetivo futuro: `xKoRx/symphony`; branch/base y SPECs se congelarán sólo después de la aceptación del diseño._

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
> - [ ] Ejecutar exact durable replay V1→V2 sobre autoridad CELL/MetricSet verificada #owner/me #type/research #area/echo — **BLOCKED_EVIDENCE**: la autoridad exacta CELL/MetricSet de wave2a no está recuperable desde Git/Library; requiere lectura RO del durable store original.
> - [ ] Resolver decisiones Owner: epsilon_ret, epsilon_aux, cliff threshold y ratificación quality order #owner/me #type/supervision #area/echo
> - [ ] Congelar SPEC funcional/técnica sólo después de aceptar el diseño #owner/me #type/dev #area/echo #blocked
> - [ ] Implementar y certificar V2 sólo después del SPEC freeze #owner/me #type/dev #area/echo #blocked

## 📆 Bitácora

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
- V2 es **aditiva**, no una mutación de V1: debe exponerse como algoritmo/policy nuevo seleccionable por configuración; V1 permanece disponible y semánticamente estable.
- Derived V2 non-finite values are rejection sentinels, never comparable stability values: any non-finite `R_retdd/R_sharpe/R_profit/R_aux/cliff` => analytical-ineligible before minima; no remaining candidates => analytical FAIL.
- V2 semantic parameters `cliff_threshold`, `epsilon_ret`, `epsilon_aux` must be finite and >=0. Invalid configured values are contract/config errors, not analytical Strategy outcomes.

## 🔗 Docs / Links

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
