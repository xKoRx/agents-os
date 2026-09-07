---
type: change_log
schema_version: 1
scope: session
created: "2026-08-12"
updated: "2026-08-12"
area: "[[Echo Forge]]"
project: "[[Stager - Cross-Platform Deployment Lifecycle]]"
application: "[[Stager]]"
entities:
  - "[[Stager - Cross-Platform Deployment Lifecycle]]"
related:
  - "[[2026-08-12-stager-f32-cooperative-lifecycle-implemented]]"
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

# F3.2 — Servidor Temporal actualizado, preflight pendiente

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Stager - Cross-Platform Deployment Lifecycle.md`

## Motivo

- Registrar que el servidor llegó a `v1.31.2`, sin sobredeclarar como completados los gates de configuración y runtime.

## Fuentes usadas

- Confirmación directa del owner el 2026-08-12.
- Inspección local de `deploy/linux/stager-runtime.service` y configuración runtime Windows: ambos conservan `shutdown_timeout` finito de cuatro horas.

## Resolución aplicada

- Se retiene el despliegue productivo y el flujo E2E. Antes de F3.3 se debe validar dynamic config `frontend.enableCancelWorkerPollsOnShutdown=true` y eliminar el deadline destructivo del runtime Stager con cobertura Linux/Windows.

## Validación

- Revisión documental y estado del planificador actualizados; no hubo mutación de host, servidor, release ni flujo.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos.

## Rollback

- No aplica: no hubo despliegue. El código local queda sin publicar y se preservan releases/estado canónico existentes.
