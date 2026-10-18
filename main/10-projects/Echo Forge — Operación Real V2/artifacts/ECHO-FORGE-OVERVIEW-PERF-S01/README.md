---
type: evidence_pack
schema_version: 1
status: final
created: "2026-10-18"
updated: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[xKoRx/symphony]]"
baseline: "xKoRx/symphony 492a271e (release 0.3.1, jar desplegado SHA 3b0063e43735f945)"
candidate: "xKoRx/symphony perf/overview-s01 @ cf8f522cc643efd20cb80c7cc6dafae59bad07d1"
verdict: "OVERVIEW_PERF_CANDIDATE_READY"
related:
  - "[[Echo Forge — Operación Real V2]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
  - "[[2026-10-18-zcode-glm53-overview-perf-s01]]"
tags:
  - kind/evidence-pack
  - area/echo
  - tech/performance
---

# ECHO-FORGE-OVERVIEW-PERF-S01 — Overview Exporter: source forensics + candidato de optimización con paridad demostrada

## FINAL HANDOFF

STATUS: `OVERVIEW_PERF_CANDIDATE_READY`

SOURCE_SHA: `492a271e84f1faa1d4050b7ab35255863b2992e5` (baseline) → `cf8f522cc643efd20cb80c7cc6dafae59bad07d1` (candidato)

BRANCH: `perf/overview-s01` (pulsada a origin, NO fusionada a master)

ROOT_CAUSE_FUNCTIONS: `norm()` / `pickValue()` (regex `Pattern.compile` por llamada vía `replaceAll` en cada clave de cada mapa escalar); `collectScalarMap()` (re-deriva metadata de reflexión y `setAccessible` por trade); triple pasada de `collectScalarMap` por trade en `buildStrategyRow` (diagnósticos + `monthlyFromTrades` + debug). XML parse, indicadores, escritura NDJSON y APIs SQX (`scanForTrades`, `mainResult`, stats) resultaron menores en este perfil.

BASELINE_SECONDS: 21 (mediana task, n=9, rango 17–31) en corpus estándar (24 estrategias NDX); 9 (n=2) en corpus heavy (6 estrategias NDX_W3_80oosSPP_V1 2,6–5,4 MB)

CANDIDATE_SECONDS: 8 (mediana task, n=3, rango 7–9) corpus estándar; 3,5 (n=2) corpus heavy

SPEEDUP: ~2,6× task en ambos corpus (distribuciones no solapadas)

CPU_BEFORE: ~1 core (secuencial por diseño del API CustomAnalysis; sin cambio — el candidato no paraleliza)

CPU_AFTER: ~1 core con ~60–65% menos trabajo de CPU de tarea (JFR: 0 `Pattern.compile` bajo métodos del exporter vs ~65% del CPU de tarea en regex/compilación antes)

MEMORY_BEFORE: MaxRSS 5,6–6,2 GB por run (corpus estándar); 2,9–3,1 GB (heavy)

MEMORY_AFTER: MaxRSS 2,5–2,8 GB por run (corpus estándar, −50%); 1,9–2,1 GB (heavy, −33%)

PARITY: EXACTA — corpus estándar overview.ndjson 24/24 + monthly.ndjson 2976/2976 con 0 diffs (normalizando `job_id`/`exported_at`); corpus heavy 6/6 + 739/739 con 0 diffs (normalizando además eco-de-config `wave_key`/`instrument`/`timeframe`/`direction` por diferencia documentada de props del run baseline heavy). Mismo orden de registros, mismos StrategyRefs, mismos errores (0/0), mismos conteos.

TESTS: sim-junit 13/13 PASS (build.sh simulator + ConsoleLauncher sobre el source modificado); paridad física arriba.

COMMITS: `cf8f522c` (único commit de la rama sobre 492a271e)

PRODUCT_DEPLOYED: NO

FORGE_0_3_1_UNCHANGED: YES (flota intacta; todos los runs en copia candidate-local `/home/echo-dev/forge-perf-s01/sqx144-perf` en Kronos; estado final restaurado a baseline: Snippets.jar y user/libs con SHA de 0.3.1)

AGENTS_OS_SESSION_CLOSED: YES (project note 23.ª sesión + agent-run + change_log + learning + sync)

NEXT: Return to GPT-6 Primary Manager for review and integration decision. La integración por el pipeline release estándar reconstruye Snippets.jar (mecanismo snippet>jar, ver DEPLOYMENT-MECHANISM.md); no se requiere acción manual de flota.

## Contenido del paquete

- `SOURCE-FORENSICS.md` — anatomía del costo por función con evidencia JFR.
- `BASELINE-PROFILE.md` — protocolo de medición, corpus, entorno y atribución baseline.
- `CANDIDATE-CHANGES.md` — delta exacto del candidato y por qué preserva la semántica.
- `PARITY-REPORT.md` — protocolo y resultados de paridad por corpus.
- `BENCHMARK-COMPARISON.md` — matriz completa de runs, tablas y limitaciones (no extrapolar).
- `DEPLOYMENT-MECHANISM.md` — hallazgo operativo snippet>jar y cache hash-keyed de snippets.txt.
