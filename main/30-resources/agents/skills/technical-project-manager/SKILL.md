---
type: skill
schema_version: 1
name: technical-project-manager
description: Plan and drive a bounded technical initiative as a short delivery horizon of daily atomic milestones, each independently verifiable and ideally promotable, then manage each day through frozen design plus one-shot implementation, independent verification, and correction/final gate. Use when the owner asks an agent to act as technical manager/TL across multiple days or coordinate autonomous development agents toward same-day measurable outcomes. Do not use for a trivial single change, a validation-only session, or release/deployment certification by itself.
scope: transversal
created: "2026-09-23"
updated: "2026-09-23"
entities: []
related:
  - "[[agents-os-implementation-planning]]"
  - "[[sdd-workflow]]"
  - "[[e2e-gated-validation]]"
  - "[[release-certification]]"
  - "[[deployment-proof]]"
  - "[[agents-os-agent-run-register]]"
  - "[[agents-os-session-close]]"
aliases:
  - project-technical-manager
  - technical delivery manager
  - daily gated delivery
  - technical manager tl
load_policy: manual
indexable: true
index_priority: critical
tags:
  - kind/skill
  - scope/transversal
  - tech/agents-os
  - action/project-management
  - action/orchestrate
---

# Technical Project Manager

## Purpose

Turn a bounded technical initiative into a short sequence of daily outcomes, then manage each day as an independently testable delivery unit with frozen scope, autonomous execution, adversarial verification, correction and a final gate.

## Minimal Read

Read only:

1. Active project/roadmap, current decisions and repository instructions.
2. Current certified baseline and evidence for dependencies of today's milestone.
3. `80-agents/skills/agents-os-implementation-planning/SKILL.md` when the initiative or today's slice still needs implementation architecture.
4. `30-resources/agents/skills/sdd-workflow/SKILL.md` when the repo uses SDD or specification/plan/tasks must remain separated.
5. Release/deployment/validation skills only when today's gate includes promotion beyond source code.

## Inputs

- Desired outcome and delivery horizon (days or bounded sessions).
- Time available for the current day.
- Repositories/entities in scope and certified starting baseline.
- Frozen owner decisions, non-goals and external dependencies.
- Available autonomous agents/surfaces and their authority limits.

## Procedure

### 1. Build the delivery horizon

1. Define the end-of-horizon product outcome and explicit non-goals.
2. Work backward into daily milestones. Each day MUST end in an observable capability, not an activity such as "work on backend".
3. Admit a daily milestone only when it is:
   - atomic enough to finish inside the available window;
   - independently testable with objective evidence;
   - useful as a stable baseline for the next day;
   - reversible or safely containable on failure;
   - ideally promotable/deployable without unfinished future code.
4. Separate capability gates from external integration gates. An independent producer, environment or team may block integration without invalidating an internally complete capability.
5. If a milestone cannot preserve meaningful verification and correction time, split, reduce or reorder it before development begins.
6. Record the horizon in the canonical project/roadmap. Future days keep outcome, dependency and gate only; do not pre-design their implementation in detail.

### 2. Freeze today's milestone

Before dispatching implementation:

1. Inspect only code/evidence necessary for today's outcome.
2. Close owner-level product, architecture and durable-data decisions. The manager/TL resolves ordinary technical choices without escalating them.
3. Freeze:
   - certified baseline;
   - outcome and non-goals;
   - allowed repositories/files or bounded discovery surface;
   - contracts/data model/semantic decisions that executors may not change;
   - technical freedom executors retain;
   - acceptance evidence and fail conditions;
   - production posture: `SOURCE_ONLY`, `READY_TO_PROMOTE`, or an explicitly authorized release/deploy gate.
4. Persist a daily execution package appropriate to the repo: SPEC/design, implementation plan, test plan, acceptance gate, impact/continuity. Use existing SDD/project artifacts instead of duplicating them.
5. Do not start Shot 1 while a business/architecture decision required by today's implementation remains open.

### 3. Execute the three-shot day

#### Shot 1 — Implementation

Dispatch one autonomous implementation mandate against the frozen package.

