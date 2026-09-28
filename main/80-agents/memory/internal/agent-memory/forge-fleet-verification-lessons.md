---
type: agent_memory
schema_version: 1
scope: project
created: "2026-09-28"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
entities:
  - "[[Echo Forge]]"
confidence: high
memory_state: active
continuity_key: forge/fleet-verification-lessons
load_policy: when_project_loaded
indexable: true
index_priority: normal
tags:
  - agent/internal
  - kind/agent-memory
  - project/echo-forge
---

# Forge — lecciones de verificación de flota/runtime (2026-09-27 recovery)

- La firma de un runtime Forge sano se lee en `evaluations[].payload.classification_input` + `metric_sets[].values` OBSERVED; las colecciones de snapshots sólo se sellan al cierre del group: nunca usarlas como señal de staleness de un probe cancelado a mitad.
- `tmpevidence` MUESTREA (dump ≠ conteo final): contar siempre por `flow_run_ref` directo en Mongo (helper top-mongo); un dump temprano ve menos filas que el estado final.
- "Activity scheduled sin Started en GetWorkflowHistory" no prueba wedge: `DescribeWorkflowExecution` (pendingActivities) es la fuente autoritativa — state=Started + last_heartbeat vivo = trabajo real (regresión de diagnóstico de esta sesión, 3h de falsa alarma).
- Sin SSH, el canal de verdad del rollout es Prometheus (`process_executable_path=/opt/stager/releases/<V>/bin/symphony` por host_key) + conducta; `deploy_release.sh` ≥0.2.127 fail-closed reporta honestamente "PUBLICADA; rollout NO VERIFICADO".
- El namespace Temporal de flota es **sqx-prop** (ETCD `/sqx-worker|/sqx-watcher/production/`); `/symphony/production/` es legado y el MCP temporal puede quedar bound a otro ns (pollers vacíos ≠ flota muerta). Helpers Go en /tmp con module `github.com/xKoRx/symphony/tmp/X` + go.mod/go.sum del repo (replace ../sdk) y app `sqx-worker` (sqx-watcher no tiene mongo/uri).
- Especificar FlowRuns durables: todo task project durable necesita `source_folder` NO vacío en versiones <0.2.128 (desde `7afb2a6` el download siempre activa); la task selection necesita `source_folder` == folder del productor (anidado soportado desde `8a89953`).
