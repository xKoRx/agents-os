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

# ML / IA / Workflow

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28
> **Actualizado**: 2026-07-01 (enlaces Echo Forge + estado VMs SQX)

## sqx-ulab (5 VMs, 3 nodos)

> **StrategyQuant X (SQX) = builder de estrategias de trading algorítmico**.
> **Infraestructura dedicada al programa [[Echo Forge]]** (`[[echo-forge]]`, Go + Java + Python) — fábrica adaptativa E2E de estrategias upstream del ecosistema Echo (SQX → WFM → MT5 demo → Echo Core vía API).
> **SSDs sagrados**: cada nodo SQX (zeus, hera, kronos) tiene un SSD WD Green SATA de 931 GB exclusivo (`local-sqx-*`) dedicado a los datasets SQX. **NO TOCAR** (regla del owner 2026-07-01).
> **Estado operativo**: 1 corriendo + 4 detenidas en mantenimiento. Cuando operen, consumirán ~80% de los recursos de su host para procesar/desarrollar estrategias.

| VMID | Nombre | Nodo | Status | CPU | RAM | Disco | Notas |
|---|---|---|---|---|---|---|---|
| **108** | **sqx-ulab-zeus-0** | zeus | **running** | **28** | **75 GB** | 50 GB + 600 GB data | Única activa. La más grande del cluster. |
| 111 | sqx-ulab-kron-0 | kronos | stopped | **76** | **137 GB** | 50 GB + 600 GB data | Detenida — la más grande por lejos (137 GB RAM) |
| 123 | sqx-ulab-hera-0 | hera | stopped | 70 | **100 GB** | 50 GB | Detenida — 100 GB RAM |
| 162 | sqx-ulab-kron-1 | kronos | stopped | 12 | 30 GB | 20 GB | Más chica |
| 170 | sqx-ulab-zeus-1 | zeus | stopped | 8 | 23 GB | 20 GB | Más chica |

**Total sqx-ulab**: 1 running + 4 stopped. Las detenidas suman **166 vCPU + 290 GB RAM** (cabe en kronos+hera, no en hades).

### Alertas sqx-ulab

- 🟡 **4 VMs detenidas esperando** — 290 GB RAM asignados pero apagados. En mantenimiento actualmente.
- 🟡 **kronos (222 GB libres) y hera (96 GB libres)** son candidatos naturales para reanimar estas VMs si es necesario.

### Documentación relacionada

- **[[Echo Forge]]** (proyecto en `10-projects/Echo Forge/`) — programa de software que orquesta SQX.
- **[[echo-forge]]** (application en `30-resources/applications/echo-forge.md`) — repo `xKoRx/symphony`, módulo `sqx`.
- SSDs sagrados: ver [[../01-topologia/nodo-zeus]], [[../01-topologia/nodo-hera]], [[../01-topologia/nodo-kronos]] § Almacenamiento local.
- Stack Echo más amplio: ver [[../02-servicios/trading]] (MT4/MT5) y [[../02-servicios/red]] (Echo API endpoints).

## echo (qemu/140)

| Item | Valor |
|---|---|
| **Propósito** | (no documentado explícitamente) |
| **VMID** | 140 |
| **Tipo** | qemu VM |
| **Nodo** | hades |
| **vCPUs** | 4 |
| **RAM** | 8 GB |
| **Disco** | 20 GB |
| **NetIn** | 247 GB |
| **NetOut** | 360 GB |
| **Estado** | ✅ Running |

## docker-echo-dev (lxc/141)

| Item | Valor |
|---|---|
| **Propósito** | Ambiente de desarrollo para `echo` (docker) |
| **VMID** | 141 |
| **Tipo** | lxc container |
| **Nodo** | hades |
| **vCPUs** | 12 |
| **RAM** | 4 GB |
| **Disco** | 20 GB |
| **Tags** | `community-script`, `docker` |
| **Estado** | ✅ Running |

## argus (qemu/160)

| Item | Valor |
|---|---|
| **Propósito** | (¿monitoreo IA?) |
| **VMID** | 160 |
| **Tipo** | qemu VM |
| **Nodo** | hades |
| **vCPUs** | 8 |
| **RAM** | 16 GB |
| **Disco** | 32 GB |
| **NetIn** | 598 GB |
| **NetOut** | 23 GB |
| **Estado** | ✅ Running |

## mcps (lxc/113)

| Item | Valor |
|---|---|
| **Propósito** | Servidores MCP (Model Context Protocol) |
| **VMID** | 113 |
| **Tipo** | lxc container |
| **Nodo** | hades |
| **vCPUs** | 2 |
| **RAM** | 4 GB |
| **Disco** | 8 GB |
| **Tags** | `community-script`, `docker` |
| **NetIn** | 90 MB |
| **Estado** | ✅ Running |

> [!note] mcps
> MCP servers permiten que LLMs externos interactúen con herramientas/datos locales. Comunidad scripts.

## temporal (qemu/158)

| Item | Valor |
|---|---|
| **Propósito** | Workflow engine (orquestación de procesos) |
| **VMID** | 158 |
| **Tipo** | qemu VM |
| **Nodo** | hades |
| **vCPUs** | 4 |
| **RAM** | 8 GB |
| **Disco** | 32 GB |
| **NetIn** | 159 GB |
| **NetOut** | 222 GB |
| **Estado** | ✅ Running |

## ubuntu-dev (qemu/159)

| Item | Valor |
|---|---|
| **Propósito** | Dev workstation (probablemente de Rodrigo) |
| **VMID** | 159 |
| **Tipo** | qemu VM |
| **Nodo** | hades |
| **vCPUs** | **24** |
| **RAM** | **64 GB** |
| **Disco** | 100 GB |
| **NetIn** | 13 GB |
| **NetOut** | 4 GB |
| **Estado** | ✅ Running |

> Una VM workstation pesada (24 vCPU, 64 GB RAM). Si Rodrigo la usa como dev environment, justifica la concentración en hades pero también es SPOF si hades cae.

## Resumen IA/ML

| Servicio | Nodo | RAM | Estado |
|---|---|---|---|
| sqx-ulab-zeus-0 | zeus | 75 GB | running |
| sqx-ulab-kron-0 | kronos | 137 GB | **stopped** |
| sqx-ulab-hera-0 | hera | 100 GB | **stopped** |
| echo | hades | 8 GB | running |
| docker-echo-dev | hades | 4 GB | running |
| argus | hades | 16 GB | running |
| mcps | hades | 4 GB | running |
| temporal | hades | 8 GB | running |
| ubuntu-dev | hades | 64 GB | running |

## Alertas

| # | Severidad | Alerta |
|---|---|---|
| 1 | 🟡 | 4 VMs sqx-ulab detenidas (290 GB RAM asignados pero apagados) |
| 2 | 🟡 | La mayoría de servicios IA/ML en hades (5 de 9) |
| 3 | 🟡 | `argus` nombre sugiere "monitoreo" pero no queda claro qué hace exactamente |

---

**Source files**: `/home/hermes/aranea/topology/services.md`, `/home/hermes/aranea/topology/discovery/{zeus,kronos,hera,hades}_20260628_211812.txt`

**Captured**: 2026-06-28 21:18 UTC. Doc generado 2026-06-30.
