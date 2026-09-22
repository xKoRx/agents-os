---
type: doc
schema_version: 1
status: active
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[MATRIZ-59-GUESTS-BACKUP]]"
  - "[[PLACEMENT-DECISIONS-20260920]]"
  - "[[MASTER-PLAN-STORAGE-BACKUP-DR]]"
  - "[[CAPACITY-AND-RESERVATIONS]]"
  - "[[TWO-LAYER-BACKUP-SPEC]]"
aliases:
  - ANALISIS-DISCO-POR-DISCO
  - Matriz disco por disco 59 guests
tags:
  - kind/doc
  - area/aranea
  - domain/backup-dr
  - project/backup-dr
created: "2026-09-21"
updated: "2026-09-21"
---

# 🔍 ANALISIS-DISCO-POR-DISCO — Optimización de storage (99 discos, 59 guests)

## Propósito

- Cumple el mandato correctivo owner "ARANEA · BACKUP FIRST" (21sep noche-5, §2): la clasificación KEEP por workload de [[PLACEMENT-DECISIONS-20260920]] §F NO satisface el análisis pedido — esta nota desciende a **disco por disco** (99 discos reales en los 59 guests, excluidos sólo los passthrough físicos de TrueNAS como unidades propias y los cdrom vacíos).
- **No investiga de nuevo**: cada fila deriva de evidencia ya medida (`guest-disk-map.json` 59/59 del assessment 19sep + `rbd du`/PROVSIZED 20sep + matrices canónicas). La clasificación aplica el placement v2 ya congelado; ningún KEEP temporal se convierte en KEEP definitivo sin análisis — los no analizados quedan UNKNOWN con su investigación asignada (§6), no KEEP.
- **Cero cambios productivos**: este documento no autoriza ninguna ejecución. Cada migración futura tiene su propio gate.

## Contenido

### 1. Reglas fijas del mandato (vinculantes)

1. **STORAGE_OPTIMIZATION_PLANNED no es requisito de BACKUP_BASELINE_VERIFIED** — Backup/DR se implementa y certifica sobre el placement actual.
2. **BACKUP_BASELINE_VERIFIED por unidad sí es requisito de su MIGRATION_READY** — ninguna migración sin su propia protección recuperable verificada (restore demostrado).
3. Los backups certificados vigentes (A1 PG/Mongo, R1/R1.5, R2 piloto, G1A/G1B) **no se detienen**.
4. W5-post: la reevaluación por VM corre **post-activación de la réplica y NUNCA simultánea con fulls** (réplica/B1/G1B); gate por VM.
5. Recertificación de cada servicio después de migrar ([[MANDATO-CERTIFICACION-SPEC]]).
6. La réplica inicial de pool0 se dimensiona y ejecuta sólo cuando SUS gates G-REP-0..5 (capacidad, integridad, ventana) estén satisfechos — sin depender de migraciones.

### 2. Resumen del análisis (99 discos)

| Decisión | Discos | Techo de liberación pool1 (prov) | Lectura |
|---|---|---|---|
| KEEP / KEEP-F04 | 57 | 0 | colocación correcta o F-04 intocable (SOs en nfs-storage/local-lvm/pool0, datos D1 en zvol pool0, SQX, PBS, firewall) |
| MIGRATE (W5-post) | 21 | 773G | SOs reconstruibles en pool1; orden: echo→MT4→DB-SOs→DEV; **alivio real = used, no prov** |
| DEFER | 13 | 340G | 125 (apagar = condición K2), labs/liberaciones 107/114/159/162/170 (290G con autorización de borrado por VMID), W3/D5, LUN2, decomisiones 100/151 |
| RECONFIGURE | 1 | 50G | staging hermes (118 scsi1): contenido regenerable tras ingesta A0; sin migración de VM |
| UNKNOWN | 7 | (ver §6) | kafka scsi1 ×3 y argus scsi1-4 → decisión 018 |

