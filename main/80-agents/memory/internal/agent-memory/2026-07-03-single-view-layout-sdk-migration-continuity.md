---
type: agent_memory
scope: internal
created: 2026-07-03
updated: 2026-09-09
index_priority: never
indexable: false
memory_state: archived
load_policy: manual
tags:
  - agent/internal
  - project/refactor-polycard
---

# Continuidad — Single View Layout SDK Migration

**Para el próximo agente que tome este curro.**

Proyecto de agente ejecutable: `[[Single View Layout — Migración al Polycard SDK]]` (bajo `[[Refactor Polycard]]`). Esa nota es el planificador único y trae TODO: tareas A1-A6 (SDK) y B1-B7 (search), código a escribir, patrones de test, decisiones y riesgos. Empezá leyéndola, no reinvestigues.

Señales que me costó levantar y no quiero que se pierdan:

- El consumo en `SearchDecoratorRegistryV1` (~línea 257) re-envuelve el decider con `webCbtAfterShipping` justo después. **No romper ese encadenamiento** al migrar — es el bug fácil de introducir.
- El `RequestContext` del SDK **no** expone vertical (solo device/displayMode). Por eso no se puede hacer "if vertical==MOTORS" dentro del decider del SDK. El argumento que justifica mover al SDK es que **Single == VIS** (solo MOT/RE lo usan).
- Ambos usos en search están **gateados por experimento** (`singleViewMotorsExperimentEnabled` / `isEnabledPolycardSingleMotors`). Opción B mantiene ese gate; Opción A (bakear en default) lo perdería. Elegí B.
- Dependencia dura: search (bloque B) no compila contra la nueva API hasta que el SDK publique versión (tarea A5). Usar SNAPSHOT o publicar primero.
- Tests de layout del SDK ya existen y son buen molde: `SingleNativeAndroidLayoutOrderTest` (parametrizado con `BaseLayoutOrderTest`). Search NO tenía test dedicado del factory.

Estado al cerrar: solo ramas creadas + doc. Cero código escrito. Repos parqueados en `feature/single-view-layout-sdk-migration` (salieron de master/develop frescos), fuera de sus features previas (`feature/discount-price-motors`, `feature/bajo-de-precio-motors`).
