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
| pool0/apps | 14,1G | SÍ | refer del propio tree; frigate media 66,7G vive en snapshots legacy pre-rebuild del jul-2025 (usados 67,3G del dataset = histéresis snapshot, no datos vivos) — exclusión OPCIONAL sólo por RC owner, por defecto va |
| pool0/trading_documents | 0,02G | SÍ | casi vacío |
| pool0/home / ix-apps | ~0G | SÍ | triviales |
| pool0/ix-applications | 10,1G | SÍ | apps TrueNAS |
| pool0/.ix-virt | 15,5G | **NO** | ISOs de instalador SCALE ×3 (4,3G) + volume `default_truenas-apps` 12,6G (Docker apps: **`app.query`=0, sin apps desplegadas** — medido 21sep) + árboles buckets/containers/deleted vacíos; restauración = re-descargar ISO / recrear dataset; sin valor de recuperación del owner |
| pool0/.system | 3,1G | **NO** | middleware system dataset real en `boot-pool/.system` (verificado `systemdataset.config`); este remanente pool0 guarda netdata RRD 455M + configs 38M + samba/nfs/cores residuales; se regenera; excluido también por el middleware (dataset oculto, no seleccionable) |
| **Total envío inicial (base `refer`)** | **2,35T** | | 2,37T de árbol vivo − 18,6G excluidos; presupuesto de diseño 2,4T |

**Ledger de cobertura (auditoría 21sep noche-3)** — `dataset | refer | inclusión | consistencia | método de recuperación`:

| dataset | refer | incl | consistencia de la copia | recuperación |
|---|---|---|---|---|
| pool0/aranea_storage | 1,09T | SÍ | file-consistent (sin app transaccional encima) | clonar snapshot destino → montar RO → copiar de vuelta |
| pool0/trading_systems | 485G | SÍ | ídem | ídem (confirmación D-W3) |
| pool0/proxmox_storage | 401G | SÍ | crash-consistent NFS (guests corriendo); prune keep-all tarea separada (WP-A0) | ídem; VM/CT individual = vzdump PBS o restore directo |
| pool0/iscsi/pg_data (zvol) | 1,25G* | SÍ | crash-consistent; PG recupera por WAL replay | clonar zvol destino → attach a VM nueva → replay → dumps G1A para punto limpio |
| pool0/iscsi/mongo_data (zvol) | 0,54G* | SÍ | crash-consistent standalone | ídem |
| pool0/iscsi/minio_data (zvol) | 50,3G | SÍ | crash-consistent | G1B manda para restore app-consistente |
| pool0/iscsi/vm-zeus-win-disk (zvol) | 193G | SÍ | crash-consistent | clonar → attach como disco nuevo, nunca sobre el original |
| pool0/iscsi/win-development (zvol) | 128G | SÍ | ídem | ídem |
| pool0/iscsi/debian-xhrvgh (zvol) | 8,8G | SÍ | ídem | ídem |
| pool0/apps (config + PG/Mongo app-datasets) | 14,1G | SÍ | file-consistent | clonar + leer |
| pool0/ix-applications | 10,1G | SÍ | file-consistent | clonar + leer |
| pool0/trading_documents + home + ix-apps | ~0G | SÍ | file-consistent | clonar + leer |
| pool0/.ix-virt | 15,5G | NO | n/a | re-descargar ISOs; `default_truenas-apps` vacío de apps (app.query=0) |
| pool0/.system | 3,1G | NO | n/a | regenerado por middleware (dataset real en boot-pool) |

\* pg_data/mongo_data: `used` (33,0/32,5G) ≫ `refer` (1,25/0,54G) porque bloques liberados en el guest siguen reservados en el zvol (refreservation 33/32,5G sobre volsize 32G — la reserva excede el volsize y el thin real usado es el refer); el envío transmite el stream actual (~GB), no los 33G históricos. `win-development` análogo (used 203G / refer 128G).

**Cobertura: 100% del contenido recuperable del árbol vivo de pool0** (todas las hojas del ledger son SÍ o NO-justificado-auditado). Con `.ix-virt`/`.system` incluidos el envío sería 2,37T (Δ +0,02T sobre el presupuesto): la exclusión es por valor de recuperación nulo, no por capacidad.

