---
type: change_log
schema_version: 1
scope: session
created: "2026-09-22"
updated: "2026-09-22"
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
application:
entities:
  - "[[RIO]]"
  - "[[rio-playmaker]]"
  - "[[rio-controlplane-flink]]"
  - "[[rio-sdk-events]]"
related:
  - "[[SPEC técnica — Continuidad de scope en control planes RIO]]"
  - "[[SPEC técnica — Routing KISS por scope en rio-playmaker]]"
  - "[[scope-naming-standard]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-22-scopes-rio-runtime-derived-cp-routing

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated / conflict-resolution
- **Archivo(s):**
  - `10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Continuidad de scope en control planes RIO.md`
  - `10-projects/Meli/Estandarización de Scopes RIO/Estandarización de Scopes RIO.md`
  - `30-resources/rio-atlas/architecture/scope-naming-standard.md`

## Motivo

- Alinear la Fase 3 con el diseño vigente de Playmaker: la lane se deduce del scope Fury canónico del runtime y no se transporta desde el header ni se duplica en `expectedScope`.

## Fuentes usadas

- Planner y SPEC técnica de Playmaker, donde `alpha-api-nonprod` y `alpha-consumer-nonprod` resuelven ambos `lane=alpha` desde el primer token.
- Baselines de `rio-sdk-events` y control planes ya verificadas el 2026-09-21 para envelope tipado, controllers y publishers.
- JARs locales `com.fury.toolkit:java-toolkit-shared` 0.2.1–0.5.0 inspeccionados con `jar`/`javap`: exponen `SegmentationUtils.getSegmentId()`, no un accessor de scope.
- JAR local `com.fury:furyutils` 1.0.1 inspeccionado con `javap`: expone `FuryUtils.getEnv(String)`, pendiente de confirmar como API soportada para los CPs.

## Resolución aplicada

- El scope Fury local pasa a ser autoridad y el filtro entrante queda como aserción `incomingLane == runtimeLane`.
- Se eliminan del diseño `expectedScope`, `RoutingContext` y el carrier controller→processor→publisher.
- El publisher resuelve la lane local justo antes de `sendWithFilters`; runtime canónico exige filtro y runtime legacy conserva el flujo sin filtro.
- La API concreta de Fury queda como G0 explícito; no se inventa una clase ni se agrega una dependencia sin validación.
- Los reconciliadores sólo pueden adoptar el patrón cuando el ownership durable impide reclamar trabajo de otra lane.

## Validación

- La SPEC mantiene el payload SDK, pipeline environment, DB y processors sin cambios.
- La matriz de tests cubre happy path, mismatch, missing, malformed, legacy y error del provider.
- Los tres documentos modificados pasan `scripts/lint.py --strict` sin findings.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Restaurar las versiones anteriores de los tres documentos y eliminar este change log; no existen cambios de código ni infraestructura.
