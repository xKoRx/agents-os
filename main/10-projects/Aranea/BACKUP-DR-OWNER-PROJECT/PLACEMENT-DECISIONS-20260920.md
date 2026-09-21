---
type: doc
schema_version: 1
status: active
icon: 🎯
slug: aranea-placement-decisions-20260920
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
related:
  - "[[MATRIZ-59-GUESTS-BACKUP]]"
  - "[[MASTER-PLAN-STORAGE-BACKUP-DR]]"
  - "[[FIRST-MAINTENANCE-WINDOW-20260920]]"
  - "[[OPERATING-STATE-20260920]]"
aliases:
  - Placement Decisions 2026-09-20
  - KEEP MIGRATE RECONFIGURE 2026-09-20
tags:
  - kind/doc
  - area/aranea
  - domain/backup-dr
created: "2026-09-20"
updated: "2026-09-21"
---

# 🎯 PLACEMENT-DECISIONS — 2026-09-20

## Propósito

- Clasificación KEEP/MIGRATE/RECONFIGURE/DEFER/UNKNOWN sobre evidencia del assessment 19-09 (handoff §3/§6) + runtime 20-09 ([[OPERATING-STATE-20260920]]), SIN reabrir el master plan: refina sus decisiones D1/D3 con datos nuevos. Los tamaños iSCSI corregidos aquí (28/32G, no 32G por defecto) no contradicen nada del plan; ajustan capacidad real.

---
## F. PLACEMENT-FREEZE-V2 — congelación final (mandato owner "Placement Freeze antes de Backup/DR", 21sep noche)

> **Autoridad máxima de esta nota donde contradiga A-E** (junto con §D). Congela la clasificación por workload; las migraciones quedan condicionadas al gate [[STORAGE-ORGANIZATION-FREEZE]]. Principio: el objetivo es el placement correcto, NO llenar la ventana — sin causalidad, no se mueve nada.

### Clasificación final por workload

| Workload | Veredicto | Clasificación de discos | Fundamento |
|---|---|---|---|
| PG 152 · Mongo 153 · MinIO 157 | **KEEP** | SO (scsi0, pool1 RBD) = reconstruible · DATOS (scsi1, zvol iSCSI pool0 LUN4/5/6) = críticos — **dos unidades distintas** | D1 KEEP_JUSTIFIED: dato T0 fuera de Ceph; migrar SO exigiría escribir en pool1 nearfull (NO_GO); protección = dumps+snapshots, no migración |
| Echo 140 + flota MT4 (124/133/134/144) + MT4 test (125, 114) | **KEEP** | SO+terminal (pool1 RBD / nfs ide0) = reconstruibles; credenciales broker fuera de alcance | sostiene la operación; vzdump llega con B1 post-D; NO tocar en operación |
| W5 down-tier SOs | **DEFER → reevaluación por VM** post-activación de la réplica (NUNCA simultánea con fulls) | por VM: beneficio/rendimiento/disponibilidad/capacidad/destino/dominio de falla/restore/alivio real; destinos válidos zeus 77,5G / hera 91,7G / `nfs-vmbackup` pool0; hades 33,4G sólo si VM ≤25G y deja ≥8G; NO trasladar la flota indiscriminadamente fuera de Ceph; NO migrar SQX (F-04) | el alivio de pool1 NO justifica por sí solo la ventana; cada VM con ficha y gate propios |
| W4 kafka 128 | **KEEP** hasta causalidad | rootfs pool1; datos scsi1 UNKNOWN → 018 | el brote "metadata out of date" sin diagnóstico (P1-4) no autoriza mover el broker; el pattern apunta a los multi-broker 136/138/139 |
| W3 pi-hole 149 | **DEFER → decisión de función D5** | rootfs local-lvm athena | corre en ATHENA (no hades); L2-dead crónico: diagnóstico + decisión reactivar+proteger vs retiro (WP-B2); sin migración planificada |
| CTs edge nfs-storage (103/113/116/137) | **KEEP** | rootfs nfs-storage (pool0) = configuración crítica en file-backend válido | correctamente configurados donde están; D-NEW-01 canceló su reubicación |
| Traefik 115 | **KEEP** | rootfs local-lvm athena = SO reconstruible + config crítica | CFG R1 diario (mecanismo más maduro); SPOF de nodo se mitiga por restore, no migración |
| etcd ×5 (+148) | **KEEP** | rootfs local-lvm/pool1 | quorum 5 hosts; snapshot lógico R1.5 diario VERIFIED |
| SQX 108/111/123 + worker 135 | **KEEP (intocable)** | local-sqx-* | F-04 sagrado |
| OPNsense 130 · TrueNAS 145 · CA 200 | **KEEP** | local-lvm / passthrough | SPOF firewall y CA = decisiones función (WP-B2), no placement |
| 100/151 (win) · 112/162/170 · labs stopped | **DEFER** | zvols/LUN/RBD según matriz | decomisión/liberación gated dueño (WP-S1); LUN2 double-attach latente |
| Pool2 (todo uso) | **RESERVADO** | — | exclusivamente réplica diaria de pool0 (D-NEW-01); PROHIBIDO: discos VM, rootfs, apps, destino PBS, uso operativo; `nfs-pool2` no se crea |

