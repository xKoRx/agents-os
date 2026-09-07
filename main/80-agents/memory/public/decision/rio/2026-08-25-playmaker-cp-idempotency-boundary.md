---
type: decision
schema_version: 1
scope: project
created: "2026-08-25"
updated: "2026-08-25"
area: "[[Meli]]"
project: "[[Playmaker — Doble dispatch al avanzar batches]]"
application: "[[rio-playmaker]]"
entities: []
related:
  - "[[playmaker-deployment-idempotency-and-cp-kvs]]"
  - "[[rio-controlplane-kafka]]"
  - "[[rio-controlplane-flink]]"
  - "[[rio-controlplane-clickhouse]]"
  - "[[rio-controlplane-fury]]"
aliases: []
confidence: verified
source_session:
load_policy: when_application_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - app/rio-playmaker
  - topic/idempotency
---

# Límite de la idempotencia de los Control Planes frente a Playmaker

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- El incidente de Playmaker produjo dos deployments activos para el mismo service y el mismo avance lógico, con IDs distintos (`6421` y `6422`), además de ejecuciones/correlation IDs distintos.
- Kafka y Flink tienen un guard KVS indexado por `deployment:<deployment_id>`; por diseño, `6421` y `6422` son dos claves distintas. ClickHouse no tiene hoy un claim distribuido cableado al flujo principal; Fury converge por natural key y `specHash` dentro de su dominio.
- Por lo tanto, la deduplicación del CP es un backstop downstream para redelivery del mismo comando, no una garantía de unicidad del avance lógico creado por Playmaker.

## Decisión

- Mantener el guard de idempotencia del CP por `deployment_id`: claim create-only con versión inicial `0`, resolución de conflictos mediante estado KVS, TTL, takeover CAS de claims stale y finalización terminal con CAS antes de publicar el resultado.
- No modificar CPs, schema, entidades persistentes, estados públicos ni contratos como parte del hotfix.
- Resolver la carrera intra-execution en `BatchCompletedEventListener` mediante mutex KVS create-only por `pipeline_execution_id + next_batch_order`; el perdedor espera con exponential backoff fuera de DB, abre una transacción fresca al adquirir y reconoce `already_materialized` mediante deployments existentes del mismo group.
- Tomar la existencia del deployment como boundary del parche: prueba que el intento fue materializado, no que BigQueue confirmó el publish.
- Diseñar como segundo track un refactor durable con tópico externo particionado por execution, publicación DB→topic recuperable, consumo at-least-once e identidad/lógica atómica y consistente; ese diseño debe resolver también el invariante cross-execution por service.
- No usar `service_id` como clave de deduplicación del CP: bloquearía redeploys legítimos y mezclaría idempotencia de comando con exclusión mutua de recurso.
- Deprecar por completo `ComponentRun.DISPATCHING`, el CAS `PENDING → DISPATCHING`, sus migraciones, compatibilidad y rollout; la implementación experimental no debe promoverse.

## Rationale

- El lock debe vivir en el listener que ejecuta el check-then-act. Serializar el result consumer no cubre dos eventos Spring `AFTER_COMMIT + @Async` que compiten después.
- Esperar el mutex evita ejecutar dos secciones críticas en paralelo, pero el perdedor sólo se vuelve idempotente si relee DB después del ganador y reconoce la materialización por `(deployment_group, component/service)`; `ComponentRun` permanece `PENDING` y no sirve como evidencia.
- La espera debe ocurrir antes de abrir la transacción DB para no retener conexiones ni fijar una vista anterior al commit del ganador.
- El patrón KVS robusto usa `save` condicional, 409 como carrera esperable, lectura del estado existente, descarte de terminal/reintento reciente, takeover CAS si el claim está stale y TTL como backstop. No es exactly-once físico ni reemplaza fencing de efectos externos.
- El hotfix es intencionalmente acotado: evita la interleaving observada sin cambiar el happy path, pero no cubre restart, DB→publish, cross-execution ni unicidad global por service.

## Consecuencias

- El hotfix debe probar dos eventos de runs distintos del mismo batch, un solo `dispatchBatch`, espera/backoff, relectura fresca, outcomes `all/none/partial`, KVS temporalmente indisponible y release owner-safe.
- La operación del parche debe monitorear tiempo/attempts de lock, conflicts, KVS unavailable, TTL/release y outcomes `dispatched`, `already_materialized` y `partial_conflict`.
- El refactor durable debe probar restart/replay, dual-write DB→topic, retries at-least-once, cross-execution y máximo un deployment vigente por service.
- La documentación técnica aplicable queda en [[playmaker-deployment-idempotency-and-cp-kvs]] y en [[Playmaker — Doble dispatch al avanzar batches]].

## Alternativas descartadas

- Agregar o promover `DISPATCHING`: cambia lifecycle/contratos y abre recuperación adicional en el nivel incorrecto.
- Poner el lock sólo en `DeploymentResultConsumerServiceImpl`: serializa el handler, pero no los listeners internos publicados después del commit.
- Retornar `409` desde el consumer para provocar retry: no asegura semántica de retry de BigQueue y no cubre la carrera async posterior.
- Usar sólo un lock sin chequeo `already_materialized`: después de esperar, el segundo listener volvería a ver runs `PENDING` y podría despachar nuevamente.
- Hacer la espera dentro de una transacción DB: retiene conexiones y puede observar una vista anterior al ganador.
- Cambiar la clave del CP a `service_id`: sacrifica redeploys legítimos y no expresa la identidad del comando.
