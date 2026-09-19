---
type: runbook
schema_version: 1
scope: area
created: "2026-09-19"
updated: "2026-09-19"
area: "[[Aranea]]"
project: "[[HERMES — Infrastructure Operations]]"
application:
entities:
  - "[[Aranea]]"
  - "[[HERMES — Infrastructure Operations]]"
related:
  - "[[provisioning-operator-contract]]"
  - "[[cluster-node-maintenance-contract]]"
  - "[[BACKUP-DR-OWNER-PROJECT]]"
aliases:
  - ceph storage operations contract
  - contrato ceph storage
  - H5 ceph contract
confidence: high
source_session:
load_policy: manual
indexable: true
index_priority: high
tags:
  - kind/runbook
  - scope/area
  - area/aranea
  - action/high-impact
  - tech/ceph
  - tech/storage
---

# ceph-storage-operations-contract

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

Contrato del futuro operador de Ceph y storage distribuido Aranea (familia D del índice [[30-resources/aranea/06-high-impact/00-index|high-impact]]). Cubre resolución del nearfull, rebalance, operaciones OSD/MON y criterios GO/NO_GO de capacidad. **Enablement-only:** NO autoriza operaciones; la ejecución es del proyecto ejecutor con owner gate para toda operación CLASS 3.

Estado habilitación (2026-09-19): **D = VERIFIED_READ** — health/pools/OSD leídos en vivo desde los 3 MONs; ninguna operación de reparación ejecutada ni autorizada.

## Baseline verificado 2026-09-19 (sondas 3/3 MONs consistentes)

- `HEALTH_WARN`: 2 OSD nearfull (osd.0 85.65%, osd.2 85.59%), 2 pools nearfull (pool1 87.26% — 834.3G/956.2G, 121.9G avail; .mgr), fragmentación bluestore 0.903/0.900, 189 PGs active+clean, VAR 0.63–1.33.
- Topología: 4 OSD NVMe (osd.0 hera, osd.1 kronos, osd.2 zeus, osd.3 kronos), 3 MONs (**en LAN 192.168.31.x, NO en la red Ceph 10.10.10.0/24**), 2 MGR, sin CephFS. Replicación x3, min_size 2.
- Pools: `pool1` (RBD, aplicación rbd, 128 PGs, selfmanaged_snaps) y `.mgr`. `pool1` alimenta discos de VMs vía storage `pool1` de PVE (shared, 5/5 nodos).
- Drift vs H4 (87.17%): ninguno material. **NO_GO de provisioning sobre pool1 vigente** ([[provisioning-operator-contract]]).
- athena no puede consultar Ceph (sin conf local) — hallazgo H4 que persiste: las consultas deben hacerse desde zeus/hera/kronos.

## Precondiciones (para el ejecutor futuro)

1. Consultar sólo desde MONs (zeus .100, hera .110, kronos .120) con SSH `ariadna`+sudo; nunca desde athena.
2. Target proof del problema real: `ceph -s` + `ceph osd df` + `ceph health detail` capturados en el run.
3. Ventana de mantenimiento aprobada (toda operación OSD/rebalance es CLASS 3, owner-gated).
4. Verificar que ninguna escritura crítica esté en vuelo (PBS jobs, backups, workloads SQX activos).
5. Confirmar salud de los 3 MONs y quorum Ceph antes de tocar OSDs.

## Clasificación de operaciones

- CLASS 1: lectura de health/stats; ajuste de pesos de alerta (nearfull/full ratio) documentado y reversible.
- CLASS 2: rebalance dirigido (reweight de un OSD), expansión de PGs de pool1 (128→256), liberación de espacio borrando discos huérfanos identificados y confirmados con su proyecto.
- CLASS 3 (owner-gated): add/remove OSD, cambios CRUSH, cambio de monmap, operación sobre pool `.mgr`, scrub manual profundo en nearfull, cualquier operación con pérdida potencial de datos.

## Procedimiento de resolución del nearfull (plantilla del ejecutor — NO ejecutado)

1. Identificar consumidores reales de pool1: `rbd ls pool1` + cruzar con `qm config` de los 39 qemu (discos `pool1:vm-XXX-disk-N`) y los rootfs de LXC en pool1 (H4: 5 LXCs con rootfs en pool1).
2. Candidatos de liberación (sólo con confirmación del proyecto dueño): discos `unused0` (p.ej. anomalía conocida de sqx-hera 123: unused0/unused1 en pool1 + local-lvm), discos de guests eliminados, VMIDs extintos (112 kronos-sqx-deprecado, 162, 170).
3. Orden de ataque recomendado por riesgo ascendente: (a) borrar discos huérfanos confirmados [CLASS 2]; (b) reweight de osd.0/osd.2 para distribuir hacia osd.1/osd.3 (40%/46% vs 85%) [CLASS 2]; (c) expandir PGs si el autoscaler no lo hace [CLASS 2]; (d) add OSD nuevo [CLASS 3].
4. Verificar después de cada paso: `ceph -s` (los nearfull deben despejarse cuando los OSD bajen de ~85% y pools de ~85%).
5. NO GO si durante la operación aparece: degraded/remapped PGs sin converger, latencia de clientes (SQX en vivo), o pérdida de quorum MON.

## Validación

- `HEALTH_OK` (o HEALTH_WARN residual sin nearfull) consistente en los 3 MONs.
- `ceph osd df`: VAR dentro de 0.8–1.2; ningún OSD > 80%.
- Guests sobre pool1 operando sin latencia anómala (verificar con su proyecto).
- Sin pérdida de objetos: `ceph osd pool ls detail` con los mismos object counts esperados (+/- los eliminados conscientemente).

## Rollback / recuperación

- Reweight y ratios: reversibles re-aplicando el valor previo (capturado en preflight).
- Borrado de discos: NO reversible — exige confirmación del proyecto dueño + snapshot/backup previo cuando sea posible (hoy: PBS opera; los guests sin backup=1 NO tienen red de seguridad — recordar backup=0 de los SQX).
- Recuperación ante fallo de OSD: documentación de recuperación NO demostrada (NOT_CERTIFIED) — escalar a owner; consola física como break-glass.
- Si la operación degrada pool1 con clientes arriba: abortar, dejar converger, reportar; NO empeorar con una segunda operación.

## Evidencia

- Sondas read-only 2026-09-19 (3 MONs): `~/aranea/work/h5-high-impact-20260919/probes/ceph_probe_20260919_{100,110,120}.txt`.
- Baseline H4 y criterio de capacidad: [[provisioning-operator-contract]], matrices en [[HERMES — Infrastructure Operations]].
- Change log H5: `80-agents/journal/logs/2026-09-19-h5-high-impact-enablement.md`.
