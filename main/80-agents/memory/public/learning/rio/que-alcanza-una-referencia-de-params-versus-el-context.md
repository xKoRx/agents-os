---
type: learning
schema_version: 1
scope: application
created: "2026-09-03"
updated: "2026-09-03"
area: "[[Meli]]"
project: "[[Crear Context]]"
application: "[[rio-playmaker]]"
entities:
  - "[[rio-playmaker]]"
related:
  - "[[Crear Context]]"
  - "[[signals-context-flow]]"
aliases:
  - params resuelve por nombre, el context por vecindad
  - hasta donde llega el context comparado con params
  - solo un componente imported viaja con datos
confidence: high
source_session: 6a7cead6-c42f-4d85-8925-3eee82b5fbba
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/application
  - tech/rio
---

# Qué alcanza una referencia ${} de params, y qué alcanza el Context

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Aprendizaje

- Un `${dp.componente[env].propiedad}` en `params` resuelve así (`ParameterParseServiceImpl.getPropertyValue`): data product **por nombre** sin exigir importación ni relación → componente **por nombre dentro de ese DP** → `resolveToSourceComponent` salta al original si es copia importada → environment por nombre → `getReferencedService` exige **`status = 'running'`** → lee `service._values`.
- El **Context** cubre lo mismo a nivel de dato, porque publica `service._values` **completo** como `outputs` de cada vecino y resuelve sus `inputs` con el mismo `ParameterResolutionService`. Lo que difiere es **el alcance**: sólo vecinos con relación activa, sólo el propio data product o el original de una copia importada, y sólo el environment del deploy.
- **Decisión vigente:** sólo un componente **imported** viaja con sus datos. Una referencia que nombra otro data product sin importación viaja con identidad y mapas vacíos. Eso es lo que ya hace `ComponentContextService.resolveSlot` — no requirió cambio de código.
- **Acoplamiento a tener presente:** cuando un componente falla, su servicio queda en `failed` (`DeploymentAttemptFactory.markFailed`), y entonces cualquier vecino cuyos parámetros lo referencien **pierde sus valores en el Context** — la resolución tira `NotFoundException` y `safelyBuildRelatedComponent` degrada a mapas vacíos. El vecino puede estar perfectamente desplegado.

## Aplicabilidad

- **Cuándo cargarlo:** al decidir si el Context alcanza para que un control plane provisione sin `${}`, o al diagnosticar un vecino que llegó con `inputs`/`outputs` vacíos.
- **Cuándo no cargarlo:** para decidir cobertura contando filas de `playmkrtst`: es una base de testing con data mala, duplicada y de legacy, y no sirve como evidencia de un contrato.

## Entidades relacionadas

- [[rio-playmaker]], [[Crear Context]], [[Adopción de Context en Control Planes]]

## Evidencia

%% Cita de fuente, NO prosa narrativa: link a sesión/log/archivo + una línea de qué la respalda. No re-parafrasear el aprendizaje ya destilado arriba (constitución: memorias compactas). %%

- Fuente: sesión `6a7cead6-c42f-4d85-8925-3eee82b5fbba` — lectura de `ParameterParseServiceImpl` y `ComponentContextService`; el vaciado del vecino se observó en el dispatch del 2026-09-03 15:32 tras fallar el deploy de los topics.
