---
type: change_log
schema_version: 1
scope: session
created: "2026-08-28"
updated: "2026-08-28"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[AGENTS OS]]"
related:
  - "[[2026-08-28-durable-artifact-verified-reads-final-e2e-normal]]"
aliases: []
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-FINAL-E2E-NORMAL
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-28-durable-artifact-verified-reads-final-e2e-normal-change-log

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `80-agents/memory/public/decision/2026-08-28-durable-artifact-verified-reads-final-e2e-normal.md`
  - `80-agents/memory/public/known-error/symphony/durable-verified-reads-apply-reconcile-infers-digest-from-key.md`
  - `80-agents/journal/logs/2026-08-28-durable-artifact-verified-reads-final-e2e-normal-change-log.md`
  - `80-agents/journal/agent-runs/2026-08-28-codex-durable-artifact-verified-reads-certification.md`
  - `80-agents/journal/feedback/system-1/2026-08-28-durable-artifact-verified-reads-final-e2e-session-feedback.md`

## Motivo

- Persistir la matriz de certificación, invariantes frozen y evidencia física en Agents OS; registrar el blocker reusable para el RCA de Apply.

## Fuentes usadas

- Baselines exactos de Symphony/SDK, manifest de release `0.2.78`, procesos de Zeus/Hera/Kronos/Windows, logs de intake real y auditoría source/runtime del path durable.
- Harness controlado contra MinIO real para valid/mismatch/missing/cohort cleanup.

## Resolución aplicada

- Se desplegó y observó `0.2.78`; no se modificó código de producto. Se cerró la certificación como BLOCKED al encontrar que Apply reconstruye digest desde key/bytes.

## Validación

- Tests dirigidos de storage, WFM físico, MT5 y carriers relevantes: PASS. Positive full chain y corruption activities posteriores al blocker: no certificados.
- `CODE_CHANGES=NONE`, `TEMPORAL_RESET_USED=NO`; foreign dirty preservado. La suite SDK completa conserva fallos de dependencias privadas/drift no atribuibles.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- No rollback: release `0.2.78` permanece activa; no se alteraron ni limpiaron cambios foreign dirty ni objetos disposable.
