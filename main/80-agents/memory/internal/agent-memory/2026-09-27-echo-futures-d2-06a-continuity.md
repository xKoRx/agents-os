---
type: agent_memory
schema_version: 1
scope: project
created: "2026-09-27"
updated: "2026-09-27"
area: "[[Echo]]"
project: "[[Echo Futures]]"
application:
entities:
  - "[[Echo Futures]]"
related:
  - "[[Echo Futures — D2-06A Market Feed Authority]]"
  - "[[Echo Futures — D2-05 Instrument Session Provider]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
aliases: []
confidence: high
memory_state: active
continuity_key: "echo-futures/d2-06a-worker-a"
supersedes:
superseded_by:
load_policy: when_project_loaded
indexable: false
index_priority: high
tags:
  - kind/agent-memory
  - scope/project
  - agent/internal
  - area/echo
---

# Echo Futures — Continuidad D2-06A (worker A)

## Continuidad

- D2-06A TOP worker A entregó el candidato y luego aplicó el **Manager Repair — D2-06A-R1** (2026-09-27) por veredicto `REPAIR_REQUIRED` del SUBMANAGER. Estado: `READY_FOR_SUBMANAGER_REVIEW` **post-repair** en el MISMO artifact [[Echo Futures — D2-06A Market Feed Authority]] (vault sync `2431864b`). NO closed; sigue re-review del SUBMANAGER D2-06 y luego integración A+B+C antes de Primary Manager review. Ningún gate self-accepted.
- **R5 elegido OPTION B (KISS): stream lógica canónica estable por Contract** — `stream_id = (instrument_id, contract_id)`, SIN binding en la identidad; `serving_authority {binding_id MARKET_DATA, members, authority_epoch}` es metadata que cambia por switch explícito. Univoco: STABLE = stream lógica + contract pinneado + stream_seq; SWITCH cambia = autoridad servidora + epoch + provenance + readiness (barrier/rebuild), jamás contract_id; ROLLOVER cambia = selección in-force de Strategy ⇒ otra stream lógica; pinneadas persisten hasta RELEASE.
- **R1 demanda económica:** `MarketDemand{operation_id, instrument_id, contract_id, ACQUIRE|RELEASE}` (sin binding), transaccional desde `echo/operation` (fact path R14 D2-04), idempotente por `(operation_id, contract_id)`. El engine resuelve demanda + autoridad activa → subscription física. Operation pinnea Contract, jamás binding/source; tras switch la misma demanda se re-sirve con la nueva autoridad; source viejo sólo cutover transicional.
- **R2/R3 identidad por clases capability-driven:** A = identity de evento estable (native id o sequence scope EVENT) ⇒ dedup exacto; B = sequence de PACKET + posición in-packet determinística ⇒ identity `(sequence, posición)`, N entries sobreviven; C = sin identidad dedup-safe ⇒ content-dedup PROHIBIDO, recovery sólo overlap-free (cursor no-solapado / snapshot / full rebuild) o `NOT_READY(RECOVERY_UNPROVABLE)`. `stream_seq` se asigna SÓLO tras aceptar la entrada como evento distinto. Evidencia first-party puntual: **CME MDP 3.0 sequence es de packet** (header del segmento UDP; packet con múltiples mensajes SBE y refresh con múltiples entries) ⇒ CME A/B = clase B POSITIONAL, nunca "venue_seq por evento". Members equivalentes exigen misma clase + espacio compartido demostrado; si no, son bindings distintos.
- **R4 switch ≠ rollover:** pure switch preserva contratos (in-force + pinneados), valida servabilidad vía `ContractIdentifier(source, MARKET_DATA, contract)` por cada stream demandada; no servable ⇒ switch RECHAZADO no-op fail-closed (`CONTRACT_NOT_SERVABLE`), jamás re-resolución silenciosa al contract del backup. Rollover = acción owner explícita D2-05, separada/componible, jamás efecto lateral. J case: main NQ=NQZ6 / backup NQ=NQH7 + switch only ⇒ NQZ6 sigue; NQH7 requiere rollover aparte.
- **R6 continuity UNKNOWN:** ≠ GAP_DETECTED y tampoco prueba positiva de continuidad. Steady-state sin primitivas opera bajo capability declarada; tras disruption un BBO fresco certifica sólo current-state. `recovery_state` (QUOTE) y `recovery_history` (TRADE) son capacidades separadas; history-dependent queda gated hasta rebuild demostrable (seam D2-06B).
- **R7 recorded stream:** `echo.market-events.v1` deja de congelarse como recorded replay stream — es transporte canónico LIVE candidato, con retention posible y fuente posible de recording; ordering/contract/retención/replay injection ⇒ D2-06C. Provenance separada: `origin.recovery_provenance = LIVE|RECOVERY_REPLAY|SNAPSHOT` (evento) vs `run_mode` (run, D2-06C) — sin colisión semántica.
- Health 3 dimensiones y calendario como autoridad del silencio se mantienen sin cambios; readiness reasons ahora incluyen `RECOVERY_UNPROVABLE` y `CONTRACT_NOT_SERVABLE`.
- Owner decisions: NONE (post-repair). Riesgos material declarado: throughput StateFun por tick ⇒ D6 obligatorio con fallback in-process; switch puede quedar bloqueado por servabilidad del backup (fail-closed deliberado).
- Echo baseline re-verificada: `origin/master == 372af59a7b83604781346613da01e3d510ea1360` (sin delta).
- Sesión one-shot cerrada con feedback explícito (sin defects operativos nuevos fuera del repair): `80-agents/journal/feedback/system-1/2026-09-27-echo-futures-d2-06a-r1-session-feedback.md`.

## Señales de carga

- Cargar con [[Echo Futures]] cuando aparezca D2-06, Market Runtime, feed authority, MarketEvent, readiness/recovery o cuando un agente dude del estado del carril A.
- Prioridad de autoridad: [[Echo Futures]] manager gates > artefacto integrado D2-06 futuro > D2-06A post-repair > esta continuidad.
- B no debe rediseñar identidad de streams, clases de dedup ni health dimensions; C no debe rediseñar el envelope ni `stream_seq` y SÍ es dueño del recorded stream; ambos consumen D2-06A post-repair como input.

## Próxima acción

- SUBMANAGER D2-06: re-review de D2-06A post-repair; si pasa, despachar/integrar B (bars/MTF/indicators/warm-up) y C (clock/ordering/LIVE-REPLAY + recorded stream); producir artefacto integrado D2-06 antes de Primary Manager review. No cerrar D2-06 global, no avanzar D2-07.
