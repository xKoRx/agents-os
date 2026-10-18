---
type: agent_memory
schema_version: 1
scope: domain
created: "2026-10-18"
updated: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
related:
  - "[[Echo Forge — Operación Real V2]]"
  - "[[aranea-ssh-mcp]]"
aliases: []
confidence: verified
memory_state: active
continuity_key: domain/forge-overview-cpu-parallelism
supersedes: ""
load_policy: manual
indexable: true
index_priority: medium
tags:
  - agent/internal
  - kind/agent-memory
  - project/echo-forge
  - scope/domain
---

# Overview CPU Parallelism S02 — continuidad (2026-10-18)

## Estado al cierre

- `PARALLEL_CANDIDATE_READY`: rama `perf/overview-s02` @ `f4755c3` (parent S01 `cf8f522`, base 0.3.1 `492a271`; pusheada, SIN merge). Exporter con paralelismo por estrategia (workers daemon + escritura ordenada post-join; `workers=auto|min(8,cores−1)|N|1=secuencial`) + sonda `EchoForgeParallelProbe` (SHA intra-run seq-vs-par ×2 pasadas).
- Evidencia: `10-projects/Echo Forge — Operación Real V2/artifacts/ECHO-FORGE-CPU-PARALLELISM-S02/` (README veredicto, CONCURRENCY-PROOFS, BENCHMARK-COMPARISON, RETESTER-OPTIMIZER-UTILIZATION). Kronos: entorno en `/home/echo-dev/forge-perf-s02/` (run-matrix.sh, analyze-s02.py, jfr-main.py, deploy-s02.sh; csv/jfr/ndjson de 17+3 runs en rec/ y out/). Flota restaurada y verificada (Snippets.jar = `71c706b2` SHA flota; sin probe en manifiesto ni fuente; sqcli.config JFR devuelto a s01/rec).
- Números: TASK mediana 21s base → 7s S01 → 4s S02; sonda 7,67s→1,59/1,64s (4,7–4,8×, w8); pico 5s 10–20 cores según workers; paridad exacta 5/5 comparaciones (24/24+2976/2976 y heavy 6/6+739/739); determinismo entre-runs S02 exacto; MaxRSS ~3,0–3,1 GB.
- NEXT: Primary Manager decide integración (pipeline release reconstruye Snippets.jar; canarios post-deploy: línea `Parallel workers: N` en log del exporter + hilos `EchoForgeOverview-W*` en JFR). Retester/Optimizer: batch del retester y `max_parallel` (grupos SIN `source`) son las palancas sin aprobación; datos por stage en Prometheus/PG pendientes de extraer.

## Lecciones/gotchas (reusables)

- **Thread-safety SQX 144 (decompile, no asumido)**: `ResultsGroup` tiene `StampedLock` propio para MUTACIONES (SQX las serializa); lecturas por-instancia usadas por el exporter son planas (`Result.stats` = lookup de stats pre-computadas, cero lazy compartido). El candidato no muta la databank ⇒ paralelismo de lectura seguro demostrado intra-run.
- **Lock single-instance SQX en vivo**: un sqcli huérfano hace que los boots siguientes salgan en 2–3 s con exit 0, "Bye/another instance" y SIN ejecutar tarea — benchmarks secuenciales deben verificar entre runs que no quede JVM viva (pgrep) y que cada out dir tenga `_SUCCESS` propio con mtime del run.
- **Sampler /proc por pgid**: el pgid se RECICLA — recortar el csv al primer salto negativo de ticks (>1000); `touch` NO trunca (usar `rm -f` + touch o `: > file`); rutas de stop-file derivar SIEMPRE de la misma variable que el csv.
- **Transporte aranea-ssh**: base64/binario → `[REDACTED]`; heredocs remotos se corrompen; sftp-download 1MB y binarios inline; receta estable = http.server efímero en Daedalus + curl + SHA256, scripts por sftp-upload, comandos compuestos cortos, runs largos con nohup + polling.
- **Defecto de sonda**: comparar `row.toString()` sin normalizar `exported_at` da MATCH 0/24 incluso par-vs-par (falsa alarma de race); normalizar timestamps antes de hashear (mismo criterio que parity.py).
- El save SQX del databank tras el exporter (`FileHandler.saveFile/OrdersList.serialize`) es secuencial, NO paralelizable desde el snippet, y mete ±5 s de ruido en `TASK FINISHED` (también en baseline: 17–31 s en S01) — medir la fase de filas con la sonda, no con TASK.
