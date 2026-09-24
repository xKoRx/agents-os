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

# Trading Portfolio Tracker — The5ers agregado

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Personal/Trading Portfolio Tracker/Trading Portfolio Tracker.md`

## Motivo

- Incorporar una cuenta histórica perdida de The5ers al inventario F0.

## Fuentes usadas

- Declaración directa del owner: cuenta The5ers High Growth 10k, perdida; costo recordado entre US$400 y US$500.

## Resolución aplicada

- Se registra 1 cuenta histórica The5ers High Growth 10k con estado `lost`.
- Se usa US$500 como costo estimado provisional por criterio pesimista, sin tratarlo como monto confirmado.
- El cash-out bruto identificado pasa de US$5.568,86 a US$6.068,86.
- Queda pendiente reconciliar si esta cuenta estaba incluida dentro del universo inicial de 17.

## Validación

- La estimación conserva el rango recordado y usa su techo, sin inventar una factura.
- La cuenta perdida no incrementa notional activo.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin credenciales ni identificadores sensibles.

## Rollback

- Revertir esta actualización si se confirma que la cuenta no existió o pertenecía a otra firma/programa.
