---
type: change_log
schema_version: 1
scope: session
created: "2026-10-07"
updated: "2026-10-07"
area: "[[Meli]]"
project: "[[Kafka — Ambiente local con servicios reales]]"
application: "[[rio-controlplane-kafka]]"
entities: []
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-10-07-kafka-small-local-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Kafka — entrega local pequeña

## Cambio

Actualización del estado y la tabla de entrega de [[Kafka — Ambiente local con servicios reales]] con una extracción nueva, separada del desarrollo congelado. Se conserva su historia; las tareas vigentes corresponden sólo al objetivo de cuatro flujos.

## Motivo y fuente

Encargo explícito del owner del 07/10; diff `feature/kafka-local-small@eb16f5f`, dos corridas físicas y reproducción independiente desde clon limpio.

## Validación

9/0/0/0 en ambas corridas finales y replay independiente; 691 tests existentes y 6 controles KVS PASS. Packaging productivo sin código local y cleanup físico PASS. Original/congelado preservados. Zord formal bloqueado por auto-review; no se atribuye una certificación inexistente.

El lint dirigido detectó el encabezado de tareas del proyecto fuera del schema; se normalizó conservando su alcance y contenido. Las cinco notas de journal pasan strict sin errores ni warnings. La consulta focalizada reconoce la entidad en el índice previo; su refresh automático no pudo escribir en caché, por lo que no se atribuye freshness.

## Rollback

Scope local, sin secretos ni dumps. Corrección de la nota de estado mediante este delta; el código se conserva en la rama nueva sin PR ni push. El cierre posterior fue solicitado explícitamente por el owner el 07/10.


Delta de cierre: checkpoint vigente en el proyecto, feedback por evento y reparación del schema de tres agent_runs existentes. No se creó L0/L1/L3 ni otro checkpoint interno. Las correcciones de notas son reversibles mediante su diff; la entrega de código permanece intacta.
