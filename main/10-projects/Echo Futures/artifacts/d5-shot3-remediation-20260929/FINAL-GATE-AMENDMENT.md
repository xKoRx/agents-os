# Echo Futures — D5 Macro Shot 3 · FINAL MANAGER GATE AMENDMENT (handoff)

**Fecha:** 2026-09-30 · **Branch:** `feature/d5-shot3-remediation` · **prior = `5f9fadde` → final HEAD = `e607b4183e041f8c7603d9b5d0db82c6f09d29a7`** (+3 commits, sin squash/rebase/force-push, historial intacto).

---

## Executive

```text
FINAL_GATE_AMENDMENT = COMPLETE
final SHA  = e607b4183e041f8c7603d9b5d0db82c6f09d29a7
MKT-07     = PASS   (dedicated deterministic test; no product change required)
TERM-03    = PASS   (exact SimExecution E2E; one test-harness seam fix, no product change)
F-MGR-02   = CLOSED (minimum product fix + mandatory reproducer, red-first verified)
F-MGR-03   = CLOSED (minimum runtime seam + full required test matrix)
ATP totals = 113 PASS / 0 FAIL / 0 INCOMPLETE / 2 DEFERRED_TO_D6 (EXE-14, SCL-03) over 115 cases
S12 status = 13/13 PASS
```

No se emite `EF_D5_FOUNDATION_PASS` ni `D5 CLOSED`: vuelve al Primary Manager para el gate.

## Four-item closure matrix

### MKT-07 — Contract rollover ≠ source switch

```text
authority  = ATP MKT-07 (Gate D5): rollover differs from source switch
reproducer = TestFuturesVertical_MKT07_ContractRolloverDiffersFromSourceSwitch (futuresvertical, green)
minimal fix= NONE (product): reuses the frozen pinning seams (Views.ResolveContract at
             materialization → ContractSnapshot + PinnedBinding; commands carry the pinned
             identity). No rollover service, no automatic Operation migration, no new owner.
tests      = 1 vertical E2E: (a) O live pinned NQZ6; (b) SOURCE SWITCH on the same contract →
             O stays live, pinned, TRADING (fresh quote → bounded add with A identity);
             (c) mapping roll NQ→NQH7 → O stays pinned A and closes on A; (d) new demand
             materializes on B (snapshot, pinned external ref sim:NQH7, M1 commands B).
result     = MKT-07 = PASS (backed by an executed test on the final tree)
```

Nota de diseño del test: la demanda nueva se entrega como cycle k+1 tras el cierre de O; entregada ANTES (deferred) el guard de orden SPEC §25 del owner absorbe el CLOSE cycle-1 posterior como stale — artefacto del orden sintético del test, no defecto (el orden de ciclos del strategy es monótono en producción).

### TERM-03 — ForceClose while bridge down

```text
authority  = ATP TERM-03 (Gate D5 integration; D5-S10 requires SimExecution)
reproducer = TestFuturesVertical_TERM03_ForceCloseWhileBridgeDown (futuresvertical, green)
minimal fix= NONE (product). ONE test-harness seam fix (bridge.go, test infrastructure): the
             events→Core finality surface no longer fabricates TERMINAL_EXECUTION_FINAL for an
             order the venue never saw — a submit the edge refused keeps its local claim until
             its command is actually delivered. (The fabricated finality released the claim and
             looped the §19 safety replan against the dead edge; the product replan itself is
             correct per §19.)
tests      = exact E2E: active Operation + exposure 5 + edge NOT READY (SimulateDisconnect) +
             ForceClose → intent persists (SAFETY_PLANE, never instant terminality), exposure
             unchanged (no synthetic success), FillCount unchanged (no fabricated Fill), venue
             order count unchanged (no blind submit), in-flight command refused fail-visibly,
             readiness NOT-READY visible. Reconnect → recovery barrier FIRST (frozen 11 steps:
             connect..reevaluate_readiness), journaled cancel reconciled against the physical
             venue state, readiness restored; at-least-once M1 topic replay → closure continues
             → TERMINAL(SAFETY_FLATTEN), exposure 0, exactly one exit fill.
result     = TERM-03 = PASS (exact E2E evidence)
```