### Migraciones: tabla única de ejecución (vacía de activas)

`ID | VMID | disco | origen | destino | tamaño real | motivo | capacidad | dependencias | indisponibilidad | riesgo | protección previa | rollback | autorización`

- **Activas: NINGUNA.** W1/W2/P0-2 CANCELADAS (D-NEW-01) · W4 condicionada a causalidad P1-4 · W3 condicionada a D5 (y sería reactivación/retiro, no migración) · W5 = reevaluación por VM con ficha por disco en preflight (`qm config`+`pvesm`), gate por VM, nunca simultánea con fulls de réplica/B1/G1B.
- **Viernes 25sep**: `MIGRATIONS_NOT_READY` — ninguna ficha pasa al sábado; la ventana 26 queda prechecks→K2→K1→P0-1 (W-01). Las validaciones W-04 del viernes se mantienen.
- Seguridad (binding): protección previa verificado + capacidad destino + rollback + conservación del volumen origen (`--delete` jamás por defecto; `pct move-volume` elimina el origen → su protección ES el vzdump previo verificado) + autorización explícita por gate. Copia preventiva sólo dentro de su ventana autorizada.

---

## A. Veredicto general

- **El placement de datos está correcto; el problema activo es capacidad de pool1.** El patrón SO-en-Ceph + datos-en-zvol-pool0 (PG 152, Mongo 153, MinIO 157) se mantiene KEEP_JUSTIFIED (master plan D1): el dato T0 vive fuera del dominio de falla de Ceph; migrar SOs hoy exigiría escribir en pool1 nearfull (NO_GO) sin demostrar HA real. La migración que ALIVIA (SOs fuera de pool1) NO es la que corrige disponibilidad — es la que evita la pérdida de los SOs reconstruibles si el cluster se degrada más.
- **Ceph NO_GO vigente.** Ningún MIGRATE escribe en pool1. Toda liberación de espacio va por el carril Ceph (WP-S1) con gates de dueño.
- **4 correcciones de disponibilidad no requieren migrar discos de datos** (W1-W4) y 1 sí, en orden (W5). Todas requieren ventana: la primera es **sábado 26-09 madrugada** (ver [[FIRST-MAINTENANCE-WINDOW-20260920]]).
- **[Errata 21sep] Las 5 fichas MIGRATE son PROPUESTAS, no destinos aprobados.** Ninguna W1-W5 está autorizada en bloque; cada una exige su gate owner explícito (indicado en la ficha) y la ventana formal. En particular W1/W2→pool2: pool2 es **single-disk (F-14)** y **comparte chasis con pool0** — su aporte es separar el dominio de falla del SO edge respecto de los datos T0, NO redundancia ni off-host (el SPOF del chasis se mantiene aceptado). El down-tier W5 lee de pool1 vía vzdump y escribe en local-lvm/PBS (respeta NO_GO).

## B. Clasificación

