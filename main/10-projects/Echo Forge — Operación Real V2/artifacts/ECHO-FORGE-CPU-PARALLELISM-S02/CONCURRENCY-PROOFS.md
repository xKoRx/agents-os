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
  - tech/concurrency
---

# CONCURRENCY-PROOFS — thread-safety SQX y pruebas de concurrencia del candidato

Mandato: "Investiga si ResultsGroup, las APIs de SQX y EchoForgeOverviewExporter admiten procesamiento concurrente seguro. No asumir thread-safety." Tres niveles de prueba: (1) análisis estático por decompilación de los jars reales del build 144, (2) sonda intra-run sobre objetos reales, (3) paridad y determinismo físicos entre runs.

## 1. Análisis estático (decompile CFR 0.152 sobre jars de `/home/kor/sqx/144/internal/libs`)

| Clase | Hallazgo | Consecuencia |
|---|---|---|
| `ResultsGroup` | Campo `StampedLock resultsGroupLock` + protocolo `lockRecord()/releaseLock()`: **SQX serializa MUTACIONES por estrategia** | SQX mismo declara que la clase no es thread-safe para escritura. El candidato NO muta: devuelve `databankRG` intacto |
| `ResultsGroup` (lecturas usadas) | `getName()`, `mainResult()`, `orders()`, `getStrategyXml()` son lecturas planas de campos/mapas por instancia; `getBestWFResultKey()` tiene un lazy-cache no-volátil benigno (sólo doble cómputo posible, nunca corrompe) | Lecturas concurrentes sobre INSTANCIAS DISTINTAS sin estado compartido mutable |
| `Result` | `extends ValuesMap` (fastutil); `stats(dir,pl,sample)` = lookup puro de stats PRE-COMPUTADAS (`StatsDontExistException` si no hubo `computeAllStats` — no hay cómputo lazy que Course-corra); locks `ReentrantLock` propios para chart/dailyEquity (rutas NO usadas por el exporter) | Sin cachés compartidos en la superficie usada |
| `SQStats` | POJO sin campos static mutables ni cómputo lazy (22 métodos públicos, 0 static salvo Logger) | Lectura concurrente segura |
| `OrdersList`/`Order` | 0 campos static mutables; objetos por estrategia | Un worker por estrategia = exclusividad de hecho |
| `Databank` | `getResultsFilePath(rg)` = concatenación de strings; sin statics mutables relevantes | `scanForTrades` no llega al Databank: `skipHeavyMethod` filtra `getDatabank` (contiene "data") |
| Riesgo residual | Getters arbitrarios invocados por reflexión (`scanForTrades`) podrían tocar caches compartidos (p.ej. `L.t()`); el riesgo se neutraliza empíricamente (§2 y §3): cualquier carrera en lectura se manifestaría como SHAs divergentes o diffs entre runs | Cubierto por las pruebas 2 y 3 |

Superficie del exporter: `Pattern` precompilados (inmutables, thread-safe), `GETTERS_CACHE/FIELDS_CACHE` = `ConcurrentHashMap` con construcción idempotente, `org.json` por-fila (sin compartir), `SimpleDateFormat` siempre creado por llamada, writers confinados al hilo llamador en fase paralela.

## 2. Sonda intra-run `EchoForgeParallelProbe` (prueba más sensible)

En un solo run de SQX, sobre los mismos `ResultsGroup` ya cargados: (a) construye cada fila con el `buildStrategyRow` real (reflection, mismo código de producción) secuencialmente y guarda SHA-256 normalizado (`exported_at` neutralizado, mismo criterio que parity.py); (b) repite el cómputo con 8 workers en 2 pasadas paralelas; (c) compara las 3 pasadas.

Resultado (corpus-pristine, 24 estrategias, `perfs02probe/probe_out/parallel_probe.log`):

