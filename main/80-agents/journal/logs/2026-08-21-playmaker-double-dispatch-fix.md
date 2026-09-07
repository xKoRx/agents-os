---
type: change_log
schema_version: 1
scope: session
created: "2026-08-21"
updated: "2026-08-21"
area: "[[Meli]]"
project: "[[Playmaker — Doble dispatch al avanzar batches]]"
application: "[[rio-playmaker]]"
entities:
  - "[[Playmaker — Doble dispatch al avanzar batches]]"
  - "[[rio-playmaker]]"
related:
  - "[[Auditoría independiente — Informe del doble dispatch]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: team
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-21-playmaker-double-dispatch-fix

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Estado posterior:** **DEPRECATED**. El equipo descartó este enfoque; no debe tratarse como solución vigente ni promoverse a staging/producción.
- **Archivo(s):**
  - `repo: melisource/fury_rio-playmaker` — `src/main/java/com/mercadolibre/rio/playmaker/service/pipeline/impl/OrchestrationServiceImpl.java`
  - `repo: melisource/fury_rio-playmaker` — `src/main/java/com/mercadolibre/rio/playmaker/repository/ComponentRunRepository.java`
  - `repo: melisource/fury_rio-playmaker` — `src/main/java/com/mercadolibre/rio/playmaker/repository/PipelineExecutionRepository.java`
  - `repo: melisource/fury_rio-playmaker` — enum, guard de operaciones, schemas de creación, Swagger y tests dirigidos

## Motivo

- La investigación pasó de diagnóstico a implementación autorizada del fix funcional para la carrera intra-execution en el proyecto [[Playmaker — Doble dispatch al avanzar batches]].

## Fuentes usadas

- Código fuente del repo en `feature/adhoc-double-dispatch`, comparación contra `develop` en `0524ce49ef34`, y el informe [[Auditoría independiente — Informe del doble dispatch]].

## Resolución aplicada

> **Nota de deprecación:** lo siguiente documenta únicamente el experimento realizado el 2026-08-21. La hipótesis vigente atribuye el problema a la concurrencia/multiplicidad de los listeners async que procesan `BatchCompletedEvent`; el estado persistente `DISPATCHING` no es la solución acordada.

- Se agregó `ComponentRunStatus.DISPATCHING` y un `UPDATE ... WHERE status=PENDING` atómico. `checkPrerequisites` toma `PipelineExecution` con lock pesimista, reclama cada run antes de construir `DeltaEntry` y el perdedor de la carrera retorna sin invocar `dispatchBatch`. `propagateFailure` usa el mismo lock y el guard de borrado considera `DISPATCHING` como operación en curso.
- El alcance deliberadamente no incluye la unicidad DB del active slot entre executions, la reparación de los deployments 6421/6422 ni el reconciliador post-commit; requieren preflight y rollout separados.
- El endpoint de history expone el nuevo valor. `ads-signals-frontend` lo normaliza hoy a `PENDING`, por lo que el runtime actual no debería romperse, pero la unión TypeScript/mapas de estado no declaran `DISPATCHING` y no mostrarán esa fase explícitamente.
- Hay una condición operativa importante: el enum JPA es `EnumType.STRING`; durante un rolling deploy un pod viejo puede fallar al leer una fila `DISPATCHING`. Se documentó en el PR #1064 que debe hacerse rollout compatible en dos fases o sin solapamiento de versiones.

## Validación

- `git diff --check` pasó. `./gradlew test` pasó completo con `BUILD SUCCESSFUL`. La validación dirigida posterior al endurecimiento pasó `DeploymentOrchestrationEnumsTest`, `OrchestrationServiceImplTest` y `DeploymentOrchestrationIntegrationTest`.
- Validación cruzada: `ads-signals-frontend` ejecutó `tests/unit/api/pipeline/pipeline.node.spec.ts` (99/99), incluyendo el normalizador que degrada estados desconocidos a `PENDING`; la suite emitió solo el warning preexistente de Haste module naming collision.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el commit de la rama `feature/adhoc-double-dispatch`; no hay cambios de DB de datos ni migración ejecutable nueva. Mantener fuera de este rollback la reparación manual del incidente y cualquier backstop global que se acuerde después.
