---
type: known_error
scope: tool
created: 2026-06-27
updated: 2026-06-27
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related:
  - "[[graphify-contract]]"
aliases:
  - graphify cache sandbox
  - graphify obsidian cache permission
confidence: verified
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
# Graphify update can fail in sandbox when cache access is blocked

## Sintoma

- `graphify-obsidian update` exits before indexing and prints a cache creation
  error under `<home>/.cache/graphify-obsidian-tmp`.

## Causa

- The CLI creates a temporary safe-copy workspace under `~/.cache`, which can be outside the agent filesystem sandbox even when the vault itself is writable.

## Impacto

- The Graphify index remains stale or missing, so startup retrieval must not silently fall back before attempting the approved retry path.

## Deteccion

- The command exits non-zero during `Indexando Obsidian Vault: Iniciando copia segura...`.
- The error mentions `graphify-obsidian-tmp` or cache/temp directory permissions.

## Mitigacion

- Retry `graphify-obsidian update` with the host-approved escalation required by the current agent surface, using a justification that the CLI needs `~/.cache` for its temporary copy.
- If escalation is unavailable or still fails, use the documented degraded retrieval path: focused Markdown search by entity plus knowledge type/topic, then record the retrieval as degraded.

## Evidencia

- 2026-06-27 Codex run: sandboxed update failed with the cache mkdir error; the escalated retry completed and rebuilt 756 nodes, 675 edges, and 91 communities.
- A later reindex after creating this memory completed with 777 nodes, 694 edges, and 93 communities; a focused query found this `known_error`.
