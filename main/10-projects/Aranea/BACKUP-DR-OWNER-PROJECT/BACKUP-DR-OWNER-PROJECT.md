---
title: "BACKUP-DR-OWNER-PROJECT — Proyecto owner Backup/DR"
type: project
schema_version: 1
owner: me
root: true
status: paused
status_detail: "Proyecto owner. Mapa de subproyectos agente. Owner tasks listadas. NO implementado. Migrado 2026-07-02 desde 30-resources/aranea/03-storage/backup-dr/ a 10-projects/Aranea/ por convención PARA (proyecto con plazo y tareas, no evergreen)."
priority: P1
icon: 📋
slug: backup-dr-owner-project
area: "[[Aranea]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-08-10
start: 2026-07-02
due:
progress: 0
repo:
jira:
prs:
aliases:
  - Backup DR owner project
  - Backup DR integral
  - Proyecto Backup DR
tags:
  - kind/project
  - area/aranea
  - project/agents-os
  - domain/backup
related:
  - "[[BACKUP-DR-DESIGN]]"
  - "[[DIFF-CONCEPTUAL]]"
  - "[[REQUEST-CHANGES]]"
design_ref: "[[BACKUP-DR-DESIGN]]"   # doc de diseño, NO parent
children:
  - "[[agent-project-00-policy-and-doc-cleanup]]"
  - "[[agent-project-01-critical-config-backup]]"
  - "[[agent-project-02-pbs-on-backup-node]]"
  - "[[agent-project-03-app-consistent-data-backups]]"
  - "[[agent-project-04-cloud-critical-tier]]"
  - "[[agent-project-05-cloud-bulk-archive-tier]]"
  - "[[agent-project-06-observability-and-alerting]]"
  - "[[agent-project-07-restore-drills]]"
  - "[[agent-project-08-session-closeout-and-learning-loop]]"
cssclasses:
  - wide
---

# 📋 Proyecto Owner: Backup/DR integral

> Proyecto owner legible. NO ejecutable directamente — para eso están los `agent-project-*`.

## 🎯 Objetivo

Pasar de "tenemos backups parciales y silenciosos" a "tenemos un sistema de backup/DR con 3-2-1 verificado, restore drills mensuales, observabilidad activa y Secret Zero protegido".

## 📊 Estado actual

- Pausado con diseño congelado y sin autorización de ejecución; los nueve proyectos de agente hijos están contractualmente migrados pero permanecen pausados.

## 📦 Alcance

- Configuración crítica (Capa A).
- Datos app-consistent (Capa B).
- VMs/LXCs tier 0/1/2/3 (Capa C).
- Snapshots ZFS locales (Capa D).
- Datasets ZFS off-site (Capa E).
- Cloud crítico + bulk (Capa F).
- Restore drills (Capa G).
- Observabilidad + alertas mínimas.
- Secret Zero + escrow.
- Runbooks + checklists + skills.

## 🚫 No-alcance

- Comprar hardware (prohibido F-01).
- Migrar TrueNAS a bare-metal (prohibido F-02).
- Agregar/sacar servidores (prohibido F-03).
- Tocar `local-sqx-*` (prohibido F-04).
- Tocar `sdf` para mirror pool2 (descartado F-05).
- Crear `pool1` en truenas (descartado F-12).
- Backup externo Ceph RBD (descartado F-10).
- Migrar `pool0_backup` dataset (prohibido F-09).

## 🔒 Restricciones

Ver [[BACKUP-DR-DESIGN]] §3 Decisiones congeladas.

## ❄️ Decisiones congeladas relevantes

F-01 capex, F-02 no migrar TrueNAS, F-03 no cambio servidores, F-04 SQX sagrados, F-05 sdf no spare, F-06 PBS=local-kronos, F-07 PBS RAM 8 GB, F-08 cloud segregado, F-09 no migrar pool0_backup, F-10 no Ceph backup externo, F-11 Opción A, F-12 Fase 2 descartada, F-13 hades SPOF aceptado, F-14 pool2 single disk aceptado.

## 🗺️ Mapa de subproyectos agente