### F-MGR-02 — profit-exit continuation after claim-releasing finality

```text
authority  = Primary Manager BLOCKER; D4-B2 §18/§19; GMM-I15/GMM-I16 frozen meanings preserved
reproducer = mandatory reproducer implemented and verified RED on the pre-fix tree (git stash
             of the fix → suite FAILS) and GREEN after:
             TestFMGR02_ProtectiveFinalityContinuesProfitExit_LONG (+_SHORT),
             TestFuturesVertical_ProfitExitContinuesAfterProtectiveFinality (E2E).
minimal fix= (1) gerardmm.afterFact: under an MM-requested termination intent an authoritative
             Fill/OrderFinal now runs exitMaintenance — re-cancel any live protective + exact
             MARKET EXIT of AvailableReducibleQty (the unclaimed reducible exposure right now).
             Safety-plane intents stay silent (the owner's safety path owns closure, §20).
             (2) operation engine: the venue TERMINAL_EXECUTION_FINAL branch now invokes MM
             (the released claim is an authoritative change of the situation, §19); a duplicate
             finality is absorbed before any evaluation (fires exactly once per released claim).
tests      = sdk: LONG/SHORT continuation, cancel-ack claim retention (no blind exit, §18.3),
             late-Fill race (no double-close, GMM-I16), stale-economics exit availability
             (MM-18), safety-intent silence, live-protective re-cancel; engine duplicate-finality
             absorption; vertical E2E of the mandatory reproducer (parked finality → claimed
             stage observable → release → exact exit 5 → terminal). No polling, no dependence on
             a later economics update. The accepted MMTriggerAccountEconomics surface is
             unchanged (its vertical test now asserts the amended completion).
result     = F-MGR-02 = CLOSED
```

### F-MGR-03 — GerardMM QUOTE trigger runtime-reachable

```text
authority  = Primary Manager BLOCKER; frozen D4-B2 §17 trigger surface (market_event = QUOTE,
             bar_close = NONE, timers = NONE); ACCOUNT_ECONOMICS remains accepted, separate cause
reproducer = full required matrix (all green):
             adverse: TestQuoteTrigger_AdverseThresholdExactlyOneBoundedAdd + vertical E2E
                      (fresh quote mid 21705 crosses the configured threshold → exactly one
                      bounded ADD through candidate→market_stream→analytics→owner→MM→M1→bridge)
             favorable: TestQuoteTrigger_FavorableThresholdExactlyOneBoundedPyramid + vertical
                      E2E (mid 21740 → one bounded pyramid, qty on the lattice)
             stale/not-ready: TestQuoteNotif03_StaleAndFutureEvidenceAbsorbed,
                      TestQuoteTrigger_NotReadyOrMissingMarkFailsClosed (stale evidence absorbed
                      by the owner BEFORE any evaluation; not-ready market fails closed)
             mutual exclusion: TestQuoteTrigger_MutualExclusion_NoBranchFlip (+ vertical: adverse
                      branch locked → favorable quote → no pyramid)
             dedup: TestQuoteNotif02_RedeliveryAbsorbedOneKeyedDelivery + vertical canonical
                      redelivery + keyed notification redelivery (no second MM decision/order)
minimal fix= minimum additive D5 runtime seam, frozen surfaces preserved:
             - operation: MMTriggerQuote kind + QuoteID identity; QuoteNotification input (one
               keyed delivery per rung, bounded dedup, stale/future absorb fail-visible, foreign
               contract absorbed); ONE evaluation's MarketContext scoped to the accepted BBO mid
               (exact, direction-symmetric, no spread model; other reads delegate).
             - market_analytics: the single shared producer — accepted canonical QUOTE fans out
               to a config-declared bounded route set (QuoteRoutesUpdate, echo/operation owner
               keys, cap 256, deterministic order, same per-target canonical dedup as TRADE
               forwards); non-parsing payload dropped fail-visibly. No per-account analytics.
             - gerardmm: onQuote per §17 precedence — termination intent first (a pending exit
               NEVER polls per quote, §19), profit objective, protective reconciliation (dynamic
               tightening between facts), bounded adds; decision identities carry the quote id.
             - units: exact PriceFromRat (typed miss for non-decimal rationals).
preserved  = shared market ownership, no per-account bar/indicator computation, serialized
             Operation ownership, decision-scoped MarketContext, stale-quote fail-closed,
             bounded fan-out. Real external market-feed certification remains D6.
result     = F-MGR-03 = CLOSED
```

