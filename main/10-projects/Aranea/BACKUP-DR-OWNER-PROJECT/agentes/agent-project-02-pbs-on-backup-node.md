---
title: "agent-project-02 — PBS on backup node"
type: project
schema_version: 1
owner: agent
root: false
status: in-progress
status_detail: "R2 MANDATO 2 EJECUTADO (2026-09-19): owner aprobó reboot único + activación fail-closed + piloto 7d con 6 CTs (148 excluido permanente). REBOOT PBS PASS (boot 22:24:05, 15/15 checks: disco/UUID/mount/datastore/snapshot/servicios/API 200/auth 200/aranea-pbs 5/5/raíz limpia/chunks sin drift). FAIL-CLOSED PASS declarado: drop-ins activos en boot real (DropInPaths + Requires=mnt-pbs\\x2ddata.mount EN VIVO en proxmox-backup Y -proxy), A/B/C/D cubiertos (D: prueba negativa segura v3 + ambos caminos de escritura cubiertos; BindsTo no requerido). PILOTO ACTIVE: timer aranea-r2-measure.timer enabled, primer disparo PROGRAMADO dom 2026-09-20 06:05 -03, expiración absoluta 2026-09-26 pre-anclada (ventana sáb 19 perdida con gate aún pendiente — sin corridas fuera de horario); driver corregido: 148 excluido permanente (mecanismo POOL1_GATED eliminado por mandato) + fix disable_timer→sudo -n (defecto real hallado en TEST B: sin sudo el auto-disable fallaba silencioso); TEST A ventana SKIP + TEST C camino ABORT completo PASS (timer real deshabilitado por el propio driver). R2 IN-PROGRESS (DoD: 7/7 días verify ok); siguiente: verificación diaria de runs, reporte día 7 → decisión D. R1.6 PAUSADO."
priority: P2
progress: 0
icon: 🖥️
slug: agent-project-02-pbs-on-backup-node
area: "[[Aranea]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-09-18
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

**Adoptar/recuperar la PBS VM 180 existente** en kronos (R0 2026-09-16: running, sin registro `pbs` en `pve_storage`, credenciales UNKNOWN; IP efectiva 192.168.31.123:8007 — UI PBS verificada 18sep, PTR pbs.lab.aranea; el 'sin ping/22/8007' de R0 sondeó la IP plan .180, sin host real) e integrarla: datastore según F-06 (`local-kronos`), usuario backup, registro en los 5 PVE nodes y schedules vzdump. NO asumir datastore interno, red, credenciales ni versión sin evidencia: se descubren dentro del gate de adopción.

## 📊 Estado actual

- **IN-PROGRESS (R2 discovery ejecutado 2026-09-18).** Gate de adopción (AGENT-TASK-02-0) resuelto con evidencia: accesos `ariadna@` demostrados y discovery completo; decisión = REUTILIZAR la VM 180 (PBS 4.2.6-1 viva, adminizada vía SSH+sudo; sin reinstalar). Pendiente: mutaciones de integración agrupadas en el bundle owner (datastore A, credenciales B, tickets C). El supuesto julio "crear VM vmid 180 desde cero" queda HISTORICAL — único procedimiento reemplazado.

## Scope

- Adoptar VM 180 existente en kronos (acceso vía owner; discovery interno read-only: versión PBS, datastore existente, servicios, red).
- Instalar/reinstalar PBS sólo si el discovery del gate de adopción lo concluye necesario (no por default).
- Configurar/validar datastore sobre `local-kronos` (F-06) partiendo del estado real de la VM.
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
- OWNER-TASK-MAINT-WINDOW (ventana de mantenimiento para la integración PBS).
- OWNER-TASK-SECRET-ZERO (passphrase datastore).

## Required owner permissions

- Habilitar acceso/consola a la VM 180 existente (owner; credenciales UNKNOWN hasta el gate).
- Acceder PVE UI de los 5 nodes para registrar storage.
- Passphrase datastore (referencia Secret Zero).

## Required credentials / secrets

- PBS API token (generado en setup).
- root PVE de los 5 nodes (registrar storage requiere escribir `/etc/pve/storage.cfg`).

## Required maintenance window

SÍ. La integración escribe `/etc/pve/storage.cfg` (se replica a los 5 nodos) y trabaja sobre la VM 180 existente. Usar OWNER-TASK-MAINT-WINDOW.

## Dependencies

