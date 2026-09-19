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
  - "[[high-impact-networking-dns-contract]]"
  - "[[proxmox-lifecycle-operator-contract]]"
  - "[[provisioning-operator-contract]]"
aliases:
  - cluster node maintenance contract
  - contrato mantenimiento nodos quorum
  - H5 cluster contract
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
  - tech/proxmox
  - tech/quorum
---

# cluster-node-maintenance-contract

%% Routing: area/project/application/entities/related usan links canónicos. Aliases son variantes humanas; tags/paths usan slugs. %%

## Propósito

Contrato del futuro operador de mantenimiento de nodos Proxmox y operaciones sensibles al quorum (familias C y J del índice [[30-resources/aranea/06-high-impact/00-index|high-impact]]). Cubre mantenimiento de nodos, cambios cluster-level, operaciones sensibles al quorum y recuperación tras fallo parcial. **Enablement-only:** NO autoriza operaciones; la ejecución es del proyecto ejecutor con owner gate para toda operación CLASS 3.

Estado habilitación (2026-09-19): **C/J = VERIFIED_READ** — quorum 5/5, servicios activos 5/5, corosync y HA leídos en vivo; SSH+sudo EJERCIDO en los 5 nodos (H1/H2/H4/H5); recuperación ante pérdida de nodo NO demostrada.

## Baseline verificado 2026-09-19

- Cluster `aranea`: 5 nodos, 1 voto c/u, quorate=yes en los 5, `Highest expected: 5`, `two_node` NO configurado.
- Corosync `ring0_addr`: IPs LAN .10/.90/.100/.110/.120 — **sin red dedicada de cluster** (riesgo: saturación LAN o mantenimiento de OPNsense puede degradar latencia de quorum).
- `datacenter.cfg` = `keyboard: es` (defaults: sin HA activa, sin fencing especial); HA sin recursos (`ha-manager status` = quorum OK, sin groups/resources).
- Servicios pve-cluster/pveproxy/corosync/pvedaemon activos 5/5; kernel drift: athena `6.8.12-29-pve` vs resto `6.8.12-18-pve` (reboot de athena = cambio de kernel + SPOF simultáneos — exigir owner gate reforzado).
- Guests por nodo (H5): athena 1 qemu+5 lxc, zeus 5+1, hera 7+3, kronos 10+1, hades 16+10 (= 39 qemu + 20 lxc).

## Precondiciones (para el ejecutor futuro)

1. Target proof: hostname + VMID real + estado vivo; jamás operar por "el nodo de la VM X" sin `qm status` verificado.
2. Ventana de mantenimiento aprobada por el owner (CLASS 3 obligatorio para reboot/shutdown de nodo).
3. Verificaciones GO previas: quorum 5/5 (`pvecm status`), Ceph sano si el nodo lleva OSD/MON (`ceph -s`; con nearfull vigente, NO_GO para drenar OSDs — ver [[ceph-storage-operations-contract]]), sin jobs PBS/vzdump activos, storage del nodo identificado (`pvesm status`).
4. Drenaje: si el nodo tiene guests, migrarlos ANTES sólo si el ejecutor tiene autoridad de lifecycle ([[proxmox-lifecycle-operator-contract]]); VMs con discos en `local-sqx-*`/`local-kronos`/`local` NO son migrables sin move-disk (CLASS 2).
5. Con athena: recordar que OPNsense 130 y Pi-hole 149 viven ahí — reboot de athena = corte de gateway+DNS+Tailscale+CA para todo el cluster (incl. el quorum mismo, que corre por LAN).

## Condiciones NO_GO (abort inmediato)

- Target ambiguo o conflicto de identidad (N4 del índice H5).
- Quorum < 5/5 o `expected votes` anómalo.
- Ceph HEALTH_WARN vigente en el nodo a mantener (hoy: osd.0 hera y osd.2 zeus, ambos nearfull ~85.6%) — drenaje u operaciones OSD prohibidas.
- Storage del nodo con dependencias desconocidas (guests de otro proyecto corriendo).
- Sin ventana aprobada, sin rollback escrito o con otro cambio de infraestructura en vuelo.
- PBS 180 o cualquier guest sagrado (SQX 108/111/123/135) en el nodo sin plan de protección confirmado por lectura (`qm config` — backup=0 verificado H2: los SQX NO tienen red de seguridad de snapshots).

## Procedimiento (plantilla del ejecutor — no ejecutado)

1. Preflight completo (precondiciones 1–5) con captura de evidencia en `~/aranea/work/<run>/`.
2. Drenaje de guests migrables (si autorizado), marcando los no-migrables como down esperado.
3. Mantenimiento mínimo: reboot/shutdown vía SSH `ariadna` (autoridad existente, AUTHORIZED_NOT_EXERCISED para power ops).
4. Post: `pvecm status` quorate 5/5, servicios activos, Ceph sano si aplica, guests reintegrados, storage disponible (`pvesm status`).
5. Verificación desde hermes-vm (management plane intacto).

## Validación

- `pvecm status` 5/5 quorate en todos los nodos tras la operación.
- Los 39 qemu + 20 lxc en el estado esperado (running/stopped igual al pre).
- `ceph -s` sin degradación nueva (los warnings nearfull preexistentes no cuentan como degradación nueva).
- SSH `ariadna` desde .122 funciona a los 5 nodos.

## Rollback / recuperación

- Rollback de un cambio cluster-level fallido: revertir el archivo `/etc/pve/` correspondiente (siempre capturado en preflight); en conflicto de config, detenerse y escalar al owner — nunca "arreglar" `/etc/pve/corosync.conf` a mano.
- Pérdida de un nodo: sin demostración operativa — el recovery documentado es consola del owner + reinstalación/rejoin; NOT_CERTIFIED hasta que un ejecutor lo demuestre en ventana.
- Pérdida de quorum total: no existe procedimiento certificado; escalar al owner (consola física).

## Evidencia

- Sondas read-only 2026-09-19: `~/aranea/work/h5-high-impact-20260919/probes/pve_probe_20260919_{10,100,110,120,90}.txt`.
- Matrices H1/H2/H4 en [[HERMES — Infrastructure Operations]].
- Change log H5: `80-agents/journal/logs/2026-09-19-h5-high-impact-enablement.md`.
