---
type: agent_memory
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
  - "[[2026-09-05-echo-forge-full-golden-flow-continuity]]"
aliases: []
confidence: high
memory_state: active
continuity_key: echo-forge/mt5-slot-pool-long-running-v2
supersedes:
superseded_by:
load_policy: when_project_loaded
indexable: false
index_priority: never
tags:
  - kind/agent-memory
  - agent/internal
  - project/echo-forge
---

# Echo Forge MT5 slot pool + long-running V2

## Continuidad

- NORMAL A PASS / CLOSED y no se revierte. HEAD == origin/master = `a10c26c887e4d203b403d2557e292ed773830b0e`; parent implementation `14899376c4d188cf09b699859426b0763e387b4c`; SDK `c85594440f6755443ceb97ec4e333cd0ddb5b0ed`; deployed release `0.2.96`; foreign dirty preserved.
- La conclusión local-only anti-duplicate de la TOP previa es SUPERSEDED / INCOMPLETE para el invariante de flota. El lease local sigue siendo Nivel 2 válido (un slot → un job local). No prueba un LogicalJobID → un proceso en toda la flota.
- TOP de corrección PASS / CLOSED: `ECHO_FORGE_MT5_GLOBAL_PHYSICAL_OWNERSHIP_V2`. Autoridad = ETCD persistente no-TTL con CAS. TTL rechazado. Takeover automático prohibido. Retry wait-on-owner / OWNED_ELSEWHERE / ACK HTM durable; jamás spawn ciego. Singleton OS obligatorio. Heartbeat no es prueba de muerte.
- Temporal: `IsRetryable` marca HEARTBEAT y START_TO_CLOSE como retryable en SDK `v1.44.1` y `v1.35.0`. Pin de misión `v1.44.1`; módulo `sqx` (binario worker) sigue en `v1.35.0` con la misma semántica. `WaitForCancellation` no altera retries de timeout. Timeout de servidor no mata el proceso OS.
- CacheClient no expone CAS. DI `etcdFull` es privado. NORMAL B debe abrir accessor a `*etcd.Client`/`Txn`. No PostgreSQL en el worker Windows para este contrato.
- El NORMAL B previo `ECHO-FORGE-MT5-LONG-RUNNING-RETRY-DRAIN-V2-NORMAL-B` queda bloqueado y se reemplaza por el nombre revisado.
- Graphify symphony stale (2026-09-03); no reparar. Graphify-obsidian colgó en esta sesión y se mató.

## Señales de carga

- Cargar con [[Echo Forge]] cuando el siguiente trabajo sea ownership global MT5, retry Temporal, drain Windows o certificación 3-slot.

## Próxima acción

- NEXT EXACT: `ECHO-FORGE-MT5-LONG-RUNNING-GLOBAL-OWNERSHIP-RETRY-DRAIN-V2-NORMAL-B`. Do not begin NORMAL B in this session.
