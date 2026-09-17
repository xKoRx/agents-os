---
title: "R0 — Backup/DR Reality Reconciliation (2026-09-16)"
type: doc
schema_version: 1
status: active
icon: 🔍
slug: backup-dr-r0-reconciliacion
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: 2026-09-16
updated: 2026-09-16
aliases:
  - R0 Backup DR
  - Backup DR reconciliation 2026-09-16
tags:
  - kind/doc
  - area/aranea
  - domain/backup-dr
  - project/backup-dr
related:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[BACKUP-DR-CONTRACT]]"
  - "[[BACKUP-DR-DESIGN]]"
cssclasses:
  - wide
---

# 🔍 R0 — Backup/DR Reality Reconciliation

> Mandato owner 2026-09-16: reactivar el carril Backup/DR. Este documento es la reconciliación diseño-vs-runtime y la autoridad de estado del proyecto hasta que R1 la reemplace. Toda afirmación lleva etiqueta DOCUMENTED (doc histórico) / DISCOVERED (evidencia runtime 2026-09-16) / CONFIGURED (config existe, sin verificación de outcome) / VERIFIED (outcome probado) / RESTORE_VERIFIED (nunca aplicado aún en Aranea) / UNKNOWN.

## 1. Alcance ejecutado

- R0.1 Documentación cargada: owner project + contrato + policy + design + 9 agent-projects + índice evergreen + legacy `04-backups` completo. DISCOVERED: `SCHEDULE-DECISIONS-TEMP.md` y `src-migration-log.md` NO existen en el vault (búsqueda global) — gap documental del mandato.
- R0.2 Inventario físico: captura `agent-read all` fresca 6/6 nodos, TS `20260916_233513` (validación previa 6/6 PASS). Evidencia: `~/aranea/topology/discovery/<nodo>_20260916_233513.txt`.
- R0.3 Discovery de mecanismos de backup existentes (read-only).
- R0.4 Reconciliación 23 unidades Tier 0 contra runtime.
- R0.5 Reconciliación F-01..F-14.
- R0.6 Clasificación de `04-backups` y docs legacy.
- R0.7 Matriz GAP de protección.
- R0.8 Roadmap R1–R8 actualizado.
- R0.9 Proyecto actualizado a ACTIVE (sin falsificar progreso técnico).

## 2. Runtime físico verificado (R0.2)

| Hecho | Valor | Etiqueta |
|---|---|---|
| Nodos PVE | athena .10, hades .90, zeus .100, hera .110, kronos .120 + TrueNAS VM .91 sobre hades | DISCOVERED |
| Versión PVE | `pve-manager/8.4.20` kernel 6.8.12-29-pve | DISCOVERED |
| Guests totales | **59** (listado completo en evidencia athena) | DISCOVERED |
| PBS | VM **180 `pbs` running en kronos**, 64 GB disco, 8 GB RAM | DISCOVERED |
| TrueNAS pools | pool0 2.59T (mirror×4 + special mirror, scrub OK 2026-09-06), pool2 4.99T **single-disk** (scrub anterior 2025-07-12), boot-pool OK | DISCOVERED |
| NFS compartido | `pool0/proxmox_storage` 1.4T, 401G usados, montado en los 5 nodos como `nfs-storage` (content incluye backup/vztmpl) | DISCOVERED |
| Hermes runtime | VM `agent` vmid 118 en kronos, 192.168.31.122 | DISCOVERED |
| DNS | Resolución Hermes vía stub (getent OK a athena.lab.aranea). Ping ICMP Hermes→Pi-hole .149 SIN respuesta (la resolución sigue funcionando vía upstream del stub) | DISCOVERED |
| pool2/backup | Dataset con backups manuales legacy (DDBB, apps, aranea_storage 38.9G…); pool2 al 28% (2.2T libres) | DISCOVERED |

Census de guests (agrupado): Tier0 contrato §2 (ver §4), sqx trio 108/111/123 running, workloads nuevos running: mcps(113), obsidian-sync(116), emqx(103), homeassistant(105), jobs(106), agent(118), worker-kronos(135), minio(157), temporal(158), daedalus(142), docker-echo-dev(141), docker-observability(127), docker-kafka(128); stopped: laboratorio/dev (100,102,104,107,109,112,114,117,120,125,132,151,159,162,170), ca(200), pbs(180 running).

