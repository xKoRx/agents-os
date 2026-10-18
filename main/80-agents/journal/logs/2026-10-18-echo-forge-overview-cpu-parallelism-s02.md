---
type: journal
schema_version: 1
created: "2026-10-18"
entities:
  - "[[Echo Forge — Operación Real V2]]"
tags:
  - kind/journal
---

# 2026-10-18 — Echo Forge: Overview CPU Parallelism S02 — PARALLEL_CANDIDATE_READY

- Corrección del Primary Manager a S01 atendida: CustomAnalysis ya no queda en 1 core. Rama `perf/overview-s02` @ `f4755c3` (parent S01 `cf8f522`, base 0.3.1 `492a271`; pusheada, sin merge a master). `EchoForgeOverviewExporter` con paralelismo acotado por estrategia (workers daemon, `AtomicInteger` work-stealing, escritura 100% post-join en orden de entrada, `workers=auto|min(8,cores−1)|N`, `workers=1` = ruta secuencial S01 intacta, fallback secuencial fail-safe) + sonda `EchoForgeParallelProbe`.
- Thread-safety SQX 144 investigado por decompilación (CFR sobre jars de flota, no asumido): `ResultsGroup.StampedLock` serializa mutaciones; superficie de lectura del exporter es por-instancia y sin lazy compartido. Candidato read-only sobre la databank.
- Pruebas de concurrencia: sonda intra-run PASS 24/24 en 3 pasadas (seq vs par×2) con speedup aislado 4,69–4,84× (w8); paridad física exacta en 5 comparaciones (base↔S02, S01↔S02, entre-runs S02, heavy 6/6+739/739); JFR: 8 hilos `EchoForgeOverview-W*` con muestras reales vs 1 hilo en baseline/S01; sampler /proc: picos 10–20 cores según `workers` (4/8/16/32).
- Benchmark: matriz 17/17 runs OK en copia candidate-local Kronos (`/home/echo-dev/forge-perf-s02/`), corpus pristine+SHA por run; TASK mediana 21s→7s(S01)→4s(S02); MaxRSS ~3,0–3,1 GB (−57% vs 7,2 GB base). Limitaciones documentadas: save SQX del databank secuencial (±5 s ruido TASK), corpus pequeño (extrapolación w10 = inferencia), 3 runs ctl invalidados por lock single-instance (sqcli huérfano; gotcha registrado).
- Retester/Optimizer (sólo análisis, subagente read-only): baja utilización = funnel con group `source` + `batch_size:1` secuencial (max_parallel ignorado fail-closed); palancas sin aprobación: `batch_size` retester y `max_parallel` en groups sin source; N-sqcli-por-host y batching optimizer>1 requieren aprobación arquitectónica. Detalle en artifacts.
- Flota intacta y estado restaurado verificado (Snippets.jar = SHA flota `71c706b2`, sin rastro del probe, sqcli.config devuelto a s01/rec). Entregables: `10-projects/Echo Forge — Operación Real V2/artifacts/ECHO-FORGE-CPU-PARALLELISM-S02/` (4 docs). Run registrado: [[2026-10-18-zcode-glm53-overview-cpu-parallelism-s02]]; continuidad interna: [[2026-10-18-overview-cpu-parallelism-s02-continuity]]; feedback: [[2026-10-18-aranea-ssh-mcp-transport-session-feedback]].
