---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D1 Analysis Pack]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
aliases:
  - Echo Futures D2-05B
  - EF Session Calendar
tags:
  - kind/doc
  - area/echo
  - echo-futures
  - architecture-design
created: "2026-09-26"
updated: "2026-09-26"
---

# Echo Futures — D2-05B Session Calendar

> [!info]+ TOP B result
> D2-05B — Session / Calendar. Design input for D2-05 integration. Echo baseline verified at 372af59a7b83604781346613da01e3d510ea1360 with no delta. No product code was changed.

## 1. Verdict

TOP_B_RESULT = READY_FOR_INTEGRATION.

V1 needs one reusable exchange-calendar authority with IANA timezone semantics and explicit exception dates. Exchange availability, ProviderProgram overlays and Account DayBoundary remain three distinct authorities.

No calendar microservice, no universal CME formula and no fixed UTC offsets.

## 2. Minimal model

### ExchangeCalendar

Stable identity for one exchange/product calendar authority.

Fields:

- calendar_id.
- timezone: IANA name such as America/Chicago.
- weekly_sessions: recurring weekly trading windows expressed in local calendar time.
- maintenance_breaks: recurring local windows inside otherwise-open sessions.
- session_date_rule: minimal explicit rule for assigning an exchange/session date from a timestamp.
- exception_dates: holiday/closed-day/early-close/session overrides keyed by local calendar date.
- product_overrides: optional sparse overrides only when a product materially differs from the base calendar.

The model stores semantic local clock time plus IANA timezone. It does not materialize permanent UTC offsets because DST changes them.

### ExchangeSession

ExchangeSession is the resolved runtime view for a timestamp/calendar, not a second conflicting source of truth.

Resolved fields:

- calendar_id.
- session_date.
- opens_at UTC.
- closes_at UTC.
- maintenance/open intervals for that session date.
- optional named windows resolved for that date.

A timestamp can therefore answer:

    is_exchange_open(ts)
    session_date(ts)
    next_boundary(ts)

without Strategy knowing timezone arithmetic.

## 3. Trade/session date

The calendar owns the conversion:

    event timestamp UTC
      -> local timestamp in calendar IANA timezone
      -> applicable weekly session + exception
      -> session_date

The session_date is a semantic market date and may differ from the civil date of session open. For overnight futures, an event during the prior civil evening may belong to the next session/trade date.

V1 does not hardcode one global CME formula. Each ExchangeCalendar carries its own minimal date-assignment rule plus exceptions.

LIVE, REPLAY and BACKTEST must call the same pure calendar/session resolution contract for identical timestamp + calendar revision/input data.

## 4. Holidays, early closes and maintenance

Precedence:

1. explicit exception for local calendar date/product;
2. product override if configured;
3. recurring base weekly schedule.

An exception can:

- mark CLOSED;
- replace open/close;
- replace maintenance intervals;
- add/remove named windows when needed.

Early close changes the resolved exchange session boundary. Maintenance is modeled as closed intervals inside the session, not as a second DayBoundary.

No rule assumes every CME product shares identical holiday hours.

## 5. Named Strategy sessions

Use NamedTradingWindow as a small config object attached to a calendar, not another calendar engine.

Fields:

- window_id / stable name.
- calendar_id.
- local start/end expression relative to the resolved session/civil day.
- optional applicability to a named exchange segment such as RTH/ETH.
- optional weekday/product scope when materially required.

Examples can include NY, London, CME_RTH, CME_ETH and custom owner-defined windows.

Strategy references window_id. Runtime resolves that name through the same ExchangeCalendar authority. Strategy never hardcodes UTC offsets.

A custom window can be narrower than exchange availability. It does not redefine whether the exchange is open.

## 6. Provider overlay

ProviderProgram rules are overlays evaluated after exchange resolution.

Example:

    ExchangeSession = OPEN
    ProviderRuleSet = NO_NEW_RISK after 15:10 CT
    result = exchange physically open, provider admission DENY_NEW_RISK

Provider overlays never mutate ExchangeCalendar.

Forced-flat is stronger: when the provider cutoff is reached, the provider safety plane emits termination intent to existing Operation state owners, per D2-04. It does not mark the exchange session closed.

## 7. Account DayBoundary

