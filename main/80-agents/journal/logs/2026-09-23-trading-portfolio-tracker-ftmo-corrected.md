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

# Trading Portfolio Tracker — FTMO corregido

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Personal/Trading Portfolio Tracker/Trading Portfolio Tracker.md`

## Motivo

- Corregir una clasificación previa errónea: los cuatro movimientos FTMO visibles correspondían a gastos, no cash-in.

## Fuentes usadas

- Captura FTMO con cuatro cuentas 100k y estados Pagado:
  - 2025-10-04: US$520,59
  - 2025-11-02: US$632,63
  - 2025-11-02: US$632,63
  - 2025-11-26: US$504,30
- Aclaración directa del owner de que la captura era parte de los gastos ya entregados.

## Resolución aplicada

- US$2.290,15 se mueve de cash-in pendiente a gasto histórico confirmado.
- Cash-out consumido conocido pasa a US$8.359,01.
- Cash recibido acreditado baja a US$5.580,71.
- Cash desplegado total conocido, incluyendo ~US$2.200 recuperables en Axi, queda en ~US$10.559,01.
- Se elimina la tarea de clasificar FTMO como reward/refund.

## Validación

- Total FTMO: 520,59 + 632,63 + 632,63 + 504,30 = US$2.290,15.
- La corrección preserva Axi como capital recuperable y no altera los payouts Orion/Axi.
- No se cambia la clasificación aún pendiente de TTP refunds/payouts.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin credenciales ni identificadores de acceso.

## Rollback

- Revertir sólo si evidencia posterior demuestra que esos cuatro cargos FTMO eran ingresos y no compras.
