---
type: decision
scope: global
created: "2026-07-01"
updated: "2026-07-01"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-tagging-system]]"
  - "[[agents-os-agent-project-workflow]]"
aliases:
  - project ownership model
  - human vs agent project ownership
  - bridge task decision
confidence: verified
source_session: "[[2026-07-01-agents-os-project-ownership-system-raw]]"
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/global
  - project/agentsos
  - priority/high
---

# Ownership de proyecto: humano vs agente + tarea puente

## Contexto

El vault mezclaba proyectos y tareas propios del usuario con proyectos/tareas ejecutados por agentes, sin ningún campo que distinguiera quién conduce la ejecución a nivel **proyecto** (solo existía `#owner/me`/`#owner/agent` a nivel tarea). Consecuencias observadas: un proyecto de agente recién creado quedó sin `parent`; varios proyectos flotaban sin padre (huérfanos); los rollups de iniciativa (ej. `[[Destaques de Precio]]`, `[[Echo Forge]]`) mostraban el flood completo de tareas de todos los subproyectos, incluidas las de agente, al inicio de la nota.

## Decisión

1. Añadir `owner: me|agent` y `root: true|false` al frontmatter de todo proyecto (Sistema 2).
2. Un proyecto de agente (`owner: agent`) vive en la subcarpeta `agentes/` de su iniciativa y siempre tiene `parent` hacia un proyecto humano.
3. El proyecto de agente se representa en su padre humano con **una sola tarea puente** (`#owner/me #type/supervision`), no con sus tareas internas expuestas.
4. Toda vista/dashboard humano (Home, Hoy, area/sprint/quarter, boards de proyecto humano) excluye explícitamente `#owner/agent` (`tags do not include #owner/agent`).
5. El ciclo de la tarea puente es `[ ] → [/] → [r]`, avanzado por el agente; solo el humano la marca `[x]` (Done) tras aceptar la entrega. Detalle operativo en `[[agents-os-agent-project-workflow]]`.

## Rationale

- Separar "quién conduce" a nivel proyecto (no solo tarea) permite dashboards agregados (ej. `[[Panel de Proyectos]]`) sin tener que inspeccionar cada tarea individual.
- La tarea puente evita que el cockpit humano se inunde con el detalle de ejecución delegada, preservando trazabilidad (un click en la puente lleva al proyecto de agente completo).
- Carpeta física `agentes/` da separación visual en el file tree sin romper links de Obsidian (que resuelven por nombre, no por path).
- Que solo el humano cierre la tarea puente preserva la semántica de "puente": el agente arranca y sigue, el humano decide cuándo el curro delegado está realmente terminado.

## Consecuencias

- Todo proyecto existente requirió un barrido de `owner`/`root` (ver `80-agents/journal/logs/2026-07-01-project-ownership-human-vs-agent-system.md`).
- Los templates de proyecto y de vistas humanas (`area`, `sprint`, `quarter`) requieren mantenimiento paralelo si se agregan más vistas nuevas — deben heredar el filtro `tags do not include #owner/agent` por defecto (ver aprendizaje relacionado).
- **Resuelto 2026-07-01**: el roadmap de `[[AGENTS OS]]` mismo mezclaba tareas `#owner/agent` dentro de un proyecto `owner: me` sin tarea puente. Se migró de forma acotada — solo la ejecución abierta (Fase 5 completa + el ítem pendiente de watcher de Fase 6) pasó al proyecto de agente `[[AGENTS OS - Beta y Hardening]]` bajo `10-projects/AGENTS OS/agentes/`, con su tarea puente sembrada en el padre. El roadmap histórico ya cerrado (Fases 0-4 y el resto de Fase 6) se dejó como registro de diseño en el proyecto padre por no ser ejecución activa que requiera supervisión — ver judgment call en `80-agents/journal/logs/2026-07-01-agents-os-self-migration-agent-project.md`. De paso se detectó y corrigió que el Tablero final de `[[AGENTS OS]]` no tenía el filtro `tags do not include #owner/agent` que sí tienen otros proyectos humanos (ej. `[[Echo Forge]]`).

## Alternativas descartadas

- Solo tag a nivel tarea (`#owner/agent`) sin campo de proyecto: insuficiente para dashboards agregados y no resolvía el problema de huérfanos.
- Separación solo por tag sin carpeta física: el usuario pidió explícitamente frontmatter + carpetas para claridad visual en el file tree.
- Permitir que el agente cierre (`[x]`) su propia tarea puente: rompe la semántica de aceptación humana y elimina el punto de control de calidad.
