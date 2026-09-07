---
type: learning
scope: global
created: "2026-07-01"
updated: "2026-07-01"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[project-ownership-human-vs-agent]]"
aliases:
  - human views must exclude agent tasks
  - vistas humanas deben excluir tareas de agente
confidence: high
source_session: "[[2026-07-01-agents-os-project-ownership-system-raw]]"
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/global
  - project/agentsos
  - priority/high
---

# Vistas humanas deben excluir `#owner/agent` explícitamente, no por omisión

## Aprendizaje

Cada dashboard/vista/board pensado para el humano (Home, Hoy, área, sprint, quarter, board de un proyecto `owner: me`) debe añadir un filtro explícito `tags do not include #owner/agent` (o su equivalente dataviewjs). No basta con "no incluir" tareas de agente en la query original: en la práctica, queries genéricas como `path includes <carpeta>` o `tags include #area/<slug>` capturan tareas de agente igual, porque viven en el mismo path/área que las humanas. El filtro debe ser positivo y explícito en cada template nuevo, no un supuesto implícito.

## Aplicabilidad

- **Cuándo cargarlo:** al crear o revisar cualquier template/dashboard/rollup que muestre tareas a un humano (`70-templates/*.md`, `90-system/*.md`, `00-inbox/Home.md`, `Hoy.md`).
- **Cuándo no cargarlo:** al construir vistas dentro de un proyecto de agente (`owner: agent`) — ahí la vista correcta muestra las tareas `#owner/agent`, no las excluye. Tampoco aplica a dossiers de entidad (`application.md`) que documentan toda la actividad de una app sin distinguir cockpit humano.

## Entidades relacionadas

- [[AGENTS OS]]
- [[Panel de Proyectos]]

## Evidencia

- Fuente: [[2026-07-01-agents-os-project-ownership-system-raw]].
- Prueba: rollups sin filtro de owner en `Destaques de Precio.md`, `Echo Forge.md` y `Home.md` mostraban tareas `#owner/agent` (reporte directo del usuario); el propio `[[AGENTS OS]]` (que define la regla) tampoco filtraba, y el gap se activó al crear `10-projects/AGENTS OS/agentes/`, cuando `path includes AGENTS OS` empezó a matchear la subcarpeta.
