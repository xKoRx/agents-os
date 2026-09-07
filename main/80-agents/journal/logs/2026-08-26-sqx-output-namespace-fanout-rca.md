---
type: change_log
schema_version: 1
scope: session
created: "2026-08-26"
updated: "2026-08-26"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-08-26-zcode-glm-5-3-sqx-output-namespace-fanout-rca-top]]"
aliases: []
confidence: verified
source_session: SQX-OUTPUT-NAMESPACE-OWNERSHIP-FANOUT-SEMANTICS-RCA-TOP
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/echo-forge
---

# 2026-08-26-sqx-output-namespace-fanout-rca

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md` (checkpoint append-only con el challenge y la decisión).

## Motivo

La sesión RCA demostró con evidencia material que la decisión congelada FD-5 («output namespace owner = producer StageExecution single», `specs/FEAT-SQX-CROSS-FLOWRUN-REUSE` en `xKoRx/symphony` @ `9517f92`, implementada en `059326d`) es incompatible con el fan-out legítimo de Retester/Optimizer/Final Reretester: N StageExecutions hermanas del mismo FlowRun comparten carpeta de etapa, `Config.Strategy` base y TaskPath, y el guard las rechaza con `CONTRACT_CONFLICT` en retry infinito.

## Fuentes usadas

- Baseline `6ec1fe69930388927d6c21f5a69c39a95876d0c8`; código del guard (`sqx/adapters/registry-postgres/output_namespace_ownership.go:85-87`), fan-out (`sqx/workflows/generic_workflow.go:1322-1352,1442-1470,1660-1672`) e identidad (`sqx/core/domain/persistence_identity.go:278-279`); cardinalidad física documentada del FlowRun durable `9b010637` (`specs/FEAT-SQX-DURABLE-PIPELINE-CLOSURE/FINAL-E2E.md:2306-2317`); listado MinIO read-only; E2E ownership 0.2.73 (Run A `52e93a46`).

## Resolución aplicada

Challenge formal contra FD-5 aceptado y persistido en el checkpoint del proyecto; la unidad de ownership requerida pasa a ser Opción A (FlowRunRef + bucket + namespace_key/stage slot; `owner_stage_execution_id` degrada a provenance; cross-FlowRun write sigue prohibido). La corrección de código/spec NO se implementó en esta sesión (read-only por diseño): queda para `SQX-OUTPUT-NAMESPACE-OWNERSHIP-FANOUT-CORRECTION-NORMAL`.

## Validación

- PASS: verificación directa de todas las líneas load-bearing por el agente padre; convergencia de 4 auditorías read-only independientes; HEAD == baseline; dirty foreign preservado.
- Degraded: PG/Mongo inaccesibles desde esta máquina (cardinalidad runtime basada en evidencia documentada de la certificación Attempt 13 + MinIO firmado).

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

El challenge es reversible documentalmente: revertir el checkpoint append y restaurar FD-5 como vigente; no se tocó código, schema ni specs del repo.
