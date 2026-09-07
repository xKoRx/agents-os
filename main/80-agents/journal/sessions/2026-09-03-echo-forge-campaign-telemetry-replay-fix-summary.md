---
type: session
schema_version: 1
scope: session
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related: []
aliases: []
confidence: high
source_session: ECHO-FORGE-CAMPAIGN-TELEMETRY-AND-REPLAY-FIX-0.2.89-NORMAL
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

%% Filename: YYYY-MM-DD[-HHMM]-<human-topic>-summary.md. Never use UUIDs/hashes as visible names; put external IDs in source_session. %%

# 2026-09-03-echo-forge-campaign-telemetry-replay-fix-summary

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Corregir los contratos TelemetryCarrier de ForgeCampaign y hacer replay-safe el workflow sin release, deploy ni C3.

## Contexto cargado

- Echo Forge checkpoint, baseline `7047a9c`, SDK `c855944`, release física `0.2.88`, C3 `BLOCKED / CLOSED`.

## Trabajo realizado

- Se agregaron cinco getters zero-value, assertions contra runtime/SDK, interceptor test real, cinco payload tests, replay regression con WorkflowID arbitrario, wrong-ID durable validation y Wave/RequestID distinction. Se eliminó el gate runtime WorkflowID del workflow.

## Artifacts creados o modificados

- Commit `a846adca3896cf578cf27eb854d9ea9bb725997d` `fix(sqx): repair campaign activity contracts`, push `origin/master`; solo seis archivos autorizados staged.

## Memoria propuesta o creada

- Decision, known-error actualizado por change log, agent run, feedback, summary y checkpoint del proyecto; Graphify quedó `ATTEMPTED / DEGRADED` sobre índice stale, con fallback enfocado.

## Decisiones

- Se preservaron `CAMPAIGN_PARTIAL_PIPELINE_REUSE` como capability gap/optional y `MT5_COMPILE_RETRY_POLICY_AUTHORITY_DRIFT` como open/non-blocking; no se marca C3 certificada.

## Pendiente

- Replay Campaign bloqueada: PASS, 5 eventos, sin nondeterminism. Control Generic: PASS, 470 eventos, sin nondeterminism. Campaign permanece Running/PENDING con `forge_campaign_start` Scheduled, attempt 151 y last failure histórico; siguiente exacto: `ECHO-FORGE-RELEASE-0.2.89-CONTAIN-BLOCKED-CAMPAIGN-AND-C3-LEAN-RECERT-NORMAL`.
