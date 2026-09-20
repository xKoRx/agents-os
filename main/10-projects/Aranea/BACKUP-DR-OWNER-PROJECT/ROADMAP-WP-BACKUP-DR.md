---
title: "ROADMAP — Work Packages Storage + Backup/DR (2026-09-20)"
type: doc
schema_version: 1
status: active
icon: 🗺️
slug: backup-dr-roadmap-wp
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: 2026-09-20
updated: 2026-09-20
aliases:
  - ROADMAP WP Backup DR
  - WPs storage backup DR
tags:
  - kind/doc
  - area/aranea
  - domain/backup-dr
  - project/backup-dr
related:
  - "[[MASTER-PLAN-STORAGE-BACKUP-DR]]"
  - "[[MATRIZ-59-GUESTS-BACKUP]]"
  - "[[MANDATOS-IMPLEMENTACION-BACKUP-DR]]"
  - "[[2026-09-16-R0-reconciliacion]]"
---

# 🗺️ ROADMAP — Work Packages

> Ejecución del [[MASTER-PLAN-STORAGE-BACKUP-DR]]. Formato: `ID | objetivo | ejecutor | dependencias | operaciones | riesgo | gate owner | validación | rollback | DoD`. Corresponde 1:1 con el roadmap R0-R8 (R0 §9) y los 9 agent-projects. Los WPs no crean proyectos nuevos: agendan/integran mecanismos ya certificados y añaden los que faltan. Ventana: Echo opera domingos desde la noche → ventanas = sábado madrugada; GATED = OK owner explícito por WP.

## Bloque A — Backup/DR: cobertura de datos y configs (carril Backup/DR)

### WP-A0 — Ingesta staging→PBS + higiene del destino NFS
`ID` WP-A0 · `objetivo` copias R1/R1.5 (traefik, second-brain, hermes-state, etcd-snap, pve-node) residir en PBS, no sólo staging; corregir prune `keep-all=1` de nfs-storage · `ejecutor` Backup/DR (Ariadna) · `dependencias` ninguna (AUTO) · `operaciones` ingesta pxar patrón G1A de run-dirs staging → `host/r0d-config-*`; PRIMERO listar contenido backup de nfs-storage (R0 lo clasifica ABANDONED/UNKNOWN — si existen vzdump antiguos, documentarlos antes de tocar retención); corregir prune-backups del storage nfs-storage en 5 nodos (documentado, idempotente); verificación round-trip 1 unidad · `riesgo` bajo (mecanismo demostrado G1A; prune nfs sólo tras inventariar lo existente) · `gate` ninguno (AUTO, sin ventana) · `validación` listing PBS `host/r0d-config-*` + round-trip sha de 1 unidad + nfs-storage sin keep-all · `rollback` eliminar snapshots ingestados; revertir storage.cfg con diff guardado · `DoD` 5 unidades config con copia en PBS + prune corregido.

### WP-A1 — Schedules de dumps G1A/G1B (PG 152, Mongo 153, MinIO 157)
`ID` WP-A1 · `objetivo` convertir los dumps certificados one-shot en jobs diarios/semanales con retención · `ejecutor` Backup/DR (Ariadna) · `dependencias` WP-A0 (destino PBS ordenado); 018 sólo si el schedule cambia alcance de lo ya ejecutado (no lo cambia: mismas unidades) · `operaciones` timers systemd en hermes: PG dump diario (patrón g1a-driver), Mongo dump diario, MinIO stream semanal; cifrado AES-256 con claves custodiadas ([[BACKUP-DR-KEY-RECOVERY]]); ingesta pxar→PBS; retención 30d sin prune (ídem G1A/G1B) hasta decisión de retención final · `riesgo` medio-bajo: dumps PG/Mongo 03:00-03:45 — ANTES de los timers R1 04:00/05:00 que corren en el MISMO host hermes (respetar solape; no re-agendar R1); MinIO semanal fuera de esa ventana; todo fuera de R2 06:05 y de operación Echo · `gate` ninguno para PG/Mongo (patrón ya autorizado y ejecutado); **MinIO semanal recurrente = GATE OWNER** (MinIO es ADD no aprobado — regla 4.1/018; sin decisión explícita, MinIO queda como one-shot G1B hasta nueva autorización) · `validación` 2 ciclos con VERIFY_TASK_OK + sha manifest + drill de 1 restore · `rollback` desactivar timers nuevos (nunca tocar R1/R2) · `DoD` PG+Mongo VERIFIED+AUTOMATED con 2 ciclos y 1 drill; MinIO según gate.

