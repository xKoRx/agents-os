---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo — Producto Integrado]]"
  - "[[Echo — Live Platform V1]]"
  - "[[Echo Forge — Factory V2 Completion]]"
  - "[[E — First Usable Vertical Slice]]"
aliases: []
tags:
  - kind/doc
  - area/echo
created: "2026-09-22"
updated: "2026-09-22"
---

# D — Revised Roadmap

> **PROPUESTA DE REPLANIFICACIÓN, pendiente de ratificación owner.** No invalida ni borra tareas/certificaciones del roadmap anterior. El primer bloque de entrega H0–H4 constituye UN vertical slice de producto, no cinco microhandoffs. DEPLOY y autorización de capital nunca se infieren de implementación. Contratos [[A — Product Contract — The Lab]], [[B — Architecture Decision Report]], realidad [[C — Reality and Gap Matrix]], especificación de primer slice [[E — First Usable Vertical Slice]].

## North star y ruta crítica

```text
H0 Authentic candidate and actual two-trade-list proof (first gate)
  -> H1 Dual-source Forge handoff contract + same E-04 analytical-admission extension
  -> H2 Echo immutable operations / single published A-B history
  -> H3 N reproducible curves + reused E-05 metrics
  -> H4 Lab strategy UI + calendar + comparable screener
  = V0 USABLE LAB (only then first real DEV E2E certification)
  -> H5 Reference REAL physical observation and forward quality
  -> H6 Portfolio research, alignment and shadow PortfolioVersion
  -> H7 E08/E09 economic integration + E12 apply lifecycle + E13 ops/front cert
  -> owner-approved separate PROD rollout and real capital gate
```

H0 is physical READ ONLY with one real strategy, NOT a prerequisite to finish architecture review; it is the first mandatory gate *before declaring the next product capability complete*. If authentic MT5 trade list is unavailable, keep H1–H4 design/adapter work moving using contract fixtures but block only PRE_REAL readiness and V0 physical certification; never invent trades, rewrite fixture as golden or launch a new generic investigation. The source-based full run stays valuable as candidate even with zero valid data for a metric.

## H0 — Authentic data proof and pinned baseline (owner of evidence: Forge)

Objective: take ONE of three authentic finalists from F-05-C FULL campaign `0ce72173…`, resolve exact StrategyVersion, identify SQX+MT5 individual operation artifacts and hashes, ranges/time basis/IS-OOS, risk/cost inputs, show source aggregate-vs-row reconciliation and overlap. Source pin: `xKoRx/symphony@745bc8b94e1f6148ddc16c02eb86a755088c2666` remote master at review; Echo master `5dd998f16aea7b2821f460188718d7a6d279829c`; feature SHAs must be resolved separately at execution. Dependencies: read-only F-05-I surface, F-05-C certificate. Contract: F04 manifest + original artifact refs; no analytics ingestion, no deployment, no broker action. Work package NORMAL H0 (one task) outputs compact artifact matrix with exact IDs/ref/digest, row counts, date A/B proposals and lossless example; no code. Tests: source hashes and trade-list totals versus source report, dual format parser validation read-only, temporal boundaries, duplicate/error matrix. Exit `DUAL_TRADE_LIST_EVIDENCED` or precise `MISSING_SQX_TRADES/MISSING_MT5_TRADES/RANGE_CONFLICT/ECONOMICS_INSUFFICIENT` with source ref, consequence and workaround ONLY if evidence-backed; may permit degraded individual curves while full V0 gate remains blocked. Usable unlock: known real candidate and exact contract deltas, avoids speculative producer/consumer work.

## H1 — Dual-source producer and bounded E-04 extension (Forge + Echo ownership separated)

