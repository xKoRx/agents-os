---
type: doc
schema_version: 1
status: active
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[BACKUP-DR-OWNER-PROJECT]]"
  - "[[FIRST-MAINTENANCE-WINDOW-20260920]]"
  - "[[K2-CEPH-RISK-20260920]]"
  - "[[OPERATING-STATE-20260920]]"
aliases:
  - ARANEA — Continuidad y ventana 25-26 sep
  - Continuidad Aranea 2026-09-21
tags:
  - kind/doc
  - area/aranea
  - domain/backup-dr
created: "2026-09-21"
updated: "2026-09-21"
---

# ARANEA — CONTINUIDAD Y VENTANA 25-26 SEP

## Delta sesión lun 21 noche-6 — CIERRE PREPARATORIO BACKUP/DR (21sep 22:26-23:0x -03)

**Mandato owner ONE-SHOT** (cierre preparatorio reutilizando el estado noche-5; sin re-inventario ni re-arquitectura; cero cambios productivos). Ejecutado: sonda runtime RO completa + preparación ejecutable + congelación 018 + medición `rbd du` completa. **Entregable central: `~/aranea/work/cierre-preparatorio-20260921/PAQUETE-EJECUCION-25-26SEP.md`** (bloques READY / READY_AFTER_OWNER_GATE / GATED-owner-pendiente / DEFER con dependencias exactas — insumo directo del freeze T-24). Otros: `018-MATRIZ-COBERTURA.md` (matriz VM+datos; ticket 018 congelado a 3 decisiones owner: firma lista + argus datos + kafka datos — respuesta 1 línea) · `RBD-DU-RESULTADOS-20260921.md` + `raw/` (sondas + rbd du completo). Hallazgos verificados esta noche:

- **Ceph 86,56/86,60% a las 22:39** (K2 NO disparada). Ritmo vespertino ≈1,8G/OSD/h en sesión US (08:05 85,2 → 22:39 86,6): margen a backfillfull ≈31,7G/OSD = **18-80h** → **riesgo nuevo: la condición K2 (≥89% ×2 ≥1h) puede disparar ANTES del viernes** → protocolo desde mié 22: 2 lecturas separadas ≥1h (`sudo ceph -c /etc/pve/ceph.conf osd df`), escalar owner si se cumple (acción gated `qm shutdown 125`).
- **162 y 170 YA ESTÁN LIBERADAS**: el owner ejecutó ambos `qmdestroy` (root@pam) el 20sep 23:58 -03 (tasks OK verificados en kronos/zeus; configs ausentes; RBDs ausentes de pool1). Toda la doc del 21sep las mantenía DEFER por derivar de inventarios 19-20sep. **Sólo queda la liberación 112** (guest stopped kronos; RBD huérfana 5,9G — alivio marginal). Huérfanas vigentes 108/112/123/167/171 = 200G prov / **46,9G usados**.
- **`rbd du` COMPLETO ejecutado** (48 imágenes, canal `sudo rbd -c /etc/pve/ceph.conf` validado contra vm-159=93G): **1.503G prov / 848G usados reales**. Alivio real: fase 1 W5-post ≈164G usados (echo+MT4+DB-SOs); escenario máximo con autorizaciones ≈572G. 127/106/141 LLENOS al prov → fichas W5-post prioritarias. Nunca prometer prov: contabilizar sólo `rbd du` post-liberación verificado.
- **W-01 re-validado live**: pool-kronos VFree **733,87G**; VM 180 scsi1 serial `pbs-data` 300G; PBS 295G/18% ext4 → opción (b) ejecutable al exacto. **Errata hades local-lvm ≈20,5G libres** (el 33,4G del freeze era el USADO del thinpool; regla restauración local en hades: VM ≤12G dejando ≥8G) — corregida en [[CAPACITY-AND-RESERVATIONS]] §5.
- **T-21b verificado SIN aplicar** (tar directo en `r1-backup.sh`; second-brain FAIL 2º día en manifest 20260921-073644) → orden W-02 correcto: D3 primero, run R1 3/3, recién entonces standby.
- **Frontera de seguridad verificada (no tocar)**: whitelist del guest PG es `command=` (sólo rsync por clave efímera) — la query Echo de 0 posiciones corre por el canal W-04 (dump de posiciones), NO por SSH directo al guest; no ampliar ese whitelist.
- Resto verde: quórum 5/5, 124/125 running, snapshots A1 vigentes (PG `2026-09-21T10:37:57Z`), hermes sin apagados desde 07:36, timers 6 vivos, R2 expira 26sep (último disparo ese día). Tickets 018-021 intactos (018 con su congelación documental). Cambios vault: erratas en [[CAPACITY-AND-RESERVATIONS]] y [[ANALISIS-DISCO-POR-DISCO]]; bitácora/status_detail proyecto; change log `2026-09-21-cierre-preparatorio-backup-dr`. Cero mutaciones de infra; Echo operando.

## Delta sesión lun 21 noche-5 — MANDATO CORRECTIVO "BACKUP FIRST" (21sep ~21:00-22:30 -03)

**Mandato owner ONE-SHOT**: corregir la dependencia revocada y completar el análisis; cero cambios productivos. Ejecutado 100% documental (RO sobre evidencia existente + parches). Hallazgos y entregables:

- **Dependencia REVOCADA eliminada de todos los documentos vivos**: `STORAGE_ORGANIZATION_COMPLETE → activar Backup/DR` ya NO existe como requisito en STORAGE-ORGANIZATION-FREEZE (redefinido: cierra la optimización de storage), Master Plan (errata noche-5), Placement §F, Ventana §8.2 DAG, Continuidad E6, Roadmap, status_detail del proyecto, TABLA-APROBACION-23SEP y MANDATO-JUEVES-24 (erratas en workspaces). Secuencia aprobada: (1) optimización — planificación completa desde ahora; (2) Backup/DR — sobre placement actual; (3) migraciones — después, protegidas por backups verificados; (4) recertificación post-migración. Reglas fijas: **STORAGE_OPTIMIZATION_PLANNED no es requisito de BACKUP_BASELINE_VERIFIED; BACKUP_BASELINE_VERIFIED por unidad SÍ es requisito de su MIGRATION_READY.** Backups certificados vigentes NO se detienen. La 1ª réplica de pool0 se dimensiona/ejecuta cuando SUS gates G-REP-0..5 estén satisfechos (no depende de migraciones).
- **[[ANALISIS-DISCO-POR-DISCO]] (NUEVO)** — mandato §2: 99 discos reales clasificados (59 guests; derivado programáticamente de `guest-disk-map.json` + evidence/05 PROV + rbd-du2 used; 0 filas sin clasificar): KEEP/KEEP-F04 57 · MIGRATE W5-post 21 (773G techo) · DEFER 13 (340G) · RECONFIGURE 1 (staging 50G) · UNKNOWN 7 (kafka scsi1 ×3 = 0 ahorro Ceph; argus scsi1-4 = mayor palanca 72G usados). +5 imágenes RBD huérfanas/residuales 200G (112-disk-0 120G, 108/123 residuales, 167/171 sin guest) → techo nominal 1363G; **alivio real proyectado 150-350G** (thin: se libera used, no prov; sólo 13/33 discos con used medido). Conclusión: el freno del growth de pool1 (+17G/OSD/día ≈ +51G lógico/día) supera a cualquier migración — K2/P1-4 primero; W5-post es alivio gradual. Única investigación pendiente para cerrar el 100%: los UNKNOWN de §6 (todos con 0-72G de impacto y ninguna bloquea Backup/DR ni la fase 1 W5-post).
- **Capacidad por fases**: [[CAPACITY-AND-RESERVATIONS]] §7 — Fase 0 baseline (BACKUP_BASELINE_VERIFIED alcanzable COMPLETO sin migrar; pool2 ≥1,71T margen; PBS 295G→595G W-01) · Fase 1 post-vm-backup (medir real → recién ahí fijar retención @repl; si vm-backup >1,03T recortar a 7d ANTES de activar) · Fase 2 post-migraciones (ahorro contabilizado sólo con `rbd du` post-liberación verificado).
- **Paquete viernes/sábado re-apuntado a Backup/DR como objetivo principal**: MANDATO-BACKUP-VMS §Operaciones con estado por bloque READY_AFTER_OWNER_GATE (B1, G-NFSVM, T-21b/W-02, réplica P6) / BLOCKED (A3, A7) / DEFER (W5-post) — ningún bloque se fuerza a PASS; MANDATO-BACKUP-DATOS con orden nocturno (T-21b/W-02 primero); T-24 usa los 4 estados; T-26 declara el objetivo principal; TABLA-APROBACION mantiene P1/P4/P6 como urgentes de primera línea.
- Archivos: 11 en vault (los listados arriba + mandatos 2/5/datos + capacidad + roadmap) · 2 en workspace (`TABLA-APROBACION-23SEP.md`, `MANDATO-JUEVES-24.md`) · 1 nuevo ([[ANALISIS-DISCO-POR-DISCO]]) · change log `80-agents/journal/change-logs/2026-09-21-backup-first-correccion.md`. **Cero mutaciones de infraestructura; Echo operando.**

## Delta sesión lun 21 noche-4 — STORAGE-ORGANIZATION-FREEZE (mandato "Placement Freeze antes de Backup/DR")

**Mandato owner ONE-SHOT** (organizar recursos ANTES de Backup/DR; NO iniciar respaldos/replicaciones/migraciones). Ejecutado documental sobre las fuentes canónicas ya congeladas noche-2/noche-3 (sin re-investigar, sin re-inventariar los 59). Entregables E1-E8:

- **E1** mapa actual/objetivo: derivable de [[MATRIZ-59-GUESTS-BACKUP]] + [[POOL0-TO-POOL2-REPLICATION-SPEC]] §1 ledger (no se duplica). **E2** [[PLACEMENT-DECISIONS-20260920]] **§F PLACEMENT-FREEZE-V2**: KEEP por workload (PG/Mongo/MinIO datos=críticos vs SO=reconstruible como unidades distintas; Echo+MT4; edge CTs; traefik; etcd; SQX F-04; OPNsense/TrueNAS/CA) · DEFER (W5 reevaluación por VM post-réplica; W4 KEEP hasta causalidad P1-4; W3=D5 función, no migración; 100/151/112/162/170) · **MIGRATE activas: NINGUNA** · pool2 RESERVADO réplica exclusiva.
- **E3** [[CAPACITY-AND-RESERVATIONS]]: presupuesto pool2 (4,08T free; +2,35T réplica → margen ≥1,71T) · pool0 (free 1,64T; vm-backup 0,43-1,03T + @repl 0,27-1,09T → margen combinado ACOTADO; orden: medir vm-backup real → fijar retención final) · pool1 (banda 85,2-87,9%, cero asignaciones nuevas) · PBS (+300G vía 2º disco pool-kronos 733,87G, opción recomendada W-01) · local-lvm (hades 33,4G / zeus 77,5G / hera 91,7G). Doble-asignación eliminada (errata de la propia nota aplicada en el mismo acto).
- **E4** plan de ejecución consolidado: [[FIRST-MAINTENANCE-WINDOW-20260920]] §8.2 — DAG organización; **viernes 25 = MIGRATIONS_NOT_READY** (sin operaciones inventadas para el calendario); sábado 26 = prechecks→K2→K1 (PENDIENTE_GO owner)→P0-1, **sin P0-2**; 1ª réplica en ventana EXCLUSIVA G-REP-3; I/O TrueNAS nunca compartido.
- **E5** runbooks: por operación autorizable ya existen (mandatos 2-6 + MANDATO-P0-v2 + W-01..W-04 + payloads réplica); corrección aplicada en [[MANDATO-MIGRACIONES-SPEC]] (fila W1/W2 estaba en imperativo, contradiciendo su CANCELADA).
- **E6** [[STORAGE-ORGANIZATION-FREEZE]]: gate **`STORAGE_ORGANIZATION_COMPLETE`** con 9 criterios — **corregido noche-5 (mandato BACKUP FIRST): NO es requisito de Backup/DR** (dependencia revocada por el owner); cierra la optimización de storage. Backup/DR avanza por sus propios gates (G-B1/G-NFSVM/G-REP-0..5); **BACKUP_BASELINE_VERIFIED por unidad es el requisito de su MIGRATION_READY**; los backups certificados no se detienen. Preparación e implementación de Backup/DR en paralelo desde ya.
- **E7** decisiones owner: tabla única `~/aranea/work/continuity-20260923/TABLA-APROBACION-23SEP.md` — urgentes **P1 (W-01) · P4 (D-piloto 6/7 criterio alternativo) · P6 (réplica G-REP-0..5)** · T=018/020/021 · P2 (T-21b+W-02) · P3 sin objeto · P5 pi-hole.
- **E8**: proyecto actualizado (bitácora + status_detail + tarea T-23a DONE), change log `80-agents/journal/change-logs/2026-09-21-hardening-replicacion-noche3.md`, mandatos anteriores corregidos. **Cero mutaciones de infraestructura; Echo operando.**