## GerardMM reachability matrix

| Trigger | Runtime producer/seam | MM behavior reachable | Dedup identity |
|---|---|---|---|
| SignalDelivery | strategy engine → signal_fanout → op owner (frozen path) | entry (MATERIALIZED), management CLOSE/CLOSE_ALL/same-cycle OPEN | delivery dedup (account_strategy:signal_id) + order guard (cycle/eval/signal) |
| Fill | bridge → events→Core gate → raw execution-events ingress (path 1) | afterFact: profit exit / protection / adds / exit maintenance (F-MGR-02) | FillDedup (provider execution identity) |
| OrderFinal | order/action observations + TERMINAL_EXECUTION_FINAL at the gate | afterFact bookkeeping + exit maintenance on released claims (F-MGR-02) | q_exec_max-zero absorption (duplicate finality never reaches MM) + venue evidence |
| AccountEconomics | AccountEconomicsUpdate keyed delivery (account-state plane; D6 physical sender) | onAccountEconomics: profit exit re-completion (accepted F-E-01, unchanged) | EconomicsDedup (UpdateID) |
| QUOTE | market_stream (ladder + canonical) → market_analytics (guard) → declared-route fan-out → op owner; decision-scoped MarketContext serves the accepted BBO mid (F-MGR-03) | onQuote: §17 precedence — termination NO_ACTION, profit objective, protective reconciliation, bounded adds | owner QuoteDedup (canonical rung id) + stale gate (regressed event_ts) + analytics per-route canonical forward dedup |
| ForceClose/Safety | provider plane (ForcedFlatCutoff sweep) → ForceCloseIntent → op owner | MM NO_ACTION under safety intent (the owner's safety replan owns closure); ForceClose intent cuts new risk | ForceCloseDedup (ForceCloseID) |

## ATP totals

```text
PASS           = 113
FAIL           = 0
INCOMPLETE     = 0
DEFERRED_TO_D6 = 2 full rows (EXE-14, SCL-03) — D6 gates per the frozen ATP
                 + D6 halves on REC-03, EXE-01/02/04/08, MKT-11/13, Budgets §20
```

Matrix regenerada en `atp-final-matrix.md` (mismo artefacto, filas MKT-07/TERM-03/MM-10/MM-12/MM-13/MKT-16 actualizadas con la marca **amended**).

## Regression (§9) — ejecutada sobre el árbol final `e607b418`

```text
cd v3/core    && go test -count=1 ./internal/functions/ ./internal/futuresvertical/ ./internal/futuresruntime/   → ok (3 pkgs; vertical incluye S12)
cd v3/sdk     && go test -count=1 ./futures/...                                                                  → ok (13 pkgs, 0 FAIL)
cd v3/futures-bridge     && go test -count=1 ./...                                                               → ok (10 pkgs, session incl.)
cd v3/futures-projector  && go test -count=1 ./...                                                              → ok (3 pkgs)
S12: go test -count=1 -v -run 'TestS12' ./internal/futuresvertical/  → 13/13 PASS (BACKTEST×2 byte-idéntico incl.)
Blocker reproducers (todos PASS): F-A-01 TimerFiresAtBoundary_BoundedQuiescence · F-C-01 EXP04/FC01 ·
F-D-01 Reservation scopes (gross/netabs/groupweighted) · F-E-01 EconomicsUpdate* · F-MGR-01 S12_LiveDecision_*
Shot-2 adversarial targeted: 23 verticales + 38 sdk (EXP01-08, FC01-08, TERM02/04/05, MM-12/15/17,
economics triggers, FMGR02, QuoteTrigger) → 0 FAIL
```

## Git

```text
prior      = 5f9fadde190c3cd85637f746fd45bb703736a7f4
final HEAD = e607b4183e041f8c7603d9b5d0db82c6f09d29a7
origin     = refs/heads/feature/d5-shot3-remediation @ e607b418 (pushed, fast-forward)
dirty      = clean (git status: 0 entradas)
commits    = e0cb7b53 (F-MGR-02) · eb8edbfb (F-MGR-03) · e607b418 (MKT-07 + TERM-03)
```

## FINAL SURGICAL FIX — F-MGR-04 (2026-09-30, Manager BLOCKER)

La observación 1 de abajo fue clasificada **F-MGR-04 = BLOCKER** por el Primary Manager y **CLOSED** @ `13e087a3bb762f65b060d3b3200fb00a67c6ff1d` (prior `e607b418`, +1 commit enfocado, pusheado, tree clean).

- **Fix**: `onManagementSignal` CLOSE/CLOSE_ALL cancela todo ENTRY/ADD con `q_exec_max > 0` vía el path existente de OrderAction (patrón D4-A2 §5.4 extendido al close técnico; AC-Q13-18). Claims retenidos hasta finality venue (F-C-01); exit sólo por el reducible NO reclamado (sin close competidor inseguro); roles reductores (EXIT/REDUCE) jamás cancelados; la continuación corre por los lifecycle facts con el `exitMaintenance` de F-MGR-02 (sin timers, polling, ni coordinación nueva).
- **Evidencia**: reproducer vertical ROJO→VERDE (`TestFuturesVertical_F_MGR04_CloseAllNeutralizesLiveAdd`: QUOTE→ADD WORKING→CLOSE_ALL→cancel→claims→finality→exit exacto→TERMINAL); suite sdk gerardmm 7 tests (LONG/SHORT, CLOSE y CLOSE_ALL, exit sólo unclaimed, roles reductores intactos, idempotencia, ENTRY ejecutable neutralizado — el estado PENDING_ENTRY+CLOSE es estructuralmente posible en el lifecycle frozen); engine race matrix (Case A cancel-finality, Case B late full fill → verdad + continuación acotada por claims 5+5, Case C partial fill → claim remanente retenido + exit no-reclamado, Case E finalidad duplicada idempotente).
- **Regresión (§17, sobre `13e087a3`)**: sdk futures 13/13 ok · core functions/futuresvertical/futuresruntime ok · futures-bridge 7/7 ok · futures-projector 3/3 ok · S12 13/13 · reproducers F-C-01 / F-E-01 / F-MGR-02 / F-MGR-03 / TERM-03 / MKT-07 → 23/23 PASS, 0 FAIL.
- **ATP se mantiene**: 113 PASS / 0 FAIL / 0 INCOMPLETE / 2 DEFERRED_TO_D6 (F-MGR-04 = evidencia adicional del gate Manager, sin fila nueva).

## Observaciones históricas (del amendment anterior)

1. ~~CLOSE (estrategia) con ADD order vivo~~ → **CERRADO por F-MGR-04** (ver arriba).
2. La finalidad no-forzada del harness ahora exige registro del venue — el comportamiento del producto (replan §19 por finalidad) quedó validado como correcto; el artefacto era evidencia fabricada del seam de test.
```
