---
title: "agent-project-03 — App-consistent data backups"
type: project
schema_version: 1
owner: agent
root: false
status: paused
status_detail: "Legacy ready, pero no autorizado para ejecución por el owner."
priority: P2
progress: 0
icon: 💾
slug: agent-project-03-app-consistent-data-backups
area: "[[Aranea]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-08-10
tags:
  - kind/project
  - area/aranea
  - project/agents-os
  - agent/owner
  - domain/backup
related:
  - "[[BACKUP-DR-DESIGN]]"
parent: "[[BACKUP-DR-OWNER-PROJECT]]"
cssclasses: wide
---

# 💾 Agent Project 03: App-consistent data backups

## 🎯 Objetivo

Implementar backups app-consistent de PostgreSQL, MongoDB, CouchDB (Obsidian), minio + sanoid policy para ZFS pool0 (truenas) + scripts de dump.

## 📊 Estado actual

- Pausado y listo para ejecución sólo cuando el owner habilite el proyecto padre; ninguna tarea del agente está completada.

## Scope

- `pg_dumpall` (PostgreSQL vm 152).
- `mongodump --oplog` (MongoDB vm 153).
- CouchDB replicación (Obsidian vault lxc 116).
- `mc mirror` (minio vm 157).
- sanoid config en truenas (templates critical/production/backup).

## Out of scope

- Backup externo Ceph (descartado F-10).
- Datasets ZFS off-site (ap-05).
- cloud push (ap-04/05).

## Required inputs

- ap-00, ap-02 done.
- Lista tier 0 (OWNER-TASK-CRITICAL-VMS).
- Conexión a PostgreSQL/MongoDB/CouchDB/minio.

## Required owner permissions

- Acceso SSH a las VMs (152, 153, 116, 157).
- Credenciales DB.
- root truenas para sanoid.

## Required credentials / secrets

- PostgreSQL superuser (en Secret Zero).
- MongoDB admin (en Secret Zero).
- CouchDB admin.
- minio root key.

## Required maintenance window

No estricto. Dumps en madrugada.

## Dependencies

- ap-02 (PBS para staging local).
- OWNER-TASK-SECRET-ZERO (credenciales DB).

## Protected resources

Todos §2. **NO** modificar DBs. Solo lectura/dump.

## Risks

| Riesgo | Mitigación |
|---|---|
| Dump inconsistente en DB en uso | `pg_dump --lock-wait-timeout`, `mongodump --oplog`, CouchDB replicación. |
| Dump muy grande satura PBS | Monitorear tamaño; ajustar retention si > 50% PBS datastore. |
| sanoid policy rompe snapshots existentes | Dry-run primero; sanoid tiene `--readonly`. |
| minio mirror bidireccional causa loop | `mc mirror` unidireccional; documentar. |

## Safety gates

- Dumps son read-only sobre la DB.
- sanoid config se valida con `sanoid --readonly` antes de aplicar.
- minio mirror solo lectura origen.

## Implementation plan

1. **PostgreSQL** (vm 152):
   - Crear `backup-postgres.sh` que corre `pg_dumpall` + `pg_dump --schema` por DB.
   - Comprimir con gzip.
   - Subir a PBS datastore (vía `pvesm` o directamente vía PBS client).
   - Cron 01:00 diario.
2. **MongoDB** (vm 153):
   - `backup-mongo.sh` con `mongodump --oplog --gzip`.
   - PBS upload.
   - Cron 01:30 diario.
3. **CouchDB** (lxc 116):
   - `backup-couchdb.sh` con `_all_dbs` + replicador o dump por DB.
   - PBS upload + pcloud tier critical (cuando ap-04 exista).
   - Cron 00:00 diario.
4. **minio** (vm 157):
   - `backup-minio.sh` con `mc mirror` sobre bucket crítico.
   - PBS upload.
   - Cron 03:00 diario.
5. **sanoid** (truenas):
   - Crear `/etc/sanoid/sanoid.conf` con templates.
   - `sanoid --readonly --verbose` para validar.
   - Activar `autosnap = yes` + `autoprune = yes`.
   - Verificar con `zfs list -t snap`.

## Validation plan

- Cada dump restaura a DB scratch y row/collection count match.
- sanoid genera snapshot según template.
- 7 días continuos sin error.

## Rollback plan

- Disable cron → no dump.
- sanoid policy revertida vía `git` o backup de sanoid.conf (ap-01).
- DBs intactas (dumps read-only).

## Evidence to collect

- Logs de cron.
- Output de restore drill (en ap-07).
- sanoid snapshot listing.
- Ticket cerrado.

## Expected artifacts

- 4 scripts bash.
- sanoid.conf con 3 templates.
- Cron jobs.
- Tickets de restore drill mensuales.

## Definition of Done

- [ ] 4 scripts + sanoid policy implementados.
- [ ] 7 días continuos de dumps exitosos.
- [ ] Restore drill PASS (ap-07) de al menos 1 dump.
- [ ] sanoid snapshots según template.

## Linked owner tasks

- OWNER-TASK-CRITICAL-VMS (cuales DBs son tier 0).
- OWNER-TASK-SECRET-ZERO (credenciales DB).

## ✅ Tareas

- [ ] **AGENT-TASK-03-1**: implementar backup-postgres.sh.
  - target_system: vm 152 (hades).
  - tags: [agent, dump]

- [ ] **AGENT-TASK-03-2**: implementar backup-mongo.sh.
  - target_system: vm 153 (hades).
  - tags: [agent, dump]

- [ ] **AGENT-TASK-03-3**: implementar backup-couchdb.sh.
  - target_system: lxc 116.
  - tags: [agent, dump]

- [ ] **AGENT-TASK-03-4**: implementar backup-minio.sh.
  - target_system: vm 157 (hades).
  - tags: [agent, dump]

- [ ] **AGENT-TASK-03-5**: configurar sanoid en truenas.
  - target_system: truenas VM.
  - commands_allowed: write_file en `/etc/sanoid/`, `sanoid --readonly`.
  - tags: [agent, sanoid]

- [ ] **AGENT-TASK-03-6**: configurar cron jobs para los 4 dumps.
  - tags: [agent, scheduling]

---

## Requirements

### Functional requirements
- FR-001: Cada dump encriptado y verificable.
- FR-002: sanoid genera snapshots según template.

### Non-functional requirements
- NFR-001: Dumps paralelos donde sea posible (PG primero, Mongo después).

### Safety requirements
- SAFE-001: Read-only sobre DBs.
- SAFE-002: sanoid `--readonly` validar antes de activar.

### Observability requirements
- OBS-001: Dump exit 0 → log INFO. != 0 → log ERROR + alerta crítica.

### Documentation requirements
- DOC-001: Cada script documenta restore.

### Acceptance criteria
- AC-001: Restore drill PG PASS.
- AC-002: Restore drill Mongo PASS.
- AC-003: sanoid snapshots según template después de 7 días.

---

**Status**: ready. NO ejecutado.
**Sesión cerrada por instrucción del owner**: 2026-07-01.

## 📆 Bitácora

- **2026-08-10** — Migrado de `agent-project` legacy a `project` v1 sin activar la ejecución; owner, parent, lifecycle, progress, tags y secciones quedaron contractuales.
