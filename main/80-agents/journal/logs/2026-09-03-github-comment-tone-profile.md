---
type: change_log
schema_version: 1
scope: session
created: "2026-09-03"
updated: "2026-09-03"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[rjara-agent-profile]]"
  - "[[human-first-technical-writing]]"
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

# 2026-09-03 — tono profesional obligatorio en comentarios de GitHub

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `80-agents/memory/public/user-preference/rjara-agent-profile.md`

## Motivo

El usuario pidió persistir como preferencia crítica que cualquier comentario de GitHub escrito en su nombre mantenga un tono preciso, conciso, clarificador, cordial, amigable y profesional. Indicó explícitamente que un tono confrontacional puede producirle un riesgo laboral.

## Fuentes usadas

- Instrucción explícita del usuario en la sesión de [[Crear Context]].
- Procedimiento canónico [[human-first-technical-writing]].

## Resolución aplicada

- Se agregó una directiva `[DURA]` global al perfil always-load.
- La directiva exige usar [[human-first-technical-writing]], auditar el tono antes de publicar y excluir formulaciones confrontacionales, defensivas, despectivas o excesivamente coloquiales.
- Para desacuerdos técnicos, se fijó la secuencia constructiva: reconocer el punto, comunicar la decisión y la evidencia, explicar brevemente el alcance y separar pendientes de forma neutral.
- La corrección inmediata se aplicó a los 15 comentarios propios existentes en los threads del PR #1068, incluidos los 14 replies y el comentario inicial sobre `sensitive`.

## Validación

- Búsqueda enfocada y consulta Graphify confirmaron que no existía una directiva equivalente en el perfil global.
- Se verificó por API que los 15 comentarios propios del PR #1068 quedaron actualizados y que ya no contienen las formulaciones confrontacionales detectadas.
- El perfil conserva `load_policy: always`, `indexable: true` e `index_priority: critical`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** contiene una preferencia personal y no se clasifica para uso compartido.

## Rollback

- Eliminar la directiva nueva y el link a [[human-first-technical-writing]] del perfil. Los comentarios remotos requieren una edición explícita adicional si se quisiera restaurar sus versiones anteriores.
