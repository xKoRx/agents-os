---
type: agent_run
schema_version: 1
scope: session
created: "2026-08-22"
updated: "2026-08-22"
area: "[[Echo]]"
project: "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
application: "[[echo-forge]]"
entities:
  - "[[Echo Forge - Arquitectura de Datos y Migración de Persistencia]]"
  - "[[Echo Forge]]"
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: ox-alpha
model_source: system
task_type: coding
task_complexity: medium
outcome: success
verification: focused_tests_full_packages_vet_build_matrix_git_diff_check_and_push_passed
evaluator: agent
user_rework: unknown
source_session: "SESSION DURABLE-EARLY-RANKING-GROUP-EXACT-ARTIFACT-KEY-IDENTITY-FIX-NORMAL"
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — Durable Builder Exact Keys Fix Normal

## Trabajo

- **Objetivo:** cerrar el blocker del Attempt 11 — `projectOutputKeys` degradaba las `UploadedKeys` del durable Builder a basenames, así `StratBatch.Keys` dejó de contener `StrategyArtifact.Key` y el guard `exactEarlyRankingArtifacts` falló closed en el group `02_retester`.
- **Alcance atribuible a esta combinación superficie×modelo:** fix mínimo en `projectOutputKeys` (durable Builder pasa a exact MinIO object key vía `durableProjectTask`), actualización del comentario obsoleto, reemplazo del test con expectativa basename obsoleta y dos regressiones nuevas (production key del Attempt 11 y set membership de 20 keys).
- **Artefactos afectados:** 2 archivos exactos en `xKoRx/symphony/sqx/activities/worker` (`project_activity.go`, `project_activity_durable_test.go`); foreign dirty preservado; checkpoint append-only en la bitácora del proyecto canónico.

## Evidencia

- **Validaciones ejecutadas:** tests focalizados (`ProjectOutputKeys|DurableBuilder`; `EarlyRankingGroup|ApplyExporterOutput|AssignProjectOutput`), paquetes completos worker + workflows, `go vet` ambos, build host de los 4 binaries y matriz cruzada (linux/amd64 worker+watcher, windows/amd64 MT5 worker, CGO-disabled, ENV=production), `git diff --check`, commit/push y verificación HEAD remoto.
- **Resultado observable:** PASS en todas; commit `e8f8274ab08a94a8596270ffc9c4056a0d44904b` publicado en `origin/master` con HEAD == origin/master.
- **Limitaciones de la evidencia:** no se ejecutó deploy ni Attempt 12 por alcance explícito; el fixture `phase4_performance.json` fue reescrito como side-effect de los tests y se preservó como foreign dirty.

## Evaluación

%% Scores opcionales 1–5: agregar al frontmatter sólo cuando exista evidencia suficiente. Si son autoevaluados, conservar evaluator: agent. %%

- **Correctness:**
- **Autonomy:**
- **Efficiency:**
- **Tool use:**
- **Overall:**

## Resultado

- **Outcome:** success; commit `fix: keep durable builder output keys exact` publicado en `origin/master`.
- **Rework posterior:** unknown.
- **Aprendizaje para comparar herramientas:** el helper existente `durableProjectTask` ya expresaba el OR de los cuatro predicados durables; el fix completo fue de una línea más comentario, y la cobertura vieja del Builder (basename) quedó documentada como expectativa obsoleta en el propio test.
