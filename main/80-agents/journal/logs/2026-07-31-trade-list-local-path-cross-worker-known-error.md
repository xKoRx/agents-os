---
type: change_log
scope: session
created: "2026-07-31"
updated: "2026-07-31"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Cierre de Etapa 4]]"
application: "[[sqx-worker]]"
entities:
  - "[[sqx-worker]]"
related:
  - "[[trade-list-exporter-local-path-cross-worker]]"
confidence: verified
source_session: "2026-07-31-trade-list-upsert-affinity"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Change log — known-error trade list local path cross-worker

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `80-agents/memory/public/known-error/symphony/trade-list-exporter-local-path-cross-worker.md`
  - `80-agents/memory/internal/agent-memory/2026-07-31-trade-list-upsert-affinity-redesign.md`

## Motivo

- Sesión diagnosticó que el split `trade_list_exporter` → `act_upsert_trade_list` pasa paths locales entre hosts; requiere rediseño.

## Fuentes usadas

- `sqx/activities/worker/trade_list_exporter_activity.go`
- `sqx/activities/worker/project_activity.go` (`UpsertTradeList`)
- `sqx/workflows/generic_workflow.go` (case trade_list_exporter)
- Spec `FEAT-SQX-TRADE-LIST-METADATA`
