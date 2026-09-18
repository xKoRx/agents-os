---
type: change_log
schema_version: 1
created: 2026-09-18
area: "[[Aranea]]"
project: "[[HERMES — Infrastructure Operations]]"
tags:
  - kind/change-log
  - area/aranea
  - project/hermes-aranea-autonomous-operations
  - domain/infrastructure
---

# 2026-09-18 — H1 Enablement · Infrastructure Operations (cero mutaciones)

## Alcance del mandato

Decisión owner: separación **Infrastructure Enablement** (este carril: certificar identidades, permisos, rutas de recuperación y documentación) vs **Backup/DR Execution** ([[BACKUP-DR-OWNER-PROJECT]]: PBS, jobs, backups, restores, drills). Este carril NO ejecuta operaciones de otros proyectos. Prohibido explícitamente: backups/restores, lifecycle, mutaciones de config, credenciales nuevas, runner R1.6, Pi-hole/step-ca, y usar una mutación como prueba de permisos. Permitido: lectura y preparación documental.

## Corrección de autoridad del proyecto

`HERMES — Infrastructure Operations`: objetivo reescrito a habilitación; H1 redefinido como **Backup & Storage Administrative Enablement** con gate `H1 ENABLEMENT PASS` (el texto anterior que ordenaba ejecutar backups/drills quedó HISTORICAL); H2–H6 convertidos a enablement-only (clasifican autoridad/contratos, no operan); SPEC H0 2026-09-18 marcado HISTORICAL; tareas I2.1–I2.5 reemplazadas por tareas de habilitación verificables; matriz de autoridad H1 nueva; Estado/Bitácora actualizados. Programa padre: referencia "ejecutar/verificar jobs → restore drill" de la Fase 3 corregida a enablement + entrada de bitácora. Boundary del Agent Access Plane intacto.

## Reconciliación de accesos instalados (inputs del owner → evidencia)

Identidades instaladas por el owner 2026-09-18: llaves SSH `ariadna_pve` / `ariadna_truenas` / `ariadna_pbs` (ED25519, sin passphrase, en `~/.ssh/` de hermes-vm), token API PVE `ariadna@pve!backup-dr` (privsep=1, expire=0, ACL `/vms` AriadnaVMBackup), api-key TrueNAS `ariadna-admin-20260918` (user `ariadna` uid 3005, FULL_ADMIN, password_disabled). Resumen por familia (detalle: matriz de autoridad H1 en la nota del proyecto):

- **G1 — Proxmox PASS**: SSH `ariadna@` + `sudo NOPASSWD: ALL` en 5/5 nodos (athena .10, zeus .100, hera .110, kronos .120, hades .90); API 200 en 5/5 para `version`+`cluster/resources` (59 guests = 39 qemu + 20 lxc, exacto vs inventario H0); vía sudo local: `pvecm status` Quorate 5/5, `storage.cfg` con 10 storages y sin `pbs`, **jobs de backup = 0** (`/cluster/backup` = `[]` vía `pvesh` con sudo; `/etc/pve/jobs.cfg` no existe — cierra con evidencia viva el fact 12 MISSING de H0). Límites: token API scope `/vms` únicamente (`/cluster/status`, `/cluster/backup`, `/storage` → 403, comportamiento correcto); permisos H2 (lifecycle) clasificados por ACL, NO ejercidos. Emergencia independiente: SSH+sudo.
- **G2 — TrueNAS PASS**: WS DDP `wss://.91/websocket` con api-key: 25.04.1, pool0+pool2 ONLINE healthy, 202 datasets (173 FS + 29 VOL), 606 snapshots, replication/cron/cloudsync = 0, servicios RUNNING (cifs/nfs/iscsitarget/smartd/ssh); SSH `ariadna` + `sudo (ALL) NOPASSWD: ALL` como recovery independiente. Gap menor: `snapshot.query`/`snapshottask.query` dan ENOMETHOD (25.04 renombró a `zfs.*`); método definitivo de snapshot-tasks por verificar (`task.query`/oneshot). Extents iSCSI no releídos (material H2/H3, R0 ya lo registró).
- **G3 — PBS PASS con límite**: SSH `ariadna@192.168.31.123` + sudo ALL; `proxmox-backup-server 4.2.6-1` (running 4.2.5), Debian 13.6, kernel 7.0.14-8-pve, servicios api+proxy activos, UI :8007 con wall 401 (jamás se probó login); `datastore list` vacío, `user.cfg` solo root@pam, sin remote/sync — **PBS VIRGEN**, consistente con el discovery R2 de Backup/DR del mismo día. Límite: RBAC/API PBS sin credencial propia (no existe aún; el usuario/token de PBS es material del ejecutor en R2).

## G4 — consumidor real desde sesión fresca (hermes CLI)

