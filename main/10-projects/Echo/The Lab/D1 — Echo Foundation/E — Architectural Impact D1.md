---
type: adr-impact
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[A — Technical SPEC D1]]"
  - "[[F — Decision Register]]"
tags: [kind/architecture, area/echo, the-lab, d1]
created: "2026-09-23"
updated: "2026-09-23"
---
# E — Architectural Impact D1

## New durable authority

`echo.canonical_operations` becomes the only durable row-level authority for canonical strategy operations.

`echo.strategy_history_state` is the current imported-history head/config for a StrategyVersion. It is not a history revision ledger.

## The Lab boundary

Lab begins downstream of canonical operations. Future `lab_curves`, points and metrics are reconstructible derivatives.

No Lab ingestion table.

## Producer boundary

The external contract is producer-agnostic. Forge is the first expected producer but its SQX/MT5 internal implementation is irrelevant to Echo.

This allows future importers to conform without changing Echo domain semantics.

## S0

The existing `NormalizedOperationV1` is not the D1 canonical-history model because it admits lifecycle/incomplete/provenance concepts explicitly rejected by M01-M10.

D1 may add a clean versioned contract and reuse wire/hash/decimal primitives.

## E05 / PG063

TradeSet/MetricSet persistence is not used as a second canonical operation store.

PG063 is not dropped in D1. Direct consumers are identified during implementation and scheduled for L-CLEAN or later convergence.

## E04 / ingestion

Existing E04 gateway/transaction/auth/idempotency infrastructure may be reused where it reduces code without coupling D1 history semantics to promotion or Forge internals.

History readiness remains independent from promotion/activation state.

## Journal

`trade_journal` remains operational Echo authority and untouched in D1. D4 will map closed Reference trades into the same `canonical_operations` model.

## Scalability choices

- exact NUMERIC values;
- flat queryable columns;
- no JSONB trade payload;
- one row per closed trade;
- bounded bulk persistence;
- minimal purposeful indexes;
- one active imported history head rather than revision chains;
- full snapshot atomic replace for manual historical reimport.