The mandate MUST provide authorities, baseline, frozen decisions, scope/non-goals, technical freedom, blocker policy, mandatory tests, evidence/Agents-OS closeout and structured response. Treat the executor as senior: allow local implementation/refactoring decisions that do not alter frozen semantics.

The executor may test its own work, but its PASS is only a candidate.

#### Shot 2 — Independent verification

Use a fresh context/agent. It MUST:

- verify the exact implementation commit rather than trust Shot 1;
- attempt to falsify the acceptance gate with independent tests/probes;
- compare relevant regressions to baseline;
- avoid fixing product code while auditing;
- report reproducible findings with severity, expected/actual and narrow correction.

Manager/TL reviews findings and freezes the accepted correction scope.

#### Shot 3 — Correction + final gate

Use a fresh implementation context to:

- fix all accepted findings without reopening frozen definitions;
- convert valuable reproducers into permanent regression tests;
- rerun the complete affected gate;
- review the final diff against the Shot 1 candidate;
- emit the final day verdict and exact certified commit.

If Shot 2 finds no defects, Shot 3 becomes reconciliation + full final gate. Do not plan a fourth shot; normal defects discovered in Shot 3 are corrected within that shot. Escalate only a genuine contradiction requiring an owner decision.

### 4. Close or promote the day

1. Final status is one of:
   - `DAY_PASS`: capability certified at an exact commit.
   - `DAY_FAIL`: material defect remains.
   - `DAY_BLOCKED_DECISION`: an owner decision is genuinely required.
   - `DAY_BLOCKED_EXTERNAL`: internal capability is complete but the separately named integration dependency is unavailable.
2. On `DAY_PASS`, make the certified commit the only baseline for the next milestone; do not build tomorrow from an earlier or unverified branch.
3. Keep source/capability PASS separate from production state.
4. When promotion is authorized, hand off in order as applicable:
   - `release-certification` for source→release integrity;
   - `deployment-proof` for release→runtime proof;
   - `e2e-gated-validation` for the production/physical product gate.
5. Update project/roadmap with outcome, certified baseline, evidence, unresolved external risks and the next day's exact milestone.

### 5. Manage the horizon continuously

At each new day:

1. Start from yesterday's accepted baseline and real evidence.
2. Revalidate only assumptions that materially changed.
3. Replan remaining daily milestones when reality changed; preserve the end outcome, not a stale calendar.
4. Never hide a missed gate by moving unfinished scope silently into the next day.
5. Close the project horizon only when its final outcome has an explicit product gate; completion of all planned activities is insufficient.

## Output

```text
Horizon outcome:
Certified starting baseline:

Daily milestones:
  Day <n>: <observable outcome> — gate: <objective evidence> — promotion: <posture>

Today:
  Outcome:
  Frozen decisions:
  Execution package:
  Shot 1: PENDING|CANDIDATE|FAIL
  Shot 2: PENDING|PASS|FINDINGS
  Shot 3: PENDING|PASS|FAIL
  Final status: DAY_PASS|DAY_FAIL|DAY_BLOCKED_DECISION|DAY_BLOCKED_EXTERNAL
  Certified commit:
  Promotion state:

Next exact milestone:
Residual external risks:
```

## Hard Rules

- A day is defined by a product/capability outcome, never by hours spent, files changed or agent activity.
- Do not admit a daily milestone that cannot be objectively tested and closed inside the available window with correction reserve.
- Do not let the implementation agent accept its own gate.
- Verification uses a fresh context and tries to falsify the result; rerunning only Shot 1 tests is insufficient.
- Frozen product, architecture, contract and durable-data decisions cannot be changed by executors to make implementation easier.
- Keep ordinary technical freedom with senior executors; do not turn mandates into line-by-line coding instructions.
- Keep internal capability gates separate from independent producer/environment/release gates.
- Do not over-design future days; detail is frozen just in time at the start of the active day.
- Do not carry an unaccepted implementation forward as the next baseline.
- `DAY_PASS` does not mean production. Production claims require the applicable release/deployment/E2E evidence and explicit authorization.
- Do not manufacture PASS with synthetic evidence when the gate explicitly requires authentic/runtime evidence.
