---
type: decision
scope: global
created: 2026-07-23
updated: 2026-07-23
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
  - "[[Echo Forge - Cierre de Etapa 4]]"
related:
  - "[[project-ownership-human-vs-agent]]"
aliases:
  - Planner-Executor Implementation Standard
  - estándar de planificación delegada
  - high-capability planner low-cost executor
confidence: verified
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/decision
  - action/implementation-planning
  - project/agents-os
  - scope/global
---

# Planner-Executor Implementation Standard

## Contexto

- Los trabajos complejos se planifican con un agente de alta capacidad, pero su implementación puede distribuirse entre agentes más rápidos y económicos.
- Un roadmap resumido obliga al ejecutor a redescubrir arquitectura, completar contratos e inventar semántica, anulando el ahorro y aumentando alucinaciones.

## Decisión

- El planificador deja el trabajo completo en un proyecto `owner: agent`, dividido en fases autónomas, balanceadas y gateadas.
- Cada fase contiene referencias verificadas, decisiones cerradas, pasos, archivos/símbolos, límites, tests, evidencia y handoff.
- Cada fase se ejecuta en un contexto nuevo; el owner acepta su gate antes de habilitar la siguiente.
- El procedimiento canónico vive en `80-agents/skills/agents-os-implementation-planning/SKILL.md`.

## Rationale

- Concentrar investigación y decisiones en una planificación de alta calidad reduce redescubrimiento, deriva semántica y uso repetido de modelos costosos.
- El gate por fase limita el blast radius y permite validar evidencia antes de acumular errores.

## Consecuencias

- La planificación inicial es más extensa y debe verificar referencias contra el estado real del repositorio.
- Los ejecutores reciben una sola fase y no deciden requisitos de negocio.
- Las capacidades técnicas desconocidas se resuelven mediante spikes explícitos, no suposiciones.
- El proyecto de agente permanece como fuente única durante implementación y revisión.

## Alternativas descartadas

- Un solo agente para planificar e implementar todo: agota contexto y dificulta validación incremental.
- Fases descritas solo con objetivos: desplaza investigación y decisiones al ejecutor.
- Mantener el plan únicamente en el chat: rompe continuidad y auditabilidad.
