---
title: "SPEC — Replicación diaria pool0 → pool2 (2026-09-21)"
type: doc
schema_version: 1
status: active
icon: 🔁
slug: pool0-to-pool2-replication-spec
area: "[[Aranea]]"
project: "[[BACKUP-DR-OWNER-PROJECT]]"
created: "2026-09-21"
updated: "2026-09-21"
aliases:
  - POOL0-TO-POOL2-REPLICATION-SPEC
  - SPEC replicación pool0 pool2
tags:
  - kind/doc
  - area/aranea
  - domain/backup-dr
  - project/backup-dr
related:
  - "[[MASTER-PLAN-STORAGE-BACKUP-DR]]"
  - "[[TWO-LAYER-BACKUP-SPEC]]"
  - "[[MANDATO-REPLICACION-SPEC]]"
---

# 🔁 SPEC — Replicación diaria pool0 → pool2

> Autoridad: D-NEW-01 (pool2 = réplica diaria de TODO pool0, sin otro uso) del mandato ONE-SHOT 21sep noche. Estado: **SPEC congelable en T-24; ejecución GATED** (gates §G). Números medidos 21sep noche (API v2.0 + SSH ariadna@truenas); regla del proyecto: re-medir en preflight antes de cada gate.

## Propósito

Especifica la réplica diaria incremental de TODO pool0 hacia pool2 según D-NEW-01: inventario, capacidad, snapshots, consistencia, vida del HDD, recuperación y gates de activación. Ejecución GATED.

## Contenido

## 1. Inventario pool0 (medido 21sep ~17:45-18:00 -03)

pool0: mirror ×3 (6 discos 932G virtuales), 4,08T size, ONLINE, scrub OK 6sep 2026 (0 errores). Used lógico 2,59T / avail dataset-view 945G. **No hay snapshots periódicos activos** (606 snapshots totales son residuos 2025 + sistema; sólo 156 en pool0, todos jul-2025 o de instalación).

| Dataset / zvol | Used | Replicación | Nota |
|---|---|---|---|
| pool0/aranea_storage | 1.114,8G | SÍ | mayor dataset de producción |
| pool0/trading_systems | 485,2G | SÍ | "todo pool0" del owner lo incluye; confirmación D-W3 (inclusión explícita, no silenciosa) |
| pool0/proxmox_storage | 416,8G | SÍ | NFS PVE; corregir prune keep-all=1 es tarea separada (WP-A0-gated), no excluir de réplica |
| pool0/iscsi (zvols) | 539,2G | SÍ | pg_data 33,0G · mongo_data 32,5G · minio_data 50,3G · vm-zeus-win-disk 203,1G · win-development 203,1G · debian-xhrvgh 17,2G |
| pool0/apps | 67,4G | SÍ | incluye frigate media 66,8G (reconstruible: exclusión OPCIONAL sólo por RC owner, por defecto va) |
| pool0/trading_documents | ~0G | SÍ | casi vacío |
| pool0/home / ix-apps | ~0G | SÍ | triviales |
| pool0/ix-applications | 10,1G | SÍ | apps TrueNAS |
| pool0/.ix-virt / pool0/.system | 15,5G / 3,1G | **NO** | exclusión técnica justificada: datasets de sistema del middleware TrueNAS (midvirt/instalación); sin valor de recuperación del owner; restauración = reinstalar SCALE/middleware |
| **Total envío inicial** | **≈2,57T** | | 2,59T − 18,6G excluidos |

Casos no replicables: ninguno en el alcance (todo dataset/zvol es replicable con zfs send/recv). Si el preflight encuentra un zvol en uso con lock exclusivo que impida el snapshot, se documenta y ese dataset entra como excepción explícita — nunca exclusión silenciosa.

## 2. Capacidad (verificada 21sep noche)

