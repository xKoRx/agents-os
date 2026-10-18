---
type: agent_run
schema_version: 1
scope: session
created: "2026-10-18"
updated: "2026-10-18"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
related:
  - "[[2026-10-18-zcode-glm53-sqx144-cpu-utilization]]"
  - "[[2026-10-18-zcode-glm53-forge-030-release-e2e]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM 5.3 Flash (account:zai-individual-coding-plan/GLM-5.3-Flash)
model_source: system
task_type: performance_optimization
task_complexity: high
outcome: success
verification: production_evidence
evaluator: agent
user_rework: none
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-10-18-zcode-glm53-overview-perf-s01

## Trabajo

- **Objetivo:** mandato TOP one-shot — reducir el costo de `EchoForgeOverviewExporter` sin alterar resultados funcionales ni contratos durables de Forge; forensics de source, baseline con profiling, candidato en rama dedicada, paridad obligatoria y comparativa real. Sin E2E, sin release, sin merge, sin tocar SQX 142/144 de flota.
- **Alcance atribuible:** forensics del exporter (1831 líneas) contra la evidencia del diagnóstico CPU; construcción de un entorno de benchmark candidate-local en Kronos (copia de 144 sin `user/data` + 4 proyectos CustomAnalysis + corpus auténticos congelados con SHA); 20+ runs físicos con JFR (`settings=profile`) y `/usr/bin/time -v`; implementación del candidato en rama `perf/overview-s01` @ `cf8f522c` (pusheada); paridad exacta en 2 corpus; suite sim-junit 13/13; paquete de evidencia en el vault.

## Evidencia

- **Causa raíz medida (no asumida):** ~60–65% del CPU de tarea es compilación de regex por llamada (`String.replaceAll`→`Pattern.compile` dentro de `norm`/`pickValue`/`matchIndicator`/`matchPriceSeries`/`toEpochMs`/`toDouble`), ~8–10% reflexión re-derivada por trade (`collectScalarMap`), y el mapa escalar de cada trade se construía 3 veces (diagnósticos + monthly + debug). XML/indicadores/escritura/getters SQX resultaron menores (contra-hipótesis refutadas con datos).
- **Candidato (memoización pura):** patterns estáticos con las mismas expresiones; caché por clase de getters+fields en el mismo orden; una sola pasada de `collectScalarMap` por trade compartida; arrays de candidatos a constantes. Cero cambios de métricas, orden, contratos ni manejo de errores.
- **Paridad EXACTA:** corpus estándar 24/24 overview + 2976/2976 monthly con 0 diffs; corpus heavy 6/6 + 739/739 con 0 diffs (normalización limitada a timestamps del run y, en heavy, eco-de-config por diferencia documentada de props). Mismo orden, mismos StrategyRefs, 0/0 errores.
- **Rendimiento:** task 21 s → 8 s (corpus estándar, distribuciones no solapadas) y 9 s → 3,5 s (heavy) ≈ **2,6×**; MaxRSS −50% (5,7–6,2 → 2,5–2,8 GB); sonda empty demostró costo fijo de maquinaria ≈ 12 ms (el speedup es del exporter). JFR post: 0 `Pattern.compile` bajo métodos del exporter.
- **Hallazgo operativo (refina "snippet>jar" de la 21.ª sesión):** `Snippets.jar` es la autoridad de ejecución y `snippets.txt` es manifiesto hash-keyed — actualizar fuente+hash a la vez NO recompila y el jar stale corre silenciosamente (5 runs trampa lo demostraron con firma JFR); una clase nueva no se descubre por jar de user/libs. Deploy manual correcto: cambiar solo la fuente (hash stale dispara recompile) o actualizar fuente+hash+jar juntos (como el pipeline deployer).
- Entregables: `10-projects/Echo Forge — Operación Real V2/artifacts/ECHO-FORGE-OVERVIEW-PERF-S01/` (README con FINAL HANDOFF, SOURCE-FORENSICS, BASELINE-PROFILE, CANDIDATE-CHANGES, PARITY-REPORT, BENCHMARK-COMPARISON, DEPLOYMENT-MECHANISM).

## Desviación y rework

- Dos correcciones de protocolo durante la sesión, documentadas: (1) los primeros 5 "candidate runs" ejecutaron código baseline por la trampa del snippet (detectado por JFR; re-medicados como candreal); (2) el run baseline heavy corrió sin exporter.properties (defaults de config) — normalización justificada y documentada en el parity report. Sin mutaciones de flota, sin workers reiniciados, sin campañas afectadas; estado final de la copia restaurado a baseline. Sin rework del owner.

## Lecciones operativas

1. **Medir antes de optimizar paga:** la hipótesis "reflexión Java repetida" del mandato era secundaria; el 65% era compilación de regex por llamada — invisible sin JFR y con fix barato y de paridad trivial.
2. **La firma JFR es un canario de deploy:** verificar "0 Pattern.compile bajo frames del exporter" distingue código nuevo de stale mejor que cualquier timing (el timing se confunde con el ruido JIT de ±30%).
3. **En flota Forge, todo benchmark de comparabilidad exige corpus pristine + SHA antes de cada run:** la tarea CustomAnalysis re-serializa el databank de entrada (24/24 SHA cambian por run).
4. **El ruido JIT de task (17–31 s para el mismo código) exige n≥2 por celda y comparación por distribuciones**, no por runs individuales; la variación observada de primer vs segundo run fue de ~33%.
