---
type: doc
schema_version: 1
status: active
icon: 📡
slug: aranea-operating-state-20260920
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[MATRIZ-59-GUESTS-BACKUP]]"
  - "[[PLACEMENT-DECISIONS-20260920]]"
  - "[[FIRST-MAINTENANCE-WINDOW-20260920]]"
  - "[[MASTER-PLAN-STORAGE-BACKUP-DR]]"
aliases:
  - Operating State 2026-09-20
  - Estado operativo Aranea 2026-09-20
tags:
  - kind/doc
  - area/aranea
  - domain/backup-dr
created: "2026-09-20"
updated: "2026-09-21"
---

# 📡 OPERATING-STATE — 2026-09-20

## Propósito

- Estado operativo real de Aranea medido en vivo el 2026-09-20 ~20:00-21:30 -03 (read-only, sin mutaciones), reconciliado contra [[MATRIZ-59-GUESTS-BACKUP]]. Actualiza la columna "Estado" de la matriz; las decisiones siguen en [[PLACEMENT-DECISIONS-20260920]] y la ventana en [[FIRST-MAINTENANCE-WINDOW-20260920]].
- **Esta nota es un HISTORICAL SNAPSHOT del 20sep** (así lo fechó su medición): el estado corriente vive en el bloque CURRENT 21sep de abajo y en [[ARANEA-CONTINUIDAD-Y-VENTANA-25-26-SEP]]. Las métricas y citas del 20sep se preservan tal como se midieron (no se falsifican retroactivamente); las correcciones se hacen por erratas marcadas.

## Método y límites

- Fuentes: `/cluster/resources` vía ariadna@athena (única sesión SSH a PVE), `ceph -s`/`ceph osd df` vía ariadna@hera, PBS vía ariadna@pbs, TrueNAS vía API WebSocket DDP con api-key existente, métricas `echo_*` y health de datasources vía MCP observabilidad RO (ARGUS, VM 160), PG 152 vía MCP postgres RO, hermes local (timers, DNS), mcps vía management path `mcps-ops` (sudo read-only).
- NO leído por dentro: guests sin canal RO autorizado (Echo 140, MT4s, kafka-hera/kronos/zeus, MinIO filesystem interno, TrueNAS zvol internals, CouchDB 116). `running`/`stopped` = estado PVE; `RUNNING` no implica aplicación sana salvo donde hay evidencia de aplicación (Echo, PG, ARGUS, MinIO :9000, mcps docker).

## Resumen

- **59/59 guests reconciliados: 43 RUNNING / 16 STOPPED.** 43/43 running con uptime ≥42d salvo 118 (1d, reinicio planificado por R2) y 113 mcps (12d). Quórum PVE 5/5, nodos online 5/5 (uptime 42d). Stop drain del clúster = 5 nodos reiniciados juntos (~18sep 01:30), patrón consistente con corte eléctrico general; sin UPS (gap H5 conocido).
- **Echo sano y EN OPERACIÓN a las 21:36 -03 (domingo): 24 sesiones de bridge vivas** (17 ejecución + 7 referencia) + gauge agregado de sesiones core, 0 rechazos/fallos de intents en 24h, ~4,88M mensajes pipe/24h, rate máximo de latencia de hop ~18ms/s, frescura de métricas 27s (scrape vivo). Los bridges reportan un **brote de errores Kafka** (ver hallazgos).
- **Ceph: nearfull EMPEORÓ de forma material desde el assessment 19-09**: osd.0/2 al **87,8%** (818/932 GiB; 19sep: 799G/85,7%) y **2 OSD con slow ops BlueStore** (hallazgo nuevo). Growth ≈ +17G/OSD lleno en ~27h. HEALTH_WARN (nearfull + slow ops).
- **Backups: 6 timers activos y verificados hoy** (A1 03:00/03:20, R1 04:00, R1.5 05:00, R2 06:05, pve semanal sáb). PBS al 16% (48G/295G), verify tasks OK en archive, 6 CTs piloto + 12 snapshots host presentes.
- **TrueNAS vivo**: pool0 y pool2 ONLINE y healthy (DDP, 2026-09-20 20:07), uptime SO 42d.

## Matriz operativa 59/59 (delta contra MATRIZ-59-GUESTS-BACKUP del mismo día)

- Convención: `RUNNING`/`STOPPED` = observado en PVE hoy. `DEGRADED` = función degradada con evidencia (servicio caído o condición de salud negativa). `UNKNOWN` = sin canal de verificación de aplicación. La lista completa por VMID con nodo y backend sigue en la MATRIZ; aquí sólo desvíos, degradados y hallazgos.

### Correcciones a la matriz documental (drift)

