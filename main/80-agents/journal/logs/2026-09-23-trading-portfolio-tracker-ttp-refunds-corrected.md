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

# Trading Portfolio Tracker — refunds TTP corregidos

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Personal/Trading Portfolio Tracker/Trading Portfolio Tracker.md`

## Motivo

- Corregir TTP: las 7 facturas mostradas son gastos y sólo existen 2 refunds de las dos cuentas funded 50k.

## Fuentes usadas

- Captura de 7 facturas TTP/contexto por US$2.237,35.
- Declaración directa del owner: 2 cuentas funded de 50k y 2 refunds; usar provisionalmente US$261,75 × 2.

## Resolución aplicada

- Se eliminan los cuatro movimientos inferidos anteriormente como cash-in TTP.
- Se registran dos refunds provisionales de US$261,75 cada uno, total US$523,50.
- Los refunds reducen costo económico, pero no trading profit.
- Cash recibido acreditado queda en US$4.484,63.
- Trading payouts mínimos confirmados se mantienen en US$3.961,13.

## Validación

- US$261,75 × 2 = US$523,50.
- El gasto TTP bruto permanece en US$2.237,35.
- No se inventan fechas exactas de los refunds.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin credenciales ni identificadores sensibles.

## Rollback

- Revertir si la evidencia posterior muestra que los refunds tuvieron otro monto.
