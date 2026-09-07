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
  - el context sin discovery es params relayado
confidence: high
source_session: 9c1f9d46-34d9-4921-809f-b823fb3343f1
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/learning
  - scope/application
---

# El Context de Playmaker está estructurado sólo en el primer nivel

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Aprendizaje

- El `ComponentContext` aporta estructura **sólo en el primer nivel** —`data_product` / `component` / `sources` / `destinations`—. Adentro de cada vecino, `inputs` es el `params` **completo y sin curar** de ese vecino. La promesa de "la misma data que `params`, pero estructurada y con sentido" se cumple a medias hasta que **discovery** defina qué claves necesita cada tipo de componente.
- **La data que el Context viene a reemplazar viaja adentro del propio Context.** El `destinations` que compone el frontend para un `catalog-signal` llega como string JSON dentro de `inputs`, con brokers y `destination_key`, al lado de la versión que reportó el CP en `outputs`. La misma información puede viajar hasta tres veces en un mensaje.
- **`inputs` y `outputs` pueden traer la misma llave con valores distintos, y `outputs` es la autoridad.** El caso ejemplar es `topic_name`: `inputs` lleva el nombre lógico del componente y `outputs` el nombre físico desplegado. Medido en `playmkrprod`: 952 coincidencias de llave entre los dos mapas, 557 eco puro y **395 con valor distinto**, 361 de ellas `topic_name` de `aws-msk-topic`. Un consumidor que lea `topic_name` de `inputs` se conecta a un tópico que no existe. Por eso no se resta a `outputs` lo que ya está en `inputs`.
- Los valores no escalares viajan como JSON dentro de un string, por el `Map<String,String>` del contrato. El caso que más pesa: `inputs.files` de un Flink lleva **el SQL del job gzippeado en base64**, difundido en cada deploy de un vecino.
- Lo que sí quedó probado en vivo: el unwrap del envelope funciona. `FlinkAppOutputBuilder` emite `{type, value, sensitive}` y los outputs llegan planos al consumidor.

## Aplicabilidad

- **Cuándo cargarlo:** al discutir si el Context ya reemplaza a las `properties` del front; al dimensionar el payload del trigger; al decidir el alcance de discovery; al interpretar la métrica de supresión.
- **Cuándo no cargarlo:** en trabajo de Playmaker ajeno al pipeline de deployment.

## Entidades relacionadas

- [[rio-playmaker]], [[Crear Context]]

## Evidencia

- Dispatch real del 2026-09-03 11:11 con la versión de test `0.0.2-component-context-test`, que loguea el `DeploymentTriggerMessage` completo antes de publicar. Componente `topic-1` (`aws-msk-topic`, id 8211) en el data product `jarita-test`, ambiente `staging`; source `jarita-signal-test` (`catalog-signal`), destination `flink-sql`.
- `params` del componente desplegado: `prefix_production`, `retention_ms`, `partitions`, `name`, `topic_name`, `description`, `prefix_staging`, `replication_factor`. **Sin clave `version`.**
- `context.component` llegó **sin** `last_deployed_version`, porque la derivación exigía una clave `version` dentro de los parámetros desplegados y ningún tipo de componente la declara. La causa quedó cerrada: la versión de un componente es el id de su `component_definition` — ver [[rio-versiona-un-componente-por-el-id-de-su-component-definition]].
- `sources[0].inputs` trajo `initiative`, `traffic_behavior`, `payload_size`, `display_name`, `identifier`, `authorized_applications` y `criticality`: metadata de catálogo que no le sirve a ningún CP para provisionar.

## Change log

- 2026-09-03 — Se retira el alias *last_deployed_version nunca se puebla* y se acota la evidencia de ese campo: la ausencia no era del contrato sino de la fuente que leía la derivación. El resto del aprendizaje —el Context estructurado sólo en el primer nivel, `inputs` como `params` sin curar del vecino— sigue vigente.
