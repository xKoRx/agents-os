---
title: "ROADMAP — Work Packages Storage + Backup/DR (2026-09-20)"
type: doc
schema_version: 1
status: active
icon: 🗺️
slug: backup-dr-roadmap-wp
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: "2026-09-20"
updated: "2026-09-21"
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
`ID` WP-A0 · `objetivo` copias R1/R1.5 (traefik, second-brain, hermes-state, etcd-snap, pve-node) residir en PBS, no sólo staging; corregir prune `keep-all=1` de nfs-storage · `ejecutor` Backup/DR (Ariadna) · `dependencias` ingesta + inventario = AUTO; mutación storage.cfg = GATE OWNER · `operaciones` ingesta pxar patrón G1A de run-dirs staging → `host/r0d-config-*` (AUTO); PRIMERO listar contenido backup de nfs-storage (AUTO read-only; R0 lo clasifica ABANDONED/UNKNOWN — si existen vzdump antiguos, documentarlos antes de tocar retención); LUEGO corregir prune-backups del storage nfs-storage en 5 nodos — **GATED: editar /etc/pve/storage.cfg es mutación de configuración PVE, no escritura documental; requiere OK owner sobre diff exacto por nodo** (documentado, idempotente); verificación round-trip 1 unidad (AUTO) · `riesgo` bajo (mecanismo demostrado G1A; prune nfs sólo tras inventariar lo existente y con gate) · `gate` ingesta/inventario/round-trip: ninguno (AUTO, sin ventana); corrección prune storage.cfg: OWNER · `validación` listing PBS `host/r0d-config-*` + round-trip sha de 1 unidad + nfs-storage sin keep-all (post-gate) · `rollback` eliminar snapshots ingestados; revertir storage.cfg con diff guardado (sólo fase gated) · `DoD` 5 unidades config con copia en PBS (AUTO) + prune corregido (post-gate).

### WP-A1 — Schedules de dumps G1A/G1B (PG 152, Mongo 153, MinIO 157)
`ID` WP-A1 · `objetivo` convertir los dumps certificados one-shot en jobs diarios/semanales con retención · `ejecutor` Backup/DR (Ariadna) · `dependencias` WP-A0 (destino PBS ordenado); 018 sólo si el schedule cambia alcance de lo ya ejecutado (no lo cambia: mismas unidades) · `operaciones` timers systemd en hermes: PG dump diario (patrón g1a-driver), Mongo dump diario, MinIO stream semanal — SÓLO con gate owner (ver A4); cifrado AES-256 con claves custodiadas ([[BACKUP-DR-KEY-RECOVERY]]); ingesta pxar→PBS; retención 30d sin prune (ídem G1A/G1B) hasta decisión de retención final · `riesgo` medio-bajo: dumps PG/Mongo 03:00-03:45 — ANTES de los timers R1 04:00/05:00 que corren en el MISMO host hermes (respetar solape; no re-agendar R1); MinIO semanal fuera de esa ventana; todo fuera de R2 06:05; **timing Echo (S-07 auditoría): los runs diarios de lunes 03:00 caen dentro de la sesión que empieza domingo noche — el OK de dumps nocturnos sobre PG/Mongo en operación queda implícito en la aprobación del plan y el primer ciclo VERIFIED lo valida midiendo duración/impacto; el dueño puede forzar ventana distinta al aprobar** · `gate` PG/Mongo dumps ya ejecutados one-shot con OK owner (G1A); **la recurrencia programada indefinida (timers) requiere autorización separada — aprobar el plan/MP-01 la incluye expresamente; el OK de G1A por sí solo NO habilita agendar**; **MinIO semanal recurrente = GATE OWNER** (MinIO es ADD no aprobado — regla 4.1/018; sin decisión explícita, MinIO queda como one-shot G1B hasta nueva autorización) · `validación` 2 ciclos con VERIFY_TASK_OK + sha manifest + drill de 1 restore · `rollback` desactivar timers nuevos (nunca tocar R1/R2) · `DoD` PG+Mongo VERIFIED+AUTOMATED con 2 ciclos y 1 drill; MinIO según gate.

