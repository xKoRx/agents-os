---
type: change_log
schema_version: 1
created: "2026-09-25"
area: "[[Echo]]"
project: "[[Echo — Producto Integrado]]"
entities:
  - "[[Echo — Producto Integrado]]"
  - "[[Echo + Echo Forge — Environment Contract]]"
related:
  - "[[Echo — Production Operational Audit 2026-09-21]]"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - area/echo
---

# 2026-09-25 — Rollout Echo PROD (D1+D3 @ 372af59a)

## Cambios

- **[[Echo — Producto Integrado]] §Estado y realidad:** nueva entrada "Rollout PROD (25-09)" con veredicto `PROD_ROLLOUT_PARTIAL_EXECUTED`, alcance ejecutado (BD + ETCD), paquete pendiente de ventana owner y deuda.
- (Registro del lado Agents-OS, memoria auto del agente y workspace externo `~/aranea/work/echo-prod-rollout-20260925/`: db/ — RUNBOOK-DB, precheck, migraciones 061–065 verbatim @ origin/master, suplementos, postcheck, backup 157.310 filas; release/ — 4 binarios `372af59a` `vcs.modified=false` + SHA256SUMS, front dist, hasura CLI+metadata+merge aditivo+apply, RUNBOOK-DEPLOY.md, RUNBOOK-HASURA.md, BUILD.md, tokens env mode 600; tool/ — helper Go efímero.)

## Efectos físicos en PROD (verificados 2026-09-25)

- PG `echo` @ .220: 13 objetos nuevos (identity/quarantine/canonical A0/canonical_operations+history_state/lab_curves), CHECK plataforma ampliado a MetaTrader5/MetaTrader4, GRANT UPDATE echo_user en 4 tablas identity, vistas 061 recreadas (contenidos idénticos a backup), 14 `mig061_backup_*` retenidos.
- ETCD `/echo/production/`: 5 keys nuevas (4 tokens auth + CORS). Ninguna key existente modificada.
- Sin cambios en binarios, nginx, Hasura metadata ni Kafka (deploy pendiente ventana owner).

## No tocado / gates vigentes

- `xKoRx/echo` repo: cero commits nuevos (worktree en workspace externo; master local `3596fc48` sigue divergido).
- Deuda `4aad647b` sin fusionar: `go test ./...` sigue prohibido contra ETCD real.
- Trading/dinero real: sin cambio de comportamiento (binarios viejos sobre esquema aditivo compatible).
