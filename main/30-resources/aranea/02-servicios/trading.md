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

# Trading — MT4 / MT5 + broker feeds

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28

> [!danger] Concentración 100% en hades
> **5 instancias MT4 corriendo** todas en **hades**. hades = 22 VMs running, 240 GB RAM. Si hades cae → todas las cuentas de trading caen (incluida la real).

## Instancias MT4 (5 running + 1 stopped)

| VMID | Nombre | Tipo | Nodo | Status | CPU | RAM | Disco | Notas |
|---|---|---|---|---|---|---|---|---|
| **124** | **mt4-real** | qemu | hades | **running** | 8 | 8 GB | 50 GB | 🔴 **CUENTA REAL (producción)** |
| 125 | mt4-test | qemu | hades | running | 8 | 16 GB | 50 GB | |
| 133 | mt4-ftmo | qemu | hades | running | 8 | 8 GB | 50 GB | FTMO prop firm |
| 134 | mt4-ttp | qemu | hades | running | 8 | 8 GB | 50 GB | TTP trend following |
| 144 | mt4-demo | qemu | hades | running | 4 | 16 GB | 50 GB | |
| 114 | mt4-test | qemu | kronos | **stopped** | 2 | 8 GB | 50 GB | (duplicado, stopped) |

**Total**: 5 running en hades (40 vCPU, 56 GB RAM asignados), 1 stopped en kronos.

## MT5 (1 stopped)

| VMID | Nombre | Tipo | Nodo | Status | CPU | RAM | Disco | Notas |
|---|---|---|---|---|---|---|---|---|
| 102 | mt5-wsl-red | qemu | zeus | **stopped** | 2 | 6 GB | 50 GB | |

## Broker feeds

> [!warning] Broker feeds no documentados
> No se captura en el wrapper `agent-read` qué broker feeds (tick data) están configurados ni el endpoint. Asumimos MetaTrader Server / broker API estándar. **Necesita refresh** con introspección.

## Almacenamiento trading

- **SMB share `trading_systems`** en truenas (485 GB usados) — datos MT4 persistentes
- **SMB share `trading_documents`** en truenas (24 MB) — guest-ok ⚠️
- **Backup en `pool2/backup/trading_systems/`** (305 GB)

## Alertas y riesgos

| # | Severidad | Riesgo |
|---|---|---|
| 1 | 🔴 | **mt4-real es producción + corre en hades** (single point of failure). Si hades cae → cuenta real down. Sin HA. |
| 2 | 🟠 | **100% de la carga trading en un solo nodo** — hades. hades ya está al 74% RAM. |
| 3 | 🟡 | mt4-test (vm/114 en kronos) está stopped — confusión con mt4-test (vm/125 en hades, running). |
| 4 | 🟡 | Sin snapshots programados de las VMs MT4 |

## Acciones recomendadas

1. **Snapshots pre-trade**: snapshot ZFS/diario antes de la apertura de mercados
2. **Migración gradual**: mover `mt4-test` (vm/125) a kronos (que tiene 222 GB RAM libres)
3. **Migrar `mt4-real`**: evaluar si conviene a bare-metal o VM en kronos/hera (más RAM libre)
4. **Backup de `trading_systems`**: verificar que las snapshots ZFS de pool2 cubren lo crítico

---

**Source files**: `/home/hermes/aranea/topology/services.md`, `/home/hermes/aranea/topology/discovery/hades_20260628_211812.txt`

**Captured**: 2026-06-28 21:18 UTC. Doc generado 2026-06-30.
