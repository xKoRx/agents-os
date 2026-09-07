---
type: change_log
schema_version: 1
scope: session
created: "2026-08-11"
updated: "2026-08-11"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[Onboarding Signals]]"
  - "[[Crear Context]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-08-11-no-mezclar-proyectos-iniciativas-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-11-no-mezclar-proyectos-directiva

## Cambio

- **Tipo:** updated (perfil global) + created (feedback + resource) + reorg (2 proyectos)
- **Archivo(s):**
  - `80-agents/memory/public/user-preference/rjara-agent-profile.md` — nueva directiva `[DURA]` "No mezclar proyectos ni iniciativas" (separar comprensión/onboarding de cambio/delivery; el discovery vive en el proyecto de comprensión; el de cambio arranca cuando el entendimiento está completo; ante duda, preguntar).
  - `80-agents/journal/feedback/system-1/2026-08-11-no-mezclar-proyectos-iniciativas-feedback.md` — feedback del evento.
  - `30-resources/rio-atlas/journeys/deploy-component.md` — **nuevo doc durable** (resource): flujo del contrato de I/O de componente as-is + dolor + evidencia. Conocimiento del sistema (no del proyecto).
  - `30-resources/rio-atlas/00-index.md` — catálogo: `deploy-component` pasa de pendiente a vista activa; "de un vistazo" actualizado.
  - `10-projects/Meli/Crear Context/Crear Context.md` — adelgazado: se removió el as-is/dolor/hallazgos (movidos a resource); queda problema, solución, dependencia y tareas de cambio en `#waiting`.
  - `10-projects/Meli/Onboarding Signals/Onboarding Signals.md` — Atlas 3 en WIP apuntando a [[deploy-component]]; bitácora (7).

## Motivo

- El usuario corrigió que metí discovery/comprensión del flujo (onboarding) dentro del proyecto de cambio [[Crear Context]]. Pidió "aprender" a no mezclar proyectos ni iniciativas, y aclaró el modelo: **documentar en `30-resources/` (durable), no en proyectos** (efímeros).

## Resolución aplicada

- Directiva durable + feedback. Reorg ejecutado: conocimiento del sistema → resource [[deploy-component]]; ambos proyectos vivos, cada uno con su alcance (onboarding = comprensión; Crear Context = cambio, dependiente).

## Validación

- Reindex Graphify tras el cambio.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales ni secretos

## Rollback

- Revertir el bullet en el perfil y borrar la nota de feedback.