| VMID | Nombre | Matriz decía | Runtime 20sep | Clasificación |
|---|---|---|---|---|
| 132 | docker-monitoreo | running | **STOPPED** (hera) | Intencional-desconocido: stopped sin registro de decisión. Sin consumo y sin impacto observado en ARGUS (160 sirve las métricas). Requiere decisión: formalizar retiro o devolver a running |
| 125 | mt4-test | stopped | **RUNNING** (hades; iniciada 20-09 18:54:44 — errata 21sep: el "up 42d" era del nodo hades, no del guest; verificación pmxcfs en [[K2-CEPH-RISK-20260920]]) | Intencional probable: terminal de prueba encendido manualmente el 20sep. Sin canal de inspección; sin evidencia de daño. Requiere regularizar en 018; es el escritor identificado de la ráfaga Ceph |

### Degradados (con evidencia)

| Unidad | Estado | Evidencia | Acción |
|---|---|---|---|
| pi-hole (149) | DEGRADED (L2-dead crónico) | ICMP 192.168.31.149 100% loss desde hermes 20sep; ARP FAILED (R1.5) | sin resolver por diseño (gated): token + decisión retiro/reactivación (WP-B2) |
| ca (200) | STOPPED intencional | consistente con decisión pendiente owner (reactivar vs retiro) | WP-B2 |
| 112/162/170, 100/151 | STOPPED DEFER | latentes LUN2 double-attach + RBD 120G huérfana (assessment E3) | WP-S1 gated dueño |

### Edge y red

| Servicio | Evidencia 20sep | Estado |
|---|---|---|
| OPNsense (130) | gateway vivo por implicación (DNS resuelve, subredes alcanzables, bridges MT4 conectados a brokers) — sin acceso directo | OPERACIONAL (indirecto), UNKNOWN detalle |
| traefik (115) | HTTPS :443 responde (404 en / sin host); certificado vigente en uso por channels de métricas y MCPs | RUNNING saludable |
| DNS hermes | resolv.conf a systemd-resolved local, resolución OK durante toda la sesión | OK |
| tailscale | cliente ausente en hermes (host del agente, esperado; gateway 119 arriba en PVE) | n/a |

### Hallazgos operativos del día (ordenados por riesgo)

1. **CRÍTICO — Ceph nearfull acelerando + slow ops nuevos.** osd.0/2: 87,82/87,78% (818G/932G) vs 85,7% el 19sep (~+17G/OSD/día). Los 2 OSD llenos además reportan slow operations BlueStore (nuevo vs assessment, que no tenía slow-ops). Escenarios del assessment siguen: caída de kronos = recovery imposible; NO_GO pool1 vigente. Márgenes por OSD lleno con ratios estándar (0,90/0,95): backfillfull ≈ 21G, full ≈ 67G — backfillfull en ~1 día si el growth no frena. ACCIÓN: identificar escritor de pool1 (ver PLACEMENT §Ceph) en la primera acción de la ventana; NO intervenir el cluster fuera del carril Ceph.
2. **ALTO — Brote Kafka en bridges Echo** (21:26-21:30 -03, durante esta medición): +147 errores/h "replica not the leader / metadata out of date" en mt4-real/ftmo/ttp, tras ~10h limpias. Efecto no observado en intents/trades (0 rechazos; los 2 trades del día se abrieron bien). docker-kafka (128, hera) arriba 42d; kafka-hera/kronos/zeus sin canal RO para revisar ISR. Hipótesis: churn de líderes en kafka (128 dev) o colisión con el I/O de Ceph nearfull. Monitorear; escalar a Echo/Forge si los errores continúan al cierre de mercado.
3. **MEDIO — mcps (113) rootfs 85% (17G/20G)** con ~8,5G reclamables (build cache 4,1G + imágenes colgantes 4,4G; total docker build cache = 8,9G con 4,1G reclaimable). Plano MCP sano (26/26 containers up), pero un rootfs lleno en el LXC de acceso degradaría el plano de acceso. `docker system prune` = mutación gated en ventana (requiere OK owner; afecta sólo cache/imágenes colgantes).
4. **MEDIO — Stop drain 18sep ~01:30** (todos los nodos/guests con uptime 42d, arrancando en ráfaga). Aceptado F-13 sin UPS; refuerza H5.
5. **BAJO — PBS tasks sqlite ausente** en la ruta documentada (tasks via archive); mecanismo funciona (verify OK en archive 20sep). Cosmético.
6. **BAJO — Drift documental 132/125** (tabla arriba).

## Detalle por dominio (verificado hoy)

