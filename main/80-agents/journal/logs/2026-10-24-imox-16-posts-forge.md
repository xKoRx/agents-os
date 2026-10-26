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
share_scope: "local"
load_policy: "manual"
indexable: false
index_priority: "never"
tags: ["kind/change-log", "scope/session"]
---

# IMOX — Dieciséis posts y preparación de campañas Forge

## Cambio

Ingesta de 16 publicaciones: fichas y fuentes en `30-resources/imox/`, actualización de índice, entrada IMOX y log, y recurso [[IMOX - Building blocks y preparación de campañas Forge]]. Cada ficha enlaza directamente a Circle y a su source. La relación metodológica con Forge proviene del usuario; no se modificó el código ni la documentación de implementación de Forge.

## Validación

Lectura web exclusivamente en Chrome; excepción posterior autorizada para PDFs descargados desde Chrome. Cobertura y límites explícitos por documento, resultados atribuidos y conflictos conservados. Validación dirigida de schema sin errores ni avisos, enlaces internos resolubles y URL de Circle presente en las fichas y fuentes. Ninguna ejecución de adjuntos, publicación o campaña.

Se incorporaron siete PDFs únicos facilitados por Rodrigo, incluyendo el suplemento de sizing cuyo locator original queda pendiente, más la versión HTML de certificación. El RAR se inventarió sin ejecutar ni auditar; el reporte de ejemplo de la skill no llegó entre los archivos. Los anexos extensos se revisaron según la cobertura declarada en cada ficha.

## Rollback

Retirar las fichas, fuentes y síntesis creadas en esta ingesta y revertir solo las filas/párrafos añadidos al índice, entrada y log, preservando la primera ingesta y cualquier cambio ajeno.
