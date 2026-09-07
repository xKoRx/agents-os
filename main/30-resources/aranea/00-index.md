---
title: Aranea — Home Lab Cluster
type: index
schema_version: 1
status: active
icon: 🕷️
slug: aranea-home
area: "[[Personal]]"
project: "[[AGENTS OS]]"
tags:
  - domain/aranea
  - domain/homelab
  - kind/index
  - area/personal
  - project/agents-os
created: 2026-06-23
updated: 2026-08-11
reviewed: 2026-06-30
aliases:
  - Aranea index
  - Cluster Aranea
  - Aranea home lab
cssclasses:
  - wide
---

# 🕷️ Aranea — Home Lab Cluster

> [!info] Resource Wiki
> Dominio activo: catálogo `00-index.md` + bitácora `log.md`. La frescura de
> inventario se controla por fuente/captura, no por actividad del log.

|> **Cluster**: 5 nodos Proxmox VE + 1 TrueNAS Scale (VM) + 1 Hermes VM = **7 máquinas**
|> **Total**: 302 threads / 767 GB RAM / ~12 TB disco útil
|> **Storage distribuido**: Ceph con 4 OSDs NVMe + TrueNAS NFS/iSCSI/SMB
>
> [!success] ✅ Frescura de los datos — al día
> **Última captura real**: **2026-06-30 19:44 UTC** vía `agent-read all` en los 6 nodos (refresh post-fix NOPASSWD).
> **Drift actual**: 0 días
> **NOPASSWD aplicado** en athena/zeus/hera/kronos/truenas/hades — `agent-read` corre vía `sudo -n` sin password. Skill: `aranea_agent_ro_inventory_refresh`.
> **Ping check 2026-06-30**: los 6 nodos responden a ICMP ✅

---

## 📊 De un vistazo

| Nodo | IP LAN | IP Ceph | Rol | CPU | Cores | RAM | Estado |
|---|---|---|---|---|---|---|---|
| **athena** | 192.168.31.10 | — | Gateway + servicios de red | i7-13620H | 16t | 16 GB | ✅ |
| **zeus** | 192.168.31.100 | 10.10.10.100 | Compute + Ceph MON/MGR/OSD.2 | Ryzen 9 5950X | 32t | 94 GB | ✅ |
| **hera** | 192.168.31.110 | 10.10.10.110 | Compute + Ceph MON/OSD.0 | 2× Xeon E5-2699 v3 | 72t | 125 GB | ✅ |
| **kronos** | 192.168.31.120 | 10.10.10.120 | Storage powerhouse + Ceph MON/MGR/OSD.1+3 | 2× Xeon E5-2698 v4 | 80t | 251 GB | ✅ |
| **hades** | 192.168.31.90 | 10.10.10.90 | **Compute-heavy (22 VMs)** | 2× Xeon E5-2697 v4 | 72t | 251 GB | ⚠️ 74% RAM |
| **truenas** | 192.168.31.91 | — | Almacenamiento compartido (VM en hades) | 2× Xeon E5-2697 v4 (virt) | 30t | 32 GB | ⚠️ turtles |
| **hermes-vm** | 192.168.31.122 | — | Agente IA (este sistema) | — | — | — | ✅ |

**Totales**: **302 threads / 767 GB RAM / 4 OSDs Ceph activos / ~55 VMs definidas / 36 running / 19 stopped**

---

## 🚨 Top 5 alertas (de `health.md`)

| # | Severidad | Alerta | Doc |
|---|---|---|---|
| 1 | 🔴 | TrueNAS corre como VM en hades — riesgo "turtles all the way down" | [[01-topologia/nodo-truenas]] |
| 2 | 🟠 | hades no contribuye a Ceph (peso 0, sin OSDs) — consumidor neto | [[01-topologia/nodo-hades]] |
| 3 | 🟠 | Ceph HEALTH_WARN — fragmentación >0.80 en osd.0/osd.2, slow ops en osd.3 | [[03-storage/ceph-pool1]] |
| 4 | 🟠 | `pool2` de truenas sin redundancia + scrub de hace 11 meses | [[03-storage/truenas-pool2]] |
| 5 | 🟠 | athena (gateway) corre como VM, OPNsense = SPOF | [[01-topologia/nodo-athena]] |

