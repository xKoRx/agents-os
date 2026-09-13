---
type: skill
schema_version: 1
name: agents-os-doctor
scope: global
created: 2026-07-25
updated: 2026-09-12
description: Lint the AGENTS OS installation and propose minimal repairs. Use when the user says "agents-os-doctor", "doctor", "health check AGENTS OS", or when retrieval/skills/bootstrap behave unexpectedly. Apply repairs only after explicit authorization.
aliases:
  - agents-os-doctor
entities:
  - "[[AGENTS OS]]"
  - "[[agents-os]]"
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - scope/global
  - action/doctor
  - action/lint
  - tech/agents-os
---

# agents-os-doctor — AGENTS OS Health Check

## Purpose

Detect drift, rot, and contract violations before they hurt retrieval or
startup. Read-only by default.

Lazy-load. Invoke only when something feels off, when a phase iteration ends,
or as part of a periodic hygiene cycle.

## Minimal Read

1. `../_shared/metadata-schema.md` — load_policy closed club, type defaults.
2. `../_shared/skill-contract.md` — folder shape, token budget, audience split.
3. `../agents-os-bootstrap/SKILL.md` — single canonical startup (the authority
   this doctor checks against).

Do not duplicate their content here.

## Executable Check

Run from the vault root:

```bash
python3 80-agents/skills/agents-os-doctor/scripts/doctor.py
```

Use `--strict` in a release gate. The script never prints matched secret
values. It validates canonical paths, the always-load closed club,
`.graphifyignore`, skill registry parity, internal credential assignments,
startup token shape and duplicate Hot Path bridges.

The checks below remain the extended manual audit.

## Checks

Run all checks. For each finding, emit severity + minimal fix.

### 1. Path integrity

- `AGENTS.md` and IDE hooks use `VAULT_ROOT`-relative references. Flag any
  machine-specific home or absolute vault path.
- `80-agents/skills/*/SKILL.md` relative refs resolve: `../_shared/`,
  `../../templates/`, `../../../templates/` depending on depth.
- `.graphifyignore` excludes `95-graphify/`, `graphify-out/`, `trash/`,
  `00-inbox/`, `40-archive/`, and the AGENTS OS packaging/distribution copies
  under `30-resources/agents-os/`.

### 2. Canonical link integrity

- Every `[[link]]` in frontmatter `area`/`project`/`application`/`entities`/
  `related` resolves to a note that exists.
- No duplicate entities that differ only by case, accent, singular/plural, or
  historical name (those belong in `aliases`).

### 3. `load_policy` closed club

Only these may use `load_policy: always`:

- `80-agents/agents-os/agent-constitution.md`
- `80-agents/skills/agents-os-bootstrap/SKILL.md`
- `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`
- exactly ONE note under `80-agents/memory/public/user-preference/` — the global
  profile. Its filename belongs to whoever installs the vault, so the check
  resolves it by looking for the single always-load note in that directory; a
  second one is a club violation and zero means the install is incomplete.

Anything else with `load_policy: always` is a violation. Flag with the
matching `when_*_loaded` policy. If a domain memory truly needs always-load,
require an ADR before allowing it.

### 4. Startup duplication

The startup procedure must live ONLY in `agents-os-bootstrap/SKILL.md`.
Flag any procedural startup steps found in:

- `AGENTS.md`
- `agents-os.md` (should be map+routing only)
- project notes
- adapters or per-surface overrides

### 5. Skill frontmatter sanity

- Every `80-agents/skills/*/SKILL.md` carries the full set the schema contract
  requires: `type`, `schema_version`, `name`, `description`, `scope`,
  `load_policy`, `indexable`, `index_priority`. A skill missing any of them is
  skipped by the corpus lint and unrankable by retrieval.
- `name` matches its folder.
- S1 notes never use `status`; there is no `draft` state to clear.
- `load_policy` matches reality (e.g. `session-close` is `manual`, not
  `always`).

The executable check enforces this section; `--strict` fails on it.

### 6. SKILL.md leanness

Flag runtime skills containing `Finish Tasks` or `Progress Log`; project state
belongs in the project note and audit history in `change_log`. Also flag a
skill above ~250 lines for manual compaction review.

### 7. Memory internal hygiene

- No credentials / tokens / passwords / API keys in any
  `80-agents/memory/internal/**/*.md`. Run a focused grep on
  `password|passwd|secret|api[_-]?key|token|AKIA|pwd` and flag any hit.