Objective: Forge emits typed SQX and MT5 trade-list artifact refs/digests/ranges/strategy version and provenance in existing `HandoffManifestV1` via compatible capability/version; Echo E-04 verifies bytes, returns same operative receipt, queues analytical admission durably and idempotently. Dependencies H0 source shape, E01/E03/E04/F04 contracts, owner ratification of extension. Scope no other ingress, no direct Forge PG Echo write, no eligibility/activation. One NORMAL Forge producer WP (export/manifest/golden corpus) and one NORMAL Echo ingress WP (validation/availability/staging), each repo only; canonical SDK additive change serialized by one designated owner before both pins updated. Tests: real fixture roundtrip, replays and digest conflict, missing second artifact preserves operative receipt but analytical readiness withheld, crash-after-copy/before-commit recovery and zero economic side effects. Gate: verified identical dual artifact refs and deterministic admission state, original E04 contract still passes. Unlock: real source evidence available to Echo without authorizing trading.

## H2 — Single canonical history and indexed operation projection (Echo only)

Objective: parse/normalize real two lists, preserve originals and rejected rows, index exact operations from sealed TradeSet E05, select deterministic SQX TRAINING and MT5 PRE_REAL by half-open A/B with explicit exclusions; create immutable history revision and one publish pointer. Dependencies H1 producer schema or documented degraded sample, E05 writer/PG063, owner A/B and boundary rule. Scope additive PG migration owned exclusively by H2, zero migrations from parallel packages; no redundant Mongo analytics, no data alteration of operational journal. One NORMAL WP includes schema, adapter, provenance/dedup, selection, publication and READ APIs. Tests: source/report reconciliation; interval A/B, crossing trade, same native ID in distinct namespaces, same economic event overlapping sources, two versions and account switch, ambiguous duplicate quarantine, exact replays and altered payload 409/conflict, concurrent publication CAS, crash before publish, complete vs partial/gap/UNKNOWN, NDJSON↔index parity/rebuild. Gate: one authentic candidate history sealed with selected ops count and digest and 0 duplicates, exclusions queryable, no mutation of original evidence or E04 operational receipt. Unlock: a StrategyVersion has one auditable history and individual trade table.

## H3 — Curve engine and semantic metrics (Echo only)

Objective: implement small versioned in-process Go CurveCalculator registry with initial cumulative R, instrument-qualified pips, fixed-capital virtual equity where inputs adequate; reuse E05 MetricCalculator for operation-based values and add separately defined curve-path metrics under same catalog. Dependencies H2 immutable history and algorithm contracts; no REAL/E08/E09 dependency. One NORMAL WP domain algorithms+storage/API with dedicated fixture evidence tests and one reviewer for contract identity only if truly needed. Test properties: same inputs/ref/digest points; altered config/new version => new run; same ref/different output => typed conflict; ordering ties/time zone; missing risk/pip/FX -> INSUFFICIENT; PF no loss undefined; Sharpe frequency/time gaps; exact decimal; no lot-size leakage into normalized R; metrics computed on full points not downsampled. Gate: authentic history shows reproducible curves and metrics with exact input lineage, recompute without reimport. Unlock: research quality independent of account sizing within real data limitations.

## H4 — First Lab UI, calendar and screener (Echo front + read boundary)

Objective: strategy/version picker, period A/B markers and temporal chart, curve selection, proven provenance and missing coverage, operation detail/calendar, comparable metrics and ranked cohort. Dependencies H2/H3 API shape frozen; UI skeleton may start in parallel after DTO/acceptance frozen, and front developer must not own PG migrations. One NORMAL WP front/read endpoints/contract tests. Tests: dates real not ordinal-only; explicit gaps, account/creation/version/promotion annotations where evidenced; win-rate proper ratio→percent; no USD default; mixed basis disables ranking, stable sort/ties/UNKNOWN last with reason, calendar uses explicit close-date convention. Gate: owner opens one strategy authentic FULL in DEV and can reproduce count/digests/curve/metrics and compare with another authentic strategy only if same basis/window; a cohort with one available strategy yields ranking view without inventing competitors. Unlock: FIRST USABLE V0, independently DEV physically certified; `SOURCE_PASS` alone is insufficient.

