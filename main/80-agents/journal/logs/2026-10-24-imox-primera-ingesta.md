---
type: change_log
schema_version: 1
scope: session
created: "2026-10-24"
updated: "2026-10-24"
area: "[[Trading]]"
project:
application:
entities: ["[[IMOX]]"]
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

# IMOX — Primera ingesta

## Cambio

Creación del dominio `30-resources/imox/`: índice, bitácora, recurso [[IMOX]], ficha [[IMOX - Base de datos para analizar resultados]] y fuente [[IMOX - Fuente - Mi base de datos para analizar resultados]], materializados desde los templates contratados. Solicitud de Rodrigo: probar acceso en Chrome y extraer la información importante del primer post para consulta personal.

## Validación

Acceso real comprobado, cuerpo y ocho comentarios leídos tras desplegar respuestas, siete capturas y un adjunto de comentario revisados visualmente. Se verifican schema y referencias locales mediante lint dirigido. Se distinguen datos ficticios, incertidumbres y opiniones. No se publicó contenido ni se ejecutó software.

## Rollback

Retirar únicamente los seis archivos creados por esta ingesta si Rodrigo decide descartarla; no se modificaron notas anteriores.
