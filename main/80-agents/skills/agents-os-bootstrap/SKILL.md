---
type: skill
schema_version: 1
name: agents-os-bootstrap
scope: global
created: 2026-07-04
updated: 2026-09-12
description: Mandatory AGENTS OS startup skill. Run once at cold start when a new session begins or the user explicitly asks to load AGENTS OS. Its loaded contract governs warm turns and entity swaps without rereading the skill or base stack. Loads the minimum operating stack and routes entity-specific context lazily.
aliases:
  - agents-os-bootstrap
entities:
  - "[[AGENTS OS]]"
  - "[[agents-os]]"
load_policy: always
indexable: true
index_priority: critical
tags:
  - kind/skill
  - scope/global
  - agent/alwaysload
  - action/bootstrap
  - tech/agents-os
---

# agents-os-bootstrap — AGENTS OS Startup

## Purpose

Single canonical startup for AGENTS OS. Detects session mode (cold / warm /
swap-entity), loads only the relevant stack, resolves the active entity, and
routes to one specialized skill when needed. Nothing else should redefine
startup.

## Canonical Authority

`AGENTS.md` invokes this skill; this file owns startup. `agents-os.md` is only
the conceptual map, the constitution contains invariants, specialized skills
contain lazy procedures, and project/journal notes contain state/history.

## Session Modes

Pick exactly one per turn:

- **Cold start** — first turn of a conversation, or no entity loaded yet.
  Load: constitution + global profile + ONE compact global internal note +
  active entity context via Context Router.
- **Warm turn, same entity** — continuation of an ongoing task on the same
  entity. Reuse what is already in context. Fetch only the delta needed.
  Never re-read constitution/profile/bootstrap.
- **Entity swap** — same conversation switches to a different entity/topic.
  Keep constitution + global profile; replace entity pack; skip global
  internal reload if already loaded this session.

Invalidation signals (re-read the affected source only, not the whole stack):
the user names a new entity, the intent clearly shifts, or a base source
changed on disk. Do NOT re-run the full ritual on every message.

## Procedure

### Cold start

1. Load always-load public invariants:
   - `80-agents/agents-os/agent-constitution.md`
   - the single always-load note under
     `80-agents/memory/public/user-preference/` — the global profile. Resolve it
     by that directory; its filename belongs to the vault owner.
2. Load exactly ONE global internal note:
   `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`.
   Do not scan `memory/internal/` for `always` notes; the contract below
   forbids any other `always` outside this single global note.
3. Load the skills registry `80-agents/skills/INDEX.md` (core catalog +
   federated rows). This is how the agent knows which skills exist and where
   they live without scanning folders. Do not read the federated domain index
   unless routing needs detail beyond the registry rows.
4. Read `agents-os.md` only if the task needs the conceptual map; do not add it
   to the base stack by ritual.
5. Identify the active entity from the user's request. If not explicit,
   infer candidates with a focused search and declare the assumed entity.
   Resolve aliases/slugs to the canonical Obsidian title.
6. Apply the domain gate from the entity's `area` frontmatter (resolve it via
   Graphify metadata/facets or the entity note; do not scan folders):
   - `[[Meli]]` → load `meli-agent-dev`.
   - `[[Echo]]` or `[[Aranea]]` → load `aranea-agent-dev`.
   - Any other area, or no resolvable entity → no domain router.
   If no entity resolves but the surface shows domain evidence (MCP tool
   prefixes `mcp__aranea-*`, or corporate tooling such as Zord/Fury/Spellbook),
   use that instead. Ambiguous or conflicting evidence fails closed: no
   router. Never load both routers; the router loads at most ONE specialized
   skill and owns the scoped preferences of its domain.
7. If the request needs vault state or domain context, route to `agents-os-context-retrieval` for the active entity (cheapest layer first; stop when sufficient). For casual or general requests that do not depend on a vault entity, skip entity retrieval.
8. Open source Markdown only for notes that affect a persistent decision,
   edit, or answer that must be verified.
9. Select at most ONE additional specialized skill (lazy-load) only if the
   task needs it and the domain router (if loaded) does not already route it.
10. Skip the orientation note unless retrieval was degraded. If degraded,
   emit the minimal `Entity / Goal / Skills / Open questions` note and flag
   the gap.

### Warm turn

1. Reuse the stack already loaded.
2. Fetch only the delta required for the new turn.
3. Only re-read a source if it changed on disk or the entity/intent shifted.
4. Do not invoke or reread bootstrap merely because the user sent another message.

### Entity swap

1. Keep the invariants and global internal note from cold start.
2. Resolve the new entity and route to `agents-os-context-retrieval` for it.
3. Re-apply the domain gate with the new entity's `area`; if the domain
   changed, drop the previous domain pack (router + scoped preferences) and
   load the new router. Never hold two domain packs at once.
4. Drop the previous entity pack from active reasoning.

## Lazy Skill Routing

The registry `80-agents/skills/INDEX.md` is already in context from cold
start; route from it instead of scanning folders. Match the task to one primary
skill and load that `SKILL.md`; load a dependency only if its procedure
requires it. Common direct routes: close → `agents-os-session-close`, repair
AGENTS OS → `agents-os-doctor`, project execution →
`agents-os-agent-project-workflow`, entity merge →
`agents-os-entity-lifecycle`, index stale or blocked update →
`agents-os-graphify-maintenance`.

Domain-gated skills route through their domain router, never directly. The
domain comes from the active entity's `area` (domain gate, cold start step 6):
`[[Meli]]` → `meli-agent-dev`; `[[Echo]]`/`[[Aranea]]` → `aranea-agent-dev`;
any other area → no router. The two domains are mutually exclusive; a domain
swap replaces the pack explicitly instead of mixing.

Do not load Nexus, MELI, or external project skills unless the request
explicitly asks for them.

## Hard Rules

- This skill is the only startup procedure. Do not duplicate it in
  `agents-os.md`, `AGENTS.md`, adapters, or project notes.
- Invariants load once per session (cold start). Warm turns reuse.
- Only ONE global internal note may use `load_policy: always`, and it may contain only compact behaviors or failure lessons transferable across domains. Domain state, releases, hashes, task progress and project-specific next steps must use `when_project_loaded`, `when_application_loaded`, `when_error_matches` or `manual`.
- Internal continuity uses one active checkpoint per `continuity_key`. Update it in place after consuming it; if replacement is required, retire the prior checkpoint to `superseded` plus `manual` in the same change. Never load `superseded` or `archived` continuity during normal startup or entity retrieval.
- Prefer Graphify / focused search before opening broad folders.
- Use canonical Obsidian titles for entity links; aliases/slugs are routing.
- Resolve vault paths from `VAULT_ROOT`; never persist a machine-specific
  absolute vault path.
- Do not create memory notes during bootstrap.
- Do not load the AGENTS OS development project unless the task is
  maintaining the system itself.
- Sufficiency-first context: the budget is a soft ceiling that escalates on
  miss, never a fixed cut. See `../_shared/graphify-contract.md`.
- Skip the orientation note unless retrieval was degraded.

## Token Targets (soft)

Cold base 3–6k tokens; warm delta <1k; entity swap 1–3k. Never cut relevant
context to satisfy a number; investigate duplicate reads or broad scans.

## Output

On cold start, optionally emit a one-line orientation:

```
Entity: [[<canonical>]] · Goal: <one phrase> · Skills selected: <list or none>
```

On warm turn or entity swap, no output unless something is wrong.
