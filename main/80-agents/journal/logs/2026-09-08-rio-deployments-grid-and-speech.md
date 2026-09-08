---
type: change_log
schema_version: 1
scope: session
created: "2026-09-08"
updated: "2026-09-08"
area: "[[Meli]]"
project: "[[Presentación deployments en RIO]]"
application: "[[rio-playmaker]]"
entities: []
related:
  - "[[Deployments en RIO — flujo completo]]"
  - "[[Guion presentación — Deployments en RIO]]"
  - "[[RIO]]"
  - "[[Agent Run — 2026-09-08 — Codex — unknown — RIO deployments presentation]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[Session Feedback - 2026-09-08 - rio-deployments-presentation]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-08-rio-deployments-grid-and-speech

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created / updated
- **Archivo(s):**
  - created `30-resources/grids/rio-deployments-critical-flow.html`
  - created `10-projects/Meli/Presentación deployments en RIO/Guion presentación — Deployments en RIO.md`
  - updated `30-resources/grids/00-index.md`
  - updated `10-projects/Meli/Presentación deployments en RIO/Presentación deployments en RIO.md`
  - created este change log

## Motivo

- Convertir la investigación técnica en una presentación corta, visual y completamente local, con speech documentado y foco en los puntos donde el progreso puede perderse.

## Fuentes usadas

- [[Deployments en RIO — flujo completo]], [[Revisión de ads-signals-knowledge-library]] y los refs locales de Playmaker, SDK Events, Materializer y control planes registrados en el documento técnico.

## Resolución aplicada

- La versión vigente del Grid tiene seis slides y tono de revisión técnica entre pares. Explica primero el flujo, el modelo de datos y el camino asíncrono de Materializer; luego revisa cuatro fronteras de recuperación y los estados inconsistentes posibles ante la muerte súbita de Playmaker o de un CP.
- Se eliminaron las slides separadas de “trampas” y “deudas P0”. La tabla de gaps conserva sólo frontera, causa y evaluación; Fury CP queda como referencia del patrón `reported/published`.
- Se documentaron los seis CPs sin KMS y el rol de KVS en cada uno, la construcción del trigger dentro de Playmaker, `DeltaComputationService`, la diferencia entre `ComponentRun` y `Deployment`, y el significado de `DeploymentLog` y `Service.values`.
- `gcp-kafka-topic` se presenta como routing pendiente de verificar en configuración viva y no como afirmación cerrada de tráfico productivo.
- La segunda revisión aclara que el Deployment se crea durante el dispatch del batch, antes del listener `AFTER_COMMIT`; elimina las etiquetas A–D y agrupa los cortes en tres familias coherentes con la slide final.
- El modelo visual se reemplaza por un diagrama entidad–relación con cardinalidades y descriptores. Materializer muestra el callback como un POST HTTP separado y la slide de gaps elimina las cuatro cajas de alternativas para explicar directamente `timeout_at` y el reconciler de Fury CP.

## Validación

- La versión final de seis slides se revisó en navegador local a 1280 × 720. Se inspeccionaron el flujo, el modelo de datos, Materializer, la tabla de gaps y los escenarios de caída; no se observó clipping ni overflow de contenido. El servidor respondió HTTP 200 y los dos bloques de script pasaron validación sintáctica; el Grid contiene exactamente seis secciones navegables.

## Cierre AGENTS OS

- Se registró la ejecución atribuible de Codex con modelo `unknown`, resultado `success`, verificación `passed` y `user_rework: major`.
- Se dejó feedback de Sistema 1 sobre QA semántico de presentaciones técnicas; la posible promoción a L3 queda diferida hasta observar repetición.
- Los artefactos de cierre y las notas modificadas pasaron lint estricto sin errores ni warnings. Graphify autoactualizó el índice y resolvió el proyecto por su título canónico; el refresh reportó deuda global ajena a estos archivos, pero terminó con freshness `fresh`.

## Compartibilidad

- **Scope:** local / team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Eliminar el Grid y el guion creados, retirar sus entradas del índice y proyecto, y eliminar este change log. No hubo publicación remota ni cambios de runtime.
