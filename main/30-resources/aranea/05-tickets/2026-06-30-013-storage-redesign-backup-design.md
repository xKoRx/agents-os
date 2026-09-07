---
type: action
schema_version: 1
project:
status: done
created: 2026-08-10
updated: 2026-08-10
tags:
  - kind/action
  - area/aranea
---

## Descripción

Registro histórico de ejecución para [[Aranea]].

## Checklist

- [x] Resultado histórico preservado

---
id: 2026-06-30-013
title: "Storage redesign + backup design proposal — SUPERSEDED por refactor backup-dr/"
type: action
schema_version: 1
status: canceled
status_detail: "Superseded 2026-07-01 por [[../../03-storage/backup-dr/BACKUP-DR-DESIGN]] (refactor completo, 16 archivos, decisiones congeladas, modelo policy/runbook/skill). Este ticket queda como histórico del journey iter 1-4. Implementación futura se trackea en nuevos tickets (018+) por subproyecto agente."
severity: high
icon: 🎫
slug: 2026-06-30-013-storage-redesign-backup-design
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-06-30
updated: 2026-08-10
closed:
owner: me
author: ariadna
aliases:
  - ticket 013
  - ticket storage-redesign
tags:
  - kind/action
  - area/personal
  - project/agents-os
  - action/ticket
related:
  - "[[2026-06-30-011-aranea-storage-audit-backup]]"
  - "[[2026-06-30-012-unlock-agent-ro-nopasswd]]"
  - "[[2026-06-30-010-aranea-full-docs]]"
  - "[[../../03-storage/DESIGN-PROPOSAL]]"
  - "[[../../03-storage/PROPUESTA-COMPLETA-ITER4]]"
  - "[[../../03-storage/backup-dr/BACKUP-DR-DESIGN]]"
  - "[[../../03-storage/backup-dr/00-index]]"
  - "[[../../03-storage/TOPOLOGY-AUDIT]]"
  - "[[../../03-storage/BACKUP-SYSTEM]]"
  - "[[../../03-storage/AUDIT]]"
---

# 2026-06-30-013 — Storage redesign + backup design proposal (RECALIBRADO)

## Descripción

Diseñar el rediseño de storage y Backup/DR; esta acción histórica fue supersedida por el diseño canónico bajo `backup-dr/`.

## Checklist

- [-] Acción cancelada por supersesión explícita; conservar la nota como evidencia histórica del journey iterativo.

## Cambio de alcance (2026-07-01, cuarta iteración)

**Nueva restricción crítica del owner**: los 3 SSDs `local-sqx-{zeus,hera,kronos}` (931 GB × 3 = ~2.8 TB SSD SATA WD Green) son **SAGRADOS** — dedicados a las VMs `sqx-ulab-{zeus,hera,kronos}-*` que son la infraestructura de **Echo Forge** (SQX Adaptive E2E Pipeline — fábrica de estrategias de trading).

**Contexto**:
- Las VMs SQX están en mantenimiento actualmente (4 de 5 stopped), pero cuando operen consumirán ~80% de los recursos de su host (kronos, hera, zeus) para generación y optimización de estrategias con StrategyQuant X.
- SQX = StrategyQuant X = builder de estrategias de trading (parte del stack Echo).
- Echo Forge es el programa de software (Go + Java + Python) que orquesta SQX → WFM → MT5 demo → Echo Core (vía API).

**Implicancia**: la Fase 2 original ("destruir VG `local-sqx-hera` para hacer `zfs recv`") queda **DESCARTADA**. Los 3 SSDs son intocables para cualquier rol que no sea SQX.

**Solución adoptada**: el plan queda **PBS off-host (kronos) + cloud tier dual segregado**. Sin capa on-cluster `zfs recv` por ahora. Si en el futuro se reactiva, el candidato es `pool-kronos` (730 GB libre, NO es SQX).

**Cambios en política cloud (owner 2026-07-01)**:
- **pcloud (1 TB)**: tier caliente, SOLO configs críticas, dumps DB, secretos. NO bulk.
- **GDrive (varios TB)**: tier bulk, snapshots ZFS pool0 (`zfs send` → archivo `.zfs`), archive mensual.

**Decisiones resueltas iter 4**:
1. PBS datastore = `local-kronos` (680 GB SSD libre)
2. PBS RAM = 8 GB (default mínimo)
3. Cloud weekly = dual segregado (pcloud critical + GDrive bulk)
4. `pool0_backup` (en pool2) = dejar como está
5. vm 123 (`sqx-ulab-hera-0`) = NO TOCAR (SQX sagrados)
6. Pool1 (Ceph) backup externo = NO (3× replication + vzdump PBS ya cubren)

