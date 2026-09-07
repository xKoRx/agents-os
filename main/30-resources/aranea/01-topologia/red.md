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

# Red — DNS, firewall, VLANs, servicios de red

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28 vía `agent-read all`
> **Estado**: ✅ Documentado con gaps de WireGuard y DNS zones

## 📡 Subnets del cluster

| Subnet | Propósito | Gateway | MTU | Nodos |
|---|---|---|---|---|
| 192.168.31.0/24 | LAN principal, gestión, VMs | 192.168.31.1 (router ISP) | 1500 | Todos |
| 10.10.10.0/24 | Ceph cluster network | — | 9000 (jumbo) | zeus, hera, kronos, hades |
| (interna truenas) | bond0 LAG failover | — | 1500 | truenas |

## 🛜 Firewall: OPNsense (qemu/130 en athena)

| Item | Valor |
|---|---|
| VMID | 130 |
| Tipo | qemu |
| Nodo | athena |
| vCPUs | 8 |
| RAM | 8 GB |
| Disco | 64 GB |
| NetIn acumulado | 1.72 TB |
| NetOut acumulado | **6.20 TB** ← todo el tráfico WAN |
| Uptime | > 136 días |

### Configuración (no detallada en el wrapper)

> [!warning] Estado detallado no capturado
> El wrapper `agent-read` no expone la configuración de OPNsense (rules, interfaces WAN/LAN, NAT, aliases). Para conocer el detalle se requiere acceso a la UI de OPNsense o expandir el wrapper con `pfctl` / `opnsense-cli`.

## 🔐 WireGuard / VPN

> [!warning] WireGuard no documentado
> No hay evidencia de WireGuard configurado ni en truenas ni en PVE en los archivos de discovery. Si existe está en algún host fuera del scope del wrapper. **Necesita refresh**.

## 🌐 DNS — Pi-hole (LXC 149 en athena)

| Item | Valor |
|---|---|
| VMID | 149 |
| Tipo | lxc |
| Nodo | athena |
| vCPUs | 2 |
| RAM | 1 GB |
| Disco | 10 GB |
| Tags | `adblock`, `community-script` |
| NetIn acumulado | 128 GB |
| Uptime | > 97 días |

### Función

- **Sinkhole DNS** + ad-blocking
- Sirve como DNS recursivo para la LAN

### Wildcard DNS `*.lab.aranea`

> [!note] Funcionalidad confirmada en tickets previos
> El DNS wildcard `*.lab.aranea` está validado por tickets `2026-06-29-001..007` y usado para exponer dashboards via Traefik (ej. `ca.lab.aranea`, `dashboard.lab.aranea`).

## 🔄 Reverse proxy — Traefik (LXC 115 en athena)

| Item | Valor |
|---|---|
| VMID | 115 |
| Tipo | lxc |
| Nodo | athena |
| vCPUs | 2 |
| RAM | 2 GB |
| Disco | 16 GB |
| Tags | `community-script`, `proxy` |
| NetIn acumulado | 18 GB |

### Función

- Reverse proxy HTTPS interno
- Integración con step-ca para emisión automática de certificados (ver ticket `2026-06-29-006-configure-traefik-stepca.md`)
- Filtros `lan-only@file` (solo IPs 192.168.31.0/24)
- Basic-auth para dashboard

## 🗂️ etcd cluster (5 miembros en LXC 101/154/155/156/147)

| Nodo | VMID | vCPUs | RAM | Status |
|---|---|---|---|---|
| athena | 101 | 1 | 2 GB | running |
| hera | 155 | 1 | 4 GB | running |
| zeus | 156 | 1 | 4 GB | running |
| kronos | 154 | 1 | 4 GB | running |
| hades | 147 | 1 | 4 GB | running |

> etcd es **infraestructura crítica** para servicios como Traefik, observability stack, y configuración distribuida.

### UI

- `etcd-keeper` (LXC 148 en hades) — UI web para etcd

## 🌐 Switch / VLANs (tabla)

| Subnet | VLAN ID | MTU | Trunk / Access |
|---|---|---|---|
| 192.168.31.0/24 | 1 | 1500 | access (PVID untagged) |
| 10.10.10.0/24 | 2 | 9000 | access / dedicado (jumbo frames) |

### Detalles VLAN por nodo

| Nodo | Configuración |
|---|---|
| athena | `enp4s0`: VLAN 1 PVID Egress Untagged; `bond0`: VLAN 1 PVID + 4094 tagged (range completo disponible) |
| zeus | Configuración mínima (no se muestra VLANs activos en este nodo) |
| hera | Configuración mínima |
| kronos | `vmbr0`, `ceph` separados; `enp4s0f1`: VLAN 1 PVID |
| hades | Configuración mínima |
| truenas | VLANs no aplican (es VM, ve bridges de hades) |

## 🖧 Routers / switches físicos

| Item | Estado |
|---|---|
| Router ISP / modem | `192.168.31.1` (gateway defecto de todos los nodos) |
| Switch 10GbE | Marca/modelo **❓ Necesita refresh** |
| Managed vs unmanaged | **❓ Necesita refresh** |
| Configuración VLANs | **❓ Necesita refresh** (configuración física) |
| Cableado | **❓ Necesita refresh** |

## ⚠️ Alertas / pendientes

| # | Severidad | Pendiente |
|---|---|---|
| 1 | 🟡 | Marca/modelo del switch físico no capturado |
| 2 | 🟡 | WireGuard (si existe) no documentado en la discovery |
| 3 | 🟡 | Reglas de OPNsense no accesibles vía wrapper |
| 4 | 🟡 | Configuración del router ISP no accesible desde PVE |

---

## Source files

- `/home/hermes/aranea/topology/discovery/{athena,zeus,hera,kronos,hades,truenas}_20260628_211812.txt` (secciones `ip_addr`, `ip_route`, `bridges`, `vlans`, `listeners`)
- `/home/hermes/aranea/topology/services.md`
- `/home/hermes/aranea/tickets/2026-06-29-006-configure-traefik-stepca.md`
- `/home/hermes/aranea/tickets/2026-06-29-007-expose-dashboard-via-traefik.md`

## Captured

2026-06-28 21:18 UTC. Doc generado 2026-06-30.
