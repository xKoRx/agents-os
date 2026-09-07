---
type: action
schema_version: 1
project:
status: done
created: 2026-08-10
updated: 2026-08-10
tags:
  - kind/action
  - area/aranea
---

## Descripción

Registro histórico de ejecución para [[Aranea]].

## Checklist

- [x] Resultado histórico preservado

---
id: 2026-06-30-012
title: "Unlock agent_ro NOPASSWD on all 6 nodes + refresh inventory"
type: action
schema_version: 1
status: done
status_detail: "✅ Cerrado 2026-06-30. NOPASSWD aplicado en 6/6 nodos. Inventario refrescado. Skill creada. Gaps #1 y #2 cerrados."
severity: medium
icon: 🎫
slug: 2026-06-30-012-unlock-agent-ro-nopasswd
area: "[[Personal]]"
project: "[[AGENTS OS]]"
created: 2026-06-30
updated: 2026-08-10
closed: 2026-06-30
owner: me
executor: ariadna
aliases:
  - ticket 012
  - ticket nopasswd
tags:
  - kind/action
  - area/personal
  - project/agents-os
  - action/ticket
related:
  - "[[2026-06-30-010-aranea-full-docs]]"
  - "[[2026-06-30-011-aranea-storage-audit-backup]]"
  - "[[2026-06-30-013-storage-redesign-backup-design]]"
  - "[[~/aranea/topology/nodes/README]]"
  - "[[../../00-index]]"
---

# 2026-06-30-012 — Unlock agent_ro NOPASSWD + refresh inventory

## Descripción

Habilitar lectura operacional sin password para `agent_ro` y refrescar el inventario de los seis nodos.

## Checklist

- [x] Acción ejecutada y validada; la evidencia permanece en la bitácora y el cierre histórico.

## Goal

Close roadmap gaps **#1** (NOPASSWD no aplicado en 5/6 nodos) and **#2** (inventario con drift de 2 días) en una sola pasada.

## Scope (lo que el owner autorizó)

NOPASSWD **controlado**, sin `NOPASSWD: ALL`:

| Nodo | Wrapper permitido |
|---|---|
| athena (192.168.31.10) | `sudo -n /usr/local/sbin/agent-read` |
| zeus (192.168.31.100) | `sudo -n /usr/local/sbin/agent-read` |
| hera (192.168.31.110) | `sudo -n /usr/local/sbin/agent-read` |
| kronos (192.168.31.120) | `sudo -n /usr/local/sbin/agent-read` |
| hades (192.168.31.90) | `sudo -n /usr/local/sbin/agent-read` (ya estaba aplicado) |
| truenas (192.168.31.91) | `sudo -n /mnt/pool0/.agent_ro/bin/agent-read` (ruta distinta) |

Reglas explícitas del owner:

- ❌ No `NOPASSWD: ALL`.
- ✅ Solo el wrapper `agent-read` permitido.
- ❌ No usar root.
- ❌ No usar `sudo bash`.
- ❌ No editar sudoers desde el agente.
- ❌ No cambiar permisos.
- ✅ Solo validar inventario.

## Bitácora

### Paso 1 — Ping check hades (transitorio offline en doc previo)

```
$ ping -c 2 -W 2 192.168.31.90
64 bytes from 192.168.31.90: icmp_seq=2 ttl=64 time=0.156 ms
--- 192.168.31.90 ping statistics ---
2 packets transmitted, 2 received, 0% packet loss
```

→ hades vivo. **6/6 nodos reachable**.

### Paso 2 — Validación matriz SSH + sudo -n + wrapper

Para cada nodo, se ejecutó `ssh agent_ro@<ip> 'sudo -n <wrapper> node'` y se inspeccionó `sudo -n -l`.

| Nodo | SSH | sudo -n -l muestra wrapper | wrapper `node` rc | stderr |
|---|---|---|---|---|
| athena | ✅ | ✅ `(root) NOPASSWD: /usr/local/sbin/agent-read` | ✅ 0 (4318 B) | — |
| hades | ✅ | ✅ `(root) NOPASSWD: /usr/local/sbin/agent-read` | ✅ 0 (4563 B) | — |
| zeus | ✅ | ✅ `(root) NOPASSWD: /usr/local/sbin/agent-read` | ✅ 0 (4679 B) | — |
| hera | ✅ | ✅ `(root) NOPASSWD: /usr/local/sbin/agent-read` | ✅ 0 (4466 B) | — |
| kronos | ✅ | ✅ `(root) NOPASSWD: /usr/local/sbin/agent-read` | ✅ 0 (4564 B) | — |
| truenas | ✅ | ✅ `(ALL) NOPASSWD: /mnt/pool0/.agent_ro/bin/agent-read` | ✅ 0 (4154 B) | — |