Ver detalle completo en `~/aranea/topology/health.md`.

---

## 📂 Catálogo

### [[01-topologia]] — Topología, nodos, red
| Doc | Contenido |
|---|---|
| [[01-topologia/README]] | Overview de la topología + leyenda |
| [[01-topologia/diagrama-red]] | Diagrama mermaid completo (routers, VLANs, subnets) |
| [[01-topologia/nodo-athena]] | Gateway + servicios de red |
| [[01-topologia/nodo-zeus]] | Compute + Ceph |
| [[01-topologia/nodo-hera]] | Compute + Ceph |
| [[01-topologia/nodo-kronos]] | Storage powerhouse + Ceph |
| [[01-topologia/nodo-hades]] | Compute-heavy (22 VMs, ⚠️) |
| [[01-topologia/nodo-truenas]] | TrueNAS VM (⚠️ turtles) |
| [[01-topologia/red]] | DNS, OPNsense, WireGuard, VLANs |
| [[01-topologia/fechas-captura]] | Tabla de fechas de captura por fuente |

### [[02-servicios]] — Catálogo de servicios
| Doc | Categoría |
|---|---|
| [[02-servicios/README]] | Índice por categoría |
| [[02-servicios/red]] | OPNsense, Pi-hole, Traefik, etcd |
| [[02-servicios/observabilidad]] | Prometheus/Grafana (presencia/ausencia) |
| [[02-servicios/trading]] | MT4/MT5 + broker feeds |
| [[02-servicios/ml-ia]] | sqx-ulab, echo, argus, mcps, temporal |
| [[02-servicios/bases-de-datos]] | Postgres, MongoDB, obsidian-sync |
| [[02-servicios/data-streaming]] | Kafka, Flink, EMQX |
| [[02-servicios/backup-storage]] | TrueNAS, minio |
| [[02-servicios/automation]] | homeassistant, runbooks |
| [[02-servicios/media-domotica]] | homeassistant, frigate |
| [[02-servicios/dns-tls]] | Pi-hole, step-ca |
| [[02-servicios/dashboard-hermes-agent]] | Hermes dashboard (loopback + tunnel Traefik) |
| [[02-servicios/misc-otros]] | El resto |

### [[03-storage]] — Inventario de almacenamiento
| Doc | Contenido |
|---|---|
| [[03-storage/README]] | Overview con tabla de capacidad |
| [[03-storage/ceph-pool1]] | Pool Ceph RBD (75% usado) |
| [[03-storage/truenas-pool0]] | Pool TrueNAS principal (4 mirrors + special) |
| [[03-storage/truenas-pool2]] | Pool TrueNAS bulk (sin redundancia ⚠️) |
| [[03-storage/nfs-shares]] | Exports NFS |
| [[03-storage/smb-shares]] | Shares SMB |
| [[03-storage/iscsi-target]] | Target iSCSI |
| [[03-storage/datasets]] | Per-dataset breakdown |
| [[03-storage/inventory]] | Storage landscape raw/used/free |
| [[03-storage/DESIGN-PROPOSAL]] | ⚠️ DEPRECATED 2026-07-01 — ver backup-dr/BACKUP-DR-DESIGN. Histórico iter 1-4. |
| [[03-storage/PROPUESTA-COMPLETA-ITER4]] | ⚠️ DEPRECATED 2026-07-01 — consolidación previa. |
| [[03-storage/backup-dr/00-index]] | **NUEVO 2026-07-01** — set completo refactor (16 archivos, 140 KB) |
| [[03-storage/backup-dr/BACKUP-DR-DESIGN]] | **NUEVO** — diseño final, capas A-G, decisiones congeladas, modelo policy/runbook/skill |
| [[../../10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/BACKUP-DR-OWNER-PROJECT]] | **MOVIDO 2026-07-02** — proyecto owner + mapa subproyectos agente. Ubicación vigente: `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/`. |
| [[../../10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/agent-project-00]] a [[../../10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/agent-project-08]] | **MOVIDO 2026-07-02** — 9 subproyectos agente (cleanup, configs, PBS, app-consistent, cloud crit, cloud bulk, observability, drills, closeout). Ubicación vigente: `10-projects/Aranea/BACKUP-DR-OWNER-PROJECT/agentes/`. |
| [[03-storage/backup-dr/BACKUP-DR-RUNBOOK]] | **NUEVO** — verdad operacional, comandos paso a paso |
| [[03-storage/backup-dr/BACKUP-DR-CHECKLIST]] | **NUEVO** — pre/post/mes/trimestral/drill |
| [[03-storage/backup-dr/backup-policy]] | **NUEVO** — policy ejecutable (cambios solo via Request Change) |
| [[03-storage/backup-dr/backup-inventory-template]] | **NUEVO** — template JSON Schema |
| [[03-storage/backup-dr/REQUEST-CHANGES]] | **NUEVO** — workflow evolución controlada |
| [[03-storage/TOPOLOGY-AUDIT]] | Auditoría crítica topológica (10 hallazgos) |
| [[03-storage/AUDIT]] | Auditoría storage previa |
| [[03-storage/BACKUP-SYSTEM]] | Task 2 previa (políticas detalladas) |

