---
title: "agent-project-02 — PBS on backup node"
type: project
schema_version: 1
owner: agent
root: false
status: paused
status_detail: "Legacy ready, pero no autorizado para ejecución por el owner."
priority: P2
progress: 0
icon: 🖥️
slug: agent-project-02-pbs-on-backup-node
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

# 🖥️ Agent Project 02: PBS on backup node

## 🎯 Objetivo

Crear VM Proxmox Backup Server en kronos, con datastore sobre `local-kronos` (SSD Samsung 870 QVO 680 GB libre), 8 GB RAM, 4 vCPU, ISO PBS 4.x sobre Debian 12. Registrar storage en los 5 PVE nodes.

## 📊 Estado actual

- Pausado y listo para ejecución sólo cuando el owner habilite el proyecto padre; ninguna tarea del agente está completada.

## Scope

- Crear VM vmid 180 en kronos.
- Install PBS sobre ISO.
- Configurar datastore `main` sobre `local-kronos`.
- Crear user `backup@pbs`.
- Registrar storage `aranea-pbs` en los 5 PVE nodes (athena, zeus, hera, kronos, hades).
- Configurar vzdump schedule diario (tier 0) + semanal (tier 1/2).

## Out of scope

- PBS datastore encryption (F-07 simple default, encryption opcional futuro).
- Cloud push (ap-04).
- Observabilidad integración (ap-06).

## Required inputs

- ap-00 done.
- ap-01 staging (no obligatorio, pero ayuda validación).
- OWNER-TASK-CRITICAL-VMS (lista tier 0).
- OWNER-TASK-MAINT-WINDOW (ventana para crear VM).
- OWNER-TASK-SECRET-ZERO (passphrase datastore).

## Required owner permissions

- Crear VM en kronos (root kronos).
- Acceder PVE UI de los 5 nodes para registrar storage.
- Passphrase datastore (referencia Secret Zero).

## Required credentials / secrets

- PBS API token (generado en setup).
- root PVE de los 5 nodes (registrar storage requiere escribir `/etc/pve/storage.cfg`).

## Required maintenance window

SÍ. Crear VM en kronos interrumpe brevemente el nodo. Usar OWNER-TASK-MAINT-WINDOW.

## Dependencies

- ap-00 done.
- OWNER-TASK-MAINT-WINDOW resuelto.

## Protected resources

| Recurso | Protección |
|---|---|
| `local-sqx-kronos` | SAGRADO. NO TOCAR. PBS datastore va en `local-kronos` (distinto). |
| Ceph MON/MGR de kronos | NO interrumpir quorum al crear VM. |

## Risks

| Riesgo | Mitigación |
|---|---|
| VM PBS muy grande para kronos | 4 vCPU + 8 GB es conservador. kronos tiene 80t + 251 GB libres. |
| PBS datastore crece sin control | Retention policy desde el inicio. Monitorear 80% threshold. |
| Passthrough vs virtio disk | Virtio (default). Passthrough solo si performance issue. |
| Registro storage en 5 nodes requiere escribir en cluster file | Coordinar; cambios en `/etc/pve/storage.cfg` se replican automáticamente. |

## Safety gates

- Ventana de mantenimiento confirmada.
- Snapshot pre-cambio de kronos (si tiene VMs productivas que puedan afectarse, NO debería).
- Diff visible antes de commit storage.cfg.

## Implementation plan

1. **Pre-flight**:
   - Validar `local-kronos` libre (~680 GB en `sdb` de kronos).
   - Descargar ISO PBS 4.x a `/var/lib/vz/template/iso/`.
2. **Crear VM**:
   ```bash
   # DANGEROUS: requiere OWNER-TASK-MAINT-WINDOW
   qm create 180 --name pbs-kronos --memory 8192 --cores 4 --sockets 1 \
     --net0 virtio,bridge=vmbr0 --scsihw virtio-scsi-pci \
     --scsi0 local-lvm:32,iothread=1 --ide2 local:iso/proxmox-backup-server_4.x.iso,media=cdrom \
     --boot order=ide2 --ostype l26
   ```
3. **Install PBS**: interactivo vía noVNC.
4. **Post-install**:
   ```bash
   # Crear datastore sobre local-kronos (montar /dev/pve/local-kronos-vm--180--disk--1 en /backup/main)
   proxmox-backup-manager datastore create main --path /backup/main \
     --prune-backups keep-daily=7,keep-weekly=4,keep-monthly=12
   proxmox-backup-manager user create backup@pbs --comment "PBS backup user"
   proxmox-backup-manager user update backup@pbs --password <STRONG>
   ```
