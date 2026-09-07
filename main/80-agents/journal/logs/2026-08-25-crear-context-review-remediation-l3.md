---
type: change_log
schema_version: 1
scope: global
created: 2026-08-25
entities:
  - "[[rio-playmaker]]"
  - "[[AGENTS OS]]"
related:
  - "[[Crear Context - Code Review Remediation]]"
tags:
  - kind/change-log
  - area/meli
  - application/rio-playmaker
---

# 2026-08-25 — Memoria pública nueva desde la remediación del Context

## Qué se creó

- `80-agents/memory/public/known-error/playmaker-environment-stub-en-dispatch-v1.md` — el `EnvironmentModel` que entrega `DeploymentGroupServiceImpl.createSingle` es un stub JPA con sólo el `id`; `name` y `type` llegan null por el camino v1 de dispatch y degradan en silencio. Descubierto al corregir la resolución de ambiente equivalente del Component Context, y confirmado en un segundo lugar (`DispatchRequest.environmentName`, preexistente).
- `80-agents/memory/public/learning/grep-acotado-no-prueba-ausencia.md` — un finding que afirma una ausencia tiene que cubrir a los productores, no sólo a los consumidores. Origen: un finding falso de esta misma sesión.

## Qué se actualizó

- `80-agents/memory/public/user-preference/rjara-agent-profile.md` — regla de construcción de tests. Log propio en `2026-08-25-profile-test-construction-rule.md`.

## Reindex

Corresponde reindexar Graphify: se agregaron dos notas `indexable: true` en `80-agents/memory/public/`.
