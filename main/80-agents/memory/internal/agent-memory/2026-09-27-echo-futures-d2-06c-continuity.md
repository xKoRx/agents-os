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

- **Mandato one-shot CUMPLIDO 2026-09-27:** `D2-06C = READY_FOR_SUBMANAGER_REVIEW`, `OWNER_DECISIONS_REQUIRED = 1`. Artefacto: `10-projects/Echo Futures/Echo Futures — D2-06C Live Replay Market Boundary.md`. Baseline: `xKoRx/echo origin/master = 372af59a` re-verificada en ventana (fetch sin delta; clon `~/aranea/work/d4-shot1-20260925/echo`); patterns inspeccionados puntualmente (module.yaml sin delivery semantics, `SendAfter`+`CancellationToken` en `mm_engine.go:610`/mock, kache/compacted, run_mode/run_id ausente del código, cero market-data/replay/clock en v3).
- Input congelado respetado: A y B (ACCEPTED_FOR_INTEGRATION) NO editados; D2-05/D2-04/D1 intactos; nota de proyecto NO promovida (es del SUBMANAGER). Prohibido al sucesor: avanzar D2-07, cerrar D2-06, seleccionar execution transport, reabrir A/B/D2-04/D2-05.
- **OWNER decision abierta OD-C1 (no bloquea review):** ¿EXACT LIVE REPLAY como capacidad V1 con recording always-on (recomendación del worker) o capacidad diferida con recording opt-in por run? El boundary congelado es idéntico en ambos casos; define sólo default de recording, retención mínima del contenido canónico y alcance de la certificación golden replay en D6.
- Decisiones congeladas por C (para review del SUBMANAGER — pueden ser corregidas, no asumirlas vigentes hasta ACCEPTED):
  1. **Tres identidades separadas:** `event_ts` (semántica técnica), `stream_seq` (orden/idempotencia del transporte por stream, A), y **`owner_input_seq`** (NUEVA: contador monótono checkpointeado por isla de dominio = runtime ordering identity; es lo que EXACT REPLAY reproduce; cruza epochs sin resetearse).
  2. **`MarketRuntimeInput` = 5 tipos:** MarketEvent | RecoveryBarrier | TimerFired | SessionWindowTransition | ConfigTransition. BAR_CLOSED NO es input grabado: **se re-deriva** (single content authority; probado contra late/timer/session/switch cases). Los journals de islas consumidoras guardan SÓLO orden referencial (`source_ref`) con integridad referencial ⇒ mismatch = `REPLAY_LOG_CORRUPT` fail-visible.
  3. **DeterministicInputLog por isla** (change-detection: se journala input que muta estado o dispara delivery; no-ops absorbidos por guards quedan como gaps legítimos del contador); egress transaccional EXACTLY_ONCE en la misma frontera de checkpoint (patrón D2-04 R14); eventos canónicos van por REF al topic (el tick jamás se duplica en el journal).
  4. **`echo.market-events.v1` SOLO es insuficiente** (sin timers/config/orden entre islas) y retención de Kafka ≠ recording contract: declarado explícitamente. Contenido purgado ⇒ `REPLAY_SOURCE_MISSING` fail-visible, jamás replay parcial silencioso.
  5. **DomainClock** (librería sdk pura): `Now/Schedule(timer_id, deadline)/Cancel`; LIVE = SendAfter wall-clock + CancellationToken; REPLAY/BACKTEST = reloj virtual (el reloj ES la secuencia de inputs); re-Schedule con mismo timer_id = replace; OPTION 1 del mandato: TimerFired se graba como input determinístico (no clock advances).
  6. **Ordering scope per-isla:** sin total order global ni sequencer central (reabriría B); el único merge cross-stream observable es strategy_engine ⇒ se journala por isla y el replay coordina por `source_ref`. BACKTEST sintetiza con precedencia canónica congelada al instante T: barriers → ConfigTransitions → transiciones sesión/ventana → eventos `(event_ts ≤ T, stream_id, stream_seq)` → timers `(deadline ≤ T, timer_id)`.
  7. **Same-instant:** LIVE = orden de admisión journalado (reproducible, no "depende de goroutines"); BACKTEST = regla canónica. El caso 09:31:00.000 canónico = transición → trade 09:30:59.900 → timer (estrategia observa barra CON el trade); el run live del caso duro B (trade llegó después del timer) produce el otro resultado válido y su replay lo reproduce por posiciones.
  8. **Cuatro modos distintos:** NORMAL RESTART = checkpoint (contadores incluidos; journal jamás sustituto); EXACT_REPLAY = manifest+journal+contenido, decision log a sink de observación, egress físico gateado por run_mode=REPLAY; COLD = `COLD_RECOVERY_REQUIRED` de D2-04 AUNQUE exista journal (el recording cubre el estado analítico mercado/strategy, jamás `mm_state`/ejecución — R12 intacto); HISTORICAL/BACKTEST = MarketHistorySource + síntesis canónica + warm-up B §17, sin claim de clonar runs live. `run_mode` formalizado: REPLAY ≡ EXACT_REPLAY, BACKTEST ≡ HISTORICAL; `recovery_provenance` sigue per-evento (A).
  9. **Manifest run-pinned** reusa snapshot-embebido D2-01 / snapshot-en-manifest D2-05 §19; config hot material = ConfigTransition journalada en posición de linearización (tabla de materialidad §13: calendar revisions, switches, rollover, requirements catalog, readiness gates aplicados; NO: thresholds telemetry-only, catalogs ajenos); strategy/MM config PINNED en manifest V1. Sin framework de revisiones nuevo.
  10. **Física:** cero funciones StateFun nuevas; 2 topics nuevos (`echo.market-run-journal.v1` transaccional, `echo.market-run-manifests.v1` compacted); `owner_input_seq` = estado aditivo C-owned en islas A/B/strategy_engine; ReplayDriver offline in-process sobre paquetes puros (patrón `v3/e2e/execution_engine.go` mock-context); equivalencia driver-vs-runtime = certificación golden replay D6.
  11. **A/B integration notes (§29 del artefacto):** cierra la pregunta abierta A §21 — el replay RE-DERIVA health/readiness de los inputs journalados (NO lo inyecta el manifest); responde los requisitos B §8/§22 (autoridad timers) y B §10/§24 (reproducir observaciones X). Costo recording ∝ streams×control-inputs + strategies×deliveries; cero × Account (case P).
- Acceptance A–P: todas PASS estructuralmente (map §30 del artefacto); golden replay físico queda como obligación D6.
- Siguiente paso: SUBMANAGER D2-06 integra A+B+C (única integración pendiente: los campos de estado aditivos + 2 topics + notes §29) → artefacto integrado D2-06 → Primary Manager review. Resolver OD-C1 con el owner en paralelo. No iniciar D2-07.
