---
type: skill
schema_version: 1
name: agents-os-implementation-planning
scope: global
created: 2026-07-23
updated: 2026-08-10
description: Produce a repository-evidenced, phase-gated implementation plan inside an owner:agent project so lower-cost or lower-capability executor agents can implement one phase at a time without rediscovering architecture or making implicit decisions. Use when planning a complex implementation, converting research into autonomous phase packages, preparing handoffs between planner and executor agents, or auditing whether a plan is safe to delegate.
entities:
  - "[[AGENTS OS]]"
related:
  - "[[Planner-Executor Implementation Standard]]"
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - action/implementation-planning
  - tech/agents-os
  - scope/global
---

# AGENTS OS Implementation Planning

## Purpose

Create one durable implementation project whose phase packages can be executed by separate agents without hidden discovery, semantic invention, or cross-phase scope drift.

## Minimal Read

Canonical create: use `materialize_schema_note.py` per `note-types.md`; never hand-copy frontmatter.

Read only:

1. `../agents-os-agent-project-workflow/SKILL.md`.
2. `references/phase-plan-contract.md`.
3. Repository instructions and the active project/entity note.
4. Sources selected through focused retrieval; do not preload the repository or vault.

## Inputs

- Canonical project/entity and repository path.
- Desired outcome and explicit non-goals.
- Intended executor capability/context constraints.
- Available code, tests, contracts, runtime evidence and human decisions.

## Procedure

1. Resolve or create one `owner: agent` project through
   `materialize_schema_note.py`; use its note as the only durable planner.
2. Capture repository reality before designing:
   - branch, HEAD, recent relevant commits and versions;
   - tracked, modified, deleted and untracked files;
   - generated artifacts, stubs, tests, production code and documentation as separate evidence classes.
3. Follow this evidence order:
   - executable code and tests;
   - runtime/configuration contracts;
   - implementation reports;
   - roadmap and historical notes.
4. Trace symbols, callers, data formats, correlation IDs and system boundaries. Record exact existing-file/symbol references in the project.
5. Build a requirement-to-evidence matrix. Classify each item `done`, `partial`, `replaced`, `missing` or `blocked`.
6. Freeze semantics before implementation:
   - obtain human answers for business definitions;
   - record technical resolutions separately;
   - convert unknown API/runtime capabilities into a bounded Phase 0 spike with expected evidence;
   - do not declare the plan ready while a business decision remains open.
7. Write the target architecture, sequence, data contracts, formulas, edge cases, error taxonomy, idempotency, rollout and rollback in the project note.
8. Decompose work by dependency and independently verifiable boundaries. Use one agent/context per phase and balance by uncertainty, integration surfaces, testing and operational risk rather than LOC.
9. Create every phase using `references/phase-plan-contract.md`. A phase must state what to read, what is already decided, exact steps, files/symbols, `No tocar`, allowed spikes, tests, deliverables, gate and handoff.
10. Add atomic tasks and a gate-control table. The phase agent leaves its gate in `review`; only the owner can persist `accepted` and enable the next phase.
11. Create one common executor prompt plus exactly one dispatch block per phase. Never send all dispatch blocks as the active assignment.
12. Validate:
    - run `python3 scripts/validate_plan.py <project-note>`;
    - verify all local references and line anchors;
    - reconcile phase/task/gate/dispatch cardinality;
    - confirm no open decision row remains in a ready plan;
    - use a fresh executor-context test when available.
13. Update project state, tasks and Bitácora. Record `ready_for_phase_0` only after validation passes.

## Output

```text
Project planner:
Repository baseline:
Requirement/evidence matrix:
Decisions closed/open:
Phases and relative load:
Gate table:
Executor prompt:
Dispatch blocks:
Validation command/result:
Ready phase:
Residual technical risks:
```

## Hard Rules

- Keep the implementation plan in the agent-project note; do not create a competing planner.
- Do not ask an executor to rediscover architecture, contracts, formulas or business semantics.
- Reference existing evidence by verified file, symbol and line when stable; mark future paths explicitly as `create`.
- Do not present local changes, generated artifacts, stubs or historical reports as HEAD production evidence.
- Do not invent fields, thresholds, formulas, fallbacks or requirements.
- Assign every technical unknown to one bounded spike with inputs, outputs and stop conditions.
- Do not combine two phases in one executor context.
- Do not let a phase accept its own gate or start the next phase.
- Stop on contradictory executable evidence with `PLAN_CONFLICT`; update the planner before continuing.
- Preserve unrelated working-tree changes; never require destructive Git cleanup.
- Keep AGENTS OS `type/tags/routing` frontmatter canonical; do not strip it to satisfy a client-specific validator with a narrower schema.