## Delta sesión lun 21 noche-3 — HARDENING FINAL DE STORAGE Y REPLICACIÓN (ONE-SHOT auditor)

**Mandato owner ONE-SHOT "Hardening final de storage y replicación"**: corregir SÓLO los bloqueantes materiales del SPEC freeze; cero cambios productivos. Ejecutado íntegro en modo RO (SSH ariadna@truenas + midclt + código instalado) + parches documentales. Hallazgos y correcciones:

- **"API 404" refutada**: `/api/v2.0/replication` sin auth = **401 (ruta existente)**; el middleware expone `replication.*`, `pool.snapshottask.*`, `cronjob.*`; el código instalado declara `transport ∈ {SSH, SSH+NETCAT, LOCAL}` (replication.py:763). → **Mecanismo definitivo: stack NATIVO zettarepl LOCAL** (snapshottask recursivo 04:45 + replication PUSH LOCAL 04:50; payload exacto en workspace); el cron+zfs de la noche-2 queda DESCARTADO. `replication.query=[]` y 0 cron jobs: faltaba crear la tarea, no la API.
- **Envío inicial real = 2,35T base `refer`** (no 2,57T): apps 67,4G→14,1G e iscsi 539G→381G en refer (bloques compartidos con snapshots legacy + zvols thin con refreservation ≫ refer; pg_data usados 33G vs refer 1,25G). Ledger de cobertura 100% auditado (SPEC §1): `.ix-virt` = ISOs + volumen Docker SIN apps (`app.query`=0); `.system` = remanente (dataset real en `boot-pool/.system`).
- **Discrepancia 4,08T zpool vs 2,15T datasets resuelta**: NO es doble conteo por orígenes borrados — es histéresis `usedbychildren` (442 snapshots legacy de `pool2/backup` con used≈0; 2,05T; el AVAIL de la vista convergerá al borrarlos — decisión owner separada). **CAPACITY_GO certificado por aritmética**: 2,35-2,37T ≤ 4,08T free → margen post-full ≥1,71T (24%); steady-state con retención 14d: 1,0-1,4T libres. pool0 ídem corregido: 945G dataset-view → **1,64T zpool**; réplica + capa vm-backup (pool1→pool0) caben con margen combinado acotado → orden recomendado: medir `pool0/vm-backup` real y después fijar retención final @repl (7 vs 14d).
- **Erratas materiales**: había 1 snapshottask legacy (id=1 → `pool0/vm_storage/hades-cdfezs`, dataset inexistente, estado HOLD) — "0 periodic-snapshot tasks" era falso; `pool0_scrub` NO existe (era hipótesis no verificada) → **`pool.scrub` nativo operativo** para la tarea mensual de pool2; `pool2/pool0_backup` opera `sync=always` (HDD; fixture probará `properties=false`/override); SMTP sin configurar (`smtp=false`) → canal de alertas nativas = gate nuevo **G-REP-5**.
- **Horario 04:45/04:50 re-fundado con dependencias reales** (timers hermes verificados: A1 03:00/03:20 · R1 04:00 · etcd 05:00 · R2 06:05 expira 26sep sin conflicto) — no por inercia; el full inicial va en ventana exclusiva propia (G-REP-3).
- **Viernes reconciliado (§5)**: **MIGRATIONS_NOT_READY** — ninguna migración con ficha completa pasa al sábado; W5 = reevaluación por VM post-activación de la réplica (NUNCA simultánea con fulls); W4=KEEP hasta causalidad P1-4; W3=D5. Independientes el sábado: K2, K1, P0-1 (gates propios). Bloqueadas por R2: B1 y todo vzdump de producción. Bloqueadas por off-site: A7/A8 (3-2-1 NO declarado).
- **Gates G-REP-0..5** (nuevos: G-REP-0 fixture `pool2/fixrep` autodestruido + G-REP-5 alertas) · payloads en `~/aranea/work/replicacion-pool0-pool2/` · fila **P6** añadida a TABLA-APROBACION-23SEP (urgente junto a P1/P4; P3 sin objeto).

## Delta sesión lun 21 noche-2 — REDIRECCIÓN OWNER D-NEW-01..06: SPEC freeze (21sep ~17:30-18:30 -03)