## 3. Mecanismos de backup existentes (R0.3)

| Mecanismo | Evidencia | Clasificación |
|---|---|---|
| vzdump/jobs de backup PVE | Sin jobs configurados; storage `nfs-storage` declara content backup pero no hay historial verificado | ABANDONED/UNKNOWN |
| PBS | VM 180 running PERO: sin ping/22/8007 desde Hermes, sin registro `pbs` en `pve_storage` de ningún nodo, sin credenciales conocidas | CONFIGURED-parcial/UNKNOWN — requiere acceso owner |
| Snapshots ZFS (sanoid/autosync) | **0 snapshots** en pool0/pool2 (`zfs list -t snap` vacío en captura) | NO EXISTE |
| TrueNAS replication/cloudsync/tareas | Sin evidencia en captura (wrapper no expone UI tasks; marcar UNKNOWN hasta acceso UI owner) | UNKNOWN |
| Dumps DB programados (pg/mongo/couchdb/minio) | No encontrados en ningún nodo (grep cron/timers negativo fuera de paquetes estándar) | NO EXISTEN |
| Restic/rclone/borg | Sin binarios, configs ni remotes detectados | NO EXISTEN |
| pool2/backup (backups manuales) | Datasets con contenido: DDBB InfluxDB 85.6M / Postgres 19.2M, apps (frigate, homeassistant, portainer), aranea_storage 38.9G, sin fechas verificables ni manifest | PARTIAL/HISTORICAL |
| Second Brain (Obsidian LiveSync CouchDB lxc 116) | Servicio running; replicación a destinos externos UNKNOWN | PARTIAL |
| Backup de Hermes (~/.hermes/backups/config) | Directorio con backup de config (2026-09-16); sin schedule ni retención | PARTIAL |
| etcd snapshots | Sin evidencia de snapshots del cluster etcd | NO EXISTE |
| step-ca backup | LXC 200 `ca` STOPPED (el servicio CA no está corriendo); sin backup conocido | UNKNOWN |

Regla §6 del mandato aplicada: snapshot ≠ backup, replication ≠ backup, NFS compartido ≠ backup. Hoy **ninguna unidad del contrato tiene backup verificado**.

## 4. Reconciliación de las 23 unidades Tier 0 (R0.4)

Contrato §2 enumera 23 workloads; por glosario §3 del propio contrato (etcd cluster = 1 unidad; análogo kafka) equivalen a **16 unidades de backup**. Clasificación KEEP/ADD contra runtime: las 23 existen y siguen identificables → **KEEP 23/23**. Cambios de ubicación: mt4-demo pasó 144 (coincide), postgres 152, mongo 153, argus 160, flink 126, hasura 129, todo coincide con runtime. ADD: ver §6.

| # | Workload contrato (VMID) | En runtime | Cambio |
|---|---|---|---|
| 1 | opnsense (130) | running athena | KEEP |
| 2 | pi-hole (149) | running athena | KEEP |
| 3 | traefik (115) | running athena | KEEP |
| 4 | truenas (145) | running hades | KEEP |
| 5-9 | etcd cluster 101/147/154/155/156 | 5/5 running | KEEP (1 unidad) |
| 10 | etcd-keeper (148) | running hades | KEEP |
| 11-13 | kafka 136/138/139 | 3/3 running | KEEP (1 unidad cluster) |
| 14 | mt4-real (124) | running hades | KEEP |
| 15 | mt4-ftmo (133) | running hades | KEEP |
| 16 | mt4-ttp (134) | running hades | KEEP |
| 17 | mt4-demo (144) | running hades | KEEP |
| 18 | echo (140) | running hades | KEEP |
| 19 | postgres (152) | running hades | KEEP |
| 20 | mongo (153) | running hades | KEEP |
| 21 | argus (160) | running hades | KEEP |
| 22 | docker-flink (126) | running hades | KEEP |
| 23 | docker-hasura (129) | running hades | KEEP |

