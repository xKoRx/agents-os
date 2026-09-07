---
type: change_log
schema_version: 1
scope: session
created: "2026-08-26"
updated: "2026-08-26"
area:
project: "[[Playmaker — Doble dispatch al avanzar batches]]"
application: "[[rio-playmaker]]"
entities:
  - "[[Playmaker — Doble dispatch al avanzar batches]]"
  - "[[rio-playmaker]]"
related:
  - "[[Descripción PR — rio-playmaker — Hotfix doble dispatch]]"
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

# Playmaker — Cierre del hotfix de doble dispatch

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Meli/Playmaker — Doble dispatch al avanzar batches/Playmaker — Doble dispatch al avanzar batches.md`

## Motivo

- Persistir el estado realmente implementado y eliminar del contexto vigente las afirmaciones antiguas de que el backoff retenía un thread o reintentaba sin límite.

## Fuentes usadas

- Código y tests de `rio-playmaker` en `feature/serialize-batch-completed-listener`, commit `1d34e7532`.
- [[Descripción PR — rio-playmaker — Hotfix doble dispatch]].

## Resolución aplicada

- Se registró el retry no bloqueante con `CompletableFuture.delayedExecutor`, el límite de 10 retries, TTL máximo de 10 segundos, reutilización del QKVS existente y las limitaciones de durabilidad.
- Se dejó como próximo paso la validación concurrente en test2/staging y la revisión del PR.

## Validación

- Rama remota sincronizada; 3215 tests, 0 fallas, 2 skipped; `git diff --check` y JaCoCo exitosos.
- Lint estricto de los artefactos modificados: 0 errores y 0 warnings. La reindexación Graphify global quedó bloqueada por deuda preexistente fuera del proyecto; el patrón ya está registrado en el feedback de 2026-08-25.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** no aplica para compartición externa; no se agregaron secretos.

## Rollback

- Revertir esta actualización de estado si el commit `1d34e7532` se abandona o el diseño cambia antes de promoverse.
