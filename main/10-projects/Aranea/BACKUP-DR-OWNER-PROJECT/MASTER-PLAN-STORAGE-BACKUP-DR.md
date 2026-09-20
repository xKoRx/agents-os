---
title: "MASTER PLAN — Aranea Storage + Backup/DR (2026-09-20)"
type: doc
schema_version: 1
status: active
icon: 🏛️
slug: backup-dr-master-plan-storage
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: 2026-09-20
updated: 2026-09-20
aliases:
  - Master Plan Storage Backup DR
  - Arquitectura objetivo storage backup DR
tags:
  - kind/doc
  - area/aranea
  - domain/backup-dr
  - project/backup-dr
related:
  - "[[MATRIZ-59-GUESTS-BACKUP]]"
  - "[[ROADMAP-WP-BACKUP-DR]]"
  - "[[MANDATOS-IMPLEMENTACION-BACKUP-DR]]"
  - "[[BACKUP-DR-CONTRACT]]"
  - "[[BACKUP-DR-DESIGN]]"
---

# 🏛️ MASTER PLAN — Storage + Backup/DR

> Arquitectura objetivo y decisiones justificadas. Diseño congelado F-01..F-14 intacto (cambios → REQUEST-CHANGES). Este plan convierte la dirección owner 19-09 + evidencia 16-20sep en un sistema completo. Fuente de verdad de guests: [[MATRIZ-59-GUESTS-BACKUP]]; ejecución: [[ROADMAP-WP-BACKUP-DR]]; prompts: [[MANDATOS-IMPLEMENTACION-BACKUP-DR]].

## 0. Estado de partida (verificado, no supuesto)

1. **Copia recuperable demostrada existe hoy para:** configs traefik/second-brain/hermes-state (R1 diario), etcd snapshot (R1.5 diario 05:00) + pve node-local (R1.5 semanal SÁB 08:30), PostgreSQL 13 bases + Mongo archive + MinIO 12 buckets (G1A/G1B one-shot en PBS, cadena restore→descifrado→drill certificada, claves con custodia doble).
2. **Piloto vzdump R2 activo** día 2/7 (6 CTs, timer 06:05, expira 26-09, fail-closed PASS). Decisión D (retención final y producción) pendiente tras 7/7 días.
3. **0 unidades tienen retención aprobada** (R1/R1.5 y piloto R2 sí están agendados); 3-2-1 NO CUMPLE (0 off-site real); PG/Mongo/MinIO/argus-data siguen `backup=0` a nivel disco.
4. **Ceph NO_GO estructural** (nearfull 85,7% = 799/932 GiB osd.0/2, causa CRUSH host + 1 OSD/host PROBADA; kronos cae = recovery imposible; QLC 64-201%; NO_GO nuevos discos pool1).
5. **hades concentra** TrueNAS(iSCSI/NFS de datos T0) + Echo PROD; SPOF aceptado (F-13) pero sin mitigación operativa hoy (UPS inexistente — gap H5).
6. pool0 sano (scrub 0 errores) pero **sin snapshots recientes = cero rollback local**; pool2 sin scrub >14 meses con 2,15T libres.

## 1. Principios

1. **El valor se protege, no el disco.** Toda unidad de backup se define por unidad de dato (contrato §3): config, dump consistente, snapshot zvol, imagen guest.
2. **Restauración demostrada = único criterio de cobertura.** Un backup sin drill no cuenta (patrón G1A/G1B/R1).
3. **3-2-1 honesto:** copia primaria (pool0/pool1/local-lvm) → PBS (2º lugar, off-host kronos) → off-site cifrado pCloud/GDrive (R4/R5). NFS-local o pool2 no cuentan como copia independiente de pool0 (F-14 asumido; pool2 = mismo chasis que pool0 vía hades→TrueNAS).
4. **No rediseñar lo certificado:** R1/R1.5/G1A/G1B/R2 se reutilizan tal cual; los WP los agendan/integran, nunca los rehacen.
5. **Ceph no se toca desde Backup/DR.** Correcciones = ejecutor Ceph/Storage (WP-S), otro carril.
6. **UNKNOWN explícito > supuesto.** Regla contrato §4.4.

