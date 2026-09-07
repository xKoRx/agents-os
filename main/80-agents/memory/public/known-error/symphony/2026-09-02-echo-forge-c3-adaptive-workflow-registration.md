---
type: known_error
schema_version: 1
scope: project
created: "2026-09-01"
updated: "2026-09-02"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related:
  - "[[2026-08-31-forge-campaign-stop-policy-v1-contract]]"
  - "[[2026-09-02-echo-forge-c3-mt5-fidelity-period-mismatch]]"
aliases: []
confidence: verified
source_session: ECHO-FORGE-C3-PHYSICAL-BLOCKERS-RCA-TOP
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
  - project/echo-forge
---

# Echo Forge C3 production worker registers AdaptiveTypeWorkflow

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- El gate de registro C3 exige `ForgeCampaignWorkflow` y `GenericSQXWorkflow`, y prohíbe `AdaptiveTypeWorkflow`; el worker productivo registra `AdaptiveTypeWorkflow` y también `AdaptiveSQXWorkflow`.

## Causa

- En `sqx/cmd/sqx-worker/main.go` líneas 331–332: `w.RegisterWorkflow(gwf.AdaptiveSQXWorkflow)` y `w.RegisterWorkflow(gwf.AdaptiveTypeWorkflow)`.
- El único CHILD_START de `AdaptiveTypeWorkflow` es `forkTypeWorkflows` en `adaptive_workflow.go`. No hay DIRECT_START productivo: watcher/dispatcher y `ForgeCampaignWorkflow` arrancan solo `GenericSQXWorkflow`.
- Las activities Adaptive-only no están registradas en el worker.

## Impacto

- La release `0.2.84` converge, pero el registration set incumple el contrato C3. No hay executions Adaptive físicas que dependan del registro.

## Detección

- Source `02fabffe958854ab30e017301a8c30aaada527ac`; RCA Temporal namespace `sqx-prop` queue `sqx-main-queue`.

## Mitigación

- Clasificación RCA: `B1_SAFE_REMOVE_REGISTRATION`. Unregister ambos workflows Adaptive. No drain. No borrar `adaptive_workflow.go` en el slice C3.
- Temporal: 0 executions Adaptive (open/closed), 0 schedules. Backward-safe.
- Resolución aplicada en `ECHO-FORGE-C3-PHYSICAL-BLOCKERS-FIX-NORMAL`: se eliminaron sólo ambos `RegisterWorkflow(gwf.Adaptive...)` del worker productivo; las definiciones y tests Adaptive se conservaron.
- El fix está en `48997d773e91dec9b8fe57fbd1650e8d8beb8b57` y requiere release físico `0.2.85` para validar runtime.

## Evidencia

- Symphony HEAD: `02fabffe958854ab30e017301a8c30aaada527ac`; flota `0.2.84`.
- RCA: `specs/FEAT-SQX-ADAPTIVE-WORKFLOW/rca/RCA-C3-B1-adaptive-registration.md`.
- Source regression: `rg` en `sqx/cmd/sqx-worker` devuelve cero registros Adaptive; worker tests normal/race y vet PASS.
