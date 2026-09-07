---
type: known_error
schema_version: 1
scope: application
created: "2026-08-25"
updated: "2026-08-25"
area: "[[Meli]]"
project: "[[Crear Context]]"
application: "[[rio-playmaker]]"
entities:
  - "[[rio-playmaker]]"
related:
  - "[[Crear Context - Code Review Remediation]]"
aliases:
  - environment stub playmaker
  - EnvironmentModel sin name ni type
  - createSingle environment stub
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - area/meli
  - application/rio-playmaker
---

# El `EnvironmentModel` del dispatch v1 llega con sólo el `id`

## Síntoma

Cualquier lógica del camino de dispatch que lea `group.getEnvironment().getName()` o `.getType()` obtiene `null` — no una excepción, un null silencioso. Por el camino del pipeline nuevo el mismo código funciona, así que el bug aparece sólo en una de las dos rutas y es fácil atribuirlo a datos malos en vez de al objeto.

## Causa

`DeploymentGroupServiceImpl.createSingle` construye el `EnvironmentModel` a mano como referencia JPA y le setea **únicamente el id** antes de guardar el grupo. Dentro del mismo persistence context, `group.getEnvironment()` devuelve ese mismo stub, no una entidad cargada: `name`, `type` y `criticality` quedan en `null`. El camino de `OrchestrationServiceImpl` relee el grupo desde la base, así que ahí sí llega la entidad completa.

## Impacto

Cualquier decisión tomada sobre el nombre o el tipo del ambiente destino degrada en silencio por el camino v1. Confirmado en dos lugares: la resolución de ambiente equivalente del Component Context —que resolvía a "no hay ambiente" y suprimía outputs cross-data-product— y `DispatchRequest.environmentName`, que viaja `null` por ese camino (preexistente, sin corregir).

## Detección

Comparar las dos rutas: si el comportamiento difiere entre un deploy despachado por `OrchestrationServiceImpl` y uno por `createSingle`, y el dato en cuestión es un campo de `EnvironmentModel` distinto del `id`, es esto.

## Mitigación

No confiar en el `EnvironmentModel` que entrega el caller para nada que no sea el `id`. Releer la fila (`environmentRepository.findById(environmentId)`) cuando se necesite el `type` o el `name`. Es lo que hace `ComponentContextServiceImpl.targetEnvironmentType`, con el comentario que explica por qué.

## Evidencia

- `DeploymentGroupServiceImpl.createSingle` — construcción del stub, `envModel.setId(environmentId)` como único setter.
- `DeploymentGroupModel.environment` — `@JoinColumn(nullable = false, updatable = false)`; la columna no admite null, pero eso no dice nada del objeto en memoria.
- `EnvironmentMapper.toModel` — para las filas creadas por la API, `name` es `normalize(type).toLowerCase()` y `type` el display name; los dos existen en base, sólo faltan en el stub.
