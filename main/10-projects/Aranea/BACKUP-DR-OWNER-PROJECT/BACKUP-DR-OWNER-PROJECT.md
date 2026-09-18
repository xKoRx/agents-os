---
title: "BACKUP-DR-OWNER-PROJECT — Proyecto owner Backup/DR"
type: project
schema_version: 1
owner: me
root: true
status: active
status_detail: "ACTIVE. R0 reconciliación completa (2026-09-16). R1 (2026-09-17, PASS WITH DEBT): 3 unidades BACKUP+RESTORE_VERIFIED, 3 SKIPPED_GATED, F-09=EXISTS. D0 saneamiento documental (2026-09-17): 9 agent-projects reconciliados, RC-20260917-001 aprobado+aplicado. R1.5 (2026-09-17, PASS WITH OWNER GATES): residuos D0 corregidos; etcd-snapshot VERIFIED+AUTOMATED (corrección: :2379 alcanzable desde hermes); pve node-local VERIFIED semanal + pmxcfs GATED; traefik +drop-in clouDNS; timers frozen 04:00/05:00/SAT 08:30 activos y probados; pi-hole GATED doble (servicio L2-dead + token). Re-verificación continuidad R1 (2026-09-18): runs automáticos del día OK, drills 4/4 PASS nuevos (traefik/etcd/second-brain/hermes-state), F-09 EXISTS live, gates sin cambios (pmxcfs bundle R1.6 en PAUSA, pi-hole L2-dead, traefik ssl), staging 283M/20%, PASS WITH DEBT mantenido. Detalles: change_logs 2026-09-17-backup-dr-r15-config-completion y 2026-09-18-backup-dr-r1-continuity-verification."
priority: P1
icon: 📋
slug: backup-dr-owner-project
area: "[[Aranea]]"
project: "[[AGENTS OS]]"
created: 2026-07-01
updated: 2026-09-18
start: 2026-07-02
due:
progress: 25
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

- **ACTIVE desde 2026-09-16** por mandato owner (reactivación del carril Backup/DR). Reconciliación R0 completa: `2026-09-16-R0-reconciliacion.md` (mismo directorio).
- R0 evidenció: 59 guests (23/23 Tier0 KEEP + ADDs propuestos), **ningún mecanismo de backup activo** (0 snapshots ZFS, sin vzdump jobs, sin restic/rclone, sin dumps DB), PBS VM 180 running en kronos pero sin registro en pve_storage ni acceso demostrado (gate owner), pool2 single-disk con scrub overdue.
- Los nueve agent-projects hijos operan según el roadmap por fases: ap-00 **DONE** (R0+D0), ap-01 **IN-PROGRESS** (R1+R1.5: 4/6 unidades VERIFIED+AUTOMATED, 2 gated), los demás `paused` hasta su fase; ap-02 cambia de "crear VM PBS" a "adoptar/recuperar VM 180 existente"; ap-06 se reescribe contra ARGUS (stack docker-observability mencionado quedó legacy).

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
| 00 | [[agent-project-00-policy-and-doc-cleanup]] | Limpieza documental del dominio — **DONE** (julio vía R0 + complemento D0 2026-09-17) | 0.5 día | nada |
| 01 | [[agent-project-01-critical-config-backup]] | Config crítica — **IN-PROGRESS**: R1.5 dejó 4/6 unidades VERIFIED+AUTOMATED (timers frozen activos), pve node-local VERIFIED con pmxcfs GATED, pi-hole GATED (servicio L2-dead + token) | 0.5 día | gates root (bundle R1.5) + pi-hole |
| 02 | [[agent-project-02-pbs-on-backup-node]] | **Adoptar PBS VM 180 existente** (R0: running, sin integrar) + datastore F-06 + registro 5 nodos | 1 día | gate owner 180 + 018 + 019 |
| 03 | [[agent-project-03-app-consistent-data-backups]] | PG, Mongo, CouchDB, minio, sanoid pool0 — fase **R3** (drills incluidos) | 1.5 días | 02 |
| 04 | [[agent-project-04-cloud-critical-tier]] | Cloud crítico + Restic — fase **R4**; proveedor por revalidar owner (F-08); sin remotes en runtime | 0.5 día | 01, 03, 020, 021 |
| 05 | [[agent-project-05-cloud-bulk-archive-tier]] | Bulk/archive + chunking — fase **R5**; proveedor por revalidar owner (F-08); sin remotes en runtime | 0.5 día | 03, 020, 021 |
| 06 | [[agent-project-06-observability-and-alerting]] | Señales de backup en **ARGUS (vm 160)** — fase **R6** vía management path (docker-observability: supuestos julio HISTORICAL) | 1 día | 02, 04 |
| 07 | [[agent-project-07-restore-drills]] | Restore por fase + certificación recurrente **R7** (drills por fase desde R1) | continuo | prácticas por fase; recurrente: R2-R6 |
| 08 | [[agent-project-08-session-closeout-and-learning-loop]] | Cierre por workload (change log canónico); session close L0/L1 sólo por orden owner | 0.5 día | por workload |

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

