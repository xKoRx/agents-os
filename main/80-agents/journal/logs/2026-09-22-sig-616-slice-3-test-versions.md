---
type: change_log
schema_version: 1
scope: session
created: "2026-09-22"
updated: "2026-09-22"
area: "[[Meli]]"
project: "[[SIG-616 — Autorización de operaciones por equipo]]"
application:
entities:
  - "[[SIG-616 — Autorización de operaciones por equipo]]"
related: []
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

# SIG-616 — Variantes de test de Slice 3

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):** `10-projects/Meli/SIG-616 — Autorización de operaciones por equipo/SIG-616 — Autorización de operaciones por equipo.md`

## Motivo

- El estado de Slice 3 no registraba las variantes temporales de autorización con roles ACME sintéticos ni sus versiones de prueba asociadas.

## Fuentes usadas

- La fuente es el repositorio `melisource/fury_rio-playmaker`: los commits publicados `844e2da344bc` y `19af793b591b`, los checks locales exitosos y `fury list-versions --limit 5`, que informó ambas versiones en estado `CREATING`.

## Resolución aplicada

- Se añadió el estado actual de las ramas `feature/sig-616-auth-p3-committer-test3-v17` y `feature/sig-616-auth-p3-viewer-test3-v18`; se documentó que `committer` permite `DEV_AND_UP`, `viewer` lo deniega y que ninguna variante fue desplegada.

## Validación

- Se ejecutaron los tests focalizados `AcmeClientRoleMockTest`, `ActionAuthorizationServiceTest`, `ActionServiceImplTest` y `ComponentAuthorizationIntegrationTest`; `git diff --check` y el contrato de testing pasaron. Fury confirmó la creación pendiente de `0.1.3-p3-committer-allowed` y `0.1.4-p3-viewer-denied`; la finalización remota sigue pendiente.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir la línea de estado de Slice 3 y borrar este change log si se invalida la evidencia; las ramas y versiones se gestionan por separado en Fury/GitHub.
