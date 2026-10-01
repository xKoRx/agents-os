# Echo Futures — D6 FINAL DESIGN FREEZE — Real NinjaTrader / Earn2Trade E2E

**Role:** TOP Principal Technical Architect / D6 Design Consolidation Specialist (no Manager, no Owner, no implementer)
**Date:** 2026-10-01
**Project:** [[Echo Futures]]
**Trigger:** `D6_N1 = PASS` — D6 design consolidation before the three D6 implementation shots.
**Physical baseline:** `D6_N1 = PASS` — read-only NinjaTrader vertical certified at Echo `xKoRx/echo@f0c82905d4eaf825c08e04f0bb97cab73e616ba5` (`origin/feature/d6-n1-readonly-vertical`), D5 frozen baseline `xKoRx/echo@13e087a3` intact beneath it.
**Verdict:** `D6_DESIGN_FREEZE = READY_FOR_MANAGER_REVIEW`

---

## 0. Evidence basis and verification method

Every design decision below is grounded in one of:

- **Physical certification (P):** N1 read-only certification + final account binding certification (`artifacts/d6-ninjatrader-n1-20261001/`), C0 transport certification, N1-R2/R3 remediations. Real AddOn sessions, real frames, `ORDERS_SENT = ORDERS_MODIFIED = ORDERS_CANCELLED = 0` throughout.
- **Frozen contract (F):** Architecture Candidate V2, Functional SPEC V1, Technical SPEC V1 (§14–§26 read at contract level), Acceptance Test Plan V1, Performance Resource Budgets V1, D5 Implementation Shots — all Owner-accepted 2026-09-29/30.
- **Source truth (S):** read directly at `f0c82905` during this design session: `capabilities/adapter.go` (ExecutionAdapter, SubmitOrder incl. `StopPrice` field, JournalRecord, ReconciliationReport, AdapterReadiness), `capabilities/readiness.go` (9-dimension conjunction), `capabilities/journal.go` (5-state M2 machine, `sameIntent`), `domain/operation.go` (`OrderType = MARKET|LIMIT` — no STOP yet), `domain/provider.go` (TransportEntitlement, binding `Validate()` fail-closed), `domain/execution.go` (session states), `cmd/futures-bridge/main.go` (topics `echo.order-commands.{account}.v1` → `echo.futures.execution-events.v1`).
- **Accepted correction (C):** C1-R1 F1 (STOP_MARKET) — Manager-accepted bounded D5 contract correction; C1-R1 F2 (OwnerRiskAcceptance model) — **SUPERSEDED by owner order (N1-R1)**: removed from product and configuration; entitlement was later corrected by owner to `ALLOWED` (N1-R2, ETCD DEV verified today: `/echo/development/futures-bridge/accounts/E2T-GAU50-01/binding/entitlement = ALLOWED`, 11 keys, `provider-external-account-id = "3"`).
- **First-party rules research (R):** Earn2Trade preflight artifacts (`artifacts/d6-earn2trade-preflight-20260930/`), GAU50 Evaluation row = HIGH evidence completeness.

Design filter applied to every addition: *"Is this required to execute one Echo strategy safely on one GAU50?"* — everything below answers yes; everything else was excluded (§13).

---

## 1. Current certified physical baseline

| Fact | Value | Evidence |
|---|---|---|
| NinjaTrader | Desktop 8.1.8.3, dev-win 192.168.31.132, owner interactive session | C0/N1 (P) |
| Tradovate transport | demo + Tradovate TCP endpoints alive; connection enumeration shows "Simulación" CBI while E2T account set is visible via `Account.All` | N1 §3, C1 §A (P) |
| AddOn | `EchoFeedAddOn` (AddOnBase) installed, compiled, connected; session `2f6a4d53…` (PID 1876); heartbeat, seq discipline, reconnect proven | N1-FINAL (P) |
| Feed channel | `echo.ntfeed.v1`, 8 observation families, **no command family**; relay `echo-nt-feed-relay` (release `7af6210a`) on Daedalus :9770; AddOn→relay one-way; relay never writes to the AddOn | N1 (P) |
| Market ingress | QUOTE/TRADE physically in `echo.futures.market-feed-candidates.v1`, frozen envelope (`source_id=NINJATRADER_ADDON`, `log_identity=ninjatrader-addon/<session>`, class-C identity, `offset=seq`) | N1 (P) |
| Selected account | `E2T-GAU50-01` → Name `RJARA114411201551`; NT `Account.Id = "3"` stable 2/2 observed NT restarts (bounded, not a guarantee) | N1-FINAL §10 (P) |
| Binding | ETCD DEV: `entitlement=ALLOWED`, `enabled=true`, `provider-id=EARN2TRADE`, `transport-id=NINJATRADER_BRIDGE`, `rule-set-id=GAU50-EVAL`, `external-contract-identifier=NQZ6`, `provider-external-account-id="3"` | ETCD RO read-back (S/P) |
| Account observations | balances (NLV 50000/cash 50000/0/0/bp 0), positions `[]`, orders `[]` with account resolved; executions primed-not-published semantics | N1-FINAL §12 (P) |
| Market data delay | demo feed `event_ts` exactly ~600 s behind arrival; dev-win clock verified correct; AddOn propagates `e.Time` faithfully | N1 §4.1 (P) |
| Entitlement | Owner corrected premise 2026-10-01 (N1-R2): Earn2Trade own-algorithm = `ALLOWED`, no attached conditions; `TransportSpec.Conditions` empty | N1-R2 (owner decision) |
| Protective order | GerardMM still emits protective `LIMIT` at stop level (physically marketable) — C1-R1 F1 correction **accepted but NOT yet implemented** @ f0c82905 | S (`domain/operation.go:41-42`, `gerardmm.go` protective path) |
| Not yet existing | No execution bridge session for any real transport (`buildSession` SIM-only), no REBUILD corpus producer, no market-freshness gate, no order-capable protocol family | C1 §B/§H, S |

