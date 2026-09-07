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
  - "[[graphifyignore-broad-raw-session-pattern]]"
aliases:
  - graphifyignore broad raw session pattern known error creation log
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
  - scope/session
---
# Graphifyignore broad raw-session pattern known error created

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `.graphifyignore`
  - `80-agents/skills/_shared/graphify-contract.md`
  - `80-agents/memory/public/known-error/agents-os/graphifyignore-broad-raw-session-pattern.md`

## Motivo

- The broad ignore pattern `**/*raw-session*.md` prevented `80-agents/skills/agents-os-retrofit-raw-session/SKILL.md` from being indexed.
- Raw sessions are already excluded by the journal raw-session directory, so the broad pattern created more risk than value.

## Fuentes usadas

- `graphify-obsidian query '08 Retrofit Raw Session' --budget 1200`
- `rg 'source_file": "80-agents/skills/agents-os-retrofit-raw-session/SKILL.md"' 95-graphify/obsidian/graph.json`
- `.graphifyignore`

## Resolución aplicada

- Removed the broad `**/*raw-session*.md` pattern.
- Updated the Graphify contract to warn against broad raw-session filename globs.
- Created a public known error for future Graphify maintenance.

## Validación

- Link and metadata check passed for the changed files.
- After reindex, Graphify rebuilt 847 nodes, 759 edges, and 98 communities.
- `rg 'source_file": "80-agents/skills/agents-os-retrofit-raw-session/SKILL.md"' 95-graphify/obsidian/graph.json` found nodes for the retrofit skill.
- Raw session filenames remained absent from `95-graphify/obsidian/graph.json`.
