---
type: change_log
schema_version: 1
scope: session
created: "2026-09-07"
updated: "2026-09-07"
area: "[[Meli]]"
project: "[[Presentación deployments en RIO]]"
application: "[[rio-playmaker]]"
entities: []
related:
  - "[[Deployments en RIO — flujo completo]]"
  - "[[RIO]]"
  - "[[rio-sdk-events]]"
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

# 2026-09-07-rio-deployments-presentation-technical-flow

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - updated `10-projects/Meli/Presentación deployments en RIO/Deployments en RIO — flujo completo.md`
  - updated `10-projects/Meli/Presentación deployments en RIO/Presentación deployments en RIO.md`
  - created este change log

## Motivo

- Reordenar el material para una presentación técnica en dos pasadas: primero flujo vigente con tecnologías y luego análisis causal de los puntos donde se puede perder progreso, con solución y deuda técnica.

## Fuentes usadas

- `origin/master` local de Playmaker, SDK Events, Materializer y los control planes Kafka, Flink, ClickHouse, Fury, Signals y Observability; guía y revisión previas del proyecto.

## Resolución aplicada

- La guía quedó dividida en funcionamiento actual, nueve puntos críticos y un backlog de nueve deudas técnicas con criterio de aceptación. Se corrigió la lectura de Materializer: owner explícito de `s3-bucket` y `gcs-bucket`, pero catch-all legacy que también recibe `gcp-kafka-topic` según la configuración base de Playmaker.

## Validación

- Frontmatter y hard-wrap verificados; rutas BigQueue, timeout job, listeners `AFTER_COMMIT`, persistencia KVS/QKVS, orden de publicación terminal y recuperación de sagas contrastados en código. Los remotes corporativos no estuvieron disponibles, por lo que se dejaron hashes locales y el límite de configuración viva explícitos.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir los dos archivos actualizados y eliminar este change log. No hubo cambios en repos, runtime ni infraestructura.
