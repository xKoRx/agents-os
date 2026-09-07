---
type: doc
schema_version: 1
status: active
created: 2026-06-27
updated: 2026-09-03
tags:
  - kind/doc
  - kind/system
  - tech/agents-os
---

# AGENTS OS System Types

Use this file when deciding where knowledge belongs.

## Propósito

Definir la frontera entre artefactos de Sistema 1 y entidades de Sistema 2.

## Contenido

## Boundary Rule

```text
Describes how agents remember/learn/work -> Sistema 1 memory
Describes what is real/current in vault  -> Sistema 2 entity
```

AGENTS OS uses a Kahneman-inspired naming model:

- **Sistema 1**: memory and learning system. It stores agent memory, public
  reusable learnings, decisions, known errors, runbooks, commands, patterns,
  raw sessions, summaries, change logs, and **skills** (the agent's operating
  procedures — see boundary below).
- **Sistema 2**: real-entity system. It stores canonical notes for real vault
  entities: projects, areas, applications, services, technologies, workflows,
  integrations, concepts, tools, and other current-truth documents.

Use Sistema 1 and Sistema 2 in new docs and skills. Do not introduce parallel
layer names for this boundary.

## Skill vs Reusable Memory (Learning/Decision/Known Error/Runbook)

Both live in Sistema 1, but they answer different questions and must not be
mixed into the same note. Confusing them makes retrieval noisy (a skill full
of narrative facts, or a learning full of step-by-step procedure) and makes
future agents load the wrong thing at the wrong time.

```text
Skill              -> a repeatable HOW. A procedure the agent actively selects
                      and follows to perform a class of task correctly.
Learning           -> a repeatable WHY-CARE. A conclusion that should silently
                      bias judgment when loaded, without being a full procedure.
Decision / ADR     -> WHY current behavior/design exists; rationale and
                      discarded alternatives.
Known Error        -> a repeatable FAILURE: symptom, cause, impact, mitigation.
Runbook            -> a narrow, mechanical, validated command/step sequence for
                      one specific recurring operation.
```

Rule of thumb:

- If it is a **procedure spanning multiple judgment calls**, invoked on demand
  to perform or orchestrate a class of task (e.g. "how to close a session",
  "how to operate an agent project") -> **skill**, under `80-agents/skills/`.
- If it is a **fact, insight, or rule of thumb** that should change future
  behavior when loaded as passive context, but is not itself a multi-step
  procedure -> **learning** (or `decision`/`known_error` per its more specific
  shape), under `80-agents/memory/public/`.
- If it is a **narrow, mechanical, validated command sequence** for one
  specific recurring operation -> **runbook**. A skill may reference or create
  runbooks as part of a broader procedure; a runbook does not itself decide
  when to be invoked.

Do not fold a skill's step-by-step procedure into a learning note (it will
read like narrative advice instead of an actionable procedure and will not be
selected/invoked the way skills are). Do not fold a one-off decision's
rationale into a skill (skills are for repeated procedures, not single
choices — a one-off choice belongs in `decision`).

## Internal Continuity Memory

- Internal continuity is a scoped checkpoint, not a session transcript or project ledger.
- Use one stable `continuity_key` per entity or concern and keep exactly one `memory_state: active` note for that key.
- The normal handoff updates the active note in place: remove obsolete progress, preserve only the current durable state and keep its concrete `load_policy`.
- Create a successor only when the scope or canonical identity changes materially. Then mark the prior note `memory_state: superseded`, set `load_policy: manual`, lower `index_priority`, link `superseded_by`, and link the successor with `supersedes`.
- `archived` memories are historical evidence and never enter normal retrieval. Missing lifecycle fields are legacy: do not bulk-load them and migrate them only when touched.

## Template Policy

Every new S1/S2 document must resolve its canonical template and current
`schema_version` through `schema-contract.md`. Fragment and derived exemptions
are valid only when that contract records an explicit reason.

Procedure:

1. Identify the Sistema 2 entity type before writing.
2. Resolve the exact `type → template` mapping in `schema-contract.md`.
3. Materialize with
   `python3 80-agents/skills/_shared/scripts/materialize_schema_note.py <type> <vault-relative-target.md>`;
   never hand-copy template frontmatter.
4. Fill task-relevant placeholders and run targeted lint on the result.
5. If the mapping or template is missing, update the contract and create the
   template first or in the same change; the contract validator must pass.
6. Log the template creation when it changes AGENTS OS operating rules or when
   it materially affects future agents.

Sistema 1 templates live under `80-agents/templates/`; Sistema 2 templates
live under `70-templates/`. The validator rejects boundary crossings,
unmapped templates and duplicate canonical mappings.

## L0 Raw Session

Complete session transcript supplied by the user.

- Purpose: audit, retrofit, traceability.
- Indexing: never by default.
- Load policy: never.
- Location: `80-agents/journal/sessions/raw/`.
- Must not contain heavy logs/dumps; store references instead.

## L1 Session Summary

