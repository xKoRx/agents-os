---
type: decision
schema_version: 1
scope: project
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities: []
related:
  - "[[2026-09-04-reretester-single-artifact-contract]]"
  - "[[2026-09-04-echo-forge-c3-lean-0289-blocked-reretester]]"
  - "[[2026-08-31-forge-campaign-stop-policy-v1-contract]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-C3-FINAL-RERETESTER-SINGLE-ARTIFACT-RCA-V1-TOP
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
---

# 2026-09-04-final-reretester-empty-fanin-rca

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- CERT-A `0.2.89` CampaignRef `11741c54-e068-4e60-adf3-bc5ffecf680c` materializó una wave y un Generic child; el child murió en `05_reretester` con `final reretester activity must return exactly one key and one StrategyArtifact`.
- El productor durable `sqx-final-reretester.v1` admite `CompleteEmpty` (0 `.sqx` es éxito de activity). El consumer del fan-out exigía 1+1 por activity y abortaba el cohort entero.

## Decisión

- **ROOT_CAUSE primaria:** `CONSUMER_CARDINALITY_ASSUMPTION_BUG`.
- Semántica correcta: empty per-strategy es eliminación de esa estrategia; el fan-in conserva solo outputs 1+1 válidos; N_out ≤ N_in.
- El test `TestFinalReretesterFanoutRejectsPartialAndInvalidOutputs` mode `zero` congela el invariante incorrecto y debe invertirse en el fix NORMAL; no se implementa en esta sesión.
- C3 physical certification permanece `BLOCKED / CLOSED`; no hay recertificación física en esta RCA.

## Rationale

- Temporal, PostgreSQL y MinIO coinciden: 3 activities, 2 produced + 1 CompleteEmpty en Hera (`225e111a-fe51-45c5-979c-d3ad6376ca65`). El error nombra esa StrategyRef. Los 2 `.sqx` reales existían y fueron descartados por el gate del workflow.
- `mergeGroupOutputs` ya salta batches vacíos; el fan-out de Final Reretester reinventó un validador más estricto que el contrato del productor.

## Consecuencias

- El FIX CONTRACT mínimo toca `validateFinalReretesterFanoutOutput` / `runFinalReretesterFanout` / `mergeFinalReretesterOutputs` y los tests de fan-out. No hay migration. Replay de historias FAILED no las reescribe. Recertificación exige identidad CERT-A nueva tras un patch de release.
- No se reabre Strategy Identity, Campaign Stop Policy, reuse parcial ni lean config como causa primaria.

## Alternativas descartadas

- Tratar empty como fallo de activity en el productor: peor; `future.Get` también tumba el cohort.
- Inferir cardinalidad solo del string de error: rechazado; la evidencia durable muestra 2 artefactos reales.
- Reusar Campaign `11741c54-…` o la histórica `592944e2-…` como fixture: prohibido.
