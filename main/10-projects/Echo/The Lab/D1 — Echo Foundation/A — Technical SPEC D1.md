---
type: spec
schema_version: 1
status: approved-for-implementation
area: "[[Echo]]"
related:
  - "[[D — Revised Roadmap]]"
  - "[[F — Decision Register]]"
tags: [kind/spec, area/echo, the-lab, d1]
created: "2026-09-23"
updated: "2026-09-23"
---
# A — Technical SPEC D1 — Echo Canonical Strategy History

## 0. Authority and scope

This SPEC freezes the D1 Echo foundation. It implements owner decisions D1-M01..M12 from [[F — Decision Register]].

D1 is Echo-first. Forge and any other producer are external clients of this contract. D1 MUST NOT inspect, redesign or patch Forge. It MUST NOT change product semantics to accommodate current producer limitations.

Baseline at planning: `xKoRx/echo master@5dd998f16aea7b2821f460188718d7a6d279829c`. The implementing agent MUST verify HEAD/worktree before edits and record the actual baseline.

No PROD, no trading activation, no broker commands, no journal mutation.

## 1. Product invariant

Echo owns canonical strategy history.

A canonical operation is exactly:

> one complete closed trade = one close = one durable row.

V3 initial deliberately does not model open trades, partial closes, deals, legs or execution copies.

The Lab consumes these operations. The Lab does not own or ingest trades.

## 2. Existing identities

Reuse the existing Echo Strategy / StrategyVersion authority. Do not invent a parallel strategy ID.

A history import targets an existing StrategyVersion. If the StrategyVersion does not exist, the history request fails. Strategy/version creation/promotion remains a separate Echo responsibility.

The persistence FK MUST use the actual current StrategyVersion key shape discovered in the baseline (including namespace if the current authority uses it).

## 3. Canonical source and periods

Allowed source values:

- `SQX` -> TRAINING_DATA.
- `MT5` -> PRE_REAL.
- `REFERENCE` -> REAL, populated later from Echo journal.

Period membership is derived only from `opened_at`:

- `SQX`: `opened_at < training_end_at`.
- `MT5`: `opened_at >= training_end_at` and, when B exists, `opened_at < live_start_at`.
- `REFERENCE`: B must exist and `opened_at >= live_start_at`.

`closed_at` never changes membership. It only positions realized result in time.

A = `training_end_at`, the first instant after the final civil training day.
B = `live_start_at`, nullable until REAL begins.

`training_timezone` is an IANA timezone used to resolve the original civil A input. Persist it with the active history head.

## 4. Canonical symbol

Echo accepts only its canonical instrument/symbol identifier.

The history request supplies one canonical `instrument_id` for the StrategyVersion history. Echo validates it using the existing Echo canonical-symbol authority. Do not create a second instrument registry or alias map in Lab/history.

The service propagates the validated canonical `instrument_id` into persisted operations. Producers resolve broker/SQX aliases outside Echo's canonical domain contract.

## 5. Wire contract

Contract version: `strategy-history.v1`.

HTTP boundary:

`PUT /api/v1/strategy-versions/{strategy_version_ref}/history`

Use the existing Gateway process and existing service-to-service auth patterns. Do not create a new process. Authenticated namespace/tenant, if current Echo identity requires it, comes from server auth context rather than an untrusted body field.

The endpoint represents the complete active imported history snapshot for SQX+MT5. PUT is intentionally replacement semantics.

### 5.1 Request

Logical shape:

```text
contract_version = strategy-history.v1
instrument_id
training_end_at            RFC3339 instant, exclusive boundary A
training_timezone          IANA timezone
live_start_at?             RFC3339 instant B, nullable

training:
  operation_count
  dataset_digest
  operations[]             CanonicalOperationInputV1

pre_real:
  operation_count
  dataset_digest
  operations[]             CanonicalOperationInputV1
```

Both dataset envelopes are required. A valid envelope MAY contain zero operations; zero count is not the same as missing dataset.

`training` maps to SQX and `pre_real` maps to MT5. Source is therefore not repeated per operation.

### 5.2 CanonicalOperationInputV1

Every field below is required unless explicitly marked optional:

- `source_trade_id`: stable source identity.
- `side`: LONG | SHORT.
- `opened_at`: RFC3339 UTC/proven instant.
- `closed_at`: RFC3339 UTC/proven instant.
- `entry_price`: exact decimal string > 0.
- `exit_price`: exact decimal string > 0.
- `stop_loss`: exact decimal string > 0; initial SL.
- `take_profit`: exact decimal string > 0; initial TP.
- `volume`: exact decimal string > 0.
- `volume_unit`: LOT | CONTRACT | BASE_UNIT.
- `gross_pnl`: exact decimal string.
- `commission`: exact decimal string; signed contribution; explicit zero when none.
- `swap`: exact decimal string; signed contribution; explicit zero when none.
- `net_pnl`: exact decimal string.
- `currency`: uppercase 3-character currency code.
- `initial_risk_money`: OPTIONAL exact decimal string > 0 when the producer can prove it.

