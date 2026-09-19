---
type: change_log
schema_version: 1
scope: session
created: "2026-09-19"
updated: "2026-09-19"
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
application:
entities:
  - "[[agent-project-02-pbs-on-backup-node]]"
  - "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[BACKUP-DR-CONTRACT]]"
aliases:
  - "R2 reboot fail-closed + activación piloto 7d"
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
  - area/aranea
---

# 2026-09-19-r2-reboot-failclosed-activation

%% Ejecución del mandato owner one-shot "BACKUP/DR R2 — ACTIVACIÓN FAIL-CLOSED + PILOTO DE MEDICIÓN DE 7 DÍAS" (noche 2026-09-18 → madrugada/mañana 2026-09-19): reboot único de PBS + activación fail-closed + piloto con set de 6 CTs. RESULT: PASS. %%

## Cambio

- **Tipo:** infra-mutation-autorizada + updated
- **Archivo(s):**
  - `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/agent-project-02-pbs-on-backup-node.md` (bitácora; tareas 02-8/02-9; `status_detail`)
  - `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/BACKUP-DR-OWNER-PROJECT.md` (bitácora; línea estado roadmap)
  - `30-resources/aranea/03-storage/backup-dr/00-index.md` ("De un vistazo")
  - `80-agents/journal/logs/2026-09-19-r2-reboot-failclosed-activation.md` (este log)
  - `~/aranea/work/r2-pbs-20260918/measurement/` (FUERA del vault): driver corregido + `state/` + timer instalado
- **Mutaciones en infra (autorizadas por este mandato):**
  1. PBS 192.168.31.123 — `sudo reboot` único (22:23 -03 del 18sep; ordenado vía SSH, sin qm reset/stop).
  2. hermes-vm — 2 archivos NUEVOS `/etc/systemd/system/aranea-r2-measure.{service,timer}` + `daemon-reload` + `enable --now` del timer. Rollback: `sudo systemctl disable --now aranea-r2-measure.timer && sudo rm` de ambos.
  3. hermes-vm local (fuera del vault): driver `r2-measure-day.sh` editado (2 cambios mínimos ordenados/implied por el mandato, ver abajo) + `state/{first_run_date,deadline_date}` creados. Rollback: git-less, copias de hash en este log.
- **Sin mutaciones:** PVE (storage.cfg/jobs.cfg/qm 180 intactos — huellas verificadas pre y post), CTs productivos, Ceph, R1, fstab de PBS, datastore.cfg.

## Motivo

- Mandato owner one-shot (2026-09-18 noche): APRUEBA (1) reboot único controlado de PBS VMID 180, (2) activación y certificación de los dos drop-ins fail-closed existentes, (3) instalación y activación del piloto automático de 7 días SOLO si la protección queda certificada. NO aprueba: reiniciar kronos/Ceph/otros guests, tocar discos/retención, incluir CT 148, schedules generales, modificar R1.6.

## Fuentes usadas

- Mandato + `owner-action-bundle-v3.md` + bitácora ap-02 + `2026-09-18-r2-mandato-ejecucion.md` + `aranea-pbs-backup-operations` (skill) + README-ACTIVACION.md del driver.
- OBSERVADO pre-reboot (read-only, 18sep 22:15–22:21 -03): baseline v3 §0 sin drift en las 5 huellas (storage.cfg sha256 87482f91…, jobs.cfg AUSENTE, qm 180 md5 1815e259…, lvs md5 ec23b35b…, fstab md5 b4e8dd0f…); VM 180 = `pbs` (name/net0/serial scsi1=pbs-data verificados de la config live); quorum 5 nodos; Ceph HEALTH_WARN (nearfull pre-existente); cero tareas PBS/PVE activas y cero vzdump en nodos (último match de ps = kernel [arc_prune]); drop-ins presentes hash común 56eefebf…; datastore 1G/279G, du 731M, 429 chunks; snapshot única ct/155/2026-09-18T22:15:24Z; auth API pre-reboot HTTP 200 (`Authorization: PBSAPIToken backup@pbs!aranea:***`) y `pvesm status aranea-pbs` active; secret del token trasladado por SSH a `~/aranea/secrets/.t21-pbs-api-token` (600, nunca por argv/stdout de logs).

## Resolución aplicada

### Reboot controlado — PASS (15/15)

- Reboot emitido 22:23 -03 vía `ssh ariadna_pbs sudo -n /sbin/reboot` (rc 0). Lección de instrumentación: `qm status` permanece `running` durante el reboot de un guest (el proceso QEMU no muere); la señal del ciclo real es `uptime -s` del guest → **boot fresco 2026-09-18 22:24:05 -03** (el primer sondeo a +2s dio un falso "running estable" y se descartó; el estado previo real era uptime desde el 09-ago).
- Post-boot 22:28 -03, verificado: disco `scsi-0QEMU_QEMU_HARDDISK_pbs-data`→sdb con UUID f7726067-25c0-41d9-aad8-3d9cff9381a0 (ext4 300G); `/mnt/pbs-data` montada rw sobre /dev/sdb; datastore `main` visible; snapshot ct/155/2026-09-18T22:15:24Z intacta; `proxmox-backup` + `-proxy` active; **DropInPaths** con ambos drop-ins y **`Requires="mnt-pbs\x2ddata.mount"` EN VIVO en ambos servicios** (raw del manager; el grep de la primera pasada falló solo por el quoting `\"` de systemd — corregido con lectura cruda); `After` con la mount en ambos; mount unit `RequiredBy=proxmox-backup.service proxmox-backup-proxy.service`; `list-dependencies` muestra la mount en ambos árboles; API HTTP 200 + auth token HTTP 200 post-boot; `aranea-pbs` active **5/5 nodos** (athena/zeus/hera/hades/kronos); rootfs 8G usados con `/` limpia; único escritor del mount = `proxmox-backup-proxy` (PID 664, usuario `backup`) + kernel mount.

