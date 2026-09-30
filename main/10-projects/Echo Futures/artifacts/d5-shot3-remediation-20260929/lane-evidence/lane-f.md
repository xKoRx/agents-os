# Lane F — futures-bridge remediation evidence (D5 Shot 3)

Worktree: `/home/kor/aranea/work/d5-shot3-20260929/wt-f-bridge`, branch `shot3/lane-f-bridge`.
Module: `v3/futures-bridge`. All work constrained to `v3/futures-bridge/**`.
Central invariant preserved in every fix: **zero blind duplicate physical submit**
(M2 journal durability before side effect; unknown delivery never converted to
retry; AMBIGUOUS whenever absence cannot be proven).

Commits (in order):

- `8843b3dc` fix(futures-bridge): F-F-01 enforce EXE-05 NEW_RISK gate at the side-effect boundary
- `f55226b7` fix(futures-bridge): F-F-02 commit Kafka offsets only after M2 journal durability
- `ece903ab` fix(futures-bridge): F-F-03 recover pre-transport crash from durable journal without livelock
- `79b3d200` fix(futures-bridge): F-F-04 ListOpenOrders port + unknown live order quarantined fail-visible

Final suite (fresh, `-count=1`): `cd v3/futures-bridge && GOTMPDIR=/home/kor/aranea/gotmp go test ./...`
→ all 8 test packages `ok`, 55 tests `--- PASS`, 0 `--- FAIL`; `go vet ./...` clean.
All v3 modules of the go.work build (`go build ./...` per module dir); the v1/v2
build failures observed in the worktree are pre-existing files untouched by this
lane (v2/gateway/internal/close_handler.go, v1/sdk pb packages).

---

## F-F-01 (MAJOR) — NEW_RISK gate decorative at the side-effect boundary

- **Finding:** `handleSubmit` (internal/session/session.go) only checked
  Connected+Authenticated before the physical transmit; a NEW submit with a
  fresh identity was physically transmitted while an AMBIGUOUS cell was active.
