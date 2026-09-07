---
type: raw_session
schema_version: 1
scope: session
created: "2026-08-18"
updated: "2026-08-18"
area: "[[Echo]]"
project: "[[Echo Forge - Reconciliación y Scoring MT5]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Reconciliación y Scoring MT5]]"
related:
  - "[[2026-08-18-echo-forge-mt5-m6-normal-closed]]"
aliases: []
confidence: verified
source_session: 62c3bb1f-553c-4963-b25d-b9633df6c4a5
load_policy: never
indexable: false
index_priority: never
tags:
  - kind/raw-session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-raw.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# Echo Forge MT5 M6-NORMAL — raw

> [!warning]+ Raw session L0
> Archivo de auditoría y retrofit. Excluido del retrieval normal y de Graphify.

## Contexto

- Agente: [[Cursor]] / Cursor Grok 4.6
- Proyecto o entidad: [[Echo Forge - Reconciliación y Scoring MT5]]
- Objetivo de la sesión: M6-NORMAL E2E sobre Foundation; owner pidió bypass de 4 puertas de scope, wave real y cierre con continuidad hacia arquitectura.

## Transcript

```
Cursor transcript 62c3bb1f-553c-4963-b25d-b9633df6c4a5
Pedido: TODO+comentar instrument/timeframe/period_* para que el comparador corra; cerrar tasks/proyecto/despliegue; cerrar sesión.
Hecho: 8f0cfa0 bypass; deploy 0.2.53; wave m6-shadow-20260818-007 example_flow_16; Temporal sqx-main-v1-830a9c9d-4118-4ed8-a705-51e5fa84868e COMPLETED 26m12s; 13 scores COMPUTED; docs 9e7c8c2.
```

## Evidencia externa

- `specs/FEAT-SQX-MT5-RECONCILIATION-SCORING/M6-NORMAL-SHADOW-EVIDENCE.md` Attempt 7
- Mongo `forge.scores` created_at ≥ 2026-08-19T01:54Z
