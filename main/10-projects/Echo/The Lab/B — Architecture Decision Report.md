---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[A — Product Contract — The Lab]]"
  - "[[C — Reality and Gap Matrix]]"
  - "[[D — Revised Roadmap]]"
aliases: []
tags:
  - kind/doc
  - area/echo
created: "2026-09-22"
updated: "2026-09-22"
---

# B — Architecture Decision Report

> **PROPUESTA, NO RATIFICADA.** Arquitectura de producto y transición, sin cambios de código, infraestructura ni datos. Las decisiones frozen se conservan salvo reapertura acotada justificada en [[F — Decision Register]]. Contrato de producto: [[A — Product Contract — The Lab]].

## 1. Diagnóstico y tesis

La arquitectura presente sirve como foundation, pero NO entrega The Lab como producto: S0 define tipos y sellos, E-05 produce TradeSet/MetricSet con calculator de métricas y persistencia write-once, E-04 acepta promociones y copia artefactos operativos; ninguno prueba el ensamblado de dos históricos de operaciones, una única historia publicada, N curvas por algoritmo y front usable. E-10 M7 desarrolla Strategy Quality Reference-forward y eligibility, no sustituye ese producto. Evitar tanto el rewrite de Echo como seguir agregando subsistemas de elegibilidad antes del primer vertical slice. Fuente: `xKoRx/echo@5dd998f1`, `specs/FEAT-FORGE-INGESTION-E1/SPEC.md`, `specs/FEAT-ANALYTICS-CONVERGENCE-A0/SPEC.md`, `v3/sdk/contracts/analytics.go`, `v3/sdk/analytics/calculator/calculator.go`; proyecto [[Echo — E-10 Strategy Quality and Eligibility]] actualizado 2026-09-22.

## 2. Ownership, autoridad y flujo

```text
FORGE (xKoRx/symphony)
  Generator + SQX evidence + MT5 validation/trade-list evidence
  StrategyVersion seal + finalist promotion + HandoffManifestV1
                   |
                   v existing E-04 ingress, verified artifact copy, receipt
ECHO identity/promotion + immutable source evidence reference
                   |
                   v one analytics-admission extension (same ingestion path)
ECHO analytics: normalize individual operations + provenance + quality
                   |
                   v deterministic period/source selection, corrections audit
ONE published HistoryRevision per selected StrategyVersion/A/B/policy
                   |
                   v ordered operations -> versioned CurveCalculators
CurveRun + exact CurvePoints + quality/coverage
                   |
                   v reusable E-05 MetricCalculator + curve-specific metrics
MetricSet (key+basis+unit+formula/window/inputs exact)
                   |
                   v existing Gateway/Hasura READ + adapted Lab front
Strategy detail / real-time-axis curves / trades calendar / screener
                   |
                   v LATER: portfolio research -> PortfolioVersion -> Echo apply

REAL branch: raw broker DEALs + Reference binding/coverage (E-06/E-07)
   -> version-pinned operation normalization -> SAME history admission
Execution branch: account-specific executions (E-08/E-09) -> separate fidelity and actual cash equity; never substituted for strategy reference.
```

Authority of operational facts remains broker/journal and raw DEALs; Forge owns original factory evidence and final promotion; Echo owns accepted identity, analytical normalization and publication. Source artifacts are immutable originals in artifact storage (MinIO if existing contract permits). PostgreSQL Echo owns normalized operations and publications, algorithm configurations/runs, metrics and indexed read models. Forge's MongoDB remains its existing domain authority only; no Echo analytics mirror. Hasura and front only read projections; the SDK defines shared semantic contracts and deterministic recipes, not a new execution engine. Ingest acceptance cannot activate trading.

## 3. Domain model and selection

Use existing `StrategyRef`, `StrategyVersionRef`, E-03 mapping/promotion, E-06 binding, `NormalizedOperationV1`, `ScopeV1`, `TradeSetV1` and `MetricSetV1`. Add the *smallest* missing Echo-owned entities, names conceptual until SPEC: `SourceEvidence` (artifact ref/digest, source, schema, time coverage, validation), `OperationProvenance` (native ID, source, strategy version, row/ref, quality), `HistoryRevision` (A/B, immutable selection-policy id/version, selected operation refs/digest, excluded refs/reasons, completeness/coverage, supersedes), `PublishedHistory` (single atomic pointer keyed by StrategyVersion plus A/B/policy selection), `CurveAlgorithm` code registry (no SQL catalog required now), `CurveRun` (inputs/config/outputs seal), `CurvePoint` and optional read-index projection. Do not invent new strategy or trade identity. Cross-source duplicates: native uniqueness detects replay *inside a source*; cross-source economic equivalence requires an explicit evidence-backed relation, never heuristic matching by timestamp or PnL. Period authority wins only after provenance and period membership are proved: SQX TRAINING, MT5 PRE_REAL, Echo Reference REAL. Ambiguous collisions fail closed with quarantined candidates and no double count. Owner must approve the A/B and crossing-trade semantics in A.