- **Techo agregado si TODAS las decisiones se ejecutaran: 1163G asignados + 200G en 5 imágenes RBD huérfanas (§5) = 1363G.**
- **Alivio REAL esperado (thin provisioning: se libera el used, no el prov)**: medido sólo en 13/33 discos pool1 (rbd du 20sep). Subconjunto medido: MIGRATE DB/temporal/etcd-keeper ≈41G · DEFER 159 = 93G · argus data ≈72G. Los ~20 discos MIGRATE sin medir (SOs 20-50G) proyectan 5-15G c/u → **rango realista 150-350G lógicos totales**, no el techo de 1,36T. `rbd du` completo + `qm config` por VM = preflight obligatorio de cada ficha W5-post. **[Noche-6: `rbd du` COMPLETO ejecutado — 48 imágenes, 1.503G prov / 848G usados reales. Alivio real por escenario: fase 1 W5-post ≈164G usados; escenario máximo con autorizaciones ≈572G. Baseline y clasificación por imagen: `~/aranea/work/cierre-preparatorio-20260921/RBD-DU-RESULTADOS-20260921.md`.]**
- **Conclusión de capacidad**: el alivio estructural de pool1 NO lo dan las migraciones; lo da frenar el growth (+17G/OSD/día ≈ +51G lógico/día con ×3 — mayor que cualquier migración en <1 semana). Prioridad real: K2/P1-4 (escritores) primero; W5-post es alivio gradual y mejora de dominios de falla.

### 3. Matriz disco por disco (99 filas)

`VMID | disco | función | backend actual | consumo | dependencias | backend objetivo | decisión | justificación | ahorro Ceph (techo prov) | riesgo`

