---
type: change_log
schema_version: 1
scope: session
created: "2026-08-21"
updated: "2026-08-21"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
  - "[[Echo Forge]]"
related: []
aliases: []
confidence: verified
source_session: "SESSION PHYSICAL-SQX-LOCK-PORTABILITY-FIX-NORMAL"
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# Physical SQX lock portability fix normal

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** created + updated
- **Archivo(s):** repo `xKoRx/symphony` commit `b80f1bca15089324f4b471a2b661b42f3b395495`; project checkpoint append-only; agent-run registration.

## Motivo

- Se cerró el blocker de build Windows/shared-package sin modificar durable data model, identity, Ranking, Classification, WFM domain, Apply domain, deployment scripts, stager o E2E.

## Fuentes usadas

- `wfm_durable_physical_lock.go` y `durable_apply_selected_run_lock.go` dejaron de importar `unix` directamente; ambos reutilizan `acquirePhysicalFileLock` con implementaciones Unix `Flock` y Windows `LockFileEx` reales.

## Resolución aplicada

- Antes: host/Linux PASS y Windows MT5 FAIL por símbolos `unix.Flock`, `LOCK_*`, `EAGAIN` y `EWOULDBLOCK`; después: host/Linux/Windows y los tres builds oficiales simulados PASS; tests focalizados, vet y diff check PASS; push y HEAD remoto PASS.

## Validación

- 

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Revertir `b80f1bca15089324f4b471a2b661b42f3b395495` si el owner invalida el primitive; no retirar el checkpoint histórico previo.
