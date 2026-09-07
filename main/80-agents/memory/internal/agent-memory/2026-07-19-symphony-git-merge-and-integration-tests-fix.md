---
type: agent_memory
schema_version: 1
scope: project
created: 2026-07-19
updated: 2026-09-03
area: "[[Personal]]"
project: "[[symphony]]"
load_policy: when_project_loaded
indexable: true
index_priority: medium
tags:
  - agent/internal
  - kind/agent-memory
  - project/symphony
  - scope/project
---

# Symphony Git Merge & Integration Tests Fix

## Continuidad
- The user ran `git pull` on local `master`, causing a divergence with `origin/master` (both branches had 1 commit that was not on the other).
- Unstaged local changes in `list_selected_strategies.go`, `config.json`, and `manifest.json` prevented a clean merge.
- The new SDK `GenerateObjectKey` implementation now includes `RunID` in the format string. When `RunID` is empty (as in the integration tests), it outputs a path with double slashes `//` (e.g. `wave_1/xauusd/l_h1/test4/v1//01_builder/`), which makes MinIO list operations fail with `unsupported characters`.

## Actions taken
1. Committed local changes in `master` to preserve the robust strategy name matching changes.
2. Merged `origin/master` into `master` using standard git merge.
3. Resolved merge conflicts in:
   - `deploy/manifest.json` (aligned with official `0.1.124` remote version).
   - `input/example/config.json` (preserved local test config `example_flow_4`).
   - `sqx/activities/worker/evaluate_wfm.go`, `generate_report.go`, `robust_activity.go` (kept both strict RequestID checks and the new heartbeat instrumentation from remote).
4. Fixed the integration tests (`internal/tasks/project_listing_integration_test.go` and `integration/project_listing_test.go`) by replacing double slashes `//` in generated prefixes with a single slash `/` to avoid MinIO listing errors.
5. Successfully ran all test suites (workflows, activities, integration, and deployer).
6. Pushed the merged changes to origin master.
7. Updated the codebase graph with `graphify-personal update .`.

## Señales de carga

- Cargar sólo al trabajar con [[symphony]] y cuando coincidan divergencias Git, tests de integración o paths con `RunID` vacío.

## Próxima acción

- Verificar el estado vigente del repositorio y de los tests antes de reutilizar esta evidencia histórica.
