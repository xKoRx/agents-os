---
type: skill
schema_version: 1
name: sdd-developer
description: Execute a ready SDD feature/change through autonomous implementation, independent adversarial verification, correction and final gate while preserving reusable regression/E2E assets and feeding repeatable agent behavior into Agents-OS feedback. Use when SPEC/PLAN/TASKS are ready and a fresh coding agent must deliver an SDD slice or feature to a certified commit. Do not use to create the initial specification/plan/tasks or for validation-only/release-only work.
scope: global
created: "2026-09-23"
updated: "2026-09-23"
entities: []
related:
  - "[[sdd-workflow]]"
  - "[[compounding-engineering-vision]]"
  - "[[technical-project-manager]]"
  - "[[e2e-gated-validation]]"
  - "[[agents-os-agent-run-register]]"
  - "[[agents-os-session-feedback]]"
  - "[[agents-os-session-close]]"
aliases:
  - sdd developer
  - sdd implementation agent
  - sdd three-shot developer
load_policy: manual
indexable: true
index_priority: critical
tags:
  - kind/skill
  - scope/global
  - tech/agents-os
  - action/sdd
  - action/development
  - action/verification
---

# SDD Developer

## Purpose

Deliver a ready SDD unit as a certified commit using a three-shot implementation loop: autonomous implementation, fresh-context adversarial verification, then correction plus final gate. Preserve executable product knowledge as tests/harnesses and report repeatable agent/process knowledge as feedback candidates for later Hygiene/Kaizen promotion.

## Minimal Read

Read only:

1. `30-resources/agents/skills/sdd-workflow/SKILL.md`.
2. The active feature's `SPEC.md`, `PLAN.md`, `TASKS.md`, `VERIFICATION.md` and repository instructions.
3. The exact certified repository baseline and only the code/tests needed by the active task.
4. `30-resources/agents/skills/e2e-gated-validation/SKILL.md` only when the acceptance gate includes a physical/runtime E2E.
5. Agents-OS run/feedback/close skills at closeout.

## Inputs

- SDD feature/change identifier.
- Ready SPEC/PLAN/TASKS and active task(s).
- Certified starting commit.
- Frozen business/architecture/data-contract decisions.
- Acceptance criteria and required evidence.
- Repository test surfaces: package tests, integration tests, canonical E2E module and reusable toolkit/test-support, when present.

## Procedure

### 1. Confirm SDD readiness

1. Verify SPEC, PLAN and TASKS are ready and internally consistent.
2. Resolve the exact active task/slice and its acceptance criteria.
3. If implementation requires inventing unresolved business semantics or architecture, stop with `SDD_NOT_READY` and return the gap to SPECIFY/PLAN through `sdd-workflow`.
4. Freeze baseline, write scope, non-goals and existing behavior that must not regress.

### 2. Build the one-shot master mandate

Every Shot 1/2/3 mandate is fresh-context and self-contained. It MUST contain these literal semantic sections:

```text
/goal
/authorities
/baseline
/frozen
/scope
/execute
/verify
/reuse
/improve
/close
```

These are prompt sections, not assumed IDE commands.

- `/goal`: one observable end state and explicit PASS/FAIL gate. Never "advance", "work on" or "investigate" as the final goal.
- `/authorities`: SPEC/PLAN/TASKS/VERIFICATION plus repository instructions.
- `/baseline`: exact certified commit/branch and relevant dependency state.
- `/frozen`: decisions the executor may not change to make coding easier.
- `/scope`: allowed discovery/write boundary and explicit non-goals.
- `/execute`: autonomous task; ordinary technical obstacles are solved inside the shot.
- `/verify`: mandatory tests/evidence and regression comparison.
- `/reuse`: classify new tests/probes/harnesses and preserve durable assets.
- `/improve`: evaluate repeatable agent/process behavior; `NONE` is valid. Persist feedback only when a concrete candidate meets the feedback trigger.
- `/close`: agent-run, SDD artifacts/status, journal/change-log as applicable, Agents-OS closeout and structured final response.

Do not complete a shot through conversational micro-prompts. A one-shot may only return to the owner for a genuine frozen-decision contradiction.

### 3. Shot 1 — IMPLEMENT

Use a fresh senior implementation context.

It MUST:

- implement only the active SDD slice;
- add normal unit/integration tests required by the SPEC;
- execute the declared gate;
- record exact changed files/commits/test commands;
- update SDD task/evidence without self-accepting the feature;
- classify reusable artifacts created during implementation.

Shot 1 output is `IMPLEMENTATION_CANDIDATE`, never final acceptance.

### 4. Shot 2 — VERIFY adversarially

Use a fresh context that does not trust Shot 1 and does not fix product code.

The verifier MUST:

1. verify the exact candidate commit and diff against baseline;
2. derive tests from acceptance criteria and invariants, not only from Shot 1's tests;
3. attack boundaries relevant to the feature: invalid inputs, persistence, concurrency, retries/idempotency, tenancy/auth, time/precision, rollback, error classification, compatibility and side effects as applicable;
4. independently recompute critical derived values when reusing product helpers would make the test tautological;
5. compare alleged regressions against the certified baseline;
6. produce exact reproducible findings with severity, expected/actual and minimal correction;
7. classify every new verifier artifact as:
   - `PERMANENT_REGRESSION`
   - `E2E_CANDIDATE`
   - `HARNESS_TOOLKIT_CANDIDATE`
   - `DISPOSABLE_REPRODUCER`.

