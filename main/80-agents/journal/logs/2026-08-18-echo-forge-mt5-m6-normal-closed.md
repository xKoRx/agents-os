---
type: change_log
schema_version: 1
scope: session
created: "2026-08-18"
updated: "2026-08-18"
area: "[[Echo]]"
project: "[[Echo Forge - Reconciliación y Scoring MT5]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Reconciliación y Scoring MT5]]"
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-08-18-echo-forge-mt5-fidelity-scope-bypass]]"
  - "[[2026-08-18-sqx-mt5-scope-identity-mismatch]]"
  - "[[2026-08-18-cursor-grok-4.6-echo-forge-mt5-m6-normal]]"
aliases: []
confidence: verified
source_session: 62c3bb1f-553c-4963-b25d-b9633df6c4a5
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo Forge MT5 — M6-NORMAL pausado (bypass de scope)

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Reconciliación y Scoring MT5.md`
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md`
  - `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`
  - `80-agents/memory/public/decision/symphony/2026-08-18-echo-forge-mt5-fidelity-scope-bypass.md`
  - `80-agents/memory/public/known-error/symphony/2026-08-18-sqx-mt5-scope-identity-mismatch.md`
  - repo `xKoRx/symphony`: `8f0cfa0` (bypass) + `9e7c8c2` (evidencia Attempt 7)

## Motivo

- Owner pidió ejercitar el comparador y pausar M6 para volver a arquitectura. M6-NORMAL/M6-TOP/M7 no se cierran.

## Fuentes usadas

- Wave `m6-shadow-20260818-007` / Temporal `sqx-main-v1-830a9c9d-4118-4ed8-a705-51e5fa84868e` COMPLETED; Mongo 13 Scores `COMPUTED`.

## Validación

- `go test ./sqx/core/evaluation/ ./sqx/activities/worker/ ./sqx/adapters/mt5/scoring/ ./sqx/workflows/` PASS. E2E Attempt 7 PASS operacional.

## Rollback

- Revertir `8f0cfa0` restaura las 4 puertas y vuelve a `NOT_COMPARABLE` en brownfield.

## Conflictos

- Ninguno. Los `COMPUTED` de Attempt 7 no contradicen el predicado original: está comentado a propósito.
