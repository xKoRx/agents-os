# Lane A (market analytics timers) — Shot 3 remediation evidence

Worktree: /home/kor/aranea/work/d5-shot3-20260929/wt-a-market, branch shot3/lane-a-market.
Baseline before any change: v3/core `go test ./internal/...` ok; v3/sdk `go test ./futures/...` ok; S12 suite ok.
Frozen Shot 1 base: 4c41ee77 (+ wire-seam 5d02adcf, harness 9275fa74). Working tree clean at end.

Authorities applied: D2-06C §5 (event time vs runtime order decoupling), §6 (DomainClock / Schedule=SendAfter durable, generation replace semantics), §7 (TimerFired identity (timer_id, generation); stale firing = deterministic NO-OP, never domain execution), §9 (same-instant precedence), §12 (session transitions are scheduled inputs; hot calendar correction re-agendas prospectively; the chain never dies), §15/§16 (TimerFired journaling in admission position); ATP MKT-14 ("timer close without next tick"), MKT-15 ("internal break grid").

---

## F-A-01 (BLOCKER) — bar/session timers were immediate sends, not temporal firings

- Finding: `ensureBarTimer` (~:675-695) and `sendSessionTimer` (~:829-840) delivered `BarCloseTimerFired`/`SessionTimerFired` with `ctx.Send` (immediate self-send). The bus (`busContext.SendAfter` ~:431) discarded the delay and `PendingMessage` had no fire-time field. Observed defect reproduced: one trade through the plain FIFO drain cascaded the immediate session chain until the 100000-message dispatch budget tripped, and the bar-close firing closed the 09:30 bar at the first trade (13:30:50Z) instead of at the 13:35:00Z boundary.
- Authority: D2-06C §6 (LIVE timers = durable `ctx.SendAfter`; deadline in runtime logical time), §7 (a firing whose instant the clock has not reached is never a logical input), §12 (scheduled inputs, never polling). No new scheduler service, no new state owner, no goroutines — only the existing `ctx.SendAfter` / bus delayed-delivery capability.
- Product fix (`v3/core/internal/functions/futures_market_analytics.go`):
  - `ensureBarTimer` keeps the (timer_id, generation) identity and sends through `sendBarCloseTimer` → `ctx.SendAfter(boundary − now, clamped ≥ 0)`;
  - `sendSessionTimer` → `ctx.SendAfter(AtUTC − now, clamped ≥ 0)`.
- Runtime/test-bus fix (`v3/core/internal/futuresvertical/bus.go`): `PendingMessage.FireAt` (delivery instant, zero = immediate); `Bus.SetClock`; `busContext.SendAfter` / `SendAfterWithCancellationToken` / `CancelDelayedMessage` real delayed semantics (token-based best-effort cancel); `Drain`/`DrainStep` hold back future-dated sends wherever they sit (never blocking deliverable messages behind them); `DrainWithPolicy` prefers `FireAt` over the payload-decode fallback (due-ness is mathematically identical: `max(clockNow, boundary) ≤ now ⇔ boundary ≤ now` for a monotone clock — so vertical bar-close timing is unchanged). Harness (`harness.go`) wires the vertical's `domain.VirtualClock` into the bus (`v.Bus.SetClock(clock.Now)`).
- Unit test infra (`v3/core/internal/functions/testutil/statefun_mock.go`): MockContext now honors delay via a controllable clock — `SetClock`, delayed queue with fire-at instants, `GetDelayedMessages`, `DeliverDue(fn)` (delivers due firings through the real `fn.Invoke` in fire-time order with a livelock bound) and token cancellation.
- Masked tests rewritten (they recorded without delivering and manually re-invoked firings):
  - `TestFuturesMarketAnalytics_TimerClosesWithoutNextTick_MKT14` — schedules, asserts NO immediate timer send, asserts the firing cannot become an input before the boundary (DeliverDue at 09:34:59 closes nothing), exactly one BAR_CLOSED at 09:35 with data to 09:30:50, quiesced consumed schedule.
  - `TestFuturesMarketAnalytics_InternalBreakTruncatesAndResumesGrid_MKT15` — real temporal delivery to the 12:03 break boundary; break-start AtUTC asserted at the configured boundary; grid truncation/resume geometry unchanged; chain re-arms prospectively (break end 12:07 → session close 16:00); bounded delayed queue.
  - `TestFuturesMarketAnalytics_BarClosedDeliveryOnNaturalClose_MKT01_MKT14` — extended: the scheduled fire-at equals the boundary and the natural close re-arms gen-2 at the next boundary (fire-at 09:40).
