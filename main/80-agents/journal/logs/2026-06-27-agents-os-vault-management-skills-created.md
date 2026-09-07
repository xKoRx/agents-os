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
# AGENTS OS Vault Management Skills Created

## Change

Created four lazy AGENTS OS skills for full vault management:

- `80-agents/skills/agents-os-note-capture/SKILL.md`
- `80-agents/skills/agents-os-entity-lifecycle/SKILL.md`
- `80-agents/skills/agents-os-relation-maintenance/SKILL.md`
- `80-agents/skills/agents-os-vault-refactor/SKILL.md`

Updated:

- `80-agents/skills/agents-os-bootstrap/SKILL.md`
- `80-agents/agents-os/agents-os.md`
- `10-projects/AGENTS OS.md`

## Source

User requested new skills for complete note, entity, and relationship
management in the vault, loaded by bootstrap in a lazy way.

## Rationale

The existing AGENTS OS skills covered memory lifecycle and narrow entity
updates, but not the full vault operations needed for note capture, entity
lifecycle, relation repair, and structural refactors.

## Validation

Graphify was reindexed successfully after the edits. Focused exact-name queries
retrieved all four new skills:

- `AGENTS OS Note Capture`
- `AGENTS OS Entity Lifecycle`
- `AGENTS OS Relation Maintenance`
- `AGENTS OS Vault Refactor`
