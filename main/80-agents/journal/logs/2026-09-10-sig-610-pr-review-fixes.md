---
type: change_log
schema_version: 1
scope: session
created: "2026-09-10"
updated: "2026-09-10"
area: "[[Meli]]"
project: "[[SIG-610 — ComponentRun de inactivación en Playmaker]]"
application: "[[rio-playmaker]]"
entities:
  - "[[SIG-610 — Seguimiento de inactivación]]"
  - "[[SIG-610 — ComponentRun de inactivación en Playmaker]]"
  - "[[rio-playmaker]]"
related:
  - "[[2026-09-10-codex-gpt-5-inactivation-concurrency-review]]"
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-10-inactivation-concurrency-session-feedback]]"
  - "[[2026-09-10-sig-610-reindex-gate-graphify-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# SIG-610 — findings de concurrencia y error resueltos

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `rio-playmaker`: `PipelineExecutionRepository`, `InactivationResultHandlerImpl` y su test unitario.
  - [[SIG-610 — Seguimiento de inactivación]].
  - [[SIG-610 — ComponentRun de inactivación en Playmaker]].

## Motivo

- Resolver dos findings del PR #1144: carrera entre terminales concurrentes y persistencia/exposición del payload crudo de error del Control Plane.

## Fuentes usadas

- Código y tests locales de `rio-playmaker`; comentarios de Ale y del bot en el PR #1144; patrón existente de `PESSIMISTIC_WRITE` del repo.

## Resolución aplicada

- Se agregó lookup con `PESSIMISTIC_WRITE` por executionId antes de los guards; el segundo terminal espera y queda como no-op.
- El handler omite el mensaje/details upstream, valida y acota el code, usa un mensaje genérico propio y no registra el payload crudo.
- Tras un primer resultado de PR coverage de 89,24%, se cubrieron las ramas legacy, datos inconsistentes, liberación de lock y sanitización según la semántica estricta de Melicov.
- Commit `1c2601f96` publicado como head de `feature/sig-610-inactivate-component-run`; ambos threads respondidos.
- Fury creó `0.0.7-test-sig-610-dev-0`; el build `1635` terminó correctamente y el tag remoto apunta a `1c2601f96d582fa5058b5f84c41395e10113d412`.

## Validación

- Suites focalizadas y `./gradlew clean test jacocoTestReport` verdes: 3.650 tests, 2 skipped y cero fallos.
- Melicov remoto confirmó PR coverage 100,00% y minimum coverage 94,66%; CI, dependencias, análisis estático, coverage y workflow quedaron verdes sobre `1c2601f96`.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Código: revertir `1c2601f96` y `6c0acae0c` si la política se rechaza. Vault: restaurar los dos project notes desde su historial y remover este log/feedback asociado.
