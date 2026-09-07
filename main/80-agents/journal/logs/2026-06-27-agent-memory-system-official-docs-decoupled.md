---
type: change_log
scope: project
created: "2026-06-27"
updated: "2026-06-27"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[agents-os]]"
related:
  - "[[agent-constitution]]"
  - "[[rjara-agent-profile]]"
aliases:
  - official docs decoupled from project context
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
  - tech/agentsos
---
# 2026-06-27 Agent Memory System Official Docs Decoupled

## Cambio

- **Tipo:** updated / moved
- **Archivo(s):**
  - `80-agents/agents-os/agents-os.md`
  - `80-agents/adapters/*.md`
  - `80-agents/skills/**/*.md`
  - `80-agents/memory/public/constitution/agent-constitution.md`
  - `80-agents/memory/public/user-preference/rjara-agent-profile.md`
  - `80-agents/memory/public/decision/agent-memory-system/public-vs-internal-memory.md`
  - `80-agents/memory/public/known-error/agent-memory-system/*.md`

## Motivo

- La documentación oficial del sistema no debe instruir a los agentes a cargar el proyecto de desarrollo del sistema.
- El objetivo operativo es enriquecer contexto de la tarea activa y ahorrar tokens frente al uso sin memoria persistente.

## Fuentes usadas

- Guía operativa del sistema.
- Skills, adaptadores y memoria always-load.
- Búsqueda de referencias a proyecto, entidades de ejemplo, beta y archive.

## Resolución aplicada

- La guía operativa ya no pide leer `10-projects/AGENTS OS.md`.
- Startup/adaptadores ahora cargan la guía operativa, memoria always-load y la entidad/tarea activa.
- Memoria always-load dejó de enlazar al proyecto de desarrollo.
- Ejemplos de contratos usan placeholders (`<active-entity>`, `[[active-project]]`) en vez de entidades reales.
- Memorias públicas del sistema se movieron de rutas `agents-os/` a `agent-memory-system/`.

## Validación

- `rg 'AGENTS OS|\\[\\[AGENTS OS\\]\\]|10-projects/AGENTS OS|project/agents-os|memory/public/.*/agents-os|search-middleware|java-polycard|vpp-backend|vis-octopus|Meli|beta|Beta|40-archive|agents-os-drafts' 80-agents/agents-os 80-agents/skills 80-agents/adapters 80-agents/memory/public` no devolvió resultados.
- `graphify-obsidian update` ejecutado tras el cambio: 737 nodes, 650 edges, 87 communities.
- `graphify-obsidian query 'Agent Memory System guía operativa inicio retrieval ahorro tokens' --budget 1200` recuperó `80-agents/agents-os/agents-os.md` y `80-agents/memory/public/constitution/agent-constitution.md`, sin recuperar `10-projects/AGENTS OS.md`.
- `rg '80-agents/memory/public/(decision|known-error)/agents-os|80-agents/agents-os/_drafts|80-agents/AGENTS.md|80-agents/LLM Wiki.md' 95-graphify/obsidian/graph.json` no devolvió resultados.
