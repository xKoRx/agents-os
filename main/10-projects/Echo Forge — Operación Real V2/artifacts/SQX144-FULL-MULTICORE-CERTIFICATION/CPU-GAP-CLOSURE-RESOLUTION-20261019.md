---
type: acceptance
schema_version: 1
status: final
created: "2026-10-19"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[xKoRx/symphony]]"
baseline: "xKoRx/symphony 492a271e (release 0.3.1); candidato S01+S02 = perf/overview-s02 @ f4755c3 (parent perf/overview-s01 @ cf8f522c, ambos publicados en origin); SQX 144.2953 (sqcli flota 7d312106); host sqx-kronos (72 cores); 1 SQX/VM en todo momento"
verdict: "ECHO_FORGE_FULL_CPU_CERTIFICATION = READY_FOR_MANAGER_ADJUDICATION — CUSTOMANALYSIS: candidato físico demostrado (13,4× paridad FULL, NO desplegado); RETESTER_N10: REAL_COMPUTATION_CONFIRMED (FAIL previo = artefacto de datación); LINEAGE: CORRECTED_AND_DEMONSTRATED (harness only)"
tags:
  - kind/acceptance
  - area/echo
  - tech/performance
---

# CPU GAP CLOSURE — RESOLUCIÓN de los 3 gaps (2026-10-19, mandato ONE-SHOT)

Resolución de los tres hallazgos de [[CPU-GAP-CLOSURE-20261019]] (NOT_CERTIFIED). Sin E2E, sin deploy, sin releases, sin merge a master, 0.3.1 intacta, sin CFX del owner modificados, sin cancelar trabajo sano, una instancia SQX por VM en todo momento (guard singleton de `fc-run.sh`; `NO_SQX_RUNNING` verificado entre fases).

## Veredictos finales

| Gap | Veredicto previo | Veredicto final |
|---|---|---|
| GAP 1 — CustomAnalysis builder | FAIL (secuencial 1,059 cores) | **REMEDIATED_PHYSICALLY (candidato, NO desplegado)** — candidato S01+S02 @ `f4755c3` demostrado sobre el corpus pristine de 300: **242,6 s → 18,1 s (13,4×) con paridad FULL** en workers=1/8/16/32; óptimo 16 workers |
| GAP 2 — Retester N=10 | FAIL (sin cómputo paralelo real) | **REAL_COMPUTATION_CONFIRMED** — el FAIL previo fue un artefacto de datación de ventana (console buffering); con la ventana del log global, N=10 quema 20,0–22,5 CPU-s reales; paralelismo real acotado por N (~8–9 cores con 10 estrategias); `RETESTER_PARALLELISM_DEFECT` REFUTADO |
| GAP 3 — Lineage Retester→Optimizer | FAIL (Optimizer consumía bytes pre-retest) | **CORRECTED_AND_DEMONSTRATED** — `fc-stage.sh` S5b corregido (siembra desde el banco de salida físico del Retester, con guardia de identidad por nombre y sellos); replay de los 10 optimizers con la cadena completa verificada por hash |

---

## GAP 1 — CustomAnalysis: candidato S01+S02 demostrado físicamente (NO desplegado)

### Discrepancia remota resuelta

Las ramas `perf/overview-s01` (`cf8f522c`) y `perf/overview-s02` (`f4755c3`, contiene S01 + candidato + probe) existían **sólo localmente**; no estaban en `xKoRx/symphony` (verificado con `git ls-remote` — el Manager tenía razón). Ancestry verificado: `f4755c3 → 568907b (S02 candidate) → cf8f522c (S01) → 492a271e (0.3.1)`. Ambas fueron **pusheadas al remoto canónico** y verificadas por ref exacto en GitHub.

### Reconstrucción del experimento (mechanismo canónico de producción, réplica escribible)

El `internal/libs` de la instalación cert es un symlink kor-owned no escribible; el `Snippets.jar` de la instalación perf candidate-local (`/home/echo-dev/forge-perf-s01/sqx144-perf`) estaba **en estado fleet `aac0e8f2`** (restaurado tras el bench S01 del 18-oct) y es escribible: se recreó allí el proyecto réplica `fc-g1ca` con el `project.cfx` byte-idéntico del cert (`7b9564a8…`) y el mismo corpus. Corpus: prefijo ordenado 300 de `overview1117`, verificado contra el sello `g1-ca-input.sha256` del cert **antes de cada corrida** (restore + sha256sum + diff del sello).

Candidato compilado en Kronos desde los bytes exactos de `f4755c3` (SHA fuente `a2833516…`, subido y verificado por SHA) con `javac` del j64 de la instalación contra los jars del SDK 144 (stubs de `forge-perf-s01/build/stubs`). Despliegue por el mecanismo real `snippet>jar` (`jar uf` de las 8 clases `EchoForgeOverviewExporter*`).

