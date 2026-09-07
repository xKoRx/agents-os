# Autonomous Phase Plan Contract

Read this file when creating or auditing an implementation plan intended for delegated execution.

## Planner Structure

The agent-project note must contain:

1. Executive summary and verified remaining work.
2. Requirement-to-evidence matrix with `done/partial/replaced/missing/blocked`.
3. Scope, non-scope and decision register.
4. Current and target architecture.
5. Data/control sequence.
6. Versioned data/activity/API contracts with examples.
7. Business formulas, source authority, units, windows and edge cases.
8. Dependency-ordered roadmap plus autonomous phase packages.
9. File/symbol map with `create/modify/no-touch`.
10. Unit, contract, integration, workflow and E2E validation.
11. Compatibility, migration, observability, rollout and rollback.
12. Risks, assumptions and human control points.
13. Definition of Done.
14. Atomic tasks by phase.
15. Common executor prompt, dispatch blocks and handoff contract.

Use the project’s existing headings/layout when they express the same contract. Do not restructure an established project only for numbering.

## Evidence Reference Contract

For each material claim:

- identify evidence class: `HEAD`, `LOCAL_CHANGE`, `GENERATED_ARTIFACT`, `PRODUCTION`, `TEST`, `STUB`, `CONTRACT`, `REPORT` or `ROADMAP`;
- cite an existing file and symbol using a portable
  `` `VAULT_ROOT/<relative-path>[:L<line>]` `` reference; include a line anchor
  only when stable;
- cite a commit/test/runtime artifact when the claim depends on version or execution;
- mark a nonexistent future path as `create`, never as current evidence;
- state the gap explicitly when no evidence exists.

Never persist `file:///`, `/Users/...`, `/home/...` or another machine-specific
vault path in a plan. Repository-external operational paths are allowed only
when they are part of the target system contract, not a way to locate the
vault.

An executor may inspect a referenced symbol to implement it. It must not search the repository to infer an unstated responsibility.

## Decision Register

Each decision row contains:

```text
ID | status | resolution | source/evidence | phase consuming it
```

Allowed ready-state statuses:

- `CONFIRMED`: human business decision.
- `TECHNICAL_RESOLUTION`: integrity/architecture decision supported by evidence.

`PROPOSED_FOR_APPROVAL` blocks `ready_for_phase_0`. Runtime capability uncertainty does not become an implicit decision; assign it to a Phase 0 spike.

## Autonomous Phase Package

Every phase package contains these exact concepts:

```markdown
### Paquete autónomo Fase N — <name>

**Misión exacta**

**Precondiciones verificables**

**Lectura obligatoria**

**Decisiones cerradas**

**Implementación paso a paso**

**Archivos esperados**

**No tocar**

**Spikes permitidos**

**Tests y asserts**

**Entregables/Gate GN**

**Handoff a Fase N+1**
```

Requirements:

- Precondition names the prior accepted gate.
- Reading list gives exact project sections and repository files/symbols.
- Closed decisions remove semantic choice from the executor.
- Steps are ordered and map to atomic tasks.
- Expected files distinguish `create`, `modify` and conditional changes.
- `No tocar` protects adjacent phases and user changes.
- Allowed spikes are narrow; unexpected architecture triggers `PLAN_CONFLICT`.
- Tests contain business invariants, not only coverage or compilation.
- Gate evidence is independently reviewable.
- Handoff states what the next agent receives and must not rediscover.

## Phase Balance

Estimate each phase using:

- unknowns remaining;
- number of system boundaries;
- production mutation risk;
- test/fixture burden;
- operational/deployment burden.

Split or rebalance a phase when it dominates several dimensions or contains two independently gateable outcomes. A low-LOC research or rollout phase can equal a high-LOC coding phase.

## Gate Control

Persist one table:

```text
Gate | current state | phase agent responsibility | owner acceptance evidence | enables
```

States:

- `pending`
- `review`
- `accepted`
- `blocked`
- `rejected`

The executor writes `review`, `blocked` or `rejected`. The owner authorizes `accepted`. Rejection reopens only the failed phase tasks.

## Atomic Task Contract

Each task contains:

```text
objective | files/symbols | preconditions | implementation | tests | expected evidence
```

Task IDs use `T<phase>.<sequence>`. The task list and phase procedure must agree.

## Executor Prompt Contract

Create:

1. one common prompt containing safety, evidence hierarchy, design invariants, project-update requirements and stop behavior;
2. one dispatch block per phase:

```text
FASE_ASIGNADA=N
PAQUETE_CANONICO=<section>
GATE_REQUERIDO=<prior gate accepted|none>
TAREAS=<range>
SALIDA=<artifacts/evidence>
STOP=<current gate review; forbidden next work>
```

Send the executor the common prompt plus one block only.

## Ready Checklist

- [ ] No open business decision.
- [ ] Technical unknowns have bounded spike owners.
- [ ] Existing references resolve and line anchors are valid.
- [ ] Every phase has all package fields.
- [ ] Phase, task, gate and dispatch counts reconcile.
- [ ] Work is dependency ordered and load-balanced.
- [ ] Tests assert business behavior and failure modes.
- [ ] Rollout and rollback are executable.
- [ ] Project note records current ready phase.
- [ ] Validator passes.
