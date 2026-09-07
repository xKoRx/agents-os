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
  - "[[agents-os]]"
aliases:
  - AGENTS OS operational guide consolidated
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
# 2026-06-27 AGENTS OS Operational Guide Consolidated

## Cambio

- **Tipo:** moved / updated
- **Archivo(s):**
  - `80-agents/agents-os/agents-os.md`
  - `40-archive/agents-os-drafts/`
  - `80-agents/skills/agents-os-bootstrap/SKILL.md`
  - `80-agents/adapters/README.md`
  - `80-agents/adapters/codex.md`
  - `80-agents/adapters/claude.md`
  - `80-agents/adapters/cursor.md`
  - `80-agents/adapters/antigravity.md`
  - `80-agents/memory/public/constitution/agent-constitution.md`
  - `80-agents/memory/public/known-error/agents-os/graphifyignore-broad-raw-session-pattern.md`
  - `.graphifyignore`
  - `10-projects/AGENTS OS.md`
  - `README.md`

## Motivo

- Antes de iniciar pruebas beta, la documentación operativa y los drafts de diseño estaban mezclados en `80-agents/agents-os/`.
- El flujo necesitaba un único lugar canónico para que Codex, Claude, Cursor y Antigravity sepan cómo iniciar, recuperar contexto, cerrar sesiones y medir la beta.

## Fuentes usadas

- `10-projects/AGENTS OS.md`
- `80-agents/agents-os/agents-os.md`
- `80-agents/skills/agents-os-bootstrap/SKILL.md`
- `80-agents/adapters/`

## Resolución aplicada

- Se movieron los documentos draft de análisis/diseño a `40-archive/agents-os-drafts/`.
- Se creó una guía operativa única en `80-agents/agents-os/agents-os.md`.
- Se actualizó bootstrap y adaptadores para iniciar desde esa guía operativa.
- Se excluyó `40-archive/` de Graphify para evitar ruido de drafts en retrieval operativo.
- Se corrigió una referencia pública al backlog draft histórico de `agents-os-retrofit-raw-session`.

## Validación

- `graphify-obsidian update` ejecutado tras este cambio: 816 nodes, 727 edges, 98 communities.
- `rg '40-archive|agents-os-drafts|07-skills-y-tareas|00-onboarding-ia' 95-graphify/obsidian/graph.json` no encontró fuentes archivadas en el grafo vivo.
- `graphify-obsidian query 'AGENTS OS guía operativa inicio flujo retrieval cierre beta' --budget 1200` recuperó `80-agents/agents-os/agents-os.md`.
- Pendiente ejecutar la beta E2E usando la nueva guía como entrypoint.