- New vertical proof (`v3/core/internal/futuresvertical/timer_semantics_test.go`): `TestFuturesVertical_TimerFiresAtBoundary_BoundedQuiescence`.
- RED (unit: `cd v3/core && GOTMPDIR=/home/kor/aranea/gotmp go test ./internal/functions/ -run 'TestFuturesMarketAnalytics_TimerClosesWithoutNextTick_MKT14|TestFuturesMarketAnalytics_BarClosedDeliveryOnNaturalClose_MKT01_MKT14|TestFuturesMarketAnalytics_InternalBreakTruncatesAndResumesGrid_MKT15' -count=1`), tail:
  ```
  --- FAIL: TestFuturesMarketAnalytics_BarClosedDeliveryOnNaturalClose_MKT01_MKT14 (0.00s)
      Error: "[]" should have 1 item(s), but has 0            (no scheduled temporal firing: the timer was an immediate send)
  --- FAIL: TestFuturesMarketAnalytics_TimerClosesWithoutNextTick_MKT14 (0.00s)
      Error: "[]" should have 1 item(s), but has 0
  --- FAIL: TestFuturesMarketAnalytics_InternalBreakTruncatesAndResumesGrid_MKT15 (0.01s)
      Messages: 09:30 natural, 09:35 timer-closed at its own boundary — should have 2 item(s), but has 1
  ```
- RED (vertical: `... go test ./internal/futuresvertical/ -run 'TestFuturesVertical_TimerFiresAtBoundary_BoundedQuiescence' -count=1`), tail:
  ```
  --- FAIL: TestFuturesVertical_TimerFiresAtBoundary_BoundedQuiescence (33.17s)
      harness.go:669: bus: owner invocation failed: bus: dispatch budget 100000 exhausted with 2 messages pending (wiring loop)
  (log also shows the premature bar_close trigger at the trade instant 13:30:50Z and "stale bar close timer absorbed generation=1")
  ```
- GREEN: both commands pass; full suites below.
- Files changed: futures_market_analytics.go, futures_market_analytics_test.go, testutil/statefun_mock.go, futuresvertical/bus.go, futuresvertical/harness.go, futuresvertical/timer_semantics_test.go (new).
- Commit: 7f565b2f `fix(futures): F-A-01 bar/session timers are temporal SendAfter firings, not immediate sends`.

---

## F-A-02 (MAJOR) — stale timer absorb OVERWROTE the live timer state

- Finding: `handleBarCloseTimer`'s stale branch executed `s.barTimers[tf] = BarTimerState{}` — an in-flight stale gen-1 firing zeroed the live gen-2 entry, so the live gen-2 firing was absorbed in turn: the bar stayed forming forever.
- Authority: D2-06C §7 — a stale (timer_id, generation) firing is a deterministic NO-OP that never executes domain and never mutates the live schedule.
- Test: `TestFuturesMarketAnalytics_StaleTimerFiringNoopPreservesLiveTimer` — drives the real race with event time decoupled from runtime order (§5): trade 09:30:50 arms gen-1@09:35; the 09:35:05 event is admitted at runtime 09:34:59.900 (natural close replaces the schedule with gen-2@09:40); the stale gen-1 firing arrives at 09:35:00 and must close nothing; the live gen-2 firing must still close the 09:35 bucket at 09:40 exactly once.
- RED (`... go test ./internal/functions/ -run 'TestFuturesMarketAnalytics_StaleTimerFiringNoopPreservesLiveTimer' -count=1`), tail:
  ```
  --- FAIL: TestFuturesMarketAnalytics_StaleTimerFiringNoopPreservesLiveTimer (0.01s)
      Error: "[{...09:30 bucket record...}]" should have 2 item(s), but has 1   (gen-2 absorbed after the overwrite: bar forming forever)
  ```
- Fix: one line — the stale branch no longer writes `s.barTimers` (pure NO-OP; store+telemetry kept).
- GREEN: same command passes; full suites below.
- Files changed: futures_market_analytics.go, futures_market_analytics_test.go.
- Commit: 5ff76ac3 `fix(futures): F-A-02 stale bar-timer firing is a pure NO-OP, never clears the live entry`.

---

## F-A-03 (MAJOR) — calendar version regression permanently killed the session chain