- ap-00 done.
- OWNER-TASK-MAINT-WINDOW resuelto.

## Protected resources

| Recurso | Protección |
|---|---|
| `local-sqx-kronos` | SAGRADO. NO TOCAR. PBS datastore va en `local-kronos` (distinto). |
| Ceph MON/MGR de kronos | NO interrumpir quorum al registrar storage / trabajar sobre la VM 180. |

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

## Implementation plan — procedimiento vigente: adopción e integración (post-gate owner)

> **Orden vigente (D0)**: el gate de adopción va PRIMERO — (0) owner habilita acceso a VM 180 + ventana 019; (0.1) discovery interno read-only; (0.2) decisión reutilizar vs reinstalar con evidencia. Recién entonces aplican los pasos 1-6 de abajo (datastore, usuario, registro en 5 nodos, schedules, smoke). La creación desde cero de julio vive SOLO en la sección HISTORICAL de abajo.

1. **Gate de adopción (pasos 0–0.2)**:
   - Owner habilita acceso/consola a la VM 180 existente + ventana (OWNER-TASK-MAINT-WINDOW).
   - Discovery interno read-only: versión PBS, datastore existente, servicios, red, credenciales.
   - Decisión con evidencia: reutilizar vs reinstalar (si reinstalar → sección HISTORICAL, con re-aprobación owner).
2. **Datastore** sobre `local-kronos` (F-06), path según discovery:
   ```bash
   proxmox-backup-manager datastore create main --path <según-discovery> \
     --prune-backups keep-daily=7,keep-weekly=4,keep-monthly=12
   ```
3. **User**:
   ```bash
   proxmox-backup-manager user create backup@pbs --comment "PBS backup user"
   proxmox-backup-manager user update backup@pbs --password <STRONG>
   ```
4. **Registrar storage en 5 PVE nodes**:
   ```bash
   # En cada uno de athena, zeus, hera, kronos, hades:
   pvesm add pbs aranea-pbs --server 192.168.31.123 --datastore main \\
     --username backup@pbs --password <STRONG> \
     --content backup --prune-backups keep-daily=7,keep-weekly=4,keep-monthly=12
   ```
5. **Schedule vzdump**:
   - Daily 02:00 — tier 0 (lista OWNER-TASK-CRITICAL-VMS).
   - Weekly Sat 02:00 — tier 1/2.
6. **Smoke test**: `vzdump` manual de 1 VM tier 0.

### HISTORICAL — creación desde cero (julio 2026; reemplazado por adopción en D0)

> Sólo aplica si el gate (0.2) concluye reinstalación; requiere re-aprobación owner + OWNER-TASK-MAINT-WINDOW. NO es el plan por defecto.

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

## Validation plan

- `qm status 180` running.
- PBS UI accesible en https://192.168.31.123:8007 (IP efectiva verificada 2026-09-18; `.180` era la IP del plan julio, sin host en la LAN).
- Datastore `main` muestra chunks.
- `pvesm status` en los 5 nodes muestra `aranea-pbs` active.
- `vzdump` manual de VM tier 0 aparece en PBS.

## Rollback plan

### Rollback vigente — integración post-adopción (NO destructivo)

- `pvesm remove aranea-pbs` en los 5 nodes (revierte el registro; no toca la VM).
- Revertir datastore/usuario dentro de la VM 180 según lo encontrado en el discovery del gate.
- La VM 180 existente y sus discos NO se destruyen.

### HISTORICAL — rollback destructivo de la creación (julio 2026)

> Sólo junto con el procedimiento HISTORICAL de creación. DESTRUCTIVO: `DANGEROUS` + re-aprobación owner si ya hay data.

- `qm stop 180 && qm destroy 180` (DANGEROUS).
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

- [ ] VM PBS 180 adoptada e integrada (visible en `pve_storage` de los 5 nodos).
- [ ] Datastore `main` con chunks reales.
- [ ] 5 nodes registran storage sin error.
- [ ] vzdump manual PASS.
- [ ] Schedules activos.

## Linked owner tasks

- OWNER-TASK-MAINT-WINDOW (ventana integración PBS).
- OWNER-TASK-CRITICAL-VMS (lista tier 0).
- OWNER-TASK-SECRET-ZERO (passphrase).

## ✅ Tareas

