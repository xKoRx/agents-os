---
type: evidence_doc
schema_version: 1
status: final
created: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
tags:
  - kind/evidence
  - area/echo
  - tech/performance
  - tech/concurrency
---

# ECHO FORGE — CPU PARALLELISM S02 — veredicto y resumen

**Veredicto: `PARALLEL_CANDIDATE_READY`. El paralelismo seguro dentro de una instancia SQX ES posible y fue demostrado con multicore real, throughput y paridad exacta.** La corrección del Primary Manager (S01 dejaba CustomAnalysis en ~1 core) queda respondida: el candidato S02 levanta el exporter de 1 a 8+ cores con salidas byte-idénticas.

## Qué se construyó

- **Rama `perf/overview-s02` @ `568907b`** (parent = S01 `cf8f522`, NO fusionada; base 0.3.1 `492a271`): `EchoForgeOverviewExporter` con paralelismo acotado por estrategia + `EchoForgeParallelProbe` (sonda de concurrencia). Detalles en [CONCURRENCY-PROOFS.md](CONCURRENCY-PROOFS.md).
- **Modelo**: N workers daemon consumen índices de estrategia de un contador compartido; cada worker construye la fila completa de UNA estrategia usando sólo APIs de lectura por instancia; **toda escritura ocurre tras el join, en orden de entrada, en el hilo llamador**. `workers=1` conserva el bucle secuencial de S01 byte a byte; `workers=auto` (default) = `min(8, cores−1)`; configurable por `exporter.properties`.
- Aislamiento: copia candidate-local `/home/echo-dev/forge-perf-s02/` en Kronos (patrón G7), flota SQX read-only, sin reinicios ni campañas afectadas. Estado restaurado y verificado al cierre (Snippets.jar = SHA flota `71c706b2`, sin rastros del probe, config JFR devuelta a S01).

## Resultados clave (corpus auténtico, host ocioso, misma sesión)

| Métrica | baseline 0.3.1 | S01 (memoización) | S02 = S01+paralelo (w8) |
|---|---|---|---|
| TASK CustomAnalysis (mediana, n≥3) | 21 s | 7 s | **4 s** (rango 3–11) |
| Fase fila (sonda aislada, 24 estr) | — | 7,67 s | **1,59–1,64 s (4,7–4,8×)** |
| Cores activos fase caliente (sampler /proc) | ~2,0 | ~2,1 | **~2,6–3,6; pico 5 s: 10–13** (w16: 16,8; w32: 20,3) |
| Hilos con muestras JFR en el exporter | 1 (main) | 1 (main) | **8 hilos `EchoForgeOverview-W*` (~200 muestras c/u)** |
| MaxRSS | 7,1–7,3 GB | 3,0 GB | 3,0–3,1 GB |
| Paridad vs baseline | — | exacta (S01) | **exacta: 24/24 + 2.976/2.976, 0 diffs; heavy 6/6 + 739/739, 0 diffs** |
| Determinismo entre runs S02 | — | — | **idénticos entre sí (0 diffs)** |

- Speedup total vs baseline (TASK, medianas): **~5,3×**; S02 aporta ~1,75× adicional sobre S01.
- El speedup de la fase de filas es estructural (4,7–5,1× medido dos veces en la sonda, misma JVM, mismos objetos).

## Respuestas directas al mandato

1. **¿APIs SQX admiten concurrencia?** Lectura concurrente por-instancia: SÍ (demostrado). Mutación concurrente: NO (SQX serializa con `StampedLock` por `ResultsGroup`; decompile en CONCURRENCY-PROOFS §1). El candidato no muta nada.
2. **Diseño acotado con orden reproducible**: sí — workers por estrategia, escritura ordenada post-join, sin dependencia del scheduling.
3. **Candidato aislado**: rama propia + copia candidate-local; nada desplegado a flota.
4. **Benchmark honesto**: multicore REAL medido por tres canales independientes (sampler /proc, JFR por hilo, sonda) — no "CPU alta" como prueba; paridad exacta exigida y obtenida.
5. **Retester/Optimizer**: causa raíz de la baja utilización identificada (funnel actual corre retest con `batch_size=1` secuencial y groups con `source` ignoran `max_parallel`); opciones con/ sin aprobación arquitectónica en [RETESTER-OPTIMIZER-UTILIZATION.md](RETESTER-OPTIMIZER-UTILIZATION.md). No se rompió el contrato de 1 sqcli/host.
6. **S01 preservado**: S02 se construyó SOBRE S01 (es la combinación evaluada); sin merge a master. El paralelismo también es aplicable al código 0.3.1 sin S01 (mismo patrón), pero no se midió esa variante.
7. **Limitaciones honestas**: corpus 24/6 estrategias (extrapolación w10 = inferencia, como S01); el save SQX del databank tras el exporter es secuencial y mete ±5 s de ruido en TASK (evidencia JFR `FileHandler.saveFile/OrdersList.serialize`); 3 runs de control quedaron invalidados por el lock single-instance de SQX ante un sqcli huérfano (gotcha documentado).

## Próximo paso sugerido

Integración de `perf/overview-s02` (incluye S01) vía el pipeline release estándar, con el canario de despliegue: línea `Parallel workers: N` en el log del exporter + hilos `EchoForgeOverview-W*` en el primer JFR post-deploy. Para el corpus real w10 se espera que el exporter baje de ~60 min a ~4–8 min (inferencia: 4,7–5,1× sobre la fase de filas medida en S01, pendiente de medición real).