Account DayBoundary remains account/economic accounting semantics used for daily HWM, daily loss and reset calculations.

It has its own:

- account/provider ruleset timezone.
- reset local time.
- resolved daily boundary.

It does not:

- close ExchangeSession;
- change session_date;
- roll Contract;
- close bars by itself.

An Account daily reset may occur while the exchange remains open.

## 8. Bar contract for D2-06

D2-05B does not design the bar builder. It freezes only the required dependency contract:

- bar bucketing receives calendar/session identity or queries the same CalendarResolver;
- bars cannot span exchange-closed maintenance gaps unless a later explicit bar policy says so;
- session-scoped bars use session_date from ExchangeCalendar;
- a bar's forming/closed decision must respect resolved session boundaries and early-close overrides;
- replay/backtest must inject the same calendar definitions/exceptions as live.

D2-06 remains responsible for event-time ordering, late events and exact bucket mechanics.

## 9. Persistence / hot config

PostgreSQL is source of truth for ExchangeCalendar, recurring schedules, named windows and dated exceptions. Control-plane changes publish compacted calendar config.

Core/Market runtime keeps a ready-gated in-memory CalendarResolver. The cache follows the existing compacted-topic pattern: full initial load, then hot updates.

For determinism, a replay/backtest run must bind to an explicit calendar dataset/revision/input snapshot even though D2-01 forbids a generic domain version framework. This is run-input provenance, not an ExchangeCalendarVersion entity.

Live hot updates apply to future timestamp resolution. They do not rewrite already-emitted market facts/bars; exact replay of a historical run uses its recorded calendar input set.

## 10. Echo V3 physical map

| Current piece | Classification | Why |
| --- | --- | --- |
| v3/core/internal/functions/account_sync.go · DayBoundaryCache · blob b0f8f1ce426ce9f5ac6285bd97a990624bd6ca9e | REUSE ACCOUNT-DAY PRIMITIVE / REPLACE AS MARKET CALENDAR | IANA location loading and local reset calculation are useful account-day primitives. The cache is tied to prop_rulesets, has UTC 23:00 fallback and no holidays/maintenance/session-date semantics; it must never become ExchangeCalendar. |
| v3/core/internal/functions/account_sync.go · EnrichedAccountSnapshot flow · same blob | REUSE | Good pattern for computing account daily state and feeding rule evaluation without synchronous hot-path SQL. |
| v3/core/internal/functions/automation_evaluator.go · AutomationEvaluatorFn · blob 9503410ef0af9768b8225a4be735d17a8c115014 | REUSE PATTERN | Stateless evaluation from enriched state + exactly-once action egress fits provider/account safety triggers. Calendar resolution itself belongs in a dedicated domain component, not in this function. |
| v3/bridge/internal/config_cache.go · ConfigCache · blob 1f46133344022b1193e15d0566c2f76e4354ff44 | REUSE PATTERN | Compacted bootstrap and hot-update cache mechanics fit calendar/config distribution. |
| Gateway/Hasura control plane | EXTEND | Good authority/update path for calendar and exceptions; must stay out of market hot path. |
| Any fixed-offset/session logic outside the canonical resolver | REPLACE / DEFERRED_DEBT | Do not propagate fixed UTC assumptions into Futures. |

## 11. Acceptance semantics

### Early close

A dated holiday override changes closes_at for the resolved ExchangeSession. The same input calendar makes LIVE and REPLAY derive the same session_date and boundaries.

### Account reset

An account can cross its DayBoundary while ExchangeSession remains OPEN. Only account daily HWM/loss state resets; Contract and exchange session are unchanged.

### CME open/provider block

Calendar says OPEN; ProviderProgram overlay says DENY_NEW_RISK. No OPEN materialization for that account, while exchange/session facts remain OPEN.

## 12. Risks / non-blocking unknowns

- The authoritative upstream source/import process for future holiday calendars is implementation/research scope. The domain model only requires durable dated exceptions.
- Exact product-level CME differences are represented by sparse overrides; do not pre-populate a taxonomy until real instruments require it.
- Historical replay correctness requires calendar input provenance. This is a D2-06/run-contract integration detail, not a blocker for D2-05.

OWNER_DECISIONS_REQUIRED = NONE.