### KEEP (ubicación justificada — sin cambios)

| Unidad | Hoy | Justificación |
|---|---|---|
| PG 152 datos (zvol LUN4 ~28G usados) | iSCSI pool0 | mirror ZFS sano, fuera de Ceph; protección = dumps A1 + PITR A2 (roadmap), no migración |
| Mongo 153 datos (LUN5 ~32G) | iSCSI pool0 | idem; RPO 1h = decisión topológica owner (A2b), no placement |
| MinIO 157 datos (LUN6, 49,8G/100G) | iSCSI pool0 | idem; G1B certificado; versioning = deuda gated |
| echo 140 SO (scsi0) + MT4 fleet | pool1 / nfs | sostiene la operación actual; el SO es reconstruible y su vzdump llega post-B1; NO tocar en operación |
| etcd ×5 | local-lvm | quorum local + R1.5 snapshot lógico diario VERIFIED |
| CTs nfs-storage (103 emqx, 113 mcps, 116 vault, 137 frigate) | nfs-storage pool0 | backend file válido; cobertura PBS creciendo (113 ya en piloto) |
| SQX 108/111/123 + worker 135 | local-sqx-* | F-04 intocable |
| PBS 180 + datastore | local-kronos | F-06/F-07; crecimiento +300G post-D-piloto (D3) |
| labs T3 stopped (12) | varios | sin valor de recuperación; fuera de cobertura por diseño |

### MIGRATE (5, con ficha completa)

#### W1 — nfs-storage fuera de pool0 (mismo chasis) → pool2 (TrueNAS)

1. **Problema**: los rootfs de 4 CTs del plano edge (mcps 113, emqx 103, obsidian-sync 116, frigate 137 — ADD-IMP/T2 y ADD-CRIT en la matriz, pendientes de aprobación 018) viven en `pool0/proxmox_storage` (NFS), junto a ISOs y discos ide0 de MT4/labs: caída de TrueNAS derriba simultáneamente el plano edge Y los datasets de datos T0 (iSCSI). Un solo dominio de falla (chasis hades) cubre datos y arranque de servicios.
2. **Evidencia**: handoff §3.2/§3.5 (dependencia circular verificada); runtime 20sep: montaje NFS con 402G usados/30% (vista de pool0; el dataset zfs usado = 416G según handoff — misma unidad, métricas distintas) y prune `keep-all=1` vigente.
3. **Objetivo**: storage PVE NUEVO `nfs-pool2` (dataset `pool2/nfs_pool2` exportado NFS) que recibe SÓLO los 4 rootfs movidos. **`nfs-storage` NO se redefine ni se toca** (corrección adversarial B1): el export pool0/proxmox_storage sigue sirviendo los discos `ide0` de los MT4 PROD (124/133/134), los labs stopped (102/109/112) e ISOs — redefinirlo habría dejado a la flota de trading sin discos de arranque. Inventario del export (handoff §3.2): 8 CT rootfs en total; se mueven 4, los demás quedan. Estado final: DOS storages NFS, cada uno con su contenido.
4. **Beneficio**: separa el dominio de falla del SO edge del de los datos T0; pool2 (HDD) es backend adecuado para CTs poco exigentes; sin capex.
5. **Dependencias/riesgo**: CTs apagados durante el movimiento de su rootfs (vzdump→restore, nunca mover el file bajo el CT vivo); no corrige I/O (no lo necesita); no es off-host (SPOF F-14 del chasis se mantiene aceptado).
6. **Capacidad destino**: pool2 libre 2,15T; rootfs a mover ≈ 138G brutos (54G del dataset PVE + margen); cabe sin tocar legacy F-09.
7. **Downtime y mecanismo**: ~15 min/CT en ventanas escalonadas (CT stop → `pct move-volume <ct> rootfs <storage-nuevo>` con vzdump previo verificado; fallback vzdump + `pct restore` al nuevo storage). NO simultáneo con A6-REPL full (I/O compartido en TrueNAS).
8. **Reversión**: re-restore del vzdump previo al backend original (`pct move-volume` elimina el volumen origen: NO hay vuelta por redefinición de storage). <10 min/CT para rootfs chicos; obsidian-sync (~64G asignados) puede tomar 20-40 min.
9. **Protección previa**: vzdump fresco VERIFICADO (verify TASK OK) de los 4 CTs ANTES de tocarlos — **113 mcps incluido: NO está en el piloto R2** (corrección adversarial B2; matriz: "VZ post-D, NO en piloto").
10. **Autorización**: OWNER — alta del storage nuevo `nfs-pool2` en storage.cfg (pmxcfs cluster-wide: una edición, replicada a los 5 nodos) + ventana 019.