## 5. Decisiones congeladas F-* (R0.5)

| F | Intención | Estado runtime 2026-09-16 | Válida | Acción |
|---|---|---|---|---|
| F-01 capex $0 | No comprar HW | Sin cambios de diseño detectados | YES | Mantener |
| F-02 no migrar TrueNAS | TrueNAS queda como VM sobre hades | truenas(145) running en hades | YES | Mantener |
| F-03 no cambiar # servidores | 5 nodos fijos | 5 nodos + hermes(118) | YES | Mantener |
| F-04 local-sqx-* sagrado | NO tocar | Los 3 VG existen en pve_storage | YES | Mantener |
| F-05 sdf no spare | sdf en pool0 mirror-0 | pool0 mirror healthy | YES | Mantener |
| F-06 PBS datastore local-kronos | PBS en kronos, datastore LVM local | PBS VM existe en kronos; integración 0; estado servicio UNKNOWN | PARTIAL | Redefinir tarea: no "crear VM" sino "recuperar/adoptar VM 180" |
| F-07 PBS 8 GB RAM | Tamaño fijo | VM con 8 GB | YES | Mantener |
| F-08 cloud segregado | pcloud=critical, gdrive=bulk | Sin remotes rclone; proveedores por validar (mandato: no asumir) | PARTIAL | Revalidar proveedor en R4/R5 con owner |
| F-09 no migrar pool0_backup | Dataset quieto | N/A hoy (no aparece en captura como dataset activo) | UNKNOWN | Verificar existencia en R1 |
| F-10 sin backup externo Ceph | Descartado | pool1 RBD presente; sin backup externo | YES | Mantener |
| F-11 Opción A (dedup PBS + ZFS comprimido) | Optimización | Pendiente de implementación | YES | Mantener |
| F-12 zfs recv on-cluster descartado | Fase 2 fuera | Sin cambios | YES | Mantener |
| F-13 hades SPOF aceptado | Riesgo asumido | hades concentra: truenas, pg, mongo, echo, argus, flink, hasura, obsidian-sync, PBS-VM-nada, minio, temporal, daedalus… | YES pero el riesgo CRECIÓ | Documentar blast radius; no re-litigar |
| F-14 pool2 single disk aceptado | Riesgo asumido | pool2 = 1 vdev sin mirror; scrub overdue (último 2025-07-12); pool2/backup contiene backups legacy | YES pero: pool2 es destino de backups Y single-disk | Scrub + decidir rol de pool2 en el diseño (no es failure-domain separado de pool0 si comparten chasis vía hades→TrueNAS VM) |

## 6. Unidades ADD detectadas (no en contrato §2)

| Unidad | Criticidad propuesta | Razón |
|---|---|---|
| Second Brain vault + LiveSync (lxc 116 CouchDB) | CRITICAL | Conocimiento operativo de Aranea y Agents-OS |
| Hermes platform state (~/.hermes config, .env refs, skills, memoria) | CRITICAL | Operador autónomo del platform |
| mcps (113) + Access Plane configs | IMPORTANT | Plano de acceso certificado |
| minio (157) + zvol pool0/iscsi/minio_data | IMPORTANT | Object storage |
| temporal (158) | IMPORTANT | Workflow engine de Echo DEV |
| daedalus (142) | IMPORTANT | Runtime DEV Echo (frozen topology owner) |
| docker-echo-dev (141), docker-kafka (128), docker-observability (127), emqx (103), homeassistant (105), jobs (106), worker-kronos (135) | IMPORTANT/TIER2 | Stateful o config |
| pool0 datasets: iscsi (pg_data 33G, mongo_data 32.5G, vm-zeus-win-disk 203G, win-development 203G, debian, minio_data 48.7G), aranea_storage 1.09T, trading_systems 485G, proxmox_storage 416G, apps/frigate | IMPORTANT | Datos reales sin snapshots |
| pool2/backup (backups legacy) | TIER2 | Preservar histórico |
| PBS VM 180 (su propio config/datastore) | IMPORTANT | El backup server debe sobrevivir |
| sqx 108/111/123 + laboratorio stopped | TIER3 |Según policy tier_3 |
| ca (200, STOPPED) | UNKNOWN→CRITICAL si reactivo | Claves CA = R-11 |

