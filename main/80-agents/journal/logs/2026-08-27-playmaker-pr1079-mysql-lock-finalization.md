---
type: change_log
schema_version: 1
scope: session
created: "2026-08-27"
updated: "2026-08-27"
area: "[[Meli]]"
project: "[[Playmaker — Doble dispatch al avanzar batches]]"
application: "[[rio-playmaker]]"
entities:
  - "[[Playmaker — Doble dispatch al avanzar batches]]"
  - "[[rio-playmaker]]"
related:
  - "[[Descripción PR — rio-playmaker — Hotfix doble dispatch]]"
  - "[[qkvs-save-version-zero-no-garantiza-create-only]]"
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

# Playmaker PR #1079 — finalización con lock MySQL

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated / conflict-resolution
- **Archivo(s):**
  - `10-projects/Meli/Playmaker — Doble dispatch al avanzar batches/Playmaker — Doble dispatch al avanzar batches.md`
  - `10-projects/Meli/Playmaker — Doble dispatch al avanzar batches/Descripción PR — rio-playmaker — Hotfix doble dispatch.md`
  - `80-agents/memory/public/known-errors/qkvs-save-version-zero-no-garantiza-create-only.md`

## Motivo

- El approach QKVS del PR no ofrecía exclusión create-only demostrable en el SDK usado. Se reemplazó por serialización transaccional sobre `pipeline_execution` con `PESSIMISTIC_WRITE`, relectura dentro del lock e idempotencia por materialización del batch.

## Fuentes usadas

- Código, diff y tests de `feature/serialize-batch-completed-listener`; review Zord; correcciones Luna; ejecución local de Gradle; checks de GitHub; documentación previa del incidente y descripción del PR #1079.

## Resolución aplicada

- La documentación vigente ahora identifica el commit final `f7d4f4881`, los tests de comportamiento con y sin lock, los límites del retry en memoria y la versión objetivo `0.0.9-listener-lock`. Las secciones QKVS antiguas permanecen sólo como historial explícitamente superseded.

## Validación

- `./gradlew test jacocoTestReport --no-daemon`: 3.232 tests, 0 fallas, 0 errores, 2 skipped; coverage global 96,36 %. `./gradlew check --no-daemon`, `git diff --check` y todos los checks del PR pasaron. `0.0.9-listener-lock` terminó correctamente en Fury después de un único retry idempotente. Las ocho notas de cierre pasaron lint estricto con `0 ERROR / 0 WARN`. La reindexación Graphify fue bloqueada por 18 findings ajenos en Signals y un known error zsh; no se alteró esa deuda fuera de alcance. La validación real en MySQL de staging continúa pendiente.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin secretos; conserva rutas y referencias operativas locales porque este log es de continuidad privada.

## Rollback

- Revertir el commit `f7d4f4881` y restaurar la descripción anterior del PR sólo si la serialización MySQL falla en staging. No volver al mutex QKVS sin una operación create-if-absent atómica documentada y un test concurrente determinístico.
