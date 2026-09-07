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
  - la version de un componente es el id de la definicion
  - v10872 es un component_definition_id
  - parameters.version es el semver retirado
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

# RIO versiona un componente por el id de su component_definition

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Aprendizaje

- **La "versión" de un componente en RIO es el `component_definition.id`**, no un semver. El `v10872` que muestra el pipeline es literalmente eso: `DrawFlowCanvas.tsx:712` arma la etiqueta como `'v' + node.runningDefinitionId`, y el par que renderiza es `runningDefinitionId → pendingDefinitionId`.
- Editar un componente **crea una fila nueva** de `component_definition`; el slot la apunta como pendiente y `DeltaComputationServiceImpl.evaluateComponent` compara pendiente contra desplegada para decidir DEPLOY o SKIP. Por eso pendiente ≠ desplegada **sólo** cuando alguien editó: un redeploy sin cambios lleva el mismo id en los dos lados, y eso es información, no redundancia.
- `parameters["version"]` es el **semver retirado** de los componentes. Sobrevive en 76 de 2.193 deploys completados de `playmkrprod`, casi todos ClickHouse: es el único template que lo mete dentro de `parameters` (`ClickHouseAdapter.ts:63`). Flink, S3, GCP y los signals llevan `version` a nivel de nodo, no de parámetros; Flink usa `fury_version`. Cualquier diseño que dependa de `parameters["version"]` nace muerto en ~96% de los casos.
- El id es **monótono**, así que sirve como orden y no sólo como identidad: igual ⇒ redeploy de la misma configuración, mayor ⇒ avance, menor ⇒ rollback. En string se pierde y encima compara mal.

## Aplicabilidad

- **Cuándo cargarlo:** al diseñar cualquier contrato, endpoint o payload que tenga que identificar "qué versión de un componente" está desplegada o desplegándose, en playmaker, el frontend o un control plane.
- **Cuándo no cargarlo:** para el `version` que rutea transporte en `BatchDispatchServiceImpl:171`, que sí lee `parameters["version"]` y es otra cosa: la versión del template para elegir adapter.

## Entidades relacionadas

- [[rio-playmaker]], [[rio-frontend]], [[Crear Context]]

## Evidencia

%% Cita de fuente, NO prosa narrativa: link a sesión/log/archivo + una línea de qué la respalda. No re-parafrasear el aprendizaje ya destilado arriba (constitución: memorias compactas). %%

- Fuente: sesión `6a7cead6-c42f-4d85-8925-3eee82b5fbba` — `DrawFlowCanvas.tsx:712` y el censo de `parameters.version` sobre `playmkrprod` (76/2.193); confirmado en el dispatch real del 2026-09-03 con `component.version` y `last_deployed_version.version` numéricos.
