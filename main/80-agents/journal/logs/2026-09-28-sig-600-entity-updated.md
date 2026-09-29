---
type: change_log
schema_version: 1
scope: session
created: "2026-09-28"
updated: "2026-09-28"
area: "[[Meli]]"
project: "[[SIG-600 — Borrado seguro de Data Products]]"
application:
entities:
  - "[[SIG-600 — Borrado seguro de Data Products]]"
related:
  - "[[rio-playmaker]]"
  - "[[ads-signals-frontend]]"
aliases:
  - Corrección de estado SIG-600 y SIG-643
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
  - area/meli
---

# 2026-09-28-sig-600-entity-updated

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Meli/SIG-600 — Borrado seguro de Data Products/SIG-600 — Borrado seguro de Data Products.md`

## Motivo

- Corregir el registro del proyecto tras restaurar SIG-600 a su contenido original.

## Fuentes usadas

- [SIG-600](https://spellbook.adminml.com/projects/SIG/specs/SIG-600) y [SIG-643](https://spellbook.adminml.com/projects/SIG/specs/SIG-643), releídos tras la edición; baseline de `rio-playmaker` y `ads-signals-frontend`.

## Resolución aplicada

- **Antes:** el proyecto afirmaba erróneamente que CA-1 y los permisos de ambas SPECs estaban alineados.
- **Ahora:** registra que SIG-600 volvió a su versión original y que la discrepancia con SIG-643 sigue abierta. Mantiene el relevamiento de rutas de deploy antes de `ready_to_code`.
- Es verdad actual del proyecto y modifica sus tareas y decisiones; no es memoria reusable de Sistema 1.

## Validación

- El contenido de SIG-600 se comparó con la copia obtenida antes de editar y coincidió exactamente (7360 caracteres). La nota del proyecto vuelve a reflejar la discrepancia entre SIG-600 y SIG-643.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos ni datos de memoria interna.

## Rollback

- Restaurar la versión previa del proyecto desde backup/versionado del vault si la actualización fuese incorrecta; conservar el historial remoto de Spellbook.
