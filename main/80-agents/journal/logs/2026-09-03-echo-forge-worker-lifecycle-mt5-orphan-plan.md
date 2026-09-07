---
type: change_log
schema_version: 1
scope: session
created: "2026-09-02"
updated: "2026-09-02"
area:
project:
application:
entities: []
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

# 2026-09-03-echo-forge-worker-lifecycle-mt5-orphan-plan

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** conflict-resolution / created / updated
- **Archivo(s):** `2026-09-03-orphan-mt5-after-cancel.md`, `2026-09-03-echo-forge-worker-execution-model-v1.md`, el checkpoint de Echo Forge y el plan canónico `2026-09-03-echo-forge-worker-lifecycle-mt5-orphan-plan.md`.

## Motivo

- Corregir el RCA persistido que atribuía erróneamente a SQX una concurrencia efectiva 1000 y exigía una Slice A de serialización.
- Persistir el plan exacto para el orphan MT5 post-cancel, incluido replay/versioning y ownership Windows.

## Fuentes usadas

- Symphony baseline `bac1d6ef93cd4714c1af4f2e44516bea44642e80` y SDK authority `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`.
- `go.temporal.io/sdk v1.44.1`, `pkg/shared/temporal/client.go`, workflows MT5/Generic y cmd-executor actuales.
- Incidente FlowRun `d7693ebe-4ea8-4c10-a65e-c45d676ac788` y contrato `ECHO-FORGE-WORKER-LIFECYCLE-AND-MT5-ORPHAN-PLAN-NORMAL`.

## Resolución aplicada

- Se retiró de la memoria pública la afirmación `WORKER_LOCAL_CONCURRENCY_CONTRACT_VIOLATION` para SQX y se fijó la normalización SDK zero→one.
- Se persistió la decisión de dos slices B/C: Temporal request-cancel + wait-all y Windows Job Object ownership/drain.
- Se dejó explícito `GetVersion` con rama legacy para replay, `context.Canceled` como cancelación requerida y el barrier físico como garantía de retry/workspace.

## Validación

- Verificación local read-only de HEAD, `go.mod`, SDK pinned, opciones Temporal, workflows y consumers del cmd-executor. No se ejecutó implementación, build, release ni smoke física porque esta sesión es plan-only.
- Se preservaron los cambios dirty preexistentes del checkout; no se modificó ningún archivo del repositorio.

## Compartibilidad

- **Scope:** team
- **Redacción revisada:** sin memoria interna, secretos ni detalles no necesarios; los identificadores de incidente son los entregados como autoridad.

## Rollback

- Revertir únicamente las actualizaciones de memoria de esta sesión mediante un nuevo change log; no revertir los cambios dirty del repositorio ni reintroducir la RCA de concurrencia rechazada.
