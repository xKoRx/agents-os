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
  - "[[2026-09-06-echo-forge-mt5-fencing-and-cancellation-v3]]"
  - "[[2026-09-06-echo-forge-mt5-execution-model-v2]]"
  - "[[2026-09-03-echo-forge-worker-execution-model-v1]]"
superseded_by: "[[2026-09-06-echo-forge-mt5-fencing-and-cancellation-v3]]"
aliases:
  - ECHO_FORGE_MT5_GLOBAL_PHYSICAL_OWNERSHIP_V2
  - cross-host MT5 ownership
confidence: verified
source_session: ECHO-FORGE-MT5-CROSS-HOST-OWNERSHIP-AND-RETRY-SAFETY-V2-TOP-CORRECTION
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

# 2026-09-06-echo-forge-mt5-global-physical-ownership-v2

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Contexto

- Slot Pool V2 NORMAL A está PASS / CLOSED en `a10c26c887e4d203b403d2557e292ed773830b0e` y prueba exclusividad física local (un slot → a lo más un job local).
- El lease vigente es un archivo de filesystem por slot (`<JobsRoot>/.echo-forge-slot-lease.json`). Workers en hosts distintos no se ven. Todos poll `sqx-mt5-queue`.
- Temporal Go SDK `v1.44.1` (pin de misión; el módulo `sqx` sigue en `v1.35.0` con la misma semántica de retry) trata `TIMEOUT_TYPE_HEARTBEAT` y `TIMEOUT_TYPE_START_TO_CLOSE` como retryable. El timeout de servidor cierra el attempt y puede despachar otro a otro worker sin probar que el proceso OS anterior murió.

## Decisión

- PROJECT DECISION FROZEN `ECHO_FORGE_MT5_GLOBAL_PHYSICAL_OWNERSHIP_V2`: para cada `LogicalJobID` en toda la flota MT5, `LIVE_PHYSICAL_EXECUTIONS <= 1` siempre.
- Nivel 1 (nuevo): ownership global persistente no-TTL en ETCD, CAS create-if-absent por `LogicalJobID`. Nivel 2 (NORMAL A): lease local de slot se conserva y no se revierte.
- Autoridad: ETCD cluster ya usado por `sqx-mt5-worker`. PostgreSQL no se introduce en el worker Windows para este contrato. CacheClient no expone CAS; NORMAL B debe usar `*etcd.Client`/`GetRawClient().Txn` vía un accessor DI documentado, no `CacheClient.Get/SetVar`.
- Key: `echo-forge/mt5/logical-jobs/<logical_job_id>` con owner host (`HOST_KEY` o hostname), worker epoch, pid, slot_id, fencing_token, state `RUNNING|SUCCEEDED|FAILED|CANCELLED`.
- Acquire: Txn compare revision=0 / create. Mismo host+epoch `RUNNING`: WAIT, no spawn. Host distinto `RUNNING`: error retryable `OWNED_ELSEWHERE`, no spawn. Release sólo tras muerte/ACK durable del proceso owned o cancelación explícita con árbol muerto.
- TTL/lease ETCD: rechazado como autoridad de ownership. Takeover automático: prohibido.
- SUPERSEDED por [[2026-09-06-echo-forge-mt5-fencing-and-cancellation-v3]]: el takeover manual con incremento de `fencing_token` deja ventana A+B durante partición y queda prohibido. OPTION A: no cross-host takeover dentro de Symphony.
- HeartbeatTimeout permanece liveness/cancelación cooperativa; no es prueba de muerte física. Retry no spawnea: espera al owner global o reusa HTM durable.
- Singleton OS (mutex nombrado Windows) obligatorio. `ONE_WORKER_PROCESS_PER_MACHINE` se enforcea físicamente. Tras crash+singleton, `KILL_ON_JOB_CLOSE` prueba muerte local y permite recuperar leases stale del epoch anterior.
- Reuso durable: si existe HTM write-once verificado para la identidad exacta (`SourceKey`/`Folder`/`DeriveArtifactKey` + `PutObjectIfAbsent`), ACK antes de rerun.
- NORMAL A local-only anti-duplicate queda `SUPERSEDED / INCOMPLETE` para el invariante de flota. El contrato local de un job por slot permanece válido.

## Rationale

- `IsRetryable` en SDK pinneado marca heartbeat y start-to-close como retryable. `WaitForCancellation` espera completion de cancelación de workflow, no retrasa retries de timeout.
- Heartbeat `NotFound` cancela el context Go de forma cooperativa; no garantiza que `terminal64` ya murió. Completar un attempt timeouteado recibe `NotFound` y se descarta.
- Con `slot_count>1`, `Acquire` toma el primer slot READY y no busca `LogicalJobID` ya owned en la misma máquina: el gap local refuerza que Nivel 1 es obligatorio.
- Un TTL que expire durante partición A↔ETCD permite a B adquirir mientras A sigue corriendo. Persistencia sin TTL sacrifica failover automático (P5) para no sacrificar at-most-one (P2).

## Consecuencias

- NEXT EXACT superseded: ver [[2026-09-06-echo-forge-mt5-fencing-and-cancellation-v3]] (`NORMAL-B1`). No implementar en esta TOP.
- El NORMAL B original (timeout/retry/drain sin ownership global) queda bloqueado y renombrado.
- Host task queues, supervisor durable separado y `MaximumAttempts=1` quedan fuera del slice primario.

## Alternativas descartadas

- TTL ETCD + fencing watchdog: mata un MT5 sano o abre duplicado en partición; viola P1 o P2.
- Colas por host como autoridad primaria: no evitan el spawn del retry si la assignment inicial sigue en cola compartida; complejidad operacional desproporcionada. Pueden ser afinidad posterior.
- Supervisor durable que separe lifetime Activity vs proceso: exige desacoplar Job Object de `KILL_ON_JOB_CLOSE`; exceso para el MVP.
- `MaximumAttempts=1`: evita duplicado de retry pero deja crash/reboot sin recovery automático; no cubre P5.
- PostgreSQL control plane en el worker Windows: CAS existe (`row_version`, `ClaimOutputNamespace`) pero añade dependencia nueva; ETCD ya está en el proceso.
