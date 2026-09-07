---
type: decision
schema_version: 1
scope: project
created: "2026-09-06"
updated: "2026-09-06"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
related:
  - "[[2026-09-06-echo-forge-mt5-global-physical-ownership-v2]]"
  - "[[2026-09-06-echo-forge-mt5-execution-model-v2]]"
aliases:
  - ECHO_FORGE_MT5_NO_CROSS_HOST_TAKEOVER_V2
  - ECHO_FORGE_MT5_CANCEL_CAUSE_V2
confidence: verified
source_session: ECHO-FORGE-MT5-GLOBAL-FENCING-AND-CANCELLATION-SEMANTICS-V3-TOP-CORRECTION
supersedes: "[[2026-09-06-echo-forge-mt5-global-physical-ownership-v2]]"
load_policy: when_project_loaded
indexable: true
index_priority: high
tags:
  - kind/decision
  - scope/project
  - project/echo-forge
  - tech/mt5
  - tech/temporal
  - tech/etcd
---

# 2026-09-06-echo-forge-mt5-fencing-and-cancellation-v3

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- El TOP V2 congeló ownership global ETCD y rechazó TTL, pero dejó takeover manual con `fencing_token` y una ventana A+B si A está particionado.
- Autoridad Temporal del `sqx-mt5-worker`: `go.temporal.io/sdk v1.35.0` (`sqx/go.mod`). Root usa `v1.44.1` y no gobierna este runtime.
- `cmd_executor.Execute` mata el Job Object ante cualquier `ctx.Done()`. El SDK cancela el activity context tanto por `CancelRequested` como por `NotFound` y por RPC retryable agotado.

## Decisión

- PROJECT DECISION FROZEN `ECHO_FORGE_MT5_NO_CROSS_HOST_TAKEOVER_V2` (OPTION A): un owner `RUNNING` de otro host jamás se reemplaza desde Symphony, ni por admin API. Permanent host loss = BLOCKED / OPERATOR ACTION REQUIRED fuera de banda.
- `fencing_token` es compare-value de CAS, no fence físico. No hay autoridad de fence (Proxmox/VMware/cloud) en el runtime actual.
- Cancelación física sólo si `temporal.IsCanceledError(context.Cause(activityCtx))`. `serviceerror.NotFound`, RPC transiente y `worker.ErrWorkerShutdown` no matan el árbol MT5 sano.
- Proceso físico corre con `context.WithoutCancel` + cancel context propio. El Activity no retorna mientras el Job Object tenga procesos. No hay daemon nuevo.
- Éxito durable = HTM/EX5 write-once de `DeriveArtifactKey` exacta; HEAD/verify antes de todo spawn. ETCD owner se borra tras muerte del árbol y publicación ACK. `SUCCEEDED` no se retiene como coordinador.
- Campaign `MaxCampaignMT5BacktestChildrenPerGeneric = 4` se suprime como safety física. La cola natural es slot_count + MaxConcurrentActivityExecutionSize.
- `tasks[].mt5.timeout` se deprecia/ignora. No `WithTimeout(task timeout)` ni `StartToClose = timeout + X` de negocio. HeartbeatTimeout queda liveness (2m, no 30s).
- NORMAL B no cabe en 14 archivos con tests existentes. Split coherente: B1 ownership/reuse/timeout/campaign; B2 cancel/Job Object/mutex/drain PENDING.

## Rationale

- Un token en ETCD no llega a un `terminal64` que no puede leer ETCD. Sin fence externo, el único invariante ALWAYS es no spawnear en otro host mientras exista `RUNNING`.
- `internalHeartBeat` de SDK v1.35.0 pasa la causa exacta a `context.WithCancelCause`. Symphony puede clasificar D1 vs D2 vs D3 vs D4.
- Cerrar el handle del Job Object (`KILL_ON_JOB_CLOSE`) mata el cálculo. El goroutine del Activity es el supervisor mínimo.

## Consecuencias

- NEXT EXACT: `ECHO-FORGE-MT5-LONG-RUNNING-GLOBAL-OWNERSHIP-RETRY-DRAIN-V2-NORMAL-B1`.
- Takeover manual con incremento de token del TOP V2 queda SUPERSEDED.
- Operator recovery de host muerto: fence físico fuera de Symphony, luego `etcdctl` delete de la key. Symphony no expone takeover.

## Alternativas descartadas

- OPTION B (takeover after external fence): no existe fencing authority en el lab/runtime actual; no se inventa Proxmox/VMware.
- Takeover manual Symphony + suicidio diferido del owner viejo: ventana split-brain hasta reconexión; viola ALWAYS.
- Supervisor/daemon separado: innecesario si el Activity no retorna y no mata por NotFound.
