---
type: change_log
schema_version: 1
scope: session
created: "2026-08-26"
updated: "2026-08-26"
area:
project: "[[Playmaker — Doble dispatch al avanzar batches]]"
application: "[[rio-playmaker]]"
entities:
  - "[[Playmaker — Doble dispatch al avanzar batches]]"
  - "[[rio-playmaker]]"
related:
  - "[[Descripción PR — rio-playmaker — Hotfix doble dispatch]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Playmaker — Regression test del doble dispatch

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - `src/test/java/com/mercadolibre/rio/playmaker/unit/service/BatchCompletedEventListenerConcurrencyTest.java`
  - `10-projects/Meli/Playmaker — Doble dispatch al avanzar batches/Descripción PR — rio-playmaker — Hotfix doble dispatch.md`
  - `10-projects/Meli/Playmaker — Doble dispatch al avanzar batches/Playmaker — Doble dispatch al avanzar batches.md`

## Motivo

- Convertir la condición de carrera observada en una reproducción determinística y revisable dentro del mismo PR del fix.

## Fuentes usadas

- Implementación del listener, mutex y guard `already_materialized` en la rama `feature/serialize-batch-completed-listener`.
- Resultado red/green del test focal y suite Gradle completa.

## Resolución aplicada

- El test conecta listener y orquestación reales con dependencias in-memory/mockeadas, usa dos threads y latches sin sleeps y fuerza el snapshot vacío compartido.
- Se dejaron dos escenarios explícitos sobre el mismo fixture: sin serialización se observan dos dispatches y falla la invariancia de uno solo; con el lock, el contendiente reintenta después de la materialización y se mantiene un único dispatch.
- La descripción del PR explica por qué el escenario pre-fix captura la falla con `assertThrows`: documenta el resultado rojo `expected: <1> but was: <2>` sin romper intencionalmente CI.

## Validación

- Los dos escenarios del test focal pasaron una ejecución inicial y cinco repeticiones consecutivas sin flakiness.
- La última suite completa, ejecutada antes de incorporar el segundo escenario explícito, terminó con 3216 tests, 0 fallas y 2 skipped; no se atribuye al commit final.
- `git diff --check` quedó limpio y el cambio final del regression test fue pusheado en `d08a9a2c5` a la rama del PR.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** no se agregaron secretos ni datos de producción.

## Rollback

- Eliminar el test y revertir las dos notas si la estrategia de lock se abandona antes de mergear el PR.
