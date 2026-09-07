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
  - "[[2026-08-12-stager-f32-unbounded-drain-entity-updated]]"
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

# F3.2 — Lifecycle cooperativo implementado localmente

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `sdk/pkg/shared/temporal/{client.go,client_test.go,go.mod,go.sum}`
  - `symphony/go.mod`, `symphony/go.sum`, `symphony/sqx/core/lifecycle/**`
  - `symphony/sqx/cmd/{sqx-worker,sqx-mt5-worker}/main.go`
  - `symphony/sqx/adapters/{quiesce-file,quiesce-etcd}/**`
  - `10-projects/Echo Forge/agentes/Stager - Cross-Platform Deployment Lifecycle.md`

## Motivo

- Implementar el contrato aprobado sin timeout destructivo y retirar la ruta legacy que llamaba `Worker.Stop()` antes de completar el drain.

## Fuentes usadas

- SPEC/PLAN/TASKS `FEAT-SQX-WORKER-LIFECYCLE` aprobados.
- Inspección del SDK Temporal y código local de Symphony/SDK/Stager.

## Resolución aplicada

- Se creó un gate atómico de admisión y conteo de activities, aplicado por interceptor Temporal.
- El SDK compartido expone `NewWorker`; preserva `StartWorker` legacy y actualiza Temporal Go SDK a `v1.44.1`.
- Linux y MT5 usan `Start` explícito y llaman `Stop` sólo tras recibir `Drained`; watchers file/ETCD sólo solicitan drain en el path nuevo.

## Validación

- PASS: `go test` y `go vet` focales de lifecycle, watchers y entrypoints; `git diff --check`; builds `linux-amd64` y `windows-amd64` temporales.
- PASS: `go test -mod=mod ./pkg/shared/temporal` y `go vet -mod=mod ./pkg/shared/temporal` en SDK.
- Pendiente: preflight real de Temporal Server, migración de schemas y test Windows/MT5 ocupado.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos.

## Rollback

- La release previa de Symphony se selecciona por Stager. No se mutaron hosts, servidor Temporal, `CURRENT`, `RUNNING`, `PENDING`, releases ni receipts.