- **PVE**: quorum 5/5 Quorate; nodos athena/hades/hera/kronos/zeus online 42d; hades al 22,6% CPU (79% RAM de 252G — esperado: aloja la flota), resto <1% CPU.
- **Ceph**: HEALTH_WARN; 4/4 OSD up/in; mon quorum hera/zeus/kronos; 129 PG active+clean; 857GiB datos; I/O en reposo 15MiB/s wr — **el growth de osd.0/2 no es I/O de clientes actual, es acumulación**; `rbd du` falló por sintaxis desde athena (client cap), no reintentado (limitación de método, no evidencia de cluster).
- **PBS (180)**: servicios active/active; datastore 48G/295G (17%, umbral 70% = 207G); `ct/` = 101,115,147,154,155,156 (6/6 piloto); `host/` = 12 grupos de snapshots (r0d-config-{r1,etcd,pve,mp01a5}, r0d-{postgresql,mongodb} con cadenas diarias 17:2x/17:3x del ciclo 1 A1, minio-* G1B, r0d-probe pendiente owner); archive 20sep: verify TASK OK recurrentes (main 14/14 previo, snapshots G1A OK).
- **Backups (timers hermes)**: aranea-r3-pg-dump 03:00 y aranea-r3-mongo-dump 03:20 armados (primer disparo lun 21sep 03:00); R1 04:00 corrió hoy OK; etcd-snap 05:00 OK; R2 06:05 corrió hoy: 6/6 CTs rc=0 (dur 13-39s), datastore 92G/189G según driver (métrica del driver; df dice 48G/295G — reconciliar en próxima ventana, probable compresión); pve-config sáb 08:30 OK.
- **PostgreSQL 152** (MCP RO): primaria (no recovery), up 9d (desde 11sep 10:00 UTC), 14 bases con allowconn, **archive_mode=off** (confirma WP-A2 pendiente), respuesta SQL inmediata.
- **Echo (métricas ARGUS)**: 25 series de sesión activa = 24 sesiones de bridge (17 ejecución {mt4-ttp 6, mt4-real 10, mt4-ftmo 2 — mt4-real incluye cuenta 80636976} + 7 referencia en mt4-demo) + 1 gauge agregado de sesiones core; 6 pipes ejecución + 7 referencia, core (140) con pipeline viva; trades/24h = 2 abiertos (cero fallos de journal); kafka_produced fluyendo. Versión bridge/core 2.0.0, deployment=production.
- **ARGUS (160)**: 3/3 datasources OK (Prometheus/Loki/Jaeger); scrape de servicios Echo fresco (27s); 865 series en namespaces de plataforma (kafka/ceph/pve/node) PERO 0 muestras — **instrumentación declarada sin scrapes vivos** (ver PLACEMENT).
- **mcps (113)**: 26/26 containers up (5d), rootfs 85% (hallazgo 3), build cache 8,9G (4,1G reclaimable).
- **TrueNAS (145/hades)**: pool0/pool2 ONLINE healthy (DDP); scrub pool2 sigue overdue (>14m, riesgo F-14 vigente, en ventana).

## CURRENT — seguimiento 2026-09-21 (lecturas RO 08:00-08:20 -03, cierre documental)

- **Backups**: catch-up de timers a las 07:36 tras apagado limpio de hermes 118 (01:09→07:36, causa no registrada). A1 2º ciclo **VERIFICADO en PBS** (`host/r0d-postgresql/2026-09-21T10:37:57Z`, `host/r0d-mongodb/2026-09-21T10:37:21Z`); etcd-snapshot OK; **R1 falló second-brain** (`tar: main: file changed as we read it`; traefik-config y hermes-state OK; manifest `~/aranea/backup-staging/20260921-073644/`) → corrección gated T-21b (diff al owner); **run R2 06:05 no ocurrió** → serie 3/7 NO consecutiva (decisión D con criterio alternativo 6/7+OK owner de MANDATO-P0).
- **Ceph**: osd.0/2 **85,19/85,17%** (794/793 GiB de 932; 08:05) — recesión completa del swing del 20sep (−24G vs techo 87,9%); HEALTH_WARN 2 nearfull osd + 2 pool nearfull; sin slow ops listadas en esta lectura. Condición de alerta K2 (≥89% ×2 lecturas ≥1h) sigue sin dispararse; banda histórica 85,6-87,9% con 4 swings en 4 días.
- **Guests verificados**: 125 mt4-test RUNNING hades (desde 20sep 18:54:44, cache=unsafe — escritor K2; premisa "125 no existe" refutada: 114 kronos stopped coexiste); 132 docker-monitoreo STOPPED hera (sin decisión); 118 agent RUNNING kronos (uptime 13min en la lectura); quórum 5/5.
- **Estado de la semana**: preparación 21-25sep sin mutaciones; ventana P0 sáb 26sep 02:00-07:00 pendiente de autorización (gates: ventana 019, OK D-piloto criterio alternativo, alta `nfs-pool2`). Fuente viva: [[ARANEA-CONTINUIDAD-Y-VENTANA-25-26-SEP]].

## Fuentes

- Evidencia cruda: `~/aranea/work/operating-state-20260920/` (pve-live.txt, ceph-live.txt, rbd-du2.txt, pbs-live.txt, truenas-query-20260920.json, runtime-guests.json).
- Referencias: [[MATRIZ-59-GUESTS-BACKUP]] (matriz 59/59 canónica), handoff assessment `~/aranea/work/storage-ceph-assessment-20260919/HANDOFF-2026-09-19.md` (baseline 19sep), métricas `~/aranea/work/master-plan-20260920/CAPACITY-METRICS.md`.