**Mandato owner ONE-SHOT "Storage Architecture + Backup/DR · Rediseño dirigido y SPEC Freeze"**: actualizar arquitectura con las decisiones D-NEW-01..06 y congelar SPECs — SIN implementar nada productivo. Ejecutado íntegro en modo documental + sondas RO (API TrueNAS v2.0 + SSH ariadna@truenas + storage.cfg vía ariadna@pve). **Cero mutaciones de infraestructura; Echo operando.**

- **Decisiones owner registradas** ([[MASTER-PLAN-STORAGE-BACKUP-DR]] §7): pool2 = EXCLUSIVAMENTE réplica diaria de todo pool0 (W1/W2 CANCELADAS; sin alta nfs-pool2; P0-2 retirado de la ventana 26) · pool0 = datos productivos + snapshots locales + espacio para respaldos recuperables de workloads de pool1 · pool1 = NO_GO vigente · DOS mecanismos no intercambiables (VM/LXC completo en PBS + datos consistentes) · cloud por prioridad (PG/Mongo→CouchDB→MinIO→configs→Secret Zero externo; 3-2-1 NO declarado sin A7) · backups SIN dependencia de Hermes.
- **Flujos congelados**: POOL1→backup recuperable en POOL0 · POOL0→snapshots→incremental DIARIO→POOL2 · DATOS CRÍTICOS→cifrado→CLOUD · PBS independiente para VMs.
- **Erratas materiales de capacidad medidas esta sesión** (API+SSH, 21sep noche): pool2 **4,08T libres a nivel zpool** (7,27T size/3,19T alloc; la vista `zfs list` AVAIL 2,15T subestima por doble conteo de snapshots legacy; sin quotas) → **todo pool0 (2,59T) SÍ cabe con ~1,5T de margen**; el "4,18T" del freeze del martes queda corregido a 4,08T (mismo orden, conclusión sin cambio); pool0 scrub OK 6sep; **pool2 SIN scrub desde jul-2025 y sin tarea programada** (única tarea id=3 apunta a pool0) → G-REP-1; sin periodic-snapshot tasks; endpoints API `/replication` y `/pool/periodic-snapshot/task` = 404 en 25.04.1 → activación por cron+script zfs.
- **Entregables nuevos**: [[POOL0-TO-POOL2-REPLICATION-SPEC]] (inventario 2,57T a enviar, capacidad, 04:45 incremental único diario, consistencia por workload, vida HDD, recuperación 5 escenarios, gates G-REP-1..4) · [[TWO-LAYER-BACKUP-SPEC]] (mecanismo A vzdump/PBS + exclusión ledger + capa `nfs-vmbackup` pool1→pool0; mecanismo B matriz por servicio con deudas; MinIO "última copia" = verificable, rotación ≥2 certificadas) · 6 mandatos `MANDATO-{PREP,BACKUP-VMS,BACKUP-DATOS,REPLICACION,MIGRACIONES,CERTIFICACION}-SPEC.md` (reemplazan el alcance obsoleto del paquete W-03; W-01/W-02/W-04 del paquete del miércoles siguen VIGENTES) · Runbook evergreen `30-resources/aranea/03-storage/zfs-replication-runbook.md`.
- **Ventana 26sep REDUCIDA**: queda prechecks → K2 → K1 → P0-1 (W-01 según gates D1+P1-1+019). P0-2/W1/W2 retirados. TABLA-APROBACION-23SEP: filas P3/P4 mantienen su formato pero P3 ya NO autoriza nfs-pool2 (queda sin objeto; decisión que queda abierta para el owner = aceptar cancelación); urgentes para el sábado: P1 (PBS growth) y P4 (D-piloto). **T-24 (jueves 24) congela el paquete REDIRIGIDO, no el v2 original.**
- Cambios a Placement/Roadmap: [[PLACEMENT-DECISIONS-20260920]] §D (cancelaciones y recolocación) · [[ROADMAP-WP-BACKUP-DR]] §Redirección. Change log: `80-agents/journal/logs/2026-09-21-redireccion-storage-backup-dr.md`.

## Delta sesión lun 21 noche — T-23 ADELANTADO: paquete de mandatos del miércoles (21sep 15:54-16:20 -03)

**Mandato owner ONE-SHOT**: paquete ejecutable para 25-26sep sin decisiones técnicas investigables pendientes. Cero mutaciones de infraestructura (Echo operando; R2 no anticipado). Entregado en `~/aranea/work/continuity-20260923/`: **W-01** (PBS growth: (a) grow ≤250G / **(b) 2º disco VG pool-kronos 733,87G — recomendada** / (c) diferir; reemplaza el +300G inviable), **W-02** (protección autónoma: standby PBS 180 con especificación cerrada — 4 timers espejo, ConditionPathExists flag manual, Persistent=false, credencial custodiada, staging >3d, prueba negativa, rollback trivial; T-21b ordenado ANTES porque el standby hereda el script corregido; 4 gates owner; ejecución post-cierre Echo del viernes, fuera de ventana), **W-03** (§0 justificación workload W1/W2 sobre pool2 single-disk: separación de dominio de falla, NO redundancia — con opción DEFER clasificada como decisión owner · §1 alta nfs-pool2 · §2 P0-2 por CT 103→116→137→113→115 · §3 W5 placement por VM: PG→zeus 77,5G, Mongo→hera 91,7G, MinIO→zeus/hera, Echo→hades sólo si cabe con ≥8G libres, MT4s condicionados, kafka excluido · §4 W3: 149 en ATHENA + L2-dead → migración RETIRADA de la ventana, decisión D5 primero), **W-04** (preflight T-25: 10 checks fail-closed con GO/NO_GO POR intervención + cierre Echo por dump G1A sin filtro temporal + criterio de vuelta a normal), **MANDATO-P0-v2** (reemplaza al borrador 20sep, queda ARCHIVADO; tabla de cambios v1→v2 con 8 correcciones trazables), **TABLA-APROBACION-23SEP** (única tabla de decisión owner: Operación/beneficio/riesgo/impacto/decisión/consecuencia de NO aprobar; códigos en 1 línea; urgentes P1/P3/P4; una aprobación general NO sustituye gates específicos), **MANDATO-JUEVES-24** (freeze: READY/DEFER por mandato). Canónico en vault: [[MANDATOS-MIERCOLES-23SEP]]. Índice M-W actualizado en `WEDNESDAY-MANDATES-INDEX.md`. R2 sigue limitado a 6/7; nada se anticipa de sus 5 disparos restantes. Siguiente paso: owner responde tabla (o bundle D1-D8) → T-24 congela → T-25 preflight+cierre Echo.