**Verificación del bytecode efectivo cargado**: (1) la clase fleet extraída (`5370f8fb…`) difiere de la candidata (`de63f659…`); (2) `javap` muestra `processDatabankParallel`/`RowOut` sólo en el candidato; (3) tras el deploy, la entrada re-extraída del jar es **byte-idéntica** (`cmp` OK) al `.class` compilado; (4) marcador runtime `Parallel workers: N` impreso por el exporter en el log de cada corrida paralela (imposible en el fleet).

Los workers se fijan por `user/projects/fc-g1ca/exporter.properties` (`workers=N`; el 0.3.1 no lee esa clave — el baseline corre intacto). Medición con el harness del cert (`fc-run.sh`): group-jiffies @200 ms + per-tid @1 s + `/usr/bin/time -v`; ventana CA = `TASK STARTED → TASK FINISHED` del log global de SQX (método idéntico para baseline y candidatos).

### Ladder (Kronos, 300 estrategias pristine, ventana TASK del log global)

| Run | Workers (marcador runtime) | Ventana CA (s) | Cores medios | Core-s | Throughput (str/s) | Speedup | Hilos de cálculo | MaxRSS (GB) |
|---|---|---|---|---|---|---|---|---|
| g1b-fleet (baseline 0.3.1) | — (secuencial) | 242,62 | 1,142 | 277,2 | 1,24 | 1,00× | 1 worker (238,3 CPU-s = 86%) + GC | 15,16 |
| g1c-w1 | n/a (ruta secuencial S01) | 106,80 | 1,417 | 151,4 | 2,81 | 2,27× | 1 worker | 8,94 |
| g1c-w8 | `Parallel workers: 8` | 28,63 | 10,131 | 290,0 | 10,48 | 8,47× | **8 workers equilibrados (15,3 CPU-s c/u, per-tid)** | 14,95 |
| g1c-w16 | `Parallel workers: 16` | 18,09 | 17,249 | 312,1 | 16,58 | **13,41×** | pool de 16 (CPU media 17,2 cores por group-jiffies; el sampler per-tid sub-muestrea en ventanas <20 s) | 15,55 |
| g1c-w32 | `Parallel workers: 32` | 16,47 | 28,954 | 476,9 | 18,21 | 14,73× | ídem (28,9 cores medios) | 16,24 |

Todos: exit 0, `Task finished`, sync `300/300/saved 300`, manifest `expected=300 written=300 errors=0 monthly_rows=33858`, overview.ndjson 300 líneas, monthly.ndjson 33.858 líneas. Baseline del cert (229,5 s / 1,059 cores en la instalación cert) consistente con este baseline réplica (242,6 s / 1,142 cores); el speedup se calcula intra-sesión, mismo método y entorno.

**Paridad FULL vs 0.3.1**: overview.ndjson (300 filas, en orden), monthly.ndjson (33.858 filas, en orden) y manifest **idénticos en los 4 puntos del ladder** tras normalizar sólo los campos volátiles por diseño (`exported_at`, `job_id`, `finished_at`) — 0 diffs.

**Cuello serial residual (declarado, no oculto)**: ~12–13% del tiempo secuencial (Amdahl desde w1→w32: 16,47 = f·106,8 + (1−f)·106,8/32 ⇒ f≈0,13): fase de escritura ordenada post-join + sync del databank (11,6 s, secuencial SQX) + arranque del pool. Es la causa del retorno decreciente de w32.

**OPTIMAL_WORKER_COUNT = 16**: 13,4× con energía +11% vs baseline (312 vs 277 core-s). w32 añade sólo +9,8% de throughput por +53% de energía (476,9 core-s) — se descarta por despilfarro, no por riesgo. w8 es el punto conservador (8,5× con energía de paridad).

### Estado del entorno al cierre

`Snippets.jar` del perf install restaurado a su estado encontrado **`aac0e8f2…` (fleet)**, verificado por SHA; instalación cert y flota sin tocar; `PRODUCT_MUTATIONS: NONE`; 0.3.1 intacta; el candidato NO está desplegado en producción (decisión de integración = GPT-6).

---

## GAP 2 — Retester N=10: REAL_COMPUTATION_CONFIRMED (el FAIL previo era un artefacto de medición)

Mandato: no declarar `SingleOptims` causa sin evidencia; corpus costoso auténtico; distinguir veredictos.

### Corpus costoso auténtico

Top-10 del corpus `overview1117` por trade count (21.130, 21.123, 21.074, 21.064, 21.049, 20.998, 20.996, 20.946, 15.239, 9.278 trades), extraídas del `overview.ndjson` del baseline, con manifiesto `gap1/expensive10-manifest.json` (nombre + SHA256 por archivo) y copia sellada en `gap1/corpus-expensive10/`.

