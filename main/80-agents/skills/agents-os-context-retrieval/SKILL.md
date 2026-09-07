---
type: skill
schema_version: 1
name: agents-os-context-retrieval
scope: global
created: 2026-07-04
updated: 2026-09-03
description: Retrieve focused context for the Agent Memory System using Graphify or an equivalent index. Use when an agent needs project/application/entity context, learnings, ADRs, known errors, runbooks, integrations, or related notes before working, while keeping context/token usage low.
entities:
  - "[[AGENTS OS]]"
  - "[[agents-os]]"
  - "[[context-router]]"
load_policy: when_entity_loaded
indexable: true
index_priority: critical
tags:
  - kind/skill
  - scope/global
  - agent/alwaysload
  - action/retrieval
  - tech/agents-os
---

# Agent Memory System Context Retrieval

## Purpose

Load the smallest useful context set. Markdown is canonical; Graphify is a derived index.

## Minimal Read

Read `../_shared/graphify-contract.md` only for syntax, budgets or fallback. Read [[token-economy-indexing-architecture]] and [[context-router]] only to justify a design decision.

## Inputs

- Entity or candidate entity.
- Topic or task.
- Available retrieval interface: `graphify-obsidian`, shell, IDE search, MCP/tool, or manual graph output.

## The four layers (route cheapest → most expensive)

Each layer reduces candidates before the next. **Start at the cheapest layer relevant to the intent** — this is not a strict waterfall that always begins at Layer 0. Pick an entry layer per intent, then climb only if insufficient. Never load a body without a prior selection.

```
Layer 0  metadata/facets    → exact file-node selection         (`filter`, 0 LLM tokens)
Layer 1  00-index.md        → curated domain catalog            (read one selected index)
Layer 2  graph relations    → typed edges + wikilink references (`path`/`affected`/`query`)
Layer 3  note body          → only chosen Markdown sources      (body-only, surgical read)
```

## Procedure

1. **Resolve the entity** to its canonical Obsidian file node through an exact file title (`<canonical>.md`) or alias filter before lexical fallback. Treat slug, repo and path as fallback routing signals; once resolved, retain the canonical Obsidian title without the `.md` suffix for wikilinks and user-facing output.
2. **Classify the intent** — fact · relation/impact · domain synthesis · code · procedure — and pick the **entry layer**, then climb cheap→expensive only as needed:

   | Intent | Entry layer | Climb if |
   |---|---|---|
   | Fact about a known entity | exact title/alias plus metadata facets | projected metadata lacks the fact |
   | Relation / impact | resolve file node, then typed graph edges and `references` | relation is absent, ambiguous or stale |
   | Domain synthesis | type/tag/routing facets → domain `00-index.md` → filtered lexical query | catalog and candidates are insufficient |
   | Code question | graphify **code** graph (`explain`/`affected`) → specific symbols | symbol missing |
   | Procedure | `type=runbook` or `type=skill` plus entity/routing filters | exact candidates do not cover the operation |
   | Unresolvable entity | title/alias filter → focused `rg`/keyword search → declare assumed entity | still ambiguous |

3. Call the needed `graphify-obsidian` query directly. The wrapper checks freshness
   and rebuilds its machine-local index automatically; do not prepend a manual update.
4. **Layer 0 selection:** use `graphify-obsidian filter` for exact `type`, `tag`, `scope`, `status`, routing, file title or alias matches. `--title` targets the file-node label and therefore includes `.md`; `--alias` uses the frontmatter value without a suffix. Combine repeated filters as an intersection. Use `query --filter key=value` only after facets have defined the candidate set; lexical terms rank inside that set rather than searching the whole corpus.
5. **Climb from the entry layer cheap→expensive; stop when sufficient.** Bootstrap already loaded the base invariants on cold start: do not reload them here. Within entity context prefer the canonical entity file, then `memory_state: active` scoped continuity with a matching `continuity_key`, active decisions/errors and relevant runbooks. Ignore `superseded` and `archived` memory unless the user asks for history; treat lifecycle-less legacy memory as candidates, never as a set to bulk-load, and migrate it when touched.
6. **Layer 2 relations:** traverse allowlisted frontmatter edges (`in_area`, `child_of`, `in_project`, `for_application`, `about`, `related_to`, `supersedes`) before generic body links when the question names that relation. Vault `[[wikilinks]]` remain `references` edges. Query backlinks with `graphify-obsidian affected "<note>.md" --relation references`; the `.md` suffix and explicit relation are required for generic backlinks. See `../_shared/graphify-contract.md`.
7. **Layer 3 body-only:** open only selected source notes and load their body without frontmatter or `tasks` blocks. A persisted decision or edit still requires verification against source Markdown because Graphify is derived.
8. Keep the context-pack inventory internal. Expose it only on degradation, ambiguity that affects the answer, or explicit audit. If a layer misses, escalate one layer and continue with the safest narrow assumption.

## Noisy Query Handling

If results anchor on templates, plugins, generated files or generic headings,
reject them. Retry with `canonical entity + memory type + concrete symptom`;
then use exact source search if still noisy. Record degradation, not “missing
knowledge”.

## Context Budget — sufficiency-first, soft ceilings

Do **not** cut context at a fixed number; that was a design error. Load cheap→expensive and **stop when the context is sufficient**. The budget is a per-tier **soft ceiling** and a smell-test, never a guillotine — the ceilings grow with the depth the intent needs:

```
fact       < relation < synthesis
(low)        (medium)   (medium-high)
```

Escalate past a tier's ceiling only after a miss, and record why.

Priority within an entity load: entity note or `explain`; critical/high scoped
memories; matching known errors; runbooks only for an operation. Prefer a
verified source over several graph neighbors.

When context is tight, prefer one verified source note over several graph neighbors.

## Fallback

Without shell, request `update`, `filter`, `explain`, `query`, `path` or `affected` from the host bridge. If exact metadata filtering is unavailable, emulate it over `graph.json`; if Graphify is unavailable or stale, use focused Markdown search, open only top candidates and report degraded status plus confidence.

## Output — the context pack

Track internally: intent, canonical entity, route/layers, selected sources,
approximate tokens, confidence and gaps. Show it only on degradation or audit.

## Validation

Run `python3 80-agents/skills/agents-os-context-retrieval/scripts/context_router_e2e.py --json` from `VAULT_ROOT`. The no-API matrix exercises project, skill, prompt, known_error, resource, application and typed project relations through two independent surfaces: the Graphify CLI and focused Markdown fallback. It fails on missing or extra candidates and reports miss rate, precision proxy, p95 latency and selected body count against the recorded Phase 2 baseline.

## Hard Rules

- Do not use abstract queries like "give me important context".
- Do not treat template nodes as evidence of live project state.
- Do not treat Graphify output as canonical without opening source notes when the answer affects persisted knowledge.
- Do not write, copy or sync Graphify output inside the vault; resolve local state through `graphify-obsidian cache-path`.
- Do not load raw sessions by default.
- Do not create or trust duplicate entity targets caused only by case, accent,
  singular/plural, or alias differences.
- Do not load a note body without a prior selection through facets, a curated index or graph relations. Body is the most expensive layer; reach it last, only for the chosen note.
- Do not cut context at a fixed token number; stop by sufficiency, not by guillotine.
- Tags are exact facets, never graph edges. For vault relations use typed frontmatter edges when semantics are explicit and `references` for generic wikilinks.
