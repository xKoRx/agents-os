---
type: decision
schema_version: 1
scope: project
created: "2026-08-27"
updated: "2026-08-27"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-08-27-sqx-historical-cohort-fanout-correction]]"
  - "[[SQX-CROSS-FLOWRUN-HISTORICAL-SOURCE-RESOLUTION-E2E-NORMAL]]"
aliases: []
confidence: verified
source_session: SQX-CROSS-FLOWRUN-HISTORICAL-SOURCE-FANOUT-CORRECTION-NORMAL
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - tech/sqx
  - tech/temporal
  - tech/idempotency
  - scope/public
  - scope/project
---

# Resolución histórica durable en el boundary del grupo

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

La capa de datos histórica de `fd042fb` es válida y produce un cohort N de `StrategyArtifacts`. `ProjectActivity`, Retester y Optimizer, en cambio, requieren exactamente una Strategy por invocación y por StageExecution.

## Decisión

Para un `group` vacío con `SourceFolder` y una tarea durable Retester u Optimizer explícita, `GenericSQXWorkflow` invoca una sola vez la Activity estrecha `resolve_historical_cohort`. La Activity conserva ownership, gate `COMPLETED`, query Mongo determinística, validaciones, identity PG y membership `REPROCESSED`, y devuelve el `StratBatch` completo.

El fan-out existente usa `group.batch_size` y proyecta el binding exacto de cada slice. Con `batch_size: 1`, cada child recibe una key y su único artifact correspondiente; el child ejecuta Retester/Optimizer sin re-resolver el histórico. El mismo-flow devuelve cohort vacío sin query Mongo, membership ni fallback a `list_strats`.

## Rationale

La resolución a nivel ProjectActivity repetía la consulta por child y entregaba N artifacts a una frontera que exige cardinalidad uno. El boundary de grupo permite resolver una vez y conservar la correspondencia Strategy/Artifact durante todo el fan-out.

## Consecuencias

`SourceFolder` y `group + batch_size` siguen siendo el contrato de usuario; no se agregan campos, schema, índice, ownership ni identidad. El step `resolve_historical_source` dentro de ProjectActivity queda superseded y removido. Los grupos vacíos legacy sin semántica durable conservan `list_strats`.

## Alternativas descartadas

Mantener la resolución dentro de ProjectActivity, recortar el cohort a una Strategy o transportar el cohort completo a cada child: todas rompen la cardinalidad durable o esconden el bug de binding.
