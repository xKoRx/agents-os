---
type: change_log
scope: project
created: 2026-06-27
updated: 2026-06-27
area:
  - "[[Personal]]"
project:
  - "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os-bootstrap]]"
aliases:
  - AGENTS OS surface adapters removed
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
# 2026-06-27 AGENTS OS Surface Adapters Removed

## Cambio

- **Tipo:** deleted / updated
- **Archivo(s):**
  - `80-agents/adapters/README.md`
  - `80-agents/adapters/codex.md`
  - `80-agents/adapters/claude.md`
  - `80-agents/adapters/cursor.md`
  - `80-agents/adapters/antigravity.md`
  - `80-agents/skills/_shared/skill-contract.md`
  - `80-agents/agents-os/agents-os.md`
  - `80-agents/skills/agents-os-bootstrap/SKILL.md`
  - `80-agents/memory/public/constitution/agent-constitution.md`
  - `10-projects/AGENTS OS.md`
  - `README.md`

## Motivo

- Los adaptadores por superficie duplicaban el contrato de startup y no aportaban diferencias estructurales reales.
- El usuario pidio eliminarlos y concentrar el comportamiento en skills canónicas.

## Fuentes usadas

- Solicitud explicita del usuario en la sesion actual.
- Revision de `80-agents/adapters/*` y referencias operativas en skills, guia, constitucion y documento de control.

## Resolución aplicada

- Se eliminaron los archivos vivos bajo `80-agents/adapters/`.
- Se actualizo el contrato de skills para prohibir adaptadores documentales por superficie salvo diferencia estructural futura.
- Se actualizo la guia operativa, bootstrap, constitucion y documento de control para dejar `agents-os-bootstrap` como entrypoint por skill.

## Validación

- `graphify-obsidian update` completó después de eliminar adaptadores: 715 nodos, 632 edges, 83 comunidades.
- `80-agents/adapters/` ya no existe.
- `rg '80-agents/adapters|Agent Memory System Adapter|Adapter —'` no devuelve referencias vivas en guía, skills, constitución, README ni `95-graphify/obsidian/graph.json`.
- `graphify-obsidian query "agents-os-bootstrap Agent Memory System Startup Invocation System Prompt Contract" --budget 1400` recupera `agents-os-bootstrap - Agent Memory System Startup`, `Invocation` y `System Prompt Contract`.