**Decisiones nuevas pendientes**:
- ¿Reactivar Fase 2 con `pool-kronos` (730 GB libre) como destino `zfs recv`? Hoy no es crítico.
- Optimización de espacio en backups (owner pidió "algo media tricky") — opciones en DESIGN-PROPOSAL § 3e.

## Cambio de alcance (2026-06-30, tercera iteración)

**Validación `sdf1` completada por owner**: el `zpool status -v` ejecutado en truenas el 2026-06-30 confirma que **`sdf` NO es spare de ZFS — está como `mirror-0` de pool0** junto con `sdc`. Los 8 SSDs SATA de hades (sda-sdh) están todos usados en los 4 mirrors de pool0.

**Implicancia**: el "Plan A — mirror pool2 con `sdf`" propuesto en la segunda iteración es **inviable** sin romper pool0. **No hay disco físico libre en hades para mirror de pool2**.

**Solución adoptada**: **Plan B definitivo** — aceptar pool2 como single disk + fortalecer off-host (PBS + cloud). NO se crean pools nuevos en corto plazo.

**Lo que esto descarta de la segunda iteración**:
- ❌ Fase 4 original "mirror pool2 con `sdf1`" → **fuera, no aplica**
- ❌ Validación de `sdf1` como pendiente → **resuelto**

**Lo que queda en pie** (igual que segunda iteración):
- ✅ PBS en VM kronos sobre SSD SATA libre (existente)
- ✅ Tier cloud con pcloud + GDrive existentes
- ✅ Reuso de `local-sqx-hera` (931 GB SSD libre) como destino `zfs recv`
- ✅ Política unificada sanoid + PBS + rclone crypt

## Restricciones del owner (sin cambios)

1. **NO comprar HW nuevo**. Usar solo lo que hay.
2. **NO migrar TrueNAS a bare-metal** en otro host. hades sigue como hypervisor de truenas.
3. **NO cambiar cantidad de servidores**. 5 Proxmox + truenas-vm-en-hades + hermes-vm.

## Goal original

Resolver los **gaps #3 (auditoría storage)** y **#4 (diseño backup)** del roadmap Aranea (`30-resources/aranea/00-index`), extendiendo Task 2 con:
1. Investigación de buenas prácticas (3-2-1, PBS, ZFS send/recv, tier cloud).
2. Propuesta de uso físico de recursos (slots PCIe, topología por nodo).
3. Reestructuración de pools TrueNAS.
4. Tier cloud con pcloud + GDrive.

## Entregable

**[[30-resources/aranea/03-storage/DESIGN-PROPOSAL]]** — 31 KB, 12 secciones, propuesta completa con:

- TL;DR de 1 página (5 puntos)
- Investigación buenas prácticas (3-2-1, herramientas, Ceph/ZFS considerations)
- Recursos reales medidos (snapshot 2026-06-30 19:44 UTC)
- **Tabla de recursos libres** que SÍ alcanzan para backup sin comprar nada:
  - `local-kronos` 680 GB SSD libre
  - `pool-kronos` 730 GB SSD libre
  - `local-sqx-hera` 931 GB SSD libre
  - `sdf1` hades 931 GB (verificar si spare)
  - pcloud ~1 TB
  - Google Drive 1-5 TB
- Recomendación uso recursos físicos (slots PCIe, topología por nodo)
- Reestructuración pools TrueNAS (Plan A si `sdf` libre / Plan B si no)
- Tier cloud (pcloud + GDrive con `rclone crypt` AES-256, $0 mensual)
- Política backup consolidada (sanoid + PBS + rclone)
- Topología objetivo
- Antes/después
- **Roadmap implementación en 5 fases, todas $0**
- Riesgos y mitigaciones (incluye "hades SPOF aceptado por owner")

### Hallazgo crítico (validado por owner 2026-06-30)

**`sdf` NO es spare** — está en `pool0 mirror-0` junto con `sdc`. Los 8 SSDs SATA de hades (sda-sdh) están todos usados en los 4 mirrors de pool0. **No hay disco físico libre en hades para mirror de pool2 sin romper pool0**.

### Hallazgos clave (medidos en snapshot fresco)

### Storage actual

