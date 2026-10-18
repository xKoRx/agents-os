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
---

# BASELINE-PROFILE — protocolo de medición y atribución física

## Entorno de benchmark (aislado, sin tocar flota)

- Host: `sqx-kronos` (76 vCPU, ocioso, load 0,00 durante toda la sesión), sesión SSH como `echo-dev` (MCP aranea-ssh, perfil sqx-kronos).
- Copia candidate-local del runtime operacional (patrón G7 certificado, contrato §0): `/home/echo-dev/forge-perf-s01/sqx144-perf/` = copia de `/home/kor/sqx/144` (SQX 144.2953, licencia verifica por hardware ID C0CCF0856B2C, "Using: 72 cores, core usage configuration '100%'") EXCLUYENDO `user/data` salvo el catálogo mínimo (data.db + data_*.h2.db + versiones, 43 MB — History/ 5,9 GB de precios no es necesario para CustomAnalysis sobre resultados existentes) y excluyendo `user/projects` y `user/log`. La instalación de flota `/home/kor/sqx/144` NO fue modificada (solo lectura).
- Ejecución idéntica a la operacional: `./sqcli -project action=start name=<proyecto>` desde el root de la copia; JVM Zulu 25.0.2 del propio runtime; `sqcli.config` de la copia (contrato `-Xms4g -XX:+UseParallelGC`, igual que flota) + opción JFR `StartFlightRecording=...settings=profile,dumponexit` añadida solo en la copia.
- Métricas: duración de tarea del project log SQX (`TASK FINISHED ... in N s`, granularidad 1 s), wall clock y MaxRSS de `/usr/bin/time -v`, atribución por JFR (agregación awk de `jdk.ExecutionSample`, ventana de tarea por timestamp local 08:44:04–08:44:33 para el run de referencia).

## Corpus auténticos congelados

1. **Corpus estándar**: 24 estrategias del databank `Results` de la operación real en Kronos (`/home/kor/sqx/144/user/projects/custom/databanks/Results/*.sqx`, NDX H1, 120–240 KB c/u, 4,9 MB total, 1.049–2.439 trades por estrategia ≈ 48.000 trades). Pristine stash + `CORPUS-SHA256SUMS.txt`; restauración + verificación SHA24/24 ANTES de cada run (la tarea CustomAnalysis re-serializa el databank de entrada: demostrado, los SHA cambian tras cada run — de ahí el protocolo restore-per-run).
2. **Corpus heavy**: 6 estrategias builder reales de campañas previas (`NDX_W3_80oosSPP_V1_Strategy *.sqx`, 2,6–5,4 MB c/u, ~16.000 trades, XML ~17 KB), mismas convenciones de freeze.
3. **Sonda empty**: proyecto idéntico con databank vacío (0 estrategias) para acotar el costo fijo de maquinaria.

## Baseline físico (jar desplegado 0.3.1, SHA `3b0063e4…`, ejecutado vía Snippets.jar — ver DEPLOYMENT-MECHANISM.md)

- Corpus estándar, 9 puntos del código baseline: **{28, 21, 31, 18, 21, 21, 27, 17, 23} s** — mediana 21 s, media 22,9 s, rango 17–31 s (ruido JIT/FS ±30%; por eso n≥2 por celda y comparación por distribuciones no solapadas). `/usr/bin/time` wall 44–58 s con ~21 s de boot fijo JVM (sonda empty: TASK 12–13 ms, wall 20,8 s → la maquinaria de tarea sin estrategias es despreciable; el tiempo de tarea es carga del databank + trabajo del exporter + re-serialización).
- Corpus heavy: 9 y 9 s.
- MaxRSS corpus estándar 5,68–6,17 GB; heavy 2,91–3,05 GB; empty 1,37 GB.
- Atribución JFR (run1, 2.986 samples totales): task window dominada por regex/`String.replaceAll`→`Pattern.compile` (~60–65%), `norm` inclusive 475, `pickValue` 283, `collectScalarMap` 175, `monthlyFromTrades` 158, `buildStrategyRow` 310.

## Archivos de evidencia (Kronos, candidate-local)

`/home/echo-dev/forge-perf-s01/`: `rec/*.jfr` (9 recordings), `rec/*-console.log`, `rec/*-time.txt` (Elapsed/MaxRSS por run), `corpus-pristine/` + `corpus-heavy/` con SHA256SUMS, `sqx144-perf/user/projects/perfs01{,-noop,-heavy,-empty}/log/global_log_*.log` (TASK FINISHED por run), `bench/` (scripts + configs de proyecto), `analyze-jfr.sh`, `parity.py`, backups `bench/Snippets.jar.bak-perf-s01` (baseline) y `bench/Snippets.jar.candidate-perf-s01` (candidato).
