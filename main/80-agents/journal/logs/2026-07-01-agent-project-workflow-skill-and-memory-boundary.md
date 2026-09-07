---
type: change_log
scope: session
created: 2026-07-01
updated: 2026-07-01
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[project-ownership-human-vs-agent]]"
aliases: []
confidence: verified
source_session: "[[2026-07-01-agents-os-project-ownership-system-raw]]"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - project/agentsos
  - change/created
---

# Skill agents-os-agent-project-workflow + frontera skill/memoria + proactividad

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `80-agents/skills/agents-os-agent-project-workflow/SKILL.md` (nueva).
  - `80-agents/skills/INDEX.md` — registrada la skill nueva en el catálogo.
  - `80-agents/agents-os/agents-os.md` — referenciada en la lista de skills lazy y en la regla de proyectos humanos vs de agente.
  - `90-system/convenciones.md` — enlace a la skill desde la sección "Proyectos humanos vs proyectos de agente".
  - `80-agents/skills/_shared/note-types.md` — nueva sección "Skill vs Reusable Memory (Learning/Decision/Known Error/Runbook)"; Sistema 1 ahora menciona explícitamente skills.
  - `80-agents/memory/public/constitution/agent-constitution.md` — puntos 4 y 5 en "Evolución y Aprendizaje de Skills": proactividad obligatoria en checkpoints naturales, y no mezclar skill con aprendizaje/memoria.

## Motivo

- El usuario pidió documentar explícitamente cómo un agente debe abordar un proyecto de agente (planificador único, ciclo de tarea puente WIP/Review/rechazo) para resiliencia ante pérdida de sesión, y separar en la documentación de Sistema 1 la diferencia entre skill (habilidad) y aprendizaje/memoria, exigiendo proactividad de los agentes en mantener ambos actualizados.

## Fuentes usadas

- Instrucción directa del usuario en esta sesión; estructura existente de `note-types.md`, `agent-constitution.md` y el catálogo de skills.

## Resolución aplicada

- Nueva skill con procedimiento explícito de 5 pasos (inicio, ejecución, cierre para revisión, rechazo, cierre proporcional) y una sección "Judgment Calls Registrados" que deja explícitas las decisiones no completamente especificadas por el usuario (solo el humano cierra la tarea puente; distinción cierre liviano/completo; recomendación no obligatoria de planificador único también para proyectos humanos).
- Frontera skill/memoria documentada con regla de bolsillo (repetible + invocado a demanda = skill; hecho/conclusión pasiva = aprendizaje/decisión/known-error; comando mecánico validado = runbook).
- Constitución actualizada con mandato explícito de proactividad y de no mezclar tipos, sin remover contenido existente.

## Validación

- Reindex de Graphify pendiente de ejecutar inmediatamente después de este log (mismo cierre).
