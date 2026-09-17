---
type: change_log
schema_version: 1
scope: session
created: "2026-09-17"
updated: "2026-09-17"
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
application: "[[rio-playmaker]]"
entities:
  - "[[Estandarización de Scopes RIO]]"
  - "[[POC KISS — Routing de scopes en Playmaker]]"
  - "[[rio-playmaker]]"
related:
  - "[[scope-naming-standard]]"
  - "[[SPEC técnica — Routing KISS por scope en rio-playmaker]]"
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

# Corrección — Scope Fury separado de Pipeline Environment

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution + updated
- **Archivo(s):**
  - `10-projects/Meli/Estandarización de Scopes RIO/Estandarización de Scopes RIO.md`
  - `10-projects/Meli/Estandarización de Scopes RIO/agentes/POC KISS — Routing de scopes en Playmaker.md`
  - `10-projects/Meli/Estandarización de Scopes RIO/SPEC técnica — Routing KISS por scope en rio-playmaker.md`
  - `10-projects/Meli/Estandarización de Scopes RIO/agentes/Scopes RIO - Discovery de Integraciones y Persistencia.md`
  - `30-resources/rio-atlas/architecture/scope-naming-standard.md`
  - `80-agents/journal/logs/2026-09-16-rio-scopes-playmaker-poc-plan.md`

## Motivo

- La versión inicial del diseño confundió el scope de infraestructura Fury con el `Environment` funcional del pipeline y propuso persistirlo en `PipelineExecution`. Rodrigo rechazó explícitamente esa equivalencia y fijó que el header nuevo sólo sirve para generar filtros BigQueue.

## Fuentes usadas

- Corrección explícita del owner en sesión del 2026-09-17.
- `rio-playmaker origin/master@f350fb26091d`: headers ya disponibles, dispatch in-memory y producer mqclient existente.
- `rio-sdk-events master@3e3acd1`: envelope de filtros ya disponible sin campo nuevo en payload.

## Resolución aplicada

- Se agregó al inicio del proyecto raíz, planner y SPEC la regla `Pipeline Environment ≠ Fury Scope`.
- Se eliminaron del diseño las migrations, cambios JPA/repository, idempotencia/history scope-aware, validación contra pipeline/runtime y triple match contra ejecución.
- El diseño vigente es `X-Rio-Scope` → carrier in-memory → `filters.modified_fields=["scope:<x>"]`; el result conserva el filtro durante esa request.
- Retry/restart durable queda fuera de la POC y requiere una decisión futura; no se permite resolverlo con persistencia encubierta.
- El funcional fue alineado para distinguir pipeline environment, scope Fury y segmento Fury.

## Validación

- `validate_plan.py`: 4 fases, 4 gates, 4 dispatches, 0 errores y 0 warnings.
- Lint estricto sobre las siete notas afectadas: `ERROR=0 WARN=0`.
- Búsqueda focalizada no encontró afirmaciones vigentes de persistencia/idempotencia/history scope-aware; las apariciones restantes del término descartado son prohibiciones explícitas o el registro histórico invalidado.
- Graphify quedó `fresh`; el título canónico y el alias `POC Playmaker scope alpha` resuelven a una única nota.
- Graphify informó deuda global fuera del delta durante auto-refresh; no bloqueó el índice derivado y no se modificaron notas ajenas.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sólo rutas relativas, SHAs y contratos técnicos; sin secretos, tokens ni payloads productivos.

## Rollback

- Revertir las notas mediante historial del vault sólo si el owner revoca esta separación. No existe código, schema ni infraestructura que revertir.