### Fail-closed — FAIL-CLOSED PASS declarado (A/B/C/D)

- A Configuración instalada: drop-ins hash 56eefebf… en ambas `.service.d/` (v3, sin drift).
- B Configuración activa: ambos servicios arrancaron el 22:24 DESPUÉS de instalar los drop-ins (18sep) → el boot real cargó la config nueva (DropInPaths + Requires en vivo).
- C Dependencia de arranque demostrada: ciclo de boot real con disco presente → servicios arriba con la dependencia ligada.
- D Protección ante pérdida del mount: mecanismo demostrado por la prueba negativa segura de v3 (unidad temporal con `Requires=<mount inexistente>` → manager la FALLA, exit 5; contraprueba mount real → exit 0) + ambos caminos de escritura cubiertos (API server root y proxy `backup`, el único proceso con FDs en el mount). `Requires/After` suficiente para el requisito aprobado; `BindsTo` no requerido. Prueba física con des-adjuntar scsi1 queda como drill opcional de ventana futura (v3 Acción 3 opcional, fuera de este mandato).

### Piloto 7 días — ACTIVADO (ACTIVE)

- Gate superado ⇒ activación según §5. Ediciones mínimas al driver validado (reutilizado, no rediseñado):
  1. **CT 148 excluido permanentemente** (orden expreso): `GUEST_ORDER` 7→6 CTs (155,156,154,101,147,115), entradas de 148 eliminadas de los mapas, mecanismo de reincorporación automática `POOL1_GATED=(148)` ELIMINADO (quedó vacío).
  2. **Fix de defecto detectado en prueba (TEST B):** `disable_timer()` llamaba `systemctl disable` sin sudo → el auto-disable (vencimiento y ABORT) habría fallado silenciosamente como el servicio corre como `hermes`. Corregido a `sudo -n systemctl disable --now` (hermes tiene NOPASSWD). **Este defecto habría dejado el piloto corriendo indefinidamente tras su caducidad si no se hubiese probado.**
- Ventana: 06:00–07:25 America/Santiago; re-verificado hoy: PBS sólo tiene daily-update 02:29 + apt-daily 06:16 (host-level, sin recursos compartidos); hermes: R1 04:00, etcd 05:00, pve-config sáb 08:30 → sin solapamiento. R1 intacto.
- Caducidad pre-anclada a la primera ejecución PROGRAMADA: la ventana del sáb 19 (06:00–07:25) venció con el gate aún PENDING; sin corridas fuera de horario (§7) → `first_run_date=2026-09-20`, `deadline_date=2026-09-26` (7 ciclos programados dom 20 → sáb 26; auto-disable el 27). Máximo 7 ciclos.
- Timer `aranea-r2-measure.timer` instalado y **enabled + active (waiting)**: próximo disparo dom 2026-09-20 06:05:00 -03. Sin `Persistent` (día perdido = día perdido).

## Validación

- Dryrun del driver modificado: exit 0, **6 prechecks** con identidad/placement/unprivileged/uptime verificados por SSH al nodo residente; **cero eventos de 148** en el JSONL.
- TEST A (ventana): `full` fuera de horario → SKIP, día no corre, no extiende, exit 0.
- TEST B (auto-disable sin sudo): falló → defecto real detectado y corregido (ver arriba).
- TEST C (camino ABORT completo, copia del driver en /tmp con BASE aislado, preflight simulado en fallo y ventana neutralizada): ABORT emitido, evento CRITICAL en JSONL aislado, **timer real quedara inactive+disabled por el propio driver**, exit 2. Limpieza completa; estado real (`first_run_date`/`deadline_date`) intacto.
- Sin secretos en logs/evidencias (grep sobre JSONL; el secreto del token vive sólo en `~/aranea/secrets/.t21-pbs-api-token`, 600).
- jobs.cfg AUSENTE post-ejecución; R1 timers intactos; huellas PVE sin drift post-reboot.

## Compartibilidad

- Scope local; sin identidad, paths sensibles ni secretos. El secreto del token PBS se referencia por ruta (owner-only, 600).

## Rollback

- Piloto: `sudo systemctl disable --now aranea-r2-measure.timer` + `sudo rm /etc/systemd/system/aranea-r2-measure.{service,timer}` + `sudo systemctl daemon-reload` (cero estado en PVE/PBS que revertir; los backups generados se PRESERVAN — prohibido borrar).
- Driver: revertir a la versión previa (sha256 5e6375a2… es el FINAL; los cambios fueron 2 ediciones descritas arriba).
- Reboot: no reversible (completado y saludable); los drop-ins se remueven con `rm` + `daemon-reload` si alguna vez se decidiera revertir el fail-closed.

## Gates residuales (estado al cierre)

1. Piloto corre SOLO: dom 20–sáb 26 sep 06:05. Verificación diaria del run + reporte día 7 para la decisión D (retención/prune/GC/jobs.cfg/Tier 0) — GATED decisión owner post-medición.
2. CT 148: excluido permanentemente de este piloto; su cobertura queda en el carril Ceph/Infrastructure Ops (pool1 nearfull 87%).
3. Prueba negativa física (des-adjuntar scsi1): drill opcional de ventana futura, fuera de este mandato.
4. Restore funcional de datos etcd y reincorporación al quorum: NO demostrados (R3/R4; fuera de R2).
5. R1.6 sigue PAUSADO. Ceph nearfull = carril Infrastructure Ops. R2 permanece IN-PROGRESS (DoD: 7/7 días con verify ok).
6. Sesión NO cerrada (orden expresa del mandato).
