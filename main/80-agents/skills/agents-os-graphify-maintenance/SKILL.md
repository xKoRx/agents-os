---
type: skill
name: agents-os-graphify-maintenance
scope: global
created: 2026-07-04
updated: 2026-09-12
index_priority: high
indexable: true
load_policy: manual
schema_version: 1
description: Maintain the local Agent Memory System Graphify index contract. Use when configuring what Graphify indexes, diagnosing a stale or blocked index (including delta-vs-global debt classification), validating that generated state and raw sessions stay outside the vault, checking graph health, or documenting a model/IDE-agnostic retrieval interface.
aliases:
  - agents-os-graphify-maintenance
tags:
  - kind/skill
  - action/graphify-maintenance
  - tech/agents-os
  - tech/graphify
  - scope/global
---

# Agent Memory System Graphify Maintenance

## Purpose

Keep Graphify aligned with Markdown truth. Ensure retrieval stays cheap, current, and consistent across agents.

## Execution Model

Canonical execution of `graphify-obsidian`, in force everywhere (skills, closes, hygiene):

1. **Default: query with auto-refresh.** Agents call the query they need
   directly; the wrapper detects corpus changes, rebuilds the machine-local
   index and serves the last-known-good graph if extraction fails. No separate
   `update` first.
2. **Explicit `update` is maintenance-only**: forced rebuild, `.graphifyignore`
   change, mass move, or hygiene cadence. It is all-vault and runs the strict
   lint gate; any finding anywhere blocks publication.
3. **Blocked `update` is not a session blocker.** Queries keep serving the
   last-known-good graph; classify the block (below) and continue. Never
   abandon a close or a retrieval because the strict gate is red.
4. `status` is the freshness interface; `cache-path` resolves the machine-local
   state. Generated state never enters the vault.

## Delta vs Global Debt (blocked update diagnosis)

When an explicit `update` is blocked, attribute the findings before acting:

1. List the session's changed files (delta) and the gate's findings (paths +
   counts).
2. Run strict lint over the delta only. Delta findings: fix them in this
   session.
3. Findings whose paths are all outside the delta are **global debt**: do not
   sanitize unrelated notes in-session; record them for
   `agents-os-hygiene-cycle` (feedback note only if the debt blocks real work
   repeatedly) and proceed with auto-refresh queries.
4. Mixed case: fix the delta, report the global remainder explicitly as
   remaining debt.

## Minimal Read

Read `../_shared/graphify-contract.md` for indexable types, command patterns, and non-shell fallback.

## Procedure

1. Identify changed notes and their `type`, `indexable`, and `index_priority`.
2. Confirm raw sessions, drafts, scratch, and attachments are excluded.
3. Diagnose with `graphify-obsidian status`; query commands auto-refresh stale
   local state. An explicit `update` is reserved for maintenance or forced
   rebuilds and keeps the strict lint gate — if it blocks, apply Delta vs
   Global Debt before touching notes.
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

In a sandbox without write access to `~/.cache`, `graphify-obsidian update` may need host escalation because the CLI creates its temporary cache there.

Use `graphify-obsidian status` as the freshness interface. If file inspection is
needed, resolve the machine-local directory with `graphify-obsidian cache-path`.
No Graphify output directory inside the vault is valid.

## Validation Examples

Run the canonical query set from `../_shared/graphify-contract.md` — that
contract owns the recipe and its budget semantics. Then add one existence check
for whatever this run created:

```bash
graphify-obsidian explain "<exact-title-created-or-changed-in-this-run>"
```

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
