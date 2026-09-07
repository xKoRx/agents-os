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

# Servicios de red

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28

## OPNsense (qemu/130)

| Item | Valor |
|---|---|
| **Propósito** | Firewall del cluster, NAT, gateway de seguridad perimetral |
| **VMID** | 130 |
| **Tipo** | qemu VM |
| **Stack** | FreeBSD / OPNsense |
| **Nodo** | athena |
| **vCPUs** | 8 |
| **RAM** | 8 GB |
| **Disco** | 64 GB |
| **NetIn** | 1.72 TB |
| **NetOut** | **6.20 TB** ← todo el tráfico WAN |
| **Uptime** | > 136 días |
| **Estado** | 🟠 Running pero **SPOF de red** (ver alertas) |

### Alertas

- 🔴 Si athena cae → OPNsense cae → toda la red se va con él
- 🟠 Considerar HA con CARP o migración a hardware dedicado

### Source

- `/home/hermes/aranea/topology/services.md`
- `/home/hermes/aranea/topology/discovery/athena_20260628_211812.txt`

## Pi-hole (lxc/149)

| Item | Valor |
|---|---|
| **Propósito** | DNS sinkhole, ad-blocking, DNS recursivo para LAN |
| **VMID** | 149 |
| **Tipo** | lxc container |
| **Stack** | Debian + Pi-hole |
| **Nodo** | athena |
| **vCPUs** | 2 |
| **RAM** | 1 GB |
| **Disco** | 10 GB |
| **Tags** | `adblock`, `community-script` |
| **NetIn** | 128 GB |
| **NetOut** | 2.6 GB |
| **Estado** | ✅ Running |

### Source

- `/home/hermes/aranea/topology/services.md`
- `/home/hermes/aranea/topology/discovery/athena_20260628_211812.txt`

## Traefik (lxc/115)

| Item | Valor |
|---|---|
| **Propósito** | Reverse proxy HTTPS interno, integración con step-ca |
| **VMID** | 115 |
| **Tipo** | lxc container |
| **Stack** | Debian + Traefik |
| **Nodo** | athena |
| **vCPUs** | 2 |
| **RAM** | 2 GB |
| **Disco** | 16 GB |
| **Tags** | `community-script`, `proxy` |
| **NetIn** | 18 GB |
| **NetOut** | 3.2 GB |
| **Estado** | ✅ Running |

### Configuración reciente

- `certificatesResolvers.stepca` configurado (ticket `2026-06-29-006`)
- Filtros `lan-only@file` (solo IPs 192.168.31.0/24)
- Basic-auth para dashboard
- Dashboard expuesto via `dashboard.lab.aranea`

### Source

- `/home/hermes/aranea/topology/services.md`
- `/home/hermes/aranea/tickets/2026-06-29-006-configure-traefik-stepca.md`
- `/home/hermes/aranea/tickets/2026-06-29-007-expose-dashboard-via-traefik.md`

## etcd cluster (5 miembros)

| Item | Valor |
|---|---|
| **Propósito** | Almacén distribuido clave-valor, usado por Traefik, observability stack, configs |
| **Tipo** | lxc containers |
| **Stack** | etcd (go) |

| Nodo | VMID | vCPUs | RAM | Disco |
|---|---|---|---|---|
| athena | 101 | 1 | 2 GB | 18 GB |
| hera | 155 | 1 | 4 GB | 18 GB |
| zeus | 156 | 1 | 4 GB | 18 GB |
| kronos | 154 | 1 | 4 GB | 18 GB |
| hades | 147 | 1 | 4 GB | 18 GB |

**Estado**: ✅ Todos los 5 miembros running.

### UI: etcd-keeper (lxc/148)

- Corriendo en **hades** (2 vCPU, 2 GB RAM, 10 GB disco)
- Tags: (ninguno especial)
- NetIn: 8.5 GB
- NetOut: 13 MB

### Source

- `/home/hermes/aranea/topology/services.md`

---

## Resumen

| Servicio | Estado | SPOF risk |
|---|---|---|
| OPNsense | ✅ | 🔴 Sí (VM en athena) |
| Pi-hole | ✅ | 🟡 Sí (única instancia) |
| Traefik | ✅ | 🟡 Sí (única instancia) |
| etcd cluster | ✅ | ✅ Resiliente (5 miembros) |

## Alertas

- 🔴 **OPNsense como VM en athena** = SPOF de red
- 🟡 No hay Pi-hole secundario (si athena cae → DNS cae)
- 🟡 No hay Traefik secundario (si athena cae → reverse proxy cae)
- ✅ etcd tiene quórum distribuido (5/5)

---

**Source files**: `/home/hermes/aranea/topology/services.md`, `/home/hermes/aranea/topology/discovery/athena_20260628_211812.txt`, tickets `2026-06-29-006` y `2026-06-29-007`

**Captured**: 2026-06-28 21:18 UTC. Doc generado 2026-06-30.