### WP-A2 — PG PITR/WAL archiving (RPO ≤1h) [GATED ventana]
`ID` WP-A2 · `objetivo` RPO 1h real en PG 152 · `ejecutor` Backup/DR con gate · `dependencias` WP-A1; ticket 019 (ventana); OK owner por mutación en PROD trading · `operaciones` medir tasa WAL (UNKNOWN hoy); `archive_mode=on` + `archive_timeout=60s` + archive_command rsync→staging hermes (WAL fuera de pool0); base backup pg_basebackup semanal; restore drill PITR a scratch · `riesgo` medio: reinicio de postgres en ventana; espacio WAL a medir antes · `gate` OWNER (ventana 019 + cambio config PROD trading) · `validación` PITR drill: restore a segundo objetivo, SELECTs reales (patrón G1A) · `rollback` archive_mode=off + revert postgresql.conf (diff guardado); timers WAL desactivados · `DoD` PITR VERIFIED con RPO medido ≤5min y drill PASS.

### WP-A2b — Mongo RPO 1h: replica set 1 nodo o PBM [GATED decisión topológica]
`ID` WP-A2b · `objetivo` cerrar el único hueco de RPO 1h · `ejecutor` Backup/DR con gate · `dependencias` decisión owner de topología (bloqueante #6 del master plan); 019 · `operaciones` convertir standalone→replica set 1 nodo (o instalar PBM); oplog tail continuo→staging · `riesgo` ALTO para un sistema trading en PROD: cambio topológico; requiere plan de reversión y ventana dedicada · `gate` OWNER explícito (no se propone por defecto; alternativa aceptada: mantener RPO 24h con dumps) · `validación` oplog tail + PITR drill Mongo · `rollback` volver a standalone desde dump+snapshot zvol previo · `DoD` decisión ejecutada y RPO medido, o decisión documentada de mantener 24h.

### WP-A3 — CouchDB 116 dump (vault LiveSync)
`ID` WP-A3 · `objetivo` dump consistente del CouchDB del vault · `ejecutor` Backup/DR · `dependencias` WP-A0 · `operaciones` CouchDB ya corre en LXC 116 con acceso por canal autorizado (R1 protege el vault exportado; aquí dump de la BD viva `_all_dbs` replicator); diario + ingesta PBS · `riesgo` bajo (lectura replicator/HTTP local) · `gate` ninguno si canal existente lo permite; si requiere credencial nueva → bundle puntual · `validación` restore a CouchDB scratch + conteo de docs vs live · `rollback` desactivar timer · `DoD` dump diario VERIFIED + 1 drill.

### WP-A4 — MinIO semanal + decisión versioning (parte gated)
`ID` WP-A4 · `objetivo` proteger artefactos SQX con historia · `ejecutor` Backup/DR · `dependencias` WP-A1 (infra del timer) · `operaciones` parte AUTO: activar el stream G1B semanal (WP-A1 ya lo incluye — separado aquí para trazabilidad con ap-03). Parte GATED: activar bucket versioning en producción MinIO (mutación en servicio trading) · `riesgo` AUTO bajo; versioning = medio (cambio en servicio vivo) · `gate` versioning: OWNER · `validación` snapshot semanal VERIFY_TASK_OK; con versioning: restore de versión anterior de 1 objeto · `rollback` timers off; versioning se desactiva por bucket · `DoD` semanal VERIFIED 2 ciclos; versioning ejecutado o deuda registrada.

### WP-A5 — Compose/config de CTs docker + mcps + PBS config
`ID` WP-A5 · `objetivo` configs de 126/129/141/127/128/158/142/113/180 bajo R1 · `ejecutor` Backup/DR · `dependencias` WP-A0 · `operaciones` exportar compose/env/units (sin secretos en claro: referencias) de cada CT/docker host + `/etc/proxmox-backup-*` de PBS 180; semanal · `riesgo` bajo · `gate` ninguno (lectura) · `validación` restore scratch de 1 compose + sha manifests · `rollback` timers off · `DoD` unidad config nueva VERIFIED para 9 targets.

### WP-A6 — pool0: snapshots + replicación selectiva pool0→pool2 + scrub pool2 [REPL inicial en ventana]
`ID` WP-A6 · `objetivo` rollback local (snapshots) + 2ª copia local de datasets seleccionados · `ejecutor` Backup/DR con gate TrueNAS · `dependencias` decisión owner de datasets (bloqueante #7 — default propuesto: `trading_documents`, `home`, `proxmox_storage`, `apps/*/config`, `iscsi` zvols T0, `aranea_storage` semanal; exclusión frigate media); 019 para full inicial · `operaciones` snapshot schedules sanoid/nativo (horario zvols T0, diario datasets); replicación local TrueNAS push→`pool2/pool0_new/` (dataset NUEVO; F-09 intacto); `zfs send -n` dry-run antes; scrub pool2 (read-only, seguro) · `riesgo` I/O del full inicial (~1,1-1,6T) en ventana; snapshots = espacio controlado con retención corta · `gate` OWNER: selección datasets + ventana full inicial; scrub AUTO (read-only) · `validación` recv de dataset de prueba + drill rollback de 1 zvol desde snapshot · `rollback` destruir `pool2/pool0_new/` (dataset nuevo); desactivar schedules · `DoD` snapshots activos + 1º full REPL VERIFIED + scrub pool2 0 errores.

### WP-A7 — Off-site crítico restic→pCloud [gates 020/021]
`ID` WP-A7 · `objetivo` 3ª copia fuera del homelab (configs + dumps + claves custodia) · `ejecutor` Backup/DR · `dependencias` 020 (Secret Zero) + 021 (OAuth) · `operaciones` restic repo cifrado en pCloud; push semanal desde staging+PBS export; drill de descarga+descifrado · `riesgo` bajo técnico; OAuth/credenciales = superficie sensible · `gate` OWNER 020+021 · `validación` 1 snapshot VERIFIED offsite + drill descarga/restauración · `rollback` revocar token; borrar repo remoto · `DoD` off-site crítico VERIFIED (3-2-1 cumple para configs/dumps).

### WP-A8 — Off-site bulk GDrive (chunked pool0 + PBS crítico) [gates 020/021]
`ID` WP-A8 · `objetivo` sobrevivir pérdida total de datasets pool0 · `ejecutor` Backup/DR · `dependencias` A7; 020+021; decisión de qué datasets van a bulk · `operaciones` rclone crypt chunked mensual de datasets irremplazables + export cifrado del datastore PBS (crítico) · `riesgo` cuotas/tiempos de carga GDrive; primer full largo (sin ventana: es push, no I/O local significativo) · `gate` OWNER 020+021 · `validación` 1 chunk VERIFIED + drill recv · `rollback` borrar remote · `DoD` bulk VERIFIED (3-2-1 cumple para pool0 selectivo).

## Bloque B — Plataforma de backup, edge y observabilidad

### WP-B1 — vzdump T0 producción (post-piloto R2) [gates 018/019/D]
`ID` WP-B1 · `objetivo` cobertura imagen-level de Tier 0 · `ejecutor` Backup/DR · `dependencias` decisión D-piloto (28sep, retención final) + 018 (lista definitiva) + 019 (ventana inicial) + crecimiento datastore (D3) · `operaciones` jobs vzdump diarios 02:00 T0 (o split para no solapar con dumps), semanal T1/T2; exclusiones §6.3 diseño; retención según D; verify jobs PBS · `riesgo` I/O de full backups sobre hades (MT4/echo: idle nocturno UNKNOWN — la serie R2 mide otros CTs; limitar bandwidth y ventanas); datastore debe crecer ANTES · `gate` OWNER (D + 018 + 019) · `validación` 7 días VERIFIED + restore drill de 1 VM T0 completa · `rollback` desactivar jobs (piloto/demostrado reversible) · `DoD` vzdump diario T0 VERIFIED+AUTOMATED.

### WP-B2 — Config exports edge/infra + decisión CA
`ID` WP-B2 · `objetivo` OPNsense/TrueNAS/pi-hole/PBS config bajo protección; resolver CA 200 · `ejecutor` Backup/DR · `dependencias` gap de acceso: OPNsense API/backup + TrueNAS API key (H1 tiene WS DDP — verificar si export config requiere bundle) + pi-hole token FTL6 · `operaciones` export config OPNsense semanal; export config TrueNAS via API (unidad nueva); pi-hole: resolver estado del servicio (.149 L2-dead) con owner y luego proteger; CA 200: ejecutar decisión owner (reactivar+backup claves o retiro formal) · `riesgo` bajo · `gate` pi-hole/CA: decisión owner; resto AUTO si canal existe · `validación` restore/reimport de config en laboratorio o scratch · `rollback` timers off · `DoD` 3-4 unidades config nuevas VERIFIED + decisión CA documentada.

### WP-B3 — Observabilidad de backups en ARGUS (R6)
`ID` WP-B3 · `objetivo` backup silencioso = backup roto · `ejecutor` Backup/DR vía management path · `dependencias` A1/B1 corriendo · `operaciones` señales: edad de último backup por unidad, VERIFY tasks PBS, espacio datastore, timers failed; alertas mínimas policy (diseño §8) · `riesgo` bajo · `gate` ninguno (RO) · `validación` disparo real de 1 alerta en test · `rollback` quitar dashboards/reglas · `DoD` alertas activas + test de disparo PASS.

### WP-B4 — Runbook canónico + closeout (R8)
`ID` WP-B4 · `objetivo` operación reproducible por tercero · `ejecutor` Backup/DR · `dependencias` A0-B3 · `operaciones` consolidar `BACKUP-DR-RUNBOOK.md` (restore procedures por unidad) + checklists; cerrar workloads con change logs (ap-08) · `riesgo` bajo · `gate` validación owner del runbook · `validación` un agente fresco ejecuta 1 restore guiado por runbook · `DoD` runbook validado + checklists 1 ciclo.

## Bloque S — Ceph/Storage (ejecutor CEPH, NO Backup/DR)

### WP-S1 — Inventario + liberaciones gated + riesgo LUN2
`ID` WP-S1 · `objetivo` aliviar pool1 con higiene segura · `ejecutor` Ceph/Storage · `dependencias` decisión dueño 112/162/170 + decomisión 100/151 (018) · `operaciones` liberar imagen RBD huérfana 120G (lock stale) y discos 162/170 si dueño confirma; resolver double-attach LUN2 (100 vs 151) antes de cualquier start; documentar fichas de disco (política alta §7 assessment) · `riesgo` medio (borrar discos = irreversible → confirmación dueño por VMID, no por nombre) · `gate` OWNER + ventana · `validación` freed GB medidos + `rbd ls` post; HEALTH sin cambios negativos · `rollback` snapshots previos de los discos a liberar donde sea posible; sino: lista de exclusión definitiva · `DoD` +140-190G lógicos liberados o decisión documentada de no liberar.

### WP-S2 — mClock balanced + compact osd.0/2 [ventana]
`ID` WP-S2 · `objetivo` quitar perfil recovery-prioritario permanente y fragmentación · `ejecutor` Ceph/Storage · `dependencias` 019; medición antes/después · `operaciones` `ceph config` global mClock→balanced + recovery_sleep>0; bluestore compact osd.0/2; métricas osd perf pre/post · `riesgo` bajo-medio (I/O temporal del compact) · `gate` OWNER ventana · `validación` HEALTH igual o mejor; latencia osd.0/2 medida antes/después · `rollback` revert config Ceph (no destructiva) · `DoD` perfil balanced activo + compact hecho + métricas registradas.

### WP-S3 — Decisión estructura pool1 (alternativa F/G)
`ID` WP-S3 · `objetivo` resolver la causa estructural (FD host + 1 OSD/host) sin capex · `ejecutor` Ceph/Storage + owner · `dependencias` S1/S2; inventario SATA sin montar hera/zeus (200G×2, 32G×2, 100G) · `operaciones` evaluar OSDs adicionales de discos existentes (clases mixtas, margen corto) vs mover SOs fuera de pool1 (estratégico) vs mantener con riesgo documentado · `riesgo` por diseño; sin capex (F-01) · `gate` OWNER (decisión estructural) · `validación` simulación CRUSH + margen post-cambio · `rollback` remover OSD añadido / revertir pesos · `DoD` decisión estructural registrada con números o F-01 revisado explícitamente.

### WP-S4 — Instrumentación de latencia Ceph (cerrar NOT_PROVEN)
`ID` WP-S4 · `objetivo` medir p95 y correlate con recoveries · `ejecutor` Ceph/Storage · `dependencias` ninguna (RO) · `operaciones` exporter de métricas osd perf/slow-ops → ARGUS (observabilidad RO existente) · `riesgo` ninguno · `gate` ninguno · `validación` series visibles 7d · `rollback` quitar exporter · `DoD` evidencia futura de lag medible.

### WP-R7 — Drills recurrentes + certificación (R7)
`ID` WP-R7 · `objetivo` cada unidad T0/T1 con drill PASS reciente (<35d); procedimientos DR ejecutados · `ejecutor` Backup/DR · `dependencias` A0/A1 (drills DR-T1/DR-T4 posibles en cuanto A0/A1 estén activos), resto según off-site/ventanas · `operaciones` ejecutar drills DR-T1..T6 según ROADMAP bloque DR; certificar estados por unidad (§14 mandato R0); calendario recurrente post-B1 · `riesgo` bajo (targets scratch) · `gate` ninguno para drills scratch; ventana para DR-5 · `validación` cada drill PASS con evidencia en change log · `rollback` borrar targets scratch · `DoD` unidad T0/T1 sin drill fresco = 0.

## Bloque DR — Procedimientos de desastre (ejecuta Backup/DR; drills por WP-R7)

Formato comprimido (procedimiento completo se redacta ejecutable en su mandato; aquí estrategia + prueba de validación):

| ID | Escenario | Estrategia (ref master plan D5) | Validación del drill | Rollback del drill |
|---|---|---|---|---|
| DR-T1 | Pérdida de una VM T0 | restore PBS a nodo alternativo; datos app desde dumps | drill: restore 1 CT + 1 VM a scratch (ya demostrado CT 990/G1A) | borrar target scratch |
| DR-T2 | Pérdida de un disco | pool0: rebuild mirror + scrub; Ceph: NO re-replicate kronos hoy (S1-S3 primero); local-lvm: restore PBS | drill: fallar 1 disco simulado no ejecutable sin riesgo → validar procedimiento documentado + healthy check | n/a (documental si no hay ventana) |
| DR-T3 | Pérdida de un nodo PVE | migración/restore guests; kronos caído = escenario especial (PBS+staging perdidos → ver master plan D5) | drill de mesa + restore de 1 guest local-lvm a otro nodo | borrar targets |
| DR-T4 | Pérdida de Ceph | reconstrucción SOs desde templates + datos ya en pool0; artefactos desde G1B | drill: levantar 1 VM de prueba con SO en local-lvm + MinIO desde G1B (ya demostrado arranque aislado) | teardown scratch |
| DR-T5 | Pérdida de TrueNAS/hades | reinstall SCALE + import pools + re-attach iSCSI/NFS | drill: en ventana, export/import de 1 dataset de prueba + checklist config export (WP-B2 prerrequisito) | revert attach |
| DR-T6 | Pérdida total Aranea | bundle off-site + Secret Zero + inventory + runbook | drill parcial: descargar resto restic + descifrar en máquina limpia | borrar copias locales de prueba |

Prerrequisito transversal: WP-B2 (config exports) y A7/A8 (off-site) — sin ellos DR-T5/DR-T6 son procedimientos incompletos. Los drills DR-T1/DR-T4 pueden ejecutarse en cuanto A0/A1 estén activos.

## Orden y paralelismo

```
AHORA (AUTO, sin ventana):      A0 → A1 → (A3, A5, A7-si-gates) en paralelo
                                 └→ A4 (MinIO semanal incluido en A1)
EN PARALELO (owner decide):     018 · 019 · 020 · 021 · D-piloto · Mongo topología · datasets REPL · CA
DESPUÉS DE GATES:               B1 (vzdump producción) · A2 (PITR ventana) · A6 (snap+REPL ventana) · B2
CARRIL CEPH (otro ejecutor):    S4 (ya) → S1 (dueño) → S2 (ventana) → S3 (decisión)
CONTINUO:                       B3 (observabilidad, tras A1/B1) · WP-R7 drills · B4 al final
```

Precedencia estricta: B1 requiere D-piloto + 018 + crecimiento datastore; A2 requiere A1+019; A6-full requiere 019; S2 requiere 019; nada del bloque S toca Backup/DR y viceversa.

## Riesgo priorizado (reducción de riesgo global, no "terminar DBs primero")

1. A7/A8+020 (elimina pérdida total) → 2. A0+A1 (protección deja de envejecer) → 3. A6 (rollback local pool0) → 4. B1 (cobertura imagen T0) → 5. S1/S2 (salud Ceph) → 6. B2 (edge/DR prerrequisitos) → 7. resto.
