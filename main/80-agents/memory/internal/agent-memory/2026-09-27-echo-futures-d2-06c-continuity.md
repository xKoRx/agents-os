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
  - "[[Echo Futures — D2-06C Live Replay Market Boundary]]"
  - "[[Echo Futures — D2-06B Bars Hot State Warmup]]"
  - "[[Echo Futures — D2-06A Market Feed Authority]]"
  - "[[Echo Futures — D2-05 Instrument Session Provider]]"
  - "[[Echo Futures — D2-04 Operation Order Fill Position]]"
aliases: []
confidence: high
memory_state: active
continuity_key: "echo-futures/d2-06c-worker-c"
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

# Echo Futures — Continuidad D2-06C (worker C)

## Continuidad

- **Mandato one-shot REPAIR CUMPLIDO 2026-09-27:** `D2-06C-R1 = READY_FOR_SUBMANAGER_REVIEW` (post-repair R1; BLOCKED_OWNER_DECISION: OD-C1 abierta, no bloquea review), `OWNER_DECISIONS_REQUIRED = 1`. Artefacto: `10-projects/Echo Futures/Echo Futures — D2-06C Live Replay Market Boundary.md` (ahora con sección "Manager Repair — D2-06C-R1" y TODO el documento actualizado). Baseline: `xKoRx/echo origin/master = 372af59a` re-verificada en la ventana del repair (fetch sin delta; clon `~/aranea/work/d3-shot3-correction-20260924/echo` entre otros). Candidato original @ vault ae960a6f; dirección general ACEPTADA por el SUBMANAGER (no rediseñar).
- **Delta R1 del repair (lo nuevo sobre el candidate v1):**
  1. **EXACT REPLAY ANCHOR = OPTION A (immutable warm-up corpus):** el recording conserva el corpus EXACTO de MarketEvents normalizados + snapshots calendario/config que el warm-up B §17 del run consumió (refs+digest+readiness assertion en el RunManifest, capturado UNA vez al iniciar el run); EXACT_REPLAY re-ejecuta ese corpus con la MISMA lógica B → mismo estado S → recién entonces `owner_input_seq=0`. PROHIBIDO re-consultar `MarketHistorySource` en replay. Sin anchor ⇒ `REPLAY_ANCHOR_MISSING`; mismatch ⇒ `REPLAY_ANCHOR_INVALID` (ambos fail-visible). La frase vieja "EXACT_REPLAY jamás pasa por warm-up" fue ELIMINADA (ahora: re-ejecuta el corpus grabado, jamás el seam live).
  2. **Runtime logical time `runtime_ts` (R2):** `DomainClock.Now()` JAMÁS deriva de `event_ts` (el candidate retrocedía ante TimerFired 09:31 + evento atrasado 09:30:59.900). `event_ts` gobierna sólo semántica técnica (barras/OHLC/session); `runtime_ts` es monotónico por isla, derivado en admisión como `max(previo, wall clock)`, journalado por entrada junto a `owner_input_seq`; REPLAY lo reproduce, BACKTEST lo sintetiza no-decreciente desde la precedencia canónica. No es campo de transporte: atributo de la entrada del journal.
  3. **TimerFired completeness (R3):** TODO TimerFired admitido se journala (SIN change-detection para timers — un firing puede ser prerequisito de control flow futuro: health tick que re-agenda); identidad `timer_id` + `generation` (re-Schedule = replace = cancel old + new generation); firing stale de generación vieja = NO-OP determinista absorbido por guard (gap legítimo); replay valida cada firing contra el timer set virtual: generación inexistente ⇒ `REPLAY_LOG_CORRUPT`, generación vieja ⇒ NO-OP idéntico al live.
  4. **Journal rule reescrita:** criterio = "¿puede este input afectar una observación de dominio presente o futura?" (NO "muta estado ahora"). ALWAYS: todo TimerFired admitido, ConfigTransition material, RecoveryBarrier, Session/Window transitions separadas, refs canónicos que pasan guards y afectan la isla, deliveries cross-island. MAY OMIT: redeliveries absorbidos pre-dominio, duplicados exactos de guards, telemetry-only sin efecto.
  5. **OD-C1 costo actualizado:** recording conserva además el anchor (captura única, acotada por MarketRequirements — el mismo span que el warm-up ya lee; no escala con duración del run; misma retención que el recording = R-C2). Opt-in diferido = compromiso AL INICIAR el run (run sin anchor = permanentemente no-replayable desde t0, R-C9). Refuerza recomendación always-on; decisión sigue del owner; arquitectura idéntica en ambos casos.
  6. **Acceptance Q–T nuevos** (anchor inicial, reloj monotónico con evento atrasado, cadena de timers no-op, reemplazo de timer con generación); riesgos R-C9/R-C10 nuevos; manifest porta `replay anchor` + `run_time_origin`; driver valida `runtime_ts` no-decreciente.
