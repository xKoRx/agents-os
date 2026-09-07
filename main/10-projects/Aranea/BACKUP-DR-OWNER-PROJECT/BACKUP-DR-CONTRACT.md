---
title: "Contrato Canónico Backup/DR Aranea"
type: doc
schema_version: 1
status: active
icon: 📜
slug: backup-dr-contract
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: 2026-07-02
updated: 2026-08-10
approved: 2026-07-02
aliases:
  - Contrato canónico Backup/DR
  - Backup DR contract
tags:
  - kind/doc
  - area/aranea
  - domain/backup-dr
  - doc/contract
  - authority/rule-of-record
related:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[BACKUP-DR-DESIGN]]"
  - "[[CONTRATO-CANONICO-PROPUESTA]]"
---

# 📜 Contrato Canónico Backup/DR Aranea

## Propósito

Mantener la regla viva y aprobada del proyecto Backup/DR Aranea, sin reemplazar el diseño congelado de referencia.

## Contenido

> **Status**: active. Aprobado por owner 2026-07-02.
> Este documento es **regla viva** del proyecto Backup/DR. No reemplaza `BACKUP-DR-DESIGN.md` (que sigue siendo el diseño congelado de referencia). Cambios a este contrato requieren aprobación explícita del owner.

## 1. Ubicación

`10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/BACKUP-DR-CONTRACT.md` (regla viva del proyecto). `30-resources/aranea/03-storage/backup-dr/` queda solo para **referencia técnica**: diseño congelado, runbook, checklist, policy, formularios. El contrato NO vive ahí.

## 2. Scope Tier 0 — congelado (NO modificar)

**Total: 23 workloads Tier 0.**

- **Tier 0a — Infraestructura base**: opnsense(130), pi-hole(149), traefik(115).
- **Tier 0b — Storage**: truenas(145).
- **Tier 0c — Quorum crítico** (etcd NUNCA <3, ideal 5): etcd-athena(101), etcd-hades(147), etcd-kronos(154), etcd-hera(155), etcd-zeus(156); etcd-keeper(148) [UI, NO quorum]; kafka-hera(136), kafka-kronos(138), kafka-zeus(139).
- **Tier 0d — Echo trading**: mt4-real(124), mt4-ftmo(133), mt4-ttp(134), mt4-demo(144), echo(140), postgres(152), mongo(153), argus(160), docker-flink(126), docker-hasura(129).

## 3. Glosario operativo (unidad de backup ≠ VM)

| Concepto | Definición | Ejemplos |
|---|---|---|
| **Servicio** | Función lógica | "DNS recursivo", "reverse proxy" |
| **Workload** | Instancia ejecutable concreta. Puede ser VM, LXC, contenedor o proceso | opnsense es servicio; vm 130 es workload |
| **VM** | Workload tipo QEMU/KVM | opnsense, truenas, mt4-*, echo, postgres, mongo, argus |
| **LXC** | Workload tipo contenedor Proxmox | pi-hole, traefik, etcd-*, etcd-keeper, docker-flink, docker-hasura |
| **Unidad de backup** | Granularidad a respaldar. **Puede ≠ workload completo** | vzdump full VM; restic dump de postgres; etcd snapshot del cluster (no cada nodo); configs de traefik (no el LXC) |

**Regla**: en Backup/DR hablamos de **workloads**, no "VMs". **etcd cluster = 1 unidad de backup** aunque sean 5 LXCs.

## 4. Reglas de no interpretación (binding)

1. **NO agregar** workloads Tier 0 sin aprobación explícita.
2. **NO sacar** workloads Tier 0 sin aprobación explícita.
3. **NO reclasificar** (mover entre tiers) sin aprobación explícita.
4. **Si falta un dato, marcar `UNKNOWN`, explicar el impacto y detenerse.** No preguntar en loop, no asumir defaults.
5. **NO interpretar silencio** como aprobación. Esperar OK explícito.
6. **NO ejecutar nada en Aranea** sin gate técnico aprobado en chat.
7. **NO consolidar memoria** ni cambiar status sin orden explícita.
8. **Propuestas primero en chat.** No crear archivos para propuestas sin aprobación explícita. Si el owner pide "muéstrame X", se muestra en chat; el archivo viene solo después del OK.
9. **Una respuesta = una salida.** Contrato, diff, gate, checklist o comando. Nunca mezclar contrato + ejecución + status + memoria + cleanup en el mismo turno.
10. **No usar `write_file` sobre archivos existentes** salvo aprobación explícita + diff previo mostrado en chat.

## 5. Decisiones abiertas (owner debe resolver)

| # | Decisión | Ticket | Bloquea |
|---|---|---|---|
| 1 | Tier 0 workloads (si hay cambios al §2) | 018 | ap-02 schedule, retention, drills |
| 2 | Ventana de mantenimiento | 019 | ap-02 crear VM PBS vmid 180 en kronos |
| 3 | Secret Zero operativo | 020 | ap-04/05 cloud, ap-02 passphrase datastore |
| 4 | OAuth scope pcloud + GDrive | 021 | ap-04/05 setup remotes rclone |

## 6. Prohibido tocar sin aprobación explícita por acción/gate

- ❌ Infraestructura Aranea (cualquier ssh, agent-read destructivo, pvesm, qm, zfs, etc.)
- ❌ `BACKUP-DR-DESIGN.md` (F-01..F-14 siguen vigentes; cambiar requiere `REQUEST-CHANGES.md`)
- ❌ Recursos sagrados: `local-sqx-{zeus,hera,kronos}` (F-04), `pool0_backup` (F-09), Ceph OSDs, `pool0 mirror vdevs`
- ❌ Status de proyectos/tickets/agentes
- ❌ Memoria persistente del agente
- ❌ Tickets 018-021 (siguen `open` hasta que el owner los cierre formalmente)

## 7. Vigencia

Este contrato **rige** desde la aprobación del owner (2026-07-02). Mientras el contrato esté activo:
- El diseño técnico de referencia es `BACKUP-DR-DESIGN.md` (design-frozen).
- El scope canónico Tier 0 es §2, pero no habilita implementación hasta aprobación explícita del owner para cada gate técnico.
- Cambios al contrato requieren nueva aprobación del owner.