## 2. Decisiones de arquitectura (con justificación)

### D1. Placement: sin regla universal; SO reconstruible ≠ dato irremplazable

El patrón verificado (SO VMs productivas en pool1 RBD + datos en zvol pool0 vía iSCSI) **se MANTIENE** para PG 152/Mongo 153/MinIO 157: el zvol pool0 es mirror sano; migrar SOs a local-lvm perdería HA-exigida y pagaríamos migraciones masivas en Ceph nearfull. La dirección "SOs fuera de pool1" (alternativa G del assessment) queda **estratégica a mediano plazo, activada sólo si el ejecutor Ceph necesita aliviar pool1**, no como proyecto de Backup/DR.

| Backend | Rol arquitectural |
|---|---|
| pool1 (Ceph RBD) | SOs VMs productivas (HA por réplica 3). Congelado para crecimiento (NO_GO nearfull); corrección estructural = carril Ceph |
| pool0 zvol iSCSI (LUN4/5/6) | Datos T0 (PG/Mongo/MinIO). Correcto; protección = dumps+PITR+snapshots, no migración |
| local-lvm | SOs reconstruibles sin HA (etcd, traefik, pi-hole, CA, TrueNAS SO, PBS SO — datastore PBS = local-kronos) |
| nfs-storage (pool0) | rootfs CTs file-backend + ISOs; corregir `keep-all=1` (WP-A0) |
| local-sqx-* | SQX sagrado F-04, intacto |
| local-kronos/pool-kronos | PBS data + jobs + labs |

### D2. Roles de PBS / pool0 / pool2 / pCloud / GDrive (sin dominio de falla compartido)

| Destino | Rol | Dominio de falla |
|---|---|---|
| PBS (VM 180, kronos, datastore 295G→crecer) | Receptor único de vzdump + dumps G1A/G1B + ingesta staging R1; dedup; retención por clase | Node kronos (SPOF del destino local — mitigación D3) |
| staging hermes (49G) | Staging de configs R1 y dumps; ingesta→PBS (WP-A0); NO destino final | vm 118 (kronos) — por eso A0 ingesta ASAP |
| pool0 snapshots (WP-A6) | Rollback local rápido (borrado/corrupción), NO backup | pool0 mismo |
| pool2 (REPL pool0→pool2, WP-A6) | 2ª copia local de datasets pool0 | mismo chasis TrueNAS que pool0 — **no es off-host**; mitigación = off-site |
| pCloud (restic crítico) | 3ª copia off-site de configs + dumps + claves custodia | externo; gates 020/021 |
| GDrive (bulk cifrado) | Off-site de pool0 seleccionado (chunked) + PBS datastore crítico | externo; gates 020/021 |

Anti-ejemplos (regla binding): vzdump→nfs-storage NO es backup de pool0 (pool0 es la fuente); snapshot pool0 ≠ backup; REPL pool0→pool2 ≠ off-site; PBS datastore sin off-site = copia local.

### D3. PBS datastore: 295G es el cuello de botella del sistema

Hoja de ruta de capacidad (ningún paso en piloto): post-D-piloto (28sep) crecer disco scsi1 `pbs-data` (VG `local-kronos` tiene 567G libres → **+300G = 595G total**, dentro F-06/F-07). Con dedup PBS (F-11) y exclusión de reconstruibles, cabe T0a-d (SO) + dumps + staging-ingest con retención 7d/4w. **Umbral de revisión: 70%.** 2º target pool2 = opción futura (WP-B2 opcional), no bloqueante. La copia fuera de PBS es lo que salva de la pérdida del disco data.

### D3.1 Apéndice — Métricas de capacidad medidas (19-20 sep, almacenadas en WS; repetir antes de decidir D-piloto)

