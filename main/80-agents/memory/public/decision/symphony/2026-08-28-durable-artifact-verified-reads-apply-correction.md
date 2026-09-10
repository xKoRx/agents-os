---
type: decision
schema_version: 1
scope: project
created: "2026-08-28"
updated: "2026-08-28"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-08-28-durable-verified-reads-apply-reconciliation-rca]]"
  - "[[2026-08-28-durable-artifact-verified-reads-final-e2e-normal]]"
aliases: []
confidence: verified
source_session: DURABLE-ARTIFACT-VERIFIED-READS-APPLY-CORRECTION-NORMAL
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - scope/project
---

# 2026-08-28-durable-artifact-verified-reads-apply-correction

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- El recovery Apply debía cerrar el intervalo físico `physical.Apply → MinIO` sin inferir autoridad desde MinIO. El baseline exacto fue `5e93c7cda3f4fcc825f3939a951247cd4e63fec2`.

## Decisión

- PostgreSQL registra primero un `StageProducerOutput` insert-only/idempotente con `DurableArtifactRef` exacto y `ProducerContextDigest`. Sólo después se escribe en MinIO. Evaluation immutable vuelve a ser la autoridad normal una vez existe.
- El contexto canónico incluye schema/version, `ProducerContractVersion`, `StageExecutionRef`, `DecisionRef` y `ConfigDigest`, serializados como documento JSON explícito y hasheado determinísticamente.
- Stage `COMPLETED` recupera exclusivamente desde `StageExecutionResults → exact EvaluationRef → immutable Evaluation → exact ArtifactRef`; Stage `RUNNING` primero intenta la Evaluation determinística y luego reconcilia el producer record. Un artifact ausente/corrupto o cualquier mismatch es `CONTRACT_CONFLICT`.

## Rationale

- MinIO quedó como dato bajo verificación: `VerifyApplySelectedRun` recibe el expected ref, hace GET, valida metadata y compara stream contra tamaño/SHA esperados. Se eliminó `ReconcileApplySelectedRun` del durable path. El rerun posterior al producer record sólo puede escribir si reproduce exactamente el ref sellado.

## Consecuencias

- La corrección cierra los gaps record→MinIO, MinIO→Evaluation y Evaluation→Complete sin hacer depender correctness de determinismo físico.

## Alternativas descartadas

- Derivar expected size/SHA desde `StatObject`, bytes encontrados, ETag, listing o key-only; cualquiera reabre la autoridad circular que este cambio cierra.
