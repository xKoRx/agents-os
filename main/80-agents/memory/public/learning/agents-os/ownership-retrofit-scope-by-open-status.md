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
  - "[[AGENTS OS - Beta y Hardening]]"
related:
  - "[[project-ownership-human-vs-agent]]"
  - "[[agents-os-agent-project-workflow]]"
  - "[[agents-os-vault-refactor]]"
aliases:
  - ownership retrofit scope
  - alcance de migración retroactiva de ownership
confidence: high
source_session: "[[2026-07-01-agents-os-self-migration-agent-project-raw-session]]"
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/global
  - project/agentsos
  - priority/high
---

# Al retrofitear ownership sobre un proyecto viejo, migrar solo tareas abiertas — el historial cerrado se queda

## Aprendizaje

Cuando un proyecto humano (`owner: me`) preexistente tiene tareas `#owner/agent` sueltas mezcladas en su roadmap sin proyecto de agente ni tarea puente (deuda pre-modelo de ownership), no conviene migrar retroactivamente **todo** el roadmap histórico a un proyecto de agente separado. El criterio correcto es migrar solo la **ejecución abierta** (tareas `[ ]`/`[/]`/`[r]` sin cerrar): eso es lo único que realmente necesita supervisión vía tarea puente y planificador resiliente a pérdida de sesión. Las tareas ya `[x]` cerradas son registro histórico de diseño, no ejecución activa — migrarlas fragmenta la narrativa del proyecto padre sin ninguna ganancia operativa, porque tareas cerradas no ensucian los boards To Do/WIP/Review (se filtran por estado) y el único punto donde sí podían aparecer sin filtrar (el Tablero del propio proyecto) se corrige agregando el filtro `tags do not include #owner/agent`, no moviendo el historial.

## Aplicabilidad

- **Cuándo cargarlo:** al encontrar un proyecto humano viejo con tareas `#owner/agent` sin tarea puente ni proyecto de agente (deuda de retrofit del modelo de ownership), antes de decidir el alcance de la migración.
- **Cuándo no cargarlo:** al crear un proyecto de agente nuevo desde cero (ahí no hay historial que evaluar, todo el trabajo es ejecución abierta) — usar directo `[[agents-os-agent-project-workflow]]`.

## Entidades relacionadas

- [[AGENTS OS]]
- [[AGENTS OS - Beta y Hardening]]
- [[project-ownership-human-vs-agent]]

## Evidencia

- Fuente: `80-agents/journal/logs/2026-07-01-agents-os-self-migration-agent-project.md`.
- Prueba: en `[[AGENTS OS]]` se migró solo la ejecución abierta (Fase 5 + pendiente de Fase 6) a `[[AGENTS OS - Beta y Hardening]]`; Fases 0-4 y el resto de Fase 6 (todas `[x]`) quedaron como historial en el proyecto padre.
