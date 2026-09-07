---
type: known_error
schema_version: 1
scope: application
created: "2026-08-13"
updated: "2026-08-13"
area: "[[Echo]]"
project: "[[Stager - Cross-Platform Deployment Lifecycle]]"
application: "[[stager-app]]"
entities:
  - "[[stager-app]]"
  - "[[Symphony]]"
related:
  - "[[Echo Forge]]"
  - "[[stager-windows-occupieddrain-delay-misses-started]]"
aliases:
  - Temporal Started no durable MT5 compile
  - heartbeat first tick 6s
confidence: verified
source_session: b0ed3608-24c7-460f-85e5-9415cc34d06a
load_policy: when_error_matches
indexable: true
index_priority: high
tags:
  - kind/known-error
  - scope/application
  - area/echo
  - app/stager
  - tech/temporal
---

# stager-mt5-heartbeat-late-started

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Síntoma

- Matching Temporal muestra `LastFailure` / `LastWorkerIdentity` pero `workflow show` se queda en `ActivityTaskScheduled` sin `ActivityTaskStarted`.
- OccupiedDrain operativo (MetaEditor visible + `Stop-Service`) no cierra G3.

## Causa

- `StartHeartbeat` esperaba el primer tick (`sqx/activity/heartbeat_seconds`, default 6s). Compile MetaEditor muere en ~1–4s: cero heartbeats, Started no durable.

## Impacto

- F3.6 se declara FAIL aunque el drain SCM sea correcto. Reintentos de OccupiedDrain no cuentan.

## Detección

- History del child `mt5-compile-*` sin evento `ActivityTaskStarted` y matching con worker identity.
- Binario Windows sha256 distinto de `fc9895b6a855010f8390e461c3f2a5aeecb69caf3c9789e2e75d4dfb159e7a0e` puede ser el worker viejo.

## Mitigación

- `StartHeartbeat` debe `RecordHeartbeat` inmediato si `activity.IsActivity(ctx)` (worker `fc9895b6…` en `f33-lifecycle`).
- No tratar compile Failed como OccupiedDrain. Gate: Started en history solapado con `Stop-Service` y cero `ActivityTaskCanceled`.

## Evidencia

- [[2026-08-13-2300-stager-g3-occupieddrain-close-summary]] — PASS `f36-occ-4d05494c` Started 02:53:28Z tras cutover del worker con heartbeat al start.