- **G4.0 carga de canales: PARTIAL — hallazgo real**: `aranea-postgres-ro` (13) + `aranea-observability-ro` (24) cargan; **`aranea-ssh` no aparece en sesión fresca**: initialize contra `192.168.31.219:3000` devuelve **503 persistente 3/3** con container healthy 20h, `/status` 200 y `connections:[]`, sin líneas de límite en logs (3h). Config del perfil correcta (entrada presente, ref `${VAR}` en `.env` 600, bearer válido — probe autenticado llega al server). Diagnóstico: pool de sesiones saturado (consumers que no hacen DELETE desde el restart de ayer); remediación canónica = `docker restart ssh-mcp` vía `mcps-ops` — **NO ejecutada por prohibición de este mandato** (mutación del plano). Este mismo `mcps-ops` seguía operativo → la independencia quedó demostrada EN VIVO con el plano degradado.
- **G4.1 PVE nativo: PASS** — sesión fresca resolvió clúster/quórum (Quorate Yes 5/5) y PBS (4.2.6-1, 0 datastores) vía SSH `ariadna` con llaves, sin secretos en el prompt ni preguntas al owner (evidencia `g4_output/g4_1_native.txt`).
- **G4.3 TrueNAS nativo: PASS** — sesión fresca construyó y ejecutó la consulta WS DDP (system.info + pool.query) leyendo la key de disco, sin imprimirla, con logout y limpieza; documentó además el quirk posicional de `pool.query` en su skill (evidencia `g4_output/g4_3_native.txt`).
- **G4.5 management independence: PASS** — `mcps-ops 'hostname'` → `mcps`, con el plano MCP en 503 simultáneo (evidencia `g4_output/g4_5_mgmt.txt`).
- Sin logout de UI, sin creación de recursos, sin snapshots, sin jobs: **zero infrastructure mutations**.

## Gaps y clasificación

| # | Gap | Clase | Impacto H1 | Acción |
|---|---|---|---|---|
| 1 | ssh-mcp 503 pool (plano consumidor) | BLOQUEO PROBADO del plano MCP | Ninguno para enablement (canales nativos OK; G4.0 parcial) | Recovery `docker restart ssh-mcp` vía `mcps-ops` + recert `tools/list`=13 en sesión nueva — pendiente de autorización (fuera de este mandato) |
| 2 | TrueNAS snapshot-tasks ENOMETHOD | gap menor de cobertura | Ninguno (replication/cloudsync/cron leídos; snapshots listados 606) | Verificar `task.query`/oneshot en próxima ventana read-only |
| 3 | PBS sin credencial API propia (solo root@pam) | BY-DESIGN pre-R2 | Ninguno: 0 datastores = nada que certificar operativamente | El ejecutor R2 crea usuario/token PBS dentro de su gate |
| 4 | Token PVE sin `Sys.Audit` en `/` | alcance elegido | Ninguno: lecturas cluster-level cubiertas por SSH+sudo | Extensión = decisión owner sólo si R2 la necesita |

**No se requiere owner action bundle nuevo para H1**: ningún gap bloquea el gate; el único bundle vigente es el de R2, ya entregado por Backup/DR (`~/aranea/work/r2-pbs-20260918/owner-action-bundle.md`, bloques A/B/C con rollback).

## Handoff H1 → Backup/DR R2 (consumible)

Capacidades certificadas disponibles para R2 sin bootstrap humano adicional: (1) SSH admin `ariadna` + sudo NOPASSWD en 5 nodos PVE y en PBS .123 (llaves por referencia en `~/.ssh/` de hermes-vm; PVE/PBS con `from=192.168.31.122`); (2) API PVE token `ariadna@pve!backup-dr` para `cluster/resources` y per-VM read (`/vms`); (3) TrueNAS FULL_ADMIN por WS DDP + SSH+sudo + `midclt`; (4) lecturas PVE cluster-level (jobs/storage/quorum) vía SSH+sudo (`pvesh`, `pvecm`, `storage.cfg`); (5) transporte TrueNAS DDP documentado (skill `truenas-admin-operations`, references `websocket-ddp-protocol.md`). Condiciones que R2 debe conocer: PBS virgen (datastore/usuario/jobs = trabajo de R2 con su bundle owner); 0 jobs de backup en PVE (verificado hoy); token PVE NO sirve para lecturas `/cluster/*` por API (usar SSH+sudo); snapshot-tasks TrueNAS por confirmar; plano ssh-mcp degradado 503 (no afecta R2 por canales nativos). R2 NO arranca desde este carril.

## Propuesta Request-Change contractual (PREPARADA, NO APLICADA)

Incompatibilidad detectada: `BACKUP-DR-CONTRACT` §4.6 («NO ejecutar nada en Aranea sin gate técnico aprobado en chat») y §7 («no habilita implementación hasta aprobación explícita para cada gate técnico») impiden la autonomía operativa persistente que el programa persigue. Propuesta mínima (a registrar por el owner/proyecto Backup/DR en `REQUEST-CHANGES.md`, no aplicada aquí): sustituir la aprobación por-acción en chat por **gates por clase de operación** (p.ej. clase "backup job create/update", clase "restore drill", clase "storage config") aprobados una vez; la ejecución dentro de una clase aprobada queda autónoma con evidencia, bitácora y rollback; fuera de clase sigue gated. La aprobación y aplicación de ese cambio pertenecen al owner y al proyecto Backup/DR.

## Verificación y publicación

- Zero infrastructure mutations: sin ejecución de `qm/pct/pvesm` mutantes, sin snapshots, sin creaciones, sin restarts, sin login UI, sin credenciales nuevas; únicos 403 de API PVE por GET de endpoints mutantes-adyacentes (`/cluster/backup`, `/cluster/status`, `/storage`) como read-intent declarado.
- Secretos: ningún valor impreso ni persistido; referencias por nombre/path únicamente. Evidencia cruda en `~/aranea/work/h1-enablement-20260918/` (fuera del vault).
- Cambios documentales: `10-projects/Aranea/agentes/HERMES — Infrastructure Operations.md` (corrección completa), `10-projects/Aranea/HERMES — ARANEA AUTONOMOUS OPERATIONS.md` (referencia Fase 3 + bitácora), `BACKUP-DR-OWNER-PROJECT.md` (nota de habilitación), `30-resources/aranea/01-topologia/fechas-captura.md` (fila 2026-09-18). Publicación vault→GitHub por el flujo canónico (~1 min, otra máquina); repo local Hermes = consumidor.
