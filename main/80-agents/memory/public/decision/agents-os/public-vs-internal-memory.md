---
type: decision
scope: project
created: 2026-06-27
updated: 2026-06-27
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agent-constitution]]"
  - "[[agent-constitution]]"
  - "[[agents-os-behavior-config]]"
aliases:
  - memoria publica vs memoria interna
  - public memory vs internal memory
  - Agent Memory System memory boundary ADR
confidence: verified
source_session:
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - area/personal
  - kind/decision
  - priority/high
  - project/agents-os
  - project/agentsos
  - scope/project
---
# Public vs Internal Memory Boundary

## Contexto

- Agent Memory System necesita memoria reutilizable para futuros agentes sin convertir cada conversacion en documentacion publica.
- El vault usa Sistema 2 para entidades reales y Sistema 1 para memoria del agente.
- La memoria interna existe para continuidad operativa del agente, pero no debe reemplazar memoria publica, ADRs, entidades canonicas ni logs auditables.

## Decisión

- Mantener dos espacios separados bajo `80-agents/memory/`:
  - `public/`: memoria compartida, auditable, legible por humanos y agentes, indexable para retrieval normal.
  - `internal/`: memoria exclusiva del agente, usada para heuristicas, hipotesis, planes, continuidad y comunicacion entre agentes.
- La memoria publica requiere estructura estable, links a entidades, confianza suficiente y log auditable cuando se crea, edita, reemplaza o elimina.
- La memoria interna es gobernada por el agente, no requiere validacion humana rutinaria y no se expone al usuario por defecto.
- Una nota interna solo se promueve a memoria publica cuando debe afectar el sistema compartido; esa promocion debe dejar log auditable.

## Rationale

- Separar espacios evita contaminar entidades canonicas con progreso de sesion o razonamiento privado.
- La memoria publica permite retrieval confiable y auditoria cuando cambia comportamiento compartido.
- La memoria interna permite continuidad cognitiva sin obligar al usuario a revisar pensamientos operativos del agente.
- El modelo conserva Markdown como fuente de verdad y Graphify como indice derivado.

## Consecuencias

- Los agentes deben cargar memoria publica always-load y memoria interna compacta segun `load_policy`.
- Cambios a memoria publica, constitucion, perfil de usuario o Sistema 2 deben registrar `type: change_log`.
- Cambios internos no requieren log publico salvo que se promuevan o modifiquen una fuente compartida.
- Las skills deben clasificar instrucciones y aprendizajes antes de persistirlos.

## Alternativas descartadas

- Guardar todo como memoria publica: aumenta ruido, costo de retrieval y carga de auditoria.
- Guardar todo como memoria interna: reduce transparencia y rompe la fuente compartida de verdad.
- Mezclar memorias en entidades Sistema 2: convierte documentacion canonica en diario de sesiones.
- Usar raw sessions como memoria primaria: conserva auditoria, pero es demasiado caro y poco preciso para retrieval normal.
