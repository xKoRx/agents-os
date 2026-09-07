---
type: change_log
schema_version: 1
scope: session
created: "2026-08-10"
updated: "2026-08-10"
area: "[[Meli]]"
project: "[[Onboarding Signals]]"
application:
entities:
  - "[[RIO]]"
related:
  - "[[AGENTS OS - Fase 3]]"
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

# 2026-08-10-rio-atlas-and-coupling

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated (entidad Sistema 2) + created (derivados no-conformes, en cuarentena)
- **Archivo(s):**
  - `30-resources/applications/RIO.md` — corregido el "Flujo de control": los triggers Playmaker→control planes van por **HTTP POST** (BigQueue sólo fallback V1), results/status por BigQueue async; Materializer por REST + Fury Streams. Añadido link a [[00-index|RIO Atlas]].
  - `30-resources/rio-atlas/{00-index, architecture/system-map, architecture/integration-map}.md` y `30-resources/rio-atlas/rio-inspector.md` — **re-materializados vía `agents-os-entity-lifecycle`** con tipos correctos (`index`, `resource`×2, `tool`) y `lint --strict` en verde (ERROR=0). Sustituyen la primera versión no conforme (`type: reference`). Descubribles por bootstrap (aliases: "RIO Atlas", "RIO System Map", "RIO Integration Map", "rio-inspector").
  - `10-projects/Meli/Onboarding Signals/Onboarding Signals.md` — backlog re-priorizado a Atlas; bitácora/decisiones/progreso (60%).
  - `10-projects/Personal/AGENTS OS/agentes/AGENTS OS - Fase 3.md` — idea preventiva (shift-left del gate).
  - `~/fuentes/rio-inspector/inspect.py` (fuera del vault) — corregido para emitir [[integration-map]] como nota `resource` conforme y escribirla directo al vault (idempotente, preserva `created`, pasa `lint --strict`); crudos json/mmd quedan en `~/fuentes`. Cierra la deuda de drift del generador.

## Motivo

- El Integration Map generado desde config reveló que el modelo previo (triggers vía BigQueue) era impreciso; corregir la entidad canónica evita propagar el error.

## Fuentes usadas

- `~/fuentes/*/src/main/resources/application*.yml` (comentarios PRODUCER/CONSUMER + "pushed via HTTP POST"); `~/fuentes/rio-inspector/rio-integrations.json`.

## Resolución aplicada

- Corrección directa en [[RIO]] con evidencia citada; derivados del Atlas dejados en cuarentena para remediación conforme (no se forzó su ingreso al corpus).

## Validación

- El gate fail-closed frenó las 3 notas no conformes antes del reindex (comportamiento esperado, Fase 3). [[RIO]] sigue conforme.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales de máquina, memoria interna ni secretos

## Rollback

- Revertir el bullet "Flujo de control" de `RIO.md` a la versión previa; borrar `30-resources/rio-atlas/` si se descarta el Atlas.
