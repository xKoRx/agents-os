---
type: change_log
schema_version: 1
scope: project
created: "2026-08-26"
updated: "2026-08-26"
area:
project: "[[Echo Forge]]"
application: "[[Symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Symphony]]"
related:
  - "[[2026-08-26-sqx-output-namespace-ownership-pre-sqx-guard]]"
aliases: []
confidence: verified
source_session: SQX-OUTPUT-NAMESPACE-OWNERSHIP-PRE-SQX-GUARD-CORRECTION-NORMAL
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/project
  - project/echo-forge
---

# 2026-08-26-sqx-output-namespace-ownership

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):** Migration 007, output ownership port/adaptador, pipeline guard y pruebas en `xKoRx/symphony`.

## Motivo

Implementar la corrección requerida por el contrato cross-FlowRun: un único producer owner por namespace durable y detección de colisión antes de SQX.

## Fuentes usadas

- Baseline `9517f92d00a5be63fb74ce5279991164e957ea1d` y contrato `FEAT-SQX-CROSS-FLOWRUN-REUSE`.

## Resolución aplicada

Se añadió claim atómico PostgreSQL con FKs, consistencia FlowRun/StageExecution, ACK idempotente del mismo owner, conflicto de owner distinto y step `claim_output_namespace` antes de `execute_sqx`.

## Validación

- PASS: worker/core, tests unitarios load-bearing, compilación adapter, vet dirigido y diff check.
- PASS: integración PostgreSQL del ownership pasó, incluyendo la carrera sobre `UNIQUE` real y aplicación de migration 007.
- Degraded suite: `go test ./sqx/adapters/registry-postgres/...` conserva un fallo en `TestUpsertStrategyV2_V0V1V2Coexistence`, fuera del alcance y de los archivos modificados.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

Revertir el commit de esta sesión; no se ejecutaron drops, backfills ni cambios destructivos.
