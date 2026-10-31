---
type: agent_memory
schema_version: 1
scope: project
created: "2026-10-31"
updated: "2026-10-31"
area: "[[Personal]]"
project: "[[AGENTS OS]]"
entities:
  - "[[AGENTS OS]]"
related: []
aliases:
  - daedalus disk pressure checkpoint
  - checkpoint disco daedalus 20261031
confidence: high
memory_state: active
continuity_key: host/daedalus-disk-pressure
supersedes:
superseded_by:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-memory
  - agent/internal
  - checkpoint
---

# daedalus 20261031 — checkpoint: presión de disco recurrente

## Patrón recurrente (2ª vez confirmada)

- La raíz (`/`, 146G) se llena por crecimiento sin tope de: `~/.cache/go-build` (19G esta vez), artefactos/log de sesiones ZCode en `~/.zcode/cli/`, y snapshots de lab con packs git duplicados en `~/Documents/Codex/<fecha>/the-lab-*/work/shot*/{A..F}` (cada shot copia el pack de 1,5G de symphony).
- `/srv/echo-work` (147G) acumula snapshots datados de lab/rescate: `lab-v4-shot4-20261023` (56G), `archive-20261023` (23G), `rescate-20261014-rootdisk` (7,2G) — pendiente decidir purga con el usuario.
- syslog llegó a 898M; journal 1G. Vacuum y `apt clean` requieren sudo interactivo (no hay sudo sin contraseña para el agente).

## Orden de limpieza validado (2026-10-31: 99%→84%, 2,7G→23G libres)

1. `rm -rf ~/.cache/go-build` (regenerable; `go clean -cache` puede fallar con "directory not empty", usar rm directo).
2. Podar `~/.zcode/cli/artifacts` con `-mtime +7` (~1,4G) y logs diarios viejos en `~/.zcode/cli/log`.
3. Pedir al usuario: `sudo journalctl --vacuum-size=200M`, `sudo apt-get clean`, y decidir purga de snapshots datados en `/srv/echo-work` y `~/Documents/Codex`.

## Pendiente

- Decisión del usuario sobre `lab-v4-shot4-20261023` (56G) y `archive-20261023` (23G) en `/srv/echo-work` — pueden ser datos activos de Echo Forge; no borrar sin confirmación.
- Gap: no existe runbook de limpieza de daedalus; candidato a crearlo si la presión se repite.
