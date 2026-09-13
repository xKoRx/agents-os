---
type: skill
schema_version: 1
name: agents-os-session-close
scope: global
created: 2026-07-05
updated: 2026-09-12
description: Close an AGENTS OS session into reusable memory artifacts by delta. Use when the user says "cierra sesión", asks to persist session learnings, or invokes this skill by name. Decides what (if anything) to persist based on the session delta; default report is one or two lines.
aliases:
  - agents-os-session-close
entities:
  - "[[AGENTS OS]]"
  - "[[agents-os]]"
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - action/close
  - tech/agents-os
  - scope/global
---

# Agent Memory System Session Close

## Purpose

Close a session by **delta**, not by ritual. Decide what (if anything) needs
to persist, persist only that, and report to the user in one or two lines
unless they ask for detail.

Two surfaces are intentionally separate:

- **Persistence** — what AGENTS OS needs to keep.
- **Report** — what the user needs to see.

## Minimal Read

Canonical create: use `materialize_schema_note.py` per `note-types.md`; never hand-copy frontmatter.

Read only when needed:

- `../_shared/metadata-schema.md` for frontmatter.
- `../_shared/note-types.md` for artifact boundaries.

## Inputs

- Current session context.
- Main entity / project / application.
- External session identifier (when exposed by the surface). Belongs only in
  `source_session`, never in the filename.
- Canonical agent surface, exact host/user-reported model and attributable code-work segments, when code was generated or evaluated.

## Procedure

## Trigger Guard

Run only when one of these holds:

