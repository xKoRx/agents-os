---
type: change_log
schema_version: 1
scope: session
created: "2026-08-24"
updated: "2026-08-24"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities:
  - "[[Strategy Identity v2]]"
related:
  - "[[durable-builder-retry-reemits-evaluations-under-same-stage]]"
  - "[[final-reretester-missing-strategy-artifact-return]]"
aliases: []
confidence: verified
source_session: DURABLE-STRATEGY-IDENTITY-V2-BUILDER-CONTRACT-CONFLICT-REQUEST-ID-NEW-NORMAL
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-24-durable-strategy-identity-v2-builder-conflict-new-request-audit

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

  - **Tipo:** conflict-resolution
- **Archivo(s):**
  - `input/example/config.json` request_id updated for the authorized fresh launch.
  - Durable/read-only audit records and session close artifacts.

## Motivo

- Determine whether Builder `contract_conflict` was request-id reuse or a reproducible defect, then run release 0.2.68 with a new request ID.

## Fuentes usadas

- Previous legacy run reused `m6-shadow-20260818-007` and the same StageExecution across three attempts. Fresh run used `strategy-v2-cert-20260824T051824Z-e3b1e0d1` and a new FlowRun/Workflow.

## Resolución aplicada

- Previous failure classified as reproducible Builder retry defect; fresh Builder passed. Fresh E2E later failed at Final Reretester output contract, so identity certification remains blocked.

## Validación

- New run: Builder `COMPLETED`, 58/58 durable stage executions `COMPLETED`, 20 v2 strategies/canonical IDs, 715 evaluations across 20 StrategyRefs. Temporal failed before TradeList/MT5/Score-Ranking with the exact Final Reretester error documented in the known-error note.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Preserve all historical data and code; no migrations, Strategy Identity changes, or code corrections were made.