**The gap this design closes:** from "observation certified, execution contracts frozen but transport-generic" to a concrete, MVP-sized execution design for exactly one GAU50 via NinjaTrader — without reopening any D4/D5 frozen contract except the Manager-accepted F1 correction, which this design freezes as implementation authority.

---

## 2. Frozen topology (D6 end state)

```text
                                   ┌──────────────────────── dev-win (owner session) ───────────────────────┐
                                   │  NinjaTrader Desktop 8.1.8.3                                            │
                                   │   └─ EchoFeedAddOn (AddOnBase, transport-only, no domain authority)     │
                                   │        ├─ market lane  ── outbound ──▶ nt-feed-relay (Daedalus :9770)   │  ← N1, UNCHANGED
                                   │        └─ execution lane ── outbound ──▶ futures-bridge (new listener)  │  ← N2/Shot 1
                                   └─────────────────────────────────────────────────────────────────────────┘
                                                                              │
   Strategy ─▶ Signal ─▶ Operation ─▶ GerardMM ─▶ ProviderRuleSet(admission/  │  Kafka (frozen D5 plane)
   (frozen D4/D5 Core plane)            Reservation/Revalidate) ─▶ M1          │
   echo.order-commands.{account}.v1 ──▶ futures-bridge ── M2 journal (journalfs)
                                          └─ NINJATRADER_BRIDGE adapter ───────┘ (execution lane)
```

Invariants preserved verbatim (frozen):

- Strategy → Signal → Operation → GerardMM → ProviderRuleSet → Futures Bridge → ExecutionAdapter → venue (frozen chain, zero renames).
- M1 = StateFun committed state + EXACTLY_ONCE transactional command egress (`echo.order-commands.{execution_account_id}.v1`); consumer uses committed transactional semantics (SPEC §18).
- M2 journal = durable write-ahead, `PREPARED → SUBMITTING → VENUE_BOUND → TERMINAL | AMBIGUOUS`, fsync before every mutating return (journalfs @ f0c82905, reused as-is).
- ReservationRevalidate → `RESERVED → EGRESS_AUTHORIZED` is the provider authorization point and is never renamed `egress_committed` (SPEC §16).
- Reconcile-before-unsafe-resubmit; no blind retry; `AMBIGUOUS` is fail-closed (SPEC §19.3).
- ProviderRuleSet = complete, read-only to MM context; `echo/provider_rules(account_id)` is the only account-wide policy authority (SPEC §17).
- One active Echo account (`E2T-GAU50-01`); the other four GAU50 evaluations receive no commands (per-account topic + per-account session + defence-in-depth, all frozen and implemented).
- Bridge has no domain authority (D2-07 §5); AddOn has no domain authority (this freeze, §6.6).
- EXACT_REPLAY/BACKTEST reuse boundary untouched; NinjaTrader never becomes a durable historical authority (one-shot bootstrap source only).

---

## 3. Account identity model (DI-1)

### 3.1 Three-layer identity (frozen)

| Layer | Identifier | Durability | Role |
|---|---|---|---|
| 1. Echo account identity | `execution_account_id` = `E2T-GAU50-01` | Durable, Echo-owned | The account everywhere in Echo: Operation owner key, Kafka keys, journal, binding prefix, readiness. Never derived from anything NinjaTrader-side. |
| 2. Provider/business account | `provider-account-ref` = NT `Account.Name` = `RJARA114411201551` (Tradovate-embedded account number) | Durable business reference (survives NT restarts; unique in discovery, match count 1/8) | **The authoritative binding identity.** This is what the owner selected (OD-2) and what names the real account at the provider. |
| 3. Platform/runtime id | NT `Account.Id` (Int64 rendered "3") | Runtime-local collection identity; stable 2/2 observed restarts, **no general guarantee** | Resolution hint + verification cross-check only. Its drift never changes the identity of the Echo account. |

Rationale from physical evidence: the N1 certifications demonstrated `Account.Id` is a small runtime-local enumerator ("0"–"7" incl. local NT accounts) whose cross-restart stability was observed but is undocumented platform behavior, while `Name` is the externally meaningful reference (N1-FINAL §7 explicitly defers this decision here). A design that keys durable identity on the Id would force re-config on platform re-enumeration; keying on `Name` makes Id drift a config-only refresh.

### 3.2 Binding configuration (evolution, additive)

ETCD `futures-bridge/accounts/E2T-GAU50-01/` gains one key:

```text
binding/provider-account-ref        = "RJARA114411201551"   ← NEW, authoritative
binding/provider-external-account-id = "3"                  ← existing key REINTERPRETED as platform-id hint (optional)
```

Rules:

- For `NINJATRADER_BRIDGE` bindings, `provider-account-ref` is **required**; `Validate()` fails closed without it. The id hint is optional.
- Resolution (AddOn): resolve by exact `Name` match among `Account.All`; **require match count == 1** (ambiguity or absence ⇒ fail-closed `PROVIDER_ACCOUNT_BINDING_NOT_VERIFIED`). If the id hint is present and the resolved object's `Id` differs ⇒ session degrades `RECONCILING`/`DISCONNECTED` with a distinct observable reason `PROVIDER_ACCOUNT_ID_DRIFT` — **never wrong-account data, never auto-remap**. Recovery from drift = owner refreshes the hint (config write, no identity change, no Echo-side restart of identity).
- Defence-in-depth (both lanes): the hello carries `expected_account_name` (+ id as evidence); the relay/bridge compares it against the binding **ref**. `MISMATCH` stays fail-closed exactly as N1 demonstrated (mismatched hello ⇒ account lane unresolved, market lane stream-level continues).
- Journal carry: `ProviderExternalAccountID` (frozen field) is populated with the **ref** going forward for NT bindings (it is the durable provider identity the journal pins; the platform id travels as evidence, not identity).

No new account-management surface, no account registry, no multi-account model. This is one binding with a corrected durable key.

### 3.3 What changes in code (scope)