- **Authority:** D2-07A §15.5 ("unresolved ambiguous submit/cancel/replace:
  account-level NEW_RISK off en V1 KISS"), §15.2 (gate conjunction); EXE-05.
- **Tests:**
  - `TestF1_NewSubmitWhileAmbiguousNotTransmitted` (new, internal/session).
  - Guards: `TestEXE05_AmbiguousSubmitBlocksNewRisk`,
    `TestEXE04_SideEffectThenCrashSuppressesDuplicate` still green.
- **RED:** `cd v3/futures-bridge && GOTMPDIR=/home/kor/aranea/gotmp go test ./internal/session/ -run 'TestF1_NewSubmitWhileAmbiguousNotTransmitted' -v`
  ```
  session_test.go:457: NEW submit during active ambiguity must be refused (fail-visible)
  --- FAIL: TestF1_NewSubmitWhileAmbiguousNotTransmitted
  ```
- **GREEN:** same command →
  ```
  --- PASS: TestF1_NewSubmitWhileAmbiguousNotTransmitted
  --- PASS: TestEXE05_AmbiguousSubmitBlocksNewRisk
  --- PASS: TestEXE04_SideEffectThenCrashSuppressesDuplicate
  ```
- **Files changed:** `internal/session/session.go` (gate in handleSubmit after
  the M2 dedup guard; refreshes ambiguity from the durable journal, refuses
  fail-visible with redelivery request), `internal/session/session_test.go`.
- **Deviations:** none. Journaled recovery unaffected: MAY_HAVE_EXECUTED
  identities still route to suppression before the gate (asserted in TestF1:
  redelivery of the ambiguous identity converges without transmission).

## F-F-02 (MAJOR) — Kafka consumer never commits offsets (at-most-once / loss)

- **Finding:** AutoCommit off but zero Commit calls and
  `Offsets.Initial=OffsetNewest`: offsets were never committed AND a group
  without a stored offset skipped to the tail — handler error or restart
  silently skipped messages. The frozen chain "offset committed + journal
  guard ⇒ DUPLICATE_SUBMIT_SUPPRESSED" was unreachable; the realized risk was
  LOSS.
- **Authority:** D2-07C §13 ("offset commit tras outcome + journal M2 ... el
  commit del side effect es el journal, nunca el offset"), §23-C; D2-07A
  constraint 8.
- **Tests (new file `adapters/kafka/command_consumer_test.go`; no broker —
  ConsumeClaim driven through fake sarama session/claim):**
  - `TestF2_ConsumerConfigNoSkipNoAutoCommit`
  - `TestF2_OffsetCommittedOnlyAfterHandlerOutcome` (per-message ordering
    `[handle:ok, mark, commit]` on a merged event timeline)
  - `TestF2_HandlerErrorLeavesOffsetUncommitted`
  - `TestF2_RedeliveryAfterUncommittedOffsetSuppressesDuplicate` (real
    session + sim adapter + fsync journal through the real ConsumeClaim)
- **RED:** `cd v3/futures-bridge && GOTMPDIR=/home/kor/aranea/gotmp go test ./adapters/kafka/ -run 'TestF2' -v`
  ```
  Offsets.Initial = -1, want OffsetOldest (a group without stored offset must never skip)
  offset never committed: with AutoCommit off the consumer must commit after the handler outcome
  after durable outcome the offset must be marked+committed: marked=[7] commits=0
  ```
- **GREEN:** same command → 4/4 PASS; full suite green.
- **Files changed:** `adapters/kafka/command_consumer.go`
  (`Offsets.Initial=sarama.OffsetOldest`; `sess.MarkMessage` + `sess.Commit()`
  strictly after the handler outcome — the handler returns only after the M2
  journal write is fsynced, so a committed offset always implies the journal
  guard exists; handler error leaves the offset untouched and surfaces the
  error), `adapters/kafka/command_consumer_test.go` (new).
- **Deviations:** Initial changed Newest→Oldest (explicitly required: without a
  stored offset, skipping = loss; replay is safe by the journal guard). Drop
  path unchanged (malformed/foreign commands can never side-effect, so their
  offsets may advance — documented fail-visible drop semantics).

## F-F-03 (MAJOR) — crash BEFORE transport livelocks recovery after restart

- **Finding:** the sim script cursor was `max(adapter-local attempts, venue
  wire crossings)` — both zero after a crash BEFORE the transport, so
  `ErrCrashInjected` (AFTER_SUBMITTING) recurred forever and the recovery
  barrier killed its own controlled resubmit at every start.
- **Authority:** D2-07A §17 (recovery sequence; "no on reconnect → replay
  pending commands"; MARKET accepted + crash before offset: same
  client_order_id query, converge, no second order), §6.1.11; frozen rule
  "re-drive = replay from durable evidence; submit once only after
  authoritative absence is proven".
- **Tests:** `TestF4_PreTransportCrashRecoveryDoesNotLivelock` (new,
  internal/session); guards: nine crash-window tests, EXE-04, EXE-09 and
  `TestCrashPointsLeaveExactJournalState_Table` still green.
- **RED:** `cd v3/futures-bridge && GOTMPDIR=/home/kor/aranea/gotmp go test ./internal/session/ -run 'TestF4_PreTransportCrashRecoveryDoesNotLivelock' -v`
  ```
  session_test.go:518: restart recovery barrier livelocked on the crash point:
    session: recovery barrier failed for acct-1: barrier: controlled resubmit of
    ord-1: sim: crash injected at AFTER_SUBMITTING
  ```
- **GREEN:** same command → PASS; full suite green. Recovery re-drives from
  the DURABLE journal: the barrier completes, the re-drive transmits exactly
  once (only after Reconcile proves authoritative absence), a second restart
  is stable, and the redelivered command hits the M2 guard ⇒
  DUPLICATE_SUBMIT_SUPPRESSED; exactly one physical order.
- **Files changed:** `adapters/sim/sim_adapter.go` (durable step cursor:
  `max(venue wire crossings, journal submit_drive:N markers)`; Submit records
  `submit_drive:N` evidence fsynced BEFORE the first crash point — the journal
  stays the only durability domain), `internal/session/session_test.go`.
- **Deviations:** adds freeform evidence lines (`submit_drive:N`) to journal
  records — the frozen STATE machine (PREPARED/SUBMITTING/VENUE_BOUND/
  TERMINAL/AMBIGUOUS) is untouched; evidence strings are the journal's
  existing extensibility surface. No session.go change needed: the barrier
  livelock died with the adapter cursor defect.

## F-F-04 (MAJOR) — reconciliation 100% journal-driven; open_order_snapshot PROVEN but no port

- **Finding:** no ListOpenOrders port existed despite the PROVEN
  `open_order_snapshot` declaration; a venue order live in the real venue but
  absent from the journal was invisible during reconciliation.
- **Authority:** D2-07A §13.2/§13.4 (open_order_snapshot PROVEN), §17 step 7
  ("listar/reconciliar open Orders Echo y detectar Orders desconocidas"),
  §17.7 ("Si no puede correlacionarse inequívocamente: AMBIGUOUS, fail
  closed"), §18 (unknown activity: mismatch/debt, never fabricated).
- **Tests:**
  - `TestF3_UnknownLiveOrderQuarantinedFailVisible` (new, internal/session:
    venue live order + empty journal ⇒ barrier survives, UNKNOWN_LIVE_ORDER
    mismatch, QuarantinedOrders surface, NEW_RISK off with
    RECONCILIATION_AUTHORITY_UNAVAILABLE, order untouched at venue, zero
    cancel attempts, nothing adopted into the journal, no fabricated
    Order/Fill, NEW submit refused at the boundary while quarantine resolves).
  - `TestF3_ListOpenOrdersDetectsUnknownLiveOrder` (new, adapters/sim: the
    port lists venue live orders; known open orders stay in OpenOrders, only
    uncorrelated ones quarantine).
- **RED:** `cd v3/futures-bridge && GOTMPDIR=/home/kor/aranea/gotmp go test ./adapters/sim/ -run 'TestF3' -v` and `... go test ./internal/session/ -run 'TestF3_UnknownLiveOrderQuarantinedFailVisible' -v`
  ```
  report.UnknownLiveOrders undefined (type capabilities.ReconciliationReport has no field or method UnknownLiveOrders)
  st.QuarantinedOrders undefined (type Status has no field or method QuarantinedOrders)
  ```
  (build failure = the missing port/surface IS the defect)
- **GREEN:** both commands → PASS; full suite green (55/55).
- **Files changed:** `core/capabilities/adapter.go` (ListOpenOrders on the
  ExecutionAdapter contract; ReconciliationReport.UnknownLiveOrders),
  `adapters/sim/venue.go` (`Venue.OpenOrders`, deterministic order),
  `adapters/sim/sim_adapter.go` (ListOpenOrders impl; detection+quarantine in
  Reconcile: mismatch + Authoritative=false), `internal/session/session.go`
  (quarantine map recomputed per barrier, Status.QuarantinedOrders, NEW-RISK
  boundary gate also holds while quarantine is unresolved),
  `internal/session/session_test.go`, `adapters/sim/sim_adapter_test.go`.
- **Deviations:** quarantine is an in-process surface + report field, not a
  journal record — the frozen journal state machine has no quarantine state
  and the journal API cannot express an uncorrelated identity; fail-visibility
  is durable-by-venue instead (the surviving venue order is re-detected at
  every barrier, so the debt cannot be forgotten). Disposition follows §17.7
  exactly: fail closed, never cancelled, never adopted, no Echo truth
  fabricated.
