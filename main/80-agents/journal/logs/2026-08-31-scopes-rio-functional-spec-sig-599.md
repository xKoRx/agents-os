---
type: change_log
schema_version: 1
scope: session
created: "2026-08-31"
updated: "2026-08-31"
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
application:
entities: []
related:
  - "[[scope-naming-standard]]"
  - "[[scope-compatibility-matrix]]"
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

# 2026-08-31-scopes-rio-functional-spec-sig-599

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `10-projects/Meli/Estandarización de Scopes RIO/Estandarización de Scopes RIO.md` — actualizado con la publicación y las decisiones funcionales vigentes.
  - `80-agents/skills/signals-func-spec-authoring/references/spellbook-access-runbook.md` — corregido para la CLI vigente y su flujo idempotente de verificación.
  - Spellbook `SIG-599` — creado como spec funcional en estado `draft`.

## Motivo

- Publicar una definición entendible por todo Signals para el sistema de ambientes RIO, la selección independiente de frontend/backend y el estándar de scopes, sin convertir el documento funcional en una spec técnica.

## Fuentes usadas

- Estado canónico del proyecto [[Estandarización de Scopes RIO]], [[scope-naming-standard]], [[scope-compatibility-matrix]], Grid narrativo v2 y reglas de authoring funcional de Signals.
- Brainstorm de Grimoire con aprobación explícita del usuario.

## Resolución aplicada

- Se publicó `SIG-599` con MeliLab como selección base, overrides `frontend`/`backend`, default `prod`, dos puntos de entrada de Playmaker, tópicos `nonsite`/`nonprod`, filtros por ambiente, nomenclatura canónica y cardinalidad diferenciada entre testing y producción.
- La spec se dejó en `draft` por solicitud explícita; no se creó spec técnica ni tasks.
- La nota de proyecto conserva como pendientes las verificaciones de plataforma y la implementación.
- El runbook deja de recomendar la API directa: `specs edit --content` preserva backticks en la CLI vigente, y un `create` con respuesta inesperada se resuelve por título exacto antes de cualquier reintento.

## Validación

- Spellbook devolvió `SIG-599` con UUID `d11690fe-cb01-4869-97e9-18addb3d013c`, estado `draft` y contenido idéntico al Markdown aprobado.
- Checklist funcional: root cause, historias, requisitos `RF-N`, criterios `CA-N`, escenarios E2E, impacto cross-app, nomenclatura y ejemplos de precedencia presentes; sin placeholders.
- El flujo CLI `create → edit → view` quedó validado con `@spellbook/cli 1.3.0`; la edición aceptó 14 kB de Markdown con backticks.
- El lint estricto de las notas canónicas del proyecto y este change log pasó sin hallazgos. El runbook es un fragmento de referencia sin frontmatter, igual que sus pares.
- `graphify-obsidian update` quedó bloqueado antes de indexar por 26 errores y 6 warnings de frontmatter preexistentes en fuentes no relacionadas; no se modificaron durante este cierre.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Eliminar `SIG-599` o restaurar una versión anterior desde Spellbook y revertir las líneas de estado añadidas al proyecto.
