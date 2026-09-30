---
type: change_log
schema_version: 1
scope: session
created: "2026-09-30"
updated: "2026-09-30"
area: "[[Meli]]"
project: "[[Kafka — Ambiente local con servicios reales]]"
application: "[[rio-controlplane-kafka]]"
entities: ["[[Kafka — Ambiente local con servicios reales]]", "[[RIO]]"]
related: ["[[Ambientes locales RIO — Comparativa de implementaciones]]"]
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: "local"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Kafka — Investigación y proyecto de ambiente local real

## Cambio

- **Tipo:** created + updated.
- **Nuevas notas:** proyecto [[Kafka — Ambiente local con servicios reales]], recurso [[Ambientes locales RIO — Comparativa de implementaciones]] y fuente [[Repositorios RIO — Ambientes locales (2026-09-30)]].
- **Índice/bitácora:** se agregó la entrada correspondiente al Atlas de RIO y su ingesta de evidencia.

## Motivo

El owner pidió buscar implementaciones vigentes en todos los control planes y Playmaker, recomendar una solución para Kafka y crear un proyecto para iterarla.

## Fuentes usadas

- [[Repositorios RIO — Ambientes locales (2026-09-30)]].
- Solicitud del owner: servicios Kafka reales, comparación de precedentes RIO y recomendación explícita.

## Resolución aplicada

- Investigación finalizada antes de iniciar la iniciativa de cambio; comparación/provenance viven en la wiki y planificación de entrega en el proyecto.
- Se propone extender el stack Kafka/MySQL existente de Playmaker con el CP real, tres brokers, acciones/PEEK y KVS Fury sandbox sujeto a verificación.
- Diez bases externas actualizadas. Se usaron worktrees limpios para Kafka y Playmaker, preservando sus checkouts originales con trabajo funcional pendiente; las bases finales coinciden con las fuentes remotas examinadas. Se retiró el worktree temporal limpio de Kafka.
- Implementación y validación runtime quedan pendientes; no se declararon como realizadas.

## Validación

- Materialización desde templates contratados v1 para proyecto, recurso, source y change log.
- Lint estricto dirigido final: cinco notas versionadas, ERROR=0 y WARN=0. Graphify recuperó un único proyecto por título exacto y por alias `Kafka local real`. Las diez bases Git finales coincidieron con los commits registrados en la fuente. El refresco global informó deuda en otros paths, pero no bloqueó el índice derivado ni el gate dirigido.

## Compartibilidad

- **Scope:** local.
- **Redacción:** sin secretos, material privado del agente ni paths absolutos de máquina en los artefactos persistidos.

## Rollback

- Retirar las tres notas nuevas y la entrada agregada al catálogo; conservar el historial append-only y registrar una operación de reversión. Las actualizaciones de bases Git externas se conservaron como fast-forward y no requieren revertir código de producto.
