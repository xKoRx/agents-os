---
type: agent_run
schema_version: 1
scope: session
created: "2026-08-22"
updated: "2026-08-22"
area: "[[Echo Forge]]"
project: "Echo Forge - Arquitectura de Datos y Migración de Persistencia"
application: "[[Symphony]]"
entities: []
related: []
aliases: []
agent_surface: "[[ZCode]]"
agent_model: "deepseek-v4-flash-0731"
model_source: host
task_type: coding
task_complexity: high
outcome: complete
verification: pass
evaluator: agent
user_rework: unknown
source_session: DURABLE-EARLY-RANKING-GROUP-CURRENT-BATCH-KEY-FIX-NORMAL
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-run
  - scope/session
---

# Agent Run — 2026-08-22-zcode-deepseek-v4-flash-early-ranking-group-batch-key-fix

## Trabajo

- **Objetivo:** Clasificar el blocker físico de Attempt 10 (`BLOCKED_BY_DURABLE_EARLY_RANKING_GROUP_CURRENT_BATCH_KEY`) y corregir la semántica de carrier del exporter top-level sin tocar ranking ni pipeline durable.
- **Alcance atribuible a esta combinación superficie×modelo:** Diagnóstico A/B/C con test de reproducción sobre el workflow real, fix de carrier semantics en el top-level de `GenericSQXWorkflow`, regressions unit+E2E del grupo ranking_snapshot, vet, build, commit y push.
- **Artefactos afectados:** `sqx/workflows/generic_workflow.go`, `sqx/workflows/mt5_identity.go` y `sqx/workflows/early_ranking_group_cutover_test.go`.

## Evidencia

- **Validaciones ejecutadas:** `go test ./sqx/workflows -count=1` (paquete completo), tests nuevos `TestEarlyRankingGroup_BuilderExporterPreservesDurableCohort`, `TestApplyExporterOutput_PreservesDurableSelectionCohort` y `TestAssignProjectOutput_StillReplacesKeysForNormalProject`; `go vet ./sqx/workflows`; `go build ./sqx/cmd/sqx-worker ./sqx/cmd/sqx-flowkit ./sqx/cmd/sqx-watcher ./sqx/cmd/sqx-mt5-worker`; `git diff --check`.
- **Resultado observable:** Root cause A confirmado en test TDD: el `overview_exporter` top-level caía en la rama `project` y `assignProjectOutput(current, out)` reemplazaba `current.Keys` por las keys del exporter (batch no vacío de metadata) preservando `StrategyArtifacts` (los 20 carriers Builder), por lo que `exactEarlyRankingArtifacts` fallaba con `artifact key ... is not an exact current batch key` exactamente como en Attempt 10. Fix: rama exporter usa `applyExporterOutput` que preserva Keys/StrategyArtifacts/RankingSnapshots/ClassificationSnapshots y solo agrega ArtifactResults; projects normales siguen usando `assignProjectOutput`. Commit `6f9988396aec3092613566fae8a12555b01081d8` pusheado con `HEAD == origin/master`.
- **Limitaciones de la evidencia:** No se ejecutó SQX, release ni E2E físico por mandato de la sesión; el contracto de la colisión se probó con el flujo de workflow real y mocks de activities sobre el `config.json` del Example Flow.

## Evaluación

%% Scores opcionales 1–5: agregar al frontmatter sólo cuando exista evidencia suficiente. Si son autoevaluados, conservar evaluator: agent. %%

- **Correctness:**
- **Autonomy:**
- **Efficiency:**
- **Tool use:**
- **Overall:**

## Resultado

- **Outcome:** PASS / CLOSED; root cause A confirmado con TDD (rojo→verde); commit `6f9988396aec3092613566fae8a12555b01081d8` pushed y `HEAD == origin/master`.
- **Rework posterior:** unknown; NEXT EXACT es `FINAL-DURABLE-E2E-DEPLOY-RERUN-NORMAL`.
- **Aprendizaje para comparar herramientas:** El guard `artifact.Key ∈ current.Keys` de `exactEarlyRankingArtifacts` es correcto y no se tocó; el defecto estaba en el carrier top-level: un exporter no es una selección y no debe reemplazar el cohort durable que alimenta el ranking_snapshot group.