- **pool2 zpool: size 7,27T · alloc 3,19T · FREE 4,08T** (fuente: `zpool list` vía SSH — el número operativo). La vista `zfs list` AVAIL 2,15T subestima porque el "used" 4,99T doble-cuenta ~1,8T de snapshots legacy compartidos con orígenes ya borrados; sin quotas/reservas en ningún dataset (verificado `zfs get -r`).
- Errata material: el freeze del martes registró "4,18T libres" (medición zpool del 21sep 17:04Z) — la re-medición de esta sesión da **4,08T** (drift real del día ~0,1T por actividad del pool o diferencia de muestra; conclusión sin cambio). El "2,15T" de la ficha W1 (19sep) era la vista dataset, no zpool.
- Presupuesto post-1ª réplica: 3,19T + 2,57T ≈ **5,76T alloc de 7,27T → ~1,5T libres (≈20%)**. Regla de operación: **si free < 1,00T → NO-SEND + alerta owner** (freno duro); aviso temprano < 1,50T.
- Crecimiento diario: UNKNOWN hoy (sin serie medida). Plan de medición: `zpool list` diario 7 días antes de activar (o `zfs list -o used` histórico) → la retención se ajusta con ese dato. Presupuesto defensivo hasta medir: delta diario ≤50G + retención 14 días ≈ ≤0,7T adicionales ⇒ aún cabe.
- **Espacio adicional en pool0** por los respaldos de pool1 (D-NEW-02): ver TWO-LAYER-BACKUP-SPEC §pool1→pool0 (presupuesto ≈100-250G sobre 945G libres de pool0 — sin conflicto).

## 3. Snapshots e incrementales (mecanismo)

- **Snapshot local pool0**: `zfs snapshot -r pool0@repl-YYYYMMDD` (recursivo = set atómico multi-dataset en un mismo txg). Frecuencia local: diaria 1× (alineada con la sesión de replicación). Retención origen: **14 × @repl-* (14 días)**; los snapshots legacy 2025 existentes NO se tocan (limpieza = decisión owner separada).
- **Sesión de replicación única diaria a pool2**: `zfs send -R -I pool0@repl-<prev> pool0@repl-<hoy> | zfs recv -F pool2/pool0-replica` — un solo stream incremental del árbol completo (incluye zvols); la primera ejecución es full (~2,57T) y las siguientes envían sólo el delta entre snapshots.
- **Horario: 04:45 -03** — fuera de dumps G1A (03:00/03:20) y R1 (04:00/05:00); R2 expira 26sep (sin conflicto futuro). Ejecución en TrueNAS (cron interno del middleware — **cero dependencia de Hermes o agentes LLM**, D-NEW-06). Nota de implementación: los endpoints `/replication` y `/pool/periodic-snapshot/task` respondieron **404** en la API de esta versión (25.04.1) en sondas RO — la activación usa cron de sistema TrueNAS + script `zfs` (equivalente, igual de no-dependiente); verificar en T-25 si existe el endpoint en una revisión de API.
- **Identificación del último snapshot común**: el script deriva `<prev>` del snapshot @repl-* más reciente presente en AMBOS lados (comparación de `zfs list -t snapshot`); nunca asume el de ayer.
- **Ejecución fallida / interrupción**: exit≠0 → el destino queda en el último snapshot común (recv es transaccional por stream; el estado previo no se corrompe con `recv -F` sobre el dataset existente); el día siguiente re-ancla en el último común y continúa incremental — **reanudación natural sin full**. `flock` en el script: sesiones solapadas imposibles.
- **Cadena perdida** (snapshot requerido borrado del origen): NO reenviar full automático. Regla: si el último común tiene >7 días, la sesión FALLA CERRADA + alerta; recuperación = full re-send en ventana aprobada tras decisión owner (la retención de 14 días en origen hace este caso requerir >7 días de fallo consecutivos).
- **Destino**: dataset NUEVO `pool2/pool0-replica` (los árboles legacy `pool2/backup`, `pool2/pool0_backup`, `pool2/zfs_backup` quedan INTACTOS — F-09). Propiedad `readonly=on` en destino (validar en fixture que recv opera con ella; si no, documentar la excepción).

## 4. Consistencia por workload (honestidad de la réplica)

La réplica es **crash-consistent** (snapshot ZFS ≠ aplicación congelada). Por workload:

| Dato | Consistencia de la réplica | Copia consistente paralela | Recuperación coordinada |
|---|---|---|---|
| PG 152 (zvol pg_data) | crash-consistent; PG recupera por WAL replay al montar | dump G1A diario app-consistente en PBS + cloud | montar zvol clonado + replay; dumps mandan para punto limpio |
| Mongo 153 (zvol mongo_data) | crash-consistent; standalone sin oplog: estado del instante | dump G1A diario (RPO 24h real) | ídem |
| MinIO (zvol minio_data) | crash-consistent | G1B semanal (última copia VERIFICABLE) | G1B manda para restore completo |
| zvols MT4/win/HA/debian | crash-consistent (la mayoría apagados la mayor parte del día) | vzdump post-B1 | n/a |
| datasets de archivos (aranea/trading/proxmox_storage) | consistente (sin app encima que abra transacciones) | — | clonar y leer |

