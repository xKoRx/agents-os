---
type: change_log
schema_version: 1
scope: session
created: "2026-09-20"
updated: "2026-09-20"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
application:
entities:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[agent-project-03-app-consistent-data-backups]]"
related:
  - "[[BACKUP-DR-CONTRACT]]"
aliases:
  - "MP-01 A3 skip CouchDB 2026-09-20"
confidence: high
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/aranea
---

# 2026-09-20-mp01-a3-skip-couchdb

%% Mandato MP-01: cláusula preflight 4 — si CouchDB requiere credencial nueva → SKIP A3 con registro, sin bloquear A0/A1/A5. %%

## Cambio

- **Tipo:** documentation (cero mutaciones de infra en este WP)

## Resultado

- SKIP A3: CouchDB 116 (LXC obsidian-sync, hades, IP real 192.168.31.32 — .116 es el VMID) accesible :5984 desde hermes pero responde `unauthorized` en `/` y `/_all_dbs`; no hay credencial en custodia agente (~/aranea/secrets/ = r0d-g1a, r0d-g1b, truenas).
- Contenido del vault (lo importante) NO queda desprotegido: unidad `second-brain` (R1, VERIFIED, diario 04:00) + ingesta PBS `host/r0d-config-r1` desde MP-01. A3 protege la BD viva del sync (couchdb server state), no el contenido del vault.
- Bundle de desbloqueo: `~/aranea/work/mp01-20260920/BUNDLE-A3-SKIP-couchdb.md` — única acción owner: credencial dedicada RO (`_reader` en DBs replicator) entregada por custodia; con eso A3 = ~30 min con patrón A1 ya operativo.

## Evidencia

`~/aranea/work/mp01-20260920/BUNDLE-A3-SKIP-couchdb.md` · PREFLIGHT.md §4.
