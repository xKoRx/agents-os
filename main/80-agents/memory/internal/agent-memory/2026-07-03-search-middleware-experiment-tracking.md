---
type: agent_memory
scope: internal
created: 2026-07-03
updated: 2026-07-03
confidence: observed
load_policy: on_demand
tags:
  - agent/internal
  - repo/search-middleware
  - topic/experiments
---

# Search Middleware Experiment Tracking

En `search-middleware`, los experimentos nuevos o migrados deben preferir
`TrackedExperimentTask`, que escribe `experimentData` mediante
`ExperimentsTracker`. `ExperimentsDataTask` esta deprecado como agregador legacy
y su comentario indica no agregar nuevos experimentos ahi.

Caso observado: `PriceDropMotorsExperimentTask` extendia `Task` plano y resolvia
`PriceDropExperimentModel`, pero no emitia exposicion porque nadie recolectaba
su `experimentData`. La solucion alineada al repo es migrarlo a
`TrackedExperimentTask<PriceDropExperimentModel>` con `isExperimentApplicable()`
gateado por `PolycardSingleMotorsExperimentTask`.

Pitfall posterior: al migrar a `TrackedExperimentTask`, el task y sus tests deben
usar `meli.rx.Observable` / `meli.rx.observers.TestSubscriber`, no `rx.*`. Si se
usa `rx.Observable`, `./gradlew clean compileJava` falla con errores de override
porque `SearchExperimentTask` declara `meli.rx.Observable`. Un `compileJava`
incremental puede quedar `UP-TO-DATE` y esconder el problema; validar con
`clean compileJava` cuando se cambie la jerarquia de tasks.
