---
type: agent_run
schema_version: 1
scope: session
created: "2026-10-17"
updated: "2026-10-17"
area: "[[Aranea]]"
project: "[[Echo Forge — Operación Real V2]]"
application:
entities: []
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM 5.3 (account:zai-individual-coding-plan/GLM-5.3-Flash, host-reported)
model_source: host
task_type: implementation
task_complexity: high
outcome: success
verification: passed
evaluator: agent
user_rework: owner-correction-mid-session
source_session:
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — FLOW_EXAMPLE_2 E2E flujo único Builder→MT5 (2026-10-16/17)

## Tarea

Mandato Owner one-shot (corregido en curso): UN `config.json` con UN `GenericSQXWorkflow` raíz — builder→overview→classification→early ranking→selection→GROUP interno `source.type=ranking_snapshot` (retester+optimizer+evaluate_wfm+select_robust_run)→apply→final reretester→tradelist/report→MQ5→EX5→MT5 (NDX_SQX H1 2026.01.01–2026.10.12 model 4)→fidelity→ranking final→promoción; resultados por tipo lógico (máx 5); sin cancelación por tiempo; cierre Agents-OS.

## Ejecución y cambios

- Spec único wave 9 SPEC_VALID (11 tasks), CFX Owner byte-exactos 4/4. Despachos: w8 (FlowRun `c6a18689`, 22:43:16Z del 16) y w9 (FlowRun `8248f7fa`, 02:07:41Z del 17) — mismo JSON salvo identidad.
- **Fix de código (único)**: `b77af11` — alias canónico `usatechidxusd_dukascopy_utc02→ndx` en `canonical_scope.go` + regresión (UTC02→ndx, UTC03→""). Causa: w8 falló no-retryable en `mt5_score_shadow_v1` ("normalized trade scope mismatch") tras MT5 30/30; el dataset del Owner no estaba en la tabla de alias. Push a master; release **0.2.147** (`69a6cd7`), rollout 3/3 verificado por SSH MCP (proceso+SHA `0e4c9908…` byte-exacto).
- Diagnóstico adicional sin fix: el "defecto resetBatchKeepBindings vs ranking_snapshot" de wave-6 NO aplica a la topología del owner (el reset sólo rompe cuando hay un group hermano ANTES del GROUP con source); y un FlowRun sellado FAILED no puede llegar a COMPLETED vía reset Temporal (`flow_run_seal` rechaza la transición — contrato correcto, verificado empíricamente con el reset `63d29c7e`).
- Monitoreo completo sin cancelar por tiempo (2h09m30s w9); verificación de polling corregida tras falso hang (export overview single-thread 25-60 min por diseño; la observación del owner de 1 core/1.8% era correcta).

## Verificación

- PG `sqx.flow_runs` `8248f7fa` **COMPLETED** (04:17:11Z); 11 stage families 100% COMPLETED (30/30 en las particionadas); 30 decisiones robust SELECTED; mágicas durables 26100091054..083; decisión FLOW `finalist_promotion` 2.0.0 STRUCTURAL_PROMOTED.
- Mongo: SelectionSnapshot `sha256:d15af7f9` (30/729 exclusiones), 6 RankingSnapshots early, **ranking final `sha256:de770a6d`** (score_descending.v1), 30 scores mt5-score.v1 COMPUTED.
- Entregables vault: `10-projects/Echo Forge — Operación Real V2/artifacts/FLOW_EXAMPLE_2_E2E_SINGLE_FLOW/` (certificación, configs, TASKS-EVIDENCE.csv, FINALISTS-BY-LOGICAL-TYPE.csv, EXECUTION-REFS.md, CORRECTIONS.md, SHA256SUMS.txt, cfx/).

## Rework

Corrección del Owner a mitad de sesión revocó el diseño A/B del mandato original; se reimplementó como flujo único sin pérdida de evidencia. Ningún rework de código tras el fix b77af11.
