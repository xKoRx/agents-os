---
type: evidence_doc
schema_version: 1
status: final
created: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[xKoRx/symphony]]"
tags:
  - kind/evidence
  - area/echo
  - tech/performance
---

# CANDIDATE-CHANGES — delta exacto y garantías de semántica

Rama `perf/overview-s01` @ `cf8f522cc643efd20cb80c7cc6dafae59bad07d1` (padre `492a271e` = release 0.3.1). Un solo archivo tocado: `sqx/exporter-plugin/src/SQ/CustomAnalysis/EchoForgeOverviewExporter.java` (+140/−78 líneas). Cero cambios en: métricas, fórmulas, clasificación, selección, orden de claves/registros, contratos de `overview.ndjson`/`monthly.ndjson`/manifest, manejo de errores, schema_version/plugin_version, y demás exporters.

## Cambios (memoización pura, sin alterar semántica)

1. **Patterns precompilados (static final):** `P_NORM_NON_ALNUM`, `P_NUM_DOT_MINUS`, `P_NUM_COMMA_DOT_MINUS`, `P_NUM_MINUS` — mismas expresiones que los `replaceAll` inline de `norm`, `matchIndicator`, `matchPriceSeries`, `toEpochMs`, `toDouble`, compiladas una vez. `Pattern` es thread-safe; los `Matcher` siguen siendo locales.
2. **Cache de reflexión por clase (ConcurrentHashMap):** `GETTERS_CACHE` (getters que pasan `getParameterCount()==0` + `isGetterLike` + `!skipHeavyMethod`, en el MISMO orden de `getMethods()`) y `FIELDS_CACHE` (fields no-static por jerarquía con `setAccessible(true)` ejecutado una vez; los que fallan quedan fuera igual que antes). `collectScalarMap` itera los arrays cacheados — mismo contenido, mismo orden, mismos `put` (mn + derivados get/is).
3. **Una sola pasada de `collectScalarMap` por trade:** `buildStrategyRow` construye `tradeMaps` una vez y la comparte entre el bucle de diagnósticos, `monthlyFromTrades(tradeMaps)` (firma privada internar cambiada) y el export debug opcional. Determinista por objeto → valores idénticos.
4. **Arrays de candidatos a constantes:** los `new String[]{...}` por trade (entry/exit price, profit, close/open time, dirección) son ahora `static final` con los MISMOS literales en el MISMO orden (`CAND_*`).

## Por qué es paridad por construcción

No se alteró ningún algoritmo de decisión: mismos filtros, mismos órdenes de iteración, misma precedencia de `pickValue` (exacta por candidato→fuzzy), mismas claves derivadas, mismos `put` en el mismo orden relativo. Los caches solo eliminan trabajo repetido cuyo resultado es determinista. Evidencia física de la semi-ingenuidad del riesgo y su control: PARITY-REPORT.md con 0 diffs en 2 corpus independientes.

## Lo que NO se hizo (explícito)

- Sin paralelismo (el task exige demostrar concurrencia segura de `ResultsGroup`/`Result`/APIs SQX antes; queda como S02 potencial, ver NEXT del README).
- Sin tocar `findTrades`/`scanForTrades`/`getStrategyXmlSafely`/`parseIndicators` (no dominantes en el perfil medido; tocarlos aumenta riesgo de paridad sin ganancia demostrada).
- Sin cambiar versiones embebidas en las filas (habría roto paridad de bytes).
- Sin pool de threads, scheduler nuevo, ni cambios de config de flota.

## Regresión

- `build.sh` simulator + JUnit ConsoleLauncher: **13/13 PASS** con el source modificado (los tests cubren los otros exporters; el Overview no tenía tests de simulator — su verificación es la paridad física).
- `scripts/verify_build.sh` no aplica tal cual: assertion de hashes G2-firmados del release; un jar candidato produce SHA distintos by design.