- Finding: `handleCalendarDataset` bumped the generation on a version regression, then unconditionally reset `s.sessionTmr` to `{Generation: N}` with zero AtUTC/Transition and never re-sent: the in-flight old-generation firing was absorbed by the guard with NOTHING armed — no future session transition could ever fire (D2-06C §12 prospective re-arm violated). A legitimate version advance wiped AtUTC too (the old firing then executed the old boundary under the new book).
- Authority: D2-06C §12 — the linearized authority owns the schedule; a hot calendar correction re-agendas prospectively and the transition armed under the old version is cancelled/replaced by timer_id; the chain never dies.
- Test: `TestFuturesMarketAnalytics_CalendarUpsertRearmsSessionChain` — trade arms gen-1@12:03; v2 upsert re-arms gen-2; the v1-over-v2 REGRESSION re-arms gen-3; at 12:03 exactly ONE break-start transition fires (stale in-flight firings absorb) and the chain continues at the break end (12:07).
- RED (`... go test ./internal/functions/ -run 'TestFuturesMarketAnalytics_CalendarUpsertRearmsSessionChain' -count=1`), tail:
  ```
  --- FAIL: TestFuturesMarketAnalytics_CalendarUpsertRearmsSessionChain (0.00s)
      Error: "[{{NQ:NQZ6 1 2026-02-18 17:03:00 +0000 UTC BREAK_START} ...}]" should have 2 item(s), but has 1
      Messages: the upsert re-armed the transition under a new generation   (17:03Z = 12:03 ET; only the in-flight gen-1 existed)
  ```
- Fix (`futures_market_analytics.go`): `handleCalendarDataset` re-arms via `rearmSessionTimer` (next transition of the linearized book under Generation+1, `SendAfter` to its AtUTC) whenever the island consumes transitions (chain armed or builders exist); the resolver is rebuilt over the new book inside the same invocation (`analyticsState.rebuildResolver`, shared with `load`) — without the rebuild the re-arm resolved against the pre-upsert book and failed `CALENDAR_UNRESOLVED` (caught immediately by the existing `TestFuturesMarketAnalytics_CalendarBookBounded`, fixed in the same commit).
- Determinism note: `authorityCalendarID` (deterministic pick, calendar_id order) is used by the re-arm so the new code path never decides by Go map iteration; the two pre-existing call sites were switched in F-A-04.
- GREEN: same command passes; full suites below.
- Files changed: futures_market_analytics.go, futures_market_analytics_test.go.
- Commit: 790f20c1 `fix(futures): F-A-03 calendar upsert re-arms the session chain prospectively`.

---

## F-A-04 (MAJOR) — calendar authority chosen by Go map iteration

- Finding: `ensureGrids` (~:403-407) and `handleSessionTimer` (~:729-733) picked the linearized dataset with `for id := range s.book.Datasets { calendarID = id; break }` — the same input anchored different grids/armed different transitions across runs (register: 56/4 distinct grids over 60 trials), violating same-input/same-output (D2-06C §3).
- Authority: D2-06C §3 (determinism invariant), §12 (the dataset linearized in the island schedules; V1 = one instrument = one calendar authority).
- Test: `TestFuturesMarketAnalytics_CalendarAuthorityDeterministic` — two calendars with different session geometry (EQ_DAILY 09:30-16:00 with a 12:03 break vs ZZ_OPEN20H 05:00-21:00) linearized in alternating order over 24 fresh owner instances; the armed session transition must be identical in every run and be EQ_DAILY's (smallest calendar_id = authority).
- RED (`... go test ./internal/functions/ -run 'TestFuturesMarketAnalytics_CalendarAuthorityDeterministic' -count=1`), tail:
  ```
  --- FAIL: TestFuturesMarketAnalytics_CalendarAuthorityDeterministic (0.01s)
      Error: Should be true
      Messages: trial 1 armed a different transition (2026-02-19 02:00:00 +0000 UTC != 2026-02-18 17:03:00 +0000 UTC): the authority pick is not deterministic
  ```
- Fix: both call sites resolve through `authorityCalendarID` (lexicographic calendar_id order of the bound book; caller guarantees non-empty).
- GREEN: `go test ./internal/functions/ -run 'TestFuturesMarketAnalytics' -count=3` ok (repeated for iteration-order stability).
- Files changed: futures_market_analytics.go, futures_market_analytics_test.go.
- Commit: 61176060 `fix(futures): F-A-04 calendar authority picked deterministically, not by map iteration`.

---

## Blocker acceptance — the six bullets and their proofs