| Métrica | Valor medido (fecha) | Implicación |
|---|---|---|
| PBS datastore main | 733M/295G tras G1A+G1B+2 días piloto | Dedup eficaz; espacio no es el blocker del piloto |
| tier 0 alloc 660G / used-in-guest ~165-185G/ciclo | R2 discovery 18sep | vzdump full T0 post-piloto cabe en +300G si dedup se comporta; re-medir si se suma flota ADD |
| dump PG 160M + Mongo 73M/día (comprimidos en PBS tras dedup ≈ menor) | G1A 20sep | dumps diarios ~decenas de MB/día efectivos |
| MinIO 64,76G lógicos → 12 snapshots pxar (dedup alto entre runs) | G1B 20sep | semanal sostenible; re-stream sólo si bucket cambia fuerte |
| pool2 libre 2,15T vs full inicial REPL 1,1-1,1,6T | assessment 19sep | REPL inicial cabe sin limpiar árboles legacy |

### D4. DBs: dumps certificados + PITR como segunda iteración; RPO 1h MongoDB = decisión de topología

- **PG 152:** dumps G1A → schedule diario (WP-A1). RPO objetivo ≤1h vía WAL archiving (archive_mode=on, archive_timeout 60s) a staging hermes + PBS (WP-A2, requiere ventana/gate: cambiar postgresql.conf de un sistema trading PROD = GATED; alternativa pgBackRest). RPO real esperado ≈1-2min. **Migrar del zvol NO.**
- **Mongo 153:** dumps G1A → schedule diario. RPO 1h **NO demostrable con standalone** (sin oplog): requiere replica set 1 nodo o PBM = **cambio topológico en PROD trading → GATED, decisión owner**. Honestidad: con dumps, RPO real = 24h.
- **MinIO 157:** G1B semanal programado (WP-A4); versioning OFF = deuda R3 gated (mutación en servicio trading); artefactos SQX incluidos.

### D4.1 Propuesta técnica de RTO por clase (requiere validación por drill; owner aprueba números)

| Clase | RTO propuesto | Base técnica |
|---|---|---|
| Configs (traefik/etcd/Hermes/vault) | ≤1h | restore staging/scratch demostrado (R1/R1.5) |
| VM/LXC T0 vía vzdump+PBS | ≤4h | restore full desde PBS, reconstrucción in situ |
| PG 152 (dump) | ≤4h | drill G1A midió horas (initdb+restore+selects) |
| PG 152 (PITR) | ≤2h | base+replay; requiere WP-A2 |
| Mongo 153 | ≤4h | drill G1A (mongorestore 55.968 docs) |
| MinIO 157 | ≤12h | drill G1B (restore+arranque) 64,76G streaming |
| pool0 dataset (REPL pool2) | ≤8h | recv sobre pool2; dimensionar en WP-A6 |
| pool0 dataset (GDrive bulk) | 24-48h | descarga+recv; sólo irremplazables |
| Reconstrucción total homelab | 3-7d | DR-T6; requiere bundle Secret Zero + inventory |

### D5. Failover-recoveries (los 6 escenarios del mandato)

Los procedimientos verificables completos viven en el ROADMAP (WP-DR1..DR6, cada uno con validación y rollback) y su ejecución va por WP-R7 drills. Aquí los límites:

| Escenario | Estrategia | RPO/RTO | Dependencia circular evitada |
|---|---|---|---|
| DR-T1 pérdida de una VM | restore PBS → mismo nodo o alternativo | por clase (D4.1) | nunca requerir la VM caída como parte del restore (dumps y vzdump no dependen del guest) |
| DR-T2 pérdida de un disco | pool0 mirror reconstruye solo (hot spare no hay; F-05); Ceph re-replica (salvo kronos = NO_GO hoy); local-lvm de nodo caído = restore PBS | pool0: RPO=0, RTO=rebuild; Ceph kronos: RPO=hasta re-replica imposible→riesgo 2 copias; local-lvm RPO=7d | no requerir TrueNAS para restaurar un zvol de TrueNAS (vzdump/dumps viven en PBS) |
| DR-T3 pérdida de un nodo PVE | guests repartibles a otros nodos (pool1 RBD + nfs migran solos; local-lvm/iSCSI requieren restore o reconexión) | pool1 guests: minutos; local-lvm: RTO restore | PBS en kronos sobrevive (F-13); si cae kronos, copias locales quedan pero off-site R4 es el 2º destino |
| DR-T4 pérdida de Ceph | SOs en pool1 se reconstruyen desde templates/config (re-instalar) + datos T0 ya viven en pool0 zvol; artefactos MinIO desde G1B | SOs: RPO irrelevante (reconstruir), RTO horas-por-VM | **ningún restore requiere pool1 vivo** (dumps/snapshots/zvols no viven en Ceph); este diseño es lo que hace DR-T4 sobrevivible |
| DR-T5 pérdida de TrueNAS/hades | SO TrueNAS = reinstalar SCALE + import pool0/pool2 (pools sobreviven al chasis); zvols intactos; restore guests dependientes (nfs CTs, iSCSI data guests) | pools: RPO=0 (disco intacto); RTO=reinstalar+import+reattach | PBS kronos + off-site no dependen de hades; config TrueNAS exportada (WP-B2) evita reconfigurar a mano |
| DR-T6 pérdida total Aranea | off-site cifrado (pCloud crítico + GDrive bulk) + Secret Zero (020) + inventory (R1) | RPO=1d configs, 1-7d datos | el bundle de recuperación vive fuera (020: caja fuerte+USB); sin 020 no hay DR-T6 |

