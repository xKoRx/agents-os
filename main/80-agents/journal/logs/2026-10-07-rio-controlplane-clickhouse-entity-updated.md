---
type: change_log
schema_version: 1
scope: session
created: "2026-10-07"
updated: "2026-10-07"
area: "[[Meli]]"
project:
application: "[[rio-controlplane-clickhouse]]"
entities: ["[[rio-controlplane-clickhouse]]"]
related: []
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

# ClickHouse — Estado local e integración Playmaker

## Cambio

- Actualización acotada de `30-resources/applications/rio-controlplane-clickhouse.md`: contrato de entrada vigente, stack y estado local/integración.
- Actualización de `30-resources/applications/00-index.md` y `log.md`; fuentes de preflight y del setup vigente materializadas bajo `_sources/`. La captura anterior de Playmaker se marca superseded sin borrar evidencia.
- Antes: stack y contratos verificados en agosto de 2026; entrada de deployment descrita como `/events` y SDK 1.3.0. Ahora: controller `/triggers/deployments`, SDK 1.6.1, Java 25, Boot 4.1.1 y estado de preflight fechado.

## Motivo

- El usuario pidió conservar un estado respecto del arranque local y posterior integración con Playmaker. Es verdad operacional de la app, respaldada por fuentes vigentes; no es una memoria de razonamiento.

## Fuentes usadas

- [[Source — ClickHouse — Preflight local 2026-10-07]].
- [[Source — ClickHouse — Develop y setup local 2026-10-07]].
- [[Source — Playmaker — Kafka local 2026-10-07]].

## Resolución aplicada

- Por instrucción explícita posterior del owner se abortó el merge y eliminó la rama antigua. CP en develop, sin cambios trackeados; referencia remota ausente. Se conserva el plan histórico [[Plan de implementación — Context en ClickHouse]] sin presentarlo como alcance vigente.
- Se documenta el launcher de Playmaker/MySQL/Kafka y la pieza de conexión pendiente, con opción de bridge temporal o adapters Kafka scoped. Se conserva la diferencia entre evidencia de arranque, DDL y ciclo integrado.

## Validación

- 2335 tests, 0 fallos/errores/omitidos; bootJar y `/ping` verificados sobre develop. Rechazo FAILED por Context ausente observado en archivo local.
- Git final y ausencia de rama remota verificados; DTO signatures entre SDK 1.5.0/1.6.1 comparadas con javap, schema 1 en ambos. DDL real e integración Playmaker no ejecutados. Metadata y links se validan con lint acotado.

## Rollback

- Retirar el bloque de estado agregado y restaurar únicamente los bullets de contratos/stack cambiados usando la versión previa de la página. No revertir cambios ajenos ni borrar evidencia fuente.
