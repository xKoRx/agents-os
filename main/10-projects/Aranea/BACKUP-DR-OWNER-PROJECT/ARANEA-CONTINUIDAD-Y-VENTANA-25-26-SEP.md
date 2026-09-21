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
