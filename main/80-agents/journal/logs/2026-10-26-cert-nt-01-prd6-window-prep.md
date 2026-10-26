---
type: change_log
schema_version: 1
scope: session
created: "2026-10-26"
updated: "2026-10-26"
area: "[[Echo]]"
project: "[[Echo Futures — Runtime Pools]]"
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
  - project/echo-futures
  - area/echo
---

# 2026-10-26 — CERT-NT-01 fase 0 PRD.6: preparación de ventana sin restart

## Qué cambió

- Nuevo documento canónico `10-projects/Echo Futures/artifacts/runtime/production-readiness/implementation-evidence/WINDOW-CARD-PRD6.md` (tarjeta final de ventana Owner materializada según la adjudicación PRD.6: release `4a041e6c` con hashes, estado PRE-VENTANA verificado, inventario de los 17 ingresses con offsets muestreados, GO/NO-GO G1-G11, P0-P10, NO-GO parciales, R1/R2 y cinco capas de desarme; readback sha256 `e40e793c68ef45789817c2bbcda4d369630668cabb2eb6ba3c9a762432fd97f9`, validador de schema 0 errores).
- Planificador [[Echo Futures — Runtime Pools]]: entrada de bitácora 2026-10-26 con el estado de fase 0 y los tres huecos P4 (roster DEV, ruta de copia G5, topic attest).
- Registro de agent-run `80-agents/journal/agent-runs/2026-10-26-zcode-glm53-cert-nt-01-prd6-window-prep.md`.

## Qué NO cambió

- Cero mutaciones de infraestructura: el job DEV `0f6901a3` sigue RUNNING sin restore; module.yaml, flink-conf, compose, ETCD DEV, Kafka DEV y Core (`ac0621a1`) intactos; PROD sólo lecturas RO; ningún arming (cinco capas de desarme idénticas a PRE).
- Release nuevo sólo en `/home/kor/opt/echo-dev/releases/4a041e6cf17b27a023a1a693a48be1034c35e7dd/` (sin repoint de `current`); único efecto físico fuera del vault: directorio `/srv/echo-work/ef-recovery/prd6-20261026/` pre-creado en .161 (preparación de savepoint target autorizada por la adjudicación).

## Fuentes

- [[EF-PROD-PRD6-MANAGER-ADJUDICATION-20261026]], [[WINDOW-CARD-PRD6]], [[Echo Futures — Runtime Pools]], [[OWNER-CHECKLIST-CERT-NT-01]].
