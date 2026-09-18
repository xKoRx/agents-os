---
type: change_log
schema_version: 1
scope: session
created: "2026-09-18"
updated: "2026-09-18"
area: "[[Echo]]"
project: "[[Echo + Echo Forge — Deferred Certification Backlog]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge]]"
  - "[[Echo]]"
related:
  - "[[Echo Forge — F-04 Magic allocation, version seal and handoff]]"
  - "[[AGENT-PLATFORM - MCP Access Plane]]"
aliases: []
confidence: verified
source_session:
source_feedbacks: []
share_scope: local
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/change-log
  - scope/session
---

# 2026-09-17-f05c-cert-f04-01-rerun3-blocked

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (nuevo delta fechado `2026-09-17/18 — Ejecución CERT-F04-01 RERUN-3` con veredicto `BLOCKED` + actualización de `Estado de entrada` + reemplazo de `Próxima tarea única recomendada para NORMAL`; sin cambio de clases A/B/C y sin ejecutar ningún gate posterior)
  - `80-agents/journal/agent-runs/2026-09-17-zcode-glm-5.3-flash-f05c-cert-f04-01-rerun3.md` (creado)

## Motivo

- Ejecución de la misión `F05C-CERT-F04-01-RERUN-3`: re-ejecutar desde cero CERT-F04-01 sobre release `0.2.100` / `a440ac4…` con UNA campaña física real de identidades todas nuevas, observada hasta terminalización, tras los fixes C1+C3+C4. Prohibiciones respetadas: sin fixes source, sin publicar release, sin editar ETCD, sin ampliar Access Plane, sin segundo watcher, sin DB writes manuales, sin gates posteriores, sin tocar f03cert.

## Fuentes usadas

- [[Echo + Echo Forge — Deferred Certification Backlog]] (deltas EXEC/C1/C2/C3/C4/RERUN del día, reglas frozen del re-run) y [[Echo Forge — F-04 Magic allocation, version seal and handoff]] (contrato F-04).
- Handoffs: agent-runs EXEC/C1/C2/C3/C4/RERUN; workdirs previos `~/aranea/work/f04-cert-f04-01-{exec,rerun}/` (input template, CFX y hashes).
- Source @ checkout `~/go/src/github.com/xKoRx/symphony` (branch `codex/f05-release-prep` @ `a440ac4…`, dirty operacional preservado): validador scratch recompilado, `report/types.go`+`report/parse.go` (diagnóstico del defecto), diffs `49fce32..a440ac4` (equivalencia de contratos de input).
- ETCD `aranea-etcd-ro` (config efectiva watcher + timeouts MT5); SSH `aranea-ssh` (Zeus staging+watcher+worker log, Hera/Kronos flota, `mt5-kronos-operator` read-only para evidence publisher, job dir y `metaeditor.log`); `sqx-flowkit` y `release-authority` contra producción; lectura read-only del historial Temporal `sqx-prop` con binario scratch local (`/tmp/thist/`, canal equivalente al CLI pre-autorizado por R1) ante el outage del MCP SSH y la ausencia de CLI.

## Resolución aplicada

- Re-run físico ejecutado completo: request_id `cert-f04-01-rerun3-20260917T231606Z-68edd951`, CampaignRef `1fc62ab5-c859-4b46-ac7f-4e0f0375e74f`, WaveRef `forge-1fc62ab5-…-w000001`, FlowRunRef `b6a1edea-ba20-4a23-8cde-0201ee22e8f0`; funnel completo sin FAILED → Decision V2 (cohort 1) → **allocation durable Magic V1 `26090011005`** (forge-live, allocation_ref `sha256:1d44410f…`, assigned 23:36:42.522Z; allocator continuó desde su estado durable real) → Apply COMPLETED → final reretester → MQ5 export durable → **compile físico Windows attempt 1 SUCCESS** (MetaEditor `0 errors, 1 warnings, 4625 ms`; EX5 176726→176426 B `6d667d70…`; log 15984 B `bdf5e5b4…`) → **`mt5_compile_persist_v1` COMPLETED** (EvaluationRef `sha256:6d1a37ce…`; cero `persistence_deadline_required`, cero `artifact_integrity` falso — fixes C1+C3+C4 validados físicamente) → **backtest físico real 54 min** (HTM 13074872 B `21917e14…`, logs tester/agent durables) → **`mt5_reconcile_v1` FAIL non-retryable `mt5 report: build not supported: build=6182`** → FlowRun/Campaign `FAILED/WAVE_FLOW_RUN_FAILED` 00:32:23.578Z.
- Veredicto **`CERT-F04-01 = BLOCKED`**: tercer defecto determinístico (entorno×contrato) — el terminal MT5 de worker-kronos auto-actualizó a build 6182, fuera de la allow-list fail-closed `{6090, 6140, 6180}` de `mt5-report.v1` (`sqx/adapters/mt5/report/types.go:13` @ `a440ac4`). Sin seal ni handoff (`strategy_versions: []`, `handoffs: []`); cero finalistas NO por filtros auténticos.
- Terminación: campaign FAILED terminal por sí misma (`flow_run_seal` COMPLETED), 0 workflows Running en `sqx-prop`, 0 procesos MT5 físicos en worker-kronos (01:00Z), worker singleton PID 5496 sin restart con pollers, Zeus sin watchers/screens, f03cert intacto, allocations 001–005 write-once permanecen.
- Limitaciones registradas: MinIO-RO 403 `sqx-strategies` (bytes no descargables; identidades por resultados durables), Mongo RO `-32003`, SSH MCP outage ~1 h (superado), Loki/OTLP sin ingestión symphony, Temporal RO MCP en namespace distinto de `sqx-prop`.

## Validación

- El flujo fue el objeto de certificación: todas las mutaciones de pipeline (intake, uploads, filas PG, allocation) provienen del flujo productivo mismo; cero mutaciones fuera del pipeline (el run se terminalizó solo; no hubo cancel).
- Unicidad demostrada (exactamente 1 campaña/FlowRun/wave); identidades todas nuevas y disjuntas de EXEC/RERUN; CFX reutilizados con hashes byte-exactos verificados in-situ; input validado contra `a440ac4` con negativos; sin bypass ni evidencia sintética.
- Vault: sólo delta documental; repos sin cambios (dirty operacional preservado); ETCD sin writes; sin secretos registrados.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales sensibles, memoria interna ni secretos

## Rollback

- Revertir el delta fechado, `Estado de entrada` y `Próxima tarea` en el backlog y borrar este log + el agent-run. El estado físico del run es durable por diseño (allocation write-once, workflows FAILED terminales) y no es objeto de rollback.