- AddOn `ResolveAccount`: Name-primary + unique-match + id cross-check (currently Id-primary — N1 implementation; small, certified-safe inversion).
- `internal/binding.Load`: read `provider-account-ref`; `ProviderAccountBinding.Validate()` extension (fail-closed when a NT-transport binding lacks it).
- Relay hello match: compare ref (currently id).
- ETCD: one key write (`provider-account-ref`), keeping `provider-external-account-id="3"` as hint.

---

## 4. Real-time market-data readiness (DI-2)

### 4.1 Physical findings and platform answer

- The NinjaTrader path (`Instrument.MarketData.Update`) natively delivers Bid/Ask/Last tick-a-tick with venue timestamps (C1 FACT; N1 physically demonstrated Bid/Ask/Last frames end-to-end).
- The ~600 s delay observed is a property of the **demo feed connection** ("Simulación") the AddOn currently subscribes — not of the Tradovate path. First-party E2T stage model (R): Evaluation = "simulated evaluation with **real market data**". No second market-data architecture is introduced; the same NT path is the realtime authority once subscribed on the correct connection.
- **Feed affinity rule (new, required):** the AddOn must source market data for execution from the connection that hosts the bound account (the E2T/Tradovate connection), never from the local demo connection. Concretely: subscribe/resubscribe the instrument in the account's connection context after every (re)connect. A demo-feed subscription is physically detectable by the freshness gate below and must fail closed.

### 4.2 Freshness model (fail-closed)

The canonical stream `NQ:NQZ6` gains an explicit freshness dimension on its serving authority (`echo/market_stream`, additive to D2-06A readiness — no new authority):

```text
market_freshness(stream_id) ∈ FRESH | STALE | UNKNOWN
  UNKNOWN (initial / no evidence)            ⇒ treated as STALE (fail-closed)
  event_ts_age = DomainClock(now) − max(event_ts accepted)
  STALE if event_ts_age > freshness_bound          (detects delayed/replayed feeds — the 600 s demo case)
  STALE if no arrival within liveness_bound while the session calendar says the market is expected active
         (detects a dead feed; bound is per-stream config, NOT a frozen universal timeout — B2/manager rule)
```

- Timestamp authority: `event_ts` = venue event time propagated by the AddOn (`e.Time`, proven faithful in N1); arrival evidence = `receive_ts` at ingress; "now" = frozen `DomainClock` (SPEC §7). No wall-clock of the AddOn host is authoritative.
- Bounds are config (per stream, hot), not product invariants — per the D1 Front B manager corrections ("no frozen universal without-tick timeout").
- **Consumption (this is what makes stale feed unable to enable execution):**
  1. Strategy analytical readiness (SPEC §9 strategy state already owns readiness) requires `market_freshness = FRESH` for every demanded stream ⇒ STALE ⇒ strategy not READY ⇒ no Signals.
  2. Admission additionally refuses new risk while any stream demanded by the AccountStrategy's Strategy requirements is not FRESH (defense in depth at the Operation boundary).
  3. Readiness/Status surfaces expose the freshness state and its reason (visible degradation, never a silent green).
- Already-open risk is not orphaned by staleness: the protective `STOP_MARKET` rests venue-side (§5) and keeps protecting during a stale window; MM tightening pauses (no fresh decisions by design). This is the frozen M2 "protection lives at the venue" property doing its job.

### 4.3 D6 verification gate (before Strategy→execution is enabled)

`REALTIME_FEED_CERTIFIED`: on the E2T/Tradovate connection of the bound account — QUOTE/TRADE end-to-end into the canonical ingress with `log_identity` of the live session; measured `event_ts_age` p50/p95/p99 under `freshness_bound`; session calendar liveness demonstrated. The currently certified demo feed (`STALE`, ~600 s) must be shown replaced by a FRESH live-path subscription for the same instrument. Until this gate passes, `SubmissionCapabilitiesReady` cannot reach true for the binding (the freshness dimension feeds the §22 conjunction through the readiness inputs; connectivity alone is never readiness — SPEC §22).

---

## 5. Order model including STOP_MARKET (DI-3)

### 5.1 Domain primitive (C1-R1 F1, adopted as frozen implementation authority)

```text
OrderType    += OrderTypeStopMarket = "STOP_MARKET"        (domain/operation.go enum)
Order        += StopPrice *units.Price                     (LIMIT/MARKET unchanged; Validate: STOP_MARKET ⇒ StopPrice != nil, LimitPrice == nil)
OrderRequest += StopPrice   (mm.go)                        (engine.go switch: STOP_MARKET ⇒ StopPrice required)
SubmitOrderIntent += StopPrice  (operation/wire.go)
BridgeCommandEnvelope: project stop_price field-by-field (futuresruntime/runtime.go)
SubmitOrder (capabilities) already carries StopPrice @ f0c82905 — validation switch extended to accept STOP_MARKET
journalfs: Terms.StopPrice + sameIntent includes stop-level (nil-safe priceEqual pattern) so dedup distinguishes stops at different levels
```

Scope of change is exactly C1-R1's list: +1 enum value, +1 price field on six surfaces, +1 validation branch on three switches, +1 sameIntent term. **Level computation, monotonic tighten, crossed→MARKET path, GerardMM economics, claims, fills, reservations, EXACT_REPLAY: unchanged.**

### 5.2 GerardMM semantics (frozen behavior, corrected physical form)

- `protectiveOrder` emits `Type: STOP_MARKET, StopPrice: desired_level` (opposite side). For LONG: SELL STOP_MARKET below mark → rests at the venue; triggers only on deterioration. For SHORT: BUY STOP_MARKET above ask.
- Tighten stays monotonic cancel+replace comparing `desired` against `protective.StopPrice`.
- `PROTECTIVE_STOP_CROSSED` → cancel protective + MARKET exit — **unchanged** (a stop placed behind the market would fire instantly; the frozen guard remains correct).
- Between MM cycles the venue-side stop is the only protection — now physically true for the first time.

