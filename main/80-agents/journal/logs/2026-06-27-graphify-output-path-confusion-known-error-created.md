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
  - "[[graphify-output-path-confusion]]"
aliases:
  - graphify output path confusion known error creation log
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
# Graphify output path confusion known error created

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `80-agents/memory/public/known-error/agents-os/graphify-output-path-confusion.md`

## Motivo

- During hygiene validation, Graphify had successfully rebuilt the live index, but the old `95-graphify/graphify-out/GRAPH_REPORT.md` made the index look stale.
- The path distinction is reusable operational knowledge for future agents validating Graphify.

## Fuentes usadas

- `graphify-obsidian update` output from 2026-06-27.
- `stat` comparison between `95-graphify/obsidian/GRAPH_REPORT.md` and `95-graphify/graphify-out/GRAPH_REPORT.md`.
- `graphify-obsidian explain "Graphify update can fail in sandbox when cache access is blocked"`.

## Resolución aplicada

- Created a public `known_error` under AGENTS OS memory with symptom, cause, impact, detection, mitigation, and evidence.

## Validación

- After reindex, Graphify rebuilt 813 nodes, 728 edges, and 95 communities.
- `graphify-obsidian query 'graphify-output-path-confusion' --budget 1200` recovered the new public known error.
