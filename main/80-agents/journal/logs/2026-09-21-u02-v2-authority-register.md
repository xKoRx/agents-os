---
type: change_log
schema_version: 1
scope: session
created: "2026-09-21"
updated: "2026-09-21"
area: "[[Personal]]"
project: "[[Polymarket Engine — MVP]]"
application:
entities:
  - "[[Polymarket Engine — MVP]]"
related:
  - "[[u02-v2-cash-confirmed]]"
  - "[[2026-09-21-u02-protocol-authority]]"
aliases:
  - "U-02 V2 authority register 2026-09-21"
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
  - area/personal
  - project/polymarket-engine
---

# 2026-09-21-u02-v2-authority-register

## Cambio

- **Tipo:** created (decisión canónica + este change log + handoff de consolidación). Sin código. Sin edición de notas que el agente Sports Reversion (S02) está actualizando (padre, continuidad Five-POC, guía, 00-index, log, POC-S03/S04).
- **Archivo(s):**
  - `main/80-agents/memory/public/decision/polymarket/u02-v2-cash-confirmed.md` (autoridad vigente)
  - `main/00-inbox/U-02 V2-CASH-CONFIRMED — handoff consolidación.md`
  - evidencia: `polymarket-engine-datasets/u02-protocol-authority-20260921/STATUS.md`

## Motivo

Mandato owner: registrar el dictamen V2 como autoridad vigente para mercados verificados; marcar `d5ce263` no aceptado para V2; conservar rama/v07/v08; `REAL_FEE_READY=false`; no implementar/recertificar/publicar; entregar al consolidator.

## Fuentes usadas

- Auditoría [[2026-09-21-u02-protocol-authority]] y `u02-protocol-authority-20260921/REPORT.md`.
- Checkout físico: integración `85e27ff` limpio; U-02 `fix/u02-buy-shares-accounting@d62768a` (código `d5ce263`); certificados v07/v08 intactos.

## Resolución aplicada

Autoridad vigente = [[u02-v2-cash-confirmed]] (`V2_CASH_CONFIRMED`). `d5ce263` = `PATCH_NOT_ACCEPTED_FOR_V2`. `REAL_FEE_READY=false`. Rama y receipts preservados.

## Validación

- `git rev-parse` integración `85e27ff`, dirty=0.
- U-02 HEAD `d62768a`, ancestro `d5ce263`, branch `fix/u02-buy-shares-accounting`.
- v07 baseline `c38f6c4`; v08 baseline `d5ce263`.
- Graphify `NOT_RUN`. Lint: notas materializadas por contrato.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin wallet, secretos ni órdenes

## Rollback

Borrar la decisión, este log, el handoff de inbox y `STATUS.md`. No toca engine, v07, v08 ni la rama U-02.

## Handoff al responsable de consolidación

Estado final listo para absorber sin reabrir U-02:

```text
U02_AUTHORITY: V2_CASH_CONFIRMED
PATCH_d5ce263: PATCH_NOT_ACCEPTED_FOR_V2
REAL_FEE_READY: false
INTEGRATION: feature/five-poc-integration@85e27ff (clean)
U02_BRANCH: fix/u02-buy-shares-accounting @ d62768a (preserve; do not merge)
V07: testdata/research-v07/certificate-v07.json baseline c38f6c4 (untouched)
V08: testdata/research-v08/certificate-v08.json baseline d5ce263 (untouched)
CANONICAL_DECISION: [[u02-v2-cash-confirmed]]
AUDIT_LOG: [[2026-09-21-u02-protocol-authority]]
EVIDENCE: polymarket-engine-datasets/u02-protocol-authority-20260921/
SPORTS_NOTES: not edited this turn (padre/continuidad/guía/wiki/POC-S03/S04)
CODE: no implement / no refactor / no recertify / no publish
LIVE: disabled
NEXT: consolidator may cite the decision; must not accept d5ce263 as V2 venue
```