| # | Subproyecto | Foco | Esfuerzo | Bloqueado por |
|---|---|---|---|---|
| 00 | [[agent-project-00-policy-and-doc-cleanup]] | Limpiar DESIGN-PROPOSAL histórico, cerrar gaps de docs | 0.5 día | nada |
| 01 | [[agent-project-01-critical-config-backup]] | /etc/pve, Traefik, OPNsense, step-ca, etcd, manifests | 1 día | 00 |
| 02 | [[agent-project-02-pbs-on-backup-node]] | Crear VM PBS en kronos, datastore local-kronos, 8 GB RAM | 1 día | 00 |
| 03 | [[agent-project-03-app-consistent-data-backups]] | PG, Mongo, CouchDB, minio, sanoid pool0 | 1.5 días | 02 |
| 04 | [[agent-project-04-cloud-critical-tier]] | pcloud + Restic cifrado, push semanal configs/dumps | 0.5 día | 01, 03 |
| 05 | [[agent-project-05-cloud-bulk-archive-tier]] | GDrive + rclone crypt + chunking, push mensual ZFS | 0.5 día | 03 |
| 06 | [[agent-project-06-observability-and-alerting]] | Stack mínimo de alertas, integración con docker-observability | 1 día | 02, 04 |
| 07 | [[agent-project-07-restore-drills]] | Calendario drills, criterios PASS/FAIL, evidencia | continuo | 04, 05 |
| 08 | [[agent-project-08-session-closeout-and-learning-loop]] | Cierre sesión, lecciones, memoria, skills | 0.5 día | 00 |

**Total esfuerzo**: ~6.5 días-hombre (sin contar drills continuos).
**Crítico path**: 00 → 01 → 02 → 03 → 04 → 06 + 05 paralelo → 07 continuo.

## ✅ Tareas

- [ ] [[agent-project-00-policy-and-doc-cleanup]] ejecutar + seguimiento #owner/me #type/supervision #area/aranea
- [ ] [[agent-project-01-critical-config-backup]] ejecutar + seguimiento #owner/me #type/supervision #area/aranea
- [ ] [[agent-project-02-pbs-on-backup-node]] ejecutar + seguimiento #owner/me #type/supervision #area/aranea
- [ ] [[agent-project-03-app-consistent-data-backups]] ejecutar + seguimiento #owner/me #type/supervision #area/aranea
- [ ] [[agent-project-04-cloud-critical-tier]] ejecutar + seguimiento #owner/me #type/supervision #area/aranea
- [ ] [[agent-project-05-cloud-bulk-archive-tier]] ejecutar + seguimiento #owner/me #type/supervision #area/aranea
- [ ] [[agent-project-06-observability-and-alerting]] ejecutar + seguimiento #owner/me #type/supervision #area/aranea
- [ ] [[agent-project-07-restore-drills]] ejecutar + seguimiento #owner/me #type/supervision #area/aranea
- [ ] [[agent-project-08-session-closeout-and-learning-loop]] ejecutar + seguimiento #owner/me #type/supervision #area/aranea

### Bloqueantes (deben resolverse antes de implementar)

- [ ] **OWNER-TASK-CRITICAL-VMS**: confirmar lista tier 0 (step-ca, OPNsense si VM, postgresql, mongodb, mt4-real, mt5-real, obsidian-sync).
  - reason: define retention y frecuencia de vzdump tier 0.
  - required_by: agent-project-02 PBS schedule.
  - blocks: implementación completa.
  - required_access: lectura VMs vía PVE.
  - expected_output: lista explícita con VMID y nombre.
  - acceptance_criteria: lista firmada por owner.
  - tags: [owner, blocking, tier0]

- [ ] **OWNER-TASK-MAINT-WINDOW**: declarar ventana de mantenimiento preferida (sábado madrugada, domingo noche, otro).
  - reason: agent-project-02 crea VM (interrumpe nodo kronos brevemente).
  - required_by: agent-project-02.
  - blocks: implementación agent-project-02.
  - required_access: schedule owner.
  - expected_output: ventana confirmada (día + hora + duración máx).
  - acceptance_criteria: ventana confirmada por escrito.
  - tags: [owner, blocking, schedule]

- [ ] **OWNER-TASK-SECRET-ZERO**: confirmar ubicación física de caja fuerte + USB cifrado para Secret Zero.
  - reason: PASS-cifrado requiere escrow offline (ver BACKUP-DR-DESIGN §7).
  - required_by: agent-project-04/05.
  - blocks: implementación tier crítico cloud.
  - required_access: bitwarden recovery + caja fuerte + USB cifrado.
  - expected_output: ubicación confirmada + procedimiento de acceso documentado.
  - acceptance_criteria: ubicación validada, USB cifrado creado y testeado.
  - tags: [owner, blocking, secret-zero]

