---
type: change_log
schema_version: 1
scope: session
created: "2026-08-12"
updated: "2026-08-12"
area: "[[Meli]]"
project: "[[Estandarización de Scopes RIO]]"
application:
entities:
  - "[[Estandarización de Scopes RIO]]"
  - "[[RIO]]"
  - "[[scope-compatibility-matrix]]"
  - "[[fury-segmentation-model]]"
  - "[[scope-naming-standard]]"
related:
  - "[[scope-inventory]]"
  - "[[00-index]]"
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

# 2026-08-12-scopes-rio-segmentation-naming-grid

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):**
  - `30-resources/rio-atlas/architecture/scope-compatibility-matrix.md` (created — Inventario 4: matriz end-to-end 39 consumidores BigQueue)
  - `30-resources/rio-atlas/architecture/fury-segmentation-model.md` (created — modelo de segmentación Fury nonprod/nonsite/legacy)
  - `30-resources/rio-atlas/architecture/scope-naming-standard.md` (created — propuesta de nomenclatura `lane[-role]`, borrador)
  - `30-resources/grids/rio-scope-inventory.html` + `30-resources/grids/00-index.md` (created — grid visual + índice de grids)
  - `30-resources/rio-atlas/architecture/scope-inventory.md` (updated — cross-link a la matriz)
  - `30-resources/rio-atlas/00-index.md` + `log.md` (updated — catálogo, KPIs, bitácora)
  - `10-projects/Meli/Estandarización de Scopes RIO/Estandarización de Scopes RIO.md` (updated — Inventario 4 ✅, tareas Naming WIP y Segmentación/Legacy, bitácora, docs, progreso 30→55)

## Motivo

- Cierre de la fase as-is (Inventario 4) y encargo del usuario: reporte visual de scopes (grid), investigación de la capability de segmentación de Fury y propuesta de nomenclatura para todo el backend RIO, con conocimiento durable persistido.

## Fuentes usadas

- Fury CLI autenticada: `fury services bigq consumers list` (39 consumidores por repo), `fury list-segments` (business segment `meli` + infra-segments), declaraciones `segment-id` y bloques `events.bigqueue.topics` en `application*.yml` de los repos backend RIO en `~/fuentes`.
- Notas base: [[scope-inventory]], [[integration-map]], [[deploy-request-path]].

## Resolución aplicada

- Se resolvió el link canal↔scope (que faltaba en Inventario 3) con la lista de consumidores BigQueue y se verificó contra código. Hallazgo canónico: la compatibilidad se rige por `(canal, segmento Fury)`, no por el nombre del scope; el segmento es propiedad del recurso, no del scope. 14 scopes tocan `legacy`.
- El MCP de Fury no quedó conectado en la sesión; se usó la CLI autenticada como fallback (sin bloqueo). No se persistieron dumps crudos (invariante 12). 

## Validación

- Totales del grid cuadran con el inventario (87 scopes, 21 used, 62 no-evidence, 1 retirement-candidate, 3 inactive). Grid renderizado y verificado en navegador. Consumidores: 39 (38 running, 1 paused).

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Notas nuevas son aditivas; revertir = borrar los 4 archivos creados y deshacer los cross-links en `scope-inventory.md`, `00-index.md`, `log.md` y la nota de proyecto.

## Auditoría posterior — 2026-08-12

- Se auditó el encargo original contra la CLI live, las fuentes capturadas y el código seleccionado. La evaluación del inventario quedó aceptada con límites; se corrigieron cuatro sobreafirmaciones: `running` no equivale a tráfico/uso, `(canal, segmento)` es routing y no compatibilidad suficiente, no hay evidencia de subsegmentos `nonprod-<lane>`, y las 14 marcas legacy son exposiciones potenciales derivadas, no recursos live distintos.
- [[scope-naming-standard]] pasó a iteración 2: gramática `lane[-role[-workload]]`, identidad `application/scope`, workloads para evitar colisiones y manifiesto versionado de bindings/contratos como fuente de compatibilidad. `alpha/beta/gamma` quedó explícitamente ilustrativo.
- El grid se conserva como snapshot exploratorio con disclaimer: el conteo bruto no es riesgo/prioridad, config base no es defecto automático y los scripts efímeros impiden reproducibilidad end-to-end. El proyecto bajó progreso 55→45 y agregó gates de manifest, segmentación live y generador versionado.

## Actualización final — 2026-08-12 21:27

- La autoridad quedó reemplazada por el service graph completo: 88 runtimes, `metadata.segment` live en 88/88, 40 consumers y cero bindings unresolved. Las métricas históricas `used/no-evidence` y la conclusión “segmento no es propiedad del scope” quedan supersedidas.
- La propuesta v2 exige `prod`, `stage` y `alpha` en todas las aplicaciones; `beta/gamma` son opcionales. El diff derivado registra 79 retiros, 9 identidades mantenidas y 76 altas; el grid usa borde rojo/gris/verde y punto amarillo sólo en 15 Streams.
- La auditoría de Playmaker, `rio-sdk-events`, mqclient 3.4.9 y Fury observó que `Filters` sólo transporta `modified_fields`; los 40 consumers reportan `MATCH_ANY` con lista vacía. Se decide proponer `X-RIO-Environment` validado al ingreso, `environment_scope` en payload, topic por ambiente y guard en el consumer. `withSegmentID` conserva únicamente el mapping físico nonprod/nonsite.
- Fuentes actualizadas: `~/fuentes/rio-inspector/rio-scopes.json`, `rio-scope-policy.json`, [[scope-inventory]], [[scope-naming-standard]] y [[Estandarización de Scopes RIO]].