### [[04-backups]] — Reservado (Task 2)
Vacío. La auditoría profunda de storages + diseño de sistema de backup va en la **siguiente tarea** (ticket `2026-06-30-011`).

### [[05-tickets]] — Tickets del sistema
| Doc | Contenido |
|---|---|
| [[05-tickets/README]] | Índice de todos los tickets |
| 11 tarjetas | Una por ticket (9 cerrados + 2 en curso) |

### [[06-diagramas]] — Diagramas visuales
| Doc | Contenido |
|---|---|
| [[06-diagramas/topologia-completa]] | Mermaid: routers, switches, VLANs, Ceph, storage |

### Runbooks transversales
| Doc | Contenido |
|---|---|
| [[ARANEA_RUNBOOK_MIGRACION_HTTPS_TRAEFIK]] | Migración incremental de servicios internos a HTTPS mediante Traefik, con validación por servicio. |

---

## 🛣️ Roadmap de gaps (necesita refresh / intervención humana)

| # | Gap | Acción |
|---|---|---|
| ~~1~~ | ~~SSH + sudo NOPASSWD para `agent_ro` no aplicado en 5/6 nodos~~ | ✅ **Resuelto 2026-06-30** — owner aplicó NOPASSWD controlado en los 6 nodos. Skill `aranea_agent_ro_inventory_refresh`. |
| ~~2~~ | ~~Inventario con drift de 2 días~~ | ✅ **Resuelto 2026-06-30** — refresh ejecutado post-fix. Ver `fechas-captura.md`. |
| 3 | Auditoría profunda de storages | ✅ **Resuelto (diseño)** — propuesta en `03-storage/DESIGN-PROPOSAL.md`, ticket `2026-06-30-013`. Anomalías topológicas en `03-storage/TOPOLOGY-AUDIT.md`. **Pendiente aprobación owner.** |
| 4 | Diseño de sistema de backup | ✅ **Resuelto (diseño)** — propuesta en `03-storage/DESIGN-PROPOSAL.md`, ticket `2026-06-30-013`. Implementación operativa queda en Fases 1-4 (**pendiente aprobación**). |
| 5 | Detalle por VM/LXC (snapshots, configs) | El wrapper `agent-read` no expone `vm <vmid> config` todavía — ver [[02-servicios/misc-otros]] § pendientes |
| 6 | Observabilidad unificada | No existe stack Prometheus/Grafana centralizado. Solo `docker-observability` en hades |

---

## 🔄 Cierre de sesión 2026-06-30 — handover

> **Status**: sesión cerrada limpiamente. Owner revisará propuesta en otra sesión. Todo el trabajo está persistido y enlazado.

### 🎯 Lo que se logró hoy (4 hitos)

