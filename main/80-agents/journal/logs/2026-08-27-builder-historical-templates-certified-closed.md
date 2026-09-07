---
type: change_log
schema_version: 1
scope: session
created: "2026-08-27"
updated: "2026-08-27"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities: []
related: []
aliases: []
confidence: verified
source_session: SQX-CROSS-FLOWRUN-BUILDER-TEMPLATES-E2E-NORMAL
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Builder histórico cross-FlowRun certificado

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `80-agents/memory/public/decision/symphony/2026-08-27-builder-historical-templates-certified-closed.md`
  - `80-agents/journal/agent-runs/2026-08-27-codex-unknown-sqx-cross-flowrun-builder-templates-e2e-normal.md`
  - `80-agents/journal/feedback/system-1/2026-08-27-sqx-cross-flowrun-builder-templates-e2e-session-feedback.md`

## Motivo

- Se completó la certificación física E2E de historical Builder templates sin modificar código ni reiniciar Temporal.

## Fuentes usadas

- Release `0.2.76`, Temporal history de D, Postgres registry, Mongo evidence, MinIO exact ObjectKeys y logs SQX del worker.

## Resolución aplicada

- Se persistió la decisión `CERTIFIED_CLOSED` y el resultado PASS/CLOSED con el siguiente track exacto `SQX-CROSS-FLOWRUN-REUSE-FINAL-CLOSURE-TOP`.

## Validación

- Source ownership/evidence permanecieron sin cambios; target ownership quedó en D; 20 outputs nuevos y 20 Evaluations fueron reconciliados.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- El registro es reversible eliminando la decisión y este log; no se alteró código ni configuración compartida.
