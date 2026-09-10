---
type: agent_memory
schema_version: 1
scope: session
created: 2026-08-10
updated: 2026-09-09
memory_state: archived
area: "[[Personal]]"
project:
application:
entities: []
related: []
confidence: medium
load_policy: manual
indexable: false
index_priority: never
tags:
  - kind/agent-memory
  - scope/session
---

## Continuidad

# Internal Memory - MinIO Path Unification Success (2026-07-13)

## Status
- **Entity**: `Symphony` (SQX Worker / Watcher)
- **Objective**: Align and unify MinIO path generation under `BuildMinIOPath` dynamic helper.
- **Success**: Code modified across all activities (`import_metadata`, `robust_activity`, `generate_report`, and `list_strategies`) and storage adapter, successfully compiled, unit-tested, built, and deployed to Zeus (`0.1.113`). E2E pipeline run of `example_flow` completed successfully.

## Architecture & Paths
- Canonical helper: `BuildMinIOPath(ctx, wave, instrument, direction, timeframe, strategy, version, requestID, folder, filename)`
  - Standardizes the key as: `wave_<wave>/<instrument>/<direction>_<timeframe>/<strategy>/<version>/<requestID>/<folder>/<filename>`
  - Capitalization: `NDX` instrument maps to lowercase `ndx`, etc.
  - Automatically prepends `wave_` to numeric waves.

## Fix details in 0.1.113
- Activity `list_strategies.go` was using a hardcoded formatting string for prefix without `requestID`, causing it to query `wave_1/ndx/l_h1/example_flow/v24/03_optimizer/` (which returned 0 strategies).
- Refactored `list_strategies.go` to use `BuildMinIOPath` and pass `req.RequestID`.

## Active Daemons on Local & Zeus
- **Local Watcher**: Running on macOS via screen (`watcher`, pid 82780). Watches `input/` folder, uploads `.cfx` to unified MinIO paths, and schedules workflows.
- **Local Deployer**: Running on macOS via screen (`deployer`, pid 82084). Watches `./deploy` and uploads releases to `deploy` bucket.
- **Zeus Worker**: Running on Linux via systemd (`symphony-worker`, version `0.1.113`). Actively executing workflows and using the new unified pathing structure.


## Señales de carga

- Cargar sólo cuando la entidad o síntoma coincida con esta continuidad.