### D6. Dependencias circulares verificadas y su resolución

| Dependencia circular | Resolución |
|---|---|
| PG/Mongo/MinIO datos en zvol pool0 vía TrueNAS (hades) — hades cae, datos inaccesibles aunque pools intactos | dumps/PITR y snapshots PBS **no dependen del guest caído ni de hades vivo**; restore a cualquier nodo con PBS; iSCSI re-attach al levantar hades |
| PBS 180 (kronos) destino único local | off-site (R4/R5) + 2º target pool2 opcional; ingesta staging en 2º lugar de falla (hermes también en kronos: mitigar moviendo staging off-kronos en R4+ o aceptando off-site como mitigación) |
| etcd quorum 5 miembros en 5 hosts | cluster sobrevive 2 caídas; snapshot lógico diario R1.5 cubre pérdida total |
| nfs-storage (pool0) rootfs de 4 CTs | vzdump de esos CTs NO es copia fuera de pool0 → PBS + off-site; REPL pool0→pool2 no cuenta como off-host |
| Vault 116 (CouchDB) rootfs nfs 64G | dump CouchDB (WP-A1) + vzdump post-D |
| mcps rootfs nfs + plano de acceso | vzdump post-D + CFG mcps-ops (WP-A5) |

### D7. Roadmap maestro R-fases ↔ carriles

El roadmap R0-R8 del proyecto es la autoridad de fases; los WPs concretos en [[ROADMAP-WP-BACKUP-DR]]. Correspondencia:

- R1/R1.5 **hecho** (configs VERIFIED) — WP-A0 los integra a PBS.
- R2 **en curso** (piloto día 2/7; D-piloto 28sep gated) — WP-B1 = decisión D + producción.
- R3 = **WP-A1..A6** (dumps scheduled, PITR, MinIO, pool0 snap/REPL, compose CFG).
- R4 = **WP-A7** (restic pCloud crítico; gates 020/021).
- R5 = **WP-A8** (GDrive bulk cifrado).
- R6 = **WP-B3** (ARGUS señales backup).
- R7 = **WP-R7** (drills recurrentes certificación).
- R8 = **WP-B4** (runbook canónico + closeout).
- Carril Ceph/Storage = **WP-S1..S4** (ejecutor distinto; handoff H5/H6 vigente).
- Carril Edge/DR = **WP-B2** (config exports OPNsense/TrueNAS/PBS/mcps + decisión CA) + **WP-DR** (procedimientos 6 escenarios).

## 3. Problemas que SÍ necesitan corrección (priorizados por reducción de riesgo global)