**Resultado: 6/6 PASS** en los 4 niveles (SSH, sudoers, wrapper, ejecución).

> **Pitfall encontrado y resuelto**: el primer intento usó `sudo -n <wrapper> hostname`. El wrapper rechaza argumentos fuera de su vocabulario (`all|node|network|storage|proxmox|ceph|services`, TrueNAS añade `shares`) y devuelve rc=2 con mensaje de uso. El test correcto es `node`.

### Paso 3 — Captura bulk `agent-read all`

| Nodo | rc | bytes | destino |
|---|---|---|---|
| athena | 0 | 632 584 | `discovery/athena_20260630_194423.txt` |
| hades | 0 | 87 695 | `discovery/hades_20260630_194423.txt` |
| zeus | 0 | 80 521 | `discovery/zeus_20260630_194423.txt` |
| hera | 0 | 79 735 | `discovery/hera_20260630_194423.txt` |
| kronos | 0 | 84 050 | `discovery/kronos_20260630_194423.txt` |
| truenas | 0 | 88 127 | `discovery/truenas_20260630_194423.txt` |

**Total: 1 052 712 bytes (1.0 MB) capturados sin error. stderr vacío en los 6 nodos.**

athena pesa ~7x más que el resto porque su `all` incluye la vista cluster completa (PVE + Ceph + VMs + servicios de todos los nodos).

### Paso 4 — Hallazgos relevantes en el snapshot fresco

- **hades**: 187/251 GiB RAM usada (74%, consistente con doc previo — no drift, es estado real). Load avg 9–10. 25 VMs/LXCs (15 qemu + 10 LXC; 1 stopped: `win-development`).
- **hades → ceph**: sigue retornando `RADOS object not found` localmente (esperado: hades no tiene config Ceph, solo bridge configurado).
- **truenas**: sigue como VM (qemu/145) en hades. Riesgo turtles persiste.
- **Cluster heartbeat**: los 6 nodos responden a SSH + sudo -n + wrapper. Inventario refrescable a demanda a partir de ahora.

### Paso 5 — Documentación actualizada

- `30-resources/aranea/00-index.md` — callout de freshness cambia de ⚠️ a ✅, gaps #1 y #2 marcados cerrados.
- `30-resources/aranea/01-topologia/fechas-captura.md` — agregadas 6 filas nuevas (TS `20260630_194423`), 6 filas previas marcadas `superseded`. Resumen de drift refleja 0 días.
- `30-resources/aranea/01-topologia/nodo-hades.md` — header `Capturado:` y footer `Source files` apuntan a la captura nueva.
- `20-areas/Aranea.md` — frontmatter `updated` + `status_detail` actualizados; sección "Estado actual" lista gaps cerrados.
- Skill nueva: `aranea_agent_ro_inventory_refresh` (en `~/.hermes/profiles/ariadna/skills/`).
- Memory (perfil ariadna): nota de TS más reciente.

## Cierre

| Gap | Estado anterior | Estado actual |
|---|---|---|
| #1 NOPASSWD no aplicado | abierto | ✅ cerrado 2026-06-30 |
| #2 Inventario drift 2d | abierto (bloqueado por #1) | ✅ cerrado 2026-06-30 |

**Cierre del ticket**: condicional según check del owner sobre el output del reporte (sección "Reporte por nodo" en el chat). **Los 6 nodos críticos pasaron** los 4 niveles (SSH / sudo -n / wrapper / `all`), por lo que el gap se considera cerrado bajo el criterio "todos los nodos críticos pasan".

## Riesgos residuales

- Wrapper `agent-read` lee estado pero **no escribe** — sin riesgo de mutación.
- El sudoers NO concede root shell ni ALL — el blast radius está limitado al wrapper.
- Los archivos crudos previos (`*_20260628_211812.txt`) **no se eliminan**: sirven como histórico de auditoría.

## Follow-ups (no parte de este ticket)

- Gap #3-4 → ticket `2026-06-30-011` (storage audit + backups).
- Gap #5 → `02-servicios/misc-otros` § pendientes (detalle por VM/LXC con snapshots).
- Considerar refrescar inventario de forma programada (cron mensual) usando la skill `aranea_agent_ro_inventory_refresh`.