> [!info] Punto de entrada único para la próxima sesión (comprensible sin acceso a la conversación del 21sep). El vault local es la ÚNICA autoridad. El handoff `ARANEA-HANDOFF-2026-09-20.md` citado por el mandato NO existe en la máquina ni en el vault (verificado en adjuntos, journal y `~/aranea/work/` al 2026-09-21 08:00 -03); su contenido relevante ya está canónico en las notas enlazadas. NO repetir investigación cerrada: Master Plan, matriz 59/59, placement, ventana, K2, assessment Ceph 19sep, G1A/G1B, MP-01, R2 y WP-A7 están cerrados y documentados — leer, no re-derivar.

## Resumen ejecutivo (2026-09-21 08:00 -03)

- Aranea opera normal: Echo sano en producción, quórum PVE 5/5, TrueNAS pools ONLINE, PBS con backups verificados, 6 timers de backup activos. Sin incidentes abiertos.
- La semana 21-25sep es PREPARACIÓN (sin mutaciones de infraestructura); la intervención P0 va el sábado 26sep 02:00-07:00, sujeta a 3 gates owner (ventana 019, OK D-piloto, alta storage `nfs-pool2`).
- Cambio mayor post-cierre (21sep): **hermes (118) estuvo APAGADA 01:09→07:36** (apagado limpio; causa no registrada en su journal — el agente despertó con el host ya iniciado). Consecuencias: A1 ejecutó su 2º ciclo en catch-up 07:36 y queda **VERIFIED** (cierre de la observación del 20sep); **el run R2 del 21sep 06:05 NO ocurrió** → la serie queda en 3/7 días con verify ok y **la decisión D-piloto ya no puede afirmar "7/7 consecutivos"** — el owner decide con la evidencia real; el mandato P0 BORRADOR ya declara explícitamente el criterio alternativo (6/7 + OK owner con métricas 25sep).
- El run R1 de hoy **falló parcial** (second-brain: `tar: main: file changed as we read it` — el vault cambia mientras se empaqueta; el fallo es recurrente en fundamento aunque hoy es la primera evidencia en journal). traefik-config y hermes-state OK. Fix en tarea T-21b; no bloquea la semana.

## Estado real por evidencia (fecha de medición, no de escritura)

| Evidencia | Estado | Medida | Fuente canónica |
|---|---|---|---|
| MP-01 A0/A5 | DONE | 20sep | Bitácora proyecto + change logs `2026-09-20-mp01-*` |
| MP-01 A1 dumps PG/Mongo | DONE — 2º ciclo verificado en PBS (`2026-09-21T10:37:57Z`/`10:37:21Z`, catch-up 07:36 por reinicio de hermes) | 21sep | PBS `host/r0d-{postgresql,mongodb}` + timers activos |
| R2 piloto vzdump | PARTIAL — 3/7 días con verify ok; run 21sep NO ocurrió (host apagado 06:05); expira 26sep | 21sep | timer `aranea-r2-measure` + datastore `ct/` |
| R1 config backup | PARTIAL hoy — traefik OK, second-brain FAIL (tar race), hermes-state OK | 21sep 07:36 | `~/aranea/backup-staging/20260921-073644/` |
| R1.5 etcd/pve-config | DONE (etcd catch-up OK 07:36; pve-config semanal sáb) | 21sep | journal hermes |
| G1A (PG/Mongo) | DONE cerrado — cadena completa certificada, claves custodiadas, plaintexts purgados | 20sep | [[BACKUP-DR-KEY-RECOVERY]] |
| G1B (MinIO) | DONE cerrado — OBJECT_COPY_PASS + FULL_DR_PASS; versioning OFF = deuda gated | 20sep | RUN-G1B + bitácora |
| WP-A7 off-site | PARTIAL — paquete Secret Zero cifrado PASS con demo clean-room; **SIN copia fuera de Aranea** (pCloud bloqueado por gates 020/021) | 20sep | `~/aranea/work/a7-offsite-20260920/` |
| K2 Ceph | Ejecutado 20sep: SAFE_TO_DEFER **con condición de alerta** (no garantiza el futuro); re-verificar al planificar la ventana | 20sep 21:57 | [[K2-CEPH-RISK-20260920]] |
| Ceph pool1 | HEALTH_WARN; 85,19/85,17% el 21sep 08:05 (4º swing de la banda 85,6-87,9); sin slow ops en esa lectura | 21sep 08:05 | [[K2-CEPH-RISK-20260920]] §Evidencia |
| VM 125 mt4-test | RUNNING en **hades** desde 20sep 18:54:44 (`qmstart:125` OK en índice de tareas); disco `pool1:vm-125-disk-1,cache=unsafe` 48,3/50G; principal escritor de la ráfaga | 21sep | [[K2-CEPH-RISK-20260920]] + pmxcfs |
| VM 114 mt4-test | STOPPED en **kronos** (114≠125; coexisten; la premisa "125 no existe" quedó refutada por evidencia viva) | 21sep | `/cluster/resources` |
| 132 docker-monitoreo | STOPPED en hera — sin decisión formal (regularizar en 018) | 21sep | [[OPERATING-STATE-20260920]] |
| Echo 140 | SANO en operación (24 sesiones bridge + core, 0 rechazos 24h al 20sep 21:36; hubo sesión de trading el domingo) | 20sep | [[OPERATING-STATE-20260920]] |
| mcps 113 | rootfs 85% (8,9G cache reclamable); 26/26 containers up | 20sep | [[OPERATING-STATE-20260920]] |
| pi-hole 149 / CA 200 | L2-dead / stopped — decisiones owner pendientes (WP-B2) | 20sep | [[OPERATING-STATE-20260920]] |

