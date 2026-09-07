---
type: change_log
scope: project
created: "2026-06-27"
updated: "2026-06-27"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[official-docs-memory-boundary]]"
aliases:
  - AGENTS OS memory scope restored
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
# 2026-06-27 AGENTS OS Memory Scope Restored

## Cambio

- **Tipo:** updated / moved / created
- **Archivo(s):**
  - `80-agents/memory/public/decision/agents-os/public-vs-internal-memory.md`
  - `80-agents/memory/public/known-error/agents-os/*.md`
  - `80-agents/memory/public/constitution/agent-constitution.md`
  - `80-agents/memory/public/user-preference/rjara-agent-profile.md`
  - `80-agents/memory/public/learning/agents-os/official-docs-memory-boundary.md`

## Motivo

- La instrucción del usuario era desacoplar la documentación oficial del sistema
  respecto del proyecto de desarrollo, no eliminar referencias de memorias.
- Las memorias sobre el proyecto `[[AGENTS OS]]` deben seguir scoped/linkeadas a
  ese proyecto para recuperarse cuando el trabajo activo sea mantenerlo.

## Resolución aplicada

- Se restauraron rutas `memory/public/.../agents-os/` para memorias del proyecto.
- Se restauraron `project: "[[AGENTS OS]]"`, `entities: [[AGENTS OS]]` y
  `project/agents-os` en memorias públicas del proyecto.
- Se restauró el scope de memoria always-load que había sido modificado.
- Se creó el learning `official-docs-memory-boundary` para evitar repetir este
  error.

## Validación

- `graphify-obsidian update`
  - Resultado: `743 nodes`, `655 edges`, `88 communities`.
- `rg` en documentación oficial (`80-agents/agents-os`, `80-agents/skills`,
  `80-agents/adapters`) no encontró referencias indebidas a `[[AGENTS OS]]`,
  `10-projects/AGENTS OS.md`, `project/agents-os`, ejemplos Meli ni drafts.
- `graphify-obsidian query 'Agent Memory System guía operativa inicio retrieval
  ahorro tokens' --budget 1200` recuperó la guía operativa oficial:
  `80-agents/agents-os/agents-os.md`.
- `graphify-obsidian query 'AGENTS OS official docs memory boundary
  documentación memoria' --budget 1200` recuperó el learning:
  `80-agents/memory/public/learning/agents-os/official-docs-memory-boundary.md`.
- `rg 'memory/public/(decision|known-error)/agent-memory-system'
  95-graphify/obsidian/graph.json` no encontró rutas obsoletas.