No JSON numbers for prices, quantity or money. Wire decimals are strings and PostgreSQL uses exact NUMERIC.

No `status`, `period`, `account_id`, broker alias, timeframe, quality blob, provenance blob, missing-fields list, deals or legs.

### 5.3 Economic normalization

Cost convention is signed contribution.

Invariant:

`net_pnl = gross_pnl + commission + swap`

The normalized producer contract MUST make this exact in decimal arithmetic. Echo does not infer missing cost components. Missing required economics rejects the whole dataset.

### 5.4 SL/TP geometry

Domain validation MUST reject obviously invalid initial geometry:

- LONG: `stop_loss < entry_price < take_profit`.
- SHORT: `take_profit < entry_price < stop_loss`.

If later product requirements add legitimate strategies outside this geometry, that requires an explicit contract version change. Do not silently weaken V1.

### 5.5 Time

Only proven instants enter canonical operations.

- `closed_at >= opened_at`.
- timestamps are normalized before persistence.
- ambiguous/unresolvable source times fail ingestion.
- no per-row timezone/evidence structure is persisted in V1.

## 6. Digest and identity

Physical PK is an internal BIGINT identity.

Durable source uniqueness:

`UNIQUE(strategy-version-key, source, source_trade_id)`

The exact StrategyVersion composite key follows the existing authority.

Echo computes a canonical `record_digest` for every normalized operation from the canonical V1 fields plus target StrategyVersion, canonical instrument and source. Do not trust an arbitrary producer record digest.

Dataset digest is deterministic over the canonical records in stable sort order:

`(opened_at, closed_at, source_trade_id)`.

The shared SDK MUST expose the digest recipe so producers can supply `dataset_digest`. Echo recomputes it and rejects mismatch.

History digest is deterministic over:

- contract version;
- StrategyVersion identity;
- instrument_id;
- training_end_at;
- training_timezone;
- live_start_at/null;
- training dataset digest + count;
- pre_real dataset digest + count.

Echo persists the active `history_digest`.

## 7. Persistence

### 7.1 echo.canonical_operations

Logical columns; actual FK widths/types MUST match existing Echo identity schema:

- `id BIGINT GENERATED ... PRIMARY KEY`
- StrategyVersion key columns/FK
- `source TEXT NOT NULL`
- `source_trade_id TEXT NOT NULL`
- `instrument_id TEXT NOT NULL`
- `side TEXT NOT NULL`
- `opened_at TIMESTAMPTZ NOT NULL`
- `closed_at TIMESTAMPTZ NOT NULL`
- `entry_price NUMERIC(38,18) NOT NULL`
- `exit_price NUMERIC(38,18) NOT NULL`
- `stop_loss NUMERIC(38,18) NOT NULL`
- `take_profit NUMERIC(38,18) NOT NULL`
- `volume NUMERIC(38,18) NOT NULL`
- `volume_unit TEXT NOT NULL`
- `gross_pnl NUMERIC(38,18) NOT NULL`
- `commission NUMERIC(38,18) NOT NULL`
- `swap NUMERIC(38,18) NOT NULL`
- `net_pnl NUMERIC(38,18) NOT NULL`
- `currency TEXT NOT NULL`
- `initial_risk_money NUMERIC(38,18) NULL`
- `record_digest TEXT NOT NULL`
- `created_at TIMESTAMPTZ NOT NULL`
- `updated_at TIMESTAMPTZ NOT NULL`

Constraints:
- source SQX|MT5|REFERENCE.
- side LONG|SHORT.
- volume_unit LOT|CONTRACT|BASE_UNIT.
- all positive price/volume fields > 0.
- optional initial_risk_money > 0 when present.
- closed_at >= opened_at.
- currency matches `^[A-Z]{3}$`.
- record_digest matches Echo SHA256-ref convention.
- exact economic identity.
- source_trade_id non-empty.
- unique StrategyVersion/source/source_trade_id.

Indexes:
- PK.
- unique identity above.
- StrategyVersion + opened_at.
- StrategyVersion + closed_at.

Do not add speculative indexes. The unique index must also support replacement lookup by StrategyVersion+source prefix.

### 7.2 echo.strategy_history_state

One current row per StrategyVersion, not a revision log:

- StrategyVersion key/FK and PK.
- `instrument_id NOT NULL`.
- `training_end_at TIMESTAMPTZ NOT NULL`.
- `training_timezone TEXT NOT NULL`.
- `live_start_at TIMESTAMPTZ NULL`.
- `training_digest TEXT NOT NULL`.
- `training_count BIGINT NOT NULL`.
- `pre_real_digest TEXT NOT NULL`.
- `pre_real_count BIGINT NOT NULL`.
- `history_digest TEXT NOT NULL`.
- `created_at TIMESTAMPTZ NOT NULL`.
- `updated_at TIMESTAMPTZ NOT NULL`.

This table is the active head/config, NOT HistoryRevision, Publication or import audit history.

No separate import/quality table in D1.

## 8. Replacement semantics

The PUT request is all-or-nothing for imported history (SQX + MT5).

Required algorithm:

1. authenticate / resolve namespace.
2. decode with bounded request size.
3. resolve existing StrategyVersion.
4. validate canonical instrument.
5. validate every DTO and decimal exactly.
6. derive source from envelope.
7. validate period boundaries by opened_at.
8. reject duplicate source_trade_id within each dataset.
9. recompute record digests, dataset digests/counts and history digest.
10. if active history_digest is identical: return unchanged; zero deletes/inserts.
11. BEGIN transaction and serialize replacement for the StrategyVersion.
12. delete existing SQX + MT5 canonical operations for this StrategyVersion.
13. bulk insert all new SQX + MT5 operations. No N network round-trips; use the best existing bounded bulk mechanism.
14. insert/update strategy_history_state.
15. COMMIT.
16. return ready response.

Any failure after BEGIN MUST rollback to the previous complete history.

Replacement MUST NOT touch REFERENCE rows.

Concurrent replacements MUST be serialized using existing DB transaction/locking primitives; no generic distributed lock.

## 9. Response

Logical response:

```text
contract_version
strategy_version_ref
history_digest
result = CREATED | REPLACED | UNCHANGED
state = HISTORY_READY
training { operation_count, dataset_digest }
pre_real { operation_count, dataset_digest }
accepted_at
```

201 for first accepted history. 200 for exact replay and successful replacement.

`HISTORY_READY` means imported history is canonical and queryable. It does not mean ACTIVE, provisioned, funded or trading.

## 10. Error semantics

Use existing Echo wire/error envelope. Map at minimum:

- malformed/unsafe wire -> 400 INVALID_INPUT/INVALID_WIRE.
- unsupported contract version -> 400.
- StrategyVersion absent -> 404.
- canonical symbol absent/unknown -> 422.
- invalid operation / time / SL-TP geometry / duplicate source_trade_id / count mismatch / digest mismatch / period violation -> 422 fail-closed.
- concurrency/identity conflict that cannot converge -> 409.
- DB unavailable -> 503 retryable.
- body over configured limit -> 413.

No partial success. Never silently drop a bad operation.

## 11. Read surface D1

D1 MUST include an application/repository read path sufficient to retrieve operations for a StrategyVersion ordered/ranged by opened_at and closed_at. It may be exposed by the same service/gateway according to existing Echo conventions.

Do not build dashboard/curve APIs in D1.

## 12. S0/E05 convergence

The current `NormalizedOperationV1` shape is superseded for this canonical-history use because it permits open/partial/incomplete operations and missing-field/provenance structures that contradict M01-M10.

Implement a clean versioned contract for this D1 use. Reuse low-level decimal/hash/wire helpers where appropriate, but do not preserve the old shape merely for compatibility.

E05 TradeSet/MetricSet persistence is not a second authority. D1 MUST NOT dual-write operations into TradeSet payloads.

Do not drop PG063 or legacy tables during D1. Identify direct consumers touched by compilation/tests and record cleanup impact for L-CLEAN.

## 13. Non-goals

- Forge code or producer implementation.
- authentic SQX/MT5 certification.
- curves, curve points, metrics or dashboard.
- Reference journal worker.
- copy/Execution fidelity.
- open trades/partial closes.
- money management/portfolio.
- legacy destruction.
- PROD deployment.
- trading activation.

## 14. D1 definition of done

This SPEC is implemented when:
- migrations apply cleanly in isolated DEV/PG integration;
- DTO/digest contract is versioned in shared Echo SDK;
- service endpoint is functional;
- existing StrategyVersion + canonical instrument are enforced;
- valid full history persists and reads back exactly;
- exact replay is no-op;
- valid changed PUT atomically replaces SQX+MT5;
- invalid operation rejects entire request;
- failure during replacement preserves previous history;
- REFERENCE is untouched;
- no trading/activation side effects;
- test suite and independent validation can reproduce evidence.