| VMID | disco | función | backend actual | consumo | dependencias | backend objetivo | decisión | justificación | ahorro Ceph | riesgo |
|---|---|---|---|---|---|---|---|---|---|---|
| 105 | scsi0 | Datos Home Assistant (zvol 50G) | iscsi-aranea | 50G | HA config+historial | pool0 zvol (actual) | KEEP | dato en pool0 correcto; SNAP + VZ post-D | — | — |
| 124 | ide0 | Terminal MT4 PROD (datos/perfil) | nfs-storage | 709474K | trading real | nfs-storage (actual) | KEEP | dato operacional del terminal; vzdump llega con B1; NO tocar en operación | — | — |
| 124 | scsi0 | SO MT4-real | pool1 | 50G prov / sin medir | trading real | nfs-vmbackup o local-lvm | MIGRATE (W5-post) | SO reconstruible; reevaluación post-réplica, nunca en sesión | 50G | medio: guest de trading, ventana obligatoria |
| 125 | scsi0 | SO+datos mt4-test (RUNNING hades, cache=unsafe) | pool1 | 50G prov / sin medir | escritor principal K2 | apagar o reevaluar | DEFER | escritor identificado growth pool1; condición K2 ≥89%×2 → shutdown gated | 50G | alto como escritor de pool1 nearfull |
| 133 | ide0 | Terminal MT4 PROD (datos) | nfs-storage | 709474K | trading real | nfs-storage (actual) | KEEP | ídem 124 | — | — |
| 133 | scsi0 | SO mt4-ftmo | pool1 | 50G prov / sin medir | trading real | nfs-vmbackup o local-lvm | MIGRATE (W5-post) | ídem 124 | 50G | medio |
| 134 | ide0 | Terminal MT4 PROD (datos) | nfs-storage | 709474K | trading real | nfs-storage (actual) | KEEP | ídem 124 | — | — |
| 134 | scsi0 | SO mt4-ttp | pool1 | 50G prov / sin medir | trading real | nfs-vmbackup o local-lvm | MIGRATE (W5-post) | ídem 124 | 50G | medio |
| 140 | scsi0 | Echo SO+core (trading PROD) | pool1 | 20G prov / sin medir | Echo completo | local-lvm hades o nfs-vmbackup | MIGRATE (W5-post fase 1) | primera ficha W5 (P1-1): mínimo riesgo, máximo alivio; G1A cubre datos; ventana con Echo cerrado | 20G | medio: PROD, drill post-restore completo |
| 142 | scsi0 | daedalus DEV (120G) | pool1 | 120G prov / sin medir | agent ops secundario | local-lvm/nfs-vmbackup | MIGRATE (W5-post) | CFG hermes-ops A5; used sin medir | 120G | medio-bajo |
| 144 | scsi0 | SO+terminal mt4-demo | pool1 | 50G prov / sin medir | trading demo | nfs-vmbackup o local-lvm | MIGRATE (W5-post) | tras echo en el orden W5 | 50G | medio |
| 145 | scsi0 | Disco físico passthrough (pool0/pool2) | UNKNOWN | 976762584K | datos T0 | físico (actual) | KEEP | passthrough = los pools mismos; no es disco virtual | — | — |
| 145 | scsi1 | Disco físico passthrough (pool0/pool2) | UNKNOWN | 976762584K | datos T0 | físico (actual) | KEEP | passthrough = los pools mismos; no es disco virtual | — | — |
| 145 | scsi10 | SO TrueNAS | local-lvm | 32G | pool0/pool2 completos | local-lvm (actual) | KEEP | pools sobreviven al SO (DR-T5); CFG export = gap WP-B2 | — | — |
| 145 | scsi11 | Disco físico passthrough (pool0/pool2) | UNKNOWN | 976762584K | datos T0 | físico (actual) | KEEP | passthrough = los pools mismos; no es disco virtual | — | — |
| 145 | scsi2 | Disco físico passthrough (pool0/pool2) | UNKNOWN | 976762584K | datos T0 | físico (actual) | KEEP | passthrough = los pools mismos; no es disco virtual | — | — |
| 145 | scsi3 | Disco físico passthrough (pool0/pool2) | UNKNOWN | 976762584K | datos T0 | físico (actual) | KEEP | passthrough = los pools mismos; no es disco virtual | — | — |
| 145 | scsi4 | Disco físico passthrough (pool0/pool2) | UNKNOWN | 976762584K | datos T0 | físico (actual) | KEEP | passthrough = los pools mismos; no es disco virtual | — | — |
| 145 | scsi5 | Disco físico passthrough (pool0/pool2) | UNKNOWN | 976762584K | datos T0 | físico (actual) | KEEP | passthrough = los pools mismos; no es disco virtual | — | — |
| 145 | scsi6 | Disco físico passthrough (pool0/pool2) | UNKNOWN | 976762584K | datos T0 | físico (actual) | KEEP | passthrough = los pools mismos; no es disco virtual | — | — |
| 145 | scsi7 | Disco físico passthrough (pool0/pool2) | UNKNOWN | 7814026584K | datos T0 | físico (actual) | KEEP | passthrough = los pools mismos; no es disco virtual | — | — |
| 145 | scsi8 | Disco físico passthrough (pool0/pool2) | UNKNOWN | 500107608K | datos T0 | físico (actual) | KEEP | passthrough = los pools mismos; no es disco virtual | — | — |
| 145 | scsi9 | Disco físico passthrough (pool0/pool2) | UNKNOWN | 488386584K | datos T0 | físico (actual) | KEEP | passthrough = los pools mismos; no es disco virtual | — | — |
| 151 | ide0 | SO win-development (stopped) | nfs-storage | 709474K | — | — (decomisión) | DEFER | decomisión gated; zvols win valor UNKNOWN → owner | — | — |
| 151 | sata0 | Datos LUN2 (zvol zeus-win ~203G) | iscsi-aranea | LUN2 zvol | UNKNOWN | — | DEFER | LUN2 double-attach con 100 → WP-S1 antes de cualquier start | — | doble attach latente |
| 151 | scsi0 | Datos LUN2 (ídem) | iscsi-aranea | LUN2 zvol | UNKNOWN | — | DEFER | ídem | — | doble attach latente |
| 152 | scsi0 | SO PostgreSQL | pool1 | 20G prov / 10.0G usados | PG PROD Echo | nfs-vmbackup o local-lvm | MIGRATE (W5-post fase 3) | SO reconstruible; G1A diarios VERIFIED; tras echo/MT4 | 20G | medio: PROD trading, drill completo |
| 152 | scsi1 | Datos PG (zvol LUN4) | iscsi-aranea | 32G | PG PROD Echo | pool0 zvol (actual) | KEEP | D1 KEEP_JUSTIFIED: dato T0 fuera de Ceph; dumps+PITR+SNAP, no migración | — | — |
| 153 | scsi0 | SO MongoDB | pool1 | 20G prov / 9.0G usados | Mongo PROD Echo | nfs-vmbackup o local-lvm | MIGRATE (W5-post fase 3) | ídem 152 | 20G | medio |
| 153 | scsi1 | Datos Mongo (zvol LUN5) | iscsi-aranea | 32G | Mongo PROD Echo | pool0 zvol (actual) | KEEP | D1; ídem | — | — |
| 157 | scsi0 | SO MinIO | pool1 | 20G prov / 8.0G usados | MinIO PROD | nfs-vmbackup o local-lvm | MIGRATE (W5-post fase 3) | ídem 152; G1B certificada | 20G | medio |
| 157 | scsi1 | Datos MinIO (zvol LUN6) | iscsi-aranea | 16777344K | MinIO PROD | pool0 zvol (actual) | KEEP | D1; ídem | — | — |
| 158 | scsi0 | temporal DEV | pool1 | 32G prov / 10.0G usados | DEV | local-lvm/nfs-vmbackup | MIGRATE (W5-post) | CFG A5; reevaluación post-réplica | 32G | — |
| 159 | scsi0 | SO lab ubuntu-dev (stopped) | pool1 | 100G prov / 93.0G usados | — | — (liberación) | DEFER | liberación gated dueño; mayor lab de pool1 | 100G | borrado irreversible |
| 160 | scsi0 | SO argus | pool1 | 32G prov / 28.0G usados | observabilidad | nfs-vmbackup o local-lvm | MIGRATE (W5-post) | SO reconstruible; ejecutar tras K1 | 32G | medio: ARGUS valida los backups |
| 160 | scsi1 | Datos Prometheus (mayor dato en pool1) | pool1 | 50G prov / 39.0G usados | métricas plataforma | — | UNKNOWN | retención vs reconstruible → 018; si owner declara reconstruible = mayor liberación individual | 0 | — |
| 160 | scsi2 | Datos métricos | pool1 | 40G prov / 4.3G usados | métricas | — | UNKNOWN | ídem | 0 | — |
| 160 | scsi3 | Datos métricos | pool1 | 10G prov / 0.07G usados | métricas | — | UNKNOWN | ídem | 0 | — |
| 160 | scsi4 | Datos métricos | pool1 | 30G prov / 0.5G usados | métricas | — | UNKNOWN | ídem | 0 | — |
| 103 | rootfs | Servicio emqx (edge MQTT) | nfs-storage | 4G | plano edge | nfs-storage (actual) | KEEP | backend file válido (D-NEW-01); W1 CANCELADA; VZ post-D | — | — |
| 113 | rootfs | mcps plano de acceso (26 containers) | nfs-storage | 20G | plano de acceso agente | nfs-storage (actual) | KEEP | D-NEW-01; CFG A5 + VZ post-D (NO en piloto R2) | — | — |
| 116 | rootfs | obsidian-sync datos (CouchDB vault 64G) | nfs-storage | 64G | vault LiveSync | nfs-storage (actual) | KEEP | CFG R1 vault + DUMP CouchDB (gated credencial) + VZ post-D | — | — |
| 126 | rootfs | docker-flink SO+checkpoints | pool1 | 50G prov / sin medir | pipelines DEV | nfs-vmbackup o local-lvm | MIGRATE (W5-post) | CFG A5 cubre config; checkpoints regenerables | 50G | medio-bajo |
| 127 | rootfs | docker-observability legacy/dev (70% lleno) | pool1 | 25G prov / sin medir | ARGUS vive en 160 | local-lvm hades/nfs-vmbackup | MIGRATE (W5-post) | candidato natural W5-post (rootfs 70%) | 25G | — |
| 129 | rootfs | docker-hasura SO+datos dev | pool1 | 50G prov / sin medir | API DEV | nfs-vmbackup o local-lvm | MIGRATE (W5-post) | ídem W5-post | 50G | medio-bajo |
| 137 | rootfs | docker-frigate SO+config (media EXCLUIDA) | nfs-storage | 50G | cámaras/config | nfs-storage (actual) | KEEP | backend file válido (D-NEW-01); media reconstruible excluida; VZ post-D | — | — |
| 141 | rootfs | docker-echo-dev | pool1 | 20G prov / sin medir | DEV | nfs-vmbackup | MIGRATE (W5-post) | ídem | 20G | — |
| 147 | mp0 | config etcd | local-lvm | 8G | quorum | local-lvm (actual) | KEEP | ídem | — | — |
| 147 | rootfs | SO etcd-hades | local-lvm | 10G | quorum | local-lvm (actual) | KEEP | R1.5 + VZ piloto | — | — |
| 148 | rootfs | etcd-keeper datos+SO (UI sin quorum) | pool1 | 10G prov / 4.0G usados | etcd (datos en snapshot lógico) | local-lvm/nfs-vmbackup | MIGRATE (W5-post) | R1.5 cubre datos; rootfs REC excluido R2; candidato menor | 10G | — |
| 107 | scsi0 | SO lab develop (stopped) | pool1 | 100G prov / sin medir | — | — (liberación) | DEFER | liberación gated dueño WP-S1 | 100G | borrado irreversible = autorización por VMID |
| 109 | ide0 | SO lab win-serv (stopped) | nfs-storage | 715188K | — | — | KEEP | lab T3 | — | — |
| 109 | scsi0 | SO lab | local-lvm | 120G | — | — | KEEP | lab T3 | — | — |
| 110 | scsi0 | SO lab testing (stopped) | local-lvm | 50G | — | — | KEEP | lab T3 | — | — |
| 117 | scsi0 | SO lab ubuntu (stopped) | local-lvm | 32G | — | — | KEEP | lab T3 | — | — |
| 120 | scsi0 | SO lab k8s (stopped) | local-lvm | 32G | — | — | KEEP | lab T3 | — | — |
| 123 | scsi0 | SQX hera (SO+app) | local-sqx-hera | 50G | SQX producción | local-sqx-hera (actual) | KEEP-F04 | F-04; RBD residual 20G en pool1 → verificar/liberar WP-S1 | — | — |
| 123 | scsi1 | Datos SQX hera | local-sqx-hera | 600G | SQX producción | local-sqx-hera (actual) | KEEP-F04 | F-04 | — | — |
| 136 | scsi0 | SO kafka-hera | pool1 | 30G prov / sin medir | kafka DEV | local-lvm/nfs-vmbackup | MIGRATE (W5-post) | SO reconstruible; datos scsi1 ya fuera de Ceph | 30G | medio-bajo |
| 136 | scsi1 | Datos kafka | local-lvm | local-lvm hera | kafka DEV | — | UNKNOWN | valor/retención → 018; backend ya fuera de Ceph | — | 0 |
| 128 | rootfs | docker-kafka SO+datos dev | pool1 | 50G prov / sin medir | pipeline Echo (bridges) | athena (ubicación) / backend por reevaluar | KEEP (hasta P1-4) | W4: NO mover sin causalidad del brote; mover de UBICACIÓN no libera Ceph (RBD sigue en pool1) | 0 | 0 ahorro |
| 132 | rootfs | docker-monitoreo (STOPPED, sin decisión) | local-lvm | 10G | — | local-lvm (actual) | KEEP | regularizar estado en 018; VZ post-D | — | — |
| 155 | mp0 | config etcd | local-lvm | 8G | quorum | local-lvm (actual) | KEEP | ídem | — | — |
| 155 | rootfs | SO etcd-hera | local-lvm | 10G | quorum | local-lvm (actual) | KEEP | ídem | — | — |
| 104 | scsi0 | SO lab ryma (stopped) | local-kronos | 50G | — | — | KEEP | lab T3 | — | — |
| 106 | scsi0 | SO+datos jobs (docker DEV) | pool1 | 32G prov / sin medir | jobs/pipelines internos | local-lvm zeus/hera o nfs-vmbackup | MIGRATE (W5-post) | reevaluación por VM post-réplica; nunca con fulls | 32G | medio-bajo |
| 111 | scsi0 | SQX kronos (SO+app) | local-sqx-kronos | 50G | SQX producción | local-sqx-kronos (actual) | KEEP-F04 | F-04 | — | — |
| 111 | scsi1 | Datos SQX kronos | local-sqx-kronos | 600G | SQX producción | local-sqx-kronos (actual) | KEEP-F04 | F-04 | — | — |
| 112 | ide0 | SO sqx deprecado (stopped) | nfs-storage | 709474K | — | — (decomisión) | DEFER | decomisión gated; disco activo = pool-kronos | — | — |
| 112 | scsi0 | Disco activo de sqx-deprecado (LVM) | pool-kronos | 120G | guest stopped por decomisión | pool-kronos (actual) | DEFER | decomisión gated dueño; la RBD vm-112-disk-0 120G sin dueño en config va en tabla de huérfanas (WP-S1) | — | — |
| 114 | scsi0 | SO mt4-test (stopped, kronos) | pool1 | 50G prov / sin medir | — | — (liberación/conservación) | DEFER | decisión dueño WP-S1/018 | 50G | — |
| 118 | scsi0 | SO hermes (ejecutor backups) | pool1 | 32G prov / sin medir | timers A1/R1/R1.5/R2 | local-lvm o nfs-vmbackup | MIGRATE (W5-post) | SO reconstruible (CFG R1); NO tocar sin standby W-02 activo | 32G | medio: es el ejecutor de la protección |
| 118 | scsi1 | Staging backups (~49G) | pool1 | 50G prov / sin medir | ingesta→PBS | regenerable (staging) | RECONFIGURE | contenido regenerable tras ingesta PBS (A0); sin migración necesaria | 50G | — |
| 135 | scsi0 | worker Windows SQX | local-sqx-kronos | 50G | SQX producción | local-sqx-kronos (actual) | KEEP-F04 | F-04; backup excluido por diseño | — | — |
| 138 | scsi0 | SO kafka-kronos | pool1 | 30G prov / sin medir | kafka DEV | local-lvm/nfs-vmbackup | MIGRATE (W5-post) | ídem 136 | 30G | medio-bajo |
| 138 | scsi1 | Datos kafka | local-kronos | local-kronos | kafka DEV | — | UNKNOWN | valor/retención → 018 | — | 0 |
| 162 | scsi0 | SO sqx-ulab-kron (stopped) | pool1 | 20G prov / 11.0G usados | — | — (liberación) | DEFER | decisión dueño WP-S1 | 20G | — |
| 180 | scsi0 | PBS SO | local-kronos | 64G | todas las copias locales | local-kronos (actual) | KEEP | F-06; CFG PBS A5/WP-B2 | — | — |
| 180 | scsi1 | PBS datastore (295G→+300G W-01) | local-kronos | 300G | todas las copias locales | local-kronos/pool-kronos (actual) | KEEP | destino, no se auto-respalda; crecimiento W-01 gated | — | — |
| 154 | mp0 | config etcd | local-lvm | 8G | quorum | local-lvm (actual) | KEEP | ídem | — | — |
| 154 | rootfs | SO etcd-kronos | local-lvm | 10G | quorum | local-lvm (actual) | KEEP | R1.5+VZ | — | — |
| 100 | ide2 | ISO/CD virtual del lab | nfs-storage | ISO ~69G | — | — | KEEP | ISO adjunta del lab stopped; sin valor de recuperación | — | — |
| 100 | virtio0 | Datos lab Win11-GPU (stopped) | iscsi-aranea | 200G | LUN2 iSCSI (double-attach con 151) | — (decomisión) | DEFER | decomisión gated dueño WP-S1; resolver attach antes de cualquier start | — | LUN2 doble attach si se enciende |
| 102 | ide0 | SO lab mt5-wsl (stopped) | nfs-storage | 709474K | — | — | KEEP | lab T3 sin valor de recuperación | — | — |
| 102 | scsi0 | SO lab | local-lvm | 50G | — | — | KEEP | lab T3 | — | — |
| 108 | scsi0 | SQX zeus (SO+app) | local-sqx-zeus | 50G | SQX producción | local-sqx-zeus (actual) | KEEP-F04 | F-04 sagrado; RBD residual 20G en pool1 sin rol en config → verificar/liberar WP-S1 | — | — |
| 108 | scsi1 | Datos SQX zeus | local-sqx-zeus | 600G | SQX producción | local-sqx-zeus (actual) | KEEP-F04 | F-04 | — | — |
| 139 | scsi0 | SO kafka-zeus | pool1 | 30G prov / sin medir | kafka DEV | local-lvm/nfs-vmbackup | MIGRATE (W5-post) | ídem 136 | 30G | medio-bajo |
| 139 | scsi1 | Datos kafka | local-lvm | local-lvm zeus | kafka DEV | — | UNKNOWN | valor/retención → 018 | — | 0 |
| 170 | scsi0 | SO sqx-ulab-zeus (stopped) | pool1 | 20G prov / 11.0G usados | — | — (liberación) | DEFER | ídem | 20G | — |
| 156 | mp0 | config etcd | local-lvm | 8G | quorum | local-lvm (actual) | KEEP | ídem | — | — |
| 156 | rootfs | SO etcd-zeus | local-lvm | 10G | quorum | local-lvm (actual) | KEEP | ídem | — | — |
| 130 | scsi0 | OPNsense SO (firewall SPOF) | local-lvm | 64G | todo el edge | local-lvm (actual) | KEEP | VZ+CFG export (gap WP-B2); SPOF por función, no placement | — | — |
| 101 | mp0 | config etcd | local-lvm | 8G | quorum etcd | local-lvm (actual) | KEEP | ídem; VZ piloto R2 activo | — | — |
| 101 | rootfs | SO+config etcd-athena | local-lvm | 10G | quorum etcd | local-lvm (actual) | KEEP | etcd snapshot lógico R1.5 diario VERIFIED; SO reconstruible | — | — |
| 115 | rootfs | traefik SO+config crítica (edge entrada) | local-lvm | 16G | edge HTTPS interno | local-lvm (actual) | KEEP | CFG R1 diario (mecanismo más maduro) + VZ piloto; SPOF nodo se mitiga por restore (W2 CANCELADA) | — | — |
| 119 | rootfs | tailscale-gateway | local-lvm | 8G | acceso remoto | local-lvm (actual) | KEEP | VZ post-D | — | — |
| 149 | rootfs | pi-hole SO (L2-dead 35d) | local-lvm | 10G | DNS redundante | — (decisión función) | DEFER | D5: reactivar+proteger vs retiro (WP-B2); no es migración | — | — |
| 200 | rootfs | CA step-ca (stopped) | local-lvm | 20G | certificados internos | — (decisión función) | KEEP (decisión pendiente) | WP-B2: reactivar+backup claves vs retiro | — | — |

