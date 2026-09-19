---
type: change_log
schema_version: 1
scope: session
created: "2026-09-19"
updated: "2026-09-19"
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

# 2026-09-19-f05c-cert-f04-01-rerun4-blocked

## Cambio

- **Tipo:** updated
- **Archivo(s):**
  - `10-projects/Echo/agentes/Echo + Echo Forge — Deferred Certification Backlog.md` (nuevo delta fechado `2026-09-19 — Ejecución CERT-F04-01 RERUN-4 (build 6182 en producción)` con veredicto `BLOCKED` + actualización de `Estado de entrada` + actualización de `Próxima tarea única recomendada para NORMAL`; CERT-F04-01 pasa a `BLOCKED` por cuarto defecto determinístico)
  - `10-projects/Echo Forge/Echo Forge.md` (entrada de bitácora 2026-09-19)
  - `80-agents/journal/agent-runs/2026-09-19-zcode-glm-5.3-flash-f05c-cert-f04-01-rerun4-blocked.md` (creado)
  - Flota/repositorio — campaña real `8a6b7dda…` sobre release `0.2.101` (allocations `26090011006–009` y artifacts durables en `sqx-strategies`; efectos documentados aquí, sin cambios de código)

## Motivo

- Ejecución de la misión `F05C-CERT-F04-01-RERUN-4` (Physical End-to-End Certification): demostrar que `0.2.101`/`c1d24c1…` procesa una ejecución MT5 real desde cero, genera un reporte auténtico build 6182 y lo ingiere con el parser certificado. Una única campaña con identidades todas nuevas; sin cambios de código, sin releases, sin repetir C5/C6/C6R/C7.

## Fuentes usadas

- Mandato maestro F05C-CERT-F04-01-RERUN-4 (texto de la misión).
- Backlog deferred (estado C7 `BLOCKED / READY TO RERUN-4`), receta física canónica del delta RERUN-3 (input JSON + CFX + patrón watcher pre-stageado), contrato [[Echo Forge — F-04 Magic allocation, version seal and handoff]].
- `release-authority` (`sqx-release-authority.v1`), `sqx-flowkit` read models, evidencia Windows vía `AraneaEvidencePublish` + `mt5-kronos-operator` read-only (contrato [[aranea-ssh-mcp]]), historial Temporal `sqx-prop` vía scratch `/tmp/thist`, lectura de artefactos vía `aranea-minio-ro` (HeadObject + presign GET).

## Resolución aplicada

- G0 PASS: release `0.2.101 CONSISTENT/EXACT_MATCH`; flota 4/4 con SHA instalado == artifact; Windows singleton PID 19436 `f5a8baa1…` EXACT, PENDING.next MISSING; `MT5_PROCS=0`; 0 workflows Running.
- G1 PASS: input RERUN-4 = receta RERUN-3 con sólo 4 campos de identidad cambiados (diff exacto demostrado); VALIDATION_OK contra structs `c1d24c1` con negativos 3/3; CFX byte-exactos in-situ; allocation 005 read-back intacta; plan persistido antes del dispatch.
- G2 PASS (dispatch único): primer arranque del watcher (23:22:55Z, input no pre-stageado) fue cerrado por el guard legacy a los 10 s sin consumir el archivo — resultado incierto resuelto según contrato (0 campañas, 0 workflows, SHA del input intacto) y re-dispatch con la MISMA identidad y archivo pre-stageado; pipeline 6/6 a las 23:24:44Z; exactamente 1 campaña nueva `8a6b7dda…` RUNNING.
- G3: funnel completo; allocations durables `26090011006–009` (allocator continuó desde 005, CAS con UNIQUE por StrategyRef); 4 compiles físicos Windows `0 errors, 1 warnings` (metaeditor.log 23:36:55–23:37:09Z); 4 backtests físicos secuenciales COMPLETED (df63bab0 23:37→00:24 ~47 min; últimos hasta ~03:15Z); invariante `<= 1` ejecución física respetada.
- G4: 4/4 HTM byte-verificados (HeadObject/presign GET por identidad autorizada; SHA256 local sobre bytes reales == durable: `c586785f…`/5195458, `ead914ab…`/12460992, `4e69d470…`/7816270, `f403fc42…`/3392778). Cambio material registrado: la capability MinIO RO ya lee `sqx-strategies` (la concesión owner aplicó tras C6) — el blocker `READ_ONLY_ARTIFACT_FETCH_REQUIRED` de C5A/C5B queda cerrado. Nota: presign de HTM 3 y 4 emitido por error desde `aranea-minio-rw` (GET-only, sin mutación).
- G5: `mt5_reconcile_v1` ×4 COMPLETED en producción con build 6182 aceptado (`structural_identity: MATCH`, evaluation_refs durables, cero `BuildNotSupported`/`StructureUnknown`/`CrosscheckFailed`); parse local con el parser certificado sobre los 4 HTM → 7/7 crosschecks PASS por estrategia.
- Fallo terminal: `forge_seal_handoff_v1` CONTRACT_CONFLICT non-retryable `member 107f1da5… source Evaluation is project@sqx-final-reretester.v1, apply authority required` (evento 492, 03:15:56.217Z). Causa primera anclada en source @ `c1d24c1`: el assembler toma `carrier.EvaluationRef` como ApplyEvaluationRef (`generic_workflow.go:1026`) pero la validación del fan-out del final reretester exige que ese campo sea reemplazado (`generic_workflow.go:1837`), mientras el gate exige authority `apply_selected_run` (`forge_seal_handoff.go:251`) — contradicción estructural, primera vez ejercitada físicamente (los runs previos murieron antes del seal). `strategy_versions: []`, `handoffs: []` ×4; campaign FAILED terminal por sí misma; 0 workflows Running post-run.
- Veredicto `CERT_F04_01_BLOCKED` (cuarto defecto determinístico). Fixes C1+C3+C4+6182 quedaron validados físicamente en producción. No se lanzó RERUN-5; no se declaró NO_GO global.

## Validación

- Toda la evidencia es durable y referenciada: identidades/etapas en `~/aranea/work/f04-cert-f04-01-rerun4/` (pre-submit-record, submit-record, evidence-summary, artifacts/ con los 4 HTM auténticos + hashes, evidence-notes del canal de observabilidad); read-backs por flowkit/Temporal/MinIO citados por timestamp y evento.
- Historial Temporal `sqx-prop`: FlowRun `sqx-main-v1-0ce058d1…`/`01a0b6d6-2f50-7c43-97bb-57d6bf1cc20c` eventos 492 (ActivityTaskFailed tipado) y 497 (WorkflowExecutionFailed); flow_run_seal COMPLETED sella el terminal.

## Compartibilidad

- **Scope:** local
- **Redacción revisada:** sin identidad, paths locales de credenciales ni secretos; URLs presignadas efímeras no registradas.

## Rollback

- La campaña terminó FAILED por sí misma (sin cancel externa, sin takeover, sin drenaje manual); las allocations `26090011006–009` son write-once y permanecen (reserva sin uso válida); los artifacts durables de `sqx-strategies` se preservan; vault append-only (revertir = eliminar el delta RERUN-4, la bitácora, este log y el agent-run). No hay cambios de código ni de release que revertir.
