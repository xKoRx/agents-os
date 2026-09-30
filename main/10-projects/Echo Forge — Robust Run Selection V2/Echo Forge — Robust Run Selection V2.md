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
progress: 70
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

## 📊 Estado actual

- **DESIGN_V2_CANDIDATE_READY — ITERATION 2 2026-09-29.** Segunda iteración TOP completada. Plain Pareto queda rechazado como stability authority: non-dominance no expresa magnitud ni materialidad y permite trade-offs como el caso 9/26 vs 8/28 de `Strategy_1.8.669`.
- Candidate V2 recomendado: `R_x = max(normalized MAD_x, normalized |center_x - median_x|)`; cliff Ret/DD permanece hard gate separado; stability authority se implementa conceptualmente mediante dos indifference bands ancladas a mínimos intra-strategy: primero `R_retdd <= min(R_retdd)+epsilon_ret`, luego `R_aux=max(R_sharpe,R_profit) <= min(R_aux)+epsilon_aux`. Quality sólo decide después de ambas equivalencias.
- La topología V2 se mantiene KISS: se agrega center representativeness porque el CELL aplicado físicamente es el centro; no se agregan edge weights, surface fitting ni pesos distintos para corner/direct neighbor sin evidencia.
- Quality se mantiene deliberadamente lexicográfica después de stability equivalence: median Ret/DD → median Sharpe → median Net Profit. No se agrega quality band en V2; el replay adversarial no encontró en los probes realizados un caso donde <1% de ventaja median Ret/DD dentro de los stability bands ocultara >5% de Sharpe o >10% de Net Profit.
- Cliff threshold sigue abierto. Replay Optimizer correctamente separado: 18/34 Strategies son pre-cliff eligible; cliff 25% elimina todos los candidates de 4, 30% de 3, 35% de 0 y 40% de 0. Por tanto 35% sigue candidate, no frozen.
- `epsilon_ret`, `epsilon_aux` y cliff threshold son decisiones semánticas Owner; no deben ajustarse mirando qué winner gusta más.
- Exact durable replay sigue pendiente: Optimizer y WFM pueden diferir por re-evaluación. Esta limitación bloquea freeze/certificación final de la policy, pero no bloquea la revisión adversarial final del diseño.
- Artefacto vigente: [[ROBUST-V2-DESIGN-ITERATION-2]].
- Próximo exacto: **Return to Primary Technical Manager for final adversarial design review. Do not start SPEC or implementation.**

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
> - [r] Revisar [[ROBUST-V2-DESIGN-ITERATION-2]] con Primary Technical Manager / adversarial final review #owner/me #type/supervision #area/echo
> - [ ] Resolver decisiones Owner: epsilon_ret, epsilon_aux y cliff threshold #owner/me #type/supervision #area/echo
> - [ ] Congelar SPEC funcional/técnica sólo después de aceptar el diseño #owner/me #type/dev #area/echo #blocked
> - [ ] Implementar y certificar V2 sólo después del SPEC freeze #owner/me #type/dev #area/echo #blocked

## 📆 Bitácora

- **2026-09-29 — TOP Design Iteration 2.** Plain Pareto rechazado como authority. Se introduce la abstracción faltante de stability indifference: `R_x=max(normalized MAD, normalized center deviation)`; Ret/DD band primero, auxiliary worst-dimension band después, quality sólo entre candidates stability-equivalent. Center topology se incorpora sin devolver performance authority al center. Se preserva cliff como hard gate separado y se rechaza corner/direct weighting por YAGNI. Gate: `DESIGN_V2_CANDIDATE_READY`; próximo paso Primary Technical Manager final adversarial review; no SPEC/product code.

- **2026-09-29 — Manager review.** Primer candidate parcialmente aceptado. Se mantienen arquitectura, separación stability/quality, cliff Ret/DD local, fail-closed y prohibición de center-first/weight optimization. Pareto como authority queda abierto: replay independiente mostró layer-1 suficientemente amplia y trade-offs concretos donde una mejora marginal de median Ret/DD domina una diferencia material de stability. Se corrige además que 18/34 Strategies ya era el máximo con 3×3 completamente passed antes del cliff 35%. Gate: `DESIGN_ITERATION_REQUIRED`; no SPEC/product code.
- **2026-09-29** — Diseño one-shot ejecutado sobre source de `xKoRx/symphony` y corpus wave2a. Se rechazó como autoridad de ranking tanto el center metric V1 como la scalarización estricta por robustness: el candidato usa cliff Ret/DD + normalized MAD + capas de estabilidad no-dominadas + calidad de meseta. Se detectó discrepancia de evidencia Optimizer-vs-WFM que obliga a un replay durable exacto antes de implementación/certificación. Estado: `DESIGN_CANDIDATE_READY_FOR_MANAGER_REVIEW`.

## 🧭 Decisiones

- Preservar la separación `evaluate_wfm` → aggregate/rank y `select_robust_run` → consume `rank == 1`.
- Mantener selección estrictamente intra-strategy.
- Tratar stability y performance level como conceptos separados.
- No usar weights search ni profit histórico para elegir la policy.

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