### 5.3 Native mapping and the no-synthetic-stop rule

- NinjaTrader native: `OrderType.StopMarket` via `Account.CreateOrder(...)` with stop price (reflection-verified present in 8.1.8.3). The order rests **server/venue-held** (Tradovate), consistent with official NT semantics: stop "waits for the price to pass the stop price, then becomes a market order".
- **Client-side / PC-simulated stops are prohibited** (NT documents local simulation as subject to connection loss and crashes — the exact failure D6 must not depend on). The AddOn never synthesizes protection; the bridge never transforms order types (transforming LIMIT→STOP in the adapter would lie about `Order.Type` and grant the transport trading authority — rejected in C1-R1, reaffirmed frozen).
- STOP_LIMIT and MIT were evaluated and rejected (fill-gap on the max-loss path; wrong primitive for protection) — C1-R1, adopted.
- **Capability gate:** the NT adapter's `CapabilityDeclaration.SupportedOrderTypes` includes `STOP_MARKET` **only after** the native venue-held gate passes (Shot 3): `Account.IsOrderTypeSupported(StopMarket)` on the bound account **and** physical proof the stop order survives an NT restart (visible in re-synced `Account.Orders` — a PC-simulated stop would not resuscitate). Until then `submission_capabilities_ready = false` ⇒ readiness fail-closed. If the gate fails, the transport is `UNSUPPORTED_FOR_V1_EXACT_SUBMISSION` — escalated, never approximated.
- TIF: protective orders carry the same TIF as today's terms (passthrough); NT maps to native `TimeInForce`. Shot 3 certifies end-of-session behavior against the GAU50 close window (§7).

### 5.4 Simulator compatibility

- SIM adapter declares `STOP_MARKET`; venue stores the type (already stored); fills remain scripted — no marketability model is introduced in V1 (explicit non-goal). Regression added: a resting protective order is stored/observed as `STOP_MARKET` with its `StopPrice`, and same-intent dedup distinguishes two stops at different levels. This keeps ATP semantics intact while the shape stops lying.

### 5.5 Restart/reconciliation behavior of the protective stop

Journal `VENUE_BOUND` + venue-held stop: after NT restart the stop reappears in re-synced `Account.Orders` (that is precisely the native gate evidence); the recovery barrier re-correlates it by client identity (`order.Name` = `client_order_id`) and native `Order.OrderId`; a stop missing from venue truth while journal says VENUE_BOUND is a reconciliation mismatch (fail-visible), not a silent reinstall. Reinstall of protection is a GerardMM decision in a later MM cycle — never an adapter-side automatic replay.

---

## 6. NinjaTrader execution transport (DI-4)

### 6.1 Dual-channel AddOn (frozen)

The AddOn keeps **exactly two outbound client connections**, each single-purpose:

| Lane | Terminator | Direction | Content | Status |
|---|---|---|---|---|
| Market lane | `nt-feed-relay` (Daedalus :9770) | AddOn → relay (one-way) | `echo.ntfeed.v1`, 8 observation families — unchanged | N1-certified, **zero churn** (the structural egress kill-switch of the feed lane is preserved forever) |
| Execution lane (new) | `futures-bridge` (new listener, config port) | Bidirectional | `echo.ntx.v1` — same wire framing/versioning/parser as `echo.ntfeed.v1` (reused), plus two new families | Shot 1 |

Rationale: the frozen topology makes the bridge the per-account session owner, M2 journal owner and only Kafka producer for execution observations. Terminating the execution lane in the bridge itself keeps the relay observation-only (its N1 no-command-family property remains structurally true) and avoids a proxy hop between adapter and journal. No Kafka inside the desktop (frozen). Separate auth token (`futures-bridge/ntx/auth-token` in ETCD DEV; never in repo).

### 6.2 Protocol families (`echo.ntx.v1`)

Reused families (AddOn → bridge, observation direction, same payloads as ntfeed): `hello | session | heartbeat | account | positions | orders | executions`.
New families:

```text
command        (bridge → AddOn)   {command_id, client_order_id?, action_id?, kind: SUBMIT|CANCEL|REPLACE,
                                   external contract identity, side, type: MARKET|LIMIT|STOP_MARKET,
                                   qty, limit_price?, stop_price?, tif?, physical_binding, provider_account_ref}
command_result (AddOn → bridge)   {command_id, client_order_id?, outcome: ACCEPTED|REJECTED|ERROR,
                                   nt_order_id?, nt_order_id_native?, reason?}
```

- The frozen `BridgeCommandEnvelope` (Core, field-by-field projection) remains the command source of truth; the adapter maps it 1:1 onto `command` frames. `command_result` is transport-level feedback only — order lifecycle truth continues to arrive exclusively via the `orders`/`executions`/`positions` observation families (frozen §20).
- Seq discipline, auth hello deadline, 64 KB frame limit, constant-time token compare, masking of account ids in logs, evidence sink semantics: identical to the certified ntfeed behavior.

### 6.3 Contract mapping (NT ↔ Echo, frozen for D6)