| # | Hito | Evidencia |
|---|---|---|
| 1 | **Inventario refrescado y sincronizado** (drift 0d) | 6 archivos `discovery/<nodo>_20260630_194423.txt` (~1 MB total). NOPASSWD validado 6/6. |
| 2 | **NOPASSWD controlado aplicado en 6 nodos** (gap #1 cerrado) | Ticket `2026-06-30-012`. Skill `aranea_agent_ro_inventory_refresh` creada. |
| 3 | **Propuesta de storage + backup completa** (gaps #3-4 cerrados-diseño, capex $0) | `03-storage/DESIGN-PROPOSAL.md` (31 KB, 12 secciones). Ticket `2026-06-30-013` iter 3. |
| 4 | **Auditoría crítica topológica** (10 anomalías) | `03-storage/TOPOLOGY-AUDIT.md` (11 KB). Anomalías separadas del scope de backup para visibilidad. |

### 📂 Documentos clave para revisar (links visuales)

#### 🎯 Empezar por aquí (resumen ejecutivo)

- **[[30-resources/aranea/03-storage/DESIGN-PROPOSAL|DESIGN-PROPOSAL.md]]** ← propuesta principal de backup (capex $0)
- **[[30-resources/aranea/03-storage/TOPOLOGY-AUDIT|TOPOLOGY-AUDIT.md]]** ← anomalías topológicas (10 hallazgos)

#### 🛠️ Tickets activos

- **[[30-resources/aranea/05-tickets/2026-06-30-012-unlock-agent-ro-nopasswd|2026-06-30-012]]** — NOPASSWD aplicado (cerrado)
- **[[30-resources/aranea/05-tickets/2026-06-30-013-storage-redesign-backup-design|2026-06-30-013]]** — propuesta de storage + backup (iter 3, pendiente aprobación)

#### 📚 Contexto histórico

- **[[30-resources/aranea/03-storage/BACKUP-SYSTEM|BACKUP-SYSTEM.md]]** — Task 2 previa (políticas detalladas)
- **[[30-resources/aranea/03-storage/AUDIT|AUDIT.md]]** — auditoría storage previa
- **[[30-resources/aranea/03-storage/inventory|inventory.md]]** — landscape storage
- [[../01-topologia/fechas-captura|fechas-captura.md]] — drift table (0 días al cierre)

#### 📄 Propuesta consolidada para revisión externa (2026-07-01)

- **[[30-resources/aranea/03-storage/PROPUESTA-COMPLETA-ITER4|PROPUESTA-COMPLETA-ITER4.md]]** ← doc standalone 33 KB, escrito para que el owner lo revise con una IA especialista en backup.

#### 🧠 Skill operativa

- `aranea_agent_ro_inventory_refresh` ← en `~/.hermes/profiles/ariadna/skills/devops/`. Refresca inventario periódicamente.

### ⚠️ Restricciones del owner aplicadas (no negociables)

1. **NO comprar HW nuevo** — usar solo lo que hay.
2. **NO migrar TrueNAS a bare-metal** — hades se queda como hypervisor de truenas.
3. **NO cambiar cantidad de servidores** — 5 Proxmox + truenas-vm-en-hades + hermes-vm = el set estable.

### ✅ 5 decisiones pendientes del owner (próxima sesión)

1. **PBS datastore**: ¿`local-kronos` (680 GB SSD) o `pool-kronos` (730 GB SSD)?
2. **PBS RAM**: ¿8 GB o 16 GB para la VM PBS?
3. **Cloud weekly**: ¿ambos (pcloud + GDrive) o uno principal?
4. **`pool0_backup` actual** (dentro de pool2): ¿migrar a kronos pool1 o dejar como está?
5. **vm 123 (`sqx-ulab-hera-0`)**: ¿se usa en el futuro? (decisión bloquea Fase 2)

### 🛣️ Roadmap de implementación (5 fases, todas $0)

```
Fase 0 (esta semana)        → scrub pool2, ceph compact, sanoid config
Fase 1 (~1 día)             → VM PBS en kronos sobre SSD libre
Fase 2 (~medio día)         → ZFS recv en hera (requiere destruir vm 123)
Fase 3 (~medio día)         → rclone crypt sobre pcloud + GDrive
Fase 4 (~medio día)         → pool2 marcado como stage + scrub mensual
Fase 5 (continuo)           → restore drills mensuales
```

### 🎓 Lecciones aprendidas (para próxima sesión)

1. **`agent-read` puede NO profundizar jerarquías ZFS/by-id** — `sdf` aparecía sin zfs_member pero estaba en pool0 mirror-0. **Siempre validar con `zpool status -v` antes de asumir disco libre.**
2. **`zpool get spare` NO es válido en ZFS** — spares son vdev type, no property. Usar `zpool status -v`.
3. **Antes de proponer "comprar X"**, listar TODOS los recursos existentes. Owner parte del principio "no compre nada, reorganice".
4. **Cuando owner corrige alcance**, reescribir propuesta completa, no patchear menciones.
5. **Auditar anomalías CON DATOS** (VMs stopped con RAM asignada, SSD consumer corriendo VMs, single-disk sin mirror) y **FLAGEAR explícitamente**, aunque estén fuera del scope principal.

### 📊 Métricas de la sesión

- **6 tickets** cerrados/creados en sesión.
- **3 docs nuevos** creados (DESIGN-PROPOSAL, TOPOLOGY-AUDIT, ticket 013 iter 3).
- **7 docs actualizados** (00-index, 01-topologia/nodo-hades, 01-topologia/fechas-captura, 03-storage/inventory, 05-tickets/README, 20-areas/Aranea, known-error).
- **1 skill nueva** creada (`aranea_agent_ro_inventory_refresh`).
- **~50 KB de documentación** producida.
- **$0 capex**, **$0 opex mensual**.

### ⏸️ Lo que NO se hizo (esperando input del owner)

- ❌ Ningún comando ejecutado en nodos remotos (excepto refresh inventario + validación NOPASSWD, autorizado).
- ❌ Ningún pool ZFS modificado.
- ❌ Ninguna VM destruida.
- ❌ Ningún HW comprado.
- ❌ Ningún rclone/PBS/sanoid configurado.

---

## ⚡ Quick commands

```bash
# Inventario rápido de un nodo (requiere NOPASSWD aplicado)
ssh -i ~/.ssh/agent_ro_aranea -o IdentitiesOnly=yes agent_ro@<ip> \
  'sudo -n /usr/local/sbin/agent-read all'

# Solo Ceph health
ssh agent_ro@kronos 'sudo -n /usr/local/sbin/agent-read ceph_health'

# Ver VMs de un nodo
ssh agent_ro@<nodo> 'sudo -n /usr/local/sbin/agent-read pve_resources'

# Estado TrueNAS
ssh agent_ro@192.168.31.91 'sudo -n /mnt/pool0/.agent_ro/bin/agent-read all'
```

---

## Source files

- `/home/hermes/aranea/topology/README.md`
- `/home/hermes/aranea/topology/services.md`
- `/home/hermes/aranea/topology/health.md`
- `/home/hermes/aranea/topology/00-access.md`
- `/home/hermes/aranea/topology/nodes/truenas.md`
- `/home/hermes/aranea/topology/nodes/README.md`
- `/home/hermes/aranea/topology/discovery/{athena,zeus,hera,kronos,hades,truenas}_20260628_211812.txt` (superseded)
- `/home/hermes/aranea/topology/discovery/{athena,zeus,hera,kronos,hades,truenas}_20260630_194423.txt` (primaria)
- `/home/hermes/aranea/tickets/` (13 tickets)
- `~/.hermes/profiles/ariadna/skills/devops/aranea_agent_ro_inventory_refresh/SKILL.md`

## Captured

**2026-06-30 19:44 UTC** vía `agent-read all` ejecutado en los 6 nodos (snapshot fresco, drift 0d). NOPASSWD controlado aplicado por owner en los 6 nodos. Sesión cerrada el **2026-06-30** con handover completo (ver § "Cierre de sesión — handover" arriba).

**Iteraciones de la propuesta de backup**:
- Iter 1: capex ~$650 USD (rechazada)
- Iter 2: capex $0, asumía `sdf` spare (rechazada al validar)
- Iter 3: capex $0, Plan B definitivo (acepta pool2 single disk + off-host priorizado) ← vigente
