---
type: change_log
schema_version: 1
scope: session
created: "2026-09-17"
updated: "2026-09-17"
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

# 2026-09-17-f05c-cert-f04-01-rerun-blocked

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (nuevo delta fechado `2026-09-17 — Ejecución CERT-F04-01 RERUN` con veredicto `BLOCKED` + actualización de `Estado de entrada` + reemplazo de `Próxima tarea única recomendada para NORMAL`; sin cambio de clases A/B/C y sin ejecutar ningún gate posterior)
  - `80-agents/journal/agent-runs/2026-09-17-zcode-glm-5.3-flash-f05c-cert-f04-01-rerun.md` (creado)

## Motivo

- Ejecución de la misión `F05C-CERT-F04-01-RERUN`: re-ejecutar desde cero CERT-F04-01 sobre release `0.2.99` / `49fce32` con UNA campaña física real de identidades nuevas, observada hasta terminalización, tras la corrección C1 y la release/rollout C2. Prohibiciones respetadas: sin fixes source, sin publicar release, sin editar ETCD, sin segundo watcher, sin DB writes manuales, sin gates posteriores, sin tocar f03cert.

## Fuentes usadas

- [[Echo + Echo Forge — Deferred Certification Backlog]] (deltas EXEC/C1/C2 del día, reglas frozen del re-run) y [[Echo Forge — F-04 Magic allocation, version seal and handoff]] (contrato F-04).
- Handoffs: agent-runs EXEC (`2026-09-17-zcode-glm-5.3-flash-f05c-cert-f04-01-exec`), C1 y C2; pre-submit/evidence del intento anterior en `~/aranea/work/f04-cert-f04-01-exec/`; runbooks `aranea-ssh-mcp` (contrato evidence publisher) y `aranea-mcp-capability-plane`.
- Source @ checkout `~/go/src/github.com/xKoRx/symphony` (branch `codex/f05-release-prep` @ `49fce32`, dirty operacional preservado): validador scratch del input, `strategy_version.go` / `artifact_compiler.go` / `mt5_compile_persist_activity.go` / `intake.go` (diagnóstico del defecto).
- ETCD `aranea-etcd-ro` (config efectiva watcher); SSH operator (Zeus staging+watcher+worker log, Hera/Kronos flota, `mt5-kronos-operator` read-only para evidence publisher, job dir y `metaeditor.log`); CLI Temporal local (pre-autorizado por R1) para describe/show/list; `sqx-flowkit` y `release-authority` contra producción.

## Resolución aplicada

- Re-run físico ejecutado completo: request_id `cert-f04-01-rerun-20260917T211613Z-0997458c`, CampaignRef `a470e565-5fbc-45b3-908d-f55c3cb4b70e`, WaveRef `forge-a470e565-…-w000001`, FlowRunRef `efc4ac0c-545b-47bd-8750-79d9abf1e4a3`; funnel completo hasta final_reretester, **allocation durable Magic V1 `26090011004`** con read-back (allocator continuó desde su estado durable real), trade list + MQ5 durables y **compile físico Windows attempt 1 SUCCESS con MetaEditor real** (`0 errors, 1 warnings, 4707 ms`; EX5 176730 B `c698331c…`; log 15984 B `96360c81…`) — la regresión del fix C1 quedó demostrada físicamente.
- Veredicto **`CERT-F04-01 = BLOCKED`**: `mt5_compile_persist_v1` falló `CONTRACT_CONFLICT artifact_integrity: compile log does not report 0 errors` con compile limpio — segundo defecto determinístico de la release: `VerifyCompiledArtifactForSeal` (`strategy_version.go:62`) matchea el log crudo UTF-16LE de MetaEditor sin `normalizeCompileLog` (el gate local del compile sí normaliza). FlowRun/Campaign `FAILED/WAVE_FLOW_RUN_FAILED` 21:35:32Z, terminal por sí mismo, sin cancelación, flota drenada.
- Sin PASS y sin gates posteriores; la evidencia de golden (CERT-F04-02) no aplica al no haber PASS.

## Validación

- El flujo fue el objeto de certificación: todas las mutaciones de pipeline (intake, uploads, filas PG, allocation) provienen del flujo productivo mismo; cero mutaciones fuera del pipeline (el run se terminalizó solo; no hubo cancel).
- Unicidad demostrada (exactamente 1 campaña/FlowRun/wave); identidades todas nuevas y disjuntas del run CANCELLED; CFX reutilizados con hashes byte-exactos verificados; sin bypass ni evidencia sintética.
- Vault: sólo delta documental; repos sin cambios (dirty operacional preservado); ETCD sin writes; sin secretos registrados.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales sensibles, memoria interna ni secretos

## Rollback

- Revertir el delta fechado, `Estado de entrada` y `Próxima tarea` en el backlog y borrar este log + el agent-run. El estado físico del run es durable por diseño (allocation write-once, workflows FAILED terminales) y no es objeto de rollback.
