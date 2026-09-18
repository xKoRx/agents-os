---
type: runbook
schema_version: 1
scope: area
created: "2026-09-18"
updated: "2026-09-18"
area: "[[Aranea]]"
project: "[[HERMES — Infrastructure Operations]]"
application:
entities:
  - "[[Aranea]]"
  - "[[HERMES — Infrastructure Operations]]"
related:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[HERMES — ARANEA AUTONOMOUS OPERATIONS]]"
aliases:
  - Proxmox operator contract
  - contrato operador Proxmox
  - H2 operator contract
confidence: high
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/area
  - area/aranea
  - action/lifecycle
  - tech/proxmox
---

# proxmox-lifecycle-operator-contract

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

Contrato consumible que describe CÓMO deberá operar un proyecto ejecutor autorizado el ciclo de vida de VMs/LXC en el clúster Proxmox `aranea` (athena .10, zeus .100, hera .110, kronos .120, hades .90; PVE 8.4.20). Este runbook NO activa ni autoriza ninguna operación: la autoridad de ejecución nace del proyecto ejecutor y de sus gates propios ([[HERMES — Infrastructure Operations]] es carril de habilitación). La clasificación de autoridad por familia/operación vive en la matriz H2 (CSV de evidencia `~/aranea/work/h2-enablement-20260918/h2_authority_matrix.csv`, resumen en la nota del proyecto).

## Precondiciones

- Resolución inequívoca del target: `nombre lógico → VMID + nodo + entorno` contra el inventario vigente (JSON de inventario H0 o posterior más reciente). Ambigüedad = abortar la operación, nunca elegir el candidato más plausible.
- Quorum sano: `pvecm status` con `Quorate: Yes` (5/5 esperado). Sin quorum no se ejecutan cambios.
- Confirmación de que el guest NO está en la lista de recursos protegidos (ver abajo).
- Captura de config pre-cambio (`qm config <vmid>` o API GET config) guardada como evidencia: es la base del rollback.
- Autorización operativa vigente del proyecto ejecutor para la familia (power/config/create/migrate/teardown) y ventana operativa si el guest es productivo.
- Capacidad real del storage destino medida (no asumida): Ceph `pool1` estaba NEARFULL al 2026-09-18 — toda creación/crecimiento sobre pool1 exige plan explícito.

### Recursos protegidos (intocables sin gate owner explícito)

- VMs de negocio sobre storages `local-sqx-zeus/kronos/hera` (discos con `backup=0`, LVM clásico sin snapshots internos): p.ej. sqx-zeus (108), sqx-kronos (111), sqx-hera (123), worker-kronos (135).
- VM TrueNAS (145 @ hades): discos por `by-id` passthrough; jamás stop/destroy/config de discos.
- VM PBS (180 @ kronos, `local-kronos`): activo de Backup/DR R2; su ciclo de vida lo gobierna [[BACKUP-DR-OWNER-PROJECT]].
- Ceph (pool1/.mgr, OSDs): sin operaciones de reparación/rebalance desde este contrato.
- El resto de los 59 guests del inventario: teardown/destroy sólo con doble target proof y confirmación del owner salvo recurso creado por el propio ejecutor en la misma tarea.

## Procedimiento

