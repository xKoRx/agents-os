---
title: "Propuesta — Contrato Canónico Backup/DR Aranea (BORRADOR, NO APROBADO)"
type: doc
schema_version: 1
status: active
icon: 📜
slug: backup-dr-contrato-canonico-propuesta
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: 2026-07-02
updated: 2026-08-10
draft_note: "Propuesta NO aprobada. Espera revisión del owner. NO modifica el diseño congelado ni los tickets."
aliases:
  - Contrato canónico Backup/DR
  - Backup DR contract draft
tags:
  - kind/doc
  - area/aranea
  - domain/backup-dr
  - doc/contract-proposal
  - lifecycle/draft
  - authority/non-canonical
related:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[BACKUP-DR-DESIGN]]"
  - "[[FORMULARIO-MINIMO]]"
---

# 📜 Propuesta — Contrato Canónico Backup/DR Aranea

## Propósito

Conservar la propuesta de contrato Backup/DR no aprobada como evidencia de diseño, sin promoverla a autoridad ni reemplazar el contrato vigente.

## Contenido

> [!warning] BORRADOR — NO aprobado. Espera revisión del owner.
> Este documento es una **propuesta** que define el contrato operativo del proyecto Backup/DR. No reemplaza `BACKUP-DR-DESIGN.md` (que sigue siendo el diseño congelado). No cierra tickets. No se ejecuta nada hasta que el owner lo apruebe explícitamente.

## 1. Scope Tier 0 — congelado (NO modificar)

**Total: 23 workloads Tier 0** (no "VMs" — ver §2).

**Tier 0a — Infraestructura base** (sin estos NADA funciona): opnsense(130), pi-hole(149), traefik(115).

**Tier 0b — Storage**: truenas(145).

**Tier 0c — Quorum crítico** (etcd NUNCA <3, ideal 5): etcd-athena(101), etcd-hades(147), etcd-kronos(154), etcd-hera(155), etcd-zeus(156); etcd-keeper(148) [UI, NO quorum]; kafka-hera(136), kafka-kronos(138), kafka-zeus(139).

**Tier 0d — Echo trading**: mt4-real(124), mt4-ftmo(133), mt4-ttp(134), mt4-demo(144), echo(140), postgres(152), mongo(153), argus(160), docker-flink(126), docker-hasura(129).

## 2. Glosario operativo (unidad de backup ≠ VM)

| Concepto | Definición | Ejemplos Aranea |
|---|---|---|
| **Servicio** | Función lógica (lo que hace) | "DNS recursivo", "reverse proxy", "orquestador echo" |
| **Workload** | Instancia ejecutable concreta que sostiene un servicio. Puede ser VM, LXC, contenedor o proceso host | opnsense es un servicio; vm 130 es el workload |
| **VM** | Tipo de workload: máquina virtual completa (QEMU/KVM) | opnsense(130), truenas(145), mt4-*(124/133/134/144), echo(140), postgres(152), mongo(153), argus(160) |
| **LXC** | Tipo de workload: contenedor Linux sobre Proxmox | pi-hole(149), traefik(115), etcd-*(101/147/154/155/156), etcd-keeper(148), docker-flink(126), docker-hasura(129) |
| **Unidad de backup** | Granularidad a respaldar (puede ≠ workload completo) | vzdump full VM; restic dump de postgres (no la VM entera); etcd snapshot del cluster (no cada nodo); configs de traefik (no el LXC) |

**Regla**: en Backup/DR hablamos de **workloads** (no "VMs") porque el scope incluye VMs, LXCs y unidades de backup lógicas. **Etcd cluster** = 1 unidad de backup aunque sean 5 LXCs.

## 3. Reglas de no interpretación (binding)

1. **NO agregar** workloads Tier 0 sin aprobación explícita del owner.
2. **NO sacar** workloads Tier 0 sin aprobación explícita del owner.
3. **NO reclasificar** (mover entre tiers) sin aprobación explícita del owner.
4. **NO asumir defaults** sobre datos no provistos (IPs, puertos, secrets, paths). Pedir antes.
5. **NO interpretar silencio** como aprobación. Esperar OK explícito.
6. **NO ejecutar nada en Aranea** sin gate técnico aprobado.
7. **NO consolidar memoria** ni cambiar status de proyectos/tickets sin orden.

## 4. Decisiones abiertas (owner debe resolver)

| # | Decisión | Ticket | Bloquea |
|---|---|---|---|
| 1 | Tier 0 workloads (este contrato es la propuesta) | 018 | ap-02 schedule vzdump, retention, drills |
| 2 | Ventana de mantenimiento (día+hora+duración+presencia+contacto) | 019 | ap-02 crear VM PBS vmid 180 en kronos |
| 3 | Secret Zero operativo (caja fuerte, USB LUKS, Bitwarden, recovery code) | 020 | ap-04/05 cloud tier, ap-02 passphrase datastore |
| 4 | OAuth scope pcloud+GDrive (A/B/C por servicio) | 021 | ap-04/05 setup remotes rclone |

## 5. Prohibido tocar hasta aprobación del owner

- ❌ Infraestructura Aranea (CUALQUIER ssh, agent-read destructivo, pvesm, qm, zfs, etc.)
- ❌ Diseño congelado `BACKUP-DR-DESIGN.md` (F-01..F-14 siguen vigentes; cambiar requiere `REQUEST-CHANGES.md`)
- ❌ Recursos sagrados: `local-sqx-{zeus,hera,kronos}` (F-04), `pool0_backup` (F-09), Ceph OSDs, `pool0 mirror vdevs`
- ❌ Status de proyectos/tickets (BACKUP-DR, SERVICIOS-DOCS, agentes)
- ❌ Memoria persistente del agente sin orden explícita
- ❌ Tickets 018-021 (siguen `open` hasta que el owner los cierre formalmente)

## 6. Aprobación requerida

Este contrato entra en vigencia solo cuando el owner responda **"contrato aprobado"** (o equivalente) por Telegram o chat. Hasta entonces, el diseño vigente es `BACKUP-DR-DESIGN.md` (design-frozen) y el contrato de scope implícito es el listado en §1 de este documento (no ejecutable, solo referencia).