### Ejecuciones (Kronos, instalación cert, sqcli flota, ventana = TASK del log global, energía = group-jiffies dentro de la ventana)

| Run | Corpus | N | Ventana (s) | CPU real (core-s) | Cores medios | `SingleOptims` |
|---|---|---|---|---|---|---|
| g2-exp10 | costoso | 10 | 2,45 | **20,20** | 8,2 | false |
| g2-exp10b | costoso (repetición inmediata, resultados ya re-guardados) | 10 | 2,24 | **20,04** | 8,9 | false |
| g2-exp10c | costoso (2.ª repetición) | 10 | 2,87 | **25,38** | 8,8 | false |
| g2-exp1 | la más pesada sola | 1 | 1,67 | **4,06** | 2,4 | false |
| g2-cohort10 | cohort barato del cert (10 del builder) | 10 | 2,68 | **22,50** | 8,4 | false |

### Verificación de las cinco preguntas del mandato

1. **SQX ejecutó realmente los diez backtests**: SÍ — 20,0–25,4 CPU-s medidos en la ventana TASK (4,06 CPU-s cuesta UNA estrategia de 21k trades sola; 10 en batch = 20–25 CPU-s, consistente con recomputación completa con data compartida). El "0,05–0,6 CPU-s" del cert se debe a que su ventana se dató por el console buffering (el mismo gotcha que ya documentaron para la CA): la energía real cayó fuera del slice medido. La misma metodología correcta aplicada al cohort barato del cert arroja **22,50 CPU-s** — no hay nada que explicar con "ruta sin cómputo".
2. **No reutilizó resultados ni saltó cálculos**: SÍ re-ejecuta SIEMPRE — la repetición inmediata sobre resultados recién re-guardados (g2-exp10b) vuelve a quemar 20,04 CPU-s; y los bytes del databank cambian materialmente input→output (forense del integ-retest del cert: `orders.bin` 852 KB→88 KB re-generado, entry `Results/Main:` renombrado al data-context del proyecto, `settings.xml`/`lastSettings.xml` actualizados).
3. **Métricas y trades válidos por estrategia**: SÍ — `TASK FINISHED` sin errores en las 5 corridas; el banco de salida se re-escribe completo (`files before sync 0 / after sync 10 / saved 10`).
4. **Outputs corresponden a config/periodo ejecutado**: SÍ — los entries internos del `.sqx` (`settings.xml`, `lastSettings.xml`, `Results/Main: <data>`) quedan regenerados bajo el contexto del proyecto `fc-retest`.
5. **¿Suficiente trabajo para saturar?**: con N=10 el trabajo disponible son 10 backtests (~2 CPU-s/estrategia en esta tarifa); el paralelismo observado (~8–9 cores medios) es real y coherente con ~1 thread por estrategia. Exigir 72 cores con 10 unidades de trabajo no tiene sentido físico: **`INSUFFICIENT_WORKLOAD` no aplica como defecto; `RETESTER_PARALLELISM_DEFECT` queda REFUTADO por energía.**

### Significado de `SingleOptims` (evidencia, 9 corridas)

`Batch size computed to: 5, SingleOptims: false, str to test: N, totalCores: 72` con N ∈ {1,3,10×4,30} y `SingleOptims: true` con N ∈ {90,300,600}: es el **selector de ruta del retester** — `false` para N ≤ totalCores (retest individual de cada estrategia, paralelismo acotado por N ≈ 1 thread/estrategia), `true` para N > totalCores (la grilla de batches del motor, la certificada en el ladder n90–n600 con 62–68 cores). En N=10 el motor elige la ruta individual; el punto de operación usa ≤10 cores **por diseño de la ruta, no por un defecto** — el escalado certificado del motor permanece intacto.

Veredicto: `REAL_COMPUTATION_CONFIRMED`; multicore en N=10: paralelismo real acotado por N (sin defecto; sin saturación posible).

---

## GAP 3 — Lineage: harness corregido y los diez saltos verificados (sólo harness, 0 cambios de producto)

### Corrección (harness del cert, no producto)

`fc-stage.sh` S5b sembraba el Optimizer con `seed_one "$COHORT"` (bytes PRE-retest). Corregido (backup `fc-stage.sh.pre-gap3-bak`): `RETESTOUT="$CERT/${SQXROOT}/user/projects/fc-retest/databanks/output"` + guardia fail-closed de identidad por nombre cohort↔retest-output + sello físico del stage `rec/integ-retest-output.sha256` + `seed_one "$RETESTOUT" ...` + sello final de lineage por estrategia (cohort==retest-input; retest-output≠cohort; optimizer-input==retest-output). Ningún archivo productivo de Forge modificado.