- [ ] **OWNER-TASK-CRITICAL-VMS** (ticket 018): confirmar lista tier 0. Base vigente = contrato §2 (23 workloads / 16 unidades) + ADDs propuestos R0 §6; la lista de 15 del formulario mínimo es la propuesta en espera de decisión. (La lista julio de este bloque —mt5-real, sin etcd/kafka/argus— quedó obsoleta y fue retirada.)
  - reason: define retention y frecuencia de vzdump tier 0.
  - required_by: agent-project-02 PBS schedule.
  - blocks: implementación completa.
  - required_access: lectura VMs vía PVE.
  - expected_output: lista explícita con VMID y nombre.
  - acceptance_criteria: lista firmada por owner.
  - tags: [owner, blocking, tier0]

- [ ] **OWNER-TASK-MAINT-WINDOW**: declarar ventana de mantenimiento preferida (sábado madrugada, domingo noche, otro).
  - reason: agent-project-02 adopta/integra la PBS VM 180 existente (registro storage replica /etc/pve/storage.cfg a los 5 nodos). La creación de VM quedó HISTORICAL (R0: la VM ya existe).
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

- AGENT-TASK-PBS-ADOPT: adoptar/integrar VM 180 existente (la creación quedó HISTORICAL — la VM ya existe, R0). Discovery gate 0-0.2 EJECUTADO 2026-09-18 (REUTILIZAR; accesos ariadna@ demostrados). Mutaciones de integración pendientes: Owner Action Bundle `~/aranea/work/r2-pbs-20260918/` (datastore/credenciales) + ventana 019.
- AGENT-TASK-PBS-DATASTORE-INIT: bloqueada por OWNER-TASK-SECRET-ZERO (passphrase).
- AGENT-TASK-RCLONE-REMOTE-SETUP: bloqueada por OWNER-TASK-OAUTH-SCOPE.
- AGENT-TASK-VZDUMP-TIER0-CFG: bloqueada por OWNER-TASK-CRITICAL-VMS.

## 📅 Calendario recomendado

> [!info] SUPERSEDED como cronograma (2026-09-17)
> El calendario S1–S3 de julio quedó reemplazado por el roadmap por fases **R0–R8** con dependencias reales: ver `[[2026-09-16-R0-reconciliacion]]` §9 (autoridad de planificación). Estado actual: R0 DONE, R1 DONE (con deuda), D0 DONE, R1.5 DONE (gates owner vigentes), R2 gate owner.

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

- [ ] Fases R0–R8 ejecutadas según roadmap R0 §9 (R0 ✅, R1 ✅ con deuda owner, D0 ✅; R2+ gates owner).
- [ ] PBS VM 180 adoptada e integrada, datastore operativo con al menos 7d de backups tier 0 (fase R2).
- [ ] Repo Restic en el proveedor crítico revalidado con owner (F-08) con al menos 1 semana de configs + dumps (fase R4).
- [ ] Tier bulk en el proveedor revalidado con owner (F-08) con al menos 1 chunk ZFS pool0 sync'd (fase R5).
- [ ] sanoid configurado en truenas con templates production/critical/backup.
- [ ] Observabilidad: señales de backup en ARGUS con las alertas mínimas de la policy activas (fase R6).
- [ ] Secret Zero documentado y validado (caja fuerte + USB cifrado).
- [ ] Restore drill tier 0 PASS reciente (< 35d).
- [ ] Restore drill DB PASS reciente (< 35d).
- [ ] Runbooks en `BACKUP-DR-RUNBOOK.md` validados por owner.
- [ ] Checklists en `BACKUP-DR-CHECKLIST.md` ejecutados al menos 1 ciclo completo.
- [ ] Request changes de evolución registrados en `REQUEST-CHANGES.md`.
- [ ] Sesión de cierre con lecciones en `agent-project-08` completada.
- [ ] Tickets 018-021 cerrados por el owner (los tickets 022-026 citados antes no existen; error de julio corregido en D0).

