---
type: agent_memory
schema_version: 1
scope: project
created: "2026-09-28"
updated: "2026-09-28"
area: "[[Echo]]"
project: "[[Echo Futures]]"
entities:
  - "[[Echo Futures]]"
related:
  - "[[Echo Futures — D2-08 Strategy Runtime]]"
  - "[[Echo Futures — D2-06 Market Runtime]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
aliases: []
confidence: high
memory_state: active
continuity_key: "echo-futures/d2-08-worker"
load_policy: when_project_loaded
indexable: false
index_priority: high
tags:
  - kind/agent-memory
  - scope/project
  - agent/internal
  - area/echo
---

# Echo Futures — Continuidad D2-08 Strategy Runtime Worker

## Continuidad

- Estado vigente: `D2-08 = READY_FOR_MANAGER_REVIEW`, `Q11 = CLOSED_CANDIDATE`, `OWNER_DECISIONS_REQUIRED = NONE`. Artifact: [[Echo Futures — D2-08 Strategy Runtime]]; handoff añadido a [[Echo Futures]] (sección D2-08). NO PASS, NO CLOSED, NO Q16/D2 final integration.
- Decisiones centrales congeladas (candidatas a manager review): isla `echo/strategy_engine` key `strategy_id` con estado técnico/indicators/readiness/timers/config/bookkeeping y CERO feedback de ejecución; ciclo lógico técnico transiciona sólo por Signals propias (jamás espera convergencia física, D2-02); trigger contract declarativo sin DSL (`bar_close`, `market_event` opt-in, `window/session_transitions`, `timers`) que alimenta MarketRequirements D2-06; evaluación ⇒ 0..N Signals ordenadas (`signal_id` UUIDv7 + sello `(strategy_eval_seq, signal_seq)`; 0 es común; >1 por decisión owner D1 — reconciliado con el "0 or 1" del mandato del worker); egress `echo.signals.v1` EXACTLY_ONCE (requisito de SPEC, carry D2-04 R2); fan-out `echo/signal_fanout` ya congelado D2-04 con target set linealizado en el island (kache read model, nunca authority) y semántica disabled = sin OPEN pero gestión de Operation viva sí; MM = plugin dentro de `echo/operation` con `mm_state` duradero (MMEngineFn PendingMM TTL = REPLACE; sdk/mm = REUSE/EXTEND sin pips); MM triggers = signal/execution facts/ForceClose/TimerFired/mercado opt-in; market context read-only compartido con notificaciones ligeras por op key subscripto; lógica pura sin Kafka/StateFun/PG/wall clock; EXACT_REPLAY = boundary D2-06 (digest de señales en decision log); adapter Core `ReferenceEvent→Signal` como seam transicional (migración = Iteración 2, DT-EF-REFERENCE-SIGNAL-03).
- Reuse map físico (baseline `372af59a`, clon `~/aranea/work/d4-shot1-20260925/echo`): `strategy_config.go` (`9169ee91`) = KVS pattern REUSE / contenido LEGACY_ONLY (es execution-policy config, NO runtime de Strategy); `execution_planner.go` (`f721f4dd`) = ADAPT patrón / REPLACE flujo (maxIntentAgeMs usa `time.Now()` — anti-patrón para el camino nuevo); `mm_engine.go` (`b04dea9b`) = ADAPT patrones (join snapshots, SendAfter, egress per-account `mm_engine.go:586`) / REPLACE estado (`PendingMM` TTL 30s cross-message); `sdk/mm` (`eb378e48`) = REUSE/EXTEND; cero `type Signal` en `v3/` (verificado; sólo ruido node_modules); `module.yaml` sin delivery semantics declarada (base del requisito EXACTLY_ONCE).
- Ratificaciones técnicas ordinarias pendientes al manager: naming físico de topics/campos, shape exacto `StrategyTriggerRequirements`/`SignalDelivery`, config EXACTLY_ONCE del egress. No hay owner decision abierta.
- Baselines: Echo `372af59a7b83604781346613da01e3d510ea1360` (fetch sin delta); Agents-OS HEAD al iniciar sesión `c592c697`; FINAL AGENTS-OS SHA = HEAD tras commit de esta sesión (registrado en el handoff entregado).
- No se implementó código, no se tocaron D2-01..07, no se abrió D3/D4/D5/D6, no se cerró D2 global.
- Siguiente paso: Primary Manager review de [[Echo Futures — D2-08 Strategy Runtime]] solamente.

## Señales de carga

- Cargar cuando se revise D2-08, se prepare D4 (SPEC S1/S2/Gerard — semántica de ciclo por Strategy y parámetros MM refinan allí sin cambiar el boundary), o se discuta la migración reference→Signal (Iteración 2).
- El wording histórico "0 or 1 Signal" del mandato del worker vs `0..N` del artifact: la resolución congelada es lista ordenada `0..N` por decisión owner D1 (A1 review) + D2-03 (único contrato Signal); el digest/orden vive en `(strategy_eval_seq, signal_seq)`.
