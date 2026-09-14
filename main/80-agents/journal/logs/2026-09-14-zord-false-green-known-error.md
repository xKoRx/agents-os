---
type: change_log
schema_version: 1
scope: session
created: 2026-09-14
updated: 2026-09-14
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[local-agents-pipeline-cli]]"
related:
  - "[[zord-output-json-false-green-on-total-reviewer-failure]]"
  - "[[2026-09-14-playmaker-pr1126-zord-session-feedback]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-14-playmaker-pr1126-zord-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Promoción del falso verde de Zord a known error

## Cambio

- **Tipo:** created.
- **Archivo(s):** `80-agents/memory/public/known-error/zord-output-json-false-green-on-total-reviewer-failure.md`.

## Motivo

- El mismo fallo total oculto por exit `0` y salida vacía se observó en dos sesiones y puede invalidar gates de review.

## Fuentes usadas

- Feedback SIG-610 del 2026-09-09 y smokes del PR #1126 del 2026-09-14.

## Resolución aplicada

- Se documentaron síntoma, detección fail-closed y mitigación hasta corregir la CLI.

## Validación

- Duplicate check dirigido por `local-agents-pipeline`, `zord`, `false green`, `error=true` y `zords: []`; no existía un L3 equivalente.
- La nota se validó con lint y consulta enfocada de retrieval al cerrar.

## Compartibilidad

- **Scope:** local.
- **Redacción revisada:** no contiene secretos ni memoria interna; conserva sólo comportamiento reproducible de la herramienta.

## Rollback

- Eliminar la nota y este log si una versión publicada de la CLI hace fail-closed y la mitigación deja de aplicar.