### WP-A2 — PG PITR/WAL archiving (RPO ≤1h) [GATED ventana]
`ID` WP-A2 · `objetivo` RPO 1h real en PG 152 · `ejecutor` Backup/DR con gate · `dependencias` WP-A1; ticket 019 (ventana); OK owner por mutación en PROD trading · `operaciones` medir tasa WAL 24h (UNKNOWN hoy); GATE DE CAPACIDAD: si la proyección mensual de WAL supera ~10G/mes, el destino staging hermes (VM 118, AMBOS discos en pool1 nearfull NO_GO) NO es viable → usar destino alternativo fuera de pool1 (datastore PBS o dataset en otro nodo) decidido en ese punto; `archive_mode=on` + `archive_timeout=60s` + archive_command rsync→destino (fuera de pool0 y, por defecto, fuera de pool1); base backup pg_basebackup semanal; restore drill PITR a scratch · `riesgo` medio: reinicio de postgres en ventana; espacio WAL a medir antes · `gate` OWNER (ventana 019 + cambio config PROD trading) · `validación` PITR drill: restore a segundo objetivo, SELECTs reales (patrón G1A) · `rollback` archive_mode=off + revert postgresql.conf (diff guardado); timers WAL desactivados · `DoD` PITR VERIFIED con RPO medido ≤5min y drill PASS.