## H5 — REAL and Strategy Quality, after V0

Objective: E06 Reference observing real version pinned at OPEN, E07 raw facts and coverage + E10 existing M7 forward DQ/expectation on SAME canonical operation model, append real into history revision without gap=0; execution account series stays separate. Dependencies real authorized Reference environment and physical gates, no E09 dependency for quality calculation. Reuse previously verified E06/E07/E10 source; manager re-review M7 T05 and sample-policy semantics owner ratification before T06–T10. One NORMAL integration WP with authentic broker evidence, another bounded E10 completion only after owner policy available. Tests: deals identity, partial closes, account changes, observation blackout, gap corrections as new history revision, strategy version roll, real SQ excludes execution fills, policies unavailable => abstain/CASH. Gate: Reference physically observed and attributed plus coverage, metrics reconciled against broker, E10 only if policy owner signed; never deploy/activate by implicit promotion. Unlock: actual live longitudinal analysis and gated quality.

## H6 — Portfolio research (E11 adapted)

Objective: versioned candidate memberships/weights and aligned source/period/basis curves; temporal overlap, covariance and drawdown of portfolio under explicitly declared capital assumptions, abstention when data poor. Dependencies V0 comparative history/metrics; E10 eligibility only if using eligibility filter rather than research sandbox. One NORMAL research WP independent of actuation. Tests: no overlapping time => correlation unavailable, missing currency/initial capital blocks monetized combination, duplicated strategy version rejected, weights/constraints/version immutable, deterministic replay. Gate: one replayable `PortfolioVersion` with evidence, no account assignments, no broker commands. Unlock: portfolio simulation/research without false diversification claims.

## H7 — Execution and lifecycle (E08/E09/E12/E13)

Objective: preserve E08 reservation/command safety and E09 expected-set fidelity, connect owner-approved PortfolioVersion allocation to account routing with reference-to-execution separation; E12 apply/rebalance/replace/pause/retire and E13 operational front/certification. Dependencies E02 remaining AC18 safety gate, E06/07 physical facts, E08 economic class C and E09 live certification, H6 portfolio/version policy, owner risk/activation authorization. One work package per coherent E08/E09 physical gate, portfolio apply lifecycle and E13 ops; no separate integration project. Tests: at-most-once intention/replay, reservation holds under unknown, no blind resend, missing expected execution visible, reconcile fill from broker DEAL, rollback/pause, zero activation without explicit owner decision. Exit: independent DEV E2E -> PHYSICAL -> CROSS-LANE -> owner-approved PROD rollout -> separately owner-approved capital. Unlock: an operable trading system, never guaranteed profitable portfolio.

## Explicit mapping of original work to new product milestones

| Original | New location and retained work | State/priority |
|---|---|---|
| E-01 S0 | H1–H3 shared semantics, pin and bounded additive extension | KEEP certified baseline; don't redo. |
| E-02 safety/auth/journal | H7 pre-capital gate, journal authority throughout | KEEP software integrated; AC18 remains independent, do not let it delay H0–H4 safe read work. |
| E-03 identity/BWC | H1/H2 mapping/version seal | KEEP source and unique identities; no re-identity. |
| E-04 ingestion | H1 extend existing accepted flow, H2 analytical admission | ADAPT; CERT-E04-01/F04-03 stay PASS for original operational scope. |
| E-05 A0 | H2 TradeSet/writer/index, H3 calculator/metric identity | KEEP+ADAPT; preserve 063 and semantics, no second engine. |
| E-06 enrollment | H5 Reference version binding | KEEP; REAL must be physically demonstrated. |
| E-07 facts/coverage | H5 REAL append/correction/coverage | KEEP; raw DEAL unreduced and unknown-first. |
| E-08 command/risk | H7 economic activation gate | KEEP source; physical/capital pending, no first-slice dependency. |
| E-09 fidelity | H7 separate account execution comparison | KEEP source; not predecessor to H2/H3/H5 quality. |
| E-10 quality/eligibility | H5 preserve M7 T05; DEFER T06–T10 until H4+ratified policy | ADAPT integration to canonical history, no competing metric model. |
| E-11 portfolio shadow | H6 research and versioning | DEFER, dependent on history/curve alignment, not individual rankings alone. |
| E-12 portfolio apply | H7 controlled deployment/application | DEFER until H6/E08 safety/owner gate. |
| E-13 front ops & cert | H4 analytics front split out early; remainder H7 ops certification | SPLIT, retain all necessary checks and closeout. |
| Forge F-01/F-02/F-03 | H0 source candidates, existing factory | KEEP closed; don't rerun. |
| Forge F-04 | H1 add authentic dual-history manifest references; E04 join already certified | ADAPT only producer evidence; preserve magic, sealing, operational handoff. |
| Forge F-05-I/F-05-C | H0 F05 read surface/golden; H4 possible read links | KEEP 0.2.105 FULL cert; independent dual-trade-list and Lab E2E additional, not undo cert. |

