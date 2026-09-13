---
type: index
schema_version: 1
status: active
icon: 🗂️
slug: echo-index
area: "[[Echo]]"
project:
created: "2026-09-13"
updated: "2026-09-13"
reviewed: "2026-09-13"
aliases:
  - "echo index"
  - "índice de Echo"
cssclasses:
  - wide
tags:
  - kind/index
  - area/echo
---

# 📂 Echo — Índice

> [!info] Subdominio de [[30-resources/applications/00-index|Applications]]
> Páginas canónicas de Echo (plataforma) y Echo Forge (fábrica), sus contratos vigentes y la frontera compartida. Reglas: [[30-resources/00-RESOURCE-WIKI|Resource Wiki]] · Bitácora compartida: `../log.md`.

## 📊 De un vistazo

- **Páginas:** 14 (2 apps + frontera + changelog + 6 contratos + 4 provenance) + 5 históricas en retención
- **Última ingesta:** 2026-09-13 (consolidación KBC → subdominio `applications/echo/`)
- **Estado:** active

## Aplicaciones

| Página | Una línea | Baseline citado |
|---|---|---|
| [[echo-core]] | Plataforma de ejecución y Trade Journal de Echo (Bridge/Core Flink StateFun/Gateway); receptor de la frontera Forge. | echo `f7ddea18` |
| [[echo-forge]] | Fábrica cuantitativa sobre SQX (Temporal): campaña multi-wave → WFM → ranking → FinalistPromotion V2 + Apply; handoff NO cableado. | symphony `9fad768c` |

## Frontera

| Página | Una línea |
|---|---|
| [[echo-forge-integration-boundary]] | Frontera Forge→Echo: contrato frozen vigente, estado implementado por lado (con baseline), gaps G1–G7 y lo que la wiki no afirma. |

## Bitácora

| Página | Una línea |
|---|---|
| [[echo-core-changelog]] | Bitácora de cambios de [[echo-core]]. |

## Contratos vigentes (source-of-record, frozen — no re-derivar)

| Contrato | Una línea |
|---|---|
| [[Echo SDK — Canonical Forge Integration and Analytics Contract V1]] | Contrato compartido SDK/analytics/handoff; autoridad congelada del lado Echo. |
| [[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]] | Ingestión, identidad runtime y Live Authority; autoridad del SPEC E-04. |
| [[Echo Forge — F-01 Canonical Generation Concurrency Contract]] | CanonicalStrategyID puro + `ExecutionIntentKey` como discriminator de publication. |
| [[Echo Forge — F-02 Finalist Model V2 Contract]] | Membership estructural ≠ Top N; Promotion 2.0.0. |
| [[Echo Forge — F-03 SQX Long-Running Contract]] | elapsed ≠ failure; ceiling `MaxInt64ns−1s`; cancel de process-tree. |
| [[Echo Forge — F-04 Magic Allocation, Version Seal and Handoff Contract]] | Magic V1, seal write-once, HandoffManifestV1; C4/C5 verificados 2026-09-12. |

## Provenance (notas source)

| Nota | Cubre |
|---|---|
| [[Echo — Fuentes de implementación 2026-09-12 (f7ddea18)]] | Baseline Echo de campaña (fase B). |
| [[Echo Forge — Fuentes de implementación 2026-09-12 (9fad768c)]] | Baseline Symphony de campaña (fase C). |
| [[Echo — Fuentes de arquitectura y producto 2026-09-06]] | Provenance histórica Echo master 04c16bd. |
| [[Echo Forge — Fuentes de arquitectura y producto 2026-09-06]] | Provenance histórica Symphony a10c26c. |

## Histórico (retención; autoridad vigente en las páginas de arriba tras verificación)

[[Echo + Echo Forge — Arquitectura de producto, gaps y roadmap de cierre 2026]] · [[Echo + Echo Forge — Independent Reality Check and Time-to-Value Plan]] · [[Echo + Echo Forge — Evidencia de revisión independiente 2026-09-06]] · [[Echo + Echo Forge — Architecture Durability and Contract Review — Fable 5.1]] · [[Echo SDK — Canonical Contract Final Freeze Review — Fable 5.1]]

## 🔗 Links

- [[30-resources/00-RESOURCE-WIKI|Reglas de la Resource Wiki]]
- `../log.md` — bitácora cronológica compartida del dominio `applications/`
