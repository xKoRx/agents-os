---
type: change_log
scope: project
created: 2026-06-27
updated: 2026-06-27
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agents-os]]"
indexable: false
index_priority: never
load_policy: manual
tags:
  - area/personal
  - kind/changelog
  - project/agents-os
  - project/agentsos
  - scope/project
---
# AGENTS OS System 1 / System 2 Template Policy

## Change

Renamed the conceptual boundary:

- Sistema 1: agent memory and learnings.
- Sistema 2: real/canonical vault entities.

Added the hard rule that every new Sistema 2 document must be created from a
template. If no matching template exists under `70-templates/`, the agent must
create the template before or in the same change, then create the document from
that template.

## Files Updated

- `80-agents/skills/_shared/note-types.md`
- `80-agents/skills/agents-os-note-capture/SKILL.md`
- `80-agents/skills/agents-os-entity-lifecycle/SKILL.md`
- `80-agents/skills/agents-os-entity-update/SKILL.md`
- `80-agents/agents-os/agents-os.md`
- `80-agents/memory/public/constitution/agent-constitution.md`
- `10-projects/AGENTS OS.md`

Additional skill contracts were mechanically aligned from Capa terminology to
Sistema terminology where they referenced the boundary.

## Source

User clarified that the intended behavior is:

- agents should create every new document from templates;
- when the missing document is part of Sistema 2, the missing template should be
  created;
- Sistema 1 should name the memory/learning system;
- Sistema 2 should name the real-entity system.

## Validation

Graphify was reindexed successfully after the edits. Focused queries retrieved:

- `Template Policy`
- `Sistema 1 Memory`
- `Sistema 2 Entity`
- `AGENTS OS System Types`

No active AGENTS OS docs, skills, or public memory notes retain the previous
layer terminology after the update.
