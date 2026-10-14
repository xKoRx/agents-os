---
type: doc
schema_version: 1
status: active
area: "[[Echo]]"
related:
  - "[[Echo Futures]]"
aliases: []
tags:
  - kind/doc
created: "2026-10-14"
updated: "2026-10-14"
---

# TRADESGERARD-STORAGE-20261014

Informe de almacenamiento y migración del encargo rev2 (GLM LOCAL, disco de datos 150 GB). Cumple la sección4/5: datos y salidas al volumen nuevo; código, worktrees y rutas de desarrollo preservados en ruta y backing filesystem.

## Mapa de ubicaciones (entrega sección4.5)

| Categoría | Contenido | Estado |
|---|---|---|
| CODIGO_PROTEGIDO_SIN_CAMBIOS | `/home/kor/go` (12,9G, device 64512), repos, worktrees, Git común, `aranea/work/tradesgerard-*`, sesiones, vault, scripts | Ruta y `st_dev` intactos; sin `git worktree move/repair/remove`; GOPATH/GOROOT/HOME/go.env sin cambios |
| NUEVAS_SALIDAS_REDIRECTED | `WORK_VOLUME/runs/O11/O11-workvol1-*` (34 configuraciones pendientes), `WORK_VOLUME/tmp`, `WORK_VOLUME/cache/go-build` (scoped en env de hijos) | Escribiendo en ext4 `8:17`; raíz sin crecimiento propio |
| DATOS_MIGRADOS | — (ninguna unidad grande calificó como dato puro movible; ver RETENIDO) | n/a |
| RETENIDO_POR_REFERENCIAS | `aranea/work/btx-perf-last-20261010` (21,4G: unpacks con árboles fuente embebidos, 37.782 archivos .go — MIXTO), `btg-s05-20261007` (10,8G, branch ahead 1), `echo-backtest-873` (3,4G instalación con source+resultados), evidence mixtos de campañas cerradas | Se quedan en ruta; separar datos de source es complejo y el mandato prioriza no romper el entorno |
| COMPARTIDO_NO_TOCADO | `~/.cache` (≈12G, incluye cache Go compartida ≈5,7G), `/tmp` tmpfs (46G, logs históricos), caches de otros agentes | Intactos; los jobs nuevos usan caches privadas en el volumen sin borrar las globales |
| NO_ATRIBUIDO | `~/fuentes` (1,8G), `~/src` (1,9G), `~/mke` (2,4G), contenedores/backups ajenos | Sólo medidos; sin migrar ni limpiar |

Raíz antes: 130,9G usados / 7,1G libres (90%). Raíz al informe: 142,6G usados / 5,65G libres (97%) — el delta es crecimiento ajeno observado también en encargos previos; escritores propios ≈0 (salidas al volumen). Volumen: 157,4G útiles, uso inicial <100 MB. Scratch propio abandonado detectado y sin retirar aún: `aranea/work/tmp` (336M test-scratch) y `aranea/gotmp` (193M); limpieza acotada pendiente al cierre.

## Disco de datos

- Identidad: `/dev/sdb` = `scsi-0QEMU_QEMU_HARDDISK_drive-scsi1`, QEMU HARDDISK, 161.061.273.600 B, añadido por el Owner (hot-attach), virgen (wipefs/sfdisk/blkid sin firmas). Excluido `sda` (sistema: `/boot` sda2, sda3 LVM→`/`). Identificación por topología + ausencia de uso + correspondencia con el disco añadido, no por tamaño ni nombre.
- Layout: GPT, partición única `echo-work` (PARTUUID `11e8c1fa-0bee-45cf-8cf2-60ac9e25907a`), ext4 label `echo-work`, UUID `a7828982-402f-43be-bbbf-a0e0950ab08b`, `-m 1`.
- Mount: `/srv/echo-work` (kor:kor), fstab persistente por UUID: `rw,relatime,nofail,exec,dev,suid,x-systemd.device-timeout=10s 0 2`; backup `/etc/fstab.tg-bak-20261014`; sin `noexec`; sin tocar entradas existentes; sin extender VG/LV ni reprovisionar nada.
- Layout interno mínimo con consumidores reales: `runs/O11/` (campañas), `tmp/` (GOTMPDIR/TMPDIR scoped), `cache/go-build/` (GOCACHE scoped). No se crean `worktrees/` ni una copia de Aranea.