Distinguish `history_revision_ref` from strategy identity: changing selection/dedup/corrections produces a new revision of SAME StrategyVersion without rewriting original evidence or operation payloads; changing trading rules produces a distinct StrategyVersion. A longitudinal multi-version projection is explicitly tagged and cannot masquerade as single-version quality. Moving between accounts only changes binding/Execution series, not Reference strategy history. Maintain immutable revision history and a single published selection pointer with compare-and-swap for safe correction and rollback.

## 4. One authority for operations and persistence

E-05 migration `063_analytics_convergence_a0` already stores immutable scopes, TradeSets and MetricSets with sealed NDJSON payload and Hasura SELECT; `canonical_trade_sets.payload_ndjson` is not a suitable *only query interface* for operation detail, temporal windows, calendar, provenance joins and curve replay at scale. Preserve E-05 canonical TradeSet + its immutable, validated NDJSON as authoritative sealed analytical generation. Add relational `canonical_operation_index` within the SAME Echo PostgreSQL as a **rebuildable projection** of validated sealed bytes, carrying `trade_set_ref`, `operation_ref`, StrategyVersion, timestamps, native/source refs, numeric fields, missing-field flags and provenance. Every indexed row records payload digest and offset/index; batch transaction checks 1:1 counts/digests against seal; index is never independently writable as another canonical history. Unique `(trade_set_ref, operation_ref)` and source native identity where provenance proves uniqueness. If a reusable normalized operation store is required before a TradeSet is sealed, stage it as immutable admission evidence, not an independent published analytics authority. Candidate operations may repeat across separate sets/revisions, but membership deduplicates within ONE published history; no mutation of old sets.

Minimal proposed PG records: source evidence/ingestion availability, history revision+membership+published pointer, reconstructed operation index, curve run+points, curve metrics referencing E-05 semantic metric identity. Use current E-05 writer/transaction and replay/conflict design; add idempotent background admission step after E-04 receipt (transactional state and outbox/retry, no second HTTP ingress), artifact verification before marking analytical readiness, and publish only after complete validated history transaction. Errors/partial data remain visible, not silent rollbacks of existing operational INGESTED. PostgreSQL numeric/decimal text exact; never `NUMERIC -> float64 -> decimal` on monetary, risk or timestamps. Raw binary/CSV/HTM/SQX/EX5 remain in artifact storage with hashes; original evidence not thrown away when excluded. No new PG-to-Mongo sync, microservice or distributed transaction between Forge/Echo. Existing copies retain immutable hash evidence; if artifact copy succeeds but DB transaction fails, retry deterministically and garbage-collect only unreferenced staged objects under a separate authorized maintenance lifecycle.

Indexes initially: `(strategy_version_ref, closed_at, operation_ref)` for detail/calendar and `(strategy_version_ref, opened_at, operation_ref)` for membership boundary; `(source_namespace, source_native_id, source_artifact_digest)` for replay; `(history_revision_ref, sequence)` for iteration; `(curve_run_ref, point_at, sequence)` for chart range; uniqueness on active published pointer and question-derived run refs. History selections and curve points are read-model materializations with immutable run metadata. Do not prematurely partition; benchmark before thresholds. Scenarios *illustrative, not measured*: 100 strategies × 2,000 operations = 200,000 operations / 4 curves ~800,000 points; 1,000 → 2,000,000 / ~8,000,000; 10,000 → 20,000,000 / ~80,000,000. Query and batch load test at next order of magnitude; inspect latency, retention and index sizes before partitioning (e.g. measured tens of millions of rows or degrading p95). Cache by immutable curve ref only after need; recompute from seals, batch by StrategyVersion, render downsampled chart only while computing metrics on full points. Incremental curves DEFER until full deterministic replay proves too costly. Existing backup/restore policies remain authoritative; no infrastructure audit or new backup design here.

## 5. CurveCalculator and MetricCalculator contracts