La incorporación de ADD al scope Tier 0 requiere aprobación owner (contrato regla 4.1). Quedan propuestas, no aprobadas.

## 7. Matriz GAP de protección (R0.7)

Estados: unidad sin ningún mecanismo = `NINGUNO`. RPO/RTO: no definidos medidos (policy los propone, nada ejecutado). Monitoring: `NO` en todas las filas (ARGUS existe pero sin señales de backup configuradas).

| Resource | Crit | Backup actual | Offsite | Restore probado | Monitoring | Estado |
|---|---|---|---|---|---|---|
| opnsense 130 | T0 | NINGUNO | no | no | no | DISCOVERED |
| pi-hole 149 | T0 | NINGUNO | no | no | no | DISCOVERED |
| traefik 115 | T0 | NINGUNO | no | no | no | DISCOVERED |
| truenas 145 (config VM) | T0 | UNKNOWN (config DB en boot-pool) | no | no | no | UNKNOWN |
| pool0 (datos: iscsi zvol DBs, aranea_storage, trading_systems, proxmox_storage) | T0 | NINGUNO (0 snapshots) | no | no | no | DISCOVERED |
| pool2 (backup legacy + destino potencial) | T0/T2 | contenido manual histórico | no | no | scrub overdue | DISCOVERED |
| etcd cluster 101/147/154/155/156 | T0 | NINGUNO | no | no | no | DISCOVERED |
| etcd-keeper 148 | T0 | NINGUNO | no | no | no | DISCOVERED |
| kafka 136/138/139 | T0 | NINGUNO | no | no | no | DISCOVERED |
| mt4-real 124 | T0 | NINGUNO | no | no | no | DISCOVERED |
| mt4-ftmo 133 | T0 | NINGUNO | no | no | no | DISCOVERED |
| mt4-ttp 134 | T0 | NINGUNO | no | no | no | DISCOVERED |
| mt4-demo 144 | T0 | NINGUNO | no | no | no | DISCOVERED |
| echo 140 | T0 | NINGUNO | no | no | no | DISCOVERED |
| postgres 152 (+zvol pg_data) | T0 | NINGUNO | no | no | no | DISCOVERED |
| mongo 153 (+zvol mongo_data) | T0 | NINGUNO | no | no | no | DISCOVERED |
| argus 160 | T0 | NINGUNO | no | no | no | DISCOVERED |
| docker-flink 126 | T0 | NINGUNO | no | no | no | DISCOVERED |
| docker-hasura 129 | T0 | NINGUNO | no | no | no | DISCOVERED |
| Second Brain + LiveSync 116 | T0 ADD | LiveSync local PARTIAL (destinos externos UNKNOWN) | UNKNOWN | no | no | PARTIAL |
| Hermes platform state | T0 ADD | backup config puntual sin schedule | no | no | no | PARTIAL |
| mcps 113 | ADD | NINGUNO | no | no | no | DISCOVERED |
| minio 157 + minio_data | ADD | NINGUNO | no | no | no | DISCOVERED |
| temporal 158 | ADD | NINGUNO | no | no | no | DISCOVERED |
| daedalus 142 | ADD | NINGUNO | no | no | no | DISCOVERED |
| docker-echo-dev 141 / kafka 128 / observability 127 / emqx 103 / HA 105 / jobs 106 / worker 135 | ADD | NINGUNO | no | no | no | DISCOVERED |
| PBS 180 | ADD | NINGUNO (el backup server sin protección propia) | no | no | no | UNKNOWN |
| ca 200 STOPPED | UNKNOWN | NINGUNO | no | no | no | UNKNOWN |
| sqx 108/111/123 + lab stopped (~17 VMs) | T3 | NINGUNO | no | no | no | DISCOVERED |

