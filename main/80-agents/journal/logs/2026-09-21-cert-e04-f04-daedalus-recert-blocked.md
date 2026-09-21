---
type: change_log
schema_version: 1
scope: session
created: "2026-09-21"
updated: "2026-09-21"
area: "[[Personal]]"
project: "[[Echo — Producto Integrado]]"
application:
entities:
  - "[[Echo]]"
  - "[[Echo Forge]]"
  - "[[Aranea]]"
related:
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[Echo — Live Platform V1]]"
  - "[[Echo Forge — Factory V2 Completion]]"
  - "[[Echo + Echo Forge — Deferred Certification Backlog]]"
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

# 2026-09-21 — Recertificación CERT-E04-01 + CERT-F04-03 en Daedalus (BLOCKED)

## Cambio

- **Tipo:** updated (Environment Contract §5.2 + reconciliación §7; Live Platform E-04; Factory V2 F04-03; Deferred Certification Backlog delta sin cierre de gates).
- **Archivo(s):**
  - `30-resources/aranea/07-integration/Echo + Echo Forge — Environment Contract.md`
  - `10-projects/Echo/agentes/Echo — Live Platform V1.md`
  - `10-projects/Echo/agentes/Echo Forge — Factory V2 Completion.md`
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md`
  - `80-agents/journal/agent-runs/2026-09-21-cursor-composer-cert-e04-f04-recert-blocked.md`
  - este change_log
- **Fuera del vault:** informe `~/aranea/work/cert-int-qa-20260921/FINDINGS-CERT-INT-QA-20260921.md` + evidence/logs.

## Motivo

- Owner mandó reanudar la certificación Forge→Echo tras el AS-BUILT de Core/Gateway DEV, sin redeploy, con auditoría exhaustiva y un solo informe.

## Fuentes usadas

- Environment Contract §5.1; FINDINGS previas 2026-09-20; corpus F04-02; runtime systemd/health/ETCD/PG MCP; suites audit `zz_audit_*` sobre PG descartable.

## Resolución aplicada

- Documentar evidencia física: runtime healthy pero ingest BLOCKED; defectos STILL_REPRODUCIBLE; golden bodies bloqueados; veredictos `CERT_E04_01_BLOCKED` / `CERT_F04_03_BLOCKED`; G6 NOT_EXECUTED. Cero cierre de gates por /health.

## Validación

- Read-back: Core/Gateway active + health 200; POST promotions 503; etcd forge_ingest/echo ingest absent; echo-develop sin promotion_records; audit H02/H07/H04/H05 FAIL; corpus validate+recompute 5/5.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos, bearers ni passwords.

## Rollback

- Revertir los cuatro deltas Markdown del vault; el workdir externo de evidencia puede conservarse.