#### W2 — Traefik 115 de local-lvm (athena) → CT sobre nfs-pool2

1. **Problema**: el edge de entrada del homelab depende del local-lvm de athena; si athena cae, traefik no arranca en otro nodo (re-restore manual).
2. **Evidencia**: matriz (rootfs:local-lvm); R1 certifica que su config es la unidad de backup más madura (CFG diario + recovery-critical `acme-stepca.json`).
3. **Objetivo**: rootfs de 115 en nfs-pool2 (W1): cualquier nodo puede levantarlo.
4. **Beneficio**: eliminación del SPOF de nodo para el edge; reconstrucción trivial con la config ya protegida.
5. **Dependencias**: W1 ejecutado; prueba de arranque en nodo alterno (verificar attach de IP).
6. **Capacidad destino**: rootfs 115 = 5-10G; trivial sobre pool2.
7. **Downtime**: 5-10 min (restore + arranque); edge HTTPS interno no debe interrumpirse >10 min — dentro de ventana y sin Echo traficando.
8. **Reversión**: restore del rootfs original local-lvm (vzdump previo); 10 min.
9. **Protección previa**: vzdump 115 + drill R1 del día (ya automático diario).
10. **Autorización**: OWNER (movimiento del edge en ventana 019; deriva de W1).

#### W3 — pi-hole 149 de local-lvm (hades) → CT nfs-storage (nodo libre)

1. **Problema**: DNS/edge redundante vive DENTRO del nodo con mayor densidad (hades, 24 guests): si hades cae, la resolución local cae con todo lo demás. Además el servicio está L2-dead hoy (verificado).
2. **Evidencia**: matriz (rootfs:local-lvm); runtime 20sep (ICMP 149 100% loss).
3. **Objetivo**: rootfs de 149 en nfs-storage (W1), en un nodo distinto de hades.
4. **Beneficio**: DNS sobrevive a la caída de hades; aislamiento de fallo del servicio crítico de resolución.
5. **Dependencias**: **resolver primero el estado del servicio** (WP-B2: token FTL6 + decisión retiro/reactivación). Si el dueño decide retiro → W3 se transforma en decomisión, no migración.
6. **Capacidad**: rootfs pequeño (<5G).
7. **Downtime**: n/a mientras esté L2-dead; si se reactiva, ventana breve.
8. **Reversión**: restore rootfs original.
9. **Protección previa**: vzdump 149.
10. **Autorización**: OWNER — decisión pi-hole (reactivar+proteger vs retiro) es bloqueante.

#### W4 — Kafka dev 128 (docker-kafka, hera) → hades