- **Ceph pool1**: 3.6 TiB raw, 2.1 TiB usados (75% pool). HEALTH_WARN por fragmentación BlueStore. 4 OSDs NVMe en zeus/hera/kronos × 2. hades weight 0.
- **TrueNAS pool0**: 4.48 TB raw mirror SSD (4 vdevs + special), 2.49 TB usado (57%). OK.
- **TrueNAS pool2**: 7.99 TB **single disk HDD**, 3.51 TB usado. Sin redundancia. Scrub 11 meses.
- **`local-sqx-hera` (931 GB)**: completamente libre (vm 123 stopped).
- **`local-kronos` (931 GB, ~680 GB libre) + `pool-kronos` (954 GB, ~730 GB libre)**: candidatos PBS.

### Hallazgo crítico: **`sdf` en hades**

- hades tiene 8 SSDs SATA (sda-sdh) + 1 HDD (sdi) + 2 NVMe special (nvme0n1, nvme1n1) + 1 NVMe boot (nvme2n1).
- pool0 usa **7 de los 8 SSDs** en 4 mirror vdevs. **`sdf` queda fuera** (su partición `sdf1` aparece como `zfs_member` pero **NO aparece en `zpool_status` de truenas** → probable spare o asignación oculta).
- **Si `sdf1` está realmente libre/spare** → puede usarse como mirror de pool2 (convierte single disk peligroso en mirror SSD).
- **Si no está libre** → Plan B: pool2 queda como single disk, batch se hace en kronos/hera.

**Acción requerida antes de Fase 4**: ejecutar en truenas:
```bash
ssh root@192.168.31.91
zpool status -v
zpool get spare pool2
zpool history pool2 | tail -50
ls -la /dev/disk/by-id/ | grep -i sdf
```

### Hallazgo crítico previo (descartado tras validación)

- **Falsa alarma sobre `sdf`**: la propuesta inicial asumía que `sdf1` (931 GB SSD en hades) era spare ZFS libre y podía usarse como mirror de pool2. **El `zpool status -v` ejecutado en truenas el 2026-06-30 confirma que NO** — `sdf` ya está como `mirror-0` de pool0.

### Diagnóstico crítico

1. **No existe off-host real** (todo en hades → si hades cae, todo muere — **aceptado por owner**).
2. **No existe off-site** (no hay DR para terremoto/incendio).
3. **pool2 single disk** es punto único de fallo del backup actual. **Sin forma de mirror sin comprar o romper pool0** — se mitiga con off-host (PBS + cloud).
4. **PBS no implementado** (vzdump a NFS, sin dedup).

### Recursos disponibles (sin comprar nada) — actualizado

| Recurso libre | Tamaño | Tipo | Uso propuesto |
|---|---|---|---|
| `local-kronos` libre | 680 GB | SSD SATA | **Datastore PBS** |
| `pool-kronos` libre | 730 GB | SSD SATA | Datastore PBS alternativo |
| `local-sqx-hera` libre | 931 GB | SSD SATA | Destino `zfs recv` desde truenas |
| ~~`sdf1` hades~~ | ~~931 GB~~ | ~~SSD SATA~~ | ❌ NO LIBRE — está en pool0 mirror-0 |
| pcloud | ~1 TB | cloud oficial | Tier caliente weekly |
| Google Drive | 1-5 TB | cloud oficial | Tier archivo monthly |
| RAM kronos | ~200 GB libre | DDR | VM PBS 8-16 GB |

**Total disponible para backup sin comprar**: ~2.3 TB SSD on-cluster + 1-6 TB cloud. **Más que suficiente**.

### Capex

**$0 one-time** · **$0 mensual** (usas espacio cloud ya contratado).

## Decisiones pendientes del owner (iter 4, actualizado)

### ✅ Resueltas iter 4 (2026-07-01)

1. **PBS datastore**: `local-kronos` (680 GB SSD libre, Samsung 870 QVO).
2. **PBS RAM**: 8 GB.
3. **Cloud weekly**: dual segregado (pcloud=critical, GDrive=bulk).
4. **`pool0_backup` actual** (dentro de pool2): dejar como está, no migrar.
5. **vm 123 (`sqx-ulab-hera-0`)**: NO TOCAR. Las 3 VMs SQX son productivas y los SSDs `local-sqx-*` son SAGRADOS (infraestructura Echo Forge).
6. **Pool1 (Ceph) backup externo**: NO. 3× replication + vzdump PBS ya cubren.

### 🟡 Pendientes nuevas (2026-07-01)