Veredicto de matriz: **0 unidades en READY; 0 con backup ejecutándose; 1 UNKNOWN con infraestructura parcial (PBS).** El runtime está hoy en el estado "backups parciales y silenciosos" que el diseño describía, agravado por 3 meses de nuevos workloads críticos sin cobertura.

## 8. Document drift (R0.6)

| Documento | Estado | Problema | Acción |
|---|---|---|---|
| `04-backups/*` (5 archivos) | REUSABLE_BUT_STALE→HISTORICAL | Era 2026-06-30 (pre-NOPASSWD, referencias BACKUP-SYSTEM/AUDIT y stack viejo; bloqueador que cita ya resuelto) | Marcar HISTORICAL/SUPERSEDED en README; preserving recovery-procedures como referencia |
| `DESIGN-PROPOSAL.md`, `PROPUESTA-COMPLETA-ITER4.md`, `BACKUP-SYSTEM.md`, `AUDIT.md`, `TOPOLOGY-AUDIT.md` (03-storage) | Sin marcar deprecated | agent-project-00 los declaraba deprecados pero frontmatter sigue `status: active` | Corregir frontmatter (hecho en este R0, ver §11) |
| `00-index.md` backup-dr | CURRENT | Apuntaba captura 2026-06-30 | Actualizado (§11) |
| `fechas-captura.md` | STALE | No registraba captura 2026-07-02 (existía en discovery/ sin actualizar docs) ni la nueva | Actualizado (§11) |
| nodo-*.md (6) | STALE | Headers de captura 2026-06-28/30 | Actualizados a 2026-09-16 (§11) |
| agent-project-02 | INVALID_ASSUMPTION parcial | Asume crear VM 180 desde cero; la VM ya existe (running, no integrada) | Reescribir alcance en R2 (adoptar/recuperar, no crear) |
| agent-project-06 | STALE | Referencia `docker-observability` como stack; mandato fija ARGUS como plataforma y `aranea-observability-ro` RO | Reescribir en R6 vía management path de observabilidad |
| Tickets 018-021 | vigentes | Siguen todo/abiertos; 019 (maint window) e 020 (secret zero) bloquean R2/R3 | Consolidar en owner bundle |
| `SCHEDULE-DECISIONS-TEMP.md`, `src-migration-log.md` | NO EXISTEN | Mandato los esperaba en 03-storage/backup-dr/ | Gap documental; no recrear sin contenido real; reportado |

## 9. Roadmap actualizado R1–R8 (R0.8)

| Fase | Alcance corregido por evidencia | Dependencia | Criterio de cierre |
|---|---|---|---|
| R1 | Bootstrap/config crítico: definir y ejecutar primer backup real de configs (traefik, pi-hole, /etc/pve export via wrapper GAP, etcd snapshot, Hermes+vault). Incluye decidir staging (Hermes VM 118) y resolver F-09 existence check | R0 (hecho) | ≥1 backup CONFIGURED+VERIFIED de cada clase de config; restore a scratch probado en 1 caso |
| R2 | PBS: recuperar/adoptar VM 180 (owner), integrar pve_storage, primer vzdump real de 1 VM T0, retention+verify | Owner gate .180 + maint window | vzdump diario T0 VERIFIED + restore drill 1 |
| R3 | App-consistent: pg_dumpall 152, mongodump 153, CouchDB 116, minio mirror, snapshots pool0 (sanoid o nativo TrueNAS), etcd snapshot cluster | R2 staging | Dumps diarios VERIFIED + 2 restore drills DB |
| R4 | Offsite crítico: proveedor + cifrado (revalidar pcloud vs alternativas), restic repo, push semanal | Owner gates OAuth/secret | 1 snapshot restic VERIFIED offsite + drill descarga |
| R5 | Bulk/archive: revalidar GDrive/pCloud/otros; chunking pool0; monthly | R4 infra | 1 chunk VERIFIED + drill recv |
| R6 | Observabilidad: señales de backup en ARGUS vía management path del stack (no RO capability), alertas mínimas policy | R2-R4 jobs | Alertas activas + test de disparo real |
| R7 | Restore drills continuos + certificación por unidad (estados §14 mandato) | R2-R6 | Cada unidad T0/T1 con drill PASS reciente |
| R8 | Autonomía operativa + closeout, skills, runbook canónico único | Todo | Criterio §25 mandato |

