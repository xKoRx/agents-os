---
type: skill
name: agents-os-graphify-maintenance
scope: global
created: 2026-07-04
updated: 2026-09-03
description: Maintain the local Agent Memory System Graphify index contract. Use when configuring what Graphify indexes, repairing auto-refresh, validating that generated state and raw sessions stay outside the vault, checking graph health, or documenting a model/IDE-agnostic retrieval interface.
tags:
  - kind/skill
  - action/graphify-maintenance
  - tech/agents-os
  - tech/graphify
---

# Agent Memory System Graphify Maintenance

## Purpose

Keep Graphify aligned with Markdown truth. Ensure retrieval stays cheap, current, and consistent across agents.

## Minimal Read

Read `../_shared/graphify-contract.md` for indexable types, command patterns, and non-shell fallback.

## Procedure

1. Identify changed notes and their `type`, `indexable`, and `index_priority`.
2. Confirm raw sessions, drafts, scratch, and attachments are excluded.
3. Validate with `graphify-obsidian status`; query commands auto-refresh stale
   local state in diagnostic-lint mode. Run explicit `update` only for
   maintenance or forced rebuilds; that path keeps the strict lint gate.
4. Validate that important Sistema 1/Sistema 2 links are discoverable through their
   canonical titles.
5. Validate that common aliases/slugs resolve back to the canonical source note
   rather than producing duplicate entity evidence.
6. Record any index gaps for hygiene review.

## Stale Index Detection

Treat the index as stale when any of these are true:

- `graphify-obsidian status` reports `stale` after changes to indexable sources.
- A query reports that automatic refresh failed and no local graph is available.
- `explain` or focused `query` cannot find a newly created indexable memory after a successful update.
- The local graph predates relevant indexable memory work.

In Codex-style sandboxes, `graphify-obsidian update` may need host escalation because the CLI creates a temporary cache under `~/.cache`.

Use `graphify-obsidian status` as the freshness interface. If file inspection is
needed, resolve the machine-local directory with `graphify-obsidian cache-path`.
No Graphify output directory inside the vault is valid.

## Validation Examples

```bash
graphify-obsidian explain "<active-entity>"
graphify-obsidian query "<active-entity> learning critical <topic>" --budget 1200
graphify-obsidian query "<active-entity> known_error <symptom>" --budget 1200
graphify-obsidian query "<active-entity> runbook <operation>" --budget 1200
graphify-obsidian explain "<exact-known-node-title>"
```

The `--budget` value is a soft starting ceiling per query, not a hard cap: if a result looks truncated, re-query with a higher ceiling. See `../_shared/graphify-contract.md` "Budget semantics".

Expected result: focused queries should return source notes relevant to the active entity. Raw sessions and journal logs should not appear in normal retrieval.
When alias hygiene changed, validate both the canonical title and one common
variant. The variant may be accepted as input, but the source note must remain
the same canonical Markdown file.

## Output

```text
Changed notes:
Should reindex:
Excluded notes checked:
Validation queries:
Index gaps:
Next action:
```

## Hard Rules

- Graphify is derived; never treat generated output as source of truth.
- Never store or sync Graphify outputs, histories, caches or wheels in the vault.
- Never invoke raw `graphify` from the vault; use `graphify-obsidian`.
- Do not create manual context packs as a parallel index.
- Do not index L0 raw sessions by default.
- Do not accept separate graph entities caused only by case/accent/alias drift
  as valid Sistema 2 truth.
