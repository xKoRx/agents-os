---
type: continuity
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[A — Technical SPEC D1]]"
  - "[[B — Implementation Plan D1]]"
  - "[[C — Test Plan D1]]"
  - "[[D — Acceptance Gate D1]]"
tags: [kind/continuity, area/echo, the-lab, d1]
created: "2026-09-23"
updated: "2026-09-23"
---
# F — Continuity D1

## Three-shot execution model

Only three development-manager turns are planned for D1:

### Shot 1 — IMPLEMENTATION
One autonomous developer implements the full Echo D1 foundation, runs its own tests, persists evidence, closes Agents-OS session and returns a structured report.

### Shot 2 — INDEPENDENT VERIFICATION
A fresh agent starts from canonical docs and implementation commit, performs adversarial review/tests against the acceptance gate, does not trust Shot 1 claims, persists evidence, closes session and returns PASS/FAIL with exact findings.

Default: verifier does not redesign the solution. It may apply only trivial test harness/evidence fixes if they do not change product behavior; product-code defects are reported for Shot 3.

### Shot 3 — CORRECTION + FINAL GATE
A fresh developer receives Shot 2 findings, fixes all valid defects without reopening frozen decisions, reruns the complete required suite, persists final evidence, closes session and returns final D1 status.

No fourth planned shot. If Shot 3 uncovers a genuine frozen-decision contradiction, manager decides explicitly; otherwise the agent owns correction to completion.

## Handoff contract for every agent

Each agent MUST:
- load current Agents-OS canonical instructions first;
- read D1 A-F + Decision Register + Revised Roadmap;
- verify actual Echo branch/HEAD/worktree;
- work only in Echo/Agents-OS evidence unless specifically authorized;
- solve normal implementation obstacles autonomously;
- not ask the owner routine technical questions;
- not change M01-M12 or D1 SPEC;
- run required tests;
- write exact evidence/feedback to Agents-OS;
- close the Agents-OS session using the canonical session-close procedure;
- return concise structured summary: baseline, commit, files, tests, evidence, blockers/deviations, next action.

## Manager rule

The manager/TL (this planning session) evaluates each returned report against [[D — Acceptance Gate D1]] and writes the next one-shot mandate. Agent claims are evidence inputs, not automatic PASS.
