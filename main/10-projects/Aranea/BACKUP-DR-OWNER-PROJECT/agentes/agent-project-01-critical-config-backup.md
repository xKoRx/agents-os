---
title: "agent-project-01 — Critical config backup"
type: project
schema_version: 1
owner: agent
root: false
status: in-progress
status_detail: "IN-PROGRESS tras reconciliación D0 (2026-09-17): R1 certificó 3/6 unidades Capa A (traefik-config, second-brain, hermes-state) con BACKUP+RESTORE_VERIFIED y drills a scratch; 3 SKIPPED_GATED con deuda owner acotada (pve-config, etcd-snapshot, pihole-config); automatización pendiente (wrapper manual sin timer/pruning — no es operativa). Detalle: change_log 2026-09-17-backup-dr-r1-bootstrap-config."
priority: P2
progress: 65
icon: 📂
slug: agent-project-01-critical-config-backup
area: "[[Aranea]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-09-17
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

Reconciliado contra evidencia R1 (2026-09-17; change log `2026-09-17-backup-dr-r1-bootstrap-config`):

| Unidad Capa A | Estado | Evidencia / gap |
|---|---|---|
| traefik-config | ✅ BACKUP_VERIFIED + RESTORE_VERIFIED | tar cz vía `agent_traefik` (LXC 115); drill sha256 8/8 vs fuente viva. Gap root-only: `secrets/ ssl/ acme.json` fuera de cobertura (canal root pendiente owner). |
| second-brain | ✅ BACKUP_VERIFIED + RESTORE_VERIFIED | vault 3.438 archivos; restore a scratch idéntico (conteo+bytes, 5 muestras sha256). |
| hermes-state | ✅ BACKUP_VERIFIED + RESTORE_VERIFIED | `~/.hermes` operacional + `~/aranea` + unit túnel (600); restore estructural validado. |
| pve-config (`/etc/pve`) | ⏸ SKIPPED_GATED | sin canal de lectura; requerimiento owner: subcommand `config` en `agent-read` (root SSH fail-closed, correcto). |
| etcd-snapshot | ⏸ SKIPPED_GATED | `etcdctl` ausente en hermes-vm; :2379 filtrado; sin certs conocidas. |
| pihole-config | ⏸ SKIPPED_GATED | api_token FTL v6 no disponible; .149 sin HTTP desde Hermes (coherente R0). |

**Pendiente para cerrar este subproyecto**: (1) las 3 unidades gated (deuda owner acotada); (2) automatización operativa — el wrapper `~/aranea/bin/r1-backup.sh` es manual, sin timer ni pruning; frecuencia y retención son decisión owner; (3) nota de alcance: restore de configuración (probado) ≠ recuperación integral de plataforma desde cero (no equivale).

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

1. (VIGENTE sólo para unidades pendientes) Staging real desde R1: `~/aranea/backup-staging/` (700) — el path julio `/opt/aranea-backup/` queda reemplazado; no recrear.
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

- [x] **AGENT-TASK-01-1**: crear estructura de staging. — EJECUTADO-equivalente en R1: `~/aranea/backup-staging/` (700) con manifests por run; path julio reemplazado.
  - target_system: PBS VM (futuro) o hermes-vm (temporal).
  - commands_allowed: mkdir, chown.
  - commands_forbidden: ninguno destructivo.
  - tags: [agent, setup]

- [~] **AGENT-TASK-01-2**: scripts wrapper. — PARCIAL en R1: wrapper único `~/aranea/bin/r1-backup.sh` (750) cubre traefik-config + second-brain + hermes-state. NO implementados: backup de `/etc/pve`, etcd, pi-hole (gated) ni step-ca/sanoid/inventory/runbooks como unidades (step-ca además fuera de R1: LXC `ca` 200 stopped).
  - commands_allowed: write_file, chmod +x.
  - expected_output: 7 archivos `.sh` ejecutables.
  - tags: [agent, scripting]

- [ ] **AGENT-TASK-01-3**: configurar cron jobs. — PENDIENTE: sin timer por decisión owner pendiente (frecuencia/ventana); el wrapper es ejecución manual.
  - commands_allowed: crontab, write_file en /etc/cron.d/.
  - tags: [agent, scheduling]

- [x] **AGENT-TASK-01-4**: validación end-to-end. — EJECUTADO-equivalente en R1: drills de restore a scratch + verificación sha256/conteo por run (2 ejecuciones del wrapper, idempotencia probada).
  - commands_allowed: bash.
  - validation: cada script exit 0 + archivo generado verificable.
  - tags: [agent, validation]

- [ ] **AGENT-TASK-01-5**: configurar retención 30d. — PENDIENTE: sin pruning; retención = decisión owner (misma deuda que frecuencia).
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

**Status**: in-progress (R1 certificó 3/6 unidades + drills; automatización y 3 unidades gated pendientes; reconciliado en D0 2026-09-17).
**Sesión cerrada por instrucción del owner**: 2026-07-01 (histórico).

## 📆 Bitácora

- **2026-08-10** — Migrado de `agent-project` legacy a `project` v1 sin activar la ejecución; owner, parent, lifecycle, progress, tags y secciones quedaron contractuales.
- **2026-09-17** — Fase R1 del mandato owner 2026-09-16/17 ejecutada contra este proyecto (drift de julio aplicado: sin PBS, sin step-ca, sin 7-day cron, restore inmediato). Certificadas: traefik-config (LXC 115 vía `agent_traefik`, configs estática+dinámica; sha256 8/8 vs fuente viva en drill), second-brain (vault 3.438 archivos, restore scratch idéntico), hermes-state (`~/.hermes` operacional + `~/aranea` + unit túnel; 600, drills PASS). Gated/deuda owner: `/etc/pve` (requiere subcommand `config` en `agent-read`), etcd snapshot (requiere etcd-client + endpoint/certs), pi-hole (requiere api_token FTL v6 o canal root). Staging `/home/hermes/aranea/backup-staging/` + wrapper `/home/hermes/aranea/bin/r1-backup.sh` (idempotencia probada, sin timer: frecuencia/retención pendiente decisión owner). Evidencia: `80-agents/journal/logs/2026-09-17-backup-dr-r1-bootstrap-config.md` + manifests por run.
