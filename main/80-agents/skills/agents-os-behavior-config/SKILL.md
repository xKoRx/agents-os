---
type: skill
schema_version: 1
name: agents-os-behavior-config
scope: global
created: 2026-06-27
updated: 2026-08-10
description: Configure Agent Memory System behavior through conversation. Use when the user changes how agents should behave, asks the agent to remember a preference, updates constitution rules, adjusts user profile, promotes internal memory to public memory, or gives session-scoped operating instructions that must be classified as temporary or persistent.
aliases:
  - agents-os-behavior-config
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/skill
  - action/config
  - tech/agents-os
  - scope/global
---

# Agent Memory System Behavior Config

## Purpose

Turn conversational instructions into the right behavior layer without corrupting memory. Decide whether an instruction is session-only, user preference, constitution, public reusable memory, internal agent memory, or a Sistema 2 entity update.

## Minimal Read

Canonical create: use `materialize_schema_note.py` per `note-types.md`; never hand-copy frontmatter.

Read only when needed:

- `../_shared/metadata-schema.md` for frontmatter and load policies.
- `../_shared/note-types.md` for Sistema 1/Sistema 2 boundaries and internal memory rules.
- Existing target notes before editing:
  - `80-agents/agents-os/agent-constitution.md`;
  - the always-load global profile under `80-agents/memory/public/user-preference/`;
  - relevant notes under `80-agents/memory/internal/`.

## Inputs

- User instruction or observed stable preference.
- Active entity/project/application.
- Evidence strength: explicit user request, repeated behavior, successful workflow, or agent hypothesis.

## Procedure

1. Capture the instruction as a concrete behavior change.
2. Classify the target:
   - session-only directive;
   - user preference;
   - constitution/global agent rule;
   - public L3 memory: learning, decision, known error, runbook, command, pattern;
   - internal agent memory;
   - Sistema 2 entity update.
3. Apply the narrowest durable layer:
   - session-only directives are obeyed now and not persisted;
   - user preferences go to the always-load global profile;
   - global rules go to `agent-constitution.md`;
   - reusable operational facts go through `agents-os-memory-distillation`;
   - canonical current facts go through `agents-os-entity-update`;
   - conflicts go through `agents-os-conflict-resolution`;
   - agent-only heuristics or continuity go to internal memory.
4. Before editing public memory or Sistema 2, check for duplicates or conflicts with focused Graphify/search.
5. Edit directly only when the target is unambiguous and evidence is high or verified.
6. Create a `type: change_log` entry for every public memory, constitution, user preference, or Sistema 2 change.
7. Reindex through `agents-os-graphify-maintenance` when changed notes are indexable.
8. Report what changed and what was intentionally treated as temporary.

## Persistence Rules

Session-only:

- Current command preferences, task constraints, temporary exclusions, or "do not close yet".
- Do not write to memory unless the user explicitly says to remember it or it reveals a stable rule.

User preference:

- Stable interaction style, working style, validation style, language, update cadence, or memory preference.
- Cross-domain directives use the single resolved global profile:
  `scope: user`, `load_policy: always`.
- Domain-specific directives use the matching scope and `when_*_loaded`
  policy; do not inflate the global profile.

Constitution:

- System-wide rules that should bind all future agents in this vault.
- Use sparingly; constitution changes should be explicit or strongly implied by a stable project decision.

Internal memory:

- Agent-to-agent continuity, heuristics, hypotheses, private operating notes, and compact plans.
- No public log is required unless the content is promoted to public memory or changes Sistema 2.

Public L3 memory:

- Reusable behavior-affecting knowledge with entity scope, load policy, and confidence.
- Must pass the memory-distillation promotion test and create a journal log.

## Internal-To-Public Promotion

Promote internal memory only when all are true:

- it should affect humans or future agents beyond private reasoning;
- it is stable enough to be shared as a rule, decision, learning, known error, runbook, command, or pattern;
- it has a clear entity scope and evidence;
- duplicate/conflict checks are complete.

Promotion workflow:

1. Open the internal source note and identify the exact claim to promote.
2. Choose the public target type using `agents-os-memory-distillation`.
3. Create or update the public memory note.
4. Leave the internal note intact or compact it to point at the public note.
5. Create a journal log with source internal note, new public target, evidence, and reason for promotion.
6. Reindex and validate focused retrieval for the public target.

## Output

```text
Instruction:
Classification:
Applied change:
Temporary directives:
Public memory changes:
Internal memory changes:
Entity updates:
Journal logs:
Graphify action:
Deferred:
```

## Hard Rules

- Do not persist every user utterance as preference.
- Do not put temporary session constraints into always-load memory.
- Do not expose or quote internal memory unless the user explicitly asks or audit requires it.
- Do not update constitution for narrow personal preference; use user preference instead.
- Do not update public memory, constitution, user profile, or Sistema 2 without a journal log.
