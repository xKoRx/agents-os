---
type: change_log
scope: session
created: 2026-08-10
updated: 2026-08-10
area: "[[Meli]]"
project:
application:
entities:
  - "[[Meli]]"
related:
  - "[[agent-constitution]]"
aliases:
  - meli vault cleanup
  - vis archive
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
  - area/meli
  - change/updated
---

# Limpieza del vault Meli — archivo VIS

## Cambio

- **Tipo:** moved / updated
- **Destino:** `40-archive/VIS/`
- **Proyectos:** se movieron las 7 unidades de proyecto Meli, conservando sus
  subcarpetas y notas de agentes bajo `40-archive/VIS/projects/`.
- **Aplicaciones:** se movieron 14 notas de aplicaciones Meli bajo
  `40-archive/VIS/applications/`.
- **Índice:** `30-resources/applications/00-index.md` ahora muestra sólo las 13
  aplicaciones que permanecen activas en el catálogo.

## Alcance excluido

Se conservaron en `30-resources/applications/` las 10 aplicaciones RIO
indicadas por el usuario: playmaker, los siete controlplanes, sdk-events y
materializer.

## Validación

- No se movieron `20-areas/Meli.md`, quarters/sprints ni templates.
- Las notas archivadas mantienen sus títulos y wikilinks internos.
- No se movieron repositorios ni credenciales; sólo notas Markdown del vault.

## Rollback

Reubicar las unidades desde `40-archive/VIS/projects/` y
`40-archive/VIS/applications/` a sus rutas originales y restaurar las filas
retiradas del índice.
