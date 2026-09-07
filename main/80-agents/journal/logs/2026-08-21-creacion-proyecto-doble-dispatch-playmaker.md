---
type: change_log
schema_version: 1
scope: session
created: "2026-08-21"
updated: "2026-08-21"
area: "[[Meli]]"
project: "[[Playmaker — Doble dispatch al avanzar batches]]"
application: "[[rio-playmaker]]"
entities:
  - "[[Playmaker — Doble dispatch al avanzar batches]]"
  - "[[Prompt maestro — Auditoría independiente del doble dispatch]]"
related:
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

# Creación del proyecto de doble dispatch de Playmaker

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `10-projects/Meli/Playmaker — Doble dispatch al avanzar batches/Playmaker — Doble dispatch al avanzar batches.md`
  - `10-projects/Meli/Playmaker — Doble dispatch al avanzar batches/Prompt maestro — Auditoría independiente del doble dispatch.md`

## Motivo

- Crear una fuente durable y específica para investigar el incidente de dos deployments activos del mismo service durante el avance de batches.
- Entregar un prompt reutilizable que obligue a investigar fuentes primarias antes de contrastar con el diagnóstico existente.

## Fuentes usadas

- Datos de deployments, pipeline execution, deployment group y component runs entregados por el usuario.
- Stacktrace adjunto del incidente.
- Código y tests de `rio-playmaker` en `develop`, snapshot `0524ce49ef34`.
- Historial Git y refs locales, incluyendo `dac615f47` y `adf5cf54f`.
- `meli/backlog.md`, deudas `DEBT-SIG186-CONCURRENT-DEACTIVATE` y `DEBT-SIG326-DISPATCH-ACTIVE-RACE`.

## Resolución aplicada

- Proyecto raíz humano `owner: me`, P1, enlazado a [[rio-playmaker]].
- Diagnóstico previo separado conceptualmente de la auditoría independiente pendiente.
- Prompt canónico con checkpoint inmutable de fase 1 antes de permitir la lectura de la nota de contraste.
- No se modificó el repositorio de Playmaker ni se realizaron operaciones sobre DB.

## Validación

- Contrato de schemas validado antes de materializar.
- Notas creadas desde templates canónicos `project`, `prompt` y `change_log`.
- `lint.py --strict` sobre las tres notas: `ERROR=0 WARN=0`.
- `graphify-obsidian update` fue ejecutado, pero el gate global quedó `NO-GO` por una deuda ajena: `10-projects/Meli/Crear Context/SPEC Tecnica — Context IO.md` no contiene la sección requerida `## Contenido`.
- La reindexación y validación por título/alias quedan pendientes hasta resolver esa nota fuera de alcance; no se modificó para evitar mezclar proyectos.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** contiene rutas locales deliberadamente porque el prompt se ejecutará en este workspace; no contiene credenciales ni secretos. La evidencia técnica del incidente permanece local.

## Rollback

- Eliminar las dos notas creadas y este change log si el usuario decide descartar completamente la iniciativa. No hay rollback sobre código o DB porque no fueron modificados.
