---
type: change_log
schema_version: 1
scope: session
created: "2026-09-17"
updated: "2026-09-17"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
entities:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[BACKUP-DR-CONTRACT]]"
  - "[[agent-project-01-critical-config-backup]]"
tags:
  - kind/change-log
  - area/aranea
  - project/backup-dr
  - domain/backup-dr
---

# 2026-09-17 — Backup/DR R1: Critical Bootstrap / Config Backup

## Alcance ejecutado

Mandato owner R1 (bootstrap/config crítico → staging Hermes VM 118). R0 no repetido;
preflight mínimo sobre captura `*_20260916_233513` + verificación live acotada.

## Resultado: PASS WITH DEBT

### Unidades certificadas (BACKUP_VERIFIED + RESTORE_VERIFIED)

| Unidad | Fuente | Método | Drill restore |
|---|---|---|---|
| traefik-config | LXC 115 (192.168.31.11) `/etc/traefik/{traefik.yaml,dynamic,conf.d}` | tar cz stream vía ssh `agent_traefik` (key-only, BatchMode) | PASS — sha256 8/8 archivos == fuente viva |
| second-brain | `/home/hermes/obsidian/SecondBrain/main` (3.438 archivos, 44,5 MB) | tar cz local | PASS — conteo+bytes idénticos, 5 muestras sha256, diff estructura 0 |
| hermes-state | `~/.hermes` set operacional + `~/aranea` + unit systemd túnel | tar cz local ×3 (600) | PASS — config.yaml YAML válido, unit con ExecStart, .env 600 presente |

### F-09

`pool2/pool0_backup` → **EXISTS**. Evidencia: `agent-read storage` truenas live
2026-09-17 (REFER 1.94T, mountpoint legacy `/mnt/mnt/pool0`) + captura R0
`truenas_20260916_233513`. No migrado, no modificado (F-09 respetado).

### Unidades SKIPPED_GATED (deuda acotada, no bloquean el resto)

1. **pve-config** (`/etc/pve` + networking): sin canal de lectura — `agent-read`
   no expone config; root SSH desde hermes falla cerrado en todos los nodos
   (probe BatchMode con las 3 llaves existentes: Permission denied, correcto).
   Necesita: subcommand `config` en `agent-read` autorizado por owner.
2. **etcd-snapshot**: `etcdctl` no instalado en hermes-vm; endpoints :2379
   (101/147/154/155/156) filtrados desde LAN; sin credenciales/certs conocidos.
   Necesita: `etcd-client` en hermes-vm + endpoint alcanzable o wrapper node-local.
3. **pihole-config**: Teleporter API v6 exige `X-FTL-APIKEY` no disponible;
   .149 sin ping/HTTP desde hermes (coherente con R0). Necesita: api_token FTL
   vía vault o canal root a `/etc/pihole`.

### Traefik gap parcial

`/etc/traefik/{secrets,ssl,backup-*,quarantine-*}` son root-only en el LXC:
el backup cubre la configuración reconstruible (estática+dinámica); acme.json
y secrets requieren canal root (deuda owner, misma familia del gate pve-config).

## Staging y reproducibilidad

- Staging: `/home/hermes/aranea/backup-staging/` (700), runs `20260917-010252`
  (certificada, con manifest.json completo y drills) y `20260917-013446`
  (segunda ejecución del wrapper, exit 0, 3/3 OK — idempotencia probada).
- Wrapper reproducible: `/home/hermes/aranea/bin/r1-backup.sh` (750). Sin
  pruning; sin timer instalado (frecuencia/retención = decisión owner; los jobs
  congelados de backup-policy.yaml apuntan a destinos PBS aún inexistentes).
- Manifests sin secretos; artefactos hermes-state son sensibles (600) y su
  contenido nunca fue desplegado ni listado.
- Restore drills: todo a scratch dentro del staging; cero toques a producción;
  scratch eliminado post-evidencia.

## Cambios documentales

- `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/agent-project-01-critical-config-backup.md`:
  reconciliado con scope R1 real (estado, bitácora).
- `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/BACKUP-DR-OWNER-PROJECT.md`:
  status_detail/progress + bitácora (solo hechos verificados).

## No hecho (explícito)

- Sin cambios al contrato, diseño, policy, tickets 018-021, ni declaraciones READY.
- R2 NO iniciado. Session close NO ejecutado (§17 del mandato).
- Offsite/failure-domain: staging en Hermes NO es offsite; ninguna unidad global READY.
