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
  - "[[2026-08-12-stager-f32-temporal-lifecycle-blocked-entity-updated]]"
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

# F3.2 — Drain cooperativo y upgrade Temporal aprobados

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Stager - Cross-Platform Deployment Lifecycle.md`
  - `symphony/specs/FEAT-SQX-WORKER-LIFECYCLE/{SPEC.md,PLAN.md,TASKS.md,changes/CHANGE-001-unbounded-cooperative-drain.md}`

## Motivo

- El owner rechaza cualquier timeout automático que pueda perder una activity/backtest de días; acepta sólo indisponibilidad breve durante el drain.

## Fuentes usadas

- Owner conversation del 2026-08-12.
- Temporal Go SDK release `v1.44.1` y Temporal Server release `v1.31.2` revisados en fuentes oficiales.
- Inspección local de Symphony, SDK compartido y Stager runtime.

## Resolución aplicada

- Se reemplazó `draining-timeout` por gate atómico de admisión/conteo, espera cooperativa sin deadline y alerta no destructiva.
- Se gateó el canary por actualización a Temporal Go SDK `v1.44.1`, Temporal Server `v1.31.2`, migración oficial de schemas y `frontend.enableCancelWorkerPollsOnShutdown=true`.
- Se mantiene que un fallo físico requiere activities idempotentes, reintentables y con checkpoints/heartbeats verificables antes de G3.

## Validación

- `bash tools/sdd/verify-spec.sh specs/FEAT-SQX-WORKER-LIFECYCLE/SPEC.md` → READY, 0 BLOQ, 0 MAY.
- `git diff --check` en Symphony → PASS.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos.

## Rollback

- Revertir el cambio documental/implementación antes de canary no toca hosts, releases, `CURRENT`, `RUNNING`, `PENDING` ni receipts. El rollback del servidor se ejecuta sólo mediante el runbook oficial tras validar schemas.