1. **Problema**: el broker kafka dev vive solo en hera junto a 1 de los 3 OSD Ceph y al MON; el brote de errores "metadata out of date" del 20sep en los 3 bridges (21:26-21:30) sugiere churn de liderazgo kafka afectando al pipeline Echo — **hipótesis pendiente de diagnóstico** (el patrón del error apunta más a los multi-broker 136/138/139 que al single-node 128; P1-4 lo resuelve). Un solo host contiene hoy a docker-kafka.
2. **Evidencia**: runtime 20sep (128 en hera; errores 21:26-21:30; kafka-hera/kronos/zeus sin ISR verificable por falta de canal); matriz (rootfs:pool1).
3. **Objetivo**: mover el CT 128 a **athena** (destino corregido por revisión adversarial: <1% CPU, sin OSD Ceph, sin PBS, densidad mínima; hades queda descartado por ser el chasis SPOF F-13 con máxima densidad y Echo PROD encima). El disco del CT está en pool1 (RBD, cualquier nodo lo monta): la migración es offline y de ubicación, no de backend.
4. **Beneficio**: separa al broker de los hosts Ceph; reduce correlación de fallos con el storage nearfull; ventana de diagnóstico del brote más limpia.
5. **Dependencias**: ventana con Echo cerrado (reinicio del broker = reconexión de bridges); verificar que clientes no dependan de un hostname ligado a hera.
6. **Capacidad destino**: athena tiene RAM/CPU sobrada; el disco no se mueve físicamente.
7. **Downtime**: 3-5 min offline.
8. **Reversión**: migrar de vuelta (mismo mecanismo); 5 min.
9. **Protección previa**: vzdump 128 (hoy NO está en piloto → primer vzdump en la ventana antes de mover) + verificar topics/offsets post-arranque.
10. **Autorización**: OWNER (componente del pipeline Echo; movimiento en ventana 019). NOTA: diagnosticar el brote de errores ANTES (puede ser churn normal de un cluster dev sin ISR de tamaño 1; si la causa es otra, W4 no la corrige).

#### W5 — Down-tier de SOs reconstruibles desde pool1 (≈64G lógicos, ~-64G por OSD lleno)

1. **Problema**: pool1 nearfull estructural (CRUSH host + 1 OSD/host, PROBADO 19-09) se agrava: 87,8% hoy con slow ops. La alternativa G del assessment (mover SOs fuera) es la única liberación estructural sin capex que no toca datos de valor.
2. **Evidencia**: rbd du 20sep: los SOs productivos identificados suman ≈64G lógicos (PG 152 20G, mongo 153 20G, echo 140 24G aprox por clase de tamaño, MT4s 133/134/144, margen). Todo el valor de esos guests vive fuera de pool1 (datos en zvol pool0 / SQX local / terminal MT4 en hades).
3. **Objetivo**: vzdump→PBS + restore del rootfs a local-lvm del nodo destino (o nfs-storage para CTs), priorizando: echo 140 → hades local-lvm (donde opera; mínimo riesgo, máximo alivio); MT4s → hades; PG/Mongo/MinIO SOs → local-lvm hades. NO migrar SQX (F-04). ≈64G base (20+20+24G: PG/Mongo/echo) — suma conservadora: con MT4s 133/134/144 y margen el total real es mayor; cuantificar exacto en preflight. Resultado esperado ≈ -64G o más por OSD lleno (87,8% → ~81% o menos).
4. **Beneficio**: des-presuriza pool1 SIN capex y sin tocar datos; reduce el riesgo del escenario "kronos cae = recovery imposible" al bajar el punto de llenado; habilita a futuro el gate de nuevos discos con evidencia.
5. **Dependencias**: piloto R2 con verify OK + decisión D-piloto (28sep) + B1 operativo (vzdump T0 como mecanismo); PBS con +300G (D3) o validación de espacio; NO ejecutar con slow ops activos.
6. **Capacidad destino**: local-lvm hades (SSD nodo; re-medir en preflight); PBS necesita room para 6-8 imágenes T0 (con dedup, dentro del +300G planificado).
7. **Downtime**: 15-30 min por VM (vzdump offline + restore + arranque + verificación app); escalonado en 2-3 ventanas; Echo 140 primero y con Echo cerrado.
8. **Reversión**: re-restore desde el snapshot PBS previo al backend original (pool1 sigue existiendo); por VM, <30 min.
9. **Protección previa**: vzdump fresco de CADA VM antes de tocar (el mismo que alimenta la migración); verify TASK OK del snapshot antes del restore.
10. **Autorización**: OWNER — primera ejecución material del down-tier (018 lista final + D-piloto + ventana); orden propuesto: echo→MT4→DB-SOs.

### RECONFIGURE (problema resoluble sin mover discos)

