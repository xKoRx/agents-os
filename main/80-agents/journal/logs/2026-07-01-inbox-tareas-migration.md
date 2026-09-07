---
type: change_log
scope: session
created: 2026-07-01
updated: 2026-07-01
area:
project:
application:
entities:
  - "[[Meli]]"
  - "[[Personal]]"
  - "[[Finanzas]]"
  - "[[Casa & Energía]]"
  - "[[Aprendizaje]]"
  - "[[Destaques de Precio]]"
  - "[[Bajó de Precio]]"
  - "[[Bajo y Muy Bajo Precio]]"
  - "[[AGENTS OS]]"
related:
  - "[[agents-os]]"
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Inbox tareas migration

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `00-inbox/tareas.md`
  - `20-areas/Meli.md`
  - `20-areas/Personal.md`
  - `20-areas/Finanzas.md`
  - `20-areas/Casa & Energía.md`
  - `20-areas/Aprendizaje.md`
  - `10-projects/Destaques de Precio/Bajó de Precio.md`
  - `10-projects/Destaques de Precio/Bajo y Muy Bajo Precio.md`
  - `10-projects/AGENTS OS.md`
  - `10-projects/Apagado No Verificado en Recos MDE.md`
  - `10-projects/Postmortem Atributos Polycard.md`
  - `10-projects/Security Guardian.md`
  - `30-resources/ideas/2026-07-01-polycard-single-en-busqueda-por-seller.md`
  - `70-templates/idea.md`
  - `90-system/convenciones.md`
  - `80-agents/skills/_shared/metadata-schema.md`
  - `80-agents/skills/_shared/note-types.md`

## Motivo

- Migrar tareas sueltas desde inbox hacia notas canónicas del Second Brain sin perder pendientes personales ni de Meli.

## Fuentes usadas

- `00-inbox/tareas.md`
- `90-system/convenciones.md`
- Notas canónicas de áreas y proyectos afectados.

## Resolución aplicada

- Se registraron las tareas claras con `#owner/me`, `#type/*` y `#area/*` en sus áreas o proyectos correspondientes.
- Se resolvieron las aclaraciones pendientes recibidas el 2026-07-01.
- Se crearon proyectos chicos para Apagado No Verificado en Recos MDE, Postmortem Atributos Polycard y Security Guardian.
- Se creó una nota de idea/validación para Polycard Single en Búsqueda por Seller bajo `30-resources/ideas/`.
- Se reforzó `70-templates/idea.md` para soportar ideas cortas, ruteadas por área/aplicación, tageadas y promovibles a tarea/proyecto.
- Se declaró `type: idea` y la taxonomía mínima de tags de idea en convenciones/schema para que el flujo sea reutilizable por AGENTS OS.
- Se evitaron duplicados para Bajó de Precio que el usuario confirmó como ya trackeados.
- Se eliminó `00-inbox/tareas.md` después de registrar o descartar todos sus ítems.

## Validación

- Graphify fue reindexado antes de la migración.
- Los ítems ambiguos fueron resueltos con respuesta del usuario.