Use a narrow in-process Go interface: `Describe() AlgorithmSpec` and `Calculate(ctx, orderedOps, config, verifiedAuxInputs) -> []CurvePoint + warnings/error`, with an explicit schema for typed parameters and required fields, algorithm ID+semver+definition/source digest, input ordering, basis/unit, missing-data policy, time-axis/tie-breaking rule and deterministic numeric rounding. A static registry maps `(algorithm_id,version)` to implementation. Do not introduce DSL, dynamic plugins, Go runtime reflection framework, database-stored scripts or an analytics microservice. Compute `CurveRun.ref = H(history revision, selected operation digest, algorithm id/version/definition digest, canonical config, period, auxiliary input digests)`; result content digest remains outside identity, same ref/different output => determinism conflict. All calculations use full ordered operations; timestamps are observed UTC and ties stable by ref.

Initial algorithms: `cumulative_r` sums `realized_net_pnl / proven_initial_risk_money` per completed trade where risk currency/FX basis compatible, otherwise explicit INSUFFICIENT and segment coverage; `cumulative_pips` requires instrument pip size/side and price fill, never aggregates incompatible symbol pips as universal economic return; `virtual_equity_fixed_risk` applies user-specified initial capital and fixed monetary risk or explicit risk fraction at each entry when simultaneity/exposure constraints are demonstrated, compounds only per documented event ordering; `observed_account_equity` is a separate data source/account projection, NOT a quality algorithm over normalized strategy operations. A simple capital-from-realized-R transform is *hypothetical conditional* and must not claim it recreates transaction costs, fill/slippage, broker margin, sizing constraints or altered exit paths. Do not simulate trailing/SL movement without candle/tick/path data. Curves may be unavailable, not zero, when inputs incomplete. Curve x-axis uses actual event time and real observation gaps; store period and source change annotations separately.

Keep E-05 `calculator.Compute` as the operation-based **MetricCalculator** for supported keys, formulas and canonical `MetricSetV1`, with adapter to newly sealed history/curve inputs. Add distinct curve metric functions ONLY for path-dependent questions (MDD, current DD, Sharpe over explicitly defined clock-frequency return series, recovery) and integrate them into one metric catalog/identity, not separate competing metrics. `Return` needs explicit denominator and cash-flow convention; PF only if real wins/losses and loss>0; SQN demands sufficiently many independent observations and explicit variance convention; Sharpe demands sample frequency, annualization, risk-free basis and treatment of empty days; drawdown needs initial capital and high-watermark convention. When no comparable basis/FX/calendar exists, disable metric comparison with typed reason. Screener ranking computes a deterministic `RankingRun` for a declared cohort/history revision/curve algorithm/metric definitions/filters/order/ties/missing policy; it is an analytical read result, NEVER the Forge finalist ranking, a prediction or an eligibility grant.

## 6. Dispositions and evidence-based boundaries

| Component | Disposition | Decision and reason |
|---|---|---|
| S0 Echo SDK `contracts` identity/digests/operation/set/metric types | KEEP + bounded ADAPT | Sound shared wire and FR-1 input-derived IDs; add only evidence-backed history/curve descriptors without redefining StrategyVersion. |
| E-04 ingestion/receipt/artifact-copy | ADAPT | Authenticated atomic operational acceptance is demonstrated; extend existing workflow to receive two authentic history refs and schedule analytical admission without changing INGESTED meaning or creating second ingress. |
| Forge factory F-01…F-05, final promotion and F-05 read surface | KEEP + ADAPT producer export | Physically certified V2 and three authentic finalists documented; exporter must prove SQX/MT5 per-trade lists, metadata and digests. No curve ownership or DB Echo writes. |
| E-05 `TradeSet`/`MetricSet` writer and calculator | KEEP + ADAPT | Writer/replay/semantic metric catalog valuable; NDJSON needs rebuildable relational index; metrics calculator reused, curve calculator added in same analytics ownership. |
| Lab legacy canonical trades, journal, outcomes, segments and mutable snapshots | ADAPT -> RETIRE selected read paths after parity | Preserve operational journal indefinitely and any evidence; existing `ReplaceByScope`, AUTO basis, defaults and unversioned snapshots cannot be new canonical analytics. Retire only redundant legacy materializers/readers after replacement verified, not historical facts. |
| E-06/E-07 Reference binding + raw DEAL/coverage | KEEP + ADAPT admission | Reference actual observation/pinned version and UNKNOWN-first coverage feed REAL; raw facts never replaced by an analytical TradeSet. |
| E-08/E-09 routing, reservation, Execution fidelity | KEEP, DEFER economic certification | Separate account execution/impact from strategy normalized quality. Preserve source, do not make execution fidelity prerequisite to history/curves. |
| E-10 M7 forward DQ, expectation, assessment, eligibility | KEEP bounded + DEFER T06–T10 | M7 integrity advances forward only; pause further eligibility until product slice and owner sample-policy ratification, then consume canonical history/metrics without building another calculator. |
| Hasura/Gateway/frontend Lab | ADAPT/REPLACE broken presentation locally | Reuse read boundary/router and components where semantically correct; replace misleading win-rate, recorded-time-only curves and unversioned legacy chart. No full front rewrite. |
| E-11/E-12/E-13 portfolio shadow/apply/front ops | DEFER implementation, KEEP requirements | Identity/time-series/separation seams now; design and execute portfolios after usable first slice, with independent owner capital gate. |
| A second standalone Lab database, Forge-built canonical curves, auto-recovery, candle backtester, generic portfolio engine | RETIRE proposal / DEFER capability | Duplication or unavailable data; no speculative engine. |

