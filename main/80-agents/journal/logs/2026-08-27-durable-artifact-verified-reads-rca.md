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
source_session: DURABLE-ARTIFACT-VERIFIED-READS-RCA-TOP
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-27-durable-artifact-verified-reads-rca

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `80-agents/memory/public/decision/symphony/2026-08-27-durable-artifact-verified-reads-rca.md` (created)
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md` (checkpoint append-only)
  - `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md` (delta interno)
  - `80-agents/journal/agent-runs/2026-08-27-zcode-glm-5-3-durable-artifact-verified-reads-rca-top.md` (created)

## Motivo

- Cierre del RCA read-only DURABLE-ARTIFACT-VERIFIED-READS-RCA-TOP: congelar invariantes de lectura verificada del durable Artifact Plane sobre baseline exacta `5e3c2b3` (write-once 0.2.77 CERTIFIED_CLOSED).

## Fuentes usadas

- Bootstrap Agents OS, decisión write-once final E2E, auditoría con 4 scouts mm-scout paralelos sobre `sqx/` y verificación parent selectiva (wiring/registration/dispatchers en `cmd/`, workflow switches, carriers Mongo).

## Resolución aplicada

- Se persistieron la autoridad durable de lectura (Evidence → DurableArtifactRef exacto), la primitiva `FetchDurableToPath` (temp oculto + streaming size/SHA + rename atómico), la evolución carrier `StrategyArtifact.Artifact`, `DownloadDurableToCustom` aditiva, taxonomía de errores (mismatch/missing → CONTRACT_CONFLICT non-retryable; transitorio → retriable), políticas de destino existente y fallo de cohort, gap material MQ5 (`ExportMT5EAResult` sin digest) y slicing S1/S2/S3. Sin cambios de código, schema, commit ni release.

## Validación

- HEADs == baselines (symphony `5e3c2b3`, sdk `ea09cc1`); evidencia file:line para cada reader/caller; verificación directa de los hechos que invertían clasificaciones (robust legacy sin wiring productivo, MT5 durable mode sin listing, project activity mapea ErrContractConflict→NonRetryable).

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- No aplica rollback de producto; las invariantes congeladas sólo cambian vía nueva decisión/challenge con evidencia material.