| ID | Unidad | Problema | Corrección | Estado |
|---|---|---|---|---|
| R-1 | nfs-storage prune | `keep-all=1` riesgo llenado | diff storage.cfg 5 nodos ya preparado (BUNDLE-A0-GATED) | GATED, listo para owner |
| R-2 | ARGUS instrumentación | 865 series de plataforma (kafka/ceph/pve/node) declaradas y SIN muestras: instrumentación muerta o scrapes caídos | reactivar scrapes/exporters (WP-S4 + revisión exporters en 160) | observabilidad, mayormente RO-safe; WP-S4 READY |
| R-3 | PBS metric drift | driver R2 reporta 92G/189G vs df 48G/295G | reconciliar cálculo del driver (compresión vs allocation) en próxima ventana | investigación local, sin mutación |
| R-4 | mcps rootfs 83% | build cache 8,9G + imágenes reclaimables | `docker system prune` gated en ventana | GATED (mutación plano acceso) |
| R-5 | Ceph slow ops + mClock | perfil high_recovery_ops + fragmentación | WP-S2 (mClock balanced + compact), ventana | carril Ceph, gated |

### DEFER (intervención válida, no segura o no urgente ahora)

| Unidad | Motivo |
|---|---|
| 100/151 (win) + LUN2 double-attach | decomisión gated dueño (WP-S1); nunca levantar ambas sin resolver attach |
| 112/162/170 liberaciones | dueño (WP-S1), borrado irreversible → autorización por VMID |
| pool0→pool2 REPL full inicial | I/O masivo en ventana (WP-A6), tras gates 018/019 y datasets; NO solapar con W1 |
| SO→pool2 de CTs adicionales | después de W1/W2, evaluar con experiencia del primer ciclo |
| 2º target PBS→pool2 | post-B1 (master plan D3) |
| CA 200 | decisión owner reactivo/retiro (WP-B2) |

### UNKNOWN (evidencia insuficiente hoy)

| Unidad | Gaps |
|---|---|
| kafka-hera/kronos/zeus (136/138/139) datos scsi1 | valor/retención UNKNOWN → 018; sin canal RO a guests |
| argus 160 datos scsi1-4 (39G/4,3G usados reales por rbd du) | retención vs reconstruible → 018 (los discos SÍ tienen datos; el 0% del métrico PVE no es fiable para data disks) |
| CouchDB 116 (A3 SKIP MP-01) | sin credencial en custodia → BUNDLE-A3 |
| MT4 fleet interior (124/133/134/144) | sin SSH a guests; `running` + métricas echo bridges es la única señal de vida |
| datasets trading_systems/trading_documents | inclusión REPL pendiente decisión dueño (A6) |

## C. Caso Ceph (resumen ejecutivo del carril, NO ejecutable por Backup/DR)

- **Estado**: HEALTH_WARN; nearfull estructural PROBADO (CRUSH host + 1 OSD/host + réplica 3) + **slow ops BlueStore nuevos en osd.0/2** (20sep) + growth medido (~+17G/OSD lleno en 27h). Márgenes por OSD lleno (818/932 GiB; ratios estándar nearfull 0,90 / backfillfull 0,95): backfillfull ≈ 21G, full ≈ 67G — a este ritmo, backfillfull en ~1 día si el growth no frena.
- **Causa del growth a identificar**: los 43 guests running escriben en pool1; candidatos: 127 (docker-observability, 70% rootfs), flink checkpoints (126), kafka topics, logs. Primera acción de la ventana: identificar escritor con las métricas de disco guest ya capturadas en `~/aranea/work/operating-state-20260920/pve-live.txt`, sin tocar el cluster.
- **Secuencia vigente del carril Ceph**: S4 (instrumentación, READY) → S1 (liberaciones gated) → S2 (mClock+compact, ventana) → S3 (decisión estructural pool1). Master plan D1: si se ejecuta W5, la alternativa G queda activada parcialmente y pool1 recupera ~64G.
- **Regla inviolable**: ninguna operación Backup/DR escribe en pool1 mientras dure NO_GO; las 5 migraciones aquí definidas lo respetan (W5 LEE de pool1 vía vzdump y ESCRIBE en local-lvm/PBS).

## Fuentes