> Consumo: `prov` = tamaño asignado (evidence/05 + PROVSIZED); `usados` medido 20sep sólo donde hay `rbd du`. Re-medir en preflight. Los discos `ide0` MT4 (nfs-storage) NO están en pool1: su reubicación no aporta ahorro Ceph.

### 4. Migraciones justificadas — lista priorizada (NINGUNA antes de backups; orden W5-post)

| Orden | VMID | Disco(s) | Destino candidato | Precondición | Ahorro (prov) |
|---|---|---|---|---|---|
| 1 | 140 echo | scsi0 | local-lvm hades o nfs-vmbackup | G1A verificado + ventana Echo cerrado + drill post-restore | 20G |
| 2 | 133/134/144/124 SOs | scsi0 | nfs-vmbackup (pool0) o local-lvm | B1/nfs-vmbackup activo + ventana fuera de sesión | 200G |
| 3 | 152/153/157 SOs | scsi0 | nfs-vmbackup o local-lvm | dumps G1A/G1B diarios verificados (ya activos) + drill completo | 60G |
| 4 | 127/141/148 CTs chicos | rootfs | local-lvm/nfs-vmbackup | CFG A5 + post-réplica | 55G |
| 5 | 106/126/129/158/142/160-SO/136-138-139 SOs | según ficha | local-lvm/nfs-vmbackup | reevaluación por VM + rbd du previo | ~368G |
| 6 | 118 hermes SO | scsi0 | local-lvm o nfs-vmbackup | **W-02 standby PBS activo ANTES** | 32G |
| — | 118 scsi1 staging | — | regenerar post-ingesta A0 | ingesta PBS verificada | 50G |