Shot 2 owns falsification, not implementation.

### 5. Shot 3 — CORRECT + FINAL GATE

Use a fresh implementation context.

It MUST:

1. fix only manager/owner-accepted Shot 2 findings;
2. preserve frozen SDD semantics;
3. convert valuable verifier reproducers into permanent executable assets;
4. rerun the complete affected suite and independent critical probes;
5. review the final diff against both baseline and Shot 1 candidate;
6. update `VERIFICATION.md` with the final acceptance matrix;
7. emit the exact certified commit and final status.

Normal defects found inside Shot 3 are corrected and re-tested within Shot 3. Do not plan a fourth shot.

### 6. Own E2E by SPEC without putting code in docs

A SPEC owns its verification logically; executable tests remain in canonical code/test modules.

For each acceptance criterion maintain in the feature `VERIFICATION.md`:

```text
AC / invariant → executable test path → test name/scenario → evidence/status
```

Placement rules:

- package-local invariant → owning package `*_test.go`;
- DB/HTTP/component integration invariant → owning integration test package;
- stable cross-component behavior → canonical E2E module, preferably grouped by feature/spec ID when the repository supports it, e.g. `v3/e2e/specs/<SPEC-ID>/`;
- reusable setup/validators/builders → canonical toolkit/test-support owner;
- SPEC directory → specification, plan, tasks, verification manifest, fixtures/data only when repository policy explicitly allows them; do not hide executable application test code under documentation paths.

A per-SPEC E2E directory is a repository convention to adopt deliberately, not a universal requirement. If no canonical E2E owner exists, first define ownership in PLAN rather than creating a competing framework.

### 7. Harvest executable knowledge

Before final PASS, inventory all tests/probes/scripts/helpers created by Shots 1–3.

Promote when:
- the asset protects a durable product invariant;
- it is deterministic/repeatable enough for CI or a documented local gate;
- ownership is clear;
- it materially reduces future rediscovery.

Verifier tests that caught a real defect are presumed valuable permanent regressions unless a documented reason rejects them.

Do not keep duplicate tests merely because different agents wrote them; merge equivalent coverage while preserving the stronger invariant.

### 8. Harvest repeatable agent behavior

At each shot close:

1. register the material execution through `agents-os-agent-run-register`;
2. return `REUSABLE_BEHAVIOR_CANDIDATES` under `/improve`;
3. candidates may include verification strategies, discovery sequences, failure guards, missing tooling, prompt/orchestration patterns or test-harness opportunities;
4. `NONE` is correct when no concrete reusable behavior emerged;
5. when warranted, persist compact session feedback with evidence and proposed class: `skill`, `runbook`, `pattern`, `known_error`, `tooling`, or `test_harness`;
6. do not create/refine shared skills from an ordinary implementation shot. Hygiene/Kaizen promotes repeated evidence, severe blockers or forward-tested improvements.

### 9. Final SDD status

Return exactly one:

- `SDD_DELIVERY_PASS`
- `SDD_DELIVERY_FAIL`
- `SDD_NOT_READY`
- `SDD_BLOCKED_EXTERNAL`

`SDD_DELIVERY_PASS` requires:
- all active acceptance criteria proven;
- no material finding pending;
- reusable verifier assets dispositioned;
- final diff within frozen scope;
- `VERIFICATION.md` updated;
- exact certified commit;
- no false claim of deployment/production unless separately certified.

## Output

```text
Feature / active task:
Certified baseline:

Shot 1:
  candidate commit:
  tests:
  reusable assets:

Shot 2:
  verified commit:
  independent probes:
  findings:
  reusable assets:

Shot 3:
  final commit:
  corrections:
  final tests:
  promoted regression/E2E/toolkit assets:

Verification matrix:
Final status: SDD_DELIVERY_PASS|SDD_DELIVERY_FAIL|SDD_NOT_READY|SDD_BLOCKED_EXTERNAL

/improve:
  REUSABLE_BEHAVIOR_CANDIDATES: <items | NONE>
  feedback persisted: <path | none>

Next exact SDD phase/task:
```

## Hard Rules

- SPEC/PLAN/TASKS must be ready before implementation; do not hide upstream ambiguity in code.
- Every Shot 1/2/3 is one-shot and executable from fresh context.
- Shot 1 never accepts itself.
- Shot 2 is adversarial and independent; rerunning only implementation tests is insufficient.
- Shot 2 does not fix product code.
- Shot 3 cannot reopen frozen product/architecture/data semantics.
- No fourth planned shot.
- Every acceptance criterion maps to executable evidence or an explicit unavailable/external gate.
- Do not equate "E2E" with "put test in a folder named e2e"; test placement follows behavior boundary and canonical ownership.
- Preserve strong verifier work as executable regression/E2E/toolkit assets rather than leaving it in temporary branches.
- Product behavior belongs in tests/harnesses; agent behavior belongs in skills/runbooks/patterns.
- `/improve` always evaluates reusable behavior but may legitimately produce `NONE`; never manufacture feedback or skills to fill a quota.
- Production/deployment claims require their own release/deployment/E2E certification.