5. **Registrar storage en 5 PVE nodes**:
   ```bash
   # En cada uno de athena, zeus, hera, kronos, hades:
   pvesm add pbs aranea-pbs --server 192.168.31.180 --datastore main \
     --username backup@pbs --password <STRONG> \
     --content backup --prune-backups keep-daily=7,keep-weekly=4,keep-monthly=12
   ```
6. **Schedule vzdump**:
   - Daily 02:00 — tier 0 (lista OWNER-TASK-CRITICAL-VMS).
   - Weekly Sat 02:00 — tier 1/2.
7. **Smoke test**: `vzdump` manual de 1 VM tier 0.

## Validation plan

- `qm status 180` running.
- PBS UI accesible en https://192.168.31.180:8007.
- Datastore `main` muestra chunks.
- `pvesm status` en los 5 nodes muestra `aranea-pbs` active.
- `vzdump` manual de VM tier 0 aparece en PBS.

## Rollback plan

- `qm stop 180 && qm destroy 180` (DANGEROUS, requiere re-aprobación si ya hay data).
- `pvesm remove aranea-pbs` en los 5 nodes.
- PBS datastore queda en `local-kronos`. Re-format si se requiere.

## Evidence to collect

- `qm config 180` output.
- PBS UI screenshot (datastore populated).
- `pvesm status` de los 5 nodes.
- vzdump log de smoke test.
- Ticket cerrado.

## Expected artifacts

- VM 180 corriendo en kronos.
- Datastore PBS operativo.
- 5 storages registrados.
- Schedules vzdump configurados.
- Ticket ap-02 cerrado.

## Definition of Done

- [ ] VM PBS creada y operativa.
- [ ] Datastore `main` con chunks reales.
- [ ] 5 nodes registran storage sin error.
- [ ] vzdump manual PASS.
- [ ] Schedules activos.

## Linked owner tasks

- OWNER-TASK-MAINT-WINDOW (ventana creación VM).
- OWNER-TASK-CRITICAL-VMS (lista tier 0).
- OWNER-TASK-SECRET-ZERO (passphrase).

## ✅ Tareas

- [ ] **AGENT-TASK-02-1**: descargar ISO PBS a kronos.
  - commands_allowed: wget, curl.
  - tags: [agent, prep]

- [ ] **AGENT-TASK-02-2**: crear VM 180 (DANGEROUS — requiere ventana).
  - commands_allowed: `qm create`.
  - commands_forbidden: cualquier `qm destroy` sin re-aprobación.
  - tags: [agent, dangerous, vm-create]

- [ ] **AGENT-TASK-02-3**: install PBS via ISO.
  - requiere noVNC, NO automatizable. Owner-driven o session interactiva.
  - tags: [agent, install, owner-interactive]

- [ ] **AGENT-TASK-02-4**: configurar datastore + user PBS.
  - commands_allowed: `proxmox-backup-manager`.
  - tags: [agent, config]

- [ ] **AGENT-TASK-02-5**: registrar storage en 5 nodes.
  - commands_allowed: `pvesm add`.
  - tags: [agent, registration]

- [ ] **AGENT-TASK-02-6**: configurar schedules vzdump.
  - tags: [agent, scheduling]

- [ ] **AGENT-TASK-02-7**: smoke test vzdump manual tier 0.
  - tags: [agent, validation]

---

## Requirements

### Functional requirements
- FR-001: VM PBS en kronos, datastore sobre `local-kronos`.
- FR-002: 5 PVE nodes registran storage.
- FR-003: Schedules vzdump tier 0 diarios + tier 1/2 semanales.

### Non-functional requirements
- NFR-001: PBS 8 GB RAM (F-07).
- NFR-002: Retention 7d + 4w + 12m (configurable después).

### Safety requirements
- SAFE-001: VM creation requiere ventana mantenimiento.
- SAFE-002: Passphrase datastore en Secret Zero.

### Observability requirements
- OBS-001: PBS verify semanal.
- OBS-002: PBS datastore % usage alert > 80%.

### Documentation requirements
- DOC-001: PBS runbook en BACKUP-DR-RUNBOOK §4.

### Acceptance criteria
- AC-001: vzdump de 1 VM tier 0 restaura correctamente.
- AC-002: Schedules ejecutan por 7 días sin error.
- AC-003: PBS datastore < 50% después de 7 días.

---

**Status**: ready. NO ejecutado.
**Sesión cerrada por instrucción del owner**: 2026-07-01.

## 📆 Bitácora

- **2026-08-10** — Migrado de `agent-project` legacy a `project` v1 sin activar la ejecución; owner, parent, lifecycle, progress, tags y secciones quedaron contractuales.
