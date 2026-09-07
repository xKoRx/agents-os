---
title: "agent-project-04 — Cloud critical tier (pcloud + Restic)"
type: project
schema_version: 1
owner: agent
root: false
status: paused
status_detail: "Legacy ready, pero no autorizado para ejecución por el owner."
priority: P2
progress: 0
icon: 🔐
slug: agent-project-04-cloud-critical-tier
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

# 🔐 Agent Project 04: Cloud critical tier (pcloud + Restic)

## 🎯 Objetivo

Configurar **Restic** sobre backend pcloud (cifrado AES-256 nativo de Restic) para tier crítico off-site: configs (Capa A) + dumps DB (Capa B subset pequeño) + manifests + runbooks. **NO** para bulk.

## 📊 Estado actual

- Pausado y listo para ejecución sólo cuando el owner habilite el proyecto padre; ninguna tarea del agente está completada.

## Scope

- Crear cuenta servicio pcloud dedicada (o usar owner account, decisión owner).
- Setup Restic repo sobre pcloud vía rclone backend.
- Push weekly: configs + dumps críticos + manifests.
- `restic check` weekly.
- Retention policy declarativa.

## Out of scope

- Tier bulk (ap-05).
- Restic sobre rclone crypt separado (Restic ya cifra nativo).

## Required inputs

- ap-01 (configs staging local).
- ap-03 (dumps DB staging local).
- OWNER-TASK-OAUTH-SCOPE (agente o owner OAuth).
- OWNER-TASK-SECRET-ZERO (passphrase Restic).

## Required owner permissions

- Cuenta pcloud con espacio (1 TB según F-08).
- OAuth app credentials (creadas por owner o agente según decisión).

## Required credentials / secrets

- pcloud OAuth client_id + client_secret (en Secret Zero).
- Restic repo passphrase (en Secret Zero).

## Required maintenance window

No estricto.

## Dependencies

- ap-01, ap-03 staging.
- OWNER-TASK-OAUTH-SCOPE resuelto.

## Protected resources

Ninguno tocado en infraestructura del cluster.

## Risks

| Riesgo | Mitigación |
|---|---|
| pcloud OAuth scope muy amplio | Usar dedicated app, mínimo scope (files读写). |
| Restic passphrase perdida | Secret Zero + escrow. |
| pcloud rate limit | `--limit-upload` y horario nocturno. |
| Push falla silencioso | `restic check` weekly + alerta si stale > 8d. |

## Safety gates

- Restic cifrado nativo. Sin cifrado adicional necesario.
- Passphrase en Secret Zero.

## Implementation plan

1. Setup rclone remote pcloud (OAuth — owner o agente según decisión).
2. Setup Restic repo:
   ```bash
   restic -r rclone:pcloud:/aranea-restic init
   ```
3. Script `backup-to-pcloud.sh`:
   - Snapshot configs desde `/opt/aranea-backup/config/`.
   - Snapshot dumps DB desde staging PBS o local.
   - Snapshot manifests desde `30-resources/aranea/`.
   - Snapshot runbooks desde Obsidian export.
4. Retention policy: `--keep-daily 7 --keep-weekly 4 --keep-monthly 12`.
5. Cron weekly Sun 03:00.
6. `restic check` weekly post-push.

## Validation plan

- `restic snapshots` lista al menos 1 snapshot.
- `restic check` PASS.
- Restore drill (ap-07) restaura subset de configs.

## Rollback plan

- `restic forget --prune` para borrar repo si es necesario.
- Disable cron.

## Evidence to collect

- `restic snapshots` output.
- `restic check` log.
- Ticket cerrado.

## Expected artifacts

- Repo Restic en pcloud.
- Script `backup-to-pcloud.sh`.
- Cron job.
- Ticket ap-04 cerrado.

## Definition of Done

- [ ] Repo Restic inicializado.
- [ ] Al menos 4 snapshots continuos.
- [ ] `restic check` PASS.
- [ ] Restore drill subset configs PASS.

## Linked owner tasks

- OWNER-TASK-OAUTH-SCOPE.
- OWNER-TASK-SECRET-ZERO.

## ✅ Tareas

- [ ] **AGENT-TASK-04-1**: setup rclone pcloud remote.
  - tags: [agent, oauth-setup]

- [ ] **AGENT-TASK-04-2**: init Restic repo.
  - tags: [agent, restic]

- [ ] **AGENT-TASK-04-3**: implementar backup-to-pcloud.sh.
  - tags: [agent, scripting]

- [ ] **AGENT-TASK-04-4**: configurar cron + restic check.
  - tags: [agent, scheduling]

---

## Requirements

### Functional requirements
- FR-001: Restic cifrado nativo AES-256.
- FR-002: Retention policy aplicada.
- FR-003: `restic check` weekly.

### Non-functional requirements
- NFR-001: Push en horario nocturno (WAN lenta).
- NFR-002: `--limit-upload` rate limit.

### Safety requirements
- SAFE-001: Passphrase en Secret Zero.

### Observability requirements
- OBS-001: `restic check` exit != 0 → alerta crítica.
- OBS-002: `cloud_sync_stale` > 8d → warning.

### Documentation requirements
- DOC-001: Procedimiento restore en BACKUP-DR-RUNBOOK §5.

### Acceptance criteria
- AC-001: 4 snapshots continuos en Restic repo.
- AC-002: Restore drill subset PASS.

---

**Status**: ready. NO ejecutado.
**Sesión cerrada por instrucción del owner**: 2026-07-01.

## 📆 Bitácora

- **2026-08-10** — Migrado de `agent-project` legacy a `project` v1 sin activar la ejecución; owner, parent, lifecycle, progress, tags y secciones quedaron contractuales.
