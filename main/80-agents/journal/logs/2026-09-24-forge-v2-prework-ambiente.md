---
type: change_log
schema_version: 1
scope: session
created: "2026-09-24"
updated: "2026-09-24"
area: "[[Echo]]"
project: "[[Echo Forge — Operación Real V2]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge — Operación Real V2]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
related: []
aliases: []
confidence: verified
source_session:
source_feedbacks:
  - "[[2026-09-24-forge-v2-prework-feedback]]"
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-24 — Forge V2 prework ambiente: veredicto y AS-BUILT

## Cambios

- **`30-resources/aranea/07-integration/Echo + Echo Forge — Environment Contract.md`:** nueva sección §5.8 (prework Forge DEV Daedalus 2026-09-24: corrección ETCD watcher DEV con rollback, runtime watcher/worker DEV, smoke de ambiente dispatch+cancel+cleanup, SQX DEV BLOCKED por decisión owner, herramientas desechables) y fila de reconciliación §7 actualizada para SQX DEV (`BLOCKED por decisión owner`; MT5 `DEFERRED_UNTIL_C6`).
- **`10-projects/Echo Forge — Operación Real V2/Echo Forge — Operación Real V2.md`:** bullet de estado con veredicto `PREWORK_BLOCKED` + blocker único (distribución y licencia SQX DEV en Daedalus) y entrada de bitácora 2026-09-24.
- **`80-agents/journal/agent-runs/2026-09-24-zcode-glm53-forge-v2-prework-ambiente.md`:** nuevo run (ZCode×GLM-5.3-Flash, outcome partial, verificación física).
- **`80-agents/journal/feedback/session/2026-09-24-forge-v2-prework-feedback.md`:** feedback de fricción (default PROD en `run_watcher.sh`, inconsistencia ETCD DEV corregida, helpers desechables por MCP etcd RO, Mongo MCP con sesión rota).

## Infraestructura (fuera del vault, con rollback)

- ETCD DEV: `/sqx-watcher/development/temporal/namespace` `sqx`→`sqx-dev` (rev 58981) y `/sqx-watcher/development/sqx/task_queue` `sqx-dev-queue`→`sqx-main-queue` (rev 58982). Rollback: restaurar `sqx` / `sqx-dev-queue`.
- MinIO DEV `sqx-strategies`: 4 objetos bajo `wave_prework_smoke_20260924/` creados y borrados (neto 0).
- PG DEV `trading_systems_test`: filas `sqx.flow_runs` (1) y `sqx.configs` (1) del smoke creadas y borradas (neto 0).
- Temporal `sqx-dev`: workflow smoke cancelado; cierra al primer arranque de un worker DEV (residuo benigno documentado).
- Daedalus: binarios/logs del smoke en `~/aranea/work/forge-prework-20260924/` (conservados como evidencia); procesos watcher/worker detenidos; repo `xKoRx/symphony` sin delta (`d9032ff8`).
