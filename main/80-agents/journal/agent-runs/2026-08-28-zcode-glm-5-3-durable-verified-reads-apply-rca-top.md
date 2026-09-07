---
type: agent_run
schema_version: 1
scope: session
created: "2026-08-28"
updated: "2026-08-28"
area: "[[Echo Forge]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[xKoRx/symphony]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
related:
  - "[[2026-08-28-durable-verified-reads-apply-reconciliation-rca]]"
aliases: []
agent_surface: "[[ZCode]]"
agent_model: GLM-5.3
model_source: builtin:zai-coding-plan/GLM-5.3
task_type: review
task_complexity: high
outcome: success
verification: verified
evaluator: agent
user_rework: unknown
source_session: DURABLE-ARTIFACT-VERIFIED-READS-APPLY-RCA-TOP
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-08-28-zcode-glm-5-3-durable-verified-reads-apply-rca-top

## Trabajo

- **Objetivo:** RCA/DESIGN read-only en `xKoRx/symphony` @ `5e93c7cda3f4fcc825f3939a951247cd4e63fec2` (== origin/master): root cause del blocker Apply reconcile (fabricación de `DurableArtifactRef` desde storage), state machine, crash matrix C0–C11, comparación Builder, capability StageExecutionResult, determinismo del productor, opciones de recovery authority y diseño exacto del fix, sin modificar código.
- **Alcance atribuible a esta combinación superficie×modelo:** lectura parent del núcleo Apply (activity, storage reconcile, write-once, control plane, binding evidence/contract, workflow wrapper, wiring) + 2 subagentes general-purpose paralelos (determinismo del productor con inspección física de muestra `.sqx`; mapeo StageExecutionResult/Builder recovery) + síntesis de opciones A–E + decisión congelada + persistencia Agents OS completa.
- **Artefactos afectados:** ninguno del repo (read-only, foreign dirty preservado); en vault: decisión symphony, checkpoint de proyecto, known-error update, change_log, agent-run, continuidad interna, feedback.

## Evidencia

- **Validaciones ejecutadas:** HEAD == baseline == origin/master; fabricación confirmada `apply_selected_run.go:26-50` con único caller productivo `durable_apply_selected_run.go:318`; `putObjectIfAbsentAndReconcile`/`reconcileExactObject` (`write_once.go:36-87`) ya implementan verify-objeto-vs-ref-caller; `CompleteStageExecution` replay-safe `stage_execution.go:140-156`; `stage_execution_results` links-only sellado en tx de completion (`:171-182`, migrations/001:253-259); `EvaluationRef` determinista sin artifact (`evidence.go:78,101-108`); veredicto determinismo BYTE_DETERMINISTIC_NOT_PROVEN (ZIP/JAR sqcli con timestamps DOS + precedente Retester +2 bytes; experimento físico especificado, `/home/kor/sqx` ausente en dev).
- **Resultado observable:** PASS/CLOSED. Autoridad recomendada: registro PG `stage_producer_outputs` INSERT-only pre-put + short-circuit por `EvaluationRef` determinista post-Evidence + eliminación de `ReconcileApplySelectedRun` del path durable; crash matrix C0–C11 cerrada fail-closed sin dependencia de determinismo; change surface ~9-10 archivos; test plan 15 casos; NEXT EXACT DURABLE-ARTIFACT-VERIFIED-READS-APPLY-CORRECTION-NORMAL.
- **Limitaciones de la evidencia:** determinismo no comprobable desde dev (requiere worker host con sqcli + project.cfx real); sin E2E ni tests (sesión read-only); riesgo de interleave zombie-writer tras UNKNOWN_COMMIT documentado como ventana rara² fail-closed.

## Evaluación

- **Correctness:** 5
- **Autonomy:** 5
- **Efficiency:** 5
- **Tool use:** 5
- **Overall:** 5

## Resultado

- **Outcome:** PASS / CLOSED; NEXT EXACT DURABLE-ARTIFACT-VERIFIED-READS-APPLY-CORRECTION-NORMAL.
- **Rework posterior:** unknown.
- **Aprendizaje para comparar herramientas:** mismo patrón eficiente que RCA anteriores: 2 scouts paralelos (~3-5 min) + verificación parent de los hechos que decidían el diseño; el discriminador clave esta vez fue leer directamente las primitivas write-once y el flujo de completion del control plane, que ya contenían ~70% de la solución (verify-vs-caller-ref + replay-safe complete); el análisis de ordenings (record-before-put vs record-after-put vs evidence-first) fue trabajo parent puro de razonamiento distribuido.