Regla de cada fila: `BACKUP_BASELINE_VERIFIED` de la unidad → ficha con `qm config`+`pvesm`+`rbd du` del preflight → gate owner → ejecución en ventana → drill/recertificación → sólo entonces liberar el disco origen de pool1 (borrado = autorización independiente).

### 5. Imágenes RBD huérfanas o residuales (200G prov, fuera de la matriz de config)

| Imagen | Prov | Usados | Estado |
|---|---|---|---|
| vm-108-disk-0 | 20G | sin medir | guest sin disco pool1 en config (residual/destruido) |
| vm-112-disk-0 | 120G | **5,9G (medido noche-6 21sep)** | guest sin disco pool1 en config (residual/destruido) — alivio real por borrarla = 5,9G, no 120G |
| vm-108-disk-0 | 20G | 11,0G | huérfana residual (config actual) |
| vm-123-disk-0 | 20G | 10,0G | huérfana residual (config actual) |
| vm-167-disk-0 | 20G | 10,0G | VMID sin guest en config actual |
| vm-171-disk-0 | 20G | 10,0G | VMID sin guest en config actual |

> [!warning] ERRATA noche-6 (21sep 22:4x, verificación live por tasks de PVE): **162 y 170 YA NO EXISTEN** — el owner ejecutó ambos `qmdestroy` (root@pam) el 20sep 23:58 -03 (tasks OK en kronos y zeus; configs ausentes; RBDs ausentes de pool1). Las filas DEFER de 162 y 170 de esta matriz quedan obsoletas. Liberaciones owner del análisis: 162 ✓, 170 ✓, **112 sigue PENDIENTE** (guest stopped kronos, disco real en pool-kronos, RBD huérfana 5,9G). Huérfanas vigentes: 108/112/123/167/171 (200G prov / **46,9G usados totales**).

