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
updated: 2026-09-18
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
| `discovery/athena_20260630_194423.txt` | 2026-06-30 19:44:23 UTC | raw agent-read | superseded 2026-09-16 | archivo histórico |
| `discovery/zeus_20260628_211812.txt` | 2026-06-28 21:18:12 UTC | raw agent-read | superseded | archivo histórico |
| `discovery/zeus_20260630_194423.txt` | 2026-06-30 19:44:23 UTC | raw agent-read | superseded 2026-09-16 | archivo histórico |
| `discovery/hera_20260628_211812.txt` | 2026-06-28 21:18:12 UTC | raw agent-read | superseded | archivo histórico |
| `discovery/hera_20260630_194423.txt` | 2026-06-30 19:44:23 UTC | raw agent-read | superseded 2026-09-16 | archivo histórico |
| `discovery/kronos_20260628_211812.txt` | 2026-06-28 21:18:12 UTC | raw agent-read | superseded | archivo histórico |
| `discovery/kronos_20260630_194423.txt` | 2026-06-30 19:44:23 UTC | raw agent-read | superseded 2026-09-16 | archivo histórico |
| `discovery/hades_20260628_211812.txt` | 2026-06-28 21:18:12 UTC | raw agent-read | superseded | archivo histórico |
| `discovery/hades_20260630_194423.txt` | 2026-06-30 19:44:23 UTC | raw agent-read | superseded 2026-09-16 | archivo histórico |
| `discovery/truenas_20260628_211812.txt` | 2026-06-28 21:18:12 UTC | raw agent-read | superseded | archivo histórico |
| `discovery/truenas_20260630_194423.txt` | 2026-06-30 19:44:23 UTC | raw agent-read | superseded 2026-09-16 | archivo histórico |
| `discovery/*_20260702_033204.txt` (6 nodos) | 2026-07-02 03:32:04 UTC | raw agent-read | no registrada en su momento; integrada retroactivamente 2026-09-16 | archivos en `discovery/` |
| `discovery/athena_20260916_233513.txt` | 2026-09-16 23:35:13 UTC | raw agent-read | superseded 2026-09-17 | R0 [[BACKUP-DR-OWNER-PROJECT]] |
`discovery/athena_20260917_185839.txt` | **2026-09-17 18:58:39 UTC** | raw agent-read | **0 días** ✅ | [[01-topologia/nodo-athena]], preflight G0 mandato Infrastructure Enablement |
| `discovery/hades_20260916_233513.txt` | 2026-09-16 23:35:13 UTC | raw agent-read | superseded 2026-09-17 | R0 [[BACKUP-DR-OWNER-PROJECT]] |
`discovery/hades_20260917_185839.txt` | **2026-09-17 18:58:39 UTC** | raw agent-read | **0 días** ✅ | [[01-topologia/nodo-hades]], preflight G0 mandato Infrastructure Enablement |
| `discovery/zeus_20260916_233513.txt` | 2026-09-16 23:35:13 UTC | raw agent-read | superseded 2026-09-17 | R0 [[BACKUP-DR-OWNER-PROJECT]] |
`discovery/zeus_20260917_185839.txt` | **2026-09-17 18:58:39 UTC** | raw agent-read | **0 días** ✅ | [[01-topologia/nodo-zeus]], preflight G0 mandato Infrastructure Enablement |
| `discovery/hera_20260916_233513.txt` | 2026-09-16 23:35:13 UTC | raw agent-read | superseded 2026-09-17 | R0 [[BACKUP-DR-OWNER-PROJECT]] |
`discovery/hera_20260917_185839.txt` | **2026-09-17 18:58:39 UTC** | raw agent-read | **0 días** ✅ | [[01-topologia/nodo-hera]], preflight G0 mandato Infrastructure Enablement |
| `discovery/kronos_20260916_233513.txt` | 2026-09-16 23:35:13 UTC | raw agent-read | superseded 2026-09-17 | R0 [[BACKUP-DR-OWNER-PROJECT]] |
`discovery/kronos_20260917_185839.txt` | **2026-09-17 18:58:39 UTC** | raw agent-read | **0 días** ✅ | [[01-topologia/nodo-kronos]], preflight G0 mandato Infrastructure Enablement |
| `discovery/truenas_20260916_233513.txt` | 2026-09-16 23:35:13 UTC | raw agent-read | superseded 2026-09-17 | R0 [[BACKUP-DR-OWNER-PROJECT]] |
| sondas vivas H1 enablement (SSH/API 8006/WS DDP sobre PVE×5, TrueNAS, PBS; evidencia fuera del vault en `~/aranea/work/h1-enablement-20260918/`) | 2026-09-18 16:30–17:30 (-03) | probes read-only live (ssh/https/wss) | **0 días** ✅ | Matriz de autoridad H1 en [[HERMES — Infrastructure Operations]] |
| auditoría read-only H2 (SSH sweep ×5 nodos: pveversion/quorum/storage.cfg/ACL/roles/sudoers/configs de guests protegidos/listsnapshots; API probe con token: 19 endpoints GET clasificados 200/403/200-filtrado; Ceph health; HA status; datacenter.cfg) | 2026-09-18 20:41–21:02 UTC | probes read-only live; evidencia fuera del vault en `~/aranea/work/h2-enablement-20260918/` | **0 días** ✅ | Matriz H2 y estado H2 en [[HERMES — Infrastructure Operations]] |
| sondeos read-only H3 guest/service enablement (sweep nativo SSH truenas/pbs/mcps/daedalus + self; cluster/resources 59=42+17 revalidado; docker/sudo/grupo docker en mcps y daedalus; qemu-guest-agent config+`qm guest cmd` vivo en 111/118/123/135/138; probes MCP Windows worker-kronos viewer/operator con CIM denegado; anomalia discos unused sqx-hera reconfirmada) | 2026-09-18 23:14–23:31 UTC | probes read-only live; evidencia fuera del vault en `~/aranea/work/h3-enablement-20260918/` | **0 días** ✅ | Matrices H3 y estado H3 en [[HERMES — Infrastructure Operations]] |
| bootstrap + certificación W1 Windows nativo (discovery qm guest exec read-only; instalación identidad/llave/ACL; probes SSH positivos/negativos desde .122; logs sshd.log; G4 hijo fresco sin MCP) | 2026-09-18 21:10–21:55 (-03) | bootstrap acotado (mutaciones W1 registradas) + probes live; evidencia fuera del vault en `~/aranea/work/w1-windows-native-20260918/` | **0 días** ✅ | Matriz H3 (fila worker-kronos), [[windows-operator-contract]], estado W1/H3 en [[HERMES — Infrastructure Operations]] |
| auditoría read-only H4 provisioning (SSH sweep ×5 nodos: pveum user/token/ACL/perms/roles; cluster/resources 59=39+20 con flag template (3 templates @hera: 109/117/120); pvesm status+cfg+list iso/vztmpl; capacidad df+vgs+lvs por nodo; Ceph health desde zeus/hera/kronos; /etc/network/interfaces ×5; scan cloud-init 0/39 VMs; rootfs/net0 de 20 LXCs; VG pve free) | 2026-09-18 22:17 / 2026-09-19 01:17 UTC | probes read-only live; evidencia fuera del vault en `~/aranea/work/h4-provisioning-20260918/` | **0 días** ✅ | Matriz H4 y [[provisioning-operator-contract]] en [[HERMES — Infrastructure Operations]] |
| auditoría read-only H5 high-impact (SSH sweep ×5 nodos PVE: pvecm/corosync/storage.cfg/pvesm/ha-manager/services/interfaces/bridges; Ceph -s/osd df/pool ls detail/health detail desde zeus+hera+kronos; TrueNAS API midclt pools/servicios/scrub zpool/shares/alerts; PBS services/drop-ins fail-closed/datastore; athena: firewall PVE, tailscale 119, pihole FTL, guests 119/149/200/130; DNS getent desde hermes-vm) | 2026-09-19 15:42–15:50 UTC | probes read-only live; evidencia fuera del vault en `~/aranea/work/h5-high-impact-20260919/probes/` | **0 días** ✅ | Índice [[30-resources/aranea/06-high-impact/00-index|high-impact H5]], contratos [[high-impact-networking-dns-contract]]/[[cluster-node-maintenance-contract]]/[[ceph-storage-operations-contract]], matrices en [[HERMES — Infrastructure Operations]] |
`discovery/truenas_20260917_185839.txt` | **2026-09-17 18:58:39 UTC** | raw agent-read | **0 días** ✅ | [[01-topologia/nodo-truenas]], preflight G0 mandato Infrastructure Enablement |
| `tickets/2026-06-29-001..009-*.md` | 2026-06-29 | ticket cerrado | 1 día | [[05-tickets/*]] |
| `tickets/2026-06-30-010..012-*.md` | 2026-06-30 | ticket | 0 días | [[05-tickets/*]] |
| **Ping check (6 nodos)** | **2026-06-30** | live | 0 días | [[00-index]], todos los `nodo-*.md` |

## 🔍 Resumen de drift

- **Inventario crudo (discovery/*.txt)**: **0 días** ✅ (refresh 2026-09-17 18:58 UTC, preflight G0; refresh previo 2026-09-16 23:35 UTC)
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
