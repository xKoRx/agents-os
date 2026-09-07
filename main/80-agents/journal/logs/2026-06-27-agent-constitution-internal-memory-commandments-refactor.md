---
type: change_log
scope: global
created: 2026-06-27
updated: 2026-06-27
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[agent-constitution]]"
  - "[[agents-os]]"
indexable: false
index_priority: never
load_policy: manual
tags:
  - area/personal
  - kind/changelog
  - project/agents-os
  - project/agentsos
  - scope/global
---
# Agent Constitution Internal Memory Commandments Refactor

## Change

Refactored `80-agents/memory/public/constitution/agent-constitution.md`.

The constitution now states that it is mandatory, not advisory. Its
commandments are focused exclusively on internal memory under
`80-agents/memory/internal/`.

## Source

User requested that the constitution make strict compliance explicit,
especially the commandments, and that those commandments focus only on internal
memory. The user also requested explicit freedom and even structural
libertinage for internal memory.

## Resolution

- Added an `Autoridad` section.
- Kept concise base rules outside the commandments.
- Replaced broad system commandments with internal-memory commandments.
- Made internal memory an agent-exclusive operational space.
- Explicitly allowed the agent to create its own structures, formats, queues,
  checkpoints, indexes, notes, messages, heuristics, and continuity signals.
- Preserved hard boundaries: no secrets, credentials, harmful material, heavy
  dumps, evidence falsification, or replacement of public/canonical sources.

## Validation

Graphify was reindexed successfully after the edits. Focused queries retrieved:

- `Agent Constitution`
- `Autoridad`
- `Mandamientos De Memoria Interna`

Text validation confirmed the constitution's commandments now focus on internal
memory, while broad AGENTS OS rules remain outside the commandments.
