---
type: agent_memory
schema_version: 1
scope: project
created: "2026-09-12"
updated: "2026-09-12"
area: "[[Aranea]]"
project:
application:
entities: ["[[Echo]]", "[[Echo Forge]]", "[[AGENTS OS]]"]
related: ["[[zcode-custom-subagent-definition-format]]", "[[delegacion-a-subagentes]]"]
aliases: []
confidence: "high"
memory_state: active
continuity_key: "echo-forge-docs-campaign/agent-factory"
supersedes:
superseded_by:
load_policy: "when_project_loaded"
indexable: false
index_priority: high
tags:
  - kind/agent-memory
  - scope/project
  - agent/internal
  - area/aranea
---

# 2026-09-12-zcode-docs-agent-factory-continuity

## Continuidad

- Fábrica lista: 10 custom subagents ZCode creados en `~/.zcode/agents/` (user scope) y validados contra el parser real: knowledge-architect (max), echo-functional-cartographer (high), forge-functional-cartographer (high), echo-forge-integration-cartographer (max), legacy-doc-curator (high), llm-wiki-documentarian (high), agents-md-gardener (high), context-budget-auditor (high), documentation-verifier (max), vault-publisher-reconciler (max). Modelo exacto `custom:builtin:zai-start-plan:GLM-5.3-Flash` (pool promocional; alias `inherit` prohibido en estos agentes). Read-only: los 7 cartographers/curators/auditors/verifier/architect sin Write/Edit; writers: llm-wiki-documentarian, agents-md-gardener, vault-publisher-reconciler con escritura acotada por prompt a su artifact único.
- Modelo de coordinación acordado: READ MANY / WRITE ONE, un artifact por especialista asignado por el orchestrator, el proyecto `owner: agent` es planner único, publicación canonical sólo en fase PUBLICATION explícita (default: la ejecuta el orchestrator). Enforcement de escritura fina es PROMPT-ONLY (ZCode no tiene ACL de paths; el allowlist de tools sí es hard).
- La campaña documental NO arrancó: no se documentó Echo ni Echo Forge, no se migró ni borró documentación, vault limpio.
- Los subagents se cargan al bootstrap de sesión: requieren sesión/task nueva para estar disponibles.

## Señales de carga

- Cargar cuando se inicie o retome la campaña de consolidación documental Echo + Echo Forge (proyecto control-plane propuesto: `10-projects/Aranea/ECHO-FORGE-DOCS/agentes/ECHO-FORGE-DOCS-OWNER-PROJECT.md`, aún no creado).

## Próxima acción

- Fase 2: crear e inicializar el proyecto control-plane (nota planner + tarea puente en el proyecto padre Aranea) y lanzar la campaña empezando por `knowledge-architect` en sesión nueva.
