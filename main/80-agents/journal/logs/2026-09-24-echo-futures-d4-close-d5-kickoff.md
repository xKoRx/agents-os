---
type: change_log
schema_version: 1
scope: session
created: "2026-09-24"
updated: "2026-09-24"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
  - "[[Echo Futures — Simulator v0]]"
  - "[[Echo Futures — D5 Prop Economics]]"
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-24 — Echo Futures D4 close and D5 kickoff

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Futures/Echo Futures.md`
  - `10-projects/Echo Futures/agentes/Echo Futures — Simulator v0.md`
  - `10-projects/Echo Futures/agentes/Echo Futures — D5 Prop Economics.md`

## Motivo

- Cerrar D4 tras certificación del simulator v0 y abrir D5 centrado en conversión desde evaluation comprada hasta primer retiro real.

## Fuentes usadas

- Resultado Shot 3 `CERTIFIED_V0`.
- Aclaración del owner sobre KPI de retiro real.
- Investigación web 2026 para delimitar el núcleo de futures prop firms principales.

## Resolución aplicada

- G4C accepted y D4 completed. D5 creado con Tier-1 inicial Topstep/Apex/MyFundedFutures/Tradeify/Take Profit Trader; FTMO Futures watchlist por lanzamiento reciente. `q=10%` queda sólo como fixture D4.

## Validación

- Bridge D4 cerrado, bridge D5 creado, baseline D5 apunta a simulator certificado `d4f42a4`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Reabrir D4 sólo ante contradicción material reproducible; revisar universo Tier-1 si evidencia actualizada lo justifica.