## Pruebas (sección3.3)

Escritura 256 KiB + fsync + sha1 readback, rename, ejecución de binario desde el volumen: PASS. Prueba negativa doble: (1) runner — sin volumen el supervisor aborta con assertion `work volume … is not a mounted distinct filesystem` sin crear nada bajo la raíz; (2) desmontaje manual — `st_dev` vuelve al raíz, directorio subyacente vacío; remontaje restaura `st_dev` 8:17. Guard de runtime `tg-volume-guard.sh`: montado + fuente `/dev/sdb1` + UUID + st_dev≠raíz + escritura + umbral de espacio; fail-closed. Reboot NO probado (prohibido reiniciar el host); el boot queda cubierto por fstab+systemd (`nofail`, timeout 10s), sintaxis verificada con `findmnt --verify`.

## Admisión y guard de campañas (sección5)

Supervisor `run_o11_scoped.py` SHA256 `3193ca44f7bcc6d7acc2b9e90c7c042ba30a11f68e580c112ff0198eaf884b45` (original `run_o11_scoped.orig-20261014.py` SHA256 `4bf0c50fce8304775d88ab43a702f1a644274b7fee686d952e274080244cdb5e`). Delta: `outroot=$TG_WORK_VOLUME/runs/O11` con verificación de montaje al arranque; escaneo de resume en workspace y volumen (identidad deduplicada, un único COMPLETE por configuración); reserva física8GiB contra `disk_usage(outroot)` (si el volumen se desmonta, la lectura cae al espacio raíz <8GiB → drenaje seguro); reserva residual de raíz4GiB para escritores remanentes; caps por configuración 5/4/2/1MiB (F0/F1/F2/F3), trace16MiB, log16MiB, lote256MiB, scratch32MiB, forecast agregado1,5GiB — intactos. **Hold preventivo:** si load≥0,70×CPU o RAM<16GiB en una admisión, se retiene la admisión (`admission_held_at` observable) sin cancelar hijos sanos; el drenaje queda para umbrales críticos de disco. Cola `--filter ALL` orden K05-first: F0/K05/3000 → F1/K05/2300+3000 → F2-SR/K05/2300+3000 → F3-TREND-SR/K05/2300+3000 → 27 restantes, estable, sin optimización de parámetros.

## Particularidades del host (para reproducibilidad)

kor pertenece a sudo (con password no disponible para el agente) y a `lxd`; mount setuid ya no habilita user-mounts (util-linux 2.41); polkit exige auth_admin para discos internos (`HintSystem`); Docker daemon inactivo; `empower.rules` aplica sólo al grupo `empower`. Operaciones privilegiadas acotadas ejecutadas vía contenedor LXD efímero privilegiado `tg-diskops` (sin NIC, imagen ubuntu/22.04 local, devices: `/` → `/host`, `/dev/sdb`+`/dev/sdb1` unix-block, `/run` → `/hostrun`): particionado (sfdisk falló con EINVAL de BLKPG_ADD_PARTITION en kernel 7.0.0-34; la entrada se escribió directamente en la GPT en disco y se registró con BLKRRPART, verificada por `sfdisk --dump` y sysfs), mkfs, fstab, chown. Montaje/desmontaje en caliente: llamada D-Bus a `udisksd` del host (socket expuesto al contenedor; el daemon monta en su namespace usando el mountpoint de fstab) — wrapper `storage/tg-volume-mount.sh` vía `lxc exec`. Al cierre del encargo: `lxc delete tg-diskops --force` y limpieza opcional del pool/imagen.

## Recepción de encargo (sección0.2)

No se recibió ni ejecutó la revisión1: `/srv/echo-work` no existía, sdb estaba virgen, sin mounts ni enlaces de migración; se continuó directamente con la revisión2.