### WP-A2b — Mongo RPO 1h: replica set 1 nodo o PBM [GATED decisión topológica]
`ID` WP-A2b · `objetivo` cerrar el único hueco de RPO 1h · `ejecutor` Backup/DR con gate · `dependencias` decisión owner de topología (bloqueante #6 del master plan); 019 · `operaciones` convertir standalone→replica set 1 nodo (o instalar PBM); oplog tail continuo→staging · `riesgo` ALTO para un sistema trading en PROD: cambio topológico; requiere plan de reversión y ventana dedicada · `gate` OWNER explícito (no se propone por defecto; alternativa aceptada: mantener RPO 24h con dumps) · `validación` oplog tail + PITR drill Mongo · `rollback` volver a standalone desde dump+snapshot zvol previo · `DoD` decisión ejecutada y RPO medido, o decisión documentada de mantener 24h.

### WP-A3 — CouchDB 116 dump (vault LiveSync)
`ID` WP-A3 · `objetivo` dump consistente del CouchDB del vault · `ejecutor` Backup/DR · `dependencias` WP-A0 · `operaciones` CouchDB ya corre en LXC 116 con acceso por canal autorizado (R1 protege el vault exportado; aquí dump de la BD viva `_all_dbs` replicator); diario + ingesta PBS · `riesgo` bajo (lectura replicator/HTTP local) · `gate` ninguno si canal existente lo permite; si requiere credencial nueva → bundle puntual · `validación` restore a CouchDB scratch + conteo de docs vs live · `rollback` desactivar timer · `DoD` dump diario VERIFIED + 1 drill.

### WP-A4 — MinIO semanal + decisión versioning (parte gated)
`ID` WP-A4 · `objetivo` proteger artefactos SQX con historia · `ejecutor` Backup/DR · `dependencias` WP-A1 (infra del timer) · `operaciones` parte gated (NO parte en AUTO): activar el stream G1B semanal — requiere el MISMO gate owner de recurrencia MinIO definido en WP-A1 (autorización one-shot G1B ≠ autorización de recurrencia); el resto del timer infra sí es parte de A1. Parte GATED adicional: activar bucket versioning en producción MinIO (mutación en servicio trading) · `riesgo` AUTO bajo; versioning = medio (cambio en servicio vivo) · `gate` versioning: OWNER · `validación` snapshot semanal VERIFY_TASK_OK; con versioning: restore de versión anterior de 1 objeto · `rollback` timers off; versioning se desactiva por bucket · `DoD` semanal VERIFIED 2 ciclos; versioning ejecutado o deuda registrada.

### WP-A5 — Compose/config de CTs docker + mcps + PBS config
`ID` WP-A5 · `objetivo` configs de 126/129/141/127/128/158/142/113/180 bajo R1 · `ejecutor` Backup/DR · `dependencias` WP-A0 · `operaciones` exportar compose/env/units (sin secretos en claro: referencias) de cada CT/docker host + `/etc/proxmox-backup-*` de PBS 180; semanal · `riesgo` bajo · `gate` ninguno (lectura) · `validación` restore scratch de 1 compose + sha manifests · `rollback` timers off · `DoD` unidad config nueva VERIFIED para 9 targets.

### WP-A6 — pool0: snapshots + replicación selectiva pool0→pool2 + scrub pool2 [REPL inicial en ventana]
`ID` WP-A6 · `objetivo` rollback local (snapshots) + 2ª copia local de datasets seleccionados · `ejecutor` Backup/DR con gate TrueNAS · `dependencias` decisión owner de datasets (bloqueante #7 — default propuesto: `home`, `proxmox_storage`, `apps/*/config`, `iscsi` zvols T0, `aranea_storage` semanal; `trading_documents` = adición OPCIONAL sujeta a recálculo de capacidad: con él el set ≈2,2T > 2,15T libres de pool2, sin margen — S-02 auditoría; exclusión frigate media); 019 para full inicial · `operaciones` snapshot schedules sanoid/nativo (horario zvols T0, diario datasets); replicación local TrueNAS push→`pool2/pool0_new/` (dataset NUEVO; F-09 intacto); `zfs send -n` dry-run antes; scrub pool2 (read-only, seguro) · `riesgo` I/O del full inicial (~1,1-1,6T) en ventana; snapshots = espacio controlado con retención corta · `gate` OWNER: selección datasets + ventana full inicial; scrub pool2 (read-only): ejecución en ventana (§4/019 — I/O masiva sobre chasis hades) · `validación` recv de dataset de prueba + drill rollback de 1 zvol desde snapshot · `rollback` STOP + desactivar schedules y replicación; RECOVERY: recv inverso o restore PBS según el objeto afectado; destruir dataset nuevo requiere CLEANUP con autorización separada, objeto exacto identificado y verificación previa de que ningún restore lo necesita · `DoD` snapshots activos + 1º full REPL VERIFIED + scrub pool2 0 errores.

### WP-A7 — Off-site crítico restic→pCloud [gates 020/021]
`ID` WP-A7 · `objetivo` 3ª copia fuera del homelab (configs + dumps + claves custodia) · `ejecutor` Backup/DR · `dependencias` 020 (Secret Zero) + 021 (OAuth) · `operaciones` restic repo cifrado en pCloud; push semanal desde staging+PBS export; drill de descarga+descifrado · `riesgo` bajo técnico; OAuth/credenciales = superficie sensible · `gate` OWNER 020+021 · `validación` 1 snapshot VERIFIED offsite + drill descarga/restauración · `rollback` revocar token · `recovery` restaurar desde PBS (escenario DR-T1); reactivar timers · `DoD` off-site crítico VERIFIED (3-2-1 cumple para configs/dumps). **Operación obligatoria: incluir copia cifrada de `r0d-g1a.key` + `r0d-g1b.key` (o su escrow dentro de Secret Zero 020) en el primer push — sin ellas los snapshots PBS y el propio off-site son irrecuperables ante pérdida de kronos (DR-T6/DR-T3).**

### WP-A8 — Off-site bulk GDrive (chunked pool0 + PBS crítico) [gates 020/021]
`ID` WP-A8 · `objetivo` sobrevivir pérdida total de datasets pool0 · `ejecutor` Backup/DR · `dependencias` A7; 020+021; decisión de qué datasets van a bulk · `operaciones` rclone crypt chunked mensual de datasets irremplazables + export cifrado del datastore PBS (crítico) · `riesgo` cuotas/tiempos de carga GDrive; primer full largo (sin ventana: es push, no I/O local significativo) · `gate` OWNER 020+021 · `validación` 1 chunk VERIFIED + drill recv · `rollback` desactivar timers/rclone (revocar token si procede; el borrado del remote es CLEANUP con autorización separada) · `DoD` bulk VERIFIED (3-2-1 cumple para pool0 selectivo).

## Bloque B — Plataforma de backup, edge y observabilidad

### WP-B1 — vzdump T0 producción (post-piloto R2) [gates 018/019/D]
`ID` WP-B1 · `objetivo` cobertura imagen-level de Tier 0 · `ejecutor` Backup/DR · `dependencias` decisión D-piloto (28sep, retención final) + 018 (lista definitiva) + 019 (ventana inicial) + crecimiento datastore (D3) · `operaciones` jobs vzdump diarios 02:00 T0 (o split para no solapar con dumps), semanal T1/T2; exclusiones §6.3 diseño; retención según D; verify jobs PBS · `riesgo` I/O de full backups sobre hades (MT4/echo: idle nocturno UNKNOWN — la serie R2 mide otros CTs; limitar bandwidth y ventanas; el horario aprobado para vzdump de guests de trading lo fija el owner al aprobar D/019 — S-07); datastore debe crecer ANTES · `gate` OWNER (D + 018 + 019) · `validación` 7 días VERIFIED + restore drill de 1 VM T0 completa · `rollback` desactivar jobs (piloto/demostrado reversible) · `DoD` vzdump diario T0 VERIFIED+AUTOMATED.

### WP-B2 — Config exports edge/infra + decisión CA
`ID` WP-B2 · `objetivo` OPNsense/TrueNAS/pi-hole/PBS config bajo protección; resolver CA 200 · `ejecutor` Backup/DR · `dependencias` gap de acceso: OPNsense API/backup + TrueNAS API key (H1 tiene WS DDP — verificar si export config requiere bundle) + pi-hole token FTL6 · `operaciones` export config OPNsense semanal; export config TrueNAS via API (unidad nueva); pi-hole: resolver estado del servicio (.149 L2-dead) con owner y luego proteger; CA 200: ejecutar decisión owner (reactivar+backup claves o retiro formal) · `riesgo` bajo · `gate` pi-hole/CA: decisión owner; resto AUTO si canal existe · `validación` restore/reimport de config en laboratorio o scratch · `rollback` timers off · `DoD` 3-4 unidades config nuevas VERIFIED + decisión CA documentada.

### WP-B3 — Observabilidad de backups en ARGUS (R6)
`ID` WP-B3 · `objetivo` backup silencioso = backup roto · `ejecutor` Backup/DR vía management path · `dependencias` A1/B1 corriendo · `operaciones` señales: edad de último backup por unidad, VERIFY tasks PBS, espacio datastore, timers failed; alertas mínimas policy (diseño §8) · `riesgo` bajo · `gate` ninguno (RO) · `validación` disparo real de 1 alerta en test · `rollback` quitar dashboards/reglas · `DoD` alertas activas + test de disparo PASS.

### WP-B4 — Runbook canónico + closeout (R8)
`ID` WP-B4 · `objetivo` operación reproducible por tercero · `ejecutor` Backup/DR · `dependencias` A0-B3 · `operaciones` consolidar `BACKUP-DR-RUNBOOK.md` (restore procedures por unidad) + checklists; cerrar workloads con change logs (ap-08) · `riesgo` bajo · `gate` validación owner del runbook · `validación` un agente fresco ejecuta 1 restore guiado por runbook · `DoD` runbook validado + checklists 1 ciclo.

## Bloque S — Ceph/Storage (ejecutor CEPH, NO Backup/DR)

### WP-S1 — Inventario + liberaciones gated + riesgo LUN2
`ID` WP-S1 · `objetivo` aliviar pool1 con higiene segura · `ejecutor` Ceph/Storage · `dependencias` decisión dueño 112/162/170 + decomisión 100/151 (018) · `operaciones` liberar imagen RBD huérfana 120G (lock stale) y discos 162/170 si dueño confirma — **identificación exacta por VMID + evidencia de propiedad (sin snapshot/volume refs vivos) + snapshot/conservación previa donde sea posible; ninguna liberación en la misma operación que un restore; borrado = autorización independiente y posterior al éxito verificado del WP**; resolver double-attach LUN2 (100 vs 151) antes de cualquier start; documentar fichas de disco (política alta §7 assessment) · `riesgo` medio (borrar discos = irreversible → confirmación dueño por VMID, no por nombre) · `gate` OWNER + ventana · `validación` freed GB medidos + `rbd ls` post; HEALTH sin cambios negativos · `rollback` snapshots previos de los discos a liberar donde sea posible; sino: lista de exclusión definitiva · `DoD` +140-190G lógicos liberados o decisión documentada de no liberar.

### WP-S2 — mClock balanced + compact osd.0/2 [ventana]
`ID` WP-S2 · `objetivo` quitar perfil recovery-prioritario permanente y fragmentación · `ejecutor` Ceph/Storage · `dependencias` 019; medición antes/después · `operaciones` `ceph config` global mClock→balanced + recovery_sleep>0; bluestore compact osd.0/2; métricas osd perf pre/post · `riesgo` bajo-medio (I/O temporal del compact) · `gate` OWNER ventana · `validación` HEALTH igual o mejor; latencia osd.0/2 medida antes/después · `rollback` revert config Ceph (no destructiva) · `DoD` perfil balanced activo + compact hecho + métricas registradas.

### WP-S3 — Decisión estructura pool1 (alternativa F/G)
`ID` WP-S3 · `objetivo` resolver la causa estructural (FD host + 1 OSD/host) sin capex · `ejecutor` Ceph/Storage + owner · `dependencias` S1/S2; inventario SATA sin montar hera/zeus (200G×2, 32G×2, 100G) · `operaciones` evaluar OSDs adicionales de discos existentes (clases mixtas, margen corto) vs mover SOs fuera de pool1 (estratégico) vs mantener con riesgo documentado · `riesgo` por diseño; sin capex (F-01) · `gate` OWNER (decisión estructural) · `validación` simulación CRUSH + margen post-cambio · `rollback` remover OSD añadido / revertir pesos · `DoD` decisión estructural registrada con números o F-01 revisado explícitamente.

### WP-S4 — Instrumentación de latencia Ceph (cerrar NOT_PROVEN)
`ID` WP-S4 · `objetivo` medir p95 y correlate con recoveries · `ejecutor` Ceph/Storage · `dependencias` ninguna (RO) · `operaciones` exporter de métricas osd perf/slow-ops → ARGUS (observabilidad RO existente) · `riesgo` ninguno · `gate` ninguno · `validación` series visibles 7d · `rollback` quitar exporter · `DoD` evidencia futura de lag medible.

### WP-R7 — Drills recurrentes + certificación (R7)
`ID` WP-R7 · `objetivo` cada unidad T0/T1 con drill PASS reciente (<35d); procedimientos DR ejecutados · `ejecutor` Backup/DR · `dependencias` A0/A1 (drills DR-T1/DR-T4 posibles en cuanto A0/A1 estén activos), resto según off-site/ventanas · `operaciones` ejecutar drills DR-T1..T6 según ROADMAP bloque DR; certificar estados por unidad (§14 mandato R0); calendario recurrente post-B1 · `riesgo` bajo (targets scratch) · `gate` ninguno para drills scratch; ventana para DR-T5 · `validación` cada drill PASS con evidencia en change log · `rollback` borrar targets scratch · `DoD` unidad T0/T1 sin drill fresco = 0.

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
                                 └→ A4 (MinIO semanal, GATED)
EN PARALELO (owner decide):     018 · 019 · 020 · 021 · D-piloto · Mongo topología · datasets REPL · CA
DESPUÉS DE GATES:               B1 (vzdump producción) · A2 (PITR ventana) · A6 (snap+REPL ventana) · B2
CARRIL CEPH (otro ejecutor):    S4 (ya) → S1 (dueño) → S2 (ventana) → S3 (decisión)
CONTINUO:                       B3 (observabilidad, tras A1/B1) · WP-R7 drills · B4 al final
```

Precedencia estricta: B1 requiere D-piloto + 018 + crecimiento datastore; A2 requiere A1+019; A6-full requiere 019; S2 requiere 019; nada del bloque S toca Backup/DR y viceversa.

## Riesgo priorizado (reducción de riesgo global, no "terminar DBs primero")

1. A7/A8+020 (elimina pérdida total) → 2. A0+A1 (protección deja de envejecer) → 3. A6 (rollback local pool0) → 4. B1 (cobertura imagen T0) → 5. S1/S2 (salud Ceph) → 6. B2 (edge/DR prerrequisitos) → 7. resto.

## Clasificación final de WPs (validación 2026-09-20, post-correcciones C1-C6)

> Un estado por WP. READY = precondiciones verificadas + autorización identificada + mecanismo demostrado + rollback/validación completos. OWNER_GATE especifica exactamente qué autoriza. Nada aquí ejecuta ni declara ejecutado.

> [!warning] Errata 21sep — dependencia D-piloto ↔ serie R2
> El run R2 del 21sep 06:05 no ocurrió (hermes apagada 01:09→07:36; catch-up ejecutó A1/R1/R1.5 pero el trigger absoluto de R2 expiró dentro del apagado). La serie queda **3/7 NO consecutiva** y el criterio original "7/7 días con verify ok" es **inalcanzable** antes de la expiración del 26sep. La decisión D (gated al owner) debe resolverse explícitamente con el criterio alternativo ya definido en `~/aranea/work/first-window-20260926/MANDATO-P0.md`: **6/7 runs OK + OK owner con CAPACITY-METRICS re-medidas 25-26sep** — o el owner difiere D, y con ella B1 y el crecimiento +300G (D3), a su calendario original (28sep). Esta errata NO cambia la clasificación de los WPs; cambia la precondición factual de B1.

**READY_TO_EXECUTE (en el instante en que el owner apruebe el plan — esa aprobación ES la autorización de recurrencia PG/Mongo):**
- **WP-A0-AUTO** (ingesta staging→PBS + inventario nfs-storage + round-trip) — mecanismo G1A demostrado; sin ventana.
- **WP-A1** para PG/Mongo (timers 03:00-03:45; rollback = timers off; R2/R1 intactos por diseño de horarios).
- **WP-A3** (CouchDB dump; canal replicator existente; drill scratch).
- **WP-A5** (exports config 9 targets; lectura).
- **WP-S4** (instrumentación RO Ceph→ARGUS; sin mutación) — carril Ceph, ejecutor propio.
- **WP-R7 parcial** (DR-T4 MinIO desde G1B; DR-T1 fase CT a scratch — fase VM post-B1) — desbloquea al completar A0/A1 primer ciclo.

**OWNER_GATE (qué autoriza exactamente):**
- **A0-gated**: editar prune nfs-storage en 5 × storage.cfg (diff exacto por nodo, post-inventario).
- **A1/A4**: stream recurrente semanal de MinIO (ADD no aprobado, regla 4.1/018); A4 versioning (mutación servicio trading).
- **A2**: ventana 019 + archive_mode en PG PROD trading. · **A2b**: topología Mongo (o deudas aceptada RPO 24h).
- **A6**: selección datasets + full inicial REPL en ventana 019.
- **A7**: tickets 020+021 (y define escrow de claves r0d — operación obligatoria del WP). · **A8**: ídem + selección bulk.
- **B1**: decisión D-piloto + 018 + 019 + crecimiento +300G datastore (fase 1 gated).
- **B2 parcial**: pi-hole (retiro/reactivación + token FTL6) y CA 200 (reactivar vs retiro).
- **S1**: liberación por VMID (112/162/170, RBD 120G) — autorización independiente de borrado. · **S2**: ventana compact/mClock. · **S3**: decisión estructural pool1.

**DEFER (válido, bloqueado por ventana/dependencia — no requiere decisión hoy):**
- **A8 full inicial** (tras A7; push largo). · **B3** (tras A1/B1 corriendo). · **WP-R7 recurrente completo + DR-T2/T3/T5/T6 drills** (según ventanas/off-site). · **B4** (cierre, tras A0-B3). · **2º target PBS→pool2** (opcional post-B1). · **MP-04 A2b si owner mantiene RPO 24h** (queda deuda documentada, no bloqueo). · **Scrub pool2** (read-only pero I/O masiva ~5T sobre chasis hades → en ventana §4/019; B-01 de la auditoría: NO es inmediato).

**BLOCKED_TECHNICAL (falta evidencia de acceso/ejecutabilidad):**
- **B2 exports OPNsense** (canal API/backup no verificado) y **export config TrueNAS** (factibilidad vía API/SSH por confirmar; WS DDP existe pero el método de export no está probado) → verificar canal o bundle; mientras, sin ejecutor definido.
- **Datos kafka (scsi1) y argus (scsi1-4)**: valor/retención UNKNOWN → resuelve 018; sin dato no hay mecanismo ejecutable.

**Camino crítico**: aprobación del plan → MP-01 (A0/A1/A3/A5) ∥ (018/019/020/021/D owner en paralelo) → A6/B1/A2 tras gates → A7 en cuanto 020/021 (riesgo #1). Paralelizable sin interferencia: carril Ceph S4/S1-S3 ∥ carril Backup/DR; A3/A5 ∥ A1; B2-diagnóstico ∥ todo lo anterior.

---

## Redirección owner 21sep noche — WPs actualizados y operaciones obsoletas retiradas

> Autoridad: D-NEW-01..06 ([[MASTER-PLAN-STORAGE-BACKUP-DR]] §7). Las entradas contradictorias de los bloques A/B anteriores quedan así modificadas; el histórico no se borra.

| WP | Estado nuevo | Cambio |
|---|---|---|
| WP-A6 (snapshots + REPL pool0→pool2 + scrub) | **REEEMPLAZADO por [[POOL0-TO-POOL2-REPLICATION-SPEC]] + [[MANDATO-REPLICACION-SPEC]]** | alcance ya NO selectivo: TODO pool0, incremental diario, gates G-REP-1..4; scrub pool2 pasa a pre-requisito G-REP-1 |
| WP-B1 (vzdump producción) | VIGENTE + ampliación | exclusión ledger de [[TWO-LAYER-BACKUP-SPEC]] §1; añade capa semanal `nfs-vmbackup` (pool1→pool0, gate G-NFSVM) |
| W1/W2 dentro de P0-2 (FIRST-MAINTENANCE-WINDOW) | **RETIRADAS** | P0-2 obsoleto; la ventana 26sep queda: prechecks → K2 → K1 → P0-1 (según W-01/gates) |
| Alta `nfs-pool2` (W-03 §1 del paquete miércoles) | **OBSOLETA** | sin consumidor tras cancelación W1/W2 |
| 2º target PBS→pool2 (DEFER de esta clasificación) | **CANCELADA** | contradice D-NEW-01 |
| WP-A2/A2b/A3/A4/A5/A7/A8 | VIGENTES sin cambios | deudas y gates ídem; prioridad cloud ahora explícita (D-NEW-05) en A7 |
| WP-B2 | VIGENTE | TrueNAS config export gana prioridad (requisito DR-T5 de la SPEC de réplica §6.5) |
| WP-B3/B4/R7/S1-S4 | VIGENTES sin cambios | — |

**Orden actualizado (consistente con esta redirección):** AHORA (AUTO): A0→A1∥(A3,A5,S4,R7-parcial) · TRAS GATES OWNER: B1(D+018+019) → G-NFSVM (capa pool1→pool0) · RÉPLICA: G-REP-1 (scrub pool2) → G-REP-2/3 (full inicial en ventana propia) → G-REP-4 (schedule diario) — I/O de réplica JAMÁS simultáneo con B1-fulls/G1B/migraciones · CLOUD: A7 en cuanto 020/021 · CARRIL CEPH: S4→S1→S2→S3 sin cambios.
