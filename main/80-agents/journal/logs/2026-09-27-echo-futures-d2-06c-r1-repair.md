---
type: change_log
schema_version: 1
scope: session
created: "2026-09-27"
updated: "2026-09-27"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
  - "[[Echo Futures — D2-06C Live Replay Market Boundary]]"
related:
  - "[[Echo Futures — D2-06A Market Feed Authority]]"
  - "[[Echo Futures — D2-06B Bars Hot State Warmup]]"
  - "[[Echo Futures — D2-05 Instrument Session Provider]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/echo
  - echo-futures
---

# 2026-09-27-echo-futures-d2-06c-r1-repair

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Futures/Echo Futures — D2-06C Live Replay Market Boundary.md` (repair R1 in place: sección "Manager Repair — D2-06C-R1", callout, §1/§2/§3/§4/§5/§6/§7/§15/§16/§18/§19/§20/§21/§22/§23/§25/§26/§27/§28/§29/§30(A–T)/§31, handoff).
  - `80-agents/memory/internal/agent-memory/2026-09-27-echo-futures-d2-06c-continuity.md` (continuidad actualizada in place con el delta R1), este change_log, feedback note del repair.

## Motivo

- Ejecución del mandato one-shot D2-06C-R1 (TOP repair bajo SUBMANAGER D2-06): el SUBMANAGER aceptó la dirección general de C y devolvió tres defectos más la regla de journal. **R1** — EXACT_REPLAY no tenía estado inicial (el warm-up B §17 del run live no estaba en el recording): elegido **OPTION A (immutable warm-up corpus)** — el recording conserva el corpus EXACTO de MarketEvents normalizados + snapshots calendario/config consumidos por el warm-up, con refs+digest en el RunManifest; el replay re-ejecuta ese corpus con la MISMA lógica B y verifica digest+readiness antes de `owner_input_seq=0` (sin segunda serialización de estado derivado, sin re-consultar `MarketHistorySource`); sin anchor ⇒ `REPLAY_ANCHOR_MISSING` fail-visible. **R2** — `DomainClock.Now()` ya no deriva de `event_ts` (retrocedía ante timer 09:31 + evento atrasado 09:30:59.900): separados event time (barras/OHLC/session) y **runtime logical time `runtime_ts`** (monotónico por isla, derivado en admisión `max(previo, wall)`, journalado por entrada; REPLAY lo reproduce; BACKTEST lo sintetiza no-decreciente). **R3** — journalado completo de TODO TimerFired admitido (sin change-detection para timers, porque un firing puede ser prerequisito de control flow futuro), identidad `timer_id`+`generation` (re-Schedule = replace; firing stale absorbido determinísticamente; replay valida contra el timer set virtual). **Journal rule** reescrita con criterio de materialidad "¿puede afectar una observación de dominio presente o futura?" (ALWAYS/MAY OMIT explícitos). **OD-C1** se mantiene owner con costo actualizado (anchor = captura única acotada por MarketRequirements, misma retención; opt-in = compromiso al iniciar el run; `OWNER DECISIONS REQUIRED = 1`).
- Baseline `xKoRx/echo origin/master = 372af59a` re-verificada en ventana (fetch sin delta ⇒ sin re-auditoría física, como mandaba el /bootstrap). Estado final: `D2-06C-R1 = READY_FOR_SUBMANAGER_REVIEW` (BLOCKED_OWNER_DECISION: OD-C1 abierta, no bloquea review); no cierra D2-06, no integra A+B+C, no avanza D2-07, no implementa código, no reabre A/B/D2-04/D2-05.

## Notas de cierre

- Sin L0/L1 (sin transcript persistible ni pedido); feedback note exigida por el mandato (lección transferible de design review: contrato de replay debe congelar el estado inicial y el criterio de journal debe ser de observabilidad, no de mutación inmediata).
- Sin `agent_run` (no hubo generación/evaluación de código).
- Validación Graphify omitida: markdown canónico persistido; el índice es derivado.
- El vault tiene auto-sync (~1 min): los archivos de cierre viajan en el sync siguiente.
