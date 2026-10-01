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
