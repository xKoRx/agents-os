---
type: decision
schema_version: 1
scope: project
created: "2026-08-26"
updated: "2026-08-26"
area: "[[Echo Forge]]"
project: "[[Echo Forge]]"
application: "[[Symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Symphony]]"
related:
  - "[[FEAT-SQX-CROSS-FLOWRUN-REUSE]]"
aliases: []
confidence: verified
source_session: SQX-OUTPUT-NAMESPACE-OWNERSHIP-PRE-SQX-GUARD-CORRECTION-NORMAL
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
  - tech/sqx
---

# 2026-08-26-sqx-output-namespace-ownership-pre-sqx-guard

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

Los namespaces físicos de salida SQX siguen siendo direccionados por `BuildMinIOPath` sin `FlowRunRef`, `StageExecutionRef`, request ID ni Temporal RunID, pero ahora pueden ser producidos por múltiples FlowRuns.

## Decisión

- El owner durable es la pareja exacta `FlowRunRef + StageExecutionRef` y vive en PostgreSQL, con `UNIQUE(bucket, namespace_key)` como autoridad de carrera.
- Un claim nuevo inserta y hace ACK; el mismo owner reintenta con ACK idempotente; cualquier otro owner recibe `CONTRACT_CONFLICT` sin mutación.
- El guard se ejecuta después de resolver StageExecution y antes de `execute_sqx`, sólo para Builder, Retester, Optimizer y Final Reretester durables. `SourceFolder` nunca se reclama.
- No hay release automático; MinIO write-once e histórico selector cross-FlowRun quedan diferidos.

## Rationale

La reserva PostgreSQL protege contra colisiones antes del side effect SQX y evita adoptar accidentalmente un namespace con artefactos parciales o de owner desconocido.

## Consecuencias

Los outputs nuevos quedan protegidos por ownership; los artifacts históricos sólo permanecen utilizables como lectura. La prueba de carrera del ownership pasó con PostgreSQL embebido; la suite completa conserva un fallo ajeno en Strategy Identity v2.

## Alternativas descartadas

- No se usa MinIO listing/metadata, filesystem lock, mutex ni serialización Temporal como autoridad.
- No se añade identidad de FlowRun al path físico ni se amplía `ControlPlaneStore` con un comando no relacionado.