| Echo contract | NinjaTrader native | Notes |
|---|---|---|
| submit (`SubmitOrder`) | `Account.CreateOrder(...)` + `Account.Submit(order)`; async | `client_order_id` ⇒ `order.Name` (the only stable client-identity primitive — retention is a Shot 3 gate) |
| ack / venue-bind | `OrderUpdate` with `OrderState Accepted/Working` + `Order.OrderId` (native Tradovate string id) populated | Journal `VENUE_BOUND` requires this venue-side evidence, not the local `command_result` |
| reject | `OrderUpdate` `Rejected` (+ `AcceptedByRisk` = local NT risk rejection → also reject-class) | Outcome REJECTED; q_exec_max claim released per frozen claim-release facts |
| working | `Working` (after `Accepted`) | OrderObservation; Operation aggregate stays WORKING per D2-04 §3.2 |
| partial fill | multiple `ExecutionUpdate` events; `Order.Filled` accumulates; state `PartFilled` | Fill identity = `Execution.ExecutionId` (native, String); dedup `(execution_account_id, ExecutionId)` frozen |
| fill (final) | `Filled` | TERMINAL evidence |
| cancel | `Account.Cancel(...)`; ack = state **Cancelled** (`CancelPending/CancelSubmitted` are transport states) | `ActionResult`; late-fill conservation on cancel/fill race is frozen (D2-07 §11) — fills that won the race are kept |
| replace/change | `Account.Change(...)`; `ChangePending/ChangeSubmitted` → new `Accepted/Working` on the same native order (NT modify in place) | GerardMM tighten = cancel+replace (frozen); NT `Change` is used only where the frozen contract issues replace actions; **never** a silent adapter decision |
| native order identity | `Order.OrderId` (venue, String) + `Order.Id` (NT-local Int64, session-scoped) + `Execution.ExecutionId` (String) + `Execution.OrderId` | Correlate **by ids, never by event arrival order or object pointers** (NT documents unordered delivery across providers) |
| execution events | `Account.OrderUpdate / ExecutionUpdate / PositionUpdate / AccountItemUpdate` | Mapped to the five frozen families (§20) with correlation enrichment as frozen |
| position | `Account.PositionUpdate` / `Positions` — net per Account×Instrument | 1:1 with frozen `PositionUpdate` shape |
| account state | `Get(AccountItem, Currency)` | Same five balance fields as N1 (fail-visible on missing items) |

Event-ordering tolerance (Fill before ACK, interleaved partials) is already frozen behavior — no change.

### 6.4 Submit sequence under M2 (frozen sequence, concrete NT mapping)

```text
1. journal.Prepare(PREPARED, full terms)              — fsync
2. journal.MarkSubmitting                             — fsync  ← durable BEFORE the channel write
3. send `command SUBMIT` over the execution lane      ← point-of-no-return (first write that can reach the venue)
4. await command_result (bounded timeout)
   ACCEPTED (local NT order identity captured)       → record evidence; NOT yet VENUE_BOUND
   REJECTED                                          → record; claim-release path per frozen facts
   timeout / disconnect / AddOn gone                 → journal AMBIGUOUS (MAY_HAVE_EXECUTED); no blind retry
5. OrderUpdate Accepted/Working + OrderId             → journal VENUE_BOUND (provider_order_ref = Order.OrderId)
6. executions → Fill facts (dedup by ExecutionId)     → TERMINAL on finality
```

Cancel/Replace follow the same shape with their action ids. The bridge sends a given command **at most once** per journal authorization — the AddOn executes each command it receives exactly once and holds **no** dedup/policy state (there is no channel-level redelivery of an already-answered command; outcome uncertainty is always resolved by reconciliation, not resend).

### 6.5 Reconciliation surface (used by the frozen barrier)

Adapter `Reconcile` over NT, per non-terminal journal record and in order: `Account.Orders` scan by `order.Name`; `Account.FindOrderById` (in-session id); `Account.Executions` scan by `Execution.OrderId`/`ExecutionId` within the retention horizon (`Account.LookbackDaysExecutions/Orders` config). Found ⇒ adopt outcome (`VENUE_BOUND`/`TERMINAL`); authoritatively absent within horizon ⇒ `ResubmitApprovedByAbsence`; neither ⇒ `AMBIGUOUS`. `ListOpenOrders` = live `Account.Orders` snapshot; uncorrelatable live orders ⇒ `UnknownLiveOrders` quarantine (fail-visible, never cancelled, never adopted). `PositionSnapshot` = fresh `Positions` (+`GetPosition`). All of this exists frozen at the interface (`adapter.go @ f0c82905`); Shot 1 implements the NT-side lookups.

### 6.6 AddOn authority boundary (hard)

The AddOn: resolves the configured account (§3.2), captures events, subscribes market data, executes received commands verbatim on the resolved account, reports outcomes. It contains **no** rule evaluation, no MM/strategy logic, no dedup policy, no retry policy, no price validation beyond term-shape, no state that survives restart except its local config file. Mismatched command (wrong account ref / unresolved instrument) ⇒ `command_result REJECTED` fail-closed. Grep-discipline gates (`Submit/Change/Cancel/Flatten/CreateOrder` absent in feed-only builds) continue as structural safety evidence; the N2 build adds exactly the command execution path and nothing else.

---

## 7. M1 / M2 physical mapping (DI-5)

Frozen meanings are not restated here — only the physical evidence that establishes each on the NinjaTrader path:

| Boundary | Frozen meaning | Physical evidence that establishes it (NT path) |
|---|---|---|
| **M1** | StateFun committed state + EXACTLY_ONCE transactional command egress | The command envelope is visible in `echo.order-commands.E2T-GAU50-01.v1` produced transactionally with the checkpointed Operation state (frozen `futures_operation.go` path — unchanged by D6) |
| **M2 start** | Durable PREPARED before any transport step | journalfs `Prepare` fsync return (journalfs @ f0c82905) before the `command` frame is written to the execution-lane socket |
| **M2 point-of-no-return** | SUBMITTING durable before the first call/write that can reach the venue | journalfs `MarkSubmitting` fsync return before the execution-lane socket write (the socket write is the first physical step with venue reach; everything after — TCP, AddOn, `Account.Submit`, Tradovate — may have executed) |
| **VENUE_BOUND** | Physical existence proven, provider identity reconciliable | `OrderUpdate` Accepted/Working with native `Order.OrderId` observed on the observation families |
| **TERMINAL** | Venue finality + fills reconciled | `Filled/Cancelled/Rejected` final state + executions recovered with `ExecutionId` dedup |
| **Crash in SUBMITTING** | MAY_HAVE_EXECUTED, no blind retry | Barrier: reconcile per §6.5; absence provable only within retention horizon; otherwise AMBIGUOUS fail-closed |