## 2. Capacidad (auditoría con aritmética verificada 21sep noche-3)

- **pool2 zpool: size 7,27T · alloc 3,19T · FREE 4,08T** (fuente: `zpool list` vía SSH — el número operativo). La vista `zfs list` AVAIL 2,15T subestima **2,05T por el histéresis de los snapshots legacy de `pool2/backup` (442 snapshots con `used`≈0: sus bloques viven en `usedbychildren` de los pares snapshot+head ya referenciados, y la raíz los vuelve a contar al propagar `usedbysnapshots` al dataset padre — aritmética ZFS, NO doble conteo de datos)**; sin quotas/reservas en ningún dataset (verificado `zfs get -r` local). **Cuando los snapshots legacy se borren (decisión owner separada), el AVAIL de la vista convergerá a ~4,2T.**
- **Errata material adicional (auditoría nocturna): el "4,18T" del martes era una lectura coetánea válida; el margen del plan usa 4,08T medido 18:23 -03 y `CAPACITY-GO` queda CERTIFICADO por aritmética de `refer`, no por el número de free.** El número relevante es: envío inicial 2,35-2,37T ≤ free 4,08T con **≥1,71T de margen post-full en el peor caso (100% del árbol replicado)**.
- Presupuesto post-1ª réplica (refer-based): 3,19T + 2,35T ≈ **5,54T alloc de 7,27T → 1,73T libres (24%)**; incluyendo `.ix-virt`/`.system`: 5,56T → 1,71T (24%). Regla de operación se mantiene: **si free < 1,00T → NO-SEND + alerta owner** (freno duro); aviso temprano < 1,50T. Los umbrales se miden sobre `zpool list`, jamás sobre la vista `zfs list`.
- Crecimiento diario: UNKNOWN (sin serie medida; primer año del dataset frigate muestra máximos ~28G/d). Plan de medición: `zpool list` diario 7 días antes de activar → la retención se ajusta con ese dato. Presupuesto defensivo hasta medir: delta diario ≤50G + retención 14 días ≈ ≤0,7T adicionales ⇒ **free post-régimen ≈1,0-1,4T: cabe, con aviso temprano activo**.
- **Espacio adicional en pool0 por los respaldos de pool1 (D-NEW-02)** — aritmética formal (auditoría): pool0 free 1,64T; capa `nfs-vmbackup` (TWO-LAYER §1, vzdump semanal keep-weekly=4 de las unidades T0 con discos en pool1) ≈ 0,43-1,03T según compresión real; snapshots `@repl-*` 14 días ≈ 0,27-1,09T según delta diario. Peor caso combinado (80G/d + 1,03T): **queda 0,12T en pool0**; escenario central (50G/d + 0,43-0,77T): 0,19-0,53T. **Ambas capas caben, pero el margen combinado es ACOTADO → orden recomendado: medir `pool0/vm-backup` real tras su primer ciclo y después fijar retención final de @repl (7 vs 14 días).** Es un orden de activación, no un bloqueo de capacidad.

## 3. Snapshots e incrementales (mecanismo)

