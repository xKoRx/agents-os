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

# Observabilidad

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28

> [!warning] Stack de observabilidad fragmentado
> No hay stack centralizado unificado Prometheus + Grafana a nivel cluster. Solo existen stacks parciales en docker-observability y docker-monitoreo.

## docker-observability (lxc/127)

| Item | Valor |
|---|---|
| **Propósito** | Stack de monitoreo dockerizado (15 GB RAM) |
| **VMID** | 127 |
| **Tipo** | lxc container |
| **Nodo** | hades |
| **vCPUs** | 6 |
| **RAM** | 15 GB |
| **Disco** | 25 GB |
| **Tags** | `base`, `docker` |
| **NetIn** | 209 GB |
| **Estado** | ✅ Running |

> Stack interno — no documentado qué herramientas exactas (Prometheus/Grafana/Loki/InfluxDB/Telegraf). **Necesita refresh el 2026-06-30+** con introspección.

## docker-monitoreo (lxc/132)

| Item | Valor |
|---|---|
| **Propósito** | Stack monitoreo dockerizado (4 GB RAM, stopped) |
| **VMID** | 132 |
| **Tipo** | lxc container |
| **Nodo** | hera (stopped) |
| **vCPUs** | 2 |
| **RAM** | 4 GB |
| **Disco** | 10 GB |
| **Tags** | `base`, `docker` |
| **Estado** | ⏸️ **Stopped** |

> Si se reactiva podría complementar a docker-observability.

## Presencia de componentes comunes (estado inferido)

| Componente | ¿Instalado en docker-observability? | ¿En truenas (SNMP)? | Notas |
|---|---|---|---|
| Prometheus | ❓ no confirmado | ❌ | No hay SNMP en truenas (`snmp STOPPED`) |
| Grafana | ❓ no confirmado | ❌ | |
| Loki | ❓ no confirmado | ❌ | |
| Promtail / Fluentd | ❓ no confirmado | ❌ | |
| Node exporter | ❓ no confirmado | ❌ | |
| Netdata | ❌ | ✅ local en truenas (`6999/loopback`) | Solo loopback en truenas |
| cAdvisor | ❓ no confirmado | ❌ | |

> [!warning] Telemetría SNMP off
> truenas tiene `snmp STOPPED`. No hay telemetría SNMP hacia监控系统 externo (LibreNMS, Zabbix, etc.). Ver [[../01-topologia/nodo-truenas]] § alertas.

## Netdata en truenas (solo loopback)

- Servicio `netdata` activo en truenas
- Escucha en `127.0.0.1:6999`
- No es remotamente accesible
- Editable vía `/etc/netdata/netdata.conf` (bind a 0.0.0.0 + firewall) — propuesto en `health.md`

## Métricas Ceph (accesibles via CLI en los nodos Ceph)

- `ceph_status`, `ceph_health`, `ceph_osd_tree`, `ceph_df`, `ceph_pool_list` son secciones del wrapper `agent-read`
- Disponibles en los 3 nodos Ceph (zeus, hera, kronos)
- **No integradas** con Prometheus todavía

## Métricas Proxmox

- Accesibles via API REST PVE (`https://<nodo>:8006/api2/json/...`)
- pvestatd + pveproxy daemon en cada nodo
- **No integradas** con stack centralizado

## Acciones recomendadas (de health.md §6)

```bash
# Implementar stack unificado Prometheus + Grafana que consuma:
# - SNMP de truenas (activar primero)
# - Ceph metrics vía mgr module (prometheus plugin)
# - Proxmox API (pve-exporter)
# - node_exporter en cada PVE node
```

## Alertas

| Severidad | Alerta |
|---|---|
| 🟡 | Stack de observabilidad fragmentado y no unificado |
| 🟡 | SNMP off en truenas → sin telemetría externa |
| 🟡 | Netdata solo loopback en truenas → no agregable |
| 🟡 | docker-monitoreo stopped → capacidad desaprovechada |

---

**Source files**: `/home/hermes/aranea/topology/services.md`, `/home/hermes/aranea/topology/health.md`, `/home/hermes/aranea/topology/discovery/hades_20260628_211812.txt`

**Captured**: 2026-06-28 21:18 UTC. Doc generado 2026-06-30.