1. **0 off-site + Secret Zero 020 sin resolver** → hoy la pérdida total (DR-T6) = pérdida total de datos. Es el riesgo #1 del sistema; mitigación barata y de máximo impacto.
2. **Dumps DB/MinIO one-shot sin schedule** → la única protección de datos T0 de Echo envejece; sin agenda, en 30d quedó obsoleta (retención G1A/G1B 30d sin prune).
G1A/G1B sin prune → riesgo de llenado lento de datastore.
3. **pool0 sin snapshots** → borrado/corrupción accidental no tiene rollback local; REPL pool0→pool2 inexistente.
4. **vzdump producción inexistente** → pérdida de VM = reinstalar+reconfigurar; piloto R2 termina 26-28sep y desbloquea.
5. **Ceph nearfull estructural** (riesgo de disponibilidad de SOs en pool1 y de flota DEV) → carril Ceph, NO Backup/DR.
6. **pi-hole .149 L2-dead + CA 200 stopped** → edge/quorum degradados; resolución de estado, no backup.
7. **LUN2 double-attach latente + RBD huérfana 120G** → riesgo latente e higiene; WP-S1 gated dueño.

## 4. Ventana de mantenimiento (Echo vuelve domingo noche)

- **Sin downtime (AUTO, no requiere ventana):** ingesta staging→PBS (A0), schedules dumps (A1/A4), snapshots zvol (A6), compose CFG (A5), observabilidad (B3), config exports read-only (B2), ingestas y timers, runbook (B4), MCP RO (S4).
- **Requiere ventana (sábado madrugada):** PITR PG (A2, reinicio postgres), Mongo topología (A2b, si owner aprueba), vzdump T0 inicial (B1: prever I/O; MT4/echo en hades con CPU/idle I/O hoy), REPL full inicial (A6, I/O masivo pool0→pool2), pool2 scrub (A6), compact Ceph + mClock (S2, ventana), liberaciones 112/162/170 (S1, dueño).
- **Diferido a próxima ventana:** revisiones de decomisión (100/151), 2º target PBS→pool2, versioning MinIO, off-site bulk inicial (GDrive full pool0). Off-site crítico (A7) es sin downtime (restic sobre staging/PBS), no requiere ventana.
- Regla: **nada arriesgado contra la operación de Echo domingos**; ventanas = sábado madrugada, y las GATED requieren OK owner explícito por WP.

## 5. Bloqueantes exclusivamente del owner (consolidados)

1. **Ticket 018** — lista Tier 0 final (propuesta vigente: 23 contrato + ADDs propuestos; matriz como insumo). Bloquea WP-B1.
2. **Ticket 019** — ventana de mantenimiento formal. Bloquea B1/A2/A6-REPL/S2.
3. **Ticket 020** — Secret Zero (ubicación caja fuerte + USB cifrado). Bloquea A7/A8/DR-T6.
4. **Ticket 021** — OAuth pCloud/GDrive (agente vs owner). Bloquea A7/A8.
5. **Decisión D-piloto (28sep)** — retención final PBS + pasar a producción (preflight AP-02). Bloquea B1.
6. **Decisión Mongo topología** — replica set 1 nodo/PBM para RPO 1h (cambio PROD trading). Bloquea RPO 1h Mongo; sin ella RPO Mongo=24h.
7. **Decisión datasets pool0→pool2 + limpieza legacy pool2** (puede posponerse: inicial cabe en 2,15T libres).
8. **Decisión CA 200** — reactivar+proteger claves vs retiro formal.
9. **Decisión dueño VMIDs 112/162/170** (liberar discos) — ejecución = carril Ceph gated.
10. **Decisión decomisión 100/151** + destino zvols win (~606G). UNKNOWN → 018.

## 6. Primer bloque tras aprobar el plan

**WP-A0** (ingesta staging→PBS + corregir prune nfs) — es AUTO, sin ventana, reutiliza mecanismo G1A demostrado, convierte las 4 unidades R1/R1.5 en una sola copia protegida en PBS y libera la dependencia del staging; se ejecuta inmediatamente después de la aprobación del plan y mientras el owner resuelve 018-021/D. En paralelo, **WP-A1** (schedules PG/Mongo/MinIO) queda listo para ejecutar sin ventana una vez aprobado (los mecanismos ya existen certificados; es agendar, no inventar).

---
*Métricas de capacidad medidas en WS: `~/aranea/work/master-plan-20260920/CAPACITY-METRICS.md` — repetir antes de decidir D-piloto (28sep).*