Orden ajustado vs plan original: R1 antes que R2 porque el staging de configs no depende de PBS y da cobertura inmediata mientras se resuelve el gate de la VM 180.

## 10. Owner gates consolidados (R0)

1. **PBS VM 180**: acceder/recuperar la VM running inalcanzable (credenciales/consola) y autorizar su adopción como servidor de backups (F-06). Bloquea R2 completo.
2. **OWNER-TASK-CRITICAL-VMS (ticket 018)**: confirmar lista Tier 0 (propuesta: contract §2 + ADDs marcados CRITICAL/IMPORTANT de §6).
3. **OWNER-TASK-MAINT-WINDOW (019)**: ventana para intervención PBS y luego jobs.
4. **OWNER-TASK-SECRET-ZERO (020)**: passphrase restic/rclone/PBS + escrow offline.
5. **OWNER-TASK-OAUTH-SCOPE (021)** + revalidación de proveedor (pcloud/gdrive vigencia 2026). Bloquea R4/R5.
6. **Decisión menor**: rol de pool2 (¿destino de backups locales pese a single-disk F-14?) y si se agenda scrub (recomendado: sí, es read-only y seguro).
7. **Confirmación estado `ca` 200 stopped** (¿retirado o protegible CRITICAL?).

OWNER_BUNDLE: se preparará al iniciar R2 (bloques idempotentes por host). Los gates 2-5 existen como tickets formales; no se duplican.

## 11. Cambios ejecutados en este R0 (todos documentales, reversibles por git del vault si existiera; aquí por backups de patch)

1. Captura física 6/6 `~/aranea/topology/discovery/<nodo>_20260916_233513.txt` (read-only vía wrapper autorizado).
2. Frontmatter deprecated: `DESIGN-PROPOSAL.md`, `PROPUESTA-COMPLETA-ITER4.md`, `BACKUP-SYSTEM.md`, `AUDIT.md`, `TOPOLOGY-AUDIT.md` (status + superseded_by).
3. `04-backups/README.md` marcado HISTORICAL con puntero a fuente canónica.
4. Actualización de captura: 6× nodo-*.md, `fechas-captura.md`, `30-resources/aranea/00-index.md`.
5. `BACKUP-DR-OWNER-PROJECT.md`: status paused→active, estado real, bitácora.
6. `20-areas/Aranea.md`: status_detail del área.
7. Change log: `80-agents/journal/logs/2026-09-16-backup-dr-r0-reconciliacion.md`.

Ningún cambio en infraestructura. Ninguna credencial tocada o registrada.

## 12. Próximo workload (R1) — listo para próxima sesión

Objetivo: primer backup real y verificado de configs críticas sin depender de PBS. Pasos de alto nivel: (1) confirmar con owner F-09 (¿existe pool0_backup?) y crear staging `/opt/aranea-backup/` en Hermes VM 118; (2) wrappers: traefik dynamic config (via canal autorizado), pi-hole config, export /etc/pve (requiere resolver GAP del wrapper con owner), etcd snapshot (requiere binario etcdctl y endpoint — descubrir en R1), dump de Hermes ~/.hermes y snapshot del vault Second Brain; (3) retención 30d local + verificación sha256 + log; (4) primer restore drill a scratch. NO abrir R2 sin gates 1-3 del bundle.

## 13. Evidencia

- Capturas: `~/aranea/topology/discovery/*_20260916_233513.txt` (athena 634K, resto ~82-88K, truenas 88K).
- Sondas PBS: ping/22/8007 desde Hermes (2026-09-16 23:5x UTC) sin respuesta; control positivo a .90/.91/.120.
- DNS: getent OK vía stub; dig directo a .149 timeout; ping ICMP a .149 sin respuesta.
- Greps mecanismos: negativos para vzdump jobs, sanoid, restic, rclone, borg en los 6 nodos (fuera de paquetes estándar del sistema).