- **Mecanismo definitivo: stack NATIVO de replicación TrueNAS 25.04.1 (plugin `replication` → motor `zettarepl`), transporte LOCAL.** Evidencia (21sep noche-3, RO): (a) `/api/v2.0/replication` responde **401 sin auth = ruta existente** (el 404 de la noche anterior fue diagnóstico defectuoso: faltaba auth, no ruta) y el middleware expone la familia completa `replication.create/query/run/restore`, `pool.snapshottask.*`, `cronjob.*`; (b) el código instalado (`plugins/replication.py:763`) declara `transport ∈ {SSH, SSH+NETCAT, LOCAL}`; (c) `replication.query=[]` y 0 cron jobs: **la API existe y no hay tareas — faltaba crear la tarea, no la API.**
- **Diseño: 1 snapshottask nativo + 1 tarea de replicación nativa encadenada** (first-party, sin scripts ni cron del owner, cero dependencia de Hermes — D-NEW-06 satisfecho con el mecanismo de mayor grado):
  - **Snapshottask** `pool.snapshottask.create`: `{dataset:"pool0", recursive:true, naming_schema:"repl-%Y-%m-%d_%H-%M", schedule:{minute:"45",hour:"4",dom:"*",month:"*",dow:"*",begin:"00:00",end:"23:59"}, lifetime_value:14, lifetime_unit:"DAY", allow_empty:false, enabled:true}` — snapshot recursivo = set atómico multi-dataset en un mismo txg. Exclusión: Plan A = campo `exclude` del snapshottask (verificar aplicación real en fixture); **Plan B garantizado** (campo confirmado en el código instalado): `exclude:["pool0/.ix-virt","pool0/.system"]` en la tarea de replicación (los snapshots fuente de esos árboles existen pero no se envían: árboles estáticos, coste ~0). Los snapshots legacy 2025 NO se tocan.
  - **Replicación** `replication.create`: `{name:"pool0-replica-diaria", direction:"PUSH", transport:"LOCAL", ssh_credentials:null, source_datasets:["pool0"], target_dataset:"pool2/pool0-replica", recursive:true, exclude:["pool0/.ix-virt","pool0/.system"], periodic_snapshot_tasks:[<id del snapshottask>], auto:true, schedule:{minute:"50",hour:"4",...}, readonly:"SET", retention_policy:"NONE", allow_from_scratch:false, enabled:true}` (retries=5 default). Validaciones leídas del código instalado: en PUSH **no** se envía `naming_schema` propio (lo aporta el snapshottask enlazado; sin tasks exigiría `also_include_naming_schema` o `name_regex`); `auto:true`+tasks+cron es la forma válida; `retention_policy:"NONE"` = la retención la manda el snapshottask en origen (14d) y una política de destino aparte (ver §3bis destino); `allow_from_scratch:false` (default) hace **fail-closed** si no hay base — jamás full implícito; `readonly:"SET"` deja el destino RO entre réplicas. **Payloads preparados, NO ejecutados** — aplicación GATED (G-REP-4), fixture primero.
- **Horario definitivo: snapshot 04:45 · réplica 04:50 -03** (5 min de colchón). Checkpoints de seguridad intactos: fuera de dumps G1A (03:00/03:20) y R1 (04:00/05:00); R2 expira 26sep sin conflicto futuro. La razón del horario 04:xx está en §4 — no se conserva por inercia: 03:30 colisiona con dumps en el peor caso, y moverla a horario diurno no reduce riesgo, solo acerca la ejecución al mercado.
- **Identificación del último snapshot común**: interna de zettarepl (deriva los incrementales de los snapshots comunes fuente/destino); nunca asume el de ayer. **Ejecución fallida/interrumpida**: la sesión queda en el último snapshot común y reintenta incremental (retries nativo + schedule siguiente) — reanudación sin full; la exclusión de solapamiento la da el runner nativo (un job por tarea).
- **Cadena perdida** (base fuera de retención en origen): zettarepl marca FAILED y `allow_from_scratch:false` impide el full automático → fallo cerrado + alerta; full re-send sólo en ventana aprobada por owner (requeriría >7 días de fallos consecutivos con retención 14d).
- **Destino**: dataset NUEVO `pool2/pool0-replica` creado como paso 0 (los árboles legacy `pool2/backup`, `pool2/pool0_backup`, `pool2/zfs_backup` quedan INTACTOS — F-09). `readonly` final del destino lo aplica la tarea vía `readonly:"SET"` (zettarepl gestiona el toggle durante recv — sin pre-set manual). **Retención destino (§3bis)**: la observación de operación vigente en `pool2/pool0_backup` fue `sync=always` (medido 21sep; HDD single-disk, dañas latencia y desgaste) — en el fixture se prueba `properties=false` (destino hereda propiedades locales de `pool2`, sync=standard) y, si el validador/recepción lo rechaza, `properties_override={"sync":"standard"}`; mantener `sync=always` sólo si nada de lo anterior funciona (excepción documentada). La retención de snapshots en destino se define con una de: (i) tarea de replicación INVERSA (PULL de retorno con `retention_policy:CUSTOM` 7d) — sólido pero añade una tarea que puede intentar enviar datos; (ii) snapshottask local en pool2 con naming `auto-*` (usa el match de naming; NO toca `@repl-*`); (iii) `cronjob` interno TrueNAS (`zettarepl destroy-equivalent`: destroy de `@repl-*` >7d) — mismo motor, superficie mínima. **Decisión entre (i)/(ii)/(iii) en el fixture, no en producción; default de diseño: (iii).**
- **Estado y visibilidad del stack nativo (para operación)**: la vista agregada de estado vive en `zettarepl.list_states` vía midclt/DDP (API WS), el histórico como jobs del middleware; el log del runner nativo queda en `/var/log/` local de TrueNAS. Consulta rápida RO equivalente: `midclt call replication.query` + `pool.snapshottask.query`.