- [ ] **OWNER-TASK-OAUTH-SCOPE**: confirmar si agente puede ejecutar OAuth flow pcloud/GDrive o si owner debe hacerlo.
  - reason: tokens OAuth son credenciales sensibles.
  - required_by: agent-project-04/05.
  - blocks: setup remotes rclone.
  - required_access: cuenta pcloud + GDrive owner.
  - expected_output: aprobación o rechazo explícito.
  - acceptance_criteria: decisión documentada.
  - tags: [owner, blocking, oauth]

### No bloqueantes (mejoras futuras)

- [ ] **OWNER-TASK-OPT-ZFS-RECV**: decidir si reactiva Fase 2 con `pool-kronos` como destino zfs recv on-cluster.
  - reason: mejora opcional de redundancia on-cluster.
  - required_by: solo si owner aprueba.
  - blocks: nada.
  - required_access: nada.
  - expected_output: aprobación o rechazo.
  - acceptance_criteria: decisión registrada.
  - tags: [owner, optional, zfs-recv]

## 🛑 Tareas bloqueadas por permisos / decisiones

- AGENT-TASK-PBS-VM-CREATE: bloqueada por OWNER-TASK-MAINT-WINDOW.
- AGENT-TASK-PBS-DATASTORE-INIT: bloqueada por OWNER-TASK-SECRET-ZERO (passphrase).
- AGENT-TASK-RCLONE-REMOTE-SETUP: bloqueada por OWNER-TASK-OAUTH-SCOPE.
- AGENT-TASK-VZDUMP-TIER0-CFG: bloqueada por OWNER-TASK-CRITICAL-VMS.

## 📅 Calendario recomendado

| Semana | Subproyectos |
|---|---|
| S1 Lun-Mié | agent-project-00 + agent-project-01 |
| S1 Jue-Vie | agent-project-02 (ventana mantenimiento) |
| S2 Lun-Mié | agent-project-03 |
| S2 Jue | agent-project-04 (requiere Secret Zero + OAuth) |
| S2 Vie | agent-project-05 |
| S3 Lun | agent-project-06 |
| S3 en adelante | agent-project-07 continuo |
| Cierre sesión | agent-project-08 |

**Nota**: calendario asume 0.5-1 día-hombre/día. Si owner tiene menos tiempo, extender calendario.

## ⚠️ Riesgos (top 5)

Ver [[BACKUP-DR-DESIGN]] §10.

Top específicos del proyecto:
1. **R-15 Restore drill falla repetidamente** → backup no confiable.
2. **R-11 step-ca pierde claves** → CA rota, todos los certs internos mueren.
3. **R-13 Bitwarden inaccesible** → Secret Zero perdido.
4. **R-02 PBS en kronos comparte host con Ceph MON** → si kronos cae, backup off-host cae.
5. **R-04/R-05 cloud provider cierra cuenta** → tier off-site perdido.

## ✅ Definición de terminado (DoD)

El proyecto se considera **completo** cuando:

- [ ] 9 agent-proyectos ejecutados sin gates DANGEROUS abiertos.
- [ ] PBS operativo en kronos, datastore `local-kronos` con al menos 7d de backups tier 0.
- [ ] Restic repo en pcloud-crit con al menos 1 semana de configs + dumps.
- [ ] rclone bulk en GDrive con al menos 1 chunk ZFS pool0 sync'd.
- [ ] sanoid configurado en truenas con templates production/critical/backup.
- [ ] Observabilidad: 16 alertas mínimas activas, channels Telegram + email + dashboard.
- [ ] Secret Zero documentado y validado (caja fuerte + USB cifrado).
- [ ] Restore drill tier 0 PASS reciente (< 35d).
- [ ] Restore drill DB PASS reciente (< 35d).
- [ ] Runbooks en `BACKUP-DR-RUNBOOK.md` validados por owner.
- [ ] Checklists en `BACKUP-DR-CHECKLIST.md` ejecutados al menos 1 ciclo completo.
- [ ] Request changes de evolución registrados en `REQUEST-CHANGES.md`.
- [ ] Sesión de cierre con lecciones en `agent-project-08` completada.
- [ ] Tickets 018-026 (1 por subproyecto) cerrados.

---

**Status**: paused. Diseño congelado; NO ejecutar sin autorización del owner.
**Sesión cerrada por instrucción del owner**: 2026-07-01.

## 📆 Bitácora

- **2026-08-10** — Parent migrado a `project` v1 para soportar contractualmente los nueve hijos `owner: agent`; se preservó la prohibición de ejecutar y se crearon sus tareas puente humanas en To Do.