1. **Trade before boundary → forming bar remains forming**: `TestFuturesMarketAnalytics_TimerClosesWithoutNextTick_MKT14` (Empty(BAR_CLOSED) after the 09:30:50 trade and after DeliverDue at 09:34:59) and `TestFuturesVertical_TimerFiresAtBoundary_BoundedQuiescence` (Empty(SentOf(BAR_CLOSED)) after the plain-drain trade).
2. **Timer at boundary → BAR_CLOSED exactly once**: MKT14 unit (exactly 1 closure at fire-at 09:35, CloseBoundary/TradeCount asserted) and the vertical test (Len == 1 at 09:35 with bar geometry).
3. **Stale replaced timer → NO-OP, live timer still fires**: `TestFuturesMarketAnalytics_StaleTimerFiringNoopPreservesLiveTimer`.
4. **Session transition fires at configured boundary**: `TestFuturesMarketAnalytics_CalendarUpsertRearmsSessionChain` (exactly one BreakStart with AtUTC == 12:03); `TestFuturesMarketAnalytics_InternalBreakTruncatesAndResumesGrid_MKT15` (BreakStart AtUTC == 12:03, break-end chain re-arm at 12:07); vertical test (exactly one SessionEnd with AtUTC == 17:00).
5. **No immediate recursive chain / no livelock**: vertical test — one trade through the plain FIFO drain quiesces with `len(Sent()) < 50` (RED pre-fix: dispatch budget 100000 exhausted in a 33s cascade), every pending firing future-dated; MKT15 bounds the delayed queue (≤ 4) with future-dated session schedule.
6. **Masked tests rewritten, real delayed delivery**: MKT14/MKT15/natural-close now drive `MockContext.SetClock` + `DeliverDue` (temporal delivery through the real `fn.Invoke`); MockContext honors delay via a controllable clock; the bus honors `FireAt` gated on the vertical's `domain.VirtualClock` (`Compose`-injected), replacing the payload-decode masking (kept only as fallback).

## Full suite results (exact commands, end state)

- `cd v3/core && GOTMPDIR=/home/kor/aranea/gotmp go test ./internal/... -count=1` → ok (internal, internal/automation, internal/functions, internal/futuresruntime, internal/futuresvertical).
- `cd v3/sdk && GOTMPDIR=/home/kor/aranea/gotmp go test ./futures/... -count=1` → ok (bars, calendar, domain, gerardmm, market, marketctx, obs, operation, provider, strategies/s1, strategies/s2, strategy, units).
- S12 (unmodified files, mandatory run): `go test ./internal/futuresvertical/ -run 'TestS12' -count=1` → ok; explicitly `TestS12_Backtest_DoubleRun_Deterministic`, `TestS12_REC04_RunProvenanceIsolation`, `TestS12_S1_ExactReplay_Golden_Breakout`, `TestS12_S2_ExactReplay_Golden_Pullback` all PASS — BACKTEST same-input run-twice is byte-identical.
- Build: `go build ./...` in v3/core and v3/sdk → OK.

## Golden changes

NONE. The vertical's `DrainTimed` due-ness is unchanged by construction (`FireAt = clockNow + clamp(boundary − clockNow) = max(clockNow, boundary)`, so `due ⇔ boundary ≤ clock-now` exactly as the old payload decode) — bar-close timing in the vertical is identical, and no golden encoded a premature close on any exercised path (the premature-close/livelock defect only manifested on the plain-`Drain` path, which no golden covered; it is now pinned by `TestFuturesVertical_TimerFiresAtBoundary_BoundedQuiescence`). No golden re-pins were necessary; S12 determinism holds.

## Escalations / out-of-scope observations (no closure faked)

1. **BreakEnd transition is never delivered to subscribers** (pre-existing, all findings' flows): the resolver resolves the break-end boundary instant (12:07) as OPEN (the boundary belongs to the open side), so `handleSessionTimer`'s `res.State == Break && f.Transition == TransitionBreakEnd` case never matches; the BreakEnd firing is consumed, the grid correctly resumes (R5 — BreakEnd requires no grid action) and the chain re-arms, but strategies never receive a BreakEnd `SessionTransitionDelivery`. The old masked flow never delivered BreakEnd either (it only fired timers with AtUTC ≤ 12:03), so this is not a regression of this lane; MKT-15's grid assertions hold. Flagged for a future decision (either arm break-end at `End − ε` resolution or match the case on `f.Transition`); NOT fixed here because no accepted finding covers it and the fix changes delivery semantics beyond this lane's mandate.
2. `v3/sdk/futures/market/wire.go` was NOT modified — no wire field was needed: the fire instant is runtime-level (bus `PendingMessage.FireAt` / MockContext delayed queue), derived from the existing `Boundary`/`AtUTC` payload fields.
