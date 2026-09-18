---
type: change_log
schema_version: 1
scope: session
created: "2026-09-18"
updated: "2026-09-18"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
application:
entities:
  - "[[agent-project-02-pbs-on-backup-node]]"
  - "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[BACKUP-DR-CONTRACT]]"
aliases:
  - "R2 PBS piloto ejecutado 2026-09-18"
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-18-r2-pbs-pilot-execution

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/agent-project-02-pbs-on-backup-node.md` (bitácora R2 piloto ejecutado; frontmatter `status_detail`/`updated`)
  - `30-resources/aranea/03-storage/backup-dr/00-index.md` (estado R2 en "De un vistazo")
  - `80-agents/journal/logs/2026-09-18-r2-pbs-pilot-execution.md` (este log)
  - Infra (mutaciones autorizadas por mandato owner 2026-09-18, bundle v2 como base): VM 180 `scsi1` nuevo + LV `local-kronos/vm-180-disk-1` 300G; datastore `main` en PBS; `backup@pbs` + token `aranea` + ACLs; storage `aranea-pbs` en PVE (cluster-wide, 1 stanza); fixture CT 990 creado→verificado→destruido.

## Motivo

- Autorización owner única ("AUTORIZACIÓN OWNER — BACKUP/DR R2 / PILOTO PBS", 2026-09-18 ~18:58, ventana online 2h, sin downtime, SIN reboot): ejecutar → verificar → corregir en alcance → un solo resultado, con el bundle v2 (`~/aranea/work/r2-pbs-20260918/owner-action-bundle-v2.md`) como base y las condiciones del mandato como restricciones superiores.

## Fuentes usadas

- Mandato owner (mensaje directo) + bundle v2 + log discovery R2 (`2026-09-18-r2-pbs-discovery-effective.md`).
- OBSERVADO live (read-only y de ejecución, sin secretos impresos): PBS .123 (ssh `ariadna_pbs`), 5 nodos PVE (ssh `ariadna_pve`, direcciones resueltas desde corosync: hera .110 / zeus .100 / hades .90 / kronos .120 / athena .10), API PBS 8007 autenticada con el token (header `PBSAPIToken` sin comillas, formato verificado en `PBSPlugin.pm`).

## Resolución aplicada

- **Fase A (disco + datastore):** `scsi1` libre pre-verificado; `qm set 180 -scsi1 local-kronos:300,iothread=1,ssd=1,discard=on,serial=pbs-data` → LV `vm-180-disk-1` 300G + hotplug OK en VM viva. Guest: `/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_pbs-data` = `sdb`, 322122547200 B, virgen (sin particiones/fs). mkfs.ext4 por by-id; fstab por UUID con `nofail,x-systemd.device-timeout=10s`; **protección anti-mount-vacío: dir `/mnt/pbs-data` 000 root:root** (visible cuando desmontado; el fs montado lo tapa con 755 root). Corrección intra-fase: primer intento de fstab quedó con UUID vacío (carrera udev tras mkfs — `lsblk -no UUID` devolvió vacío); re-leído del device y `sed` de la línea rota, 1 línea final. Datastore `main` @ `/mnt/pbs-data` con `--verify-new true`; path verificado como el fs montado; servicios `proxmox-backup`/`-proxy` active.
- **Fase B (identidad + integración):** `backup@pbs` creado; ACL `DatastoreBackup` (rol PBS 4.2 SIN punto — el bundle escribía el nombre del PRIVILEGIO `Datastore.Backup`) sobre `/datastore/main` a usuario Y token. Verificación efectiva exacta: ambos auth-ids muestran solo `Datastore.Backup` en `/datastore/main`; sin Prune/Modify/admin → gate ABORT superado. Token generado con `user generate-token` (sin `--output-format`, no soportado); JSON con clave `value` (no `secret`); secreto capturado a archivo 600 root en PBS, trasladado a kronos SOLO por stdin (sha16 verificado), registro ÚNICO `pvesm add pbs aranea-pbs` desde kronos con `--username 'backup@pbs!aranea' --password <stdin>` + `--fingerprint` TLS (capturado desde el propio PBS: `5F:BA:AD:61…:78`); secreto persistido por el plugin en `/etc/pve/priv/storage/aranea-pbs.pw` (600, 37B); storage.cfg sin secretos. `pvesm status` = **active en 5/5 nodos**; sha256 storage.cfg idéntico en los 5 con exactamente 1 stanza nueva; `/tmp/toksec`+`tokraw`+`tokerr` destruidos en ambas máquinas (shred).
- **Fase C (backup piloto):** `vzdump 155 --storage aranea-pbs --mode snapshot` (sin flags extra): 25s total, 2.05 GiB leídos → 472.5 MiB comprimidos a ~121 MiB/s, backup incremental (3% reutilizado — sin previo, efecto chunks metadata), CT 155 corriendo todo el ciclo (uptime 40d continuo, snapshot LVM fino creado y eliminado). Snapshot PBS `ct/155/2026-09-18T22:15:24Z` con 5 archivos, owner `backup@pbs!aranea`, `verification.state="ok"` (verify automático `--verify-new`); verify explícito `proxmox-backup-manager verify main` → TASK OK. Evidencia API con el token desde kronos (opción `--config` de curl, secreto fuera de argv).
- **Fase D (restore aislado):** CTID 990 pre-verificado libre en 5/5; `pct restore 990 <volid> --storage local-lvm --unprivileged` (storage como OPCIÓN, no posicional; corrección al bundle) → 21s, rootfs 10G + mp0 8G. NUNCA arrancado. Config heredado neutralizado (`--delete net0` — traía la IP productiva del nodo etcd .251 — y `--onboot 0`). Verificación por montaje ro: hostname `etcd-hera`, filesystem completo, `etcd.service` presente. Cleanup autorizado: `pct destroy 990` + LVs `vm-990-disk-{0,1}` eliminados, sin residuos.
- **HALLAZGO material:** el volumen `mp0` (`/var/lib/etcd`, los datos) está **EXCLUIDO del backup por la config del propio CT 155** — task log: `excluding volume mount point mp0 ('/var/lib/etcd') from backup (disabled)`; el snapshot restaurado contiene rootfs íntegro pero mp0 vacío (datos reales en vivo: 128M wal+snap). No es defecto del pipeline PBS; corregirlo exige mutar config de 155 (prohibida por el mandato). Queda para decisión owner: activar backup del mp0 vs mantener la protección lógica R1 como única vía (los datos etcd son reconstruibles desde snapshot etcd 3.6, pero la config TLS del rootfs SÍ quedó respaldada).
- **Fase E (medición):** 429 chunks, 473M aparentes / ~496 MB lógicos en `.chunks`; datastore 731M sobre 295G útiles (0.25%). Huella por unidad medida; NO se extrapola a retención 7d+4w+12m.
- **Fase G sustituida (sin reboot):** validación no disruptiva de persistencia: `findmnt --verify` sin errores; UUID fstab == UUID device; unit `mnt-pbs\x2ddata.mount` generada por systemd-fstab-generator con `Requires/After=systemd-fsck@dev-disk-by\x2duuid-…`; datastore visible tras remontaje lógico. La prueba real de reboot queda pendiente de ventana específica (no simulada como PASS).
- **No-colateral verificado:** `qm config 180` delta único = línea `scsi1`; `lvs local-kronos` delta único = `vm-180-disk-1 300G`; jobs.cfg sigue ausente; storage.cfg solo estanza nueva; sin residuos en `/tmp` de PBS/kronos/hera; sin otros guests tocados.

## Validación

- Autenticación end-to-end probada: `pvesm status` active 5/5 + backup real completado + API con token 200 (no solo exit codes).
- Verificación efectiva de privilegios usuario y token: exactamente `Datastore.Backup` en `/datastore/main` (conjunto, no orden).
- Integridad del snapshot certificada por `verification.state=ok` a nivel datastore (verify automático) + verify explícito TASK OK.
- Restore validado ESTRUCTURALMENTE (contenido legible ro); NO se declara restore funcional (el CT nunca se ejecutó, por mandato).
- CT 155 intacto post-todo (running, uptime continuo).
- Correcciones de sintaxis PBS 4.2/PVE 8.4 aplicadas con evidencia (roles sin punto; `generate-token` sin `--output-format`; JSON key `value`; header API `PBSAPIToken` sin comillas; `pct restore` con `--storage`): aprendizajes transferibles para runbook futuro.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos (ningún valor de token impreso o persistido; solo longitudes y ubicaciones)

## Rollback

- Ejecutado/parcialmente disponible, sin destrucción de datos: des-adjuntar `scsi1` (`qm set 180 --delete scsi1`) y des-registrar storage (`pvesm remove aranea-pbs`) es trivial; el LV `vm-180-disk-1` y el datastore `main` contienen YA el snapshot piloto → por regla del bundle **no se eliminan automáticamente**; reversión completa (lvremove / datastore destroy / user remove) queda como decisión owner explícita. Fixture 990 ya destruido. Rollback de credenciales disponible: `user remove backup@pbs` (elimina token y ACLs) + borrar `aranea-pbs.pw`.
