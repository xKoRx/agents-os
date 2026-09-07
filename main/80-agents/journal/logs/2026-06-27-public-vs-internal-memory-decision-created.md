---
type: change_log
scope: session
created: 2026-06-27
updated: 2026-06-27
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[AGENTS OS]]"
related:
  - "[[public-vs-internal-memory]]"
aliases:
  - public vs internal memory decision creation log
confidence: verified
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - area/personal
  - change/created
  - kind/changelog
  - project/agents-os
  - project/agentsos
  - scope/session
---
# Public vs internal memory decision created

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `80-agents/memory/public/decision/agents-os/public-vs-internal-memory.md`

## Motivo

- The public/internal memory boundary was already stable in the AGENTS OS control note, constitution, and behavior-config skill.
- Fase 6 still required a formal ADR/decision memory for this boundary.

## Fuentes usadas

- `10-projects/AGENTS OS.md`
- `80-agents/memory/public/constitution/agent-constitution.md`
- `80-agents/skills/agents-os-behavior-config/SKILL.md`
- `80-agents/skills/_shared/note-types.md`

## Resolución aplicada

- Created a public `type: decision` memory scoped to `[[AGENTS OS]]`.
- Documented the boundary, rationale, consequences, rejected alternatives, and internal-to-public promotion requirement.

## Validación

- Metadata follows the AGENTS OS beta schema.
- Decision is stored under `80-agents/memory/public/decision/` and should be indexable by Graphify.
- Change log is stored under `80-agents/journal/logs/` with `indexable: false`.