1. Seleccionar canal en este orden: (1) API PVE con token `ariadna@pve!backup-dr` para lecturas per-VM cubiertas por `VM.Audit` (`/nodes/{n}/{qemu|lxc}/{vmid}/status/current`, `/config`); (2) SSH `ariadna@<nodo>` + sudo para todo lo demás (root-equivalent); (3) consola PVE por el owner como break-glass. El token NO sirve para `/cluster/*`, `/storage`, node status ni ninguna mutación (privsep=1; ver matriz H2).
2. Distinguir capacidad API de capacidad SSH: tener sudo NO implica que el token tenga lifecycle; y un 200 filtrado (lista vacía en `/storage`, `/cluster/tasks`, `/pools` sin `Sys.Audit`/`Datastore.Audit`) NO es evidencia de vacío real ni de permiso.
3. Power (start/stop/shutdown/reboot): target proof + estado actual leído en el mismo minuto; soft shutdown con timeout antes de hard stop; LXC `mcps`/Daedalus son críticos (sostienen el plano MCP): su restart es materia de [[HERMES — Agent Access Operations]] o gate propio.
4. Config/recursos: cambio mínimo reversible (`qm set` uno a uno), con config pre capturada; resize de disco sólo creciendo y verificando filesystem guest; nunca sobre discos `backup=0` sin plan de rollback documentado.
5. Create/clone: VMID libre verificado contra inventario (colisiones = abort); storages con espacio real; jamás convertir en template un guest protegido (`qm template` no es trivialmente reversible).
6. Migración: `local-sqx-*` y `local-kronos` son LVM `nodes`-restricted `shared=0` → migrar = mover discos completos (downtime real); `pool1` (RBD) es shared → migración liviana. Destino online + storage disponible + quorum antes de emitir `qm migrate`.
7. Concurrencia: un solo operador por guest a la vez; nunca dos cambios de config simultáneos sobre el mismo VMID; operaciones de storage masivas (move-disk) serializadas y fuera de ventanas de backup (R2 futuro).
8. Timeouts y parciales: toda operación con timeout explícito; si una operación queda parcial (task running, estado intermedio), NO reintentar a ciegas: leer task/status real, esperar o compensar según estado observado; repetir un side-effect incierto sólo después de demostrar por estado durable que no ocurrió.
9. Idempotencia donde el comando lo permita (config `set` al valor deseado es idempotente; create/destroy no: verificar existencia antes).
10. Evidencia auditable por operación: timestamp UTC, VMID+nodo, canal, identidad (sin secretos), comando/endpoint, resultado, config pre/post, task ID o exit, clasificación outcome. Sin secretos en evidencia; rutas y nombres only.

## Validación

- Post-change: la capa que posee la semántica valida — power: `status/current` + servicio interno del guest UP (un exit 0 NO prueba el servicio); config: `qm config` refleja el valor + el guest lo percibe; migrate: guest running en destino + servicio UP; create/clone: guest arranca y responde según su rol.
- Contrastar dos fuentes cuando existan (API + SSH) ante cualquier resultado sorpresivo; contradicción = investigar, no promediar.
- Registrar el cambio en el proyecto ejecutor y, si toca canon de habilitación, devolver hallazgos a [[HERMES — Infrastructure Operations]].

## Rollback / recuperación

- Config: reaplicar los valores de la config pre capturada (paso a paso, verificando cada uno).
- Power: operación inversa (start/stop) + verificación de servicio; tras hard stop asumir fsck/verificación dentro del guest.
- Migración: migrar de vuelta al origen si el destino se degrada.
- Snapshot/restore: hoy NO hay red de seguridad (0 snapshots en guests verificados y 0 jobs de backup en PVE; PBS virgen pendiente R2): el rollback de datos NO existe hasta que R2 opere —factor de riesgo dominante a declarar en toda tarea.
- Acceso: si la API PVE falla → SSH+sudo (canal independiente verificado); si SSH falla → consola PVE por owner (break-glass); llaves SSH de Ariadna viven en `~/.ssh/` de hermes-vm con `from=192.168.31.122` (si hermes-vm muere, el owner reinstala acceso por consola física).
- Abort inmediato y escalamiento al owner: target ambiguo, quorum perdido, guest protegido involucrado, secreto expuesto, resultado incierto tras un reintento, o cualquier efecto fuera del scope autorizado.

## Evidencia

- Clasificación de autoridad por operación (34 filas, familias A–G, 2026-09-18): `~/aranea/work/h2-enablement-20260918/h2_authority_matrix.csv` + probes crudos del mismo directorio (`ssh_sweep*_out.txt`, `api_probe.out`); resumen y límites en [[HERMES — Infrastructure Operations]].
- Change log de la habilitación: `80-agents/journal/logs/` (entrada H2 2026-09-18).
- Estado vivo del clúster al momento del contrato: quorum 5/5, 59 guests (39 qemu + 20 lxc), 10 storages, Ceph HEALTH_WARN (osd.0/osd.2 nearfull), HA vacío, 0 jobs de backup.
