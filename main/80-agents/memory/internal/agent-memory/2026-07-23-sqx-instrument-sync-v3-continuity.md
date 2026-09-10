---
type: agent_memory
scope: session
created: 2026-07-23
updated: 2026-09-09
index_priority: never
memory_state: archived
project: "[[Symphony]]"
entities:
  - "[[Symphony]]"
  - "[[sqx-instrument-sync]]"
related: []
load_policy: manual
indexable: false
tags:
  - kind/internal-memory
  - scope/session
  - area/symphony
---

# Continuidad — sqx-instrument-sync v3.0.0

## Qué quedó hecho

- Skill `sqx-instrument-sync` reescrita a v3.0.0.
- Script `~/sync_user_data_zeus.sh` en Zeus (hash SHA-256 `767b4a1bf03740c7f747962e8ee4877a89c656cf7b1ee17a133a43651b2dc502`).
- Fuente de verdad en repo: `.agents/skills/sqx-instrument-sync/scripts/sync_user_data_zeus.sh`.
- Sync ahora incluye DBs H2 (`data_futures.h2.db`, `data_stock.h2.db`, `data.db`), versiones, `connections.txt`, `History/` y cualquier subcarpeta futura. Solo excluye `*.lock` y `*.tmp`.
- `--delete --delete-excluded` activado para garantizar identidad total.
- Subcomandos: `audit`, `sync`, `verify`, `manifest`, `diff`. Lock con flock. Preflight completo. Logs rotados máx 10.
- Probado en cluster real 2026-07-23: Hera/Kronos divergían en H2, sync los replicó, 3 hosts con hash maestro `1383ab9e...` (27 entradas), idempotente.

## Atención / no olvidar

- **Condición operacional**: el sqcli de SQX debe estar caído durante el sync (pisar H2 vivos corrompe estado). El proceso `symphony` worker sí puede seguir activo.
- **No usar `--delete-excluded` con las exclusiones runtime viejas** (H2): eso borra los runtime files en destino. Solo tiene sentido con las exclusiones mínimas actuales (`*.lock`, `*.tmp`).
- La cobertura del manifest es TODO `~/sqx/user/data`. No hardcodedar subcarpetas; cualquier nueva subcarpeta queda automáticamente cubierta.
- El `RESUMEN_POR_SUBCARPETA` actual no cuenta bien archivos en la raíz (sin `/`). Es cosmético; el `FAIL_*` individual sí funciona.

## Próximos pasos posibles

- Commit + PR del cambio siguiendo Conventional Commits (`feat(sqx-instrument-sync): ...`).
- Revisar si conviene programar el sync en cron dentro de ventana de mantenimiento.
- Considerar promover la distinción "symphony worker ≠ sqcli" a un learning/known-error si vuelve a causar fricción.