Regla: **NUNCA declarar** la réplica como "backup consistente de PostgreSQL/MongoDB/MinIO": para eso están dumps/G1B (two-layer, ver [[TWO-LAYER-BACKUP-SPEC]]). La réplica cubre borrado/corrupción a nivel bloque y pérdida del dataset.

## 5. Vida útil del HDD (pool2, single-disk)

Una sesión diaria (04:45): escritura del delta diario después de la inicial; sin servicios productivos, sin apps, sin full innecesarios. Scrub: **pool2 NO tiene scrub desde jul-2025** (verificado: last scrub 12jul2025 0 errores; la única tarea de scrub del sistema (id=3) apunta a pool0, scrubbed 6sep). Requisito gate: (1) **scrub manual de pool2 ANTES de la primera réplica** (ventana propia, ~7h estimadas por el histórico de pool0: 1,5T scrubbed en 1h28m → 7,27T ≈ 7h) y (2) tarea de scrub MENSUAL para pool2 creada con la activación. SMART/temperatura: alertas middleware TrueNAS vigentes; check semanal script: `zpool status pool2` sin errores + `smartctl` sin contadores nuevos (output a log local TrueNAS). Control de degradación: cualquier error de scrub o lectura → NO-SEND + alerta (no confiar la réplica a un disco degradado). No desactivar verificaciones para reducir desgaste.

## 6. Recuperación (procedimientos, resumen ejecutable en MANDATO-REPLICACION-SPEC)

1. **Archivo eliminado**: clonar `pool2/pool0-replica/<ds>@repl-<d>` en TrueNAS → montar RO → copiar de vuelta a ruta nueva; jamás sobrescribir el origen.
2. **Dataset dañado**: comparar snapshot origen vs réplica; rollback del origen al snapshot (tras copia de seguridad del estado actual) o clonar la réplica como dataset nuevo y conmutar el mountpoint.
3. **Zvol corrupto**: clonar `pool2/pool0-replica/iscsi/<zvol>@repl-<d>` → attach a la VM como disco nuevo (nunca sobre el original) → validar guest → conmutar.
4. **Pérdida completa de pool0**: reconstrucción de datasets desde `pool2/pool0-replica` (último snapshot común) + dumps PBS para consistencia app; Mirror vdevs dañados = reemplazo de discos (capex gated F-01) antes de importar.
5. **Pérdida completa de TrueNAS/chasis**: **pool2 NO ayuda** (mismo chasis, F-14): recuperación = reinstalar SCALE + importar pool0/pool2 si los discos sobreviven; si el chasis/discos se pierden → sólo off-site (A7/A8, bloqueado) + PBS si kronos vive. Deuda declarada, no promesa.
- Verificación post-recv de CADA sesión: exit=0 + `zfs list` destino con snapshot del día + (semanal) scrub de los datasets replicados o comparación de tamaños. Validación de restore: 1 drill con dataset de prueba en fixture antes de declarar la réplica operativa.

## 7. Gates owner (todos requeridos; una aprobación general NO sustituye gates)

- **G-REP-1**: scrub pool2 previo OK (0 errores) — ventana propia, no solapa con G1B/fulls.
- **G-REP-2**: confirmación del alcance: todo pool0 (default) con la exclusión técnica de `.ix-virt`/`.system` + inclusión EXPLÍCITA de trading_systems/trading_documents (D-W3) y de frigate media.
- **G-REP-3**: ventana para la 1ª transferencia completa (~2,57T; 8-12h estimadas a HDD; presupuesto de I/O exclusivo: sin G1B/fulls/migraciones sobre TrueNAS ese día; propuesta: madrugada sábado-domingo con Echo cerrado, fuera de la ventana P0).
- **G-REP-4**: activación del schedule diario (04:45) + retención 14/14 + scrub mensual pool2.
- Rollback global: desactivar cron + destruir `pool2/pool0-replica` (destrucción = autorización independiente e irreversible, jamás en la misma operación).

## 8. Contrato con los otros flujos (sin cadenas circulares)

- PBS NO vive en pool0 ni pool2 (VM 180 en kronos) — vzdump no depende de la réplica; la réplica no depende de PBS. Único punto de contacto: G1B lee minio_data (zvol) — horarios separados + flock.
- Cloud lee de PBS/dumps (no de pool2) — cadena pool1→pool0→pool2 acíclica: pool1→pool0 es vzdump/dump→PBS→ingesta; pool0→pool2 es snapshot local.
- Si cae TrueNAS: PBS y dumps sobreviven (DR-T5); si cae kronos: réplica y pool0 sobreviven (DR-T3 mitigado por esta réplica para el dominio pool0).
