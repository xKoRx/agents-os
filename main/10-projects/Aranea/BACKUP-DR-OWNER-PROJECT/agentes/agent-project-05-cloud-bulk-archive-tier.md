---
title: "agent-project-05 — Cloud bulk/archive tier (GDrive + rclone crypt)"
type: project
schema_version: 1
owner: agent
root: false
status: paused
status_detail: "Legacy ready, pero no autorizado para ejecución por el owner."
priority: P2
progress: 0
icon: ☁️
slug: agent-project-05-cloud-bulk-archive-tier
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

# ☁️ Agent Project 05: Cloud bulk/archive tier (GDrive + rclone crypt)

## 🎯 Objetivo

Configurar **rclone crypt** sobre GDrive para tier bulk off-site: snapshots ZFS pool0 chunked, datasets grandes (frigate/media, aranea_storage), backups históricos de VMs.

## 📊 Estado actual

- Pausado y listo para ejecución sólo cuando el owner habilite el proyecto padre; ninguna tarea del agente está completada.

## Scope

- Setup rclone remote GDrive.
- Setup rclone crypt sobre GDrive.
- Script de export ZFS chunked con checksums y manifest.
- Script de export de datasets grandes.
- Push monthly + verificación parcial.

## Out of scope

- Tier crítico (ap-04).
- Streaming directo ZFS → GDrive (no efficient, WAN lenta).

## Required inputs

- ap-03 (sanoid snapshots pool0).
- OWNER-TASK-OAUTH-SCOPE.
- OWNER-TASK-SECRET-ZERO (passphrase rclone crypt).

## Required owner permissions

- Cuenta GDrive con espacio (varios TB según F-08).
- OAuth app credentials.

## Required credentials / secrets

- GDrive OAuth client_id + client_secret.
- rclone crypt passphrase (en Secret Zero).
- rclone crypt salt (en Secret Zero).

## Required maintenance window

Push monthly 1° del mes 04:00. Requiere WAN libre.

## Dependencies

- ap-03 (snapshots ZFS).
- OWNER-TASK-OAUTH-SCOPE resuelto.

## Protected resources

pool0 (read-only para `zfs send`). NO modificar.

## Risks

| Riesgo | Mitigación |
|---|---|
| Archivo único > 50 GB causa problemas en GDrive | Chunking obligatorio (recomendado ≤ 8 GB por chunk). |
| WAN lenta corta el push | `--bwlimit` + retry exponencial + `--partial`. |
| rclone crypt passphrase perdida | Secret Zero. |
| Manifest drift (chunks huérfanos) | `restic check` o script propio de validación. |

## Safety gates

- Read-only sobre ZFS source.
- Chunking + manifest + checksums obligatorios.

## Implementation plan

1. Setup rclone GDrive remote (OAuth).
2. Setup rclone crypt sobre `gdrive:/aranea-archive-crypt`.
3. Script `chunk-and-upload-pool0.sh`:
   ```bash
   # Por cada snapshot semanal de pool0/ds:
   SNAP=$(zfs list -t snap -o name -H | grep "pool0/ds@weekly-" | sort | tail -1)
   zfs send -w -c "$SNAP" | split -b 8G - /tmp/chunk-${SNAP//\//_}.part.
   # Genera SHA-256 sidecars y manifest.json
   # rclone copy cada chunk a gdrive-crypt:/pool0-archive/${SNAP}/
   ```
4. Script `upload-datasets.sh` para datasets grandes.
5. Push monthly 1° 04:00.
6. `rclone check` post-push para validar subset.

## Validation plan

- Chunks subidos verificables en GDrive.
- Manifest descargable.
- Restore drill (ap-07) restaura 1 chunk random.

## Rollback plan

- `rclone purge` para borrar subset si falla validación.
- Script idempotente.

## Evidence to collect

- Output de `rclone ls gdrive-crypt:/pool0-archive/`.
- Manifest descargado.
- Ticket cerrado.

## Expected artifacts

- Repo cifrado en GDrive.
- Scripts chunked.
- Cron monthly.
- Ticket ap-05 cerrado.

## Definition of Done

- [ ] rclone crypt setup.
- [ ] Primer chunk de snapshot subido.
- [ ] Manifest válido.
- [ ] Restore drill 1 chunk PASS.

## Linked owner tasks

- OWNER-TASK-OAUTH-SCOPE.
- OWNER-TASK-SECRET-ZERO.

## ✅ Tareas

- [ ] **AGENT-TASK-05-1**: setup rclone GDrive + crypt.
  - tags: [agent, oauth-setup]

- [ ] **AGENT-TASK-05-2**: implementar chunk-and-upload-pool0.sh.
  - tags: [agent, scripting, zfs]

- [ ] **AGENT-TASK-05-3**: implementar upload-datasets.sh.
  - tags: [agent, scripting]

- [ ] **AGENT-TASK-05-4**: configurar cron monthly.
  - tags: [agent, scheduling]

- [ ] **AGENT-TASK-05-5**: implementar rclone check subset.
  - tags: [agent, validation]

---

## Requirements

### Functional requirements
- FR-001: Chunking ≤ 8 GB por chunk.
- FR-002: Manifest JSON con `{chunk, size, sha256, source_snap, created_at}`.
- FR-003: Checksums SHA-256 por chunk.

### Non-functional requirements
- NFR-001: Push nocturno 04:00 con `--bwlimit`.
- NFR-002: `rclone check` post-push.

### Safety requirements
- SAFE-001: Read-only sobre ZFS source.
- SAFE-002: Passphrase en Secret Zero.

### Observability requirements
- OBS-001: Push exit != 0 → warning + reintento.
- OBS-002: `cloud_sync_stale` > 35d → warning.

### Documentation requirements
- DOC-001: Procedimiento restore chunk en BACKUP-DR-RUNBOOK §6.

### Acceptance criteria
- AC-001: 1 chunk subido verificable.
- AC-002: Restore drill 1 chunk PASS.

---

**Status**: ready. NO ejecutado.
**Sesión cerrada por instrucción del owner**: 2026-07-01.

## 📆 Bitácora

- **2026-08-10** — Migrado de `agent-project` legacy a `project` v1 sin activar la ejecución; owner, parent, lifecycle, progress, tags y secciones quedaron contractuales.
