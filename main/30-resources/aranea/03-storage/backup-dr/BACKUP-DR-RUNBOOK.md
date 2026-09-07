---
title: "BACKUP-DR-RUNBOOK — Runbook operacional"
type: runbook
scope: project
icon: 📖
slug: backup-dr-runbook
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-07-01
tags: [aranea, backup, runbook, ops, kind/runbook, area/personal, project/agents-os]
related: "[[BACKUP-DR-DESIGN]]"
parent: "[[BACKUP-DR-OWNER-PROJECT]]"
cssclasses: wide
---

# 📖 BACKUP-DR-RUNBOOK — Runbook operacional

> Verdad operacional humana. Comandos ejecutables paso a paso. Cada paso tiene validación.

---

## §1. Backup manual de VM tier 0 (PBS)

### §1.1 Listar VMs tier 0

```bash
ssh root@kronos
pvesh get /cluster/resources --type vm --output-format json | \
  jq -r '.[] | select(.tags | inside(["tier0"])) | "\(.vmid) \(.name)"'
```

Validar: output lista VMs tier 0.

### §1.2 Backup manual a PBS

```bash
vzdump <vmid> --storage aranea-pbs --mode snapshot --compress zstd --remove 0
```

Validar: `tail /var/log/vzdump/vzdump-<vmid>-*.log` → "Backup finished successfully".

### §1.3 Verificar en PBS UI

`https://192.168.31.180:8007` → datastore `main` → verificar snapshot existe.

---

## §2. Restore manual de VM tier 0 (PBS)

### §2.1 Listar snapshots disponibles

```bash
ssh root@kronos
pvesm list aranea-pbs
```

### §2.2 Restore a VMID nuevo

```bash
qmrestore <archive-name> <new-vmid> --storage local-lvm
```

Validar: VMID nuevo aparece en PVE UI, status running.

### §2.3 Validar VM arrancada

```bash
qm status <new-vmid>  # debe ser running
ssh root@<new-vmid-ip> "systemctl status <servicio>"
```

PASS si servicio responde.

---

## §3. Backup manual PostgreSQL

```bash
ssh postgres@192.168.31.<vm152-ip>
pg_dumpall -U postgres -f /tmp/pg-dumpall-$(date +%Y%m%d).sql
gzip /tmp/pg-dumpall-*.sql

# Subir a PBS staging
scp /tmp/pg-dumpall-*.sql.gz root@kronos:/opt/aranea-backup/postgres/
```

Validar: archivo .sql.gz existe en staging.

---

## §4. PBS — verify, prune, datastore full

### §4.1 Verify semanal

```bash
proxmox-backup-manager verify --datastore main
```

PASS si exit 0.

### §4.2 Prune manual (si retention auto falla)

```bash
proxmox-backup-manager prune --datastore main \
  --keep-daily 7 --keep-weekly 4 --keep-monthly 12
```

### §4.3 Datastore > 80% — expandir

Si `pvesm status` muestra > 80%:
1. Verificar snapshots huérfanos: `proxmox-backup-manager prune`.
2. Forzar GC: `proxmox-backup-manager garbage-collect --datastore main`.
3. Si persiste, considerar expandir a `pool-kronos` (NO SQX, libre).

---

## §5. Restic — push, restore, check

### §5.1 Push manual

```bash
RESTIC_REPO=rclone:pcloud:/aranea-restic
RESTIC_PASSWORD=<from-secret-zero>
restic -r $RESTIC_REPO backup /opt/aranea-backup/config/
```

### §5.2 Restore subset

```bash
restic -r $RESTIC_REPO restore latest --target /tmp/restore --include "/etc/pve/*"
```

### §5.3 Check weekly

```bash
restic -r $RESTIC_REPO check
```

PASS si exit 0.

---

## §6. rclone crypt GDrive — push, restore, check

### §6.1 Push manual chunked

```bash
SNAP=pool0/aranea_storage@weekly-20260630
zfs send -w -c $SNAP | split -b 8G - /tmp/chunk-${SNAP//\//_}.part.
sha256sum /tmp/chunk-*.part.* > /tmp/manifest.sha256
rclone copy /tmp/chunk-* gdrive-crypt:/pool0-archive/$(date +%Y%m)/ \
  --bwlimit "08:00,10M 22:00,off"
```

### §6.2 Restore chunk

```bash
rclone copy gdrive-crypt:/pool0-archive/202606/chunk-X.part.001 /tmp/restore/
cat /tmp/restore/chunk-X.part.* | zfs recv pool0/aranea_storage
```

### §6.3 Check subset

```bash
rclone check /tmp/manifest gdrive-crypt:/pool0-archive/202606/ \
  --one-way --size-only
```

---

## §7. SMART check

```bash
smartctl -a /dev/sd<X>
```

Alertas:
- `Reallocated_Sector_Ct > 0` → crítico.
- `Current_Pending_Sector > 0` → warning.
- `Offline_Uncorrectable > 0` → crítico.

---

## §8. Secret Zero recovery procedure

Si bitwarden está inaccesible:

1. Localizar caja fuerte (ubicación en OWNER-TASK-SECRET-ZERO).
2. Localizar USB cifrado en caja fuerte.
3. Desbloquear USB con passphrase recovery (recovery code de bitwarden).
4. Montar USB, copiar secretos necesarios.
5. Reconstruir acceso a bitwarden.

Owner-driven. NO automatizable.

---

## §9. Troubleshooting común

| Síntoma | Causa probable | Acción |
|---|---|---|
| `vzdump` falla con "no space left" | PBS datastore full | §4.3 expandir. |
| `restic check` reporta corruption | Backend dañado | Restore desde otro snapshot; investigar pcloud. |
| `rclone sync` falla con rate limit | GDrive throttling | Esperar + retry; reducir `--transfers`. |
| `etcd snapshot` falla | Quorum perdido | Investigar red/cluster Proxmox primero. |
| `step ca backup` falla con passphrase | Secret Zero no documentado | OWNER-TASK-SECRET-ZERO pendiente. |

---

**Status**: design-frozen. Comandos NO ejecutados.
**Sesión cerrada por instrucción del owner**: 2026-07-01.
