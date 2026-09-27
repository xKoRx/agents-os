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

- D2-06A TOP worker A entregó [[Echo Futures — D2-06A Market Feed Authority]] como `READY_FOR_SUBMANAGER_REVIEW` (2026-09-27). NO está closed; sigue el gate del SUBMANAGER D2-06 y luego el artefacto integrado A+B+C antes de Primary Manager review. Ningún gate fue self-accepted.
- Diseño central congelado como candidato: **binding MARKET_DATA = autoridad lógica**; stream = `(binding_id, contract_id)`; feeds equivalentes = members dentro del binding (arbitraje first-wins por venue seq); fuentes heterogéneas = bindings distintos, switch explícito con readiness loss/rebuild, nunca blend.
- MarketEvent mínimo = QUOTE(BBO)+TRADE; identidades separadas transport / semantic (venue seq o content tuple) / `stream_seq` contiguo post-arbitraje (idempotencia downstream obligatoria); `authority_epoch` + `origin{source_id, feed_kind}`; `receive_ts` jamás semántica de dominio.
- Subscription = demand sets idempotentes (config catalog ∪ `MarketDemand` ACQUIRE/RELEASE transaccional desde `echo/operation`, idempotente por operation_id); RETIRING mantiene vivo el contract pinneado de una Operation tras rollover; UNSUBSCRIBE sólo con demand vacío. Sin reference counting framework.
- Health = 3 dimensiones (liveness por member con heartbeats/inactividad sólo bajo sesión OPEN; continuity sólo por primitivas del source — timestamp jump NO es evidencia; freshness config por source/instrument). Calendar CLOSED ⇒ silencio esperado, jamás failure; timeout universal prohibido (B2 manager).
- Recovery = máquina conceptual única, ejecución capability-specific (replay/snapshot/natural-refresh → dedup overlap → RecoveryBarrier → rebuild downstream = contrato D2-06B → READY con epoch nueva). Fuera de replay bounds ⇒ NOT_READY fail-closed, sin síntesis.
- Física propuesta: StateFun `echo/market_stream` key `stream_id`; adapters → `echo.market-feed-candidates.v1`; canónico `echo.market-events.v1` (AT_LEAST_ONCE + stream_seq; transporte Y recorded stream) + control compactado `echo.market-stream-state.v1`; egress canónico deliberadamente NO exact-once (latencia ticks vs checkpoint) — diferencia declarada vs D2-04.
- Owner decisions: NONE. Riesgo material declarado: throughput StateFun por tick sin benchmark ⇒ D6 obligatorio, fallback in-process declarado como deuda condicional.
- Echo baseline re-verificada por el worker: `origin/master == 372af59a7b83604781346613da01e3d510ea1360` (sin delta).

## Señales de carga

- Cargar con [[Echo Futures]] cuando aparezca D2-06, Market Runtime, feed authority, MarketEvent, readiness/recovery o cuando un agente dude del estado del carril A.
- Prioridad de autoridad: [[Echo Futures]] manager gates > artefacto integrado D2-06 futuro > D2-06A candidate > esta continuidad.
- B no debe rediseñar identidad de streams ni health dimensions; C no debe rediseñar el envelope ni `stream_seq`; ambos consumen D2-06A como input.

## Próxima acción

- SUBMANAGER D2-06: revisar D2-06A; despachar/integrar B (bars/MTF/indicators/warm-up) y C (clock/ordering/LIVE-REPLAY boundary); producir artefacto integrado D2-06 antes de Primary Manager review. No cerrar D2-06 global, no avanzar D2-07.