```
PROBE_SEQ ms=7670
PROBE_PAR1 ms=1585
PROBE_PAR2 ms=1636
PROBE_MATCH seq_vs_par1=24/24 seq_vs_par2=24/24 par1_vs_par2=24/24
PROBE_SPEEDUP par1=4.84 par2=4.69
PROBE_VERDICT PASS
```

- **Concurrencia segura demostrada intra-run**: lecturas paralelas sobre los objetos reales producen filas idénticas al recorrido secuencial (48 comparaciones por estrategia en total, 0 divergencias).
- **Speedup aislado de la fase de filas: 4,69–4,84× con 8 workers** (sin I/O de archivos, sin boot JVM).
- Defecto corregido durante la sesión: la primera versión de la sonda comparó `toString()` sin normalizar `exported_at` → MATCH 0/24 incluso entre pasadas paralelas (era un defecto del PROBE, no del exporter; commit `f4755c3`).

## 3. Paridad física y determinismo entre runs (parity2.py, mismo corpus pristine + SHA verificado por run)

| Comparación | overview.ndjson | monthly.ndjson | Resultado |
|---|---|---|---|
| baseline (base-r3) vs S02 (s02-r3) | 24 vs 24 | 2.976 vs 2.976 | **0 diffs, mismo orden** |
| baseline (base-r1) vs S02 (s02-r1) | 24 vs 24 | 2.976 vs 2.976 | **0 diffs** |
| S01 (s01-r3) vs S02 (s02-r3) | 24 vs 24 | 2.976 vs 2.976 | **0 diffs** (S02 ⊃ S01) |
| S02 run a vs run b (r1↔r2; w8-r2↔r3) | idénticos | idénticos | **determinismo bajo concurrencia** |
| heavy: baseline (base-h2) vs S02 (s02-h2) | 6 vs 6 | 739 vs 739 | **0 diffs** |

La paridad es del contenido completo de fila (métricas, overview por muestra, indicadores, bloques, diagnósticos, monthly agregado), con la misma normalización de S01 (`job_id`, `exported_at`, `finished_at`).

## 4. Diseño del candidato (por qué el orden es reproducible)

- **Fan-out**: `AtomicInteger` con contador de índices compartido; cada worker toma la siguiente estrategia (balanceo natural ante estrategias de peso desigual). Resultados a `rows[index]` — la posición es independiente del scheduling.
- **Fase ordenada**: tras `join` de todos los lanes, el hilo de `processDatabank` escribe en orden de entrada: línea overview, filas monthly, líneas trades_debug por estrategia; los logs de progreso `processed i/N` se emiten en las mismas posiciones que el secuencial (contenido idéntico; única línea extra en modo paralelo: `Parallel workers: N` — canario de despliegue).
- **Contención de errores**: todo `Throwable` por estrategia se atrapa dentro del worker → fila de error idéntica a la ruta secuencial; si un hueco quedara `null` (fallo del executor), se reconstruye secuencialmente post-join (`parallel_fallback_sequential=N` en log).
- **`workers=1`**: bucle secuencial original intacto → rollback = poner `workers=1` (o restore del jar), sin cambio de outputs.
- **Exclusividad**: un `ResultsGroup` lo procesa un solo worker a la vez; ningún objeto se comparte entre workers para escritura.

## 5. Artifacts de la investigación

- Decompile de clases clave: Kronos `/home/echo-dev/forge-perf-s02/decompiled/` (ResultsGroup, Result, SQStats, OrdersList, Databank, CustomAnalysisMethod, Debugger del build 144).
- Sonda y shas por estrategia: `user/projects/perfs02probe/probe_out/parallel_probe.{log,shas.tsv}` (en la copia candidate-local).
- Fuente del candidato: rama `perf/overview-s02` (`568907b` + `f4755c3`), `sqx/exporter-plugin/src/SQ/CustomAnalysis/{EchoForgeOverviewExporter,EchoForgeParallelProbe}.java`. Simulator JUnit: 13/13 PASS con los cambios.
