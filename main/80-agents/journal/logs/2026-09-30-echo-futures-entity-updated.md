---
type: change_log
schema_version: 1
scope: session
created: "2026-09-30"
updated: "2026-09-30"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
related:
  - "[[Echo Futures/artifacts/d6-earn2trade-preflight-20260930/EARN2TRADE-FIRST-PARTY-PREFLIGHT-RESEARCH]]"
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

# Echo Futures entity updated — 2026-09-30

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Futures/Echo Futures.md`

## Motivo

- El Owner seleccionó Gauntlet Mini 50K (GAU50) como cuenta canónica Earn2Trade para el MVP de D6.
- TCP50 deja de ser candidato activo para este MVP porque su growth path no aporta al objetivo actual.

## Fuentes usadas

- Decisión explícita del Owner en sesión.
- `10-projects/Echo Futures/artifacts/d6-earn2trade-preflight-20260930/EARN2TRADE-FIRST-PARTY-PREFLIGHT-RESEARCH.md`

## Resolución aplicada

- Se registró `D6_E2T_PROGRAM = GAU50`.
- Se mantuvo intacto el blocker existente de automatización/API entitlement.
- No se autorizó implementación ni se modificaron contratos D5.

## Validación

- El proyecto canónico fue actualizado sobre `master`.
- Commit de la entidad: `28fad5539d3eb6f6ac910dd90193066131b2d6fd`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni credenciales.

## Rollback

- Revertir el commit de actualización del proyecto si el Owner cambia la selección de programa.


## Additional change — GAU50 evaluation inventory

### Cambio

- **Tipo:** updated
- **Archivo:** `10-projects/Echo Futures/Echo Futures.md`

### Motivo

- El Owner confirmó la compra de 5 evaluaciones GAU50, cada una con un reset gratuito.

### Resolución aplicada

- Se registraron 5 evaluaciones compradas + 5 resets gratuitos.
- Capacidad operacional registrada: hasta 10 intentos de evaluación totales.
- Se evitó modelarlo como 10 cuentas simultáneas.

### Fuente

- Confirmación explícita del Owner en sesión.

### Validación

- Commit de la entidad: `e3946baf7fae5ec24deced2d8cfc8d799fe7a0f0`.


## Additional change — NinjaTrader certification target

### Cambio

- **Tipo:** updated
- **Archivo:** `10-projects/Echo Futures/Echo Futures.md`

### Motivo

- El Owner confirmó que las GAU50 compradas usan Tradovate / NinjaTrader y autorizó comenzar la certificación.

### Resolución aplicada

- Se fijó `D6_E2T_TRANSPORT_CERT_TARGET = NINJATRADER_TRADOVATE`.
- La certificación comienza por prueba física sin órdenes antes de cualquier implementación.
- Tradovate REST/WebSocket directo queda fuera del primer camino D6.
- La ambigüedad pública de policy/entitlement se conserva como riesgo aceptado por Owner, no como permiso confirmado.

### Fuente

- Confirmación explícita del Owner en sesión.
- Evidencia oficial Earn2Trade sobre NinjaTrader–Tradovate y setup de Evaluation.

### Validación

- Commit de la entidad: `4e953c3abe4d0697b88b064656bbf641c7440664`.


## Additional change — C0 manager reclassification

### Cambio

- **Tipo:** updated
- **Archivo:** `10-projects/Echo Futures/Echo Futures.md`

### Motivo

- El artifact C0 certificó transporte físico pero quedó bloqueado por límites de observabilidad de la identidad local.
- El Owner aportó evidencia física adicional: un único login Tradovate en NinjaTrader Desktop expone las 5 GAU50 compradas.

### Resolución aplicada

- Se registró `EVALUATION_ACCOUNT_VISIBLE = PASS (OWNER_OBSERVED)`.
- Se registró `GAU50_VISIBLE = PASS (OWNER_OBSERVED, count=5)`.
- Se re-clasificó el estado como `D6_C0_NINJATRADER = PARTIAL_PASS_PENDING_GUI_OBSERVABLES`.
- El acceso ACL de `echo-dev` no se promovió a decisión arquitectónica.
- Reconnect/restart permanece pendiente para certificación física final, pero no bloquea C1.

### Fuente

- Artifact C0 de certificación NinjaTrader/Tradovate.
- Observación física explícita del Owner en sesión.

### Validación

- Commit de la entidad: `4f8de1222b561ae0dd6d714f1234d636c0aba86c`.
