---
type: change_log
schema_version: 1
scope: session
created: "2026-08-29"
updated: "2026-08-29"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-08-29-exporter-double-execution-root-cause]]"
  - "[[2026-08-29-durable-verified-reads-exporter-double-execution]]"
aliases: []
confidence: verified
source_session: c6fb690d-88af-4e9d-88d0-f416d9d033e5
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-29-exporter-double-execution-rca

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `80-agents/memory/public/decision/symphony/2026-08-29-exporter-double-execution-root-cause.md` (creado)
  - `80-agents/memory/public/known-error/symphony/2026-08-29-durable-verified-reads-exporter-double-execution.md` (actualizado: diagnóstico RESUELTO)
  - `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md` (checkpoint RCA)
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md` (bullet de fase activa)

## Motivo

El known-error del 2026-08-29 afirmaba una «subida fantasma sin `ActivityTaskStarted`» y `attempt=1`. Ambas afirmaciones resultaron incorrectas y habrían dirigido el fix hacia infraestructura en vez del defecto de producto.

## Fuentes usadas

- Historial Temporal completo (41 eventos, página única) y metadatos + cuerpo del objeto MinIO, recuperados del rollout local de la sesión ZCode previa.
- Lectura de `generic_workflow.go`, `project_activity.go`, `steps.go`, `write_once.go`, `durable_artifacts.go`, `adapter.go` (Mongo) y `EchoForgeOverviewExporter.java` en `xKoRx/symphony`.
- Semántica documentada de escritura perezosa de `ActivityTaskStarted` en Temporal.

## Resolución aplicada

Se sustituyó el diagnóstico abierto por la causa raíz demostrada (tarea no durable con artefactos byte-no-deterministas por construcción) y se corrigieron las dos afirmaciones inválidas. El known-error queda enlazado a la decisión.

## Validación

- Cadena de atribución del primer PUT cerrada por cinco vías independientes (metadatos, cuerpo, cardinalidad de la config, cronología, confinamiento de `GetInfo`).
- Igualdad de tamaño entre ambos artefactos probada por la clase de error (`checksum mismatch`, no size mismatch).
- Sin acceso al laboratorio: no fue posible verificar host del primer intento ni Mongo del run. Registrado como límite explícito.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir los cuatro archivos a su estado previo restaura el diagnóstico abierto; el RCA quedaría sin registro.
