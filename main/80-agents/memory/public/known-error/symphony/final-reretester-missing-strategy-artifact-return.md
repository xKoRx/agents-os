---
type: known_error
schema_version: 1
scope: application
created: "2026-08-24"
updated: "2026-08-24"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities:
  - "[[StrategyQuant X]]"
  - "[[Strategy Identity v2]]"
related:
  - "[[2026-08-24-durable-strategy-identity-v2-builder-conflict-new-request-audit]]"
aliases:
  - final reretester StrategyArtifact contract
  - final reretester exactly one key error
confidence: verified
source_session: DURABLE-STRATEGY-IDENTITY-V2-BUILDER-CONTRACT-CONFLICT-REQUEST-ID-NEW-NORMAL
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - app/echo-forge
  - tech/symphony
---

# Final Reretester returns no StrategyArtifact

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- La corrida fresca pasa Builder, clasificación/ranking, Retester, Optimizer, WFM, Robust y Apply, pero Temporal falla en `05_reretester` con `final reretester activity must return exactly one key and one StrategyArtifact`.

## Causa

- Para la estrategia `b42281a9-fdde-40a0-8d7a-ab26570b7d08`, el activity persiste una evaluación (`sha256:8ae121cc521fa4f9a091e8220cb7a1bd369c886b2a611b530237a35163bf02e6`) pero no devuelve el contrato de salida esperado: no hay Artifact asociado.

## Impacto

- TradeList, MT5 y Score/Ranking no se ejecutan; la certificación de Strategy Identity v2 queda bloqueada aunque la continuidad de StrategyRef previa sea correcta.

## Detección

- Temporal Workflow History termina con `WorkflowExecutionFailed`; verificar el activity `project` de `05_reretester` y la forma de su resultado antes de una nueva certificación.

## Mitigación

- No corregir durante la auditoría. Capturar el error exacto, la StageExecution y las colecciones persistidas; el siguiente handoff es `DURABLE-BUILDER-STAGE-COMPLETION-CONFLICT-RCA-TOP` según el contrato de sesión.

## Evidencia

- Fresh run: RequestID `strategy-v2-cert-20260824T051824Z-e3b1e0d1`; FlowRun `576541a7-bea2-4d66-b806-99fedfde231a`; StageExecution `d5c2b631-220d-4d8d-ab4c-8e459602108a`; Workflow `sqx-main-v1-1aafdc1f-c31f-44de-8189-9931d7d84e3c`, RunID `01a03234-c7e5-74a5-ae48-87fbd221eed1`.
