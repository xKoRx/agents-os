---
type: change_log
schema_version: 1
scope: session
created: "2026-09-16"
updated: "2026-09-16"
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
application:
entities:
  - "[[Estandarización de Scopes RIO]]"
related:
  - "[[ads-signals-frontend]]"
  - "[[rio-playmaker]]"
  - "[[rio-sdk-events]]"
  - "[[rio-controlplane-flink]]"
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

# Estandarización de Scopes RIO — planificación de POC alpha

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Meli/Estandarización de Scopes RIO/Estandarización de Scopes RIO.md`

## Motivo

- Incorporar al proyecto canónico la planificación de la segunda fase: una POC end-to-end de deploy sobre `alpha`, con límites claros y separación futura por SPEC técnica.

## Fuentes usadas

- Proyecto canónico, discovery de integraciones, matriz de compatibilidad, snapshot Fury del 2026-09-03 y revisión read-only de las ramas locales vigentes de `ads-signals-frontend`, `rio-playmaker`, `rio-sdk-events` y `rio-controlplane-flink`.

## Resolución aplicada

- Se acotó la POC a deploys con Flink, se eliminó el header custom como requisito, se fijó que MeliLab/query params pertenecen al front, se adoptó el filtro BigQueue `scope:alpha` como capability disponible, se mantuvieron los topics de deployment y se separó el trabajo en cinco futuras SPECs técnicas más un runbook de integración. Tras el review KISS/YAGNI se eliminó la columna redundante de gates y se limitó Playmaker al producer del golden path pipeline, conservando el legacy sólo por compatibilidad.

## Validación

- Se verificó que el proyecto contiene topología, decisiones, fases, criterios de aceptación, rollout, rollback y tareas independientes para SDK, Front, Playmaker, Flink, Infra Fury y el runbook de integración.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir la sección `POC alpha end-to-end`, las tareas POC y las decisiones del 2026-09-16 si el equipo cambia el CP piloto o amplía la cobertura más allá de deploys antes de aprobar las SPECs técnicas.
