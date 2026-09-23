---
type: plan
schema_version: 1
status: approved-for-implementation
area: "[[Echo]]"
related:
  - "[[A — Technical SPEC D1]]"
  - "[[D — Revised Roadmap]]"
  - "[[F — Decision Register]]"
tags: [kind/plan, area/echo, the-lab, d1]
created: "2026-09-23"
updated: "2026-09-23"
---
# B — Implementation Plan D1

## Objective

Implement the Echo-only foundation defined by [[A — Technical SPEC D1]] in one development shot. No Forge changes.

## Authority order

1. D1 Technical SPEC.
2. Decision Register M01-M12.
3. Revised Roadmap D1.
4. Existing Echo Strategy/StrategyVersion and canonical-symbol authorities.
5. Existing repository/gateway conventions.

If existing code conflicts with 1-3, adapt the code; do not silently change the model.

## Work packages

### WP1 — Baseline and impact map

Verify current `xKoRx/echo` HEAD/worktree, migration head and relevant concurrent branches. Locate only:
- StrategyVersion persistence/key shape.
- canonical symbol authority/resolver.
- Gateway routing/auth/error conventions.
- S0 wire/decimal/hash helpers.
- E05/PG063 direct compile-time consumers impacted by contract change.
- PostgreSQL repository transaction/bulk facilities.

Record the actual paths and baseline before edits.

Do not audit Forge, PROD, infra or unrelated Echo features.

### WP2 — Shared contract/domain

Create/version the D1 contract in the shared Echo SDK.

Responsibilities:
- request/dataset/operation/response DTOs;
- strict validators;
- decimal-string validation;
- canonical digest recipes;
- enum/constants;
- deterministic canonical ordering;
- error typing compatible with existing wire envelope.

The contract must be producer-agnostic. No SQX/MT5 parsing code.

Replace or supersede the old analytical S0 operation shape only as needed. Preserve unrelated S0 contracts.

### WP3 — PostgreSQL migration and repository

Add the next safe migration after inspecting the actual migration head:
- `echo.canonical_operations`;
- `echo.strategy_history_state`;
- constraints/indexes/FKs from SPEC.

Repository/application persistence:
- load current history head;
- range/read operations;
- serialize replacement;
- delete imported sources only;
- bounded bulk insert;
- upsert active history state;
- transaction rollback.

Do not dual-write TradeSet.

### WP4 — Application service

Implement a producer-agnostic `StrategyHistoryService` or equivalent consistent with repository architecture.

Pipeline:
validate target -> validate symbol -> validate all input -> digest/count -> exact replay fast path -> transaction replacement -> response.

No partial commits.

### WP5 — Gateway boundary

Mount `PUT /api/v1/strategy-versions/{strategy_version_ref}/history` in existing Gateway.

Use existing service-auth/error/config patterns. Do not invent a new process or auth platform.

Body limit must be configurable and suitable for multi-year operation lists, not inherited blindly from a tiny control-plane manifest.

### WP6 — Tests and evidence

Implement all tests from [[C — Test Plan D1]].

Use PostgreSQL integration tests for transaction/rollback/idempotency. Fixtures prove Echo contract only, never Forge physical compatibility.

### WP7 — Documentation/session close

Update D1 implementation evidence in Agents-OS:
- actual baseline/branch/commit;
- files/migrations changed;
- tests executed and exact results;
- unresolved risks;
- any SPEC deviation (deviation requires explicit owner approval; otherwise fix implementation);
- feedback for next agent.

Close the Agents-OS session using the canonical session-close procedure.

## Parallelism inside one developer shot

The implementing agent may use subagents/worktrees for:
- SDK/domain;
- PostgreSQL/repository;
- gateway/tests;

but remains responsible for reconciling them into one coherent branch and running the complete suite.

There must be exactly one migration owner.

## Technical freedom

The dev may choose:
- package names consistent with repo;
- SQL bulk mechanism already supported by Echo;
- internal service/repository interfaces;
- helper factoring;
- test fixture organization;
- exact auth adapter reuse.

The dev MUST NOT change:
- operation semantics/columns;
- required fields;
- M01-M12;
- endpoint semantics;
- atomic full-history replacement;
- source/period rules;
- one current history-state row;
- no-Forge/no-PROD/no-trading scope.

If an immutable repo fact makes the SPEC impossible, the dev must solve around it when possible. Only a genuine contradiction with a frozen decision may end as BLOCKED; it must include exact path/evidence and the narrowest proposed decision change.
