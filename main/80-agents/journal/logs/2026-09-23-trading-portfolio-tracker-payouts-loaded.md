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

# Trading Portfolio Tracker — payouts iniciales cargados

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Personal/Trading Portfolio Tracker/Trading Portfolio Tracker.md`

## Motivo

- Incorporar la primera evidencia real de payouts entregada por el owner y avanzar F0 sin introducir doble conteo.

## Fuentes usadas

- Captura Axi Select "Tus pagos": seis montos visibles entre enero y agosto de 2026.
- Captura de listado de cuatro pagos Completed con IDs 132082, 133971, 136965 y 137652.
- Certificado Orion "Overall Rewards" fechado 2026-09-23 por US$2.417,58.

## Resolución aplicada

- Se registraron seis pagos Axi Select por un subtotal de US$2.178,87.
- Se registraron cuatro pagos por US$1.619,58 con firma pendiente porque la captura no expone su origen.
- Orion se registró como acumulado reconciliable de US$2.417,58 y no como evento adicional del ledger.
- Se fijó cash-in confirmado conservador en US$4.596,45 y máximo provisional en US$6.216,03 si el lote pendiente resulta ser independiente de Orion.

## Validación

- Sumas verificadas aritméticamente.
- El lote de firma pendiente queda explícitamente excluido del total conservador para impedir doble conteo.
- No se inventaron cuenta origen, fees ni fechas de día para los pagos Axi que sólo muestran mes.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** no contiene números de cuenta, credenciales ni identificadores de acceso; sólo IDs de transacción visibles en la evidencia del owner.

## Rollback

- Revertir el commit de actualización del proyecto y este log si se determina que las capturas no corresponden a payouts reales.