Restart safety: the journal is bridge-local durable storage (journalfs, single writer per account) — an AddOn or NT restart cannot lose it; a bridge restart reloads non-terminal records in the barrier (`ListNonTerminal`) exactly as frozen. No D6 change to M1/M2 semantics.

---

## 8. Journal / idempotency / reconciliation (frozen, NT-specific facts)

- **No native venue submit idempotency exists** in the NinjaScript API (C1 FACT) ⇒ this transport belongs to the frozen "idempotency via journal + reconciliation" class. Nothing new is invented; the frozen machinery is the design.
- Dedup identities (frozen): command/journal key `(execution_account_id, client_order_id)`; fill `(execution_account_id, Execution.ExecutionId)`; actions by stable `action_id`/`replace_request_id`. `sameIntent` extended with `StopPrice` (§5.1).
- Client identity round-trip: `order.Name` must return on every `OrderUpdate` and in `Account.Orders` after reconnect/restart — **Shot 3 gate** (retention). `Order.Id` (Int64) is session-scoped and never used across sessions.
- Reconciliation horizon: `LookbackDaysExecutions/LookbackDaysOrders` must exceed the maximum tolerable outage; the barrier fails closed (`AMBIGUOUS`/not-ready) when the horizon cannot cover an outage (frozen R5 rule). Shot 3 measures the actual retention of the GAU50/Tradovate account and pins config.
- M2 journal store: journalfs as certified; deployment keeps it on durable local disk of the bridge host (Performance Budgets §4.5 bounded-state budget applies; measurement obligation listed in §12).

---

## 9. ProviderRuleSet placement (DI-6)

- **Authority unchanged:** only `echo/provider_rules(account_id)` enforces account-wide policy; GerardMM reads the complete RuleSet read-only for its economic decisions; no rule lives in the AddOn, the bridge, the Strategy or MM-as-authority. Reservation + mandatory `ReservationRevalidate` precede every egress (frozen §15–§16) — no order can leave without them (enforced by frozen code paths; NT work adds no bypass).
- **GAU50-EVAL v1 materialization (Shot 1, config/domain-data work):** an ACTIVE `ProviderRuleSet` `GAU50-EVAL` v1 for `EARN2TRADE/GAU50` with mandatory `SourceRefs` (the accepted preflight artifacts + N1-R2 owner correction). Enforceable typed families:
  - Capacity cap: **max 6 contracts** (scope ACCOUNT, typed family per frozen capacity model).
  - Trading window: **no new risk after 15:50 CT; flat window 15:50–17:00 CT** (admission/window rule per frozen admission contract; GerardMM exits respect it under frozen window semantics).
  - Account-day economics context: EOD drawdown **USD 2,000**, daily loss limit **USD 1,100** — these are provider hard constraints against which the owner's GerardMM SL/TP monetary model (day 1/2 = SL 2000 / TP 1500) is configured; MM economics remain owner configuration (frozen D4), not RuleSet caps.
  - Documented non-enforceable facts (recorded via SourceRefs/notes only — **never encoded as fake caps**): 30% consistency rule, news allowed, no minimum trading days. Consistency is a provider-monitored account outcome, not a pre-egress quantity in any frozen typed family; encoding it as a cap would pretend an enforcement that does not exist.
- `TransportSpec.Conditions` stays empty (`ALLOWED` per N1-R2 owner correction — plain grant, general conduct prohibitions only).
- Live/LiveSim rule profiles (trailing drawdown etc.) are **not** modeled in V1 (no Live objective in MVP); a program transition is a config+RuleSet version event, not code.

---

## 10. Warm-up + strategy runtime path (DI-7)

End-to-end path (all stages frozen; D6 builds the missing wiring only):

```text
Realtime:  AddOn (account's connection) ─▶ relay ─▶ echo.futures.market-feed-candidates.v1
           ─▶ echo/market_stream (canonical, freshness FRESH) ─▶ echo/market_analytics (bars)
           ─▶ echo/strategy_engine (S1/S2, analytical READY) ─▶ Signal ─▶ fan-out ─▶ echo/operation
Warm-up:   AddOn BarsRequest (Minute, one-shot ≈17+ days) ─▶ 5m-exact deterministic TRADE synthesis
           ─▶ published through the SAME canonical ingress BEFORE RUN_START ─▶ REBUILD corpus
           ─▶ RUN_START control envelope pins ReplayAnchor (refs+digest in run manifest) ─▶ strategy READY
Execution: Operation ─▶ GerardMM ─▶ admission/ReservationRevalidate (GAU50-EVAL v1) ─▶ M1
           ─▶ bridge ─▶ M2 journal ─▶ execution lane ─▶ AddOn ─▶ Account (GAU50) ─▶ Tradovate venue
```

Minimum warm-up requirement (frozen inputs): S2 needs 51 H4 + 20×5m + headroom (lookback 64) ⇒ ≥17 days of session history; S1 needs 5m OHLC for the NY opening range. 5m-exact synthesis (4 deterministic TRADE events per 5m bucket) reproduces every frozen warm-up value exactly (C1 §B SUPPORTED_INTERPRETATION, accepted here as design with the fidelity gate below). Failure ⇒ `WARMUP_INCOMPLETE` ⇒ analytical readiness not READY (fail-closed, already frozen downstream behavior). NT stays a one-shot bootstrap source; the corpus is pinned in the run manifest; NT is never consulted at replay.

Fidelity gate (Shot 3): warm-up corpus through the real path yields S1/S2 warm-up values byte-identical to the S12-certified expectations (replay determinism discipline).

---

## 11. Recovery model (DI-8)

All cases resolve through the frozen barrier (`RunRecoveryBarrier` steps 1–8) + adapter NT lookups; **no case replays commands blindly**:

