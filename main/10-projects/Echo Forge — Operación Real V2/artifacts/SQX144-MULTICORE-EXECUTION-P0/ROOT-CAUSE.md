---
type: evidence_pack
schema_version: 1
status: final
created: "2026-10-18"
updated: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[xKoRx/symphony]]"
baseline: "xKoRx/symphony 492a271e84f1faa1d4050b7ab35255863b2992e5 (release 0.3.1); SQX 144.2953 y 142; host sqx-kronos 76 vCPU"
verdict: "SQX144_MULTICORE_EXECUTION_PASS_WITH_SUPPLY_DEFECT"
related:
  - "[[Echo Forge — Operación Real V2]]"
  - "[[SQX144-CPU-UTILIZATION-20261018]]"
  - "[[ECHO-FORGE-CPU-PARALLELISM-S02]]"
tags:
  - kind/evidence-pack
  - area/echo
  - tech/performance
---

# ROOT-CAUSE — utilización multinúcleo de SQX 144 en la flota Forge

## Veredicto

`SQX144_MULTICORE_EXECUTION_PASS_WITH_SUPPLY_DEFECT` — **SQX 144 SÍ aprovecha todos los cores asignados cuando recibe trabajo paralelizable suficiente** (demostrado físicamente en builder, retest por databank y optimizer WFO, con un solo proceso sqcli por VM); la subutilización observada en las ejecuciones de la flota **no es una limitación del motor**: es un **defecto de suministro de trabajo del funnel Forge** (lotes de 1 estrategia + grupos `source` secuenciales fail-closed + 1 actividad por host), que entrega a cada JVM SQX menos unidades independientes de trabajo que sus cores.

## La pregunta del mandato, respondida con medición

"¿Por qué SQX puede preparar decenas de ejecutores y terminar usando uno o pocos cores?" — Porque **preparar el pool es estático y el consumo depende del trabajo**: SQX crea 72 executors al boot ("Preparing thread executors: 72") y sólo los ocupa si hay N≥~10 estrategias por corrida (retest), una generación genética en curso (builder) o un WFO de optimizer. Medido en Kronos (76 vCPU, 1 sqcli, settings 100 %/ON):

| workload suministrado | cores que SQX realmente usa (fase caliente) | fuente |
|---|---|---|
| retest de 1-5 estrategias (batch_size:1 del funnel) | ~2-5 (pico 5-10) | retest144-n10/n30 + builder E2E w10 (sar) |
| retest databank N=450-600 | **picos 72,6-74,1 de 76; throughput 36,7 str/s aún creciendo** | CPU-BENCHMARK.csv |
| builder genético (islands 8, pop 400) | **media 68,46 sostenida 40 min; pico5 77,6; mediana RUNNABLE 72** | build144-r3 |
| optimizer WFO de 1 estrategia | **pico5 72,6; media 20,6** | opt144-r3 |

La cadena ejecución→CPU es directa: `Temporal → worker (MaxConcurrentActivityExecutionSize=1) → CommandExecutor (setsid, sin affinity/quota) → sqcli (launcher Go que exec-reemplaza a la JVM en el mismo proceso) → pools SQX (72 executors)`. Sin restricción física en ningún eslabón (S01: cgroups/cpu.max ausente, cpuset completo, %steal 0; esta sesión: JVM dentro del proceso sqcli con 258 threads, 150 de ellos con ticks reales).

## Respuestas A–H (sección 5 del mandato)

- **A. Pool inicializado sin trabajo suficiente: SÍ — causa primaria.** El funnel entrega 1 estrategia por corrida en retester/optimizer/final-reretester (batch_size:1 y contrato exactly-1-upstream) y los groups con `source` procesan chunks secuencialmente (fail-closed, `max_parallel` ignorado: `generic_workflow.go:1790-1834`, `config.go:268-271`). Con N<~10, SQX usa 1-5 cores aunque el pool sea de 72.
- **B. Restricción interna de scheduling: NO para retest/builder/optimizer.** El "Batch size computed to: X … totalCores: 72" de SQX reparte los N entre cores; a N≥450 el pico toca 74 cores. (Única semántica especial medida: el batch interno arranca en ~5 y crece con N; no se observó techo <76.)
- **C. Workflow fragmentando trabajo: SÍ — causa primaria en fases de retest** (mismo punto A; detalle en WORKLOAD-AND-BATCHING-ANALYSIS.md). No es rediseño: es configuración de tamaño de lote declarada "iterable por campaña" por el owner (2026-09-28).
- **D. Configuración de paralelismo pendiente: NO.** Max Performance (100 %/ON) demostrado aplicándose en cada arranque CLI ("Using: 72 cores, core usage configuration: '100%'"); `threadAffinity=false`.
- **E. CLI ≠ GUI en paralelismo: sin diferencia demostrable.** El CLI usa 76 cores desde el arranque CLI (build/opt/retest) — la ruta CLI NO degrada el paralelismo. GUI-vs-CLI físico bloqueado por ausencia de X en la flota (GUI-VS-CLI.md); la pregunta operativa queda respondida por medición directa.
- **F. Regresión 144 vs 142: NO demostrada.** Mismo workload equivalente (darwinex N=30, mismas estrategias, mismas settings): wall 26,87 s (144) vs 25,95 s (142), mismo perfil de cores. Incompatibilidad REAL en el otro sentido: los datos UTC02 adaptados para 144 **no cargan en 142** (NPE `BacktestDataFeed.loadDataForFeed`) — SQX-142-VS-144.md.
- **G. Contención que serializa: la secuencialidad está EN FORGE, no en SQX** (punto A/C). Dentro de SQX no se midió contención que freine el paralelismo con trabajo suficiente.
- **H. Otros factores físicos: ninguno.** Heap efectivo -Xms4g/-Xmx55g, MaxRSS 7-18 GB de 125 GB, ParallelGC, sin swap, host ocioso durante toda la batería.

## Consecuencia operacional

Durante las campañas actuales, los stages de retest de finalists y optimizer corren a 1-5 cores por host de 28/64/76 — hay 90-95 % de CPU comprada ociosa en las fases que el E2E w10 midió como dominantes (retest 2-3 cores/host). La corrección es de CONFIGURACIÓN de campaña (tamaño de lote del retester) y una decisión de arquitectura acotada (fan-out de groups con `source`), no una corrección de SQX ni del launcher; REMEDIATION.md detalla vías con su gate de aprobación. El mandato S01/S02 (overview exporter) queda fuera: su CustomAnalysis secuencial explica el 87 % del wall del builder de Forge y ya tiene candidato (perf/overview-s02), no re-tratado aquí.
