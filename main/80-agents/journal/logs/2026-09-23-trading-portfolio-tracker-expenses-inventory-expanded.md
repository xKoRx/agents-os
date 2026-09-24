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

# Trading Portfolio Tracker — gastos e inventario ampliados

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Personal/Trading Portfolio Tracker/Trading Portfolio Tracker.md`

## Motivo

- Incorporar nueva evidencia de gastos, corregir Orion, ampliar inventario y separar refunds de payouts.

## Fuentes usadas

- Captura de 7 facturas Paid por US$2.237,35.
- Captura WSF de pagos por US$717,50 más transición Step-2 de US$0.
- Captura FTMO con cuatro movimientos Pagado por US$2.290,15.
- Declaración directa del owner sobre Orion: 2×100k, 3×50k, 1×25k Flash; una 50k perdida por inactividad; retiros reales US$1.365,82 y US$416,44.
- Declaración directa del owner sobre TTP: 2×50k funded y 2 refunds.
- Precios públicos actuales de Orion consultados el 2026-09-23 para una estimación conservadora, explicitada como no histórica.

## Resolución aplicada

- Orion queda con 6 cuentas históricas, 5 activas y US$325k de notional activo.
- El costo Orion se estima en US$2.614,01 usando promedio conservador de programas comparables actuales para 100k/50k y Orion Zero 25k como proxy pesimista para Flash.
- El certificado Orion de US$2.417,58 deja de contarse como retiro; cash realmente retirado: US$1.782,26.
- Se cargaron US$2.237,35 de facturas TTP/contexto y US$717,50 de WSF.
- Se registraron cuatro movimientos FTMO Pagado por US$2.290,15, pendientes de clasificar reward vs refund.
- Los dos refunds TTP se registran como eventos conocidos con monto todavía pendiente de asociación.

## Validación

- Totales aritméticos verificados.
- Ninguna estimación Orion se presenta como gasto histórico probado.
- Refunds y payouts quedan separados para no inflar trading profit.
- No se infieren estados actuales de WSF/FTMO más allá de la evidencia visible.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin credenciales ni identificadores de acceso.

## Rollback

- Revertir la actualización del proyecto y este log si las capturas se atribuyeron a una firma incorrecta.
