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
  - "[[2026-09-16-R0-reconciliacion]]"
aliases:
  - "R2 PBS discovery efectivo 2026-09-18"
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-18-backup-dr-r2-session-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
  - area/aranea
  - project/backup-dr
---

# 2026-09-18 — R2 PBS: discovery efectivo (accesos demostrados) + bundle owner

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/agent-project-02-pbs-on-backup-node.md` (AGENT-TASK-02-0: discovery ejecutado + decisión reutilizar con evidencia; bitácora; frontmatter `updated`)
  - `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/BACKUP-DR-OWNER-PROJECT.md` (bitácora R2 discovery; frontmatter `updated`)
  - `80-agents/journal/logs/2026-09-18-r2-pbs-discovery-effective.md` (este log)
  - `~/aranea/work/r2-pbs-20260918/owner-action-bundle.md` + `execution-plan.md` (FUERA del vault, workspace operativo; bundle mutador consolidado)

## Motivo

- Mandato owner (2026-09-18): R2 adopción e integración de PBS con accesos ya disponibles, sin pedir credenciales instaladas, gates vigentes respetados, y UN Owner Action Bundle para lo mutador pendiente.

## Fuentes usadas

- **OBSERVADO (live, read-only, sin secretos impresos):**
  - PBS `192.168.31.123` (`ariadna@`, key `ariadna_pbs`, sudo NOPASSWD): `proxmox-backup-manager version` = 4.2.6-1 (running 4.2.5); Debian 13; servicios `proxmox-backup` + `-proxy` running; datastore list = VACÍO; users = solo `root@pam`; ACL vacía; remote/sync/verify/prune/gc jobs = ninguno; `df /` = 47G total, 7.2G usados, 38G libres; disco único `sda` 64G (LVM `pbs-swap` 7.8G + `pbs-root` 47.9G); `/var/lib/proxmox-backup` = 1.1M; tasks archive = solo logrotate/aptupdate diarios (ningún backup histórico); FQDN `pbs.lab.aranea`.
  - PVE kronos `192.168.31.120` (`ariadna@`, key `ariadna_pve`, sudo NOPASSWD): `qm config 180` = name pbs, 4 cores, 8192 MB, `scsi0: local-kronos:vm-180-disk-0,size=64G` (F-06 demostrada a nivel disco), description "sin datastore aún"; `storage.cfg` sin entrada pbs (sha256 e9a94fbb…); `jobs.cfg` VACÍO (sin vzdump jobs); VG `local-kronos` 931.5G con 567.5G libres; `pvesm status` kronos: local-kronos 39% usado.
  - Cluster: `pvecm nodes` = hera/zeus/hades/kronos/athena; `ariadna@` verificado en los 5; `storage.cfg` idéntico en zeus (mismo sha256, sin `pbs`).
  - Huella tier 0 (contrato §2, 23 workloads, medida live `pvesh` + `qm guest cmd`): alloc 660G; used-in-guest sumado ~165-185G por ciclo (mt4 C: 32.1G + 25.0G + 24.7G + 21.4G; kafka 3× ~17.5-18.8G; postgres ~4.7G; mongo ~6.9G; argus 20.9G; echo 6.0G; etcd 5× ~2-3G; LXC ligeros). Cifra de dimensionamiento, no canónica.
- **DOCUMENTADO:** contrato §2 (23/16 congelado), R0 (ADDs propuestos no aprobados), ap-02 (procedimiento adopción), log `2026-09-18-pbs-identity-conflict.md` (identidad 180/123/111; aquí sólo re-verificada en vivo hostname/IP/VMID).

## Resolución aplicada

- **Acceso administrativo PBS: PASS** (no bloqueado): SSH demostrado en PBS y 5 nodos PVE con las dos keys nuevas (`~/.ssh/ariadna_pbs`, `~/.ssh/ariadna_pve`, creadas 2026-09-18 13:05/13:23, ED25519); sudo NOPASSWD funcional en PBS y kronos; sin impresión de secretos.
- **Discovery PBS efectivo: PASS.** PBS viva, actualizada y administrable pero VIRGEN funcional (0 datastores, 0 usuarios de integración, 0 jobs). La adopción es de CONFIGURACIÓN, no de instalación/recuperación. Decisión gate 0.2: **REUTILIZAR** (evidencia arriba); reinstalación queda HISTORICAL y descartada.
- **F-06 confirmada a nivel disco** (VM 180 reside en VG `local-kronos`). Gap de capacidad: los 38G internos NO alcanzan para tier 0 (~600G con retención 7d+4w+12m sobre huella full ~185G); se propone LV dedicado en la MISMA VG `local-kronos` (consistente con F-06): A1 300G / A2 500G / A3 650G, en bundle.
- **Gates re-clasificados con evidencia:** tickets 018/019 siguen `todo` (sin resolución formal en vault ni RC); NO existe autorización explícita previa para datastore/LV+mkfs ni para `pvesm add`. Por contrato regla 4.6 y modelo AUTO/GATED, NINGUNA mutación se ejecutó. `pvesm status`/`storage.cfg` verificados intactos; `jobs.cfg` vacío (sin riesgo de vzdump fantasma).
- **Entregado OWNER ACTION BUNDLE único** (`~/aranea/work/r2-pbs-20260918/owner-action-bundle.md`): A datastore (tamaño + quién ejecuta mkfs), B credenciales (user vs API token, recomendado token), C formalización 018/019; target/diff/riesgo/rollback/autorización mínima por ítem; plan post-OK ~30-45min (A → B → backup piloto → restore drill).
- **Backup piloto / restore drill: NOT EXECUTED** (requieren bloques A+B aprobados).
- R1.6 sigue PAUSADO (no tocado). D0 no reabierto. Cierre de sesión ejecutado aparte por pedido explícito del owner (feedback incluido), no como ritual.

## Validación

- Sin mutación: `storage.cfg` sha256 idéntico pre/post sesión (kronos y zeus); `jobs.cfg` vacío; datastore list PBS vacío antes y después; 0 comandos de escritura en infra (solo `qm config/status`, `pvesh get`, `pvesm status`, `cat`, `ls`, `df`, `vgs`, `ss`, `du`, `proxmox-backup-manager * list`, `qm guest cmd get-fsinfo`).
- Identidad PBS re-verificada en vivo: hostname `pbs.lab.aranea`, IP .123, VMID 180 en kronos (coherente con log identidad 18sep).

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales, memoria interna ni secretos

## Rollback

- Documental: borrar este log + revertir bitácora/frontmatter en ap-02 y proyecto owner. No hay rollback de infra (cero mutaciones).