- Input congelado respetado: A y B (ACCEPTED_FOR_INTEGRATION) NO editados; D2-05/D2-04/D1 intactos; nota de proyecto NO promovida (es del SUBMANAGER). Prohibido al sucesor: avanzar D2-07, cerrar D2-06, integrar A+B+C, seleccionar execution transport, reabrir A/B/D2-04/D2-05.
- **OWNER decision abierta OD-C1 (no bloquea review):** ¿EXACT LIVE REPLAY como capacidad V1 con recording always-on (recomendación, ahora reforzada por R1) o capacidad diferida con recording opt-in por run (compromiso al iniciar)? El boundary congelado es idéntico en ambos casos; define sólo default de recording, retención mínima (contenido canónico + anchor) y alcance de la certificación golden replay en D6.
- Decisiones congeladas por C (para re-review del SUBMANAGER — pueden ser corregidas, no asumirlas vigentes hasta ACCEPTED):
  1. **Cuatro identidades separadas:** `event_ts` (semántica técnica), `stream_seq` (orden/idempotencia del transporte por stream, A), **`owner_input_seq`** (contador monótono checkpointeado por isla = runtime ordering identity; cruza epochs), y **`runtime_ts`** (runtime logical time monotónico por isla = única fuente de `DomainClock.Now()`; jamás `event_ts`).
  2. **`MarketRuntimeInput` = 5 tipos:** MarketEvent | RecoveryBarrier | TimerFired{timer_id, generation, deadline} | SessionWindowTransition | ConfigTransition. BAR_CLOSED NO es input grabado: **se re-deriva** (single content authority). `runtime_ts` NO es campo de transporte: atributo de la entrada del journal. Journals de islas consumidoras = SÓLO orden (`source_ref`) con integridad referencial ⇒ mismatch = `REPLAY_LOG_CORRUPT` fail-visible.
  3. **DeterministicInputLog por isla** (criterio de materialidad "presente o futura observación de dominio"; ALWAYS/MAY OMIT congelados; egress transaccional EXACTLY_ONCE en la misma frontera de checkpoint, patrón D2-04 R14; eventos canónicos por REF — el tick jamás se duplica).
  4. **`echo.market-events.v1` SOLO es insuficiente** (sin timers/config/orden entre islas/estado inicial) y retención de Kafka ≠ recording contract. Contenido purgado ⇒ `REPLAY_SOURCE_MISSING` fail-visible.
  5. **DomainClock** (librería sdk pura): `Now/Schedule(timer_id, deadline)→TimerHandle{timer_id, generation}/Cancel`; LIVE = `runtime_ts` derivado + SendAfter durable; REPLAY = runtime_ts journalados; BACKTEST = sintético no-decreciente; generación cancelada jamás ejecuta dominio (guard); OPTION 1 del mandato intacta (TimerFired = input determinístico grabado, ahora COMPLETO).
  6. **Replay anchor:** Run Recording = RunManifest + ReplayAnchor + DeterministicInputLog + contenido canónico. Anchor capturado una vez al iniciar el run (§16); driver lo re-ejecuta como paso 2 (§21) antes de seq=0.
  7. **Ordering scope per-isla:** sin total order global ni sequencer central; el único merge cross-stream observable es strategy_engine ⇒ journal por isla + replay coordina por `source_ref`. BACKTEST sintetiza con precedencia canónica congelada: barriers → ConfigTransitions → transiciones sesión/ventana → eventos `(event_ts ≤ T, stream_id, stream_seq)` → timers `(deadline ≤ T, timer_id)`.
  8. **Same-instant:** LIVE = orden de admisión journalado; BACKTEST = regla canónica. Caso 09:31:00.000 canónico = transición → trade 09:30:59.900 → timer (estrategia observa barra CON el trade); el run live del caso duro (trade llegó después del timer) es el otro resultado válido y su replay lo reproduce por posiciones.
  9. **Cuatro modos distintos:** NORMAL RESTART = checkpoint (contadores incluidos; journal jamás sustituto); EXACT_REPLAY = manifest+anchor+journal+contenido, decision log a sink de observación, egress físico gateado por run_mode=REPLAY, jamás MarketHistorySource; COLD = `COLD_RECOVERY_REQUIRED` de D2-04 AUNQUE exista journal (recording cubre estado analítico mercado/strategy, jamás `mm_state`/ejecución — R12 intacto); HISTORICAL/BACKTEST = MarketHistorySource + síntesis canónica + warm-up B §17, sin claim de clonar runs live. `run_mode` formalizado: REPLAY ≡ EXACT_REPLAY, BACKTEST ≡ HISTORICAL; `recovery_provenance` per-evento (A) intacta.
  10. **Manifest run-pinned** reusa snapshot-embebido D2-01 / snapshot-en-manifest D2-05 §19; ahora porta `replay anchor` + `run_time_origin`; config hot material = ConfigTransition journalada en posición (tabla §13); strategy/MM config PINNED V1. Sin framework de revisiones nuevo.
  11. **Física:** cero funciones StateFun nuevas; 2 topics nuevos (`echo.market-run-journal.v1` transaccional, `echo.market-run-manifests.v1` compacted); `owner_input_seq` = estado aditivo C-owned en islas A/B/strategy_engine; ReplayDriver offline in-process sobre paquetes puros (patrón `v3/e2e/execution_engine.go` mock-context); equivalencia driver-vs-runtime = certificación golden replay D6.
  12. **A/B integration notes (§29):** cierra la pregunta abierta A §21 — el replay RE-DERIVA health/readiness de los inputs journalados (NO lo inyecta el manifest); responde requisitos B §8/§22 (timers) y B §10/§24 (observaciones X); warm-up B §17 insumo del anchor. Costo recording ∝ streams×control-inputs + strategies×deliveries + anchor único por run; cero × Account (case P).
- Acceptance A–T: todas PASS estructuralmente (map §30 del artefacto); golden replay físico queda como obligación D6.
- Siguiente paso: SUBMANAGER D2-06 re-revisa C post-repair y luego integra A+B+C (única integración pendiente: campos de estado aditivos + 2 topics + anchor + notes §29) → artefacto integrado D2-06 → Primary Manager review. Resolver OD-C1 con el owner en paralelo. No iniciar D2-07.