- Domain memories use `when_*_loaded`, not `always`.
- An internal memory outside the canonical global file may not declare `scope: global`; route it to its project, application, error or an explicit manual trigger.
- The single global internal memory stays below 1,000 approximate tokens and contains only transferable behavior or failure lessons. Project status, releases, hashes, execution IDs, task progress and domain-specific next steps are violations even when the file is in the allowed path.
- Notes marked `indexable: false` are also excluded via `.graphifyignore`
  (intent matches enforcement).
- A `continuity_key` has exactly one `memory_state: active` note. Active continuity uses an automatic scoped trigger; `superseded` and `archived` use `manual` or `never`, with low/never index priority; superseded notes require `superseded_by`.

### 8. Project ↔ skill consistency

- Skills referenced in `80-agents/skills/INDEX.md` exist on disk.
- Skills existing on disk appear in `INDEX.md`.
- Project notes claiming a skill is "pending" or "draft" match the skill's
  actual frontmatter state.

### 9. Resource wiki freshness

- Un dominio activo (definido por `00-index.md` con `status: active`) usa el
  casing exacto `00-index.md`, tiene un solo catálogo raíz y contiene `log.md`.
- Freshness sigue el contrato event-driven de
  `30-resources/00-RESOURCE-WIKI.md`; no reportar staleness sólo por falta de
  operaciones recientes.

### 10. Journal artifact naming

- Files in `80-agents/journal/sessions/`, `journal/sessions/raw/`,
  `journal/feedback/`, `journal/logs/` follow the canonical naming
  (`YYYY-MM-DD[-HHMM]-<human-topic>-*.md`). Flag UUID/hash-only filenames.

### 11. Startup token shape (smoke)

If shell is available and the agent can count tokens on the always-load set,
report the approximate startup token count and compare to soft benchmarks:

- Cold start: 3-6k tokens.
- Warm turn: <1k new tokens.
- Entity swap: 1-3k tokens for the new pack.

If shell isn't available, skip and note as "manual check needed".

## Procedure

1. Run the executable check, then any manual sections relevant to the request. Use focused reads; never dump the whole vault.
2. For each always-load item, classify every fact as transferable behavior or domain state. A fact is transferable only if it changes agent behavior across unrelated entities without carrying project identifiers or progress.
3. Move domain sources to `when_project_loaded`, `when_application_loaded`, `when_error_matches` or `manual`. Remove duplicated project ledgers from the global memory after verifying their canonical project, decision, known-error or runbook source.
4. For continuity, resolve `continuity_key` and prefer updating its active note in place. If a successor is necessary, require one active successor and retire the predecessor to `superseded` plus `manual` in the same patch.
5. Compact the global internal memory to behavior-level rules, below 1,000 approximate tokens. Do not preserve releases, hashes, execution IDs, completed-task history or project-specific next steps there.
6. Collect findings into the Output block with severity and propose the minimal fix for each HIGH/MEDIUM finding.
7. Do NOT apply fixes by default. List them and wait for approval; an explicit user request to sanitize or repair is approval for that stated scope.
8. Apply an approved fix set atomically and emit one consolidated `change_log` in `80-agents/journal/logs/`.
9. Reindex Graphify when indexed metadata or note bodies changed, then rerun Doctor strict and the Context Router E2E.

## Output

```text
Doctor run: YYYY-MM-DD HH:MM
Checks run: <count> · Passed: <count> · Findings: <count>

Findings by severity:
  HIGH:    <count>   (security, broken canonical path, contract violation)
  MEDIUM:  <count>   (drift, duplication, stale state)
  LOW:     <count>   (style, naming, freshness)

HIGH findings:
  - [<check-id>] <file>:<line> — <issue> · Fix: <one line>

MEDIUM findings:
  - [<check-id>] <file>:<line> — <issue> · Fix: <one line>

LOW findings:
  - [<check-id>] <file> — <issue>

Approved fixes applied: <count>
Change log: <path or "none">
Graphify freshness: <ok | recommend agents-os-graphify-maintenance>
```

## Hard Rules

- Read-only by default. Never auto-apply fixes.
- Use focused search (Grep/Glob); never scan the whole vault.
- One consolidated `change_log` per approved fix set, not one per file.
- Report severity honestly. Do not soften contract violations to "low".
- If a check cannot run (no shell, missing tool), say so explicitly in the
  output; do not silently skip.
