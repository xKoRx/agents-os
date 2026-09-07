---
type: change_log
scope: project
created: 2026-06-27
updated: 2026-06-27
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
  - "[[agent-constitution]]"
related:
  - "[[agents-os-behavior-config]]"
  - "[[public-vs-internal-memory]]"
aliases:
  - agent constitution commandments updated
  - mandamientos AGENTS OS endurecidos
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - area/personal
  - kind/changelog
  - project/agents-os
  - project/agentsos
  - scope/project
---
# Agent Constitution Commandments Updated

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `80-agents/memory/public/constitution/agent-constitution.md`
  - `10-projects/AGENTS OS.md`

## Motivo

- El usuario indicó que los mandamientos existentes eran blandos y no representaban el uso real descrito por el proyecto.
- Los mandamientos estaban centrados casi exclusivamente en memoria interna, dejando fuera reglas operativas clave: bootstrap, Graphify, separación Capa 1/Capa 2, logging, cierre, higiene y seguridad.

## Fuentes usadas

- `10-projects/AGENTS OS.md`
- `80-agents/agents-os/agents-os.md`
- `80-agents/memory/public/constitution/agent-constitution.md`
- `80-agents/memory/public/user-preference/rjara-agent-profile.md`
- `80-agents/memory/public/decision/agents-os/public-vs-internal-memory.md`
- `80-agents/skills/agents-os-behavior-config/SKILL.md`

## Resolución aplicada

- Se reemplazó el bloque de mandamientos centrado en memoria interna por mandamientos explícitos de uso del AGENTS OS.
- Se mantuvo la regla de memoria interna como parte del flujo completo, pero ya no como el único eje de la constitución.
- Se actualizó la bitácora del proyecto para reflejar el endurecimiento de la constitución.
- Se reforzó explícitamente que la memoria interna la gobierna el agente y puede usarla como estime conveniente: estructura, reglas, nombres, formatos, criterios de carga, planes, hipótesis, heurísticas, advertencias y mensajes a futuros agentes.

## Validación

- Cambio aplicado directamente sobre la constitución `load_policy: always`.
- Se creó este log auditable porque la constitución y el documento de control del proyecto son memoria pública/canónica.
- Se ejecutó `graphify-obsidian update`; salida viva validada en `95-graphify/obsidian/GRAPH_REPORT.md` con 738 nodos, 651 edges y 87 comunidades.
- `graphify-obsidian explain "Agent Constitution"` recuperó `80-agents/memory/public/constitution/agent-constitution.md` y el nodo `Mandamientos de uso del AGENTS OS`.
- `graphify-obsidian query "AGENTS OS mandamientos uso constitucion" --budget 1200` recuperó la constitución y el nodo de mandamientos desde la salida viva.
- `graphify-obsidian explain "Regla explícita de memoria interna"` recuperó `80-agents/memory/public/constitution/agent-constitution.md` línea 69.
