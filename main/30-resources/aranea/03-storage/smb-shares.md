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

# SMB Shares

## Propósito

Documentación canónica legacy de [[Aranea]]; se conserva el contenido histórico y su estado requiere verificación antes de uso operativo.

## Contenido


> **Capturado**: 2026-06-28
> **Servidor**: truenas (192.168.31.91)
> **Servicio**: cifs / Samba (RUNNING)

## Shares

| Share | Path en truenas | Guest OK | Tamaño | Función |
|---|---|---|---|---|
| `aranea_storage` | `/mnt/pool0/aranea_storage` | **no** | 998 GB usados (47%) | Storage general del cluster |
| `trading_systems` | `/mnt/pool0/trading_systems` | **no** | 485 GB usados (31%) | Datos de MetaTrader (MT4) |
| `trading_documents` | `/mnt/pool0/trading_documents` | **SÍ** ⚠️ | 24 MB | Documentos trading (público para guests) |

## Alertas críticas

| # | Severidad | Alerta |
|---|---|---|
| 1 | 🟠 | **`trading_documents` con `guestok = true`** — cualquier host de la LAN puede leer este share sin autenticarse. Confirmar con Rodrigo si es intencional. |

### Acción recomendada

```bash
# En truenas, via Web UI o midcli:
midclt call smb.update 4 '{"guestok": false}'

# Alternativa via shell:
midclt call smb.get_smb_shares | jq '.[] | select(.name=="trading_documents")'
```

## Configuración recomendada (producción)

| Aspecto | Estado actual | Recomendación |
|---|---|---|
| Guest OK | Solo en `trading_documents` | Desactivar |
| Auth | Local users en truenas | OK para homelab |
| SMB version | SMB2/SMB3 (asumido) | OK |
| ACLs por share | No capturado | Documentar |

## Acceso desde clientes

### Linux

```bash
# Mount manual
sudo mount -t cifs //192.168.31.91/aranea_storage /mnt/storage \
  -o username=<user>,password=<pass>,uid=1000,gid=1000

# O via fstab
//192.168.31.91/aranea_storage /mnt/storage cifs credentials=/etc/samba/creds,uid=1000,gid=1000 0 0
```

### Windows

```
\\192.168.31.91\aranea_storage
\\192.168.31.91\trading_systems
\\192.168.31.91\trading_documents  (sin password si guest OK)
```

### macOS

```
smb://192.168.31.91/aranea_storage
```

## Puertos SMB

```
tcp  0.0.0.0:139     smbd (NetBIOS)
tcp  0.0.0.0:445     smbd (SMB directa)
tcp  0.0.0.0:5357    wsdd.py (Web Services Discovery)
udp  0.0.0.0:137     nmbd (NetBIOS name)
udp  0.0.0.0:138     nmbd (NetBIOS datagram)
```

## Servicios relacionados en truenas

| Servicio | Estado |
|---|---|
| cifs (Samba) | RUNNING |
| smbd (daemon) | RUNNING |
| nmbd (NetBIOS) | RUNNING |
| wsdd (Web Services Discovery) | RUNNING |
| avahi-daemon (mDNS) | RUNNING |

## Backup

- `aranea_storage` → backup en `pool2/backup/aranea_storage/` (39 GB)
- `trading_systems` → backup en `pool2/backup/trading_systems/` (305 GB)
- `trading_documents` → ❓ sin backup explícito

---

## Source files

- `/home/hermes/aranea/topology/nodes/truenas.md`
- `/home/hermes/aranea/topology/health.md` §5
- `/home/hermes/aranea/topology/discovery/truenas_20260628_211812.txt`

## Captured

2026-06-28 21:18 UTC. Doc generado 2026-06-30.
