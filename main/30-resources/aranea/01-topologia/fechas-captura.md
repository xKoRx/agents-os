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

# Fechas de captura — honestidad documental

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> Esta tabla registra la fecha de captura de **cada fuente de datos** usada para producir la documentación de Aranea. La honestidad documental exige marcar el drift entre captura y lectura.

## 📅 Tabla de fuentes

| Fuente | Fecha captura | Tipo | Drift al 2026-06-30 | Usado en |
|---|---|---|---|---|
| `topology/README.md` | 2026-06-28 | manual | 2 días | [[00-index]], [[01-topologia/README]], todos los nodos |
| `topology/services.md` | 2026-06-28 | manual | 2 días | [[02-servicios/*]] |
| `topology/health.md` | 2026-06-28 | manual | 2 días | [[00-index]], [[01-topologia/nodo-truenas]], etc. |
| `topology/nodes/truenas.md` | 2026-06-28 | manual | 2 días | [[01-topologia/nodo-truenas]] |
| `topology/nodes/README.md` | 2026-06-28 | manual | 2 días | [[01-topologia/README]] § bloqueador |
| `topology/00-access.md` | 2026-06-28 | manual | 2 días | [[01-topologia/red]], [[00-index]] § roadmap |
| `discovery/athena_20260628_211812.txt` | 2026-06-28 21:18:12 UTC | raw agent-read | superseded | archivo histórico |
| `discovery/athena_20260630_194423.txt` | **2026-06-30 19:44:23 UTC** | raw agent-read | **0 días** ✅ | [[01-topologia/nodo-athena]], este doc |
| `discovery/zeus_20260628_211812.txt` | 2026-06-28 21:18:12 UTC | raw agent-read | superseded | archivo histórico |
| `discovery/zeus_20260630_194423.txt` | **2026-06-30 19:44:23 UTC** | raw agent-read | **0 días** ✅ | [[01-topologia/nodo-zeus]], este doc |
| `discovery/hera_20260628_211812.txt` | 2026-06-28 21:18:12 UTC | raw agent-read | superseded | archivo histórico |
| `discovery/hera_20260630_194423.txt` | **2026-06-30 19:44:23 UTC** | raw agent-read | **0 días** ✅ | [[01-topologia/nodo-hera]], este doc |
| `discovery/kronos_20260628_211812.txt` | 2026-06-28 21:18:12 UTC | raw agent-read | superseded | archivo histórico |
| `discovery/kronos_20260630_194423.txt` | **2026-06-30 19:44:23 UTC** | raw agent-read | **0 días** ✅ | [[01-topologia/nodo-kronos]], este doc |
| `discovery/hades_20260628_211812.txt` | 2026-06-28 21:18:12 UTC | raw agent-read | superseded | archivo histórico |
| `discovery/hades_20260630_194423.txt` | **2026-06-30 19:44:23 UTC** | raw agent-read | **0 días** ✅ | [[01-topologia/nodo-hades]], este doc |
| `discovery/truenas_20260628_211812.txt` | 2026-06-28 21:18:12 UTC | raw agent-read | superseded | archivo histórico |
| `discovery/truenas_20260630_194423.txt` | **2026-06-30 19:44:23 UTC** | raw agent-read | **0 días** ✅ | [[01-topologia/nodo-truenas]], este doc |
| `tickets/2026-06-29-001..009-*.md` | 2026-06-29 | ticket cerrado | 1 día | [[05-tickets/*]] |
| `tickets/2026-06-30-010..012-*.md` | 2026-06-30 | ticket | 0 días | [[05-tickets/*]] |
| **Ping check (6 nodos)** | **2026-06-30** | live | 0 días | [[00-index]], todos los `nodo-*.md` |

## 🔍 Resumen de drift

- **Inventario crudo (discovery/*.txt)**: **0 días** ✅ (refresh 2026-06-30 19:44 UTC)
- **Documentación manual (README/services/health)**: 2 días (no regenerada en este refresh — solo se actualizaron timestamps de fuente)
- **Tickets históricos**: 1-2 días
- **Tickets en curso (010, 011, 012)**: 0 días
- **Ping check**: 0 días ✅

## 🚧 Bloqueadores activos (impiden refresh fresco)

| Bloqueador | Detalle | Nodos afectados | Tickets abiertos |
|---|---|---|---|
| ~~SSH NOPASSWD no aplicado~~ | ~~`ssh agent_ro@<ip>` funciona, `sudo -n /usr/local/sbin/agent-read` pide password~~ | ~~athena, zeus, hera, kronos, truenas~~ | ✅ **Resuelto 2026-06-30** (ticket `2026-06-30-012`) |

## 📋 Comando canónico de refresh (cuando se desbloquee)

```bash
#!/bin/bash
KEY="/home/hermes/.ssh/agent_ro_aranea"
DEST="/home/hermes/aranea/topology/discovery"
TS=$(date +%Y%m%d_%H%M%S)

declare -A NODES=(
  [athena]="192.168.31.10"
  [zeus]="192.168.31.100"
  [hera]="192.168.31.110"
  [kronos]="192.168.31.120"
  [hades]="192.168.31.90"
)

for name in "${!NODES[@]}"; do
  ip="${NODES[$name]}"
  ssh -i "$KEY" -o IdentitiesOnly=yes -o BatchMode=yes \
    "agent_ro@$ip" \
    'sudo -n /usr/local/sbin/agent-read all' \
    > "$DEST/${name}_${TS}.txt"
done

# TrueNAS
ssh -i "$KEY" -o IdentitiesOnly=yes -o BatchMode=yes \
  agent_ro@192.168.31.91 \
  'sudo -n /mnt/pool0/.agent_ro/bin/agent-read all' \
  > "$DEST/truenas_${TS}.txt"
```

## 📅 Comando de refresh de docs

Una vez capturado el nuevo discovery, regenerar estos docs:

- [[00-index]] (corazones: total RAM, total cores, alert count)
- [[01-topologia/nodo-athena]]
- [[01-topologia/nodo-zeus]]
- [[01-topologia/nodo-hera]]
- [[01-topologia/nodo-kronos]]
- [[01-topologia/nodo-hades]]
- [[01-topologia/nodo-truenas]]
- [[02-servicios/*]] (catálogo puede cambiar)
- [[03-storage/*]] (puede cambiar Ceph usage, etc.)

## ⚠️ Convención

> Toda conclusión en esta documentación lleva fecha de captura.
> Cuando un valor cambia con el tiempo (RAM usage, Ceph utilization, VM status), se prefiere **re-capturar y re-documentar** que actualizar in-place, para mantener audit trail.

---

## Source files

- `/home/hermes/aranea/topology/discovery/{athena,zeus,hera,kronos,hades,truenas}_20260628_211812.txt`
- `/home/hermes/aranea/topology/{README,services,health}.md`
- `/home/hermes/aranea/topology/nodes/{README,truenas}.md`
- `/home/hermes/aranea/topology/00-access.md`
- `/home/hermes/aranea/tickets/*.md`

## Captured

Documento generado el **2026-06-30**. Datos crudos más recientes: **2026-06-28 21:18:12 UTC**.
