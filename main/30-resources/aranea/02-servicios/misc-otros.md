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

# Misceláneos / otros servicios

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28

Servicios que no encajan en las otras categorías.

## etcd-keeper (lxc/148)

| Item | Valor |
|---|---|
| **Propósito** | UI web para cluster etcd |
| **VMID** | 148 |
| **Tipo** | lxc container |
| **Nodo** | hades |
| **vCPUs** | 1 |
| **RAM** | 2 GB |
| **Disco** | 10 GB |
| **Estado** | ✅ Running |

Ver [[red]] § etcd para el cluster completo.

## obsidian-sync (lxc/116)

Ver [[bases-de-datos]] § obsidian-sync.

## docker-hasura (lxc/129)

Ver [[automation]] § docker-hasura.

## Templates definidos (no instanciados)

| VMID | Nombre | Nodo | CPU | RAM | Disco | Tags |
|---|---|---|---|---|---|---|
| 109 | win-serv-22 | hera | 16 | 34 GB | 120 GB | template |
| 117 | ubuntu-server | hera | 5 | 12 GB | 32 GB | template |
| 120 | k8s-node-2 | hera | 5 | 12 GB | 32 GB | template, kubernetes |

> Templates Windows / Ubuntu / k8s disponibles para clonar.

## VMs stopped (no instanciadas al inicio, recursos disponibles)

| VMID | Nombre | Nodo | CPU | RAM | Disco | Notas |
|---|---|---|---|---|---|---|
| 100 | win11-gpu-red | zeus | 4 | 10 GB | 200 GB | stopped |
| 102 | mt5-wsl-red | zeus | 2 | 6 GB | 50 GB | stopped |
| 104 | ryma-linux | kronos | 2 | 4 GB | 50 GB | exposed |
| 107 | develop | hera | 4 | 17 GB | 100 GB | stopped |
| 110 | testing | hera | 8 | 17 GB | 50 GB | trading, stopped |
| 111 | sqx-ulab-kron-0 | kronos | 76 | 137 GB | 50 GB | stopped ⚠️ |
| 112 | kronos-sqx | kronos | 4 | 30 GB | 120 GB | stopped |
| 114 | mt4-test | kronos | 2 | 8 GB | 50 GB | stopped |
| 121 | docker-mongodb-local | hera | 6 | 20 GB | 10 GB | docker, stopped |
| 122 | docker-postgres-local | hera | 8 | 17 GB | 10 GB | docker, stopped |
| 123 | sqx-ulab-hera-0 | hera | 70 | 100 GB | 50 GB | stopped ⚠️ |
| 132 | docker-monitoreo | hera | 2 | 4 GB | 10 GB | base, docker, stopped |
| 151 | win-development | hades | 16 | 32 GB | 200 GB | stopped |
| 162 | sqx-ulab-kron-1 | kronos | 12 | 30 GB | 20 GB | stopped |
| 170 | sqx-ulab-zeus-1 | zeus | 8 | 23 GB | 20 GB | stopped |

**Total stopped**: ~16 VMs con 222 vCPU + 463 GB RAM asignados pero apagados.

## Servicios en estado "desconocido"

| VMID | Nombre | Estado | Notas |
|---|---|---|---|
| 113 | mcps | running | Ver [[ml-ia]] |
| 116 | obsidian-sync | running | Ver [[bases-de-datos]] |
| 118 | agent | running | **Es la VM que corre Hermes-agent** (ver [[../01-topologia/nodo-kronos]]) |
| 140 | echo | running | Ver [[ml-ia]] |
| 160 | argus | running | Ver [[ml-ia]] |

## Pendientes del wrapper `agent-read`

El wrapper actual **NO expone** ciertas secciones que serían útiles. Ver `00-access.md` § "Subcomandos faltantes":

```bash
# Faltantes en PVE:
ceph config          # config dump
pve-firewall         # rules
vm <vmid> config     # config detallada de una VM
vm <vmid> snapshot   # snapshots
corosync             # detail
systemd-unit <name>  # status de un servicio

# Faltantes en truenas:
apps                 # TrueNAS apps / ix-apps
cloud-backup         # tasks programadas
disk-smart           # health por disco
```

### Modo "deep" propuesto

Ejecutar `pvesm status`, `zpool iostat -v`, etc. solo bajo demanda.

## Alertas

| # | Severidad | Alerta |
|---|---|---|
| 1 | 🟡 | 16 VMs stopped con 463 GB RAM asignados pero apagados — recursos ociosos |
| 2 | 🟡 | Wrapper `agent-read` incompleto — falta detalle por VM (config, snapshots) |

---

**Source files**: `/home/hermes/aranea/topology/services.md`, `/home/hermes/aranea/topology/00-access.md`, `/home/hermes/aranea/topology/discovery/{zeus,hera,kronos,hades}_20260628_211812.txt`

**Captured**: 2026-06-28 21:18 UTC. Doc generado 2026-06-30.