La RBD `vm-112-disk-0` (120G, lock stale) es la huérfana ya conocida de WP-S1; 108/123 tienen su disco real en local-sqx (F-04) — la imagen residual en pool1 requiere verificación de ausencia de refs vivas; 167/171 no existen como guests en la config actual. Ninguna se borra sin identificación por VMID + evidencia + autorización independiente (regla WP-S1).

### 6. UNKNOWN que faltan para cerrar el 100% del análisis (única investigación pendiente)

| Disco | Pregunta | Cómo se resuelve | Impacto en ahorro |
|---|---|---|---|
| 136/138/139 scsi1 (datos kafka ×3) | ¿valor/retención de los datos? | 018 + canal RO a guests | **0** — backend ya es local-lvm/local-kronos (fuera de Ceph) |
| 160 scsi1-4 (datos argus, 130G prov / ~72G usados) | ¿retención vs reconstruible? | 018 (decisión owner) | **Mayor palanca individual (72G)** si owner declara reconstruible |
| 124/133/134/144 interior MT4 | ¿qué hay dentro del terminal? | sin SSH; W-04/mejor canal | 0 en Ceph (ide0 = nfs-storage) |
| 116 CouchDB | credencial `_reader` | BUNDLE-A3 (gate owner) | 0 (rootfs nfs-storage) |

Ninguno de estos UNKNOWN bloquea Backup/DR ni la 1ª fase W5-post (echo/MT4/DB-SOs).

## Fuentes

- Evidencia: `~/aranea/work/storage-ceph-assessment-20260919/A/guest-disk-map.json` (59/59, discos y backends) · `.../evidence/05-ceph-config-rbd.txt` (prov RBD 19sep) · `~/aranea/work/operating-state-20260920/rbd-du2.txt` (used 20sep, 15 imágenes) · matrices canónicas del proyecto.
- Clasificación y reglas: [[PLACEMENT-DECISIONS-20260920]] §F/§D · [[MASTER-PLAN-STORAGE-BACKUP-DR]] §7 (D-NEW-01..06) + errata noche-5 · [[MATRIZ-59-GUESTS-BACKUP]] · [[TWO-LAYER-BACKUP-SPEC]] · [[CAPACITY-AND-RESERVATIONS]] §7 (presupuestos por fases).
- Mandato: owner "ARANEA · BACKUP FIRST" (21sep noche-5). Cambios: change log `80-agents/journal/change-logs/2026-09-21-backup-first-correccion.md`.