## 4. Consistencia por workload (honestidad de la réplica)

> **Addendum auditoría 21sep noche-3 — dependencias reales del horario (reemplaza el argumento por inercia):** mapa verificado de los checkpoints de protección (timers hermes + cronograma pool0): 03:00 dumps PG · 03:20 dump Mongo (A1, I/O liviano sobre pool0) · 04:00 R1 (empaqueta el vault de hermes; NO toca TrueNAS) · 04:45 → **snapshot pool0** · 04:50 → **réplica a pool2** · 05:00 etcd snapshot · 06:05 R2 (vzdump CTs a PBS — LEE pool0 vía los rootfs NFS `proxmox_storage`, expira 26sep; sin conflicto futuro con la réplica que ya corrió 04:50). La ventana 04:45-04:50 queda libre por diseño: separada de A1 (evita snapshot mientras el dump Mongo puede seguir escribiendo su zvol) y suficientemente lejos de R1/R2. La primera transferencia completa NO corre a esta hora: va en su ventana exclusiva propia (G-REP-3) — el horario diario rige para el régimen incremental.

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

Una sesión diaria (04:45): escritura del delta diario después de la inicial; sin servicios productivos, sin apps, sin full innecesarios. Scrub: **pool2 sin scrub desde jul-2025** (último: 12jul2025, 0 errores, 07:01h — verificado vía `zpool status` y `pool.query`; la única tarea de scrub existente (id=3, semanal) apunta a pool0, scrubbed 6sep). **El servicio nativo `pool.scrub` existe y está operativo** (corrección: "sin tarea para pool2" era correcto, pero el mecanismo para crearla es nativo de primera parte). Requisito gate: (1) **scrub manual de pool2 ANTES de la primera réplica** (~7h, ventana propia) y (2) tarea de scrub MENSUAL para pool2 (`pool.scrub.create`, primer domingo 00:00) creada con la activación — nota operativa: ese domingo la réplica 04:50 corre durante la cola del scrub; contención de I/O aceptada y documentada (un día al mes; zfs serializa internamente). SMART/temperatura: alertas del middleware TrueNAS como fuente primaria (el subsistema nativo cubre scrub fallido/pool degradado; el canal de entrega queda como gate propio, G-REP-5); check semanal opcional vía `cronjob` interno: `zpool status pool2` sin errores + `smartctl` sin contadores nuevos (log local TrueNAS). Control de degradación: cualquier error de scrub o lectura → NO-SEND + alerta (no confiar la réplica a un disco degradado). No desactivar verificaciones para reducir desgaste.

## 6. Recuperación (procedimientos, resumen ejecutable en MANDATO-REPLICACION-SPEC)