- [x] **AGENT-TASK-02-0**: gate de adopción — acceso owner a VM 180 + discovery read-only + decisión reutilizar/reinstalar.
  - EJECUTADO 2026-09-18: accesos `ariadna@` demostrados en PBS (192.168.31.123) y 5 nodos; PBS 4.2.6-1 viva, VIRGEN (0 datastores/usuarios/jobs); decisión REUTILIZAR con evidencia; huella tier 0 medida (~165-185G used-in-guest por ciclo); gap de capacidad documentado (LV propuesto en VG local-kronos). Mutaciones → Owner Action Bundle (`~/aranea/work/r2-pbs-20260918/`). Evidencia: change log `2026-09-18-r2-pbs-discovery-effective`.
  - tags: [agent, gated, owner-interactive, done-2026-09-18]

- [ ] **AGENT-TASK-02-1**: descargar ISO PBS a kronos (HISTORICAL — sólo si el gate concluye reinstalación).
  - commands_allowed: wget, curl.
  - tags: [agent, prep, historical]

- [ ] **AGENT-TASK-02-2**: crear VM 180 (HISTORICAL — sólo si el gate concluye reinstalación; DANGEROUS — requiere ventana).
  - commands_allowed: `qm create`.
  - commands_forbidden: cualquier `qm destroy` sin re-aprobación.
  - tags: [agent, dangerous, vm-create, historical]

- [ ] **AGENT-TASK-02-3**: install PBS via ISO (HISTORICAL — sólo si el gate concluye reinstalación).
  - requiere noVNC, NO automatizable. Owner-driven o session interactiva.
  - tags: [agent, install, owner-interactive, historical]

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

- [x] **AGENT-TASK-02-7a**: backup piloto 155 + restore estructural 990 (ejecutado 2026-09-18 bajo mandato owner; ver bitácora).
  - tags: [agent, done-2026-09-18, pilot]

- [x] **AGENT-TASK-02-8**: aplicar fail-closed del datastore PBS (drop-in systemd; bundle v3 Acción 1) — EJECUTADO 2026-09-18 noche + **ACTIVADO Y CERTIFICADO 2026-09-19** (mandato owner 2: reboot único aprobado). Drop-ins en `proxmox-backup` Y `proxmox-backup-proxy` (extensión justificada: proxy=ingreso de backups, user `backup`). Activación demostrada en el boot real 22:24:05 (DropInPaths + `Requires="mnt-pbs\x2ddata.mount"` EN VIVO en ambos servicios, After, RequiredBy inverso, list-dependencies). **FAIL-CLOSED PASS declarado**: A instalada (hash 56eefebf), B activa tras reboot, C dependencia de arranque demostrada en ciclo real, D mecanismo demostrado por prueba negativa segura (exit 5 con mount inexistente / exit 0 con mount real) + ambos caminos de escritura cubiertos (API root + proxy backup, único proceso con FDs en el mount); BindsTo no requerido. Prueba física con des-adjuntar scsi1 = drill opcional de ventana futura.
  - tags: [agent, done-2026-09-19, fail-closed-pass, pbs-config]

- [x] **AGENT-TASK-02-9**: ejecutar medición 7 días — **ACTIVADA 2026-09-19** (gate fail-closed demostrado el mismo día; mandato owner 2). **Set final: 6 CTs** (155/156/154/101/147/115; **CT 148 EXCLUIDO PERMANENTEMENTE por mandato** — mecanismo de reincorporación automática eliminado del driver). Timer `aranea-r2-measure.timer` enabled (06:05 diario America/Santiago, ventana 06:00–07:25); primera ejecución PROGRAMADA dom 2026-09-20 06:05 (ventana sáb 19 perdida con el gate aún pendiente — sin corridas fuera de horario); **expiración absoluta 2026-09-26 pre-anclada** en `state/` (auto-disable el 27). Validaciones: dryrun 6 CTs exit 0 (148 ausente), TEST ventana SKIP, TEST camino ABORT completo PASS (timer real deshabilitado por el driver); fix de defecto real: `disable_timer` ahora con `sudo -n` (sin sudo el auto-disable habría fallado silencioso). Exclusiones v3 respetadas (mp0 de facto; 152/153; kafka; mt4; truenas); cero cambios en CTs/jobs.cfg/R1.
  - tags: [agent, gated, driver-ready, measurement]

