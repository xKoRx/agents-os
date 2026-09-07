---
type: change_log
schema_version: 1
scope: session
created: "2026-08-23"
updated: "2026-08-23"
area: "[[Echo]]"
project: "[[Echo Forge]]"
application: "[[Symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[sqx-wfm-durable-export-heartbeat-timeout-while-sqcli-running]]"
aliases: []
confidence: verified
source_session: "DURABLE-WFM-EXPORT-HEARTBEAT-TIMEOUT-WHILE-SQCLI-STILL-RUNNING-NORMAL"
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-08-23 echo-forge wfm export heartbeat liveness

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo Forge/agentes/Echo Forge - Arquitectura de Datos y Migración de Persistencia.md`
  - `80-agents/memory/internal/agent-memory/global/agents-os-operating-continuity.md`
  - `80-agents/memory/internal/agent-memory/2026-08-23-echo-forge-final-e2e-attempt-16-continuity.md`
  - `80-agents/memory/public/known-error/symphony/sqx-wfm-durable-export-heartbeat-timeout-while-sqcli-running.md`
  - `80-agents/journal/agent-runs/2026-08-23-1822-cursor-grok-4-6-wfm-export-heartbeat-liveness.md`
  - repo `github.com/xKoRx/symphony` paths `sqx/activities/worker/wfm_durable_export_activity.go` y `sqx/activities/worker/wfm_durable_export_activity_test.go`

## Motivo

- Corregir el blocker físico de Attempt 16: Temporal vencía `HeartbeatTimeout=2m` en `wfm_durable_export` mientras `sqcli` seguía ejecutándose.

## Fuentes usadas

- Attempt 16 WorkflowID `sqx-main-v1-436c77d6-4b9a-4308-a89e-062dab0df373`
- `[[sqx-wfm-durable-export-heartbeat-timeout-while-sqcli-running]]`
- `sqx/core/instrumentation/heartbeat.go` (`StartHeartbeatWithDetails`, default 6s, ETCD `sqx/activity/heartbeat_seconds`)

## Resolución aplicada

- Activity A inicia `StartHeartbeatWithDetails` (`phase=wfm_physical_export`) inmediatamente antes de `physical.Export` y lo detiene con `defer Stop` al retornar. Constructor y wiring de producción sin cambios (`etcd` nil → intervalo 6s). Tests de interceptor Temporal demuestran heartbeats mientras el exporter está bloqueado.

## Validación

- `HEAD == origin/master == 435562b04bef931c5b16602c95235db6e1b6c434`
- `go test ./sqx/activities/worker -run 'WFMDurableExport'` PASS
- `go test ./sqx/activities/worker` PASS
- `go test ./sqx/workflows` PASS
- `go vet ./sqx/activities/worker ./sqx/workflows` PASS
- build `./sqx/cmd/sqx-worker` PASS
- `git diff --check` PASS

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir el commit `435562b` restaura el one-shot heartbeat previo a `physical.Export`. No toca workers ni release 0.2.66.