---

**Status**: active (reactivado por owner 2026-09-16). El diseño de referencia sigue congelado (F-01..F-14); cambios semánticos vía REQUEST-CHANGES. Ejecución por fases R0–R8 según `2026-09-16-R0-reconciliacion.md`.
**Sesión cerrada por instrucción del owner**: 2026-07-01 (histórico). Reactivación: 2026-09-16.

## 📆 Bitácora

- **2026-08-10** — Parent migrado a `project` v1 para soportar contractualmente los nueve hijos `owner: agent`; se preservó la prohibición de ejecutar y se crearon sus tareas puente humanas en To Do.
- **2026-09-16** — Owner autoriza reactivación (mandato Backup/DR autónomo). R0 reality reconciliation completado sin cambios en infraestructura: captura 6/6 nodos (TS 20260916_233513), mecanismos de backup descubiertos, 23/23 Tier0 KEEP, F-01..F-14 reconciliadas, matriz GAP y roadmap R1–R8 en [[2026-09-16-R0-reconciliacion]]. Gates owner consolidados en R0 §10 (PBS 180 + tickets 018-021 vigentes).
- **2026-09-17 (D0)** — Saneamiento documental completo (mandato owner): 9 agent-projects reconciliados, runbook/checklist con estados por sección, 9 docs legacy con advertencia individual, índices/área/README alineados, wikilinks corregidos, RC-20260917-001 propuesto (banner DESIGN_FROZEN en el design). Sin cambios a contract/design/policy/tickets. Evidencia: `80-agents/journal/logs/2026-09-17-backup-dr-d0-documentation-consistency.md`.
- **2026-09-17** — **R1 ejecutado (PASS WITH DEBT)**. Staging real en Hermes VM 118 (`~/aranea/backup-staging/`, 700) + wrapper `~/aranea/bin/r1-backup.sh` (2 ejecuciones, idempotencia probada, sin pruning/timer — frecuencia y retención pendientes decisión owner). Certificadas BACKUP+RESTORE_VERIFIED: traefik-config (LXC 115, configs estática+dinámica, drill sha256 8/8 vs fuente viva), second-brain (vault 3.438 archivos, drill idéntico), hermes-state (`~/.hermes` operacional + `~/aranea` + unit túnel, 600). SKIPPED_GATED con deuda owner: `/etc/pve` (necesita subcommand `config` en `agent-read`), etcd snapshot (necesita etcd-client + endpoint/certs), pi-hole (necesita api_token FTL v6 o root). F-09: `pool2/pool0_backup` **EXISTS** (live + captura R0), intacto. Traefik parcial: `secrets/ ssl/ acme.json` root-only quedan fuera (gap registrado). Cero toques a producción; tickets 018-021 intactos; R2 no iniciado. Evidencia: change_log `80-agents/journal/logs/2026-09-17-backup-dr-r1-bootstrap-config.md` + `manifest.json` por run.
- **2026-09-17 (R1.5)** — **Mandato owner one-shot ejecutado (PASS WITH OWNER GATES)**. D0 residuos corregidos (RC contradicción + reclasificación L0/L1/L3). etcd-snapshot: :2379 resultó alcanzable desde hermes (corrección de R1), snapshot cluster 3.6.4 rev 55033 con pre-checks quorum/hashkv, drill scratch PASS, timer DAILY 05:00. pve-config: node-local 5/5 nodos VERIFIED con drill, timer SAT 08:30; pmxcfs GATED (extensión agent-read config requiere root; script ya captura cuando exista). traefik-config: +drop-in systemd clouDNS (permite re-emitir acme.json); `acme-stepca.json` identificado recovery-critical (CA lxc-200 stopped). pi-hole: GATED doble — hallazgo operativo .149 L2-dead (ARP FAILED desde athena) + api_token. Timers systemd frozen activos y probados (04:00/05:00/SAT 08:30; Persistent; journal). Fix manifest sha null. Evidencia: change_log `80-agents/journal/logs/2026-09-17-backup-dr-r15-config-completion.md`, manifests `manifest-etcd.jsonl`/`manifest-pve.jsonl` + restore-drill.json por run.
- **2026-09-18** — **Re-verificación de continuidad R1 (mandato owner día 2)**: R1/R1.5 no repetidos. Runs automáticos del día OK (04:00: 3 unidades; 05:00: etcd rev 56625, 985 keys, 5/5 healthy); 3 timers active+enabled. Restore drills nuevos 4/4 PASS (traefik 11/11 sha vs fuente viva; etcd restore a data-dir TEMP aislado sin arrancar; second-brain 3587/3587; hermes-state sha -c + YAML + unit). F-09 EXISTS (live truenas 2026-09-18). Gates sin cambios: pmxcfs (bundle R1.6 en PAUSA owner), pi-hole (L2-dead), traefik ssl root-only. Staging 283M/20%. Veredicto: PASS WITH DEBT mantenido. Evidencia: `80-agents/journal/logs/2026-09-18-backup-dr-r1-continuity-verification.md` + `restore-drill.json` en runs `20260918-*`.
- **2026-09-18** — Continuidad documental (mandato owner): razón de OWNER-TASK-MAINT-WINDOW alineada a adopción (no creación); estado del calendario superseded incluye R1.5. Sin cambios de alcance, gates ni decisiones. Evidencia: change_log `80-agents/journal/logs/2026-09-18-backup-dr-continuidad-documental.md` + `RC-20260918-001-continuidad-documental.md`.
- **2026-09-18 (H1 enablement, carril Infrastructure)** — Nota de habilitación para R2 (sin cambios en este proyecto): las capacidades administrativas que R2 consume ya están certificadas read-only por [[HERMES — Infrastructure Operations]] — SSH admin `ariadna`+sudo en 5 PVE + PBS (.123) + TrueNAS (matriz de autoridad en esa nota; llaves por referencia, secretos nunca expuestos). PBS confirmado VIRGEN (4.2.6-1, 0 datastores, root@pam) — consistente con el discovery R2 de este proyecto; el usuario/token de PBS y el datastore siguen siendo trabajo gated de R2 (bundle vigente). El carril Infrastructure NO ejecuta backups ni toca tickets/jobs; handoff y gaps: `80-agents/journal/logs/2026-09-18-h1-enablement.md`.
- **2026-09-18 (R2)** — **Discovery efectivo PBS ejecutado (mandato owner R2; cero mutaciones).** Acceso administrativo PASS: keys nuevas `ariadna_pbs`/`ariadna_pve` (creadas 18sep por owner) demostradas en PBS 192.168.31.123 y los 5 nodos, sudo NOPASSWD. PBS 4.2.6-1 (Debian 13) viva y administrable pero VIRGEN: 0 datastores, solo root@pam, 0 ACL, 0 jobs, tasks archive solo logrotate/aptupdate; 38G libres internos; VM 180 sobre VG `local-kronos` (F-06 nivel disco OK; VG con 567.5G libres); `storage.cfg` sin pbs y `jobs.cfg` vacío (sin vzdump fantasma); huella tier 0 (contrato §2) medida live: alloc 660G, used-in-guest ~165-185G/ciclo ⇒ retención completa ~600G ⇒ LV dedicado propuesto en la misma VG (300/500/650G). Decisión gate 0.2: REUTILIZAR. Gates: tickets 018/019 siguen `todo`; sin autorización explícita para LV+mkfs ni `pvesm add` ⇒ OWNER ACTION BUNDLE único entregado (`~/aranea/work/r2-pbs-20260918/owner-action-bundle.md`, bloques A/B/C con rollback y ejecución post-OK ~30-45min). Piloto/restore NOT EXECUTED. R1.6 sigue PAUSADO. Evidencia: `80-agents/journal/logs/2026-09-18-r2-pbs-discovery-effective.md`.