- The user explicitly asks to close the session ("cierra sesión", "cierra
  AGENTS OS", "cierra con detalle").
- The user asks to persist the session as closeout artifacts.
- The user invokes this skill by name.

Finishing a task, reaching a checkpoint, or noticing reusable knowledge is
NOT a trigger by itself.

## Delta Classifier

Select every row whose trigger is evidenced; most sessions match one. Act only
on those rows.

| Session delta | Action |
|---|---|
| No new knowledge or state | No artifacts. Report `Continuidad lista. Próximo paso: X.` |
| Operational continuity only | Update project/control note OR internal memory checkpoint, not both. No L0/L1. |
| Reusable knowledge (rule/decision/error/runbook/entity fact) | L3 + `change_log`; validate retrieval with one focused query (auto-refresh) |
| Transcript available or explicitly requested | L0; L1 only if it adds navigation beyond the project note |
| Real friction / degradation / gap detected | Brief feedback note (event-driven, see below) |
| Material code-generation/evaluation segment | Ensure one `agent_run` per attributable surface×model via `agents-os-agent-run-register`; this is independent from feedback and creates no L0/L1. |
| Explicit audit request | Show full inventory (L0 + L1 + L3 + feedback + logs + Graphify status) |

## Default Report

One or two lines. Do not enumerate artifacts created, updated, or skipped
unless the user asks for detail or an error/conflict needs a decision.

```text
Sesión cerrada. Continuidad lista. Próximo paso: <X>.
```

Nothing else by default. No tables of artifacts. No `L0 / L1 / L3 / feedback /
logs / Graphify / next tasks` inventory — that lives in the **detailed mode**.

## Detailed Mode

Triggered by `cierre con detalle`, an explicit audit request, or when a
conflict/error needs a human decision. Output the full inventory:

```text
Raw session:
Session summary:
Session feedback:
Learnings:
ADRs:
Known errors:
Runbooks:
Entity updates:
Conflicts:
Journal logs:
Graphify action:
Next tasks:
```

## Closeout Naming

When L0/L1 are created, use:

```text
80-agents/journal/sessions/raw/YYYY-MM-DD[-HHMM]-<human-topic>-raw.md
80-agents/journal/sessions/YYYY-MM-DD[-HHMM]-<human-topic>-summary.md
```

Rules:

- `<human-topic>` is lowercase kebab-case derived from the project, app, or
  session objective.
- `HHMM` only on same-day title collisions.
- External IDs, UUIDs, hashes go in `source_session` only.
- Never use a UUID/hash as the filename, prefix, H1, or human topic.
- L1 summaries live directly under `80-agents/journal/sessions/`; do not
  create sibling `summary/`, `summaries/`, or `system-1/` directories.

## Tactical Mode (subsumed by Delta Classifier)

The old "tactical mode" was a special case of the delta classifier. It
applies when **all** hold:

- The work was operational/tactical (code-review, debug, triage, lookup).
- No reusable rule, decision, known-error, runbook, or Sistema 2 fact emerged.
- The session's value is continuity, not canon.

In that case: keep the floor, skip the expensive tail. Optionally update
internal memory if there is real continuity delta (mandamiento 16 is
delta-based now, not mandatory per session). Skip feedback unless friction
was real. Skip L1/L3/entity unless real knowledge emerged.

When evidence is insufficient to classify knowledge as reusable, do not
inflate the close. Preserve only operational continuity and leave the
classification as an explicit follow-up if it can affect a future decision.

## Close Artifact Budget (soft ceiling + link, don't describe)

Ephemeral close scaffolding (L0 + L1 + feedback combined) targets a **soft
ceiling of ~1–1.5k tokens**. Smell-test, not guillotine. Hit it by **linking,
not truncating**:

- Reference entities, logs, and notes with `[[wikilinks]]`. The vault-aware
  graph (`graphify-obsidian`, Layer 2) resolves the link; the context is one
  hop away without padding the summary.
- Prefer link + one line over a paragraph.

**L3 memory is exempt.** Learnings, decisions, known-errors, runbooks are
reusable knowledge — write them (compact per their own rule) even if they
push past the ceiling. Trimming L3 to fit a number repeats the retrieval-cap
design error.

## Output

- Default: the 1-2 line report above.
- Detailed: the inventory block above.

## Hard Rules

- Do not run a full AGENTS OS close automatically at task completion. Wait
  for an explicit user closeout request. If continuity is needed without a
  closeout request, update the relevant project/control note or internal
  memory compactly instead of creating L0/L1/feedback.
- Persistence ≠ Report. The user does not need to see the inventory unless
  they asked for detail or a decision is needed.
- Decide artifacts by the delta classifier. Do not create more than the
  delta justifies.
- Create L0 only when transcript content is available or the user explicitly
  asks for a placeholder. Never create an empty L0 by ritual.
- Never use UUID/hash/external ID as filename, prefix, H1, or human topic.
- Never overwrite a canonical entity fact without a journal log.
- Feedback is event-driven (next section).

## Feedback (event-driven)

Create a feedback note ONLY when one of these holds:

- Real friction was encountered (tool failure, missing support, slow path).
- Retrieval was degraded and a workaround was needed.
- A gap in Sistema 1 was detected that the system does not solve.
- Periodic sampling (e.g. the hygiene cycle asks for one this week).

Do NOT create feedback just because the closeout ran. A clean session with
no friction → no feedback note.

When feedback is warranted:

- One general note under `80-agents/journal/feedback/system-1/` using
  `YYYY-MM-DD-<entity-or-topic>-session-feedback.md`.
- Graphify-specific feedback is captured during `agents-os-hygiene-cycle`
  aggregation, NOT as a second automatic note at every close. Only create a
  dedicated Graphify feedback note if Graphify was used AND something
  notable happened (degradation, novel query pattern, new pitfall).
- Keep answers short: 1-3 bullets per section. One Pain Pattern Candidate
  at most.

## Graphify Freshness

Query commands auto-refresh the local index, so a session that wrote canonical
notes normally needs no explicit rebuild. Validate with one focused query or
`explain "<exact title>"` for what this close created.

Recommend `agents-os-graphify-maintenance` only when:

- A query reports the index stale or auto-refresh failed.
- An explicit rebuild is justified (maintenance cadence, `.graphifyignore`
  change, mass move).
- An `update` blocked on findings outside this session's delta: classify
  delta-vs-global there; do not sanitize unrelated notes at close.

Tactical/no-artifact closes require no Graphify action.

## Agent Run Registration

Before final reporting, invoke `agents-os-agent-run-register` for every material coding/debug/review/testing segment from the session that is not already recorded. A model switch or cross-surface handoff creates separate runs; never infer an unreported model. Runs are journal evidence, not session feedback, and do not require Graphify reindex by themselves.
