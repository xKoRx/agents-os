---
type: change_log
scope: session
created: 2026-08-10
updated: 2026-08-10
area: "[[Meli]]"
project:
application:
entities:
  - "[[rio-playmaker]]"
  - "[[rio-controlplane-clickhouse]]"
  - "[[rio-controlplane-fury]]"
  - "[[rio-controlplane-flink]]"
  - "[[rio-controlplane-kafka]]"
  - "[[rio-controlplane-signals]]"
  - "[[rio-controlplane-kms]]"
  - "[[rio-controlplane-observability]]"
  - "[[rio-sdk-events]]"
  - "[[rio-materializer]]"
related:
  - "[[70-templates/application]]"
  - "[[30-resources/applications/00-index]]"
aliases:
  - rio applications created
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
  - change/created
---

# Aplicaciones RIO creadas

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `30-resources/applications/rio-*.md` (10 notas de aplicación)
  - `30-resources/applications/00-index.md`
  - `30-resources/applications/log.md`
  - `~/fuentes/rio-*/` (10 repositorios clonados)

## Motivo

- El usuario pidió clonar los repositorios RIO en el workspace externo y registrarlos como aplicaciones usando nombres locales `rio-*`.

## Fuentes usadas

- Remotes de GitHub verificados con `gh repo view`.
- README y manifests Gradle de cada repositorio clonado.
- `70-templates/application.md`.

## Resolución aplicada

- Se clonaron los 10 repositorios bajo el workspace externo con nombres locales `rio-*`.
- Se crearon notas canónicas con títulos `rio-*`, `slug` equivalente y alias del remote original.
- Se actualizó el índice y la bitácora de aplicaciones.

## Validación

- Los 10 clones tienen remote `git@github.com:melisource/...` y checkout válido.
- Las notas nuevas pasan el lint puntual de entidad application.
- El checkout local de `rio-playmaker` reportó una colisión entre `CLAUDE.md` y `Claude.md` por filesystem case-insensitive; el clone terminó exitosamente.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin credenciales, secretos ni dumps.

## Rollback

- Mover a archivo las 10 notas, quitar sus filas del índice y retirar los 10 directorios clonados; conservar este log como auditoría.
