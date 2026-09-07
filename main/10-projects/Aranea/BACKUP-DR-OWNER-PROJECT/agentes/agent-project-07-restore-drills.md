---
title: "agent-project-07 — Restore drills"
type: project
schema_version: 1
owner: agent
root: false
status: paused
status_detail: "Legacy ready, pero no autorizado para ejecución por el owner."
priority: P2
progress: 0
icon: 🔄
slug: agent-project-07-restore-drills
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

# 🔄 Agent Project 07: Restore drills

## 🎯 Objetivo

Implementar calendario de restore drills con criterios PASS/FAIL explícitos. **Backup no es válido sin drill PASS reciente**.

## 📊 Estado actual

- Pausado y listo para ejecución sólo cuando el owner habilite el proyecto padre; ninguna tarea del agente está completada.

## Scope

6 drills definidos en BACKUP-DR-DESIGN §5 Capa G:
1. Restore 1 VM tier 0 desde PBS (mensual).
2. Restore dump PostgreSQL (mensual).
3. Restore dump MongoDB (mensual).
4. Restore Restic repo desde pcloud (trimestral).
5. Restore ZFS chunk desde GDrive (trimestral).
6. Restore step-ca completo (semestral).

## Out of scope

- Disaster recovery test (cluster caído entero).
- Performance benchmarking.

## Required inputs

- ap-01, ap-02, ap-03, ap-04, ap-05 todos completados.

## Required owner permissions

- OWNER-TASK-SECRET-ZERO (passphrases para step-ca drill).
- Aprobación de ventana para drills que requieren reinicio de VM (drill 1).

## Required credentials / secrets

- PBS API token.
- Restic passphrase.
- rclone crypt passphrase.
- step-ca passphrase.

## Required maintenance window

Drill 1 (restore VM) requiere ventana corta (~30 min para boot verification).

## Dependencies

- ap-01..05 done.

## Protected resources

Drill se hace en entorno scratch (no producción). VMs restored se aíslan en VLAN separada o se destruyen después.

## Risks

| Riesgo | Mitigación |
|---|---|
| Drill restaura VM sobre VM productiva | Naming convention `drill-<vmname>-<date>`, no producción. |
| Drill falla por drift (configs cambiaron) | Iterar drill, ajustar scripts, no skip. |
| Drill consume storage | Cleanup post-drill. |

## Safety gates

- Drill SIEMPRE en entorno scratch.
- Cleanup obligatorio post-drill.
- PASS/FAIL registrado en log + ticket.

## Implementation plan

1. Crear `drill-restore-vm-pbs.sh` — automatiza drill 1.
2. Crear `drill-restore-pg.sh` — drill 2.
3. Crear `drill-restore-mongo.sh` — drill 3.
4. Crear `drill-restic-pcloud.sh` — drill 4.
5. Crear `drill-zfs-chunk-gdrive.sh` — drill 5.
6. Crear `drill-stepca-recovery.sh` — drill 6 (requiere owner ejecutarlo).
7. Cron jobs mensuales/trimestrales/semestrales.
8. Logs en `/var/log/aranea-drills/`.
9. Cada drill emite PASS/FAIL a alerting.

## Validation plan

- Cada drill ejecutó al menos 1 ciclo PASS en implementación.
- Drill 6 (step-ca) ejecutado por owner.

## Rollback plan

- Scripts idempotentes.
- Cleanup post-drill.

## Evidence to collect

- Drill logs.
- PASS/FAIL records.
- Tickets cerrados.

## Expected artifacts

- 6 scripts drill.
- Cron jobs.
- Tickets mensuales/trimestrales.
- Drill evidence en Obsidian.

## Definition of Done

- [ ] 6 scripts implementados.
- [ ] Drill 1 PASS en primer intento.
- [ ] Drill 2 PASS.
- [ ] Drill 3 PASS.
- [ ] Drill 4 PASS.
- [ ] Drill 5 PASS.
- [ ] Drill 6 ejecutado por owner PASS.
- [ ] Calendario drills activo.

## Linked owner tasks

- OWNER-TASK-SECRET-ZERO (drill 6).

## ✅ Tareas

- [ ] **AGENT-TASK-07-1**: implementar 6 scripts drill.
  - tags: [agent, drill]

- [ ] **AGENT-TASK-07-2**: configurar cron calendar.
  - tags: [agent, scheduling]

- [ ] **AGENT-TASK-07-3**: ejecutar primer ciclo PASS.
  - tags: [agent, validation]

---

## Requirements

### Functional requirements
- FR-001: 6 drills calendarizados.
- FR-002: PASS/FAIL registrado.

### Non-functional requirements
- NFR-001: Drill en entorno scratch únicamente.
- NFR-002: Cleanup post-drill.

### Safety requirements
- SAFE-001: Naming `drill-*` para evitar confusión con producción.
- SAFE-002: Drill 1 solo si ventana mantenimiento OK.

### Observability requirements
- OBS-001: Drill FAIL → alerta crítica + Request Change automático.

### Documentation requirements
- DOC-001: Cada drill documenta qué mide.

### Acceptance criteria
- AC-001: 6 drills implementados.
- AC-002: Primer ciclo PASS.
- AC-003: Calendario activo.

---

**Status**: ready. NO ejecutado.
**Sesión cerrada por instrucción del owner**: 2026-07-01.

## 📆 Bitácora

- **2026-08-10** — Migrado de `agent-project` legacy a `project` v1 sin activar la ejecución; owner, parent, lifecycle, progress, tags y secciones quedaron contractuales.
