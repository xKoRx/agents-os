---
type: change_log
schema_version: 1
scope: session
created: 2026-09-23
updated: 2026-09-23
area: "[[Personal]]"
project: "[[Trading Portfolio Tracker]]"
application:
entities:
  - "[[Trading Portfolio Tracker]]"
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

# Trading Portfolio Tracker — Axi reclasificado

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Personal/Trading Portfolio Tracker/Trading Portfolio Tracker.md`

## Motivo

- Corregir la clasificación económica de Axi Select según información directa del owner.

## Fuentes usadas

- Declaración directa del owner: aproximadamente US$2.200 en Axi corresponden a inversión recuperable actualmente.

## Resolución aplicada

- Axi deja de considerarse gasto hundido.
- Se registra ~US$2.200 como capital desplegado recuperable.
- Cash-out bruto consumido conocido se mantiene en US$6.068,86 + FTMO pendiente.
- Cash desplegado total conocido pasa a ~US$8.268,86 + FTMO pendiente.

## Validación

- La reclasificación no altera los payouts Axi ya registrados.
- Se mantiene separada la noción de capital recuperable, gasto consumido y cash-in.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin credenciales ni identificadores sensibles.

## Rollback

- Revertir si se confirma que el capital Axi dejó de ser recuperable.
