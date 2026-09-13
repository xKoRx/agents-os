---
type: change_log
schema_version: 1
scope: session
created: "2026-09-13"
updated: "2026-09-13"
area: "[[Echo]]"
project: "[[Echo — Knowledge Base Consolidation]]"
application: "[[xKoRx/echo]]"
entities:
  - "[[Echo — Knowledge Base Consolidation]]"
  - "[[echo-core]]"
  - "[[echo-forge]]"
  - "[[echo-forge-integration-boundary]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[Echo SDK — Canonical Forge Integration and Analytics Contract V1]]"
  - "[[Echo — Forge Ingestion, Runtime Identity and Live Authority Contract V1]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: team
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-13-kbc-echo-subdomain-publication

%% Routing: area/project/application/entities/related usan links canónicos. %%

## Cambio

- **Tipo:** moved + updated + created
- **Archivo(s):**
  - `30-resources/applications/echo/00-index.md` (creado)
  - 16 renames `30-resources/applications/*.md` → `30-resources/applications/echo/*.md` (identidad preservada, git mv)
  - `30-resources/applications/echo/echo-core.md` (reescritura con baseline `xKoRx/echo@f7ddea18`)
  - `30-resources/applications/echo/echo-forge.md` (reescritura con baseline `xKoRx/symphony@9fad768c`; elimina claim falso de entrega a Echo)
  - `30-resources/applications/echo/echo-forge-integration-boundary.md` (creada)
  - 2 notas source nuevas por baseline (`f7ddea18` / `9fad768c`)
  - `30-resources/applications/00-index.md` (puntero único al subdominio; 13 filas Echo fuera; contadores 14 apps)
  - `30-resources/00-RESOURCE-WIKI.md` (declara `applications/echo/` subdominio activo)
  - `30-resources/applications/log.md` (entrada de ingest)

## Motivo

Campaña [[Echo — Knowledge Base Consolidation]] (fases A–H): topología aprobada, cartografías Echo/Forge/frontera verificadas adversarialmente (PASS con unknowns), manifest de publicación reconciliado contra HEAD.

## Decisiones

- Supersede de las 5 piezas históricas DIFERIDO hasta verificar cobertura de sus 32 deudas/hitos (protocolo en artifact `10-publication-plan.md`).
- MERGE de `GUIA_WORKER_TEMPORAL_MT5.md` y archive moves de `sqx/` diferidos (verificación pendiente).
- `last_verified` mantiene las fechas de verificación real (2026-09-12/13 contra los SHAs citados), no la fecha de publicación.
- Graphify: reindex pendiente (CLI no disponible en la sesión).

## Impacto en routing

- Índice raíz de `applications/` ya no lista echo-core/echo-forge como filas de catálogo: apunta al sub-índice. Los wikilinks por nombre (`[[echo-core]]`, `[[echo-forge]]`) resuelven igual tras el MOVE.
