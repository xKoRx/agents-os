---
type: change_log
schema_version: 1
scope: session
created: "2026-09-01"
updated: "2026-09-01"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[Symphony]]"
entities: []
related: []
aliases: []
confidence: verified
source_session: ECHO-FORGE-C3-RELEASE-CONVERGENCE-RECOVERY-NORMAL
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Echo Forge C3 AdaptiveTypeWorkflow registration

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created
- **Archivo(s):**
  - `80-agents/memory/public/known-error/symphony/2026-09-02-echo-forge-c3-adaptive-workflow-registration.md`

## Motivo

- La certificación física encontró evidencia source-level que afecta un gate contractual: el worker productivo registra `AdaptiveTypeWorkflow`, explícitamente prohibido por C3.

## Fuentes usadas

- Lectura de `sqx/cmd/sqx-worker/main.go` en Symphony `02fabffe...`; convergencia real de `0.2.84`; gate de supply también bloqueado por promoción vacía.

## Resolución aplicada

- Se creó el known error como memoria pública reutilizable; no se modificó source, no se hizo commit/push y no se alteró la base de datos.

## Validación

- Registro source verificable; la release conserva `vcs.revision=02fabffe...` y el worker activo es `0.2.84`.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Nuevo commit que quite el registro prohibido y repetición completa del ciclo con nueva release e identidades físicas.