Distilled summary of a session.

- Purpose: human/agent recap and bridge to L3.
- Indexing: excluded from the normal Graphify corpus.
- Location: `80-agents/journal/sessions/`.
- Should link raw session, entities, learnings, decisions, known errors.
- If a later phase includes summaries in retrieval, change them to `indexable: true` and `index_priority: low` with an explicit decision/log.

## Session Feedback

Structured evaluation note written by the acting agent at session close.

- Purpose: expose AGENTS OS friction, useful pieces, noisy pieces, missing
  support, and improvement candidates.
- Indexing: excluded from the normal Graphify corpus by default.
- Location: `80-agents/journal/feedback/system-1/`.
- Template: resolve the canonical mapping in `schema-contract.md`.
- Promotion: repeated or high-severity patterns may be promoted later to L3
  learning, known error, runbook, or ADR through memory distillation.
- Must not contain secrets, heavy evidence, or private chain-of-thought.

## Agent Run

Registro compacto de una ejecución de código atribuible a una combinación superficie×modelo.

- Purpose: evidence for later comparison of coding surfaces and models without selecting only sessions that had friction.
- Location: `80-agents/journal/agent-runs/`.
- Identity: `agent_surface` links a canonical `type: agent` profile; `agent_model` preserves the exact host/user-reported identifier.
- Granularity: one record per materially attributable surface×model segment; a model switch creates another record.
- Evidence: outcome, verification and user rework are primary; scores are optional and declare their evaluator.
- Indexing: excluded from normal Graphify retrieval with the rest of the journal; dashboards aggregate the frontmatter directly.
- Procedure: [[agents-os-agent-run-register]].

## Graphify Feedback

Structured evaluation note written by the acting agent focused solely on Graphify's utility and accuracy.

- Purpose: capture Graphify queries, budgets, synonym resolution efficiency, template noise, and token savings.
- Indexing: excluded from the normal Graphify corpus.
- Location: `80-agents/journal/feedback/graphify/`.
- Specialized derived template: recorded explicitly in `schema-contract.md`.
- Promotion: used by the Kaizen memory skill to optimize `.graphifyignore`, aliases, and query strategies.

## Sistema 2 Entity

Canonical note for a real thing: project, application, service, area, technology, workflow, integration, concept, or idea.

- Answers: what it is, current state, responsibilities, integrations, rules.
- Indexing: high priority.
- Has one canonical Obsidian title. Variants belong in `aliases`; automation
  identifiers belong in `slug`, tags, and semantic paths.
- Routing metadata that points to entities uses canonical links, not raw slugs.
- Should link related memory, but not become a session diary.

### Idea

Small, atomic Sistema 2 note for a possible validation, improvement, risk, or opportunity.

- Location: `30-resources/ideas/`.
- Template: resolve the canonical mapping in `schema-contract.md`.
- Must route to at least one area and, when known, application/project/entities.
- Should stay short: observation, motive, classification, related links, and one next action.
- Promotion path: keep as `seed/exploring` while uncertain; promote to task or project when it requires real execution.

## Sistema 1 Memory

Reusable operational knowledge.

### Learning

Reusable conclusion that should change future behavior.

Create only when it has scope and load policy.

### Decision / ADR

Decision and rationale. Explains why current behavior exists.

Do not replace the current canonical fact in the entity note; link both.

### Known Error

Repeatable failure, symptom, cause, impact, detection, mitigation.

Use when a future agent can avoid or diagnose the failure.

### Runbook

Validated operational procedure.

Use for repeated commands, release routines, checks, migrations, or recovery steps.

### Command / Pattern

Reusable operational snippet or repeated implementation pattern.

Use only when it is stable enough to help future sessions and too small to deserve a full runbook.

### Agent Memory

Internal agent memory: heuristics, hypotheses, plans, and continuity notes used by future agents.

Store in `80-agents/memory/internal/`. This memory is exclusive to the agent: it is a place for thoughts, internal continuity, agent-to-agent communication, private operating structure, and any rules or content the agent chooses for its own future use.

Rules:

- The agent governs its internal memory structure, names, formats, and content.
- Do not expose, summarize, or cite internal memory to the user unless explicitly requested or needed for audit.
- Do not use internal memory as public documentation, a canonical entity, an ADR, or a public-memory log.
- Promote internal memory to public memory only when it should affect the shared system; log that promotion when it changes public memory or canonical entities.
- Keep it compact; use `load_policy: always` only when it is truly worth initial context budget.

### Conflict

Explicit contradiction found between new information and existing Sistema 1 or
Sistema 2 knowledge.

The agent resolves with available context, updates affected notes, and records the change as `type: change_log` in `80-agents/journal/logs/`. Do not model conflict with a `status` field.

## Rejection Rules

Do not create L3 memory for:

- one-off implementation progress;
- raw command output;
- temporary debugging notes;
- vague advice without an entity or scope;
- facts that belong only in a canonical Sistema 2 entity update.
