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
progress: 50
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

- **DESIGN_CANDIDATE_READY_FOR_MANAGER_REVIEW — 2026-09-29.** Reconstrucción V1 verificada en `xKoRx/symphony`: `dispersion_cov` usa Sharpe CoV + Net Profit CoV, pero el durable ranking ordena primero por `ranking_metric(center)` y sólo después usa `robustness_score` como tie-break; wave2a usa `sharpe_ratio`.
- El candidato V2 propone separar tail-risk Ret/DD, dispersión robusta y nivel de performance: cliff Ret/DD contra la mediana local; normalized MAD por métrica; capas de estabilidad no-dominadas; calidad de meseta por medianas Ret/DD → Sharpe → Net Profit; tie-break técnico determinista.
- El umbral exacto del cliff sigue siendo decisión del Owner. Los pesos 40/30/30, 50/25/25 y 60/20/20 quedan como sensibilidad de un score diagnóstico, no como autoridad de ranking.
- Replay wave2a de diseño completado sobre el export disponible. Existe un gap de evidencia: los valores del Optimizer pueden diferir levemente de la re-evaluación WFM durable (ejemplo documentado 1.33 vs 1.35 de Sharpe para la misma CELL 7/32), por lo que la certificación final de la policy debe replayear `cells.tsv`/MetricSets WFM exactos.
- Artefacto principal: [[ROBUST-V2-DESIGN-CANDIDATE]].
- Próximo exacto: Owner-mediated return to Primary Technical Manager for design iteration. Do not start implementation.

## 🧱 Entrega de desarrollo

_No aplica todavía — esta fase es exclusivamente diseño pre-implementación. Repo objetivo futuro: `xKoRx/symphony`; branch/base y SPECs se congelarán sólo después de la aceptación del diseño._

## 🧩 Subproyectos

- Ninguno.

## ✅ Tareas

> - [x] Reconstruir V1 desde source y verificar el ranking efectivo de wave2a #owner/me #type/research #area/echo
> - [x] Analizar el corpus wave2a y buscar contraejemplos a las políticas candidatas #owner/me #type/research #area/echo
> - [x] Diseñar contrato matemático candidato V2 sin product code #owner/me #type/research #area/echo
> - [r] Revisar [[ROBUST-V2-DESIGN-CANDIDATE]] con Primary Technical Manager #owner/me #type/supervision #area/echo
> - [ ] Resolver decisiones Owner: cliff threshold y aceptación de la semántica de ranking por capas no-dominadas #owner/me #type/supervision #area/echo
> - [ ] Congelar SPEC funcional/técnica sólo después de aceptar el diseño #owner/me #type/dev #area/echo #blocked
> - [ ] Implementar y certificar V2 sólo después del SPEC freeze #owner/me #type/dev #area/echo #blocked

## 📆 Bitácora

- **2026-09-29** — Diseño one-shot ejecutado sobre source de `xKoRx/symphony` y corpus wave2a. Se rechazó como autoridad de ranking tanto el center metric V1 como la scalarización estricta por robustness: el candidato usa cliff Ret/DD + normalized MAD + capas de estabilidad no-dominadas + calidad de meseta. Se detectó discrepancia de evidencia Optimizer-vs-WFM que obliga a un replay durable exacto antes de implementación/certificación. Estado: `DESIGN_CANDIDATE_READY_FOR_MANAGER_REVIEW`.

## 🧭 Decisiones

- Preservar la separación `evaluate_wfm` → aggregate/rank y `select_robust_run` → consume `rank == 1`.
- Mantener selección estrictamente intra-strategy.
- Tratar stability y performance level como conceptos separados.
- No usar weights search ni profit histórico para elegir la policy.

## 🔗 Docs / Links

- [[Echo Forge — Operación Real V2]]
- [[ROBUST-V2-DESIGN-CANDIDATE]]
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