- [x] **AGENT-TASK-02-10**: reboot controlado PBS (bundle v3 Acción 3) — **EJECUTADO 2026-09-19** (mandato owner 2: reboot único aprobado, sin la prueba negativa física opcional). Boot 22:24:05, fstab+drop-in+datastore validados post-reinicio (15/15 checks; detalle en bitácora y change log del día).
  - tags: [agent, gated, maintenance-window, owner-decision-pending]

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

**Status**: in-progress. R2 piloto ejecutado + cierre resuelto (2026-09-18); pendientes: OK owner bundle v3 (fail-closed, medición 7d, reboot), retención/schedules, criterios 7d.
**Sesión cerrada por instrucción del owner**: 2026-07-01.

## 📆 Bitácora

- **2026-08-10** — Migrado de `agent-project` legacy a `project` v1 sin activar la ejecución; owner, parent, lifecycle, progress, tags y secciones quedaron contractuales.
- **2026-09-18** — Continuidad documental (mandato owner): separación física entre HISTORICAL (creación desde cero, julio) y vigente (adopción + integración post-gate); rollback dividido en vigente (no destructivo) e HISTORICAL (destructivo); referencias operativas de creación alineadas a adopción; añadida AGENT-TASK-02-0 (gate de adopción). Historia preservada, decisiones congeladas intactas.
- **2026-09-18 (R2 discovery)** — Gate de adopción AGENT-TASK-02-0 EJECUTADO (mandato owner R2): accesos `ariadna@` demostrados (PBS .123 y 5 nodos, sudo NOPASSWD), PBS 4.2.6-1/Debian 13 viva y virgen (0 datastores, solo root@pam, sin jobs), F-06 a nivel disco confirmada (`scsi0: local-kronos:vm-180-disk-0`), `storage.cfg`/`jobs.cfg` intactos, VG local-kronos con 567.5G libres, huella tier 0 medida (~165-185G used-in-guest/ciclo; alloc 660G). Decisión 0.2: REUTILIZAR. Cero mutaciones (regla contrato 4.6): bundle owner único en `~/aranea/work/r2-pbs-20260918/` con A datastore (LV 300/500/650G), B credenciales (token recomendado), C tickets 018/019. Piloto y restore NOT EXECUTED. Evidencia: `80-agents/journal/logs/2026-09-18-r2-pbs-discovery-effective.md`.
- **2026-09-18 (R2 bundle v2)** — Owner corrigió el contrato de ejecución y aceptó A1-piloto + B-token: **650G descartado**; 300G = tamaño INICIAL DE PILOTO (no dimensionamiento final ni aprobación de retención 7d+4w+12m — se decide post-medición); disco nuevo identificado inequívocamente en ambas capas: `local-kronos/vm-180-disk-1` (PVE, serial `pbs-data`) + `/dev/disk/by-id/scsi-0QEMU_QEMU_HARDDISK_pbs-data` (guest), con baseline criptográfico pre (md5 qemu/lxc disk-lines, pvs, lvs) y regla **no-lvremove automático una vez con datos respaldados**; B: token mínimo (`user generate-token`, verificado en PBS 4.2 — `token` no existe como comando) + ACL `Datastore.Backup` a nivel usuario, verificación efectiva usuario Y token, secreto solo por stdin → `/etc/pve/priv/storage/aranea-pbs.pw` (storage.cfg sin secretos, plugin PBSPlugin.pm verificado); registro ÚNICO + propagación 5/5; C corregido: vzdump cubre SO/VM — PG 152 y Mongo 153 (data en iscsi `backup=0`), TrueNAS 145 (discos físicos 1TB×2) y data-disks Kafka quedan EXPRESOS con mecanismo complementario (dumps R3 / snapshots ZFS) o GAP, no "protegidos por vzdump parcial"; piloto 155 → restore CT 990 SIN boot ni quorum (verificación por montaje ro + destroy fixture); sintaxis datastore = flags `--keep-*` directos (sin `--prune-backups`), retención NO configurada en este bundle; prueba de persistencia = reboot controlado ÚNICO de PBS (contingencia de hotplug declarada). Esperando aprobación explícita del owner sobre `owner-action-bundle-v2.md` (v1 SUPERSEDED).
- **2026-09-18 (R2 piloto EJECUTADO)** — Mandato owner único ejecutado (ventana online 2h, sin downtime, SIN reboot). **A)** Disco nuevo `local-kronos/vm-180-disk-1` 300G añadido a VM 180 (`scsi1`, serial `pbs-data`, hotplug en VM viva), formateado por by-id, fstab por UUID con `nofail,x-systemd.device-timeout=10s` + **dir `/mnt/pbs-data` 000 anti-mount-vacío**; datastore `main` con `--verify-new true`. Corrección intra-fase: fstab quedó con UUID vacío (carrera udev tras mkfs); re-leído del device y reparado. **B)** `backup@pbs` + token `aranea`, rol `DatastoreBackup` (PBS 4.2: roles SIN punto — el bundle escribía el privilegio `Datastore.Backup`) sobre `/datastore/main` a usuario Y token; verificación efectiva exacta (solo Backup, sin Prune/Modify); secreto solo por stdin → `/etc/pve/priv/storage/aranea-pbs.pw` (600); registro ÚNICO `aranea-pbs` con fingerprint TLS capturado desde el propio PBS; **`pvesm status` active 5/5 nodos**, storage.cfg idéntico con 1 stanza, cfg sin secretos; `/tmp` sin residuos en PBS y kronos. **C) Backup piloto 155: PASS** — 25s, 2.05 GiB→472.5 MiB (~121 MiB/s), snapshot `ct/155/2026-09-18T22:15:24Z` con `verification.state=ok` (verify automático) + verify explícito TASK OK; CT corriendo ininterrumpido (uptime 40d). API del token: header `PBSAPIToken=<id>:<secreto>` SIN comillas (formato verificado en `PBSPlugin.pm`), curl `--config` 600. **D) Restore estructural CT 990: PASS** — `pct restore --storage local-lvm --unprivileged` (storage como OPCIÓN), NUNCA arrancado, `net0` productiva eliminada del config heredado (`--delete net0`, traía la IP del nodo etcd .251) + `onboot 0`; verificación por montaje ro OK; fixture destruido sin residuos (LVs fuera). **HALLAZGO material: `mp0` (`/var/lib/etcd`, los datos) está EXCLUIDO del backup por la config del propio CT 155** (task log: `excluding volume mount point mp0 from backup (disabled)`); el snapshot cubre rootfs+config TLS pero NO los datos etcd; corregirlo exige mutar config 155 (prohibida en el mandato) → decisión owner pendiente. **E)** 429 chunks; 731M/295G (0.25%). **G sustituida (sin reboot)**: `findmnt --verify` limpio + unit systemd-fstab-generator con fsck por UUID; reboot real pendiente de ventana específica. Evidencia: `80-agents/journal/logs/2026-09-18-r2-pbs-pilot-execution.md`.
- **2026-09-18 (R2 closeout)** — Mandato owner "cierre del piloto y preparación operativa" ejecutado (toda la fase read-only + local; cero mutaciones en infra). **Hallazgo etcd resuelto:** la exclusión de mp0 NO viene de un flag del CT 155 sino del **default de PVE 8.4.20** (mount points no-root excluidos sin flag explícito; verificado en `LXC/Config.pm` `mp_desc` y en las configs reales de 101/147/148/154/155/156, que comparten patrón rootfs+mp0 sin flags); rootfs SÍ entra. Decisión operativa provisional: **MANTENER exclusión de facto** (cero ediciones a CTs); protección de datos = cadena R1 (timer 05:00, run del día rev 56625/985 keys, 5/5 healthy) con **restore offline re-demostrado hoy** (etcdutl 3.6.4 exit=0 a scratch, NUNCA arrancado, borrado post-evidencia). Procedimiento de recuperación combinada documentado (R1 estructural PBS → R2 datos snapshot lógico → R3 servicio → R4 quorum; R1/R2 demostrados — R2 sólo offline —, R3/R4 NO demostrados). **Seguridad del montaje:** hallazgo de corrección — la protección "dir 000" del piloto NO quedó aplicada (`/mnt/pbs-data` = 755 backup:backup real); con `nofail` y servicios sin dependencia del mount, un arranque sin disco dejaría PBS (root) escribiendo chunks en raíz (38G libres). Propuesta fail-closed: drop-in `proxmox-backup.service.d/10-require-pbs-data.conf` (`Requires/After=mnt-pbs\x2ddata.mount`), validado localmente (`systemd-escape` + INI), con diff/pruebas/rollback en bundle v3 Acción 1; prueba negativa física diferida a ventana. **Línea base capacidad:** 733M/295G (1%), 429 chunks, snapshot única verified ok, VG soporte 267.5G libres; umbrales adv 70% / ABORT 85% / mínima 30G libres; retención lógica (no configurada) ≠ liberación física (GC ausente → sólo crece). **Plan 7 días (NO activado):** 7 CTs unprivileged con raíz en local-lvm (155/156/154/101/147/148/115), serie 03:05-04:30, driver local con log JSONL, cero estado persistente en PVE/PBS, métricas/ABORT/recuperación/criterio de éxito/desactivación definidos; exclusiones con causa (datos etcd mp0; 152/153 iscsi `backup=0`→R3 dumps; kafka pool1 Ceph GATED; mt4 `cache=unsafe` diferido; truenas passthrough→ZFS). **Riesgo storage:** Ceph pool1 87.16% nearfull pre-existente NO se corrige aquí y NO afecta al set activo (todo local-lvm); kafka GATED mientras persista. **Bundle ÚNICO v3** (`~/aranea/work/r2-pbs-20260918/owner-action-bundle-v3.md`): 3 acciones independientes — 1) fail-closed (aplicable hoy sin reboot), 2) medición 7d, 3) reboot controlado en ventana futura (+ prueba negativa física opcional) — con baseline criptográfico pre, preflight, ABORT y rollback por acción. Tareas nuevas: AGENT-TASK-02-8/02-9/02-10. Análisis completo: `~/aranea/work/r2-pbs-20260918/r2-closeout-analysis.md`. Evidencia: `80-agents/journal/logs/2026-09-18-r2-closeout.md`.
- **2026-09-18 (R2 ejecución de mandato)** — Owner aprobó acciones 1+2 del bundle v3 y rechazó la 3 (reinicio de PBS). **Baseline v3 §0 sin drift** (5 huellas + capacidad, re-verificadas pre-mutación). **Acción 1 ejecutada con extensión justificada:** el mandato exige cubrir los caminos de ingreso de backups ⇒ drop-ins idénticos instalados en `proxmox-backup` Y `proxmox-backup-proxy` (observado: proxy corre como usuario `backup`, dueño del datastore 755, con sólo `Wants=` sobre el API server y cero dependencia del mount). Verificación positiva manager-level PASS (DropInPaths en ambos, Requires/After con `mnt-pbs\x2ddata.mount`, mount unit con `RequiredBy=` ambos servicios, daemon-reload sin warnings, servicios active sin interrupción). Pruebas negativa/positiva seguras PASS con la misma sintaxis del drop-in en unidades temporales: mount inexistente → `Failed to start … not found` exit 5; mount real → exit 0; cleanup cero. `systemd-analyze verify` no soporta drop-ins/units generadas (artefacto registrado; validación real contra manager vivo). **CLASIFICACIÓN: PENDING ACTIVATION** — ambos servicios arrancaron antes del drop-in; daemon-reload no protege instancias vivas; activación efectiva requiere reinicio de servicios o el reinicio completo de la VM PBS (GATED/NO aprobado). FAIL-CLOSED PASS NO declarado; piloto NO habilitado por ese gate. **Acción 2: driver preparado y validado, NO activado** (plan B del mandato): `~/aranea/work/r2-pbs-20260918/measurement/` — r2-measure-day.sh (serial, 7 CTs orden v3, preflight+re-chequeo, verify main, JSONL, dryrun integrado, caducidad 7d + auto-disable, ventana 06:00–07:25 acotada) + r2-helper.sh + README-ACTIVACION.md; dryrun ×3 con correcciones en caliente (array GUESTS/GUEST_ORDER loop mudo; note() unbound; parse ceph df textual→JSON percent_used ×100). **Ventana 06:00–07:25 reconciliada con timers REALES medidos** (R1 04:00 dura ~6s; etcd 05:00 ~18s; pve-config sáb 08:30; nodos: sólo apt-daily/man-db 05:00-08:00; PBS: sólo daily-update 05:33) — horarios congelados de R1 intactos. **CORRECCIÓN placement: CT 148 rootfs = pool1 (Ceph RBD), no local-lvm como declara v3** ⇒ mismo gate que kafka: auto-excluido mientras pool1 ≥85% (87.21% medido al cierre); set efectivo 6 CTs (155/156/154/101/147/115). Integridad/cobertura intactas (restore funcional y quorum siguen NO demostrados; mp0 de facto; sin tocar CTs). Rollback de infra: rm de los 2 drop-ins + daemon-reload. Evidencia: `80-agents/journal/logs/2026-09-18-r2-mandato-ejecucion.md`.