- [[OPERATING-STATE-20260920]] (runtime 20sep), handoff assessment `~/aranea/work/storage-ceph-assessment-20260919/HANDOFF-2026-09-19.md` (§3.2, §3.5, §4, §6), [[MASTER-PLAN-STORAGE-BACKUP-DR]] (D1/D3/§4/§5), [[MATRIZ-59-GUESTS-BACKUP]], [[FIRST-MAINTENANCE-WINDOW-20260920]] (secuencia de ejecución).

---

## D. Redirección owner 21sep noche (D-NEW-01..06) — cancelaciones y recolocación

> Autoridad: mandato ONE-SHOT 21sep noche (§7 del [[MASTER-PLAN-STORAGE-BACKUP-DR]]). No altera el histórico A-C; donde contradiga, manda esta sección. Las fichas W1/W2 anteriores quedan CANCELADAS (no P0 condicionado); W3/W4/W5 se recalifican.

| Ficha | Veredicto nuevo | Detalle |
|---|---|---|
| W1 (4 CTs edge → nfs-pool2) | **CANCELADA** | D-NEW-01: pool2 exclusivo para réplica de pool0. Sin alta `nfs-pool2`, sin P0-2 en la ventana 26. Si el problema de dominio de falla del edge volviera a priorizarse: destinos alternativos pool0 (`nfs-vmbackup` para rootfs) / pool1 (bloqueado NO_GO) / local-lvm por nodo — según características del workload; NO pool2. Estado actual de los 4 CTs: **correctamente configurados donde están** (nfs-storage pool0 es backend file válido) — no hay migración que inventar |
| W2 (traefik 115 → nfs-pool2) | **CANCELADA** | ídem W1. 115 queda en local-lvm athena con CFG R1 diario (mecanismo más maduro del sistema); su SPOF de nodo se mitiga por restore, no por migración |
| W3 (pi-hole 149) | **DEFER → decisión de función (D5)** | 149 corre en ATHENA (no hades) y está L2-dead: resolver por diagnóstico y decisión (reactivar+proteger vs retiro), no por supervivencia a hades. Sin migración planificada |
| W4 (kafka 128 hera→athena) | **KEEP hasta diagnóstico (D6/P1-4)** | No mover el broker sin causalidad demostrada del brote "metadata out of date"; el diagnóstico RO manda. La ficha original ya lo condicionaba |
| W5 (down-tier SOs desde pool1) | **RECALIFICADA — reevaluación por VM** | No asumir que todos los SOs deben salir de pool1: por VM evaluar beneficio/rendimiento/disponibilidad/capacidad/destino/dominio de falla/restore/alivio real de Ceph. Hades local-lvm (33,4G) NO es destino de la propuesta anterior. Nueva opción habilitada por D-NEW-02: rootfs destino = `nfs-vmbackup` (pool0, ver [[TWO-LAYER-BACKUP-SPEC]] §1) además de zeus 77,5G / hera 91,7G. El alivio de pool1 NO justifica por sí solo la ventana: placement correcto > llenar la ventana |
| Alta `nfs-pool2` (habilitador D4) | **CANCELADA** | sin W1/W2 no tiene consumidor; la ventana 26sep pierde P0-2 (queda K2/K1/P0-1) |
| 2º target PBS→pool2 (D3/WP-B2 opcional) | **CANCELADA** | contradice D-NEW-01 (pool2 no recibe backups de VMs); la 2ª copia local de VMs vive en `nfs-vmbackup` (pool0) |

**Matriz corregida resumida**: KEEP = PG/Mongo/MinIO datos (zvol pool0) + SOs donde estén salvo reevaluación W5 por VM + etcd×5 + CTs edge en nfs-storage + SQX F-04 + PBS 180. MIGRATE = ninguna activa (W1/W2 canceladas; W5 condicionada a la reevaluación; W4 gated a diagnóstico). RECONFIGURE = R-1..R-5 sin cambios. DEFER = W3 (D5), 100/151, 112/162/170, REPL-full (ahora SPEC réplica), CA 200. UNKNOWN = kafka/argus data, CouchDB credencial, MT4 interior — sin cambios.
