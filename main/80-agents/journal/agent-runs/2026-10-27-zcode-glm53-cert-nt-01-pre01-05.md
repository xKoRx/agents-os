---
type: agent_run
schema_version: 1
scope: session
created: "2026-10-27"
updated: "2026-10-27"
area: "[[Echo]]"
project: "[[Echo Futures — Runtime Pools]]"
application:
entities: []
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3-Flash
model_source: session
task_type: implementation
task_complexity: high
outcome: success
verification: full
evaluator: agent
user_rework: none
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — CERT-NT-01 resolución PRE-01..05 (pre-ventana, SHA 5a0cf62f)

## Trabajo

- **Objetivo:** mandato 2026-10-27 (Fase 0 ACCEPTED, OWNER_WINDOW_REQUEST=NOT_READY): resolver únicamente la preparación pre-ventana — PRE-01 roster desde `Runtime.ExpectedRoster()` con correspondencia de estado real, PRE-02 relay SFTP con staging inocuo, PRE-04 reconciliación P1/P2/P6 con corte portable único, PRE-03 topic como provisioning planificado; UNA tarjeta final; prohibido reiniciar Flink DEV / FX / PROD / Ninja / cuentas.
- **Cambios en source** (`5a0cf62f`, FF push a `origin/feature/ef-runtime-pools`, ls-remote verificado): guard de migración fail-closed con evidencia económica real (dispatcher `EconomicEvidence` sobre los 7 owners, sonda json.RawMessage, marker `legacy_state_present`, split de summaries, `Validate` exigente); subcomando `expected-roster` (ParseConfigSnapshot + ExpectedRoster, stdout JSON puro = `--roster-file` del seal); `seal --cut-kind savepoint` (join contra último savepoint COMPLETED, id sellado = sonda `sp-<n>`, copia self-contained, manifest `cut_kind`); seam REST `LatestCompletedSavepoint(+Time)`; usage doc completo (D-5).
- **Evidencia DEV:** roster derivado contra ETCD (RO): 8 keys ACTIVE (`417d77d1…`) — 0 keys `operation` proyectadas (config sin bindings) y 3 provider_rules (CERTNT01-SIM01/02/03) sin evidencia de journal ⇒ clasificación honesta pre-declarada en la tarjeta (5 esperadas `present` por journal/boot previo, 3 `absent` admisibles; divergencia ⇒ NO-GO G8). Release reconstruido `5a0cf62f` (core `3f044d4e…`, control `411e55cc…`, sonda `c84ca495…`), sin repoint.

## Verificación

- Tests nuevos con oráculo (present/absent/fail-closed/registro exhaustivo/Validate; seal savepoint refusals+happy path; expected-roster fail-closed): PASS. Suites dirigidas + `runtimecontrol` + `recovery` + `futuresruntime` + `cmd`: PASS. `go build` módulo v3 completo: PASS.
- **Fallos PREEXISTENTES demostrados en base limpia `4a041e6c`** (git stash + re-run, NO introducidos): `TestFEFBW4CapacityCampaign` (timeout >4 min) y `TestEconomicMinimumCoreTypedConfigAndProtectionParity` (paridad OHLC LIVE/BACKTEST). Declarados al Manager; la suite de `functions` NO está limpia en base.
- **Limitaciones honestas:** (a) la sonda nunca leyó bytes REALES de savepoint (formato SavepointV3 vs checkpoint fixture) — la lectura física es P1 en ventana, fail-closed STOP; el trigger de savepoint de prueba pre-ventana no está autorizado ("savepoint activo con impacto" reservado a la ventana); (b) PRE-02 (relay staging) y PRE-05 (docker inspect binds JM/TM) NO ejecutadas: el servidor MCP `aranea-ssh` expiró a mitad de sesión ("Session not found or expired", incluidas sftp-* y list-connections) y su reinicialización es acción del host — receta exacta y oracles documentados como G0 de la tarjeta.

## Rework

- Ninguno del mandato. Tarjeta única reescrita ([[WINDOW-CARD-PRD6]], readback `be5094c0…`, schema 0 errores) con la decisión Manager verbatim + resolución por enmienda + solicitud de UNA autorización Owner condicionada a G0; planner, change_log y este run actualizados.
