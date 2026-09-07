---
type: known_error
scope: agent
created: "2026-06-30"
updated: "2026-06-30"
resolved: "2026-06-30"
severity: medium
area: "[[Personal]]"
project: "[[AGENTS OS]]"
application:
entities:
  - "[[Aranea]]"
related:
  - "[[~/aranea/topology/nodes/README]]"
  - "[[30-resources/aranea/01-topologia/fechas-captura]]"
aliases: []
confidence: high
source_session: "[[2026-06-30-1636-aranea-docs-storage-batch-summary]]"
load_policy: never
indexable: true
index_priority: medium
tags:
  - kind/known-error
  - scope/agent
  - area/personal
  - project/agents-os
---

# Known error: drift operacional Aranea por NOPASSWD no aplicado

> [!warning]+ Known error
> **Severidad:** medium · **Estado:** known · **Detectado:** 2026-06-30

## Síntoma

SSH desde `hermes@VM-Hermes` (192.168.31.122) hacia los Proxmox nodes y TrueNAS funciona, pero `sudo -n /usr/local/sbin/agent-read` falla con:

```text
sudo: a password is required
```

Esto bloquea el refresh del inventario Aranea capturado por la sesión del owner en `~/aranea/topology/discovery/*.txt` (del 2026-06-28).

## Afectados

- `athena` (192.168.31.10)
- `zeus` (192.168.31.100)
- `hera` (192.168.31.110)
- `kronos` (192.168.31.120)
- `truenas` (192.168.31.91, wrapper en `/mnt/pool0/.agent_ro/bin/agent-read`)
- `hades` (192.168.31.90) — además **offline** (no responde a ping)

## Causa raíz

El usuario `agent_ro` en cada nodo remoto no tiene `NOPASSWD` configurado para el wrapper `agent-read`. La documentación en `~/aranea/topology/nodes/README.md` y `~/aranea/topology/00-access.md` describe el *diseño objetivo* (NOPASSWD aplicado) pero la configuración real nunca se aplicó, o se revirtió en algún momento posterior.

## Workaround vigente

**Ya no aplica** — NOPASSWD controlado aplicado el 2026-06-30 en los 6 nodos (athena/zeus/hera/kronos/hades/truenas). Inventario refrescado en el mismo pase. Ticket de cierre: `2026-06-30-012`. Skill de refresh: `aranea_agent_ro_inventory_refresh`.

## Fix recomendado

Aplicar en cada nodo (vía SSH del owner como root):

```bash
# Proxmox nodes
echo 'agent_ro ALL=(ALL) NOPASSWD: /usr/local/sbin/agent-read' \
  > /etc/sudoers.d/agent_ro
chmod 440 /etc/sudoers.d/agent_ro
visudo -c

# TrueNAS (path distinto)
# Agente corre como root dentro del jail/host
echo 'agent_ro ALL=(ALL) NOPASSWD: /mnt/pool0/.agent_ro/bin/agent-read' \
  > /etc/sudoers.d/agent_ro
```

Después validar desde VM Hermes:

```bash
KEY="/home/hermes/.ssh/agent_ro_aranea"
for ip in 192.168.31.10 192.168.31.100 192.168.31.110 192.168.31.120; do
  ssh -i "$KEY" -o IdentitiesOnly=yes -o BatchMode=yes \
    agent_ro@$ip 'sudo -n /usr/local/sbin/agent-read hostname'
done
```

## Bloqueos

- Requiere OK explícito del owner
- Requiere acceso root en cada nodo
- Hades requiere diagnóstico de hardware antes (no responde a ping)

## Estado

**resolved** (2026-06-30). El NOPASSWD fue aplicado por el owner de forma controlada (solo el wrapper `agent-read`, sin `NOPASSWD: ALL`). Validación 6/6 PASS ejecutada por ariadna: SSH + sudo -n + wrapper + `agent-read all` en los 6 nodos. Inventario refrescado el 2026-06-30 19:44 UTC. Tickets relacionados: `2026-06-30-010` (docs), `2026-06-30-011` (storage audit + backups), `2026-06-30-012` (este fix).
