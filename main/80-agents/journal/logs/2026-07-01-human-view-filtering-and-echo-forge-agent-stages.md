---
type: change_log
scope: session
created: 2026-07-01
updated: 2026-07-01
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[convenciones]]"
  - "[[Echo Forge]]"
  - "[[Destaques de Precio]]"
related:
  - "[[agents-os-tagging-system]]"
  - "[[Panel de Proyectos]]"
aliases: []
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/agentsos
  - change/updated
---

# Vistas humanas sin tareas de agente + etapas Echo Forge como proyectos de agente

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - Etapas Echo Forge → `owner: agent`, movidas a `Echo Forge/agentes/` (Etapas 1-3, Etapa 4, Etapas 5-7, Etapas 8-10). Tareas puente sembradas en Echo Forge con estado real (1-3 `[x]`, 4 `[/]`, 5-7 `[ ]`, 8-10 `[ ]`) más la de echo-forge-wfm.
  - `70-templates/project.md` — board de tareas reescrito: adaptativo por `owner` (humano muestra mías + puentes en columnas por estado; agente muestra tareas del agente), catch de "sin owner", y snippet comentado de rollup de iniciativa (`#owner/me`). Eliminado el Tablero estático redundante.
  - `70-templates/area.md`, `sprint.md`, `quarter.md` — queries de tareas con `tags do not include #owner/agent`. `meeting.md` — action item de ejemplo con `#owner/me`.
  - `80-agents/skills/agents-os-tagging-system/SKILL.md` — `#type/supervision`, sección de ownership de proyecto, regla de vista humana, hard rules y progress log.
  - `10-projects/Destaques de Precio/Destaques de Precio.md` y `Echo Forge/Echo Forge.md` — rollup de iniciativa filtrado a `#owner/me` por subproyecto (fin del flood "todas las tareas al inicio"); Tablero con `tags do not include #owner/agent`.
  - `10-projects/Destaques de Precio/Bajó de Precio.md` — board adaptativo por owner.
  - `00-inbox/Home.md` — Standup sin secciones de agente; muestra mías + puentes + sección "Delegado" (`#type/supervision`) + catch "sin owner".
  - `00-inbox/Hoy.md` — universo de tareas filtra `#owner/agent`.

## Motivo

- El usuario veía tareas de agente mezcladas en Home, Hoy y en rollups de iniciativa (Destaques). Regla nueva: las vistas humanas muestran solo `#owner/me` (incluye puentes `#type/supervision`), nunca `#owner/agent`. Las etapas de Echo Forge eran ejecución de agente y debían modelarse como proyectos de agente con su tarea puente.

## Fuentes usadas

- Decisiones del usuario en la sesión; `convenciones.md`; skill `agents-os-tagging-system`; estado real de proyectos.

## Resolución aplicada

- Board de proyecto adaptativo por `owner`.
- Filtro `tags do not include #owner/agent` en todas las vistas humanas (Home, Hoy, area/sprint/quarter, tableros de proyecto humano).
- Rollups de iniciativa por `#owner/me` agrupado por subproyecto.
- Etapas Echo Forge convertidas a proyectos de agente + puentes con estado real.

## Validación

- Ediciones aplicadas; pendiente confirmar render en Obsidian (dataview/tasks) por el usuario.
- Reindex Graphify ejecutado y query enfocada validada.

## Seguimiento diferido

- Proyectos de agente hoja (Search Middleware, echo-forge-wfm, etapas) conservan el board antiguo de 3 vías, que ya muestra las tareas de agente correctamente; retrofit al board adaptativo es opcional.
- `application.md` mantiene visibilidad completa (incluye tareas de agente) por ser dossier de entidad, no cockpit humano.
