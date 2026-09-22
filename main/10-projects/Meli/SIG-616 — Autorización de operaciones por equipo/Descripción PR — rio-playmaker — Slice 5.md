---
type: doc
schema_version: 1
status: active
area: "[[Meli]]"
related:
  - "[[SIG-616 — Autorización de operaciones por equipo]]"
  - "[[SPEC técnica — Slice 5 — Actions restantes]]"
  - "[[rio-playmaker]]"
aliases:
  - PR Slice 5 SIG-616
tags:
  - kind/doc
  - project/sig-616-operation-authorization
created: "2026-09-16"
updated: "2026-09-21"
---

# Descripción PR — rio-playmaker — Slice 5

**PR:** [#1182](https://github.com/melisource/fury_rio-playmaker/pull/1182) · `feature/operation-authorization-by-team-f5` @ `6363d7e0e736bac94a8263c4fcaf1bef3a8c71fa` · base `feature/operation-authorization-by-team-f4` @ `ccce34382d1b7e6bdab395f5acd42fbb5a1b968f` · SPEC [[SPEC técnica — Slice 5 — Actions restantes]].

## Description

`feat(auth): configure remaining mutating Actions`

Este PR completa el Slice 5 de SIG-616 agregando configuración para las Actions mutantes ya existentes de Flink y ClickHouse. No introduce Actions, no clasifica lecturas, no rechaza pares desconocidos y no cambia precreation ni el tratamiento de componentes importados.

El enforcement reutiliza el puerto `ActionPermissionProvider` heredado de Slice 2. La implementación actual carga `component-type`, `action` y `access-level` desde `app.action-authorization.permissions`; una futura fuente Discovery puede implementar el mismo puerto sin cambiar `ActionService` ni sus consumidores.

Changes:

- Agrega a la configuración los pares exactos `start/stop` de `flink-sql`, `flink-job`, `aws-flink-sql` y `aws-flink-job`.
- Agrega `start-materialized-view/stop-materialized-view` para `clickhouse-mat-view`.
- Todos los pares nuevos usan `DEV_AND_UP` y se autorizan antes de deployment context, KVS y BigQueue.
- Los pares no configurados continúan por el flujo existente sin una regla ACME nueva.
- Mantiene sin cambios Actions de lectura, precreation, polling, imports, eventos, KVS, productores y Control Planes.
- Documenta `403` para la ruta component-bound cuando una regla configurada deniega la operación.

## How Has This Been Tested?

HEAD de código validado: `7afaa526c`; HEAD publicado con documentación: `6363d7e0e`.

- Tests focalizados de `ConfiguredActionPermissionProviderTest`, `ActionAuthorizationServiceTest`, `ActionServiceImplTest`, `ActionControllerTest` y `ActionResultControllerTest`: `BUILD SUCCESSFUL`.
- `./gradlew check`: `BUILD SUCCESSFUL`; 2 tests preexistentes skipped.
- Verificación estática: no existen `AUTHORIZED_ACTIONS`, `ActionKey` ni `ActionAuthorizationPolicy` en producción; la matriz vive únicamente en configuración.
- Smoke no productivo con Tiger/ACME reales: pendiente por falta de credenciales/acceso.

## Issue

- [SIG-616 — Autorización de operaciones por equipo](https://spellbook.adminml.com/projects/SIG/specs/SIG-616)
- [SIG-621 — Autorización de operaciones por equipo](https://spellbook.adminml.com/projects/SIG/specs/SIG-621)