1. **Archivo eliminado**: clonar `pool2/pool0-replica/<ds>@repl-<d>` en TrueNAS → montar RO → copiar de vuelta a ruta nueva; jamás sobrescribir el origen.
2. **Dataset dañado**: comparar snapshot origen vs réplica; rollback del origen al snapshot (tras copia de seguridad del estado actual) o clonar la réplica como dataset nuevo y conmutar el mountpoint.
3. **Zvol corrupto**: clonar `pool2/pool0-replica/iscsi/<zvol>@repl-<d>` → attach a la VM como disco nuevo (nunca sobre el original) → validar guest → conmutar.
4. **Pérdida completa de pool0**: reconstrucción de datasets desde `pool2/pool0-replica` (último snapshot común) + dumps PBS para consistencia app; Mirror vdevs dañados = reemplazo de discos (capex gated F-01) antes de importar.
5. **Pérdida completa de TrueNAS/chasis**: **pool2 NO ayuda** (mismo chasis, F-14): recuperación = reinstalar SCALE + importar pool0/pool2 si los discos sobreviven; si el chasis/discos se pierden → sólo off-site (A7/A8, bloqueado) + PBS si kronos vive. Deuda declarada, no promesa.
- Verificación post-recv de CADA sesión: exit=0 + `zfs list` destino con snapshot del día + (semanal) scrub de los datasets replicados o comparación de tamaños. Validación de restore: 1 drill con dataset de prueba en fixture antes de declarar la réplica operativa.

## 7. Gates owner (todos requeridos; una aprobación general NO sustituye gates)

- **G-REP-0**: fixture de validación en pool2 (workspace `pool2/fixrep` autodestruido): snapshottask+replication creados deshabilitados/en dataset de prueba, 1 ciclo real ejecutado, verificación de: exclusión Plan A vs Plan B, `properties=false` vs `sync` del destino, mecanismo de retención destino (i)/(ii)/(iii), restore drill de un dataset hijo y de un zvol. Sin fixture verificado NO hay G-REP-3/4 (clase AUTO por ser efímero y autolimitado; su creación muta pool2 → se anuncia en el bundle y se registra).
- **G-REP-1**: scrub pool2 previo OK (0 errores) — ventana propia, no solapa con G1B/fulls; ~7h (12jul2025: 3,5T en 07:01h).
- **G-REP-2**: confirmación del alcance: todo el árbol vivo de pool0 (envío base **2,35T**) con la exclusión técnica de `.ix-virt`/`.system` (justificada en el ledger §1) + inclusión EXPLÍCITA de trading_systems/trading_documents (D-W3). Nota frigate: el dataset vivo entra completo (~14,1G refer); el histórico de media (~52,9G, jul-2025) vive sólo en snapshots legacy y NO viaja (no existe en el árbol vivo — decisión implícita de alcance que el owner valida al aprobar este gate).
- **G-REP-3**: ventana exclusiva para la 1ª transferencia completa (~2,35T; 7-11h estimadas a HDD; presupuesto de I/O exclusivo: sin G1B/fulls/migraciones sobre TrueNAS ese día; propuesta: madrugada sábado-domingo con Echo cerrado, fuera de la ventana P0).
- **G-REP-4**: activación del stack nativo (snapshottask 04:45 + replication 04:50, enabled) + retención 14/7-14 + scrub mensual pool2 (`pool.scrub.create`).
- **G-REP-5**: canal de alertas del middleware (G1A dump del día → alert owner): requisito de operación autónoma (D-NEW-06) mientras no exista SMTP.
- Rollback global: deshabilitar/eliminar snapshottask+replication (`pool.snapshottask.delete` + `replication.delete`, sin tocar snapshots) + destruir `pool2/pool0-replica` (destrucción = autorización independiente e irreversible, jamás en la misma operación).

## 8. Contrato con los otros flujos (sin cadenas circulares)

- PBS NO vive en pool0 ni pool2 (VM 180 en kronos) — vzdump no depende de la réplica; la réplica no depende de PBS. Único punto de contacto: G1B lee minio_data (zvol) — horarios separados + flock.
- Cloud lee de PBS/dumps (no de pool2) — cadena pool1→pool0→pool2 acíclica: pool1→pool0 es vzdump/dump→PBS→ingesta; pool0→pool2 es snapshot local.
- Si cae TrueNAS: PBS y dumps sobreviven (DR-T5); si cae kronos: réplica y pool0 sobreviven (DR-T3 mitigado por esta réplica para el dominio pool0).
