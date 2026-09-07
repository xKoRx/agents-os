---
type: known_error
scope: tool
created: 2026-06-27
updated: 2026-09-03
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[graphify-contract]]"
  - "[[80-agents/skills/agents-os-retrofit-raw-session/SKILL|agents-os-retrofit-raw-session]]"
aliases:
  - graphifyignore broad raw session pattern
  - raw session glob excludes retrofit skill
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - area/personal
  - kind/knownerror
  - priority/high
  - project/agents-os
  - project/agentsos
  - scope/tool
---
# Broad raw-session ignore pattern can exclude non-journal skills

## Sintoma

- `graphify-obsidian update` succeeds, but a skill such as `agents-os-retrofit-raw-session` does not appear in the local `graph.json`.
- Queries for the skill retrieve only a historical backlog section, not the actual `SKILL.md`.

## Causa

- The `.graphifyignore` rule `**/*raw-session*.md` can match paths whose parent directory contains `raw-session`, not only raw-session filenames.
- This accidentally excludes `80-agents/skills/agents-os-retrofit-raw-session/SKILL.md`.

## Impacto

- The skill exists in Markdown but is not discoverable through normal Graphify retrieval.
- Future agents may think the skill is missing, stale, or only documented in the backlog.

## Deteccion

- Search the live graph for the skill source path:
  - `rg 'source_file": "80-agents/skills/agents-os-retrofit-raw-session/SKILL.md"' "$(graphify-obsidian cache-path)/graph.json"`
- If no node exists but the file appears in the `graphify-obsidian update` copy list, inspect `.graphifyignore` broad globs.

## Mitigacion

- Exclude raw sessions by directory:
  - `80-agents/journal/sessions/raw/`
  - `80-agents/journal/sessions/raw/**`
- Avoid broad `raw-session` filename globs unless they are proven not to match parent directories.
- After changing `.graphifyignore`, reindex and validate:
  - the skill source appears in the local graph resolved by `cache-path`;
  - raw session files remain absent from the graph.

## Evidencia

- 2026-06-27 Codex run: before removing the broad pattern, `graphify-obsidian query '08 Retrofit Raw Session'` only recovered the backlog node, and `rg` found no source nodes for the retrofit skill.
- After removing the pattern and reindexing, Graphify rebuilt 847 nodes, 759 edges, and 98 communities; `agents-os-retrofit-raw-session` was recovered from its `SKILL.md` and raw session filenames remained absent from the local graph.
