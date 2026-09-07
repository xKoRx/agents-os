---
type: session
scope: session
created: "2026-07-01"
updated: "2026-07-01"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
  - "[[Destaques de Precio]]"
  - "[[Echo Forge]]"
related:
  - "[[2026-07-01-agents-os-project-ownership-system-raw]]"
aliases:
  - resumen sistema ownership humano agente
confidence: high
source_session: "[[2026-07-01-agents-os-project-ownership-system-raw]]"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/session
  - scope/session
---

# 2026-07-01 — AGENTS OS: modelo de ownership humano/agente

> [!info]+ Session summary L1
> Resumen operativo. Para beta queda fuera del corpus normal de Graphify.

## Objetivo

- Diseñar y aplicar un sistema de seguimiento que distinga proyectos/tareas humanas de las de agente, sin depender de que una IA recuerde enlazar `parent` manualmente, y sin que las tareas de agente contaminen las vistas humanas (Home, Hoy, rollups de proyecto).

## Contexto cargado

- Bootstrap completo de AGENTS OS: `agents-os.md`, `agent-constitution.md`, `rjara-agent-profile.md`, memoria interna de continuidad.
- `90-system/convenciones.md`, `_shared/metadata-schema.md`, `_shared/note-types.md`, skill `agents-os-vault-refactor`.
- Estado real de proyectos existentes (`10-projects/`), incluyendo el proyecto recién creado sin `parent` que disparó la sesión.

## Trabajo realizado

1. **Modelo de ownership de proyecto** (`owner: me|agent`, `root: true|false` en frontmatter) — nuevo eje que complementa `#owner/me|agent` a nivel tarea.
2. **Tarea puente** (`#type/supervision`): un proyecto de agente se representa en su padre humano con una sola tarea que arranca + sigue el curro delegado.
3. **Carpeta `agentes/`**: los proyectos de agente viven en la subcarpeta `agentes/` de su iniciativa; movidos `Search Middleware…`, `echo-forge-wfm-troubleshooting`, y las 4 etapas de Echo Forge.
4. **Regla anti-huérfano**: subproyectos con `parent` obligatorio; solo iniciativas raíz llevan `root: true`. Cazador de huérfanos/sin-owner en el nuevo dashboard.
5. **Panel de Proyectos** (`90-system/Panel de Proyectos.md`): cockpit de supervisión, vistas agente/humano/huérfanos/sin-owner, enlazado desde Home.
6. **Regla de vista humana**: todo dashboard/board humano excluye `#owner/agent` explícitamente (`tags do not include #owner/agent`); el trabajo delegado se ve solo vía tarea puente. Aplicado a `Home.md`, `Hoy.md`, `area.md`, `sprint.md`, `quarter.md`, y a los rollups de `Destaques de Precio` y `Echo Forge` (que antes mostraban el flood completo de tareas de todos los subproyectos).
7. **Template de proyecto** (`70-templates/project.md`) rehecho: board adaptativo por `owner` (humano → mías + puentes por columna de estado; agente → tareas del agente), snippet de rollup de iniciativa comentado, callout explicando el modelo.
8. **Skill `agents-os-tagging-system`** actualizada con el nuevo tag, el modelo de ownership de proyecto y la regla de vista humana.
9. **AGENTS OS (`agents-os.md`)**: nueva regla obligatoria de creación de proyectos de agente (owner, parent, carpeta, tarea puente sembrada).

## Artifacts creados o modificados

- Ver `80-agents/journal/logs/2026-07-01-project-ownership-human-vs-agent-system.md` y `2026-07-01-human-view-filtering-and-echo-forge-agent-stages.md` para el listado completo de archivos.

## Memoria propuesta o creada

- Decision: modelo de ownership humano/agente + tarea puente (ver `80-agents/memory/public/decision/agents-os/`).
- Learning: las vistas humanas deben excluir `#owner/agent` explícitamente; no basta con no incluirlo (ver `80-agents/memory/public/learning/agents-os/`).

## Decisiones

- Separación por frontmatter + carpetas físicas (`agentes/`), no solo por tag.
- Tag de tarea puente: `#type/supervision`.
- Solo el humano marca la tarea puente como Done; el agente la mueve como máximo a Review.

## Pendiente

- Retrofit opcional del board de 3 columnas en proyectos de agente hoja al nuevo board adaptativo (no bloqueante, ya muestran bien sus tareas).
- El roadmap de `[[AGENTS OS]]` mezcla tareas `#owner/agent` dentro de un proyecto `owner: me` sin tarea puente — deuda pre-existente, flageada para revisión futura, no corregida en esta sesión (fuera de alcance pedido).
- Nueva skill `agents-os-agent-project-workflow` y frontera skill/memoria en `_shared/note-types.md`: pendientes al momento de este resumen, se completan en el mismo cierre.
