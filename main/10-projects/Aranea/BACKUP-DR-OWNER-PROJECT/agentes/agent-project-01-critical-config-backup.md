---
title: "agent-project-01 — Critical config backup"
type: project
schema_version: 1
owner: agent
root: false
status: paused
status_detail: "Legacy ready, pero no autorizado para ejecución por el owner."
priority: P2
progress: 0
icon: 📂
slug: agent-project-01-critical-config-backup
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

# 📂 Agent Project 01: Critical config backup

## 🎯 Objetivo

Implementar backup de configuración crítica (Capa A de BACKUP-DR-DESIGN §5.1) hacia PBS (cuando esté listo en ap-02) + staging local. NO toca PBS hasta que ap-02 esté done.

## 📊 Estado actual

- Pausado y listo para ejecución sólo cuando el owner habilite el proyecto padre; ninguna tarea del agente está completada.

## Scope

- /etc/pve (todos los nodos).
- /etc/network/interfaces.
- Traefik dynamic configs.
- step-ca backup (script wrapper).
- etcd snapshot (script wrapper).
- Inventario (markdown + JSON).
- sanoid.conf.
- Runbooks críticos.

## Out of scope

- PBS storage (ap-02).
- rclone cloud push (ap-04/05).
- OPNsense export XML (requiere owner export manual).

## Required inputs

- ap-00 done.
- BACKUP-DR-DESIGN §5.1 tabla.

## Required owner permissions

- Lectura `/etc/pve`, `/etc/network/interfaces`, `/etc/traefik/`, `/etc/sanoid/`, `/etc/step-ca/`.
- Step-ca backup passphrase (de Secret Zero, OWNER-TASK-SECRET-ZERO pendiente).
- Aprobación ventana para etcd snapshot (no rompe nada, pero requiere quorum estable).

## Required credentials / secrets

- step-ca backup passphrase (referencia a Secret Zero).
- etcd client cert/key (en /etc/etcd).

## Required maintenance window

No estricto. Cron jobs se configuran y validan en horas de bajo uso (madrugada).

## Dependencies

- ap-00 (cleanup).
- ap-02 (PBS debe existir para destino local definitivo; mientras tanto, staging local).

## Protected resources

Todos los §2 BACKUP-DR-DESIGN. NO tocar.

## Risks

| Riesgo | Mitigación |
|---|---|
| Backup de /etc/pve interrumpe PVE API | Hacer en ventana nocturna, verificar antes. |
| step-ca backup sin passphrase | Bloqueado por OWNER-TASK-SECRET-ZERO. |
| Inventario stale | Script diario genera snapshot del estado. |

## Safety gates

- Backup NO modifica archivos originales.
- Diff visible antes/después en smoke test.

## Implementation plan

1. Crear `/opt/aranea-backup/` con subdirs `config/`, `etcd/`, `step-ca/`, `inventory/`, `runbooks/`.
2. Crear scripts wrapper:
   - `backup-etc-pve.sh` — `tar czf /opt/aranea-backup/config/etc-pve-$(date +%Y%m%d).tgz /etc/pve`.
   - `backup-traefik.sh` — `tar czf /opt/aranea-backup/config/traefik-$(date +%Y%m%d).tgz /etc/traefik/`.
   - `backup-stepca.sh` — invoca `step ca backup` + cifra con passphrase Secret Zero.
   - `backup-etcd.sh` — `etcdctl snapshot save /opt/aranea-backup/etcd/etcd-$(date +%Y%m%d).db`.
   - `backup-inventory.sh` — copia `backup-inventory-template.json` con timestamp.
   - `backup-sanoid-config.sh` — copia `/etc/sanoid/sanoid.conf`.
   - `backup-runbooks.sh` — `tar czf /opt/aranea-backup/runbooks/...tgz` desde Obsidian export.
3. Crear cron jobs en hermes-vm (o PBS VM cuando exista).
4. Smoke test: cada script genera archivo esperado y verifica con `tar tzf` o `etcdctl snapshot status`.
5. Configurar retención local: 30 días (`find -mtime +30 -delete`).

## Validation plan

- Cada script genera archivo verificable.
- Smoke test manual en ventana de prueba.
- Cron logs en `/var/log/aranea-backup/`.
- Restore drill (ap-07) verifica end-to-end.

## Rollback plan

- Scripts idempotentes. Disable cron → no backup.
- Archivos staging son nuevos, no afectan nada.

## Evidence to collect

- Logs de cron jobs.
- Output de `ls -la /opt/aranea-backup/`.
- Output de smoke test.
- Ticket cerrado.

## Expected artifacts

- 7 scripts bash.
- Cron jobs configurados.
- Staging local `/opt/aranea-backup/`.
- Ticket ap-01 cerrado.

## Definition of Done

- [ ] 7 scripts implementados y testeados.
- [ ] Cron jobs activos y verificados por al menos 7 días.
- [ ] Staging local poblado.
- [ ] Sin errores en logs.
- [ ] Smoke test PASS.

## Linked owner tasks

- OWNER-TASK-SECRET-ZERO (passphrase step-ca).

## ✅ Tareas

- [ ] **AGENT-TASK-01-1**: crear estructura `/opt/aranea-backup/`.
  - target_system: PBS VM (futuro) o hermes-vm (temporal).
  - commands_allowed: mkdir, chown.
  - commands_forbidden: ninguno destructivo.
  - tags: [agent, setup]

- [ ] **AGENT-TASK-01-2**: implementar 7 scripts wrapper.
  - commands_allowed: write_file, chmod +x.
  - expected_output: 7 archivos `.sh` ejecutables.
  - tags: [agent, scripting]

- [ ] **AGENT-TASK-01-3**: configurar cron jobs.
  - commands_allowed: crontab, write_file en /etc/cron.d/.
  - tags: [agent, scheduling]

- [ ] **AGENT-TASK-01-4**: smoke test end-to-end.
  - commands_allowed: bash.
  - validation: cada script exit 0 + archivo generado verificable.
  - tags: [agent, validation]

- [ ] **AGENT-TASK-01-5**: configurar retención 30d.
  - tags: [agent, retention]

---

## Requirements

### Functional requirements
- FR-001: Cada elemento de Capa A cubierto por script específico.
- FR-002: Cron ejecuta a las horas definidas en BACKUP-DR-DESIGN §6.2.

### Non-functional requirements
- NFR-001: Scripts idempotentes y read-only sobre origen.
- NFR-002: Logs estructurados.

### Safety requirements
- SAFE-001: Sin comandos destructivos.
- SAFE-002: step-ca backup cifrado con passphrase Secret Zero.

### Observability requirements
- OBS-001: Cada script exit 0 → log INFO. Exit != 0 → log ERROR + alerta.

### Documentation requirements
- DOC-001: Scripts con header `# Description`, `# Usage`, `# Restores`.

### Acceptance criteria
- AC-001: 7 días continuos de cron jobs sin fallos.
- AC-002: Smoke test restaura un /etc/pve desde staging.
- AC-003: step-ca backup se restaura y verifica (`step ca verify`).

---

**Status**: ready. NO ejecutado.
**Sesión cerrada por instrucción del owner**: 2026-07-01.

## 📆 Bitácora

- **2026-08-10** — Migrado de `agent-project` legacy a `project` v1 sin activar la ejecución; owner, parent, lifecycle, progress, tags y secciones quedaron contractuales.
