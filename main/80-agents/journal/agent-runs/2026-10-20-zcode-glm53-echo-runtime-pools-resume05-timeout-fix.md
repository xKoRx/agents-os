---
type: agent_run
schema_version: 1
scope: session
created: "2026-10-20"
updated: "2026-10-20"
area: "[[Echo]]"
project: "[[Echo Futures — Runtime Pools]]"
application:
entities:
  - "[[Echo Futures — Runtime Pools]]"
related:
  - "[[2026-10-19-zcode-glm53-echo-runtime-pools-resume03-typename-fix]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash (account:zai-individual-coding-plan/GLM-5.3-Flash)
model_source: host
task_type: coding
task_complexity: high
outcome: success
verification: full_suite
evaluator: agent
user_rework: unknown
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-10-20-zcode-glm53-echo-runtime-pools-resume05-timeout-fix

## Trabajo

- **Objetivo:** CERT-NT-01 / RESUME-05 — perfilar, corregir y demostrar estabilidad del timeout StateFun→Core (submanager LOCAL + especialistas A/B/B'/C one-shot GLM-5.3-Flash).
- **Alcance:** fix de producto `112ccccd` en `v3/core/internal/functions/futures_market_stream.go` (+75/−1: coalescing de persist-marks, 1 store/envelope + memo por batch en load) + regresión `futures_market_stream_persistence_cost_test.go`; release `~/opt/echo-dev/releases/112ccccd…`; push FF `c37d1351..112ccccd` (master `d74b6525` intacto); deploy core (PID 2936052); module verbatim `aa7a019c` (batch 1000 SIN cambio: candidato 100 NO aprobado por verificación); prueba sostenida real 31,7 min; paquete Owner JSON Sim101 completado (ID "2" obtenido del evidence-log del relay nt-feed y verificado contra source de ambos AddOns; parser real C# en .132 ALL_PASS 7/7 + negativo fail-closed).

## Evidencia

- **RCA con medición directa (A, agent_915ad212-22e6-4db5-871b-e0578dc5ea96):** harness in-proc sobre la ruta de producción real con 1001 envelopes reales de p4 (offsets 23.865.542–23.866.542) reproduce el incidente bit-a-bit (request 2.517.570 B vs 2.513.303 B; 147,8 s > timeout 120 s). Perfil CPU: `store()` 59% (2 EffectPersistState/envelope serializan el mismo bundle) + `load()` 40% (re-deserializa por envelope); spec `futures_ms_sequencer` con ventana dedup llena (4096+4096) = 2,1 MB JSON; engine ≈1%. Unidades reconciliadas: 1001 = maxNumBatchRequests; stream_seq = aceptados canónicos; 4460 = commitados visibles; Δ2288 = aceptado-no-commitado (granularidad de batch + reintentos), NO filtrado. Perfiles cpu/heap/allocs/block/mutex conservados en `~/aranea/work/cert-nt-01-a-resume5/measure/`.
- **Verificación independiente (B agent inactivo-kill sin id + B' agent_8833ea21-a458-45b1-b4f8-d6715aa60d86):** VERIFIED — rojo/verde replicado en worktrees separados; suites fix = patrón EXACTO de baseline (5 heredadas, 0 nuevas); diferencial base↔fix byte-idéntico salvo duración; 7/7 ataques adversariales PASS (staleness memo, fallo mid-batch all-or-nothing, equivalencia memo↔round-trip, tick real interleaved, overflow cap, protocolo SDK v3.3.0 storage-fresco-por-request); `-race` 0; ventana dedup 4096+4096 y criterio intactos (sólo cambia CUÁNDO se serializa). Sustained: +18,4 env/s (b1000) / +21,1 env/s (b100) de pendiente a 47 env/s live ⇒ MITIGACION_INSUFICIENTE sin C2 PASS. Config batch 100: throughput idéntico ⇒ NO aprobada.
- **Despliegue y prueba sostenida (C, agent_5d7f3d1a-7f59-4e6b-9212-c92e4b18b4ca):** preflight VERDE; core 112ccccd (owners:7, health 200, FX lag→0); verbatim → job `faf27ca3` 38/38 en 65 s, 0 excepciones; **ESTABILIDAD PASS**: 31,7 min con feed vivo (ingress 46,1 rec/s): 0 timeouts/restarts/excepciones, 14 checkpoints COMPLETED, ETCD intacto (revs 61253/61254), armado ausente. **FRESQUEZA FAIL confirmado**: servicio real 20,5 rec/s ⇒ pendiente +25,6 rec/s; edad del evento 129→1.334 s ≫ `DefaultFreshnessBounds{30s/60s/5s}` (FreshnessStale; admisión continúa por diseño D6). Monitoreo CSV en `~/aranea/work/cert-nt-01-c-resume5/monitor/`.
- **Spot-check final del submanager:** job 38/38 running, 19 chk COMPLETED/0 failed (REST .75:8082), core PID 2936052 health ok, ls-remote feature==112ccccd/master==d74b6525.

## Evaluación

- **Correctness:** 5 — RCA medida (no inferida), fix mínimo verificado adversarialmente, estabilidad demostrada en runtime Flink real.
- **Autonomy:** 5 — pipeline completo A→B→C con B dekillizado y re-cerrado (B'), sin re-trabajo del Manager.
- **Residual:** paridad de ingress NO alcanzada (palanca arquitectural: estado shardado/incremental del sequencer — fuera de alcance); servicio real 20,5 vs 28,1 in-proc (overhead HTTP/wire sin descomponer); estabilidad ≠ frescura: el éxito incluye progreso y frescura, no sólo ausencia de excepciones.