## Dependencies, ownership, parallelism and resource constraints

Two tracks only: Forge owns original artifacts/producer, Echo owns SDK contract change, ingestion, analytics, UI and eventual live execution; Agents-OS houses documentation. Safe parallelism: H0 data proof with H4 UI mock contract design only; after one SDK change frozen, Forge H1 producer and Echo H1 consumer can proceed in separate repos; after H2 DTO frozen, H3 algorithm and H4 front can work in parallel, but H2 alone owns migration/schema, H3 owns calculator and curve storage migration serialized behind H2, H4 owns no migration. No separate feature branches sharing migration numbers or direct pushes to common dev runtime; pin commits before source work. NORMAL for whole coherent WPs; TOP only for demonstrated conflict in S0/frozen identity or cross-repo contract; GOD only genuinely systemic contradiction. No microhandoffs.

## Product gates and quality policy

Each H0–H4 WP records exact SHA, allowed files, source-of-truth contract, tests on critical paths and negative cases, coverage policy in scoped development rules, and then distinct `IMPLEMENTED`, `SOURCE_VERIFIED`, `DEV_INTEGRATED`, `AUTHENTIC_PHYSICAL_CERTIFIED`, `DEPLOYED`, `PROD_CERTIFIED` status with evidence IDs. Do not infer current production from master, source from reported branch or deployment from a release matrix. Preserve earlier cert verdicts in their original scopes. No product acceptance from synthetic golden, `SOURCE_PASS`, 201-only, empty Hasura, graph screenshot or aggregate HTM only. First certified outcome includes authentic StrategyVersion, both individual historical artifacts or explicit failure, immutable operations/history refs, replayable curves/metrics, usable front and zero trading side effects.

## Primary risks and explicit response

Two trade histories may not exist as expected: H0 exposes exact artifact gap, H1 adjusts export only from real evidence; no synthetic rows. Disparate SQX vs MT5 executions and report timestamps: document differences, quarantine ambiguous correspondence and do not claim price-level identity; scope R/pips only when comparable. Version/account continuity: version pin and Reference binding, separate Execution. Storage inflation: relational projection rebuildable; benchmark before partitioning. Wrong money management counterfactual: only transforms preserving observed entry/exit path and validated cost/constraints, else INSUFFICIENT. Backfill/replay: append-only, no destructive migration, immutable history revisions and published-pointer rollback. Avoid advancing E10 assessment as proxy for product usable.

## Next exact action

After Rodrigo ratifies [[F — Decision Register]], execute H0 read-only on ONE authentic F-05-C finalist, publish its exact evidence matrix, then implement H1–H4 as one vertical slice with four coherent code work packages across the two existing tracks. Do not start E10 T06–T10, new infra audits, trading activation or generic engine work as a substitute.
