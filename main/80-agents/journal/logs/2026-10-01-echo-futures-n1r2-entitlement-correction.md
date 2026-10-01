---
type: change_log
schema_version: 1
scope: session
created: "2026-10-01"
updated: "2026-10-01"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
related:
  - "[[Echo Futures/artifacts/d6-ninjatrader-n1-20261001/N1-R2-CORRECT-EARN2TRADE-ENTITLEMENT]]"
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

# Echo Futures N1-R2 entitlement correction — 2026-10-01

## Cambio

- **Tipo:** updated + artifact nuevo
- **Archivo(s):**
  - `10-projects/Echo Futures/Echo Futures.md` (warning superseded en N1-R1 + sección D6 N1-R2)
  - `10-projects/Echo Futures/artifacts/d6-ninjatrader-n1-20261001/N1-R2-CORRECT-EARN2TRADE-ENTITLEMENT.md` (nuevo)

## Motivo

- El owner corrigió la premisa vigente: Earn2Trade SÍ permite automatización/estrategia propia; el blocker `entitlement=UNKNOWN` (OD-1 de N1-R1) era falso y debía eliminarse sin owner-risk model, bypass, nuevo enum ni nueva policy layer, usando el contrato D5 existente.

## Fuentes usadas

- Corrección owner 2026-10-01 (mandato N1-R2).
- Contrato D5 congelado `v3/sdk/futures/domain/provider.go` @ `xKoRx/echo@7af6210a`.
- Criterio canónico ALLOWED/CONDITIONAL del project note (Front C authoritative matrix, manager 2026-09-26).
- Research E2T existente `artifacts/d6-earn2trade-preflight-20260930/` (Pass 1 + Pass 2).

## Resolución aplicada

- Clasificación demostrada `ALLOWED` (criterio canónico + cero condiciones documentadas adjuntas al grant; `TransportSpec.Conditions` vacío; HARD RULE del mandato no dispara).
- ETCD DEV: `/echo/development/futures-bridge/accounts/E2T-GAU50-01/binding/entitlement` `UNKNOWN` → `ALLOWED`, única clave mutada, read-back doble (writer SDK + MCP ETCD RO), claves hermanas intactas, herramienta efímera borrada del worktree.
- Runtime: `echo-nt-feed-relay` (release `7af6210a`, sin rebuild) reiniciado; error `cannot be enabled with UNKNOWN automation entitlement` eliminado del journal; binding pasa `ProviderAccountBinding.Validate`.
- Project note: consecuencia bloqueante de N1-R1 marcada superseded; sección D6 N1-R2 añadida; historia preservada (research preflight intacto como historia válida de su fecha).

## Validación

- Referencias `OwnerRiskAcceptance`/`PhysicalEgressApproved` = 0 en el repo @ `7af6210a`; worktree limpio antes y después.
- Tests targeted ok: `v3/futures-bridge/internal/binding`, `v3/sdk/futures/domain`.
- `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0` (estructural; sin orden de verificación).
- Estado vault persistido por el sync cron del repo (`~/secondbrain`).

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni credenciales.

## Rollback

- Repoint ETCD `entitlement` a `UNKNOWN` y revertir las secciones del project note/artifact sólo si el owner revoca la corrección o una evidencia posterior refuta la clasificación `ALLOWED`; semántica D5 fail-closed se restaura sola al repoint.
