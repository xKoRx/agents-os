---
type: change_log
schema_version: 1
scope: session
created: "2026-10-27"
updated: "2026-10-27"
area: "[[Meli]]"
project: "[[SIG-659 — Discovery & CLI]]"
application: "[[rio-playmaker]]"
entities:
  - "[[SIG-659 — Discovery & CLI]]"
related:
  - "[[rio-sdk-events]]"
  - "[[rio-controlplane-kafka]]"
  - "[[RIO]]"
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

# 2026-10-27-sig-659-rio-bus-transport

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Meli/SIG-659 — Discovery & CLI/SIG-659 — Discovery & CLI.md`

## Motivo

- El owner arranca el transporte del P0 (Discovery como primer cliente de un mecanismo de mensajería agnóstico playmaker ↔ CP) y pidió dejar en el proyecto lo que se va a hacer, con una propuesta de solución.

## Fuentes usadas

- Spellbook: SIG-635, SIG-644, SIG-671, SIG-697 y SIG-699 leídas por CLI; búsqueda de una spec de transporte sin resultados.
- Código en refs remotas: `rio-playmaker@origin/develop 0c0e319c9`, `rio-sdk-events@origin/master b928149` y ramas `discovery-v2-0*`, `rio-controlplane-kafka@origin/develop f4b5701`.
- RAG `dev-training-ue` (capacitación Fury de BigQueue): filtros habilitados por tópico, ack por HTTP 200 y reintento hasta TTL.

## Resolución aplicada

- Estado actual, próximo paso, sección nueva "🚌 Transporte — RIO Bus" (hechos de código, propuesta, decisiones T-1 a T-5), tareas `F1·bus`, fila del SDK en la tabla de entrega, bitácora y decisión de reparto.

## Validación

- `lint.py --strict` sobre la nota del proyecto.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir la nota del proyecto a su contenido del 2026-10-22 (sección del transporte, tareas `F1·bus` y entradas del 2026-10-27). 
