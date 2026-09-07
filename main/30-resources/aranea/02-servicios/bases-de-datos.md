---
type: doc
schema_version: 1
status: active
area: "[[Aranea]]"
related: []
aliases: []
tags:
  - kind/doc
created: 2026-08-10
updated: 2026-08-10
---

# Bases de datos

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28

## Producción

### postgresql (qemu/152)

| Item | Valor |
|---|---|
| **Propósito** | Base de datos relacional principal |
| **VMID** | 152 |
| **Tipo** | qemu VM |
| **Nodo** | hades |
| **vCPUs** | 8 |
| **RAM** | 24 GB |
| **Disco** | 20 GB |
| **NetIn** | 780 GB |
| **NetOut** | 677 GB |
| **Estado** | ✅ Running |

> DB activa con mucho tráfico. Si hades cae → DB caída.

### mongodb (qemu/153)

| Item | Valor |
|---|---|
| **Propósito** | Base de datos documental |
| **VMID** | 153 |
| **Tipo** | qemu VM |
| **Nodo** | hades |
| **vCPUs** | 8 |
| **RAM** | 24 GB |
| **Disco** | 20 GB |
| **NetIn** | 3.5 GB |
| **NetOut** | 1.1 GB |
| **Estado** | ✅ Running |

## Desarrollo (stopped)

### docker-mongodb-local (lxc/121)

| Item | Valor |
|---|---|
| **Propósito** | MongoDB local para dev |
| **VMID** | 121 |
| **Tipo** | lxc container |
| **Nodo** | hera |
| **vCPUs** | 6 |
| **RAM** | 20 GB |
| **Disco** | 10 GB |
| **Tags** | `docker` |
| **Estado** | ⏸️ **Stopped** |

### docker-postgres-local (lxc/122)

| Item | Valor |
|---|---|
| **Propósito** | Postgres local para dev |
| **VMID** | 122 |
| **Tipo** | lxc container |
| **Nodo** | hera |
| **vCPUs** | 8 |
| **RAM** | 17 GB |
| **Disco** | 10 GB |
| **Tags** | `docker` |
| **Estado** | ⏸️ **Stopped** |

## Sincronización Obsidian (CouchDB)

### obsidian-sync (lxc/116)

| Item | Valor |
|---|---|
| **Propósito** | CouchDB para sincronización del vault de Obsidian |
| **VMID** | 116 |
| **Tipo** | lxc container |
| **Nodo** | hades |
| **vCPUs** | 2 |
| **RAM** | 2 GB |
| **Disco** | 64 GB (del cual ~2 GB usados) |
| **Tags** | `community-script`, `database` |
| **NetIn** | 2.9 GB |
| **NetOut** | 1.5 GB |
| **Estado** | ✅ Running |

> [!warning] SPOF de Obsidian sync
> `obsidian-sync` está en **hades**. Si hades cae → se pierde la sincronización del vault. **Necesita refresh** — ¿debería estar en otro nodo?

## Resumen

| DB | VMID | Nodo | RAM | Status |
|---|---|---|---|---|
| PostgreSQL | 152 | hades | 24 GB | ✅ |
| MongoDB | 153 | hades | 24 GB | ✅ |
| Obsidian sync (CouchDB) | 116 | hades | 2 GB | ✅ |
| docker-mongodb-local | 121 | hera | 20 GB | ⏸️ stopped |
| docker-postgres-local | 122 | hera | 17 GB | ⏸️ stopped |

## Alertas

| # | Severidad | Alerta |
|---|---|---|
| 1 | 🔴 | **Toda la DB producción en hades** — single point of failure. PostgreSQL + MongoDB + Obsidian sync en el mismo host. |
| 2 | 🟡 | No hay replicación / DR configurada (Postgres streaming, Mongo replica set, etc.) — **necesita refresh** con introspección |
| 3 | 🟡 | Bases de datos dev en hera están stopped (20+17 GB RAM asignados pero apagados) |

## Acciones recomendadas

1. **Replicación PostgreSQL**: configurar streaming replication a otro nodo (kronos sería natural)
2. **Replica set MongoDB**: al menos 3 nodos
3. **Mover obsidian-sync** a nodo con menos carga (kronos tiene 222 GB RAM libres)
4. **Backups automatizados**: pg_dump + mongo dump → `/mnt/pool0/proxmox_storage/backups/db/`

---

**Source files**: `/home/hermes/aranea/topology/services.md`, `/home/hermes/aranea/topology/discovery/{hades,hera}_20260628_211812.txt`

**Captured**: 2026-06-28 21:18 UTC. Doc generado 2026-06-30.
