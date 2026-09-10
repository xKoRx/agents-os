---
type: known_error
schema_version: 1
scope: application
created: "2026-08-27"
updated: "2026-08-27"
area: "[[Meli]]"
project: "[[Playmaker — Doble dispatch al avanzar batches]]"
application: "[[rio-playmaker]]"
entities:
  - "[[Playmaker — Doble dispatch al avanzar batches]]"
related:
  - "[[Descripción PR — rio-playmaker — Hotfix doble dispatch]]"
aliases:
  - QKVS version 0 no es CAS en Playmaker
  - QKVS create-only batch listener
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - area/meli
  - app/rio-playmaker
---

# QKVS `save(version=0)` no garantiza create-only en el flujo de Playmaker

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- Dos listeners concurrentes intentan adquirir la misma llave con `save(version=0)` y ambos continúan como ganadores, por lo que el batch siguiente puede materializarse dos veces.

## Causa

- En el camino concreto del SDK QKVS usado por `rio-playmaker`, `save(version=0)` no se comportó como una operación create-if-absent/CAS atómica. La versión inicial del payload no equivale por sí sola a exclusión mutua del backend.

## Impacto

- Un mutex construido sobre esa suposición permite dos secciones críticas simultáneas y no protege contra deployments duplicados.

## Detección

- Ejecutar una prueba concurrente determinística contra el primitive real o un contrato de integración que obligue a que exactamente un contendiente gane. Los mocks que sólo simulan conflicto no acreditan la semántica del backend.

## Mitigación

- No usar `save(version=0)` como lock sin una garantía create-only documentada y validada contra el backend/SDK exactos. Para el hotfix del PR #1079, serializar sobre la fila existente de `pipeline_execution` con `PESSIMISTIC_WRITE`, releer bajo el lock y mantener idempotencia por materialización.

## Evidencia

- El enfoque QKVS fue retirado de `feature/serialize-batch-completed-listener`; el commit final `f7d4f4881` y los tests de comportamiento prueban 2 dispatches sin exclusión y exactamente 1 con el row lock.
- Contexto y límites: [[Playmaker — Doble dispatch al avanzar batches]] y [[Descripción PR — rio-playmaker — Hotfix doble dispatch]].