## Delta sesión lun 21 tarde-2 — CONGELACIÓN para el martes 22 (medido 17:02-17:11Z)

**Congelamiento ejecutado** (mandato `~/aranea/work/continuity-20260921/MANDATO-MARTES-22.md`, read-only, cero mutaciones; Echo operando): workspace `~/aranea/work/continuity-20260922/` → `CAPACITY-FREEZE.md` (números fechados), `PLACEMENT-FREEZE.md` (W1-W5/PBS/Ceph toda PENDIENTE_DECISIÓN, ninguna DECIDIDA), `BUNDLE-DECISIONES-MARTES.md` (D1-D8 con opciones/evidencia/impacto/rollback), `WEDNESDAY-MANDATES-INDEX.md` (borrador de mandatos del miércoles), `raw/` (sondas RO). El martes sólo registra decisiones del owner y redirige al cronograma.

**Serie R2 al cierre del 21**: 1 OK de 3 disparos posibles (19 skip fuera de ventana; 20 OK 6/6+verify; 21 perdido por apagado); quedan 5 disparos (22-26) → D-A tolerancia CERO. Próximo disparo: mar 22 06:05 (requiere hermes encendida). Protección del día: A1 2º ciclo VERIFIED (PG `2026-09-21T10:37:57Z` + Mongo `10:37:21Z`, ambos verify TASK OK); R1 second-brain **FAIL 2º día consecutivo** (tar-race; T-21b sigue gated); etcd OK (rev 58563).

**4 erratas materiales medidas hoy** (no bloquean decisiones; refinan mandatos): (1) VG `local-kronos` VFree real = **267,5G** (el 567,5G del baseline era pre-creación del disco pbs-data de 300G) → el `+300G` de MANDATO-P0 §P0-1 no es ejecutable tal cual; opciones: grow ≤250G / 2º disco en VG `pool-kronos` (VFree 733,9G) / diferir — se pide junto a D1. (2) hades local-lvm **33,4G libres** < los ~64G de W5 → reparto por VM (zeus 77,5G / hera 91,7G) o alcance reducido en T-23. (3) pi-hole 149 corre en **athena** (no hades como decía la ficha W3) → el argumento "sobrevivir a hades" cae; decisión = reactivar+proteger vs retiro. (4) pool2 **4,18T libres** (holgura; decisión W1 no cambia).

**K2 del día**: osd.0/2 **85,55/85,57%** (17:10:51Z), HEALTH_WARN + slow ops BlueStore (2 OSD); fondo hoy ≈ +0,37G/h; **condición de alerta NO disparada** (margen ~32G/OSD a 89%). Canal verificado: `pvesh /nodes/<nodo>/ceph/osd` (el `sudo ceph` de hades falla sin `-c /etc/pve/ceph.conf` — feedback registrado). Lectura 2 del día: **85,59/85,59% a las 17:31:17Z** — sin condición de alerta; ambas lecturas congeladas en el freeze.

**mcps 113**: rootfs 88% / 2,4G libres / 26 containers (17:06Z vía mcps-ops) — estable; prune sigue en P1. ping 149: 100% loss (17:07Z) — L2-dead persiste.

## Delta sesión lun 21 tarde — medido 09:27-09:50Z (post-cierre documental de la mañana)