| Case | Resolution |
|---|---|
| Echo (Core) restart | Frozen StateFun recovery + M1 EXACTLY_ONCE redelivery semantics — unchanged; bridge journal unaffected |
| Futures Bridge restart | Journal reload (`ListNonTerminal`) → full barrier → readiness re-conjunction before new risk |
| AddOn reconnect | AddOn reconnects (proven in N1), fresh hello with expected ref; bridge verifies binding, re-syncs account event streams; seq discipline rejects stale/duplicate frames (proven behavior) |
| NinjaTrader restart | Bridge/AddOn lane drops → DISCONNECTED → AddOn re-announces; barrier re-verifies `Account.All` (§3.2 resolution), re-syncs Orders/Executions/Positions; server-held orders survive venue-side (that is the §5.3 native-stop gate); retention gates apply |
| Connection loss (NT↔Tradovate) | AddOn session/connection observations + event-stream staleness ⇒ readiness drops (`ORDER_EXECUTION_EVENT_STREAM_NOT_HEALTHY`); reconnect → resubscribe → barrier; missed fills recovered from `Executions` horizon with `ExecutionId` dedup |
| Working order during restart | Venue-side order re-synced in `Account.Orders`; journal record still VENUE_BOUND; correlated by `order.Name`+`OrderId`; no action until correlation completes; uncorrelatable live orders → `UnknownLiveOrders` quarantine (fail-visible) |
| Submit outcome ambiguous | §6.4 step 4: journal AMBIGUOUS (MAY_HAVE_EXECUTED) → reconcile-before-resubmit; retry legal only via `ResubmitApprovedByAbsence`; otherwise stays AMBIGUOUS and blocks new-risk readiness (`UNRESOLVED_M2_AMBIGUITY`) |
| Partial fill before disconnect | Recovered from `Executions` history with `ExecutionId` dedup; late fills after cancel conserved (frozen); Operation exposure converges from Fill facts |

New-risk stays off through the entire barrier in every case (frozen §22).

---

## 12. Observability / readiness

- **Readiness conjunction:** frozen 9-dimension `EvaluateExecutionReadiness` unchanged; the freshness dimension enters through analytical/admission gating (§4.2) and is additionally surfaced as its own status reason (`MARKET_DATA_NOT_FRESH`) so degradation is actionable.
- Visible-degradation principle (N1-proven style): every gate emits a deterministic reason — `PROVIDER_ACCOUNT_ID_DRIFT`, `PROVIDER_ACCOUNT_BINDING_NOT_VERIFIED`, `MARKET_DATA_NOT_FRESH`, `SUBMISSION_CAPABILITIES_NOT_EXACT_READY` (until the native-stop gate passes), `UNRESOLVED_M2_AMBIGUITY`, `UNKNOWN_LIVE_ORDERS_QUARANTINED`, `ENTITLEMENT` state, `WARMUP_INCOMPLETE`. No silent greens.
- Session/health surfaces: ExecutionSessionObservation (`CONNECTED/AUTHENTICATED/DISCONNECTED/RECONCILING`) per frozen family; AddOn heartbeat counters (frames, order_events semantics as certified); lane health (relay + execution lane separately); OTEL as available.
- Performance measurement obligations (D6 certification, per Performance Budgets V1 "MEASUREMENT REQUIRED IN D6"): account-scale topology evidence for the one-account vertical, market ingestion p50/p95/p99, event-to-bar latency, evaluation latency, Signal→delivery, SignalDelivery→MM decision, execution-event→MM decision, admission/revalidation latency, M2 journal fsync cost, plus the freshness bounds calibration (§4.2). No fabricated SLOs; measurements recorded in the Shot 3 certification artifact.

---

## 13. Explicit non-goals (reaffirmed)

No provider-specific Strategy; no provider-specific GerardMM subclass; no copier; no multi-account coordinator; no generic plugin framework; no provider DSL; no saga/workflow framework; no global sequencer; no global event sourcing; no snapshots framework; no portfolio engine; no provider optimizer; no cross-host takeover; no rollover subsystem (hot mapping stays owner-managed); no `HARD_CAP_WINS`, `max_admissible_qty`, `WIND_DOWN`; no broad Core redesign; no second market-data architecture; no marketability model in the simulator; no client-side synthetic stops; no order-type transformation in the adapter; no dedup/retry/policy state in the AddOn; no direct Tradovate REST/WS path in V1; no Live/LiveSim rule modeling; no account-management platform; no multi-GAU50 concurrency.

---

## 14. Acceptance gates (D6)

Structural (Shot 1, software-verifiable):

1. G-F1: STOP_MARKET correction complete (domain→engine→wire→envelope→journal/sameIntent→GerardMM→sim) with green regressions; protective order physically resting shape asserted in sim.
2. G-ID: Name-primary binding with unique-match + id-drift fail-closed behaviour in AddOn, relay/bridge hello defence, and `Validate()`; migration key written; wrong-account data structurally impossible.
3. G-NTX: execution-lane protocol (auth, seq, command/command_result families) with ≥95% coverage on new logic; feed lane byte-unchanged.
4. G-ADAPTER: NINJATRADER_BRIDGE adapter implements the frozen `ExecutionAdapter` with NT lookups; `buildSession` transport branch; capability declaration excludes STOP_MARKET until G-STOP passes.
5. G-FRESH: freshness dimension FRESH/STALE/UNKNOWN on the serving authority + readiness/admission consumption + status surface; stale-demo scenario test (600 s lag ⇒ no new risk).
6. G-RULES: GAU50-EVAL v1 ACTIVE with mandatory SourceRefs; max-6 cap + 15:50 CT window enforced through frozen admission/reservation paths; non-enforceable facts documented-not-encoded.
7. G-WARMUP: REBUILD corpus producer path publishes canonical envelopes pre-RUN_START with anchor pinning; S12-style fidelity regression.
8. G-EGRESS-0: with no owner authorization, zero physical orders are possible (bridge not enabled for the account / capability gate / structural grep gates), demonstrated by tests + deployment state.

Physical (Shot 3, owner-gated — none may be fabricated from sim evidence):