### Replay mínimo sobre outputs existentes (labels nuevos `integ-opt2-01..10` para preservar la evidencia FAIL original)

Cadena verificada por identidad canónica (nombre) y hashes físicos, para las 10 estrategias del cohort:

- **Builder → cohort**: sello del cert (`state/builder-output.sha256` ⊇ `state/cohort.sha256`) — sin cambios, OK.
- **Cohort → Retester INPUT**: el banco input de hoy proviene de `$CERT/cohort` vía `fc-prep.sh` (sello `fc-retest-n10-input.sha256`, respaldado el histórico en `gap2/evidence-backup/`).
- **Retester INPUT → OUTPUT**: banco de salida físico post-retest sellado (`rec/integ-retest-output2.sha256`, 10/10, hashes ≠ cohort — bytes retesteados).
- **Retester OUTPUT → Optimizer INPUT**: 10 optimizers re-ejecutados (`integ-opt2-01..10`, `Task finished` 10/10) sembrados desde ese banco; sellos `rec/integ-opt2-XX-source.sha256` == sello del output del retester, estrategia por estrategia.

| Estrategia (orden sorted) | cohort (pre-retest) | retest INPUT | retest OUTPUT | optimizer INPUT | Cadena |
|---|---|---|---|---|---|
| (10 filas — ver `gap2/lineage-final.tsv` en Kronos) | == builder output | == cohort | ≠ cohort (re-escrito) | == retest OUTPUT | **10/10 OK** |

La semántica productiva de `steps.go` @ 492a271e (el retester publica los .sqx retesteados y la etapa siguiente los consume como upstream) queda ahora demostrada por el harness corregido. WFO intacto (cada optimizer re-ejecuta sus propios backtests sobre su input).

---

## Crudo y reproducibilidad (Kronos)

- GAP 1: `$CERT/gap1/` — `src/EchoForgeOverviewExporter.java` (SHA `a2833516…` = f4755c3), `classes/`, `verify-extract/` (entrada del jar == build), `Snippets.jar.fleet-aac0e8f2.jar` (backup/restore), `baseline-outputs/` + `SHA256SUMS.txt` (salidas 0.3.1 del cert), `runs/g1b-fleet|g1c-w{1,8,16,32}/` (ndjson+manifest+logs), `analyze-g1.py`, `parity-g1.py`, `gap1-run.sh`, `ladder.sh`; recs `g1b-fleet-*` y `g1c-w*-*.csv/log`.
- GAP 2: `$CERT/gap1/corpus-expensive10/` + `expensive10-manifest.json`; `g2-bytes-forensics.sh`, `g2-entry-diff.sh`, `g2-energy.sh`, `g2-tid.sh`, `g2-final3.sh`; recs `g2-exp10{,b,c}-*`, `g2-exp1-*`, `g2-cohort10-*`; snapshots `gap2/{corpus-expensive10,g2exp1-output,g2exp10b-output,integ-retest-output-snapshot,evidence-backup}`.
- GAP 3: `fc-stage.sh` corregido + `fc-stage.sh.pre-gap3-bak`; `fc-lineage-replay.sh`; recs `integ-opt2-01..10-*`, `integ-retest-output2.sha256`, `lineage-replay.log`; `gap2/lineage-final.tsv`.
- `NO_SQX_RUNNING` verificado entre fases; única instancia SQX por VM en todo momento.

## Gotchas para el próximo verificador

- **La datación de ventanas por consola SQX produce mediciones de energía FALSAS** (éste es el hallazgo que revierte el FAIL del cert): "Task finished in 0.93 s" y jiffies "planos" son efecto del buffering; la ventana canónica es `TASK STARTED → TASK FINISHED` del `global_log` del proyecto, convertida de hora local (UTC−6 en Kronos) a epoch. Con esa ventana, el mismo cohort que el cert midió en 0,05 CPU-s quema 22,50 CPU-s.
- El sampler per-tid de `fc-run.sh` sub-muestrea en ventanas <20 s (detección de JVM intermitente): los group-jiffies @200 ms son la fuente autoritativa de energía; el per-tid sirve para forma (workers equilibrados en w8), no para sumas.
- `internal/` de las instalaciones de flota es symlink kor-owned: para experiments de exporter usar la instalación candidate-local escribible (`forge-perf-s01/sqx144-perf`, `Snippets.jar` en estado fleet) y restaurar el SHA encontrado al cerrar.
- `fc-prep.sh` pisa `rec/fc-retest-n<N>-input.sha256`: respaldar sellos históricos antes de re-usar el proyecto (hecho en `gap2/evidence-backup/`).
- El jar del exporter se actualiza con `jar uf` (mecanismo `snippet>jar`); verificar bytecode efectivo con entrada extraída `cmp` + marcador runtime en el log del exporter.