Legacy defects are documented in `xKoRx/echo/specs/FEAT-ANALYTICS-CONVERGENCE-A0/SPEC.md` §3 and [[Echo — E-05 Analytics Convergence A0]]; do not re-audit certified prior findings without contradiction. F-05 physical certification documented [[Echo Forge — Factory V2 Completion]]. E-10 latest [[Echo — E-10 Strategy Quality and Eligibility]].

## 7. Safe transition and rollback

Phase 0 freeze baseline and exact evidence (source SHA and existing snapshots, migration history) as documentation only in this review. Phase 1 append compatible analytics artifacts and DB tables in isolated DEV, without modifying E-04 receipt meanings, live policies, journal writes or existing portfolio positions. Phase 2 one authentic read-only candidate: parse SQX/MT5 originals, report field coverage/reconciliation, add explicit source-native dedup tests and operation index, stage history without publishing on disagreement. Phase 3 immutable history publication pointer + curve/metric shadow generation; old UI and new UI may dual-READ for parity, but **never dual-write independent canonical analytics**. Phase 4 per-cohort read cutover after operation count/digest, R/pips, time bounds, quality flags and metric basis parity or explicitly explained semantic differences; restore old read route and previous published revision pointer on rollback. Phase 5 retire legacy materializers/readers ONLY after functional parity, safe backups and separate owner authorization; operational journal and original broker facts never retired. Correct history by append-only correction/revision with actor/evidence/time/reason, no destructive UPDATE; idempotent rerun and no trading effects are hard invariants. DEV integration, physical certification, PROD rollout and monetary activation are four distinct approvals/gates.

## 8. Adversarial challenges

Owner premise 'SQX=training, MT5=pre-real' is target semantics, not proven by F-05 HTM or E-04 manifest certification: MT5 reports may contain only aggregates or replay training, mismatched instruments, timezone and ranges. Demand two operation lists and coverage at H0; if absent, PRE_REAL unknown, never infer trades. 'Exactly one history' must be scoped to a StrategyVersion and published selection revision or version changes silently contaminate quality. An operation opened before A/B and closed after cannot safely be wholly attributed to closed-only returns of both periods; show longitudinal and segregate strict segment metrics until owner approves convention. R and pips do not become percent, and rescaling executed trade results is not an alternative-exit backtest. Changing risk fractions can change available margin and concurrent position feasibility; label unsupported. Quality of normalized strategy cannot use actual lot size from an Execution account. Historical rankings are not portfolios; temporal overlap and risk covariance must be demonstrated. Freeze alone cannot justify missing dual history, but code changes must be narrow and ratified; no global rewrite.

## 9. Sources and confidence

GitHub `xKoRx/echo` remote master `5dd998f16aea7b2821f460188718d7a6d279829c`; target files `v3/sdk/contracts/analytics.go`, `v3/sdk/analytics/calculator/calculator.go`, `specs/FEAT-FORGE-INGESTION-E1/SPEC.md`, `specs/FEAT-ANALYTICS-CONVERGENCE-A0/SPEC.md`. `xKoRx/symphony` remote master `745bc8b94e1f6148ddc16c02eb86a755088c2666`; factory result evidenced in Agents-OS notes, not re-read from physical artifacts. Echo feature branch consolidated `865532078f2c1993e7a3a542a78a9db0fad1f015` and E-10 M7 `1485baa4574b3a65fa97cf0be842ca8ac581097a` from contemporaneous project notes, not both verified as Git HEAD in this session. No direct DB/MinIO/broker/runtime access, no infra audits; Graphify unavailable, focused Markdown fallback. Confidence high for architectural *proposal* and verified source excerpts, lower for actual historical trade-list availability and current deployed state. No physical certificate created.