9. G-REALTIME: live-connection feed freshness within bounds (§4.3).
10. G-STOP: native venue-held STOP_MARKET (`IsOrderTypeSupported` + stop visible in `Account.Orders` after NT restart).
11. G-ID-Retention: `Order.Name` + `Order.OrderId` retention across reconnect/restart; `ExecutionId` uniqueness/stability realtime↔history↔restart.
12. G-HORIZON: `LookbackDays*` retention measured vs tolerable outage; config pinned.
13. G-E2E: one controlled owner-authorized order cycle on the selected GAU50 (entry MARKET + protective STOP_MARKET install + tighten via cancel/replace + cancel + flat), journal states VENUE_BOUND/TERMINAL observed, fills deduped, readiness transitions demonstrated; restart/reconnect drill during a working protective stop; zero unknown live orders at close-out.
14. G-PERF: §12 measurement set recorded.

---

## 15. Implementation slicing (exactly three shots)

### Shot 1 — IMPLEMENTATION (egress structurally disabled)

Scope: §3 (identity model + migration), §5 (F1 STOP_MARKET complete stack), §6 (execution lane + adapter + transport branch), §4.2 (freshness), §9 (GAU50-EVAL v1), §10 (warm-up/REBUILD producer path), gates G-F1…G-EGRESS-0, full `go test -race -cover` suites + regressions (canonical command per repo rules; no global `go test ./...`), fresh branch FF on `f0c82905`, push FF, zero orders.
Must NOT: enable the bridge session for the account; add STOP_MARKET to NT capability declaration; touch D5-frozen contracts beyond the enumerated F1 surfaces; touch the feed-lane AddOn behaviors certified in N1 except the account-resolution inversion (§3.3).

### Shot 2 — ADVERSARIAL REVIEW (independent, on Shot 1 candidate)

Reviewers challenge against frozen contracts + N1 physical evidence, minimum adversarial set: M1/M2 boundary violations; double-submit paths (timeout/redelivery/reconnect); Id-drift and duplicate-Name account resolution; stale-feed enablement (any path to a Signal or admission with STALE feed); protective stop lifecycle (tighten races, crossed-window, restart during VENUE_BOUND stop); cancel/replace + late-fill races; quarantine correctness; journal/sameIntent stop-level dedup; entitlement/binding fail-closed; GAU50-EVAL values vs SourceRefs; warm-up fidelity and anchor pinning; AddOn authority creep; scope creep vs §13. Output: findings register (BLOCKER/MAJOR/MINOR) — no code changes during review.

### Shot 3 — REMEDIATION + FINAL CERTIFICATION (owner-gated egress)

Fix Shot 2 findings; then execute the physical ladder in order, each gate blocking the next: G-REALTIME → G-STOP → G-ID-Retention → G-HORIZON → G-E2E (single controlled cycle + restart drill) → G-PERF → independent acceptance verdict. Emits (or refuses) the `EF_D6_E2E_PASS` candidate. **`OWNER_PHYSICAL_EGRESS_AUTHORIZATION_REQUIRED` stands immediately before G-REALTIME/G-STOP/G-E2E**: a control-plane approval (owner instruction recorded in project note/session evidence) — deliberately NOT a product field, class or table (the owner explicitly rejected the `OwnerRiskAccepted` product model in N1-R1; this design does not resurrect it in any form).

---

## 16. Owner decision register

| ID | Decision | Status |
|---|---|---|
| OD-D6-1 | **Physical egress authorization** for `E2T-GAU50-01` before first real order (covers G-REALTIME test traffic, G-STOP stop install, G-E2E cycle) | REQUIRED before Shot 3 physical ladder; control-plane approval, no product artifact |
| OD-D6-2 | **Ratify GAU50-EVAL v1 rule values** (max 6; DD 2000 EOD; DLL 1100; 15:50 CT window; consistency 30% documented) materialized from the 2026-09-30 preflight before first egress — terms may have changed since research date | REQUIRED (config act with provenance) |
| OD-D6-3 | **Realtime data provisioning**: conditional escalation only — if G-REALTIME measures the live E2T/Tradovate feed stale/delayed (not expected per first-party stage model), owner decides data entitlement/alternative | CONDITIONAL (escalate only on G-REALTIME failure) |
| OD-D6-4 | AddOn installation/config/restart cycles on dev-win remain owner-assisted operational steps (existing ACL reality, N1-proven checklist pattern) | STANDING (operational, not architectural) |

No owner decision is required for: the account identity model (explicitly delegated to the Primary Manager by the N1 certification), the STOP_MARKET correction (Manager-accepted truth-of-contract), freshness bounds (technical config), or the shot slicing (manager).

---

## 17. /verify checklist (design closure)

- No contradiction with D5 frozen contracts — verified against SPEC §14–§26 and source @ f0c82905; the only D5 delta is Manager-accepted F1 (enumerated surfaces).
- No provider logic in Strategy/MM — ProviderRuleSet authority untouched; GAU50 values live in RuleSet/config only.
- No dependence on `Account.Id` as durable identity — Name-primary model with Id as verified hint.
- No delayed feed can enable execution — freshness gates analytical readiness + admission; demo-lag scenario fail-closed by design; G-REALTIME physical gate.
- Protective order is not LIMIT — STOP_MARKET frozen; GerardMM emission corrected by mandate; LIMIT shape impossible after G-F1.
- Native STOP_MARKET path explicit — server-held only, capability-gated, synthetic prohibited, restart-proof required.
- One active account remains sufficient — per-account topic/session/journal/binding all frozen and reused; nothing multi-account added.
- No order leaves without ProviderRuleSet + ReservationRevalidate — frozen Core paths reused; no transport bypass exists (bridge/addon have no admission authority).
- M1/M2 coherent — meanings untouched; physical evidence table §7.
- Ambiguous submits never blindly retried — §6.4/§11; retry only via authoritative absence.
- Restart reconciliation explicit — §11 case table over the frozen barrier.
- AddOn is not a business-domain authority — §6.6 hard boundary; commands verbatim, no policy state.
- Scope MVP-sized — every addition mapped to "required to execute one strategy safely on one GAU50"; non-goals §13.