7. **¿Reactivar Fase 2** usando `pool-kronos` (730 GB libre, NO es SQX) como destino `zfs recv` secundario on-cluster? Hoy PBS + cloud cubren; la respuesta puede ser "no por ahora".
8. **Optimización de espacio en backups**: owner pidió "algo media tricky". Opciones detalladas en DESIGN-PROPOSAL § 3e (PBS dedup nativa, ZFS raw + compressed, rclone --partial, excluir caches, BorgBackup/restic). Owner es dev/trading — prefiere simple y robusto. Pendiente presentarle 1-2 opciones con tradeoffs para que decida.

> **Eliminado**: validación de `sdf1` → confirmado que NO es spare (está en pool0 mirror-0).

## Fases de implementación (todas $0)

- **Fase 0 — Quick wins** (esta semana): `zpool scrub pool2`, `ceph osd compact`, sanoid config
- **Fase 1 — PBS en kronos** (~1 día): crear VM PBS en kronos sobre SSD SATA libre
- **Fase 2 — Destino secundario `zfs recv` en hera** (~medio día): destruir VG `local-sqx-hera`, crear ZFS pool recv
- **Fase 3 — Tier cloud** (~medio día): rclone config para pcloud + GDrive, sync jobs
- **Fase 4 — Pool2 scrub mensual + sanoid** (~medio día): marcar pool2 como stage, configurar scrub y sanoid (NO mirror — inviable sin comprar HW o romper pool0)
- **Fase 5 — Restore drills** (continuo): schedule mensual

Detalle completo en [[DESIGN-PROPOSAL]] § 9.

## Estado de gaps del roadmap

| Gap | Estado |
|---|---|
| #3 Auditoría profunda de storages | ✅ **Diseño cerrado** — pendiente ejecución |
| #4 Diseño de sistema de backup | ✅ **Diseño cerrado** — pendiente ejecución |

> Cerrar el "diseño" no es cerrar el "gap operativo". Los gaps operativos de backup real (PBS off-host, cloud tier, mirror pool2) son las Fases 1-4. Cada fase será un ticket separado cuando se apruebe.

## Lo que NO está implementado (deliberado)

- No se ha tocado ningún disco, pool, ni configuración.
- No se ha comprado HW.
- No se ha configurado rclone, PBS, ni sanoid.
- Solo se ha **escrito la propuesta** recalibrada con las restricciones del owner.

## Lo que cambió vs versión anterior del ticket

- **Tercera iteración (esta)**: Validación `sdf1` completada → NO es spare, está en pool0 mirror-0. Fase 4 original descartada. Plan B definitivo (aceptar pool2 single disk + fortalecer off-host).
- **Segunda iteración**: Recalibrado por restricciones owner (capex $0, sin migración TrueNAS, sin cambio de servidores).
- **Primera iteración**: Propuesta inicial con capex (~$650) — descartada.

## Próximo paso

Owner revisa [[DESIGN-PROPOSAL]] (iter 4, con cambios), responde las 2 decisiones nuevas pendientes (decisiones 7 y 8), y aprueba para ejecutar.

**Si aprueba**:
- **Ticket 018 — Fase 1: PBS en kronos** (~1 día): crear VM PBS sobre `local-kronos`, datastore main, user backup@pbs, registrar storage en los 5 PVE nodes, schedule vzdump.
- **Ticket 019 — Fase 3a: rclone pcloud** (~medio día): config pcloud OAuth + crypt, sync weekly de configs/dumps a `aranea-configs`.
- **Ticket 020 — Fase 3b: rclone GDrive** (~medio día): config GDrive OAuth + crypt, sync monthly de snapshots pool0 a `aranea-pool0-archive`.
- **Ticket 021 — Fase 0 (quick wins)** (~medio día): scrub pool2, ceph compact, sanoid config.

**Tickets ya abiertos de iter 3 que se mantienen abiertos** (alternativas/follow-ups):
- **015 — DNS dashboard.lab.aranea** → apunta a .122 en vez de Traefik.11. Low.
- **016 — Hermes config v31→v32**. Low.
- **017 — Dashboard healthcheck script+cron**. Low.

Tickets 014 (dashboard recovery) ya cerrado.

## Referencias

- [[DESIGN-PROPOSAL]] — propuesta completa recalibrada
- [[BACKUP-SYSTEM]] — Task 2 previa
- [[AUDIT]] — auditoría storage
- [[inventory]] — landscape completo
- `aranea_agent_ro_inventory_refresh` — skill de refresh inventario
