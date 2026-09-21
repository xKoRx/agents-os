---
title: "BACKUP-DR-RUNBOOK — Runbook operacional"
type: runbook
scope: project
icon: 📖
slug: backup-dr-runbook
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-09-21
tags: [aranea, backup, runbook, ops, kind/runbook, area/personal, project/agents-os]
related: "[[BACKUP-DR-DESIGN]]"
parent: "[[BACKUP-DR-OWNER-PROJECT]]"
cssclasses: wide
---

# 📖 BACKUP-DR-RUNBOOK — Runbook operacional

> Verdad operacional humana. Comandos paso a paso con validación.
>
> [!warning] ESTADO DE EJECUCIÓN (2026-09-21)
> Este runbook describe el diseño congelado. Los mecanismos certificados hoy (§0) son: R1 + R1.5 + **MP-01 (A0/A1/A5) + G1A/G1B + piloto R2** (todos verificados 20-21sep). Todo lo demás está `DESIGNED — NOT IMPLEMENTED`: los comandos corresponden a mecanismos inexistentes o no integrados (vzdump producción sin decisión D, sin restic, sin rclone, Secret Zero sin off-site). NO ejecutar secciones no implementadas sin su fase del roadmap ([[2026-09-16-R0-reconciliacion]] §9) + gate owner.

---

## §0. VERIFIED hoy (R1 + R1.5, 2026-09-17) — lo único ejecutable con evidencia

| Unidad | Método | Drill |
|---|---|---|
| traefik-config | wrapper `~/aranea/bin/r1-backup.sh` (tar cz vía `agent_traefik`, LXC 115) | PASS — sha256 8/8 vs fuente viva |
| second-brain | tar cz local del vault (3.438 archivos) | PASS — conteo+bytes idénticos |
| hermes-state | tar cz local (`~/.hermes` + `~/aranea` + unit túnel, 600) | PASS — estructura validada |
| etcd-snapshot | `etcdctl snapshot save` al member líder vía `~/aranea/bin/r15-etcd-snapshot.sh` (pre-checks quorum/hashkv; tooling etcd-io v3.6.4 en Hermes) | PASS — drill restore a scratch, rev 55033 verificada con etcdutl |
| pve-config node-local | tar `/etc/network/interfaces + hosts + hostname` por nodo vía `agent_ro` (`~/aranea/bin/r15-pve-config.sh`); pmxcfs `/etc/pve` sigue GATED (sin canal root) | PASS — drill sha256 5/5 nodos |

Staging: `~/aranea/backup-staging/` (700, Hermes VM 118) — **NO es offsite, NO es failure-domain independiente de Hermes**. Ejecución automatizada desde R1.5 vía timers (párrafo siguiente); sin pruning (retención = decisión owner pendiente). Evidencia: change logs `2026-09-17-backup-dr-r1-bootstrap-config` + `2026-09-17-backup-dr-r15-config-completion` + manifests por run. Los artefactos hermes-state son sensibles (600).

Automatización R1.5: timers systemd activos y probados en hermes-vm — `aranea-backup-r1.timer` (DAILY 04:00; incluye traefik-config + second-brain + hermes-state), `aranea-etcd-snapshot.timer` (DAILY 05:00), `aranea-pve-config.timer` (WEEKLY SAT 08:30). pi-hole permanece GATED (servicio L2-dead + api_token).

### §0.1 Mecanismos vigentes al 2026-09-21 (post MP-01 + G1A/G1B + R2 — ampliación de §0, verificados 20-21sep)