**Serie R2 certificada con evidencia dura** (runlog driver + journal hermes + PBS): first_run=**20sep**
(el 19 NO ejecutó: 2 intentos manuales 12:11/12:13 -03 fuera de ventana 06:00-07:30 → skip "día
perdido"; run-20260919.jsonl); 20sep ciclo completo 6/6 CTs rc=0 + verify TASK OK 09:08:05Z
(snapshots ct/* 09:05-09:08Z en PBS, listado verificado); 21sep perdido por apagado de hermes (timer
**non-Persistent por diseño**: journal "día perdido = día perdido"). Quedan 5 disparos (22-26).
**Serie máxima 6/7 → D-A con tolerancia CERO; un día más perdido = sólo D-B.** Errata aplicada en
`~/aranea/work/first-window-20260926/MANDATO-P0.md` (§6/§7 se leen "6/7").

**Desacoplamiento Hermes (E2, WP-HD staged)**: inventario verificado — los 6 jobs de protección viven
TODOS en hermes (5 timers Persistent=true con catch-up demostrado; R2 non-Persistent por diseño).
Candidatos verificados: PBS 180 up 2d11h (ya ejecuta ingesta A1/A0; datastore 232G libres), daedalus
up 4d14h. Propuesta gated: **ejecutor standby = PBS 180 con timers espejo ConditionPathExists +
Persistent=false, flag manual ACTIVE** (activar en la rutina de apagado, desactivar al arrancar) —
sin auto-activación, sin catch-up retroactivo (regla: no reponer después de 09:00 en día de mercado).
No ejecutar: 3 gates owner (diseño, credencial, ejecución) — `~/aranea/work/continuity-20260921/E2-WP-HERMES-DECOUPLING.md`.

**T-21b empaquetado**: diff exacto preparado y probado con fixture aislado (escritor concurrente:
staging atómico 4/4 rc=0 tar íntegro; tar directo 3/4 rc=1 por race; prueba negativa sin falso PASS;
dry-run de patch limpio). OWNER_GATE mantiene — `~/aranea/work/continuity-20260921/T21B-R1-TAR-RACE-FIX.diff`
(+ `T21B-FIX-TEST.sh`; aplicar/rollback documentados en el header del diff).

**Deltas del día vs tabla de la mañana**: pi-hole 149 — PVE lo lista **RUNNING** pero sigue L2-dead
(ICMP 100% loss 09:36; W3/B2 sin cambio real); mcps 113 rootfs **88%** (subió desde 85%; 2,4G libres;
prune gated → añadir a P1); Ceph osd.0/2 **85,20/85,23%** (banda estable, sin condición de alerta;
slow ops BlueStore aún listadas en health; 135 op/s wr fondo); Echo **1 posición abierta** verificada
09:44 -03 vía canal dump propio (protección G1A intacta; mercado activo → cero intervenciones); A7
payload 288M **≈264M** vs 16G libres de daedalus (baseline corregida — push viable); Prometheus no
está expuesto como servicio HTTP consultable desde hermes (160:9090/127:9090 cerrados) — el precheck
Echo de la ventana usa el canal dump de posiciones, no métricas.

**E1 — estado del lunes (por componente, medido hoy)**: A1 **PASS** (2º ciclo VERIFIED en PBS —
histórico, no nuevo hoy); R1 **PARTIAL** (traefik+hermes-state OK; second-brain FAIL tar-race → diff
listo gated); CouchDB/A3 **BLOCKED** (sólo credencial owner `_reader` desbloquea; bundle A3 vigente);
R2 **PARTIAL** (serie certificada arriba); desacoplamiento **DEFER a gates** (diseño listo); Ceph
**STABLE-WARN** (85,2%, alerta no disparada); Echo **SANO en operación** (1 posición abierta, sin
rechazos); W1-W5 **sin cambios** (matriz del martes en E4-E5 staged); MANDATO-MARTES-22 **READY** en
`~/aranea/work/continuity-20260921/MANDATO-MARTES-22.md`.



- **DONE:** R0, D0, R1 (mecanismo), R1.5, R2-discovery, G1A (+custodia+purga), G1B, MP-01 (A0/A1/A5; A3 SKIP con bundle), Master Plan + 2 validaciones adversariales, matriz 59/59, placement, ventana P0 diseñada, mandato P0 borrador.
- **PARTIAL:** R2 (3/7 días válidos; run 21sep perdido), A7 (sin off-site real aún), R1 (fallo tar de hoy pendiente de fix), A3 (SKIP con bundle de desbloqueo).
- **OWNER_GATE:** ventana 019, D-piloto (retención final + producción vzdump), alta `nfs-pool2`, tickets 018-021, topología Mongo, datasets REPL, CA 200, pi-hole, liberaciones 112/162/170 (borrado = autorización independiente por VMID), prune nfs-storage, MinIO recurrente/versioning, pCloud (autorizar acceso), purga `~/.ssh/r0d_ephemeral*` + `probe/p.txt`.
- **DEFER:** A8 full, B3, R7 completo, B4, 2º target PBS→pool2, W2-W5 (ventanas siguientes), P1-1..P1-5, P2-1..P2-4.

## Decisiones vigentes (no re-abrir)

- F-01..F-14 congelados (F-01 sin capex, F-04 SQX intocable, F-09 `pool0_backup` preservado, F-13/F-14 SPOF aceptados).
- D1 placement PG/Mongo/MinIO KEEP_JUSTIFIED — NO migrar; el dato T0 vive en zvol pool0, fuera de Ceph.
- NO_GO escribir en pool1 (nearfull estructural probado; banda 85,6-87,9% con ráfaga-recesión; full_ratio 0,95).
- W1/W2 a pool2 son PROPUESTAS con ficha, no destinos aprobados; pool2 es single-disk y comparte chasis con pool0 (F-14) — su valor es separar dominio de falla del SO edge, no redundancia.
- `nfs-storage` (pool0) INTOCADO en P0-2: sólo un storage nuevo `nfs-pool2` recibe los 4 rootfs (protege ide0 de MT4 PROD, labs e ISOs).
- `pct move-volume` elimina el volumen origen; la conservación del origen es el vzdump previo verificado — `--delete` jamás autorizado por defecto.
- K2: sin intervención, con condición de alerta única (≥89% ×2 lecturas ≥1h) y acción preparada gated (`qm shutdown 125`); SAFE_TO_DEFER del 20sep NO garantiza el futuro.
- Carriles separados: Backup/DR (Ariadna) ≠ Ceph/Storage (ejecutor propio, MP-07) ≠ trading (intocable: ni Echo ni MT4 ni credenciales ni riesgo).
- R2 corre exactamente como está hasta expirar el 26sep; 148 excluido permanente; horarios R1/R1.5/A1 intocables.

## Cronograma lun 21 → sáb 26 sep (carriles en paralelo sin mutaciones concurrentes)

| Día | Backup/DR (Ariadna) | Ceph/Storage | Echo/operación |
|---|---|---|---|
| Lun 21 | Reconciliación documental (esta sesión) + fix R1 tar (T-21b) | — | cierres operativos del día |
| Mar 22 | Decisiones de placement/capacidad listas para el owner (bloqueantes 5/7/10 en una página) | — | — |
| Mié 23 | Paquete completo de backups en borrador: jobs vzdump B1 (lista 018), exclusiones, retención propuesta, diseño jobs — sin activar | — | — |
| Jue 24 | Freeze del paquete de ejecución: permisos, rollback, bundle owner único | — | — |
| Vie 25 | Preflight GO/NO_GO (métricas D re-medidas; `ceph osd df`; verify PBS); **cierre operativo real de Echo** — comprobar 0 posiciones abiertas + prevenir nuevas entradas (comprobación con el criterio GO/NO_GO de abajo, no supuesto) | — | cierre Echo |
| Sáb 26 | **VENTANA 02:00-07:00** (si gates OK): K2-check → K1 → P0-1 (D+PBS+300G) → P0-2 (4 CTs a `nfs-pool2`) según mandato | — | sin sesión |

Paralelizables sin riesgo: carril documental/prep de Backup/DR ∥ diagnóstico kafka P1-4 (RO) ∥ operación Echo. Nunca simultáneo: TrueNAS/pool0 (A6 ∥ W1), Ceph (W5 ∥ S2), edge (W2 aislado).

## Primer mandato seguro para el agente siguiente

1. Bootstrap Agents-OS + router Aranea (`30-resources/agents/skills/aranea-agent-dev/SKILL.md`); leer esta nota, [[BACKUP-DR-OWNER-PROJECT]] (bitácora), [[FIRST-MAINTENANCE-WINDOW-20260920]] y [[K2-CEPH-RISK-20260920]].
2. Verificar delta runtime (read-only): `ceph osd df` (¿≥89% en 2 lecturas separadas ≥1h? → condición de alerta K2), timers de hermes, `/cluster/resources`, último run R2 (expira 26sep), staging de R1 (¿fix tar aplicado?).
3. Ejecutar SOLO la tarea del día del cronograma; nada GATED sin OK owner explícito y registrado; **prohibido**: backups/migraciones/reinicios/cambios Ceph/TrueNAS/PBS/scrub/borrados fuera de la ventana autorizada.
4. Si el owner entrega los gates: ejecutar la ventana con `~/aranea/work/first-window-20260926/MANDATO-P0.md` (borrador vigente; prechecks §5 antes de cada intervención; ABORT según su regla 3; una mutación a la vez).

## Rutas

- Proyecto: `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/` — bitácora y gates en [[BACKUP-DR-OWNER-PROJECT]]; tickets 018-021 en `10-projects/Aranea/05-tickets/`.
- Documentos técnicos: [[MASTER-PLAN-STORAGE-BACKUP-DR]] · [[MATRIZ-59-GUESTS-BACKUP]] · [[ROADMAP-WP-BACKUP-DR]] · [[MANDATOS-IMPLEMENTACION-BACKUP-DR]] · [[OPERATING-STATE-20260920]] · [[PLACEMENT-DECISIONS-20260920]] · [[FIRST-MAINTENANCE-WINDOW-20260920]] · [[K2-CEPH-RISK-20260920]] · [[BACKUP-DR-KEY-RECOVERY]].
- Evidencia en `~/aranea/work/` (hermes): `operating-state-20260920/`, `k2-ceph-risk-20260920/`, `first-window-20260926/` (MANDATO-P0), `master-plan-20260920/` (CAPACITY-METRICS), `weekend-gate-01-20260919/` (G1A/G1B), `mp01-20260920/`, `a7-offsite-20260920/`, `r2-pbs-20260918/`.
- Recursos evergreen: `30-resources/aranea/03-storage/backup-dr/` ([[BACKUP-DR-RUNBOOK]], [[BACKUP-DR-CHECKLIST]], BACKUP-DR-DESIGN congelado); runbooks Ceph/operación: `30-resources/runbooks/ceph-storage-operations-contract.md` + `cluster-node-maintenance-contract.md`.

## Condiciones GO/NO_GO

- **Ceph (pre-ventana):** osd.0/osd.2 ≥89% en 2 lecturas separadas ≥1h, o HEALTH lista `OSD_BACKFILLFULL`/`OSD_FULL`, o latencia commit ≥500ms sostenida >1h con sesiones Echo activas → escalar owner (acción preparada gated: `qm shutdown 125`; alternativas en [[K2-CEPH-RISK-20260920]]). Banda histórica 85,6-87,9% con retrocesos confirmados = NO accionar por una sola lectura ni por anticipación.
- **Echo (ventana):** precheck `SELECT count(*) FROM echo.trade_journal WHERE closed_at IS NULL;` = 0 (SIN filtro temporal) + sin sesiones activas; si hay posición/sesión → ABORT de P0-1/P0-2 (la ventana continúa sólo con K2/K1). El cierre operativo del viernes 25 se comprueba con este criterio + prevención de nuevas entradas (acción del owner sobre su plataforma; el agente verifica y registra, no la ejecuta).
- **PBS:** verify main TASK OK en precheck + datastore <70% antes de P0-1; el run R2 06:05 del sábado es el último por expiración natural (validar su OK, no renovar el timer).

## Gate vigente de autorización (21sep noche — reemplaza TABLA-APROBACION-23SEP)

Autorización PUNTUAL por operación (owner, sin aprobaciones generales): instrumento único
`~/aranea/work/cierre-preparatorio-20260921/GATE-AUTORIZACION-PUNTUAL-22SEP.md` — contiene
P1 (W-01 → `qm set 180 -scsi2`, errata scsi1 corregida), P2a (T-21b aplicar; hash base
bca1d148…, sin aplicar), W-02 a/b/c separados (depende P2a), P4=D-B baseline (D-A sólo con
6/7 + métricas 25sep + dependencia apagado nocturno resuelta), P6=G-REP-0..5 sin ninguno
aprobado, ticket 018 con las 3 decisiones exactas (ticket NO se cierra con UNKNOWN), 020/021
pendientes owner, K2 protocolo MARTES 22 (2 lecturas ≥1h; 21sep 22:39 = 86,56/86,60%).
Erratas corregidas esta noche: P0-1 slot `-scsi1`→`-scsi2` (scsi1 = datastore pbs-data vivo);
"miércoles 22"→martes 22; 112 = 5,9G usados reales (no 120G) en CAPACITY/MANDATOS;
162/170 eliminadas del universo en MATRIZ/CAPACITY/MANDATOS con marcadores de corrección.
