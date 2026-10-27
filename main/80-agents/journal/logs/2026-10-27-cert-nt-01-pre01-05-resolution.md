---
type: change_log
schema_version: 1
scope: session
created: "2026-10-27"
updated: "2026-10-27"
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

# 2026-10-27 — CERT-NT-01: resolución PRE-01..05 pre-ventana (SHA 5a0cf62f)

## Qué cambió

- Repo `xKoRx/echo` `feature/ef-runtime-pools`: commit `5a0cf62f` (FF sobre `4a041e6c`, push REMOTE_VERIFIED) — PRE-01 guard honesto (`legacy_state_present` + `EconomicEvidence` + `MigrationEvidenceError` + split en summaries + `Validate`), subcomando `expected-roster`, PRE-04 `seal --cut-kind savepoint` + seam `LatestCompletedSavepoint(+Time)` + manifest `cut_kind`, usage doc completo (cierra D-5). 13 archivos, +537/−43.
- Release inmutable `/home/kor/opt/echo-dev/releases/5a0cf62f8ddbffa0a4926d1c1883085be7b87b6d/` (echo-core `3f044d4e…`, echo-runtime-control `411e55cc…`, sonda `c84ca495…` sin cambios; vcs.modified=false) — sin repoint de `current`.
- Vault: [[WINDOW-CARD-PRD6]] reescrita como TARJETA ÚNICA con la decisión Manager PRE-01..05 verbatim + resolución por enmienda + GO/NO-GO G0-G11 (saveport-first) + solicitud de autorización condicionada (readback sha256 `be5094c081a8e0a7dee2aea84e414bf81dae666190d864da14640cb1f5c8315c`, validador 0 errores); bitácora del planner (entrada 2026-10-27); agent-run `2026-10-27-zcode-glm53-cert-nt-01-pre01-05.md`.
- Workspace: `~/aranea/work/ef-prd6-20261026/evidence/roster-dev-5a0cf62f.json` (roster DEV derivado de ETCD, sha256 `417d77d1…`).

## Qué NO cambió

- Cero mutaciones de runtime: job `0f6901a3` RUNNING sin restore; module/flink-conf/compose/ETCD/Kafka DEV intactos; topic attest NO creado; Core `ac062a1` sin repoint; PROD cero escrituras; cinco capas de desarme idénticas. La prueba de relay PRE-02 y el `docker inspect` PRE-05 quedaron bloqueados por la expiración del servidor MCP `aranea-ssh` (receta exacta en G0 de la tarjeta; requiere reinicialización del host).

## Fuentes

- [[WINDOW-CARD-PRD6]], [[EF-PROD-PRD6-MANAGER-ADJUDICATION-20261026]], planner [[Echo Futures — Runtime Pools]], [[OWNER-CHECKLIST-CERT-NT-01]].
