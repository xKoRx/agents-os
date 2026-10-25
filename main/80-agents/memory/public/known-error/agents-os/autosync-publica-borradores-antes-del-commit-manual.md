---
type: known_error
schema_version: 1
scope: project
created: "2026-10-25"
updated: "2026-10-25"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities: ["[[AGENTS OS]]"]
related: ["[[2026-10-25-forge-dynamic-groups-session-feedback]]"]
aliases: []
confidence: verified
source_session:
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/project
---

# Autosync publica borradores antes del commit manual

## Síntoma

Un borrador escrito en un checkout con sincronización automática puede llegar al remoto antes del commit manual del agente.

## Causa

El agente trató el árbol de trabajo como staging privado y comprobó demasiado tarde la visibilidad del remoto. El sincronizador actuó sobre archivos ya escritos.

## Impacto

Eliminar el archivo del árbol actual no lo elimina de commits históricos. La recuperación del árbol y la remediación del historial son acciones distintas.

## Detección

Antes de escribir material restringido, resolver Git root/remoto, comprobar visibilidad del repositorio con su proveedor y leer las reglas locales de sincronización. Si la visibilidad no está probada, conservar el borrador fuera del árbol sincronizado hasta resolver el destino.

## Mitigación

Escribir el contenido restringido en un destino privado verificado y dejar en el vault público sólo el enlace y estado mínimo. Ante exposición, detener nuevas copias, retirar la versión actual, informar al owner y registrar el alcance restante. No modificar la sincronización ni reescribir historia sin autorización aplicable.

## Evidencia

[[2026-10-25-forge-dynamic-groups-session-feedback]]: visibilidad verificada con el proveedor, publicación automática observada y retiro actual comprobado; el historial permanece. Búsqueda de duplicados por autosync/repositorio público/visibilidad en memoria pública sin una nota equivalente. Graphify CLI no disponible; búsqueda directa de Markdown.