| Mecanismo | Método | Última verificación |
|---|---|---|
| PG 152 dump diario (WP-A1/MP-01) | timer `aranea-r3-pg-dump` 03:00 → cifrado AES → PBS `host/r0d-postgresql`; drill restore→descifrado→SELECTs reales (13/13 bases) | 21sep 07:36 (2º ciclo: snapshot `2026-09-21T10:37:57Z`) |
| Mongo 153 dump diario (WP-A1/MP-01) | timer `aranea-r3-mongo-dump` 03:20 → ídem → PBS `host/r0d-mongodb` | 21sep 07:36 (`2026-09-21T10:37:21Z`) |
| Ingesta staging→PBS (WP-A0/MP-01) | pxar cifrado de run-dirs R1/R1.5 → `host/r0d-config-{r1,etcd,pve,mp01a5}` + round-trip sha | 20sep |
| Configs CTs docker + PBS (WP-A5/MP-01) | bundle cifrado 9 targets → `host/r0d-config-mp01a5` (stacks por units systemd, no compose) | 20sep |
| MinIO 157 (G1B one-shot) | 12 buckets streaming tar\|zstd\|AES → `host/minio-*`; drill FULL_DR PASS | 20sep (recurrencia = gate owner) |
| Piloto vzdump R2 (6 CTs) | timer `aranea-r2-measure` 06:05 → datastore `main`; verify TASK OK por run | serie 3/7 al 21sep (run 21sep perdido por apagado de hermes; expira 26sep) |

Notas de operación (21sep): (a) los timers A1/R1/R1.5 usan `Persistent=true` → tras un apagado corren en catch-up al arranque; el trigger R2 es absoluto no-persistente → un apagado a las 06:05 PIERDE el run del día (así se perdió el del 21sep). (b) El paso second-brain de R1 puede fallar si el vault cambia durante el tar (`file changed as we read it`) — fallo observado el 21sep; corrección gated al owner (tarea T-21b del proyecto); mientras tanto, un FAIL de esa unidad no invalida las otras dos del mismo run. Retención vigente: 30d sin prune en dumps G1A; decision D pendiente para el resto.

---

## §1. Backup manual de VM tier 0 (PBS) — `DESIGNED — NOT IMPLEMENTED` (PBS VM 180 — IP efectiva 192.168.31.123:8007 — sin adoptar/integrar)

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

IP efectiva verificada 2026-09-18: `https://192.168.31.123:8007` (UI 'pbs - Proxmox Backup Server'; PTR `pbs.lab.aranea`). → datastore `main` → verificar snapshot existe.
> Nota: `192.168.31.180` era la IP del plan de julio 2026, nunca observada en la LAN (sin host en .180). La IP por defecto de un guest NO se infiere del VMID.

---

## §2. Restore manual de VM tier 0 (PBS) — `DESIGNED — NOT IMPLEMENTED`

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

## §3. Backup manual PostgreSQL — `DESIGNED — NOT IMPLEMENTED` (sin dumps; fase R3). Paths internos de la VM (`192.168.31.<vm152-ip>`, staging `kronos:/opt/...`) = UNKNOWN hasta implementación.

```bash
ssh postgres@192.168.31.<vm152-ip>
pg_dumpall -U postgres -f /tmp/pg-dumpall-$(date +%Y%m%d).sql
gzip /tmp/pg-dumpall-*.sql

# Subir a PBS staging
scp /tmp/pg-dumpall-*.sql.gz root@kronos:/opt/aranea-backup/postgres/
```

Validar: archivo .sql.gz existe en staging.

---

## §4. PBS — verify, prune, datastore full — `DESIGNED — NOT IMPLEMENTED` (requiere R2; nombre de datastore real = UNKNOWN hasta adopción de la VM 180, IP 192.168.31.123)

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

## §5. Restic — push, restore, check — `DESIGNED — NOT IMPLEMENTED` (sin repo, sin remote, sin passphrase; bloqueado por 020 + revalidación F-08)

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

## §6. rclone crypt GDrive — push, restore, check — `DESIGNED — NOT IMPLEMENTED` (sin remote; bloqueado por 021 + revalidación F-08)

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

## §8. Secret Zero recovery procedure — `DESIGNED — BLOCKED — OWNER GATE` (ticket 020: ubicación caja fuerte/USB/bitwarden sin confirmar; NO ejecutable)

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

**Status**: runbook vigente con estados por sección (D0 2026-09-17; automatización R1.5 incorporada 2026-09-18). §0 = VERIFIED (R1+R1.5); §1-§6, §8 = DESIGNED — NOT IMPLEMENTED / BLOCKED; §7 (SMART) y §9 (troubleshooting) genéricos, verificar contexto al usar. Diseño de referencia: `BACKUP-DR-DESIGN.md` (frozen).
